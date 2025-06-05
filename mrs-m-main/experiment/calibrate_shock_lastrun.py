#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on February 16, 2024, at 13:30
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from init_shock
from psychopy.parallel import ParallelPort
from subprocess import Popen
import time

dlg = gui.Dlg(title='set up calibration')
dlg.addField('room', choices =['VR', 'behavior']) #added 6/14
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel

BIO = True if user_input[1] == 'yes' and user_input[0] == 'VR' else False #added 6/14
BIO2 = True if user_input[1] == 'yes' and user_input[0] == 'behavior' else False #added 6/14

if BIO:
    pport = ParallelPort(address='0xEFF8') #added 6/14
elif BIO2:
    pport = ParallelPort(address='0x3FB8') #added 6/14

else:
    class PortEmulator(object):
        def __init__(self, address=None):
            pass
        def setData(self, data=None):
            logging.warn("Sent data to non-existent PPort:{}".format(data))
        def setPin(self, pin, data):
            logging.warn(f"Sent data to non-existent PPort pin: {pin}, {data}")
    pport = PortEmulator()

pport.setData(0) #reset the pins

def shock():
    pport.setPin(2,1)
    time.sleep(.005)
    pport.setPin(2,0)

def stim_marker(on_or_offset='',SHOCK=False):
    if SHOCK:
        shock()
    if 'on' in on_or_offset:
        pport.setPin(4,1)
    elif 'off' in on_or_offset:
        pport.setPin(4,0)


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'instructions_setup'  # from the Builder filename that created this script
expInfo = {
    '': '',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/shock_calibration/shock_calibration'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\mrs-m\\experiment\\calibrate_shock_lastrun.py',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=(-0.1765, -0.1765, -0.1765), colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = True
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "slide1" ---
text = visual.TextStim(win=win, name='text',
    text='We will now calibrate the intensity level of the electrical shock.\n\nThe pulse is very short, only 50 milliseconds.\n\nPress space to continue…\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slide1_resp = keyboard.Keyboard()

# --- Initialize components for Routine "slide2" ---
slide2_text = visual.TextStim(win=win, name='slide2_text',
    text='For the purposes of the experiment, the electrical pulse is meant to be annoying.\n\nIt is meant to be something that you do not like, and that you would anticipate receiving.\n\nHowever, it is not meant to be something that would make you say “ouch!”\n\nPress space to continue…\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slide2_resp = keyboard.Keyboard()

# --- Initialize components for Routine "slide3" ---
slide3_text = visual.TextStim(win=win, name='slide3_text',
    text='We will start the calibration at a low level that you might not even feel.\n\nWe will then move it up in stages until it is something that you would describe as highly annoying and unpleasant, but not painful.\n\nOn a scale from 0 (least painful or no sensation) to 9 (worst pain imaginable) the pulse should feel like a 5 or 6.\n',
    font='Open Sans',
    pos=(0, 0), height=0.045, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slide3_resp = keyboard.Keyboard()

# --- Initialize components for Routine "slide4" ---
slide4_text = visual.TextStim(win=win, name='slide4_text',
    text='Press space to deliver a shock.\n\nUsing the intensity scale, please how intense each shock felt.\n\nPress escape to exit calibration.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slide4_resp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "slide1" ---
continueRoutine = True
# update component parameters for each repeat
slide1_resp.keys = []
slide1_resp.rt = []
_slide1_resp_allKeys = []
# keep track of which components have finished
slide1Components = [text, slide1_resp]
for thisComponent in slide1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "slide1" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text.started')
        text.setAutoDraw(True)
    
    # *slide1_resp* updates
    waitOnFlip = False
    if slide1_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        slide1_resp.frameNStart = frameN  # exact frame index
        slide1_resp.tStart = t  # local t and not account for scr refresh
        slide1_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(slide1_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'slide1_resp.started')
        slide1_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(slide1_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(slide1_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if slide1_resp.status == STARTED and not waitOnFlip:
        theseKeys = slide1_resp.getKeys(keyList=['space','1','2','3','4'], waitRelease=False)
        _slide1_resp_allKeys.extend(theseKeys)
        if len(_slide1_resp_allKeys):
            slide1_resp.keys = _slide1_resp_allKeys[-1].name  # just the last key pressed
            slide1_resp.rt = _slide1_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in slide1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "slide1" ---
for thisComponent in slide1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if slide1_resp.keys in ['', [], None]:  # No response was made
    slide1_resp.keys = None
thisExp.addData('slide1_resp.keys',slide1_resp.keys)
if slide1_resp.keys != None:  # we had a response
    thisExp.addData('slide1_resp.rt', slide1_resp.rt)
thisExp.nextEntry()
# the Routine "slide1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "slide2" ---
continueRoutine = True
# update component parameters for each repeat
slide2_resp.keys = []
slide2_resp.rt = []
_slide2_resp_allKeys = []
# keep track of which components have finished
slide2Components = [slide2_text, slide2_resp]
for thisComponent in slide2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "slide2" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *slide2_text* updates
    if slide2_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        slide2_text.frameNStart = frameN  # exact frame index
        slide2_text.tStart = t  # local t and not account for scr refresh
        slide2_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(slide2_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'slide2_text.started')
        slide2_text.setAutoDraw(True)
    
    # *slide2_resp* updates
    waitOnFlip = False
    if slide2_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        slide2_resp.frameNStart = frameN  # exact frame index
        slide2_resp.tStart = t  # local t and not account for scr refresh
        slide2_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(slide2_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'slide2_resp.started')
        slide2_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(slide2_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(slide2_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if slide2_resp.status == STARTED and not waitOnFlip:
        theseKeys = slide2_resp.getKeys(keyList=['space','1','2','3','4'], waitRelease=False)
        _slide2_resp_allKeys.extend(theseKeys)
        if len(_slide2_resp_allKeys):
            slide2_resp.keys = _slide2_resp_allKeys[-1].name  # just the last key pressed
            slide2_resp.rt = _slide2_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in slide2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "slide2" ---
for thisComponent in slide2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if slide2_resp.keys in ['', [], None]:  # No response was made
    slide2_resp.keys = None
thisExp.addData('slide2_resp.keys',slide2_resp.keys)
if slide2_resp.keys != None:  # we had a response
    thisExp.addData('slide2_resp.rt', slide2_resp.rt)
thisExp.nextEntry()
# the Routine "slide2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "slide3" ---
continueRoutine = True
# update component parameters for each repeat
slide3_resp.keys = []
slide3_resp.rt = []
_slide3_resp_allKeys = []
# keep track of which components have finished
slide3Components = [slide3_text, slide3_resp]
for thisComponent in slide3Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "slide3" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *slide3_text* updates
    if slide3_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        slide3_text.frameNStart = frameN  # exact frame index
        slide3_text.tStart = t  # local t and not account for scr refresh
        slide3_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(slide3_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'slide3_text.started')
        slide3_text.setAutoDraw(True)
    
    # *slide3_resp* updates
    waitOnFlip = False
    if slide3_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        slide3_resp.frameNStart = frameN  # exact frame index
        slide3_resp.tStart = t  # local t and not account for scr refresh
        slide3_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(slide3_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'slide3_resp.started')
        slide3_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(slide3_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(slide3_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if slide3_resp.status == STARTED and not waitOnFlip:
        theseKeys = slide3_resp.getKeys(keyList=['space','1','2','3','4'], waitRelease=False)
        _slide3_resp_allKeys.extend(theseKeys)
        if len(_slide3_resp_allKeys):
            slide3_resp.keys = _slide3_resp_allKeys[-1].name  # just the last key pressed
            slide3_resp.rt = _slide3_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in slide3Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "slide3" ---
for thisComponent in slide3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if slide3_resp.keys in ['', [], None]:  # No response was made
    slide3_resp.keys = None
thisExp.addData('slide3_resp.keys',slide3_resp.keys)
if slide3_resp.keys != None:  # we had a response
    thisExp.addData('slide3_resp.rt', slide3_resp.rt)
thisExp.nextEntry()
# the Routine "slide3" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
calibration = data.TrialHandler(nReps=100.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='calibration')
thisExp.addLoop(calibration)  # add the loop to the experiment
thisCalibration = calibration.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisCalibration.rgb)
if thisCalibration != None:
    for paramName in thisCalibration:
        exec('{} = thisCalibration[paramName]'.format(paramName))

for thisCalibration in calibration:
    currentLoop = calibration
    # abbreviate parameter names if possible (e.g. rgb = thisCalibration.rgb)
    if thisCalibration != None:
        for paramName in thisCalibration:
            exec('{} = thisCalibration[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "slide4" ---
    continueRoutine = True
    # update component parameters for each repeat
    slide4_resp.keys = []
    slide4_resp.rt = []
    _slide4_resp_allKeys = []
    # keep track of which components have finished
    slide4Components = [slide4_text, slide4_resp]
    for thisComponent in slide4Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "slide4" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *slide4_text* updates
        if slide4_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            slide4_text.frameNStart = frameN  # exact frame index
            slide4_text.tStart = t  # local t and not account for scr refresh
            slide4_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(slide4_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'slide4_text.started')
            slide4_text.setAutoDraw(True)
        
        # *slide4_resp* updates
        waitOnFlip = False
        if slide4_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            slide4_resp.frameNStart = frameN  # exact frame index
            slide4_resp.tStart = t  # local t and not account for scr refresh
            slide4_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(slide4_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'slide4_resp.started')
            slide4_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(slide4_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(slide4_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if slide4_resp.status == STARTED and not waitOnFlip:
            theseKeys = slide4_resp.getKeys(keyList=['space','1','2','3','4'], waitRelease=False)
            _slide4_resp_allKeys.extend(theseKeys)
            if len(_slide4_resp_allKeys):
                slide4_resp.keys = _slide4_resp_allKeys[-1].name  # just the last key pressed
                slide4_resp.rt = _slide4_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        # Run 'Each Frame' code from code_2
        if 'space' in slide4_resp.keys:
            shock()
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in slide4Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "slide4" ---
    for thisComponent in slide4Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if slide4_resp.keys in ['', [], None]:  # No response was made
        slide4_resp.keys = None
    calibration.addData('slide4_resp.keys',slide4_resp.keys)
    if slide4_resp.keys != None:  # we had a response
        calibration.addData('slide4_resp.rt', slide4_resp.rt)
    # the Routine "slide4" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 100.0 repeats of 'calibration'


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
