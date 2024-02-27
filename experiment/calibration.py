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
# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import cv2 as cv
import time
import datetime
import pandas as pd

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations, talk_ready
from auxillary import show_current_stage, left_or_right, confirm_ready, dump_trialset_to_json, create_data_folders
from randomizer import create_random_trials
from recorder import Recorder#, start_video_recording, stop_video_recording, set_participant_id, set_trial_set, get_is_currently_recording
from threader import Threader

fps = 30

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

'''
class Threader():

    resulting_output = {}
    def set_resulting_output(self, value):
        self.resulting_output = value
    def get_resulting_output(self):
        return self.resulting_output
    
    def start_listening(self, args):
        video_recorder = args[0]
        # Create a shared flag between the threads
        thread_stop = threading.Event()

        while not video_recorder.get_is_currently_recording():
            print("[THREADING] Awaiting Start of Recording")
            time.sleep(1)
        
        # Create threads for script logic and timer, passing the shared flag
        script_thread = threading.Thread(target=self.await_keypress, args=(thread_stop,))
        timer_thread = threading.Thread(target=self.timer, args=(thread_stop,))

        script_thread.start()
        timer_thread.start()
        script_thread.join()
        timer_thread.join()
        
        #return output
    
    def parallel(self, first_event, second_event, first_args = None, second_args = None):
        # Create threads for script logic and timer, passing the shared flag
        if first_args == None:
            script_thread = threading.Thread(target=first_event)
        else:
            script_thread = threading.Thread(target=first_event, args=(first_args,))
        if second_args == None:
            timer_thread = threading.Thread(target=second_event)
        else:
            timer_thread = threading.Thread(target=second_event, args=(second_args,))

        script_thread.start()
        timer_thread.start()
        script_thread.join()
        timer_thread.join()
    
    def await_keypress(self, thread_stop):
        start_time = time.time()
        print('Start time: {start_time}')
        output = {'valid':False, 'reason': 'initialization', 'duration':-1}
        #print("[THREADING] Watching Keystrokes")
        while not thread_stop.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch() # Required to be called, but does not actually do anything?
                arrow_key = msvcrt.getch().decode('utf-8')
                thread_stop.set()

                # Consider if the arrow keys here have to be used or not.
                if arrow_key == 'M':
                    output = {'valid': True, 'reason': 'right', 'duration': time.time() - start_time}
                elif arrow_key == 'K':
                    output = {'valid': True, 'reason': 'left', 'duration': time.time() - start_time}
                else:
                    output = {'valid': False, 'reason': 'wrongkey', 'duration': time.time() - start_time}
                break

            # Check if the time limit is reached
            elapsed_time = time.time() - start_time
            max_duration = 4
            if elapsed_time >= max_duration:
                print(f"[THREADING] Time limit of {max_duration} seconds exceeded")
                output = {'valid':False, 'reason': 'overtime', 'duration':time.time() - start_time}
                thread_stop.set()
                break
        print(f"[THREADING] Keystroke: {output['reason']} - Took: {output['duration']}")
        self.set_resulting_output(output)

    def timer(self, thread_stop):
        i = 0
        start_time = time.time()
        while not thread_stop.is_set():
            print(f"Time passed: {str(time.time() - start_time)[:5]}")
            time.sleep(0.05)
            i+=1
        print(f"[THREADING] I's: {i}")
'''

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

def run_test():
    # Parameters
    df = pd.DataFrame(columns=['time', 'frame_id'])
    dictionary_list = []
    next_item_times = []
    i=0

    # Start recording the video
    while not video_recorder.get_is_currently_recording():
        print("[EXPERIMENT-RECORDER] WARNING: Currently not recording.")
        time.sleep(1)

    time.sleep(2)
    nao.tts.request(NaoqiTextToSpeechRequest('please get in front of the Pepper'))
    #nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[1], recorded_joints=["LShoulderRoll"], recorded_times=[[1]])))
    #nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[-1], recorded_joints=["RShoulderRoll"], recorded_times=[[1]])))
    nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.3], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]])))
    
    # Time tracking
    start_time = time.time()
    current_time = time.time()
    print(f'Start time: {start_time}')

    # Actually execute the motions
    while time.time() < start_time + (len(focus_point) * time_inbetween):
        # For every 3 seconds, go to the next output.
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
    print("finished saving all images to disk")
    video_recorder.stop_video_recording()

folder_name = './calibration_images_output/'

imgs = queue.Queue()


def on_image(image_message: CompressedImageMessage):
    # we could use cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image)

# Create camera configuration using vflip to flip the image vertically
conf = NaoqiCameraConf(vflip=0, auto_focus=True) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more

#nao = Pepper(ip="10.0.0.237", top_camera_conf=conf)
nao = Nao(ip="10.0.0.237", top_camera_conf=conf)
nao.top_camera.register_callback(on_image)
nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, -.4], recorded_joints=['HeadPitch'], recorded_times=[[0, 1]])))
#nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[3], recorded_joints=["LShoulderRoll"], recorded_times=[[1]])))
#nao.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[-3], recorded_joints=["RShoulderRoll"], recorded_times=[[1]])))


'''
while True:
    img = imgs.get()
    cv2.imshow('', img[..., ::-1])  # cv2 is BGR instead of RGB
    cv2.waitKey(1)
'''

video_recorder = Recorder()
video_recorder.set_capture_device(0)
video_recorder.set_is_calibration(True)
threader = Threader()
threader.parallel(video_recorder.start_video_recording, run_test)

video_recorder.stop_video_recording()
print("done with parallel")

nao.tts.request(NaoqiTextToSpeechRequest('Saved images. Calibration test is over.'))
