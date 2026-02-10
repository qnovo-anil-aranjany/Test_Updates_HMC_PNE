"""Test Module Description:
    Test module for 'fs_AFC_CalcTemperatureRatio' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_CalcTemperatureRatio'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .main import *

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

RUN_STACK_PARAM_TESTS = False  # Set True to run stack-parametrized testing.
LOG_STACK_PARAM_INPUTS = True  # Set True to log stack-parametrized inputs into html.
WRITE_STACK_PARAM_RESULTS = (
    False  # Set True to write stack-parametrized results into JSON.
)

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": -300,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 31.29782766,
                },
            },
            id="Test_Case_1_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 249,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 1.156358124,
                },
            },
            id="Test_Case_2_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 250,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 1.152729559,
                },
            },
            id="Test_Case_3_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 251,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 1.149126425,
                },
            },
            id="Test_Case_4_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 299,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 1.002568758,
                },
            },
            id="Test_Case_5_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 300,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 1.0,
                },
            },
            id="Test_Case_6_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 301,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 0.997448644,
                },
            },
            id="Test_Case_7_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 349,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 0.893206067,
                },
            },
            id="Test_Case_8_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 350,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 0.891372187,
                },
            },
            id="Test_Case_9_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 351,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 0.889550573,
                },
            },
            id="Test_Case_10_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "Le_T_CellTemp": 570,
                },
                "Expected": {
                    "Le_r_TemperatureRatio": 0.691555515,
                },
            },
            id="Test_Case_11_MatchEquation",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_fs_AFC_CalcTemperatureRatio_behavioral(lib, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_AFC_CalcTemperatureRatio' function.
    """

    # Setup Variables
    # ------------------------------------------------
    lib.s_AFC_Calc.VeAFC_T_StdU_RefCellTemp = lib.s_AFC_Param.KeAFC_T_RefTemp / 10.0
    Le_T_CellTemp = test_cases["Inputs"]["Le_T_CellTemp"]
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    Le_r_TemperatureRatio = lib.fs_AFC_CalcTemperatureRatio(Le_T_CellTemp)

    # Compare Results
    # ------------------------------------------------
    compare_result(
        test_cases["Expected"]["Le_r_TemperatureRatio"], Le_r_TemperatureRatio
    )


# =======================================================================
# Stack-Parametrized Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {}

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_CalcTemperatureRatio_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        set_lib_inputs(lib, test_cases)

        lib.fs_API_SetInputsAFC(
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
            ffi.addressof(lib, "VaAFC_Cmp_CTE_Info"),
            ffi.addressof(lib, "VeAFC_e_ErrorFlags"),
            ffi.addressof(lib, "VeAFC_I_ChgPackCurr"),
            ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
            ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
        )

        # Run Function
        # ------------------------------------------------

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            validate_test_cases(lib, test_cases, read_json_results)

        # Log Stack-Parametrized Inputs
        # ------------------------------------------------
        if MAKE_HTML and LOG_STACK_PARAM_INPUTS:
            log_stack_parametrized_inputs(test_cases)

        # Optional: Log Stack-Parametrized Test Data
        # JSON file can be found in /buildoutputs/reports
        # ------------------------------------------------
        if WRITE_STACK_PARAM_RESULTS:
            vars_record = []

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record
            )
