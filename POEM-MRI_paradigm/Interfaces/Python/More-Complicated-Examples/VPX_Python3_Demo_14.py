# ViewPoint EyeTracker (R) interface to Python 3 (VPX_Python3_Demo.py)
#       Verify the sections below marked:       # <<<< CHANGE AS NEEDED <<<< 
#       Paths must use either (a) Forward Slashes, or (b) Double Back Slashes !!!
#       To use Python 2 change: print("x") --to--> print "x"
#       25-Feb-2014 : kfa : added getGazePoint, getGazePoint2, EYE_B, and formated print
#       07-Dec-2010 : kfa : changed to Python3 and added vpxDll access check.
#
#       To run this, either put this file in the Python root directory, or do:
#               import sys                      # to set where to look for modules
#               sys.path.append("C:/ARI/VP")    # <<<< CHANGE AS NEEDED
#               import VPX_Python3_Demo         # <<<< CHANGE AS NEEDED, without .py
#
#       This demo prints a line whenever an ROI is newly entered or exited.
#       Nothing is printed while the the gaze point remains inside an ROI.
#       Example:        [3,19] means the gaze point just entered ROI#3 and ROI#19,
#                       [-3] means the gazepoint has just exited ROI#3
#
from ctypes import *
import os
#
#  Load the ViewPoint library
#  REMEMBER: Paths must use either (a) Forward Slashes, or (b) Double Back Slashes !!!
#vpxDll = "C:/ARI/VP/VPX_InterApp.dll"  # <<<< CHANGE AS NEEDED <<<< 
vpxDll = "C:/MsDev/Projects/VP/VPX_InterApp.dll"
if ( not os.access(vpxDll,os.F_OK) ):
        print("WARNING: Invalid vpxDll path; you need to edit the .py file")
cdll.LoadLibrary( vpxDll )
vpx = CDLL( vpxDll )
#
#  ViewPoint CONSTANTS (see vpx.h for a full listing of constants)
VPX_STATUS_ViewPointIsRunning = 1
EYE_A = 0
EYE_B = 1
VPX_DAT_FRESH = 2
ROI_NO_EVENT = -9999
#
vpx.VPX_SendCommand( str('dataFile_newUnique; say "using str" ') )
vpx.VPX_SendCommand('say "Hello from Python" ')
# If everyting is okay, the above message will print in the ViewPoint History window.
if ( vpx.VPX_GetStatus(VPX_STATUS_ViewPointIsRunning) < 1 ):
        print("ViewPoint is not running")
#
#  Create needed structures and callback function
class RealPoint(Structure):
        _fields_ = [("x",c_float),("y",c_float)]
#  Create function prototypes
funcRealPoint = CFUNCTYPE( c_int, POINTER(RealPoint) )
getGazePoint = funcRealPoint(vpx.VPX_GetGazePoint)
#
funcRealPoint2 = CFUNCTYPE( c_int, c_int, POINTER(RealPoint) )
getGazePoint2 = funcRealPoint2(vpx.VPX_GetGazePoint2)
#
VPX_CALLBACK = CFUNCTYPE( c_int, c_int, c_int, c_int, c_int )
        #       The first param is the return value, the last four are function parameters: msg,subMsg,p1,p2
def ViewPointMessageCallback( msg, subMsg, p1, p2, ):
        if ( msg == VPX_DAT_FRESH ):
                roiListA = []                   # Need to declare and clear the list
                gpA = RealPoint(1.1,1.1)        # Need to declare a RealPoint variable
                gpB = RealPoint(1.1,1.1)
                for ix in range(5):
                        roiNumberA = vpx.VPX_ROI_GetEventListItem( EYE_A, ix )
                        if ( ROI_NO_EVENT == roiNumberA ):
                                break
                        else:
                                getGazePoint( gpA )
                                getGazePoint2( EYE_B, gpB )
                                roiListA.append( roiNumberA )
                if (len(roiListA)>0):
                        print(roiListA,'A[{0:5.3f},{1:5.3f}]; B[{0:5.3f},{1:5.3f}]'.format(gpA.x,gpA.y,gpB.x,gpB.y) ) 
        return 0
#
#  Register the Python callback function with the ViewPoint DLL
vpxCallback = VPX_CALLBACK(ViewPointMessageCallback)
vpx.VPX_InsertCallback(vpxCallback)

