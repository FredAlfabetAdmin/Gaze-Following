#####################################################################
## NOTE: YOU HAVE IMPORT THE CSV AND SELECT 'Text' FOR THE ID      ##
#####################################################################

import json
import os
import time
import pandas as pd
import numpy as np

import datetime

participant = '1'
folder = f'./experiment/data/part_{participant}/'

# Specify the path to your JSON file
def find_json_files(folder_path):
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def calculate_fps(time_duration, num_items):
    # Parse the time duration string to extract total seconds
    total_seconds = sum(x * float(t) for x, t in zip([3600, 60, 1], time_duration.split(':')))

    # Convert total seconds to frames per second
    fps = num_items / total_seconds
    return fps

def find_closest(data, value):
    index = np.argmin(np.abs(np.array(data) - value))
    if data.iloc[index] > value:
        index -= 1
    return index
    #return min(data, key=lambda x:abs(x - value))

json_files = find_json_files(folder)
#print(json_files)
data_set = {}
for filename in json_files:
    # Open the JSON file and load its contents into a Python variable
    with open(filename, 'r') as file:
        name = filename
        #print()
        #print(name)
        #print(name)
        #name = name.replace(folder, '').replace('.json', '')[-6:]
        data = pd.DataFrame(json.load(file))
        if 'pepper' in name:
            name = 'pepper'
            data['ID'] = data['ID'].str[-6:]
            print(data['ID'])
        elif '4K' in name:
            name = '4K'
            data['ID'] = data['ID'].str[-6:]
        elif 'times' in name:
            name = 'times'
            print(data.columns)
            data = data.drop('frame_id', axis='columns')
        elif 'frames' in name:
            name = 'frames'
            data = data.drop('frame_id', axis='columns')
        data_set[name] = data
        #data_set[name] = data_set[name].astype({'time': 'str'})
        #print(data_set[name].head(5))
        data_set[name].to_csv(name + '.csv')

# for col in data_set.keys():
    # data_set[col] = data_set[col].astype({'time': 'str'})
        



print('***********************')
transfer_moments = {}
data_set['4K']['speech'] = np.nan
data_set['pepper']['speech'] = np.nan
last_point_4K = 0e
last_point_pepper = 0
for t in data_set['times'].iterrows():
    #print()
    #print(t[1]['speech'])
    #print(t)
    # Closest match:
    time_focus = t[1]['time']
    
    index_4k = find_closest(data_set['4K']['time'], time_focus)
    index_pepper = find_closest(data_set['pepper']['time'], time_focus)
    #print(f'Focus time: {time_focus} - time_4K: {data_set["4K"].iloc[index_4k]} - time_pepper: {data_set["pepper"].iloc[index_pepper]}')
    transfer_moments[t[0]] = {
        'time_focus':{'time':time_focus,'speech':t[1]['speech']},
        'time_4k':      {'ID': index_4k,        'time':data_set["4K"].iloc[index_4k]['time']},#,           'dif':time_focus - data_set["4K"].iloc[index_4k]['time']},
        'time_pepper':  {'ID': index_pepper,    'time':data_set["pepper"].iloc[index_pepper]['time']}#,   'dif':time_focus - data_set["pepper"].iloc[index_pepper]['time']}
        }
    if t[1]['speech'] not in (
        " ",
        "the part ended, please take off your glasses",
        "calibration finished! thank you very much!"):
        data_set['4K']['speech'].iloc[last_point_4K : index_4k] = t[1]['speech']
        data_set['pepper']['speech'].iloc[last_point_pepper : index_pepper] = t[1]['speech']
    
    last_point_4K = index_4k
    last_point_pepper = index_pepper
# print("** Transfer moments: **")
# for x in transfer_moments:
#     print()
#     print(transfer_moments[x])

# Take the transfer moment and place the speech as appended to the DataFrame based on the 

data_set['4K'].to_csv('4K_lin' + '.csv')
data_set['pepper'].to_csv('pepper_lin' + '.csv')


print('fin')