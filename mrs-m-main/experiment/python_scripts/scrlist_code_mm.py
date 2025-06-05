#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:36:03 2022

@author: sab5394
"""

import pandas as pd 
import os 
import numpy as np 
import glob
import re

#using subject MM101 as the example for this script 
home_dir = os.path.expanduser('~')


#%% Run first (used in compile function)
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
  
     # list.sort(key=natural_keys)
    

#%% Compile function

#change group and phase; arguments are strings 

def compile_dfs(group, phase):
    data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m_dataeditsrepo', 'experiment', 'data', f'{group}', f'{group}{phase}')
    os.chdir(data_dir)

    dflist = glob.glob('./*csv')
    dflist.sort(key=natural_keys)
    totalframe = []
#iterate through list of files in group1baseline and import the csv of the corresponding name
    for file in dflist: 
        totalframe.append(pd.read_csv(file)) 

#concatenate thedataframes
    allfiledf = pd.concat(totalframe)

    allfiledf.to_csv(f'{group}{phase}_compiled.csv')
    
    return totalframe, allfiledf
    
      
#%%
#create list of subjects in each group so that I can iterate through it to get the filenames using glob
group1 = ['sub-MM001',
          'sub-MM002',
          'sub-MM003',
          'sub-MM004',
          'sub-MM025',
          'sub-MM026',
          'sub-MM027',
          'sub-MM028',
          'sub-MM029',        
          'sub-MM049',
          'sub-MM050',
          'sub-MM061',
          'sub-MM064', # memory KeyError: "['stimulus2.started', 'mem_question2.started', 'def_old2.started', 'maybe_old2.started', 'maybe_new2.started', 'def_new2.started', 'stimulus2.stopped', 'mem_question2.stopped', 'def_old2.stopped', 'maybe_old2.stopped', 'maybe_new2.stopped', 'def_new2.stopped'] not in index"
          'sub-MM065', 
          "sub-MM066", 
          "sub-MM067", 
          "sub-MM068", 
          "sub-MM069", 
          'sub-MM091',
          'sub-MM092',
          'sub-MM097']       
                      

group2 = ['sub-MM005',
          'sub-MM006',
          'sub-MM007',
          'sub-MM008',
          'sub-MM009',
          'sub-MM030',
          'sub-MM031',
          'sub-MM032',
          'sub-MM033', 
          'sub-MM035',
          'sub-MM057',
          'sub-MM058',
          'sub-MM062',
          'sub-MM071', 
          'sub-MM072', 
          'sub-MM073', 
          'sub-MM074',  
          'sub-MM076', 
          'sub-MM095', 
          'sub-MM098',
          'sub-MM099']
                      
    
group3 = ['sub-MM011',
          'sub-MM012',
          'sub-MM013',
          'sub-MM014',
          'sub-MM015',
          'sub-MM016',
          'sub-MM036',
          'sub-MM037',
          'sub-MM038',
          'sub-MM039',
          'sub-MM040', #THIS SUBJECT IS MISSING RENEWAL DATA, is messing up the renewal run 
          'sub-MM051',
          'sub-MM052',
          'sub-MM053', 
          'sub-MM077',  
          'sub-MM079',  
          'sub-MM081', 
          'sub-MM082',          
          'sub-MM090',
  #        'sub-MM094', 
    #      'sub-MM096' left these out bc joey was like.... lets just finish this pls
                      ]

group4 = ['sub-MM017',
          'sub-MM018',
          'sub-MM019',
          'sub-MM020',
          'sub-MM021',
          'sub-MM022',
          'sub-MM041',
          'sub-MM043',
          'sub-MM044',
          'sub-MM045',
          'sub-MM046',
          'sub-MM054',
          'sub-MM055',
          'sub-MM056',
          'sub-MM063', 
          'sub-MM083', 
          'sub-MM084', 
          'sub-MM085', 
          'sub-MM086', 
          'sub-MM087', 
          'sub-MM088']

groups = ['group1', 'group2', 'group3', 'group4']

                    
#groups updated on 5/24
#%%#get names of files for SCR analysis for group 1

filelist = []

def makescrlist(subject):
    scr_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'scr', f'{subject}')
    os.chdir(scr_dir)
    for dirs, subdirs, files in os.walk(scr_dir):
        for file in files:
            filelist.append(file) #just copy the output names into an excel sheet, delete items you dont want, and save it as a .txt file
    return filelist  

#%%

for subject in group1:
    makescrlist(subject)
    
for subject in group2:
    makescrlist(subject)
    
for subject in group3:
    makescrlist(subject)
    
for subject in group4:
    makescrlist(subject)


#%%   natural sorting to sort lists in numerical order 

#creating functions
import re
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
    
for file in filelist:
    filelist.sort(key=natural_keys)
     
#%%
scr_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'scr')
os.chdir(scr_dir)

df = pd.DataFrame(filelist)
df.to_csv('scrlist.csv')

