import queue
import cv2
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf
from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.pepper import Pepper
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
import time
import pandas as pd

focus_point = [
    ' ',
    'please look at my head camera',
    'please look at my face',
    'please look at my tablet',
    'please look at my left elbow',
    'please look at my right elbow',
    'the part ended, please take off your glasses',
    ' ',
    'please look at my head camera',
    'please look at my face ',
    'please look at my tablet',
    'please look at my left arm',
    'please look at my right arm',
    'calibration finished! thanks very much!']

focus_point = [
    ' ',
    'please look at my head camera',
    'please look at my face']
current_focus_point = 0
time_inbetween = 4

nao = Nao(ip="10.0.0.237")
def calibrate():
    df = pd.DataFrame(columns=['time', 'frame_id'])
    dictionary_list = []
    next_item_times = []
    i=0

    start_time = time.time()
    current_time = time.time()
    print(f'Start time: {start_time}')
    while time.time() < start_time + (len(focus_point) * time_inbetween):
        # For every 3 seconds, go to the next output.
        #print(focus_point[current_focus_point])
        to_check = ((current_focus_point * time_inbetween) + start_time)
        
        print(f'Seconds remaining until next bodypart: {(to_check - current_time):.4f}')

        frame_id = f'{i:010}'
        dictionary_data = {
            'current_focus_point': current_focus_point,
            'frame_id': frame_id,
            'time': current_time
        }
        dictionary_list.append(dictionary_data)

        if current_time > to_check:
            print(f'Time to execute the next calibration part at {time.time()} - passed: {time.time() - start_time}')
            print(f'{focus_point[current_focus_point]}')
            next_item_times.append({
                'current_focus_point':current_focus_point,
                'frame_id': frame_id,
                'time':current_time,
                'speech':focus_point[current_focus_point]})
            nao.tts.request(NaoqiTextToSpeechRequest(focus_point[current_focus_point]))
            current_focus_point += 1
            
            print('done')
        if current_focus_point == len(focus_point):
            print('finished. Breaking')
            break
        current_time = time.time()
        i+=1

    # Save the datapoints to a file
    df = pd.DataFrame(dictionary_list)
    df.to_csv('./data_frames.csv', index=False)
    df = pd.DataFrame(next_item_times)
    df.to_csv('./data_focus_times.csv', index=False)
    print("finished calibration recording")
print('fin')