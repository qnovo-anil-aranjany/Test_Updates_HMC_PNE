#ifndef TEST_CONFIG_H_
#define TEST_CONFIG_H_

#ifdef UNITTEST

/************************************************
 * Include Header Files
 ************************************************/
#include <stdio.h>
#include "qnovo_types.h"
#include "qnovo_bms_config.h"
#include "swc_adaptive_fast_charge.h"


/************************************************
 * Global Variables: Mock Inputs from Customers
 ************************************************/
#define NVM_ARRAY_SIZE     9000
#define CTE_INFO_ARRAY_SIZE 32

extern t_uint32            VaAPI_Cmp_NVMRegion[NVM_ARRAY_SIZE];

extern t_I_milliamp        VeAPI_I_PackCurr;
extern t_bool              VeAPI_b_PackCurr_DR;
extern t_U_millivolt_cell  VaAPI_U_CellVolts[MAX_NUM_CELLS];
extern t_bool              VaAPI_b_CellVolts_DR[MAX_NUM_CELLS];
extern t_T_celsius         VaAPI_T_TempSnsrs[MAX_NUM_TEMP_SNSRS];
extern t_bool              VaAPI_b_TempSnsrs_DR[MAX_NUM_TEMP_SNSRS];
extern t_T_celsius         VeAPI_T_MinTempSnsr;
extern t_bool              VeAPI_b_MinTempSnsr_DR;
extern t_T_celsius         VeAPI_T_MaxTempSnsr;
extern t_bool              VeAPI_b_MaxTempSnsr_DR;
extern t_Cap_milliamphr    VeAPI_Cap_ChgPackCapcty;
extern t_bool              VeAPI_b_ChgPackCapcty_DR;
extern t_Pct_percent       VeAPI_Pct_PackSOC;
extern t_bool              VeAPI_b_PackSOC_DR;
extern t_bool              VeAPI_b_EVSEChgStatus;
extern t_int32             VeAPI_e_EVSEChgLevel;

/* Transient Output */
extern t_uint8 VaAFC_Cmp_CTE_Info[CTE_INFO_ARRAY_SIZE];

/* Outputs to Customers */
extern t_uint32            VeAFC_e_ErrorFlags;
extern t_I_milliamp_chg    VeAFC_I_ChgPackCurr;
extern t_U_millivolt_pack  VeAFC_U_ChgPackVolt;
extern t_bool              VeAFC_b_ChgCompletionFlag;

/* Functions to get extern const values from the actual code */
t_uint32 get_afc_sw_ver(void);

extern t_float32 standard_expf(t_float32 x);


#else
#endif


#endif /* TEST_CONFIG_H_ */
