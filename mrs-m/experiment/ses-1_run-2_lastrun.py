#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on February 16, 2024, at 13:33
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

# Run 'Before Experiment' code from beg_exp_code
from psychopy.parallel import ParallelPort
from subprocess import Popen
import time

'''fear-acquisition'''
expName = 'fear-acquisition'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-MM')[-1]) for i in os.listdir('data') if 'sub-MM' in i])
dlg.addField('room', choices =['VR', 'behavior']) #added 6/14
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])

user_input = dlg.show()
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-MM{0:0=3d}'.format(int(expInfo['participant']))

BIO = True if user_input[2] == 'yes' and user_input[1] == 'VR' else False #added 6/14
BIO2 = True if user_input[2] == 'yes' and user_input[1] == 'behavior' else False #added 6/14

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
    pport.setPin(2,0) #adjusted for vr room, their shock is through pin 2 (pin 9 in MRI room) 6/8

def stim_marker(on_or_offset='',SHOCK=False):
    if SHOCK:
        shock()
    if 'on' in on_or_offset:
        pport.setPin(4,1)
    elif 'off' in on_or_offset:
        pport.setPin(4,0) #pin 4 for events 6/8


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'fear-acquisition'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '001',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\mrs-m\\experiment\\ses-1_run-2_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[-0.1765, -0.1765, -0.1765], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
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

