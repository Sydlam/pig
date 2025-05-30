// app-2255-demoView.cpp : implementation of the Capp2255demoView class
// Copyright 2007-2009 (C)  Sensoray Corporation Inc.
// D.A.

#include "stdafx.h" 
#include "app-2255-demo.h"
#include "settings.h"
#include "format.h"  
#include "scale.h"
#include "framerate.h"
#include "color.h"
#include "osd.h"
#include "InputType.h"
#include "app-2255-demoDoc.h"
#include "app-2255-demoView.h"
#include ".\app-2255-demoview.h"
#include "s2255f.h"
#include "image.h"
#include "Shlwapi.h"
#include "vfw.h"

#include "assert.h"



extern struct s2255_device_info G_devices[8];
extern int G_num_devices;
// Capp2255demoView
IMPLEMENT_DYNCREATE(Capp2255demoView, CView)


// Command call backs
BEGIN_MESSAGE_MAP(Capp2255demoView, CView)
ON_COMMAND_RANGE(ID_ACQUIRE_START, ID_ACQUIRE_START4, OnAcquireStart)  
ON_COMMAND_RANGE(ID_ACQUIRE_STOP, ID_ACQUIRE_STOP4, OnAcquireStop)
ON_COMMAND_RANGE(ID_BOARD_1, ID_BOARD_8, OnBoard)  
ON_UPDATE_COMMAND_UI_RANGE(ID_ACQUIRE_START, ID_ACQUIRE_START4, OnUpdateAcquireStart)
ON_UPDATE_COMMAND_UI_RANGE(ID_ACQUIRE_STOP, ID_ACQUIRE_STOP4, OnUpdateAcquireStop)
ON_UPDATE_COMMAND_UI_RANGE(ID_BOARD_1, ID_BOARD_8, OnUpdateBoard)

ON_WM_ERASEBKGND()
ON_COMMAND(ID_VIEW_FRAMERATE, OnViewFramerate)
ON_COMMAND(ID_VIEW_TS, OnViewTS)
ON_UPDATE_COMMAND_UI(ID_VIEW_FRAMERATE, OnUpdateViewFramerate)
ON_UPDATE_COMMAND_UI(ID_VIEW_TS, OnUpdateViewTS)
ON_UPDATE_COMMAND_UI(ID_VIEW_DISPLAYIMAGE, OnUpdateViewDisplayimage)
ON_COMMAND(ID_VIEW_DISPLAYIMAGE, OnViewDisplayimage)
ON_COMMAND_RANGE(ID_SETTINGS_CHANNEL1, ID_SETTINGS_CHANNEL4, OnSettingsChannel)
ON_COMMAND(ID_SETTINGS_ALLCHANNELS, OnSettingsAllchannels)
ON_COMMAND(ID_ACQUIRE_STARTALL, OnAcquireStartall)
ON_COMMAND(ID_ACQUIRE_STOPALL, OnAcquireStopall)
ON_BN_CLICKED(ID_TOOLS_QUERYFW, OnQueryFW)
ON_BN_CLICKED(ID_TOOLS_QUERYSN, OnQuerySN)
ON_COMMAND(ID_RECORD_START, OnRecordStart)
ON_COMMAND(ID_RECORD_STOP, OnRecordStop)
ON_COMMAND(ID_RECORD_CHANNEL1, OnRecordChannel1)
ON_COMMAND(ID_RECORD_CHANNEL2, OnRecordChannel2)
ON_COMMAND(ID_RECORD_CHANNEL3, OnRecordChannel3)
ON_COMMAND(ID_RECORD_CHANNEL4, OnRecordChannel4)
ON_UPDATE_COMMAND_UI(ID_RECORD_CHANNEL1, OnUpdateRecord1)
ON_UPDATE_COMMAND_UI(ID_RECORD_CHANNEL2, OnUpdateRecord2)
ON_UPDATE_COMMAND_UI(ID_RECORD_CHANNEL3, OnUpdateRecord3)
ON_UPDATE_COMMAND_UI(ID_RECORD_CHANNEL4, OnUpdateRecord4)
ON_UPDATE_COMMAND_UI(ID_RECORD_START, OnUpdateRecordStart)
ON_UPDATE_COMMAND_UI(ID_RECORD_STOP, OnUpdateRecordStop)

ON_COMMAND(ID_RECORD_HELP, OnRecordHelp)
END_MESSAGE_MAP()


// Capp2255demoView construction/destruction
Capp2255demoView::Capp2255demoView()
{
}

Capp2255demoView::~Capp2255demoView()
{
}

BOOL Capp2255demoView::PreCreateWindow(CREATESTRUCT& cs)
{
    // TODO: Modify the Window class or styles here by modifying
    //  the CREATESTRUCT cs
    return CView::PreCreateWindow(cs);
}


// Capp2255demoView drawing
void Capp2255demoView::OnDraw(CDC* pDC)
{
    CView::OnDraw( pDC);
    return;
}


typedef struct 
{
    Capp2255demoDoc  *pDoc;
    Capp2255demoView *pView;
    int              channel;
} acq_thread_param_t;

