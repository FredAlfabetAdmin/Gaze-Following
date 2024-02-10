# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import os
import cv2 as cv
import datetime
import time

# This function records a video based on the device used (local webcam = 0; logitech/webcam = 1)
def start_video_recording(capture_device: int = 0, particpant_id: int = -1, trial_id: int = -1):
    # Some setup
    global cap, currently_recording, finished_up_recording
    cap = cv.VideoCapture(capture_device)
    out = cv.VideoWriter(get_video_name(particpant_id, trial_id), cv.VideoWriter_fourcc(*'XVID'), fps, (640, 480))

    # This records the video
    currently_recording = True
    finished_up_recording = False
    while cap.isOpened() and currently_recording:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        #frame = cv.flip(frame, 0) # Flips the video output upside down
        
        # Write to video frames to the VideoCapture
        out.write(frame)
        #cv.imshow('frame', frame) # Consider checking if this can be removed to reduce memory/CPU-usage
        if cv.waitKey(1) == ord('q'): # Press 'q' on the Python Window to stop the script
            break
    finished_up_recording = True

def stop_video_recording():
    global cap, out, currently_recording, finished_up_recording
    currently_recording = False
    while not finished_up_recording:
        print("not done yet")
        time.sleep(0.1)
    # Release everything if job is finished
    cap.release()
    out.release()
    cv.destroyAllWindows()

# This function generates a folder for the output of the video with a name for a video, based on the current (date-)time.
def get_video_name(participant_id: int = -1, trial_id: int =- 1):
    # Parameters
    video_output_folder = './video_output/'
    now = str(datetime.datetime.now())
    video_plus_date = str(video_output_folder + now.replace(':','_') + "/")
    file_output = video_plus_date + f'{participant_id}_{trial_id}_output.avi'
    
    # Create the folders
    os.makedirs(video_output_folder, exist_ok=True)
    os.makedirs(video_plus_date)
    
    return file_output

# GLOBALS
fps = 30
cap = cv.VideoCapture(0)
out = cv.VideoWriter(get_video_name(-1, -1), cv.VideoWriter_fourcc(*'XVID'), fps, (640, 480))
currently_recording = False
finished_up_recording = False

def get_is_currently_recording():
    global currently_recording
    return currently_recording

#record_video()
#print("fin")