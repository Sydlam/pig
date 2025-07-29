#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 10:36:09 2022

@author: sab5394
"""

'''
Started this file to be more specific and clean about my code. 

Goals: 

1) Add the group column to each output file for each subject (EXTCC or CC)

'''

#%% 

#THIS CELL IS DEDICATED TO IMPORTING ALL THE THINGS I NEED TO GET THIS CODE WORKING.

#import necessary packages 

import pandas as pd 
import os 
import numpy as np 

#using subject MM101 as the example for this script 
subject = 'sub-MM059'
condition = 'EXT' #either 'CC' or 'EXT'

#%% misc code

#set the directory 
home_dir = os.path.expanduser('~')
subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
os.chdir(subject_dir)

#import files that I need to use for this 
    
soutypdf = pd.read_csv(f'{subject}_ses-2_task-soutyp_events-input.csv').set_index(['trial_type', 'stimulus'])
print(soutypdf)
arouvaldf = pd.read_csv(f'{subject}_ses-2_task-arouval_events-input.csv').set_index(['trial_type', 'stimulus'])
print(arouvaldf)
memdf = pd.read_csv(f'{subject}_ses-2_task-rec-memory_events-input.csv').set_index(['trial_type', 'stimulus'])
print(memdf)

#import the input files created for all of the day 1 tasks in order to get access to their data that we will add to the memory files. 
#doing this using a dictionary and a list comprehension: 
#define the phases
day1_phases = ['base', 'fear', 'extcc']  
#import the files into the dictionary: 
day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases}

#add the phase for baseline because for some reason it is missing from the input file (oops): 
day1_inputs['base']['phase'] = 'base'
#now the code below will work. 

#for each day 1 phase, index out the individual phase and select only the following columns to add to this selective dictionary. Then set the index to trial type.
stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases}

print(stimset)





#%% #THIS CELL IS DEDICATED TO ADDING SUBJECT NUMBER 


#set the directory 
home_dir = os.path.expanduser('~')
subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
os.chdir(subject_dir)

def addsubnum(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                sub_strip = subject.strip('sub-MM')
                outputfile['subject'] = f'{sub_strip}'
                subcol = outputfile.pop('subject')
                outputfile.insert(4, 'subject', subcol)
                outputfile.to_csv(f'{file}')
                

#Made some changes on 10/3 that I haven't tried running yet (moving the group number to the front of the dataset). Make sure to try this before running it again.
#10/3 1:29 PM

#%% THIS CELL IS DEDICATED TO ADDING GROUP 


#base and arouval are the ones that had no group at all. 
#rec memory, soutyp, and fear always seem to have the wrong group. (see MM demos sheet in group=fixed tab.)

#first, I am creating functions to add the nonexistent group to base or arouval. 

#then I need to write a function to correct the wrong group OR change the code in the input file to where it works. maybe it will be easier to just do it on the back end?



#set the directory 
home_dir = os.path.expanduser('~')
subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
os.chdir(subject_dir)


#had no group at all
def addgroup_base(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'baseline' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 0', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')
                    
#had no group at all                   
def addgroup_arouval(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'arouval' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 0', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')  

#group was wrong
def addgroup_mem(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'rec_memory' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 70', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')
                     
#group was wrong
def addgroup_fear(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'acquisition' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 61', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')    
               
#group was wrong                   
def addgroup_soutyp(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'task-soutyp' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 86', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')                     

#didn't account for this one but it is worth doing anyway
def addgroup_renewal(subject):
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if 'renewal' in file and '_2022-' in file and '.csv' in file:
                outputfile = pd.read_csv(file)
                outputfile.set_index('trial_type', inplace=True)
                #outputfile = outputfile.drop(columns=(['Unnamed: 86', 'index']))
                if condition == 'CC':
                    outputfile.loc['CS+', 'group'] = 'CS+CC'
                    outputfile.loc['CS-', 'group'] = 'CS-CC'
                    groupcol = outputfile.pop('group')
                    outputfile.insert(4, 'group', groupcol)
                    outputfile.to_csv(f'{file}')
                else:
                     outputfile.loc['CS+', 'group'] = 'CS+EXT'
                     outputfile.loc['CS-', 'group'] = 'CS-EXT'
                     groupcol = outputfile.pop('group')
                     outputfile.insert(4, 'group', groupcol)
                     outputfile.to_csv(f'{file}')
                     
#%% ADDING ORIGINAL TRIAL NUMBERS TO SOUTYP 

#change the subject and run this code for each subject. 


def trialnums_soutyp(subject): #this works!
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    os.chdir(subject_dir)
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles:
            if 'ses-2' in file and 'soutyp' in file and '2022' in file and '.csv' in file:
                soutypdf = pd.read_csv(f'{subfolder}/{file}')
    day1_phases = ['base', 'fear', 'extcc']  
    day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases}
  #add the phase for baseline because for some reason it is missing from the input file (oops): 
    day1_inputs['base']['phase'] = 'base'
  #add dataframes that are just the stimuli, and then separate them out into conditions
    stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases}
    base_csp = stimset['base'].loc['CS+']
    base_csm = stimset['base'].loc['CS-']
    fear_csp = stimset['fear'].loc['CS+']
    fear_csm = stimset['fear'].loc['CS-']
    extcc_csp = stimset['extcc'].loc['CS+']
    extcc_csp['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    extcc_csm = stimset['extcc'].loc['CS-']
    extcc_csm['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
  #concatenate the above subsets vertically into one dataframe
    vertical_concat = pd.concat([base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm])
  #left merge the dataframes together using stimulus and phase as the columns on which to merge, which is what will create the origin_trialnumber column (but it will be named trial_cs after the vertical concat dataframe)
    soutyp_originaltrialnums = pd.merge(soutypdf, vertical_concat, on=['stimulus', 'phase'], how='left')
  #rename the column from trial_cs to origin_trialnumber
    soutyp_originaltrialnums = soutyp_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
  #move it to the front of the dataframe instead of the end 
    ortrialnums = soutyp_originaltrialnums.pop('origin_trialnumber')
    soutyp_originaltrialnums.insert(4, 'origin_trialnumber', ortrialnums)
    soutyp_originaltrialnums = soutyp_originaltrialnums.drop([0,1,2,3,4,5,6,7,8,9,10])
    soutyp_originaltrialnums.reset_index(inplace=True, drop=True)
    print(soutyp_originaltrialnums[['trial_type', 'phase', 'origin_trialnumber']].head(55))
    cleansoutypdir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_soutyp')
    os.chdir(cleansoutypdir)
    soutyp_originaltrialnums.to_csv(f'{subject}_soutypoutput_edited.csv')
    
#%% ADDING ORIGINAL TRIAL NUMBERS TO AROUVAL



def trialnums_arouval(subject): #this works!
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    os.chdir(subject_dir)
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles:
            if 'ses-2' in file and 'arouval' in file and '2022' in file and '.csv' in file:
                arouvaldf = pd.read_csv(f'{subfolder}/{file}')
    day1_phases = ['base', 'fear', 'extcc']  
    day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases}
    day1_inputs['base']['phase'] = 'base'
    renewal_inputs = pd.read_csv(f'{subject}_ses-2_task-renewal_events-input.csv').set_index('trial_type')
    stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases}
    renewal_csp = renewal_inputs.loc['CS+']
    renewal_csm = renewal_inputs.loc['CS-']
    base_csp = stimset['base'].loc['CS+']
    base_csm = stimset['base'].loc['CS-']
    fear_csp = stimset['fear'].loc['CS+']
    fear_csm = stimset['fear'].loc['CS-']
    extcc_csp = stimset['extcc'].loc['CS+']
    extcc_csp['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    extcc_csm = stimset['extcc'].loc['CS-']
    extcc_csm['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    vertical_concat = pd.concat([base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm, renewal_csp, renewal_csm])
    arouval_originaltrialnums = pd.merge(arouvaldf, vertical_concat, on=['stimulus', 'phase'], how='left') #at this point, renewal trial numbers still aren't reading
    arouval_originaltrialnums = arouval_originaltrialnums.drop(columns=['trial_y', 'cs_duration', 'iti_duration'])
    arouval_originaltrialnums = arouval_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
    ortrialnums = arouval_originaltrialnums.pop('origin_trialnumber')
    arouval_originaltrialnums.insert(4, 'origin_trialnumber', ortrialnums)
    print(arouval_originaltrialnums[['trial_type', 'phase', 'origin_trialnumber']].head(55))
    arouval_originaltrialnums.to_csv(f'{subject}_arouvaloutput_edited.csv')
    
    #THIS WORKS! 
                  
#%% ADDING ORIGINAL TRIAL NUMBERS TO REC MEMORY



def trialnums_mem(subject): #this works!
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    os.chdir(subject_dir)
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles:
            if 'ses-2' in file and 'rec_memory' in file and '2022' in file and '.csv' in file:
               memdf = pd.read_csv(f'{subfolder}/{file}')
    day1_phases = ['base', 'fear', 'extcc']  
    day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases}
    day1_inputs['base']['phase'] = 'base'
    renewal_inputs = pd.read_csv(f'{subject}_ses-2_task-renewal_events-input.csv').set_index('trial_type')
    stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases}
    renewal_csp = renewal_inputs.loc['CS+']
    renewal_csm = renewal_inputs.loc['CS-']
    base_csp = stimset['base'].loc['CS+']
    base_csm = stimset['base'].loc['CS-']
    fear_csp = stimset['fear'].loc['CS+']
    fear_csm = stimset['fear'].loc['CS-']
    extcc_csp = stimset['extcc'].loc['CS+']
    extcc_csp['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    extcc_csm = stimset['extcc'].loc['CS-']
    extcc_csm['phase'] = 'extcc' #without this code, their phases were just ext. will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    vertical_concat = pd.concat([base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm])
    mem_originaltrialnums = pd.merge(memdf, vertical_concat, on=['stimulus', 'phase'], how='left') #at this point, renewal trial numbers still aren't reading
    mem_originaltrialnums = mem_originaltrialnums.drop(columns='Unnamed: 75')
    mem_originaltrialnums = mem_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
    ortrialnums = mem_originaltrialnums.pop('origin_trialnumber')
    mem_originaltrialnums.insert(4, 'origin_trialnumber', ortrialnums)
    print(mem_originaltrialnums[['trial_type', 'phase', 'origin_trialnumber']].head(55))
    mem_originaltrialnums.to_csv(f'{subject}_memoutput_edited.csv')
                     
#%% #RUN IN THIS ORDER: 
    
    
addsubnum(subject)
addgroup_arouval(subject)
addgroup_base(subject)
addgroup_fear(subject)
addgroup_mem(subject)
addgroup_renewal(subject)
addgroup_soutyp(subject)
#%%
trialnums_arouval(subject)
trialnums_mem(subject)
trialnums_soutyp(subject)