// acquisition thread.  parameter is type (acq_thread_param_t *).
static DWORD WINAPI AcquireThread( LPVOID lpParameter)
{
    DWORD res;
    int i;
    int images = 0;
    acq_thread_param_t *param = (acq_thread_param_t *) lpParameter;
    DWORD last_tick_count = GetTickCount();
    HANDLE hobjects[2];
    // index to channels start at 0, channels 1-4
    int idx = param->channel - 1;
    int chn = param->channel;
    Capp2255demoDoc  *pDoc = param->pDoc; 
    Capp2255demoView *pView = param->pView;
    
    if( pDoc == NULL) {
        free(param);
        return (DWORD) -1;
    }
    // Check and make sure device handle is valid.
    if( pDoc->m_hdev == NULL) {
        AfxMessageBox(_T("device not open.  Please restart application"));
        free(param);
        pDoc->m_running[idx] = 0;
        pDoc->m_ack_thread[idx] = NULL;
        return (DWORD) -3;
    }
    
    // This capture mode uses continuous capture.  Check to see if occasional snapshots were used with 
    // single mode
    if( pDoc->m_mode[idx].single) {
        pDoc->m_mode[idx].single = 0;
        if( S2255_SetMode( pDoc->m_hdev, idx+1, &pDoc->m_mode[idx]) != 0) {
            AfxMessageBox(_T("Failed to set mode back to continuous capture"));
        }
    }
    
    // Create an event to stop this acquisition thread
    pDoc->m_stop_event[idx] = CreateEvent( NULL, TRUE, FALSE, NULL);
    
    //----------------------------------------
    // allocate space for pDoc->m_numbuf frames
    memset(&pDoc->m_buf[idx], 0, sizeof(pDoc->m_buf[idx]));
    pDoc->m_buf[idx].dwFrames = (ULONG) pDoc->m_numbuf;
    
    UINT32 size;
    size = S2255_GetImageSize( &pDoc->m_mode[idx]);
    for( i=0;i<pDoc->m_numbuf;i++) {
        pDoc->m_buf[idx].frame[i].pdata = (char *) malloc(size);
    }
    
    // done setting up buffers
    //----------------------------------------
    // Register user buffer and frames with the API(and driver) 
    if( S2255_RegBuffer( pDoc->m_hdev, idx+1, &pDoc->m_buf[idx], size) != 0) {
        AfxMessageBox(_T("Board already being used or failed to register buffer"));
        CloseHandle(pDoc->m_stop_event[idx]);
        pDoc->m_stop_event[idx] = NULL;
        pDoc->m_running[idx] = 0;
        
        // free buffers
        for( i=0;i<pDoc->m_numbuf;i++) {
            //pDoc->m_buf[idx].lpbmi[i]->bmiHeader.biSizeImage = 0;
            free( pDoc->m_buf[idx].frame[i].pdata );
        }
        free(param);
        pDoc->m_ack_thread[idx] = NULL;
        return (DWORD) -3;
    }
    

    // Start Acquisition
    if (S2255_StartAcquire( pDoc->m_hdev, chn, &pDoc->m_buf_event[idx]) != 0) {
        AfxMessageBox(_T("Start Acquire Failed"));
        CloseHandle(pDoc->m_stop_event[idx]);
        pDoc->m_stop_event[idx] = NULL;
        pDoc->m_running[idx] = 0;
        // free buffers
        
        for( i=0;i<pDoc->m_numbuf;i++) {
            //pDoc->m_buf[idx].lpbmi[i]->bmiHeader.biSizeImage = 0;
            free( pDoc->m_buf[idx].frame[i].pdata );
        }
        free(param);
        pDoc->m_ack_thread[idx] = NULL;
        return (DWORD) -4;
    }

    // set up events
    hobjects[1] = pDoc->m_buf_event[idx];
    hobjects[0] = pDoc->m_stop_event[idx];
    pDoc->m_recvd_buf[idx] = 0;
    while (1) {  
        res = WaitForMultipleObjects(2, hobjects, FALSE, 6000);
        if( res == WAIT_TIMEOUT) {
            // timeout waiting for frame.  should not get here
            OutputDebugString(_T("2255-demo. frame timeout"));
            continue;
        } else if(res == WAIT_OBJECT_0) {
            // WAIT_OBJECT_0 is stop event.  
            break;
        } else if(res == (WAIT_OBJECT_0 + 1)) {
            // update the frame rate
            DWORD diff;
            int frm_idx = pDoc->m_recvd_buf[idx];
            int buf_state;
            int buflen;
            UINT32 ts;
            DWORD tick_count = GetTickCount();
            pDoc->m_framecount++;
            // done with buffer, dq it
            buf_state = S2255_QueryBufExt(pDoc->m_hdev, idx + 1, frm_idx, &ts);
            if (buf_state != 2) {
                OutputDebugString(_T("out of sync\n"));
            }
            images++;
            // approximate the current frame rate
            diff = tick_count - last_tick_count;
            if( (images == 10) && diff ) {
                pDoc->cur_frame_rate[idx] = 10*1000/diff;
                images = 0;
                last_tick_count = tick_count;
            }
            // point to current RGB image for the channel
            pDoc->image[idx] = (unsigned char *)pDoc->m_buf[idx].frame[frm_idx].pdata;
            switch (pDoc->m_mode[idx].color & MASK_COLOR) {
                case COLOR_RGB:
                    buflen = pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth * pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight * 3;
                    break;
                case COLOR_Y8:
                    buflen = pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth * pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight * 1;
                    break;
                case COLOR_JPG:
                    buflen = pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biSizeImage;
                    break;
            }

                // do work with image.  EG. if snapshots being taken
            if (pDoc->m_bTriggerSnapshot[idx]) {
                switch (pDoc->m_mode[idx].color & MASK_COLOR) {
                case COLOR_RGB:
                    save_image_uncompressed( pDoc->image[idx], 
                        pDoc->m_strSnapshot[idx].GetBuffer(MAX_PATH),
                        pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,
                        pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth,
                        pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth*3,
                        0);
                    break;
                case COLOR_Y8:
                    save_image_uncompressed_mono( pDoc->image[idx], 
                        pDoc->m_strSnapshot[idx].GetBuffer(MAX_PATH),
                        pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,
                        pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth);
                    break;
                case COLOR_JPG:
                    {
                        FILE *fout = _tfopen(pDoc->m_strSnapshot[idx].GetBuffer(MAX_PATH), _T("wb+"));
                        if (fout != NULL) {
                            fwrite(pDoc->image[idx], 
                                1, 
                                pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biSizeImage,
                                fout);
                            fclose(fout);
                        } else {
                            OutputDebugString(_T("could not open file!\n"));
                        }
                    }
                    break;
                }
                pDoc->m_bTriggerSnapshot[idx] = FALSE;
            }
            // draw the image (if displaying the images)
            pView->DrawNewImage(idx, frm_idx, ts);
            if (pDoc->m_bRecording && (idx == pDoc->m_record_channel) && pDoc->pavi) {
                int hr;
                hr = AVIStreamWrite(pDoc->pavi, pDoc->recframes++, 1, pDoc->image[idx], buflen,0, NULL, NULL);
                if (hr != 0) {
                    OutputDebugString(TEXT("failed to record frame\n"));
                }
            }
            S2255_DqBuf( pDoc->m_hdev, chn, pDoc->m_recvd_buf[idx]);
            pDoc->m_recvd_buf[idx]++;
            if((unsigned int) pDoc->m_recvd_buf[idx] == pDoc->m_buf[idx].dwFrames) {
                pDoc->m_recvd_buf[idx] = 0;
            }
        }
    }
    
    // Thread loop exited.  Call S2255_StopAcquire to stop acquisition
    if( S2255_StopAcquire( pDoc->m_hdev, chn ) != 0) {
        //AfxMessageBox("Stop failed");
        OutputDebugString(_T("stop failed!"));
    }
    if (pDoc->m_bRecording && idx == pDoc->m_record_channel) {
        pDoc->StopRecordFile();
    }


    // Close our stop event
    CloseHandle(pDoc->m_stop_event[idx]);
    // Set event handles to NULL (m_buf_event[idx] closed in StopAcquire)
    pDoc->m_buf_event[idx] = NULL;
    pDoc->m_stop_event[idx] = NULL;
    // free user allocated buffers
    for( i=0;i<pDoc->m_numbuf;i++) {
        pDoc->m_buf[idx].lpbmi[i]->bmiHeader.biSizeImage = 0;
        free( pDoc->m_buf[idx].frame[i].pdata );
        pDoc->m_buf[idx].frame[i].pdata = NULL;
    }
    // Free the acquisition thread parameter
    free(param);
    // Set running state to 0, thread handle to null
    pDoc->m_running[idx] = 0;
    InvalidateRect(pView->m_hWnd, &pDoc->m_pos[idx], TRUE);
    // return success
    return 0;
}



