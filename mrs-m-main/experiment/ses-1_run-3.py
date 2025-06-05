#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on Fri Jun 17 17:03:50 2022
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

from psychopy.parallel import ParallelPort
from subprocess import Popen
import time

expName = 'extinction-cc'  # from the Builder filename that created this script
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
psychopyVersion = '2021.2.3'
expName = 'extinction-cc'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/sab5394/Desktop/mrs-m/experiment/ses-1_run-3.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=False, screen=0, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "in_begin_experiment"
in_begin_experimentClock = core.Clock()
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='Press SPACE to continue the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# Initialize components for Routine "iti"
itiClock = core.Clock()
fix_cross = visual.ShapeStim(
    win=win, name='fix_cross', vertices='cross',
    size=(0.03, 0.03),
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
iti_animals = visual.TextStim(win=win, name='iti_animals',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
iti_tools = visual.TextStim(win=win, name='iti_tools',
    text='2\nNo',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "trial"
trialClock = core.Clock()
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
ext_image = visual.ImageStim(
    win=win,
    name='ext_image', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# Initialize components for Routine "cc"
ccClock = core.Clock()
cc_image = visual.ImageStim(
    win=win,
    name='cc_image', 
    image='sin', mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
cc_yes = visual.TextStim(win=win, name='cc_yes',
    text='1\nYes',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
cc_no = visual.TextStim(win=win, name='cc_no',
    text='2\nNo',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "in_end_experiment"
in_end_experimentClock = core.Clock()
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
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "in_begin_experiment"-------
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
in_begin_experimentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in_begin_experiment"-------
while continueRoutine:
    # get current time
    t = in_begin_experimentClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in_begin_experimentClock)
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
        beg_exp.setAutoDraw(True)
    if beg_exp.status == STARTED:
        if bool((beg_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            beg_exp.tStop = t  # not accounting for scr refresh
            beg_exp.frameNStop = frameN  # exact frame index
            win.timeOnFlip(beg_exp, 'tStopRefresh')  # time at next scr refresh
            beg_exp.setAutoDraw(False)
    
    # *beg_exp_resp* updates
    waitOnFlip = False
    if beg_exp_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beg_exp_resp.frameNStart = frameN  # exact frame index
        beg_exp_resp.tStart = t  # local t and not account for scr refresh
        beg_exp_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beg_exp_resp, 'tStartRefresh')  # time at next scr refresh
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
            win.timeOnFlip(beg_exp_resp, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in_begin_experiment"-------
for thisComponent in in_begin_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('beg_exp.started', beg_exp.tStartRefresh)
thisExp.addData('beg_exp.stopped', beg_exp.tStopRefresh)
# check responses
if beg_exp_resp.keys in ['', [], None]:  # No response was made
    beg_exp_resp.keys = None
thisExp.addData('beg_exp_resp.keys',beg_exp_resp.keys)
if beg_exp_resp.keys != None:  # we had a response
    thisExp.addData('beg_exp_resp.rt', beg_exp_resp.rt)
thisExp.addData('beg_exp_resp.started', beg_exp_resp.tStartRefresh)
thisExp.addData('beg_exp_resp.stopped', beg_exp_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "in_begin_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
extcc_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-1_task-extcc_events-input.csv'),
    seed=None, name='extcc_trials')
thisExp.addLoop(extcc_trials)  # add the loop to the experiment
thisExtcc_trial = extcc_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisExtcc_trial.rgb)
if thisExtcc_trial != None:
    for paramName in thisExtcc_trial:
        exec('{} = thisExtcc_trial[paramName]'.format(paramName))

for thisExtcc_trial in extcc_trials:
    currentLoop = extcc_trials
    # abbreviate parameter names if possible (e.g. rgb = thisExtcc_trial.rgb)
    if thisExtcc_trial != None:
        for paramName in thisExtcc_trial:
            exec('{} = thisExtcc_trial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "iti"-------
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    itiComponents = [fix_cross, iti_animals, iti_tools]
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
    itiClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "iti"-------
    while continueRoutine:
        # get current time
        t = itiClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=itiClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix_cross* updates
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)
        
        # *iti_animals* updates
        if iti_animals.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_animals.frameNStart = frameN  # exact frame index
            iti_animals.tStart = t  # local t and not account for scr refresh
            iti_animals.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_animals, 'tStartRefresh')  # time at next scr refresh
            iti_animals.setAutoDraw(True)
        if iti_animals.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_animals.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_animals.tStop = t  # not accounting for scr refresh
                iti_animals.frameNStop = frameN  # exact frame index
                win.timeOnFlip(iti_animals, 'tStopRefresh')  # time at next scr refresh
                iti_animals.setAutoDraw(False)
        
        # *iti_tools* updates
        if iti_tools.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            iti_tools.frameNStart = frameN  # exact frame index
            iti_tools.tStart = t  # local t and not account for scr refresh
            iti_tools.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(iti_tools, 'tStartRefresh')  # time at next scr refresh
            iti_tools.setAutoDraw(True)
        if iti_tools.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > iti_tools.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                iti_tools.tStop = t  # not accounting for scr refresh
                iti_tools.frameNStop = frameN  # exact frame index
                win.timeOnFlip(iti_tools, 'tStopRefresh')  # time at next scr refresh
                iti_tools.setAutoDraw(False)
        
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
    
    # -------Ending Routine "iti"-------
    for thisComponent in itiComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    extcc_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    extcc_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)
    extcc_trials.addData('iti_animals.started', iti_animals.tStartRefresh)
    extcc_trials.addData('iti_animals.stopped', iti_animals.tStopRefresh)
    extcc_trials.addData('iti_tools.started', iti_tools.tStartRefresh)
    extcc_trials.addData('iti_tools.stopped', iti_tools.tStopRefresh)
    # the Routine "iti" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    trials_resp.keys = []
    trials_resp.rt = []
    _trials_resp_allKeys = []
    ext_image.setImage(stimulus)
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set the response colors to white
    animal_resp_color = 'white'
    tool_resp_color = 'white'
    
    # keep track of which components have finished
    trialComponents = [trials_resp, animal, tool, ext_image]
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
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
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
                win.timeOnFlip(trials_resp, 'tStopRefresh')  # time at next scr refresh
                trials_resp.status = FINISHED
        if trials_resp.status == STARTED and not waitOnFlip:
            theseKeys = trials_resp.getKeys(keyList=['num_1', 'num_2', '1', '2'], waitRelease=False)
            _trials_resp_allKeys.extend(theseKeys)
            if len(_trials_resp_allKeys):
                trials_resp.keys = _trials_resp_allKeys[-1].name  # just the last key pressed
                trials_resp.rt = _trials_resp_allKeys[-1].rt
        
        # *animal* updates
        if animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            animal.frameNStart = frameN  # exact frame index
            animal.tStart = t  # local t and not account for scr refresh
            animal.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(animal, 'tStartRefresh')  # time at next scr refresh
            animal.setAutoDraw(True)
        if animal.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > animal.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                animal.tStop = t  # not accounting for scr refresh
                animal.frameNStop = frameN  # exact frame index
                win.timeOnFlip(animal, 'tStopRefresh')  # time at next scr refresh
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
            tool.setAutoDraw(True)
        if tool.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > tool.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                tool.tStop = t  # not accounting for scr refresh
                tool.frameNStop = frameN  # exact frame index
                win.timeOnFlip(tool, 'tStopRefresh')  # time at next scr refresh
                tool.setAutoDraw(False)
        if tool.status == STARTED:  # only update if drawing
            tool.setColor(tool_resp_color, colorSpace='rgb', log=False)
        
        # *ext_image* updates
        if ext_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ext_image.frameNStart = frameN  # exact frame index
            ext_image.tStart = t  # local t and not account for scr refresh
            ext_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ext_image, 'tStartRefresh')  # time at next scr refresh
            ext_image.setAutoDraw(True)
        if ext_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > ext_image.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                ext_image.tStop = t  # not accounting for scr refresh
                ext_image.frameNStop = frameN  # exact frame index
                win.timeOnFlip(ext_image, 'tStopRefresh')  # time at next scr refresh
                ext_image.setAutoDraw(False)
        #change the color of the response if one is pressed
        if 'num_1' in trials_resp.keys:
            animal_resp_color = 'darkgrey'
        elif 'num_2' in trials_resp.keys:
            tool_resp_color = 'darkgrey'
        
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
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trials_resp.keys in ['', [], None]:  # No response was made
        trials_resp.keys = None
    extcc_trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        extcc_trials.addData('trials_resp.rt', trials_resp.rt)
    extcc_trials.addData('trials_resp.started', trials_resp.tStartRefresh)
    extcc_trials.addData('trials_resp.stopped', trials_resp.tStopRefresh)
    extcc_trials.addData('animal.started', animal.tStartRefresh)
    extcc_trials.addData('animal.stopped', animal.tStopRefresh)
    extcc_trials.addData('tool.started', tool.tStartRefresh)
    extcc_trials.addData('tool.stopped', tool.tStopRefresh)
    extcc_trials.addData('ext_image.started', ext_image.tStartRefresh)
    extcc_trials.addData('ext_image.stopped', ext_image.tStopRefresh)
    #send the event code
    stim_marker('offset',SHOCK=False)
    
    # ------Prepare to start Routine "cc"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    cc_image.setImage(cc_stimulus)
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set colors 
    cc_yescol = 'darkgrey'
    cc_nocol = 'darkgrey'
    
    # keep track of which components have finished
    ccComponents = [cc_image, cc_yes, cc_no]
    for thisComponent in ccComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    ccClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "cc"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = ccClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=ccClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *cc_image* updates
        if cc_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cc_image.frameNStart = frameN  # exact frame index
            cc_image.tStart = t  # local t and not account for scr refresh
            cc_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cc_image, 'tStartRefresh')  # time at next scr refresh
            cc_image.setAutoDraw(True)
        if cc_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cc_image.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                cc_image.tStop = t  # not accounting for scr refresh
                cc_image.frameNStop = frameN  # exact frame index
                win.timeOnFlip(cc_image, 'tStopRefresh')  # time at next scr refresh
                cc_image.setAutoDraw(False)
        if cc_image.image() =='stims/crosshair.jpg': 
            cc_yescol = 'white'
            cc_nocol = 'white'
        
        # *cc_yes* updates
        if cc_yes.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cc_yes.frameNStart = frameN  # exact frame index
            cc_yes.tStart = t  # local t and not account for scr refresh
            cc_yes.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cc_yes, 'tStartRefresh')  # time at next scr refresh
            cc_yes.setAutoDraw(True)
        if cc_yes.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cc_yes.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                cc_yes.tStop = t  # not accounting for scr refresh
                cc_yes.frameNStop = frameN  # exact frame index
                win.timeOnFlip(cc_yes, 'tStopRefresh')  # time at next scr refresh
                cc_yes.setAutoDraw(False)
        if cc_yes.status == STARTED:  # only update if drawing
            cc_yes.setColor(cc_yescol, colorSpace='rgb', log=False)
        
        # *cc_no* updates
        if cc_no.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cc_no.frameNStart = frameN  # exact frame index
            cc_no.tStart = t  # local t and not account for scr refresh
            cc_no.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cc_no, 'tStartRefresh')  # time at next scr refresh
            cc_no.setAutoDraw(True)
        if cc_no.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cc_no.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                cc_no.tStop = t  # not accounting for scr refresh
                cc_no.frameNStop = frameN  # exact frame index
                win.timeOnFlip(cc_no, 'tStopRefresh')  # time at next scr refresh
                cc_no.setAutoDraw(False)
        if cc_no.status == STARTED:  # only update if drawing
            cc_no.setColor(cc_nocol, colorSpace='rgb', log=False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ccComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "cc"-------
    for thisComponent in ccComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    extcc_trials.addData('cc_image.started', cc_image.tStartRefresh)
    extcc_trials.addData('cc_image.stopped', cc_image.tStopRefresh)
    #send the event code
    stim_marker('offset',SHOCK=False)
    extcc_trials.addData('cc_yes.started', cc_yes.tStartRefresh)
    extcc_trials.addData('cc_yes.stopped', cc_yes.tStopRefresh)
    extcc_trials.addData('cc_no.started', cc_no.tStartRefresh)
    extcc_trials.addData('cc_no.stopped', cc_no.tStopRefresh)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'extcc_trials'


# ------Prepare to start Routine "in_end_experiment"-------
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
in_end_experimentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in_end_experiment"-------
while continueRoutine:
    # get current time
    t = in_end_experimentClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in_end_experimentClock)
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
            win.timeOnFlip(end_exp_resp, 'tStopRefresh')  # time at next scr refresh
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
        end_exp.setAutoDraw(True)
    if end_exp.status == STARTED:
        if bool((end_exp_resp.keys)=='space'):
            # keep track of stop time/frame for later
            end_exp.tStop = t  # not accounting for scr refresh
            end_exp.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_exp, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in_end_experiment"-------
for thisComponent in in_end_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if end_exp_resp.keys in ['', [], None]:  # No response was made
    end_exp_resp.keys = None
thisExp.addData('end_exp_resp.keys',end_exp_resp.keys)
if end_exp_resp.keys != None:  # we had a response
    thisExp.addData('end_exp_resp.rt', end_exp_resp.rt)
thisExp.addData('end_exp_resp.started', end_exp_resp.tStartRefresh)
thisExp.addData('end_exp_resp.stopped', end_exp_resp.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('end_exp.started', end_exp.tStartRefresh)
thisExp.addData('end_exp.stopped', end_exp.tStopRefresh)
# the Routine "in_end_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
