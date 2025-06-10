#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.1),
    on June 14, 2022, at 13:44
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

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

from psychopy.parallel import ParallelPort
from subprocess import Popen
import time
import pandas as pd 
import os
import numpy as np 
import random

home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'Experiments', 'mrs-m', 'experiment', 'data')
input_dir = os.path.join(home_dir,'Desktop', 'Experiments', 'mrs-m', 'experiment', 'stims')
os.chdir(input_dir)

dlg = gui.Dlg(title = 'MM subject initialization')
dlg.addField('participant')
dlg.addField('CS_order', choices=['A','T'])
dlg.addField('phase_order_input', choices=[1,2,3,4,5,6])
dlg.addField('extcc', choices=['ext', 'cc'])
dlg.addField('room', choices =['VR', 'behavior']) #added 6/14
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
    
bidsID = 'sub-MM{0:0=3d}'.format(int(user_input[0]))
cs_order = user_input[1]
phase_order_input = user_input[2]
extcc_input = user_input[3]
room_input = user_input[4] #added 6/14


#PARALLEL PORT CODE

#BIO = True if user_input[4] == 'yes' else False
BIO = True if user_input[5] == 'yes' and user_input[4] == 'VR' else False #added 6/14
BIO2 = True if user_input[5] == 'yes' and user_input[4] == 'behavior' else False #added 6/14

if BIO:
    pport = ParallelPort(address='0xEFF8') #added 6/14
elif BIO2:
    pport = ParallelPort(address='0x3FE0') #added 6/14
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
      
#CREATE INPUT FILES CODE

cs_cats = {'CS+':'animals' if cs_order == 'A' else 'tools',
           'CS-':'tools' if cs_order == 'A' else 'animals'}
phase_order = {1:[1,2,3],
               2:[1,3,2], 
               3:[3,2,1], 
               4:[3,1,2], 
               5:[2,1,3], 
               6:[2,3,1]}

#create variables that are lists of my phases to be used for iteration later
phases = ['base','fear','extcc','renewal_1', 'mem_1','sou_typ_val_1']
day1_phases = ['base','fear','extcc']

#CREATE DAY 1 DATAFRAMES:

#create list of day 1 phases
day1_phases = ['base','fear','extcc']
#create dataframe of stims (the one with the 6 columns of 24 animals or tools)
stims = pd.read_csv('day1_stims_groups.csv')
day1_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns
day2_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again
soutypval_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again!
#read in the different task templates for each phase, and name them after each phase (using list comprehension)
day1_dfs = {phase: pd.read_csv(f'../task_templates/{phase}_template.csv').set_index(['trial_type', 'trial']) for phase in day1_phases}
itis = [5,6,7]

#for each phase (count them) in day 1 phases (base, fear, extcc):
for p, phase in enumerate(day1_phases):
    #and for each of CS+ and CS-:
        for con in ['CS+','CS-']:
        #find the stimulus column in each phase and for both CS+ and CS-, 
        #and fill it with either animals or tools from the day1_stims_groups csv, 
        #depending on the cs_cats relationship. Made sure all variables were in the code. 
            day1_dfs[phase].loc[con,'stimulus'] = day1_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values  
        #shuffle the itis and create a random set of 48    
        iti_blocks = [np.random.choice(itis, 8, replace=True) for i in range(6)]
        #put them all together into one list
        iti_blocks = np.concatenate(iti_blocks)
        #put the list into the iti_duration column in each dataframe
        #how do i select just a column.....?
        day1_dfs[phase].loc[:, 'iti_duration'] = iti_blocks
        #reset the indices
        day1_dfs[phase] = day1_dfs[phase].reset_index()
   
#FILL IN EXTINCTION CC STIMS 

cc_stims = pd.read_csv('cc_stims.csv') 
day1_dfs['extcc'] = day1_dfs['extcc'].set_index('cc')

#note that once it is the index, pandas will not recognize it as a column anymore!

if extcc_input == 'cc':
    day1_dfs['extcc'].loc[1, 'cc_stimulus'] = cc_stims.values
    day1_dfs['extcc'].loc[0, 'cc_stimulus'] = 'stims/transparent.png'
else:
    day1_dfs['extcc'].loc[[0,1], 'cc_stimulus'] = 'stims/transparent.png'
    
#RENEWAL 
 