// stop acquisition
void Capp2255demoView::OnAcquireStop(UINT nID)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = nID - ID_ACQUIRE_STOP;
    // register
    if( pDoc == NULL) 
        return;
    
    if (idx >= 4) {
        AfxMessageBox(_T("resource.h IDs must be sequential! failing\n"));
        return;
    }
    
    if( !pDoc->m_running[idx]) {
        AfxMessageBox(_T("S2255: Acquisition thread not running"));
        return;
    }
    SetEvent( pDoc->m_stop_event[idx]);
    // wait for acquisition thread to stop
    WaitForSingleObject( pDoc->m_ack_thread[idx], INFINITE);
	CloseHandle(pDoc->m_ack_thread[idx]);
	pDoc->m_ack_thread[idx] = NULL;
    if (pDoc->m_fps_changed[idx]) {
        pDoc->m_mode[idx].fdec = pDoc->m_prev_fdec[idx];
        S2255_SetMode(pDoc->m_hdev, (idx+1), &pDoc->m_mode[idx]);
        pDoc->m_fps_changed[idx] = 0;
    }
    
    
    pDoc->cur_frame_rate[idx] =-1;
    return;
}

//The only reason this function is overriden is to prevent flicker caused by
// painting the background on an active video window.
BOOL Capp2255demoView::OnEraseBkgnd(CDC* pDC)
{   
    CRect rect;
    HRGN rgn;
    int j;
    int width;
    int height;
    Capp2255demoDoc *pDoc = GetDocument();
    GetClientRect(&rect);
    rgn = CreateRectRgn(0,0, rect.Width(), rect.Height());
    // exclude each active draw window
    if (pDoc == NULL) {
        return CView::OnEraseBkgnd(pDC);
    }
    
    for( j = 0; j < MAX_CHANNELS; j++) {
        if( pDoc->m_running[j] ) {
            width = pDoc->m_pos[j].right - pDoc->m_pos[j].left;
            height = pDoc->m_pos[j].bottom - pDoc->m_pos[j].top;
            if ((pDoc->m_mode[j].color & MASK_COLOR) == COLOR_JPG)
                continue;
            if( pDoc->m_mode[j].scale == SCALE_2CIFS) {
                height /= 2;
                width /= 2;
            }
            else if (pDoc->m_mode[j].scale == SCALE_1CIFS || pDoc->m_mode[j].scale == SCALE_1CIFSF) {
                height /=4;
                width /=4;
            }
            ExcludeClipRect( pDC->m_hDC, pDoc->m_pos[j].left, 
                pDoc->m_pos[j].top, 
                pDoc->m_pos[j].left+ width ,
                pDoc->m_pos[j].top+height);
        }
    }
    FillRgn( pDC->m_hDC, rgn, GetSysColorBrush( COLOR_WINDOW));
    return TRUE;
}

