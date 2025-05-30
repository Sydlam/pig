//----------------------------------------------------------------------------------------------------
//  DO NOT WRITE NEW CODE WITH THINGS FROM THIS FILE.
//  THEY ARE PROVIDED ONLY FOR BACKWARD COMPATIBILITY.
//----------------------------------------------------------------------------------------------------

#define VPX_SDK_LEGACY_VERSION 295.111
	// This VPX_SDK_LEGACY_VERSION constant is NOT checked by VPX_VersionsCheckError;
	// the user should verify that this is equal to VPX_SDK_VERSION in the file VPX.h




	/*---------------------------------/
	/		282.087  Legacy Below      /
	/---------------------------------*/


/*------------------------------------------------------------------
                           PARAMETERS
--------------------------------------------------------------------*/

/*
#ifndef _EYE_ENUMS_
#define _EYE_ENUMS_

typedef enum { DARK_PUPIL_Method, BRIGHT_PUPIL_Method }
        PupilType ;

typedef enum { PUPIL_ONLY_Method, GLINT_ONLY_Method, VECTOR_DIF_Method } // , UNUSABLE_Method
        FeaturesMethod ;

#endif
*/

typedef enum { 
	SetUp_Mode, 
	HighPrecision_Mode, 
	HighSpeed_Mode
	} VideoProcessingMode ;

