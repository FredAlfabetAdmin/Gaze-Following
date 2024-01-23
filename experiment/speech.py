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
    talk("left")

def talk_right():
    print("Talking right")
    talk("right")

def talk(value):
    pepper.tts.request(NaoqiTextToSpeechRequest(value))

def talk_intro(value):
    talk(f"Please focus on {value}")

def talk_preparations():
    talk("I am warming up my joints, vocal cords and charging my display.")