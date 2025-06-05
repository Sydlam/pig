#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:53:58 2022

@author: sab5394
"""

import os 
home_dir = os.path.expanduser('~')
data_dir = os.path.join(home_dir, 'Desktop', 'mrs-m', 'experiment', 'data')
input_dir = os.path.join(home_dir,'Desktop', 'mrs-m', 'experiment', 'stims', 'cc_stims')
os.chdir(input_dir)

#%%
cc_dir = os.path.join('stims', 'cc_stims')


#%%
listoffiles = list()

for (dirpath, nothinghere, filenames) in os.walk(input_dir):
   listoffiles += [os.path.join(dirpath,file) for file in filenames]
   
#%%

filesdf = pd.DataFrame(listoffiles)