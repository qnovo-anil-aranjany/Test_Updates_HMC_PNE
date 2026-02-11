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

/* Get functions to test versioning */
t_uint32 get_afc_sw_ver(void);

t_uint32 get_afc_sw_ver(void) {
    return QnovoAFC_SW_Version;
}

t_float32 standard_expf(t_float32 x) {
    return expf(x);
}



#else
#endif
int main(void) {

  return 0;
}
