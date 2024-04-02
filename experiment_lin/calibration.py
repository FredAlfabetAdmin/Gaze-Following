import queue
import cv2
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf
from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording, NaoqiMotionRecorderConf
from sic_framework.devices.common_naoqi.naoqi_autonomous import NaoBasicAwarenessRequest, NaoBackgroundMovingRequest, NaoRestRequest, NaoWakeUpRequest
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.pepper import Pepper
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import cv2 as cv
import time
import pandas as pd
import sys
import threading
import os

from auxillary import show_current_stage,  save_dataframe_to_csv, append_info_to_list, get_brio_id, dump_trialset_to_json
from recorder import Recorder
from threader import Threader, write_single_frame, set_active, start_processing_images
from settings import participant_id, ip, has_eyetracker, is_training
from tablet import show_tablet_empty, set_pepper_tablet
from time_frame_matching import execute_csv

############################################################
def calibrate():
    df = pd.DataFrame(columns=['time', 'frame_id'])
    dictionary_list = []
    next_item_times = []
    i = 0

    start_time = time.time()
    current_time = time.time()
    print(f'Start time: {start_time}')
    
    # Save the datapoints to a file
    df = pd.DataFrame(dictionary_list)
    df.to_csv('./data_frames.csv', index=False)
    df = pd.DataFrame(next_item_times)
    df.to_csv('./data_focus_times.csv', index=False)
    print("finished calibration recording")

def run_test(video_recorder: Recorder):
    # Parameters
    current_focus_point = 0
    time_inbetween = 4
    #next_item_times = []

    print('In run test')
    '''
    focus_point = [
        ' ',
        'please look at my head camera',
        'please look at my face',
        'please look at my tablet',
        'please look at  left elbow',
        'please look at  right elbow',
        'the part ended, please take off your glasses',
        ' ',
        'please look at my head camera',
        'please look at my face ',
        'please look at my tablet',
        'please look at  left elbow',
        'please look at  right elbow',
        'calibration finished! thank you very much!',
        '']
    '''
    
    focus_point = [
        f'This calibration is for {"with" if video_recorder.get_is_eyetracker() else "without"} eyetracker',
        ' ',
        'please look at my head camera',
        'please look at my nose',
        'please look at my tablet',
        'please look at  left elbow',
        'please look at  right elbow',
        'calibration finished! thank you very much!',
        '']

    '''
    focus_point = [
        ' ',
        'please look at my head camera',
        'please look at my face']
    '''
    
    # Start recording the video
    # print(video_recorder.get_currently_recording())
    # while not video_recorder.get_currently_recording():
    #     print("[EXPERIMENT-RECORDER] WARNING: Currently not recording.")
    #     time.sleep(1)

    time.sleep(2)
    nao.tts.request(NaoqiTextToSpeechRequest('please get in front of the Pepper'))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[1], recorded_joints=["LShoulderRoll"], recorded_times=[[1]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[-1], recorded_joints=["RShoulderRoll"], recorded_times=[[1]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.3], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]])))
    
    # This line for some reason causes a slight movement of the HeadYaw to the left or right.
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.4], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]]))) 
    
    # Recalibrate the head yaw to be centered
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[-0.5, 0.5, 0], recorded_joints=['HeadYaw'], recorded_times=[[0, 1, 2]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=['HeadYaw'], recorded_times=[[0, 1]])))

    # Time tracking
    start_time = time.time()
    current_time = time.time()
    last_execution_time = time.time()
    print(f'Start time: {start_time}')

    # Actually execute the motions
    i = 0
    round_info = {}
    while len(focus_point) > current_focus_point:       
        if current_time > last_execution_time + time_inbetween:
            passed = f'{(current_time - start_time):010}'
            #print(f'Time to execute the next calibration part at {current_time} - passed: {passed} - {focus_point[current_focus_point]}')
            new_data = {
                'start': last_execution_time,
                'end':current_time,
                'speech':focus_point[current_focus_point]}
            #next_item_times.append(new_data)
            round_info[current_focus_point] = new_data
            nao.tts.request(NaoqiTextToSpeechRequest(focus_point[current_focus_point]))
            current_focus_point += 1
            last_execution_time = time.time()
            #print(f'[CALIBRATION] Gave new instructions')
        if current_focus_point == len(focus_point):
            #print('[CALIBRATION] Finished all instructions')
            break
        current_time = time.time()
        i += 1

    # Save the datapoints to a file
    #print(round_info)
    data = pd.DataFrame(round_info) 
    #print(data)
    data = data.transpose()
    #print(data)
    #data_experiment_round_info = pd.concat([data_experiment_round_info, data])
    data.to_csv(video_recorder.get_video_name() + 'round_info.csv', sep = ';')

    #save_dataframe_to_csv(next_item_times, video_recorder.get_video_name() + 'data_focus_times')
    #video_recorder.get_is_eyetracker()

    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["LShoulderRoll"], recorded_times=[[0]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["RShoulderRoll"], recorded_times=[[0]])))
    video_recorder.stop_video_recording()
    #print("[CALIBRATION] Finished calibration recording")
    