// view framerate
void Capp2255demoView::OnViewFramerate()
{
    Capp2255demoDoc *pDoc = GetDocument();
    
    if( pDoc == NULL) {
        return;
    }
    pDoc->m_bViewFR = !pDoc->m_bViewFR;
    Invalidate(TRUE);
}

void Capp2255demoView::OnUpdateViewFramerate(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck( pDoc->m_bViewFR);
}

void Capp2255demoView::OnViewTS()
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pDoc->m_bViewTS = !pDoc->m_bViewTS;
    Invalidate(TRUE);
}

void Capp2255demoView::OnUpdateViewTS(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck( pDoc->m_bViewTS);
}

void Capp2255demoView::OnUpdateViewDisplayimage(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck( pDoc->m_bViewImage);
}

void Capp2255demoView::OnViewDisplayimage()
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pDoc->m_bViewImage = !pDoc->m_bViewImage;
    Invalidate(TRUE);
}

// initial update.  set the window size to default width,height
void Capp2255demoView::OnInitialUpdate()
{
    Capp2255demoDoc *pDoc = GetDocument();
    ASSERT(pDoc != NULL);
    CView::OnInitialUpdate();
    CRect rect;
    GetWindowRect( &rect);
    CWnd *main = ::AfxGetMainWnd();
    main->SetWindowPos(NULL, 0,0, pDoc->m_pos[0].right,pDoc->m_pos[0].bottom, SWP_NOMOVE);
}

void Capp2255demoView::OnUpdateAcquireStop(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = pCmdUI->m_nID - ID_ACQUIRE_STOP;
    if ((pDoc == NULL) || (idx >= MAX_CHANNELS))
        return;
    pCmdUI->SetCheck(pDoc->m_running[idx] ? 0 : 1);
}


void Capp2255demoView::OnUpdateAcquireStart(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = pCmdUI->m_nID - ID_ACQUIRE_START;
    
    if ((pDoc == NULL) || (idx >= MAX_CHANNELS))
        return;
    pCmdUI->SetCheck( pDoc->m_running[idx] ? 1 : 0);
}



// creates the acquisition thread for capturing and displaying frames
void Capp2255demoView::CreateAcquisitionThread( int channel)
{
    int idx = channel - 1;
    DWORD threadID;
    
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL)
        return;
    
    if( pDoc->m_running[idx]) {
        AfxMessageBox(_T("S2255: Acquisition thread already running"));
        return;
    }
    acq_thread_param_t *prm = (acq_thread_param_t *) malloc( sizeof( acq_thread_param_t ));
    if( prm == NULL) {
        AfxMessageBox(_T("out of memory\n"));
        return;
    }
    prm->channel = idx+1;
    prm->pDoc = pDoc;
    prm->pView = this;
    pDoc->m_running[idx] = 1;
    pDoc->m_ack_thread[idx] = CreateThread(NULL, NULL, &AcquireThread, prm, NULL, &threadID);
}


void Capp2255demoView::OnAcquireStart(UINT nID)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = nID - ID_ACQUIRE_START;
    BOOL bPAL = FALSE;
    CRect rect;
    CWnd *pWnd = ::AfxGetMainWnd();
    int maxW, maxH;
    
    assert(pDoc != NULL);
    pWnd->GetWindowRect(&rect);
    
    if (idx >= 4) {
        AfxMessageBox(_T("resource.h IDs must be sequential! failing\n"));
        return;
    }
    
    // begin of window resize code
    if( pDoc->m_mode[idx].format == FORMAT_PAL) {
        bPAL = TRUE;
    }
    
    switch (idx) {
    case 0: //channel 1
        maxW = bPAL ? PAL_W + 30 : NTSC_W + 30;
        maxH = bPAL ? PAL_H + 30 : NTSC_H + 30;
        break;
    case 1: //channel 2
        maxW = bPAL ? PAL_W * 2 + 30 : NTSC_W * 2 +30;
        maxH = bPAL ? PAL_H + 30 : NTSC_H + 30;
        break;
    case 2: //channel 3
        maxW = bPAL ? PAL_W + 10: NTSC_W + 10;
        maxH = bPAL ? PAL_H *2 + 30: NTSC_H * 2 + 30;
        break;
    case 3: //channel 4
        maxW = bPAL ? PAL_W * 2 + 30 : NTSC_W * 2 + 30;
        maxH = bPAL ? PAL_H * 2 + 30 : NTSC_H * 2 + 30;
        break;
    default:
        // should not get here
        return;
    }
    if ((rect.Width() <= maxW) || (rect.Height() <= maxH)) {
        // make large enough for all channels
        pWnd->SetWindowPos(NULL, 0, 0,
            (rect.Width() <= maxW) ? maxW : rect.Width(), 
            (rect.Height() <= maxH) ? maxH : rect.Height(),
            SWP_NOMOVE);
        
    }
    // end of window resize code    
    
    // start the acquisition
    CreateAcquisitionThread(idx+1);
    
}


