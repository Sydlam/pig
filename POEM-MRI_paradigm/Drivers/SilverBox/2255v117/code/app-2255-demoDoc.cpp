// app-2255-demoDoc.cpp : implementation of the Capp2255demoDoc class
// Copyright 2007-2009 (C)  Sensoray Corporation Inc.

#include "stdafx.h"
#include "app-2255-demoDoc.h"
#include "s2255f.h"
#include ".\app-2255-demodoc.h"
#include "resource.h"
#include "image.h"

DEVINFO2255 G_devices[MAX_2255_DEVICES];
int G_num_devices;
// Capp2255demoDoc
IMPLEMENT_DYNCREATE(Capp2255demoDoc, CDocument)  

BEGIN_MESSAGE_MAP(Capp2255demoDoc, CDocument)
ON_COMMAND(ID_SNAPSHOTS_CHANNEL1, OnSnapshotsChannel1)
ON_COMMAND(ID_SNAPSHOTS_CHANNEL2, OnSnapshotsChannel2)
ON_COMMAND(ID_SNAPSHOTS_CHANNEL3, OnSnapshotsChannel3)
ON_COMMAND(ID_SNAPSHOTS_CHANNEL4, OnSnapshotsChannel4)
ON_COMMAND(ID_TOOLS_VIDEOSTATUS, OnToolsVideostatus)
END_MESSAGE_MAP()


// Capp2255demoDoc construction/destruction
Capp2255demoDoc::Capp2255demoDoc()
{
    int i;
    // Window positions
    RECT pos1[MAX_CHANNELS] = { {0, 0, NTSC_W, NTSC_H},   
                                {NTSC_W+WINDOW_X, 0, NTSC_W*2+WINDOW_X, NTSC_H}, 
                                {0, NTSC_H+WINDOW_Y, NTSC_W, NTSC_H*2 + WINDOW_Y},
                                {NTSC_W+WINDOW_X,NTSC_H+WINDOW_Y,NTSC_W*2+WINDOW_X,NTSC_H*2 + WINDOW_Y}};
    
    RECT pos2[MAX_CHANNELS] = { {0,0,PAL_W,PAL_H},   
                                {PAL_W+WINDOW_X,0, PAL_W*2+WINDOW_X, PAL_H}, 
                                {0, PAL_H+WINDOW_Y, PAL_W, PAL_H*2 + WINDOW_Y},
                                {PAL_W+WINDOW_X, PAL_H+WINDOW_Y,PAL_W*2+ WINDOW_X, PAL_H*2 + WINDOW_Y}};
    
    MODE2255 mode_sing = { DEF_MODE_NTSC_SING };
    
    memcpy( m_posNTSC, pos1,sizeof(pos1));
    memcpy( m_posPAL,pos2,sizeof(pos2));
    memcpy( m_pos, m_posNTSC, sizeof( m_pos));
    m_hdev = NULL;
    m_numbuf = NUM_FRAMES;
    for (i = 0; i < MAX_CHANNELS; i++) {
        m_stop_event[i] = NULL;
        m_ack_thread[i] = NULL;
        m_buf_event[i] = NULL;
        m_stop_event[i] = NULL; // stop event for channel
        m_running[i] = FALSE;
        image[i] = NULL;
        cur_frame_rate[i] = -1;
        memset( &m_buf[i], 0, sizeof(m_buf[i]));
        m_recvd_buf[i] = 0;
        m_mode[i] = mode_sing;
        m_bTriggerSnapshot[i] = FALSE;
        m_fps_changed[i] = 0;
        memset(&m_osd[i], 0, sizeof(s2255_osd));
        strcpy(m_osd[i].line, "Time: ^t^nDate: ^d");
        m_osd[i].fraction = 0;
        m_osd[i].osdChan = i;
        m_osd[i].positionTop = 1;
        m_osd[i].year2 = 1;
        m_osd[i].xOffset = 10;
        m_osd[i].yOffset = 50;
    }   
    m_bViewImage = TRUE;
    m_bViewFR = TRUE;
    m_bViewTS = FALSE;
    m_framecount = 0;
    m_bRecording = FALSE;
    m_record_channel = 0;
}

Capp2255demoDoc::~Capp2255demoDoc()
{
    m_hdev = NULL;
}

