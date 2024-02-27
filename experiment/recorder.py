# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import os
import cv2 as cv
import datetime
import time
import pandas as pd
from auxillary import get_participant_folder

fps = 30

class Recorder():
    # PARAMETERS
    currently_recording = False
    participant_id = -1
    trial_set = -1
    capture_device = -1
    finished_up_recording = True
    current_focus_point = None
    cap: cv.VideoCapture = None
    is_calibration = False

    # GETTERS     
    def get_is_currently_recording(self):
        return self.currently_recording
    def get_is_calibration(self):
        return self.is_calibration

    # SETTERS
    def set_participant_id(self,_participant_id):
        self.participant_id = _participant_id
    def set_trial_set(self,_trial_set):
        self.trial_set = _trial_set
    def set_is_calibration(self, _is_calibration):
        self.is_calibration = _is_calibration
    def set_capture_device(self, capture_device):
        self.capture_device = capture_device
   
    # FUNCTIONS TO RECORD
    def start_video_recording(self):
        # Some Parameter setup
        self.cap = cv.VideoCapture(self.capture_device)
        self.currently_recording = True
        self.finished_up_recording = False
        dictionary_list = []
        i=0
        a = {}

        # Only start when it is actually recording
        while self.cap.isOpened() and self.currently_recording:
            # Get the frame
            ret, frame = self.cap.read()
            if not ret:
                print("[VIDEO] Can't receive frame (stream end?). Exiting ...") # From the OpenCV tutorial
                break

            # Get the current time.
            frame_id = f'{i:010}'
            dictionary_data = {
                'ID':frame_id,
                'time':time.time()
                #'image':img[..., ::-1], # Consider adding the image to the dictionary already. Check with I/O speeds.
            }

            dictionary_list.append(dictionary_data)
            i += 1
            if cv.waitKey(1) == ord('q'): # Press 'q' on the Python Window to stop the script
                break
        cv.destroyAllWindows()

        # Save all images to the disk.
        for img in a:
            print(img)
            print(a[img])
            print(a[img]['ID'])
            cv.imwrite(f"./{a[img]['ID']:05}.jpg", a[img]['image'])
        print("finished saving all images to disk")

        self.finished_up_recording = True

    # Stop recording the video
    def stop_video_recording(self):
        #global cap, out, currently_recording, finished_up_recording
        self.currently_recording = False
        print("[VIDEO] Stopping Recording")
        while not self.finished_up_recording:
            print("[VIDEO] Still stopping")
            time.sleep(0.1)
        
        # Release everything if job is finished
        self.cap.release()
        #self.out.release()
        cv.destroyAllWindows()

    # This function generates a folder for the output of the video with a name for a video, based on the current (date-)time.
    def get_video_name(self):
        # Parameters
        video_output_folder = get_participant_folder(self.participant_id) + '/'
        video_output_folder += 'calibration_' if self.get_is_calibration else 'experiment_'

        now = str(datetime.datetime.now())
        video_plus_date = str(video_output_folder + now.replace(':', '_') + "/")
        file_output = video_plus_date + f'{self.participant_id}_{self.trial_set}_output.avi'
        
        # Create the folders
        os.makedirs(video_output_folder, exist_ok=True)
        os.makedirs(video_plus_date)
        
        return file_output