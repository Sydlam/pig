// s2255.dll Please see manual at http://www.sensoray.com/2255
// 4/4/2013 (added S2255_SetOsd text onscreen display)
#ifndef S2255F_H
#define S2255F_H

#include "s2255.h"
#define S2255_SPEC __declspec(dllimport)

extern "C" {
S2255_SPEC int __stdcall S2255_DeviceOpen(int board, HANDLE *hdev);
S2255_SPEC int __stdcall S2255_DeviceClose(HANDLE hdev);
S2255_SPEC int __stdcall S2255_SetMode(HANDLE hdev, int channel, MODE2255 *mode);
S2255_SPEC int __stdcall S2255_RegBuffer(HANDLE hdev, int channel, BUFFER *pBuf, UINT32 bufsize);
S2255_SPEC int __stdcall S2255_DqBuf(HANDLE hdev, int channel,int frmnum );
S2255_SPEC int __stdcall S2255_StartAcquire(HANDLE hdev, int channel, HANDLE *phevent);
S2255_SPEC int __stdcall S2255_StopAcquire(HANDLE hdev, int channel);
S2255_SPEC int __stdcall S2255_GetSN(HDEVICE hdev, SN2255 *sn );
// returns firmware version
S2255_SPEC int __stdcall S2255_GetFirmware(HDEVICE hdev, UINT32 *usb, UINT32 *dsp);
// returns Driver version and DLL version
S2255_SPEC int __stdcall S2255_GetVersions(HDEVICE hdev, UINT32 *dll, UINT32 *driver);

// blocking call to capture single frame.
// less efficient than StartAcquire/StopAcquire looping capture
// please see manual.  It is not required to use this function to get frames
S2255_SPEC int __stdcall S2255_GrabFrame(HDEVICE hdev, int chn, unsigned char *pFrame, unsigned long size, unsigned long timeout, BITMAPINFO *lpbmi);

S2255_SPEC UINT32 __stdcall S2255_GetImageSize( MODE2255 *mode);
S2255_SPEC UINT32 __stdcall S2255_GetVidStatus( HDEVICE hdev, int chn, UINT32 *pStatus);

// queries state of the buffer.
// returns:
// 0 if unused, available or free
// 1 if currently being filled  (should not use buffer in this case)
// 2 if ready or filled (needs DEQUEUED after use).  Will get an signal when this happens
//-1 if err
S2255_SPEC int __stdcall S2255_QueryBuf(HDEVICE hdev, int chn, int frmnum);
S2255_SPEC int __stdcall S2255_QueryBufExt(HDEVICE hdev, int chn, int frmnum, unsigned int *ts);


// if *pCount == 0 the number of attached devices is set in *pCount
// if *pCount != && pDevices != NULL, then pDevices assumed to point a 
//    list of at least *pCount DEVINFO2255
// structures which get filled in with board number and serial number 
// information.
S2255_SPEC int __stdcall S2255_Enumerate(int *pCount, DEVINFO2255 *pDevices);

// see s2255_osd in s2255.h
S2255_SPEC int __stdcall S2255_SetOsd(HDEVICE hdev, s2255_osd *osd);



// backward compatibility
// Note: These are just renamed functions of the above.  
// The names were changed to make the style more consistent
S2255_SPEC int __stdcall S2255_enumerate(int *pCount, struct s2255_device_info *pDevices);
S2255_SPEC int __stdcall S2255_query_buf(HDEVICE hdev, int chn, int frmnum);
S2255_SPEC int __stdcall S2255_query_buf_ext(HDEVICE hdev, int chn, int frmnum, unsigned int *ts);
S2255_SPEC UINT32 __stdcall S2255_get_image_size( MODE2255 *mode);
S2255_SPEC UINT32 __stdcall S2255_get_vid_status( HDEVICE hdev, int chn, UINT32 *pStatus);
S2255_SPEC int __stdcall S2255_DQBUF(HANDLE hdev, int channel,int frmnum );
// S2255_GetFrame obsoleted.  please upgrade to S2255_GrabFrame for easier access to BITMAPINFO
//S2255_SPEC int __stdcall S2255_GetFrame(HANDLE hdev, int channel, unsigned char *pFrame, unsigned long size, unsigned long timeout);



}
#endif
