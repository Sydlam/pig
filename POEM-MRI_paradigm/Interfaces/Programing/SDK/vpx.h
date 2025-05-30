/*------------------------------------------------------------------
/   VPX.h
/
/		VPX_*  functions are __cdecl
/		vpxs_* functions are __stdcall WINAPI
/
/	When importing the dll into matlab, you must do:
/		#define  _IMPORTING_INTO_MATLAB
/
/	If you do not want to include <windows.h>, 
/	you must do the following before calling this .h file:
/		#define  _NO_WINDOWS_ 
/
/
/						- DO NOT MODIFY ANYTHING BELOW !!!
/
/--------------------------------------------------------------------*/

#ifndef VPX_DOT_H
#define VPX_DOT_H

#ifndef _NO_WINDOWS_
#include <windows.h>
#endif

#define VPX_SDK_VERSION		295.111

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

#define VPX_DAT_FRESH_BIT_FLAG_ThinnedOp	0x00000001
#define VPX_DAT_FRESH_BIT_FLAG_Heartbeat	0x00000002

#define REALTIME_DATA_BUFFER_EyeA		0x00000001
#define REALTIME_DATA_BUFFER_EyeB		0x00000002
#define REALTIME_DATA_BUFFER_Binocular	0x00000004
#define REALTIME_DATA_BUFFER_Head		0x00000008
#define REALTIME_IMAGE_BUFFER_EyeA		0x00000010
#define REALTIME_IMAGE_BUFFER_EyeB		0x00000020
#define REALTIME_IMAGE_BUFFER_SceneA	0x00000040
#define REALTIME_IMAGE_BUFFER_SceneB	0x00000080
#define REALTIME_ALL					0xFFFFFFFF

#define VPX_LatestData				((unsigned __int64)-1)

#define MAX_IMAGE_BUFFER_WIDTH		640
#define MAX_IMAGE_BUFFER_HEIGHT		480

#define VPX_MAX_COMMAND_STRING		1024

#define tenK 10000

#define MIN_ROI_INDEX	1
#define MAX_ROI_INDEX	99
#define MAX_ROI_BOXES	(MAX_ROI_INDEX + 1)

#define MAX_ROI_DISPLAY  10
#define ROI_NOT_HIT   -9999
#define ROI_NO_EVENT  -9999

#define MAX_GLINTS 4

#define VPX_EyeType INT
#define EYE_A 					0
#define EYE_B 					1
#define SCENE_A					2
#define SCENE_B					3
#define OBSERVER				4
#define VIDEO_SCREEN			5
#define EYE_MOVIE_CHANNEL   	6
#define DUAL_EYE_MOVIE_CHANNEL  7
#define MAX_ROUTING 			8

#define VPX_MESSAGE "VPX_message"

#define PointInRectQ(pt,rr) ( ( pt.x < rr.right ) && ( pt.y < rr.bottom ) && ( rr.left < pt.x ) && ( rr.top < pt.y ) )

#define VPX_InitializeSDK VPX_InitializeSDK_Function(sizeof(VPX_PositionAngle), sizeof(VPX_EyeDataRecord), sizeof(VPX_BinocularDataRecord), sizeof(VPX_GetImageRecord), (float)VPX_SDK_VERSION);

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

typedef enum {
		VPX_CALLBACK_HEAD,
		VPX_CALLBACK_INSERTED,
		VPX_CALLBACK_INSERT_DUPLICATE,
		VPX_CALLBACK_LIST_LENGTH_EXCEEDED,
		VPX_CALLBACK_INSERT_ERROR,
		VPX_CALLBACK_REMOVED,
		VPX_CALLBACK_NOT_FOUND,
		VPX_CALLBACK_LIST_IS_EMPTY,
		VPX_CALLBACK_REMOVE_ERROR,
		VPX_CALLBACK_TAIL
	} VPX_CallbackResult;
		
