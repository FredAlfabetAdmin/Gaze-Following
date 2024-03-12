# To remove:
# open terminal: cd sic_framework\tests\demo_webserver\ ; python demo_pepper_guess_number.py

"""
To execute:
# Might be better to disable the Pepper's autonomous life before executing the code.

# confirm Docker Framework is running
# confirm TP-Link Wi-Fi
open terminal: cd sic_framework\services\dialogflow ; python dialogflow.py
open terminal: cd sic_framework\services\webserver ; python webserver_pepper_tablet.py

# confirm that the participant_id and capture_device are correct!
open terminal: cd experiment ; python experiment.py
"""

#------------------------------- Preparations: -------------------------------#
# Imports
import cv2 as cv
import time
import sys
import queue
from sic_framework.devices import Pepper
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import NaoqiMotionRecorderConf

from sic_framework.core.message_python2 import CompressedImageMessage
#from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf
#from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording, NaoqiMotionRecorderConf
from sic_framework.devices.common_naoqi.naoqi_autonomous import NaoBasicAwarenessRequest, NaoBackgroundMovingRequest, NaoWakeUpRequest#, NaoRestRequest
#from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.pepper import Pepper
#from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations, talk_ready
from auxillary import show_current_stage, left_or_right, confirm_ready, dump_trialset_to_json, create_data_folders, save_dataframe_to_csv, append_info_to_list, get_brio_id
from randomizer import create_random_trials
from recorder import Recorder#, start_video_recording, stop_video_recording, set_participant_id, set_trial_set, get_is_currently_recording
from threader import Threader, write_single_frame, set_active #,start_listening, parallel

#------------------------------- Functions: -------------------------------#
# test_left and test_right are there for when the robot is not there but you still want to test some of the code.
def test_left():
    print('left')
    time.sleep(1)
def test_right():
    print('right')
    time.sleep(2)

# This function executes the set of trials
def execute_set_of_trials(args):
    video_recorder, trial_set = args

    # Confirm if the participant is ready to start a new trial
    Threader().parallel(confirm_ready, talk_ready)

    time.sleep(3)
    
    # If needed, grab a subset of the trials
    trials = create_random_trials()[0:5] # Remove this later to use all trials and not just a singular one.
    current_trial = 0

    # Execute all the trials in the trials set
    show_current_stage("Executing trials")
    print("[EXPERIMENT] NOW RECORDING!")
    trial_data = {}
    for trial in trials:
        print(f"** Executing trial: {current_trial} **")
        talk_intro(trial["primary"])
        trial['start'] = time.time()

        # To determine the Ground Object (GO)
        if trial['first_item'] == 'visual':
            #print("Showing tablet")
            first_event = show_tablet_left if left_or_right(trial['congruent'], trial['direction']) else show_tablet_right
        elif trial['first_item'] == 'gesture':
            #print("Moving gesture")
            first_event = move_peppers_left if left_or_right(trial['congruent'], trial['direction']) else move_peppers_right
        else:
            #print("Talking")
            first_event = talk_left if left_or_right(trial['congruent'], trial['direction']) else talk_right

        # And the Figure Object (FO)
        if trial['second_item'] == 'visual':
            print()
            second_event = show_tablet_right if trial['direction'] == 'right' else show_tablet_left 
        elif trial['second_item'] == 'gesture':
            second_event = move_peppers_left if trial['direction'] == 'right' else move_peppers_right
        else:
            second_event = talk_left if trial['direction'] == 'right' else talk_right

        # Execute the actual code.
        threader = Threader() # Possibly an entry into catching the return value of start_listening
        threader.parallel(execute_single_trial, threader.start_listening, first_args = [first_event, second_event, threader])

        # Do something with the resulting trial
        trial['end'] = time.time()
        trial_keystroke = threader.get_resulting_output()
        trial['trial_id'] = current_trial
        trial['result'] = trial['direction'] == trial_keystroke['reason']
        trial['keystroke'] = trial_keystroke
        trial_data[current_trial] = trial
        # Consider writing the 'trial' to a specific file instead of one big dictionary (leaky)

        # Reset the Pepper
        show_tablet_empty()
        current_trial += 1
        time.sleep(3) # Remove later.
        #i+=1
    
    print(trial_data)
    dump_trialset_to_json(trial_data, trial_set, participant_id)
    #video_recorder.stop_video_recording()

    # Save the datapoints to a file
    #save_dataframe_to_csv(df, video_recorder.get_video_name() + 'data_frames')
    #save_dataframe_to_csv(next_item_times, video_recorder.get_video_name() + 'data_focus_times')
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["LShoulderRoll"], recorded_times=[[0]])))
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["RShoulderRoll"], recorded_times=[[0]])))
    video_recorder.stop_video_recording()
    print("[CALIBRATION] Finished calibration recording")

