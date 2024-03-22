#####################################################################
## NOTE: YOU HAVE IMPORT THE CSV AND SELECT 'Text' FOR THE ID      ##
#####################################################################

import json
import os
import pandas as pd
import numpy as np
participant = '1'
participant = 'data_second_exhaustion'
#folder = f'./experiment/data/part_{participant}/'
folder = f'./experiment/{participant}/'
file_output_camera = 'output_'+f'{participant}_camera.csv'
file_output_round_info = 'output_'+f'{participant}_round_info.csv'

data_experiment_camera = pd.DataFrame()
data_experiment_round_info = pd.DataFrame()
json_files = []
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

for filename in json_files:
    # Open the JSON file and load its contents into a Python variable
    with open(filename, 'r') as file:
        name = filename

        if 'training' not in name and 'calibration' not in name:
            trial_round = filename.split("trialset_")[1][0:1]
            data = pd.DataFrame(json.load(file))
            if 'pepper' in filename or '4K' in filename:
                if 'pepper' in name:
                    name = 'pepper'
                else:
                    name='4K'
                
                if 'calibration' not in filename: # Note: Change later to also include the calibration
                    #print(filename)
                    data = data.rename(columns={'ID':'frame_id'})
                    #data['ID'] = data['ID'].str[-6:]
                    data['trial_round'] = trial_round
                    data['camera_source'] = name
                    data_experiment_camera = pd.concat([data_experiment_camera, data])

            elif 'round_info' in name:
                name = 'round_info'
                data = pd.DataFrame([{**{"index": k}, **v, **v.pop("keystroke")} for k, v in data.items()]).set_index('index')
                data.drop(columns='keystroke', inplace=True)
                #data['trial_round'] = trial_round
                data_experiment_round_info = pd.concat([data_experiment_round_info, data])

            else:
                print(f"CANNOT PROCESS FILE {filename}!!")
                raise Exception
            
# Show the inner workings of the round info saving:
data_experiment_round_info = data_experiment_round_info.reset_index()
data_experiment_round_info = data_experiment_round_info.rename(columns={data_experiment_round_info.columns[0]: 'trial_number'})

# Create the output file for the round info.
data_experiment_camera = data_experiment_camera.sort_values('time')
data_experiment_camera['time'] = pd.to_datetime(data_experiment_camera['time'], unit='s')
data_experiment_round_info['start'] = pd.to_datetime(data_experiment_round_info['start'], unit='s')
data_experiment_round_info['end'] = pd.to_datetime(data_experiment_round_info['end'], unit='s')
data_experiment_round_info['duration'] = pd.to_datetime(data_experiment_round_info['duration'], unit='s')
data_experiment_round_info.to_csv(file_output_round_info, sep=';')

'''
# Create the output file for the camera data
within_ranges = (data_experiment_camera['time'].values[:, np.newaxis] >= data_experiment_round_info['start'].values) & (data_experiment_camera['time'].values[:, np.newaxis] <= data_experiment_round_info['end'].values)
data_experiment_camera['trial_number'] = np.where(within_ranges.any(axis=1), data_experiment_round_info['trial_number'].values[within_ranges.argmax(axis=1)], np.nan)
#indexes_to_set = np.where(within_ranges.any(axis=1))[0]
'''

# Create a boolean mask indicating which rows fall within the specified ranges
within_ranges = (data_experiment_camera['time'].values[:, np.newaxis] >= data_experiment_round_info['start'].values) & (data_experiment_camera['time'].values[:, np.newaxis] <= data_experiment_round_info['end'].values)
for column in data_experiment_round_info.columns:
    data_experiment_camera[column] = np.nan
data_experiment_camera[data_experiment_round_info.columns] = np.where(within_ranges.any(axis=1)[:, np.newaxis], data_experiment_round_info.values[np.argmax(within_ranges, axis=1)], np.nan)
#print(data_experiment_camera.columns)
data_experiment_camera = data_experiment_camera.rename(columns={'duration':'repsonse_time',
                                                        'valid':'keywaspressed',
                                                        'direction':'direction_of_focus',
                                                        'first_item':'focus_modality',
                                                        'second_item':'secondary_modality'
                                                        })
data_experiment_camera = data_experiment_camera.drop('trial_id', axis=1)

print(data_experiment_camera.columns)
data_experiment_camera.to_csv(file_output_camera, sep=';')


print('fin')