// Called when new settings acquired
// chn 1 - 4 
void Capp2255demoView::OnNewSettings(int chn) 
{
    CPropertySheet sheet;
    CSettings      lvls;
    CFrameRate     rate;
    CFormat        fmt;
	CInputType	   input_type;
    CScale         scl;
    COsd           osd;
    BOOL           bRedraw = FALSE;
    CColor         clr;
    BOOL           bChanged = FALSE;
    int            res;
    BOOL           bALL= FALSE;
    int            idx = 0;
    BOOL           bPAL = FALSE;
    int            j;
    Capp2255demoDoc* pDoc = GetDocument();
    ASSERT_VALID(pDoc);
    if (!pDoc)
        return;
    
    // The following code just gathers all the changed settings and calls S2255_SetMode
    // if anything has changed
    if( chn < 0) {
        int k;
        for (k = 0; k < MAX_CHANNELS; k++) {
            if (pDoc->m_running[k]) {
                AfxMessageBox(_T("You must stop all acquisitions before changing settings for all channels"));
                return;
            }
        }
        bALL = TRUE;
        // work off channel 0 settings
        chn = 1;
    }
    for(j=0;j<MAX_CHANNELS;j++) {
        if( pDoc->m_mode[j].format == FORMAT_PAL) {
            bPAL = TRUE;
        }
    }
    idx = chn - 1;
    sheet.SetTitle(_T("Settings"));

    lvls.m_iBright = (int) pDoc->m_mode[idx].bright;
    lvls.m_iContrast = (int) pDoc->m_mode[idx].contrast;
    lvls.m_iHue = (int) pDoc->m_mode[idx].hue;
    lvls.m_iSat = (int) pDoc->m_mode[idx].saturation;
    
    lvls.pDoc = pDoc;
    lvls.m_channel = chn;
    lvls.mode = pDoc->m_mode[idx];
    
    rate.pDoc = pDoc;
    rate.m_channel = chn;
    rate.mode = pDoc->m_mode[idx];
    
    scl.m_index = (int) (pDoc->m_mode[idx].scale -1);
    fmt.m_index = (int) (pDoc->m_mode[idx].format -1);
    clr.m_index = (int) ((pDoc->m_mode[idx].color & MASK_COLOR) - 1);
    clr.m_iJPG = (pDoc->m_mode[idx].color & MASK_JPG_QUALITY) >> 8;
	input_type.m_index = (int) ((pDoc->m_mode[idx].color & MASK_INPUT_TYPE) >> 16);
	input_type.mode = pDoc->m_mode[idx];
	input_type.pDoc = pDoc;
	input_type.m_channel = chn;
    // Can't change scale, color or format while running
    // Note: user image memory is allocated in the AcquireThread 
    scl.m_bStreaming = pDoc->m_running[idx];
    clr.m_bStreaming = pDoc->m_running[idx];
    fmt.m_bStreaming = pDoc->m_running[idx];
    rate.m_bStreaming = pDoc->m_running[idx];
    input_type.m_bStreaming = pDoc->m_running[idx];
    if( pDoc->m_mode[idx].fdec != FDEC_5) {
        rate.m_index = (int) (pDoc->m_mode[idx].fdec - 1);
    }
    else {
        rate.m_index = (int) (pDoc->m_mode[idx].fdec - 2);
    }
    
    osd.pDoc = pDoc;
    osd.m_channel = chn;
    osd.osd = pDoc->m_osd[idx];


    sheet.AddPage( &lvls);
    sheet.AddPage( &input_type);
    sheet.AddPage( &rate);
    sheet.AddPage( &scl);
    sheet.AddPage( &fmt);
    sheet.AddPage( &clr);
    sheet.AddPage( &osd);
    
    res = (int) sheet.DoModal();
    
    if( res == IDOK) {
        // handle OSD
        int old_jpeg_quality;
        // update changed parameters
        if((unsigned int) lvls.m_iBright != pDoc->m_mode[idx].bright) {
            pDoc->m_mode[idx].bright = (UINT32) lvls.m_iBright;
            bChanged = TRUE;
        }
        if((unsigned int)  lvls.m_iContrast!= pDoc->m_mode[idx].contrast) {
            pDoc->m_mode[idx].contrast = (UINT32) lvls.m_iContrast;
            bChanged = TRUE;
        }
        if((unsigned int)  lvls.m_iHue != pDoc->m_mode[idx].hue) {
            pDoc->m_mode[idx].hue = (UINT32) lvls.m_iHue;
            bChanged = TRUE;
        }
        if((unsigned int)  lvls.m_iSat != pDoc->m_mode[idx].saturation) {
            pDoc->m_mode[idx].saturation = (UINT32) lvls.m_iSat;
            bChanged = TRUE;
        }
        if((unsigned int)  scl.m_index != (pDoc->m_mode[idx].scale - 1)) {
            pDoc->m_mode[idx].scale = (UINT32) (scl.m_index + 1);
            bChanged = TRUE;
            bRedraw = TRUE;
        }
        if((unsigned int)  fmt.m_index != (pDoc->m_mode[idx].format - 1)) {
            pDoc->m_mode[idx].format = (UINT32) (fmt.m_index + 1);
            bChanged = TRUE;
        }
        old_jpeg_quality = (pDoc->m_mode[idx].color & MASK_JPG_QUALITY) >> 8;
        if((unsigned int)  clr.m_index != ((pDoc->m_mode[idx].color & MASK_COLOR) - 1)) {
			pDoc->m_mode[idx].color &= ~MASK_COLOR;
            pDoc->m_mode[idx].color |= (UINT32) (clr.m_index + 1);
            bChanged = TRUE;
        }

        if((unsigned int)  input_type.m_index != ((pDoc->m_mode[idx].color & MASK_INPUT_TYPE) >> 16)) {
			pDoc->m_mode[idx].color &= ~MASK_INPUT_TYPE;
            pDoc->m_mode[idx].color |= (UINT32) (input_type.m_index << 16);
            bChanged = TRUE;
        }
        
        if (old_jpeg_quality != clr.m_iJPG) {
            bChanged = TRUE;
        }
        
        pDoc->m_mode[idx].color &= ~ MASK_JPG_QUALITY;
        pDoc->m_mode[idx].color |= (clr.m_iJPG << 8);
        
        if ((unsigned int) rate.m_index != (pDoc->m_mode[idx].fdec - 1)) {
            pDoc->m_mode[idx].fdec = (UINT32) (rate.m_index + 1);
            if( pDoc->m_mode[idx].fdec == 4) {
                pDoc->m_mode[idx].fdec = FDEC_5;
            }
            bChanged = TRUE;
        }
        pDoc->m_osd[idx] = osd.osd;
    } else {
        bChanged = lvls.bChanged;
        S2255_SetOsd(pDoc->m_hdev, &pDoc->m_osd[idx]);
    }
    
    if( !bALL) {
        if( bChanged ) {
            if( S2255_SetMode( pDoc->m_hdev,chn, &pDoc->m_mode[idx]) != 0) {
                AfxMessageBox(_T("Failed to set mode"));
            }
        }
    }
    else {
        for(j=0;j<MAX_CHANNELS;j++) {
            // always change for all channels
            //if( bChanged ) 
            if( res == IDOK)
            { 
                pDoc->m_mode[j] = pDoc->m_mode[0];
                if( S2255_SetMode( pDoc->m_hdev,j+1, &pDoc->m_mode[j]) != 0) {
                    AfxMessageBox(_T("Failed to set mode"));
                }
            }
        }
    }

    if( bChanged) {
        BOOL bPrevPAL = bPAL;
        // search through all channels.  If any pal, use PAL window settings,
        // otherwise use NTSC
        for(j=0;j<MAX_CHANNELS;j++) {
            if( pDoc->m_mode[j].format == FORMAT_PAL) {
                bPAL = TRUE;
            }
        }
        if( bPAL && !bPrevPAL) {
            // switch view positions to PAL
            memcpy( pDoc->m_pos, pDoc->m_posPAL, sizeof(pDoc->m_pos));
            Invalidate(TRUE);
        }
        else if( !bPAL && bPrevPAL) {
            // switch to NTSC
            memcpy( pDoc->m_pos, pDoc->m_posNTSC, sizeof(pDoc->m_pos));
            Invalidate( TRUE);
        } else if( bRedraw) {
            Invalidate( TRUE);
        }
    }
    return;
}

