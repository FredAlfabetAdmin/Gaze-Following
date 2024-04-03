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
    print("[SPEECH] Talking Left")
    talk("Please tap the " + "left" + "arrow")

def talk_right():
    print("[SPEECH] Talking Right")
    talk("Please tap the " + "right" + "arrow")

def talk_ready():
    talk("When ready, please click Y and then ENTER")
    print("[SPEECH] Request Ready")

def talk_existing_participant():
    talk("Participant already has a folder. Check with experimenter.")
    print("[SPEECH] Request Ready")

def finished_round():
    talk("Round finished.")
    print("[SPEECH] Round finished")

def talk_change_eyetracker():
    talk("Five rounds have finished. Please contact the researcher for changing the eye-tracker. Press Y and then ENTER to continue.")
    print("[SPEECH] Finished 5 rounds")

def talk_wrong_key():
    talk("That key was the wrong key.")
    print("[SPEECH] Wrong key pressed")

def talk_response_slow():
    talk("You took too long to respond.")
    print("[SPEECH] Response time too slow")

def talk_response_correct():
    talk("You clicked the correct key!.")
    print("[SPEECH] Response correct")

def talk_is_training():
    talk("The following trials are training. Feedback will be given on pressing the wrong buttons, taking too long or pressing the correct key. This will ONLY happen for the training.")
    print("[SPEECH] Trials are training.")

def talk_eyetracker_status(has_eyetracker):
    appender = 'ON'
    if not has_eyetracker:
        appender = 'OFF'
    talk(f"The following trials have the eyetracker:")
    time.sleep(0.3)
    talk(f"{appender}")

def talk(value):
    pepper.tts.request(NaoqiTextToSpeechRequest(value))

def talk_intro(value):
    print(f"[SPEECH] Focus {value}")
    talk(f"Get Ready! Now focus on {value}")

def talk_preparations():
    print(f"[SPEECH] Confirmation Module")
    talk("Confirmation of speech module.")