#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on May 30, 2025, at 12:57
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
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

# Run 'Before Experiment' code from setup_code
# from psychopy.sound import Sound
from psychopy.parallel import ParallelPort
import serial
from subprocess import Popen
import time
from psychopy import prefs
from FAB_preferences import *
import psychtoolbox as ptb
prefs.general['audioLib'] = ['PTB']
from psychopy import sound, core
print(sound.audioLib)


'''setup exp parameters'''
expName = 'FAB'  
expInfo = {'participant': ''}
study_prefix='FB'

'''setup user input GUI'''
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split(f'sub-{study_prefix}')[-1]) for i in os.listdir('data') if f'sub-{study_prefix}' in i])
dlg.addField('Init port?', choices=['yes','no (testing parallel)','no (testing serial)'])
dlg.addField('room/port', choices =[port_label_1, port_label_2]) 

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
    
'''setup variables based on input'''   
expInfo = {'participant':user_input[0]}
bidsID = f'sub-{study_prefix}'+'{0:0=3d}'.format(int(expInfo['participant']))#provided from itec_preferences.py

'''port setup'''
port_type = ''
BIO = True if user_input[1] == 'yes' and user_input[2] == port_label_1 else False 
BIO2 = True if user_input[1] == 'yes' and user_input[2] == port_label_2 else False 

if BIO == True:
    if port_type_1 == 'P':
        port = ParallelPort(address=port_address_1)
        port_type = "parallel"
    elif port_type_1 == 'S':
        port = serial.Serial(port_address_1)
        port_type = "serial"
elif BIO2 == True:
    if port_type_2 == 'P':
        port = ParallelPort(address=port_address_2)
        port_type = "parallel"
    elif port_type_2 == 'S':
        port = serial.Serial(port_address_2)
        port_type = "serial"
else:
    if user_input[1] == 'no (testing parallel)':
        port_type = "parallel"
        class PortEmulator(object):
            def __init__(self, address=None):
                pass
            def setData(self, data=None):
                logging.warn("Sent data to non-existent pPort:{}".format(data))
            def setPin(self, pin, data):
                logging.warn(f"Sent data to non-existent pPort pin: {pin}, {data}")
    elif user_input[1] == 'no (testing serial)': #untested
        port_type = "serial"
        class PortEmulator(object):
            def __init__(self, address=None):
                pass
            def flush(self):
                logging.warn(f"flushed non-existent sPort")
            def write(self,data):
                logging.warn(f"Sent data to non-existent sPort: {data}")
                
    port = PortEmulator()
    
if port_type == "parallel":
    port.setData(0) #reset the pins

    def shock():
        port.setPin(shock_code,1) #1 corresponds to pin ON
        time.sleep(shock_duration)
        port.setPin(shock_code,0) #0 corresponds to pin OFF

    def stim_marker(on_or_offset='',SHOCK=False):
        if SHOCK:
            shock()
        if 'on' in on_or_offset:
            port.setPin(stimulus_code,1)
        elif 'off' in on_or_offset:
            port.setPin(stimulus_code,0)
            
    def FPS_marker():
        port.setPin(FPS_code,1)
        time.sleep(FPS_duration)
        port.setPin(FPS_code,0)
        
    def FPS_marker_control(on_or_offset=''):
        if 'on' in on_or_offset:
            port.setPin(FPS_code,1)
        elif 'off' in on_or_offset:
            port.setPin(FPS_code,0)

#### HAS NOT BEEN TESTED ####
#### assumes BIOPAC/etc can read integer and port.write() will correctly send, otherwise might need to use some combination of port.print() and byte(code)
if port_type == "serial":
    port.flush()
    def shock():
        port.write(int(shock_code))
        time.sleep(shock_duration)
        port.write(int(0))

    def stim_marker(on_or_offset='',SHOCK=False):
        if SHOCK:
            shock()
        if 'on' in on_or_offset:
            port.write(int(stimulus_code))
        elif 'off' in on_or_offset:
            port.write(int(0))
            

