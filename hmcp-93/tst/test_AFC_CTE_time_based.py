"""Test Module Description:
    Test module for CTE time based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *
import time
import os

SKIP_TEST = False

ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE = 15
if not SKIP_TEST:
    _SUBDIR_NAME = "test_data/time_based_data/input_data"
    _FILENAME = "4_260204_AFC+CTE_3646_MP1.1.8.0.0_AC_charger02.csv"
    #_FILENAME = "test_cte.csv"
    LOG_FILE = "cte_test_log_4.txt"

    module_path = abspath(__file__)
    _OUTPUT = "test_data/time_based_data/output_data"
    dir_path = join(dirname(module_path), _OUTPUT)
    log_file = join(dir_path, f"processed_CTE_{LOG_FILE}")
    if os.path.exists(log_file):
        os.remove(log_file)

    """
    Write logs to a file for later debugging.
    """
    def write_to_log(data):
        '''
        module_path = abspath(__file__)
        _OUTPUT = "test_data/time_based_data/output_data"
        dir_path = join(dirname(module_path), _OUTPUT)
        log_file = join(dir_path, f"processed_CTE_{LOG_FILE}")
        if os.path.exists(log_file):
            os.remove(log_file)
        '''
        with open(log_file, 'a') as file:
            file.write(data)
            file.write("\n")

    """
    Parse data from csv file and populate Input structure
    """
    def parse_AFC_HMC_Data():
        module_path = abspath(__file__)
        dir_path = join(dirname(module_path), _SUBDIR_NAME)
        csv_path = join(dir_path, _FILENAME)

        test_cases = []

        # Open the CSV file
        # Iterate over each row in the CSV
        for row in iter_file(csv_path):
            # Get inputs
            test_filename = 'AFC_CTE_Behavioural_Test.csv'
            Time = int(ast.literal_eval(row["Time"]))
            StartSOC = int(row["cte_input_params.soc_start"])
            EndSOC = int(row["cte_input_params.soc_end"])
            CTE_Mah = int(row["cte_input_params.battcap_mah"])
            CTE_Amb = int(row["cte_input_params.ambient_temp"])
            CTE_PowChg = int(row["cte_input_params.pwr_chg"])

            battery_state = int(row["cte_input_params.charging_now"])
            EVSEChgStatus = int(row["cte_input_params.charging_now"])
            cte_tbmin     = int(row["cte_input_params.tb_min"])
            cte_tbmax     = int(row["cte_input_params.tb_max"])
            cte_charging_80_input = int(row["cte_result.charging.time_80"])

            # Format data for parametrized test
            test_case = {
                "Inputs": {
                    "filename": test_filename,
                    "Time": Time,
                    "StartSOC": StartSOC,
                    "EndSOC": EndSOC,
                    "CTE_Mah": CTE_Mah,
                    "CTE_Amb": CTE_Amb,
                    "CTE_PowChg": CTE_PowChg,
                    "battery_state": battery_state,
                    "EVSEChgStatus": EVSEChgStatus,
                    "cte_tbmin": cte_tbmin,
                    "cte_tbmax": cte_tbmax,
                    "input_charge_time_80": cte_charging_80_input,
                },
                "Expected": {},
            }
            test_cases.append(test_case)
        return test_cases


    """
    Test case: time based test
    Read csv file, get parsed data in Input structure.
    Call AFC for each line from Input structure, populate AFC_CTE info structure.
    After each AFC call, call CTE for 10 times (each 100 ms)
    Receive CTE estimates and validate.
    """
    def test_hmc_afc_cte_behavioural(lib, setup_parameters):
        all_time_steps = parse_AFC_HMC_Data()

        # Initialize results
        results = {
            "Filename": [],
            "Time": [],
            "StartSOC": [],
            "EndSOC": [],
            "Battery_State": [],
            "EVSEChgStatus": [],
            " ": [],
            "ErrorFlags (dec)": [],
            "ErrorFlags (bin)": [],
            "ChgCompletionFlag": [],
            "CTE_Status": [],
            "charger_2_45_kw.time_80": [],
            "charger_2_45_kw.time_end_soc": [],
            "charger_2_64_kw.time_80": [],
            "charger_2_64_kw.time_end_soc": [],
            "charger_2_76_kw.time_80": [],
            "charger_2_76_kw.time_end_soc": [],
            "charger_2_88_kw.time_80": [],
            "charger_2_88_kw.time_end_soc": [],
            "charger_3_2_kw.time_80": [],
            "charger_3_2_kw.time_end_soc": [],
            "charger_10_9_kw.time_80": [],
            "charger_10_9_kw.time_end_soc": [],
            "charger_10_kw.time_80": [],
            "charger_10_kw.time_end_soc": [],
            "charger_50_kw.time_80": [],
            "charger_50_kw.time_end_soc": [],
            "charger_350_kw.time_80": [],
            "charger_350_kw.time_end_soc": [],
            "charging.time_80": [],
            "charging.time_end_soc": [],
        }
        cte_first_execution = True
        expected_result = True
        actual_result = True
        charging_started = False

        # For current charger
        soc_start_time_80 = 0
        soc_start_time_100 = 0
        expected_charge_time_80 = 0
        charging_80_completed = False
        charging_100_completed = False

        # for 350 kw
        soc_start_time_350_80 = 0
        soc_start_time_350_100 = 0
        expected_charge_time_350_80 = 0
        charging_350_80_completed = False
        charging_350_100_completed = False

        # For 50kw charger
        soc_start_time_50_80 = 0
        soc_start_time_50_100 = 0
        expected_charge_time_50_80 = 0
        charging_50_80_completed = False
        charging_50_100_completed = False

        # For 10_9kw charger
        soc_start_time_10_9_80 = 0
        soc_start_time_10_9_100 = 0
        expected_charge_time_10_9_80 = 0
        charging_10_9_80_completed = False
        charging_10_9_100_completed = False

        # For 10kw charger
        soc_start_time_10_80 = 0
        soc_start_time_10_100 = 0
        expected_charge_time_10_80 = 0
        charging_10_80_completed = False
        charging_10_100_completed = False

        # For 2_45kw charger
        soc_start_time_2_45_80 = 0
        soc_start_time_2_45_100 = 0
        expected_charge_time_2_45_80 = 0
        charging_2_45_80_completed = False
        charging_2_45_100_completed = False

        # For 3_2kw charger
        soc_start_time_3_2_80 = 0
        soc_start_time_3_2_100 = 0
        expected_charge_time_3_2_80 = 0
        charging_3_2_80_completed = False
        charging_3_2_100_completed = False

        # For 2_88kw charger
        soc_start_time_2_88_80 = 0
        soc_start_time_2_88_100 = 0
        expected_charge_time_2_88_80 = 0
        charging_2_88_80_completed = False
        charging_2_88_100_completed = False

        # For 2_64kw charger
        soc_start_time_2_64_80 = 0
        soc_start_time_2_64_100 = 0
        expected_charge_time_2_64_80 = 0
        charging_2_64_80_completed = False
        charging_2_64_100_completed = False

        # For 2_76kw charger
        soc_start_time_2_76_80 = 0
        soc_start_time_2_76_100 = 0
        expected_charge_time_2_76_80 = 0
        charging_2_76_80_completed = False
        charging_2_76_100_completed = False

        # previous CTE estimates (for comparing with current estimate)
        previous_charger_350_kw_time_end_soc = 0
        previous_charger_350_kw_time_80 = 0
        previous_charger_50_kw_time_end_soc = 0
        previous_charger_50_kw_time_80 = 0
        previous_charger_10_9_kw_time_end_soc = 0
        previous_charger_10_9_kw_time_80 = 0
        previous_charger_10_kw_time_end_soc = 0
        previous_charger_10_kw_time_80 = 0
        previous_charger_2_45_kw_time_end_soc = 0
        previous_charger_2_45_kw_time_80 = 0
        previous_charger_3_2_kw_time_end_soc = 0
        previous_charger_3_2_kw_time_80 = 0
        previous_charger_2_88_kw_time_end_soc = 0
        previous_charger_2_88_kw_time_80 = 0
        previous_charger_2_64_kw_time_end_soc = 0
        previous_charger_2_64_kw_time_80 = 0
        previous_charger_2_76_kw_time_end_soc = 0
        previous_charger_2_76_kw_time_80 = 0
        previous_charger_time_end_soc = 0
        previous_charger_time_80 = 0

        expected_charge_time_80 = 0
        expected_charge_time_350_80 = 0
        expected_charge_time_50_80 = 0
        expected_charge_time_10_9_80 = 0
        expected_charge_time_10_80 = 0
        expected_charge_time_2_45_80 = 0
        expected_charge_time_3_2_80 = 0
        expected_charge_time_2_88_80 = 0
        expected_charge_time_2_64_80 = 0
        expected_charge_time_2_76_80 = 0
        expected_charge_time_100 = 0
        expected_charge_time_350_100 = 0
        expected_charge_time_50_100 = 0
        expected_charge_time_10_9_100 = 0
        expected_charge_time_10_100 = 0
        expected_charge_time_2_45_100 = 0
        expected_charge_time_3_2_100 = 0
        expected_charge_time_2_88_100 = 0
        expected_charge_time_2_64_100 = 0
        expected_charge_time_2_76_100 = 0


        ele_addr = ffi.addressof(lib, "cte_status")
        status_ptr = ffi.cast("uint32_t*", ele_addr)

        test_i = 0
        for each_time_step in all_time_steps:
            # Initialize lib values before AFC call.
            test_filename = each_time_step["Inputs"]["filename"]
            input_time = each_time_step["Inputs"]["Time"]
            input_time_80 = each_time_step["Inputs"]["input_charge_time_80"]
            battery_state = each_time_step["Inputs"]["battery_state"]
            lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]


            lib.afc_cte_info.magic = 0x6C47;
            lib.afc_cte_info.data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            test_i+=1
            # Call CTE each 100 ms (AFC is called every 1s and CTE is called every 100ms)
            for i in range(10):
                lib.qnovo_cte(each_time_step["Inputs"]["StartSOC"], each_time_step["Inputs"]["EndSOC"], each_time_step["Inputs"]["cte_tbmin"],
                              each_time_step["Inputs"]["cte_tbmax"], each_time_step["Inputs"]["CTE_Amb"],
                              each_time_step["Inputs"]["CTE_PowChg"], each_time_step["Inputs"]["CTE_Mah"],
                              lib.VeAPI_b_EVSEChgStatus, ffi.addressof(lib, "afc_cte_info"),
                              ffi.addressof(lib, "cte_estimates"), status_ptr)
                #print(f"TestI : {test_i} and status {lib.cte_status}")
                if lib.cte_status == 0:
                    break
                time.sleep(0.1)

            # Record results
            results["Filename"].append(test_filename)
            results["Time"].append(input_time)
            results["StartSOC"].append(each_time_step["Inputs"]["StartSOC"])
            results["EndSOC"].append(each_time_step["Inputs"]["EndSOC"])
            results["Battery_State"].append(battery_state)
            results["EVSEChgStatus"].append(lib.VeAPI_b_EVSEChgStatus)
            results[" "].append("")  # Divider between input and output
            results["ErrorFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
            results["ErrorFlags (bin)"].append(format(lib.VeAFC_e_ErrorFlags, "032b"))
            results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)

            results["CTE_Status"].append(lib.cte_status)
            results["charging.time_end_soc"].append(lib.cte_estimates.charging.time_end_soc)
            results["charging.time_80"].append(lib.cte_estimates.charging.time_80)

            results["charger_350_kw.time_end_soc"].append(lib.cte_estimates.charger_350_kw.time_end_soc)
            results["charger_350_kw.time_80"].append(lib.cte_estimates.charger_350_kw.time_80)
            results["charger_50_kw.time_end_soc"].append(lib.cte_estimates.charger_50_kw.time_end_soc)
            results["charger_50_kw.time_80"].append(lib.cte_estimates.charger_50_kw.time_80)
            results["charger_10_9_kw.time_end_soc"].append(lib.cte_estimates.charger_10_9_kw.time_end_soc)
            results["charger_10_9_kw.time_80"].append(lib.cte_estimates.charger_10_9_kw.time_80)
            results["charger_10_kw.time_end_soc"].append(lib.cte_estimates.charger_10_kw.time_end_soc)
            results["charger_10_kw.time_80"].append(lib.cte_estimates.charger_10_kw.time_80)
            results["charger_2_45_kw.time_end_soc"].append(lib.cte_estimates.charger_2_45_kw.time_end_soc)
            results["charger_2_45_kw.time_80"].append(lib.cte_estimates.charger_2_45_kw.time_80)
            results["charger_3_2_kw.time_end_soc"].append(lib.cte_estimates.charger_3_2_kw.time_end_soc)
            results["charger_3_2_kw.time_80"].append(lib.cte_estimates.charger_3_2_kw.time_80)
            results["charger_2_88_kw.time_end_soc"].append(lib.cte_estimates.charger_2_88_kw.time_end_soc)
            results["charger_2_88_kw.time_80"].append(lib.cte_estimates.charger_2_88_kw.time_80)
            results["charger_2_64_kw.time_end_soc"].append(lib.cte_estimates.charger_2_64_kw.time_end_soc)
            results["charger_2_64_kw.time_80"].append(lib.cte_estimates.charger_2_64_kw.time_80)
            results["charger_2_76_kw.time_end_soc"].append(lib.cte_estimates.charger_2_76_kw.time_end_soc)
            results["charger_2_76_kw.time_80"].append(lib.cte_estimates.charger_2_76_kw.time_80)

            # Store previous cte estimates for first time CTE call.
            if cte_first_execution:
                write_to_log(f"CTE First execution, charging started : {charging_started}, battery_state : {battery_state}")
                cte_first_execution = False
                previous_charger_350_kw_time_end_soc = 0
                previous_charger_350_kw_time_80 = 0
                previous_charger_50_kw_time_end_soc = 0
                previous_charger_50_kw_time_80 = 0
                previous_charger_10_9_kw_time_end_soc = 0
                previous_charger_10_9_kw_time_80 = 0
                previous_charger_10_kw_time_end_soc = 0
                previous_charger_10_kw_time_80 = 0
                previous_charger_2_45_kw_time_end_soc = 0
                previous_charger_2_45_kw_time_80 = 0
                previous_charger_3_2_kw_time_end_soc = 0
                previous_charger_3_2_kw_time_80 = 0
                previous_charger_2_88_kw_time_end_soc = 0
                previous_charger_2_88_kw_time_80 = 0
                previous_charger_2_64_kw_time_end_soc = 0
                previous_charger_2_64_kw_time_80 = 0
                previous_charger_2_76_kw_time_end_soc = 0
                previous_charger_2_76_kw_time_80 = 0
                previous_charger_time_end_soc = 0
                previous_charger_time_80 = 0
            else:
                # Second CTE call onwards , compare CTE estimates
                if previous_charger_time_80 > 0:
                    if lib.cte_estimates.charging.time_end_soc > previous_charger_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_100: against input time : : {input_time}, "
                                     f"current est : {lib.cte_estimates.charging.time_end_soc},"
                                     f"previous est: {previous_charger_time_end_soc}")
                    if abs(lib.cte_estimates.charging.time_end_soc - previous_charger_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_100: against input time : : {input_time}, "
                                     f"current est : {lib.cte_estimates.charging.time_end_soc},"
                                     f"previous est: {previous_charger_time_end_soc}")

                    if lib.cte_estimates.charging.time_80 > previous_charger_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charging.time_80},"
                                     f"previous est: {previous_charger_time_80}")
                    if abs(lib.cte_estimates.charging.time_80 - previous_charger_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5 , check output file "
                                     f"Current Charger_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charging.time_80},"
                                     f"previous est: {previous_charger_time_80}")

                    if lib.cte_estimates.charger_350_kw.time_end_soc > previous_charger_350_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_350_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_350_kw.time_end_soc},"
                                     f"previous est: {previous_charger_350_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_350_kw.time_end_soc - previous_charger_350_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_350_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_350_kw.time_end_soc},"
                                     f"previous est: {previous_charger_350_kw_time_end_soc}")

                    if lib.cte_estimates.charger_350_kw.time_80 > previous_charger_350_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_350_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_350_kw.time_80},"
                                     f"previous est: {previous_charger_350_kw_time_80}")
                    if abs(lib.cte_estimates.charger_350_kw.time_80 - previous_charger_350_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_350_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_350_kw.time_80},"
                                     f"previous est: {previous_charger_350_kw_time_80}")

                    if lib.cte_estimates.charger_50_kw.time_end_soc > previous_charger_50_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_50_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_50_kw.time_end_soc},"
                                     f"previous est: {previous_charger_50_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_50_kw.time_end_soc - previous_charger_50_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_50_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_50_kw.time_end_soc},"
                                     f"previous est: {previous_charger_50_kw_time_end_soc}")

                    if lib.cte_estimates.charger_50_kw.time_80 > previous_charger_50_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_50_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_50_kw.time_80},"
                                     f"previous est: {previous_charger_50_kw_time_80}")
                    if abs(lib.cte_estimates.charger_50_kw.time_80 - previous_charger_50_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_50_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_50_kw.time_80},"
                                     f"previous est: {previous_charger_50_kw_time_80}")

                    if lib.cte_estimates.charger_10_9_kw.time_end_soc > previous_charger_10_9_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_9_kw.time_end_soc},"
                                     f"previous est: {previous_charger_10_9_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_10_9_kw.time_end_soc - previous_charger_10_9_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_9_kw.time_end_soc},"
                                     f"previous est: {previous_charger_10_9_kw_time_end_soc}")

                    if lib.cte_estimates.charger_10_9_kw.time_80 > previous_charger_10_9_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_9_kw.time_80},"
                                     f"previous est: {previous_charger_10_9_kw_time_80}")
                    if abs(lib.cte_estimates.charger_10_9_kw.time_80 - previous_charger_10_9_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_9_kw.time_80},"
                                     f"previous est: {previous_charger_10_9_kw_time_80}")

                    if lib.cte_estimates.charger_10_kw.time_end_soc > previous_charger_10_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output  "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_kw.time_end_soc},"
                                     f"previous est: {previous_charger_10_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_10_kw.time_end_soc - previous_charger_10_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output  "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_kw.time_end_soc},"
                                     f"previous est: {previous_charger_10_kw_time_end_soc}")

                    if lib.cte_estimates.charger_10_kw.time_80 > previous_charger_10_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_kw.time_80},"
                                     f"previous est: {previous_charger_10_kw_time_80}")
                    if abs(lib.cte_estimates.charger_10_kw.time_80 - previous_charger_10_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_10_kw.time_80},"
                                     f"previous est: {previous_charger_10_kw_time_80}")

                    if lib.cte_estimates.charger_2_45_kw.time_end_soc > previous_charger_2_45_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_45_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_45_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_2_45_kw.time_end_soc - previous_charger_2_45_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_45_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_45_kw_time_end_soc}")

                    if lib.cte_estimates.charger_2_45_kw.time_80 > previous_charger_2_45_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_2_45_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_45_kw.time_80},"
                                     f"previous est: {previous_charger_2_45_kw_time_80}")
                    if abs(lib.cte_estimates.charger_2_45_kw.time_80 - previous_charger_2_45_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_2_45_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_45_kw.time_80},"
                                     f"previous est: {previous_charger_2_45_kw_time_80}")

                    if lib.cte_estimates.charger_3_2_kw.time_end_soc > previous_charger_3_2_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_3_2_kw.time_end_soc},"
                                     f"previous est: {previous_charger_3_2_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_3_2_kw.time_end_soc - previous_charger_3_2_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_3_2_kw.time_end_soc},"
                                     f"previous est: {previous_charger_3_2_kw_time_end_soc}")

                    if lib.cte_estimates.charger_3_2_kw.time_80 > previous_charger_3_2_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_3_2_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_3_2_kw.time_80},"
                                     f"previous est: {previous_charger_3_2_kw_time_80} ")
                    if abs(lib.cte_estimates.charger_3_2_kw.time_80 - previous_charger_3_2_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_3_2_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_3_2_kw.time_80},"
                                     f"previous est: {previous_charger_3_2_kw_time_80} ")

                    if lib.cte_estimates.charger_2_88_kw.time_end_soc > previous_charger_2_88_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_88_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_88_kw_time_end_soc} ")
                    if abs(lib.cte_estimates.charger_2_88_kw.time_end_soc - previous_charger_2_88_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_88_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_88_kw_time_end_soc} ")

                    if lib.cte_estimates.charger_2_88_kw.time_80 > previous_charger_2_88_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_2_88_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_88_kw.time_80},"
                                     f"previous est: {previous_charger_2_88_kw_time_80}")
                    if abs(lib.cte_estimates.charger_2_88_kw.time_80 - previous_charger_2_88_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_2_88_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_88_kw.time_80},"
                                     f"previous est: {previous_charger_2_88_kw_time_80}")

                    if lib.cte_estimates.charger_2_64_kw.time_end_soc > previous_charger_2_64_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_64_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_64_kw_time_end_soc}")
                    if abs(lib.cte_estimates.charger_2_64_kw.time_end_soc - previous_charger_2_64_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_64_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_64_kw_time_end_soc}")

                    if lib.cte_estimates.charger_2_64_kw.time_80 > previous_charger_2_64_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_2_64_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_64_kw.time_80},"
                                     f"previous est: {previous_charger_2_64_kw_time_80}")

                    if abs(lib.cte_estimates.charger_2_64_kw.time_80 - previous_charger_2_64_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_2_64_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_64_kw.time_80},"
                                     f"previous est: {previous_charger_2_64_kw_time_80}")

                    if lib.cte_estimates.charger_2_76_kw.time_end_soc > previous_charger_2_76_kw_time_end_soc:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_76_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_76_kw_time_end_soc}")

                    if abs(lib.cte_estimates.charger_2_76_kw.time_end_soc - previous_charger_2_76_kw_time_end_soc) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_10_9_100: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_76_kw.time_end_soc},"
                                     f"previous est: {previous_charger_2_76_kw_time_end_soc}")

                    if lib.cte_estimates.charger_2_76_kw.time_80 > previous_charger_2_76_kw_time_80:
                        write_to_log(f"Current CTE estimate is greater than previous estimate, check output file "
                                     f"Current Charger_2_76_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_76_kw.time_80},"
                                     f"previous est: {previous_charger_2_76_kw_time_80}")
                    if abs(lib.cte_estimates.charger_2_76_kw.time_80 - previous_charger_2_76_kw_time_80) > 5:
                        write_to_log(f"Current CTE estimate is greater than 5, check output file "
                                     f"Current Charger_2_76_80: against input time : {input_time},"
                                     f"current est : {lib.cte_estimates.charger_2_76_kw.time_80},"
                                     f"previous est: {previous_charger_2_76_kw_time_80}")

                    # Store current value as previous value
                    previous_charger_time_end_soc = lib.cte_estimates.charging.time_end_soc
                    previous_charger_time_80 = lib.cte_estimates.charging.time_80
                    previous_charger_350_kw_time_end_soc = lib.cte_estimates.charger_350_kw.time_end_soc
                    previous_charger_350_kw_time_80 = lib.cte_estimates.charger_350_kw.time_80
                    previous_charger_50_kw_time_end_soc = lib.cte_estimates.charger_50_kw.time_end_soc
                    previous_charger_50_kw_time_80 = lib.cte_estimates.charger_50_kw.time_80
                    previous_charger_10_9_kw_time_end_soc = lib.cte_estimates.charger_10_9_kw.time_end_soc
                    previous_charger_10_9_kw_time_80 = lib.cte_estimates.charger_10_9_kw.time_80
                    previous_charger_10_kw_time_end_soc = lib.cte_estimates.charger_10_kw.time_end_soc
                    previous_charger_10_kw_time_80 = lib.cte_estimates.charger_10_kw.time_80
                    previous_charger_2_45_kw_time_end_soc = lib.cte_estimates.charger_2_45_kw.time_end_soc
                    previous_charger_2_45_kw_time_80 = lib.cte_estimates.charger_2_45_kw.time_80
                    previous_charger_3_2_kw_time_end_soc = lib.cte_estimates.charger_3_2_kw.time_end_soc
                    previous_charger_3_2_kw_time_80 = lib.cte_estimates.charger_3_2_kw.time_80
                    previous_charger_2_88_kw_time_end_soc = lib.cte_estimates.charger_2_88_kw.time_end_soc
                    previous_charger_2_88_kw_time_80 = lib.cte_estimates.charger_2_88_kw.time_80
                    previous_charger_2_64_kw_time_end_soc = lib.cte_estimates.charger_2_64_kw.time_end_soc
                    previous_charger_2_64_kw_time_80 = lib.cte_estimates.charger_2_64_kw.time_80
                    previous_charger_2_76_kw_time_end_soc = lib.cte_estimates.charger_2_76_kw.time_end_soc
                    previous_charger_2_76_kw_time_80 = lib.cte_estimates.charger_2_76_kw.time_80

            # Charging started (Charging state was unplugged)
            if battery_state == 1 and charging_started is False and input_time_80 > 0:
                write_to_log(f"Charging started: input time : {input_time}")
                # Store input time from csv data as charging start time
                soc_start_time_80 = input_time
                soc_start_time_100 = input_time
                soc_start_time_350_80 = input_time
                soc_start_time_350_100 = input_time
                soc_start_time_50_80 = input_time
                soc_start_time_50_100 = input_time
                soc_start_time_10_9_80 = input_time
                soc_start_time_10_9_100 = input_time
                soc_start_time_10_80 = input_time
                soc_start_time_10_100 = input_time
                soc_start_time_2_45_80 = input_time
                soc_start_time_2_45_100 = input_time
                soc_start_time_3_2_80 = input_time
                soc_start_time_3_2_100 = input_time
                soc_start_time_2_88_80 = input_time
                soc_start_time_2_88_100 = input_time
                soc_start_time_2_64_80 = input_time
                soc_start_time_2_64_100 = input_time
                soc_start_time_2_76_80 = input_time
                soc_start_time_2_76_100 = input_time

                expected_charge_time_80 = lib.cte_estimates.charging.time_80
                expected_charge_time_350_80 = lib.cte_estimates.charger_350_kw.time_80
                expected_charge_time_50_80 = lib.cte_estimates.charger_50_kw.time_80
                expected_charge_time_10_9_80 = lib.cte_estimates.charger_10_9_kw.time_80
                expected_charge_time_10_80 = lib.cte_estimates.charger_10_kw.time_80
                expected_charge_time_2_45_80 = lib.cte_estimates.charger_2_45_kw.time_80
                expected_charge_time_3_2_80 = lib.cte_estimates.charger_3_2_kw.time_80
                expected_charge_time_2_88_80 = lib.cte_estimates.charger_2_88_kw.time_80
                expected_charge_time_2_64_80 = lib.cte_estimates.charger_2_64_kw.time_80
                expected_charge_time_2_76_80 = lib.cte_estimates.charger_2_76_kw.time_80
                expected_charge_time_100 = lib.cte_estimates.charging.time_end_soc
                expected_charge_time_350_100 = lib.cte_estimates.charger_350_kw.time_end_soc
                expected_charge_time_50_100 = lib.cte_estimates.charger_50_kw.time_end_soc
                expected_charge_time_10_9_100 = lib.cte_estimates.charger_10_9_kw.time_end_soc
                expected_charge_time_10_100 = lib.cte_estimates.charger_10_kw.time_end_soc
                expected_charge_time_2_45_100 = lib.cte_estimates.charger_2_45_kw.time_end_soc
                expected_charge_time_3_2_100 = lib.cte_estimates.charger_3_2_kw.time_end_soc
                expected_charge_time_2_88_100 = lib.cte_estimates.charger_2_88_kw.time_end_soc
                expected_charge_time_2_64_100 = lib.cte_estimates.charger_2_64_kw.time_end_soc
                expected_charge_time_2_76_100 = lib.cte_estimates.charger_2_76_kw.time_end_soc
                write_to_log(f"Expected expected_charge_time_80 : {expected_charge_time_80}")
                write_to_log(f"Expected expected_charge_time_350_80 : {expected_charge_time_350_80}")
                charging_started = True

            if charging_started:
                # Charging started and 80% charging completed now. Current Charger
                if battery_state == 1 and lib.cte_estimates.charging.time_80 == 0 and charging_80_completed is False:
                    write_to_log(f"Charger 80 reached, input time : {input_time}")
                    soc_end_time_80 = input_time
                    charging_80_completed = True
                    actual_charge_time_80 = soc_end_time_80 - soc_start_time_80
                    write_to_log(f"Expected charge time: {expected_charge_time_80}, actual : {actual_charge_time_80}")
                    if expected_charge_time_80 and actual_charge_time_80:
                        write_to_log(f"Expected ChargeTime: {expected_charge_time_80} and Actual ChargeTime: {actual_charge_time_80}")
                        average = (actual_charge_time_80 + expected_charge_time_80) / 2
                        diff = abs(actual_charge_time_80 - expected_charge_time_80)
                        deviation_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity current charger: {deviation_80}")
                        if deviation_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for current charger 80% capacity is above KPI: {deviation_80}")

                # Charging started and 80% charging completed now. 350kw charger
                if battery_state == 1 and lib.cte_estimates.charger_350_kw.time_80 == 0 and charging_350_80_completed is False:
                    soc_end_time_350_80 = input_time
                    charging_350_80_completed = True
                    actual_charge_time_350_80 = soc_end_time_350_80 - soc_start_time_350_80
                    if expected_charge_time_350_80 and actual_charge_time_350_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_350_80} and Actual ChargeTime: {actual_charge_time_350_80}")
                        average = (actual_charge_time_350_80 + expected_charge_time_350_80) / 2
                        diff = abs(actual_charge_time_350_80 - expected_charge_time_350_80)
                        deviation_350_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_350_kw 80% capacity: {deviation_350_80}")
                        if deviation_350_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 350kw  80% capacity is above KPI: {deviation_350_80}")

                # Charging started and 80% charging completed now. 50kw charger
                if battery_state == 1 and lib.cte_estimates.charger_50_kw.time_80 == 0 and charging_50_80_completed is False:
                    soc_end_time_50_80 = input_time
                    charging_50_80_completed = True
                    actual_charge_time_50_80 = soc_end_time_50_80 - soc_start_time_50_80
                    if expected_charge_time_50_80 and actual_charge_time_50_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_50_80} and Actual ChargeTime: {actual_charge_time_50_80}")
                        average = (actual_charge_time_50_80 + expected_charge_time_50_80) / 2
                        diff = abs(actual_charge_time_50_80 - expected_charge_time_50_80)
                        deviation_50_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_50_kw 80% capacity 50_80: {deviation_50_80}")
                        if deviation_50_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 50kw capacity is above KPI: {deviation_50_80}")

                # Charging started and 80% charging completed now. 10_9kw charger
                if battery_state == 1 and lib.cte_estimates.charger_10_9_kw.time_80 == 0 and charging_10_9_80_completed is False:
                    soc_end_time_10_9_80 = input_time
                    charging_10_9_80_completed = True
                    actual_charge_time_10_9_80 = soc_end_time_10_9_80 - soc_start_time_10_9_80
                    if expected_charge_time_10_9_80 and actual_charge_time_10_9_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_10_9_80} and Actual ChargeTime: {actual_charge_time_10_9_80}")
                        average = (actual_charge_time_10_9_80 + expected_charge_time_10_9_80) / 2
                        diff = abs(actual_charge_time_10_9_80 - expected_charge_time_10_9_80)
                        deviation_10_9_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_10_9_kw 80% capacity 10_9_80: {deviation_10_9_80}")
                        if deviation_10_9_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 10_9kw capacity is above KPI: {deviation_10_9_80}")

                # Charging started and 80% charging completed now. 10kw charger
                if battery_state == 1 and lib.cte_estimates.charger_10_kw.time_80 == 0 and charging_10_80_completed is False:
                    soc_end_time_10_80 = input_time
                    charging_10_80_completed = True
                    actual_charge_time_10_80 = soc_end_time_10_80 - soc_start_time_10_80
                    if expected_charge_time_10_80 and actual_charge_time_10_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_10_80} and Actual ChargeTime: {actual_charge_time_10_80}")
                        average = (actual_charge_time_10_80 + expected_charge_time_10_80) / 2
                        diff = abs(actual_charge_time_10_80 - expected_charge_time_10_80)
                        deviation_10_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_10_kw 80% capacity 10_80: {deviation_10_80}")
                        if deviation_10_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 10kw capacity is above KPI: {deviation_10_80}")

                # Charging started and 80% charging completed now. 2_45kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_45_kw.time_80 == 0 and charging_2_45_80_completed is False:
                    soc_end_time_2_45_80 = input_time
                    charging_2_45_80_completed = True
                    actual_charge_time_2_45_80 = soc_end_time_2_45_80 - soc_start_time_2_45_80
                    if expected_charge_time_2_45_80 and actual_charge_time_2_45_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_45_80} and Actual ChargeTime: {actual_charge_time_2_45_80}")
                        average = (actual_charge_time_2_45_80 + expected_charge_time_2_45_80) / 2
                        diff = abs(actual_charge_time_2_45_80 - expected_charge_time_2_45_80)
                        deviation_2_45_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_2_45_kw 80% capacity 2_45_80: {deviation_2_45_80}")
                        if deviation_2_45_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 2_45kw capacity is above KPI: {deviation_2_45_80}")

                # Charging started and 80% charging completed now. 3_2kw charger
                if battery_state == 1 and lib.cte_estimates.charger_3_2_kw.time_80 == 0 and charging_3_2_80_completed is False:
                    soc_end_time_3_2_80 = input_time
                    charging_3_2_80_completed = True
                    actual_charge_time_3_2_80 = soc_end_time_3_2_80 - soc_start_time_3_2_80
                    if expected_charge_time_3_2_80 and actual_charge_time_3_2_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_3_2_80} and Actual ChargeTime: {actual_charge_time_3_2_80}")
                        average = (actual_charge_time_3_2_80 + expected_charge_time_3_2_80) / 2
                        diff = abs(actual_charge_time_3_2_80 - expected_charge_time_3_2_80)
                        deviation_3_2_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_3_2_kw 80% capacity 3_2_80: {deviation_3_2_80}")
                        if deviation_3_2_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 3_2kw capacity is above KPI: {deviation_3_2_80}")

                # Charging started and 80% charging completed now. 2_88kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_88_kw.time_80 == 0 and charging_2_88_80_completed is False:
                    soc_end_time_2_88_80 = input_time
                    charging_2_88_80_completed = True
                    actual_charge_time_2_88_80 = soc_end_time_2_88_80 - soc_start_time_2_88_80
                    if expected_charge_time_2_88_80 and actual_charge_time_2_88_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_88_80} and Actual ChargeTime: {actual_charge_time_2_88_80}")
                        average = (actual_charge_time_2_88_80 + expected_charge_time_2_88_80) / 2
                        diff = abs(actual_charge_time_2_88_80 - expected_charge_time_2_88_80)
                        deviation_2_88_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_2_88_kw 80% capacity 2_88_80: {deviation_2_88_80}")
                        if deviation_2_88_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 2_88kw capacity is above KPI: {deviation_2_88_80}")

                # Charging started and 80% charging completed now. 2_64kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_64_kw.time_80 == 0 and charging_2_64_80_completed is False:
                    soc_end_time_2_64_80 = input_time
                    charging_2_64_80_completed = True
                    actual_charge_time_2_64_80 = soc_end_time_2_64_80 - soc_start_time_2_64_80
                    if expected_charge_time_2_64_80 and actual_charge_time_2_64_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_64_80} and Actual ChargeTime: {actual_charge_time_2_64_80}")

                        average = (actual_charge_time_2_64_80 + expected_charge_time_2_64_80) / 2
                        diff = abs(actual_charge_time_2_64_80 - expected_charge_time_2_64_80)
                        deviation_2_64_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_2_64_kw 80% capacity 2_64_80: {deviation_2_64_80}")
                        if deviation_2_64_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 2_64kw capacity is above KPI: {deviation_2_64_80}")

                # Charging started and 80% charging completed now. 2_76kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_76_kw.time_80 == 0 and charging_2_76_80_completed is False:
                    soc_end_time_2_76_80 = input_time
                    charging_2_76_80_completed = True
                    actual_charge_time_2_76_80 = soc_end_time_2_76_80 - soc_start_time_2_76_80
                    if expected_charge_time_2_76_80 and actual_charge_time_2_76_80:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_76_80} and Actual ChargeTime: {actual_charge_time_2_76_80}")

                        average = (actual_charge_time_2_76_80 + expected_charge_time_2_76_80) / 2
                        diff = abs(actual_charge_time_2_76_80 - expected_charge_time_2_76_80)
                        deviation_2_76_80 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for charger_2_76_kw 80% capacity 2_76_80: {deviation_2_76_80}")
                        if deviation_2_76_80 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% for 2_76kw capacity is above KPI: {deviation_2_76_80}")

                # Charging started and 100% charging completed now. Current Charger.
                if battery_state == 1 and lib.cte_estimates.charging.time_end_soc == 0 and charging_100_completed is False:
                    soc_end_time_100 = input_time
                    charging_100_completed = True
                    actual_charge_time_100 = soc_end_time_100 - soc_start_time_100
                    if expected_charge_time_100 and actual_charge_time_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_100} and Actual ChargeTime: {actual_charge_time_100}")

                        average = (actual_charge_time_100 + expected_charge_time_100) / 2
                        diff = abs(actual_charge_time_100 - expected_charge_time_100)
                        deviation_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity current charger: {deviation_100}")
                        if deviation_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for current charger is above KPI: {deviation_100}")

                # Charging started and 100% charging completed now. 350kw charger
                if battery_state == 1 and lib.cte_estimates.charger_350_kw.time_end_soc == 0 and charging_350_100_completed is False:
                    soc_end_time_350_100 = input_time
                    charging_350_100_completed = True
                    actual_charge_time_350_100 = soc_end_time_350_100 - soc_start_time_350_100
                    if expected_charge_time_350_100 and actual_charge_time_350_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_350_100} and Actual ChargeTime: {actual_charge_time_350_100}")

                        average = (actual_charge_time_350_100 + expected_charge_time_350_100) / 2
                        diff = abs(actual_charge_time_350_100 - expected_charge_time_350_100)
                        deviation_350_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 350kw: {deviation_350_100}")
                        if deviation_350_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for 350kw is above KPI: {deviation_350_100}")

                # Charging started and 100% charging completed now. 50kw charger
                if battery_state == 1 and lib.cte_estimates.charger_50_kw.time_end_soc == 0 and charging_50_100_completed is False:
                    soc_end_time_50_100 = input_time
                    charging_50_100_completed = True
                    actual_charge_time_50_100 = soc_end_time_50_100 - soc_start_time_50_100
                    if expected_charge_time_50_100 and actual_charge_time_50_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_50_100} and Actual ChargeTime: {actual_charge_time_50_100}")

                        average = (actual_charge_time_50_100 + expected_charge_time_50_100) / 2
                        diff = abs(actual_charge_time_50_100 - expected_charge_time_50_100)
                        deviation_50_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 50kw: {deviation_50_100}")
                        if deviation_50_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for 50kw is above KPI: {deviation_50_100}")

                # Charging started and 100% charging completed now. 10_9kw charger
                if battery_state == 1 and lib.cte_estimates.charger_10_9_kw.time_end_soc == 0 and charging_10_9_100_completed is False:
                    soc_end_time_10_9_100 = input_time
                    charging_10_9_100_completed = True
                    actual_charge_time_10_9_100 = soc_end_time_10_9_100 - soc_start_time_10_9_100
                    if expected_charge_time_10_9_100 and actual_charge_time_10_9_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_10_9_100} and Actual ChargeTime: {actual_charge_time_10_9_100}")

                        average = (actual_charge_time_10_9_100 + expected_charge_time_10_9_100) / 2
                        diff = abs(actual_charge_time_10_9_100 - expected_charge_time_10_9_100)
                        deviation_10_9_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 10_9kw: {deviation_10_9_100}")
                        if deviation_10_9_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for 10_9kw is above KPI: {deviation_10_9_100}")

                # Charging started and 100% charging completed now. 10kw charger
                if battery_state == 1 and lib.cte_estimates.charger_10_kw.time_end_soc == 0 and charging_10_100_completed is False:
                    soc_end_time_10_100 = input_time
                    charging_10_100_completed = True
                    actual_charge_time_10_100 = soc_end_time_10_100 - soc_start_time_10_100
                    if expected_charge_time_10_100 and actual_charge_time_10_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_10_100} and Actual ChargeTime: {actual_charge_time_10_100}")

                        average = (actual_charge_time_10_100 + expected_charge_time_10_100) / 2
                        diff = abs(actual_charge_time_10_100 - expected_charge_time_10_100)
                        deviation_10_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 10kw: {deviation_10_100}")
                        if deviation_10_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for 10kw is above KPI: {deviation_10_100}")

                # Charging started and 100% charging completed now. 2_45kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_45_kw.time_end_soc == 0 and charging_2_45_100_completed is False:
                    soc_end_time_2_45_100 = input_time
                    charging_2_45_100_completed = True
                    actual_charge_time_2_45_100 = soc_end_time_2_45_100 - soc_start_time_2_45_100
                    if expected_charge_time_2_45_100 and actual_charge_time_2_45_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_45_100} and Actual ChargeTime: {actual_charge_time_2_45_100}")

                        average = (actual_charge_time_2_45_100 + expected_charge_time_2_45_100) / 2
                        diff = abs(actual_charge_time_2_45_100 - expected_charge_time_2_45_100)
                        deviation_2_45_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 2_45kw: {deviation_2_45_100}")
                        if deviation_2_45_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(f"Deviation in estimate for 80% capacity for 2_45kw is above KPI: {deviation_2_45_100}")

                # Charging started and 100% charging completed now. 3_2kw charger
                if battery_state == 1 and lib.cte_estimates.charger_3_2_kw.time_end_soc == 0 and charging_3_2_100_completed is False:
                    soc_end_time_3_2_100 = input_time
                    charging_3_2_100_completed = True
                    actual_charge_time_3_2_100 = soc_end_time_3_2_100 - soc_start_time_3_2_100
                    if expected_charge_time_3_2_100 and actual_charge_time_3_2_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_3_2_100} and Actual ChargeTime: {actual_charge_time_3_2_100}")

                        average = (actual_charge_time_3_2_100 + expected_charge_time_3_2_100) / 2
                        diff = abs(actual_charge_time_3_2_100 - expected_charge_time_3_2_100)
                        deviation_3_2_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 3_2kw: {deviation_3_2_100}")
                        if deviation_3_2_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(
                                f"Deviation in estimate for 80% capacity for 3_2kw is above KPI: {deviation_3_2_100}")

                # Charging started and 100% charging completed now. 2_88kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_88_kw.time_end_soc == 0 and charging_2_88_100_completed is False:
                    soc_end_time_2_88_100 = input_time
                    charging_2_88_100_completed = True
                    actual_charge_time_2_88_100 = soc_end_time_2_88_100 - soc_start_time_2_88_100
                    if expected_charge_time_2_88_100 and actual_charge_time_2_88_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_88_100} and Actual ChargeTime: {actual_charge_time_2_88_100}")

                        average = (actual_charge_time_2_88_100 + expected_charge_time_2_88_100) / 2
                        diff = abs(actual_charge_time_2_88_100 - expected_charge_time_2_88_100)
                        deviation_2_88_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 2_88kw: {deviation_2_88_100}")
                        if deviation_2_88_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(
                                f"Deviation in estimate for 80% capacity for 2_88kw is above KPI: {deviation_2_88_100}")

                # Charging started and 100% charging completed now. 2_64kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_64_kw.time_end_soc == 0 and charging_2_64_100_completed is False:
                    soc_end_time_2_64_100 = input_time
                    charging_2_64_100_completed = True
                    actual_charge_time_2_64_100 = soc_end_time_2_64_100 - soc_start_time_2_64_100
                    if expected_charge_time_2_64_100 and expected_charge_time_2_64_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_64_100} and Actual ChargeTime: {expected_charge_time_2_64_100}")

                        average = (actual_charge_time_2_64_100 + expected_charge_time_2_64_100) / 2
                        diff = abs(actual_charge_time_2_64_100 - expected_charge_time_2_64_100)
                        deviation_2_64_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 2_64kw: {deviation_2_64_100}")
                        if deviation_2_64_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(
                                f"Deviation in estimate for 80% capacity for 2_64kw is above KPI: {deviation_2_64_100}")

                # Charging started and 100% charging completed now. 2_76kw charger
                if battery_state == 1 and lib.cte_estimates.charger_2_76_kw.time_end_soc == 0 and charging_2_76_100_completed is False:
                    soc_end_time_2_76_100 = input_time
                    charging_2_76_100_completed = True
                    actual_charge_time_2_76_100 = soc_end_time_2_76_100 - soc_start_time_2_76_100
                    if expected_charge_time_2_76_100 and actual_charge_time_2_76_100:
                        write_to_log(
                            f"Expected ChargeTime: {expected_charge_time_2_76_100} and Actual ChargeTime: {actual_charge_time_2_76_100}")

                        average = (actual_charge_time_2_76_100 + expected_charge_time_2_76_100) / 2
                        diff = abs(actual_charge_time_2_76_100 - expected_charge_time_2_76_100)
                        deviation_2_76_100 = (diff / average) * 100
                        write_to_log(f"Deviation in estimate for 80% capacity 2_76kw: {deviation_2_76_100}")
                        if deviation_2_76_100 > ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE:
                            write_to_log(
                                f"Deviation in estimate for 80% capacity for 2_76kw is above KPI: {deviation_2_76_100}")

            # charging is done and now next charge cycle.
            if battery_state == 0 and charging_started is True:
                write_to_log("Resetting after a cycle")
                charging_started = False
                soc_start_time_80 = 0
                soc_start_time_100 = 0
                expected_charge_time_80 = 0
                charging_80_completed = False
                charging_100_completed = False

                soc_start_time_350_80 = 0
                soc_start_time_350_100 = 0
                expected_charge_time_350_80 = 0
                charging_350_80_completed = False
                charging_350_100_completed = False

                soc_start_time_50_80 = 0
                soc_start_time_50_100 = 0
                expected_charge_time_50_80 = 0
                charging_50_80_completed = False
                charging_50_100_completed = False

                soc_start_time_10_9_80 = 0
                soc_start_time_10_9_100 = 0
                expected_charge_time_10_9_80 = 0
                charging_10_9_80_completed = False
                charging_10_9_100_completed = False

                soc_start_time_10_80 = 0
                soc_start_time_10_100 = 0
                expected_charge_time_10_80 = 0
                charging_10_80_completed = False
                charging_10_100_completed = False

                soc_start_time_2_45_80 = 0
                soc_start_time_2_45_100 = 0
                expected_charge_time_2_45_80 = 0
                charging_2_45_80_completed = False
                charging_2_45_100_completed = False

                soc_start_time_3_2_80 = 0
                soc_start_time_3_2_100 = 0
                expected_charge_time_3_2_80 = 0
                charging_3_2_80_completed = False
                charging_3_2_100_completed = False

                soc_start_time_2_88_80 = 0
                soc_start_time_2_88_100 = 0
                expected_charge_time_2_88_80 = 0
                charging_2_88_80_completed = False
                charging_2_88_100_completed = False
                deviation_2_88_80 = 0

                soc_start_time_2_64_80 = 0
                soc_start_time_2_64_100 = 0
                expected_charge_time_2_64_80 = 0
                charging_2_64_80_completed = False
                charging_2_64_100_completed = False

                soc_start_time_2_76_80 = 0
                soc_start_time_2_76_100 = 0
                expected_charge_time_2_76_80 = 0
                charging_2_76_80_completed = False
                charging_2_76_100_completed = False
                cte_first_execution = True

        '''
        try:
            compare_result(deviation_80, ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE)
            compare_result(expected_result, actual_result)
        except AssertionError as err:
            logger.error(f"Error is: {err}")
        
        logger.info(f"\nCTE Status: {lib.cte_status}")
        logger.info(f"\ndeviation_80: {deviation_80}")
        logger.info(f"\ndeviation_100: {deviation_100}")
        logger.info(f"\ndeviation_350_80: {deviation_350_80}")
        logger.info(f"\ndeviation_350_100: {deviation_350_100}")
        logger.info(f"\ndeviation_50_80: {deviation_50_80}")
        logger.info(f"\ndeviation_50_100: {deviation_50_100}")
        logger.info(f"\ndeviation_10_9_80: {deviation_10_9_80}")
        logger.info(f"\ndeviation_10_9_100: {deviation_10_9_100}")
        logger.info(f"\ndeviation_10_80: {deviation_10_80}")
        logger.info(f"\ndeviation_10_100: {deviation_10_100}")
        logger.info(f"\ndeviation_2_45_80: {deviation_2_45_80}")
        logger.info(f"\ndeviation_2_45_100: {deviation_2_45_100}")
        logger.info(f"\ndeviation_2_88_80: {deviation_2_88_80}")
        logger.info(f"\ndeviation_2_88_100: {deviation_2_88_100}")
        logger.info(f"\ndeviation_2_64_80: {deviation_2_64_80}")
        logger.info(f"\ndeviation_2_64_100: {deviation_2_64_100}")
        logger.info(f"\ndeviation_2_76_80: {deviation_2_76_80}")
        logger.info(f"\ndeviation_2_76_100: {deviation_2_76_100}")
        logger.info(f"\ndeviation_3_2_80: {deviation_3_2_80}")
        logger.info(f"\ndeviation_3_2_100: {deviation_3_2_100}")
        '''

        # Write results into csv
        module_path = abspath(__file__)
        _OUTPUT = "test_data/time_based_data/output_data"

        dir_path = join(dirname(module_path), _OUTPUT)
        csv_path = join(dir_path, f"processed_CTE_{_FILENAME}")
        write_output_to_excel(results, csv_path)
