#pragma once
#include "afxwin.h"
#include "s2255.h"
#include "app-2255-demoDoc.h"

// COsd dialog

class COsd : public CPropertyPage
{
	DECLARE_DYNAMIC(COsd)

public:
	COsd();
	virtual ~COsd();

// Dialog Data
	enum { IDD = IDD_OSD };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
    void UpdateOsd();
	DECLARE_MESSAGE_MAP()
public:
    Capp2255demoDoc  *pDoc;
    
    int m_channel;
    BOOL m_bOsdOn;
    int m_iOsdX;
    int m_iOsdY;
    BOOL m_bLargeFont;
    CString m_sOsdText;
    CButton m_radZero;
    CButton m_btnHelp;
	CSliderCtrl m_sldX;
    CSliderCtrl m_sldY;

    int m_iTransparency;
    s2255_osd osd;
    afx_msg void OnBnClickedCheckOsdon();
    afx_msg void OnEnChangeEditOsdtext();
    afx_msg void OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);
    int m_iX;
    int m_iY;
    afx_msg void OnBnClickedCheckLargefont();
    afx_msg void OnBnClickedRadioZero();
    afx_msg void OnBnClickedRadio25();
    afx_msg void OnBnClickedRadio50();
    afx_msg void OnBnClickedRadio100();
	afx_msg void OnBnClickedHelp();
    BOOL OnInitDialog();
};
