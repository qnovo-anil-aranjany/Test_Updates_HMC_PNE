"""Test Module Description:
    Test module for 'AFC_LogCorrIdxEvent' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'AFC_LogCorrIdxEvent'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

ffi = cffi.FFI()
MAKE_HTML = True
TOTAL_BYTES = 18

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")

ele_addr = ffi.new("uint8_t [18]")
data_ptr = ffi.cast("uint8_t *", ele_addr)

def get_set_bit_positions(number):
    """
    Returns a list of positions of set bits in the binary representation of a number.
    Positions are 0-indexed from the right (least significant bit).
    """
    if number < 0:
        raise ValueError("Input number must be non-negative.")
    positions = []
    index = 0
    temp_number = number
    while temp_number > 0:
        # Check if the rightmost bit is set
        if (temp_number & 1) == 1:
            positions.append(index)
        # Right shift the number to check the next bit
        temp_number >>= 1
        index += 1
    return positions


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 1,
                    "test_cell_values": [
                        [73, 1, 1],
                        [3, 1, -32768],
                        [23, 1, -13108],
                        [100, 1, 13107],
                        [189, 1, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 0,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 1,
                },
                "Expected": {
                    "expected_indexes": [189, 100, 73, 23, 3],
                    "corr_incr_val": 1,
                    "cycle_count": 0,
                    "stage": 1,
                    "expected_temp": [-4377, 13107, 1, -13108, -32768],
                },
            },
            id="test_case_logcorridxevent_1",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for initial test"
                    "SAD value is 1, volt value is 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 0,
                    "test_cell_values": [
                        [73, 1, 1],
                        [3, 1, -32768],
                        [23, 1, -13108],
                        [100, 1, 13107],
                        [189, 1, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 5,
                },
                "Expected": {
                    "expected_indexes": [189, 100, 73, 23, 3],
                    "corr_incr_val": 0,
                    "cycle_count": 2,
                    "stage": 5,
                    "expected_temp": [-4377, 13107, 1, -13108, -32768],
                },
            },
            id="test_case_logcorridxevent_2",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for second test"
                    "SAD value is 0, volt value is 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 0,
                    "test_cell_values": [
                        [73, 0, 1],
                        [3, 0, -32768],
                        [23, 0, -13108],
                        [100, 0, 13107],
                        [189, 0, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 10,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                },
                "Expected": {
                    "expected_indexes": [191, 190, 189, 188, 187],
                    "corr_incr_val": 0,
                    "cycle_count": 10,
                    "stage": 14,
                    "expected_temp": [-4377, -4377, -4377, -4377, -4377],
                },
            },
            id="test_case_logcorridxevent_3",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for third test"
                    "SAD value is 0, volt value is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 1,
                    "test_cell_values": [
                        [73, 10, 1],
                        [3, 109, -32768],
                        [23, 745, -13108],
                        [100, 1300, 13107],
                        [189, 3000, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 100,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                },
                "Expected": {
                    "expected_indexes": [189, 100, 23, 3, 73],
                    "corr_incr_val": 1,
                    "cycle_count": 100,
                    "stage": 14,
                    "expected_temp": [-4377, 13107, -13108, -32768, 1],
                },
            },
            id="test_case_logcorridxevent_4",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for fourth test"
                    "SAD value is 1, volt value is varies"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 1,
                    "test_cell_values": [
                        [73, 1000, 1],
                        [3, 1000, -32768],
                        [23, 1000, -13108],
                        [100, 1000, 13107],
                        [189, 1000, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 110,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 0,
                },
                "Expected": {
                    "expected_indexes": [189, 100, 73, 23, 3],
                    "corr_incr_val": 1,
                    "cycle_count": 110,
                    "stage": 0,
                    "expected_temp": [-4377, 13107, 1, -13108, -32768],
                },
            },
            id="test_case_logcorridxevent_5",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for fifth test"
                    "SAD value is 1, volt value is same for 5 cells"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "ele_addr": data_ptr,
                    "corr_incr_val": 1,
                    "test_cell_values": [
                        [73, -1, 1],
                        [3, -1, -32768],
                        [23, -1, -13108],
                        [100, -1, 13107],
                        [189, -1, -4377],
                    ],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 316,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                },
                "Expected": {
                    "expected_indexes": [191, 190, 189, 188, 187],
                    "corr_incr_val": 1,
                    "cycle_count": 316,
                    "stage": 11,
                    "expected_temp": [-4377, -4377, -4377, -4377, -4377],
                },
            },
            id="test_case_logcorridxevent_6",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for fourth insertion"
                    "SAD value is 1, volt value is defau;t for all cells (0)"
                ),
            ],
        ),
    ],
)

def test_AFC_LogCorrIdxEvent_log_events(lib, setup_parameters, test_cases) -> None:
    """
    Tests for logging event handling verification
    """
    try:
        set_lib_inputs(lib, test_cases)
        lib.fs_API_SetInputsAFC(
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
        if "test_cell_values" in test_cases["Inputs"]:
            for item in test_cases["Inputs"]["test_cell_values"]:
                i, j, k = item
                if j != -1:
                    lib.cell_volts_temp[i] = j

                lib.s_API_Var.VaAPI_T_TempSnsrs[
                    lib.KaINP_i_Temp2CellIdx[i]
                ] = k
        else:
            print("Provide test_cell_values for test")

        # logging event call method AFC_LogCorrIdxEvent

        lib.AFC_LogCorrIdxEvent(list(lib.cell_volts_temp))


        # Parse log buffer and get result data
        result = process_log_buffer(lib)
        result.print_buffer()

        # Get and compare indexes logged with expected result
        expected_indexes = test_cases["Expected"]["expected_indexes"]
        compare_result(expected_indexes, result.indexes)
        expected_cycle_count = test_cases["Expected"]["cycle_count"]
        compare_result(expected_cycle_count, result.cycle_count)
        expected_stage = test_cases["Expected"]["stage"]
        compare_result(expected_stage, result.stage)
        expected_temp = test_cases["Expected"]["expected_temp"]
        compare_result(expected_temp, result.temperatures)
        # expected_ov_flag = test_cases["Expected"]["corr_incr_val"]
        # compare_result(expected_ov_flag, result.ov_flag)

    except OverflowError:
        print("An overflow of assigned variable occurred")
    else:
        pass
