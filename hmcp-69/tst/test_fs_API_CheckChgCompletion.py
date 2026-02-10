"""Test Module Description:
    Test module for 'fs_API_CheckChgCompletion' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_API_CheckChgCompletion'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

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
                    "VeAPI_Pct_PackSOC": 7500,
                    "VeAPI_T_MinTempSnsr": -200,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 331600,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC1_MaxSOC_75.0%_-20.0degC_-15.1degC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE and the charge "
                    "current limit is set to 0A when two specific conditions are met simultaneously: (1) the battery "
                    "pack operates within a temperature range of -20.0°C to -15.1°C, and (2) the SOC reaches or "
                    "exceeds 75.0%. These criteria ensure proper charge termination and current control under cold "
                    "temperature conditions at high charge levels."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 8430,
                    "VeAPI_T_MinTempSnsr": -150,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 331600,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC2_MaxSOC_84.3%_-15.0degC_-10.1degC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE and the charge "
                    "current limit is set to 0A when two specific conditions are met simultaneously: (1) the battery "
                    "pack operates within a temperature range of -15.0°C to -10.1°C, and (2) the SOC reaches or "
                    "exceeds 84.3%. These criteria ensure proper charge termination and current control under cold "
                    "temperature conditions at high charge levels."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9100,
                    "VeAPI_T_MinTempSnsr": -100,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 331600,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC3_MaxSOC_91.0%_-10.0degC_-5.1degC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE and the charge "
                    "current limit is set to 0A when two specific conditions are met simultaneously: (1) the battery "
                    "pack operates within a temperature range of -10.0°C to -5.1°C, and (2) the SOC reaches or "
                    "exceeds 91.0%. These criteria ensure proper charge termination and current control under cold "
                    "temperature conditions at high charge levels."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9530,
                    "VeAPI_T_MinTempSnsr": -50,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 331600,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC4_MaxSOC_95.3%_-5.0degC_-0.1degC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE and the charge "
                    "current limit is set to 0A when two specific conditions are met simultaneously: (1) the battery "
                    "pack operates within a temperature range of -5.0°C to -0.1°C, and (2) the SOC reaches or "
                    "exceeds 95.3%. These criteria ensure proper charge termination and current control under cold "
                    "temperature conditions at high charge levels."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9700,
                    "VeAPI_T_MinTempSnsr": 0,
                    "VeAFC_e_ErrorFlags": 1,
                    "VeAFC_I_ChgPackCurr": 331600,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC5_MaxSOC_97.0%_0.0degC_57.0degC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE and the charge "
                    "current limit is set to 0A when two specific conditions are met simultaneously: (1) the battery "
                    "pack operates within a temperature range of 0.0°C to 57.0°C, and (2) the SOC reaches or "
                    "exceeds 97.0%. These criteria ensure proper charge termination and current control under cold "
                    "temperature conditions at high charge levels."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9700,
                    "VeAPI_T_MinTempSnsr": -200,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC6_Current_Zero_Before_75%_SOC",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag switches to TRUE if the current "
                    "limit reaches 0A before 75.0% SOC at temperature range between -20.0°C and -15.1°C. This can "
                    "happen due to the limitation of the battery accepting more charge at low temperature at a given "
                    "max allow voltage."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 7499,
                    "VeAPI_T_MinTempSnsr": -200,
                    "VeAFC_e_ErrorFlags": 1,
                    "VeAFC_I_ChgPackCurr": 0,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC7_Current_Zero_Before_75%_SOC_with_Error",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag does not switches to TRUE if the "
                    "current limit reaches 0A before 75.0% SOC at temperature range between -20.0°C and -15.1°C, but "
                    "with a warning flag present."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9699,
                    "VeAPI_T_MinTempSnsr": 0,
                    "VeAPI_T_MaxTempSnsr": 570,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
                "Expected": {
                    "VeAFC_b_ChgCompletionFlag": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="TC8_Current_Zero_Before_97%_SOC_at_MaxTemperature",
            marks=[
                mark.description(
                    "This test case verifies that the charge completion boolean flag does not switches to TRUE if the "
                    "current limit reaches 0A before 97.0% SOC at temperature range between 0.0°C and 57.0°C, but "
                    "max allowable temperature is reached which is 57.0°C. Due to the derating logic, it could drive "
                    "current limit down to 0A and this ensure that the software does not misinterpret that derate "
                    "current as a charge completion indicator. The derate current is simply to protect the battery "
                    "from overheating."
                ),
                mark.jira_id("QAFC-51"),
            ],
        ),
    ],
)
def test_fs_API_CheckChgCompletion(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_API_CheckChgCompletion' function.
    """

    # Setup Variables
    # ------------------------------------------------
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

    # Run Function
    # ------------------------------------------------
    lib.fs_API_CheckChgCompletion()
    print(f"\nCurrent: {lib.VeAFC_I_ChgPackCurr}, {lib.VeAFC_e_ErrorFlags}")


    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)


# =======================================================================
# Stack-Parametrized Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "VeAPI_Pct_PackSOC": [50, 7900, 10000],
        "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": [0, 20, 22, 25],
        "s_AFC_Calc.VeAFC_e_QNS_State": [0, 1, 2],
        "VaAPI_U_CellVolts": [([x] * 10) for x in [0, 3500, 4200, 4500]],
        "VeAPI_T_MinTempSnsr": [0, 360],
        "VeAPI_T_MaxTempSnsr": [550, 990],
        "KeINP_n_MaxNumCells": [1, 10],
        "Le_b_CPVTrackingFlag": [0, 1],
    }
    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_f_AFC_MainPrdc_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        tracking_flag = test_cases["Inputs"]["Le_b_CPVTrackingFlag"]
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
        lib.f_AFC_MainPrdc(tracking_flag)

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            if lib.s_AFC_Calc.VeAFC_I_CV_Curr >= 1590138752:
                pytest.xfail(
                    "Known issue where signed to unsigned changes 's_AFC_Calc.VeAFC_I_CV_Curr' results from -1000A."
                )
            else:
                validate_test_cases(lib, test_cases, read_json_results)

        # Log Stack-Parametrized Inputs
        # ------------------------------------------------
        if MAKE_HTML and LOG_STACK_PARAM_INPUTS:
            log_stack_parametrized_inputs(test_cases)

        # Optional: Log Stack-Parametrized Test Data
        # JSON file can be found in /buildoutputs/reports
        # ------------------------------------------------
        if WRITE_STACK_PARAM_RESULTS:
            vars_record = [
                "s_AFC_Calc.VeAFC_e_QNS_State",
                "s_AFC_Calc.VeAFC_Cnt_PresentStgNum",
                "s_AFC_Calc.VeAFC_I_CV_Curr",
                "s_AFC_Calc.VaAFC_b_ValidSampleFlag",
                "s_AFC_Calc.VaAFC_U_SampleCellVolt",
                "VeAFC_U_ChgPackVolt",
                "VeAFC_I_ChgPackCurr",
            ]

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record
            )
