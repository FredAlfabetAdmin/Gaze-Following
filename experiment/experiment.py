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
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf

from motions import move_pepper_left, move_pepper_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations, talk_ready, finished_round, talk_response_slow, talk_wrong_key, talk_change_eyetracker, talk_is_training, talk_eyetracker_status, talk_response_correct
from auxillary import show_current_stage, left_or_right, confirm_ready, dump_trialset_to_json, create_data_folders, save_dataframe_to_csv, append_info_to_list, get_brio_id, csv_with_rounds_exists
from randomizer import create_random_trials
from recorder import Recorder#, start_video_recording, stop_video_recording, set_participant_id, set_trial_set, get_is_currently_recording
from threader import Threader, write_single_frame, set_active #,start_listening, parallel
from settings import participant_id, ip, has_eyetracker, is_training

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
    video_recorder, trial_round = args

    # Confirm if the participant is ready to start a new trial
    Threader().parallel(confirm_ready, talk_ready)

    time.sleep(3)
    
    # If needed, grab a subset of the trials
    trials = create_random_trials()
    if video_recorder.get_is_training():
        trials = trials[0:5]
    current_trial = 0

    trials = trials[0:2]

    # Execute all the trials in the trials set
    show_current_stage(f"Executing trials - {video_recorder.get_is_eyetracker()}")
    print("[EXPERIMENT] NOW RECORDING!")
    trial_data = {}
    print(len(trials))
    for trial in trials:
        print(f"** Executing trial: {current_trial + 1} / {len(trials)}**")
        #talk_intro(trial["primary"])
        talk_intro(trial["first_item"])
        trial['start'] = time.time()

        if trial['first_item'] == 'tablet':
            #print("Showing tablet")
            #first_event = show_tablet_left if left_or_right(trial['congruent'], trial['direction']) == 'left' else show_tablet_right
            first_event = show_tablet_left if trial['direction'] == 'left' else show_tablet_right
        elif trial['first_item'] == 'gesture':
            #print("Moving gesture")
            #first_event = move_pepper_left if left_or_right(trial['congruent'], trial['direction']) == 'left' else move_pepper_right
            first_event = move_pepper_left if trial['direction'] == 'left' else move_pepper_right
        else:
            #print("Talking")
            #first_event = talk_left if left_or_right(trial['congruent'], trial['direction']) == 'left' else talk_right
            first_event = talk_left if trial['direction'] == 'left' else talk_right

        # And the Figure Object (FO)
        if trial['second_item'] == 'tablet':
            second_event = show_tablet_left if (trial['direction'] == 'left' and trial['congruent']) or (trial['direction'] =='right' and trial['congruent'] == False) else show_tablet_right
        elif trial['second_item'] == 'gesture':
            second_event = move_pepper_left if (trial['direction'] == 'left' and trial['congruent']) or (trial['direction'] =='right' and trial['congruent'] == False) else move_pepper_right
        else:
            print('talking 2nd')
            second_event = talk_left if (trial['direction'] == 'left' and trial['congruent']) or (trial['direction'] =='right' and trial['congruent'] == False) else talk_right
        print(f'trail["direction"]: {trial["direction"]} - trial["congruent"]: {trial["congruent"]}')
        print(f'first event: {first_event}')
        print(f'second event: {second_event} - trail["direction"]: {trial["direction"]}')

        # Execute the actual code.
        threader = Threader() # Possibly an entry into catching the return value of start_listening
        threader.parallel(execute_single_trial, threader.start_listening, first_args = [first_event, second_event, threader])

        # Do something with the resulting trial
        trial['round'] = trial_round
        trial['end'] = time.time()
        trial_keystroke = threader.get_resulting_output()
        trial['trial_id'] = current_trial
        trial['result'] = trial['direction'] == trial_keystroke['reason']
        print(f"KEYSTOKE WAS CORRECT: {trial['result']}")
        trial['keystroke'] = trial_keystroke
        trial_data[current_trial] = trial
        
        # Extra information for the participant during training:
        if video_recorder.get_is_training():
            # If response too slow:
            if trial_keystroke['reason'] == 'overtime':
                talk_response_slow()
            
            # If wrong key press:
            if not trial['result'] and trial_keystroke['valid']:
                talk_wrong_key()
            
            if trial['result']:
                talk_response_correct()

        # Reset the Pepper
        show_tablet_empty()
        current_trial += 1
        time.sleep(0.5) # Found by Lin and changed to 0.5 at 02-04-24 #time.sleep(3) # Remove later.
        #i+=1
    finished_round()
    print(trial_data)
    dump_trialset_to_json(trial_data, video_recorder.get_video_name())
    #video_recorder.stop_video_recording()

    # Save the datapoints to a file
    #save_dataframe_to_csv(df, video_recorder.get_video_name() + 'data_frames')
    #save_dataframe_to_csv(next_item_times, video_recorder.get_video_name() + 'data_focus_times')
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["LShoulderRoll"], recorded_times=[[0]])))
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0], recorded_joints=["RShoulderRoll"], recorded_times=[[0]])))
    video_recorder.stop_video_recording()
    print("[EXPERIMENT] Finished experiment recording")