// On New Document.
// First call to the API
#define FILE_SAVE_VERSION 0x00000002L
BOOL Capp2255demoDoc::OnNewDocument()
{
    MODE2255 mode_cont = { DEF_MODE_NTSC_CONT};
    int chn;
    if (!CDocument::OnNewDocument()) {
        return FALSE;
    }
    
	// set count to 0 and look for number of boards
    S2255_Enumerate(&G_num_devices, NULL);
	if (G_num_devices == 0) {
		AfxMessageBox(_T("No 2255's found\n"));
		return -4;
	}
	if (G_num_devices > MAX_2255_DEVICES)
		G_num_devices = MAX_2255_DEVICES; // only support 8 boards max in this application.
	S2255_Enumerate(&G_num_devices, G_devices);
    //Open the first device (boardNum may not be 0 if two boards plugged in initially and 
	// the original "first" board 0 removed.)
	m_board = G_devices[0].boardNum;
    if( S2255_DeviceOpen(G_devices[0].boardNum, &m_hdev) != 0) {
        AfxMessageBox(_T("Failed to open 2255 device!\n"));
        return -4;
    }
    
    //----------------------------------------------------------------
    // Set up acquisition modes
    m_mode[0] = mode_cont;
    // make default display mode RGB
    m_mode[0].color &= ~MASK_COLOR;
    m_mode[0].color |= (COLOR_RGB & MASK_COLOR);

    m_mode[0].scale = SCALE_1CIFS;  
    // set all channels to same mode as channel 0 
    for( chn=1; chn<= MAX_CHANNELS; chn++) {
        m_mode[chn-1] = m_mode[0]; 
    }

    DoSettings(TRUE);

    for( chn=1; chn<= MAX_CHANNELS; chn++) {
        if( S2255_SetMode( m_hdev, chn, &m_mode[chn-1]) != 0) {
            AfxMessageBox(_T("Failed to set mode"));
        }
        S2255_SetOsd(m_hdev, &m_osd[chn-1]);
    }
    
    return TRUE;
}

void Capp2255demoDoc::OnCloseDocument()
{
    int i;
    // close all streams
    for( i=0;i<MAX_CHANNELS;i++) {
        if( m_stop_event[i]) {
            SetEvent( m_stop_event[i]);
            // wait for acquisition thread to stop
            WaitForSingleObject( m_ack_thread[i], INFINITE);
        }
    }
    if( S2255_DeviceClose(m_hdev) != 0) {
        AfxMessageBox(_T("Failed to close device"));
    }
    m_hdev = NULL;
    DoSettings(FALSE);
    CDocument::OnCloseDocument();
}


// Capp2255demoDoc serialization
void Capp2255demoDoc::Serialize(CArchive& ar)
{
    if (ar.IsStoring()) {
    } else {
    }
}


// Capp2255demoDoc diagnostics
#ifdef _DEBUG
void Capp2255demoDoc::AssertValid() const
{
    CDocument::AssertValid();
}

void Capp2255demoDoc::Dump(CDumpContext& dc) const
{
    CDocument::Dump(dc);
}
#endif //_DEBUG



// Capp2255demoDoc commands
void Capp2255demoDoc::DocSnapshotCommon(int idx)
{
    CString strFileName;
    CString strFilter;
    BOOL bJPEG = ((m_mode[idx].color & MASK_COLOR)== COLOR_JPG) ? TRUE : FALSE;
    if (bJPEG) {
        strFilter = "All files (*.jpg) |*.jpg||";
    } else {
        strFilter = _T("All files (*.bmp) |*.bmp||");
    }
    CFileDialog FileDlg(FALSE, NULL, NULL, OFN_HIDEREADONLY ,strFilter);
    
    if( m_running[idx] ) {
        if( m_bTriggerSnapshot[idx] ) {
            AfxMessageBox(_T("Snapshot already triggered."));
            return;
        }
        // get the filename
        if (FileDlg.DoModal() == IDOK)
        {
            CString name = FileDlg.GetPathName();
            if (bJPEG) {
                if( name.Find(_T(".jpg"))== -1) {
                    strFileName = name + CString(_T(".jpg"));
                } else {
                    strFileName = name;
                }
            } else {
                if( name.Find(_T(".bmp"))== -1) {
                    strFileName = name + CString(_T(".bmp"));
                } else {
                    strFileName = name;
                }
            }
            
        } else return;
        m_strSnapshot[idx] = strFileName;
        m_bTriggerSnapshot[idx] = TRUE;
    } else {
        // get the filename
        if (FileDlg.DoModal() == IDOK)
        {
            CString name = FileDlg.GetPathName();
            if (bJPEG) {
                if( name.Find(_T(".jpg")) == -1) {
                    strFileName = name + CString(_T(".jpg"));
                } else {
                    strFileName = name;
                }
            } else {
                if( name.Find(_T(".bmp")) == -1) {
                    strFileName = name + CString(_T(".bmp"));
                } else {
                    strFileName = name;
                }
            }
            
        } else return;
        SingleSnapshot( strFileName, idx);
    }
    
}
void Capp2255demoDoc::OnSnapshotsChannel1()
{
    DocSnapshotCommon(0);
}

