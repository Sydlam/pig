#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on Tue Jun 10 12:33:46 2025
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
prefs.hardware['audioLib'] = 'ptb'
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
study_prefix= "FB"

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
    

slider_width = 1
slider_height = .03
slider_orientation = 0
slider_ticks=[0, 100]


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
            exp_rating_all.append(exp_rating)
            exp_rt_all.append(slider_rt)
    return marker_position, mouseRec, first, slider_rt, exp_rating, exp_rating_all, exp_rt_all
    


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'conditioning'  # from the Builder filename that created this script
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
    originPath='/Users/sydneylambert/Desktop/pig/FAB/ses-1_run-1_lastrun.py',
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

# --- Initialize components for Routine "inst_acq1" ---
inst1 = visual.TextStim(win=win, name='inst1',
    text='You will see four pictures of fractal patterns. These will appear in the center of the screen for a few seconds.\n\nSome pictures will be followed by a loud white noise, and others will not.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_response = keyboard.Keyboard()

# --- Initialize components for Routine "inst_acq2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='We will be measuring your level of sweating from sensors on your left hand.\n\nThese are sensitive to movement and posture, so please sit up straight and do not shift around during the experiment.\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_response = keyboard.Keyboard()

# --- Initialize components for Routine "inst_acq3" ---
inst1_2 = visual.TextStim(win=win, name='inst1_2',
    text="This is a learning experiment. If you pay attention to the pictures, then you can learn the association between the pictures and the noise.\n\nIn other words, you will learn to predict when the noise will occur or won't occur, based on the types of picture that you see.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_response_2 = keyboard.Keyboard()

# --- Initialize components for Routine "sliderdemo" ---
sliderright = visual.TextStim(win=win, name='sliderright',
    text='noise (100%)',
    font='Open Sans',
    pos=(0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
sliderleft = visual.TextStim(win=win, name='sliderleft',
    text='no noise (0%)',
    font='Open Sans',
    pos=(-0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
instdemo = visual.TextStim(win=win, name='instdemo',
    text='On each trial, you will rate from 0% to 100% how likely it is that you will hear a noise by moving the cursor on the rating bar with your mouse. The cursor will always show up in the middle of the bar. You will need to move it to the left or the right side.\n\nYou can leave the cursor anywhere on the scale depending on how certain you are.\n\n\n\n\n\n\n',
    font='Open Sans',
    pos=(0, -0.06), height=0.045, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
shape_demo = visual.Rect(
    win=win, name='shape_demo',
    width=(1, 0.07)[0], height=(1, 0.07)[1],
    ori=0.0, pos=(0, -0.35), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[0.0000, 0.0000, 0.0000],
    opacity=None, depth=-4.0, interpolate=True)
slider0l_d = visual.Slider(win=win, name='slider0l_d',
    startValue=None, size=(0.45, 0.03), pos=(-0.275, -0.35), units='height',
    labels=None, ticks=(0,50), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-5, readOnly=True)
expect0_d = visual.TextStim(win=win, name='expect0_d',
    text='How much do you expect a noise?\n\n',
    font='Open Sans',
    pos=(0, -0.3), height=0.045, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
slider0r_d = visual.Slider(win=win, name='slider0r_d',
    startValue=None, size=(0.45, 0.03), pos=(0.275, -0.35), units='height',
    labels=None, ticks=(50,100), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-7, readOnly=True)
markerdemo = visual.Rect(
    win=win, name='markerdemo',
    width=(0.03, 0.07)[0], height=(0.03, 0.07)[1],
    ori=0.0, pos=[0,0], anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[1.0000, -1.0000, -1.0000],
    opacity=1.0, depth=-8.0, interpolate=True)
mouse_d = event.Mouse(win=win)
x, y = [None, None]
mouse_d.mouseClock = core.Clock()
resp_demo = keyboard.Keyboard()

# --- Initialize components for Routine "inst_acq4" ---
inst4 = visual.TextStim(win=win, name='inst4',
    text='PLEASE MAKE A RATING ON EVERY TRIAL.\nWe are measuring how fast you respond, and you only need to give your rating when a picture is onscreen.\n\nPlease note: Your ratings do NOT influence whether you will hear a noise or not during the experiment. In other words, you cannot trigger or prevent the noise with your answers.',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_response = keyboard.Keyboard()

# --- Initialize components for Routine "inst_acq5" ---
inst5 = visual.TextStim(win=win, name='inst5',
    text="Please keep your eyes open and watch the screen the whole time. Pay attention to learn the relationship between the noise and what's on the screen.\n\nAlso make sure you make a rating for every image using the cursor onscreen.\n\nAre you ready?",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst5_response = keyboard.Keyboard()

# --- Initialize components for Routine "fixation_cross" ---
cross_start = visual.ShapeStim(
    win=win, name='cross_start', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "conditioning" ---
textr_cond = visual.TextStim(win=win, name='textr_cond',
    text='noise (100%)',
    font='Open Sans',
    pos=(0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
img_cond = visual.ImageStim(
    win=win,
    name='img_cond', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.45, 0.45),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
textl_cond = visual.TextStim(win=win, name='textl_cond',
    text='no noise (0%)',
    font='Open Sans',
    pos=(-0.45, -0.4), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
shape_cond = visual.Rect(
    win=win, name='shape_cond',
    width=(1, 0.07)[0], height=(1, 0.07)[1],
    ori=0.0, pos=(0, -0.35), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[0.0000, 0.0000, 0.0000],
    opacity=None, depth=-4.0, interpolate=True)
sliderl_cond = visual.Slider(win=win, name='sliderl_cond',
    startValue=None, size=(0.45, 0.03), pos=(-0.275, -0.35), units='height',
    labels=None, ticks=(0,50), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-5, readOnly=True)
expect_cond = visual.TextStim(win=win, name='expect_cond',
    text='How much do you expect a noise?\n\n',
    font='Open Sans',
    pos=(0, -0.3), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
sliderr_cond = visual.Slider(win=win, name='sliderr_cond',
    startValue=None, size=(0.45, 0.03), pos=(0.275, -0.35), units='height',
    labels=None, ticks=(50,100), granularity=None,
    style='slider', styleTweaks=(), opacity=None,
    labelColor=[1.0000, 1.0000, 1.0000], markerColor=[1.0000, -1.0000, -1.0000], lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.04,
    flip=False, ori=0.0, depth=-7, readOnly=True)
marker_cond = visual.Rect(
    win=win, name='marker_cond',
    width=(0.03, 0.07)[0], height=(0.03, 0.07)[1],
    ori=0.0, pos=[0,0], anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor=[1.0000, -1.0000, -1.0000],
    opacity=1.0, depth=-8.0, interpolate=True)
mouse_cond = event.Mouse(win=win)
x, y = [None, None]
mouse_cond.mouseClock = core.Clock()

# --- Initialize components for Routine "iti" ---
cross_2 = visual.ShapeStim(
    win=win, name='cross_2', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# --- Initialize components for Routine "breaktime" ---
inst_break = visual.TextStim(win=win, name='inst_break',
    text='Take a break!\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_response_5 = keyboard.Keyboard()

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
routineForceEnded = not continueRoutine
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
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
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
    
    # --- Prepare to start Routine "inst_acq1" ---
    continueRoutine = True
    # update component parameters for each repeat
    inst1_response.keys = []
    inst1_response.rt = []
    _inst1_response_allKeys = []
    # keep track of which components have finished
    inst_acq1Components = [inst1, inst1_response]
    for thisComponent in inst_acq1Components:
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
    
    # --- Run Routine "inst_acq1" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *inst1* updates
        
        # if inst1 is starting this frame...
        if inst1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            inst1.frameNStart = frameN  # exact frame index
            inst1.tStart = t  # local t and not account for scr refresh
            inst1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1.started')
            # update status
            inst1.status = STARTED
            inst1.setAutoDraw(True)
        
        # if inst1 is active this frame...
        if inst1.status == STARTED:
            # update params
            pass
        
        # *inst1_response* updates
        waitOnFlip = False
        
        # if inst1_response is starting this frame...
        if inst1_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            inst1_response.frameNStart = frameN  # exact frame index
            inst1_response.tStart = t  # local t and not account for scr refresh
            inst1_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst1_response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1_response.started')
            # update status
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
                inst1_response.duration = _inst1_response_allKeys[-1].duration
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
        for thisComponent in inst_acq1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "inst_acq1" ---
    for thisComponent in inst_acq1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if inst1_response.keys in ['', [], None]:  # No response was made
        inst1_response.keys = None
    trials.addData('inst1_response.keys',inst1_response.keys)
    if inst1_response.keys != None:  # we had a response
        trials.addData('inst1_response.rt', inst1_response.rt)
        trials.addData('inst1_response.duration', inst1_response.duration)
    # the Routine "inst_acq1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "inst_acq2" ---
    continueRoutine = True
    # update component parameters for each repeat
    inst2_response.keys = []
    inst2_response.rt = []
    _inst2_response_allKeys = []
    # keep track of which components have finished
    inst_acq2Components = [inst2, inst2_response]
    for thisComponent in inst_acq2Components:
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
    
    # --- Run Routine "inst_acq2" ---
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
        if inst2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            inst2.frameNStart = frameN  # exact frame index
            inst2.tStart = t  # local t and not account for scr refresh
            inst2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2.started')
            # update status
            inst2.status = STARTED
            inst2.setAutoDraw(True)
        
        # if inst2 is active this frame...
        if inst2.status == STARTED:
            # update params
            pass
        
        # *inst2_response* updates
        waitOnFlip = False
        
        # if inst2_response is starting this frame...
        if inst2_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            inst2_response.frameNStart = frameN  # exact frame index
            inst2_response.tStart = t  # local t and not account for scr refresh
            inst2_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst2_response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2_response.started')
            # update status
            inst2_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(inst2_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(inst2_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if inst2_response.status == STARTED and not waitOnFlip:
            theseKeys = inst2_response.getKeys(keyList=['space'], waitRelease=False)
            _inst2_response_allKeys.extend(theseKeys)
            if len(_inst2_response_allKeys):
                inst2_response.keys = _inst2_response_allKeys[-1].name  # just the last key pressed
                inst2_response.rt = _inst2_response_allKeys[-1].rt
                inst2_response.duration = _inst2_response_allKeys[-1].duration
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
        for thisComponent in inst_acq2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "inst_acq2" ---
    for thisComponent in inst_acq2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if inst2_response.keys in ['', [], None]:  # No response was made
        inst2_response.keys = None
    trials.addData('inst2_response.keys',inst2_response.keys)
    if inst2_response.keys != None:  # we had a response
        trials.addData('inst2_response.rt', inst2_response.rt)
        trials.addData('inst2_response.duration', inst2_response.duration)
    # the Routine "inst_acq2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "inst_acq3" ---
    continueRoutine = True
    # update component parameters for each repeat
    inst1_response_2.keys = []
    inst1_response_2.rt = []
    _inst1_response_2_allKeys = []
    # keep track of which components have finished
    inst_acq3Components = [inst1_2, inst1_response_2]
    for thisComponent in inst_acq3Components:
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
    
    # --- Run Routine "inst_acq3" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *inst1_2* updates
        
        # if inst1_2 is starting this frame...
        if inst1_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            inst1_2.frameNStart = frameN  # exact frame index
            inst1_2.tStart = t  # local t and not account for scr refresh
            inst1_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst1_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1_2.started')
            # update status
            inst1_2.status = STARTED
            inst1_2.setAutoDraw(True)
        
        # if inst1_2 is active this frame...
        if inst1_2.status == STARTED:
            # update params
            pass
        
        # *inst1_response_2* updates
        waitOnFlip = False
        
        # if inst1_response_2 is starting this frame...
        if inst1_response_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            inst1_response_2.frameNStart = frameN  # exact frame index
            inst1_response_2.tStart = t  # local t and not account for scr refresh
            inst1_response_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst1_response_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1_response_2.started')
            # update status
            inst1_response_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(inst1_response_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(inst1_response_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if inst1_response_2.status == STARTED and not waitOnFlip:
            theseKeys = inst1_response_2.getKeys(keyList=['space'], waitRelease=False)
            _inst1_response_2_allKeys.extend(theseKeys)
            if len(_inst1_response_2_allKeys):
                inst1_response_2.keys = _inst1_response_2_allKeys[-1].name  # just the last key pressed
                inst1_response_2.rt = _inst1_response_2_allKeys[-1].rt
                inst1_response_2.duration = _inst1_response_2_allKeys[-1].duration
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
        for thisComponent in inst_acq3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "inst_acq3" ---
    for thisComponent in inst_acq3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if inst1_response_2.keys in ['', [], None]:  # No response was made
        inst1_response_2.keys = None
    trials.addData('inst1_response_2.keys',inst1_response_2.keys)
    if inst1_response_2.keys != None:  # we had a response
        trials.addData('inst1_response_2.rt', inst1_response_2.rt)
        trials.addData('inst1_response_2.duration', inst1_response_2.duration)
    # the Routine "inst_acq3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "sliderdemo" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_demo_2
    # initiate old rating as 50
    oldRating = 50
    
    # set start position of the slider to end position of the previous trial
    marker_position = (0,-0.35)
    
    # record the current position of the mouse
    mouseRec=mouse_cond.getPos()
    first = 1
    slider_rt = 999
    exp_rating = 999
    exp_rating_all = list()
    exp_rt_all = list()
    
    
    
    slider0l_d.reset()
    slider0r_d.reset()
    # setup some python lists for storing info about the mouse_d
    gotValidClick = False  # until a click is received
    resp_demo.keys = []
    resp_demo.rt = []
    _resp_demo_allKeys = []
    # keep track of which components have finished
    sliderdemoComponents = [sliderright, sliderleft, instdemo, shape_demo, slider0l_d, expect0_d, slider0r_d, markerdemo, mouse_d, resp_demo]
    for thisComponent in sliderdemoComponents:
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
    
    # --- Run Routine "sliderdemo" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_demo_2
        #mouse_d, first, mouseRec, slider_shaped
        # first = 0 or 1, mouseRec as updated rating, mouse0 as initial location,slidershape as where the slider is
        marker_position, mouseRec, first, slider_rt, exp_rating, exp_rating_all, exp_rt_all = getmarker(mouse_cond, first, mouseRec, shape_cond, slider_rt, exp_rating, marker_position, exp_rating_all, exp_rt_all)
        
        # *sliderright* updates
        
        # if sliderright is starting this frame...
        if sliderright.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderright.frameNStart = frameN  # exact frame index
            sliderright.tStart = t  # local t and not account for scr refresh
            sliderright.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderright, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderright.started')
            # update status
            sliderright.status = STARTED
            sliderright.setAutoDraw(True)
        
        # if sliderright is active this frame...
        if sliderright.status == STARTED:
            # update params
            pass
        
        # *sliderleft* updates
        
        # if sliderleft is starting this frame...
        if sliderleft.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderleft.frameNStart = frameN  # exact frame index
            sliderleft.tStart = t  # local t and not account for scr refresh
            sliderleft.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderleft, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderleft.started')
            # update status
            sliderleft.status = STARTED
            sliderleft.setAutoDraw(True)
        
        # if sliderleft is active this frame...
        if sliderleft.status == STARTED:
            # update params
            pass
        
        # *instdemo* updates
        
        # if instdemo is starting this frame...
        if instdemo.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instdemo.frameNStart = frameN  # exact frame index
            instdemo.tStart = t  # local t and not account for scr refresh
            instdemo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instdemo, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instdemo.started')
            # update status
            instdemo.status = STARTED
            instdemo.setAutoDraw(True)
        
        # if instdemo is active this frame...
        if instdemo.status == STARTED:
            # update params
            pass
        
        # *shape_demo* updates
        
        # if shape_demo is starting this frame...
        if shape_demo.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            shape_demo.frameNStart = frameN  # exact frame index
            shape_demo.tStart = t  # local t and not account for scr refresh
            shape_demo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(shape_demo, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'shape_demo.started')
            # update status
            shape_demo.status = STARTED
            shape_demo.setAutoDraw(True)
        
        # if shape_demo is active this frame...
        if shape_demo.status == STARTED:
            # update params
            pass
        
        # *slider0l_d* updates
        
        # if slider0l_d is starting this frame...
        if slider0l_d.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            slider0l_d.frameNStart = frameN  # exact frame index
            slider0l_d.tStart = t  # local t and not account for scr refresh
            slider0l_d.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(slider0l_d, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'slider0l_d.started')
            # update status
            slider0l_d.status = STARTED
            slider0l_d.setAutoDraw(True)
        
        # if slider0l_d is active this frame...
        if slider0l_d.status == STARTED:
            # update params
            pass
        
        # *expect0_d* updates
        
        # if expect0_d is starting this frame...
        if expect0_d.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            expect0_d.frameNStart = frameN  # exact frame index
            expect0_d.tStart = t  # local t and not account for scr refresh
            expect0_d.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(expect0_d, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'expect0_d.started')
            # update status
            expect0_d.status = STARTED
            expect0_d.setAutoDraw(True)
        
        # if expect0_d is active this frame...
        if expect0_d.status == STARTED:
            # update params
            pass
        
        # *slider0r_d* updates
        
        # if slider0r_d is starting this frame...
        if slider0r_d.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            slider0r_d.frameNStart = frameN  # exact frame index
            slider0r_d.tStart = t  # local t and not account for scr refresh
            slider0r_d.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(slider0r_d, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'slider0r_d.started')
            # update status
            slider0r_d.status = STARTED
            slider0r_d.setAutoDraw(True)
        
        # if slider0r_d is active this frame...
        if slider0r_d.status == STARTED:
            # update params
            pass
        
        # *markerdemo* updates
        
        # if markerdemo is starting this frame...
        if markerdemo.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            markerdemo.frameNStart = frameN  # exact frame index
            markerdemo.tStart = t  # local t and not account for scr refresh
            markerdemo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(markerdemo, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'markerdemo.started')
            # update status
            markerdemo.status = STARTED
            markerdemo.setAutoDraw(True)
        
        # if markerdemo is active this frame...
        if markerdemo.status == STARTED:
            # update params
            markerdemo.setPos(marker_position, log=False)
        # *mouse_d* updates
        
        # if mouse_d is starting this frame...
        if mouse_d.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_d.frameNStart = frameN  # exact frame index
            mouse_d.tStart = t  # local t and not account for scr refresh
            mouse_d.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_d, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_d.started', t)
            # update status
            mouse_d.status = STARTED
            mouse_d.mouseClock.reset()
            prevButtonState = [0, 0, 0]  # if now button is down we will treat as 'new' click
        
        # *resp_demo* updates
        waitOnFlip = False
        
        # if resp_demo is starting this frame...
        if resp_demo.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            resp_demo.frameNStart = frameN  # exact frame index
            resp_demo.tStart = t  # local t and not account for scr refresh
            resp_demo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resp_demo, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'resp_demo.started')
            # update status
            resp_demo.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resp_demo.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resp_demo.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resp_demo.status == STARTED and not waitOnFlip:
            theseKeys = resp_demo.getKeys(keyList=['space'], waitRelease=False)
            _resp_demo_allKeys.extend(theseKeys)
            if len(_resp_demo_allKeys):
                resp_demo.keys = _resp_demo_allKeys[-1].name  # just the last key pressed
                resp_demo.rt = _resp_demo_allKeys[-1].rt
                resp_demo.duration = _resp_demo_allKeys[-1].duration
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
        for thisComponent in sliderdemoComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "sliderdemo" ---
    for thisComponent in sliderdemoComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_demo_2
    
    
    
    # store data for trials (TrialHandler)
    # check responses
    if resp_demo.keys in ['', [], None]:  # No response was made
        resp_demo.keys = None
    trials.addData('resp_demo.keys',resp_demo.keys)
    if resp_demo.keys != None:  # we had a response
        trials.addData('resp_demo.rt', resp_demo.rt)
        trials.addData('resp_demo.duration', resp_demo.duration)
    # the Routine "sliderdemo" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "inst_acq4" ---
    continueRoutine = True
    # update component parameters for each repeat
    inst4_response.keys = []
    inst4_response.rt = []
    _inst4_response_allKeys = []
    # keep track of which components have finished
    inst_acq4Components = [inst4, inst4_response]
    for thisComponent in inst_acq4Components:
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
    
    # --- Run Routine "inst_acq4" ---
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
        if inst4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            inst4.frameNStart = frameN  # exact frame index
            inst4.tStart = t  # local t and not account for scr refresh
            inst4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4.started')
            # update status
            inst4.status = STARTED
            inst4.setAutoDraw(True)
        
        # if inst4 is active this frame...
        if inst4.status == STARTED:
            # update params
            pass
        
        # *inst4_response* updates
        waitOnFlip = False
        
        # if inst4_response is starting this frame...
        if inst4_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            inst4_response.frameNStart = frameN  # exact frame index
            inst4_response.tStart = t  # local t and not account for scr refresh
            inst4_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst4_response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4_response.started')
            # update status
            inst4_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(inst4_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(inst4_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if inst4_response.status == STARTED and not waitOnFlip:
            theseKeys = inst4_response.getKeys(keyList=['space'], waitRelease=False)
            _inst4_response_allKeys.extend(theseKeys)
            if len(_inst4_response_allKeys):
                inst4_response.keys = _inst4_response_allKeys[-1].name  # just the last key pressed
                inst4_response.rt = _inst4_response_allKeys[-1].rt
                inst4_response.duration = _inst4_response_allKeys[-1].duration
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
        for thisComponent in inst_acq4Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "inst_acq4" ---
    for thisComponent in inst_acq4Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if inst4_response.keys in ['', [], None]:  # No response was made
        inst4_response.keys = None
    trials.addData('inst4_response.keys',inst4_response.keys)
    if inst4_response.keys != None:  # we had a response
        trials.addData('inst4_response.rt', inst4_response.rt)
        trials.addData('inst4_response.duration', inst4_response.duration)
    # the Routine "inst_acq4" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "inst_acq5" ---
    continueRoutine = True
    # update component parameters for each repeat
    inst5_response.keys = []
    inst5_response.rt = []
    _inst5_response_allKeys = []
    # keep track of which components have finished
    inst_acq5Components = [inst5, inst5_response]
    for thisComponent in inst_acq5Components:
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
    
    # --- Run Routine "inst_acq5" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *inst5* updates
        
        # if inst5 is starting this frame...
        if inst5.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            inst5.frameNStart = frameN  # exact frame index
            inst5.tStart = t  # local t and not account for scr refresh
            inst5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst5.started')
            # update status
            inst5.status = STARTED
            inst5.setAutoDraw(True)
        
        # if inst5 is active this frame...
        if inst5.status == STARTED:
            # update params
            pass
        
        # *inst5_response* updates
        waitOnFlip = False
        
        # if inst5_response is starting this frame...
        if inst5_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            inst5_response.frameNStart = frameN  # exact frame index
            inst5_response.tStart = t  # local t and not account for scr refresh
            inst5_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(inst5_response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst5_response.started')
            # update status
            inst5_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(inst5_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(inst5_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if inst5_response.status == STARTED and not waitOnFlip:
            theseKeys = inst5_response.getKeys(keyList=['space'], waitRelease=False)
            _inst5_response_allKeys.extend(theseKeys)
            if len(_inst5_response_allKeys):
                inst5_response.keys = _inst5_response_allKeys[-1].name  # just the last key pressed
                inst5_response.rt = _inst5_response_allKeys[-1].rt
                inst5_response.duration = _inst5_response_allKeys[-1].duration
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
        for thisComponent in inst_acq5Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "inst_acq5" ---
    for thisComponent in inst_acq5Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if inst5_response.keys in ['', [], None]:  # No response was made
        inst5_response.keys = None
    trials.addData('inst5_response.keys',inst5_response.keys)
    if inst5_response.keys != None:  # we had a response
        trials.addData('inst5_response.rt', inst5_response.rt)
        trials.addData('inst5_response.duration', inst5_response.duration)
    # the Routine "inst_acq5" was not non-slip safe, so reset the non-slip timer
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
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 2.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *cross_start* updates
    
    # if cross_start is starting this frame...
    if cross_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        cross_start.frameNStart = frameN  # exact frame index
        cross_start.tStart = t  # local t and not account for scr refresh
        cross_start.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cross_start, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'cross_start.started')
        # update status
        cross_start.status = STARTED
        cross_start.setAutoDraw(True)
    
    # if cross_start is active this frame...
    if cross_start.status == STARTED:
        # update params
        pass
    
    # if cross_start is stopping this frame...
    if cross_start.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross_start.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            cross_start.tStop = t  # not accounting for scr refresh
            cross_start.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_start.stopped')
            # update status
            cross_start.status = FINISHED
            cross_start.setAutoDraw(False)
    
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
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-2.000000)

# set up handler to look after randomisation of conditions etc
conditioning_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f"data/{bidsID}/{bidsID}_ses-1_task-conditioning_events-input.xlsx"),
    seed=None, name='conditioning_trials')
thisExp.addLoop(conditioning_trials)  # add the loop to the experiment
thisConditioning_trial = conditioning_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisConditioning_trial.rgb)
if thisConditioning_trial != None:
    for paramName in thisConditioning_trial:
        exec('{} = thisConditioning_trial[paramName]'.format(paramName))

for thisConditioning_trial in conditioning_trials:
    currentLoop = conditioning_trials
    # abbreviate parameter names if possible (e.g. rgb = thisConditioning_trial.rgb)
    if thisConditioning_trial != None:
        for paramName in thisConditioning_trial:
            exec('{} = thisConditioning_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "conditioning" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_cond
    #send the event code
    stim_marker('onset',SHOCK=False)
    thisExp.timestampOnFlip(win, 'stim_onset')
    
    # initiate old rating as 50
    oldRating = 50
    
    # set start position of the slider to end position of the previous trial
    marker_position = (0,-0.35)
    
    # record the current position of the mouse
    mouseRec=mouse_cond.getPos()
    first = 1
    slider_rt = 999
    exp_rating = 999
    exp_rating_all = list()
    exp_rt_all = list()
    
    
    
    img_cond.setPos(location)
    img_cond.setImage(path)
    sliderl_cond.reset()
    sliderr_cond.reset()
    # setup some python lists for storing info about the mouse_cond
    gotValidClick = False  # until a click is received
    # Run 'Begin Routine' code from FPS_control
    # create sound if FPS == 1
    # preschedule sound object
    flag = 0
    if FPS == 1:
        now = ptb.GetSecs()
        mySound = sound.Sound('stimuli/calibrationprobe1.wav', stereo=True, hamming=False, name='mySound')
        mySound.setVolume(1)
        FPSstart = now+FPS_timing
        thisExp.addData('FPSstart', routineTimer.getTime())
        mySound.play(when=FPSstart)
    
    
    
    
    # keep track of which components have finished
    conditioningComponents = [textr_cond, img_cond, textl_cond, shape_cond, sliderl_cond, expect_cond, sliderr_cond, marker_cond, mouse_cond]
    for thisComponent in conditioningComponents:
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
    
    # --- Run Routine "conditioning" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_cond
        #mouse_d, first, mouseRec, slider_shaped
        # first = 0 or 1, mouseRec as updated rating, mouse0 as initial location,slidershape as where the slider is
        marker_position, mouseRec, first, slider_rt, exp_rating, exp_rating_all, exp_rt_all = getmarker(mouse_cond, first, mouseRec, shape_cond, slider_rt, exp_rating, marker_position, exp_rating_all, exp_rt_all)
        
        
        
        
        
        
        
        # *textr_cond* updates
        
        # if textr_cond is starting this frame...
        if textr_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textr_cond.frameNStart = frameN  # exact frame index
            textr_cond.tStart = t  # local t and not account for scr refresh
            textr_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textr_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textr_cond.started')
            # update status
            textr_cond.status = STARTED
            textr_cond.setAutoDraw(True)
        
        # if textr_cond is active this frame...
        if textr_cond.status == STARTED:
            # update params
            pass
        
        # if textr_cond is stopping this frame...
        if textr_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textr_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                textr_cond.tStop = t  # not accounting for scr refresh
                textr_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textr_cond.stopped')
                # update status
                textr_cond.status = FINISHED
                textr_cond.setAutoDraw(False)
        
        # *img_cond* updates
        
        # if img_cond is starting this frame...
        if img_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            img_cond.frameNStart = frameN  # exact frame index
            img_cond.tStart = t  # local t and not account for scr refresh
            img_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(img_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'img_cond.started')
            # update status
            img_cond.status = STARTED
            img_cond.setAutoDraw(True)
        
        # if img_cond is active this frame...
        if img_cond.status == STARTED:
            # update params
            pass
        
        # if img_cond is stopping this frame...
        if img_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > img_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                img_cond.tStop = t  # not accounting for scr refresh
                img_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'img_cond.stopped')
                # update status
                img_cond.status = FINISHED
                img_cond.setAutoDraw(False)
        
        # *textl_cond* updates
        
        # if textl_cond is starting this frame...
        if textl_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textl_cond.frameNStart = frameN  # exact frame index
            textl_cond.tStart = t  # local t and not account for scr refresh
            textl_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textl_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textl_cond.started')
            # update status
            textl_cond.status = STARTED
            textl_cond.setAutoDraw(True)
        
        # if textl_cond is active this frame...
        if textl_cond.status == STARTED:
            # update params
            pass
        
        # if textl_cond is stopping this frame...
        if textl_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textl_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                textl_cond.tStop = t  # not accounting for scr refresh
                textl_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textl_cond.stopped')
                # update status
                textl_cond.status = FINISHED
                textl_cond.setAutoDraw(False)
        
        # *shape_cond* updates
        
        # if shape_cond is starting this frame...
        if shape_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            shape_cond.frameNStart = frameN  # exact frame index
            shape_cond.tStart = t  # local t and not account for scr refresh
            shape_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(shape_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'shape_cond.started')
            # update status
            shape_cond.status = STARTED
            shape_cond.setAutoDraw(True)
        
        # if shape_cond is active this frame...
        if shape_cond.status == STARTED:
            # update params
            pass
        
        # if shape_cond is stopping this frame...
        if shape_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > shape_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                shape_cond.tStop = t  # not accounting for scr refresh
                shape_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'shape_cond.stopped')
                # update status
                shape_cond.status = FINISHED
                shape_cond.setAutoDraw(False)
        
        # *sliderl_cond* updates
        
        # if sliderl_cond is starting this frame...
        if sliderl_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderl_cond.frameNStart = frameN  # exact frame index
            sliderl_cond.tStart = t  # local t and not account for scr refresh
            sliderl_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderl_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderl_cond.started')
            # update status
            sliderl_cond.status = STARTED
            sliderl_cond.setAutoDraw(True)
        
        # if sliderl_cond is active this frame...
        if sliderl_cond.status == STARTED:
            # update params
            pass
        
        # if sliderl_cond is stopping this frame...
        if sliderl_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sliderl_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                sliderl_cond.tStop = t  # not accounting for scr refresh
                sliderl_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sliderl_cond.stopped')
                # update status
                sliderl_cond.status = FINISHED
                sliderl_cond.setAutoDraw(False)
        
        # *expect_cond* updates
        
        # if expect_cond is starting this frame...
        if expect_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            expect_cond.frameNStart = frameN  # exact frame index
            expect_cond.tStart = t  # local t and not account for scr refresh
            expect_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(expect_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'expect_cond.started')
            # update status
            expect_cond.status = STARTED
            expect_cond.setAutoDraw(True)
        
        # if expect_cond is active this frame...
        if expect_cond.status == STARTED:
            # update params
            pass
        
        # if expect_cond is stopping this frame...
        if expect_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > expect_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                expect_cond.tStop = t  # not accounting for scr refresh
                expect_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'expect_cond.stopped')
                # update status
                expect_cond.status = FINISHED
                expect_cond.setAutoDraw(False)
        
        # *sliderr_cond* updates
        
        # if sliderr_cond is starting this frame...
        if sliderr_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderr_cond.frameNStart = frameN  # exact frame index
            sliderr_cond.tStart = t  # local t and not account for scr refresh
            sliderr_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderr_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderr_cond.started')
            # update status
            sliderr_cond.status = STARTED
            sliderr_cond.setAutoDraw(True)
        
        # if sliderr_cond is active this frame...
        if sliderr_cond.status == STARTED:
            # update params
            pass
        
        # if sliderr_cond is stopping this frame...
        if sliderr_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sliderr_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                sliderr_cond.tStop = t  # not accounting for scr refresh
                sliderr_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sliderr_cond.stopped')
                # update status
                sliderr_cond.status = FINISHED
                sliderr_cond.setAutoDraw(False)
        
        # *marker_cond* updates
        
        # if marker_cond is starting this frame...
        if marker_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            marker_cond.frameNStart = frameN  # exact frame index
            marker_cond.tStart = t  # local t and not account for scr refresh
            marker_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(marker_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'marker_cond.started')
            # update status
            marker_cond.status = STARTED
            marker_cond.setAutoDraw(True)
        
        # if marker_cond is active this frame...
        if marker_cond.status == STARTED:
            # update params
            marker_cond.setPos(marker_position, log=False)
        
        # if marker_cond is stopping this frame...
        if marker_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > marker_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                marker_cond.tStop = t  # not accounting for scr refresh
                marker_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'marker_cond.stopped')
                # update status
                marker_cond.status = FINISHED
                marker_cond.setAutoDraw(False)
        # *mouse_cond* updates
        
        # if mouse_cond is starting this frame...
        if mouse_cond.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_cond.frameNStart = frameN  # exact frame index
            mouse_cond.tStart = t  # local t and not account for scr refresh
            mouse_cond.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_cond, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_cond.started', t)
            # update status
            mouse_cond.status = STARTED
            mouse_cond.mouseClock.reset()
            prevButtonState = [0, 0, 0]  # if now button is down we will treat as 'new' click
        
        # if mouse_cond is stopping this frame...
        if mouse_cond.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mouse_cond.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                mouse_cond.tStop = t  # not accounting for scr refresh
                mouse_cond.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('mouse_cond.stopped', t)
                # update status
                mouse_cond.status = FINISHED
        # Run 'Each Frame' code from FPS_control
        if FPS == 1:
            if flag == 0 and ptb.GetSecs() >= FPSstart:
                FPS_marker()
                thisExp.addData('FPStrigger', routineTimer.getTime())
                flag = 1
        
        
        
        
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
        for thisComponent in conditioningComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "conditioning" ---
    for thisComponent in conditioningComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_cond
    stim_marker('offset',SHOCK=bool(int(us))) #deliver shock if need be
    #save the offset time
    thisExp.addData('CS_duration', t)
    
    # thisExp.addData('routineTiming', routineTimer.getTime())
    if exp_rating != 999:
        thisExp.addData('exp_rating_final', exp_rating)
        
    # will throw an error if subject didn't move
    if slider_rt != 999:
        thisExp.addData('exp_rt_final', slider_rt)
    
    
    thisExp.addData('exp_rating_all', exp_rating_all)
    thisExp.addData('exp_rt_all', exp_rt_all)
    
    
    
    # store data for conditioning_trials (TrialHandler)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
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
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *cross_2* updates
        
        # if cross_2 is starting this frame...
        if cross_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cross_2.frameNStart = frameN  # exact frame index
            cross_2.tStart = t  # local t and not account for scr refresh
            cross_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cross_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'cross_2.started')
            # update status
            cross_2.status = STARTED
            cross_2.setAutoDraw(True)
        
        # if cross_2 is active this frame...
        if cross_2.status == STARTED:
            # update params
            pass
        
        # if cross_2 is stopping this frame...
        if cross_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > cross_2.tStartRefresh + iti-frameTolerance:
                # keep track of stop time/frame for later
                cross_2.tStop = t  # not accounting for scr refresh
                cross_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cross_2.stopped')
                # update status
                cross_2.status = FINISHED
                cross_2.setAutoDraw(False)
        
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
    # Run 'End Routine' code from iti_code_2
    thisExp.addData('iti_duration', routineTimer.getTime())
    
    
    
    # the Routine "iti" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'conditioning_trials'


# --- Prepare to start Routine "breaktime" ---
continueRoutine = True
# update component parameters for each repeat
inst1_response_5.keys = []
inst1_response_5.rt = []
_inst1_response_5_allKeys = []
# keep track of which components have finished
breaktimeComponents = [inst_break, inst1_response_5]
for thisComponent in breaktimeComponents:
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

# --- Run Routine "breaktime" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst_break* updates
    
    # if inst_break is starting this frame...
    if inst_break.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        inst_break.frameNStart = frameN  # exact frame index
        inst_break.tStart = t  # local t and not account for scr refresh
        inst_break.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst_break, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst_break.started')
        # update status
        inst_break.status = STARTED
        inst_break.setAutoDraw(True)
    
    # if inst_break is active this frame...
    if inst_break.status == STARTED:
        # update params
        pass
    
    # *inst1_response_5* updates
    waitOnFlip = False
    
    # if inst1_response_5 is starting this frame...
    if inst1_response_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst1_response_5.frameNStart = frameN  # exact frame index
        inst1_response_5.tStart = t  # local t and not account for scr refresh
        inst1_response_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1_response_5, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1_response_5.started')
        # update status
        inst1_response_5.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst1_response_5.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst1_response_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst1_response_5.status == STARTED and not waitOnFlip:
        theseKeys = inst1_response_5.getKeys(keyList=['space'], waitRelease=False)
        _inst1_response_5_allKeys.extend(theseKeys)
        if len(_inst1_response_5_allKeys):
            inst1_response_5.keys = _inst1_response_5_allKeys[-1].name  # just the last key pressed
            inst1_response_5.rt = _inst1_response_5_allKeys[-1].rt
            inst1_response_5.duration = _inst1_response_5_allKeys[-1].duration
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
    for thisComponent in breaktimeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "breaktime" ---
for thisComponent in breaktimeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst1_response_5.keys in ['', [], None]:  # No response was made
    inst1_response_5.keys = None
thisExp.addData('inst1_response_5.keys',inst1_response_5.keys)
if inst1_response_5.keys != None:  # we had a response
    thisExp.addData('inst1_response_5.rt', inst1_response_5.rt)
    thisExp.addData('inst1_response_5.duration', inst1_response_5.duration)
thisExp.nextEntry()
# the Routine "breaktime" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
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