void Capp2255demoView::OnSettingsChannel(UINT nID)
{
    unsigned int idx = nID - ID_SETTINGS_CHANNEL1;
    OnNewSettings(idx + 1);
}


void Capp2255demoView::OnSettingsAllchannels()
{
    OnNewSettings(-1);
}

// start all channels at same time
void Capp2255demoView::OnAcquireStartall()
{
    Capp2255demoDoc *pDoc = GetDocument();
    BOOL bPAL=FALSE;
    int  j;
    int  fullfps = 0; // number of channels at full fps
    CRect rect;
    int idx;
    CWnd *pWnd = ::AfxGetMainWnd();
    if( pDoc == NULL) {
        return;
    }
    pWnd->GetClientRect(&rect);
    // check if trying to start all with full frame rate and color
    // if so, change frame rate to 1/2
    for( j=0; j<MAX_CHANNELS; j++) {
        if( (pDoc->m_mode[j].fdec == FDEC_1 ) && ((pDoc->m_mode[j].color & MASK_COLOR) != COLOR_Y8)  &&
            ((pDoc->m_mode[j].scale == SCALE_4CIFS) || (pDoc->m_mode[j].scale == SCALE_4CIFSI))) {
            fullfps++;
        }
    }
    
    if (fullfps >=2 ) {
        // need to 1/2 the frame rate
        for (j = 0; j < MAX_CHANNELS; j++) {
            pDoc->m_prev_fdec[j] = pDoc->m_mode[j].fdec;
            pDoc->m_fps_changed[j] =1;
            pDoc->m_mode[j].fdec = FDEC_2;
            S2255_SetMode(pDoc->m_hdev, (j+1), &pDoc->m_mode[j]);
        }
    } 
    
    // start all channels
    for (idx = 0;idx < MAX_CHANNELS; idx++) {
        if( pDoc->m_running[idx]) {
            continue;
        }
        OnAcquireStart(ID_ACQUIRE_START + idx);
    }
    
}

// stop all channels
void Capp2255demoView::OnAcquireStopall()
{
    Capp2255demoDoc *pDoc = GetDocument();
    int idx;
    if (pDoc == NULL) 
        return;
    
    for (idx = 0; idx < MAX_CHANNELS; idx++) {
        if( !pDoc->m_running[idx]) {
            continue;
        }
        OnAcquireStop(ID_ACQUIRE_STOP + idx);
    }
    return;
}