#ifdef __cplusplus
extern "C" {
#endif

	/*---------------------------------/
	/		283.000  Legacy Below      /
	/---------------------------------*/

VPX_DECLSPEC PTCHAR CALLCONV  VPX_GetViewPointHomeFolder( PTCHAR pathString );
	// VPX_GetViewPointDirectory concatenates the full path to the ViewPoint folder
	// onto the end of the provided string.  Note: this is not a copy operation,
	// the user is responsible for providing a null sting if that is what is desired.
	// E.g. usage: 
	//		TCSTR pictureFile = TEXT("") ;				// clear
	//		VPX_GetViewPointHomeFolder( pictureFile );	// adds:  ...ViewPoint/"
	//		lstrcat( pictureFile, IMAGE_FOLDER );		// adds   "/Images/"
	//		lstrcat( pictureFile, myPicture.bmp );		// adds   "myPicture.bmp"
	//
	// RemoteLink Access: Undefined return value.


	/*---------------------------------/
	/		282.085  Legacy Below      /
	/---------------------------------*/


// Renamed for clarity in 2.8.2.*, do not use VPX_STATUS_StimulusWindowShape in future development.
#define VPX_STATUS_StimulusWindowShape VPX_STATUS_StimulusImageShape

VPX_DECLSPEC int CALLCONV  VPX_GetFixationDuration(DWORD *fd); // DEPRECATED
	// This function is DEPRECATED, instead use VPX_GetFixationSeconds.
	// VPX_GetFixationDuration retrieves the number of milliseconds
	// that the total velocity has been below the VelocityCriteria.
	// A zero value indicates a saccade is occurring.


// *** PROGRAM CONTROL *********************************
/*
		Please note that most of these individual function call commands
		are deprecated and should not be used in future development 
		if there is an equivalent command line parser (CLP) string 
		that can be sent via the routine: VPX_SendCommand(str);
*/

VPX_DECLSPEC int CALLCONV  VPX_AcceleratorKeys( BOOL tf );
	// This enables/disables the use of  accelerator keys for 
	// menu items.  If disabled ViewPoint will not respond to 
	// key board commands such as Control-Q to quit.  This is
	// useful when embedding VP into a 3rd party application
	// and the developer launches VP with only the EyeCamera
	// window showing, and he does not want this window to 
	// respond to VP menu item accelerator keys 

VPX_DECLSPEC int CALLCONV  VPX_QuitViewPoint();
	// VPX_QuitViewPoint is equivalent to the menu Quit or Exit.
	// All threads are terminated and VP terminates properly.
	// Use  VPX_SendCommand("quitViewPoint")  in future development.

// *** EyeCamera Window Scan Specifications ***

	// The following routines correspond to using the mouse in the EyeCamera window
	// to drag out pupil and glint scan rectangles and the glint scan offset vector.


VPX_DECLSPEC int CALLCONV  VPX_GetPupilScanArea( VPX_RealRect *rr );
VPX_DECLSPEC int CALLCONV  VPX_SetPupilScanArea( VPX_RealRect rr );
VPX_DECLSPEC int CALLCONV  VPX_GetGlintScanSize( VPX_RealPoint *rp );
VPX_DECLSPEC int CALLCONV  VPX_SetGlintScanSize( VPX_RealPoint rp );
VPX_DECLSPEC int CALLCONV  VPX_GetGlintScanOffset( VPX_RealPoint *rp );
VPX_DECLSPEC int CALLCONV  VPX_SetGlintScanOffset( VPX_RealPoint rp );
VPX_DECLSPEC int CALLCONV  VPX_GetGlintScanUnyokedOffset( VPX_RealPoint *rp );
VPX_DECLSPEC int CALLCONV  VPX_SetGlintScanUnyokedOffset( VPX_RealPoint rp );

// *** COMMANDS ***
// PLEASE NOTE: The following functions are part of the legacy interface and 
//  may not be supported in future versions.
// Whenever possible use VPX_SendCommandString()rather than the functions below.
// E.g.: rather than VPX_DataFile_NewUnique(), 
//   instead use VPX_SendCommandString("dataFile_NewUnique")

// Menu: File > DataFile > *
VPX_DECLSPEC int CALLCONV  VPX_DataFile_NewUnique();
VPX_DECLSPEC int CALLCONV  VPX_DataFile_Close();
VPX_DECLSPEC int CALLCONV  VPX_DataFile_Pause( BOOL tf );		// 1.0.43, this renames: VPX_CapturePause
VPX_DECLSPEC int CALLCONV  VPX_DataFile_StoreRejectData( BOOL tf );
VPX_DECLSPEC int CALLCONV  VPX_DataFile_InsertMarker( CHAR c );
VPX_DECLSPEC int CALLCONV  VPX_DataFile_Buffering( BOOL tf );

// Menu: Video > *
VPX_DECLSPEC int CALLCONV  VPX_Video_Freeze( BOOL tf );
VPX_DECLSPEC int CALLCONV  VPX_Video_ShowThresholdDots( BOOL tf );
VPX_DECLSPEC int CALLCONV  VPX_Video_ShowEyeCameraToolBar( BOOL tf );

VPX_DECLSPEC int CALLCONV  VPX_Video_Mode( VideoProcessingMode mode );
VPX_DECLSPEC int CALLCONV  VPX_Video_WindowVisible( BOOL tf );

VPX_DECLSPEC int CALLCONV  VPX_SetImageBrightness2( VPX_EyeType eyn, float value );
VPX_DECLSPEC int CALLCONV  VPX_SetImageContrast2( VPX_EyeType eyn, float value );
VPX_DECLSPEC int CALLCONV  VPX_SetImageBrightness( float value );
VPX_DECLSPEC int CALLCONV  VPX_SetImageContrast( float value );

VPX_DECLSPEC int CALLCONV  VPX_Video_Reset( void );

// Menu: Calibrate > *
VPX_DECLSPEC int CALLCONV  VPX_AutoCalibrate();
VPX_DECLSPEC int CALLCONV  VPX_StopCalibration();
VPX_DECLSPEC int CALLCONV  VPX_ReCalibratePoint( int code );
VPX_DECLSPEC int CALLCONV  VPX_SlipCorrection( int selection );	// 2.4.0.90 this replaces: VPX_EyeSpace_SlipCorrection
VPX_DECLSPEC int CALLCONV  VPX_SetCalibrationDensity( int nCalPointsCode );
VPX_DECLSPEC int CALLCONV  VPX_SetCalibrationPoints( int nCalPoints );
VPX_DECLSPEC int CALLCONV  VPX_SetCalibrationSpeed( int speed );
VPX_DECLSPEC int CALLCONV  VPX_SetCalibrationConfirm( BOOL tf );
VPX_DECLSPEC int CALLCONV  VPX_EyeSpace_SelectPoint( int selection );

// STIMWIND
VPX_DECLSPEC int CALLCONV  VPX_StimWind_Hide( void );
VPX_DECLSPEC int CALLCONV  VPX_StimWind_Adjustable( void );
VPX_DECLSPEC int CALLCONV  VPX_StimWind_FullDisplay( int monitor );
VPX_DECLSPEC int CALLCONV  VPX_StimWind_AutoShowOnCalibrate( BOOL tf );

// INTERFACE
VPX_DECLSPEC int CALLCONV  VPX_CursorControl( BOOL tf );

// MAIN CONTROLS
VPX_DECLSPEC int CALLCONV  VPX_SetPositiveLockThresholdTracking2( VPX_EyeType eyn, int tf );
VPX_DECLSPEC int CALLCONV  VPX_AutoThreshold2( VPX_EyeType eyn );
VPX_DECLSPEC int CALLCONV  VPX_SetPupilThreshold2( VPX_EyeType eyn, float value );  // normalized value range: 0.0 ... 1.0
VPX_DECLSPEC int CALLCONV  VPX_SetGlintThreshold2( VPX_EyeType eyn, float value );  // normalized value range: 0.0 ... 1.0
VPX_DECLSPEC int CALLCONV  VPX_SetPupilResolution2( VPX_EyeType eyn, float value ); // integer value range: 1 .. 20
VPX_DECLSPEC int CALLCONV  VPX_SetGlintResolution2( VPX_EyeType eyn, float value ); // integer value range: 1 .. 20
VPX_DECLSPEC int CALLCONV  VPX_SetPupilType2( VPX_EyeType eyn, int code );		  // See above, typedef PupilType
VPX_DECLSPEC int CALLCONV  VPX_SetFeatureMethod2( VPX_EyeType eyn, int code );	  // See above, typedef FeaturesMethod (Note plural)
//
VPX_DECLSPEC int CALLCONV  VPX_AutoThreshold(void); 
VPX_DECLSPEC int CALLCONV  VPX_SetPupilThreshold( float value ); 
VPX_DECLSPEC int CALLCONV  VPX_SetGlintThreshold( float value ); 
VPX_DECLSPEC int CALLCONV  VPX_SetPupilResolution( float value ); 
VPX_DECLSPEC int CALLCONV  VPX_SetGlintResolution( float value ); 
VPX_DECLSPEC int CALLCONV  VPX_SetPupilType( int code ); 
VPX_DECLSPEC int CALLCONV  VPX_SetFeatureMethod( int code ); 

VPX_DECLSPEC int CALLCONV  VPX_SetSmoothing( int nPoints );
VPX_DECLSPEC int CALLCONV  VPX_SetPupilOvalCriteria( float value );
VPX_DECLSPEC int CALLCONV  VPX_SetVelocityCriteria( float value );


// *** ROI ***

VPX_DECLSPEC int CALLCONV  VPX_SetROI_RealRect(int n, VPX_RealRect rr );	
	// Use: VPX_SendCommand("setROI_RealRect %d %g %g %g %g",roiIndex, rr.left, rr.top, rr.right, rr.bottom );
	
VPX_DECLSPEC int CALLCONV  VPX_SetROI_isoEccentric( int nTargets );
	//
	// RemoteLink Access: YES


	/*---------------------------------/
	/		282.071 Legacy Below       /
	/---------------------------------*/


/*------------------------------------------------------------------
/		VIEWPOINT DIRECTORY STRUCTURE PATH CONSTANTS
/--------------------------------------------------------------------*/
#define IMAGE_FOLDER			TEXT("/Images/")
#define SOUNDS_FOLDER			TEXT("/Sounds/")
#define SETTINGS_FOLDER			TEXT("/Settings/")
#define DATA_FOLDER  			TEXT("/Data/")
#define CALIBRATION_FOLDER  	TEXT("/Calibration/")
#define DOCUMENTATION_FOLDER	TEXT("/Documentation/")
#define SDK_FOLDER				TEXT("/SDK/")

/*------------------------------------------------------------------
/		LAUNCHING VIEWPOINT
/--------------------------------------------------------------------*/
#define VPX_LaunchWithFreeCameraWindow 1
#define VPX_LaunchWithHiddenMainWindow 2
	// e.g., int options = VPX_LaunchWithFreeCameraWindow | VPX_LaunchWithHiddenMainWindow ;
	// 		 VPX_LaunchViewPointEx( options );
#define VPX_LaunchWithHidenMainWindow  2	
	// mispelling, replace with: VPX_LaunchWithHiddenMainWindow
VPX_DECLSPEC int CALLCONV  VPX_LaunchViewPoint();
	// DEPRECATED, instead use: VPX_LaunchApp( "ViewPoint.exe", "" );
VPX_DECLSPEC int CALLCONV  VPX_LaunchViewPointEx( int options );
	// DEPRECATED, instead use: VPX_LaunchApp( "ViewPoint.exe", " -freeEyeCamera -hideMain" ); etc.

/*------------------------------------------------------------------
/		ROI_InCode
/--------------------------------------------------------------------*/
VPX_DECLSPEC int CALLCONV  VPX_DisplayROI_InCode( HWND hWnd, int code );
	// DEPRECATED, Only for backward compatibility.
	// VPX_DisplayROI_InCode draws a text string of 
	// the form "__2____7__" in the window hWnd, showing 
	// the code argument has ROIs 2 and 7 as active.
VPX_DECLSPEC int CALLCONV  VPX_GetROI_InCode(int *code);
	// DEPRECATED, Only for backward compatibility.
	// INSTEAD USE: VPX_ROI_GetHitListItem and VPX_ROI_GetHitListLength
VPX_DECLSPEC int CALLCONV  VPX_GetROI_InCode2( VPX_EyeType eye, int *code);
	// DEPRECATED, Only for backward compatibility.
	// INSTEAD USE: VPX_ROI_GetHitListItem and VPX_ROI_GetHitListLength
	// VPX_GetROI_InCode retrieves a bit code indicating which of
	// the ROI the position of gaze is currently inside.

//////////


#ifdef __cplusplus
}
#endif
