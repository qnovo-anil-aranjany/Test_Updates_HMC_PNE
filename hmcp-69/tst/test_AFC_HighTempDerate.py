"""Test Module Description:
    Test module for HighTempDerate

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.12.4
    - Pytest version >= 8.0.1
"""
import math
from typing import Any

from python_calamine import CalamineWorkbook

from .__main__ import *

_MODULE_PATH = abspath(__file__)

ffi = cffi.FFI()
SKIP_TEST = False
MAKE_HTML = True

_MAX_CURRENT = 331600

def iter_excel_calamine(file_path, sheet_name=None):
    print(f"iter_excel_calamine {file_path}")
    workbook = CalamineWorkbook.from_path(file_path)

    if sheet_name:
        rows = iter(workbook.get_sheet_by_name(sheet_name).to_python())
    else:
        rows = iter(workbook.get_sheet_by_index(0).to_python())

    headers = list(map(str, next(rows)))
    for row in rows:
        yield dict(zip(headers, row))
    workbook.close()


if not SKIP_TEST:
    _FILENAME = "high_temp_derate_data.xlsx"

    def parse_AFC_high_temp_derate_data(sheet_name=None):
        file_path = join(dirname(_MODULE_PATH), "test_data", _FILENAME)
        print(file_path)
        test_cases = []
        soc = 0
        for row in iter_excel_calamine(file_path, sheet_name=sheet_name):
            for key, value in row.items():
                temp = float(key)
                ratio = float(value)
                if math.isclose(ratio, 1.0, abs_tol=1e-6):
                    ratio = 1
                test_case = {
                    "Inputs": {
                        "soc": soc,
                        "temp": temp,
                        "ratio": ratio,
                        "output": ratio,
                    },
                    "Expected": {},
                }
                test_cases.append(test_case)
            soc += 5
        return test_cases

    # HTD configurations: (sheet_name, initial_temp)
    HTD_CONFIGS = [
        ("HTD0", -150),
        ("HTD1", 0),
        ("HTD2", 220),
        ("HTD3", 270),
        ("HTD4", 295),
        ("HTD5", 296),
    ]

    # Load all test data with config info
    HTD_TEST_DATA = []
    for sheet_name, initial_temp in HTD_CONFIGS:
        test_cases = parse_AFC_high_temp_derate_data(sheet_name=sheet_name)
        for test_case in test_cases:
            HTD_TEST_DATA.append((sheet_name, initial_temp, test_case))

    def set_afc_inputs(lib, ffi):
        """Helper to call fs_API_SetInputsAFC with all parameters"""
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

    @pytest.mark.parametrize("sheet_name,initial_temp,test_case", HTD_TEST_DATA)
    def test_AFC_HighTemp_Derate(lib: Any, setup_parameters, sheet_name, initial_temp, test_case):
        """
        Verification of AFC_HiTemperatureDerate function for all HTD configurations.
        """
        # Initial setup with config-specific temperature
        lib.VeAPI_T_MaxTempSnsr = initial_temp
        set_afc_inputs(lib, ffi)
        lib.fs_API_SelectHTDParameters()

        # Set test-specific values
        lib.VeAPI_T_MaxTempSnsr = int(10 * test_case["Inputs"]["temp"])
        lib.VeAFC_I_ChgPackCurr = _MAX_CURRENT
        lib.VeAPI_Pct_PackSOC = int(100 * test_case["Inputs"]["soc"])
        print(f"Temp set is: {lib.VeAPI_T_MaxTempSnsr}")
        print(f"soc set is : {lib.VeAPI_Pct_PackSOC}")

        # Run function
        set_afc_inputs(lib, ffi)
        lib.fs_API_AttemptDerateChgCurr()

        actual = lib.VeAFC_I_ChgPackCurr
        expected = test_case["Inputs"]["output"] * _MAX_CURRENT
        print(f"ACTUAL : {actual}")
        print(f"EXPECTED   : {int(expected)}")

        # Accommodate minor differences
        if abs(int(expected) - actual) == 1:
            expected = actual

        compare_result(int(expected), actual)