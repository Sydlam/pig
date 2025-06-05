#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 13:13:07 2022

@author: sab5394
"""

#RUN THIS CODE FOR EACH SUBJECT TO ADD THE TRIAL NUMBERS TO THE OUTPUT FILES FOR SOURCE TYPICALITY VALENCE AND SOURCE MEMORY


import os 
import pandas as pd 
import numpy as np 

#%% 
#SET THE SUBJECT EVERY TIME I WANT TO RUN THIS CODE 

subject = 'sub-MM001'
day1_phases = ['base','fear','extcc']

home_dir = os.path.expanduser('~')
subject_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'data', f'{subject}')
os.chdir(subject_dir)

#entirety of soutypval input file, setting the index to the stimulus and the trial type
soutypdf = pd.read_csv(f'{subject}_ses-2_task-soutyp_events-input.csv').set_index(['trial_type', 'stimulus'])

#day1_phases = ['base','fear','extcc']

#making a dictionary that has a key that is the phase and a value that is the dataframe. 

day1_inputs = {phase: pd.read_csv(f'{subject}_ses-1_task-{phase}_events-input.csv') for phase in day1_phases}
renewal_inputs = pd.read_csv(f'{subject}_ses-2_task-renewal_events-input.csv')

#%%
#adds the phase column to the base input file which for some reason doesnt have it? Consider adding this? 8/24
day1_inputs['base']['phase'] = 'base'
#%%
#creating stim lists for each phase

stimset = {phase: day1_inputs[f'{phase}'][['stimulus', 'trial_cs', 'phase', 'trial_type']].set_index('trial_type') for phase in day1_phases}

#%%
#TRYING TO PUT EVERYTHING BELOW THIS POINT INTO A LOOP 

cs_phases = ['base_csp', 'base_csm', 'fear_csp', 'fear_csm', 'extcc_csp', 'extcc_csm']

#trying to select out only the options from each CS type

#for each phase:
for phase in cs_phases: 
    #for both CS+ and CS-:
    for con in ['CS+', 'CS-']:  
        #create a new dictionary where the key is the phase name from the list of cs_phases, and the key is the CS+ or CS- from the stimset values' datasets.
        cs_stimset = {phase: stimset[phase].loc[con]} 
        
        #this is where I am leaving off. So close! 8/26

#brute force for the loop above:

#separate out into dataframes separated by CS type

base_csp = stimset['base'].loc['CS+']
base_csm = stimset['base'].loc['CS-']
fear_csp = stimset['fear'].loc['CS+']
fear_csm = stimset['fear'].loc['CS-']
extcc_csp = stimset['extcc'].loc['CS+']
extcc_csm = stimset['extcc'].loc['CS-']

#create a list of all of those dataframes
csgrouplist = [base_csm, base_csp, fear_csm, fear_csp, extcc_csp, extcc_csm]

#reset the indices 
for x in csgrouplist: 
    x = x.reset_index(inplace = True)

    
#%%

#This was my attempt at looping the brute force method below. But that didn't work. 9/14

for phase in csgrouplist: 
    for con in ['CS+', 'CS-']:
        #'base_csm_CS+_trials' = soutypdf indexed by where each item in the phase column is equal to the phase in the loop AND wehre the trial type matches the condition in the loop
        f'{phase}_{con}_trials' = soutypdf.loc[(soutypdf['phase'] == f'{phase}') & (soutypdf['trial_type'] == f'{con}')] #resume here
    
    
#%%
soutypdf = soutypdf.reset_index()

#BRUTE FORCE: This is creating a subset of the soutypval input sheet for each individual subject per each phase and trial type. 9/14

#soutypdf['origin_trialnumber'] = base_csm['trial_cs'] #ValueError: cannot reindex on an axis with duplicate labels
base_csm_trials = soutypdf.loc[(soutypdf['phase'] == 'base') & (soutypdf['trial_type'] == 'CS-')]

#soutypdf['origin_trialnumber'] = base_csp['trial_cs'] #ValueError: cannot reindex on an axis with duplicate labels
base_csp_trials = soutypdf.loc[(soutypdf['phase'] == 'base') & (soutypdf['trial_type'] == 'CS+')]

#soutypdf['origin_trialnumber'] = fear_csp['trial_cs'] #ValueError: cannot reindex on an axis with duplicate labels
fear_csp_trials = soutypdf.loc[(soutypdf['phase'] == 'fear') & (soutypdf['trial_type'] == 'CS+')]

#soutypdf['origin_trialnumber'] = fear_csm['trial_cs'] #ValueError: cannot reindex on an axis with duplicate labels
fear_csm_trials = soutypdf.loc[(soutypdf['phase'] == 'fear') & (soutypdf['trial_type'] == 'CS-')]

#same code as above, but with some extra code from nicole added. 
#We are inserting block number, aka whether it is the first or second half of the day 1 phase where the photo was presented.



#soutypdf['origin_trialnumber'] = extcc_csm['trial_cs'] #ValueError: cannot reindex on an axis with duplicate labels
extcc_csm_trials = soutypdf.loc[(soutypdf['phase'] == 'extcc') & (soutypdf['trial_type'] == 'CS-')]

extcc_csm_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(0), np.less_equal(extcc_csm_trials['origin_trialnumber'], 12)),
 'block'
] = '1'
extcc_csm_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(12), np.less_equal(extcc_csm_trials['origin_trialnumber'], 24)),
 'block'
] = '2'

#%%

#THIS IS WHERE THIS LEFT OFF, 9/14. THIS IS THE ATTEMPT AT DOING BLOCK

#set both of their indices to stimulus
soutypdf = soutypdf.reset_index(inplace=True).set_index('stimulus')
extcc_csp = extcc_csp.reset_index(inplace=True).set_index('stimulus')

soutypdf['origin_trialnumber'] = extcc_csp['trial_cs']
extcc_csp_trials = soutypdf.loc[(soutypdf['phase'] == 'extcc') & (soutypdf['trial_type'] == 'CS+')]
extcc_csp_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(0), np.less_equal(extcc_csp_trials['origin_trialnumber'], 12)),
 'block'
] = '1'

extcc_csp_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(12), np.less_equal(extcc_csp_trials['origin_trialnumber'], 24)),
 'block'
] = '2'


#%%

soutypdf.loc[soutypdf['phase'] == 'extcc']

#%%
phasestims = pd.concat([basestims, extccstims, fearstims, renewalstims])
soutypdf['origin_trialnumber'] = phasestims['trial_cs']
   
#%%

soutypdf['origin_trialnumber'] = basestims['trial_cs']
#%%%
soutypdf['origin_trialnumber'] = extccstims['trial_cs']

#%%
soutypdf['origin_trialnumber'] = fearstims['trial_cs']
soutypdf['origin_trialnumber'] = renewalstims['trial_cs']

#%%
memdf['origin_trialnumber'] = phasestims['trial_cs']
arouvaldf['origin_trialnumber'] = phasestims['trial_cs']
#%%
soutypdf.to_csv(f'{subject}_ses-2_task-soutyp_events-input.csv')
memdf.to_csv(f'{subject}_ses-2_task-renewal_events-input.csv')
arouvaldf.to_csv(f'{subject}_ses-2_task-arouval_events-input.csv')

#%%
soutypdf.to_csv('a_seewhatsup.csv')

#%%
#ADD BLOCK PER SUB-UNIT OF CS TYPE AND PHASE

extcc_csm_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(0), np.less_equal(extcc_csm_trials['origin_trialnumber'], 12)),
 'block'
] = '1'

extcc_csm_trials.loc[
 np.logical_and(extcc_csm_trials['origin_trialnumber'].gt(12), np.less_equal(extcc_csm_trials['origin_trialnumber'], 24)),
 'block'
] = '2'


#%%

memdf = pd.read_csv(f'{subject}_ses-2_task-rec-memory_events-input.csv').set_index('trial_type')
arouvaldf = pd.read_csv(f'{subject}_ses-2_task-arouval_events-input.csv').set_index('trial_type')