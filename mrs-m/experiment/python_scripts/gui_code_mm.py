#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:06:33 2022

@author: sab5394
"""
 #FIRST FILE ONLY, TO SET UP THE GUI FOR ALL OF THE INPUTS LATER ON 
import pandas as pd 
import os
import numpy as np 
import random


home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'pig','mrs-m', 'experiment', 'data')
input_dir = os.path.join(home_dir,'Desktop', 'pig'.'mrs-m', 'experiment', 'stims')
os.chdir(input_dir)

# expName = 'instructions_setup'
# expInfo = {'participant': ', 'CS_order': '', 'phase_order': '', 'extcc': ''}

dlg = gui.Dlg(title = 'MM subject initialization')
dlg.addField('participant')
dlg.addField('CS_order', choices=['A','T'])
dlg.addField('phase_order_input', choices=['1','2','3','4','5','6'])
dlg.addField('extcc_input', choices=['ext', 'cc'])

user_input = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel

bidsID = 'sub-MM{0:0=3d}'.format(int(user_input[0]))
cs_order = user_input[1]
phase_order_input = int(user_input[2]) #MOST RECENT EDIT FOR KEYERROR BUG 5/17
extcc_input = user_input[3]

#%%


#ALL FILES AFTER THE INPUT FILES HAVE ALREADY BEEN GENERATED 

'''fear-acquisition'''
expName = 'fear-acquisition'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.Dlg(title='Init participant')
dlg.addField('participant', choices = [int(i.split('sub-MM')[-1]) for i in os.listdir('data') if 'sub-MM' in i])
#IF IT IS A CONDITIONING/SHOCK TRIAL:
dlg.addField('Init parallel port?', choices=['yes','no (testing)'])

user_input = dlg.show()
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo = {'participant':user_input[0]}
bidsID = 'sub-MM{0:0=3d}'.format(int(expInfo['participant']))
BIO = True if user_input[1] == 'yes' else False