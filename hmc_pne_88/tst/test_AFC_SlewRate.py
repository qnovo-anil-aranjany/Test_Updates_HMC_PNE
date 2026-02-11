"""Test Module Description:
    Test module for HIghTempDerate

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.12.4
    - Pytest version >= 8.0.1
"""
from typing import Any

from .main import *

# for time based tests
_MODULE_PATH = abspath(__file__)

ffi = cffi.FFI()
SKIP_TEST = False
MAKE_HTML = True
_MAX_CURRENT = 331600
_FILENAME = "slewrate_data.xlsx"


def parse_AFC_slew_rate_data(sheet_name=None):
    file_path = join(dirname(_MODULE_PATH), "test_data", _FILENAME)
    test_cases = []
    for row in iter_file(file_path, sheet_name=sheet_name):
        max_temp_snsr = int(row["MaxTempSnsr"])
        pack_soc = int(row["PackSOC"])
        pack_curr = int(row["PackCurr"])
        call_htd = int(row["call_htd"])
        loop = int(row["loop"])
        logger.info(f"\nloop", loop)
        chg_pack_curr = [int(item) for item in ast.literal_eval(row["ChgPackCurr"])]
        test_case = {
            "Inputs": {
                "max_temp_snsr": max_temp_snsr,
                "pack_curr": pack_curr,
                "pack_soc": pack_soc,
                "call_htd": call_htd,
                "loop": loop,
            },
            "Expected": {"chg_pack_curr": chg_pack_curr},
        }
        test_cases.append(test_case)
    return test_cases


if not SKIP_TEST:
    test_cases = parse_AFC_slew_rate_data()
    logger.info(test_cases)

    @pytest.mark.parametrize("test_case", test_cases)
    def test_AFC_SlewRate_coverage(lib: Any, test_case):
        """
        This test function performs verification of specific operating conditions relevant to the
        'AFC_HiTemperatureDerate' function.
        """
        logger.info(test_case)
        for i in range(test_case["Inputs"]["loop"]):
            lib.VeAPI_T_MaxTempSnsr = test_case["Inputs"]["max_temp_snsr"]
            lib.VeAPI_Pct_PackSOC = test_case["Inputs"]["pack_soc"]
            lib.VeAPI_I_PackCurr = test_case["Inputs"]["pack_curr"]
            lib.VeAFC_I_ChgPackCurr = _MAX_CURRENT

            # lib.VeAPI_Pct_PackSOC = int(100 * test_cases["Inputs"]["soc"])
            logger.debug(f"Temp set is: {lib.VeAPI_T_MaxTempSnsr}")
            logger.debug(f"soc set is : {lib.VeAPI_Pct_PackSOC}")
            # Run Function
            # ------------------------------------------------
            lib.fs_API_SelectHTDParameters()
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

            logger.debug(f"\nActual temp before: {lib.VeAPI_T_MaxTempSnsr}")
            logger.debug(f"\nActual current before : {lib.VeAFC_I_ChgPackCurr}")
            lib.fs_API_CheckExceedTempRange()
            if (
                "call_htd" in test_case["Inputs"]
                and test_case["Inputs"]["call_htd"] is 1
            ):
                lib.fs_API_AttemptDerateChgCurr()
            actual = lib.VeAFC_I_ChgPackCurr
            expected = test_case["Expected"]["chg_pack_curr"][i]
            compare_result(expected, actual)

    @pytest.mark.parametrize("test_case", test_cases)
    def Atest_AFC_SlewRate_coverage(lib: Any, test_case):
        """
        This test function performs verification of specific operating conditions relevant to the
        'AFC_HiTemperatureDerate' function.
        """
        logger.info(test_case)
        for i in range(test_case["Inputs"]["loop"]):
            lib.VeAPI_T_MaxTempSnsr = test_case["Inputs"]["max_temp_snsr"]
            lib.VeAPI_Pct_PackSOC = test_case["Inputs"]["pack_soc"]
            lib.VeAPI_I_PackCurr = test_case["Inputs"]["pack_curr"]
            lib.VeAFC_I_ChgPackCurr = _MAX_CURRENT
            lib.VeAPI_b_PackCurr_DR = 1
            lib.VeAPI_b_MinTempSnsr_DR = 1
            lib.VeAPI_b_MaxTempSnsr_DR = 1
            lib.VeAPI_b_ChgPackCapcty_DR = 1
            lib.VeAPI_b_EVSEChgStatus = 1
            lib.VeAPI_b_PackSOC_DR = 1
            # lib.VeAPI_Pct_PackSOC = int(100 * test_cases["Inputs"]["soc"])
            logger.info(f"\nTemp set is: {lib.VeAPI_T_MaxTempSnsr}")
            logger.info(f"\nsoc set is : {lib.VeAPI_Pct_PackSOC}")
            # Run Function
            # ------------------------------------------------

            lib.Qnovo_AFC_1000ms(
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
                lib.VeAPI_e_EVSEChgLevel,
                ffi.addressof(lib, "VaAFC_Cmp_CTE_Info"),
                ffi.addressof(lib, "VeAFC_e_ErrorFlags"),
                ffi.addressof(lib, "VeAFC_I_ChgPackCurr"),
                ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
                ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
            )
            actual = lib.VeAFC_I_ChgPackCurr
            expected = test_case["Expected"]["chg_pack_curr"][i]
            compare_result(expected, actual)