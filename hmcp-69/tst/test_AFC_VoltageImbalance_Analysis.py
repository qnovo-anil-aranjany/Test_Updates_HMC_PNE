"""Test Module Description:
    Test module for AFC Voltage Imbalance.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""


from .__main__ import *

ffi = cffi.FFI()

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

RUN_STACK_PARAM_TESTS = True  # Set True to run stack-parametrized testing.
LOG_STACK_PARAM_INPUTS = False  # Set True to log stack-parametrized inputs into html.
WRITE_STACK_PARAM_RESULTS = (
    False  # Set True to write stack-parametrized results into JSON.
)
MAKE_HTML = True
if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


_NUM_SE = 10


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3204, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Normal working condition, detected one SE with voltage imbalances."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3179, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Normal working condition, detected two SE with voltage imbalances."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3179, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3179, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Analysis flag was not ready."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3179, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [3200] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [3500] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [1] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "Check robustness of function if volatile carried over from previous run or if it contained unintended values."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 16384,
                },
            },
            id="Test_Case_5",
            marks=[
                mark.description(
                    "Set VoltageSumMAD to 0 and trigger warning."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 4,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 8,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3204, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 16384,
                },
            },
            id="Test_Case_6",
            marks=[
                mark.description(
                    "Set Ve_t_SamplingTime to 0 and trigger warning."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "KeINP_n_MaxNumCells": _NUM_SE,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": 0,
                    "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": 0,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3201, 3202, 3179, 3203, 3204, 3205, 3206, 3207, 3208, 3209],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "VeAFC_e_ErrorFlags": 16384,
                },
            },
            id="Test_Case_7",
            marks=[
                mark.description(
                    "Set Le_U_VoltageImbalanceThreshold to 0 and trigger warning."
                ),
            ],
        ),
    ],
)
# @allure.feature(
#     """
#         JIRA-ID: QAFC-90, QAFC-91, QAFC-92, QAFC-93, QAFC-94, QAFC-95, QAFC-96, QAFC-97, QAFC-98, QAFC-99, QAFC-100,\
#         QAFC-102, QAFC-104, QAFC-105, QAFC-106, QAFC-107, QAFC-108, QAFC-109, QAFC-110, QAFC-111, QAFC-112
#
#         Steps:\
#         Step1: Have the source files ready for generating binary for swc_fast_charge.,\
#         Step2: Generate binary (shared dll using cmake) using cmake,\
#         3: StepInvoke method AFC_MainPrdc from afc binary via cffi using input param Le_T_CellTemp,\
#         Step4: compare output with expected value from input param - sAFC_Calc.Ve_e_QNS_State, Ve_Cnt_PresentStgNum,
#         Ve_I_CV_Curr, Va_b_ValidSampleFlag, Va_U_SampleCellVolt, VeAFC_U_ChgPackVolt, VeAFC_I_ChgPackCurr,\
#         Step5: Test result should match with expected value,
#
#         Source_File_In_Test: swc_afc_algo.c
#         Method_In_Test: AFC_MainPrdc
#
#         parent_suite: swc_fast_charge
#         suite: afc_main_prdc
#         sub_suite: main_prdc
#     """
# )
def test_AFC_VoltageImbalance_Analysis(lib, setup_parameters, test_cases) -> None:
    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    lib.AFC_VoltageImbalance_Analysis()

    # Use these lines for updating testrail when required
    # logger.info(
    #     f"ACTUAL: AFC_Calc.Ve_e_QNS_State={lib.AFC_Calc.Ve_e_QNS_State},"
    #     f"AFC_Calc.Ve_Cnt_PresentStgNum={lib.AFC_Calc.Ve_Cnt_PresentStgNum},"
    #     f"AFC_Calc.Ve_I_CV_Curr={lib.AFC_Calc.Ve_I_CV_Curr},"
    #     f"AFC_Calc.Va_b_ValidSampleFlag={lib.AFC_Calc.Va_b_ValidSampleFlag},"
    #     f"AFC_Calc.Va_U_SampleSEVolt={lib.AFC_Calc.Va_U_SampleSEVolt},"
    #     f"VeAFC_U_ChgPackVolt={lib.VeAFC_U_ChgPackVolt},"
    #     f"VeAFC_I_ChgPackCurr={lib.VeAFC_I_ChgPackCurr}"
    # )

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)


