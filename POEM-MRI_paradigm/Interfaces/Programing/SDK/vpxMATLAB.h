/*------------------------------------------------------------------
/   vpxMATLAB.h  KFA 2015-Dec-11 for MATLAB 64-bit
/
/
/	- DO NOT MODIFY ANYTHING BELOW !!!
/
/--------------------------------------------------------------------*/

#ifndef VPX_DOT_H
#define VPX_DOT_H

#define _IMPORTING_INTO_MATLAB
#define BOOL int // KFA 294


#define VPX_SDK_VERSION		294.0  //.111

// begin EXPORT / IMPORT 
#ifdef _EXPORTING
   #define VPX_DECLSPEC    __declspec(dllexport)
#else
	#define VPX_DECLSPEC   __declspec(dllimport)
#endif
// end EXPORT / IMPORT 

#define CALLCONV  __cdecl

#ifdef __cplusplus
extern "C" {
#endif

/*------------------------------------------------------------------
/						VIEWPOINT PROGRAM CONSTANTS
/--------------------------------------------------------------------*/

#define VPX_MAX_COMMAND_STRING		1024

#define MIN_ROI_INDEX	1
#define MAX_ROI_INDEX	99
#define MAX_ROI_BOXES	MAX_ROI_INDEX + 1

#define MAX_ROI_DISPLAY  10
#define ROI_NOT_HIT   -9999
#define ROI_NO_EVENT  -9999

#define MAX_GLINTS 4

#define VPX_EyeType int
#define EYE_A 					0
#define EYE_B 					1
#define SCENE_A					2
#define SCENE_B					3
#define OBSERVER				4
#define VIDEO_SCREEN				5
#define EYE_MOVIE_CHANNEL   			6
#define DUAL_EYE_MOVIE_CHANNEL  		7
#define MAX_ROUTING 				8

#define VPX_MESSAGE "VPX_message"

#define PointInRectQ(pt,rr) ( ( pt.x < rr.right ) && ( pt.y < rr.bottom ) && ( rr.left < pt.x ) && ( rr.top < pt.y ) )


/*------------------------------------------------------------------
/						Data Quality Codes
/--------------------------------------------------------------------*/
#define VPX_DataQuality int
#define VPX_QUALITY_PupilScanFailed		5
#define VPX_QUALITY_PupilFitFailed		4
#define VPX_QUALITY_PupilCriteriaFailed	3
#define VPX_QUALITY_PupilFallBack		2
#define VPX_QUALITY_PupilOnlyIsGood		1
#define VPX_QUALITY_GlintIsGood			0

/*------------------------------------------------------------------
/						Multi Glint Quality Codes
/--------------------------------------------------------------------*/
#define VPX_GlintDataQuality int
#define VPX_GLINT_QUALITY_ScanFailed			5
#define VPX_GLINT_QUALITY_FitFailed				4
#define VPX_GLINT_QUALITY_WidthCriteriaFailed	3
#define VPX_GLINT_QUALITY_AspectCriteriaFailed	2
#define VPX_GLINT_QUALITY_NoOperation			1
#define VPX_GLINT_QUALITY_Good					0

/*------------------------------------------------------------------
/						DLL Distributor Connection
/--------------------------------------------------------------------*/
#define VPX_DistributorType				int
#define VPX_Distributor_None			0
#define VPX_Distributor_IsViewPoint		1
#define VPX_Distributor_IsRemoteLink	2
#define VPX_Distributor_IsEtherClient	3

/*------------------------------------------------------------------
/						Status Items
/--------------------------------------------------------------------*/
typedef enum {
	VPX_STATUS_HEAD = 0,
	VPX_STATUS_ViewPointIsRunning,
	VPX_STATUS_VideoIsFrozen,
	VPX_STATUS_DataFileIsOpen,
	VPX_STATUS_DataFileIsPaused,
	VPX_STATUS_AutoThresholdInProgress,
	VPX_STATUS_CalibrationInProgress,
	VPX_STATUS_StimulusImageShape,
	VPX_STATUS_BinocularModeActive,
	VPX_STATUS_SceneVideoActive,
	VPX_STATUS_DistributorAttached,
	VPX_STATUS_CalibrationPoints,
	VPX_STATUS_TTL_InValues,
	VPX_STATUS_TTL_OutValues,
	VPX_STATUS_TorsionActive,
	VPX_STATUS_BinocularAveraging,
	VPX_STATUS_TAIL
} VPX_StatusItem;

/*------------------------------------------------------------------
/				BinocularAveraging Items
/--------------------------------------------------------------------*/
typedef enum {
	VPX_BinocularAveraging_Off = 0,
	VPX_BinocularAveraging_Only_Y,
	VPX_BinocularAveraging_Both_XY,
	VPX_BinocularAveraging_ParallaxCorrection,
} VPX_BinocularAveragingType;

/*------------------------------------------------------------------
/						VPX_EyeEventType
/--------------------------------------------------------------------*/
typedef enum 
{
	VPX_EVENT_HEAD = 0,
	VPX_EVENT_NoEvent,
	VPX_EVENT_Fixation_Start,
	VPX_EVENT_Fixation_Continue,
	VPX_EVENT_Fixation_Stop,
	VPX_EVENT_Drift_Start,
	VPX_EVENT_Drift_Continue,
	VPX_EVENT_Drift_Stop,
	VPX_EVENT_Saccade_Start,
	VPX_EVENT_Saccade_Continue,
	VPX_EVENT_Saccade_Stop,
	VPX_EVENT_Blink_Start,
	VPX_EVENT_Blink_Continue,
	VPX_EVENT_Blink_Stop,
	VPX_EVENT_NoBlink,
	VPX_EVENT_TAIL
} VPX_EyeEventType;

/*------------------------------------------------------------------
/						PRECISION TIMING
/--------------------------------------------------------------------*/
#define SINCE_PRECISE_INIT_TIME		((double*)(0))

// bit flags
#define LEAVE_PRECISE_HOLD_TIME		0
#define RESET_PRECISE_HOLD_TIME		1
#define SINCE_SYSTEM_INIT_TIME		2
#define SINCE_DLL_INIT_TIME			0

#define PRECISE_TIME_UNAVAILABLE	-3.0
#define PRECISE_TIME_INITIALIZING	-4.0

/*---------------------------------------------------------------------------------
/						NOTIFICATION CODES for vp_message WindowsMessage
/---------------------------------------------------------------------------------*/
typedef enum {

	VPX_ENUM_NOTIFICATIONS_HEAD	= 0,
	
	VPX_Obsolete_01		=   1,

	VPX_DAT_FRESH		=   2,

	VPX_Obsolete_03		=   3,
	VPX_Obsolete_04		=   4,	
		
	VPX_CAL_WARN		=   5,
	VPX_CAL_BEGIN		=   6,
	VPX_CAL_SHOW		=   7,
	VPX_CAL_ZOOM		=   8,
	VPX_CAL_SNAP		=   9,
	VPX_CAL_HIDE		=  10,
	VPX_CAL_END			=  11,
	VPX_CAL_TAIL		=  12,

	VPX_ROI_CHANGE		=  13,

	VPX_Obsolete_14	=  14,
	VPX_Obsolete_15	=  15,
	VPX_Obsolete_16	=  16,
	VPX_Obsolete_17	=  17,	
	VPX_Obsolete_18	=  18,
	VPX_Obsolete_19	=  19,

	VPX_COMMAND_STRING	=  20,
	VPX_STATUS_CHANGE	=  21,

	VPX_Obsolete_22	=  22,
	VPX_Obsolete_23	=  23,
	VPX_Obsolete_24	=  24,

	VPX_VIDEO_FrameAvailable	=  25,
	VPX_TRIGGER_EVENT			=  26,
	VPX_VIDEO_SyncSignal		=  27,

	VPX_VIDEO_BufferedImageAvailable		=  28,
	VPX_DAT_FRESH_BufferedEyeDataAvailable	=  29,
	VPX_DAT_FRESH_BufferedHeadDataAvailable	=  30,

	VPX_DAT_FRESH_EYES	=   VPX_DAT_FRESH,
	VPX_DAT_FRESH_HEAD	=   33,
	VPX_DAT_FRESH_3DWS  =   34,

	VPX_TTL_IN		= 164,
	VPX_TTL_OUT		= 165,
		
	VPX_ENUM_NOTIFICATIONS_TAIL

} VP_Message_NotificationCodes;


/*------------------------------------------------------------------
/						ENUMS
/--------------------------------------------------------------------*/

typedef enum { 
		VPX_PARSE_HEAD = 0,
		VPX_PARSE_OK,
		VPX_PARSE_ACTION,
		VPX_PARSE_END,
		VPX_PARSE_COMMENT,
		VPX_PARSE_OBSOLETE,
		VPX_PARSE_ERROR_HEAD,
		VPX_PARSE_ERROR_UnknownCommand,
		VPX_PARSE_ERROR_MissingParameter,
		VPX_PARSE_ERROR_EmptyLine,
		VPX_PARSE_ERROR_SendMessageTimeOut,
		VPX_PARSE_ERROR_IllegalParameter,
		VPX_PARSE_ERROR_ParserIsNotRunning,
		VPX_PARSE_ERROR_SendMessageFailed,
		VPX_PARSE_TAIL 
	} VPX_ParseType;

		


/*------------------------------------------------------------------
/						TYPEDEFS
/--------------------------------------------------------------------*/

// typedef int (*VPX_CALLBACK)( int msg, int submsg, int param1, int param2, void* userPtr);

typedef float VPX_RealType ;

typedef struct {
    VPX_RealType  x ;
    VPX_RealType  y ;
    } VPX_RealPoint ;

typedef struct {
    VPX_RealType  x ;
    VPX_RealType  y ;
    VPX_RealType  z ;
    } VPX_RealPoint3D ;

typedef struct {
    VPX_RealType  left ;
    VPX_RealType  top ;
    VPX_RealType  right ;
    VPX_RealType  bottom ;
    } VPX_RealRect ;

typedef struct {
    VPX_RealType  x ;
    VPX_RealType  y ;
    VPX_RealType  z ;
    VPX_RealType  roll ;
    VPX_RealType  pitch ;
    VPX_RealType  yaw ;
    } VPX_PositionAngle ;

typedef struct {
    int  left ;
    int  top ;
    int  right ;
    int  bottom ;
    } VPX_IntRect ;


typedef signed short VPX_RoiHitListType[ MAX_ROI_BOXES ];

typedef struct
{
	VPX_RealPoint	glintPosition ;
	VPX_GlintDataQuality glintQuality ;
} VPX_GlintRecord;



/*------------------------------------------------------------------------------------
/	VPX_CalibrationEventRecord
/------------------------------------------------------------------------------------*/
typedef struct
{
	int				calEvent;
	int				index1;
	VPX_RealPoint 	stimPtA, stimPtB;
	int				slipMode;
	int				snapMode;
	int				singlePoint;
	int				zoomSize;
	int				eyes;
} VPX_CalibrationEventRecord;

// begin MATLAB FIX
#ifdef _IMPORTING_INTO_MATLAB
	#define  VPX_SendCommand   VPX_SendCommandString
#else
	VPX_DECLSPEC int CALLCONV VPX_SendCommand( char *szFormat, ...);
#endif
// end MATLAB FIX

/*------------------------------------------------------------------------------------
/	Function Prototypes
/------------------------------------------------------------------------------------*/

VPX_DECLSPEC int CALLCONV  VPX_SendCommandString( char *cmd );

VPX_DECLSPEC int CALLCONV  VPX_GetPupilAngle2( VPX_EyeType eyn, double *pa );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilCentroid2( VPX_EyeType eyn, VPX_RealPoint *pc );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilSize( VPX_RealPoint *ps );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilSize2( VPX_EyeType eyn, VPX_RealPoint *ps );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilDiameter2( VPX_EyeType eyn, double* pd);
VPX_DECLSPEC int CALLCONV  VPX_GetPupilPoint( VPX_RealPoint *pp );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilPoint2( VPX_EyeType eyn, VPX_RealPoint *pp );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilAspectRatio( double *ar );
VPX_DECLSPEC int CALLCONV  VPX_GetPupilAspectRatio2( VPX_EyeType eyn, double *ar );

VPX_DECLSPEC int CALLCONV  VPX_GetGlintCentroid2( VPX_EyeType eyn, VPX_RealPoint *gc );
VPX_DECLSPEC int CALLCONV  VPX_GetGlintPoint( VPX_RealPoint *gp );
VPX_DECLSPEC int CALLCONV  VPX_GetGlintPoint2( VPX_EyeType eyn, VPX_RealPoint *gp );

VPX_DECLSPEC int CALLCONV  VPX_GetDiffVector( VPX_RealPoint *dv);
VPX_DECLSPEC int CALLCONV  VPX_GetDiffVector2( VPX_EyeType eyn, VPX_RealPoint *dv );

VPX_DECLSPEC int CALLCONV  VPX_GetPupilOvalRect( VPX_RealRect *ovr);
VPX_DECLSPEC int CALLCONV  VPX_GetPupilOvalRect2( VPX_EyeType eyn, VPX_RealRect *ovr );

VPX_DECLSPEC int CALLCONV  VPX_GetGazePoint( VPX_RealPoint *gp );
VPX_DECLSPEC int CALLCONV  VPX_GetGazePoint2( VPX_EyeType eyn, VPX_RealPoint *gp );
VPX_DECLSPEC int CALLCONV  VPX_GetGazePointSmoothed2( VPX_EyeType eyn, VPX_RealPoint *gp );
VPX_DECLSPEC int CALLCONV  VPX_GetGazePointCorrected2( VPX_EyeType eyn, VPX_RealPoint *gp );
VPX_DECLSPEC int CALLCONV  VPX_GetGazeAngle2( VPX_EyeType eyn, VPX_RealPoint *ga );
VPX_DECLSPEC int CALLCONV  VPX_GetGazeAngleSmoothed2( VPX_EyeType eyn, VPX_RealPoint *ga );
VPX_DECLSPEC int CALLCONV  VPX_GetGazeAngleCorrected2( VPX_EyeType eyn, VPX_RealPoint *ga );
VPX_DECLSPEC int CALLCONV  VPX_GetGazeBinocular( VPX_RealPoint *gb );

VPX_DECLSPEC int CALLCONV  VPX_GetDataQuality2( VPX_EyeType eyn, VPX_DataQuality *quality );

VPX_DECLSPEC int CALLCONV  VPX_GetTotalVelocity(double *velocity);
VPX_DECLSPEC int CALLCONV  VPX_GetTotalVelocity2( VPX_EyeType eyn, double *velocity );
VPX_DECLSPEC int CALLCONV  VPX_GetComponentVelocity(  VPX_RealPoint *velocity );	
VPX_DECLSPEC int CALLCONV  VPX_GetComponentVelocity2( VPX_EyeType eyn, VPX_RealPoint *velocity );	
VPX_DECLSPEC int CALLCONV  VPX_GetVelocityBinocular( double *velocity );

VPX_DECLSPEC int CALLCONV  VPX_GetFixationSeconds2( VPX_EyeType eyn, double *fs );
VPX_DECLSPEC int CALLCONV  VPX_GetDrift2( VPX_EyeType eyn, double *drift);

VPX_DECLSPEC int CALLCONV  VPX_GetTorsion(double *degrees);
VPX_DECLSPEC int CALLCONV  VPX_GetTorsion2( VPX_EyeType eyn, double *degrees );

VPX_DECLSPEC VPX_EyeEventType CALLCONV  VPX_GetBlinkEvent2( VPX_EyeType eyn );
VPX_DECLSPEC VPX_EyeEventType CALLCONV  VPX_GetEyeMovementEvent2( VPX_EyeType eyn );

VPX_DECLSPEC int CALLCONV  VPX_GetDataTime2( VPX_EyeType eyn, double *tm);
VPX_DECLSPEC int CALLCONV  VPX_GetDataDeltaTime2( VPX_EyeType eyn, double *tm );
VPX_DECLSPEC int CALLCONV  VPX_GetStoreTime2( VPX_EyeType eyn, double *tm);
VPX_DECLSPEC int CALLCONV  VPX_GetStoreDeltaTime2( VPX_EyeType eyn, double *tm);


VPX_DECLSPEC int CALLCONV  VPX_GetHeadPositionAngle( VPX_PositionAngle *pa );
VPX_DECLSPEC int CALLCONV  VPX_GetPanelHit( VPX_EyeType eyn, int *panelNumber );
VPX_DECLSPEC int CALLCONV  VPX_GetVergenceAngle( VPX_RealType *angleDeg );
VPX_DECLSPEC int CALLCONV  VPX_GetGazePoint3D( VPX_RealPoint3D *gazePointCM );
VPX_DECLSPEC int CALLCONV  VPX_GetVersionAngle( VPX_RealPoint *angleDeg );
VPX_DECLSPEC int CALLCONV  VPX_GetVersionComponentVelocity( VPX_RealPoint *velDeg_Sec );
VPX_DECLSPEC int CALLCONV  VPX_GetVersionTotalVelocity( double *velDeg_Sec );

VPX_DECLSPEC int CALLCONV  VPX_GetStatus( VPX_StatusItem statusRequest );

VPX_DECLSPEC int CALLCONV  VPX_GetMeasuredScreenSize( VPX_RealPoint *sz );
VPX_DECLSPEC int CALLCONV  VPX_GetMeasuredViewingDistance( VPX_RealType *vd );

VPX_DECLSPEC int CALLCONV  VPX_GetROI_RealRect(int n, VPX_RealRect *rr );
VPX_DECLSPEC int CALLCONV  VPX_SetROI_isoEccentric( int nTargets );

VPX_DECLSPEC int CALLCONV  VPX_ROI_GetHitListLength( VPX_EyeType eyn );
VPX_DECLSPEC int CALLCONV  VPX_ROI_GetHitListItem( VPX_EyeType eyn, int NthHit );
VPX_DECLSPEC int CALLCONV  VPX_ROI_GetEventListItem( VPX_EyeType eyn, int NthEvent );
VPX_DECLSPEC int CALLCONV  VPX_ROI_MakeHitListString(VPX_EyeType eyn, char *dataString, int maxStringLength, BOOL indicateOverflow, char *noHitsString);
VPX_DECLSPEC int CALLCONV  VPX_GetCalibrationStimulusPoint2( VPX_EyeType eyn, int ixPt, VPX_RealPoint *calPt );
VPX_DECLSPEC int CALLCONV  VPX_GetCalibrationEventRecord( VPX_CalibrationEventRecord *calEventRec );

VPX_DECLSPEC BOOL CALLCONV  VPX_IsPrecisionDeltaTimeAvailableQ(void);
VPX_DECLSPEC double CALLCONV  VPX_GetPrecisionDeltaTime( double *inHoldTime, int resetHoldTime );

VPX_DECLSPEC int CALLCONV  VPX_LaunchApp( char* appNameArg, char* cmdLineArg );
VPX_DECLSPEC int CALLCONV  VPX_GetViewPointAppCount(int *apps);

VPX_DECLSPEC int CALLCONV  VPX_GetMessageListLength( int *num );
VPX_DECLSPEC int CALLCONV  VPX_GetMessagePostCount( int *num );
VPX_DECLSPEC int CALLCONV  VPX_RemoveNonRespondingMessageTargets(void);

////// 294
//////VPX_DECLSPEC int CALLCONV  VPX_InsertCallback( VPX_CALLBACK callbackFunction, void* userPtr );
//////VPX_DECLSPEC int CALLCONV  VPX_RemoveCallback( VPX_CALLBACK callbackFunction );
VPX_DECLSPEC int CALLCONV  VPX_GetCallbackListLength(void);
VPX_DECLSPEC int CALLCONV  VPX_GetLayeredAppCallbackListLength(void);

VPX_DECLSPEC int CALLCONV  VPX_VersionMismatch( double version );
VPX_DECLSPEC double CALLCONV  VPX_GetDLLVersion(void);
VPX_DECLSPEC double CALLCONV  VPX_GetRevisionNumber(void);



VPX_DECLSPEC int CALLCONV  VPX_DebugSDK(int onOff);



/*------------------------------------------------------------------------------------
/	Function Prototype Wrapper Macros
/------------------------------------------------------------------------------------*/
#define VPX_GetGazePointSmoothed(_p) VPX_GetGazePointSmoothed2(EYE_A, _p)
#define VPX_GetDataQuality(_p)  VPX_GetDataQuality2(EYE_A, _p)
#define VPX_GetDataTime(_p)  VPX_GetDataTime2(EYE_A, _p)
#define VPX_GetDataDeltaTime(_p)  VPX_GetDataDeltaTime2(EYE_A, _p)
#define VPX_GetViewPointSeconds VPX_GetPrecisionDeltaTime(SINCE_PRECISE_INIT_TIME,LEAVE_PRECISE_HOLD_TIME)
#define VPX_GetVersionAngles(_p) VPX_GetVersionAngle(_p)
#define VPX_GetFixationSeconds(_p) VPX_GetFixationSeconds2(EYE_A, _p)
#define VPX_GetCalibrationStimulusPoint(_ix, _p) VPX_GetCalibrationStimulusPoint2(EYE_A, _ix, _p)

#ifdef __cplusplus
}
#endif

#endif // #ifndef VPX_DOT_H

