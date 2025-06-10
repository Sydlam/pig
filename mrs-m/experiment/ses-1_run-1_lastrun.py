#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on Mon Jun  9 10:18:02 2025
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

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from input_files_code
from psychopy.parallel import ParallelPort
from subprocess import Popen
import time
import pandas as pd 
import os
import numpy as np 
import random

home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'pig', 'mrs-m', 'experiment', 'data')
input_dir = os.path.join(home_dir,'Desktop', 'pig', 'mrs-m', 'experiment', 'stims')
os.chdir(input_dir)

dlg = gui.Dlg(title = 'PYG subject initialization')
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

if extcc_input == 'cc':
    itis = [4,5,6]
else:
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
    day1_dfs['extcc'].loc[0, 'cc_stimulus'] = 'stims/crosshair.png'
    day1_dfs['extcc'].loc[1, 'group'] = 'CS+CC'
    day1_dfs['extcc'].loc[0, 'group'] = 'CS-CC'
else:
    day1_dfs['extcc'].loc[[0,1], 'cc_stimulus'] = 'stims/crosshair.png'
    day1_dfs['extcc'].loc[1, 'group'] = 'CS+EXT'
    day1_dfs['extcc'].loc[0, 'group'] = 'CS-EXT'
    
#ADD GROUP FOR BASE 7/14/22

day1_dfs['base'] = day1_dfs['base'].set_index('trial_type')

if extcc_input == 'CC':
    day1_dfs['base'].loc['CS+', 'group'] = 'CS+CC'
    day1_dfs['base'].loc['CS-', 'group'] = 'CS-CC'

else:
  day1_dfs['extcc'] = day1_dfs['extcc'].reset_index()
day1_dfs['extcc'].loc[day1_dfs['extcc']['stim'] == 'CS+', 'group'] = 'CS+EXT'

#ADD GROUP FOR FEAR 7/14/22

day1_dfs['fear'] = day1_dfs['fear'].set_index('trial_type')

if extcc_input == 'CC':
    day1_dfs['fear'].loc['CS+', 'group'] = 'CS+CC'
    day1_dfs['fear'].loc['CS-', 'group'] = 'CS-CC'

else:
    day1_dfs['fear'].loc['CS+', 'group'] = 'CS+EXT'
    day1_dfs['fear'].loc['CS-', 'group'] = 'CS-EXT'
    
#RENEWAL
 
renewal_stims = pd.read_csv('renewal_stims.csv')
renewal_stims = renewal_stims.sample(frac=1).reset_index(drop=True) #shuffle within columns 
renewal_df = pd.read_csv('../task_templates/renewal_template.csv').set_index(['trial_type', 'trial'])

for con in ['CS+', 'CS-']:
    renewal_df.loc[con, 'stimulus'] = renewal_stims[f'{cs_cats[con]}'].values

renewal_df.loc['new', 'stimulus'] = f'stims/tr1renewal_{cs_cats[con]}.jpg'  #assigns the first row named "new" with a novel and consistent pic of the subject's CS-...
renewal_df.loc['new', 'iti_duration'] = '5'  #assigns the first row named "new" with an iti of 5 seconds

#ADD GROUP FOR RENEWAL 7/14/22

if extcc_input == 'CC':
    renewal_df.loc['CS+', 'group'] = 'CS+CC'
    renewal_df.loc['CS-', 'group'] = 'CS-CC'

else:
    renewal_df.loc['CS+', 'group'] = 'CS+EXT'
    renewal_df.loc['CS-', 'group'] = 'CS-EXT'

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
mem_df.reset_index(['trial_type']) #changed this to fix but 6/9
itis_mem = [2,3]
iti_mem_blocks = [np.random.choice(itis_mem, 20, replace=True) for i in range(12)]
iti_mem_blocks = np.concatenate(iti_mem_blocks)
mem_df.loc[:, 'iti_duration'] = iti_mem_blocks

#add all same stims as day 1 except reshuffled, according to the same user input as on day 1.
for p, phase in enumerate(day1_phases):
    for con in ['CS+','CS-']:
            mem_df.loc[(con, phase), 'stimulus'] = day2_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values       
       
#load rec. mem foil stims
foil_stims = pd.read_csv('foil_stims_list.csv').sample(frac=1).reset_index(drop=True)