void Capp2255demoDoc::OnSnapshotsChannel2()
{
    DocSnapshotCommon(1);
}

void Capp2255demoDoc::OnSnapshotsChannel3()
{
    DocSnapshotCommon(2);
}

void Capp2255demoDoc::OnSnapshotsChannel4()
{
    DocSnapshotCommon(3);
}

// single snapshot capture
// SN_GetFrame should only be used for very occasional snapshots. For example
// once or twice a second max.  For higher frame rates, please use SN_StartAcquire.
int Capp2255demoDoc::SingleSnapshot(CString fname, int idx)
{
    int res;
    int size;
    BITMAPINFO bmi;
    unsigned char *pdata;
    // save current mode( single snapshot for demo purpose only)
    if( m_running[idx]) {
        return -1;
    }
    size = S2255_GetImageSize( &m_mode[idx]);
    pdata = (unsigned char *) malloc(size);
    
    // grab the frame 1000 ms timeout
    res = S2255_GrabFrame( m_hdev, idx+1, (unsigned char *)pdata, size, 1000, &bmi);
    if( res != 0) {
        // free the buffers
        free( pdata );
        AfxMessageBox(_T("snapshot timed out"));
        return res;
    }
    // successfully got frame
    switch (m_mode[idx].color & MASK_COLOR) {
    case COLOR_RGB:
        save_image_uncompressed((const unsigned char *) pdata, 
            fname.GetBuffer(MAX_PATH),
            bmi.bmiHeader.biHeight,
            bmi.bmiHeader.biWidth,
            bmi.bmiHeader.biWidth*3,
            0);
        break;
    case COLOR_Y8:
        save_image_uncompressed_mono((const unsigned char *) pdata, 
            fname.GetBuffer(MAX_PATH),
            bmi.bmiHeader.biHeight,
            bmi.bmiHeader.biWidth);
        break;
    case COLOR_JPG:
        {
            FILE *fout = _tfopen(fname.GetBuffer(MAX_PATH), _T("wb+"));
            if (fout != NULL) {
                fwrite(pdata, 1, bmi.bmiHeader.biSizeImage, fout);
                fclose(fout);
            } else {
                OutputDebugString(_T("could not open file!\n"));
            }
        }
        break;
    }
    // free buffer
    free(pdata);
    AfxMessageBox(_T("saved snapshot"));
    return 0;
}


void Capp2255demoDoc::OnToolsVideostatus()
{
    UINT32 status[MAX_CHANNELS];
    int i;
    int hr;
    TCHAR statstring[4][50];
    TCHAR fullstring[200];
    for (i = 0; i < MAX_CHANNELS; i++) {
        hr = S2255_GetVidStatus(m_hdev, i + 1, &status[i]);
        if (hr != 0) {
            AfxMessageBox(_T("Failed to get video status"));
            return;
        }
        if (status[i] & 1) {
            _stprintf(statstring[i], _T("Channel %d: Video present %s\n"), i + 1,
                status[i] & 0x0100 ? _T("50Hz") : _T("60Hz"));
        } else {
            _stprintf(statstring[i], _T("Channel %d: No signal detected\n"), i + 1);
        }
    }
    _stprintf(fullstring, _T("%s %s %s %s\n"), statstring[0], statstring[1], statstring[2], statstring[3]);
    AfxMessageBox(fullstring);
}

