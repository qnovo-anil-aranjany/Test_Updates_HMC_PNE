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
    _FILENAME = "Behavioral_Test_20240423_SendToHMC.xlsx"

    _MODULE_PATH = Path(__file__).parent
    _BASE_DIR = _MODULE_PATH / "test_data" / "time_based"

    _DIR_PATH_INPUT_DATA = _BASE_DIR / "input_data"
    _DIR_PATH_OUTPUT_DATA = _BASE_DIR / "output_data"
    _DIR_PATH_REFERENCE_DATA = _BASE_DIR / "reference_data"

    def parse_AFC_logging_test_data(file_path):
        test_cases = []
        i = 0
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
                i += 1

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
                },
                "Expected": {},
            }

            test_cases.append(test_case)
            i += 1
            # if i > 1000:
            #    break

        return test_cases

    def test_AFC_logging_behavioral(lib: Any, setup_parameters):
        """
        Time based tests for logging verification.
        """
        input_file_name = join(dirname(_BASE_DIR), _DIR_PATH_INPUT_DATA, _FILENAME)
        print(f"\nInput file: {input_file_name}")
        output_file_path = dirname(input_file_name.replace("input", "output"))
        makedirs(output_file_path, exist_ok=True)

        all_time_steps = parse_AFC_logging_test_data(input_file_name)
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
        }

        # Initial log buffer
        process_log_buffer(lib, 0, True)
        for i in range(192):
            cpv_idx = f"NVM_CPVCorrIdx[{i}]"
            results[cpv_idx] = []

        row_count = 2
        # logger.info(f"Warning Flags: {results["WarningFlags (dec)"]}")
        print(f"Early Flags: {lib.s_AFC_Track.Ne_b_EarlyAgingWarning}")
        print(f"Abnormal Flags: {lib.s_AFC_Track.Ne_b_AbnormalAging}")
        print(f"Extreme Flags: {lib.s_AFC_Track.Ne_b_ExtremeAging}")

        count = 0
        final_output = []

        for i in range(5):
            for each_time_step in all_time_steps:
                # save current Na_Cnt_HighestCPVCorrIdx to compare later if this is changed.
                previous_Na_Cnt_HighestCPVCorrIdx = list(
                    lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx
                )
                prev_log_buffer_elements_count = get_num_elements_from_buffer(lib)

                output_file_name = input_file_name.replace("input", "output").replace(
                    ".xlsx", f"_{row_count}.csv"
                )
                # logger.info(f"output_file_name: {output_file_name}")
                # Setup Variables
                # ------------------------------------------------
                lib.VeAPI_I_PackCurr = each_time_step["Inputs"]["PackCurr"]
                lib.VeAPI_b_PackCurr_DR = each_time_step["Inputs"]["PackCurr_DR"]
                lib.VaAPI_U_CellVolts = each_time_step["Inputs"]["CellVolts"]
                lib.VaAPI_b_CellVolts_DR = each_time_step["Inputs"]["CellVolts_DR"]
                lib.VaAPI_T_TempSnsrs = each_time_step["Inputs"]["TempSnsrs"]
                lib.VaAPI_b_TempSnsrs_DR = each_time_step["Inputs"]["TempSnsrs_DR"]
                lib.VeAPI_T_MinTempSnsr = each_time_step["Inputs"]["MinTempSnsr"]
                lib.VeAPI_b_MinTempSnsr_DR = each_time_step["Inputs"]["MinTempSnsr_DR"]
                lib.VeAPI_T_MaxTempSnsr = each_time_step["Inputs"]["MaxTempSnsr"]
                lib.VeAPI_b_MaxTempSnsr_DR = each_time_step["Inputs"]["MaxTempSnsr_DR"]
                lib.VeAPI_Cap_ChgPackCapcty = each_time_step["Inputs"]["ChgPackCapcty"]
                lib.VeAPI_b_ChgPackCapcty_DR = each_time_step["Inputs"]["ChgPackCapcty_DR"]
                lib.VeAPI_Pct_PackSOC = each_time_step["Inputs"]["PackSOC"]
                lib.VeAPI_b_PackSOC_DR = each_time_step["Inputs"]["PackSOC_DR"]
                lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]

                # Run Function
                # ------------------------------------------------
                lib.Qnovo_AFC(
                    lib.VaAPI_Cmp_NVMRegion,
                    lib.VaAPI_Cmp_NVMLoggingRegion,
                    lib.VeAPI_I_PackCurr,
                    lib.VeAPI_b_PackCurr_DR,
                    lib.VaAPI_U_CellVolts,
                    lib.VaAPI_b_CellVolts_DR,
                    lib.VaAPI_T_TempSnsrs,
                    lib.VaAPI_b_TempSnsrs_DR,
                    lib.VeAPI_T_MinTempSnsr,
                    lib.VeAPI_b_MinTempSnsr_DR,
                    lib.VeAPI_T_MaxTempSnsr,
                    lib.VeAPI_b_MaxTempSnsr_DR,
                    lib.VeAPI_Cap_ChgPackCapcty,
                    lib.VeAPI_b_ChgPackCapcty_DR,
                    lib.VeAPI_Pct_PackSOC,
                    lib.VeAPI_b_PackSOC_DR,
                    lib.VeAPI_b_EVSEChgStatus,
                    lib.VeAPI_e_EVSEChgLevel,
                    ffi.addressof(lib, "VaAFC_Cmp_CTE_Info"),
                    ffi.addressof(lib, "VeAFC_e_ErrorFlags"),
                    ffi.addressof(lib, "VeAFC_I_ChgPackCurr"),
                    ffi.addressof(lib, "VeAFC_I_MaxReferenceCurr"),
                    ffi.addressof(lib, "VeAFC_I_MitigatedCurr"),
                    ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
                    ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
                    ffi.addressof(lib, "VeAFC_b_ExtremeAgingFlag"),
                    ffi.addressof(lib, "VeAFC_b_AbnormalAgingFlag"),
                    ffi.addressof(lib, "VeAFC_b_EarlyWarningAgingFlag"),
                    ffi.addressof(lib, "VeAFC_b_EOLFlag"),
                    ffi.addressof(lib, "VeAFC_b_SOCImbalanceFlag"),
                )
                # Record results
                results["PackCurr"].append(lib.VeAPI_I_PackCurr)
                results["PackCurr_DR"].append(lib.VeAPI_b_PackCurr_DR)
                results["SEVolts"].append(lib_array_to_list(lib.VaAPI_U_CellVolts))
                results["SEVolts_DR"].append(lib_array_to_list(lib.VaAPI_b_CellVolts_DR))
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
                results["Battery_State"].append(1)
                results["EVSEChgStatus"].append(lib.VeAPI_b_EVSEChgStatus)
                results[" "].append("")  # Divider between input and output
                results["WarningFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
                results["WarningFlags (bin)"].append(
                    format(lib.VeAFC_e_ErrorFlags, "032b")
                )
                results["ChgPackCurr"].append(lib.VeAFC_I_ChgPackCurr)
                results["ChgPackVolt"].append(lib.VeAFC_U_ChgPackVolt)
                results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)
                results["Ne_Cnt_ChargeCycleNum"].append(
                    lib.s_AFC_Track.Ne_Cnt_ChargeCycleNum
                )
                results["Ne_Cnt_SocIncrAccum"].append(lib.s_AFC_Track.Ne_Cnt_SocIncrAccum)
                results["Ne_b_EarlyAgingWarning"].append(
                    lib.VeAFC_b_EarlyWarningAgingFlag
                )
                results["Ne_b_AbnormalAging"].append(
                    lib.VeAFC_b_AbnormalAgingFlag
                )
                results["Ne_b_ExtremeAging"].append(lib.VeAFC_b_ExtremeAgingFlag)
                results["Na_Cnt_HighestCPVCorrIdx"].append(
                    list(lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx)
                )

                cpvidx_result = [
                    lib_array_to_list(i) for i in lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx
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
                    lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx
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
                            f" Current Indexes: {list(lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx)}"
                        )
                        print(
                            f"Present Stage: {lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum}"
                        )
                        print(f"Previous count: {prev_log_buffer_elements_count}")
                        print(f"Current count: {log_buffer_elements_count}")
                    assert log_buffer_elements_count == prev_log_buffer_elements_count

            if count > 0:
                output_file_name = input_file_name.replace("input", "output").replace(
                    ".xlsx", f"_{row_count}.csv"
                )
                write_output_to_csv(final_output, output_file_name)
                count = 0
                final_output = []

        print(f"Iteration : {row_count}")
        # logger.info(f"Warning Flags: {results["WarningFlags (dec)"]}")
        print(f"Early Flags: {lib.VeAFC_b_EarlyWarningAgingFlag}")
        print(f"Abnormal Flags: {lib.VeAFC_b_AbnormalAgingFlag}")
        print(f"Extreme Flags: {lib.VeAFC_b_ExtremeAgingFlag}")
        print(f"EOL Flags: {lib.s_AFC_Track.Ne_b_EOLFlag}")

        # Parse log buffer and get result data
        result = process_log_buffer(lib, 198, True)
        # result.print_buffer()

        # write_output_to_excel(results, output_file_name)
        # logger.info(f"Output file: {output_file_name}")
        """
        res_data = parse_AFC_Behavioral_Test_data(output_file_name)
        logger.info(f"Reference file name : {reference_file_name}")
        ref_data = parse_AFC_Behavioral_Test_data(reference_file_name)
        if not validate_with_refrence_data(res_data, ref_data):
            pytest.fail(
                "Result data vs Reference data mismatch, see logs for exact mismatch"
            )
        """
