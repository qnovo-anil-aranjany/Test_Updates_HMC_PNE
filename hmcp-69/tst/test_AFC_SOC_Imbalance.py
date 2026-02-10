"""Test Module Description:
    Test module for 'AFC_LogSocImbalanceEvent' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'AFC_LogSocImbalanceEvent'
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

data_ptr = ffi.new("uint16_t *")

@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 255,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 1,
                    "cell_id": 1,
                },
                "Expected": {
                    "cycle_count": 255,
                    "cell_id": 1,
                },
            },
            id="test_case_log_soc_ombalance_1",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 5,
                    "cell_id": 2,
                },
                "Expected": {
                    "cycle_count": 2,
                    "cell_id": 2,
                },
            },
            id="test_case_log_soc_ombalance_2",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 2"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 10,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                    "cell_id": 3,
                },
                "Expected": {
                    "cycle_count": 10,
                    "cell_id": 3,
                },
            },
            id="test_case_log_soc_ombalance_3",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 3"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 100,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                    "cell_id": 4,
                },
                "Expected": {
                    "cycle_count": 100,
                    "cell_id": 4,
                },
            },
            id="test_case_log_soc_ombalance_4",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 4"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 110,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 0,
                    "cell_id": 5,
                },
                "Expected": {
                    "cycle_count": 110,
                    "cell_id": 5,
                },
            },
            id="test_case_log_soc_ombalance_5",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 5"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 316,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "cell_id": 6,
                },
                "Expected": {
                    "expected_temp": [-4377, -4377, -4377, -4377, -4377],
                    "cycle_count": 316,
                    "cell_id": 6,
                },
            },
            id="test_case_log_soc_ombalance_6",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 6"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 65535,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "cell_id": 191,
                },
                "Expected": {
                    "expected_temp": [-4377, -4377, -4377, -4377, -4377],
                    "cycle_count": 65535,
                    "cell_id": 191,
                },
            },
            id="test_case_log_soc_ombalance_7",
            marks=[
                mark.description(
                    "This test case check for soc imbalance buffer handle for initial test cell_id 191"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 65536,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "cell_id": 191,
                },
                "Expected": {
                    "expected_temp": [-4377, -4377, -4377, -4377, -4377],
                    "cycle_count": 65535,
                    "cell_id": 191,
                },
            },
            id="test_case_log_soc_ombalance_8",
            marks=[
                mark.description("This test case check for overflow error"),
            ],
        ),
    ],
)

def test_AFC_Log_SOC_Imbalance_event(lib, setup_parameters, test_cases) -> None:
    """
    Verify SOC imbalance is correctly logged.
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

        # logging event call method AFC_LogSocImbalanceEvent
        lib.AFC_LogSocImbalanceEvent(test_cases["Inputs"]["cell_id"])

        ele_addr = ffi.new("uint8_t [3]")
        obj = ffi.addressof(
            lib.AFC_LoggingTrack[0], "Ne_Afc_Soc_Imbalance_Logging_Circ_Buff_Handle"
        )
        num_elements_inserted = data_ptr
        lib.LIB_CircBuffNumElementsInserted(obj, num_elements_inserted)
        print(f"\nElements Inserted: {num_elements_inserted[0]}")

        # Get recent inserted element
        lib.LIB_CircBuffGetElement(obj, 0, ele_addr)

        py_list = ffi.unpack(ele_addr, 3)
        actual_cycle_count = int.from_bytes(
            bytes(py_list[:2]), byteorder="little", signed=False
        )
        print(f"\nActual Cycle Count logged: {actual_cycle_count}")
        expected_cycle_id = test_cases["Expected"]["cycle_count"]
        compare_result(expected_cycle_id, actual_cycle_count)

        actual_cell_id = int.from_bytes(
            bytes(py_list[2:]), byteorder="little", signed=False
        )
        print(f"\nActual cell_id logged: {actual_cell_id}")
        expected_cell_id = test_cases["Expected"]["cell_id"]
        compare_result(expected_cell_id, actual_cell_id)

    except OverflowError:
        print("\nAn overflow of assigned variable occurred")
    else:
        pass
