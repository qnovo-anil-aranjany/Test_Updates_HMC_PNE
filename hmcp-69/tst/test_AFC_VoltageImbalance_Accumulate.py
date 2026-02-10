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
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [999999]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [999999]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 1,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [
                        999999
                    ]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [1] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort": [0]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations": [0]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags": [0] * _NUM_SE,
                },
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Check if initialization function working correctly, prefill it with junk values."
                ),
            ],
        ),
    ],
)

def test_AFC_VoltageImbalance_VMInit(lib, setup_parameters, test_cases) -> None:
    """
    Verify VM init for Voltage Imbalance functionality code.
    """
    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    lib.AFC_VoltageImbalance_VMInit()

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


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "NumExecution": 2,
                    "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": 2,
                    "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VaAPI_U_CellVolts": [3200] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3200]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Normal working condition, accumulated voltages and met sufficient sample time."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "NumExecution": 1,
                    "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": 2,
                    "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": 1,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VaAPI_U_CellVolts": [3200] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Attempt to accumulate but did not meet threshold for valid sample increment."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "NumExecution": 2,
                    "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": 2,
                    "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": 2,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [0] * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VaAPI_U_CellVolts": [3200] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [3200]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VeAFC_e_ErrorFlags": 0,
                },
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Accumulating SE voltages, but not sufficient sample time."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "NumExecution": 1,
                    "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": 2,
                    "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": 3,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 201,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [1999999999]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VaAPI_U_CellVolts": [3200] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [1999999999]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VeAFC_e_ErrorFlags": 4096,
                },
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "Check for execution counter overflow warning, will only send out a warning that Ve_Cnt_ExecutionCounter is near overflow."
                ),
            ],
        ),
        param(
            {
                "Inputs": {
                    "NumExecution": 100,
                    "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": 2,
                    "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": 3,
                    "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": 0,
                    "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": 0,
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [1999999999]
                    * _NUM_SE,
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 0,
                    "VaAPI_U_CellVolts": [3200] * _NUM_SE,
                },
                "Expected": {
                    "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [
                        1999999999 + 3200
                    ]
                    * _NUM_SE,  # todo: this comparison is not working as expected
                    "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": 1,
                    "VeAFC_e_ErrorFlags": 8192,
                },
            },
            id="Test_Case_5",
            marks=[
                mark.description(
                    "Check for accumulation overflow risk prevention, will not allow Va_U_SE_ChargeVoltageSums to overflow even with a lot of execution."
                ),
            ],
        ),
    ],
)

def test_AFC_VoltageImbalance_Accumulate(lib, setup_parameters, test_cases) -> None:
    """
    Verify functionality for accumulate within voltage imbalance code base.
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
    for i in range(test_cases["Inputs"]["NumExecution"]):
        lib.AFC_VoltageImbalance_Accumulate()

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
if RUN_STACK_PARAM_TESTS:
    _NUM_SE = 192
    param_inputs = {
        "NumExecution": [0, 1, 2],
        "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample": [1, 2],
        "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime": [0, 1, 2],
        "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter": [0],
        "AFC_VM_VoltageImbalance.Ve_t_SamplingTime": [0],
        "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums": [
            ([x] * _NUM_SE) for x in [0, 1999999999]
        ],
        "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis": [0, 1],
        "VaAPI_U_CellVolts": [([x] * _NUM_SE) for x in [3200]],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)

    def test_AFC_VoltageImbalance_Accumulate_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input
        conditions to achieve improved code coverage.
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
        for i in range(test_cases["Inputs"]["NumExecution"]):
            lib.AFC_VoltageImbalance_Accumulate()

        dict_record = {"NumExecution": test_cases["Inputs"]["NumExecution"]}

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            validate_test_cases(
                lib, test_cases, read_json_results, dict_to_compare=dict_record
            )

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
                "AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample",
                "AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime",
                "AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter",
                "AFC_VM_VoltageImbalance.Ve_t_SamplingTime",
                "AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums",
                "AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis",
                "VaAPI_U_CellVolts",
                "VeAFC_e_ErrorFlags",
            ]

            record_test_data(
                lib,
                test_cases,
                write_json_results,
                var_to_record=vars_record,
                dict_to_record=dict_record,
            )