typedef enum { 
		VPX_NO_ERROR = 0,
		VPX_IMAGE_BUFFER_OK = 0,

		VPX_ERROR_InternalError = -1,
		VPX_ERROR_InternalException = -2,
		VPX_ERROR_InvalidWidthStep = -3,
		VPX_ERROR_InvalidWidth = -4,
		VPX_ERROR_InvalidHeight = -5,
		VPX_ERROR_InvalidSourceBuffer = -6,
		VPX_ERROR_InvalidRect = -7,
		VPX_ERROR_InvalidBitsPerChannel = -8,
		VPX_ERROR_InvalidColorChannels = -9,
		VPX_ERROR_NoAlphaChannel = -10,
		VPX_ERROR_ImageFlip = -11,
		VPX_ERROR_ImageSwapRedAndBlue = -12,
		VPX_ERROR_ImageSetAlphaValue = -13,
		VPX_ERROR_InvalidEyeType = -14,
		VPX_ERROR_InvalidCount = -15,
		VPX_ERROR_InvalidBufferFlags = -16,
		VPX_ERROR_InvalidSize = -17,
		VPX_ERROR_InvalidArgPtr = -18,
		VPX_ERROR_OutOfMemory = -19,
		VPX_ERROR_InvalidBuffer = -20,
		VPX_ERROR_InvalidBufferSize = -21,
		VPX_ERROR_InvalidStructSize = -22,
		VPX_ERROR_InvalidSDKVersion = -23,
		VPX_ERROR_IndexNoLongerValid = -24,
		VPX_ERROR_IndexingIntoUnbufferedData = -25,
		VPX_ERROR_IndexOutOfRange = -26,
	} VPX_SDKFunctionResult;

typedef enum {
		VPX_GetImage_8U = 8,
		VPX_GetImage_32F = 32,
	} VPX_GetImageBitsPerChannel;

typedef enum {
		VPX_GetImage_BGRA = 4,
	} VPX_GetImageColorChannels;


/*------------------------------------------------------------------
/						TYPEDEFS
/--------------------------------------------------------------------*/

typedef INT (*VPX_CALLBACK)(INT msg, INT submsg, INT param1, INT param2, void* userPtr);

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

typedef struct {
    int sourceBuffer;
    int destWidthStep;
    int destWidth;
    int destHeight;
	VPX_IntRect destRect;
	VPX_GetImageBitsPerChannel destBitsPerChannel;
	VPX_GetImageColorChannels destColorChannels;

	int flipAroundHorizontalAxis;
	int flipAroundVerticalAxis;
	int swapRedAndBlue;
	int setAlphaValue;
	unsigned char alphaValue;

	} VPX_GetImageRecord;

typedef signed short VPX_RoiHitListType[ MAX_ROI_BOXES ];

typedef struct
{
	VPX_RealPoint	glintPosition ;
	VPX_GlintDataQuality glintQuality ;
} VPX_GlintRecord;


/*------------------------------------------------------------------
/						VPX_EyeDataRecord
/--------------------------------------------------------------------*/
typedef struct { 
		double		torsionDegrees ;
		double		pupilAspectRatio ;
		double		dataTime ;
		double		dataDeltaTime ;
		double		storeTime ;
		double		storeDeltaTime ;
		double		fixationSeconds ;
		double		totalDrift ;
		double		totalVelocity ;

		VPX_RealPoint	 gazePoint ;
		VPX_RealPoint	 gazePointSmoothed ;
		VPX_RealPoint	 gazePointCorrected ;
		VPX_RealPoint	 gazeAngle ;
		VPX_RealPoint	 gazeAngleSmoothed ;
		VPX_RealPoint	 gazeAngleCorrected ;
		VPX_RealPoint	 pupilSize ;
		double			 pupilDiameter_MM ;
		double			 pupilAngle ;
		int				 regionCode ;
		int				 fixationDuration ;
		VPX_EyeEventType blinkEvent ;
		VPX_EyeEventType moveEvent ;
		VPX_RealPoint	 componentVelocity ;

		VPX_RealPoint	pupilCentroid ;
		VPX_RealPoint	glintCentroid ;
		VPX_RealRect	pupilOvalRect ;
		VPX_RealPoint	pupilPosition ;
		VPX_RealPoint	glintPosition ;
		VPX_RealPoint	diffVector ;
		VPX_GlintRecord	glintList[MAX_GLINTS] ;
		int				glintCount ;
		int				dataQuality ;

		int					panelHit ;

		VPX_RoiHitListType  roiHitList ;
		VPX_RoiHitListType  roiEventList ;
		int					roiHitListLength ;

		VPX_RealType	framesPerSecond ;

		VPX_EyeType		eye ;

} VPX_EyeDataRecord; 

