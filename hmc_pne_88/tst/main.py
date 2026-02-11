"""
 For all imports for test files.
"""

import ast
import faulthandler
import json
import random
import re
import copy
import sys
from itertools import product
from os.path import abspath, dirname, join
from os import makedirs
from pathlib import Path
from typing import Any, Dict, List, Tuple

import allure
import cffi
import numpy as np
import pytest
from cffi import FFI
from pytest import FixtureRequest, fail, fixture, mark, param

from submodules.tool_test_automation.src.common.fixtures import (
    lib,
    read_json_results,
    write_json_results,
)
from submodules.tool_test_automation.src.common.logutil import logger
from submodules.tool_test_automation.src.common.paths import (
    BUILDOUTPUTS_BINARY_PATH,
    BUILDOUTPUTS_SRC_PATH,
    PROJECT_PATH,
    TEST_FRAMEWORK_PATH,
)
from submodules.tool_test_automation.src.common.platforms import *
from submodules.tool_test_automation.src.common.run_venv import populate_envs
from submodules.tool_test_automation.src.common.utils import (
    HeaderDependencyOrder,
    HeaderExtractDeclarations,
    clean_dat_files,
    clean_gcda_files,
    compare_result,
    generate_requirement_link,
    iter_file,
    lib_array_to_list,
    log_for_testrail_update,
    log_stack_parametrized_inputs,
    record_test_data,
    set_lib_inputs,
    size,
    validate_test_cases,
    validate_with_reference_data,
    write_output_to_excel,
    write_output_to_csv,
)

ffi = cffi.FFI()

# for time based tests
_MODULE_PATH = abspath(__file__)
_TIME_BASED_INPUT_DATA = "test_data\\time_based_data\\input_data"
_TIME_BASED_OUTPUT_DATA = "test_data\\time_based_data\\output_data"
_TIME_BASED_REFERENCE_DATA = "test_data\\time_based_data\\reference_data"

#_NVM_ARRAY_SIZE = 17500
_NUM_CELL = 192
_NUM_TEMP_SNSR = 18
_TOTAL_BYTES = 18


"""
ParamDict class is used to get the initial library data before any tests start making changes to the library data.
This is a singleton class. store_initial_param_values will get initial lib data values and store in a dict.
When tests need to be reinitialized to initial library data, tests can use the fixture setup_parameters defined below this class.

When adding a new library data, make sure to add into this class method store_initial_param_values
and setup_parameters fixture defined in this file. 
"""

warning_map = {
    0: "AFC_No_Warnings",
    1: "Warn_AFC_InputsNotReady",
    2: "Warn_AFC_NVMInitFailed",
    3: "Warn_AFC_ExceedChgCurrRange",
    4: "Warn_AFC_ExceedTempRange",
    5: "Warn_AFC_ChgCapacityZero",
    6: "Warn_AFC_ExceedMaxStage",
    7: "Warn_AFC_OverSADVoltLim",
    8: "Warn_AFC_OverSafetyVoltLim",
    9: "Warn_AFC_OverCvVoltLim",
    10: "Warn_AFC_CPVIdxOutOfRange",
    11: "Warn_AFC_TuningLimOOR",
    12: "Warn_AFC_EarlyWarnAging",
    13: "Warn_AFC_AbnormalAging",
    14: "Warn_AFC_ExtremeAging",
}


class LogParseResult:
    def __init__(self):
        self.indexes = []
        self.cycle_count = None
        self.stage = None
        self.highest_index = None
        self.temperatures = []

    def set_indexes(self, value):
        self.indexes = value

    def set_cycle_count(self, value):
        self.cycle_count = value

    def set_stage(self, value):
        self.stage = value

    def set_highest_index(self, value):
        self.highest_index = value

    def set_temperatures(self, value):
        self.temperatures = value

    def print_buffer(self):
        logger.debug(f"Log:  Indexes : {self.indexes}")
        logger.debug(f"Log:  Cycle Count : {self.cycle_count}")
        logger.debug(f"Log:  Stage : {self.stage}")
        logger.debug(f"Log:  Highest Index : {self.highest_index}")
        logger.debug(f"Log:  Temperatures : {self.temperatures}")


