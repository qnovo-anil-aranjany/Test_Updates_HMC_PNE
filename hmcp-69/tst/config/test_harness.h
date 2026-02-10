/* ===================================================================
   This is an isolated_header file.
   It is designed solely for testing purposes (pytest + cffi cdef).
   WARNING: This header file is not intended for inclusion in any compilation units.
   =================================================================== */

#ifndef TEST_HARNESS_H_
#define TEST_HARNESS_H_

#pragma message ("Warning: You are including an isolated header file intended only for test extraction purposes.")

/************************************************
 * Expose Function Prototypes
 ************************************************/
void                fs_AFC_SetupStageParam(void);
t_I_milliamp_chg    fs_AFC_CalcChgCurrPresentStg(t_uint8 Le_i_PresentStageIdx);
t_uint8             fs_AFC_FindHighestCPVStageIdx(void);
t_uint8             fs_AFC_AttemptToIncCPVIdx(t_uint8 Le_i_CPV_PresentIndex);
t_U_millivolt_cell  fs_AFC_CalcTempCurrCompVolt(t_U_millivolt_cell Le_U_CellVolt,
                                                t_U_millivolt_cell Le_U_CellOCV,
                                                t_float32 Le_r_TemperatureRatio,
                                                t_float32 Le_r_CurrRatio);
t_I_milliamp_chg    fs_AFC_CalcTempCompChgCurr(t_I_milliamp_chg Le_I_ChgCurr, t_T_celsius Le_T_TempSnsr);
t_float32           fs_AFC_CalcCurrRatio(void);
t_float32           fs_AFC_CalcTemperatureRatio(t_T_celsius Le_T_TempSnsr);
void                fs_AFC_LoadNVM(t_uint8 Le_Cnt_StageNum);
void                fs_AFC_SaveNVM(t_uint8 Le_Cnt_StageNum);
void                fs_AFC_CPVTrack(void);
void                fs_API_SetInputsAFC(void      *La_Cmp_Input_NVMRegion,
                                void              *La_Cmp_Input_NVMLoggingRegion,
                                t_I_milliamp       Le_I_Input_PackCurr,
                                t_bool             Le_b_Input_PackCurr_DR,
                                t_U_millivolt_cell *La_U_Input_CellVolts,
                                t_bool             *La_b_Input_CellVolts_DR,
                                t_T_celsius        *La_T_Input_TempSnsrs,
                                t_bool             *La_b_Input_TempSnsrs_DR,
                                t_T_celsius        Le_T_Input_MinTempSnsr,
                                t_bool             Le_b_Input_MinTempSnsr_DR,
                                t_T_celsius        Le_T_Input_MaxTempSnsr,
                                t_bool             Le_b_Input_MaxTempSnsr_DR,
                                t_Cap_milliamphr   Le_Cap_Input_ChgPackCapcty,
                                t_bool             Le_b_Input_ChgPackCapcty_DR,
                                t_Pct_percent      Le_Pct_Input_PackSOC,
                                t_bool             Le_b_Input_PackSOC_DR,
                                t_bool             Le_b_Input_EVSEChgStatus,
								void			   *Le_Cmp_Transient_CTE_Info,
                                t_uint32           *Le_e_Output_ErrorFlags,
                                t_I_milliamp_chg   *Le_I_Output_ChgPackCurr,
                                t_I_milliamp_chg   *Le_I_Output_MaxReferenceCurr,
                                t_I_milliamp_chg   *Le_I_Output_MitigatedCurr,
                                t_U_millivolt_pack *Le_I_Output_ChgPackVolt,
								t_bool			   *Le_b_Output_ChgCompletionFlag,
								t_bool			   *Le_b_Output_ExtremeAgingFlag,
                                t_bool			   *Le_b_Output_AbnormalAgingFlag,
                                t_bool			   *Le_b_Output_EarlyWarningAgingFlag,
                                t_bool			   *Le_b_Output_EOLFlag,
                                t_bool			   *Le_b_Output_SOCImbalanceFlag);

void fs_API_CheckExceedChgCurrRange(void);
void fs_API_CheckExceedTempRange(void);
void fs_API_AttemptDerateChgCurr(void);
void fs_API_CheckChgCompletion(void);
void fs_API_SelectHTDParameters(void);
void AFC_LogCorrIdxEvent( t_U_millivolt_cell  series_elements_val[]);



/************************************************
 * Exposed Struct Definitions
 ************************************************/
struct st_AFC_AlgorithmParameters {
  /* Voltage Parameters */
  t_U_millivolt_cell  KeAFC_U_CV_RatedChgCellVolt;
  t_I_milliamp_chg    KeAFC_I_CV_ChgCurr;
  t_I_milliamp_chg    KeAFC_I_CV_ChgStepCurr;

  /* Stage Parameters */
  t_Pct_percent       KaAFC_Pct_Stg_SOC[CeAFC_n_MaxNumStages];
  t_I_milliamp_chg    KaAFC_I_Stg_ChgMaxCurr[CeAFC_n_MaxNumStages];
  t_I_milliamp_chg    KaAFC_I_Stg_ChgMinCurr[CeAFC_n_MaxNumStages];
  t_I_milliamp_chg    KaAFC_I_Stg_ChgStepCurr[CeAFC_n_MaxNumStages];
  t_U_millivolt_cell  KaAFC_U_Stg_RefStartCellVolt[CeAFC_n_MaxNumStages];
  t_U_millivolt_cell  KaAFC_U_Stg_RefBandCellVolt[CeAFC_n_MaxNumStages];
  t_U_millivolt_cell  KaAFC_U_Stg_SADCellLim[CeAFC_n_MaxNumStages];