for con in ['CS+','CS-']:
    mem_df.loc[(con, 'foil'), 'stimulus'] = foil_stims[f'{cs_cats[con]}'].values

#ADD GROUP FOR MEM 7/14/22

if extcc_input == 'CC':
    mem_df.loc['CS+', 'group'] = 'CS+CC'
    mem_df.loc['CS-', 'group'] = 'CS-CC'

else:
    mem_df.loc['CS+', 'group'] = 'CS+EXT'
    mem_df.loc['CS-', 'group'] = 'CS-EXT'

#SOUTYP

soutyp_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again!
soutyp_df = pd.read_csv('../task_templates/soutyp_template.csv').set_index(['trial_type', 'phase'])
#add all same stims as day 1 except reshuffled, according to the same user input as on day 1.
for p, phase in enumerate(day1_phases):
    for con in ['CS+','CS-']:
           soutyp_df.loc[(con, phase), 'stimulus'] = soutyp_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values       

#ADD GROUP FOR SOUTYP 7/14/22

if extcc_input == 'CC':
    soutyp_df.loc['CS+', 'group'] = 'CS+CC'
    soutyp_df.loc['CS-', 'group'] = 'CS-CC'

else:
    soutyp_df.loc['CS+', 'group'] = 'CS+EXT'
    soutyp_df.loc['CS-', 'group'] = 'CS-EXT'
    
#EXPORT DATA TO CSVs                                                        
os.chdir(data_dir)
os.makedirs(f'{bidsID}',exist_ok=True)
for phase in day1_phases:
  ses = 1
  phase_str = phase.split('_')[0]
  day1_dfs[phase].reset_index().to_csv(f'{bidsID}/{bidsID}_ses-{ses}_task-{phase_str}_events-input.csv',index=False)
 
renewal_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-renewal_events-input.csv',index=False)
mem_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-rec-memory_events-input.csv',index=False)
soutyp_df.reset_index().to_csv(f'{bidsID}/{bidsID}_ses-2_task-soutyp_events-input.csv',index=False)
# Run 'Before Experiment' code from col_code_ex


# Run 'Before Experiment' code from cs_code




# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'baseline'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
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
    originPath='/Users/sydneylambert/Desktop/pig/mrs-m/experiment/ses-1_run-1_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0, 
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
inst1_resp = keyboard.Keyboard()
inst1 = visual.TextStim(win=win, name='inst1',
    text='First, please make sure your cell phone is silenced. \n\nWe will be measuring how much you are sweating from the sensors on your hand. \n\nThese are very sensitive to movement and posture, so please sit up straight and do not shift around in your seat or move during the experiment. \n\nPress SPACE to continue... ',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "in2" ---
inst2 = visual.TextStim(win=win, name='inst2',
    text='During this part of the experiment, you will see a picture of either an animal or tool. \nYou will see this picture for a few seconds.\n\nEach time you see a picture of an animal or tool, I want you to tell me which category you think the picture belongs to: \n\n1 = animals\n2 = tools\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst2_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in3" ---
inst3 = visual.TextStim(win=win, name='inst3',
    text='Please make a response for EVERY PICTURE. We are also measuring how fast you press the button. Please try to be as quick and accurate as possible.\n\nYou only need to press a button when you see a picture of an animal or tool.\n\nPress SPACE to see what this will look like: ',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst3_resp = keyboard.Keyboard()

# --- Initialize components for Routine "ex_iti" ---
ex_iti_resp = keyboard.Keyboard()
ex_animal_iti = visual.TextStim(win=win, name='ex_animal_iti',
    text='1\nanimals',
    font='Open Sans',
    pos=(-.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
ex_tool_iti = visual.TextStim(win=win, name='ex_tool_iti',
    text='2\ntools',
    font='Open Sans',
    pos=(.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
ex_crosshair = visual.ImageStim(
    win=win,
    name='ex_crosshair', 
    image='stims/whitecrosshair.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "ex_trial" ---
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

# --- Initialize components for Routine "in4" ---
inst4 = visual.TextStim(win=win, name='inst4',
    text='So, to recap:\n\nWhen you see a picture of an animal or a tool, press 1 or 2 to put the picture in its category. Please respond as quickly and as accurately as possible. Please make a response for every picture as soon as the picture appears on the screen.\n\nAny questions?\n',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
inst4_resp = keyboard.Keyboard()

# --- Initialize components for Routine "in_begin_experiment" ---
beg_exp = visual.TextStim(win=win, name='beg_exp',
    text='Press SPACE to begin the experiment.',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
beg_exp_resp = keyboard.Keyboard()

# --- Initialize components for Routine "iti" ---
ani_iti = visual.TextStim(win=win, name='ani_iti',
    text='',
    font='Open Sans',
    pos=(-.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
tool_iti = visual.TextStim(win=win, name='tool_iti',
    text='2\ntools',
    font='Open Sans',
    pos=(.15,-.325), height=0.03, wrapWidth=None, ori=0.0, 
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
base_image = visual.ImageStim(
    win=win,
    name='base_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
trials_resp = keyboard.Keyboard()
animal = visual.TextStim(win=win, name='animal',
    text='1\nanimals',
    font='Open Sans',
    pos=(-.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
tool = visual.TextStim(win=win, name='tool',
    text='2\ntools',
    font='Open Sans',
    pos=(.15, -.325), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);

# --- Initialize components for Routine "in_end_experiment" ---
end_exp_resp = keyboard.Keyboard()
end_exp = visual.TextStim(win=win, name='end_exp',
    text='Experimenter press SPACE to exit the task.',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
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
frameN = -1

# --- Run Routine "in1" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *inst1_resp* updates
    waitOnFlip = False
    
    # if inst1_resp is starting this frame...
    if inst1_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst1_resp.frameNStart = frameN  # exact frame index
        inst1_resp.tStart = t  # local t and not account for scr refresh
        inst1_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst1_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst1_resp.started')
        # update status
        inst1_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst1_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst1_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if inst1_resp is stopping this frame...
    if inst1_resp.status == STARTED:
        if bool((inst1_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst1_resp.tStop = t  # not accounting for scr refresh
            inst1_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1_resp.stopped')
            # update status
            inst1_resp.status = FINISHED
            inst1_resp.status = FINISHED
    if inst1_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst1_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst1_resp_allKeys.extend(theseKeys)
        if len(_inst1_resp_allKeys):
            inst1_resp.keys = _inst1_resp_allKeys[-1].name  # just the last key pressed
            inst1_resp.rt = _inst1_resp_allKeys[-1].rt
            inst1_resp.duration = _inst1_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # *inst1* updates
    
    # if inst1 is starting this frame...
    if inst1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    
    # if inst1 is stopping this frame...
    if inst1.status == STARTED:
        if bool((inst1_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst1.tStop = t  # not accounting for scr refresh
            inst1.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst1.stopped')
            # update status
            inst1.status = FINISHED
            inst1.setAutoDraw(False)
    
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
    thisExp.addData('inst1_resp.duration', inst1_resp.duration)
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst2.started')
        # update status
        inst2.status = STARTED
        inst2.setAutoDraw(True)
    
    # if inst2 is active this frame...
    if inst2.status == STARTED:
        # update params
        pass
    
    # if inst2 is stopping this frame...
    if inst2.status == STARTED:
        if bool((inst2_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2.tStop = t  # not accounting for scr refresh
            inst2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2.stopped')
            # update status
            inst2.status = FINISHED
            inst2.setAutoDraw(False)
    
    # *inst2_resp* updates
    waitOnFlip = False
    
    # if inst2_resp is starting this frame...
    if inst2_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst2_resp.frameNStart = frameN  # exact frame index
        inst2_resp.tStart = t  # local t and not account for scr refresh
        inst2_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst2_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst2_resp.started')
        # update status
        inst2_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst2_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst2_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if inst2_resp is stopping this frame...
    if inst2_resp.status == STARTED:
        if bool((inst2_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst2_resp.tStop = t  # not accounting for scr refresh
            inst2_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst2_resp.stopped')
            # update status
            inst2_resp.status = FINISHED
            inst2_resp.status = FINISHED
    if inst2_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst2_resp.getKeys(keyList=['space'], waitRelease=False)
        _inst2_resp_allKeys.extend(theseKeys)
        if len(_inst2_resp_allKeys):
            inst2_resp.keys = _inst2_resp_allKeys[-1].name  # just the last key pressed
            inst2_resp.rt = _inst2_resp_allKeys[-1].rt
            inst2_resp.duration = _inst2_resp_allKeys[-1].duration
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
# check responses
if inst2_resp.keys in ['', [], None]:  # No response was made
    inst2_resp.keys = None
thisExp.addData('inst2_resp.keys',inst2_resp.keys)
if inst2_resp.keys != None:  # we had a response
    thisExp.addData('inst2_resp.rt', inst2_resp.rt)
    thisExp.addData('inst2_resp.duration', inst2_resp.duration)
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst3.started')
        # update status
        inst3.status = STARTED
        inst3.setAutoDraw(True)
    
    # if inst3 is active this frame...
    if inst3.status == STARTED:
        # update params
        pass
    
    # if inst3 is stopping this frame...
    if inst3.status == STARTED:
        if bool((inst3_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst3.tStop = t  # not accounting for scr refresh
            inst3.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst3.stopped')
            # update status
            inst3.status = FINISHED
            inst3.setAutoDraw(False)
    
    # *inst3_resp* updates
    waitOnFlip = False
    
    # if inst3_resp is starting this frame...
    if inst3_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        inst3_resp.frameNStart = frameN  # exact frame index
        inst3_resp.tStart = t  # local t and not account for scr refresh
        inst3_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(inst3_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst3_resp.started')
        # update status
        inst3_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(inst3_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(inst3_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if inst3_resp is stopping this frame...
    if inst3_resp.status == STARTED:
        if bool((inst3_resp.keys)=='space'):
            # keep track of stop time/frame for later
            inst3_resp.tStop = t  # not accounting for scr refresh
            inst3_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst3_resp.stopped')
            # update status
            inst3_resp.status = FINISHED
            inst3_resp.status = FINISHED
    if inst3_resp.status == STARTED and not waitOnFlip:
        theseKeys = inst3_resp.getKeys(keyList=['space'], waitRelease=False)
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
    thisExp.addData('inst3_resp.duration', inst3_resp.duration)
thisExp.nextEntry()
# the Routine "in3" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "ex_iti" ---
continueRoutine = True
# update component parameters for each repeat
ex_iti_resp.keys = []
ex_iti_resp.rt = []
_ex_iti_resp_allKeys = []
# keep track of which components have finished
ex_itiComponents = [ex_iti_resp, ex_animal_iti, ex_tool_iti, ex_crosshair]
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
frameN = -1

# --- Run Routine "ex_iti" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ex_iti_resp* updates
    waitOnFlip = False
    
    # if ex_iti_resp is starting this frame...
    if ex_iti_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_iti_resp.frameNStart = frameN  # exact frame index
        ex_iti_resp.tStart = t  # local t and not account for scr refresh
        ex_iti_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_iti_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_iti_resp.started')
        # update status
        ex_iti_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ex_iti_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ex_iti_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if ex_iti_resp is stopping this frame...
    if ex_iti_resp.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_iti_resp.tStop = t  # not accounting for scr refresh
            ex_iti_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_iti_resp.stopped')
            # update status
            ex_iti_resp.status = FINISHED
            ex_iti_resp.status = FINISHED
    if ex_iti_resp.status == STARTED and not waitOnFlip:
        theseKeys = ex_iti_resp.getKeys(keyList=['space'], waitRelease=False)
        _ex_iti_resp_allKeys.extend(theseKeys)
        if len(_ex_iti_resp_allKeys):
            ex_iti_resp.keys = _ex_iti_resp_allKeys[-1].name  # just the last key pressed
            ex_iti_resp.rt = _ex_iti_resp_allKeys[-1].rt
            ex_iti_resp.duration = _ex_iti_resp_allKeys[-1].duration
            # a response ends the routine
            continueRoutine = False
    
    # *ex_animal_iti* updates
    
    # if ex_animal_iti is starting this frame...
    if ex_animal_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_animal_iti.frameNStart = frameN  # exact frame index
        ex_animal_iti.tStart = t  # local t and not account for scr refresh
        ex_animal_iti.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_animal_iti, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_animal_iti.started')
        # update status
        ex_animal_iti.status = STARTED
        ex_animal_iti.setAutoDraw(True)
    
    # if ex_animal_iti is active this frame...
    if ex_animal_iti.status == STARTED:
        # update params
        pass
    
    # if ex_animal_iti is stopping this frame...
    if ex_animal_iti.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_animal_iti.tStop = t  # not accounting for scr refresh
            ex_animal_iti.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_animal_iti.stopped')
            # update status
            ex_animal_iti.status = FINISHED
            ex_animal_iti.setAutoDraw(False)
    
    # *ex_tool_iti* updates
    
    # if ex_tool_iti is starting this frame...
    if ex_tool_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_tool_iti.frameNStart = frameN  # exact frame index
        ex_tool_iti.tStart = t  # local t and not account for scr refresh
        ex_tool_iti.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_tool_iti, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_tool_iti.started')
        # update status
        ex_tool_iti.status = STARTED
        ex_tool_iti.setAutoDraw(True)
    
    # if ex_tool_iti is active this frame...
    if ex_tool_iti.status == STARTED:
        # update params
        pass
    
    # if ex_tool_iti is stopping this frame...
    if ex_tool_iti.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_tool_iti.tStop = t  # not accounting for scr refresh
            ex_tool_iti.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_tool_iti.stopped')
            # update status
            ex_tool_iti.status = FINISHED
            ex_tool_iti.setAutoDraw(False)
    
    # *ex_crosshair* updates
    
    # if ex_crosshair is starting this frame...
    if ex_crosshair.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_crosshair.frameNStart = frameN  # exact frame index
        ex_crosshair.tStart = t  # local t and not account for scr refresh
        ex_crosshair.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_crosshair, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_crosshair.started')
        # update status
        ex_crosshair.status = STARTED
        ex_crosshair.setAutoDraw(True)
    
    # if ex_crosshair is active this frame...
    if ex_crosshair.status == STARTED:
        # update params
        pass
    
    # if ex_crosshair is stopping this frame...
    if ex_crosshair.status == STARTED:
        if bool((ex_iti_resp.keys)=='space'):
            # keep track of stop time/frame for later
            ex_crosshair.tStop = t  # not accounting for scr refresh
            ex_crosshair.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_crosshair.stopped')
            # update status
            ex_crosshair.status = FINISHED
            ex_crosshair.setAutoDraw(False)
    
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
    for thisComponent in ex_itiComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "ex_iti" ---
for thisComponent in ex_itiComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ex_iti_resp.keys in ['', [], None]:  # No response was made
    ex_iti_resp.keys = None
thisExp.addData('ex_iti_resp.keys',ex_iti_resp.keys)
if ex_iti_resp.keys != None:  # we had a response
    thisExp.addData('ex_iti_resp.rt', ex_iti_resp.rt)
    thisExp.addData('ex_iti_resp.duration', ex_iti_resp.duration)
thisExp.nextEntry()
# the Routine "ex_iti" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "ex_trial" ---
continueRoutine = True
# update component parameters for each repeat
ex_trials_resp.keys = []
ex_trials_resp.rt = []
_ex_trials_resp_allKeys = []
# Run 'Begin Routine' code from col_code_ex
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
frameN = -1

# --- Run Routine "ex_trial" ---
routineForceEnded = not continueRoutine
while continueRoutine and routineTimer.getTime() < 5.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ex_trials_resp* updates
    waitOnFlip = False
    
    # if ex_trials_resp is starting this frame...
    if ex_trials_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_trials_resp.frameNStart = frameN  # exact frame index
        ex_trials_resp.tStart = t  # local t and not account for scr refresh
        ex_trials_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_trials_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_trials_resp.started')
        # update status
        ex_trials_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ex_trials_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ex_trials_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    
    # if ex_trials_resp is stopping this frame...
    if ex_trials_resp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_trials_resp.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            ex_trials_resp.tStop = t  # not accounting for scr refresh
            ex_trials_resp.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_trials_resp.stopped')
            # update status
            ex_trials_resp.status = FINISHED
            ex_trials_resp.status = FINISHED
    if ex_trials_resp.status == STARTED and not waitOnFlip:
        theseKeys = ex_trials_resp.getKeys(keyList=['num_1','num_2','1','2'], waitRelease=False)
        _ex_trials_resp_allKeys.extend(theseKeys)
        if len(_ex_trials_resp_allKeys):
            ex_trials_resp.keys = _ex_trials_resp_allKeys[-1].name  # just the last key pressed
            ex_trials_resp.rt = _ex_trials_resp_allKeys[-1].rt
            ex_trials_resp.duration = _ex_trials_resp_allKeys[-1].duration
    
    # *ex_tool* updates
    
    # if ex_tool is starting this frame...
    if ex_tool.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_tool.frameNStart = frameN  # exact frame index
        ex_tool.tStart = t  # local t and not account for scr refresh
        ex_tool.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_tool, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_tool.started')
        # update status
        ex_tool.status = STARTED
        ex_tool.setAutoDraw(True)
    
    # if ex_tool is active this frame...
    if ex_tool.status == STARTED:
        # update params
        ex_tool.setColor(ex_tool_resp_color, colorSpace='rgb', log=False)
    
    # if ex_tool is stopping this frame...
    if ex_tool.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_tool.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            ex_tool.tStop = t  # not accounting for scr refresh
            ex_tool.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_tool.stopped')
            # update status
            ex_tool.status = FINISHED
            ex_tool.setAutoDraw(False)
    
    # *ex_animal* updates
    
    # if ex_animal is starting this frame...
    if ex_animal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ex_animal.frameNStart = frameN  # exact frame index
        ex_animal.tStart = t  # local t and not account for scr refresh
        ex_animal.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ex_animal, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'ex_animal.started')
        # update status
        ex_animal.status = STARTED
        ex_animal.setAutoDraw(True)
    
    # if ex_animal is active this frame...
    if ex_animal.status == STARTED:
        # update params
        ex_animal.setColor(ex_animal_resp_color, colorSpace='rgb', log=False)
    
    # if ex_animal is stopping this frame...
    if ex_animal.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > ex_animal.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            ex_animal.tStop = t  # not accounting for scr refresh
            ex_animal.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ex_animal.stopped')
            # update status
            ex_animal.status = FINISHED
            ex_animal.setAutoDraw(False)
    # Run 'Each Frame' code from col_code_ex
    #change the color of the response if one is pressed
    if 'num_1' in ex_trials_resp.keys:
        ex_animal_resp_color = 'darkgrey'
    elif 'num_2' in ex_trials_resp.keys:
        ex_tool_resp_color = 'darkgrey'
    
    # *image* updates
    
    # if image is starting this frame...
    if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        image.frameNStart = frameN  # exact frame index
        image.tStart = t  # local t and not account for scr refresh
        image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'image.started')
        # update status
        image.status = STARTED
        image.setAutoDraw(True)
    
    # if image is active this frame...
    if image.status == STARTED:
        # update params
        pass
    
    # if image is stopping this frame...
    if image.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > image.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            image.tStop = t  # not accounting for scr refresh
            image.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'image.stopped')
            # update status
            image.status = FINISHED
            image.setAutoDraw(False)
    
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
    for thisComponent in ex_trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "ex_trial" ---
for thisComponent in ex_trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ex_trials_resp.keys in ['', [], None]:  # No response was made
    ex_trials_resp.keys = None
thisExp.addData('ex_trials_resp.keys',ex_trials_resp.keys)
if ex_trials_resp.keys != None:  # we had a response
    thisExp.addData('ex_trials_resp.rt', ex_trials_resp.rt)
    thisExp.addData('ex_trials_resp.duration', ex_trials_resp.duration)
thisExp.nextEntry()
# Run 'End Routine' code from col_code_ex
#send the event code
stim_marker('offset',SHOCK=False)

# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-5.000000)

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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst4.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4.stopped')
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'inst4_resp.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'inst4_resp.stopped')
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
# check responses
if inst4_resp.keys in ['', [], None]:  # No response was made
    inst4_resp.keys = None
thisExp.addData('inst4_resp.keys',inst4_resp.keys)
if inst4_resp.keys != None:  # we had a response
    thisExp.addData('inst4_resp.rt', inst4_resp.rt)
    thisExp.addData('inst4_resp.duration', inst4_resp.duration)
thisExp.nextEntry()
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'beg_exp.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'beg_exp.stopped')
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'beg_exp_resp.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'beg_exp_resp.stopped')
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
# check responses
if beg_exp_resp.keys in ['', [], None]:  # No response was made
    beg_exp_resp.keys = None
thisExp.addData('beg_exp_resp.keys',beg_exp_resp.keys)
if beg_exp_resp.keys != None:  # we had a response
    thisExp.addData('beg_exp_resp.rt', beg_exp_resp.rt)
    thisExp.addData('beg_exp_resp.duration', beg_exp_resp.duration)
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
    
    # --- Prepare to start Routine "iti" ---
    continueRoutine = True
    # update component parameters for each repeat
    ani_iti.setText('1\nanimals')
    # keep track of which components have finished
    itiComponents = [ani_iti, tool_iti, crosshair]
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
        
        # *ani_iti* updates
        
        # if ani_iti is starting this frame...
        if ani_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ani_iti.frameNStart = frameN  # exact frame index
            ani_iti.tStart = t  # local t and not account for scr refresh
            ani_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ani_iti, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'ani_iti.started')
            # update status
            ani_iti.status = STARTED
            ani_iti.setAutoDraw(True)
        
        # if ani_iti is active this frame...
        if ani_iti.status == STARTED:
            # update params
            pass
        
        # if ani_iti is stopping this frame...
        if ani_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > ani_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                ani_iti.tStop = t  # not accounting for scr refresh
                ani_iti.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ani_iti.stopped')
                # update status
                ani_iti.status = FINISHED
                ani_iti.setAutoDraw(False)
        
        # *tool_iti* updates
        
        # if tool_iti is starting this frame...
        if tool_iti.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            tool_iti.frameNStart = frameN  # exact frame index
            tool_iti.tStart = t  # local t and not account for scr refresh
            tool_iti.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(tool_iti, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'tool_iti.started')
            # update status
            tool_iti.status = STARTED
            tool_iti.setAutoDraw(True)
        
        # if tool_iti is active this frame...
        if tool_iti.status == STARTED:
            # update params
            pass
        
        # if tool_iti is stopping this frame...
        if tool_iti.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > tool_iti.tStartRefresh + iti_duration-frameTolerance:
                # keep track of stop time/frame for later
                tool_iti.tStop = t  # not accounting for scr refresh
                tool_iti.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'tool_iti.stopped')
                # update status
                tool_iti.status = FINISHED
                tool_iti.setAutoDraw(False)
        
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
    # Run 'Begin Routine' code from cs_code
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
        # Run 'Each Frame' code from cs_code
        #change the color of the response if one is pressed
        if 'num_1' in trials_resp.keys:
            animal_resp_color = 'darkgrey'
        elif 'num_2' in trials_resp.keys:
            tool_resp_color = 'darkgrey'
        
        # *base_image* updates
        
        # if base_image is starting this frame...
        if base_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_image.frameNStart = frameN  # exact frame index
            base_image.tStart = t  # local t and not account for scr refresh
            base_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'base_image.started')
            # update status
            base_image.status = STARTED
            base_image.setAutoDraw(True)
        
        # if base_image is active this frame...
        if base_image.status == STARTED:
            # update params
            pass
        
        # if base_image is stopping this frame...
        if base_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > base_image.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                base_image.tStop = t  # not accounting for scr refresh
                base_image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'base_image.stopped')
                # update status
                base_image.status = FINISHED
                base_image.setAutoDraw(False)
        
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'animal.started')
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
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'animal.stopped')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'tool.started')
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
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'tool.stopped')
                # update status
                tool.status = FINISHED
                tool.setAutoDraw(False)
        
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
    # Run 'End Routine' code from cs_code
    #send the event code
    stim_marker('offset',SHOCK=False)
    # check responses
    if trials_resp.keys in ['', [], None]:  # No response was made
        trials_resp.keys = None
    trials.addData('trials_resp.keys',trials_resp.keys)
    if trials_resp.keys != None:  # we had a response
        trials.addData('trials_resp.rt', trials_resp.rt)
        trials.addData('trials_resp.duration', trials_resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-5.000000)
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'end_exp_resp.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_exp_resp.stopped')
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
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'end_exp.started')
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_exp.stopped')
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
# check responses
if end_exp_resp.keys in ['', [], None]:  # No response was made
    end_exp_resp.keys = None
thisExp.addData('end_exp_resp.keys',end_exp_resp.keys)
if end_exp_resp.keys != None:  # we had a response
    thisExp.addData('end_exp_resp.rt', end_exp_resp.rt)
    thisExp.addData('end_exp_resp.duration', end_exp_resp.duration)
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
