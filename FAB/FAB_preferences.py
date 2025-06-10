
'''set-up info'''
study_prefix = 'FB' # change to study identifier; string, SU stands for summation

port_label_1 = "VR" #string
port_type_1 = 'P' #serial (S) or parallel (P), case sensitive; string
port_address_1 = '0xEFF8' #string

port_label_2 = "Behavior" #string
port_type_2 = 'P' #serial (S) or parallel (P), case sensitive; string
port_address_2 = '0x3FB8'#string

shock_duration = .05 # milisecond format (); integer
shock_code = 2 # event/trigger code for shock delivery, for parallel port will correspond to pin that sends correct code; integer
stimulus_code = 4 # event/trigger code for stimulus onset/on,  for parallel port will correspond to pin that sends correct code; integer
FPS_code = 3 # event/trigger code for FPS audio file onset/finish audio file playing,  for parallel port will correspond to pin that sends correct code; integer
cs_duration= 5
FPS_duration = 0.05
iti_range=range(4,6)