void Capp2255demoView::DrawNewImage(int idx, int frm_idx, unsigned int ts)
{
    Capp2255demoDoc *pDoc = GetDocument();
    CDC* pDC = GetDC();
    BOOL res ;
    HDC hdc = pDC->GetSafeHdc();
    
    // update image if viewing images
    if (pDoc->m_bViewImage) {
        switch (pDoc->m_mode[idx].color & MASK_COLOR) {
        case COLOR_RGB:
            res = SetDIBitsToDevice(hdc, pDoc->m_pos[idx].left, 
                pDoc->m_pos[idx].top, 
                (ULONG) pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth,
                (ULONG) pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,
                0, 
                0, 
                0, 
                (UINT) pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,
                pDoc->image[idx],
                pDoc->m_buf[idx].lpbmi[frm_idx], 
                DIB_RGB_COLORS);
            break;
        case COLOR_Y8:
            // StretchDIBits used instead of SetDIBits because for monochrome we need to flip the
            // image(vertical direction)
            res = StretchDIBits( hdc, 
                pDoc->m_pos[idx].left,  
                pDoc->m_pos[idx].top + pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight , 
                pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth,
                -pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,  //flip Y8 monochrome display
                0,
                0, 
                pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biWidth,
                pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biHeight,
                pDoc->image[idx], pDoc->m_buf[idx].lpbmi[frm_idx], 
                DIB_RGB_COLORS, 
                SRCCOPY);
            break;
        case COLOR_JPG:
            TCHAR str[100];
            _stprintf(str, _T("Jpeg size %d"), pDoc->m_buf[idx].lpbmi[frm_idx]->bmiHeader.biSizeImage);
            TextOut(hdc, pDoc->m_pos[idx].left + 25,
                pDoc->m_pos[idx].top + 50,
                str, _tcslen(str));
            _stprintf(str, _T("Note: No JPEG display in this demo"));
            TextOut(hdc, pDoc->m_pos[idx].left + 25,
                pDoc->m_pos[idx].top + 75,
                str, _tcslen(str));
            _stprintf(str, _T("Use Snapshot feature to save JPEGs"));
            TextOut(hdc, pDoc->m_pos[idx].left + 25,
                pDoc->m_pos[idx].top + 100,
                str, _tcslen(str));
            res = 1;
            break;
        default:
            OutputDebugString(_T("invalid mode\n"));
            res = 1;
        }
        if( res == 0) {
            int err = GetLastError();
            OutputDebugString(_T("failed to set DIBITS\n"));
        }
    }
    // update frame rate if displaying frame rate

    if (pDoc->m_bViewFR) {
        TCHAR frame_str[100];
        if ( pDoc->cur_frame_rate[idx] != -1) {
            _stprintf(frame_str, _T("%d fps"), pDoc->cur_frame_rate[idx]);
            pDC->TextOut(pDoc->m_pos[idx].left + 10, pDoc->m_pos[idx].top + 10, frame_str);
        }
    }
    if (pDoc->m_bRecording && idx == pDoc->m_record_channel) {
        TCHAR frame_str[100];
        COLORREF c;
        _stprintf(frame_str, _T("Recording"), pDoc->cur_frame_rate[idx]);
        c = pDC->GetTextColor();
        pDC->SetTextColor(RGB(255,0,0));
        pDC->TextOut(pDoc->m_pos[idx].left + 10, pDoc->m_pos[idx].top + 140, frame_str);
        pDC->SetTextColor(c);

    }


    if (pDoc->m_bViewTS) {
        TCHAR frame_str[100];
        _stprintf(frame_str, _T("%d ms"), ts);
        pDC->TextOut(pDoc->m_pos[idx].left + 10, pDoc->m_pos[idx].top + 40, frame_str);
    }
    ReleaseDC(pDC);
}

// all code below is not required.  used for debug only
void Capp2255demoView::OnQueryFW(void)
{
    UINT32 usb, dll, driver, dsp;
    CString str;
    int res;
    Capp2255demoDoc *pDoc;
    driver = 0;
    dll = 0;
    pDoc = (Capp2255demoDoc *) GetDocument();
    res = S2255_GetFirmware(pDoc->m_hdev, &usb, &dsp);
    if (res) {
        AfxMessageBox(_T("could not query firmware\n"));
    }
    res = S2255_GetVersions(pDoc->m_hdev, &driver, &dll);
    if (res) {
        AfxMessageBox(_T("Could not query driver and DLL version.\n"));
    }
    str.Format(_T("USB: %02d.%02d. DSP: %d.%d.%d, Driver %d.%d.%d, DLL %d.%d.%d.%d"), (usb >> 8) & 0xff,
                (usb & 0xff), dsp / 10000, (dsp % 10000) /100, (dsp % 100),
                (driver >> 16) & 0xff, (driver >> 8) & 0xff, (driver & 0xff),
                (dll >> 24) & 0xff, (dll >> 16) & 0xff, (dll >> 8) & 0xff, (dll & 0xff));
    AfxMessageBox(str);
    if (usb < 780) {
        AfxMessageBox(_T("USB version out of date.  Download USB firmware updater from Sensoray's 2255 website.\n"));
    }
    if (dsp < 10200) {
		if (dsp != 0)
			AfxMessageBox(_T("DSP firmware version out of date.  New driver was not installed.\n"));
		else
			AfxMessageBox(_T("DSP version could not be queried.\n"));
    }
    if (driver < 0x00010023) {
        AfxMessageBox(_T("Driver version out of date. New driver was not installed.\n"));
    }
    if (dll < 0x01010503) {
        AfxMessageBox(_T("DLL version not correct.  Did you install DLL correctly?\n"));
    }
    return;
}

void Capp2255demoView::OnQuerySN(void)
{
    SN2255 sn;
	int res;
	Capp2255demoDoc *pDoc;
	TCHAR str[100];

    pDoc = (Capp2255demoDoc *) GetDocument();

	res = S2255_GetSN(pDoc->m_hdev, &sn);

	if (res) {
        AfxMessageBox(_T("Could not query SN\n"));
    }

    _stprintf(str, _T("Serial Number: %d\nDate Programmed: %02d-%02d-%02d"), sn.serial_number, sn.month, sn.day, sn.year);
	AfxMessageBox(str);
    return;
}


