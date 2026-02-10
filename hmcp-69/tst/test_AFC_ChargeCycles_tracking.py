"""Test Module Description:
    Test module for 'AFC_KeepTrackOfChrgCycles' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'AFC_KeepTrackOfChrgCycles'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

ffi = cffi.FFI()
MAKE_HTML = True

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
                    "VeAPI_Pct_PackSOC": 0,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 0,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 0,
                },
            },
            id="test_case_track_chargecycle_1",
            marks=[
                mark.description(
                    "This test case check for first time setting for Ne_Cnt_SocIncrAccum,"
                    "which is 0 with current implementation logic"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 1000,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 1000,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 0,
                },
            },
            id="test_case_track_chargecycle_2",
            marks=[
                mark.description(
                    "This test case check for second time setting for Ne_Cnt_SocIncrAccum,"
                    "which is an increment from previous with current implementation logic for 1000,"
                    "current_soc > previous_soc, soc_increment = current_soc - previous_soc, and soc_increment < 10K"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 10000,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 0,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 1,
                },
            },
            id="test_case_track_chargecycle_3",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 100%,"
                    "where Ne_Cnt_SocIncrAccum is set back to 0 and charge cycle is incremented by 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 10,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 0,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 1,
                },
            },
            id="test_case_track_chargecycle_4",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 10% for next charging,"
                    "At this point previous_soc is 10K, and in algorithm we just set the previous soc to current soc"
                    "no other changes to other data points"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 15,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 5,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 1,
                },
            },
            id="test_case_track_chargecycle_5",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 15%%,"
                    "where Ne_Cnt_SocIncrAccum is current_soc - previous_soc(15-10), and charge cycle is same as 1"
                    "previous_soc is set to 15 (current_soc)"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 10000,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 9990,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 1,
                },
            },
            id="test_case_track_chargecycle_6",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 100%,"
                    "where Ne_Cnt_SocIncrAccum is current_soc - previous_soc + Ne_Cnt_SocIncrAccum (10000 - 15 + 5),"
                    " previous_soc is set to 10K, and charge cycle is 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 100,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 9990,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 1,
                },
            },
            id="test_case_track_chargecycle_7",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 100%, previous_soc at this point is 10K"
                    "since current soc is 100, no changes other than setting previous_soc to 100 internally"
                    "where Ne_Cnt_SocIncrAccum is retained as 9990 and charge cycle is 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 200,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 90,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 2,
                },
            },
            id="test_case_track_chargecycle_8",
            marks=[
                mark.description(
                    "This test case check Ne_Cnt_SocIncrAccum reaching 100%, previous_soc at this point is 100"
                    "where Ne_Cnt_SocIncrAccum is Ne_Cnt_SocIncrAccum + (cur_soc - previous_soc): 9990 + 200 - 100"
                    "Ne_Cnt_SocIncrAccum > 10K so Ne_Cnt_SocIncrAccum is set to Ne_Cnt_SocIncrAccum - 10K"
                    "and charge cycle is incremented by 1"
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 2000000,
                },
                "Expected": {
                    "s_AFC_Track.Ne_Cnt_SocIncrAccum": 90,
                    "s_AFC_Track.Ne_Cnt_ChargeCycleNum": 2,
                },
            },
            id="test_case_track_chargecycle_9",
            marks=[
                mark.description(
                    "This test case packsoc is already 100% There is no effect for Ne_Cnt_SocIncrAccum"
                    "charge cycle num is reatined as 2"
                ),
            ],
        ),
    ],
)
def test_AFC_TrackChargeCycles(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'AFC_CheckChgCompletion' function.
    """

    # Setup Variables
    # ------------------------------------------------
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
        #print(f"\nPrevious SOC: {lib.Le_Pct_Previous_SOC}")

        lib.AFC_KeepTrackOfChrgCycles(test_cases["Inputs"]["VeAPI_Pct_PackSOC"])
    except OverflowError:
        print("\nAn overflow of assigned variable occurred")
    else:
        print(
            f"\nlib.AFC_Track.Ne_Cnt_SocIncrAccum: {lib.s_AFC_Track.Ne_Cnt_SocIncrAccum}"
        )
        expected = test_cases["Expected"]["s_AFC_Track.Ne_Cnt_SocIncrAccum"]
        actual = lib.s_AFC_Track.Ne_Cnt_SocIncrAccum
        compare_result(expected, actual)

        expected = test_cases["Expected"]["s_AFC_Track.Ne_Cnt_ChargeCycleNum"]
        actual = lib.s_AFC_Track.Ne_Cnt_ChargeCycleNum
        compare_result(expected, actual)
        print(
            f"\nAFC_Track->Ne_Cnt_ChargeCycleNum: {lib.s_AFC_Track.Ne_Cnt_ChargeCycleNum}"
        )
