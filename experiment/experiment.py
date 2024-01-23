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
open terminal: cd experiment ; python experiment.py
"""

#------------------------------- Preparations: -------------------------------#
# Imports
import datetime
from sic_framework.devices import Pepper
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import NaoqiMotionRecorderConf

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech, talk_intro, talk_preparations 
from auxillary import show_current_stage, left_or_right
from randomizer import create_random_trials
from threader import start_listening

# Variables
port = 8080
#machine_ip = '10.0.0.240'
#robot_ip = '10.0.0.164' # Marvin # Has SSL error.
robot_ip = '10.0.0.180' # Ada

# Pepper device setup
conf = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60)
pepper = Pepper(robot_ip, motion_record_conf = conf)

#------------------------------- CODE: -------------------------------#
# Preparations
show_current_stage("Starting preparations")

trials = create_random_trials()
print(trials)

# Prepare Talk/Speech
set_pepper_speech(pepper)
talk_preparations()

# Prepare Tablet/Screen
set_pepper_tablet(pepper)
show_tablet_vu_logo()
show_tablet_empty()

# Prepare Motion/Gestures
set_pepper_motion(pepper)
move_peppers_left()
move_peppers_right()
move_peppers_static()

show_current_stage("Executing trials")
current_trial = 0
for trial in trials:
    print(f"Executing trial: {current_trial}")
    print("== FIRST PART ==")
    
    talk_intro(trial["primary"])

    # To determine the Ground Object (GO)
    if trial['first_item'] == 'visual':
        print("Showing tablet")
        show_tablet_left() if left_or_right(trial['congruent'], trial['direction']) else show_tablet_right()
    elif trial['first_item'] == 'gesture':
        print("Moving gesture")
        move_peppers_left() if left_or_right(trial['congruent'], trial['direction']) else move_peppers_right()
    else:
        print("Talking")
        talk_left() if left_or_right(trial['congruent'], trial['direction']) else talk_right()

    # Track the response time.
    #start_time = datetime.datetime.now()
    #print("Started at ", start_time)
    print("== SECOND PART ==")
    # And the Figure Object (FO)
    if trial['second_item'] == 'visual':
        print()
        show_tablet_right() if trial['direction'] == 'right' else show_tablet_left() 
    elif trial['second_item'] == 'gesture':
        move_peppers_left() if trial['direction'] == 'right' else move_peppers_right()
    else:
        talk_left() if trial['direction'] == 'right' else talk_right()

    # Complete the response time tracking
    #start_listening()
    #intermediate_time = datetime.datetime.now() - start_time

    # Might also make an implementation similar to start_listening(talk_right()), 
    # but have to check if that already executes the code of talk_right() during
    # the call or if it is only executed later. Could always pass as string with a decoder.

    #final_time = datetime.datetime.now() - start_time


    # Reset the Pepper
    show_tablet_empty()
    #move_peppers_static()
    current_trial += 1
    print()

# Finalizing
show_current_stage("Finishing up")
#move_peppers_static()
show_tablet_vu_logo()

print("fin")



############################### TO DO: ##########################
# - Make the second item and the timer work at the same time. 
# - Clean the actuators from the output.
# - Append the LShoulderPitch and RShoulderPitch to the actuators BEFORE the experiment starts (perhaps this causes the robot to move both arms at the same time?)
# - Measure the duration that it takes for the speech, tablet and gesture to be started and executed.
# - Complete the differentiation between the 
# - 