#!/usr/bin/env python
# only use this script to generate participant unique order
import psychopy.iohub as io
from psychopy.hardware import keyboard
from psychopy import gui, core
import pandas as pd
import numpy as np
import random
import os
from FAB_preferences import *
from itertools import combinations, permutations, combinations_with_replacement

# enter subject ID
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant')
dlg.addField('order', choices =[1,2,3,4]) 


user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel

bidsID = f'sub-{user_input[0]}'

# user input 1 is counterbalancing order
ind = int(user_input[1])
os.mkdir(f'data/{bidsID}')
template_folder = f'templates/Order {ind}'

# Phase
conditioning = pd.read_excel(f'{template_folder}/conditioning.xlsx')
compound= pd.read_excel(f'{template_folder}/compound.xlsx')
recall= pd.read_excel(f'{template_folder}/recall.xlsx')
# Other phases (compound, recall, decision, rating) - similar to conditioning

# conditioning starts with CS1+ and CS3+ or CS2+ and CS-, randomized
# within each conditioning block, randomize order of the 2 CS
# compound starts with CS1+ CS2+ or CS3+ CS-, counterbalanced
# recall starts with CS1+ or CS3+, counterbalanced
# left_compound could be CS1+ CS3+ or CS2+ CS-, randomized

# dlg box define order
orders = [[0,1], [1,0], [1,1], [0,0]]
ord = orders[ind - 1]
# random shuffle order within conditioning
cond = [['CS1+', 'CS3+'], ['CS2+', 'CS-']]
#for i in range(1):
#    random.shuffle(cond[i])
#random.shuffle(cond)




# define order for compound extinction using ord[0]
# compound[ord[0]] is the first compound stim
stim_name_compound = ['CS1+ CS2+', 'CS3+ CS-']
stim_name_compound = [stim_name_compound[ord[0]], stim_name_compound[1-ord[0]]]

# define order for recall using ord[1]
# recall_stim[ord[1]] is the first recall stim
recall_stim = ['CS1+', 'CS3+']
recall_stim = [recall_stim[ord[1]], recall_stim[1-ord[1]]]

# location of CS1+ and CS3+, always occur on the same side of the screen
# either [CS2 and CS-] or [CS1 and CS3]
left_compound = random.sample([['CS1+', 'CS3+'], ['CS2+', 'CS-']], 1)[0]

# will be used as global variables later
stim_name = ['CS1+', 'CS2+', 'CS3+', 'CS-']
stim_csv = ['stim1', 'stim2', 'stim3', 'stim4']
stim_pics = ['a', 'b', 'c', 'd']
cs_duration=5



phases = ['conditioning', 'compound', 'recall'] 
phase_dataframe = [conditioning, compound, recall] 
for i in range(len(phases)):
    phase_dataframe[i].to_excel(f'data/{bidsID}/{bidsID}_ses-{1}_task-{phases[i]}_events-input.xlsx',index=False)