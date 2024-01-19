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
import random
import time
from sic_framework.devices import Pepper
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import NaoqiMotionRecorderConf

from motions import move_peppers_left, move_peppers_right, set_pepper_motion, move_peppers_static
from tablet import show_tablet_empty, show_tablet_right, show_tablet_vu_logo, show_tablet_left, set_pepper_tablet
from speech import talk_left, talk_right, set_pepper_speech
from auxillary import show_current_stage

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
set_pepper_tablet(pepper)
set_pepper_motion(pepper)
set_pepper_speech(pepper)
show_tablet_vu_logo()
move_peppers_static()

# Actual 'experiment'
show_current_stage("Starting experiment")
for x in range(8):
    # Based on (*X*, move, talk and show by condition
    print(f"X: {x}")
    if random.randint(0,1) == 0:
        show_tablet_left()
        move_peppers_right()
        talk_right()
    else:
        show_tablet_right()
        move_peppers_left()
        talk_left()
    
    # Reset the Pepper
    show_tablet_empty()
    #move_peppers_static()

# Finalizing
show_current_stage("Finishing up")
#move_peppers_static()
show_tablet_vu_logo()

#'''
print("fin")