renewal_stims = pd.read_csv('renewal_stims.csv')
renewal_stims = renewal_stims.sample(frac=1).reset_index(drop=True) #shuffle within columns 
renewal_df = pd.read_csv('../task_templates/renewal_template.csv').set_index(['trial_type', 'trial'])

for con in ['CS+', 'CS-']:
    renewal_df.loc[con, 'stimulus'] = renewal_stims[f'{cs_cats[con]}'].values

renewal_df.loc['new', 'stimulus'] = f'stims/tr1renewal_{cs_cats[con]}.jpg'  #assigns the first row named "new" with a novel and consistent pic of the subject's CS-...
renewal_df.loc['new', 'iti_duration'] = '5'  #assigns the first row named "new" with an iti of 5 seconds

#SET ITIs
itis = [5,6,7]
iti_blocks = [np.random.choice(itis, 6, replace=True) for i in range(4)]
#put them all together into one list
iti_blocks = np.concatenate(iti_blocks)
#put the list into the iti_duration column in each dataframe
#how do i select just a column.....?
renewal_df.loc[['CS+', 'CS-'], 'iti_duration'] = iti_blocks 
 
#RECOGNITION MEMORY
mem_df = pd.read_csv('../task_templates/mem_template.csv').set_index(['trial_type', 'phase'])

#SET REC. MEMORY ITI

mem_df.reset_index(['trial_type']) #changed this to fix but 6/9
itis_mem = [1,2]
iti_mem_blocks = [np.random.choice(itis_mem, 20, replace=True) for i in range(12)]
iti_mem_blocks = np.concatenate(iti_mem_blocks)
mem_df.loc[:, 'iti_duration'] = iti_mem_blocks

#add all same stims as day 1 except reshuffled, according to the same user input as on day 1.
for p, phase in enumerate(day1_phases):
    for con in ['CS+','CS-']:
            mem_df.loc[(con, phase), 'stimulus'] = day2_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values       
       
#LOAD REC. MEMORY FOIL STIMS
 
foil_stims = pd.read_csv('foil_stims_list.csv').sample(frac=1).reset_index(drop=True)

for con in ['CS+','CS-']:
    mem_df.loc[(con, 'foil'), 'stimulus'] = foil_stims[f'{cs_cats[con]}'].values
    
#SOUTYPVAL 

soutypval_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again!
soutypval_df = pd.read_csv('../task_templates/soutypval_template.csv').set_index(['trial_type', 'phase'])
#add all same stims as day 1 except reshuffled, according to the same user input as on day 1.
for p, phase in enumerate(day1_phases):
    for con in ['CS+','CS-']:
           soutypval_df.loc[(con, phase), 'stimulus'] = soutypval_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values       
       
os.chdir(data_dir)
os.makedirs(f'{bidsID}',exist_ok=True)
for phase in day1_phases:
  ses = 1
  phase_str = phase.split('_')[0]
  day1_dfs[phase].reset_index().to_csv(f'{bidsID}/{bidsID}_ses-{ses}_task-{phase_str}_events-input.csv',index=False)
 
renewal_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-renewal_events-input.csv',index=False)
mem_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-rec-memory_events-input.csv',index=False)
soutypval_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-soutypval_events-input.csv',index=False)






# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.1'
expName = 'baseline'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f'data/{bidsID}/{bidsID}_ses-1_task-{expName}_{expInfo["date"]}'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\dunsmoorlab\\Desktop\\mrs-m\\experiment\\ses-1_run-1.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# Setup ioHub
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