/*------------------------------------------------------------------------------------
/	VPX_BinocularDataRecord
/------------------------------------------------------------------------------------*/
typedef struct
{
	// From VP.
	double cyclovergence;
	double disparity;
	double velocityBinocular;
	VPX_RealPoint gazeBinocular;

	// From 3DWS
	VPX_RealType vergenceAngle_Deg;
	VPX_RealPoint3D vergedGazePoint_CM;
	VPX_RealPoint versionAngle_Deg;
	VPX_RealPoint versionComponentVelocity_Deg_Sec;
	double versionTotalVelocity_Deg_Sec;

} VPX_BinocularDataRecord;

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

VPX_DECLSPEC POINT CALLCONV  VPX_GetCursorPosition(void);

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
VPX_DECLSPEC int CALLCONV  VPX_drawROI( HWND hWnd, int activeRegion );
VPX_DECLSPEC int CALLCONV  VPX_ROI_GetHitListLength( VPX_EyeType eyn );
VPX_DECLSPEC int CALLCONV  VPX_ROI_GetHitListItem( VPX_EyeType eyn, int NthHit );
VPX_DECLSPEC int CALLCONV  VPX_ROI_GetEventListItem( VPX_EyeType eyn, int NthEvent );
VPX_DECLSPEC int CALLCONV  VPX_ROI_MakeHitListString(VPX_EyeType eyn, char *dataString, int maxStringLength, BOOL indicateOverflow, char *noHitsString);
VPX_DECLSPEC int CALLCONV  VPX_ROI_MakeHitListString_EDR(VPX_EyeDataRecord* pEyeDataRecord, char *dataString, int maxStringLength, BOOL indicateOverflow, char *noHitsString);

VPX_DECLSPEC int CALLCONV  VPX_GetCalibrationStimulusPoint2( VPX_EyeType eyn, int ixPt, VPX_RealPoint *calPt );
VPX_DECLSPEC int CALLCONV  VPX_GetCalibrationEventRecord( VPX_CalibrationEventRecord *calEventRec );

VPX_DECLSPEC BOOL CALLCONV  VPX_IsPrecisionDeltaTimeAvailableQ(void);
VPX_DECLSPEC double CALLCONV  VPX_GetPrecisionDeltaTime( double *inHoldTime, int resetHoldTime );

VPX_DECLSPEC int CALLCONV  VPX_LaunchApp( char* appNameArg, char* cmdLineArg );
VPX_DECLSPEC int CALLCONV  VPX_GetViewPointAppCount(int *apps);

VPX_DECLSPEC int CALLCONV  VPX_InsertMessageRequest(HWND hWnd, UINT msg );
VPX_DECLSPEC int CALLCONV  VPX_RemoveMessageRequest(HWND hWnd );
VPX_DECLSPEC int CALLCONV  VPX_GetMessageListLength( int *num );
VPX_DECLSPEC int CALLCONV  VPX_GetMessagePostCount( int *num );
VPX_DECLSPEC int CALLCONV  VPX_RemoveNonRespondingMessageTargets(void);
VPX_DECLSPEC int CALLCONV  VPX_InsertCallback( VPX_CALLBACK callbackFunction, void* userPtr );
VPX_DECLSPEC int CALLCONV  VPX_RemoveCallback( VPX_CALLBACK callbackFunction );
VPX_DECLSPEC int CALLCONV  VPX_GetCallbackListLength(void);
VPX_DECLSPEC int CALLCONV  VPX_GetLayeredAppCallbackListLength(void);