# Run 'Before Experiment' code from functions
def dragOnly():
    click = bool(slider0.mouse.getPressed()[0])
    xy = slider0.mouse.getPos()

    if click:
        # Update current but don't set Rating (mouse is still down)
        # Dragging has to start inside a "valid" area (i.e., on the
        # slider), but may continue even if the mouse moves away from
        # the slider, as long as the mouse button is not released.
        if (slider0.validArea.contains(slider0.mouse, units=slider0.units) and slider0.markerPos is None):
            slider0.markerPos = slider0._posToRating(xy)  # updates marker
            slider0._dragging = True
        elif (slider0.marker.contains(slider0.mouse, units=slider0.units) or
                slider0._dragging):
            slider0.markerPos = slider0._posToRating(xy)  # updates marker
            slider0._dragging = True
    else:  # mouse is up - check if it *just* came up
        if slider0._dragging:
            slider0._dragging = False
            if slider0.markerPos is not None:
                slider0.recordRating(slider0.markerPos)
            return slider0.markerPos
        else:
            # is up and was already up - move along
            return None
    slider0._mouseStateXY = xy
    
slideSpeed = 1
slider_granularity = .1
slider_decimals = 1
slider_width = 1
slider_height = .03
slider_orientation = 0
slider_ticks=[0, 100]
slider_labels=['no shock','shock']

