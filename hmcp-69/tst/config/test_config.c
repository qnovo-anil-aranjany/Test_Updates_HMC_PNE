/**********************************************************************
 * This file is to allow source code to compile for testing purposes.
 **********************************************************************/

#ifdef UNITTEST

/************************************************
 * Include Header Files
 ************************************************/
#include <math.h>

#include "test_config.h"
#include "qnovo_afc_api.h"


/************************************************
 * Global Variables: Mock Inputs from Customers
 ************************************************/
t_uint32            VaAPI_Cmp_NVMRegion[NVM_ARRAY_SIZE];
t_uint8             VaAPI_Cmp_NVMLoggingRegion[NVM_LOGGING__BYTE_SIZE];
t_I_milliamp        VeAPI_I_PackCurr;
t_bool              VeAPI_b_PackCurr_DR;
t_U_millivolt_cell  VaAPI_U_CellVolts[MAX_NUM_CELLS];
t_bool              VaAPI_b_CellVolts_DR[MAX_NUM_CELLS];
t_T_celsius         VaAPI_T_TempSnsrs[MAX_NUM_TEMP_SNSRS];
t_bool              VaAPI_b_TempSnsrs_DR[MAX_NUM_TEMP_SNSRS];
t_T_celsius         VeAPI_T_MinTempSnsr;
t_bool              VeAPI_b_MinTempSnsr_DR;
t_T_celsius         VeAPI_T_MaxTempSnsr;
t_bool              VeAPI_b_MaxTempSnsr_DR;
t_Cap_milliamphr    VeAPI_Cap_ChgPackCapcty;
t_bool              VeAPI_b_ChgPackCapcty_DR;
t_Pct_percent       VeAPI_Pct_PackSOC;
t_bool              VeAPI_b_PackSOC_DR;
t_bool              VeAPI_b_EVSEChgStatus;
t_int32             VeAPI_e_EVSEChgLevel;

/* Transient Output */
t_uint8	VaAFC_Cmp_CTE_Info[CTE_INFO_ARRAY_SIZE];

/* Outputs to Customers */
t_uint32            VeAFC_e_ErrorFlags;
t_I_milliamp_chg    VeAFC_I_ChgPackCurr;
t_U_millivolt_pack  VeAFC_U_ChgPackVolt;
t_bool              VeAFC_b_ChgCompletionFlag;
t_I_milliamp_chg    VeAFC_I_MaxReferenceCurr;
t_I_milliamp_chg 	VeAFC_I_MitigatedCurr;
t_bool              VeAFC_b_ExtremeAgingFlag;
t_bool              VeAFC_b_AbnormalAgingFlag;
t_bool              VeAFC_b_EarlyWarningAgingFlag;
t_bool              VeAFC_b_EOLFlag;
t_bool              VeAFC_b_SOCImbalanceFlag;

/* Get functions to test versioning */
t_uint32 get_afc_sw_ver(void);

t_U_millivolt_cell  cell_volts_temp[192];
LIB_CircBuffHandle_t Input_CircBuffHandle_t;
t_uint8*             ele_addr;

/* Obfuscation */
t_int32 VeAPI_Cmp_LogSrc;
t_uint32 VeAPI_Cmp_LogSrcSize = sizeof(VeAPI_Cmp_LogSrc);
t_int32 VeAPI_Cmp_LogDst;

t_int32 VeAPI_Cmp_LogSrcArray[GENERIC_LOG_ARRAY_SIZE];
t_uint32 VeAPI_Cmp_LogSrcArraySize = sizeof(VeAPI_Cmp_LogSrcArray);
t_int32 VeAPI_Cmp_LogDstArray[GENERIC_LOG_ARRAY_SIZE];
t_U_millivolt_cell  cell_volts_temp[192];
LIB_CircBuffHandle_t Input_CircBuffHandle_t;
t_uint8*             ele_addr;

CTE_ESTIMATES_T cte_estimates;
t_uint32 cte_status;


t_uint32 get_afc_sw_ver(void) {
    return QnovoAFC_SW_Version;
}

t_float32 standard_expf(t_float32 x) {
    return expf(x);
}

AFC_INFO_T afc_cte_info;

int main(void) {
//    printf("Size of NVM (s_AFC_Track) w/o packing = %i Bytes\n", sizeof(struct st_AFC_CPVTracking));
//    printf("Size of VRAM (st_AFC_TransientCalculation) w/o packing = %i Bytes\n", sizeof(struct st_AFC_TransientCalculation));
//
//    return 0;
//
//    printf("Size of struct INPUT_STRUCTURE = %i\n", sizeof(INP_FIELD));
//
//    /* Checks if pragma pack(push, 2) messes up the struct values. */
//    for (int i = 0; i < CeAFC_n_MaxNumStages; i++)
//    {
//    printf("KaAFC_I_Stg_ChgMaxCurr = %u\n", s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr[i]);
//    }
//
//    fs_AFC_NVMInit();
//
//    for (int i = 0; i < CeAFC_n_MaxNumStages; i++)
//    {
//    printf("KaAFC_I_Stg_ChgMaxCurr = %u\n", s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr[i]);
//    }
//
//    fs_AFC_CPVTrack();
//
//    for (int i = 0; i < CeAFC_n_MaxNumStages; i++)
//    {
//    printf("KaAFC_I_Stg_ChgMaxCurr = %u\n", s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr[i]);
//    }
//
//    printf("Size of s_AFC_Track = %i\n", sizeof(struct st_AFC_CPVTracking));

  return 0;
}


#else
#endif
