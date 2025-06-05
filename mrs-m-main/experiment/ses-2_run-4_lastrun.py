#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.1),
    on March 08, 2024, at 13:57
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
import pandas as pd
import os

expName = 'arouval'  # from the Builder filename that created this script
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-MM')[-1]) for i in os.listdir('data') if 'sub-MM' in i])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-MM{0:0=3d}'.format(int(expInfo['participant']))

home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', bidsID)
input_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'stims')
os.chdir(data_dir)

#RENEWAL STIMS
renewal_input = pd.read_csv(f'{bidsID}_ses-2_task-renewal_events-input.csv')
renewal_stims = renewal_input['stimulus'].values
renewal_stims_trials_phase = renewal_input[['stimulus', 'trial', 'trial_type']].drop(labels=0)
renewal_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
renewal_stims_trials_phase['phase'] = 'renewal'
print(renewal_stims_trials_phase)

#BASE STIMS 
base_input = pd.read_csv(f'{bidsID}_ses-1_task-base_events-input.csv')
base_stims = base_input['stimulus'].values
base_stims_trials_phase = base_input[['stimulus', 'trial', 'trial_type']]
base_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
base_stims_trials_phase['phase'] = 'base'
print(base_stims_trials_phase)

#FEAR STIMS
fear_input = pd.read_csv(f'{bidsID}_ses-1_task-fear_events-input.csv')
fear_stims = fear_input['stimulus'].values
fear_stims_trials_phase = fear_input[['stimulus', 'trial', 'trial_type', 'us']] #Select these columns
fear_stims_trials_phase['phase'] = 'fear' #Create a column for the phase so I can keep them straight
#Drop the CSs that were shocked to:
fear_stims_trials_phase = fear_stims_trials_phase.set_index('us')
fear_stims_trials_phase = fear_stims_trials_phase.drop(index=1)
#Reset the index so that us isn't the index anymore
fear_stims_trials_phase = fear_stims_trials_phase.reset_index()
print(fear_stims_trials_phase)

#EXTCC STIMS 
extcc_input = pd.read_csv(f'{bidsID}_ses-1_task-extcc_events-input.csv')
extcc_stims = extcc_input['stimulus'].values
extcc_stims_trials_phase = extcc_input[['stimulus', 'trial', 'trial_type']]
extcc_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
extcc_stims_trials_phase['phase'] = 'extcc'
print(extcc_stims_trials_phase)


#RENEWAL: select the stims
renewal_stims_trials_phase = renewal_stims_trials_phase.set_index('trial_type')
renewal_stims_csm = renewal_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
renewal_stims_csp = renewal_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
renewal_stims = pd.concat([renewal_stims_csp, renewal_stims_csm])
print(renewal_stims)

base_stims_trials_phase = base_stims_trials_phase.set_index('trial_type')
base_stims_csm = base_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
base_stims_csp = base_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
base_stims = pd.concat([base_stims_csp, base_stims_csm])
print(base_stims)

fear_stims_trials_phase = fear_stims_trials_phase.set_index('trial_type')
fear_stims_csm = fear_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
fear_stims_csp = fear_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
fear_stims = pd.concat([fear_stims_csp, fear_stims_csm])
print(fear_stims)

extcc_stims_trials_phase = extcc_stims_trials_phase.set_index('trial_type')
extcc_stims_csm = extcc_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
extcc_stims_csp = extcc_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
extcc_stims = pd.concat([extcc_stims_csp, extcc_stims_csm])
print(extcc_stims)

all_stims = pd.concat([base_stims, fear_stims, extcc_stims, renewal_stims])
all_stims.rename(columns={'trial': 'original_trial'})
print(all_stims)

#FILL IN THE TEMPLATE WITH ALL MY STIMS 

#import the template 
arouval_df = pd.read_csv('../../task_templates/arouval_template.csv').set_index(['trial_type', 'phase'])
all_stims = all_stims.set_index(['trial_type', 'phase'])

for con in ['CS-', 'CS+']:
    for phase in ['base', 'fear', 'extcc', 'renewal']:
        arouval_df.loc[(con, phase), 'stimulus'] = all_stims.loc[(con, phase)]

arouval_df.reset_index()