def on_image(image_message: CompressedImageMessage):
    imgs.put(image_message.image)

def record_pepper(video_recorder: Recorder):
    pepper_frameless = []
    i = 0
    #print("[PEPPER] Info on Pepper recording:")
    i_await = 0
    while not video_recorder.get_currently_recording():
        sys.stdout.write(f'\r[PEPPER] Awaiting 4K start ({i_await} seconds passed)')
        sys.stdout.flush()
        time.sleep(1)
        i_await += 1
    #print("[PEPPER] Starting to calibrate video")
    
    set_active(True)
    img = imgs.get()
    #print(f"PEPPER SHAPE: {img.shape}")
    while video_recorder.get_currently_recording():
        #pass
        img = imgs.get()
        pepper_frameless , i = append_info_to_list(pepper_frameless, i)
        write_single_frame(i, img[..., ::-1], video_recorder.get_video_name(), _4K = False)
    #print("[PEPPER] Ended video recording loop Pepper")
    cv.destroyAllWindows()    
    set_active(False)
    #print(f'[PEPPER] Starting to write the Pepper dataframe to IO ({len(pepper_frameless)} items)')
    save_dataframe_to_csv(video_recorder.get_video_name(), pepper_frameless, 'pepper', video_recorder.get_is_eyetracker())
    #print("[PEPPER] Finished saving images from Pepper")

######################## PARAMETER SETUP ########################
imgs = queue.Queue()

# Pepper preparation
nao = Pepper(ip,top_camera_conf = NaoqiCameraConf(vflip=0, res_id=2))#, motion_record_conf = conf_rec, top_camera_conf=conf_cam)
nao.top_camera.register_callback(on_image)
nao.autonomous.request(NaoWakeUpRequest())
nao.autonomous.request(NaoBasicAwarenessRequest(False))
nao.autonomous.request(NaoBackgroundMovingRequest(False))
#nao.top_camera.register_callback(on_image)

set_pepper_tablet(nao)
#show_tablet_vu_logo()
show_tablet_empty()

# Prepare the recorder
is_eyetracker = has_eyetracker
training = is_training
video_recorder = Recorder()
video_recorder.set_capture_device(get_brio_id())
video_recorder.set_participant_id(participant_id)
video_recorder.set_is_eyetracker(is_eyetracker)
video_recorder.set_calibration_formal_mode('calibration')
video_recorder.set_is_training(False)

threader = Threader()

if len(os.listdir(video_recorder.get_video_name())) > 0:
    input("WARNING: DIRECTORY ALREADY EXISTS!")
#csv_with_rounds_exists(video_recorder.participant_id, trial_round, video_recorder.get_is_eyetracker(), video_recorder.get_calibration_formal_mode())

# Execute the actual calibration
show_current_stage('STARTING CALIBRATION')
def run_nothing():
    pass

if video_recorder.participant_id == -1:
    if str.lower(input("WARNING: PARTICIPANT ID IS -1. CHECK IF CORRECT!! continue [Y/n]?")) != 'y':
        raise Exception

threader.triple_parallel(video_recorder.start_video_recording, record_pepper, run_test, second_args=video_recorder, third_args=video_recorder)
#threader.triple_parallel(run_nothing, run_nothing, run_test, third_args=video_recorder)
#nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["LShoulderRoll"], recorded_times=[[0, 1]])))
#nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["RShoulderRoll"], recorded_times=[[0, 1]])))

#video_recorder.stop_video_recording()
#print("[CALIBRATION] Finished executing the calibration")

nao.tts.request(NaoqiTextToSpeechRequest('Saved images. Calibration test is over.'))
#print("fin")