// InputType.cpp : implementation file
// Copyright Sensoray Company 2007-2010

#include "stdafx.h"
#include "app-2255-demo.h"
#include "InputType.h"
#include "s2255f.h"

// CInputType dialog
IMPLEMENT_DYNAMIC(CInputType, CPropertyPage)
CInputType::CInputType()
	: CPropertyPage(CInputType::IDD)
{
    m_bStreaming = FALSE;
    m_index = 0;
	m_channel = 0;
	pDoc = NULL;
	memset(&mode, 0, sizeof(mode));
}

CInputType::~CInputType()
{
}

void CInputType::DoDataExchange(CDataExchange* pDX)
{
	CPropertyPage::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_RADIO_COMPOSITE, m_rad1);
    DDX_Control(pDX, IDC_RADIO_SVIDEO, m_rad2);
    DDX_Radio(pDX, IDC_RADIO_COMPOSITE, m_index);
}


BEGIN_MESSAGE_MAP(CInputType, CPropertyPage)
    ON_BN_CLICKED(IDC_RADIO_COMPOSITE, OnBnClickedRadioComposite)
    ON_BN_CLICKED(IDC_RADIO_SVIDEO, OnBnClickedRadioSvideo)
END_MESSAGE_MAP()


// CInputType message handlers
BOOL CInputType::OnInitDialog()
{
	CPropertyPage::OnInitDialog();

    if( m_bStreaming)
    {
        // disable the controls if currently streaming
        //m_rad2.EnableWindow(FALSE);
        //m_rad1.EnableWindow(FALSE);
    }

	return TRUE;  // return TRUE unless you set the focus to a control
	// EXCEPTION: OCX ProperTy Pages should return FALSE
}

void CInputType::OnBnClickedRadioComposite()
{
    //SetModified( TRUE);
}

void CInputType::OnBnClickedRadioSvideo()
{
    //SetModified( TRUE);
}


BOOL CInputType::OnApply()
{
    UpdateData(TRUE);
    if( pDoc == NULL)
        return FALSE;

    mode.color &= ~MASK_INPUT_TYPE;
	if (m_index)
		mode.color |= (1 << 16);
    S2255_SetMode( pDoc->m_hdev, m_channel, &mode);
    return TRUE;
}