arouval_df.to_csv(f'{bidsID}_ses-2_task-arouval_events-input.csv')


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.1'
expName = 'arouval'  # from the Builder filename that created this script
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
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\mrs-m\\experiment\\ses-2_run-4_lastrun.py',
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
    text='Before you go, we would like to ask you two last questions about the pictures that you saw on your first visit (i.e., these are all OLD pictures).\n\nSpecifically, we are going to ask you how much you LIKED the picture during the study (i.e. VALENCE) and \nhow AROUSED/ACTIVATED the picture made you feel during the study.\n\nPlease consider how you felt in response to seeing the image DURING the computerized task ONLY.\n\nPress SPACE to continue… ',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst1_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='VALENCE describes how much you like an image. Please click the dot that best describes how much you liked each image during the study.\n\nAROUSAL/ACTIVATION, in this case, is defined as feelings of attentiveness, alertness or activity. The opposite of arousal is boredom or relaxation. Arousal can often cause physiological changes such as increased heart rate. Please click the dot that best describes how aroused each image made you feel during the study.\n\nPress SPACE to continue...',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in7" ---
inst7 = visual.TextStim(win=win, name='inst7',
    text='You will provide your rating for both VALENCE and AROUSAL using a mouse and a scale. \n\nFor VALENCE, you can answer:\n\nStrongly disliked \nNeutral\nStrongly liked\n\nFor AROUSAL, you can answer: \n\nNot at all aroused \nSomewhat aroused \nVery aroused\n\nPlease do your best to ONLY consider your reactions to these types of images DURING the task, and not at other points in your life. \n\nAs with typicality in the last task, you can click anywhere on the scale to describe how you felt about the image on the screen during the task.\n\nPress SPACE to continue…\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst7_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in8" ---
inst8 = visual.TextStim(win=win, name='inst8',
    text='To recap: \n\nYou will see a picture that you saw on your first visit in the middle of the screen. You will first rate how much you LIKED or DISLIKED the picure during the study, on a scale of strongly disliked to strongly liked. You will then be asked to rate how AROUSED/ACTIVATED the same picture made you, on a scale of not at at all aroused to very aroused.\n\nDo you have any questions about these instructions?',
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

# --- Initialize components for Routine "prac_val" ---
pracval_image = visual.ImageStim(
    win=win,
    name='pracval_image', 
    image='stims/banana.jpg', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
pracval_resp = keyboard.Keyboard()
pracval_question = visual.TextStim(win=win, name='pracval_question',
    text='What was your level of VALENCE for this image?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
pracval_slider = visual.Slider(win=win, name='pracval_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Strongly disliked', 'Neutral', 'Strongly liked'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=0.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-3, readOnly=False)

# --- Initialize components for Routine "val_feedback" ---
valfeedback_resp = keyboard.Keyboard()
valfeedback_text = visual.TextStim(win=win, name='valfeedback_text',
    text='Great! The number you pressed should reflect how much you liked the image during the task. \n\nIf you have any questions about this task, ask your experimenter now. ',
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

# --- Initialize components for Routine "prac_arousal" ---
practyp_image = visual.ImageStim(
    win=win,
    name='practyp_image', 
    image='stims/banana.jpg', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
practyp_resp = keyboard.Keyboard()
practyp_question = visual.TextStim(win=win, name='practyp_question',
    text='What was your level of AROUSAL/ACTIVATION for this image?',
    font='Open Sans',
    pos=(0, 0.3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
practyp_slider = visual.Slider(win=win, name='practyp_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Not', 'Somewhat', 'Very'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-3, readOnly=False)

# --- Initialize components for Routine "arousal_feedback" ---
prac_arousal_resp = keyboard.Keyboard()
prac_arousal_text = visual.TextStim(win=win, name='prac_arousal_text',
    text='Great! \n\nYour answer should have reflected how physiologically aroused/activated the picture made you feel during the task. \n\nDo you have any questions about this task? If so, please ask your experimenter now.',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

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

# --- Initialize components for Routine "val" ---
val_pic = visual.ImageStim(
    win=win,
    name='val_pic', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
val_question = visual.TextStim(win=win, name='val_question',
    text='What was your level of VALENCE for this image?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
val_slider = visual.Slider(win=win, name='val_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Strongly disliked', 'Neutral', 'Strongly liked'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-2, readOnly=False)

# --- Initialize components for Routine "iti" ---
crosshair = visual.ImageStim(
    win=win,
    name='crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "arousal" ---
arousal_pic = visual.ImageStim(
    win=win,
    name='arousal_pic', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
arousal_question = visual.TextStim(win=win, name='arousal_question',
    text='What was your level of AROUSAL/ACTIVATION for this image?',
    font='Open Sans',
    pos=(0, .3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
arousal_slider = visual.Slider(win=win, name='arousal_slider',
    startValue=None, size=(0.6, 0.05), pos=(0, -0.325), units=None,
    labels=['Not aroused', 'Somewhat aroused', 'Very aroused'], ticks=(1, 2, 3, 4, 5, 6, 7), granularity=0.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.03,
    flip=False, ori=0.0, depth=-2, readOnly=False)

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

# --- Prepare to start Routine "in7" ---
continueRoutine = True
# update component parameters for each repeat
inst7_resp.keys = []
inst7_resp.rt = []
_inst7_resp_allKeys = []
# keep track of which components have finished
in7Components = [inst7, inst7_resp]
for thisComponent in in7Components:
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

# --- Run Routine "in7" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst7* updates
    if inst7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst7.frameNStart = frameN  # exact frame index
        inst7.tStart = t  # local t and not account for scr refresh
        inst7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst7, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst7.started')
        inst7.setAutoDraw(True)
    if inst7.status == STARTED:
        if bool(inst7_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst7.tStop = t  # not accounting for scr refresh
            inst7.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst7.stopped')
            inst7.setAutoDraw(False)
    
    # *inst7_resp* updates
    waitOnFlip = False
    if inst7_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst7_resp.frameNStart = frameN  # exact frame index
        inst7_resp.tStart = t  # local t and not account for scr refresh
        inst7_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst7_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst7_resp.started')
        inst7_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst7_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst7_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if inst7_resp.status == STARTED:
        if bool(inst7_resp.keys=='space'):
            # keep track of stop time/frame for later
            inst7_resp.tStop = t  # not accounting for scr refresh
            inst7_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst7_resp.stopped')
            inst7_resp.status = FINISHED
    if inst7_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst7_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst7_resp_allKeys.extend(theseKeys)
        if len(_inst7_resp_allKeys):
            inst7_resp.keys = _inst7_resp_allKeys[-1].name  # just the last key pressed
            inst7_resp.rt = _inst7_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in in7Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "in7" ---
for thisComponent in in7Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst7_resp.keys in ['', [], None]:  # No response was made
    inst7_resp.keys = None
thisExp.addData('inst7_resp.keys',inst7_resp.keys)
if inst7_resp.keys != None:  # we had a response
    thisExp.addData('inst7_resp.rt', inst7_resp.rt)
thisExp.nextEntry()
# the Routine "in7" was not non-slip safe, so reset the non-slip timer
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

# --- Prepare to start Routine "prac_val" ---
continueRoutine = True
# update component parameters for each repeat
pracval_resp.keys = []
pracval_resp.rt = []
_pracval_resp_allKeys = []
pracval_slider.reset()
# keep track of which components have finished
prac_valComponents = [pracval_image, pracval_resp, pracval_question, pracval_slider]
for thisComponent in prac_valComponents:
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

# --- Run Routine "prac_val" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *pracval_image* updates
    if pracval_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracval_image.frameNStart = frameN  # exact frame index
        pracval_image.tStart = t  # local t and not account for scr refresh
        pracval_image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracval_image, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'pracval_image.started')
        pracval_image.setAutoDraw(True)
    
    # *pracval_resp* updates
    waitOnFlip = False
    if pracval_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracval_resp.frameNStart = frameN  # exact frame index
        pracval_resp.tStart = t  # local t and not account for scr refresh
        pracval_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracval_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'pracval_resp.started')
        pracval_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(pracval_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(pracval_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if pracval_resp.status == STARTED and not waitOnFlip:
        theseKeys = pracval_resp.getKeys(keyList=['1','2','3','4','5','6','7'], waitRelease=False)
        _pracval_resp_allKeys.extend(theseKeys)
        if len(_pracval_resp_allKeys):
            pracval_resp.keys = _pracval_resp_allKeys[-1].name  # just the last key pressed
            pracval_resp.rt = _pracval_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *pracval_question* updates
    if pracval_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracval_question.frameNStart = frameN  # exact frame index
        pracval_question.tStart = t  # local t and not account for scr refresh
        pracval_question.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracval_question, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'pracval_question.started')
        pracval_question.setAutoDraw(True)
    
    # *pracval_slider* updates
    if pracval_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pracval_slider.frameNStart = frameN  # exact frame index
        pracval_slider.tStart = t  # local t and not account for scr refresh
        pracval_slider.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pracval_slider, 'tStartRefresh')  # time at next scr refresh
        pracval_slider.setAutoDraw(True)
    
    # Check pracval_slider for response to end routine
    if pracval_slider.getRating() is not None and pracval_slider.status == STARTED:
        continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prac_valComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_val" ---
for thisComponent in prac_valComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if pracval_resp.keys in ['', [], None]:  # No response was made
    pracval_resp.keys = None
thisExp.addData('pracval_resp.keys',pracval_resp.keys)
if pracval_resp.keys != None:  # we had a response
    thisExp.addData('pracval_resp.rt', pracval_resp.rt)
thisExp.nextEntry()
thisExp.addData('pracval_slider.response', pracval_slider.getRating())
thisExp.addData('pracval_slider.rt', pracval_slider.getRT())
# the Routine "prac_val" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "val_feedback" ---
continueRoutine = True
# update component parameters for each repeat
valfeedback_resp.keys = []
valfeedback_resp.rt = []
_valfeedback_resp_allKeys = []
# keep track of which components have finished
val_feedbackComponents = [valfeedback_resp, valfeedback_text]
for thisComponent in val_feedbackComponents:
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

# --- Run Routine "val_feedback" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *valfeedback_resp* updates
    waitOnFlip = False
    if valfeedback_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        valfeedback_resp.frameNStart = frameN  # exact frame index
        valfeedback_resp.tStart = t  # local t and not account for scr refresh
        valfeedback_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(valfeedback_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'valfeedback_resp.started')
        valfeedback_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(valfeedback_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(valfeedback_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if valfeedback_resp.status == STARTED:
        if bool(valfeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            valfeedback_resp.tStop = t  # not accounting for scr refresh
            valfeedback_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'valfeedback_resp.stopped')
            valfeedback_resp.status = FINISHED
    if valfeedback_resp.status == STARTED and not waitOnFlip:
        theseKeys = valfeedback_resp.getKeys(keyList=['space'], waitRelease=False)
        _valfeedback_resp_allKeys.extend(theseKeys)
        if len(_valfeedback_resp_allKeys):
            valfeedback_resp.keys = _valfeedback_resp_allKeys[-1].name  # just the last key pressed
            valfeedback_resp.rt = _valfeedback_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *valfeedback_text* updates
    if valfeedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        valfeedback_text.frameNStart = frameN  # exact frame index
        valfeedback_text.tStart = t  # local t and not account for scr refresh
        valfeedback_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(valfeedback_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'valfeedback_text.started')
        valfeedback_text.setAutoDraw(True)
    if valfeedback_text.status == STARTED:
        if bool(valfeedback_resp.keys=='space'):
            # keep track of stop time/frame for later
            valfeedback_text.tStop = t  # not accounting for scr refresh
            valfeedback_text.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'valfeedback_text.stopped')
            valfeedback_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in val_feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "val_feedback" ---
for thisComponent in val_feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if valfeedback_resp.keys in ['', [], None]:  # No response was made
    valfeedback_resp.keys = None
thisExp.addData('valfeedback_resp.keys',valfeedback_resp.keys)
if valfeedback_resp.keys != None:  # we had a response
    thisExp.addData('valfeedback_resp.rt', valfeedback_resp.rt)
thisExp.nextEntry()
# the Routine "val_feedback" was not non-slip safe, so reset the non-slip timer
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

# --- Prepare to start Routine "prac_arousal" ---
continueRoutine = True
# update component parameters for each repeat
practyp_resp.keys = []
practyp_resp.rt = []
_practyp_resp_allKeys = []
practyp_slider.reset()
# keep track of which components have finished
prac_arousalComponents = [practyp_image, practyp_resp, practyp_question, practyp_slider]
for thisComponent in prac_arousalComponents:
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

# --- Run Routine "prac_arousal" ---
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
    for thisComponent in prac_arousalComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prac_arousal" ---
for thisComponent in prac_arousalComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if practyp_resp.keys in ['', [], None]:  # No response was made
    practyp_resp.keys = None
thisExp.addData('practyp_resp.keys',practyp_resp.keys)
if practyp_resp.keys != None:  # we had a response
    thisExp.addData('practyp_resp.rt', practyp_resp.rt)
thisExp.nextEntry()
thisExp.addData('practyp_slider.response', practyp_slider.getRating())
thisExp.addData('practyp_slider.rt', practyp_slider.getRT())
# the Routine "prac_arousal" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "arousal_feedback" ---
continueRoutine = True
# update component parameters for each repeat
prac_arousal_resp.keys = []
prac_arousal_resp.rt = []
_prac_arousal_resp_allKeys = []
# keep track of which components have finished
arousal_feedbackComponents = [prac_arousal_resp, prac_arousal_text]
for thisComponent in arousal_feedbackComponents:
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

# --- Run Routine "arousal_feedback" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *prac_arousal_resp* updates
    waitOnFlip = False
    if prac_arousal_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        prac_arousal_resp.frameNStart = frameN  # exact frame index
        prac_arousal_resp.tStart = t  # local t and not account for scr refresh
        prac_arousal_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(prac_arousal_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'prac_arousal_resp.started')
        prac_arousal_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(prac_arousal_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(prac_arousal_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if prac_arousal_resp.status == STARTED and not waitOnFlip:
        theseKeys = prac_arousal_resp.getKeys(keyList=['space'], waitRelease=False)
        _prac_arousal_resp_allKeys.extend(theseKeys)
        if len(_prac_arousal_resp_allKeys):
            prac_arousal_resp.keys = _prac_arousal_resp_allKeys[-1].name  # just the last key pressed
            prac_arousal_resp.rt = _prac_arousal_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *prac_arousal_text* updates
    if prac_arousal_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        prac_arousal_text.frameNStart = frameN  # exact frame index
        prac_arousal_text.tStart = t  # local t and not account for scr refresh
        prac_arousal_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(prac_arousal_text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'prac_arousal_text.started')
        prac_arousal_text.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in arousal_feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "arousal_feedback" ---
for thisComponent in arousal_feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if prac_arousal_resp.keys in ['', [], None]:  # No response was made
    prac_arousal_resp.keys = None
thisExp.addData('prac_arousal_resp.keys',prac_arousal_resp.keys)
if prac_arousal_resp.keys != None:  # we had a response
    thisExp.addData('prac_arousal_resp.rt', prac_arousal_resp.rt)
thisExp.nextEntry()
# the Routine "arousal_feedback" was not non-slip safe, so reset the non-slip timer
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
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-2_task-arouval_events-input.csv'),
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
    
    # --- Prepare to start Routine "val" ---
    continueRoutine = True
    # update component parameters for each repeat
    val_pic.setImage(stimulus)
    val_slider.reset()
    # keep track of which components have finished
    valComponents = [val_pic, val_question, val_slider]
    for thisComponent in valComponents:
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
    
    # --- Run Routine "val" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *val_pic* updates
        if val_pic.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            val_pic.frameNStart = frameN  # exact frame index
            val_pic.tStart = t  # local t and not account for scr refresh
            val_pic.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(val_pic, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'val_pic.started')
            val_pic.setAutoDraw(True)
        
        # *val_question* updates
        if val_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            val_question.frameNStart = frameN  # exact frame index
            val_question.tStart = t  # local t and not account for scr refresh
            val_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(val_question, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'val_question.started')
            val_question.setAutoDraw(True)
        
        # *val_slider* updates
        if val_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            val_slider.frameNStart = frameN  # exact frame index
            val_slider.tStart = t  # local t and not account for scr refresh
            val_slider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(val_slider, 'tStartRefresh')  # time at next scr refresh
            val_slider.setAutoDraw(True)
        
        # Check val_slider for response to end routine
        if val_slider.getRating() is not None and val_slider.status == STARTED:
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in valComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "val" ---
    for thisComponent in valComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('val_slider.response', val_slider.getRating())
    trials.addData('val_slider.rt', val_slider.getRT())
    # the Routine "val" was not non-slip safe, so reset the non-slip timer
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
    
    # --- Prepare to start Routine "arousal" ---
    continueRoutine = True
    # update component parameters for each repeat
    arousal_pic.setImage(stimulus)
    arousal_slider.reset()
    # keep track of which components have finished
    arousalComponents = [arousal_pic, arousal_question, arousal_slider]
    for thisComponent in arousalComponents:
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
    
    # --- Run Routine "arousal" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *arousal_pic* updates
        if arousal_pic.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            arousal_pic.frameNStart = frameN  # exact frame index
            arousal_pic.tStart = t  # local t and not account for scr refresh
            arousal_pic.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(arousal_pic, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'arousal_pic.started')
            arousal_pic.setAutoDraw(True)
        
        # *arousal_question* updates
        if arousal_question.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            arousal_question.frameNStart = frameN  # exact frame index
            arousal_question.tStart = t  # local t and not account for scr refresh
            arousal_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(arousal_question, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'arousal_question.started')
            arousal_question.setAutoDraw(True)
        
        # *arousal_slider* updates
        if arousal_slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            arousal_slider.frameNStart = frameN  # exact frame index
            arousal_slider.tStart = t  # local t and not account for scr refresh
            arousal_slider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(arousal_slider, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'arousal_slider.started')
            arousal_slider.setAutoDraw(True)
        
        # Check arousal_slider for response to end routine
        if arousal_slider.getRating() is not None and arousal_slider.status == STARTED:
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in arousalComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "arousal" ---
    for thisComponent in arousalComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('arousal_slider.response', arousal_slider.getRating())
    trials.addData('arousal_slider.rt', arousal_slider.getRT())
    # the Routine "arousal" was not non-slip safe, so reset the non-slip timer
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