void Capp2255demoView::OnBoard(UINT nID)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = nID - ID_BOARD_1;
    BOOL bPAL = FALSE;
	int last_board;
    CWnd *pWnd = ::AfxGetMainWnd();
    assert(pDoc != NULL);
	assert(idx < MAX_2255_DEVICES);
	last_board = pDoc->m_board;
	pDoc->m_board = idx;
    
	if (pDoc->m_board != last_board) {
		int chn;
		// this won't be called if anything is active on the board(streaming, etc...)
		S2255_DeviceClose(pDoc->m_hdev);
		if( S2255_DeviceOpen(pDoc->m_board, &pDoc->m_hdev) != 0) {
			AfxMessageBox(_T("Failed to open 2255 board!\n"));
			return;
		}
	    for( chn=1; chn<= MAX_CHANNELS; chn++) {
		    if( S2255_SetMode(pDoc->m_hdev, chn, &pDoc->m_mode[chn-1]) != 0) {
			    AfxMessageBox(_T("Failed to set mode"));
			}
		}
	}
    return;
   
}

void Capp2255demoView::OnUpdateBoard(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    unsigned int idx = pCmdUI->m_nID - ID_BOARD_1;
	int i;
	BOOL bEnable = FALSE;
	TCHAR text[100];
	assert(idx < MAX_2255_DEVICES);
	_stprintf(text, _T("Board %d\n"), idx);
	for (i = 0; i < G_num_devices; i++) {
		if (G_devices[i].boardNum == (int) idx) {
			int j;
			bEnable = TRUE;
			// don't allow board change if any stream is active on the board
			for( j = 0; j < MAX_CHANNELS; j++) {
				if( pDoc->m_running[j] ) {
					bEnable = FALSE;
					break;
				}
			}
			_stprintf(text, _T("Board %d, SN %d"), idx, G_devices[i].serialNumber);
		}
	}
	pCmdUI->SetCheck(pDoc->m_board == (int)idx);
	pCmdUI->SetText(text);
	pCmdUI->Enable(bEnable);
    
}


void Capp2255demoView::OnRecordStart()
{
    Capp2255demoDoc *pDoc = GetDocument();
    CString strFileName;
    CString strFilter("All file (*.avi) |*.avi||");
    CFileDialog FileDlg(FALSE, NULL, NULL, OFN_HIDEREADONLY ,strFilter);

    if (!pDoc->m_running[pDoc->m_record_channel]) {
        AfxMessageBox(TEXT("Please start acquisition first"));
        return;
    }
    if (FileDlg.DoModal() == IDOK) {
        CString temp;
        
        strFileName = FileDlg.GetPathName();
        ::PathRemoveExtension(strFileName.GetBuffer(NULL));
        temp = strFileName;
        pDoc->m_sRecordName = temp;
        pDoc->m_sRecordName.Format(TEXT("%s.avi"), temp.GetBuffer(NULL));
    } else {
        return;
    }
    if (!pDoc->m_bRecording) {
        if (pDoc->m_running[pDoc->m_record_channel]) {
            pDoc->StartRecordFile(pDoc->m_record_channel, pDoc->m_sRecordName);
        }
    }
}

void Capp2255demoView::OnRecordStop()
{
    Capp2255demoDoc *pDoc = GetDocument();
    CWinApp *pApp;
    pDoc->StopRecordFile();
    pApp = AfxGetApp();
    Invalidate();
    pApp->GetMainWnd()->Invalidate();

}

void Capp2255demoView::OnRecordChannel1()
{
    Capp2255demoDoc *pDoc = GetDocument();
    CWinApp *app = AfxGetApp();
    pDoc->m_record_channel = 0;
   
}

void Capp2255demoView::OnRecordChannel2()
{
    Capp2255demoDoc *pDoc = GetDocument();
    pDoc->m_record_channel = 1;
}

void Capp2255demoView::OnRecordChannel4()
{
    Capp2255demoDoc *pDoc = GetDocument();
    pDoc->m_record_channel = 3;
}

void Capp2255demoView::OnRecordChannel3()
{
    Capp2255demoDoc *pDoc = GetDocument();
    pDoc->m_record_channel = 2;
}


void Capp2255demoView::OnUpdateRecord1(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck(pDoc->m_record_channel == 0);
    if (!pDoc->m_running[0]  || pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(!pDoc->m_bRecording);
}

void Capp2255demoView::OnUpdateRecord2(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck(pDoc->m_record_channel == 1);
    if (!pDoc->m_running[1] || pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(!pDoc->m_bRecording);
}
void Capp2255demoView::OnUpdateRecord3(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck(pDoc->m_record_channel == 2);
    if (!pDoc->m_running[2] || pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(!pDoc->m_bRecording);
}
void Capp2255demoView::OnUpdateRecord4(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if( pDoc == NULL) {
        return;
    }
    pCmdUI->SetCheck(pDoc->m_record_channel == 3);
    if (!pDoc->m_running[3] || pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(!pDoc->m_bRecording);
}


void Capp2255demoView::OnUpdateRecordStart(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    pCmdUI->SetCheck(pDoc->m_bRecording);
    if (pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(!pDoc->m_bRecording);
}

void Capp2255demoView::OnUpdateRecordStop(CCmdUI *pCmdUI)
{
    Capp2255demoDoc *pDoc = GetDocument();
    if (pDoc->m_board) {
        pCmdUI->Enable(0);
        return;
    }
    pCmdUI->Enable(pDoc->m_bRecording);
}

void Capp2255demoView::OnRecordHelp()
{
    Capp2255demoDoc *pDoc = GetDocument();
    if (pDoc->m_board) {
        AfxMessageBox(TEXT("This demo allows record for board 0 only"));

    } else {
        AfxMessageBox(TEXT("This demo only allows recording one channel at a time.  Please note that this is not a limitation of the board."));
        if ((pDoc->m_mode[pDoc->m_record_channel].color & MASK_COLOR) == COLOR_Y8) {
            AfxMessageBox(TEXT("Use VLC to play back Y8 grayscale AVIs.  WMP is not supported."));
        }

    }

}
