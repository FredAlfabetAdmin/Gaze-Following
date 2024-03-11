import os
import json
import pandas as pd
import time

# Pretty prints the current stage in the terminal
def show_current_stage(value):
    string_func = lambda x: ''.join(["=" for _ in range(len(x))])
    print("")
    print(f"====={string_func(value)}=====")
    print(f"===  {value}  ===")
    print(f"====={string_func(value)}=====")

# Determines for the first item if which direction it has to go.
def left_or_right(congruent, direction):
    if (congruent and direction == 'left') or (not congruent and direction == 'right'):
        return 'left'
    else: 
        return 'right'

# Checks with the participant if they are ready for the next set of trials.
def confirm_ready():
    ready_for_next = ''
    while not (ready_for_next == 'Y' or ready_for_next == 'y'):
        ready_for_next = input("Pausing. Ready to continue? [Y/n]")
    return True

# This function appends data to the end of a file (useful for saving trialdata)
folder_data = './data/'
def dump_trialset_to_json(data, trial_set, participant_id):
    with open(get_participant_folder(participant_id) + f'trial_info_{trial_set}.json', 'w') as f:
        json.dump(data, f)

# This function creates the data folder and the folder for the data of a specific participant
def create_data_folders(participant_id):
    folder_name = get_participant_folder(participant_id)
    print(folder_name)
    if os.path.isdir(folder_name):
        ok = input('8888888888888888888888888888\nWARNING THIS PARTICIPANT ALREADY HAS A FOLDER! CONTINUE? [Y/n]\n8888888888888888888888888888')
        if ok.upper() != 'Y':
            raise Exception ('INPUT WAS NOT Y. ABORT')
    os.makedirs(folder_data, exist_ok=True)
    os.makedirs(get_participant_folder(participant_id), exist_ok=True)

def get_participant_folder(participant_id):
    return folder_data + f'part_{participant_id}/'

def save_dataframe_to_csv(dict, filename):
    df = pd.DataFrame(dict)    
    df.to_json(f'{filename}.json', index=False)
    print(f"[I/O] Finished writing {filename} to json")

def append_info_to_list(_frameless_list, _i):
    formatted_i = '{:010d}'.format(_i)
    _frameless_data = {
        'ID':formatted_i,
        'time':time.time()
    }
    _frameless_list.append(_frameless_data)
    _i += 1
    return _frameless_list, _i