def execute_single_trial(args):# first_event, second_event, current_trial):
     first_event, second_event, threader = args
     threader.parallel(first_event, second_event)
    
def on_image(image_message: CompressedImageMessage):
    imgs.put(image_message.image)

def record_pepper(video_recorder: Recorder):
    pepper_frameless = []
    i = 0
    print("[PEPPER] Info on Pepper recording:")
    i_await = 0
    while not video_recorder.get_currently_recording():
        sys.stdout.write(f'\r[PEPPER] Awaiting 4K start ({i_await} seconds passed)')
        sys.stdout.flush()
        time.sleep(1)
        i_await += 1
    print("[PEPPER] Starting to calibrate video")
    
    set_active(True)
    while video_recorder.get_currently_recording():
        #pass
        img = imgs.get()
        pepper_frameless , i = append_info_to_list(pepper_frameless, i)
        write_single_frame(i, img[..., ::-1], video_recorder.get_video_name(), _4K = False)
    print("[PEPPER] Ended video recording loop Pepper")
    cv.destroyAllWindows()    
    set_active(False)
    print(f'[PEPPER] Starting to write the Pepper dataframe to IO ({len(pepper_frameless)} items)')
    save_dataframe_to_csv(pepper_frameless, video_recorder.get_video_name() + 'pepper')
    print("[PEPPER] Finished saving images from Pepper")

#------------------------------- CODE: -------------------------------#
     
# Variables
port = 8080
folder_name = './calibration_images_output/'
ip = [
    '10.0.0.148', # 148 = Alan
    '10.0.0.197', # 197 = Herbert
    '10.0.0.165', # 197 = Marvin
    '10.15.3.144' # 144 = Marvin
    ][2]
participant_id = 1

imgs = queue.Queue()
#capture_device = 0
participant_id = 1

# Pepper device setup
conf = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60)
pepper = Pepper(ip, motion_record_conf = conf)
pepper.top_camera.register_callback(on_image)
pepper.autonomous.request(NaoWakeUpRequest())
pepper.autonomous.request(NaoBasicAwarenessRequest(False))
pepper.autonomous.request(NaoBackgroundMovingRequest(False))
# Preparations
show_current_stage("Starting preparations")

# Prepare Tablet/Screen
set_pepper_tablet(pepper)
#show_tablet_vu_logo()
show_tablet_empty()

# Prepare Motion/Gestures
set_pepper_motion(pepper)
move_peppers_static()

# Prepare Talk/Speech
set_pepper_speech(pepper)
talk_preparations()

# Finalizing
show_tablet_vu_logo()
show_current_stage("Finishing up")

if participant_id == -1:
    print("Warning: participant ID is currently at default (-1)")

create_data_folders(participant_id)

experiment_length = 2
for trial_number in range(experiment_length):
    video_recorder = Recorder()
    video_recorder.set_capture_device(get_brio_id())
    video_recorder.set_participant_id(participant_id)
    video_recorder.set_trial_set(trial_number)
    threader = Threader()

    threader.triple_parallel(video_recorder.start_video_recording, record_pepper, execute_set_of_trials, second_args=video_recorder, third_args=[video_recorder,trial_number])
    #threader.parallel(video_recorder.start_video_recording, execute_set_of_trials, None, [video_recorder,trial_number])
    video_recorder.stop_video_recording()
    print(f"TRIAL SET {trial_number} was completed!")
    if trial_number < experiment_length - 1:
        confirm_ready()

show_current_stage("[EXPERIMENT] END OF EXPERIMENT!")
print("fin")
