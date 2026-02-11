"""Test Module Description:
    Test module for HSD time-based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

import csv

from .main import *

SKIP_TEST = False

if not SKIP_TEST:
    _SUBDIR_NAME = "time_based_data"
    #_FILENAME = "Behavioral_20260122_Guo_RawDataFile_16.csv"
    _FILENAME = "slew_rate_data.csv"

    def parse_AFC_Behavioral_Test_20240423():
        module_path = abspath(__file__)
        dir_path = join(dirname(module_path), _SUBDIR_NAME)
        csv_path = join(dir_path, _FILENAME)

        test_cases = []
        print(csv_path)
        # Open the CSV file
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)

            # Iterate over each row in the CSV
            for row in reader:
                # Get inputs
                test_filename = "Test_01"
                Time = int(row["Time"])
                PackSOC = int(row["PackSOC"])
                PackSOC_DR = int(row["PackSOC_DR"])
                PackCurr = int(row["PackCurr"])
                PackCurr_DR = int(row["PackCurr_DR"])

                try:
                    CellVolts = [
                        int(item) for item in ast.literal_eval(row["CellVolts"])
                    ]
                except TypeError:
                    CellVolts = [int(row["CellVolts"])]

                try:
                    CellVolts_DR = [
                        int(item) for item in ast.literal_eval(row["CellVolts_DR"])
                    ]
                except TypeError:
                    CellVolts_DR = [int(row["CellVolts_DR"])]

                try:
                    TempSnsrs = [
                        int(item) for item in ast.literal_eval(row["TempSnsrs"])
                    ]
                except TypeError:
                    TempSnsrs = [int(row["TempSnsrs"])]

                try:
                    TempSnsrs_DR = [
                        int(item) for item in ast.literal_eval(row["TempSnsrs_DR"])
                    ]
                except TypeError:
                    TempSnsrs_DR = [int(row["TempSnsrs_DR"])]

                MinTempSnsr = int(row["MinTempSnsr"])
                MinTempSnsr_DR = int(row["MinTempSnsr_DR"])

                MaxTempSnsr = int(row["MaxTempSnsr"])
                MaxTempSnsr_DR = int(row["MaxTempSnsr_DR"])

                ChgPackCapcty = int(row["ChgPackCapcty"])
                ChgPackCapcty_DR = int(row["ChgPackCapcty_DR"])

                battery_state = row["EVSEChgStatus"]
                EVSEChgStatus = int(row["EVSEChgStatus"])
                loop = int(row["Loop"])
                Expected_ChgPackCurr = [int(item) for item in ast.literal_eval(row["Expected_ChgPackCurr"])]
                # Format data for parametrized test
                test_case = {
                    "Inputs": {
                        "filename": test_filename,
                        "Time": Time,
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
                        "loop": loop,
                    },
                    "Expected": {
                        "Expected_ChgPackCurr": Expected_ChgPackCurr,
                    },
                }

                test_cases.append(test_case)

        return test_cases

    def test_AFC_Behavioral_Test_20240423(lib):
        all_time_steps = parse_AFC_Behavioral_Test_20240423()

        # Initialize results
        results = {
            "Filename": [],
            "Time": [],
            "PackCurr": [],
            "PackCurr_DR": [],
            "CellVolts": [],
            "CellVolts_DR": [],
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
            "ErrorFlags (dec)": [],
            "ErrorFlags (bin)": [],
            "ChgPackCurr": [],
            "ChgPackVolt": [],
            "ChgCompletionFlag": [],
            "AFC_NVM_MagicNumber": [],
            "AFC_CTE_MagicNumber": [],
            "AFC_CTE_HighestIndex": [],
            "NVM_HighestIndex": [],
            "NVM_HighestIndex2": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (dec)": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (bin)": [],
            "QnovoAFC_LogVar2\nl_InitializedFlag": [],
            "QnovoAFC_LogVar3\nl_ValidSampleFlag": [],
            "QnovoAFC_LogVar4\nl_QNS_State": [],
            "QnovoAFC_LogVar5\nl_PresentStageNum": [],
            "QnovoAFC_LogVar6\nl_HighestIndex": [],
            "QnovoAFC_LogVar9\nl_CPVCorrIdx": [],
            "QnovoAFC_LogVar10\nl_CV_Curr": [],
            "QnovoAFC_LogVar11\nl_ProtocolStgCurr": [],
            "QnovoAFC_LogVar13\nl_ColdCompensatedCurr": [],
            "QnovoAFC_LogVar14\nl_CompensatedVolt": [],
            "QnovoAFC_LogVar15\nl_SampleCellVolt": [],
            "QnovoAFC_LogVar16\nl_RefCellVolt": [],
        }

        for each_time_step in all_time_steps:
            # Setup Variables
            # ------------------------------------------------
            test_filename = each_time_step["Inputs"]["filename"]
            input_time = each_time_step["Inputs"]["Time"]
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
            battery_state = each_time_step["Inputs"]["battery_state"]
            lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]

            print("\n Loop start")
            for i in range(each_time_step["Inputs"]["loop"]):
                # Run Function
                # ------------------------------------------------
                lib.Qnovo_AFC_1000ms(
                    lib.VaAPI_Cmp_NVMRegion,
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
                    ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
                    ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
                )
                print(f"\nlib.VeAFC_I_ChgPackCurr : {lib.VeAFC_I_ChgPackCurr}")
                compare_result(each_time_step["Expected"]["Expected_ChgPackCurr"][i], lib.VeAFC_I_ChgPackCurr)
                # Record results
                results["Filename"].append(test_filename)
                results["Time"].append(input_time)
                results["PackCurr"].append(lib.VeAPI_I_PackCurr)
                results["PackCurr_DR"].append(lib.VeAPI_b_PackCurr_DR)
                results["CellVolts"].append(lib_array_to_list(lib.VaAPI_U_CellVolts))
                results["CellVolts_DR"].append(lib_array_to_list(lib.VaAPI_b_CellVolts_DR))
                results["TempSnsrs"].append(lib_array_to_list(lib.VaAPI_T_TempSnsrs))
                results["TempSnsrs_DR"].append(lib_array_to_list(lib.VaAPI_b_TempSnsrs_DR))
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
                results["ErrorFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
                results["ErrorFlags (bin)"].append(format(lib.VeAFC_e_ErrorFlags, "032b"))
                results["ChgPackCurr"].append(lib.VeAFC_I_ChgPackCurr)
                results["ChgPackVolt"].append(lib.VeAFC_U_ChgPackVolt)
                results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)

                results["AFC_NVM_MagicNumber"].append(lib.s_AFC_Track.NeAFC_b_InitNVMStatus)
                results["AFC_CTE_MagicNumber"].append(
                    lib.s_AFC_CTE_Data.VeAFC_b_InitNVMStatusCTE
                )

                lib.LIB_Deobfuscate(
                    ffi.addressof(lib.s_AFC_CTE_Data, "VaAFC_Cnt_CPVCorrIdx"),
                    size(lib.s_AFC_CTE_Data.VaAFC_Cnt_CPVCorrIdx),
                    0xBD,
                )
                results["AFC_CTE_HighestIndex"].append(
                    lib_array_to_list(lib.s_AFC_CTE_Data.VaAFC_Cnt_CPVCorrIdx)
                )

                max_indices = [
                    max(lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx[i][j] for i in range(1))
                    for j in range(15)
                ]
                results["NVM_HighestIndex"].append(max_indices)

                results["NVM_HighestIndex2"].append(
                    lib_array_to_list(lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx)
                )

                results["QnovoAFC_LogVar1\nl_LoggingPath (dec)"].append(
                    lib.QnovoAFC_LogVar1
                )
                results["QnovoAFC_LogVar1\nl_LoggingPath (bin)"].append(
                    format(lib.QnovoAFC_LogVar1, "032b")
                )

                results["QnovoAFC_LogVar2\nl_InitializedFlag"].append(lib.QnovoAFC_LogVar2)

                results["QnovoAFC_LogVar3\nl_ValidSampleFlag"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar3)
                )

                results["QnovoAFC_LogVar4\nl_QNS_State"].append(lib.QnovoAFC_LogVar4)
                results["QnovoAFC_LogVar5\nl_PresentStageNum"].append(lib.QnovoAFC_LogVar5)
                results["QnovoAFC_LogVar6\nl_HighestIndex"].append(lib.QnovoAFC_LogVar6)
                results["QnovoAFC_LogVar9\nl_CPVCorrIdx"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar9)
                )
                results["QnovoAFC_LogVar10\nl_CV_Curr"].append(lib.QnovoAFC_LogVar10)
                results["QnovoAFC_LogVar11\nl_ProtocolStgCurr"].append(
                    lib.QnovoAFC_LogVar11
                )
                results["QnovoAFC_LogVar13\nl_ColdCompensatedCurr"].append(
                    lib.QnovoAFC_LogVar13
                )
                results["QnovoAFC_LogVar14\nl_CompensatedVolt"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar14)
                )
                results["QnovoAFC_LogVar15\nl_SampleCellVolt"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar15)
                )
                results["QnovoAFC_LogVar16\nl_RefCellVolt"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar16)
                )
            print("\n Loop End")
        # Write results into csv
        print(f"processed_{_FILENAME}")
        with open(f"processed_{_FILENAME}", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(results.keys())
            rows = zip(*results.values())
            writer.writerows(rows)
