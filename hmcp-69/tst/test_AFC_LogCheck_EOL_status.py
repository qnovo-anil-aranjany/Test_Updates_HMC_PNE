"""Test Module Description:
    Test module for verifying EOL condition via unit test in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'AFC_MainPrdc'
    functions for the fast charging algorithm calculate EOL status.

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


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 0,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 1,
                    "highest_index": 60,
                },
                "Expected": {
                    "highest_index": 60,
                    "total_mitigations": 60,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_1",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 60, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 5,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 5,
                    "highest_index": 54,
                },
                "Expected": {
                    "highest_index": 54,
                    "total_mitigations": 114,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_2",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 114, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 10,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                    "highest_index": 62,
                },
                "Expected": {
                    "highest_index": 62,
                    "total_mitigations": 174,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_3",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 174, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 15,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 14,
                    "highest_index": 60,
                },
                "Expected": {
                    "highest_index": 60,
                    "total_mitigations": 234,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_4",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 234, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 20,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 3,
                    "highest_index": 59,
                },
                "Expected": {
                    "highest_index": 59,
                    "total_mitigations": 293,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_5",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 293, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 316,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "highest_index": 60,
                },
                "Expected": {
                    "highest_index": 60,
                    "total_mitigations": 353,
                    "eol_status": 0,
                },
            },
            id="test_case_logcorridxevent_6",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 353, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 317,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "highest_index": 50,
                },
                "Expected": {
                    "highest_index": 50,
                    "total_mitigations": 403,
                    "eol_status": 1,
                },
            },
            id="test_case_logcorridxevent_7",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 403, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 318,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 10,
                    "highest_index": 58,
                },
                "Expected": {
                    "highest_index": 58,
                    "total_mitigations": 461,
                    "eol_status": 1,
                },
            },
            id="test_case_logcorridxevent_8",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 461, eol status is 0"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 319,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 8,
                    "highest_index": 61,
                },
                "Expected": {
                    "highest_index": 61,
                    "total_mitigations": 522,
                    "eol_status": 1,
                },
            },
            id="test_case_logcorridxevent_9",
            marks=[
                mark.description(
                    "This test case check for eol (end of life) status for total mitigations 6522, eol status is 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "cell_volts_temp": [np.uint16(0) for _ in range(192)],
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 320,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 4,
                    "highest_index": 1,
                },
                "Expected": {
                    "highest_index": 1,
                    "total_mitigations": 523,
                    "eol_status": 1,
                },
            },
            id="test_case_logcorridxevent_10",
            marks=[
                mark.description(
                    "This test case check for log buffer handle for fourth insertion"
                    "SAD value is 1, volt value is defau;t for all cells (0)"
                ),
            ],
        ),
    ],
)
def test_AFC_logCorrIdxEvent_eol_check(lib, setup_parameters, test_cases) -> None:
    """
    Check for EOL warnings for logging, when charge cycle reach expected life term.
    """
    try:
        set_lib_inputs(lib, test_cases)

        lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx[lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum] = (
            test_cases
        )["Inputs"]["highest_index"]
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
        lib.f_AFC_MainPrdc(False)
        print(f"\nEOL Flag : {lib.s_AFC_Track.Ne_b_EOLFlag}")

        expected_eol_flag = test_cases["Expected"]["eol_status"]
        actual_eol_flag = lib.s_AFC_Track.Ne_b_EOLFlag
        compare_result(expected_eol_flag, actual_eol_flag)
    except OverflowError:
        print("\nAn overflow of assigned variable occurred")
