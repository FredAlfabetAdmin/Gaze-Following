#------------------------------- Preparations: -------------------------------#
# Imports
import time
from sic_framework.devices import Pepper
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest

# Variables
pepper = None

#------------------------------- Functions: -------------------------------#
def set_pepper_speech(_pepper):
    global pepper
    pepper = _pepper

def talk_left():
    print("Talking left")
    talk("Please tap the "+"left" + "arrow")

def talk_right():
    print("Talking right")
    talk("Please tap the "+"right" + "arrow")

def talk(value):
    pepper.tts.request(NaoqiTextToSpeechRequest(value))

def talk_intro(value):
    talk(f"Let's focus on {value}")

def talk_preparations():
    talk("Confirmation of speech module.")