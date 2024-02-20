import os
import json

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
'''
def append_trial_data_to_file(participant_id, data):
    with open(folder_data + f'part_{participant_id}' + "/trial_info.txt", "a+") as file_:
        file_.writelines(str(data) + "\r")
'''
def dump_trialset_to_json(data, trial_set, participant_id):
    with open(get_participant_folder(participant_id) + f'trial_info_{trial_set}.json', 'w') as f:
        json.dump(data, f)

# This function creates the data folder and the folder for the data of a specific participant
def create_data_folders(participant_id):
    os.makedirs(folder_data, exist_ok=True)
    os.makedirs(get_participant_folder(participant_id), exist_ok=True)

def get_participant_folder(participant_id):
    return folder_data + f'part_{participant_id}/'