# Create a slider_shape in this routine with the same size as the slider
# Check if mouse is moving within slider_shape, if so change marker position accordingly
# this function is executed each frame, defines mouse location for that frame and record the location as final location
def getmarker(mouse_d, first, mouseRec, slider_shaped, slider_rt, exp_rating, marker_position, exp_rating_all, exp_rt_all):
    # if the mouse has never hit the square
    # if it's the first time, return rt and rating as 999
    if first == 1:
        mouse_x = mouse_d.getPos()[0]
        mouse_y = mouse_d.getPos()[1]
    # if mouse3 moved to the area of the marker, starts moving by setting first to 0
        if mouse_x <= 0.035 and mouse_x >= -0.035 and mouse_y <= -0.335 and mouse_y >= -0.365:
            first = 0
    # record the time when mouse hit the square
            thisExp.addData('marker_hit', t)
     # if in this frame, doesn't hit marker, quit the function,nothing happens
    # if already hit the marker
    if first == 0:
        # if the mouse position is not the same as the last one
        # if the shape contains the mouse 
        if slider_shaped.contains(mouse_d) and mouse_d.getPos()[0] != mouseRec[0]:
            # update mouse location and marker position
            mouseRec = mouse_d.getPos()
            marker_position = (mouseRec[0], -0.35)
            exp_rating = mouseRec[0]/slider_width*(slider_ticks[-1]-slider_ticks[0])+(slider_ticks[0]+slider_ticks[-1])/2
            exp_rating = round(exp_rating, 1)
            slider_rt = t
     #       thisExp.addData('exp_rating', exp_rating)
            exp_rating_all.append(exp_rating)
     #       thisExp.addData('exp_rating_t', slider_rt)
            exp_rt_all.append(slider_rt)
    return marker_position, mouseRec, first, slider_rt, exp_rating, exp_rating_all, exp_rt_all
    


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'extinction_recall'  # from the Builder filename that created this script
expInfo = {
    '': '',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\Experiments\\FAB\\ses-1_run-3_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
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

# --- Initialize components for Routine "setup" ---
# Run 'Begin Experiment' code from setup_code
trialClock = core.Clock()

# --- Initialize components for Routine "final_reminder" ---
text = visual.TextStim(win=win, name='text',
    text='Ready to resume?\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
wait_for_start_key = keyboard.Keyboard()

# --- Initialize components for Routine "fixation_cross" ---
cross_start = visual.ShapeStim(
    win=win, name='cross_start', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "recall" ---
textr_recall = visual.TextStim(win=win, name='textr_recall',
    text='noise (100%)',
    font='Open Sans',
    pos=(0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
img_recall = visual.ImageStim(
    win=win,
    name='img_recall', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.45, 0.45),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
textl_recall = visual.TextStim(win=win, name='textl_recall',
    text='no noise (0%)',
    font='Open Sans',
    pos=(-0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
shape_recall = visual.Rect(
    win=win, name='shape_recall',
    width=(1, 0.07)[0], height=(1, 0.07)[1],
    ori=0.0, pos=(0, -0.35), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[0.0000, 0.0000, 0.0000],
    opacity=None, depth=-4.0, interpolate=True)
sliderl_recall = visual.Slider(win=win, name='sliderl_recall',
    startValue=None, size=(0.45, 0.03), pos=(-0.275, -0.35), units='height',
    labels=None, ticks=(0,50), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-5, readOnly=True)
expect_recall = visual.TextStim(win=win, name='expect_recall',
    text='How much do you expect a noise?\n\n',
    font='Open Sans',
    pos=(0, -0.3), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
sliderr_recall = visual.Slider(win=win, name='sliderr_recall',
    startValue=None, size=(0.45, 0.03), pos=(0.275, -0.35), units='height',
    labels=None, ticks=(50,100), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-7, readOnly=True)
marker_recall = visual.Rect(
    win=win, name='marker_recall',
    width=(0.03, 0.07)[0], height=(0.03, 0.07)[1],
    ori=0.0, pos=[0,0], anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[1.0000, -1.0000, -1.0000],
    opacity=1.0, depth=-8.0, interpolate=True)
mouse_recall = event.Mouse(win=win)
x, y = [None, None]
mouse_recall.mouseClock = core.Clock()

# --- Initialize components for Routine "iti" ---
cross_2 = visual.ShapeStim(
    win=win, name='cross_2', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "setup" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
setupComponents = []
for thisComponent in setupComponents:
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

# --- Run Routine "setup" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "setup" ---
for thisComponent in setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
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
    
    # --- Prepare to start Routine "final_reminder" ---
    continueRoutine = True
    # update component parameters for each repeat
    wait_for_start_key.keys = []
    wait_for_start_key.rt = []
    _wait_for_start_key_allKeys = []
    # keep track of which components have finished
    final_reminderComponents = [text, wait_for_start_key]
    for thisComponent in final_reminderComponents:
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
    
    # --- Run Routine "final_reminder" ---
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
            text.setAutoDraw(True)
        
        # *wait_for_start_key* updates
        waitOnFlip = False
        if wait_for_start_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            wait_for_start_key.frameNStart = frameN  # exact frame index
            wait_for_start_key.tStart = t  # local t and not account for scr refresh
            wait_for_start_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(wait_for_start_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'wait_for_start_key.started')
            wait_for_start_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(wait_for_start_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(wait_for_start_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if wait_for_start_key.status == STARTED and not waitOnFlip:
            theseKeys = wait_for_start_key.getKeys(keyList=['space'], waitRelease=False)
            _wait_for_start_key_allKeys.extend(theseKeys)
            if len(_wait_for_start_key_allKeys):
                wait_for_start_key.keys = _wait_for_start_key_allKeys[-1].name  # just the last key pressed
                wait_for_start_key.rt = _wait_for_start_key_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in final_reminderComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "final_reminder" ---
    for thisComponent in final_reminderComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if wait_for_start_key.keys in ['', [], None]:  # No response was made
        wait_for_start_key.keys = None
    trials.addData('wait_for_start_key.keys',wait_for_start_key.keys)
    if wait_for_start_key.keys != None:  # we had a response
        trials.addData('wait_for_start_key.rt', wait_for_start_key.rt)
    # Run 'End Routine' code from start_reset_clock
    globalClock.reset()
    # the Routine "final_reminder" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'


# --- Prepare to start Routine "fixation_cross" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
fixation_crossComponents = [cross_start]
for thisComponent in fixation_crossComponents:
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

# --- Run Routine "fixation_cross" ---
while continueRoutine and routineTimer.getTime() < 3.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *cross_start* updates
    if cross_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        cross_start.frameNStart = frameN  # exact frame index
        cross_start.tStart = t  # local t and not account for scr refresh
        cross_start.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cross_start, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'cross_start.started')
        cross_start.setAutoDraw(True)
    if cross_start.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross_start.tStartRefresh + 3-frameTolerance:
            # keep track of stop time/frame for later
            cross_start.tStop = t  # not accounting for scr refresh
            cross_start.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_start.stopped')
            cross_start.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixation_crossComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation_cross" ---
for thisComponent in fixation_crossComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from reset_clock
globalClock.reset()
# using non-slip timing so subtract the expected duration of this Routine
routineTimer.addTime(-3.000000)

# set up handler to look after randomisation of conditions etc
recall_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f"data/{bidsID}/{bidsID}_ses-1_task-recall_events-input.xlsx"),
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
    
    # --- Prepare to start Routine "recall" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_recall
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    # record global start time
    thisExp.timestampOnFlip(win, 'stim_onset')
    
    # initiate old rating as 50
    oldRating = 50
    
    # set start position of the slider to end position of the previous trial
    marker_position = (0,-0.35)
    
    # record the current position of the mouse
    mouseRec=mouse_recall.getPos()
    first = 1
    slider_rt = 999
    exp_rating = 999
    exp_rating_all = list()
    exp_rt_all = list()
    
    
    
    img_recall.setPos(location)
    img_recall.setImage(path)
    sliderl_recall.reset()
    sliderr_recall.reset()
    # setup some python lists for storing info about the mouse_recall
    gotValidClick = False  # until a click is received
    # Run 'Begin Routine' code from preload
    # create sound if FPS == 1
    # preschedule sound object
    flag = 0
    if FPS == 1:
        now = ptb.GetSecs()
        mySound = sound.Sound('stimuli/calibrationprobe1.wav', stereo=True, hamming=False, name='mySound')
        mySound.setVolume(1)
        mySound.play(when=now + FPS_timing)
        timestart = now+FPS_timing
        thisExp.addData('FPS_scheduled', timestart)
    
    
    # keep track of which components have finished
    recallComponents = [textr_recall, img_recall, textl_recall, shape_recall, sliderl_recall, expect_recall, sliderr_recall, marker_recall, mouse_recall]
    for thisComponent in recallComponents:
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
    
    # --- Run Routine "recall" ---
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_recall
        #mouse_d, first, mouseRec, slider_shaped
        # first = 0 or 1, mouseRec as updated rating, mouse0 as initial location,slidershape as where the slider is
        marker_position, mouseRec, first, slider_rt, exp_rating, exp_rating_all, exp_rt_all = getmarker(mouse_recall, first, mouseRec, shape_recall, slider_rt, exp_rating, marker_position, exp_rating_all, exp_rt_all)
        
        
        
        
        
        
        
        # *textr_recall* updates
        if textr_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textr_recall.frameNStart = frameN  # exact frame index
            textr_recall.tStart = t  # local t and not account for scr refresh
            textr_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textr_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textr_recall.started')
            textr_recall.setAutoDraw(True)
        if textr_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textr_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                textr_recall.tStop = t  # not accounting for scr refresh
                textr_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textr_recall.stopped')
                textr_recall.setAutoDraw(False)
        
        # *img_recall* updates
        if img_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            img_recall.frameNStart = frameN  # exact frame index
            img_recall.tStart = t  # local t and not account for scr refresh
            img_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(img_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'img_recall.started')
            img_recall.setAutoDraw(True)
        if img_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > img_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                img_recall.tStop = t  # not accounting for scr refresh
                img_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'img_recall.stopped')
                img_recall.setAutoDraw(False)
        
        # *textl_recall* updates
        if textl_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textl_recall.frameNStart = frameN  # exact frame index
            textl_recall.tStart = t  # local t and not account for scr refresh
            textl_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textl_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textl_recall.started')
            textl_recall.setAutoDraw(True)
        if textl_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textl_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                textl_recall.tStop = t  # not accounting for scr refresh
                textl_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textl_recall.stopped')
                textl_recall.setAutoDraw(False)
        
        # *shape_recall* updates
        if shape_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            shape_recall.frameNStart = frameN  # exact frame index
            shape_recall.tStart = t  # local t and not account for scr refresh
            shape_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(shape_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'shape_recall.started')
            shape_recall.setAutoDraw(True)
        if shape_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > shape_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                shape_recall.tStop = t  # not accounting for scr refresh
                shape_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'shape_recall.stopped')
                shape_recall.setAutoDraw(False)
        
        # *sliderl_recall* updates
        if sliderl_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderl_recall.frameNStart = frameN  # exact frame index
            sliderl_recall.tStart = t  # local t and not account for scr refresh
            sliderl_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderl_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderl_recall.started')
            sliderl_recall.setAutoDraw(True)
        if sliderl_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sliderl_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                sliderl_recall.tStop = t  # not accounting for scr refresh
                sliderl_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sliderl_recall.stopped')
                sliderl_recall.setAutoDraw(False)
        
        # *expect_recall* updates
        if expect_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            expect_recall.frameNStart = frameN  # exact frame index
            expect_recall.tStart = t  # local t and not account for scr refresh
            expect_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(expect_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'expect_recall.started')
            expect_recall.setAutoDraw(True)
        if expect_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > expect_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                expect_recall.tStop = t  # not accounting for scr refresh
                expect_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'expect_recall.stopped')
                expect_recall.setAutoDraw(False)
        
        # *sliderr_recall* updates
        if sliderr_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderr_recall.frameNStart = frameN  # exact frame index
            sliderr_recall.tStart = t  # local t and not account for scr refresh
            sliderr_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderr_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderr_recall.started')
            sliderr_recall.setAutoDraw(True)
        if sliderr_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sliderr_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                sliderr_recall.tStop = t  # not accounting for scr refresh
                sliderr_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sliderr_recall.stopped')
                sliderr_recall.setAutoDraw(False)
        
        # *marker_recall* updates
        if marker_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            marker_recall.frameNStart = frameN  # exact frame index
            marker_recall.tStart = t  # local t and not account for scr refresh
            marker_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(marker_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'marker_recall.started')
            marker_recall.setAutoDraw(True)
        if marker_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > marker_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                marker_recall.tStop = t  # not accounting for scr refresh
                marker_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'marker_recall.stopped')
                marker_recall.setAutoDraw(False)
        if marker_recall.status == STARTED:  # only update if drawing
            marker_recall.setPos(marker_position, log=False)
        # *mouse_recall* updates
        if mouse_recall.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_recall.frameNStart = frameN  # exact frame index
            mouse_recall.tStart = t  # local t and not account for scr refresh
            mouse_recall.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_recall, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_recall.started', t)
            mouse_recall.status = STARTED
            mouse_recall.mouseClock.reset()
            prevButtonState = [0, 0, 0]  # if now button is down we will treat as 'new' click
        if mouse_recall.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mouse_recall.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                mouse_recall.tStop = t  # not accounting for scr refresh
                mouse_recall.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('mouse_recall.stopped', t)
                mouse_recall.status = FINISHED
        # Run 'Each Frame' code from preload
        if FPS == 1:
            if flag == 0 and t >= FPS_timing:
                # send trigger
                FPS_marker()
                thisExp.addData('FPStrigger', t)
                flag = 1
        
        
        
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in recallComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "recall" ---
    for thisComponent in recallComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_recall
    stim_marker('offset',SHOCK=bool(int(us))) #deliver shock if need be
    #save the offset time
    thisExp.timestampOnFlip(win, 'stim_offset')
    
    thisExp.addData('CS_duration', t)
    # thisExp.addData('routineTiming', routineTimer.getTime())
    if exp_rating != 999:
        thisExp.addData('exp_rating_final', exp_rating)
        
    # will throw an error if subject didn't move
    if slider_rt != 999:
        thisExp.addData('exp_rt_final', slider_rt)
    
    thisExp.addData('exp_rating_all', exp_rating_all)
    thisExp.addData('exp_rt_all', exp_rt_all)
    
    
    # store data for recall_trials (TrialHandler)
    # using non-slip timing so subtract the expected duration of this Routine
    routineTimer.addTime(-5.000000)
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from iti_code_2
    thisExp.addData('iti_begin_cond', routineTimer.getTime())
    
    # keep track of which components have finished
    itiComponents = [cross_2]
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
        
        # *cross_2* updates
        if cross_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross_2.frameNStart = frameN  # exact frame index
            cross_2.tStart = t  # local t and not account for scr refresh
            cross_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_2.started')
            cross_2.setAutoDraw(True)
        if cross_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cross_2.tStartRefresh + iti-frameTolerance:
                # keep track of stop time/frame for later
                cross_2.tStop = t  # not accounting for scr refresh
                cross_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cross_2.stopped')
                cross_2.setAutoDraw(False)
        
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
    # Run 'End Routine' code from iti_code_2
    thisExp.addData('iti_duration', routineTimer.getTime())
    
    
    
    # the Routine "iti" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'recall_trials'

# Run 'End Experiment' code from setup_code
if port_type == "serial":
    port.close()

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