VPX_DECLSPEC int CALLCONV  VPX_VersionMismatch( double version );
VPX_DECLSPEC double CALLCONV  VPX_GetDLLVersion(void);
VPX_DECLSPEC double CALLCONV  VPX_GetRevisionNumber(void);

VPX_DECLSPEC int CALLCONV  VPX_SetEyeImageWindow( VPX_EyeType eyn, HWND hWnd );
VPX_DECLSPEC int CALLCONV  VPX_SetEyeImageDisplayRect( VPX_EyeType eyn, RECT displayRect );
VPX_DECLSPEC int CALLCONV  VPX_SetExternalStimulusWindow( HWND hWnd );

VPX_DECLSPEC HWND CALLCONV  VPX_GetViewPointStimulusWindow(void);
VPX_DECLSPEC HWND CALLCONV  VPX_GetViewPointGazeSpaceWindow(void);

VPX_DECLSPEC int CALLCONV  VPX_DebugSDK(int onOff);

VPX_DECLSPEC int CALLCONV  VPX_RectFrame(HDC hdc, int x1, int y1, int x2, int y2, int t);
VPX_DECLSPEC int CALLCONV  VPX_EllipseFrame(HDC hdc, int x1, int y1, int x2, int y2, int t);

VPX_DECLSPEC int CALLCONV  VPX_WindowRECT2RealRect( RECT nr, RECT clientRect, VPX_RealRect * rr );
VPX_DECLSPEC int CALLCONV  VPX_RealRect2WindowRECT( VPX_RealRect rr, RECT clientRect, RECT * scaledRect );
VPX_DECLSPEC int CALLCONV  VPX_LParam2RealPoint( LPARAM codedLoc, VPX_RealPoint *pt );
VPX_DECLSPEC int CALLCONV  VPX_LParam2RectPoint( LPARAM codedLoc, RECT clientRect, POINT *pt );

VPX_DECLSPEC int CALLCONV  VPX_SetRealtimeBufferSize( unsigned __int32 uiBufferFlags, unsigned __int32 uiSize );
VPX_DECLSPEC unsigned __int32 CALLCONV  VPX_EnableRealtimeBuffering( int iEnable );
VPX_DECLSPEC unsigned __int32 CALLCONV  VPX_GetRealtimeBufferIndex(void);
VPX_DECLSPEC unsigned __int64 CALLCONV  VPX_GetRealtimeBufferedCountSinceEnabled(void);
VPX_DECLSPEC int CALLCONV  VPX_GetRealtimeHeadPositionAngles( unsigned __int64 uiIndex, __int32 iCount, VPX_PositionAngle* psHeadPositionAngles );
VPX_DECLSPEC int CALLCONV  VPX_GetRealtimeEyeDataRecords( VPX_EyeType iEye, unsigned __int64 uiIndex, __int32 iCount, VPX_EyeDataRecord* psEyeDataRecords );
VPX_DECLSPEC int CALLCONV  VPX_GetRealtimeBinocularDataRecords( unsigned __int64 uiIndex, __int32 iCount, VPX_BinocularDataRecord * psBinocularDataRecords );
VPX_DECLSPEC int CALLCONV  VPX_GetRealtimeImageBufferData( VPX_GetImageRecord gir, unsigned __int64 uiIndex, __int32 iCount, char* pcImageBuffers );

VPX_DECLSPEC int CALLCONV  VPX_InitializeSDK_Function(__int32 positionAngleSize,
													  __int32 eyeDataRecordSize,
													  __int32 binocularDataRecordSize,
													  __int32 getImageRecordSize,
													  float SDK_Version
													  );

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

