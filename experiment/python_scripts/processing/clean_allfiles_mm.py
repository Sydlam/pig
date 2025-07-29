#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:32:20 2023

@author: sab5394


5/24 at earlybird, 10:30: got stuck on subject 40 of renewal cleaning. fix that and run. 
need to concatenate all of the conditioning runs still. 
need to clean and concatenate all of the memory runs. 

5/27 in the airport. took out subject 40 and ran group 3 again. going to concatenate the conditioning runs now.

6/5 at earlybird, finished everything <3

6/21 in lab, fixed the error with arouval (accidentally copied over soutyp data). need to clean all the data for the excluded subjects and make sure that I am fixing the groups 
when I go in and edit? do it here? idk

"""
#%%
import pandas as pd
import os
import re
import glob

#%%

home_dir = os.path.expanduser('~')

#%% DEFINING THE GROUPS updated on 4/25

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
  #        'sub-MM064', # memory KeyError: "['stimulus2.started', 'mem_question2.started', 'def_old2.started', 'maybe_old2.started', 'maybe_new2.started', 'def_new2.started', 'stimulus2.stopped', 'mem_question2.stopped', 'def_old2.stopped', 'maybe_old2.stopped', 'maybe_new2.stopped', 'def_new2.stopped'] not in index"
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
          'sub-MM060',
          'sub-MM062',
          'sub-MM071', 
          'sub-MM072', 
          'sub-MM073', 
          'sub-MM074',  
          'sub-MM076', 
          'sub-MM095', 
          'sub-MM098']
                      
    
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

excludedsubs = ['sub-MM010', 
                'sub-MM023', 
                'sub-MM024', 
                'sub-MM034',
                'sub-MM047', 
                'sub-MM048', 
                'sub-MM059', 
                'sub-MM070']
                    
#groups updated on june 21st
#%% BASE 
   
def fixbase_everything(subject):
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    cleanbl_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_baseline')
    os.chdir(subject_dir)
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if ".csv" in file and "baseline" in file and "_202" in file: 
                df = pd.read_csv(os.path.join(subject_dir, file))
                df.set_index('trial_type', inplace=True)
                if condition == 'CC':
                        df.loc['CS+', 'group'] = 'CS+CC'
                        df.loc['CS-', 'group'] = 'CS-CC'
                        
                else:
                        df.loc['CS+', 'group'] = 'CS+EXT'
                        df.loc['CS-', 'group'] = 'CS-EXT'
                        
                df.reset_index(inplace=True)                        
                df['subject'] = subject.strip('sub-MM')    
                df['phase'] = 'base' 
                df = df.drop([0, 1, 2, 3, 4, 5, 6])                
                df = df[df.columns.drop(list(df.filter(regex='inst|ex|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant|.stopped')))]
                df = df[['subject',
                         'trial_type',
                         'trial',
                         'phase',
                         'stimulus',
                         'cs_duration',
                         'iti_duration',
                         'trial_cs',
                         'group',
                         'block',
                         'trials_resp.keys',
                         'trials_resp.rt',
                         'trials_resp.started',
                         'animal.started',
                         'tool.started',
                         'session',
                         'date',
                         'psychopyVersion',
                         'frameRate']]
                df.reset_index(inplace=True, drop=True)
                os.chdir(cleanbl_dir)
                df.to_csv(f'cleaned_{file}')
            
#ran successfully on all groups 5/24/23. needs to be concatenated

#%%                set condition to CC and run groups 1 and 3. 
condition = 'CC'

for subject in group1:
    fixbase_everything(subject)
    
for subject in group3:
    fixbase_everything(subject)                
#%%             change condition to EXT and run groups 2 and 4.

condition = 'EXT'

for subject in group2:
    fixbase_everything(subject)
    
for subject in group4:
    fixbase_everything(subject)

#%% FEAR 
    
def fixfear_everything(subject):
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    cleanfear_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_fear')
    os.chdir(subject_dir)
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if ".csv" in file and "fear-acquisition" in file and "_202" in file: 
                df = pd.read_csv(os.path.join(subject_dir, file))
                df.set_index('trial_type', inplace=True)
                if condition == 'CC':
                        df.loc['CS+', 'group'] = 'CS+CC'
                        df.loc['CS-', 'group'] = 'CS-CC'
                        
                else:
                        df.loc['CS+', 'group'] = 'CS+EXT'
                        df.loc['CS-', 'group'] = 'CS-EXT'
                        
                df.reset_index(inplace=True)                        
                df['subject'] = subject.strip('sub-MM')    
                df = df.drop([0, 1, 2, 3, 4, 5])                
                df = df[df.columns.drop(list(df.filter(regex='inst|ex|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant|.stopped')))]
                df = df[['subject',
                         'trial_type',
                         'trial',
                         'phase',
                         'stimulus',
                         'cs_duration',
                         'iti_duration',
                         'trial_cs',
                         'group',
                         'block',
                         'trials_resp.keys',
                         'trials_resp.rt',
                         'trials_resp.started',
                         'animal.started',
                         'tool.started',
                         'session',
                         'date',
                         'psychopyVersion',
                         'frameRate']]
                df.reset_index(inplace=True, drop=True)
                os.chdir(cleanfear_dir)
                df.to_csv(f'cleaned_{file}')
            
#successfully run on all subjects on 5/24/23. needs to be concatenated, but run on sub64 first 

#%%                set condition to CC and run groups 1 and 3. 

condition = 'CC'

for subject in group1:
    fixfear_everything(subject)
    
for subject in group3:
    fixfear_everything(subject)                
#%%             change condition to EXT and run groups 2 and 4.

condition = 'EXT'

for subject in group2:
    fixfear_everything(subject)
    
for subject in group4:
    fixfear_everything(subject)
#%% EXTCC 
    
def fixextcc_everything(subject):
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    cleanextcc_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_extcc')
    os.chdir(subject_dir)
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if ".csv" in file and "extinction-cc" in file and "_202" in file: 
                df = pd.read_csv(os.path.join(subject_dir, file))
                df.set_index('trial_type', inplace=True)
                if condition == 'CC':
                        df.loc['CS+', 'group'] = 'CS+CC'
                        df.loc['CS-', 'group'] = 'CS-CC'
                        
                else:
                        df.loc['CS+', 'group'] = 'CS+EXT'
                        df.loc['CS-', 'group'] = 'CS-EXT'
           
                df['phase'] = 'extcc'           
                df.reset_index(inplace=True)                        
                df['subject'] = subject.strip('sub-MM')    
                df = df.drop([0])                
                df = df[df.columns.drop(list(df.filter(regex='inst|ex|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant|.stopped')))] 
                df = df[['subject',
                         'trial_type',
                         'trial',
                         'cc',
                         'phase',
                         'stimulus',
                         'cc_stimulus',
                         'cs_duration',
                         'iti_duration',
                         'trial_cs',
                         'group',
                         'block',
                         'trials_resp.keys',
                         'trials_resp.rt',
                         'trials_resp.started',
                         'animal.started',
                         'tool.started',
                         'cc_image.started',
                         'session',
                         'date',
                         'psychopyVersion',
                         'frameRate']]
                df.reset_index(inplace=True, drop=True)
                os.chdir(cleanextcc_dir)
                df.to_csv(f'cleaned_{file}')
            
#run on all subjects on 5/24/23. needs to be concatenated, but run on sub64 first

#%%                set condition to CC and run groups 1 and 3. 

condition = 'CC'

for subject in group1:
    fixextcc_everything(subject)
    
for subject in group3:
    fixextcc_everything(subject)                
#%%             change condition to EXT and run groups 2 and 4.

condition = 'EXT'

for subject in group2:
    fixextcc_everything(subject)
    
for subject in group4:
    fixextcc_everything(subject)    
#%% RENEWAL 
    
def fixrenewal_everything(subject):
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    cleanrenewal_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_renewal')
    os.chdir(subject_dir)
    for dirs, subdirs, files in os.walk(subject_dir):
        for file in files:
            if ".csv" in file and "renewal" in file and "_202" in file: 
                df = pd.read_csv(os.path.join(subject_dir, file))
                df.set_index('trial_type', inplace=True)
                if condition == 'CC':
                        df.loc['CS+', 'group'] = 'CS+CC'
                        df.loc['CS-', 'group'] = 'CS-CC'
                        
                else:
                        df.loc['CS+', 'group'] = 'CS+EXT'
                        df.loc['CS-', 'group'] = 'CS-EXT'
           
                df['phase'] = 'renewal'           
                df.reset_index(inplace=True)                        
                df['subject'] = subject.strip('sub-MM')    
                df = df.drop([0])                
                df = df[df.columns.drop(list(df.filter(regex='inst|ex|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant|.stopped')))] 
                df = df[['subject',
                         'trial_type',
                         'trial',
                         'phase',
                         'stimulus',
                         'cs_duration',
                         'iti_duration',
                         'trial_cs',
                         'group',
                         'trials_resp.keys',
                         'trials_resp.rt',
                         'trials_resp.started',
                         'animal.started',
                         'tool.started',
                         'session',
                         'date',
                         'psychopyVersion',
                         'frameRate']]
                df.reset_index(inplace=True, drop=True)
                os.chdir(cleanrenewal_dir)
                df.to_csv(f'cleaned_{file}')

#%%                set condition to CC and run groups 1 and 3. 

condition = 'CC'

for subject in group1:
    fixrenewal_everything(subject)
    
for subject in group3:
    fixrenewal_everything(subject)    

#after running: KeyError: "['trials_resp.rt'] not in index"            
#%%             change condition to EXT and run groups 2 and 4.

condition = 'EXT'

for subject in group2:
    fixrenewal_everything(subject)
    
for subject in group4:
    fixrenewal_everything(subject)
    
#%% CONCATENATE CONDITIONING

#wrote the concatenation code into a loop 5/27

cfolderlist = ['cleaned_baseline', 'cleaned_fear', 'cleaned_extcc', 'cleaned_renewal']

for folder in cfolderlist:
    data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{folder}')
    os.chdir(data_dir)

    cleanedrenewalfiles = glob.glob('./*csv')

#create an empty list on which to append the dataframes of the filenames in group1baseline
    cleaneddataframe = []
#iterate through list of files in group1baseline and import the csv of the corresponding name
    for file in cleanedrenewalfiles: 
        cleaneddataframe.append(pd.read_csv(file)) 

#concatenate thedataframes
    cleaneddatadf = pd.concat(cleaneddataframe)

    cleaneddatadf.to_csv(f'{folder}_compiled.csv' )
#%% RECOGNITION MEMORY add original trial numbers and clean, all in one
#ran successfully except for sub 64 who was missing some cols, noted in the counterbalancing sheet

def trialnums_clean_mem(subject): #this works!
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}') #setting directory per subject
    os.chdir(subject_dir) #change to directory
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles: #walk through every file in the directory
            if 'ses-2' in file and 'rec_memory' in file and '_202' in file and '.csv' in file: #pick out each subject's rec mem output file
               memdf = pd.read_csv(f'{subfolder}/{file}')
     #starting all of the original trial numbers code           
    day1_phases = ['base', 'fear', 'extcc']  #create list of day 1 phases
    day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases} #read the day 1 input files specific to the subject per iteration
    day1_inputs['base']['phase'] = 'base' #adding the phase column for base bc it wasnt there originally oops
    #renewal_inputs = pd.read_csv(f'{subject}_ses-2_task-renewal_events-input.csv').set_index('trial_type')
    stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases} #imports all of the stimuli from day 1 phases input files
    #renewal_csp = renewal_inputs.loc['CS+']
    #renewal_csm = renewal_inputs.loc['CS-']
    base_csp = stimset['base'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    base_csm = stimset['base'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    fear_csp = stimset['fear'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    fear_csm = stimset['fear'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csp = stimset['extcc'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csp['phase'] = 'extcc' #correcting phase from "ext". will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    extcc_csm = stimset['extcc'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csm['phase'] = 'extcc' #correcting phase from "ext". will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
   
    vertical_concat = pd.concat([base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm]) #concatenating the original inputs into one df
    mem_originaltrialnums = pd.merge(memdf, vertical_concat, on=['stimulus', 'phase'], how='left') #merging two dataframes to the left in order to assign the trial numbers to the stimulus in the mem dataset
    #that was the big line of code that actually assigned the stimuli their trial numbers. printing the df now should have all the data I need. 
    #now to clean:
    #clean using regex
    mem_originaltrialnums.drop(list(mem_originaltrialnums.filter(regex='inst|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant')), axis=1, inplace=True) #regular expression
    #rename trial_cs as origin_trialnumber
    mem_originaltrialnums = mem_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
    mem_originaltrialnums['subject'] = subject.strip('sub-MM') #add subject column
    #set groups
    if condition == 'CC':
            mem_originaltrialnums.loc['CS+', 'group'] = 'CS+CC'
            mem_originaltrialnums.loc['CS-', 'group'] = 'CS-CC'
            
    else:
            mem_originaltrialnums.loc['CS+', 'group'] = 'CS+EXT'
            mem_originaltrialnums.loc['CS-', 'group'] = 'CS-EXT'
    mem_originaltrialnums.drop([0,1,2,3,4], inplace=True) #drop unnecessary columns
    mem_originaltrialnums.reset_index(drop=True, inplace=True) #reset the index after drop
    #reordering all the columns explicitly
    mem_originaltrialnums = mem_originaltrialnums[['subject', 
             'trial_type', 
             'trial', 
             'phase', 
             'origin_trialnumber', 
             'group', 
             'stimulus', 
             'old_or_new', 
             'cs_duration', 
             'block',
             'iti_duration',
             'mem_resp.keys', 
             'mem_resp.rt', 
             'mem_image.started',
             'mem_question.started',
             'def_old.started',
             'maybe_old.started',
             'maybe_new.started',
             'def_new.started',
             'mem_resp.started',
             'stimulus2.started',
             'mem_question2.started',
             'def_old2.started',
             'maybe_old2.started',
             'maybe_new2.started',
             'def_new2.started',
             'stimulus2.stopped',
             'mem_question2.stopped',
             'def_old2.stopped',
             'maybe_old2.stopped',
             'maybe_new2.stopped',
             'def_new2.stopped',
             'session',
             'date',
             'expName',
             'psychopyVersion',
             'frameRate']]
    #show my work
    print(mem_originaltrialnums[['trial_type', 'phase', 'origin_trialnumber']].head(55))
    #create and change directory
    cleanmem_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_recmem') #setting directory per subject
    os.chdir(cleanmem_dir) #change to directory
    mem_originaltrialnums.to_csv(f'{subject}_memoutput_cleaned_edited.csv')   
#%%                set condition to CC and run groups 1 and 3. 

condition = 'CC'

for subject in group1:
    trialnums_clean_mem(subject)
  
for subject in group3:
    trialnums_clean_mem(subject)              
#%%             change condition to EXT and run groups 2 and 4.

condition = 'EXT'

for subject in group2:
    trialnums_clean_mem(subject) #for some reason subject 95 wont work ()
   
for subject in group4:
    trialnums_clean_mem(subject)
    
#%% CONCATENATE recognition memory 

#I just changed the necessary paramaters for every subject and moved them manually into their own folder lol
 
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_recmem')
cleaned_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'concat_memory')
os.chdir(data_dir)

cleanedrecmemfiles = glob.glob('./*csv')

import re
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#define the list here if you haven't already

cleanedrecmemfiles.sort(key=natural_keys)
print(cleanedrecmemfiles)

#create an empty list on which to append the dataframes of the filenames in group1baseline
cleanedrecmemframe = []
#iterate through list of files in group1baseline and import the csv of the corresponding name
for file in cleanedrecmemfiles: 
    cleanedrecmemframe.append(pd.read_csv(file)) 

#concatenate thedataframes
cleanedrecmemdf = pd.concat(cleanedrecmemframe)

os.chdir(cleaned_dir)
cleanedrecmemdf.to_csv('cleanedrecmem_compiled.csv') 

#all subjects cleaned and compiled including 64 and 40. 5/27       
#%%SOUTYP add original trial numbers and clean, all in one

def trialnums_clean_soutyp(subject):
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    cleansoutyp_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_soutyp')
    os.chdir(subject_dir)
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles: #walk through every file in the directory

            if ".csv" in file and "soutyp" in file and "_202" in file: 
                soutypdf = pd.read_csv(os.path.join(subject_dir, file))
          #      df.set_index('trial_type', inplace=True) pretty sure the index is already trial_type fresh out of psychopy
                if condition == 'CC':
                        soutypdf.loc['CS+', 'group'] = 'CS+CC'
                        soutypdf.loc['CS-', 'group'] = 'CS-CC'
                        
                else:
                        soutypdf.loc['CS+', 'group'] = 'CS+EXT'
                        soutypdf.loc['CS-', 'group'] = 'CS-EXT'
            
     #adding original trial numbers (INDENT IS MESSED UP HERE, 1:28 PM MAY 7TH)      
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

    soutypdf.reset_index(inplace = True, drop = True)
    soutypdf = soutypdf[soutypdf.columns.drop(list(soutypdf.filter(regex='inst|prac|feedback|Unnamed|iti|end_exp|beg_exp|crosshair|RepN|trials.this|participant')))] #regular expression
    soutypdf = soutypdf.drop([0,1,2,3,4, 5, 6, 7, 8, 9, 10])
    soutypdf['subject'] = subject.strip('sub-MM') #add subject column



    soutyp_originaltrialnums = pd.merge(soutypdf, vertical_concat, on=['stimulus', 'phase'], how='left')
#rename the column from trial_cs to origin_trialnumber
    soutyp_originaltrialnums = soutyp_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
  
   #reordering all the columns explicitly
    soutyp_originaltrialnums = soutyp_originaltrialnums[['subject', 
            'trial_type', 
            'trial', 
            'phase', 
            'origin_trialnumber', 
            'group', 
            'stimulus', 
            'block', 
            'sou_slider.response',
            'sou_slider.rt',
            'typ_slider.response',
            'typ_slider.rt',
            'sou_resp.started',
            'sou_pic.started',
            'sou_question.started',
            'sou_resp.keys',  
            'typ_resp.started',
            'typ_pic.started',
            'typ_question.started',
            'typ_resp.keys',
            'session',
            'date',
            'expName',
            'psychopyVersion',
            'frameRate']]
    soutyp_originaltrialnums.drop([144,145,146], inplace = True)
    print(soutyp_originaltrialnums)    
   #export and replace the original edit file with the cleaned one
    cleansoutyp_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_soutyp') #setting directory per subject
    os.chdir(cleansoutyp_dir) #change to directory
    soutyp_originaltrialnums.to_csv(f'{subject}_soutypoutput_cleaned_edited.csv')   
    
#got it working on 5/7

#%%                set condition to CC and run groups 1 and 3. 
condition = 'CC'

for subject in group1:
    trialnums_clean_soutyp(subject)
  
for subject in group3:
    trialnums_clean_soutyp(subject)                
#%%             change condition to EXT and run groups 2 and 4.
condition = 'EXT'

for subject in group2:
   trialnums_clean_soutyp(subject)
    
for subject in group4:
    trialnums_clean_soutyp(subject)    
#%% CONCATENATE soutyp
 
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_soutyp')
concat_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'concat_memory')
os.chdir(data_dir)

cleanedsoutypfiles = glob.glob('./*csv')

#create an empty list on which to append the dataframes of the filenames in group1baseline
cleanedsoutypframe = []
#iterate through list of files in group1baseline and import the csv of the corresponding name
for file in cleanedsoutypfiles: 
    cleanedsoutypframe.append(pd.read_csv(file)) 

#concatenate thedataframes
cleanedsoutypdf = pd.concat(cleanedsoutypframe)

os.chdir(concat_dir)
cleanedsoutypdf.to_csv('cleanedsoutyp_compiled.csv')   

#works, done and sent to joey on 5/7     


#%% AROUVAL add original trial numbers and clean, all in one 

#copied from ortrialnum file and modified 5/15

def trialnums_clean_arouval(subject): #this works!
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
    os.chdir(subject_dir)
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles:
            if 'ses-2' in file and 'arouval' in file and '_202' in file and '.csv' in file:
                arouvaldf = pd.read_csv(f'{subfolder}/{file}')
                arouvaldf.set_index('trial_type', inplace=True) 
  #groups
                if condition == 'CC':
                    arouvaldf.loc['CS+', 'group'] = 'CS+CC'
                    arouvaldf.loc['CS-', 'group'] = 'CS-CC'                         
                else:
                    arouvaldf.loc['CS+', 'group'] = 'CS+EXT'
                    arouvaldf.loc['CS-', 'group'] = 'CS-EXT'
                arouvaldf.reset_index(inplace=True)
  #beginning of origianl trial numbers code (needs testing) (LOSING AROUSAL COLUMNS AT SOME POINT IN THIS BLOCK) 5/15              
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
    arouval_otn = pd.merge(arouvaldf, vertical_concat, on=['stimulus', 'phase'], how='left') 
    arouval_otn.drop(columns=['trial_y', 'cs_duration', 'iti_duration'], inplace=True)
    arouval_otn.rename(columns={'trial_cs':'origin_trialnumber', 'trial_x':'trial', 'group_x':'group'}, inplace=True)
  #end of arouval code 
 
  #reset index, drop trash columns and empty rows, add subject column
    arouval_otn.reset_index(inplace = True, drop = True)
    arouval_otn = arouval_otn[arouval_otn.columns.drop(list(arouval_otn.filter(regex='inst|prac|feedback|Unnamed|iti|end_exp|beg_exp|crosshair|RepN|trials.this|participant|group_y')))] #regular expression
    arouval_otn = arouval_otn.drop([0,1,2,3,4, 5, 6, 7, 8, 9,50])
    arouval_otn['subject'] = subject.strip('sub-MM') #add subject column

 #reorder  
    arouval_otn = arouval_otn[[
     'subject',
     'trial_type',
     'trial',
     'phase',
     'origin_trialnumber',
     'group',
     'stimulus',
     'block',
     'arousal_slider.response',
     'arousal_slider.rt',
     'val_slider.response',
     'val_slider.rt',
     'val_pic.started',
     'val_question.started',
     'arousal_pic.started',
     'arousal_question.started',
     'arousal_slider.started',
     'session',
     'date',
     'expName',
     'psychopyVersion',
     'frameRate']]

    #export and replace the original edit file with the cleaned one 
    cleanarouval_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_arouval')
    os.chdir(cleanarouval_dir) #change to directory
    arouval_otn.to_csv(f'{subject}_arouvaloutput_cleaned_edited.csv')   

                 
#WORKS! run after last subject is run (sydney will give you the word)
#%%               set condition to CC and run groups 1 and 3. 
condition = 'CC'

for subject in group1:
    trialnums_clean_arouval(subject)
 
for subject in group3:
    trialnums_clean_arouval(subject)                
#%%             change condition to EXT and run groups 2 and 4.
condition = 'EXT'

for subject in group2:
   trialnums_clean_arouval(subject)
  
for subject in group4:
    trialnums_clean_arouval(subject)    
#%% CONCATENATE arouval
 
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_arouval')
concat_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', 'concat_memory')

os.chdir(data_dir)

cleanedarouvalfiles = glob.glob('./*csv')

#create an empty list on which to append the dataframes of the filenames in group1baseline
cleanedarouvalframe = []
#iterate through list of files in group1baseline and import the csv of the corresponding name
for file in cleanedarouvalfiles: 
    cleanedarouvalframe.append(pd.read_csv(file)) 

#concatenate thedataframes
cleanedarouvaldf = pd.concat(cleanedarouvalframe) #bug was in this line. fixed on 6/21
os.chdir(concat_dir)

cleanedarouvaldf.to_csv('cleanedarouval_compiled.csv')   

#%%

    import re
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [ atoi(c) for c in re.split(r'(\d+)', text) ]

    #define the list here if you haven't already

    cleanedrecmemfiles.sort(key=natural_keys)
    print(cleanedrecmemfiles)



combined_csv = pd.concat([pd.read_csv(f) for f in soutypfiles])
combined_csv.to_csv('see.csv')

#%%
#IF YOU NEED TO CLEAN AN INDIVIDUAL REC MEM RUN: 


def trialnums_clean_mem(sub64): #CREATED FOR SUBJECT 64, IT IS MISSING SOME ROWS IN THE ORGANIZATION BECAUSE OF THE BUG 64 WAS CAUSING
 #change the directory 
    home_dir = os.path.expanduser('~')
    subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', 'sub-MM064') #setting directory per subject
    os.chdir(subject_dir) #change to directory
    for subfolder, nothinghere, datafiles in os.walk(subject_dir):
        for file in datafiles: #walk through every file in the directory
            if 'ses-2' in file and 'rec_memory' in file and '_202' in file and '.csv' in file: #pick out each subject's rec mem output file
               memdf = pd.read_csv(f'{subfolder}/{file}')
     #starting all of the original trial numbers code           
    day1_phases = ['base', 'fear', 'extcc']  #create list of day 1 phases
    day1_inputs = {phase: pd.read_csv(f'sub-MM064_ses-1_task-{phase}_events-input.csv') for phase in day1_phases} #read the day 1 input files specific to the subject per iteration
    day1_inputs['base']['phase'] = 'base' #adding the phase column for base bc it wasnt there originally oops
    #renewal_inputs = pd.read_csv(f'{subject}_ses-2_task-renewal_events-input.csv').set_index('trial_type')
    stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases} #imports all of the stimuli from day 1 phases input files
    #renewal_csp = renewal_inputs.loc['CS+']
    #renewal_csm = renewal_inputs.loc['CS-']
    base_csp = stimset['base'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    base_csm = stimset['base'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    fear_csp = stimset['fear'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    fear_csm = stimset['fear'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csp = stimset['extcc'].loc['CS+'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csp['phase'] = 'extcc' #correcting phase from "ext". will mess up the iteration in the for loop later on using phases if i don't correct now 9/27
    extcc_csm = stimset['extcc'].loc['CS-'] #making separate dfs for CS+ and CS- from each day 1 phase
    extcc_csm['phase'] = 'extcc' #correcting phase from "ext". will mess up the iteration in the for loop later on using phases if i don't correct now 9/27

    vertical_concat = pd.concat([base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm]) #concatenating the original inputs into one df
    mem_originaltrialnums = pd.merge(memdf, vertical_concat, on=['stimulus', 'phase'], how='left') #merging two dataframes to the left in order to assign the trial numbers to the stimulus in the mem dataset
    #that was the big line of code that actually assigned the stimuli their trial numbers. printing the df now should have all the data I need. 
    #now to clean:
    #clean using regex
    mem_originaltrialnums.drop(list(mem_originaltrialnums.filter(regex='inst|Unnamed|end_exp|beg_exp|crosshair|RepN|trials.this|participant')), axis=1, inplace=True) #regular expression
    #rename trial_cs as origin_trialnumber
    mem_originaltrialnums = mem_originaltrialnums.rename(columns={'trial_cs':'origin_trialnumber'})
    mem_originaltrialnums['subject'] = subject.strip('sub-MM') #add subject column
    #set groups
    if condition == 'CC':
            mem_originaltrialnums.loc['CS+', 'group'] = 'CS+CC'
            mem_originaltrialnums.loc['CS-', 'group'] = 'CS-CC'

    else:
            mem_originaltrialnums.loc['CS+', 'group'] = 'CS+EXT'
            mem_originaltrialnums.loc['CS-', 'group'] = 'CS-EXT'
    mem_originaltrialnums.drop([0,1,2,3,4], inplace=True) #drop unnecessary columns
    mem_originaltrialnums.reset_index(drop=True, inplace=True) #reset the index after drop
    #reordering all the columns explicitly
    mem_originaltrialnums = mem_originaltrialnums[['subject', 
             'trial_type', 
             'trial', 
             'phase', 
             'origin_trialnumber', 
             'group', 
             'stimulus', 
             'old_or_new', 
             'cs_duration', 
             'block',
             'iti_duration',
             'mem_resp.keys', 
             'mem_resp.rt', 
             'mem_image.started',
             'mem_question.started',
             'def_old.started',
             'maybe_old.started',
             'maybe_new.started',
             'def_new.started',
             'mem_resp.started',
             'session',
             'date',
             'expName',
             'psychopyVersion',
             'frameRate']]
    #show my work
    print(mem_originaltrialnums[['trial_type', 'phase', 'origin_trialnumber']].head(55))
    #create and change directory
    cleanmem_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', 'cleaned_recmem') #setting directory per subject
    os.chdir(cleanmem_dir) #change to directory
    mem_originaltrialnums.to_csv('sub-MM064_memoutput_cleaned_edited.csv')