  /* Temperature Parameters */
  t_T_celsius KeAFC_T_CPV_MaxTempLim;
  t_T_celsius KeAFC_T_CPV_MinTempLim;
  t_T_celsius KeAFC_T_RefTemp;

  /* Current & Voltage Compensation Coefficients */
  /* Note: no 'c' */
  t_float32 KeAFC_k_Coeff_a;
  t_float32 KeAFC_k_Coeff_b;
  t_float32 KeAFC_k_Coeff_c;
  t_float32 KeAFC_k_Coeff_d;
  t_float32 KeAFC_k_Coeff_e;
  t_float32 KeAFC_k_Coeff_f;
  t_float32 KeAFC_k_Coeff_g;
  t_float32 KeAFC_k_Coeff_h;
};

struct st_INP_TransientCalculation {
    t_T_celsius VeINP_T_MinTemp;
    t_T_celsius VeINP_T_MaxTemp;
};

struct st_API_VariableInterface {
    void 				*VeAPI_Cmp_NVMRegion;
    void 				*Ve_n_NVMLoggingRegionSize;

    t_I_milliamp 		VeAPI_I_PackCurr;
    t_bool 				VeAPI_b_PackCurr_DR;
    t_U_millivolt_cell 	*VaAPI_U_CellVolts;
    t_bool 				*VaAPI_b_CellVolts_DR;
    t_T_celsius 		*VaAPI_T_TempSnsrs;
    t_bool 				*VaAPI_b_TempSnsrs_DR;
    t_T_celsius 		VeAPI_T_MinTempSnsr;
    t_bool 				VeAPI_b_MinTempSnsr_DR;
    t_T_celsius 		VeAPI_T_MaxTempSnsr;
    t_bool 				VeAPI_b_MaxTempSnsr_DR;
    t_Cap_milliamphr 	VeAPI_Cap_ChgPackCapcty;
    t_bool 				VeAPI_b_ChgPackCapcty_DR;
    t_Pct_percent 		VeAPI_Pct_PackSOC;
    t_bool 				VeAPI_b_PackSOC_DR;
    t_bool 				VeAPI_b_EVSEChgStatus;

    void				*VaAFC_Cmp_CTE_Info;

    /* Outputs mirror customer inputs */
    t_uint32 			*VeAFC_e_ErrorFlags;
    t_I_milliamp_chg 	*VeAFC_I_ChgPackCurr;
    t_I_milliamp_chg 	*VeAFC_I_MaxReferenceCurr;
    t_I_milliamp_chg 	*VeAFC_I_MitigatedCurr;
    t_U_millivolt_pack 	*VeAFC_U_ChgPackVolt;
    t_bool 				*VeAFC_b_ChgCompletionFlag;
    t_bool 				*VeAFC_b_ExtremeAgingFlag;
    t_bool 				*VeAFC_b_AbnormalAgingFlag;
    t_bool 				*VeAFC_b_EarlyWarningAgingFlag;
    t_bool 				*VeAFC_b_EOLFlag;
    t_bool 				*VeAFC_b_SOCImbalanceFlag;
};

struct AFC_Param_VoltageImbalance_t {
	t_uint8 Ke_Cmp_SigmaLevel;
	t_U_millivolt_cell Ke_Cmp_NoiseFloor;
	t_time Ke_t_MinSamplingTime;
	t_uint8 Ke_Cnt_ThresholdForValidSample;
};

struct st_API_AfcParam_t {
    t_I_milliamp_chg   KaAPI_AFC_I_Stg_ChgMaxCurr[CeAFC_n_MaxNumStages];
};

/************************************************
 * Exposed Struct Declarations
 ************************************************/
extern struct st_AFC_TransientCalculation s_AFC_Calc;
extern struct st_AFC_AlgorithmParameters  s_AFC_Param;
extern struct st_INP_TransientCalculation s_INP_Calc;
extern struct AFC_Param_VoltageImbalance_t AFC_Param_VoltageImbalance;


/************************************************
 * Exposed Global Variables
 ************************************************/
extern t_uint8            VaAFC_Cnt_CPVCorrIdx[MAX_NUM_CELLS];
extern t_U_millivolt_cell VaAFC_U_RefCellVolt[MAX_NUM_CELLS];
extern t_bool             VeAFC_b_ControllerWakeUp;
extern t_bool             VeAFC_b_ChargeSessionInit;
extern t_uint16           KeINP_n_MaxNumCells;
extern t_uint8            KeINP_n_MaxNumTempSnsrs;
extern t_U_millivolt_cell KaLIB_U_OCVAxis[CeLIB_n_MaxNumOCVPoints];
extern t_Pct_percent      KaLIB_Pct_SOCAxis[CeLIB_n_MaxNumOCVPoints];
extern STATIC struct st_API_VariableInterface s_API_Var;
extern struct st_API_AfcParam_t s_API_AfcParam;
extern STATIC void AFC_KeepTrackOfChrgCycles(t_Pct_percent Le_Pct_SOC);

#endif // TEST_HARNESS_H_
