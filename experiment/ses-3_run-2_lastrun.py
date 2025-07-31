#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on Wed Jul 30 15:08:09 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Run 'Before Experiment' code from beg_exp_code
from psychopy.parallel import ParallelPort
from subprocess import Popen
import time

expName = 'recall'  # from the Builder filename that created this script
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-PYG')[-1]) for i in os.listdir('data') if 'sub-PYG' in i])
dlg.addField('room', choices =['VR', 'behavior']) #added 6/14
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])

user_input = dlg.show()
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-PYG{0:0=3d}'.format(int(expInfo['participant']))

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
psychopyVersion = '2023.1.3'
expName = 'recall'  # from the Builder filename that created this script
expInfo = {
    'session': '2',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-2_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/sydneylambert/Desktop/pig/experiment/ses-3_run-2_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1512, 982], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[-0.1765, -0.1765, -0.1765], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
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
ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='event')

# --- Initialize components for Routine "ins1" ---
inst3 = visual.TextStim(win=win, name='inst3',
    text='Now we are going to test your memory for the pictures that you saw on your first visit.\nPlease let us know whether you expected a memory test today: \n\n\n1 = No, I did not expect a memory test at all. \n\n2 = I am somewhat surprised by this memory test. \n\n3 = I am only a little surprised by a memory test.\n \n4 = I somewhat expected a memory test. \n\n5 = Yes, I knew there would be a memory test. \n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst3_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='For each picture, please indicate whether you saw the picture on your first visit (it is “OLD”), or whether you did NOT see the picture on your first visit (it is “NEW”). \n\nYou will rate the confidence of your decision by indicating whether the picture is: \n\n1 = Old\n2 = New\n\n\nYou will not be receiving any shocks during this portion of the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst5_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in4" ---
inst4 = visual.TextStim(win=win, name='inst4',
    text='PLEASE MAKE A RESPONSE ON EVERY TRIAL, even if you are just guessing.  \n\nWe are measuring how fast you press the button. \n\nYou only need to press a button when you see a picture. \n\nPress SPACE to continue with the instructions...\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in_begin_experiment" ---
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='--',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# --- Initialize components for Routine "initial_iti" ---
iti_old = visual.TextStim(win=win, name='iti_old',
    text='1\nDefinitely Old',
    font='Open Sans',
    pos=(-.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
maybe_old_2 = visual.TextStim(win=win, name='maybe_old_2',
    text='2\nMaybe Old',
    font='Open Sans',
    pos=(-.10,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
maybe_new_2 = visual.TextStim(win=win, name='maybe_new_2',
    text='3\nMaybe New',
    font='Open Sans',
    pos=(.10,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
iti_new = visual.TextStim(win=win, name='iti_new',
    text='4\nDefinitely New',
    font='Open Sans',
    pos=(.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
iti_initial = visual.ImageStim(
    win=win,
    name='iti_initial', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)

# --- Initialize components for Routine "trial" ---
trials_resp = keyboard.Keyboard()
mem_quest = visual.TextStim(win=win, name='mem_quest',
    text='Is this picture OLD or NEW?',
    font='Open Sans',
    pos=(0, .3), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
old = visual.TextStim(win=win, name='old',
    text='1\nDefinitely Old',
    font='Open Sans',
    pos=(-.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
maybe_old = visual.TextStim(win=win, name='maybe_old',
    text='2\nMaybe Old',
    font='Open Sans',
    pos=(-.10,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
maybe_new = visual.TextStim(win=win, name='maybe_new',
    text='3\nMaybe New',
    font='Open Sans',
    pos=(.10,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
new = visual.TextStim(win=win, name='new',
    text='4\nDefinitely New',
    font='Open Sans',
    pos=(.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
recall_image = visual.ImageStim(
    win=win,
    name='recall_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
# Run 'Begin Experiment' code from cs_code
response_made = True

# --- Initialize components for Routine "iti" ---
old_iti = visual.TextStim(win=win, name='old_iti',
    text='1\nDefinitely Old',
    font='Open Sans',
    pos=(-.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
maybe_old_3 = visual.TextStim(win=win, name='maybe_old_3',
    text='2\nMaybe Old',
    font='Open Sans',
    pos=(-.10, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
maybe_new_3 = visual.TextStim(win=win, name='maybe_new_3',
    text='3\nMaybe New',
    font='Open Sans',
    pos=(.10, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
new_iti = visual.TextStim(win=win, name='new_iti',
    text='4\nDefinitely New',
    font='Open Sans',
    pos=(.3, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
iti_trial = visual.ImageStim(
    win=win,
    name='iti_trial', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
warning_text = visual.TextStim(win=win, name='warning_text',
    text='',
    font='Open Sans',
    pos=(0, .3), height=0.04, wrapWidth=None, ori=0.0, 
    color='orange', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-6.0);

# --- Initialize components for Routine "final_iti" ---
iti_old2 = visual.TextStim(win=win, name='iti_old2',
    text='1\nDefinitely Old',
    font='Open Sans',
    pos=(-.30, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
maybe_old_4 = visual.TextStim(win=win, name='maybe_old_4',
    text='2\nMaybe Old',
    font='Open Sans',
    pos=(-.1, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
maybe_new_4 = visual.TextStim(win=win, name='maybe_new_4',
    text='3\nMaybe New',
    font='Open Sans',
    pos=(.1, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
iti_new2 = visual.TextStim(win=win, name='iti_new2',
    text='4\nDefinitely New',
    font='Open Sans',
    pos=(.3, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
iti_final = visual.ImageStim(
    win=win,
    name='iti_final', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)

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

# --- Prepare to start Routine "ins1" ---
continueRoutine = True
# update component parameters for each repeat
inst3_resp.keys = []
inst3_resp.rt = []
_inst3_resp_allKeys = []
# keep track of which components have finished
ins1Components = [inst3, inst3_resp]
for thisComponent in ins1Components:
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

# --- Run Routine "ins1" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst3* updates
    
    # if inst3 is starting this frame...
    if inst3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3.frameNStart = frameN  # exact frame index
        inst3.tStart = t  # local t and not account for scr refresh
        inst3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst3.status = STARTED
        inst3.setAutoDraw(True)
    
    # if inst3 is active this frame...
    if inst3.status == STARTED:
        # update params
        pass
    
    # *inst3_resp* updates
    waitOnFlip = False
    
    # if inst3_resp is starting this frame...
    if inst3_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3_resp.frameNStart = frameN  # exact frame index
        inst3_resp.tStart = t  # local t and not account for scr refresh
        inst3_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst3_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst3_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst3_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst3_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst3_resp.getKeys(keyList=['1','2','3','4','5'], waitRelease=False)
        _inst3_resp_allKeys.extend(theseKeys)
        if len(_inst3_resp_allKeys):
            inst3_resp.keys = _inst3_resp_allKeys[-1].name  # just the last key pressed
            inst3_resp.rt = _inst3_resp_allKeys[-1].rt
            inst3_resp.duration = _inst3_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ins1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "ins1" ---
for thisComponent in ins1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "ins1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "in2" ---
continueRoutine = True
# update component parameters for each repeat
inst5_resp.keys = []
inst5_resp.rt = []
_inst5_resp_allKeys = []
# keep track of which components have finished
in2Components = [inst2, inst5_resp]
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
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst2* updates
    
    # if inst2 is starting this frame...
    if inst2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst2.frameNStart = frameN  # exact frame index
        inst2.tStart = t  # local t and not account for scr refresh
        inst2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst2, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst2.status = STARTED
        inst2.setAutoDraw(True)
    
    # if inst2 is active this frame...
    if inst2.status == STARTED:
        # update params
        pass
    
    # if inst2 is stopping this frame...
    if inst2.status == STARTED:
        if bool((inst5_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2.tStop = t  # not accounting for scr refresh
            inst2.frameNStop = frameN  # exact frame index
            # update status
            inst2.status = FINISHED
            inst2.setAutoDraw(False)
    
    # *inst5_resp* updates
    waitOnFlip = False
    
    # if inst5_resp is starting this frame...
    if inst5_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst5_resp.frameNStart = frameN  # exact frame index
        inst5_resp.tStart = t  # local t and not account for scr refresh
        inst5_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst5_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst5_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst5_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst5_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if inst5_resp is stopping this frame...
    if inst5_resp.status == STARTED:
        if bool((inst5_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst5_resp.tStop = t  # not accounting for scr refresh
            inst5_resp.frameNStop = frameN  # exact frame index
            # update status
            inst5_resp.status = FINISHED
            inst5_resp.status = FINISHED
    if inst5_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst5_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst5_resp_allKeys.extend(theseKeys)
        if len(_inst5_resp_allKeys):
            inst5_resp.keys = _inst5_resp_allKeys[-1].name  # just the last key pressed
            inst5_resp.rt = _inst5_resp_allKeys[-1].rt
            inst5_resp.duration = _inst5_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
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
# the Routine "in2" was not non-slip safe, so reset the non-slip timer
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
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst4* updates
    
    # if inst4 is starting this frame...
    if inst4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst4.frameNStart = frameN  # exact frame index
        inst4.tStart = t  # local t and not account for scr refresh
        inst4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst4, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst4.status = STARTED
        inst4.setAutoDraw(True)
    
    # if inst4 is active this frame...
    if inst4.status == STARTED:
        # update params
        pass
    
    # if inst4 is stopping this frame...
    if inst4.status == STARTED:
        if bool((inst4_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst4.tStop = t  # not accounting for scr refresh
            inst4.frameNStop = frameN  # exact frame index
            # update status
            inst4.status = FINISHED
            inst4.setAutoDraw(False)
    
    # *inst4_resp* updates
    waitOnFlip = False
    
    # if inst4_resp is starting this frame...
    if inst4_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst4_resp.frameNStart = frameN  # exact frame index
        inst4_resp.tStart = t  # local t and not account for scr refresh
        inst4_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst4_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        inst4_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst4_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst4_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if inst4_resp is stopping this frame...
    if inst4_resp.status == STARTED:
        if bool((inst4_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst4_resp.tStop = t  # not accounting for scr refresh
            inst4_resp.frameNStop = frameN  # exact frame index
            # update status
            inst4_resp.status = FINISHED
            inst4_resp.status = FINISHED
    if inst4_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst4_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst4_resp_allKeys.extend(theseKeys)
        if len(_inst4_resp_allKeys):
            inst4_resp.keys = _inst4_resp_allKeys[-1].name  # just the last key pressed
            inst4_resp.rt = _inst4_resp_allKeys[-1].rt
            inst4_resp.duration = _inst4_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
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
# the Routine "in4" was not non-slip safe, so reset the non-slip timer
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
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *beg_exp* updates
    
    # if beg_exp is starting this frame...
    if beg_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beg_exp.frameNStart = frameN  # exact frame index
        beg_exp.tStart = t  # local t and not account for scr refresh
        beg_exp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beg_exp, 'tStartRefresh')  # time at next scr refresh
        # update status
        beg_exp.status = STARTED
        beg_exp.setAutoDraw(True)
    
    # if beg_exp is active this frame...
    if beg_exp.status == STARTED:
        # update params
        pass
    
    # if beg_exp is stopping this frame...
    if beg_exp.status == STARTED:
        if bool((beg_exp_resp.keys)=='5'):
            # keep track of stop time/frame for later
            beg_exp.tStop = t  # not accounting for scr refresh
            beg_exp.frameNStop = frameN  # exact frame index
            # update status
            beg_exp.status = FINISHED
            beg_exp.setAutoDraw(False)
    
    # *beg_exp_resp* updates
    waitOnFlip = False
    
    # if beg_exp_resp is starting this frame...
    if beg_exp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beg_exp_resp.frameNStart = frameN  # exact frame index
        beg_exp_resp.tStart = t  # local t and not account for scr refresh
        beg_exp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beg_exp_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        beg_exp_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(beg_exp_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(beg_exp_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if beg_exp_resp is stopping this frame...
    if beg_exp_resp.status == STARTED:
        if bool((beg_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            beg_exp_resp.tStop = t  # not accounting for scr refresh
            beg_exp_resp.frameNStop = frameN  # exact frame index
            # update status
            beg_exp_resp.status = FINISHED
            beg_exp_resp.status = FINISHED
    if beg_exp_resp.status == STARTED and not waitOnFlip:
        theseKeys = beg_exp_resp.getKeys(keyList=['5'], waitRelease=False)
        _beg_exp_resp_allKeys.extend(theseKeys)
        if len(_beg_exp_resp_allKeys):
            beg_exp_resp.keys = _beg_exp_resp_allKeys[-1].name  # just the last key pressed
            beg_exp_resp.rt = _beg_exp_resp_allKeys[-1].rt
            beg_exp_resp.duration = _beg_exp_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
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
# the Routine "in_begin_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "initial_iti" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
initial_itiComponents = [iti_old, maybe_old_2, maybe_new_2, iti_new, iti_initial]
for thisComponent in initial_itiComponents:
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

# --- Run Routine "initial_iti" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 10.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *iti_old* updates
    
    # if iti_old is starting this frame...
    if iti_old.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_old.frameNStart = frameN  # exact frame index
        iti_old.tStart = t  # local t and not account for scr refresh
        iti_old.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_old, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_old.status = STARTED
        iti_old.setAutoDraw(True)
    
    # if iti_old is active this frame...
    if iti_old.status == STARTED:
        # update params
        pass
    
    # if iti_old is stopping this frame...
    if iti_old.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_old.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_old.tStop = t  # not accounting for scr refresh
            iti_old.frameNStop = frameN  # exact frame index
            # update status
            iti_old.status = FINISHED
            iti_old.setAutoDraw(False)
    
    # *maybe_old_2* updates
    
    # if maybe_old_2 is starting this frame...
    if maybe_old_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        maybe_old_2.frameNStart = frameN  # exact frame index
        maybe_old_2.tStart = t  # local t and not account for scr refresh
        maybe_old_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(maybe_old_2, 'tStartRefresh')  # time at next scr refresh
        # update status
        maybe_old_2.status = STARTED
        maybe_old_2.setAutoDraw(True)
    
    # if maybe_old_2 is active this frame...
    if maybe_old_2.status == STARTED:
        # update params
        maybe_old_2.setColor('white', colorSpace='rgb', log=False)
    
    # if maybe_old_2 is stopping this frame...
    if maybe_old_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > maybe_old_2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            maybe_old_2.tStop = t  # not accounting for scr refresh
            maybe_old_2.frameNStop = frameN  # exact frame index
            # update status
            maybe_old_2.status = FINISHED
            maybe_old_2.setAutoDraw(False)
    
    # *maybe_new_2* updates
    
    # if maybe_new_2 is starting this frame...
    if maybe_new_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        maybe_new_2.frameNStart = frameN  # exact frame index
        maybe_new_2.tStart = t  # local t and not account for scr refresh
        maybe_new_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(maybe_new_2, 'tStartRefresh')  # time at next scr refresh
        # update status
        maybe_new_2.status = STARTED
        maybe_new_2.setAutoDraw(True)
    
    # if maybe_new_2 is active this frame...
    if maybe_new_2.status == STARTED:
        # update params
        maybe_new_2.setColor('white', colorSpace='rgb', log=False)
    
    # if maybe_new_2 is stopping this frame...
    if maybe_new_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > maybe_new_2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            maybe_new_2.tStop = t  # not accounting for scr refresh
            maybe_new_2.frameNStop = frameN  # exact frame index
            # update status
            maybe_new_2.status = FINISHED
            maybe_new_2.setAutoDraw(False)
    
    # *iti_new* updates
    
    # if iti_new is starting this frame...
    if iti_new.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_new.frameNStart = frameN  # exact frame index
        iti_new.tStart = t  # local t and not account for scr refresh
        iti_new.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_new, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_new.status = STARTED
        iti_new.setAutoDraw(True)
    
    # if iti_new is active this frame...
    if iti_new.status == STARTED:
        # update params
        pass
    
    # if iti_new is stopping this frame...
    if iti_new.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_new.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_new.tStop = t  # not accounting for scr refresh
            iti_new.frameNStop = frameN  # exact frame index
            # update status
            iti_new.status = FINISHED
            iti_new.setAutoDraw(False)
    
    # *iti_initial* updates
    
    # if iti_initial is starting this frame...
    if iti_initial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_initial.frameNStart = frameN  # exact frame index
        iti_initial.tStart = t  # local t and not account for scr refresh
        iti_initial.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_initial, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'iti_initial.started')
        # update status
        iti_initial.status = STARTED
        iti_initial.setAutoDraw(True)
    
    # if iti_initial is active this frame...
    if iti_initial.status == STARTED:
        # update params
        pass
    
    # if iti_initial is stopping this frame...
    if iti_initial.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_initial.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_initial.tStop = t  # not accounting for scr refresh
            iti_initial.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'iti_initial.stopped')
            # update status
            iti_initial.status = FINISHED
            iti_initial.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initial_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "initial_iti" ---
for thisComponent in initial_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-10.000000)

# set up handler to look after randomisation of conditions etc
bps1_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-3_task-bps1_events-input.csv'),
    seed=None, name='bps1_trials')
thisExp.addLoop(bps1_trials)  # add the loop to the experiment
thisBps1_trial = bps1_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBps1_trial.rgb)
if thisBps1_trial != None:
    for paramName in thisBps1_trial:
        exec('{} = thisBps1_trial[paramName]'.format(paramName))

for thisBps1_trial in bps1_trials:
    currentLoop = bps1_trials
    # abbreviate parameter names if possible (e.g. rgb = thisBps1_trial.rgb)
    if thisBps1_trial != None:
        for paramName in thisBps1_trial:
            exec('{} = thisBps1_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    trials_resp.keys = []
    trials_resp.rt = []
    _trials_resp_allKeys = []
    recall_image.setImage(stim)
    # Run 'Begin Routine' code from cs_code
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set the response colors to white
    old_resp_color = 'white'
    new_resp_color = 'white'
    maybe_old_resp_color = 'white'
    maybe_new_resp_color = 'white'
    # keep track of which components have finished
    trialComponents = [trials_resp, mem_quest, old, maybe_old, maybe_new, new, recall_image]
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
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trials_resp* updates
        waitOnFlip = False
        
        # if trials_resp is starting this frame...
        if trials_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            trials_resp.frameNStart = frameN  # exact frame index
            trials_resp.tStart = t  # local t and not account for scr refresh
            trials_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trials_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trials_resp.started')
            # update status
            trials_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trials_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trials_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if trials_resp is stopping this frame...
        if trials_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > trials_resp.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                trials_resp.tStop = t  # not accounting for scr refresh
                trials_resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trials_resp.stopped')
                # update status
                trials_resp.status = FINISHED
                trials_resp.status = FINISHED
        if trials_resp.status == STARTED and not waitOnFlip:
            theseKeys = trials_resp.getKeys(keyList=['num_1','num_2','1','2','3','4','num_3','num_4'], waitRelease=False)
            _trials_resp_allKeys.extend(theseKeys)
            if len(_trials_resp_allKeys):
                trials_resp.keys = _trials_resp_allKeys[0].name  # just the first key pressed
                trials_resp.rt = _trials_resp_allKeys[0].rt
                trials_resp.duration = _trials_resp_allKeys[0].duration
        
        # *mem_quest* updates
        
        # if mem_quest is starting this frame...
        if mem_quest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mem_quest.frameNStart = frameN  # exact frame index
            mem_quest.tStart = t  # local t and not account for scr refresh
            mem_quest.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mem_quest, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'mem_quest.started')
            # update status
            mem_quest.status = STARTED
            mem_quest.setAutoDraw(True)
        
        # if mem_quest is active this frame...
        if mem_quest.status == STARTED:
            # update params
            pass
        
        # if mem_quest is stopping this frame...
        if mem_quest.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mem_quest.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                mem_quest.tStop = t  # not accounting for scr refresh
                mem_quest.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'mem_quest.stopped')
                # update status
                mem_quest.status = FINISHED
                mem_quest.setAutoDraw(False)
        
        # *old* updates
        
        # if old is starting this frame...
        if old.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            old.frameNStart = frameN  # exact frame index
            old.tStart = t  # local t and not account for scr refresh
            old.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(old, 'tStartRefresh')  # time at next scr refresh
            # update status
            old.status = STARTED
            old.setAutoDraw(True)
        
        # if old is active this frame...
        if old.status == STARTED:
            # update params
            old.setColor(old_resp_color, colorSpace='rgb', log=False)
        
        # if old is stopping this frame...
        if old.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > old.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                old.tStop = t  # not accounting for scr refresh
                old.frameNStop = frameN  # exact frame index
                # update status
                old.status = FINISHED
                old.setAutoDraw(False)
        
        # *maybe_old* updates
        
        # if maybe_old is starting this frame...
        if maybe_old.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_old.frameNStart = frameN  # exact frame index
            maybe_old.tStart = t  # local t and not account for scr refresh
            maybe_old.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_old, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_old.status = STARTED
            maybe_old.setAutoDraw(True)
        
        # if maybe_old is active this frame...
        if maybe_old.status == STARTED:
            # update params
            maybe_old.setColor(maybe_old_resp_color, colorSpace='rgb', log=False)
        
        # if maybe_old is stopping this frame...
        if maybe_old.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_old.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybe_old.tStop = t  # not accounting for scr refresh
                maybe_old.frameNStop = frameN  # exact frame index
                # update status
                maybe_old.status = FINISHED
                maybe_old.setAutoDraw(False)
        
        # *maybe_new* updates
        
        # if maybe_new is starting this frame...
        if maybe_new.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_new.frameNStart = frameN  # exact frame index
            maybe_new.tStart = t  # local t and not account for scr refresh
            maybe_new.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_new, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_new.status = STARTED
            maybe_new.setAutoDraw(True)
        
        # if maybe_new is active this frame...
        if maybe_new.status == STARTED:
            # update params
            maybe_new.setColor(maybe_new_resp_color, colorSpace='rgb', log=False)
        
        # if maybe_new is stopping this frame...
        if maybe_new.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_new.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybe_new.tStop = t  # not accounting for scr refresh
                maybe_new.frameNStop = frameN  # exact frame index
                # update status
                maybe_new.status = FINISHED
                maybe_new.setAutoDraw(False)
        
        # *new* updates
        
        # if new is starting this frame...
        if new.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            new.frameNStart = frameN  # exact frame index
            new.tStart = t  # local t and not account for scr refresh
            new.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(new, 'tStartRefresh')  # time at next scr refresh
            # update status
            new.status = STARTED
            new.setAutoDraw(True)
        
        # if new is active this frame...
        if new.status == STARTED:
            # update params
            new.setColor(new_resp_color, colorSpace='rgb', log=False)
        
        # if new is stopping this frame...
        if new.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > new.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                new.tStop = t  # not accounting for scr refresh
                new.frameNStop = frameN  # exact frame index
                # update status
                new.status = FINISHED
                new.setAutoDraw(False)
        
        # *recall_image* updates
        
        # if recall_image is starting this frame...
        if recall_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            recall_image.frameNStart = frameN  # exact frame index
            recall_image.tStart = t  # local t and not account for scr refresh
            recall_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(recall_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'recall_image.started')
            # update status
            recall_image.status = STARTED
            recall_image.setAutoDraw(True)
        
        # if recall_image is active this frame...
        if recall_image.status == STARTED:
            # update params
            pass
        
        # if recall_image is stopping this frame...
        if recall_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > recall_image.tStartRefresh + cs_duration-frameTolerance:
                # keep track of stop time/frame for later
                recall_image.tStop = t  # not accounting for scr refresh
                recall_image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'recall_image.stopped')
                # update status
                recall_image.status = FINISHED
                recall_image.setAutoDraw(False)
        # Run 'Each Frame' code from cs_code
        #change the color of the response if one is pressed
        if '1' in trials_resp.keys:
            old_resp_color = 'orange'
        elif '2' in trials_resp.keys:
            maybe_old_resp_color = 'orange'
        elif '3' in trials_resp.keys:
            maybe_new_resp_color = 'orange'
        elif '4' in trials_resp.keys:
            new_resp_color = 'orange'
        
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
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
    bps1_trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        bps1_trials.addData('trials_resp.rt', trials_resp.rt)
        bps1_trials.addData('trials_resp.duration', trials_resp.duration)
    # Run 'End Routine' code from cs_code
    #send the event code
    stim_marker('offset',SHOCK=False)
    
    # Store whether a valid response was made
    if trials_resp.keys in ['1', '2','3','4']:
        response_made = True
    else:
        response_made = False
    
    # Log response
    thisExp.addData('response_detected', response_made)
    print(f"[Trial] trials_resp.keys: {trials_resp.keys}, response_made: {response_made}")
    
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_2
    iti_clock = core.Clock()
    
    # Create a timer that runs during ITI
    warning_timer = 0  # Use simple variable instead of core.Clock (safer)
    warning_opacity = 0  # Default = hidden
    
    # If no response was made, prepare to show the warning
    if 'response_made' in globals() and not response_made:
        warning_timer = 3  # Show for 3 seconds
        warning_opacity = 1
    
    
    print(f"[ITI] response_made: {response_made}, warning shown: {warning_opacity == 1}")
    
    warning_text.setOpacity(warning_opacity)
    # keep track of which components have finished
    itiComponents = [old_iti, maybe_old_3, maybe_new_3, new_iti, iti_trial, warning_text]
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
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *old_iti* updates
        
        # if old_iti is starting this frame...
        if old_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            old_iti.frameNStart = frameN  # exact frame index
            old_iti.tStart = t  # local t and not account for scr refresh
            old_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(old_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            old_iti.status = STARTED
            old_iti.setAutoDraw(True)
        
        # if old_iti is active this frame...
        if old_iti.status == STARTED:
            # update params
            pass
        
        # if old_iti is stopping this frame...
        if old_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > old_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                old_iti.tStop = t  # not accounting for scr refresh
                old_iti.frameNStop = frameN  # exact frame index
                # update status
                old_iti.status = FINISHED
                old_iti.setAutoDraw(False)
        
        # *maybe_old_3* updates
        
        # if maybe_old_3 is starting this frame...
        if maybe_old_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_old_3.frameNStart = frameN  # exact frame index
            maybe_old_3.tStart = t  # local t and not account for scr refresh
            maybe_old_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_old_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_old_3.status = STARTED
            maybe_old_3.setAutoDraw(True)
        
        # if maybe_old_3 is active this frame...
        if maybe_old_3.status == STARTED:
            # update params
            pass
        
        # if maybe_old_3 is stopping this frame...
        if maybe_old_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_old_3.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybe_old_3.tStop = t  # not accounting for scr refresh
                maybe_old_3.frameNStop = frameN  # exact frame index
                # update status
                maybe_old_3.status = FINISHED
                maybe_old_3.setAutoDraw(False)
        
        # *maybe_new_3* updates
        
        # if maybe_new_3 is starting this frame...
        if maybe_new_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_new_3.frameNStart = frameN  # exact frame index
            maybe_new_3.tStart = t  # local t and not account for scr refresh
            maybe_new_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_new_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_new_3.status = STARTED
            maybe_new_3.setAutoDraw(True)
        
        # if maybe_new_3 is active this frame...
        if maybe_new_3.status == STARTED:
            # update params
            pass
        
        # if maybe_new_3 is stopping this frame...
        if maybe_new_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_new_3.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybe_new_3.tStop = t  # not accounting for scr refresh
                maybe_new_3.frameNStop = frameN  # exact frame index
                # update status
                maybe_new_3.status = FINISHED
                maybe_new_3.setAutoDraw(False)
        
        # *new_iti* updates
        
        # if new_iti is starting this frame...
        if new_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            new_iti.frameNStart = frameN  # exact frame index
            new_iti.tStart = t  # local t and not account for scr refresh
            new_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(new_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            new_iti.status = STARTED
            new_iti.setAutoDraw(True)
        
        # if new_iti is active this frame...
        if new_iti.status == STARTED:
            # update params
            pass
        
        # if new_iti is stopping this frame...
        if new_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > new_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                new_iti.tStop = t  # not accounting for scr refresh
                new_iti.frameNStop = frameN  # exact frame index
                # update status
                new_iti.status = FINISHED
                new_iti.setAutoDraw(False)
        
        # *iti_trial* updates
        
        # if iti_trial is starting this frame...
        if iti_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_trial.frameNStart = frameN  # exact frame index
            iti_trial.tStart = t  # local t and not account for scr refresh
            iti_trial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_trial, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'iti_trial.started')
            # update status
            iti_trial.status = STARTED
            iti_trial.setAutoDraw(True)
        
        # if iti_trial is active this frame...
        if iti_trial.status == STARTED:
            # update params
            pass
        
        # if iti_trial is stopping this frame...
        if iti_trial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_trial.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_trial.tStop = t  # not accounting for scr refresh
                iti_trial.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'iti_trial.stopped')
                # update status
                iti_trial.status = FINISHED
                iti_trial.setAutoDraw(False)
        # Run 'Each Frame' code from code_2
        # Countdown the warning display timer
        if iti_clock.getTime() >= iti_duration:
            continueRoutine = False
        
        if warning_timer > 0:
            warning_timer -= frameDur  # frameDur is time between frames
            if warning_timer <= 0:
                warning_opacity = 0
        
        # *warning_text* updates
        
        # if warning_text is starting this frame...
        if warning_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            warning_text.frameNStart = frameN  # exact frame index
            warning_text.tStart = t  # local t and not account for scr refresh
            warning_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(warning_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'warning_text.started')
            # update status
            warning_text.status = STARTED
            warning_text.setAutoDraw(True)
        
        # if warning_text is active this frame...
        if warning_text.status == STARTED:
            # update params
            warning_text.setText('Please make a response for each trial', log=False)
        
        # if warning_text is stopping this frame...
        if warning_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > warning_text.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                warning_text.tStop = t  # not accounting for scr refresh
                warning_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'warning_text.stopped')
                # update status
                warning_text.status = FINISHED
                warning_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
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
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'bps1_trials'


# --- Prepare to start Routine "final_iti" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
final_itiComponents = [iti_old2, maybe_old_4, maybe_new_4, iti_new2, iti_final]
for thisComponent in final_itiComponents:
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

# --- Run Routine "final_iti" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 10.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *iti_old2* updates
    
    # if iti_old2 is starting this frame...
    if iti_old2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_old2.frameNStart = frameN  # exact frame index
        iti_old2.tStart = t  # local t and not account for scr refresh
        iti_old2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_old2, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_old2.status = STARTED
        iti_old2.setAutoDraw(True)
    
    # if iti_old2 is active this frame...
    if iti_old2.status == STARTED:
        # update params
        pass
    
    # if iti_old2 is stopping this frame...
    if iti_old2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_old2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_old2.tStop = t  # not accounting for scr refresh
            iti_old2.frameNStop = frameN  # exact frame index
            # update status
            iti_old2.status = FINISHED
            iti_old2.setAutoDraw(False)
    
    # *maybe_old_4* updates
    
    # if maybe_old_4 is starting this frame...
    if maybe_old_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        maybe_old_4.frameNStart = frameN  # exact frame index
        maybe_old_4.tStart = t  # local t and not account for scr refresh
        maybe_old_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(maybe_old_4, 'tStartRefresh')  # time at next scr refresh
        # update status
        maybe_old_4.status = STARTED
        maybe_old_4.setAutoDraw(True)
    
    # if maybe_old_4 is active this frame...
    if maybe_old_4.status == STARTED:
        # update params
        pass
    
    # if maybe_old_4 is stopping this frame...
    if maybe_old_4.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > maybe_old_4.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            maybe_old_4.tStop = t  # not accounting for scr refresh
            maybe_old_4.frameNStop = frameN  # exact frame index
            # update status
            maybe_old_4.status = FINISHED
            maybe_old_4.setAutoDraw(False)
    
    # *maybe_new_4* updates
    
    # if maybe_new_4 is starting this frame...
    if maybe_new_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        maybe_new_4.frameNStart = frameN  # exact frame index
        maybe_new_4.tStart = t  # local t and not account for scr refresh
        maybe_new_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(maybe_new_4, 'tStartRefresh')  # time at next scr refresh
        # update status
        maybe_new_4.status = STARTED
        maybe_new_4.setAutoDraw(True)
    
    # if maybe_new_4 is active this frame...
    if maybe_new_4.status == STARTED:
        # update params
        pass
    
    # if maybe_new_4 is stopping this frame...
    if maybe_new_4.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > maybe_new_4.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            maybe_new_4.tStop = t  # not accounting for scr refresh
            maybe_new_4.frameNStop = frameN  # exact frame index
            # update status
            maybe_new_4.status = FINISHED
            maybe_new_4.setAutoDraw(False)
    
    # *iti_new2* updates
    
    # if iti_new2 is starting this frame...
    if iti_new2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_new2.frameNStart = frameN  # exact frame index
        iti_new2.tStart = t  # local t and not account for scr refresh
        iti_new2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_new2, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_new2.status = STARTED
        iti_new2.setAutoDraw(True)
    
    # if iti_new2 is active this frame...
    if iti_new2.status == STARTED:
        # update params
        pass
    
    # if iti_new2 is stopping this frame...
    if iti_new2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_new2.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_new2.tStop = t  # not accounting for scr refresh
            iti_new2.frameNStop = frameN  # exact frame index
            # update status
            iti_new2.status = FINISHED
            iti_new2.setAutoDraw(False)
    
    # *iti_final* updates
    
    # if iti_final is starting this frame...
    if iti_final.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_final.frameNStart = frameN  # exact frame index
        iti_final.tStart = t  # local t and not account for scr refresh
        iti_final.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_final, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'iti_final.started')
        # update status
        iti_final.status = STARTED
        iti_final.setAutoDraw(True)
    
    # if iti_final is active this frame...
    if iti_final.status == STARTED:
        # update params
        pass
    
    # if iti_final is stopping this frame...
    if iti_final.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_final.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            iti_final.tStop = t  # not accounting for scr refresh
            iti_final.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'iti_final.stopped')
            # update status
            iti_final.status = FINISHED
            iti_final.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in final_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "final_iti" ---
for thisComponent in final_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-10.000000)

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
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_exp_resp* updates
    waitOnFlip = False
    
    # if end_exp_resp is starting this frame...
    if end_exp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_exp_resp.frameNStart = frameN  # exact frame index
        end_exp_resp.tStart = t  # local t and not account for scr refresh
        end_exp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_exp_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        end_exp_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(end_exp_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(end_exp_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if end_exp_resp is stopping this frame...
    if end_exp_resp.status == STARTED:
        if bool((end_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            end_exp_resp.tStop = t  # not accounting for scr refresh
            end_exp_resp.frameNStop = frameN  # exact frame index
            # update status
            end_exp_resp.status = FINISHED
            end_exp_resp.status = FINISHED
    if end_exp_resp.status == STARTED and not waitOnFlip:
        theseKeys = end_exp_resp.getKeys(keyList=['space'], waitRelease=False)
        _end_exp_resp_allKeys.extend(theseKeys)
        if len(_end_exp_resp_allKeys):
            end_exp_resp.keys = _end_exp_resp_allKeys[-1].name  # just the last key pressed
            end_exp_resp.rt = _end_exp_resp_allKeys[-1].rt
            end_exp_resp.duration = _end_exp_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # *end_exp* updates
    
    # if end_exp is starting this frame...
    if end_exp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_exp.frameNStart = frameN  # exact frame index
        end_exp.tStart = t  # local t and not account for scr refresh
        end_exp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_exp, 'tStartRefresh')  # time at next scr refresh
        # update status
        end_exp.status = STARTED
        end_exp.setAutoDraw(True)
    
    # if end_exp is active this frame...
    if end_exp.status == STARTED:
        # update params
        pass
    
    # if end_exp is stopping this frame...
    if end_exp.status == STARTED:
        if bool((end_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            end_exp.tStop = t  # not accounting for scr refresh
            end_exp.frameNStop = frameN  # exact frame index
            # update status
            end_exp.status = FINISHED
            end_exp.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
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
# the Routine "in_end_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# Run 'End Experiment' code from code

thisExp.saveAsWideText(filename + '.csv')


# Now do cleanup AFTER saving
import pandas as pd
filename = f'data/{bidsID}/{bidsID}_ses-2_task-{expName}_{expInfo["date"]}'

try:
    df = pd.read_csv(filename + '.csv')
    cols_to_drop = [
        'recall_trials.thisRepN',
        'recall_trials.thisTrialN',
        'recall_trials.thisN',
        'recall_trials.thisIndex'
    ]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    df.to_csv(filename + '.csv', index=False)

except Exception as e:
    print(f"Failed to clean data file: {e}")


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