void Capp2255demoDoc::StartRecordFile(int channel, CString path)
{
	AVISTREAMINFO strhdr;
	BITMAPINFOHEADER bi;
    RECT r;
    int hr;
    int nframes = 0;
    int w, h;
    BOOL bPAL;
    bPAL = (m_mode[channel].format == FORMAT_PAL);
    switch (m_mode[channel].scale & 0x0f) {
        case SCALE_4CIFSI:
        case SCALE_4CIFS:
            w = bPAL ? 704 : 640;
            h = bPAL ? 576 : 480;
            break;
        case SCALE_1CIFS:
        case SCALE_1CIFSF:
            w = bPAL ? 352 : 320;
            h = bPAL ? 288 : 240;
            break;
        case SCALE_2CIFS:
            w = bPAL ? 704 : 640;
            h = bPAL ? 288 : 240;
            break;
    }
    m_record_channel = channel;
    //w = m_mode[channel].mode;
	AVIFileInit();
	//hr = AVIFileOpen(&pfile, path, OF_WRITE | OF_CREATE, NULL);
    hr = AVIFileOpen(&pfile, path, OF_WRITE | OF_CREATE, NULL);
    if (hr != 0) {
        AfxMessageBox(TEXT("Failed to open file"));
        return;
    }
	ZeroMemory(&strhdr, sizeof(strhdr));
	strhdr.fccType = streamtypeVIDEO;
	strhdr.fccHandler = 0;
	strhdr.dwScale = 1000;
    strhdr.dwRate = bPAL ? 25000 : 29970;
    switch (m_mode[channel].scale & 0x0f) {
        case SCALE_1CIFSF:
            strhdr.dwRate *= 2;
            break;
        default:
            break;
    }
	r.left = 0;
	r.top = 0;
	r.bottom = h;
	r.right = w;
	strhdr.rcFrame = r;
	ZeroMemory(&bi, sizeof(bi));
	bi.biWidth = w;
	bi.biHeight = h;
    switch (m_mode[channel].color & MASK_COLOR) {
    case COLOR_RGB:
        bi.biCompression = BI_RGB;
        bi.biBitCount = 24;
        break;
    case COLOR_Y8:
        bi.biCompression = 0x30303859;//'008Y';
        bi.biBitCount = 8;
        break;
    case COLOR_JPG:
        bi.biCompression = 'GPJM';
        bi.biBitCount = 16;
        break;
    }
	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biPlanes = 1;
	hr = AVIFileCreateStream(pfile, &pavi, &strhdr);
    if (hr != 0) {
        AfxMessageBox(TEXT("Failed to create AVI stream"));
        return;
    }
	hr = AVIStreamSetFormat(pavi, 0, &bi, sizeof(bi));
    if (hr != 0) {
        AfxMessageBox(TEXT("Failed to set AVI format"));
        return;
    }
    m_bRecording = TRUE;
    recframes = 0;
    return;
}


void Capp2255demoDoc::StopRecordFile()
{
    if (pavi)
		AVIStreamRelease(pavi);
    pavi = NULL;
    if (pfile)
	    AVIFileRelease(pfile);
    pfile = NULL;
	AVIFileExit();
    m_bRecording = FALSE;
}


void Capp2255demoDoc::DoSettings(BOOL bLoad)
{
    int fileVer;
    CFile *file;
    BOOL res;
    int j;
    file = new CFile();
    if (bLoad) {
        res = file->Open("settings.bin", CFile::modeRead, NULL);
        if (!res)
            return;
    } else {
        res = file->Open("settings.bin", CFile::modeWrite | CFile::modeCreate, NULL);
        if (!res)
            return;
    }
    CArchive ar(file, bLoad ? CArchive::load : CArchive::store);

    if (ar.IsStoring()) {
        ar << FILE_SAVE_VERSION;
        for (j = 0; j < MAX_CHANNELS; j++) {
            ar.Write(&m_mode[j], sizeof(MODE2255));
        }
        for (j = 0; j < MAX_CHANNELS; j++) {
            ar.Write(&m_osd[j], sizeof(s2255_osd));
        }
        ar << m_bViewFR;
        ar << m_bViewTS;
    } else {
        ar >> fileVer;
        if (fileVer != FILE_SAVE_VERSION) {
            OutputDebugString("invalid file version");
            ar.Close();
            file->Close();
            return;
        }
        for (j = 0; j < MAX_CHANNELS; j++) {
            ar.Read(&m_mode[j], sizeof(MODE2255));
        }
        for (j = 0; j < MAX_CHANNELS; j++) {
            ar.Read(&m_osd[j], sizeof(s2255_osd));
        }
        ar >> m_bViewFR;
        ar >> m_bViewTS;

    }
    ar.Close();
    file->Close();
}