class ParamDict:
    __instance = None

    def __new__(cls):
        if ParamDict.__instance is None:
            ParamDict.__instance = super(ParamDict, cls).__new__(cls)
            ParamDict.__instance.initialized = False

        return ParamDict.__instance

    def __init__(self):
        if self.initialized:
            return
        else:
            self.lib = self.lib_util()
            self.param_dict = self.store_initial_param_values()
            self.initialized = True

    @staticmethod
    def lib_util():
        """To load a shared library file for testing.

        Loads the shared library file from the BUILDOUTPUTS path and yields the loaded .dll/.so object.
        Handles cases where no or multiple shared library files are found.
        """

        error_msg = "Shared library loading failed:"

        btype = "customer_build"
        build_type = populate_envs("BUILD_TYPE").lower()
        if build_type == "generic_build":
            btype = "generic_builds"
        swc_component = populate_envs("SW_COMPONENT").lower()
        binary_path = BUILDOUTPUTS_BINARY_PATH / btype / swc_component
        logger.debug(f"binary_path: {binary_path}")
        if LINUX:
            cpath = "config_" + populate_envs("SW_COMPONENT").lower()
            binary_path = TEST_FRAMEWORK_PATH / "cmake" / cpath
        if binary_path == "none":
            logger.error("No binary directory populated into environment")
            return
        logger.debug(f"BINARY_PATH:INIT{binary_path}")
        shared_lib_file = [
            file
            for extension in ["*.dll", "*.so"]
            for file in binary_path.glob(extension)
        ]
        btype = "customer_build"
        build_type = populate_envs("BUILD_TYPE").lower()
        if build_type == "generic_build":
            btype = "generic_builds"
        swc_component = populate_envs("SW_COMPONENT").lower()
        bpath = BUILDOUTPUTS_SRC_PATH / btype / swc_component
        header_files = HeaderDependencyOrder(bpath)

        header_files = header_files.get_dependency_order()
        types_index = None

        for type_file in header_files:
            if "qnovo_types.h" in type_file:
                types_index = header_files.index(type_file)

        if types_index:
            header_files[0], header_files[types_index] = (
                header_files[types_index],
                header_files[0],
            )

        declarations = HeaderExtractDeclarations().get_declarations(header_files)

        #ffi = FFI()
        ffi.cdef(declarations)

        if len(shared_lib_file) == 1:
            clean_gcda_files()
            return ffi.dlopen(str(shared_lib_file[0]))
        elif len(shared_lib_file) == 0:
            error_msg = (
                f"{error_msg} No shared library file found in the specified directory."
            )
            logger.error(error_msg)
            fail(error_msg)
        else:
            error_msg = (
                f"{error_msg} Multiple shared library files found. Expected only one."
            )
            logger.error(error_msg)
            fail(error_msg)

    def store_initial_param_values(self):
        """
        store initial library values into a dict
        :return: p_dict, dictionary with initial library data.
        """
        try:
            print("\n store_initial_param_values")
            ffi = FFI()
            p_dict = {}
            p_dict["VeAPI_b_PackSOC_DR"] = 1
            p_dict["VeAPI_b_PackCurr_DR"] = 1
            p_dict["VaAPI_b_CellVolts_DR"] = [1] * size(self.lib.VaAPI_b_CellVolts_DR)
            p_dict["VaAPI_b_TempSnsrs_DR"] = [1] * size(self.lib.VaAPI_b_TempSnsrs_DR)
            p_dict["VeAPI_b_MinTempSnsr_DR"] = 1
            p_dict["VeAPI_b_MaxTempSnsr_DR"] = 1
            p_dict["VeAPI_b_ChgPackCapcty_DR"] = 1
            # NVM Initialization
            # ------------------------------------------------
            p_dict["VeAFC_b_Initialized"] = 0
            p_dict["VeAPI_b_EVSEChgStatus"] = 1
            p_dict["VeAPI_I_PackCurr"] = 1

            faulthandler.enable(file=sys.stderr)

            self.lib.fs_API_SetInputsAFC(
                self.lib.VaAPI_Cmp_NVMRegion,
                self.lib.VeAPI_I_PackCurr,
                self.lib.VeAPI_b_PackCurr_DR,
                self.lib.VaAPI_U_CellVolts,
                self.lib.VaAPI_b_CellVolts_DR,
                self.lib.VaAPI_T_TempSnsrs,
                self.lib.VaAPI_b_TempSnsrs_DR,
                self.lib.VeAPI_T_MinTempSnsr,
                self.lib.VeAPI_b_MinTempSnsr_DR,
                self.lib.VeAPI_T_MaxTempSnsr,
                self.lib.VeAPI_b_MaxTempSnsr_DR,
                self.lib.VeAPI_Cap_ChgPackCapcty,
                self.lib.VeAPI_b_ChgPackCapcty_DR,
                self.lib.VeAPI_Pct_PackSOC,
                self.lib.VeAPI_b_PackSOC_DR,
                self.lib.VeAPI_b_EVSEChgStatus,
                ffi.addressof(self.lib, "VaAFC_Cmp_CTE_Info"),
                ffi.addressof(self.lib, "VeAFC_e_ErrorFlags"),
                ffi.addressof(self.lib, "VeAFC_I_ChgPackCurr"),
                ffi.addressof(self.lib, "VeAFC_U_ChgPackVolt"),
                ffi.addressof(self.lib, "VeAFC_b_ChgCompletionFlag"),
            )

            self.lib.f_AFC_NVMInit()

            # Calculation
            # ------------------------------------------------
            p_dict["s_AFC_Calc.VeAFC_e_QNS_State"] = 0
            p_dict["s_AFC_Calc.VeAFC_Cnt_PresentStgNum"] = 0
            p_dict["s_AFC_Calc.VeAFC_I_CV_Curr"] = self.lib.s_AFC_Calc.VeAFC_I_CV_Curr
            p_dict["s_AFC_Calc.VaAFC_b_ValidSampleFlag"] = [0] * size(
                self.lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag
            )
            p_dict["s_AFC_Calc.VaAFC_U_SampleCellVolt"] = [0] * size(
                self.lib.s_AFC_Calc.VaAFC_U_SampleCellVolt
            )
            p_dict["VeAPI_T_MinTempSnsr"] = 300
            p_dict["VeAPI_T_MaxTempSnsr"] = 558
            p_dict["s_AFC_Calc.VeAFC_T_StdU_RefCellTemp"] = 350.0 / 10.0

            # Customer Inputs
            # ------------------------------------------------
            p_dict["KeINP_n_MaxNumCells"] = 1
            p_dict["KeINP_n_MaxNumTempSnsrs"] = 1
            p_dict["KaINP_i_Temp2CellIdx"] = [1]
            p_dict["VeAPI_Pct_PackSOC"] = 5000
            p_dict["VeAPI_Cap_ChgPackCapcty"] = 16 * 1000
            random.seed(44)
            noise_mV = 1
            p_dict["VaAPI_U_CellVolts"] = [4200 + int(noise_mV)]
            p_dict["VaAPI_T_TempSnsrs"] = [
                -150 + i * 50 for i in range(size(self.lib.VaAPI_T_TempSnsrs) - 2)
            ]
            p_dict["VeAPI_I_PackCurr"] = 12600
            #p_dict["VeAPI_t_ActualChgTime"] = 1260
            #p_dict["VeAPI_t_DesiredChgTime"] = 1260

            # Customer Outputs
            # ------------------------------------------------
            p_dict["VeAFC_e_ErrorFlags"] = 0
            p_dict["VeAFC_I_ChgPackCurr"] = 0
            p_dict["VeAFC_U_ChgPackVolt"] = 0
            p_dict["VeAFC_b_ChgCompletionFlag"] = 0
            p_dict["KaLIB_U_OCVAxis"] = [self.lib.KaLIB_U_OCVAxis[i] for i in range(36)]
            p_dict["KaLIB_Pct_SOCAxis"] = [
                self.lib.KaLIB_Pct_SOCAxis[i] for i in range(36)
            ]

            # NVM
            # ------------------------------------------------
            size_row, size_col = size(self.lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx )
            p_dict["s_AFC_Track.NtAFC_Cnt_CPVCorrIdx"] = [
                [0] * size_col for _ in range(size_row)
            ]
            size_row, size_col = size(self.lib.s_AFC_Track.NtAFC_U_RefCellVolt)
            p_dict["s_AFC_Track.NtAFC_U_RefCellVolt"] = [
                [0] * size_col for _ in range(size_row)
            ]
            p_dict["s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx"] = [0] * size(
                self.lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx
            )
            p_dict["s_AFC_Calc.VaAFC_U_RefCellVolt"] = [0] * size(
                self.lib.s_AFC_Calc.VaAFC_U_RefCellVolt
            )

            # Parameters/Calibrations, based on Volvo battery cell characterization
            # ------------------------------------------------
            p_dict[
                "sAFC_P.Ve_U_CVFloatCellVolt"
            ] = self.lib.sAFC_P.Ve_U_CVFloatCellVolt
            p_dict[
                "sAFC_P.Ve_U_SafetyMaxVolt"
            ] = self.lib.sAFC_P.Ve_U_SafetyMaxVolt
            p_dict["s_AFC_Param.KeAFC_I_CV_ChgCurr"] = self.lib.s_AFC_Param.KeAFC_I_CV_ChgCurr
            p_dict[
                "s_AFC_Param.KeAFC_I_CV_ChgStepCurr"
            ] = self.lib.s_AFC_Param.KeAFC_I_CV_ChgStepCurr

            p_dict["s_AFC_Param.KaAFC_Pct_Stg_SOC"] = [
                self.lib.s_AFC_Param.KaAFC_Pct_Stg_SOC[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr"] = [
                self.lib.s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KaAFC_I_Stg_ChgMinCurr"] = [
                self.lib.s_AFC_Param.KaAFC_I_Stg_ChgMinCurr[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KaAFC_I_Stg_ChgStepCurr"] = [
                self.lib.s_AFC_Param.KaAFC_I_Stg_ChgStepCurr[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt"] = [
                self.lib.s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt"] = [5] * size(
                self.lib.s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt
            )

            p_dict["s_AFC_Param.KaAFC_U_Stg_SADCellLim"] = [
                self.lib.s_AFC_Param.KaAFC_U_Stg_SADCellLim[i] for i in range(20)
            ]

            p_dict["s_AFC_Param.KeAFC_T_CPV_MaxTempLim"] = 558
            p_dict["s_AFC_Param.KeAFC_T_CPV_MinTempLim"] = 100
            p_dict["s_AFC_Param.KeAFC_T_RefTemp"] = 300
            p_dict["s_AFC_Param.KeAFC_k_Coeff_a"] = 0.000320821
            p_dict["s_AFC_Param.KeAFC_k_Coeff_b"] = -0.025756017
            p_dict["s_AFC_Param.KeAFC_k_Coeff_c"] = 0.000005193
            p_dict["s_AFC_Param.KeAFC_k_Coeff_d"] = 0.50211625
            p_dict["s_AFC_Param.KeAFC_k_Coeff_e"] = 0.008769628
            p_dict["s_AFC_Param.KeAFC_k_Coeff_f"] = 0.539655006
            p_dict["s_AFC_Param.KeAFC_k_Coeff_g"] = -0.012695392
            p_dict["s_AFC_Param.KeAFC_k_Coeff_h"] = 1.3
            '''
            p_dict["AFC_Tunable_Param.Ka_I_Stg_ChgMaxCurr"] = [
                345000,
                345000,
                345000,
                345000,
                345000,
                334000,
                311000,
                290000,
                270000,
                251000,
                232000,
                214000,
                197000,
                180000,
                165000,
                150000,
                136000,
                123000,
                111000,
                100000,
                90000,
                81000,
                72000,
                61000,
                50000,
            ]
            p_dict[
                "INP_Snsr.Ke_Cap_RatedPackCapcity"
            ] = self.lib.INP_Snsr.Ke_Cap_RatedPackCapcity
            p_dict["VaAFC_r_C_rate"] = [
                float(x) / p_dict["INP_Snsr.Ke_Cap_RatedPackCapcity"]
                for x in p_dict["AFC_Param.Ka_I_Stg_ChgMaxCurr"]
            ]
            p_dict["KeAFC_Pct_TunableEndSOC"] = self.lib.KeAFC_Pct_TunableEndSOC
            '''
            return p_dict
        except Exception as e:
            logger.error(f"*** Storing Initial values failed:*** {e}")


@pytest.fixture(scope="function")
def setup_parameters(lib) -> None:
    """This fixture re-initializes the global variables in the specified library module at the beginning of each test
    function. These variables are reset to their initial values for every standard and parametrized test case, ensuring
    consistent test conditions.

    Args:
        lib (module): The shared library module, either a .dll (Windows) or .so (Unix/Linux) file, containing the global
         variables to be initialized.
    """
    logger.debug(
        "Set up parameters which is initialized at the beginning of test execution)"
    )
    ffi = FFI()
    pd = pytest.paramdict

    # Data Ready Signals
    # ------------------------------------------------
    lib.VeAPI_b_PackSOC_DR = pd["VeAPI_b_PackSOC_DR"]
    lib.VeAPI_b_PackCurr_DR = pd["VeAPI_b_PackCurr_DR"]
    lib.VaAPI_b_CellVolts_DR = pd["VaAPI_b_CellVolts_DR"]
    lib.VaAPI_b_TempSnsrs_DR = pd["VaAPI_b_TempSnsrs_DR"]
    lib.VeAPI_b_MinTempSnsr_DR = pd["VeAPI_b_MinTempSnsr_DR"]
    lib.VeAPI_b_MaxTempSnsr_DR = pd["VeAPI_b_MaxTempSnsr_DR"]
    lib.VeAPI_b_ChgPackCapcty_DR = pd["VeAPI_b_ChgPackCapcty_DR"]

    # NVM Initialization
    # ------------------------------------------------
    lib.VeAFC_b_Initialized = pd["VeAFC_b_Initialized"]
    lib.VeAPI_b_EVSEChgStatus = pd["VeAPI_b_EVSEChgStatus"]
    lib.VeAPI_I_PackCurr = pd["VeAPI_I_PackCurr"]

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

    lib.f_AFC_NVMInit()


    # Calculation
    # ------------------------------------------------
    lib.s_AFC_Calc.VeAFC_e_QNS_State = pd["s_AFC_Calc.VeAFC_e_QNS_State"]
    lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum = pd["s_AFC_Calc.VeAFC_Cnt_PresentStgNum"]
    lib.s_AFC_Calc.VeAFC_I_CV_Curr = pd["s_AFC_Calc.VeAFC_I_CV_Curr"]
    lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag = pd["s_AFC_Calc.VaAFC_b_ValidSampleFlag"]
    lib.s_AFC_Calc.VaAFC_U_SampleCellVolt = pd["s_AFC_Calc.VaAFC_U_SampleCellVolt"]
    lib.VeAPI_T_MinTempSnsr = pd["VeAPI_T_MinTempSnsr"]
    lib.VeAPI_T_MaxTempSnsr = pd["VeAPI_T_MaxTempSnsr"]
    lib.s_AFC_Calc.VeAFC_T_StdU_RefCellTemp = pd["s_AFC_Calc.VeAFC_T_StdU_RefCellTemp"]

    # Customer Inputs
    # ------------------------------------------------
    lib.KeINP_n_MaxNumCells = pd["KeINP_n_MaxNumCells"]
    lib.KeINP_n_MaxNumTempSnsrs = pd["KeINP_n_MaxNumTempSnsrs"]
    lib.KaINP_i_Temp2CellIdx = pd["KaINP_i_Temp2CellIdx"]
    lib.VeAPI_Pct_PackSOC = pd["VeAPI_Pct_PackSOC"]
    lib.VeAPI_Cap_ChgPackCapcty = pd["VeAPI_Cap_ChgPackCapcty"]
    lib.VaAPI_U_CellVolts = pd["VaAPI_U_CellVolts"]
    lib.VaAPI_T_TempSnsrs = pd["VaAPI_T_TempSnsrs"]

    # lib.VeAPI_I_PackCurr = pd["VeAPI_I_PackCurr"]

    # Customer Outputs
    # ------------------------------------------------
    lib.VeAFC_e_ErrorFlags = pd["VeAFC_e_ErrorFlags"]
    lib.VeAFC_I_ChgPackCurr = pd["VeAFC_I_ChgPackCurr"]
    lib.VeAFC_U_ChgPackVolt = pd["VeAFC_U_ChgPackVolt"]
    lib.VeAFC_b_ChgCompletionFlag = pd["VeAFC_b_ChgCompletionFlag"]

    # OCV vs. SOC
    # ------------------------------------------------
    lib.KaLIB_U_OCVAxis = pd["KaLIB_U_OCVAxis"]
    lib.KaLIB_Pct_SOCAxis = pd["KaLIB_Pct_SOCAxis"]

    # NVM
    # ------------------------------------------------
    lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx = pd["s_AFC_Track.NtAFC_Cnt_CPVCorrIdx"]
    lib.s_AFC_Calc.VaAFC_U_RefCellVolt = pd["s_AFC_Calc.VaAFC_U_RefCellVolt"]
    lib.s_AFC_Track.NtAFC_U_RefCellVolt = pd["s_AFC_Track.NtAFC_U_RefCellVolt"]
    lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx = pd["s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx"]

    # Parameters/Calibrations, based on Volvo battery cell characterization
    # ------------------------------------------------
    lib.sAFC_P.Ve_U_CVFloatCellVolt = pd["sAFC_P.Ve_U_CVFloatCellVolt"]
    lib.sAFC_P.Ve_U_SafetyMaxVolt = pd["sAFC_P.Ve_U_SafetyMaxVolt"]
    lib.s_AFC_Param.KeAFC_I_CV_ChgCurr = pd["s_AFC_Param.KeAFC_I_CV_ChgCurr"]
    lib.s_AFC_Param.KeAFC_I_CV_ChgStepCurr = pd["s_AFC_Param.KeAFC_I_CV_ChgStepCurr"]
    lib.s_AFC_Param.KaAFC_Pct_Stg_SOC = pd["s_AFC_Param.KaAFC_Pct_Stg_SOC"]
    lib.s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr = pd["s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr"]
    lib.s_AFC_Param.KaAFC_I_Stg_ChgMinCurr = pd["s_AFC_Param.KaAFC_I_Stg_ChgMinCurr"]
    lib.s_AFC_Param.KaAFC_I_Stg_ChgStepCurr = pd["s_AFC_Param.KaAFC_I_Stg_ChgStepCurr"]
    lib.s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt = pd["s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt"]
    lib.s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt = pd["s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt"]
    lib.s_AFC_Param.KaAFC_U_Stg_SADCellLim = pd["s_AFC_Param.KaAFC_U_Stg_SADCellLim"]
    lib.s_AFC_Param.KeAFC_T_CPV_MaxTempLim = pd["s_AFC_Param.KeAFC_T_CPV_MaxTempLim"]
    lib.s_AFC_Param.KeAFC_T_CPV_MinTempLim = pd["s_AFC_Param.KeAFC_T_CPV_MinTempLim"]
    lib.s_AFC_Param.KeAFC_T_RefTemp = pd["s_AFC_Param.KeAFC_T_RefTemp"]
    lib.s_AFC_Param.KeAFC_k_Coeff_a = pd["s_AFC_Param.KeAFC_k_Coeff_a"]
    lib.s_AFC_Param.KeAFC_k_Coeff_b = pd["s_AFC_Param.KeAFC_k_Coeff_b"]
    lib.s_AFC_Param.KeAFC_k_Coeff_c = pd["s_AFC_Param.KeAFC_k_Coeff_c"]
    lib.s_AFC_Param.KeAFC_k_Coeff_d = pd["s_AFC_Param.KeAFC_k_Coeff_d"]
    lib.s_AFC_Param.KeAFC_k_Coeff_e = pd["s_AFC_Param.KeAFC_k_Coeff_e"]
    lib.s_AFC_Param.KeAFC_k_Coeff_f = pd["s_AFC_Param.KeAFC_k_Coeff_f"]
    lib.s_AFC_Param.KeAFC_k_Coeff_g = pd["s_AFC_Param.KeAFC_k_Coeff_g"]
    lib.s_AFC_Param.KeAFC_k_Coeff_h = pd["s_AFC_Param.KeAFC_k_Coeff_h"]


    yield

    clean_dat_files(PROJECT_PATH)


def parametrize_args(
    params: Dict[str, List[Any]]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Prepares arguments for pytest.mark.parametrize by generating all combinations of named parameters
    encapsulated in dictionaries with corresponding IDs. Each test case dictionary includes the parameters
    under 'Inputs' and a descriptive string under 'Descriptions'.

    Args:
        params: A dictionary where each key is a parameter name and each value is a list of parameter values.

    Returns:
        output: A list of dictionaries, each dictionary represents a test case with 'Inputs' and 'Descriptions'.
        ids: A list of strings, each representing an ID for the corresponding test case.
    """

    inputs_name = "Inputs"
    description_name = "Descriptions"
    id_name = "tid"
    id_prefix = "Param_Case"

    all_combinations = list(product(*params.values()))

    output = []
    ids = []

    for i, combo in enumerate(all_combinations, start=1):
        # id_value = f"{id_prefix}_{i}"
        id_value = i
        ids.append(id_value)

        combo_dict = {name: value for name, value in zip(params.keys(), combo)}
        description_parts = [f"\t{id_name}_{i}"] + [
            f"\t{name} = {value}" for name, value in combo_dict.items()
        ]
        description = "\n".join(description_parts)
        description = f" {id_name}_{i}".strip()

        output.append({inputs_name: combo_dict, description_name: description})

    return output, ids


def parametrize_afc_api_input_data(param_file_name: str) -> List[Dict[str, Any]]:
    """
    Prepares arguments for pytest.mark.parametrize by generating params from an input specification read from a file.
    Args:
        param_file_name: name of file where the test parameters for parametrization are defined.

    Returns:
        list of dict with all parameters for test

    """
    output = []
    ids = []
    file_path = join(dirname(_MODULE_PATH), "test_data", "json", param_file_name)
    try:
        with open(file_path, "r") as file:
            input_args = json.load(file)
    except FileNotFoundError:
        logger.error(f"NO FILE : {file_path}")
        input_args = []

    if file_path:
        i = 0
        for item in input_args:
            id_value = i
            ids.append(id_value)
            if (
                "VaAPI_Cmp_NVMRegion" in item["Inputs"]
                and "VaAPI_Cmp_NVMRegion_Size" in item["Inputs"]
            ):
                logger.debug("T 1")
                item["Inputs"]["VaAPI_Cmp_NVMRegion"] = (
                    item["Inputs"]["VaAPI_Cmp_NVMRegion"]
                    * item["Inputs"]["VaAPI_Cmp_NVMRegion_Size"]
                )
            if (
                "VaAPI_U_SEVolts" in item["Inputs"]
                and "VaAPI_U_SEVolts_Size" in item["Inputs"]
            ):
                logger.debug(2)
                item["Inputs"]["VaAPI_U_SEVolts"] = (
                    item["Inputs"]["VaAPI_U_SEVolts"]
                    * item["Inputs"]["VaAPI_U_SEVolts_Size"]
                )
            if (
                "VaAPI_b_CellVolts_DR" in item["Inputs"]
                and "VaAPI_b_CellVolts_DR_Size" in item["Inputs"]
            ):
                logger.debug(3)
                item["Inputs"]["VaAPI_b_CellVolts_DR"] = (
                    item["Inputs"]["VaAPI_b_CellVolts_DR"]
                    * item["Inputs"]["VaAPI_b_CellVolts_DR_Size"]
                )
            if (
                "VaAPI_T_TempSnsrs" in item["Inputs"]
                and "VaAPI_T_TempSnsrs_Size" in item["Inputs"]
            ):
                logger.debug(4)
                item["Inputs"]["VaAPI_T_TempSnsrs"] = (
                    item["Inputs"]["VaAPI_T_TempSnsrs"]
                    * item["Inputs"]["VaAPI_T_TempSnsrs_Size"]
                )
            if (
                "VaAPI_b_TempSnsrs_DR" in item["Inputs"]
                and "VaAPI_b_TempSnsrs_DR_Size" in item["Inputs"]
            ):
                logger.debug(5)
                item["Inputs"]["VaAPI_b_TempSnsrs_DR"] = (
                    item["Inputs"]["VaAPI_b_TempSnsrs_DR"]
                    * item["Inputs"]["VaAPI_b_TempSnsrs_DR_Size"]
                )
            if "AFC_Calc.Va_Cnt_CPVCorrIdx" in item["Expected"]:
                logger.debug(5)
                item["Expected"]["AFC_Calc.Va_Cnt_CPVCorrIdx"] = (
                    item["Expected"]["AFC_Calc.Va_Cnt_CPVCorrIdx"] * 192
                )
            output.append({"Inputs": item["Inputs"], "Expected": item["Expected"]})
            i += 1
    return output, ids


@fixture(scope="module")
def input_file_name(request):
    """
    Args:
        request: fixture request object

    Returns:
        full path to input file for time based test.

    """
    return join(dirname(_MODULE_PATH), _TIME_BASED_INPUT_DATA, request.param)


@fixture(scope="module")
def output_file_name(request):
    """
    Args:
        request: fixture request object

    Returns:
        full path to output file for time based test.

    """
    out_filename = request.param.replace(".", "_o_.")
    return join(dirname(_MODULE_PATH), _TIME_BASED_OUTPUT_DATA, request.param)


@fixture(scope="module")
def reference_file_name(request):
    """
    Args:
        request: fixture request object

    Returns:
        full path to reference file for time based test.

    """
    ref_filename = "reference_" + request.param
    return join(dirname(_MODULE_PATH), _TIME_BASED_REFERENCE_DATA, ref_filename)


def get_num_elements_from_buffer(lib):
    obj = ffi.addressof(lib.AFC_LoggingTrack[0], "Ne_Afc_Logging_Circ_Buff_Handle")
    num_elements_inserted = ffi.new("uint16_t *")
    lib.LIB_CircBuffNumElementsInserted(obj, num_elements_inserted)
    return num_elements_inserted[0]


def process_log_buffer(lib, extn=1, write_to_file=False):
    """
    Process the log buffer and extract result, assign to return result data object of LogParseResult
    """
    result = LogParseResult()
    lfilename = f"log_buffer_{extn}.xlsx"
    log_data_fname = join(dirname(_MODULE_PATH), _TIME_BASED_OUTPUT_DATA, lfilename)
    log_data = {
        "Indexes": [],
        "Cycle_Count": [],
        "Stage": [],
        "Highest_index": [],
        "Temperatures": [],
    }

    # Get buffer (logged data) and parse
    obj = ffi.addressof(lib.AFC_LoggingTrack[0], "Ne_Afc_Logging_Circ_Buff_Handle")
    logger.info(f"Elements Inserted: {get_num_elements_from_buffer(lib)}")
    for i in range(extn):
        ele_addr = ffi.new("uint8_t [18]")
        # Get last logged element
        lib.LIB_CircBuffGetElement(obj, i, ele_addr)
        # Get and compare indexes logged
        result.indexes = [
            ele_addr[3],
            ele_addr[6],
            ele_addr[9],
            ele_addr[12],
            ele_addr[15],
        ]

        # Unpack buffer data
        py_list = ffi.unpack(ele_addr, _TOTAL_BYTES)
        #logger.debug(py_list)

        u32_word = int.from_bytes(bytes(py_list[:3]), byteorder="little", signed=False)
        result.cycle_count = 0xFFF & (u32_word >> 12)
        result.stage = 0x3F & (u32_word >> 6);
        result.highest_index = 0x3F & (u32_word >> 0);

        # Extract temperature logged
        result.temperatures = [
            int.from_bytes(py_list[4:6], byteorder="little", signed=True),
            int.from_bytes(py_list[7:9], byteorder="little", signed=True),
            int.from_bytes(py_list[10:12], byteorder="little", signed=True),
            int.from_bytes(py_list[13:15], byteorder="little", signed=True),
            int.from_bytes(py_list[16:18], byteorder="little", signed=True),
        ]
        logger.debug("\n\n RESULT \n\n")
        logger.debug(f"Warning Flags: {lib.VeAFC_e_WarningFlags}")
        logger.debug(f"Early Flags: {lib.AFC_Outputs.EarlyWarningAgingFlag[0]}")
        logger.debug(f"Abnormal Flags: {lib.AFC_Outputs.AbnormalAgingFlag[0]}")
        logger.debug(f"Extreme Flags: {lib.AFC_Outputs.ExtremeAgingFlag[0]}")
        result.print_buffer()

        log_data["Indexes"].append(result.indexes)
        log_data["Cycle_Count"].append(result.cycle_count)
        log_data["Stage"].append(result.stage)
        log_data["Highest_index"].append(result.highest_index)
        log_data["Temperatures"].append(result.temperatures)
    if write_to_file:
        write_output_to_excel(log_data, log_data_fname)
    return result
