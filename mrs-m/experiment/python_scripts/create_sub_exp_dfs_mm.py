#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:43:07 2022

@author: sab5394
"""

import pandas as pd 
import os
import numpy as np 
import random


home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop','pig', 'mrs-m', 'experiment', 'data')
input_dir = os.path.join(home_dir,'Desktop', 'pig','mrs-m', 'experiment', 'stims')
os.chdir(input_dir)

#%%


'''set in psychopy'''
# expInfo = {'participant':'0'}
# bidsID = 'sub-SP000'
# tag_order = 'a'
# CS_order = '1'
# test_order = '1'
'''set in psychopy'''

# expName = 'instructions_setup'
# expInfo = {'participant': ', 'CS_order': '', 'phase_order': '', 'extcc': ''}

dlg = gui.Dlg(title = 'MM subject initialization')
dlg.addField('participant')
dlg.addField('CS_order', choices=['A','T'])
dlg.addField('phase_order_input', choices=[1,2,3,4,5,6])
dlg.addField('extcc', choices=['ext', 'cc'])

#added on 6/13
dlg.addField('room', choices =['behavior', 'VR'])
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])


user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel
#%%
bidsID = 'sub-MM{0:0=3d}'.format(int(user_input[0]))
cs_order = user_input[1]
phase_order_input = user_input[2]
extcc_input = user_input[3]

#added on 6/13
room_input = user_input[4]

#%%

#PARALLEL PORT CODE 
#BIO = True if user_input[5] == 'yes' else False
BIO = True if user_input[5] == 'yes' and user_input[4] = 'VR' else False
BIO2 = True if user_input[5] == 'yes' and user_input[4] = 'behavior' else False

if BIO:
    pport = ParallelPort(address='0xEFF8')
#added on 6/13 
if BIO2:
    pport = ParallelPort(address='0x3FE0')

#%%
    
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

#%% 

#FOR TESTING IN PYTHON FILE:
    #mrs-m code-- note that "cs_order" has to match what is in my gui
bidsID = 'MM999'
cs_order = 'A'
phase_order_input = 4 
extcc_input = 'CC'
room_input = 'behavior'

#%%

cs_cats = {'CS+':'animals' if cs_order == 'A' else 'tools',
           'CS-':'tools' if cs_order == 'A' else 'animals'}
phase_order = {1:[1,2,3],
               2:[1,3,2], 
               3:[3,2,1], 
               4:[3,1,2], 
               5:[2,1,3], 
               6:[2,3,1]}
#%%
#added on 6/13
if room_input == 'behavior':
    
else:
    day1_dfs['extcc'].loc[[0,1], 'cc_stimulus'] = 'stims/transparent.png'

#create f strings that will output the name of the column that I want to index depending on the inputs
#the first part takes the group that is the CS+ and puts it in the f string. 
#the second part uses the phase_order_input that the RA clicks and uses it to select one of the dictionaries, and within that one value from the dictionary values

#%%

#create variables that are lists of my phases to be used for iteration later
phases = ['base','fear','extcc','renewal_1', 'mem_1','sou_typ_val_1']
day1_phases = ['base','fear','extcc']

#%%

#CREATE DAY 1 DATAFRAMES:

#create list of day 1 phases
day1_phases = ['base','fear','extcc']
#create dataframe of stims (the one with the 6 columns of 24 animals or tools)
stims = pd.read_csv('day1_stims_groups.csv')
day1_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns
day2_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again
soutypval_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again!
#read in the different task templates for each phase, and name them after each phase (using list comprehension)
day1_dfs = {phase: pd.read_csv(f'../task_templates/{phase}_template.csv').set_index(['trial_type'], ['block']) for phase in day1_phases}
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
#%%   
#FILL IN EXTINCTION CC STIMS 

cc_stims = pd.read_csv('cc_stims.csv') 

day1_dfs['extcc'] = day1_dfs['extcc'].set_index('cc')

#note that once it is the index, pandas will not recognize it as a column anymore!

if extcc_input == 'CC':
    day1_dfs['extcc'].loc[1, 'cc_stimulus'] = cc_stims.values
    day1_dfs['extcc'].loc[0, 'cc_stimulus'] = 'stims/crosshair.png'
    day1_dfs['extcc'].loc[1, 'group'] = 'CS+CC'
    day1_dfs['extcc'].loc[0, 'group'] = 'CS-CC'

else:
    day1_dfs['extcc'].loc[[0,1], 'cc_stimulus'] = 'stims/crosshair.png'
    day1_dfs['extcc'].loc[1, 'group'] = 'CS+EXT'
     day1_dfs['extcc'].loc[0, 'group'] = 'CS-EXT'
    
#this works!

#%%

#ADD GROUP FOR BASE 7/14/22

day1_dfs['base'] = day1_dfs['base'].set_index('trial_type')

if extcc_input == 'CC':
    day1_dfs['base'].loc['CS+', 'group'] = 'CS+CC'
    day1_dfs['base'].loc['CS-', 'group'] = 'CS-CC'

else:
    day1_dfs['extcc'].loc['CS+', 'group'] = 'CS+EXT'
    day1_dfs['extcc'].loc['CS-', 'group'] = 'CS-EXT'
    
#%%

#ADD GROUP FOR FEAR 7/14/22

day1_dfs['fear'] = day1_dfs['fear'].set_index('trial_type')

if extcc_input == 'CC':
    day1_dfs['fear'].loc['CS+', 'group'] = 'CS+CC'
    day1_dfs['fear'].loc['CS-', 'group'] = 'CS-CC'

else:
    day1_dfs['fear'].loc['CS+', 'group'] = 'CS+EXT'
    day1_dfs['fear'].loc['CS-', 'group'] = 'CS-EXT'
    


 #%%

 #RENEWAL 

 renewal_stims = pd.read_csv('renewal_stims.csv')
 renewal_stims = renewal_stims.sample(frac=1).reset_index(drop=True) #shuffle within columns 
 renewal_df = pd.read_csv('../task_templates/renewal_template.csv').set_index(['trial_type'])

 for con in ['CS+', 'CS-']:
     renewal_df.loc[con, 'stimulus'] = renewal_stims[f'{cs_cats[con]}'].values

 renewal_df.loc['new', 'stimulus'] = f'stims/tr1renewal_{cs_cats[con]}.jpg'  #assigns the first row named "new" with a novel and consistent pic of the subject's CS-...
 renewal_df.loc['new', 'iti_duration'] = '5'  #assigns the first row named "new" with an iti duration of 5 secs
#%%

#ADD GROUP FOR RENEWAL 7/14/22

if extcc_input == 'CC':
    renewal_df.loc['CS+', 'group'] = 'CS+CC'
    renewal_df.loc['CS-', 'group'] = 'CS-CC'

else:
    renewal_df.loc['CS+', 'group'] = 'CS+EXT'
    renewal_df.loc['CS-', 'group'] = 'CS-EXT'


#%%
 #SET ITIs
 itis = [5,6,7]
 iti_blocks = [np.random.choice(itis, 6, replace=True) for i in range(4)]
 #put them all together into one list
 iti_blocks = np.concatenate(iti_blocks)
 #put the list into the iti_duration column in each dataframe
 #how do i select just a column.....?
 renewal_df.loc[['CS+', 'CS-'], 'iti_duration'] = iti_blocks 
 
#%%

#RECOGNITION MEMORY
mem_df = pd.read_csv('../task_templates/mem_template.csv').set_index(['trial_type', 'phase'])

#SET REC. MEMORY ITI

mem_df.reset_index(['trial_type'])
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
    
#%%    
    
#ADD GROUP FOR MEM 7/14/22

if extcc_input == 'CC':
    mem_df.loc['CS+', 'group'] = 'CS+CC'
    mem_df.loc['CS-', 'group'] = 'CS-CC'

else:
    mem_df.loc['CS+', 'group'] = 'CS+EXT'
    mem_df.loc['CS-', 'group'] = 'CS-EXT'
                                                                                                                                                                                   

#%%

#SOUTYP 

soutypval_stims = stims.sample(frac=1).reset_index(drop=True) #shuffle within columns again!
soutypval_df = pd.read_csv('../task_templates/soutypval_template.csv').set_index(['trial_type', 'phase'])
#add all same stims as day 1 except reshuffled, according to the same user input as on day 1.
for p, phase in enumerate(day1_phases):
    for con in ['CS+','CS-']:
           soutypval_df.loc[(con, phase), 'stimulus'] = soutypval_stims[f'{cs_cats[con]}_{phase_order[phase_order_input][p]}'].values       
       
#%%

#ADD GROUP FOR SOUTYP 7/14/22

if extcc_input == 'CC':
    soutypval_df.loc['CS+', 'group'] = 'CS+CC'
    soutypval_df.loc['CS-', 'group'] = 'CS-CC'

else:
    soutypval_df.loc['CS+', 'group'] = 'CS+EXT'
    soutypval_df.loc['CS-', 'group'] = 'CS-EXT'
                                                  

#%%
os.chdir(data_dir)
os.makedirs(f'data/{bidsID}',exist_ok=True)
for phase in day1_phases:
  ses = 1
  phase_str = phase.split('_')[0]
  day1_dfs[phase].reset_index().to_csv(f'../data/{bidsID}/{bidsID}_ses-{ses}_task-{phase_str}_events-input.csv',index=False)
  
  #%%
  
renewal_df.reset_index().to_csv(f'../data/{bidsID}/{bidsID}_ses-2_task-renewal_events-input.csv',index=False)
mem_df.reset_index().to_csv(f'../data/{bidsID}/{bidsID}_ses-2_task-rec-memory_events-input.csv',index=False)
soutypval_df.reset_index().to_csv(f'../data/{bidsID}/{bidsID}_ses-2_task-soutypval_events-input.csv',index=False)

