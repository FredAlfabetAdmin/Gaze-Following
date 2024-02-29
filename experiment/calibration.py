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

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations, talk_ready
from auxillary import show_current_stage, left_or_right, confirm_ready, dump_trialset_to_json, create_data_folders, save_dataframe_to_csv
from randomizer import create_random_trials
from recorder import Recorder#, start_video_recording, stop_video_recording, set_participant_id, set_trial_set, get_is_currently_recording
from threader import Threader

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
    global is_recording_pepper
    #df = pd.DataFrame(columns=['time', 'frame_id'])
    dictionary_list = []
    next_item_times = []
    current_focus_point = 0
    time_inbetween = 4

    print('In run test')
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
        'calibration finished! thanks very much!',
        '']

    #'''
    focus_point = [
        ' ',
        'please look at my head camera',
        'please look at my face']
    #'''
    
    # Start recording the video
    print(video_recorder.get_currently_recording())
    while not video_recorder.get_currently_recording():
        print("[EXPERIMENT-RECORDER] WARNING: Currently not recording.")
        time.sleep(1)

    time.sleep(2)
    nao.tts.request(NaoqiTextToSpeechRequest('please get in front of the Pepper'))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[1], recorded_joints=["LShoulderRoll"], recorded_times=[[1]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[-1], recorded_joints=["RShoulderRoll"], recorded_times=[[1]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.3], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]])))
    
    # Time tracking
    start_time = time.time()
    current_time = time.time()
    last_execution_time = time.time()
    print(f'Start time: {start_time}')

    # Actually execute the motions
    i=0
    while len(focus_point) > current_focus_point:
        frame_id = f'{i:010}'
        dictionary_data = {
            'current_focus_point': current_focus_point,
            'frame_id': frame_id,
            'time': current_time
        }
        dictionary_list.append(dictionary_data)
        
        if current_time > last_execution_time + 3:
            passed = f'{(current_time - start_time):010}'
            print(f'Time to execute the next calibration part at {current_time} - passed: {passed} - {focus_point[current_focus_point]}')
            next_item_times.append({
                'current_focus_point':current_focus_point,
                'frame_id': frame_id,
                'time':current_time,
                'speech':focus_point[current_focus_point]})
            nao.tts.request(NaoqiTextToSpeechRequest(focus_point[current_focus_point]))
            current_focus_point += 1
            last_execution_time = time.time()
            print(f'[CALIBRATION] Gave new instructions')
        if current_focus_point == len(focus_point):
            print('[CALIBRATION] Finished all instructions')
            break
        current_time = time.time()
        i+=1

    # Save the datapoints to a file
    #save_dataframe_to_csv(dictionary_list, video_recorder.get_video_name() + 'data_frames')
    save_dataframe_to_csv(next_item_times, video_recorder.get_video_name() + 'data_focus_times')
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["LShoulderRoll"], recorded_times=[[0]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["RShoulderRoll"], recorded_times=[[0]])))
    video_recorder.stop_video_recording()
    is_recording_pepper = False
    print("[CALIBRATION] Finished calibration recording")
    
def on_image(image_message: CompressedImageMessage):
    # we could use cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image)

def record_pepper(video_recorder: Recorder):
    pepper_with_frames = []
    pepper_frameless = []
    i = 0
    print("[PEPPER] Info on Pepper recording:")
    i_await=0
    while not video_recorder.get_currently_recording():
        sys.stdout.write(f'\r[PEPPER] Awaiting 4K start ({i_await} seconds passed)')
        sys.stdout.flush()
        time.sleep(1)
        i_await+=1
    print("[PEPPER] Starting to calibrate video")
    imgs = queue.Queue()
    global is_recording_pepper
    while is_recording_pepper:
        img = imgs.get()
   
        # Get the current time.
        pepper_with_frames, pepper_frameless , i = video_recorder.append_info_to_list(pepper_with_frames, pepper_frameless, i, img[..., ::-1])
        if (cv.waitKey(1) == ord('q')) or not video_recorder.get_currently_recording(): # Press 'q' on the Python Window to stop the script
            print("Breaking from Pepper output")
            break
    print("[PEPPER] Ended video recording loop Pepper")
    cv.destroyAllWindows()    
    print("[PEPPER] Starting saving images from Pepper")
    print(f'[PEPPER] Amount of frames in Pepper Dictionary: {len(pepper_frameless)}')
    save_dataframe_to_csv(pepper_frameless, video_recorder.get_video_name() + '_pepper')
    video_recorder.save_images(pepper_with_frames, False)
    print("[PEPPER] Finished saving images from Pepper")
    #video_recorder.finished_up_recording = True

######################## PARAMETER SETUP ########################
folder_name = './calibration_images_output/'
ip = [
    '10.0.0.148', # 148 = Alan
    '10.0.0.197', # 197 = Herbert
    '10.0.0.165', # 197 = Marvin
    '10.15.3.144' # 144 = Marvin
    ][0]

imgs = queue.Queue()

# Pepper preparation
conf = NaoqiCameraConf(vflip=0, auto_focus=True) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more
nao = Pepper(ip=ip, top_camera_conf=conf, motion_record_conf = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60))
nao.top_camera.register_callback(on_image)
nao.autonomous.request(NaoWakeUpRequest())
nao.autonomous.request(NaoBasicAwarenessRequest(False))
nao.autonomous.request(NaoBackgroundMovingRequest(False))
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.4], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]])))
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 3], recorded_joints=["LShoulderRoll"], recorded_times=[[0, 1]])))
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -3], recorded_joints=["RShoulderRoll"], recorded_times=[[0, 1]])))

# Added moving the arms back down as to prevent overheating of the arms
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["LShoulderRoll"], recorded_times=[[0, 1]])))
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["RShoulderRoll"], recorded_times=[[0, 1]])))

# Prepare the recorder
video_recorder = Recorder()
video_recorder.set_capture_device(1)
video_recorder.set_is_calibration(True)
#video_recorder.set_currently_recording(True)
threader = Threader()

# Execute the actual calibration
show_current_stage('STARTING CALIBRATION')
is_recording_pepper = True
threader.triple_parallel(video_recorder.start_video_recording, record_pepper, run_test, second_args=video_recorder, third_args=video_recorder)
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["LShoulderRoll"], recorded_times=[[0, 1]])))
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, 0], recorded_joints=["RShoulderRoll"], recorded_times=[[0, 1]])))

#video_recorder.stop_video_recording()
print("[CALIBRATION] Finished executing the calibration")

nao.tts.request(NaoqiTextToSpeechRequest('Saved images. Calibration test is over.'))
print("fin")