# --- Initialize components for Routine "in1" ---
inst1_resp = keyboard.Keyboard()
inst1 = visual.TextStim(win=win, name='inst1',
    text='In this next portion of the experiment, you will again see pictures of animals and tools. \n\nHowever, this time, following certain pictures, you will receive an electrical shock to your wrist, right before the picture goes away. \n\n\nPress SPACE to continue with instructions…',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "in2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='This is a learning experiment. \n\nIf you pay attention to the pictures, then you can learn the association between the pictures and the shock. \n\nIn other words, you can learn to predict the shock based on the pictures that you see. \n\nIn the beginning you will just be guessing, but you may learn to predict the shock with some accuracy over time. \n\nPress SPACE to continue with instructions…',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in3" ---
inst3 = visual.TextStim(win=win, name='inst3',
    text='On each trial, you will tell me whether you expect to receive a shock. \n\nYour job is to answer "Yes" or "No" to the following question by pressing the corresponding key on the keypad: \n\nDo you expect to receive a shock following this picture? \n\n1 = Yes \n2 = No \n\nPress SPACE to continue...',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst3_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in4" ---
inst4 = visual.TextStim(win=win, name='inst4',
    text='PLEASE MAKE A RESPONSE ON EVERY TRIAL, even if you are just guessing.  \n\nWe are measuring how fast you press the button. \n\nYou only need to press a button when you see a picture. \n\nPress SPACE to continue with the instructions...\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in5" ---
inst5 = visual.TextStim(win=win, name='inst5',
    text='To recap: \n\nYour job is to answer "Yes" or "No" to whether you expect to receive a shock. \n\nPlease note: You are NOT influencing the shocks with your button presses. \nIn other words, you cannot trigger a shock or avoid a shock with your responses. \nTo be clear: Pressing the "wrong" button will not give you a shock. \n\nDo you have any questions before we get started?',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst5_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in_begin_experiment" ---
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='Press SPACE to begin the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# --- Initialize components for Routine "iti" ---
iti_animal = visual.TextStim(win=win, name='iti_animal',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
iti_tool = visual.TextStim(win=win, name='iti_tool',
    text='2\nNo',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
crosshair = visual.ImageStim(
    win=win,
    name='crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)

# --- Initialize components for Routine "trial" ---
trials_resp = keyboard.Keyboard()
animal = visual.TextStim(win=win, name='animal',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
tool = visual.TextStim(win=win, name='tool',
    text='2\nNo',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
stim_image = visual.ImageStim(
    win=win,
    name='stim_image', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "in_end_experiment" ---
end_exp_resp = keyboard.Keyboard()
end_exp = visual.TextStim(win=win, name='end_exp',
    text='Experimenter press SPACE to exit the task.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "in1" ---
continueRoutine = True
# update component parameters for each repeat
inst1_resp.keys = []
inst1_resp.rt = []
_inst1_resp_allKeys = []
# keep track of which components have finished
in1Components = [inst1_resp, inst1]
for thisComponent in in1Components:
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

# --- Run Routine "in1" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst1_resp* updates
    waitOnFlip = False
    if inst1_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst1_resp.frameNStart = frameN  # exact frame index
        inst1_resp.tStart = t  # local t and not account for scr refresh
        inst1_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1_resp.started')
        inst1_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst1_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst1_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst1_resp.status == STARTED:
        if bool((inst1_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst1_resp.tStop = t  # not accounting for scr refresh
            inst1_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1_resp.stopped')
            inst1_resp.status = FINISHED
    if inst1_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst1_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst1_resp_allKeys.extend(theseKeys)
        if len(_inst1_resp_allKeys):
            inst1_resp.keys = _inst1_resp_allKeys[-1].name  # just the last key pressed
            inst1_resp.rt = _inst1_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *inst1* updates
    if inst1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst1.frameNStart = frameN  # exact frame index
        inst1.tStart = t  # local t and not account for scr refresh
        inst1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1.started')
        inst1.setAutoDraw(True)
    if inst1.status == STARTED:
        if bool((inst1_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst1.tStop = t  # not accounting for scr refresh
            inst1.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1.stopped')
            inst1.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in1" ---
for thisComponent in in1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst1_resp.keys in ['', [], None]:  # No response was made
    inst1_resp.keys = None
thisExp.addData('inst1_resp.keys',inst1_resp.keys)
if inst1_resp.keys != None:  # we had a response
    thisExp.addData('inst1_resp.rt', inst1_resp.rt)
thisExp.nextEntry()
# the Routine "in1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in2" ---
continueRoutine = True
# update component parameters for each repeat
inst2_resp.keys = []
inst2_resp.rt = []
_inst2_resp_allKeys = []
# keep track of which components have finished
in2Components = [inst2, inst2_resp]
for thisComponent in in2Components:
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

# --- Run Routine "in2" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst2* updates
    if inst2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst2.frameNStart = frameN  # exact frame index
        inst2.tStart = t  # local t and not account for scr refresh
        inst2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst2.started')
        inst2.setAutoDraw(True)
    if inst2.status == STARTED:
        if bool((inst2_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2.tStop = t  # not accounting for scr refresh
            inst2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2.stopped')
            inst2.setAutoDraw(False)
    
    # *inst2_resp* updates
    waitOnFlip = False
    if inst2_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst2_resp.frameNStart = frameN  # exact frame index
        inst2_resp.tStart = t  # local t and not account for scr refresh
        inst2_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst2_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst2_resp.started')
        inst2_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst2_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst2_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst2_resp.status == STARTED:
        if bool((inst2_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2_resp.tStop = t  # not accounting for scr refresh
            inst2_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2_resp.stopped')
            inst2_resp.status = FINISHED
    if inst2_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst2_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst2_resp_allKeys.extend(theseKeys)
        if len(_inst2_resp_allKeys):
            inst2_resp.keys = _inst2_resp_allKeys[-1].name  # just the last key pressed
            inst2_resp.rt = _inst2_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in2" ---
for thisComponent in in2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst2_resp.keys in ['', [], None]:  # No response was made
    inst2_resp.keys = None
thisExp.addData('inst2_resp.keys',inst2_resp.keys)
if inst2_resp.keys != None:  # we had a response
    thisExp.addData('inst2_resp.rt', inst2_resp.rt)
thisExp.nextEntry()
# the Routine "in2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in3" ---
continueRoutine = True
# update component parameters for each repeat
inst3_resp.keys = []
inst3_resp.rt = []
_inst3_resp_allKeys = []
# keep track of which components have finished
in3Components = [inst3, inst3_resp]
for thisComponent in in3Components:
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

# --- Run Routine "in3" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst3* updates
    if inst3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3.frameNStart = frameN  # exact frame index
        inst3.tStart = t  # local t and not account for scr refresh
        inst3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst3.started')
        inst3.setAutoDraw(True)
    if inst3.status == STARTED:
        if bool((inst3_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst3.tStop = t  # not accounting for scr refresh
            inst3.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst3.stopped')
            inst3.setAutoDraw(False)
    
    # *inst3_resp* updates
    waitOnFlip = False
    if inst3_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3_resp.frameNStart = frameN  # exact frame index
        inst3_resp.tStart = t  # local t and not account for scr refresh
        inst3_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst3_resp.started')
        inst3_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst3_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst3_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst3_resp.status == STARTED:
        if bool((inst3_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst3_resp.tStop = t  # not accounting for scr refresh
            inst3_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst3_resp.stopped')
            inst3_resp.status = FINISHED
    if inst3_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst3_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst3_resp_allKeys.extend(theseKeys)
        if len(_inst3_resp_allKeys):
            inst3_resp.keys = _inst3_resp_allKeys[-1].name  # just the last key pressed
            inst3_resp.rt = _inst3_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in3Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in3" ---
for thisComponent in in3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst3_resp.keys in ['', [], None]:  # No response was made
    inst3_resp.keys = None
thisExp.addData('inst3_resp.keys',inst3_resp.keys)
if inst3_resp.keys != None:  # we had a response
    thisExp.addData('inst3_resp.rt', inst3_resp.rt)
thisExp.nextEntry()
# the Routine "in3" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in4" ---
continueRoutine = True
# update component parameters for each repeat
inst4_resp.keys = []
inst4_resp.rt = []
_inst4_resp_allKeys = []
# keep track of which components have finished
in4Components = [inst4, inst4_resp]
for thisComponent in in4Components:
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

# --- Run Routine "in4" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst4* updates
    if inst4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst4.frameNStart = frameN  # exact frame index
        inst4.tStart = t  # local t and not account for scr refresh
        inst4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst4, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst4.started')
        inst4.setAutoDraw(True)
    if inst4.status == STARTED:
        if bool((inst4_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst4.tStop = t  # not accounting for scr refresh
            inst4.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4.stopped')
            inst4.setAutoDraw(False)
    
    # *inst4_resp* updates
    waitOnFlip = False
    if inst4_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst4_resp.frameNStart = frameN  # exact frame index
        inst4_resp.tStart = t  # local t and not account for scr refresh
        inst4_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst4_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst4_resp.started')
        inst4_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst4_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst4_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst4_resp.status == STARTED:
        if bool((inst4_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst4_resp.tStop = t  # not accounting for scr refresh
            inst4_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4_resp.stopped')
            inst4_resp.status = FINISHED
    if inst4_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst4_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst4_resp_allKeys.extend(theseKeys)
        if len(_inst4_resp_allKeys):
            inst4_resp.keys = _inst4_resp_allKeys[-1].name  # just the last key pressed
            inst4_resp.rt = _inst4_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in4Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in4" ---
for thisComponent in in4Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst4_resp.keys in ['', [], None]:  # No response was made
    inst4_resp.keys = None
thisExp.addData('inst4_resp.keys',inst4_resp.keys)
if inst4_resp.keys != None:  # we had a response
    thisExp.addData('inst4_resp.rt', inst4_resp.rt)
thisExp.nextEntry()
# the Routine "in4" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in5" ---
continueRoutine = True
# update component parameters for each repeat
inst5_resp.keys = []
inst5_resp.rt = []
_inst5_resp_allKeys = []
# keep track of which components have finished
in5Components = [inst5, inst5_resp]
for thisComponent in in5Components:
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

# --- Run Routine "in5" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst5* updates
    if inst5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst5.frameNStart = frameN  # exact frame index
        inst5.tStart = t  # local t and not account for scr refresh
        inst5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst5, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst5.started')
        inst5.setAutoDraw(True)
    if inst5.status == STARTED:
        if bool((inst5_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst5.tStop = t  # not accounting for scr refresh
            inst5.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst5.stopped')
            inst5.setAutoDraw(False)
    
    # *inst5_resp* updates
    waitOnFlip = False
    if inst5_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst5_resp.frameNStart = frameN  # exact frame index
        inst5_resp.tStart = t  # local t and not account for scr refresh
        inst5_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst5_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst5_resp.started')
        inst5_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst5_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst5_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst5_resp.status == STARTED:
        if bool((inst5_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst5_resp.tStop = t  # not accounting for scr refresh
            inst5_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst5_resp.stopped')
            inst5_resp.status = FINISHED
    if inst5_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst5_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst5_resp_allKeys.extend(theseKeys)
        if len(_inst5_resp_allKeys):
            inst5_resp.keys = _inst5_resp_allKeys[-1].name  # just the last key pressed
            inst5_resp.rt = _inst5_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in5Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in5" ---
for thisComponent in in5Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst5_resp.keys in ['', [], None]:  # No response was made
    inst5_resp.keys = None
thisExp.addData('inst5_resp.keys',inst5_resp.keys)
if inst5_resp.keys != None:  # we had a response
    thisExp.addData('inst5_resp.rt', inst5_resp.rt)
thisExp.nextEntry()
# the Routine "in5" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in_begin_experiment" ---
continueRoutine = True
# update component parameters for each repeat
beg_exp_resp.keys = []
beg_exp_resp.rt = []
_beg_exp_resp_allKeys = []
# keep track of which components have finished
in_begin_experimentComponents = [beg_exp, beg_exp_resp]
for thisComponent in in_begin_experimentComponents:
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

# --- Run Routine "in_begin_experiment" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *beg_exp* updates
    if beg_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beg_exp.frameNStart = frameN  # exact frame index
        beg_exp.tStart = t  # local t and not account for scr refresh
        beg_exp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beg_exp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'beg_exp.started')
        beg_exp.setAutoDraw(True)
    if beg_exp.status == STARTED:
        if bool((beg_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            beg_exp.tStop = t  # not accounting for scr refresh
            beg_exp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'beg_exp.stopped')
            beg_exp.setAutoDraw(False)
    
    # *beg_exp_resp* updates
    waitOnFlip = False
    if beg_exp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beg_exp_resp.frameNStart = frameN  # exact frame index
        beg_exp_resp.tStart = t  # local t and not account for scr refresh
        beg_exp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beg_exp_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'beg_exp_resp.started')
        beg_exp_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(beg_exp_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(beg_exp_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if beg_exp_resp.status == STARTED:
        if bool((beg_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            beg_exp_resp.tStop = t  # not accounting for scr refresh
            beg_exp_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'beg_exp_resp.stopped')
            beg_exp_resp.status = FINISHED
    if beg_exp_resp.status == STARTED and not waitOnFlip:
        theseKeys = beg_exp_resp.getKeys(keyList=['space'], waitRelease=False)
        _beg_exp_resp_allKeys.extend(theseKeys)
        if len(_beg_exp_resp_allKeys):
            beg_exp_resp.keys = _beg_exp_resp_allKeys[-1].name  # just the last key pressed
            beg_exp_resp.rt = _beg_exp_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in_begin_experimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in_begin_experiment" ---
for thisComponent in in_begin_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if beg_exp_resp.keys in ['', [], None]:  # No response was made
    beg_exp_resp.keys = None
thisExp.addData('beg_exp_resp.keys',beg_exp_resp.keys)
if beg_exp_resp.keys != None:  # we had a response
    thisExp.addData('beg_exp_resp.rt', beg_exp_resp.rt)
thisExp.nextEntry()
# the Routine "in_begin_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
cond_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-1_task-fear_events-input.csv'),
    seed=None, name='cond_trials')
thisExp.addLoop(cond_trials)  # add the loop to the experiment
thisCond_trial = cond_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisCond_trial.rgb)
if thisCond_trial != None:
    for paramName in thisCond_trial:
        exec('{} = thisCond_trial[paramName]'.format(paramName))

for thisCond_trial in cond_trials:
    currentLoop = cond_trials
    # abbreviate parameter names if possible (e.g. rgb = thisCond_trial.rgb)
    if thisCond_trial != None:
        for paramName in thisCond_trial:
            exec('{} = thisCond_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [iti_animal, iti_tool, crosshair]
    for thisComponent in itiComponents:
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
    
    # --- Run Routine "iti" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *iti_animal* updates
        if iti_animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_animal.frameNStart = frameN  # exact frame index
            iti_animal.tStart = t  # local t and not account for scr refresh
            iti_animal.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_animal, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'iti_animal.started')
            iti_animal.setAutoDraw(True)
        if iti_animal.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_animal.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_animal.tStop = t  # not accounting for scr refresh
                iti_animal.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'iti_animal.stopped')
                iti_animal.setAutoDraw(False)
        
        # *iti_tool* updates
        if iti_tool.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_tool.frameNStart = frameN  # exact frame index
            iti_tool.tStart = t  # local t and not account for scr refresh
            iti_tool.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_tool, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'iti_tool.started')
            iti_tool.setAutoDraw(True)
        if iti_tool.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_tool.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_tool.tStop = t  # not accounting for scr refresh
                iti_tool.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'iti_tool.stopped')
                iti_tool.setAutoDraw(False)
        
        # *crosshair* updates
        if crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            crosshair.frameNStart = frameN  # exact frame index
            crosshair.tStart = t  # local t and not account for scr refresh
            crosshair.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(crosshair, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'crosshair.started')
            crosshair.setAutoDraw(True)
        if crosshair.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > crosshair.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                crosshair.tStop = t  # not accounting for scr refresh
                crosshair.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'crosshair.stopped')
                crosshair.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in itiComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "iti" ---
    for thisComponent in itiComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "iti" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    trials_resp.keys = []
    trials_resp.rt = []
    _trials_resp_allKeys = []
    stim_image.setImage(stimulus)
    # Run 'Begin Routine' code from cs_code
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set the response colors to white
    animal_resp_color = 'white'
    tool_resp_color = 'white'
    # keep track of which components have finished
    trialComponents = [trials_resp, animal, tool, stim_image]
    for thisComponent in trialComponents:
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
    
    # --- Run Routine "trial" ---
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trials_resp* updates
        waitOnFlip = False
        if trials_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            trials_resp.frameNStart = frameN  # exact frame index
            trials_resp.tStart = t  # local t and not account for scr refresh
            trials_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trials_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trials_resp.started')
            trials_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trials_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trials_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trials_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > trials_resp.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                trials_resp.tStop = t  # not accounting for scr refresh
                trials_resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trials_resp.stopped')
                trials_resp.status = FINISHED
        if trials_resp.status == STARTED and not waitOnFlip:
            theseKeys = trials_resp.getKeys(keyList=['num_1','num_2','1','2'], waitRelease=False)
            _trials_resp_allKeys.extend(theseKeys)
            if len(_trials_resp_allKeys):
                trials_resp.keys = _trials_resp_allKeys[0].name  # just the first key pressed
                trials_resp.rt = _trials_resp_allKeys[0].rt
        
        # *animal* updates
        if animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            animal.frameNStart = frameN  # exact frame index
            animal.tStart = t  # local t and not account for scr refresh
            animal.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(animal, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'animal.started')
            animal.setAutoDraw(True)
        if animal.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > animal.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                animal.tStop = t  # not accounting for scr refresh
                animal.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'animal.stopped')
                animal.setAutoDraw(False)
        if animal.status == STARTED:  # only update if drawing
            animal.setColor(animal_resp_color, colorSpace='rgb', log=False)
        
        # *tool* updates
        if tool.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            tool.frameNStart = frameN  # exact frame index
            tool.tStart = t  # local t and not account for scr refresh
            tool.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(tool, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'tool.started')
            tool.setAutoDraw(True)
        if tool.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > tool.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                tool.tStop = t  # not accounting for scr refresh
                tool.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'tool.stopped')
                tool.setAutoDraw(False)
        if tool.status == STARTED:  # only update if drawing
            tool.setColor(tool_resp_color, colorSpace='rgb', log=False)
        
        # *stim_image* updates
        if stim_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stim_image.frameNStart = frameN  # exact frame index
            stim_image.tStart = t  # local t and not account for scr refresh
            stim_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stim_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stim_image.started')
            stim_image.setAutoDraw(True)
        if stim_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stim_image.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                stim_image.tStop = t  # not accounting for scr refresh
                stim_image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim_image.stopped')
                stim_image.setAutoDraw(False)
        # Run 'Each Frame' code from cs_code
        #change the color of the response if one is pressed
        if 'num_1' in trials_resp.keys:
            animal_resp_color = 'darkgrey'
            tool_resp_color = 'white'
        elif 'num_2' in trials_resp.keys:
            tool_resp_color = 'darkgrey'
            animal_resp_color = 'white'
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trials_resp.keys in ['', [], None]:  # No response was made
        trials_resp.keys = None
    cond_trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        cond_trials.addData('trials_resp.rt', trials_resp.rt)
    # Run 'End Routine' code from cs_code
    #send the event code
    stim_marker('offset',SHOCK=bool(int(us))) #deliver shock if need be
    
    #make sure to debug this later, added from home on 6/8
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'cond_trials'


# --- Prepare to start Routine "in_end_experiment" ---
continueRoutine = True
# update component parameters for each repeat
end_exp_resp.keys = []
end_exp_resp.rt = []
_end_exp_resp_allKeys = []
# keep track of which components have finished
in_end_experimentComponents = [end_exp_resp, end_exp]
for thisComponent in in_end_experimentComponents:
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

# --- Run Routine "in_end_experiment" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_exp_resp* updates
    waitOnFlip = False
    if end_exp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_exp_resp.frameNStart = frameN  # exact frame index
        end_exp_resp.tStart = t  # local t and not account for scr refresh
        end_exp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_exp_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'end_exp_resp.started')
        end_exp_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(end_exp_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(end_exp_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if end_exp_resp.status == STARTED:
        if bool((end_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            end_exp_resp.tStop = t  # not accounting for scr refresh
            end_exp_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_exp_resp.stopped')
            end_exp_resp.status = FINISHED
    if end_exp_resp.status == STARTED and not waitOnFlip:
        theseKeys = end_exp_resp.getKeys(keyList=['space'], waitRelease=False)
        _end_exp_resp_allKeys.extend(theseKeys)
        if len(_end_exp_resp_allKeys):
            end_exp_resp.keys = _end_exp_resp_allKeys[-1].name  # just the last key pressed
            end_exp_resp.rt = _end_exp_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *end_exp* updates
    if end_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_exp.frameNStart = frameN  # exact frame index
        end_exp.tStart = t  # local t and not account for scr refresh
        end_exp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_exp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'end_exp.started')
        end_exp.setAutoDraw(True)
    if end_exp.status == STARTED:
        if bool((end_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            end_exp.tStop = t  # not accounting for scr refresh
            end_exp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_exp.stopped')
            end_exp.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in_end_experimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in_end_experiment" ---
for thisComponent in in_end_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if end_exp_resp.keys in ['', [], None]:  # No response was made
    end_exp_resp.keys = None
thisExp.addData('end_exp_resp.keys',end_exp_resp.keys)
if end_exp_resp.keys != None:  # we had a response
    thisExp.addData('end_exp_resp.rt', end_exp_resp.rt)
thisExp.nextEntry()
# the Routine "in_end_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