# Initialize components for Routine "in1"
in1Clock = core.Clock()
inst1_resp = keyboard.Keyboard()
inst1 = visual.TextStim(win=win, name='inst1',
    text='First, please make sure your cell phone is silenced. \n\nWe will be measuring how much you are sweating from the sensors on your hand. \n\nThese are very sensitive to movement and posture, so please sit up straight and do not shift around in your seat or move during the experiment. \n\nPress SPACE to continue... ',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "in2"
in2Clock = core.Clock()
inst2 = visual.TextStim(win=win, name='inst2',
    text='During this part of the experiment, you will see a picture of either an animal or tool. \nYou will see this picture for a few seconds.\n\nEach time you see a picture of an animal or tool, I want you to tell me which category you think the picture belongs to: \n\n1 = animals\n2 = tools\n\nPress SPACE to continue...\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_resp = keyboard.Keyboard()

# Initialize components for Routine "in3"
in3Clock = core.Clock()
inst3 = visual.TextStim(win=win, name='inst3',
    text='Please make a response for EVERY PICTURE. We are also measuring how fast you press the button. Please try to be as quick and accurate as possible.\n\nYou only need to press a button when you see a picture of an animal or tool.\n\nPress SPACE to see what this will look like: ',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst3_resp = keyboard.Keyboard()

# Initialize components for Routine "ex_iti"
ex_itiClock = core.Clock()
ex_fix_cross = visual.ShapeStim(
    win=win, name='ex_fix_cross', vertices='cross',
    size=(0.03, 0.03),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
ex_iti_resp = keyboard.Keyboard()
ex_animal_iti = visual.TextStim(win=win, name='ex_animal_iti',
    text='1\nanimals',
    font='Open Sans',
    pos=(-.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
ex_tool_iti = visual.TextStim(win=win, name='ex_tool_iti',
    text='2\ntools',
    font='Open Sans',
    pos=(.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "ex_trial"
ex_trialClock = core.Clock()
ex_trials_resp = keyboard.Keyboard()
ex_tool = visual.TextStim(win=win, name='ex_tool',
    text='2\ntools',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
ex_animal = visual.TextStim(win=win, name='ex_animal',
    text='1\nanimals',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
image = visual.ImageStim(
    win=win,
    name='image', 
    image='stims/dummystim.jpg', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)

# Initialize components for Routine "in4"
in4Clock = core.Clock()
inst4 = visual.TextStim(win=win, name='inst4',
    text='So, to recap:\n\nWhen you see a picture of an animal or a tool, press 1 or 2 to put the picture in its category. Please respond as quickly and as accurately as possible. Please make a response for every picture as soon as the picture appears on the screen.\n\nAny questions?\n',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_resp = keyboard.Keyboard()

# Initialize components for Routine "in_begin_experiment"
in_begin_experimentClock = core.Clock()
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='Press SPACE to begin the experiment.',
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
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
ani_iti = visual.TextStim(win=win, name='ani_iti',
    text='',
    font='Open Sans',
    pos=(-.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
tool_iti = visual.TextStim(win=win, name='tool_iti',
    text='2\ntools',
    font='Open Sans',
    pos=(.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "trial"
trialClock = core.Clock()
base_image = visual.ImageStim(
    win=win,
    name='base_image', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
trials_resp = keyboard.Keyboard()
animal = visual.TextStim(win=win, name='animal',
    text='1\nanimals\n',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
tool = visual.TextStim(win=win, name='tool',
    text='2\ntools\n',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);

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

# ------Prepare to start Routine "in1"-------
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
in1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in1"-------
while continueRoutine:
    # get current time
    t = in1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in1Clock)
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
            win.timeOnFlip(inst1_resp, 'tStopRefresh')  # time at next scr refresh
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
        inst1.setAutoDraw(True)
    if inst1.status == STARTED:
        if bool((inst1_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst1.tStop = t  # not accounting for scr refresh
            inst1.frameNStop = frameN  # exact frame index
            win.timeOnFlip(inst1, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in1"-------
for thisComponent in in1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if inst1_resp.keys in ['', [], None]:  # No response was made
    inst1_resp.keys = None
thisExp.addData('inst1_resp.keys',inst1_resp.keys)
if inst1_resp.keys != None:  # we had a response
    thisExp.addData('inst1_resp.rt', inst1_resp.rt)
thisExp.addData('inst1_resp.started', inst1_resp.tStartRefresh)
thisExp.addData('inst1_resp.stopped', inst1_resp.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('inst1.started', inst1.tStartRefresh)
thisExp.addData('inst1.stopped', inst1.tStopRefresh)
# the Routine "in1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "in2"-------
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
in2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in2"-------
while continueRoutine:
    # get current time
    t = in2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in2Clock)
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
        inst2.setAutoDraw(True)
    if inst2.status == STARTED:
        if bool((inst2_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2.tStop = t  # not accounting for scr refresh
            inst2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(inst2, 'tStopRefresh')  # time at next scr refresh
            inst2.setAutoDraw(False)
    
    # *inst2_resp* updates
    waitOnFlip = False
    if inst2_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst2_resp.frameNStart = frameN  # exact frame index
        inst2_resp.tStart = t  # local t and not account for scr refresh
        inst2_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst2_resp, 'tStartRefresh')  # time at next scr refresh
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
            win.timeOnFlip(inst2_resp, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in2"-------
for thisComponent in in2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('inst2.started', inst2.tStartRefresh)
thisExp.addData('inst2.stopped', inst2.tStopRefresh)
# check responses
if inst2_resp.keys in ['', [], None]:  # No response was made
    inst2_resp.keys = None
thisExp.addData('inst2_resp.keys',inst2_resp.keys)
if inst2_resp.keys != None:  # we had a response
    thisExp.addData('inst2_resp.rt', inst2_resp.rt)
thisExp.addData('inst2_resp.started', inst2_resp.tStartRefresh)
thisExp.addData('inst2_resp.stopped', inst2_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "in2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "in3"-------
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
in3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in3"-------
while continueRoutine:
    # get current time
    t = in3Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in3Clock)
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
        inst3.setAutoDraw(True)
    if inst3.status == STARTED:
        if bool((inst3_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst3.tStop = t  # not accounting for scr refresh
            inst3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(inst3, 'tStopRefresh')  # time at next scr refresh
            inst3.setAutoDraw(False)
    
    # *inst3_resp* updates
    waitOnFlip = False
    if inst3_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3_resp.frameNStart = frameN  # exact frame index
        inst3_resp.tStart = t  # local t and not account for scr refresh
        inst3_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3_resp, 'tStartRefresh')  # time at next scr refresh
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
            win.timeOnFlip(inst3_resp, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in3"-------
for thisComponent in in3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('inst3.started', inst3.tStartRefresh)
thisExp.addData('inst3.stopped', inst3.tStopRefresh)
# check responses
if inst3_resp.keys in ['', [], None]:  # No response was made
    inst3_resp.keys = None
thisExp.addData('inst3_resp.keys',inst3_resp.keys)
if inst3_resp.keys != None:  # we had a response
    thisExp.addData('inst3_resp.rt', inst3_resp.rt)
thisExp.addData('inst3_resp.started', inst3_resp.tStartRefresh)
thisExp.addData('inst3_resp.stopped', inst3_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "in3" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "ex_iti"-------
continueRoutine = True
# update component parameters for each repeat
ex_iti_resp.keys = []
ex_iti_resp.rt = []
_ex_iti_resp_allKeys = []
# keep track of which components have finished
ex_itiComponents = [ex_fix_cross, ex_iti_resp, ex_animal_iti, ex_tool_iti]
for thisComponent in ex_itiComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ex_itiClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "ex_iti"-------
while continueRoutine:
    # get current time
    t = ex_itiClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ex_itiClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ex_fix_cross* updates
    if ex_fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_fix_cross.frameNStart = frameN  # exact frame index
        ex_fix_cross.tStart = t  # local t and not account for scr refresh
        ex_fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_fix_cross, 'tStartRefresh')  # time at next scr refresh
        ex_fix_cross.setAutoDraw(True)
    if ex_fix_cross.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_fix_cross.tStop = t  # not accounting for scr refresh
            ex_fix_cross.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_fix_cross, 'tStopRefresh')  # time at next scr refresh
            ex_fix_cross.setAutoDraw(False)
    
    # *ex_iti_resp* updates
    waitOnFlip = False
    if ex_iti_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_iti_resp.frameNStart = frameN  # exact frame index
        ex_iti_resp.tStart = t  # local t and not account for scr refresh
        ex_iti_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_iti_resp, 'tStartRefresh')  # time at next scr refresh
        ex_iti_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ex_iti_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ex_iti_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if ex_iti_resp.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_iti_resp.tStop = t  # not accounting for scr refresh
            ex_iti_resp.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_iti_resp, 'tStopRefresh')  # time at next scr refresh
            ex_iti_resp.status = FINISHED
    if ex_iti_resp.status == STARTED and not waitOnFlip:
        theseKeys = ex_iti_resp.getKeys(keyList=['space'], waitRelease=False)
        _ex_iti_resp_allKeys.extend(theseKeys)
        if len(_ex_iti_resp_allKeys):
            ex_iti_resp.keys = _ex_iti_resp_allKeys[-1].name  # just the last key pressed
            ex_iti_resp.rt = _ex_iti_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *ex_animal_iti* updates
    if ex_animal_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_animal_iti.frameNStart = frameN  # exact frame index
        ex_animal_iti.tStart = t  # local t and not account for scr refresh
        ex_animal_iti.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_animal_iti, 'tStartRefresh')  # time at next scr refresh
        ex_animal_iti.setAutoDraw(True)
    if ex_animal_iti.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_animal_iti.tStop = t  # not accounting for scr refresh
            ex_animal_iti.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_animal_iti, 'tStopRefresh')  # time at next scr refresh
            ex_animal_iti.setAutoDraw(False)
    
    # *ex_tool_iti* updates
    if ex_tool_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_tool_iti.frameNStart = frameN  # exact frame index
        ex_tool_iti.tStart = t  # local t and not account for scr refresh
        ex_tool_iti.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_tool_iti, 'tStartRefresh')  # time at next scr refresh
        ex_tool_iti.setAutoDraw(True)
    if ex_tool_iti.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_tool_iti.tStop = t  # not accounting for scr refresh
            ex_tool_iti.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_tool_iti, 'tStopRefresh')  # time at next scr refresh
            ex_tool_iti.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ex_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "ex_iti"-------
for thisComponent in ex_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('ex_fix_cross.started', ex_fix_cross.tStartRefresh)
thisExp.addData('ex_fix_cross.stopped', ex_fix_cross.tStopRefresh)
# check responses
if ex_iti_resp.keys in ['', [], None]:  # No response was made
    ex_iti_resp.keys = None
thisExp.addData('ex_iti_resp.keys',ex_iti_resp.keys)
if ex_iti_resp.keys != None:  # we had a response
    thisExp.addData('ex_iti_resp.rt', ex_iti_resp.rt)
thisExp.addData('ex_iti_resp.started', ex_iti_resp.tStartRefresh)
thisExp.addData('ex_iti_resp.stopped', ex_iti_resp.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('ex_animal_iti.started', ex_animal_iti.tStartRefresh)
thisExp.addData('ex_animal_iti.stopped', ex_animal_iti.tStopRefresh)
thisExp.addData('ex_tool_iti.started', ex_tool_iti.tStartRefresh)
thisExp.addData('ex_tool_iti.stopped', ex_tool_iti.tStopRefresh)
# the Routine "ex_iti" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "ex_trial"-------
continueRoutine = True
routineTimer.add(5.000000)
# update component parameters for each repeat
ex_trials_resp.keys = []
ex_trials_resp.rt = []
_ex_trials_resp_allKeys = []
#send the event code
stim_marker('onset',SHOCK=False)

#set the response colors to white
ex_animal_resp_color = 'white'
ex_tool_resp_color = 'white'

# keep track of which components have finished
ex_trialComponents = [ex_trials_resp, ex_tool, ex_animal, image]
for thisComponent in ex_trialComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ex_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "ex_trial"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = ex_trialClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ex_trialClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ex_trials_resp* updates
    waitOnFlip = False
    if ex_trials_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_trials_resp.frameNStart = frameN  # exact frame index
        ex_trials_resp.tStart = t  # local t and not account for scr refresh
        ex_trials_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_trials_resp, 'tStartRefresh')  # time at next scr refresh
        ex_trials_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ex_trials_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ex_trials_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if ex_trials_resp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_trials_resp.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            ex_trials_resp.tStop = t  # not accounting for scr refresh
            ex_trials_resp.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_trials_resp, 'tStopRefresh')  # time at next scr refresh
            ex_trials_resp.status = FINISHED
    if ex_trials_resp.status == STARTED and not waitOnFlip:
        theseKeys = ex_trials_resp.getKeys(keyList=['num_1','num_2','1','2'], waitRelease=False)
        _ex_trials_resp_allKeys.extend(theseKeys)
        if len(_ex_trials_resp_allKeys):
            ex_trials_resp.keys = _ex_trials_resp_allKeys[-1].name  # just the last key pressed
            ex_trials_resp.rt = _ex_trials_resp_allKeys[-1].rt
    
    # *ex_tool* updates
    if ex_tool.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_tool.frameNStart = frameN  # exact frame index
        ex_tool.tStart = t  # local t and not account for scr refresh
        ex_tool.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_tool, 'tStartRefresh')  # time at next scr refresh
        ex_tool.setAutoDraw(True)
    if ex_tool.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_tool.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            ex_tool.tStop = t  # not accounting for scr refresh
            ex_tool.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_tool, 'tStopRefresh')  # time at next scr refresh
            ex_tool.setAutoDraw(False)
    if ex_tool.status == STARTED:  # only update if drawing
        ex_tool.setColor(ex_tool_resp_color, colorSpace='rgb', log=False)
    
    # *ex_animal* updates
    if ex_animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_animal.frameNStart = frameN  # exact frame index
        ex_animal.tStart = t  # local t and not account for scr refresh
        ex_animal.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_animal, 'tStartRefresh')  # time at next scr refresh
        ex_animal.setAutoDraw(True)
    if ex_animal.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_animal.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            ex_animal.tStop = t  # not accounting for scr refresh
            ex_animal.frameNStop = frameN  # exact frame index
            win.timeOnFlip(ex_animal, 'tStopRefresh')  # time at next scr refresh
            ex_animal.setAutoDraw(False)
    if ex_animal.status == STARTED:  # only update if drawing
        ex_animal.setColor(ex_animal_resp_color, colorSpace='rgb', log=False)
    #change the color of the response if one is pressed
    if 'num_1' in ex_trials_resp.keys:
        ex_animal_resp_color = 'darkgrey'
    elif 'num_2' in ex_trials_resp.keys:
        ex_tool_resp_color = 'darkgrey'
    
    # *image* updates
    if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        image.frameNStart = frameN  # exact frame index
        image.tStart = t  # local t and not account for scr refresh
        image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
        image.setAutoDraw(True)
    if image.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > image.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            image.tStop = t  # not accounting for scr refresh
            image.frameNStop = frameN  # exact frame index
            win.timeOnFlip(image, 'tStopRefresh')  # time at next scr refresh
            image.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ex_trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "ex_trial"-------
for thisComponent in ex_trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ex_trials_resp.keys in ['', [], None]:  # No response was made
    ex_trials_resp.keys = None
thisExp.addData('ex_trials_resp.keys',ex_trials_resp.keys)
if ex_trials_resp.keys != None:  # we had a response
    thisExp.addData('ex_trials_resp.rt', ex_trials_resp.rt)
thisExp.addData('ex_trials_resp.started', ex_trials_resp.tStartRefresh)
thisExp.addData('ex_trials_resp.stopped', ex_trials_resp.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('ex_tool.started', ex_tool.tStartRefresh)
thisExp.addData('ex_tool.stopped', ex_tool.tStopRefresh)
thisExp.addData('ex_animal.started', ex_animal.tStartRefresh)
thisExp.addData('ex_animal.stopped', ex_animal.tStopRefresh)
#send the event code
stim_marker('offset',SHOCK=False)

thisExp.addData('image.started', image.tStartRefresh)
thisExp.addData('image.stopped', image.tStopRefresh)

# ------Prepare to start Routine "in4"-------
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
in4Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "in4"-------
while continueRoutine:
    # get current time
    t = in4Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=in4Clock)
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
        inst4.setAutoDraw(True)
    if inst4.status == STARTED:
        if bool((inst4_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst4.tStop = t  # not accounting for scr refresh
            inst4.frameNStop = frameN  # exact frame index
            win.timeOnFlip(inst4, 'tStopRefresh')  # time at next scr refresh
            inst4.setAutoDraw(False)
    
    # *inst4_resp* updates
    waitOnFlip = False
    if inst4_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst4_resp.frameNStart = frameN  # exact frame index
        inst4_resp.tStart = t  # local t and not account for scr refresh
        inst4_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst4_resp, 'tStartRefresh')  # time at next scr refresh
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
            win.timeOnFlip(inst4_resp, 'tStopRefresh')  # time at next scr refresh
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

# -------Ending Routine "in4"-------
for thisComponent in in4Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('inst4.started', inst4.tStartRefresh)
thisExp.addData('inst4.stopped', inst4.tStopRefresh)
# check responses
if inst4_resp.keys in ['', [], None]:  # No response was made
    inst4_resp.keys = None
thisExp.addData('inst4_resp.keys',inst4_resp.keys)
if inst4_resp.keys != None:  # we had a response
    thisExp.addData('inst4_resp.rt', inst4_resp.rt)
thisExp.addData('inst4_resp.started', inst4_resp.tStartRefresh)
thisExp.addData('inst4_resp.stopped', inst4_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "in4" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

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
trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(f'data/{bidsID}/{bidsID}_ses-1_task-base_events-input.csv'),
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
    
    # ------Prepare to start Routine "iti"-------
    continueRoutine = True
    # update component parameters for each repeat
    ani_iti.setText('1\nanimals')
    # keep track of which components have finished
    itiComponents = [fix_cross, ani_iti, tool_iti]
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
        
        # *ani_iti* updates
        if ani_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ani_iti.frameNStart = frameN  # exact frame index
            ani_iti.tStart = t  # local t and not account for scr refresh
            ani_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ani_iti, 'tStartRefresh')  # time at next scr refresh
            ani_iti.setAutoDraw(True)
        if ani_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > ani_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                ani_iti.tStop = t  # not accounting for scr refresh
                ani_iti.frameNStop = frameN  # exact frame index
                win.timeOnFlip(ani_iti, 'tStopRefresh')  # time at next scr refresh
                ani_iti.setAutoDraw(False)
        
        # *tool_iti* updates
        if tool_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            tool_iti.frameNStart = frameN  # exact frame index
            tool_iti.tStart = t  # local t and not account for scr refresh
            tool_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(tool_iti, 'tStartRefresh')  # time at next scr refresh
            tool_iti.setAutoDraw(True)
        if tool_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > tool_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                tool_iti.tStop = t  # not accounting for scr refresh
                tool_iti.frameNStop = frameN  # exact frame index
                win.timeOnFlip(tool_iti, 'tStopRefresh')  # time at next scr refresh
                tool_iti.setAutoDraw(False)
        
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
    trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)
    trials.addData('ani_iti.started', ani_iti.tStartRefresh)
    trials.addData('ani_iti.stopped', ani_iti.tStopRefresh)
    trials.addData('tool_iti.started', tool_iti.tStartRefresh)
    trials.addData('tool_iti.stopped', tool_iti.tStopRefresh)
    # the Routine "iti" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    #send the event code
    stim_marker('onset',SHOCK=False)
    
    #set the response colors to white
    animal_resp_color = 'white'
    tool_resp_color = 'white'
    
    base_image.setImage(stimulus)
    trials_resp.keys = []
    trials_resp.rt = []
    _trials_resp_allKeys = []
    # keep track of which components have finished
    trialComponents = [base_image, trials_resp, animal, tool]
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
        #change the color of the response if one is pressed
        if 'num_1' in trials_resp.keys:
            animal_resp_color = 'darkgrey'
        elif 'num_2' in trials_resp.keys:
            tool_resp_color = 'darkgrey'
        
        # *base_image* updates
        if base_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_image.frameNStart = frameN  # exact frame index
            base_image.tStart = t  # local t and not account for scr refresh
            base_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_image, 'tStartRefresh')  # time at next scr refresh
            base_image.setAutoDraw(True)
        if base_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > base_image.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                base_image.tStop = t  # not accounting for scr refresh
                base_image.frameNStop = frameN  # exact frame index
                win.timeOnFlip(base_image, 'tStopRefresh')  # time at next scr refresh
                base_image.setAutoDraw(False)
        
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
            theseKeys = trials_resp.getKeys(keyList=['num_1','num_2','1','2'], waitRelease=False)
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
    #send the event code
    stim_marker('offset',SHOCK=False)
    trials.addData('base_image.started', base_image.tStartRefresh)
    trials.addData('base_image.stopped', base_image.tStopRefresh)
    # check responses
    if trials_resp.keys in ['', [], None]:  # No response was made
        trials_resp.keys = None
    trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        trials.addData('trials_resp.rt', trials_resp.rt)
    trials.addData('trials_resp.started', trials_resp.tStartRefresh)
    trials.addData('trials_resp.stopped', trials_resp.tStopRefresh)
    trials.addData('animal.started', animal.tStartRefresh)
    trials.addData('animal.stopped', animal.tStopRefresh)
    trials.addData('tool.started', tool.tStartRefresh)
    trials.addData('tool.stopped', tool.tStopRefresh)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'


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
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
