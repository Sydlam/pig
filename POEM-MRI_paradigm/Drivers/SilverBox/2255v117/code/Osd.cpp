// Osd.cpp : implementation file
//

#include "stdafx.h"
#include <assert.h>
#include "app-2255-demo.h"
#include "Osd.h"
#include "s2255f.h"


// COsd dialog

IMPLEMENT_DYNAMIC(COsd, CPropertyPage)

COsd::COsd()
	: CPropertyPage(COsd::IDD)
    , m_bOsdOn(FALSE)
    , m_iOsdX(0)
    , m_iOsdY(0)
    , m_bLargeFont(FALSE)
    , m_sOsdText(_T("OSD Test"))
    , m_iTransparency(0)
    , m_iX(0)
    , m_iY(0)
{

}

COsd::~COsd()
{
}

void COsd::DoDataExchange(CDataExchange* pDX)
{
    CPropertyPage::DoDataExchange(pDX);
    DDX_Check(pDX, IDC_CHECK_OSDON, m_bOsdOn);
    DDX_Slider(pDX, IDC_SLIDER_OSD_X, m_iOsdX);
    DDV_MinMaxInt(pDX, m_iOsdX, 0, 640);
    DDX_Slider(pDX, IDC_SLIDER_OSD_Y, m_iOsdY);
    DDV_MinMaxInt(pDX, m_iOsdY, 0, 480);
    DDX_Check(pDX, IDC_CHECK_LARGEFONT, m_bLargeFont);
    DDX_Text(pDX, IDC_EDIT_OSDTEXT, m_sOsdText);
    DDX_Control(pDX, IDC_RADIO_ZERO, m_radZero);
    DDX_Radio(pDX, IDC_RADIO_ZERO, m_iTransparency);
    DDX_Text(pDX, IDC_STATIC_XVAL, m_iX);
    DDX_Text(pDX, IDC_STATIC_YVAL, m_iY);
    DDX_Control(pDX, IDC_SLIDER_OSD_X, m_sldX);
	DDX_Control(pDX, IDC_BUTTON_HELPTEXT, m_btnHelp);
    DDX_Control(pDX, IDC_SLIDER_OSD_Y, m_sldY);

}


BEGIN_MESSAGE_MAP(COsd, CPropertyPage)
    ON_BN_CLICKED(IDC_CHECK_OSDON, OnBnClickedCheckOsdon)
    ON_WM_HSCROLL()
    ON_EN_CHANGE(IDC_EDIT_OSDTEXT, OnEnChangeEditOsdtext)
    ON_BN_CLICKED(IDC_CHECK_LARGEFONT, OnBnClickedCheckLargefont)
    ON_BN_CLICKED(IDC_RADIO_ZERO, OnBnClickedRadioZero)
    ON_BN_CLICKED(IDC_RADIO_25, OnBnClickedRadio25)
    ON_BN_CLICKED(IDC_RADIO_50, OnBnClickedRadio50)
    ON_BN_CLICKED(IDC_RADIO_100, OnBnClickedRadio100)
	ON_BN_CLICKED(IDC_BUTTON_HELPTEXT, OnBnClickedHelp)
END_MESSAGE_MAP()


// COsd message handlers

void COsd::UpdateOsd()
{
    UpdateData(TRUE);
    osd.osdOn = this->m_bOsdOn ? (m_bLargeFont ? 2 : 1) : 0;
    osd.osdChan = m_channel - 1;
    osd.positionTop = 1;
    switch (m_iTransparency) {
        case 0: //0 %
            osd.transparent = 0;
            break;
        case 1:// 25%
            osd.transparent = 3;
            break;
        case 2:// 50%
            osd.transparent = 2;
            break;
        case 3://100%
            osd.transparent = 1;
            break;
    }
    osd.xOffset = m_iOsdX;
    osd.yOffset = m_iOsdY;
    
    strcpy(osd.line, m_sOsdText.GetBuffer(NULL));
    S2255_SetOsd(pDoc->m_hdev, &osd);
}


void COsd::OnBnClickedCheckOsdon()
{
    UpdateOsd();
}

BOOL COsd::OnInitDialog() 
{
    BOOL bRes;
    bRes = CPropertyPage::OnInitDialog();
    m_sldX.SetRange(0, 640, TRUE);
    m_sldY.SetRange(0, 480, TRUE);
    m_sOsdText = osd.line;
    m_iOsdX = osd.xOffset;
    m_iX = m_iOsdX;
    m_iOsdY = osd.yOffset;
    m_iY = m_iOsdY;
    m_bOsdOn = osd.osdOn;
    switch (osd.transparent) {
        case 0:
        case 2:
            m_iTransparency = osd.transparent;
            break;
        case 1:
            m_iTransparency = 3;
            break;
        case 3:
            m_iTransparency = 1;
            break;
    }
    m_bLargeFont = (osd.osdOn == 2);
    assert((m_channel - 1) == osd.osdChan);
	m_btnHelp.SetIcon(::LoadIcon(NULL, IDI_QUESTION));
    UpdateData(FALSE);

    return bRes;

}

void COsd::OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar)
{
	if( pScrollBar)
	{
        BOOL bmoved = FALSE;
        switch( nSBCode )
        {
        case SB_LEFT:
            bmoved = TRUE;
            break;
        case SB_RIGHT:
            bmoved = TRUE;
            break;
        case SB_LINELEFT:
            bmoved = TRUE;
            break;
        case SB_LINERIGHT:
            bmoved = TRUE;
            break;
        case SB_PAGELEFT:
            bmoved = TRUE;
            break;
        case SB_PAGERIGHT:
            bmoved = TRUE;
            break;
        case SB_THUMBPOSITION:
            break;
        case SB_THUMBTRACK:
            bmoved = TRUE;
            break;
        case SB_ENDSCROLL:
            break;
        default:
            break;
        }
        if( bmoved) {
            
        }
    }
    CPropertyPage::OnHScroll(nSBCode, nPos, pScrollBar);
    UpdateOsd();
    m_iX = m_iOsdX;
    m_iY = m_iOsdY;
    UpdateData(FALSE);
}

void COsd::OnEnChangeEditOsdtext()
{
    UpdateOsd();
}

void COsd::OnBnClickedCheckLargefont()
{
    UpdateOsd();   
}

void COsd::OnBnClickedRadioZero()
{
    UpdateOsd();
}

void COsd::OnBnClickedRadio25()
{
    UpdateOsd();
}

void COsd::OnBnClickedRadio50()
{
    UpdateOsd();
}

void COsd::OnBnClickedRadio100()
{
    UpdateOsd();
}

void COsd::OnBnClickedHelp()
{
	::MessageBox(m_hWnd, TEXT("Use ^t for time, ^d for date, ^n for new line"), 
		TEXT("OSD Help"), MB_OK);
}
