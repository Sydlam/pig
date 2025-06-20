#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on Wed Jun 18 10:33:05 2025
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
dlg.addField('room', choices =['VR', 'behavior']) #added 6/16
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
# Run 'Before Experiment' code from col_code




# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'ext'  # from the Builder filename that created this script
expInfo = {
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
    originPath='/Users/sydneylambert/Desktop/pig/mrs-m/experiment/ses-1_run-3 copy_lastrun.py',
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
    text='Press SPACE to continue the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# --- Initialize components for Routine "iti" ---
iti_animals = visual.TextStim(win=win, name='iti_animals',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
iti_tools = visual.TextStim(win=win, name='iti_tools',
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
recall_image = visual.ImageStim(
    win=win,
    name='recall_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "iti" ---
iti_animals = visual.TextStim(win=win, name='iti_animals',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
iti_tools = visual.TextStim(win=win, name='iti_tools',
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
recall_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-2_task-recall_events-input.csv'),
    seed=None, name='recall_trials')
thisExp.addLoop(recall_trials)  # add the loop to the experiment
thisRecall_trial = recall_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisRecall_trial.rgb)
if thisRecall_trial != None:
    for paramName in thisRecall_trial:
        exec('{} = thisRecall_trial[paramName]'.format(paramName))

for thisRecall_trial in recall_trials:
    currentLoop = recall_trials
    # abbreviate parameter names if possible (e.g. rgb = thisRecall_trial.rgb)
    if thisRecall_trial != None:
        for paramName in thisRecall_trial:
            exec('{} = thisRecall_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [iti_animals, iti_tools, crosshair]
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
        
        # *iti_animals* updates
        
        # if iti_animals is starting this frame...
        if iti_animals.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_animals.frameNStart = frameN  # exact frame index
            iti_animals.tStart = t  # local t and not account for scr refresh
            iti_animals.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_animals, 'tStartRefresh')  # time at next scr refresh
            # update status
            iti_animals.status = STARTED
            iti_animals.setAutoDraw(True)
        
        # if iti_animals is active this frame...
        if iti_animals.status == STARTED:
            # update params
            pass
        
        # if iti_animals is stopping this frame...
        if iti_animals.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_animals.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_animals.tStop = t  # not accounting for scr refresh
                iti_animals.frameNStop = frameN  # exact frame index
                # update status
                iti_animals.status = FINISHED
                iti_animals.setAutoDraw(False)
        
        # *iti_tools* updates
        
        # if iti_tools is starting this frame...
        if iti_tools.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_tools.frameNStart = frameN  # exact frame index
            iti_tools.tStart = t  # local t and not account for scr refresh
            iti_tools.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_tools, 'tStartRefresh')  # time at next scr refresh
            # update status
            iti_tools.status = STARTED
            iti_tools.setAutoDraw(True)
        
        # if iti_tools is active this frame...
        if iti_tools.status == STARTED:
            # update params
            pass
        
        # if iti_tools is stopping this frame...
        if iti_tools.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_tools.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_tools.tStop = t  # not accounting for scr refresh
                iti_tools.frameNStop = frameN  # exact frame index
                # update status
                iti_tools.status = FINISHED
                iti_tools.setAutoDraw(False)
        
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
    trials_resp.keys = []
    trials_resp.rt = []
    _trials_resp_allKeys = []
    recall_image.setImage(stim)
    # Run 'Begin Routine' code from col_code
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set the response colors to white
    animal_resp_color = 'white'
    tool_resp_color = 'white'
    
    # keep track of which components have finished
    trialComponents = [trials_resp, animal, tool, recall_image]
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
    while continueRoutine and routineTimer.getTime() < 5.0:
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
            if tThisFlipGlobal > trials_resp.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                trials_resp.tStop = t  # not accounting for scr refresh
                trials_resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trials_resp.stopped')
                # update status
                trials_resp.status = FINISHED
                trials_resp.status = FINISHED
        if trials_resp.status == STARTED and not waitOnFlip:
            theseKeys = trials_resp.getKeys(keyList=['num_1','num_2','1','2'], waitRelease=False)
            _trials_resp_allKeys.extend(theseKeys)
            if len(_trials_resp_allKeys):
                trials_resp.keys = _trials_resp_allKeys[0].name  # just the first key pressed
                trials_resp.rt = _trials_resp_allKeys[0].rt
                trials_resp.duration = _trials_resp_allKeys[0].duration
        
        # *animal* updates
        
        # if animal is starting this frame...
        if animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            animal.frameNStart = frameN  # exact frame index
            animal.tStart = t  # local t and not account for scr refresh
            animal.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(animal, 'tStartRefresh')  # time at next scr refresh
            # update status
            animal.status = STARTED
            animal.setAutoDraw(True)
        
        # if animal is active this frame...
        if animal.status == STARTED:
            # update params
            animal.setColor(animal_resp_color, colorSpace='rgb', log=False)
        
        # if animal is stopping this frame...
        if animal.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > animal.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                animal.tStop = t  # not accounting for scr refresh
                animal.frameNStop = frameN  # exact frame index
                # update status
                animal.status = FINISHED
                animal.setAutoDraw(False)
        
        # *tool* updates
        
        # if tool is starting this frame...
        if tool.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            tool.frameNStart = frameN  # exact frame index
            tool.tStart = t  # local t and not account for scr refresh
            tool.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(tool, 'tStartRefresh')  # time at next scr refresh
            # update status
            tool.status = STARTED
            tool.setAutoDraw(True)
        
        # if tool is active this frame...
        if tool.status == STARTED:
            # update params
            tool.setColor(tool_resp_color, colorSpace='rgb', log=False)
        
        # if tool is stopping this frame...
        if tool.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > tool.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                tool.tStop = t  # not accounting for scr refresh
                tool.frameNStop = frameN  # exact frame index
                # update status
                tool.status = FINISHED
                tool.setAutoDraw(False)
        
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
            if tThisFlipGlobal > recall_image.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                recall_image.tStop = t  # not accounting for scr refresh
                recall_image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'recall_image.stopped')
                # update status
                recall_image.status = FINISHED
                recall_image.setAutoDraw(False)
        # Run 'Each Frame' code from col_code
        #change the color of the response if one is pressed
        if '1' in trials_resp.keys:
            animal_resp_color = 'darkgrey'
        elif '2' in trials_resp.keys:
            tool_resp_color = 'darkgrey'
        
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
    recall_trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        recall_trials.addData('trials_resp.rt', trials_resp.rt)
        recall_trials.addData('trials_resp.duration', trials_resp.duration)
    # Run 'End Routine' code from col_code
    #send the event code
    stim_marker('offset',SHOCK=False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'recall_trials'


# --- Prepare to start Routine "iti" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
itiComponents = [iti_animals, iti_tools, crosshair]
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
    
    # *iti_animals* updates
    
    # if iti_animals is starting this frame...
    if iti_animals.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_animals.frameNStart = frameN  # exact frame index
        iti_animals.tStart = t  # local t and not account for scr refresh
        iti_animals.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_animals, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_animals.status = STARTED
        iti_animals.setAutoDraw(True)
    
    # if iti_animals is active this frame...
    if iti_animals.status == STARTED:
        # update params
        pass
    
    # if iti_animals is stopping this frame...
    if iti_animals.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_animals.tStartRefresh + iti_duration-frameTolerance:
            # keep track of stop time/frame for later
            iti_animals.tStop = t  # not accounting for scr refresh
            iti_animals.frameNStop = frameN  # exact frame index
            # update status
            iti_animals.status = FINISHED
            iti_animals.setAutoDraw(False)
    
    # *iti_tools* updates
    
    # if iti_tools is starting this frame...
    if iti_tools.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        iti_tools.frameNStart = frameN  # exact frame index
        iti_tools.tStart = t  # local t and not account for scr refresh
        iti_tools.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(iti_tools, 'tStartRefresh')  # time at next scr refresh
        # update status
        iti_tools.status = STARTED
        iti_tools.setAutoDraw(True)
    
    # if iti_tools is active this frame...
    if iti_tools.status == STARTED:
        # update params
        pass
    
    # if iti_tools is stopping this frame...
    if iti_tools.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > iti_tools.tStartRefresh + iti_duration-frameTolerance:
            # keep track of stop time/frame for later
            iti_tools.tStop = t  # not accounting for scr refresh
            iti_tools.frameNStop = frameN  # exact frame index
            # update status
            iti_tools.status = FINISHED
            iti_tools.setAutoDraw(False)
    
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

# Now do cleanup AFTER saving
import pandas as pd
filename = f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

try:
    df = pd.read_csv(filename + '.csv')
    cols_to_drop = [
        'ext_trials.thisRepN',
        'ext_trials.thisTrialN',
        'ext_trials.thisN',
        'ext_trials.thisIndex'
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
