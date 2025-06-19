#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on Wed Jun 18 13:03:26 2025
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
expName = 'bps1'  # from the Builder filename that created this script
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-PYG')[-1]) for i in os.listdir('data') if 'sub-PYG' in i])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-PYG{0:0=3d}'.format(int(expInfo['participant']))



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'bps3'  # from the Builder filename that created this script
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
    originPath='/Users/sydneylambert/Desktop/pig/mrs-m/experiment/ses-2_run-4_bps3_lastrun.py',
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
iti_question = visual.TextStim(win=win, name='iti_question',
    text='Is this picture OLD or NEW?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
crosshair = visual.ImageStim(
    win=win,
    name='crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
defold_iti = visual.TextStim(win=win, name='defold_iti',
    text='H\nDefinitely old',
    font='Open Sans',
    pos=(-.25,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
maybeold_iti = visual.TextStim(win=win, name='maybeold_iti',
    text='J\nMaybe old',
    font='Open Sans',
    pos=(-.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
maybenew_iti = visual.TextStim(win=win, name='maybenew_iti',
    text='K\nMaybe new',
    font='Open Sans',
    pos=(.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
defnew_iti = visual.TextStim(win=win, name='defnew_iti',
    text='L\nDefinitely new',
    font='Open Sans',
    pos=(.25,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);

# --- Initialize components for Routine "trial" ---
mem_image = visual.ImageStim(
    win=win,
    name='mem_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
mem_question = visual.TextStim(win=win, name='mem_question',
    text='Is this picture OLD or NEW?',
    font='Open Sans',
    pos=(0,.3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
def_old = visual.TextStim(win=win, name='def_old',
    text='H\nDefinitely old',
    font='Open Sans',
    pos=(-.25, -.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
maybe_old = visual.TextStim(win=win, name='maybe_old',
    text='J\nMaybe old',
    font='Open Sans',
    pos=(-.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
maybe_new = visual.TextStim(win=win, name='maybe_new',
    text='K\nMaybe new',
    font='Open Sans',
    pos=(.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
def_new = visual.TextStim(win=win, name='def_new',
    text='L\nDefinitely new',
    font='Open Sans',
    pos=(.25, -.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
mem_resp = keyboard.Keyboard()

# --- Initialize components for Routine "trial_button" ---
stimulus2 = visual.ImageStim(
    win=win,
    name='stimulus2', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
mem_question2 = visual.TextStim(win=win, name='mem_question2',
    text='Is this picture OLD or NEW?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
def_old2 = visual.TextStim(win=win, name='def_old2',
    text='H\nDefinitely old',
    font='Open Sans',
    pos=(-.25, -.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
maybe_old2 = visual.TextStim(win=win, name='maybe_old2',
    text='J\nMaybe old',
    font='Open Sans',
    pos=(-.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
maybe_new2 = visual.TextStim(win=win, name='maybe_new2',
    text='K\nMaybe new',
    font='Open Sans',
    pos=(.08,-.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
def_new2 = visual.TextStim(win=win, name='def_new2',
    text='L\nDefinitely new',
    font='Open Sans',
    pos=(.25, -.325), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
# Run 'Begin Experiment' code from col_code
def_old2_col = 'white'
maybe_old2_col = 'white'
maybe_new2_col = 'white'
def_new2_col = 'white'

# --- Initialize components for Routine "in_end_experiment" ---
end_exp_resp = keyboard.Keyboard()
end_exp = visual.TextStim(win=win, name='end_exp',
    text='Please wait for the experimenter to continue with the task.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

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
        if bool((beg_exp_resp.keys)=='space'):
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
        theseKeys = beg_exp_resp.getKeys(keyList=['space'], waitRelease=False)
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

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-2_task-bps3_events-input.csv'),
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
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [iti_question, crosshair, defold_iti, maybeold_iti, maybenew_iti, defnew_iti]
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
        
        # *iti_question* updates
        
        # if iti_question is starting this frame...
        if iti_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_question.frameNStart = frameN  # exact frame index
            iti_question.tStart = t  # local t and not account for scr refresh
            iti_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_question, 'tStartRefresh')  # time at next scr refresh
            # update status
            iti_question.status = STARTED
            iti_question.setAutoDraw(True)
        
        # if iti_question is active this frame...
        if iti_question.status == STARTED:
            # update params
            pass
        
        # if iti_question is stopping this frame...
        if iti_question.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_question.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_question.tStop = t  # not accounting for scr refresh
                iti_question.frameNStop = frameN  # exact frame index
                # update status
                iti_question.status = FINISHED
                iti_question.setAutoDraw(False)
        
        # *crosshair* updates
        
        # if crosshair is starting this frame...
        if crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            crosshair.frameNStart = frameN  # exact frame index
            crosshair.tStart = t  # local t and not account for scr refresh
            crosshair.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(crosshair, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'crosshair.started')
            # update status
            crosshair.status = STARTED
            crosshair.setAutoDraw(True)
        
        # if crosshair is active this frame...
        if crosshair.status == STARTED:
            # update params
            pass
        
        # if crosshair is stopping this frame...
        if crosshair.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > crosshair.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                crosshair.tStop = t  # not accounting for scr refresh
                crosshair.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'crosshair.stopped')
                # update status
                crosshair.status = FINISHED
                crosshair.setAutoDraw(False)
        
        # *defold_iti* updates
        
        # if defold_iti is starting this frame...
        if defold_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            defold_iti.frameNStart = frameN  # exact frame index
            defold_iti.tStart = t  # local t and not account for scr refresh
            defold_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(defold_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            defold_iti.status = STARTED
            defold_iti.setAutoDraw(True)
        
        # if defold_iti is active this frame...
        if defold_iti.status == STARTED:
            # update params
            pass
        
        # if defold_iti is stopping this frame...
        if defold_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > defold_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                defold_iti.tStop = t  # not accounting for scr refresh
                defold_iti.frameNStop = frameN  # exact frame index
                # update status
                defold_iti.status = FINISHED
                defold_iti.setAutoDraw(False)
        
        # *maybeold_iti* updates
        
        # if maybeold_iti is starting this frame...
        if maybeold_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybeold_iti.frameNStart = frameN  # exact frame index
            maybeold_iti.tStart = t  # local t and not account for scr refresh
            maybeold_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybeold_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybeold_iti.status = STARTED
            maybeold_iti.setAutoDraw(True)
        
        # if maybeold_iti is active this frame...
        if maybeold_iti.status == STARTED:
            # update params
            pass
        
        # if maybeold_iti is stopping this frame...
        if maybeold_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybeold_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybeold_iti.tStop = t  # not accounting for scr refresh
                maybeold_iti.frameNStop = frameN  # exact frame index
                # update status
                maybeold_iti.status = FINISHED
                maybeold_iti.setAutoDraw(False)
        
        # *maybenew_iti* updates
        
        # if maybenew_iti is starting this frame...
        if maybenew_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybenew_iti.frameNStart = frameN  # exact frame index
            maybenew_iti.tStart = t  # local t and not account for scr refresh
            maybenew_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybenew_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybenew_iti.status = STARTED
            maybenew_iti.setAutoDraw(True)
        
        # if maybenew_iti is active this frame...
        if maybenew_iti.status == STARTED:
            # update params
            pass
        
        # if maybenew_iti is stopping this frame...
        if maybenew_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybenew_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                maybenew_iti.tStop = t  # not accounting for scr refresh
                maybenew_iti.frameNStop = frameN  # exact frame index
                # update status
                maybenew_iti.status = FINISHED
                maybenew_iti.setAutoDraw(False)
        
        # *defnew_iti* updates
        
        # if defnew_iti is starting this frame...
        if defnew_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            defnew_iti.frameNStart = frameN  # exact frame index
            defnew_iti.tStart = t  # local t and not account for scr refresh
            defnew_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(defnew_iti, 'tStartRefresh')  # time at next scr refresh
            # update status
            defnew_iti.status = STARTED
            defnew_iti.setAutoDraw(True)
        
        # if defnew_iti is active this frame...
        if defnew_iti.status == STARTED:
            # update params
            pass
        
        # if defnew_iti is stopping this frame...
        if defnew_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > defnew_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                defnew_iti.tStop = t  # not accounting for scr refresh
                defnew_iti.frameNStop = frameN  # exact frame index
                # update status
                defnew_iti.status = FINISHED
                defnew_iti.setAutoDraw(False)
        
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
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    mem_image.setImage(stim)
    mem_resp.keys = []
    mem_resp.rt = []
    _mem_resp_allKeys = []
    # keep track of which components have finished
    trialComponents = [mem_image, mem_question, def_old, maybe_old, maybe_new, def_new, mem_resp]
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
        
        # *mem_image* updates
        
        # if mem_image is starting this frame...
        if mem_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mem_image.frameNStart = frameN  # exact frame index
            mem_image.tStart = t  # local t and not account for scr refresh
            mem_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mem_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'mem_image.started')
            # update status
            mem_image.status = STARTED
            mem_image.setAutoDraw(True)
        
        # if mem_image is active this frame...
        if mem_image.status == STARTED:
            # update params
            pass
        
        # *mem_question* updates
        
        # if mem_question is starting this frame...
        if mem_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mem_question.frameNStart = frameN  # exact frame index
            mem_question.tStart = t  # local t and not account for scr refresh
            mem_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mem_question, 'tStartRefresh')  # time at next scr refresh
            # update status
            mem_question.status = STARTED
            mem_question.setAutoDraw(True)
        
        # if mem_question is active this frame...
        if mem_question.status == STARTED:
            # update params
            pass
        
        # *def_old* updates
        
        # if def_old is starting this frame...
        if def_old.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            def_old.frameNStart = frameN  # exact frame index
            def_old.tStart = t  # local t and not account for scr refresh
            def_old.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(def_old, 'tStartRefresh')  # time at next scr refresh
            # update status
            def_old.status = STARTED
            def_old.setAutoDraw(True)
        
        # if def_old is active this frame...
        if def_old.status == STARTED:
            # update params
            def_old.setColor('white', colorSpace='rgb', log=False)
        
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
            pass
        
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
            pass
        
        # *def_new* updates
        
        # if def_new is starting this frame...
        if def_new.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            def_new.frameNStart = frameN  # exact frame index
            def_new.tStart = t  # local t and not account for scr refresh
            def_new.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(def_new, 'tStartRefresh')  # time at next scr refresh
            # update status
            def_new.status = STARTED
            def_new.setAutoDraw(True)
        
        # if def_new is active this frame...
        if def_new.status == STARTED:
            # update params
            pass
        
        # *mem_resp* updates
        waitOnFlip = False
        
        # if mem_resp is starting this frame...
        if mem_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mem_resp.frameNStart = frameN  # exact frame index
            mem_resp.tStart = t  # local t and not account for scr refresh
            mem_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mem_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'mem_resp.started')
            # update status
            mem_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(mem_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(mem_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if mem_resp.status == STARTED and not waitOnFlip:
            theseKeys = mem_resp.getKeys(keyList=['h', 'j', 'k', 'l'], waitRelease=False)
            _mem_resp_allKeys.extend(theseKeys)
            if len(_mem_resp_allKeys):
                mem_resp.keys = _mem_resp_allKeys[0].name  # just the first key pressed
                mem_resp.rt = _mem_resp_allKeys[0].rt
                mem_resp.duration = _mem_resp_allKeys[0].duration
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
    if mem_resp.keys in ['', [], None]:  # No response was made
        mem_resp.keys = None
    trials.addData('mem_resp.keys',mem_resp.keys)
    if mem_resp.keys != None:  # we had a response
        trials.addData('mem_resp.rt', mem_resp.rt)
        trials.addData('mem_resp.duration', mem_resp.duration)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "trial_button" ---
    continueRoutine = True
    # update component parameters for each repeat
    stimulus2.setImage(stim)
    # Run 'Begin Routine' code from col_code
    def_old2_col = 'white'
    maybe_old2_col = 'white'
    maybe_new2_col = 'white'
    def_new2_col = 'white'
    # keep track of which components have finished
    trial_buttonComponents = [stimulus2, mem_question2, def_old2, maybe_old2, maybe_new2, def_new2]
    for thisComponent in trial_buttonComponents:
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
    
    # --- Run Routine "trial_button" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 0.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *stimulus2* updates
        
        # if stimulus2 is starting this frame...
        if stimulus2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stimulus2.frameNStart = frameN  # exact frame index
            stimulus2.tStart = t  # local t and not account for scr refresh
            stimulus2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stimulus2, 'tStartRefresh')  # time at next scr refresh
            # update status
            stimulus2.status = STARTED
            stimulus2.setAutoDraw(True)
        
        # if stimulus2 is active this frame...
        if stimulus2.status == STARTED:
            # update params
            pass
        
        # if stimulus2 is stopping this frame...
        if stimulus2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stimulus2.tStartRefresh + .5-frameTolerance:
                # keep track of stop time/frame for later
                stimulus2.tStop = t  # not accounting for scr refresh
                stimulus2.frameNStop = frameN  # exact frame index
                # update status
                stimulus2.status = FINISHED
                stimulus2.setAutoDraw(False)
        
        # *mem_question2* updates
        
        # if mem_question2 is starting this frame...
        if mem_question2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mem_question2.frameNStart = frameN  # exact frame index
            mem_question2.tStart = t  # local t and not account for scr refresh
            mem_question2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mem_question2, 'tStartRefresh')  # time at next scr refresh
            # update status
            mem_question2.status = STARTED
            mem_question2.setAutoDraw(True)
        
        # if mem_question2 is active this frame...
        if mem_question2.status == STARTED:
            # update params
            pass
        
        # if mem_question2 is stopping this frame...
        if mem_question2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mem_question2.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                mem_question2.tStop = t  # not accounting for scr refresh
                mem_question2.frameNStop = frameN  # exact frame index
                # update status
                mem_question2.status = FINISHED
                mem_question2.setAutoDraw(False)
        
        # *def_old2* updates
        
        # if def_old2 is starting this frame...
        if def_old2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            def_old2.frameNStart = frameN  # exact frame index
            def_old2.tStart = t  # local t and not account for scr refresh
            def_old2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(def_old2, 'tStartRefresh')  # time at next scr refresh
            # update status
            def_old2.status = STARTED
            def_old2.setAutoDraw(True)
        
        # if def_old2 is active this frame...
        if def_old2.status == STARTED:
            # update params
            def_old2.setColor(def_old2_col, colorSpace='rgb', log=False)
        
        # if def_old2 is stopping this frame...
        if def_old2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > def_old2.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                def_old2.tStop = t  # not accounting for scr refresh
                def_old2.frameNStop = frameN  # exact frame index
                # update status
                def_old2.status = FINISHED
                def_old2.setAutoDraw(False)
        
        # *maybe_old2* updates
        
        # if maybe_old2 is starting this frame...
        if maybe_old2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_old2.frameNStart = frameN  # exact frame index
            maybe_old2.tStart = t  # local t and not account for scr refresh
            maybe_old2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_old2, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_old2.status = STARTED
            maybe_old2.setAutoDraw(True)
        
        # if maybe_old2 is active this frame...
        if maybe_old2.status == STARTED:
            # update params
            maybe_old2.setColor(maybe_old2_col, colorSpace='rgb', log=False)
        
        # if maybe_old2 is stopping this frame...
        if maybe_old2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_old2.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                maybe_old2.tStop = t  # not accounting for scr refresh
                maybe_old2.frameNStop = frameN  # exact frame index
                # update status
                maybe_old2.status = FINISHED
                maybe_old2.setAutoDraw(False)
        
        # *maybe_new2* updates
        
        # if maybe_new2 is starting this frame...
        if maybe_new2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            maybe_new2.frameNStart = frameN  # exact frame index
            maybe_new2.tStart = t  # local t and not account for scr refresh
            maybe_new2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(maybe_new2, 'tStartRefresh')  # time at next scr refresh
            # update status
            maybe_new2.status = STARTED
            maybe_new2.setAutoDraw(True)
        
        # if maybe_new2 is active this frame...
        if maybe_new2.status == STARTED:
            # update params
            maybe_new2.setColor(maybe_new2_col, colorSpace='rgb', log=False)
        
        # if maybe_new2 is stopping this frame...
        if maybe_new2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > maybe_new2.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                maybe_new2.tStop = t  # not accounting for scr refresh
                maybe_new2.frameNStop = frameN  # exact frame index
                # update status
                maybe_new2.status = FINISHED
                maybe_new2.setAutoDraw(False)
        
        # *def_new2* updates
        
        # if def_new2 is starting this frame...
        if def_new2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            def_new2.frameNStart = frameN  # exact frame index
            def_new2.tStart = t  # local t and not account for scr refresh
            def_new2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(def_new2, 'tStartRefresh')  # time at next scr refresh
            # update status
            def_new2.status = STARTED
            def_new2.setAutoDraw(True)
        
        # if def_new2 is active this frame...
        if def_new2.status == STARTED:
            # update params
            def_new2.setColor(def_new2_col, colorSpace='rgb', log=False)
        
        # if def_new2 is stopping this frame...
        if def_new2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > def_new2.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                def_new2.tStop = t  # not accounting for scr refresh
                def_new2.frameNStop = frameN  # exact frame index
                # update status
                def_new2.status = FINISHED
                def_new2.setAutoDraw(False)
        # Run 'Each Frame' code from col_code
        if 'h' in mem_resp.keys: 
            def_old2_col = 'darkgray'
            maybe_old2_col = 'white'
            maybe_new2_col = 'white'
            def_new2_col = 'white'
        elif 'j' in mem_resp.keys:
            def_old2_col = 'white'
            maybe_old2_col = 'darkgray'
            maybe_new2_col = 'white'
            def_new2_col = 'white'
        elif 'k' in mem_resp.keys:
            def_old2_col = 'white'
            maybe_old2_col = 'white'
            maybe_new2_col = 'darkgray'
            def_new2_col = 'white'
        elif 'l' in mem_resp.keys:
            def_old2_col = 'white'
            maybe_old2_col = 'white'
            maybe_new2_col = 'white'
            def_new2_col = 'darkgray'
        
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
        for thisComponent in trial_buttonComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial_button" ---
    for thisComponent in trial_buttonComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.500000)
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

# Clean up the file
import pandas as pd
import os

filename = f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

try:
    df = pd.read_csv(filename + '.csv')
    
    cols_to_drop = [
        'bps3_trials.thisRepN',
        'bps3_trials.thisTrialN',
        'bps3_trials.thisN',
        'bps3_trials.thisIndex'
    ]
    
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    #  Overwrite the original file with the cleaned version
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
