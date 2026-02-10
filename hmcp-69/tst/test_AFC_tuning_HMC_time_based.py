"""Test Module Description:
    Test module for HSD time-based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.12.4
    - Pytest version >= 8.0.1
"""

from .__main__ import *
from os import makedirs
import copy


ffi = cffi.FFI()
SKIP_TEST = False
MAKE_HTML = True
if not SKIP_TEST:
    _FILENAME = "Behavioral_Test_tuning.xlsx"

    _MODULE_PATH = Path(__file__).parent
    _BASE_DIR = _MODULE_PATH / "time_based_data"

    _DIR_PATH_INPUT_DATA = _BASE_DIR / "input_data"
    _DIR_PATH_OUTPUT_DATA = _BASE_DIR / "output_data"
    _DIR_PATH_REFERENCE_DATA = _BASE_DIR / "reference_data"


    Ab = 1.2
    Dp = 1.5
    Tbgn = 490
    Tlim = 560
    default_alpha = 1.02
    alpha_delta = 0.01
    alpha_max = 1.08
    UNLOCK = "unlock"
    DEFAULT = "default"

    def parse_AFC_logging_test_data(file_path):
        test_cases = []
        for row in iter_file(file_path):
            try:
                PackSOC = int(float(row["PackSOC"]))
                PackSOC_DR = int(row["PackSOC_DR"])
                PackCurr = int(float(row["PackCurr"]))
                PackCurr_DR = int(row["PackCurr_DR"])
                try:
                    CellVolts = [
                        int(float(item)) for item in ast.literal_eval(row["SEVolts"])
                    ]
                except TypeError:
                    CellVolts = [int(row["SEVolts"])]

                try:
                    CellVolts_DR = [
                        int(item) for item in ast.literal_eval(row["SEVolts_DR"])
                    ]
                except TypeError:
                    CellVolts_DR = [int(row["SEVolts_DR"])]
                try:
                    MinTempSnsr = int(float(row["MinTempSnsr"]))
                    MaxTempSnsr = int(float(row["MaxTempSnsr"]))
                except ValueError:
                    MinTempSnsr = p_MinTempSnsr
                    MaxTempSnsr = p_MaxTempSnsr
                p_MinTempSnsr = MinTempSnsr
                p_MaxTempSnsr = MaxTempSnsr

                MinTempSnsr_DR = int(row["MinTempSnsr_DR"])

                MaxTempSnsr_DR = int(row["MaxTempSnsr_DR"])

                TempSnsrs = [MaxTempSnsr for _ in range(18)]
                TempSnsrs_DR = [1 for _ in range(18)]

                try:
                    ChgPackCapcty = int(float(row["ChgPackCapcty"]))
                except ValueError:
                    ChgPackCapcty = 0
                ChgPackCapcty_DR = int(row["ChgPackCapcty_DR"])

                battery_state = row["Battery_State"]
                EVSEChgStatus = int(row["EVSEChgStatus"])

                Apply_Tuning = int(row["ApplyTuning"])
                Tuning_Type = int(row["TuningType"])
                Applied_Alpha = int(row["AppliedAlpha"])
                Expected_Alpha = int(row["ExpectedAlpha"])

            except KeyError:
                print("Key not found in input data")
            except ValueError:
                continue

            # Format data for parametrized test
            test_case = {
                "Inputs": {
                    "PackSOC": PackSOC,
                    "PackSOC_DR": PackSOC_DR,
                    "PackCurr": PackCurr,
                    "PackCurr_DR": PackCurr_DR,
                    "CellVolts": CellVolts,
                    "CellVolts_DR": CellVolts_DR,
                    "TempSnsrs": TempSnsrs,
                    "TempSnsrs_DR": TempSnsrs_DR,
                    "MinTempSnsr": MinTempSnsr,
                    "MinTempSnsr_DR": MinTempSnsr_DR,
                    "MaxTempSnsr": MaxTempSnsr,
                    "MaxTempSnsr_DR": MaxTempSnsr_DR,
                    "ChgPackCapcty": ChgPackCapcty,
                    "ChgPackCapcty_DR": ChgPackCapcty_DR,
                    "battery_state": battery_state,
                    "EVSEChgStatus": EVSEChgStatus,
                    "Apply_Tuning": Apply_Tuning,
                    "Tuning_Type": Tuning_Type,
                    "Applied_Alpha": Applied_Alpha,
                    "Expected_Alpha": Expected_Alpha,
                },
                "Expected": {},
            }

            test_cases.append(test_case)

        return test_cases


    def test_AFC_tuning_behavioral(
        lib: Any):
        csv_filename = _DIR_PATH_INPUT_DATA / _FILENAME
        print(csv_filename)
        ofile_path = _DIR_PATH_OUTPUT_DATA
        output_file_name = _FILENAME.replace("input", "output")
        output_file_path = ofile_path / output_file_name
        makedirs(output_file_path, exist_ok=True)

        all_time_steps = parse_AFC_logging_test_data(csv_filename)
        # Initialize results
        results = {
            "PackCurr": [],
            "PackCurr_DR": [],
            "SEVolts": [],
            "SEVolts_DR": [],
            "TempSnsrs": [],
            "TempSnsrs_DR": [],
            "MinTempSnsr": [],
            "MinTempSnsr_DR": [],
            "MaxTempSnsr": [],
            "MaxTempSnsr_DR": [],
            "ChgPackCapcty": [],
            "ChgPackCapcty_DR": [],
            "PackSOC": [],
            "PackSOC_DR": [],
            "Battery_State": [],
            "EVSEChgStatus": [],
            " ": [],
            "WarningFlags (dec)": [],
            "WarningFlags (bin)": [],
            "ChgPackCurr": [],
            "ChgPackVolt": [],
            "ChgCompletionFlag": [],
            "NVM_Warnings": [],
            "Ne_Cnt_ChargeCycleNum": [],
            "Ne_Cnt_SocIncrAccum": [],
            "Ne_b_EarlyAgingWarning": [],
            "Ne_b_AbnormalAging": [],
            "Ne_b_ExtremeAging": [],
            "Na_Cnt_HighestCPVCorrIdx": [],
            "Ab": [],
            "Dp": [],
            "Tbgn": [],
            "Tlim": [],
            "Alpha": [],
        }
        # Initial log buffer
        process_log_buffer(lib, 0, True)
        for i in range(192):
            cpv_idx = f"NVM_CPVCorrIdx[{i}]"
            results[cpv_idx] = []

        row_count = 2
        # logger.info(f"Warning Flags: {results["WarningFlags (dec)"]}")
        # logger.info(f"Early Flags: {lib.AFC_Track.Ne_b_EarlyAgingWarning}")
        # logger.info(f"Abnormal Flags: {lib.AFC_Track.Ne_b_AbnormalAging}")
        # logger.info(f"Extreme Flags: {lib.AFC_Track.Ne_b_ExtremeAging}")

        current_alpha = default_alpha
        expected_alpha = default_alpha
        count = 0
        final_output = []
        test_alpha = 1.02
        for i in range(5):
            for each_time_step in all_time_steps:
                # save current Na_Cnt_HighestCPVCorrIdx to compare later if this is changed.
                previous_Na_Cnt_HighestCPVCorrIdx = list(
                    lib.AFC_Track.Na_Cnt_HighestCPVCorrIdx
                )
                prev_log_buffer_elements_count = get_num_elements_from_buffer(lib)

                output_file_name = csv_filename.replace("input", "output").replace(
                    ".xlsx", f"_tuning_{row_count}.csv"
                )
                # logger.info(f"output_file_name: {output_file_name}")
                # Setup Variables
                # ------------------------------------------------
                lib.VeAPI_I_PackCurr = each_time_step["Inputs"]["PackCurr"]
                lib.VeAPI_b_PackCurr_DR = each_time_step["Inputs"]["PackCurr_DR"]
                lib.VaAPI_U_SEVolts = each_time_step["Inputs"]["CellVolts"]
                lib.VaAPI_b_SEVolts_DR = each_time_step["Inputs"]["CellVolts_DR"]
                lib.VaAPI_T_TempSnsrs = each_time_step["Inputs"]["TempSnsrs"]
                lib.VaAPI_b_TempSnsrs_DR = each_time_step["Inputs"]["TempSnsrs_DR"]
                lib.VeAPI_T_MinTempSnsr = each_time_step["Inputs"]["MinTempSnsr"]
                lib.VeAPI_b_MinTempSnsr_DR = each_time_step["Inputs"]["MinTempSnsr_DR"]
                lib.VeAPI_T_MaxTempSnsr = each_time_step["Inputs"]["MaxTempSnsr"]
                lib.VeAPI_b_MaxTempSnsr_DR = each_time_step["Inputs"]["MaxTempSnsr_DR"]
                lib.VeAPI_Cap_ChgPackCapcty = each_time_step["Inputs"]["ChgPackCapcty"]
                lib.VeAPI_b_ChgPackCapcty_DR = each_time_step["Inputs"][
                    "ChgPackCapcty_DR"
                ]
                lib.VeAPI_Pct_PackSOC = each_time_step["Inputs"]["PackSOC"]
                lib.VeAPI_b_PackSOC_DR = each_time_step["Inputs"]["PackSOC_DR"]
                battery_state = each_time_step["Inputs"]["battery_state"]
                lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]

                tuning_type = each_time_step["Inputs"]["TuningType"]
                tuning_set = each_time_step["Inputs"]["ApplyTuning"]

                lib.VeAPI_e_TuningState = 1
                lib.VeAPI_e_Ab = Ab
                lib.VeAPI_e_Dp = Dp
                lib.VeAPI_e_Tbgn = Tbgn
                lib.VeAPI_e_Tlim = Tlim

                # ToDo Apply tuning on if charging status is True
                if (
                    lib.VeAPI_b_EVSEChgStatus == 0
                    and battery_state != "Charging"
                    and tuning_set
                ):
                    # Ab, Dp, Tbgn, Tlim are global variables.
                    lib.VeAPI_e_TuningState = 1
                    if tuning_type == 0:
                        lib.VeAPI_e_Alpha = default_alpha
                        expected_alpha = default_alpha
                    else:
                        lib.VeAPI_e_Alpha = current_alpha
                        expected_alpha = lib.VeAPI_e_Alpha
                        current_alpha += alpha_delta
                        if current_alpha > alpha_max:
                            current_alpha = default_alpha
                elif battery_state == "Charging" and tuning_set:
                    lib.VeAPI_e_TuningState = 1
                    if tuning_type == 0:
                        lib.VeAPI_e_Alpha = default_alpha
                        expected_alpha = default_alpha
                    else:
                        lib.VeAPI_e_Alpha = current_alpha
                        expected_alpha = lib.VeAPI_e_Alpha
                        current_alpha += alpha_delta
                        if current_alpha > alpha_max:
                            current_alpha = default_alpha

                # Run Function
                # ------------------------------------------------
                lib.Qnovo_AFC(
                    ffi.addressof(lib, "AFC_Inputs"), ffi.addressof(lib, "AFC_Outputs")
                )

                if tuning_applied:
                    tuning_applied = False
                    print("New Tuning Applied")
                    expected = lib.AFC_HiTempDerate.Ke_k_Alpha
                    actual = current_alpha
                    compare_result(expected, actual, rtol=1e-2)
                else:
                    print("Default Tuning Applied")
                    expected = lib.AFC_HiTempDerate.Ke_k_Alpha
                    actual = test_alpha
                    compare_result(expected, actual, rtol=1e-2)
                    tuning_turn = DEFAULT

                # Record results
                results["PackCurr"].append(lib.VeAPI_I_PackCurr)
                results["PackCurr_DR"].append(lib.VeAPI_b_PackCurr_DR)
                results["SEVolts"].append(lib_array_to_list(lib.VaAPI_U_SEVolts))
                results["SEVolts_DR"].append(lib_array_to_list(lib.VaAPI_b_SEVolts_DR))
                results["TempSnsrs"].append(lib_array_to_list(lib.VaAPI_T_TempSnsrs))
                results["TempSnsrs_DR"].append(
                    lib_array_to_list(lib.VaAPI_b_TempSnsrs_DR)
                )
                results["MinTempSnsr"].append(lib.VeAPI_T_MinTempSnsr)
                results["MinTempSnsr_DR"].append(lib.VeAPI_b_MinTempSnsr_DR)
                results["MaxTempSnsr"].append(lib.VeAPI_T_MaxTempSnsr)
                results["MaxTempSnsr_DR"].append(lib.VeAPI_b_MaxTempSnsr_DR)
                results["ChgPackCapcty"].append(lib.VeAPI_Cap_ChgPackCapcty)
                results["ChgPackCapcty_DR"].append(lib.VeAPI_b_ChgPackCapcty_DR)
                results["PackSOC"].append(lib.VeAPI_Pct_PackSOC)
                results["PackSOC_DR"].append(lib.VeAPI_b_PackSOC_DR)
                results["Battery_State"].append(battery_state)
                results["EVSEChgStatus"].append(lib.VeAPI_b_EVSEChgStatus)
                results[" "].append("")  # Divider between input and output
                results["WarningFlags (dec)"].append(lib.VeAFC_e_WarningFlags)
                results["WarningFlags (bin)"].append(
                    format(lib.VeAFC_e_WarningFlags, "032b")
                )
                results["ChgPackCurr"].append(lib.VeAFC_I_ChgPackCurr)
                results["ChgPackVolt"].append(lib.VeAFC_U_ChgPackVolt)
                results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)
                results["Ne_Cnt_ChargeCycleNum"].append(
                    lib.AFC_Track.Ne_Cnt_ChargeCycleNum
                )
                results["Ne_Cnt_SocIncrAccum"].append(lib.AFC_Track.Ne_Cnt_SocIncrAccum)
                results["Ne_b_EarlyAgingWarning"].append(
                    lib.AFC_Outputs.EarlyWarningAgingFlag[0]
                )
                results["Ne_b_AbnormalAging"].append(
                    lib.AFC_Outputs.AbnormalAgingFlag[0]
                )
                results["Ne_b_ExtremeAging"].append(lib.AFC_Outputs.ExtremeAgingFlag[0])
                results["Na_Cnt_HighestCPVCorrIdx"].append(
                    list(lib.AFC_Track.Na_Cnt_HighestCPVCorrIdx)
                )

                results["Ab"].append(lib.VeAPI_e_Ab)
                results["Dp"].append(lib.VeAPI_e_Dp)
                results["Tbgn"].append(lib.VeAPI_e_Tbgn)
                results["Tlim"].append(lib.VeAPI_e_Tlim)
                results["Alpha"].append(lib.VeAPI_e_Alpha)

                cpvidx_result = [
                    lib_array_to_list(i) for i in lib.AFC_Track.Nt_Cnt_CPVCorrIdx
                ]
                for j in range(192):
                    cpv_idx = f"NVM_CPVCorrIdx[{j}]"
                    results[cpv_idx] = cpvidx_result[j]

                final_output.append(copy.deepcopy(results))
                for key in results:
                    results[key] = []

                row_count += 1
                count += 1
                if count == 10000:
                    write_output_to_csv(final_output, output_file_name)
                    final_output = []
                    count = 0

                # check previous_Na_Cnt_HighestCPVCorrIdx
                log_buffer_elements_count = get_num_elements_from_buffer(lib)
                if previous_Na_Cnt_HighestCPVCorrIdx != list(
                    lib.AFC_Track.Na_Cnt_HighestCPVCorrIdx
                ):
                    # check if log added
                    if log_buffer_elements_count <= prev_log_buffer_elements_count:
                        print("Log not inserted when index incremented")
                        assert (
                            log_buffer_elements_count > prev_log_buffer_elements_count
                        )
                    else:
                        print("Log inserted")
                else:
                    if log_buffer_elements_count != prev_log_buffer_elements_count:
                        print(
                            f"Previous Indexes:{previous_Na_Cnt_HighestCPVCorrIdx}"
                        )
                        print(
                            f" Current Indexes: {list(lib.AFC_Track.Na_Cnt_HighestCPVCorrIdx)}"
                        )
                        print(
                            f"Present Stage: {lib.AFC_Calc.Ve_Cnt_PresentStgNum}"
                        )
                        print(f"Previous count: {prev_log_buffer_elements_count}")
                        print(f"Current count: {log_buffer_elements_count}")
                    assert log_buffer_elements_count == prev_log_buffer_elements_count

            if count > 0:
                output_file_name = csv_filename.replace("input", "output").replace(
                    ".xlsx", f"_tuning_{row_count}.csv"
                )
                write_output_to_csv(final_output, output_file_name)
                count = 0
                final_output = []

        print(f"Iteration : {row_count}")
        # logger.info(f"Warning Flags: {results["WarningFlags (dec)"]}")
        # logger.info(f"Early Flags: {lib.AFC_Outputs.EarlyWarningAgingFlag[0]}")
        # logger.info(f"Abnormal Flags: {lib.AFC_Outputs.AbnormalAgingFlag[0]}")
        # logger.info(f"Extreme Flags: {lib.AFC_Outputs.ExtremeAgingFlag[0]}")
        # logger.info(f"EOL Flags: {lib.AFC_Outputs.EOLFlag[0]}")

        # Parse log buffer and get result data
        result = process_log_buffer(lib, 198, True)
