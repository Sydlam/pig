#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:03:54 2022

@author: sophiabibb
"""

#arouval stim set creation 


import pandas as pd 
import os
import numpy as np 
import random

#%%

bidsID = 'sub-MM{0:0=3d}'.format(int(user_input[0]))

#%%

#bidsID = 'sub-MM101' #for testing in python

home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data', bidsID)
input_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'stims')
os.chdir(data_dir)


#%%
#RENEWAL STIMS
renewal_input = pd.read_csv(f'{bidsID}_ses-2_task-renewal_events-input.csv')
renewal_stims = renewal_input['stimulus'].values
renewal_stims_trials_phase = renewal_input[['stimulus', 'trial', 'trial_type']].drop(labels=0)
renewal_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
renewal_stims_trials_phase['phase'] = 'renewal'
print(renewal_stims_trials_phase)

#%%
#BASE STIMS 
base_input = pd.read_csv(f'{bidsID}_ses-1_task-base_events-input.csv')
base_stims = base_input['stimulus'].values
base_stims_trials_phase = base_input[['stimulus', 'trial', 'trial_type']]
base_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
base_stims_trials_phase['phase'] = 'base'
print(base_stims_trials_phase)
#%%
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
#%%
#EXTCC STIMS 
extcc_input = pd.read_csv(f'{bidsID}_ses-1_task-extcc_events-input.csv')
extcc_stims = extcc_input['stimulus'].values
extcc_stims_trials_phase = extcc_input[['stimulus', 'trial', 'trial_type']]
extcc_stims_trials_phase['us'] = 0 #to give all the dataframes the same columns so i can concatenate later
extcc_stims_trials_phase['phase'] = 'extcc'
print(extcc_stims_trials_phase)

#%%
#RENEWAL: select the stims
renewal_stims_trials_phase = renewal_stims_trials_phase.set_index('trial_type')
renewal_stims_csm = renewal_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
renewal_stims_csp = renewal_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
renewal_stims = pd.concat([renewal_stims_csp, renewal_stims_csm])
print(renewal_stims)
#%%
base_stims_trials_phase = base_stims_trials_phase.set_index('trial_type')
base_stims_csm = base_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
base_stims_csp = base_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
base_stims = pd.concat([base_stims_csp, base_stims_csm])
print(base_stims)
#%%
fear_stims_trials_phase = fear_stims_trials_phase.set_index('trial_type')
fear_stims_csm = fear_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
fear_stims_csp = fear_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
fear_stims = pd.concat([fear_stims_csp, fear_stims_csm])
print(fear_stims)
#%%
extcc_stims_trials_phase = extcc_stims_trials_phase.set_index('trial_type')
extcc_stims_csm = extcc_stims_trials_phase.loc['CS-'].sample(n=5).reset_index()
extcc_stims_csp = extcc_stims_trials_phase.loc['CS+'].sample(n=5).reset_index()
extcc_stims = pd.concat([extcc_stims_csp, extcc_stims_csm])
print(extcc_stims)
#%%
all_stims = pd.concat([base_stims, fear_stims, extcc_stims, renewal_stims])
all_stims.rename(columns={'trial': 'original_trial'})
print(all_stims)

#%%
#FILL IN THE TEMPLATE WITH ALL MY STIMS 

#import the template 
arouval_df = pd.read_csv('../../task_templates/arouval_template.csv').set_index(['trial_type', 'phase'])

all_stims = all_stims.set_index(['trial_type', 'phase'])

#%%
for con in ['CS-', 'CS+']:
    for phase in ['base', 'fear', 'extcc', 'renewal']:
        arouval_df.loc[(con, phase), 'stimulus'] = all_stims.loc[(con, phase)]

arouval_df.reset_index()

#%%
arouval_df.to_csv(f'{bidsID}_ses-2_task-arouval_events-input.csv')









