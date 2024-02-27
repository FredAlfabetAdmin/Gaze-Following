# To remove:
# open terminal: cd sic_framework\tests\demo_webserver\ ; python demo_pepper_guess_number.py

"""
The Dialogflow and Webserver pepper tablet should be running. You can start them with:
[services/dialogflow] python dialogflow.py
[services/webserver]  python webserver_pepper_tablet.py

to execute:
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
import datetime, time

from sic_framework.devices import Pepper
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import NaoqiMotionRecorderConf

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations, talk_ready
from auxillary import show_current_stage, left_or_right, confirm_ready, dump_trialset_to_json, create_data_folders
from randomizer import create_random_trials
from recorder import Recorder#, start_video_recording, stop_video_recording, set_participant_id, set_trial_set, get_is_currently_recording
from threader import Threader #,start_listening, parallel

# Variables
port = 8080
#machine_ip = '10.0.0.240'
#robot_ip = '10.0.0.164' # Marvin # Has SSL error.
#robot_ip = '10.0.0.165' # Marvin # Has SSL error.
robot_ip = '10.15.3.144' # Marvin # Has SSL error.
#robot_ip = '10.0.0.180' # Ada
#robot_ip='10.15.3.226'
capture_device = 0
participant_id = 2

# Pepper device setup
conf = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60)
pepper = Pepper(robot_ip, motion_record_conf = conf)

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

    # Start recording the video
    while not video_recorder.get_is_currently_recording():
        print("[EXPERIMENT-RECORDER] WARNING: Currently not recording.")
        time.sleep(1)
    
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
        #print("== FIRST PART ==")
        
        talk_intro(trial["primary"])

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

        # Track the response time.
        #print("== SECOND PART ==")
        # And the Figure Object (FO)
        if trial['second_item'] == 'visual':
            print()
            second_event = show_tablet_right if trial['direction'] == 'right' else show_tablet_left 
        elif trial['second_item'] == 'gesture':
            second_event = move_peppers_left if trial['direction'] == 'right' else move_peppers_right
        else:
            second_event = talk_left if trial['direction'] == 'right' else talk_right

        # if you want to just test the rest of the code without a robot.
        #first_event = test_left
        #second_event = test_right

        # Execute the actual code.
        threader = Threader() # Possibly an entry into catching the return value of start_listening
        threader.parallel(execute_single_trial, threader.start_listening, [first_event, second_event, threader], [video_recorder])

        # Do something with the resulting trial
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
    dump_trialset_to_json(trial_data, trial_set, participant_id)
    video_recorder.stop_video_recording()

def execute_single_trial(args):# first_event, second_event, current_trial):
     first_event, second_event, threader = args
     #start_time = time.time()
     threader.parallel(first_event, second_event)
     #stop_time = time.time()
     #passed_time = stop_time - start_time
     #print(f"Trial {current_trial} took {str(passed_time)} seconds")

#------------------------------- CODE: -------------------------------#
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

if participant_id == 1:
    print("Warning: participant ID is currently at default (-1)")

create_data_folders(participant_id)

experiment_length = 2
for trial_number in range(experiment_length):
    video_recorder = Recorder()
    video_recorder.set_capture_device(capture_device)
    video_recorder.set_participant_id(participant_id)
    video_recorder.set_trial_set(trial_number)
    threader = Threader()

    threader.parallel(video_recorder.start_video_recording, execute_set_of_trials, None, [video_recorder,trial_number])
    video_recorder.stop_video_recording()
    print(f"TRIAL SET {trial_number} was completed!")
    if trial_number < experiment_length - 1:
        confirm_ready()

show_current_stage("[EXPERIMENT] END OF EXPERIMENT!")
print("fin")

############################### TO DO: ##########################
# = Make the second item and the timer work at the same time. 
#   - Initial test made with #threader (https://github.com/FredAlfabetAdmin/Gaze-Following/blob/dd2a264518d9b516316af6c65dc34b7d9d2f1b0c/experiment/threader.py)
#   - Synchronize the input timer count-start with the start-time of the measurement (consider having one that starts before the code is executed and one that starts the exact moment that the 'left' word is spoken - systematic shift/bias?)

# = Clean the actuators from the output.
#   - The current implementation loads the actuators during the 'preparation' and should not be displayed after that.

# = Append the LShoulderPitch and RShoulderPitch to the actuators BEFORE the experiment starts (perhaps this causes the robot to move both arms at the same time?)
#   - Remove the initial forward motion of both arms
#   - Add the sidewards motion of both arms to confirm the arms moving around
#   - Current implementation only makes use of the stiffness. This might be good enough for our experiment. Requires further inspection if current implementation is insufficient.

# = Measure the duration that it takes for the speech, tablet and gesture to be started and executed.
#   - Possibly not required anymore

# = Remove the time.sleep at the end of each trial. Normalize based on inputs
#   - Consider if using a 1 second time sleep between the choice and the actual input is more user friendly.

# = Decide on post-trial resetting of tablet and motion.
#   - Perhaps the tablet and the motions are already turning off?

# = Create a storage of the duration of each trial:
#   - Setup
#   - Response duration
#   - Improve the dictionary creation and writing. (consider 'json' module)

# = Save a video or photo from every trial, per trial set or for the whole experiment?
#   - Research the possiblity in terms of data-writing, etc. Per trial might clog up the system, but allows for earlier catch of errors.
#   - Check if using the webcam/4K causes the input to be lit up with the white circle.
#   - Confirm that the speed between trails is OK and do not require a full shot-down and start-up to record. (might lead to errors and non-recordings otherwise?)
#   - Current setup is aimed at recording a video every trial set.

# = Generate some practice-trials
#   - Can probably use a subset of the code written in 'randomizer.create_random_trials()'

# Five different Trial sets
# = Implement the five different trial-sets.
# = Confirm the textual instructions for the participant (part of five different trial-sets)

# = Determine what to do when a user clicks on a button that is not the LEFT or RIGHT arrow key.

# = Determine what to do when a trial is done
#   - Save or append it to a file?
#   - Confirmation or denial of correct input/output

# = Rename 'visual' as it might confuse the participant for the gesture?

# =  Convert the data output from two individual folders to one 'participant' folder.
#   - Can also implement a check to see if that participant already has an ID. Without it might lead to overwriting data.

# = Remove the 'motions' folder
