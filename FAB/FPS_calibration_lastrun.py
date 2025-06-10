#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on May 30, 2025, at 12:45
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



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'FPS_calibration'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/calibration/FPS/{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\Experiments\\FAB\\FPS_calibration_lastrun.py',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
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

# --- Initialize components for Routine "inst0_FPS" ---
inst0 = visual.TextStim(win=win, name='inst0',
    text='You will be hearing loud static noises through the headphones. These loud noises are brief and similar in volume to things you come across in your daily life, like a car honking its horn or an airplane flying over head. ',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst0_response = keyboard.Keyboard()

# --- Initialize components for Routine "inst1_FPS" ---
inst1 = visual.TextStim(win=win, name='inst1',
    text='You will hear 3 bursts of white noise. \nAll you need to do is listen to the noises, nothing else. \n\nDo you have any questions?\n\n\n\n',
    font='Open Sans',
    pos=(0, -0.1), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_response = keyboard.Keyboard()

# --- Initialize components for Routine "getready" ---
inst_final = visual.TextStim(win=win, name='inst_final',
    text='Are you ready?\n\nPress spacebar to START...\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
final_response = keyboard.Keyboard()

# --- Initialize components for Routine "cross_2" ---
cross_3 = visual.ShapeStim(
    win=win, name='cross_3', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "FPS_sound" ---
cross = visual.ShapeStim(
    win=win, name='cross', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "iti" ---
cross_iti = visual.ShapeStim(
    win=win, name='cross_iti', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "inst0_FPS" ---
continueRoutine = True
# update component parameters for each repeat
inst0_response.keys = []
inst0_response.rt = []
_inst0_response_allKeys = []
# keep track of which components have finished
inst0_FPSComponents = [inst0, inst0_response]
for thisComponent in inst0_FPSComponents:
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

# --- Run Routine "inst0_FPS" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst0* updates
    if inst0.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        inst0.frameNStart = frameN  # exact frame index
        inst0.tStart = t  # local t and not account for scr refresh
        inst0.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst0, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst0.started')
        inst0.setAutoDraw(True)
    
    # *inst0_response* updates
    waitOnFlip = False
    if inst0_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst0_response.frameNStart = frameN  # exact frame index
        inst0_response.tStart = t  # local t and not account for scr refresh
        inst0_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst0_response, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst0_response.started')
        inst0_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst0_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst0_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst0_response.status == STARTED and not waitOnFlip:
        theseKeys = inst0_response.getKeys(keyList=['space'], waitRelease=False)
        _inst0_response_allKeys.extend(theseKeys)
        if len(_inst0_response_allKeys):
            inst0_response.keys = _inst0_response_allKeys[-1].name  # just the last key pressed
            inst0_response.rt = _inst0_response_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in inst0_FPSComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "inst0_FPS" ---
for thisComponent in inst0_FPSComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst0_response.keys in ['', [], None]:  # No response was made
    inst0_response.keys = None
thisExp.addData('inst0_response.keys',inst0_response.keys)
if inst0_response.keys != None:  # we had a response
    thisExp.addData('inst0_response.rt', inst0_response.rt)
thisExp.nextEntry()
# the Routine "inst0_FPS" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "inst1_FPS" ---
continueRoutine = True
# update component parameters for each repeat
inst1_response.keys = []
inst1_response.rt = []
_inst1_response_allKeys = []
# keep track of which components have finished
inst1_FPSComponents = [inst1, inst1_response]
for thisComponent in inst1_FPSComponents:
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

# --- Run Routine "inst1_FPS" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst1* updates
    if inst1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        inst1.frameNStart = frameN  # exact frame index
        inst1.tStart = t  # local t and not account for scr refresh
        inst1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1.started')
        inst1.setAutoDraw(True)
    
    # *inst1_response* updates
    waitOnFlip = False
    if inst1_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst1_response.frameNStart = frameN  # exact frame index
        inst1_response.tStart = t  # local t and not account for scr refresh
        inst1_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1_response, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1_response.started')
        inst1_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst1_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst1_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst1_response.status == STARTED and not waitOnFlip:
        theseKeys = inst1_response.getKeys(keyList=['space'], waitRelease=False)
        _inst1_response_allKeys.extend(theseKeys)
        if len(_inst1_response_allKeys):
            inst1_response.keys = _inst1_response_allKeys[-1].name  # just the last key pressed
            inst1_response.rt = _inst1_response_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in inst1_FPSComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "inst1_FPS" ---
for thisComponent in inst1_FPSComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst1_response.keys in ['', [], None]:  # No response was made
    inst1_response.keys = None
thisExp.addData('inst1_response.keys',inst1_response.keys)
if inst1_response.keys != None:  # we had a response
    thisExp.addData('inst1_response.rt', inst1_response.rt)
thisExp.nextEntry()
# the Routine "inst1_FPS" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "getready" ---
continueRoutine = True
# update component parameters for each repeat
final_response.keys = []
final_response.rt = []
_final_response_allKeys = []
# keep track of which components have finished
getreadyComponents = [inst_final, final_response]
for thisComponent in getreadyComponents:
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

# --- Run Routine "getready" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst_final* updates
    if inst_final.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        inst_final.frameNStart = frameN  # exact frame index
        inst_final.tStart = t  # local t and not account for scr refresh
        inst_final.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst_final, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst_final.started')
        inst_final.setAutoDraw(True)
    
    # *final_response* updates
    waitOnFlip = False
    if final_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        final_response.frameNStart = frameN  # exact frame index
        final_response.tStart = t  # local t and not account for scr refresh
        final_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(final_response, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'final_response.started')
        final_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(final_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(final_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if final_response.status == STARTED and not waitOnFlip:
        theseKeys = final_response.getKeys(keyList=['space'], waitRelease=False)
        _final_response_allKeys.extend(theseKeys)
        if len(_final_response_allKeys):
            final_response.keys = _final_response_allKeys[-1].name  # just the last key pressed
            final_response.rt = _final_response_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in getreadyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "getready" ---
for thisComponent in getreadyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if final_response.keys in ['', [], None]:  # No response was made
    final_response.keys = None
thisExp.addData('final_response.keys',final_response.keys)
if final_response.keys != None:  # we had a response
    thisExp.addData('final_response.rt', final_response.rt)
thisExp.nextEntry()
# the Routine "getready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "cross_2" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
cross_2Components = [cross_3]
for thisComponent in cross_2Components:
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

# --- Run Routine "cross_2" ---
while continueRoutine and routineTimer.getTime() < 3.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *cross_3* updates
    if cross_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        cross_3.frameNStart = frameN  # exact frame index
        cross_3.tStart = t  # local t and not account for scr refresh
        cross_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cross_3, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'cross_3.started')
        cross_3.setAutoDraw(True)
    if cross_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross_3.tStartRefresh + 3-frameTolerance:
            # keep track of stop time/frame for later
            cross_3.tStop = t  # not accounting for scr refresh
            cross_3.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_3.stopped')
            cross_3.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in cross_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "cross_2" ---
for thisComponent in cross_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine
routineTimer.addTime(-3.000000)

# set up handler to look after randomisation of conditions etc
FPS_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/fps_order.xlsx'),
    seed=None, name='FPS_trials')
thisExp.addLoop(FPS_trials)  # add the loop to the experiment
thisFPS_trial = FPS_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisFPS_trial.rgb)
if thisFPS_trial != None:
    for paramName in thisFPS_trial:
        exec('{} = thisFPS_trial[paramName]'.format(paramName))

for thisFPS_trial in FPS_trials:
    currentLoop = FPS_trials
    # abbreviate parameter names if possible (e.g. rgb = thisFPS_trial.rgb)
    if thisFPS_trial != None:
        for paramName in thisFPS_trial:
            exec('{} = thisFPS_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "FPS_sound" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from FPS
    flag = 0
    mySound = sound.Sound('stimuli/calibrationprobe1.wav', stereo=True, hamming=False, name='mySound')
    mySound.play()
    
    
    # keep track of which components have finished
    FPS_soundComponents = [cross]
    for thisComponent in FPS_soundComponents:
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
    
    # --- Run Routine "FPS_sound" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *cross* updates
        if cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross.frameNStart = frameN  # exact frame index
            cross.tStart = t  # local t and not account for scr refresh
            cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross.started')
            cross.setAutoDraw(True)
        if cross.status == STARTED:
            if bool(flag == 0):
                # keep track of stop time/frame for later
                cross.tStop = t  # not accounting for scr refresh
                cross.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cross.stopped')
                cross.setAutoDraw(False)
        # Run 'Each Frame' code from FPS
        
        
        
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FPS_soundComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "FPS_sound" ---
    for thisComponent in FPS_soundComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from FPS
    flag = 1
    # the Routine "FPS_sound" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [cross_iti]
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
        
        # *cross_iti* updates
        if cross_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross_iti.frameNStart = frameN  # exact frame index
            cross_iti.tStart = t  # local t and not account for scr refresh
            cross_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross_iti, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_iti.started')
            cross_iti.setAutoDraw(True)
        if cross_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cross_iti.tStartRefresh + iti-frameTolerance:
                # keep track of stop time/frame for later
                cross_iti.tStop = t  # not accounting for scr refresh
                cross_iti.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cross_iti.stopped')
                cross_iti.setAutoDraw(False)
        
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
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'FPS_trials'


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
