// Copyright Sensoray Company 2007-2009
// app-2255-demoView.h : interface of the Capp2255demoView class
//

#pragma once

class Capp2255demoView : public CView
{
protected: // create from serialization only
	Capp2255demoView();
	DECLARE_DYNCREATE(Capp2255demoView)
// Attributes
public:
	Capp2255demoDoc* GetDocument() const;

// Operations
public:
    void    OnNewSettings( int chn ); 
    void    CreateAcquisitionThread( int channel);
// Overrides
	public:
protected:
    virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
// Implementation
public:
	virtual ~Capp2255demoView();
protected:

// Generated message map functions
protected:
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnQueryFW();
	afx_msg void OnQuerySN();
	afx_msg void OnBoard(UINT nID);
    afx_msg void OnAcquireStart(UINT nID);
    afx_msg void OnAcquireStop(UINT nID);
    afx_msg void OnUpdateRecordStart(CCmdUI *pCmdUI);
    afx_msg void OnUpdateRecordStop(CCmdUI *pCmdUI);
    afx_msg void OnUpdateAcquireStart(CCmdUI *pCmdUI);
    afx_msg void OnUpdateAcquireStop(CCmdUI *pCmdUI);
	afx_msg void OnUpdateBoard(CCmdUI *pCmdUI);
    afx_msg BOOL OnEraseBkgnd(CDC* pDC);
    afx_msg void OnViewFramerate();
    afx_msg void OnUpdateViewFramerate(CCmdUI *pCmdUI);
    afx_msg void OnViewTS();
    afx_msg void OnUpdateViewTS(CCmdUI *pCmdUI);
    afx_msg void OnUpdateViewDisplayimage(CCmdUI *pCmdUI);
    afx_msg void OnViewDisplayimage();
    virtual void OnInitialUpdate();
    afx_msg void OnSettingsChannel(UINT nID);
    afx_msg void OnSettingsAllchannels();
    afx_msg void OnAcquireStartall();
    afx_msg void OnAcquireStopall();
    void DrawNewImage(int idx, int frm_index, unsigned int ts);
    afx_msg void OnRecordStart();
    afx_msg void OnRecordStop();
    afx_msg void OnRecordChannel1();
    afx_msg void OnRecordChannel2();
    afx_msg void OnRecordChannel3();
    afx_msg void OnRecordChannel4();
    afx_msg void OnUpdateRecord1(CCmdUI *pCmdUI);
    afx_msg void OnUpdateRecord2(CCmdUI *pCmdUI);
    afx_msg void OnUpdateRecord3(CCmdUI *pCmdUI);
    afx_msg void OnUpdateRecord4(CCmdUI *pCmdUI);
    afx_msg void OnRecordHelp();
};

inline Capp2255demoDoc* Capp2255demoView::GetDocument() const
{
    return reinterpret_cast<Capp2255demoDoc*>(m_pDocument); 
}