# =======================================================================
# Stack-Parametrized Test Cases for Code Coverage
# =======================================================================
_NUM_SE = 192
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "KeINP_n_MaxNumCells": [_NUM_SE],
        "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel": [0, 2, 4, 8],
        "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor": [0, 2, 4, 8],
        "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": [0, 1],
        "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [[3201, 3202, 3179, 3203, 3204, 3205, 3206, 3207, 3208, 3209] + [3205] * (_NUM_SE - 10)],
        "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [[0] * _NUM_SE],
        "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [[0] * _NUM_SE],
        "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": [0, 1, 2],
        "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [[0] * _NUM_SE],
        "QnovoAFC_Log_VoltageImbalance_ZScore": [[0.0] * _NUM_SE],
        "QnovoAFC_Log_VoltageImbalance_Threshold": [0],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    # @allure.feature(
    #     """
    #         JIRA-ID: QAFC-90, QAFC-91, QAFC-92, QAFC-93, QAFC-94, QAFC-95, QAFC-96, QAFC-97, QAFC-98, QAFC-99, QAFC-100,\
    #         QAFC-102, QAFC-104, QAFC-105, QAFC-106, QAFC-107, QAFC-108, QAFC-109, QAFC-110, QAFC-111, QAFC-112
    #
    #         Steps:\
    #         Step1: StepHave the source files ready for generating binary for swc_fast_charge.,\
    #         Step2: Generate binary (shared dll using cmake) using cmake,\
    #         Step3: Invoke method AFC_MainPrdc from afc binary via cffi using input param Le_T_CellTemp,\
    #         Step4: compare output with expected value from result json file,\
    #         Step5: Test result should match with expected value,
    #
    #         Source_File_In_Test: swc_afc_algo.c
    #         Method_In_Test: AFC_MainPrdc
    #
    #         parent_suite: swc_fast_charge
    #         suite: afc_main_prdc
    #         sub_suite: main_prdc_coverage
    #         label: Integration
    #     """
    # )
    def test_AFC_VoltageImbalance_Analysis_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        set_lib_inputs(lib, test_cases)

        # Run Function
        # ------------------------------------------------
        lib.AFC_VoltageImbalance_Analysis()

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            validate_test_cases(lib, test_cases, read_json_results)

        # Use these lines for updating testrail when required
        # log_for_testrail_update("AFC_MainPrdc")
        # logger.info(
        #     f"ACTUAL: AFC_Calc.Ve_e_QNS_State={lib.AFC_Calc.Ve_e_QNS_State},"
        #     f"AFC_Calc.Ve_Cnt_PresentStgNum={lib.AFC_Calc.Ve_Cnt_PresentStgNum},"
        #     f"AFC_Calc.Ve_I_CV_Curr={lib.AFC_Calc.Ve_I_CV_Curr},"
        #     f"AFC_Calc.Va_b_ValidSampleFlag={lib.AFC_Calc.Va_b_ValidSampleFlag},"
        #     f"AFC_Calc.Va_U_SampleSEVolt={lib.AFC_Calc.Va_U_SampleSEVolt},"
        #     f"VeAFC_U_ChgPackVolt={lib.VeAFC_U_ChgPackVolt},"
        #     f"VeAFC_I_ChgPackCurr={lib.VeAFC_I_ChgPackCurr}"
        # )

        # Log Stack-Parametrized Inputs
        # ------------------------------------------------
        if MAKE_HTML and LOG_STACK_PARAM_INPUTS:
            log_stack_parametrized_inputs(test_cases)

        # Optional: Log Stack-Parametrized Test Data
        # JSON file can be found in /buildoutputs/reports
        # ------------------------------------------------
        if WRITE_STACK_PARAM_RESULTS:
            vars_record = [
                "KeINP_n_MaxNumCells",
                "AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel",
                "AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor",
                "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis",
                "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums",
                "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort",
                "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations",
                "AFC_VM_VoltageImbalance.Ve_t_SamplingTime",
                "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags",
                "QnovoAFC_Log_VoltageImbalance_ZScore",
                "QnovoAFC_Log_VoltageImbalance_Threshold",
                "VeAFC_e_ErrorFlags",
            ]

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record,
            )
