import json
import os
import time

import datetime

folder = './experiment/data/part_-1/'

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

json_files = find_json_files(folder)
for filename in json_files:
    if 'data_focus_times' not in filename:
        # Open the JSON file and load its contents into a Python variable
        with open(filename, 'r') as file:
            data = json.load(file)
            
            print(f'File: {filename}')
            # Extract timestamps
            timestamps = list(data['time'].values())

            # Calculate FPS
            total_frames = len(timestamps)
            time_duration = timestamps[-1] - timestamps[0]
            fps = total_frames / time_duration

            print("Total Frames:", total_frames)
            print("Time Duration (seconds):", time_duration)
            print("FPS:", fps)
            print()