def execute_single_trial(args):# first_event, second_event, current_trial):
     first_event, second_event, threader = args
     threader.parallel(first_event, second_event)
    
imgs = queue.Queue()

def on_image(image_message: CompressedImageMessage):
    imgs.put(image_message.image)

def record_pepper(video_recorder: Recorder):
    global i
    pepper_frameless = []
    print("[PEPPER] Info on Pepper recording:")
    i_await = 0
    while not video_recorder.get_currently_recording():
        sys.stdout.write(f'\r[PEPPER] Awaiting 4K start ({i_await} seconds passed)')
        sys.stdout.flush()
        time.sleep(1)
        i_await += 1
    print("[PEPPER] Starting to calibrate video")
    
    set_active(True)
    img = imgs.get()
    print(f'PEPPER Camera Resolution: {img.shape}')
    if img.shape[0] < 480 or img.shape[1] < 640:
        
        raise Exception("PEPPER CAMERA DOES NOT RUN AT REQUIRED RESOLUTION!")
    while video_recorder.get_currently_recording():
        #pass
        img = imgs.get()
        pepper_frameless, _ = append_info_to_list(pepper_frameless, '{:07}'.format(int(i)))
        i += 1
        write_single_frame('{:07}'.format(i), img[..., ::-1], video_recorder.get_video_name(), _4K = False)
    print("[PEPPER] Ended video recording loop Pepper")
    cv.destroyAllWindows()    
    set_active(False)
    print(f'[PEPPER] Starting to write the Pepper dataframe to IO ({len(pepper_frameless)} items)')
    save_dataframe_to_csv(video_recorder.get_video_name(), pepper_frameless, 'pepper', video_recorder.get_is_eyetracker(), video_recorder.get_calibration_formal_mode())
    #save_dataframe_to_csv(pepper_frameless, video_recorder.get_video_name() + 'pepper')
    print("[PEPPER] Finished saving images from Pepper")


#------------------------------- CODE: -------------------------------#
     
# Variables
port = 8080
folder_name = './experiment_images_output/'

# Pepper device setup
#conf_rec = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60)
#conf_cam = NaoqiCameraConf(vflip=1) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more
pepper = Pepper(ip,top_camera_conf = NaoqiCameraConf(vflip=0, res_id=2))#, motion_record_conf = conf_rec, top_camera_conf=conf_cam)
pepper.top_camera.register_callback(on_image)
pepper.autonomous.request(NaoWakeUpRequest())
pepper.autonomous.request(NaoBasicAwarenessRequest(False))
pepper.autonomous.request(NaoBackgroundMovingRequest(False))

imgs = queue.Queue()

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


is_eyetracker = has_eyetracker
training = is_training
video_recorder = Recorder()
video_recorder.set_capture_device(get_brio_id())
video_recorder.set_participant_id(participant_id)
video_recorder.set_is_eyetracker(is_eyetracker)
video_recorder.set_calibration_formal_mode('formal')
video_recorder.set_is_training(is_training)
i = 0
if training:
    another_one = True
    while another_one:
        talk_is_training()
        video_recorder.set_trial_set(0)
        threader = Threader()
        threader.triple_parallel(video_recorder.start_video_recording, record_pepper, execute_set_of_trials, second_args=video_recorder, third_args=[video_recorder, 0])
        video_recorder.stop_video_recording()
        if input("Another one? [Y/n]").upper() != 'Y':
            another_one = False

else:
    experiment_length = 5
    start = 0
    talk_eyetracker_status(video_recorder.get_is_eyetracker())
    for trial_round in range(start, start + experiment_length):
        # Check if the current status of the csv already contains this setting.
        csv_with_rounds_exists(video_recorder.participant_id, trial_round, video_recorder.get_is_eyetracker(), video_recorder.get_calibration_formal_mode())
        video_recorder.set_trial_set(trial_round)

        threader = Threader()
        threader.triple_parallel(video_recorder.start_video_recording, record_pepper, execute_set_of_trials, second_args=video_recorder, third_args=[video_recorder, trial_round])
        video_recorder.stop_video_recording()
        print(f"TRIAL SET {trial_round} was completed!")
        #video_recorder.clear_round_info_csv() # Clear the round_info.csv from dir
        if trial_round ==  start + experiment_length - 1: # Last round. Change Eye-Tracker
            talk_change_eyetracker()
            print("END OF THIS SET OF (NON-) EYE-TRACKER")
            while input('PRESS Y AND ENTER TO CONTINUE! [y]').lower() != "y":
                pass
        elif trial_round < experiment_length - 1:
            confirm_ready()
            print("continuing")

show_current_stage("[EXPERIMENT] END OF EXPERIMENT!")

print("fin")