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
                    "VeAPI_Pct_PackSOC": 0,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.752060565,
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
                    "VeAPI_Pct_PackSOC": 1000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.780961736,
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
                    "VeAPI_Pct_PackSOC": 2000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.809862908,
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
                    "VeAPI_Pct_PackSOC": 3000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.83876408,
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
                    "VeAPI_Pct_PackSOC": 4000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.867665252,
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
                    "VeAPI_Pct_PackSOC": 5000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.896566423,
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
                    "VeAPI_Pct_PackSOC": 6000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.925467595,
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
                    "VeAPI_Pct_PackSOC": 7000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.954368767,
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
                    "VeAPI_Pct_PackSOC": 8000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 0.983269939,
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
                    "VeAPI_Pct_PackSOC": 9000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 1.01217111,
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
                    "VeAPI_Pct_PackSOC": 10000,
                },
                "Expected": {
                    "Le_r_CurrRatio": 1.041072282,
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
    ],
)
def test_fs_AFC_CalcCurrRatio_behavioral(lib, test_cases, setup_parameters) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_AFC_CalcTemperatureRatio' function.
    """

    # Setup Variables
    # ------------------------------------------------
    lib.VeAPI_Cap_ChgPackCapcty = 1
    lib.VeAPI_I_PackCurr = 1
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
    Le_r_CurrRatio = lib.fs_AFC_CalcCurrRatio()

    # Compare Results
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["Le_r_CurrRatio"], Le_r_CurrRatio)


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
