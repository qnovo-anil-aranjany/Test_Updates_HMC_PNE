"""Test Module Description:
    Test module for AFC Voltage Imbalance time-based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""
from .__main__ import *
import re

_SKIP_TEST = False
_COMPARE_TO_REFERENCE = False

_NUM_SE = 192
_NUM_TEMP = 18

MAKE_HTML = True
if not _SKIP_TEST:
    _MODULE_PATH = Path(__file__).parent
    _BASE_DIR = _MODULE_PATH / "test_data" / "time_based"
    _TEST_SUBDIR = "VoltageImbalanceAnalysis-AfcVehicleFleetTest2024Dataloader-251118-140811"

    _DIR_PATH_INPUT_DATA = _BASE_DIR / "input_data" / _TEST_SUBDIR
    _DIR_PATH_OUTPUT_DATA = _BASE_DIR / "output_data" / _TEST_SUBDIR
    _DIR_PATH_REFERENCE_DATA = _BASE_DIR / "reference_data" / _TEST_SUBDIR

    ffi = cffi.FFI()

    def get_files_from_folder(folder_path):
        """
        Get all CSV or XLSX files from a folder (not mixed).
        """
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")

        csv_files = list(folder.glob("*.csv"))
        xlsx_files = list(folder.glob("*.xlsx"))

        if csv_files and xlsx_files:
            raise ValueError(f"Folder contains both CSV and XLSX files. Cannot mix types.")

        def natural_sort_key(path):
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split(r'(\d+)', path.name)]

        if csv_files:
            csv_files.sort(key=natural_sort_key)
            return [f.name for f in csv_files]
        elif xlsx_files:
            xlsx_files.sort(key=natural_sort_key)
            return [f.name for f in xlsx_files]
        else:
            raise ValueError(f"No CSV or XLSX files found in: {folder_path}")

    def parse_AFC_test_data(file_name, file_path):
        test_cases = []
        for row in iter_file(file_path):

            # Parse Inputs
            Time = int(ast.literal_eval(row["time_s"]))
            PackSOC = 5000
            PackSOC_DR = 1
            PackCurr = 3316
            PackCurr_DR = 1

            try:
                SEVolts = [int(item * 1000) for item in ast.literal_eval(row["se_voltages_V"])]
            except TypeError:
                SEVolts = [int(row["se_voltages_V"])]

            SEVolts_DR = [1] * _NUM_SE

            TempSnsrs = [250] * _NUM_TEMP
            TempSnsrs_DR = [1] * _NUM_TEMP

            MinTempSnsr = 250
            MinTempSnsr_DR = 1

            MaxTempSnsr = 250
            MaxTempSnsr_DR = 1

            ChgPackCapcty = 125800
            ChgPackCapcty_DR = 1

            EVSEChgStatus = row["is_charging"]
            if EVSEChgStatus.lower() == 'true':
                EVSEChgStatus = 1
            elif EVSEChgStatus.lower() == 'false':
                EVSEChgStatus = 0
            else:
                raise ValueError(f"Cannot determine boolean")

            # Parse Expected
            if row["new_se_voltage_z_scores"] == 'null':
                expected_z_score = row["new_se_voltage_z_scores"]
            else:
                expected_z_score = [item for item in ast.literal_eval(row["new_se_voltage_z_scores"])]

            if expected_z_score == 'null':
                expected_voltage_imbalance = 'null'
            else:
                expected_voltage_imbalance = [int(item < -4.0) for item in expected_z_score]

            if row["raw_z_scores__"] == 'null':
                expected_raw_z_score = row["raw_z_scores__"]
            else:
                expected_raw_z_score = [item for item in ast.literal_eval(row["raw_z_scores__"])]

            if row["noise_floor_threshold"] == 'null':
                expected_noise_floor_threshold = row["noise_floor_threshold"]
            else:
                expected_noise_floor_threshold = ast.literal_eval(row["noise_floor_threshold"])

            # Format data for parametrized test
            test_case = {
                "Inputs": {
                    "Filename": file_name,
                    "Time": Time,
                    "PackSOC": PackSOC,
                    "PackSOC_DR": PackSOC_DR,
                    "PackCurr": PackCurr,
                    "PackCurr_DR": PackCurr_DR,
                    "SEVolts": SEVolts,
                    "SEVolts_DR": SEVolts_DR,
                    "TempSnsrs": TempSnsrs,
                    "TempSnsrs_DR": TempSnsrs_DR,
                    "MinTempSnsr": MinTempSnsr,
                    "MinTempSnsr_DR": MinTempSnsr_DR,
                    "MaxTempSnsr": MaxTempSnsr,
                    "MaxTempSnsr_DR": MaxTempSnsr_DR,
                    "ChgPackCapcty": ChgPackCapcty,
                    "ChgPackCapcty_DR": ChgPackCapcty_DR,
                    "EVSEChgStatus": EVSEChgStatus,
                },
                "Expected": {
                    "VoltageImbalance": expected_voltage_imbalance,
                    "Z_Score": expected_raw_z_score,
                    "Noise_Floor_Threshold": expected_noise_floor_threshold,
                },
            }

            test_cases.append(test_case)
        return test_cases

    def record_result(results, lib, input_time, each_time_step):
        """Record a single timestep result. Also initializes results dict if empty."""

        # Define the data to record
        data = {
            "Time": input_time,
            "PackCurr": lib.VeAPI_I_PackCurr,
            "SEVolts": list(lib.VaAPI_U_CellVolts),
            "EVSEChgStatus": lib.VeAPI_b_EVSEChgStatus,
            "Expected_VoltageImbalance": each_time_step["Expected"]["VoltageImbalance"],
            "Expected_Z_Score": each_time_step["Expected"]["Z_Score"],
            "Expected_Noise_Floor_Threshold": each_time_step["Expected"]["Noise_Floor_Threshold"],
            " ": "",  # Divider between input and output
            "Output_VoltageImbalance": list(lib.AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags),
            "QnovoAFC_Log_VoltageImbalance_ZScore": list(lib.QnovoAFC_Log_VoltageImbalance_ZScore),
            "QnovoAFC_Log_VoltageImbalance_Threshold": lib.QnovoAFC_Log_VoltageImbalance_Threshold,
            "ChargeVoltageSums": list(lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums),
            "ChargeVoltageSums_Sort": list(lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort),
            "ExecutionCounter": lib.AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter,
            "SamplingTime": lib.AFC_VM_VoltageImbalance.Ve_t_SamplingTime,
            "AbsoluteVoltageSumDeviations": list(lib.AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations),
            "ReadyForAnalysis": lib.AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis,
        }

        # Append to results
        for key, value in data.items():
            if key not in results:
                results[key] = []  # Initialize if first call
            results[key].append(value)

    _CSV_FILES = get_files_from_folder(_DIR_PATH_INPUT_DATA)

    @pytest.mark.parametrize("csv_filename", _CSV_FILES)
    def test_AFC_time_based_VoltageImbalance(lib: Any, csv_filename: str):

        # Build paths for this specific CSV file
        file_path_input = join(_DIR_PATH_INPUT_DATA, csv_filename)
        file_path_output = join(_DIR_PATH_OUTPUT_DATA, f"processed_{csv_filename}")
        file_path_reference = join(_DIR_PATH_REFERENCE_DATA, f"reference_{csv_filename}")

        # Parse test data
        all_time_steps = parse_AFC_test_data(file_name=csv_filename, file_path=file_path_input)

        # Initialize results
        results = {}

        for each_time_step in all_time_steps:
            # Setup Variables
            # ------------------------------------------------
            input_time = each_time_step["Inputs"]["Time"]
            lib.VeAPI_I_PackCurr = each_time_step["Inputs"]["PackCurr"]
            lib.VeAPI_b_PackCurr_DR = each_time_step["Inputs"]["PackCurr_DR"]
            lib.VaAPI_U_CellVolts = each_time_step["Inputs"]["SEVolts"]
            lib.VaAPI_b_CellVolts_DR = each_time_step["Inputs"]["SEVolts_DR"]
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
            for i in range(10):
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
            record_result(results, lib, input_time, each_time_step)

            # Compare results
            expected_voltage_imbalance = each_time_step["Expected"]["VoltageImbalance"]
            if expected_voltage_imbalance != 'null':
                actual_voltage_imbalance = list(lib.AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags)
                compare_result(expected=expected_voltage_imbalance, actual=actual_voltage_imbalance)

        #write_output_to_excel(results, file_path_output)

        #todo: simulate controller on/off - loss of data

        if _COMPARE_TO_REFERENCE:
            output_data = str(Path(file_path_output).with_suffix('.xlsx'))
            reference_data = str(Path(file_path_reference).with_suffix('.xlsx'))
            if not validate_with_reference_data(output_data, reference_data):
                pytest.fail(
                    "Result data vs Reference data mismatch, see logs for more information"
                )
