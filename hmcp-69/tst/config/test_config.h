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
#include "cfg_global_defs.h"
#include "lib_common_utils.h"
#include "qnovo_afc_api.h"
#include "qnovo_cte.h"


/************************************************
 * Global Variables: Mock Inputs from Customers
 ************************************************/
#define NVM_ARRAY_SIZE     3750
#define CTE_INFO_ARRAY_SIZE 32
#define NVM_LOGGING__BYTE_SIZE 4000
#define GENERIC_LOG_ARRAY_SIZE      100


extern t_uint32            VaAPI_Cmp_NVMRegion[NVM_ARRAY_SIZE];
extern t_uint8            VaAPI_Cmp_NVMLoggingRegion[NVM_LOGGING__BYTE_SIZE];

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
extern t_I_milliamp_chg    VeAFC_I_MaxReferenceCurr;
extern t_I_milliamp_chg    VeAFC_I_MitigatedCurr;
extern t_bool              VeAFC_b_ExtremeAgingFlag;
extern t_bool              VeAFC_b_AbnormalAgingFlag;
extern t_bool              VeAFC_b_EarlyWarningAgingFlag;
extern t_bool              VeAFC_b_EOLFlag;
extern t_bool              VeAFC_b_SOCImbalanceFlag;


/* Functions to get extern const values from the actual code */
t_uint32 get_afc_sw_ver(void);

extern t_int32 VeAPI_Cmp_LogSrc;
extern t_uint32 VeAPI_Cmp_LogSrcSize;
extern t_int32 VeAPI_Cmp_LogDst;

extern t_int32 VeAPI_Cmp_LogSrcArray[GENERIC_LOG_ARRAY_SIZE];
extern t_uint32 VeAPI_Cmp_LogSrcArraySize;
extern t_int32 VeAPI_Cmp_LogDstArray[GENERIC_LOG_ARRAY_SIZE];

extern t_float32 standard_expf(t_float32 x);
extern t_U_millivolt_cell  cell_volts_temp[192];
extern LIB_CircBuffHandle_t Input_CircBuffHandle_t;
extern t_uint8*             ele_addr;

extern CTE_ESTIMATES_T cte_estimates;
extern t_uint32 cte_status;
typedef struct {
    uint16_t magic;
    uint8_t data[30];
} AFC_INFO_T;
extern AFC_INFO_T afc_cte_info;


#else
#endif


#endif /* TEST_CONFIG_H_ */
