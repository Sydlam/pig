#pragma once

#include "s2255.h"
#include "app-2255-demodoc.h"

// CInputType dialog

class CInputType : public CPropertyPage
{
	DECLARE_DYNAMIC(CInputType)

public:
	CInputType();
	virtual ~CInputType();
    BOOL m_bStreaming;
    int  m_index;
	MODE2255 mode;
    BOOL OnInitDialog();
	BOOL OnApply();
	Capp2255demoDoc *pDoc ;
	int m_channel;
    // Dialog Data
	enum { IDD = IDD_PROPPAGE_INPUTTYPE };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
    CButton m_rad1;
    CButton m_rad2;
	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnBnClickedRadioComposite();
    afx_msg void OnBnClickedRadioSvideo();


};
