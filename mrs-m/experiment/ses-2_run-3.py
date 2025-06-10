#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on September 13, 2022, at 10:01
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

# Run 'Before Experiment' code from init_code
expName = 'sou_typ_val'  # from the Builder filename that created this script
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-MM')[-1]) for i in os.listdir('data') if 'sub-MM' in i])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-MM{0:0=3d}'.format(int(expInfo['participant']))



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'soutyp'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '001',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-2_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\mrs-m\\experiment\\ses-2_run-3.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
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
inst1 = visual.TextStim(win=win, name='inst1',
    text='Now we would like to ask you some questions about the pictures that you saw on your first visit.\n\nSpecifically, we are going to ask you: \n\nWHEN did you see each picture, and\n\nHow TYPICAL is the picture for its category.\n\nPress SPACE to continue…\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='If you recall, the experiment on your first visit was divided into 3 different phases: \n\nPhase 1 was at the beginning, when you were classifying each picture as either an animal or a tool. \n\nPhase 2 was in the middle, when you received shocks following some of the pictures. \n\nPhase 3 was last, when you received no shocks.\n\n\nPress SPACE to continue… \n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in3" ---
inst3 = visual.TextStim(win=win, name='inst3',
    text='The first question you will answer about each picture is:\n\nWhen did you see this picture? \n\nTo the best of your ability, you will answer: \n\nPhase 1, \nPhase 2, or\nPhase 3 \n\nFor this task, you will respond by clicking the correct dot underneath the photo with your mouse. \nWe will have some practice trials to help orient you to this task. \n\nNote that all of the pictures you will see in this task were shown to you during the experiment on your first visit. \n(There are no “new” pictures.) \n\nIf you have any questions about these instructions, please ask your experimenter. \n\nPress SPACE to continue… \n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst3_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in4" ---
inst4 = visual.TextStim(win=win, name='inst4',
    text='We will now go over the second question that we will ask about each picture: \n\nHow TYPICAL is this picture for its category?\n\nIn other words, you will rate how representative a picture is of the entire category.\n\nFor example, an apple is a typical fruit, as it is very representative of the entire fruit category. On the other hand, a dragonfruit is not a typical fruit, at least in American grocery stores.\n\nPress SPACE to continue…',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in5" ---
inst5 = visual.TextStim(win=win, name='inst5',
    text='You will provide your rating using a scale. \nFor this scale, you can answer:\n\nNot at all typical\nSomewhat typical\nVery typical\n\nAs an example, on this scale an apple would be rated very highly as it is a very typical fruit, and a dragonfruit would be rated very low because it is a very atypical fruit.\n\nRemember that you can click on any of the dots from 1 to 7 on the scale.\n\nPress SPACE to continue…',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst5_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in8" ---
inst8 = visual.TextStim(win=win, name='inst8',
    text='To recap: \n\nYou will see a picture that you saw on your first visit in the middle of the screen. First, you will tell us WHEN you saw this picture: \nPhase 1 (no shocks, categorizing photos), \nPhase 2 (photos and shocks), or \nPhase 3 (photos and no shocks).\n\nYou will then rate how TYPICAL that same picture is for its category, on a scale of \n1 (least typical) to \n7 (most typical). \n\nDo you have any questions about these instructions? If so, please ask your experimenter now.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst8_resp = keyboard.Keyboard()

# --- Initialize components for Routine "prep_practrials" ---
inst_practrials = visual.TextStim(win=win, name='inst_practrials',
    text='We are now going to do a practice trial so you can become familiar with this task. \n\nPress SPACE to begin the practice trial.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst_practrials_resp = keyboard.Keyboard()

# --- Initialize components for Routine "prac_iti" ---
prac_crosshair = visual.ImageStim(
    win=win,
    name='prac_crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "prac_sou" ---
prac_when = visual.TextStim(win=win, name='prac_when',
    text='When did you see this picture?\n(For this example, respond as if this were a picture you saw when you were getting shocked.)',
    font='Open Sans',
    pos=(0, .32), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
pracwhen_image = visual.ImageStim(
    win=win,
    name='pracwhen_image', 
    image='stims/banana.jpg', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
pracsou_slider = visual.Slider(win=win, name='pracsou_slider',
    startValue=None, size=(0.35, 0.05), pos=(0, -0.325), units=None,
    labels=['Phase 1', 'Phase 2', 'Phase 3'], ticks=(1, 2, 3), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-3, readOnly=False)

# --- Initialize components for Routine "sou_feedback" ---
soufeedback_resp = keyboard.Keyboard()
soufeedback_text = visual.TextStim(win=win, name='soufeedback_text',
    text=None,
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "prac_iti" ---
prac_crosshair = visual.ImageStim(
    win=win,
    name='prac_crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "prac_typ" ---
practyp_image = visual.ImageStim(
    win=win,
    name='practyp_image', 
    image='stims/banana.jpg', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
practyp_resp = keyboard.Keyboard()
practyp_question = visual.TextStim(win=win, name='practyp_question',
    text='How typical is this picture?',
    font='Open Sans',
    pos=(0, 0.3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
practyp_slider = visual.Slider(win=win, name='practyp_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Not', 'Somewhat', 'Very'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-4, readOnly=False)

# --- Initialize components for Routine "typ_feedback" ---
typfeedback_text = visual.TextStim(win=win, name='typfeedback_text',
    text=None,
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
typfeedback_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in_begin_experiment" ---
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='Press SPACE to begin the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# --- Initialize components for Routine "big_iti" ---
long_crosshair = visual.ImageStim(
    win=win,
    name='long_crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "sou" ---
sou_resp = keyboard.Keyboard()
sou_pic = visual.ImageStim(
    win=win,
    name='sou_pic', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
sou_question = visual.TextStim(win=win, name='sou_question',
    text='When did you see this picture?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
sou_slider = visual.Slider(win=win, name='sou_slider',
    startValue=None, size=(0.35, 0.05), pos=(0, -0.325), units=None,
    labels=['Phase 1', 'Phase 2', 'Phase 3'], ticks=(1, 2, 3), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-3, readOnly=False)

# --- Initialize components for Routine "iti" ---
crosshair = visual.ImageStim(
    win=win,
    name='crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "typ" ---
typ_resp = keyboard.Keyboard()
typ_pic = visual.ImageStim(
    win=win,
    name='typ_pic', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
typ_question = visual.TextStim(win=win, name='typ_question',
    text='How typical is this picture?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
typ_slider = visual.Slider(win=win, name='typ_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Not', 'Somewhat', 'Very'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-3, readOnly=False)

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
in1Components = [inst1, inst1_resp]
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

# --- Prepare to start Routine "in8" ---
continueRoutine = True
# update component parameters for each repeat
inst8_resp.keys = []
inst8_resp.rt = []
_inst8_resp_allKeys = []
# keep track of which components have finished
in8Components = [inst8, inst8_resp]
for thisComponent in in8Components:
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

# --- Run Routine "in8" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst8* updates
    if inst8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst8.frameNStart = frameN  # exact frame index
        inst8.tStart = t  # local t and not account for scr refresh
        inst8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst8, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst8.started')
        inst8.setAutoDraw(True)
    if inst8.status == STARTED:
        if bool(inst8_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst8.tStop = t  # not accounting for scr refresh
            inst8.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst8.stopped')
            inst8.setAutoDraw(False)
    
    # *inst8_resp* updates
    waitOnFlip = False
    if inst8_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst8_resp.frameNStart = frameN  # exact frame index
        inst8_resp.tStart = t  # local t and not account for scr refresh
        inst8_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst8_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst8_resp.started')
        inst8_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst8_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst8_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst8_resp.status == STARTED:
        if bool(inst8_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst8_resp.tStop = t  # not accounting for scr refresh
            inst8_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst8_resp.stopped')
            inst8_resp.status = FINISHED
    if inst8_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst8_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst8_resp_allKeys.extend(theseKeys)
        if len(_inst8_resp_allKeys):
            inst8_resp.keys = _inst8_resp_allKeys[-1].name  # just the last key pressed
            inst8_resp.rt = _inst8_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in8Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in8" ---
for thisComponent in in8Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst8_resp.keys in ['', [], None]:  # No response was made
    inst8_resp.keys = None
thisExp.addData('inst8_resp.keys',inst8_resp.keys)
if inst8_resp.keys != None:  # we had a response
    thisExp.addData('inst8_resp.rt', inst8_resp.rt)
thisExp.nextEntry()
# the Routine "in8" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "prep_practrials" ---
continueRoutine = True
# update component parameters for each repeat
inst_practrials_resp.keys = []
inst_practrials_resp.rt = []
_inst_practrials_resp_allKeys = []
# keep track of which components have finished
prep_practrialsComponents = [inst_practrials, inst_practrials_resp]
for thisComponent in prep_practrialsComponents:
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

# --- Run Routine "prep_practrials" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst_practrials* updates
    if inst_practrials.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst_practrials.frameNStart = frameN  # exact frame index
        inst_practrials.tStart = t  # local t and not account for scr refresh
        inst_practrials.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst_practrials, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst_practrials.started')
        inst_practrials.setAutoDraw(True)
    if inst_practrials.status == STARTED:
        if bool(inst_practrials_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst_practrials.tStop = t  # not accounting for scr refresh
            inst_practrials.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst_practrials.stopped')
            inst_practrials.setAutoDraw(False)
    
    # *inst_practrials_resp* updates
    waitOnFlip = False
    if inst_practrials_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst_practrials_resp.frameNStart = frameN  # exact frame index
        inst_practrials_resp.tStart = t  # local t and not account for scr refresh
        inst_practrials_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst_practrials_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst_practrials_resp.started')
        inst_practrials_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst_practrials_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst_practrials_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst_practrials_resp.status == STARTED:
        if bool(inst_practrials_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst_practrials_resp.tStop = t  # not accounting for scr refresh
            inst_practrials_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst_practrials_resp.stopped')
            inst_practrials_resp.status = FINISHED
    if inst_practrials_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst_practrials_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst_practrials_resp_allKeys.extend(theseKeys)
        if len(_inst_practrials_resp_allKeys):
            inst_practrials_resp.keys = _inst_practrials_resp_allKeys[-1].name  # just the last key pressed
            inst_practrials_resp.rt = _inst_practrials_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prep_practrialsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prep_practrials" ---
for thisComponent in prep_practrialsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst_practrials_resp.keys in ['', [], None]:  # No response was made
    inst_practrials_resp.keys = None
thisExp.addData('inst_practrials_resp.keys',inst_practrials_resp.keys)
if inst_practrials_resp.keys != None:  # we had a response
    thisExp.addData('inst_practrials_resp.rt', inst_practrials_resp.rt)
thisExp.nextEntry()
# the Routine "prep_practrials" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "prac_iti" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
prac_itiComponents = [prac_crosshair]
for thisComponent in prac_itiComponents:
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

# --- Run Routine "prac_iti" ---
while continueRoutine and routineTimer.getTime() < 1.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *prac_crosshair* updates
    if prac_crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        prac_crosshair.frameNStart = frameN  # exact frame index
        prac_crosshair.tStart = t  # local t and not account for scr refresh
        prac_crosshair.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(prac_crosshair, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'prac_crosshair.started')
        prac_crosshair.setAutoDraw(True)
    if prac_crosshair.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > prac_crosshair.tStartRefresh + 1.0-frameTolerance:
            # keep track of stop time/frame for later
            prac_crosshair.tStop = t  # not accounting for scr refresh
            prac_crosshair.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'prac_crosshair.stopped')
            prac_crosshair.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prac_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_iti" ---
for thisComponent in prac_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine
routineTimer.addTime(-1.000000)

# --- Prepare to start Routine "prac_sou" ---
continueRoutine = True
# update component parameters for each repeat
pracsou_slider.reset()
# keep track of which components have finished
prac_souComponents = [prac_when, pracwhen_image, pracsou_slider]
for thisComponent in prac_souComponents:
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

# --- Run Routine "prac_sou" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *prac_when* updates
    if prac_when.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        prac_when.frameNStart = frameN  # exact frame index
        prac_when.tStart = t  # local t and not account for scr refresh
        prac_when.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(prac_when, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'prac_when.started')
        prac_when.setAutoDraw(True)
    
    # *pracwhen_image* updates
    if pracwhen_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracwhen_image.frameNStart = frameN  # exact frame index
        pracwhen_image.tStart = t  # local t and not account for scr refresh
        pracwhen_image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracwhen_image, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'pracwhen_image.started')
        pracwhen_image.setAutoDraw(True)
    
    # *pracsou_slider* updates
    if pracsou_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracsou_slider.frameNStart = frameN  # exact frame index
        pracsou_slider.tStart = t  # local t and not account for scr refresh
        pracsou_slider.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracsou_slider, 'tStartRefresh')  # time at next scr refresh
        pracsou_slider.setAutoDraw(True)
    
    # Check pracsou_slider for response to end routine
    if pracsou_slider.getRating() is not None and pracsou_slider.status == STARTED:
        continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prac_souComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_sou" ---
for thisComponent in prac_souComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from pracwhen_code
if pracsou_slider.rating in [2]:
    soufeedback_text.text = 'Correct! Phase 2 was when you received shocks.\n\nPress any button to continue...'
elif pracsou_slider.rating in [1]:
        soufeedback_text.text = 'Incorrect. Remember, Phase 1 was when you were classifying animals and tools.\n\nPress any space to continue...'
elif pracsou_slider.rating in [3]:
        soufeedback_text.text = 'Remember, Phase 3 was when you received no shocks.\n\nPress space to continue...'
thisExp.addData('pracsou_slider.response', pracsou_slider.getRating())
thisExp.addData('pracsou_slider.rt', pracsou_slider.getRT())
# the Routine "prac_sou" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "sou_feedback" ---
continueRoutine = True
# update component parameters for each repeat
soufeedback_resp.keys = []
soufeedback_resp.rt = []
_soufeedback_resp_allKeys = []
# keep track of which components have finished
sou_feedbackComponents = [soufeedback_resp, soufeedback_text]
for thisComponent in sou_feedbackComponents:
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

# --- Run Routine "sou_feedback" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *soufeedback_resp* updates
    waitOnFlip = False
    if soufeedback_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        soufeedback_resp.frameNStart = frameN  # exact frame index
        soufeedback_resp.tStart = t  # local t and not account for scr refresh
        soufeedback_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(soufeedback_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'soufeedback_resp.started')
        soufeedback_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(soufeedback_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(soufeedback_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if soufeedback_resp.status == STARTED:
        if bool(soufeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            soufeedback_resp.tStop = t  # not accounting for scr refresh
            soufeedback_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'soufeedback_resp.stopped')
            soufeedback_resp.status = FINISHED
    if soufeedback_resp.status == STARTED and not waitOnFlip:
        theseKeys = soufeedback_resp.getKeys(keyList=['space'], waitRelease=False)
        _soufeedback_resp_allKeys.extend(theseKeys)
        if len(_soufeedback_resp_allKeys):
            soufeedback_resp.keys = _soufeedback_resp_allKeys[-1].name  # just the last key pressed
            soufeedback_resp.rt = _soufeedback_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *soufeedback_text* updates
    if soufeedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        soufeedback_text.frameNStart = frameN  # exact frame index
        soufeedback_text.tStart = t  # local t and not account for scr refresh
        soufeedback_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(soufeedback_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'soufeedback_text.started')
        soufeedback_text.setAutoDraw(True)
    if soufeedback_text.status == STARTED:
        if bool(soufeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            soufeedback_text.tStop = t  # not accounting for scr refresh
            soufeedback_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'soufeedback_text.stopped')
            soufeedback_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in sou_feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "sou_feedback" ---
for thisComponent in sou_feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if soufeedback_resp.keys in ['', [], None]:  # No response was made
    soufeedback_resp.keys = None
thisExp.addData('soufeedback_resp.keys',soufeedback_resp.keys)
if soufeedback_resp.keys != None:  # we had a response
    thisExp.addData('soufeedback_resp.rt', soufeedback_resp.rt)
thisExp.nextEntry()
# the Routine "sou_feedback" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "prac_iti" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
prac_itiComponents = [prac_crosshair]
for thisComponent in prac_itiComponents:
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

# --- Run Routine "prac_iti" ---
while continueRoutine and routineTimer.getTime() < 1.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *prac_crosshair* updates
    if prac_crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        prac_crosshair.frameNStart = frameN  # exact frame index
        prac_crosshair.tStart = t  # local t and not account for scr refresh
        prac_crosshair.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(prac_crosshair, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'prac_crosshair.started')
        prac_crosshair.setAutoDraw(True)
    if prac_crosshair.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > prac_crosshair.tStartRefresh + 1.0-frameTolerance:
            # keep track of stop time/frame for later
            prac_crosshair.tStop = t  # not accounting for scr refresh
            prac_crosshair.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'prac_crosshair.stopped')
            prac_crosshair.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prac_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_iti" ---
for thisComponent in prac_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine
routineTimer.addTime(-1.000000)

# --- Prepare to start Routine "prac_typ" ---
continueRoutine = True
# update component parameters for each repeat
practyp_resp.keys = []
practyp_resp.rt = []
_practyp_resp_allKeys = []
practyp_slider.reset()
# keep track of which components have finished
prac_typComponents = [practyp_image, practyp_resp, practyp_question, practyp_slider]
for thisComponent in prac_typComponents:
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

# --- Run Routine "prac_typ" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *practyp_image* updates
    if practyp_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practyp_image.frameNStart = frameN  # exact frame index
        practyp_image.tStart = t  # local t and not account for scr refresh
        practyp_image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practyp_image, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'practyp_image.started')
        practyp_image.setAutoDraw(True)
    
    # *practyp_resp* updates
    waitOnFlip = False
    if practyp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practyp_resp.frameNStart = frameN  # exact frame index
        practyp_resp.tStart = t  # local t and not account for scr refresh
        practyp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practyp_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'practyp_resp.started')
        practyp_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(practyp_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(practyp_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if practyp_resp.status == STARTED and not waitOnFlip:
        theseKeys = practyp_resp.getKeys(keyList=['1','2','3','4','5','6','7'], waitRelease=False)
        _practyp_resp_allKeys.extend(theseKeys)
        if len(_practyp_resp_allKeys):
            practyp_resp.keys = _practyp_resp_allKeys[-1].name  # just the last key pressed
            practyp_resp.rt = _practyp_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *practyp_question* updates
    if practyp_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practyp_question.frameNStart = frameN  # exact frame index
        practyp_question.tStart = t  # local t and not account for scr refresh
        practyp_question.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practyp_question, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'practyp_question.started')
        practyp_question.setAutoDraw(True)
    
    # *practyp_slider* updates
    if practyp_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practyp_slider.frameNStart = frameN  # exact frame index
        practyp_slider.tStart = t  # local t and not account for scr refresh
        practyp_slider.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practyp_slider, 'tStartRefresh')  # time at next scr refresh
        practyp_slider.setAutoDraw(True)
    
    # Check practyp_slider for response to end routine
    if practyp_slider.getRating() is not None and practyp_slider.status == STARTED:
        continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prac_typComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_typ" ---
for thisComponent in prac_typComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from practyp_code
if practyp_slider.rating in [5, 6, 7]:
    typfeedback_text.text = 'Correct! Bananas are a very typical fruit.\n\nPress any button to continue...'
elif practyp_slider.rating in [1, 2, 3, 4]:
    typfeedback_text.text = 'Incorrect. A fruit that is more typical should be rated more highly on this scale. Because bananas are very typical fruits, they should have been rated more highly.\n\nPress SPACE to continue with practice trial...'

# check responses
if practyp_resp.keys in ['', [], None]:  # No response was made
    practyp_resp.keys = None
thisExp.addData('practyp_resp.keys',practyp_resp.keys)
if practyp_resp.keys != None:  # we had a response
    thisExp.addData('practyp_resp.rt', practyp_resp.rt)
thisExp.nextEntry()
thisExp.addData('practyp_slider.response', practyp_slider.getRating())
thisExp.addData('practyp_slider.rt', practyp_slider.getRT())
# the Routine "prac_typ" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "typ_feedback" ---
continueRoutine = True
# update component parameters for each repeat
typfeedback_resp.keys = []
typfeedback_resp.rt = []
_typfeedback_resp_allKeys = []
# keep track of which components have finished
typ_feedbackComponents = [typfeedback_text, typfeedback_resp]
for thisComponent in typ_feedbackComponents:
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

# --- Run Routine "typ_feedback" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *typfeedback_text* updates
    if typfeedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        typfeedback_text.frameNStart = frameN  # exact frame index
        typfeedback_text.tStart = t  # local t and not account for scr refresh
        typfeedback_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(typfeedback_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'typfeedback_text.started')
        typfeedback_text.setAutoDraw(True)
    if typfeedback_text.status == STARTED:
        if bool(typfeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            typfeedback_text.tStop = t  # not accounting for scr refresh
            typfeedback_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'typfeedback_text.stopped')
            typfeedback_text.setAutoDraw(False)
    
    # *typfeedback_resp* updates
    waitOnFlip = False
    if typfeedback_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        typfeedback_resp.frameNStart = frameN  # exact frame index
        typfeedback_resp.tStart = t  # local t and not account for scr refresh
        typfeedback_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(typfeedback_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'typfeedback_resp.started')
        typfeedback_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(typfeedback_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(typfeedback_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if typfeedback_resp.status == STARTED:
        if bool(typfeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            typfeedback_resp.tStop = t  # not accounting for scr refresh
            typfeedback_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'typfeedback_resp.stopped')
            typfeedback_resp.status = FINISHED
    if typfeedback_resp.status == STARTED and not waitOnFlip:
        theseKeys = typfeedback_resp.getKeys(keyList=['space'], waitRelease=False)
        _typfeedback_resp_allKeys.extend(theseKeys)
        if len(_typfeedback_resp_allKeys):
            typfeedback_resp.keys = _typfeedback_resp_allKeys[-1].name  # just the last key pressed
            typfeedback_resp.rt = _typfeedback_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in typ_feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "typ_feedback" ---
for thisComponent in typ_feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if typfeedback_resp.keys in ['', [], None]:  # No response was made
    typfeedback_resp.keys = None
thisExp.addData('typfeedback_resp.keys',typfeedback_resp.keys)
if typfeedback_resp.keys != None:  # we had a response
    thisExp.addData('typfeedback_resp.rt', typfeedback_resp.rt)
thisExp.nextEntry()
# the Routine "typ_feedback" was not non-slip safe, so reset the non-slip timer
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
trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-2_task-soutyp_events-input.csv'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "big_iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    big_itiComponents = [long_crosshair]
    for thisComponent in big_itiComponents:
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
    
    # --- Run Routine "big_iti" ---
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *long_crosshair* updates
        if long_crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            long_crosshair.frameNStart = frameN  # exact frame index
            long_crosshair.tStart = t  # local t and not account for scr refresh
            long_crosshair.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(long_crosshair, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'long_crosshair.started')
            long_crosshair.setAutoDraw(True)
        if long_crosshair.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > long_crosshair.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                long_crosshair.tStop = t  # not accounting for scr refresh
                long_crosshair.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'long_crosshair.stopped')
                long_crosshair.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in big_itiComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "big_iti" ---
    for thisComponent in big_itiComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-1.000000)
    
    # --- Prepare to start Routine "sou" ---
    continueRoutine = True
    # update component parameters for each repeat
    sou_resp.keys = []
    sou_resp.rt = []
    _sou_resp_allKeys = []
    sou_pic.setImage(stimulus)
    sou_slider.reset()
    # keep track of which components have finished
    souComponents = [sou_resp, sou_pic, sou_question, sou_slider]
    for thisComponent in souComponents:
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
    
    # --- Run Routine "sou" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *sou_resp* updates
        waitOnFlip = False
        if sou_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sou_resp.frameNStart = frameN  # exact frame index
            sou_resp.tStart = t  # local t and not account for scr refresh
            sou_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sou_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sou_resp.started')
            sou_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(sou_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(sou_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if sou_resp.status == STARTED and not waitOnFlip:
            theseKeys = sou_resp.getKeys(keyList=['1','2','3'], waitRelease=False)
            _sou_resp_allKeys.extend(theseKeys)
            if len(_sou_resp_allKeys):
                sou_resp.keys = _sou_resp_allKeys[-1].name  # just the last key pressed
                sou_resp.rt = _sou_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *sou_pic* updates
        if sou_pic.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sou_pic.frameNStart = frameN  # exact frame index
            sou_pic.tStart = t  # local t and not account for scr refresh
            sou_pic.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sou_pic, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sou_pic.started')
            sou_pic.setAutoDraw(True)
        
        # *sou_question* updates
        if sou_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sou_question.frameNStart = frameN  # exact frame index
            sou_question.tStart = t  # local t and not account for scr refresh
            sou_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sou_question, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sou_question.started')
            sou_question.setAutoDraw(True)
        
        # *sou_slider* updates
        if sou_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sou_slider.frameNStart = frameN  # exact frame index
            sou_slider.tStart = t  # local t and not account for scr refresh
            sou_slider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sou_slider, 'tStartRefresh')  # time at next scr refresh
            sou_slider.setAutoDraw(True)
        
        # Check sou_slider for response to end routine
        if sou_slider.getRating() is not None and sou_slider.status == STARTED:
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in souComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "sou" ---
    for thisComponent in souComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if sou_resp.keys in ['', [], None]:  # No response was made
        sou_resp.keys = None
    trials.addData('sou_resp.keys',sou_resp.keys)
    if sou_resp.keys != None:  # we had a response
        trials.addData('sou_resp.rt', sou_resp.rt)
    trials.addData('sou_slider.response', sou_slider.getRating())
    trials.addData('sou_slider.rt', sou_slider.getRT())
    # the Routine "sou" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [crosshair]
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
    while continueRoutine and routineTimer.getTime() < 0.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
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
            if tThisFlipGlobal > crosshair.tStartRefresh + .5-frameTolerance:
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
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-0.500000)
    
    # --- Prepare to start Routine "typ" ---
    continueRoutine = True
    # update component parameters for each repeat
    typ_resp.keys = []
    typ_resp.rt = []
    _typ_resp_allKeys = []
    typ_pic.setImage(stimulus)
    typ_slider.reset()
    # keep track of which components have finished
    typComponents = [typ_resp, typ_pic, typ_question, typ_slider]
    for thisComponent in typComponents:
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
    
    # --- Run Routine "typ" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *typ_resp* updates
        waitOnFlip = False
        if typ_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            typ_resp.frameNStart = frameN  # exact frame index
            typ_resp.tStart = t  # local t and not account for scr refresh
            typ_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(typ_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'typ_resp.started')
            typ_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(typ_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(typ_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if typ_resp.status == STARTED and not waitOnFlip:
            theseKeys = typ_resp.getKeys(keyList=['1','2','3','4','5','6','7'], waitRelease=False)
            _typ_resp_allKeys.extend(theseKeys)
            if len(_typ_resp_allKeys):
                typ_resp.keys = _typ_resp_allKeys[-1].name  # just the last key pressed
                typ_resp.rt = _typ_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *typ_pic* updates
        if typ_pic.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            typ_pic.frameNStart = frameN  # exact frame index
            typ_pic.tStart = t  # local t and not account for scr refresh
            typ_pic.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(typ_pic, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'typ_pic.started')
            typ_pic.setAutoDraw(True)
        
        # *typ_question* updates
        if typ_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            typ_question.frameNStart = frameN  # exact frame index
            typ_question.tStart = t  # local t and not account for scr refresh
            typ_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(typ_question, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'typ_question.started')
            typ_question.setAutoDraw(True)
        
        # *typ_slider* updates
        if typ_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            typ_slider.frameNStart = frameN  # exact frame index
            typ_slider.tStart = t  # local t and not account for scr refresh
            typ_slider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(typ_slider, 'tStartRefresh')  # time at next scr refresh
            typ_slider.setAutoDraw(True)
        
        # Check typ_slider for response to end routine
        if typ_slider.getRating() is not None and typ_slider.status == STARTED:
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in typComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "typ" ---
    for thisComponent in typComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if typ_resp.keys in ['', [], None]:  # No response was made
        typ_resp.keys = None
    trials.addData('typ_resp.keys',typ_resp.keys)
    if typ_resp.keys != None:  # we had a response
        trials.addData('typ_resp.rt', typ_resp.rt)
    trials.addData('typ_slider.response', typ_slider.getRating())
    trials.addData('typ_slider.rt', typ_slider.getRT())
    # the Routine "typ" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'


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
