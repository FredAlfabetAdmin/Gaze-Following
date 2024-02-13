# Can probably remove ./motions due to force setting of the joints

#------------------------------- Preparations: -------------------------------#
# Imports
import time
from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.pepper import Pepper

# Setup
pepper = None
chain = ["LShoulderRoll", "RShoulderRoll"]

#------------------------------- Functions: -------------------------------#
def move_joints(angle = 0, chain = chain):
    #global pepper
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0, angle, 0], recorded_joints=[chain], recorded_times=[[0, 1, 2.5]])))

def move_shoulder_pitch():
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0.5, 1, 1.6], recorded_joints=["RShoulderPitch"], recorded_times=[[2, 4, 6]])))
    pepper.motion_record.request(PlayRecording(NaoqiMotionRecording(recorded_angles=[0.5, 1, 1.6], recorded_joints=["LShoulderPitch"], recorded_times=[[2, 4, 6]])))

def move_peppers_left(angle = 1):
    print("[MOVING] Left arm")
    move_joints(angle, chain[0]) # always positive

def move_peppers_right(angle = -1):
    print("[MOVING] Right arm")
    move_joints(angle, chain[1]) # always negative

def move_peppers_static():
    print("[MOVING] Resetting both arms")
    move_peppers_left(angle = 1)
    move_peppers_right(angle = -1)

def move_peppers_head():
    print("[MOVING] Calibrating Head")
    move_joints(.25, 'HeadPitch')

def set_pepper_motion(_pepper):
    global pepper
    pepper = _pepper

    # Disable "alive" activity for the whole body and set stiffness of the arm to zero
    pepper.motion.request(NaoqiIdlePostureRequest("Body", False))
    pepper.stiffness.request(Stiffness(0.7, chain))
    pepper.stiffness.request(Stiffness(0.7, ["RShoulderPitch","LShoulderPitch"]))
    move_peppers_head()
    #move_peppers_left()
    #move_peppers_right()
    #move_shoulder_pitch()