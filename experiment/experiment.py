import random
import time

'''
from sic_framework.core.utils import is_sic_instance
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, \
    GetIntentRequest, RecognitionResult, QueryResult, Dialogflow
from sic_framework.services.webserver.webserver_pepper_tablet import Webserver, HtmlMessage, WebserverConf, TranscriptMessage, ButtonClicked
from sic_framework.devices.common_naoqi.pepper_tablet import NaoqiTablet, UrlMessage
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
'''
from sic_framework.devices.common_naoqi.pepper_tablet import UrlMessage
from sic_framework.devices import Pepper

"""
This demo shows you how to interact with Pepper tablet to play a “guess the number” game

The Dialogflow and Webserver pepper tablet should be running. You can start them with:
[services/dialogflow] python dialogflow.py
[services/webserver]  python webserver_pepper_tablet.py

to execute:
# Might be better to disable the Pepper's autonomous life before executing the code.

# confirm Docker Framework is running
# confirm TP-Link Wi-Fi
open terminal: cd sic_framework\services\dialogflow ; python dialogflow.py
open terminal: cd sic_framework\services\webserver ; python webserver_pepper_tablet.py
open terminal: cd sic_framework\tests\demo_webserver\ ; python demo_pepper_guess_number.py
"""

port = 8080
machine_ip = '10.0.0.240'
#robot_ip = '10.0.0.164' # Marvin # Has SSL error.
robot_ip = '10.0.0.180' # Ada

# the HTML file to be rendered
arrow_left =  'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/U%2B2190.svg/2560px-U%2B2190.svg.png'
arrow_right = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/U%2B2192.svg/2560px-U%2B2192.svg.png'
flag_empty = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/White_flag_of_surrender.svg/2560px-White_flag_of_surrender.svg.png'

# Pepper device setup
pepper = Pepper(ip=robot_ip)

def show_left():
    print("showing left")
    pepper.tablet_display_url.send_message(UrlMessage(arrow_left))
    time.sleep(4)
def show_right():
    print("showing right")
    pepper.tablet_display_url.send_message(UrlMessage(arrow_right))
    time.sleep(4)
def show_empty():
    print("showing none")
    pepper.tablet_display_url.send_message(UrlMessage(flag_empty))
    time.sleep(2)

print("sending-------------")
print("displaying html on Pepper display")
show_empty()
for x in range(8):
    print(f"X: {x}")
    if random.randint(0,1) == 0:
        show_left()
    else:
        show_right()
    show_empty()

print("fin")