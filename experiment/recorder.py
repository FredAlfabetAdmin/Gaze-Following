# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import os
import cv2 as cv
import datetime
import time
from auxillary import get_participant_folder

fps = 30

class Recorder():
    currently_recording = False
    participant_id = -1
    trial_set = -1
    capture_device = -1
    finished_up_recording = True
    cap: cv.VideoCapture = None
    out: cv.VideoWriter = None
    
    def get_is_currently_recording(self):
        #print(self.currently_recording)
        return self.currently_recording

    def set_participant_id(self,_participant_id):
        self.participant_id = _participant_id

    def set_trial_set(self,_trial_set):
        self.trial_set = _trial_set
    
    def set_capture_device(self, capture_device):
        self.capture_device = capture_device
   
    def start_video_recording(self):
        # Some setup
        self.cap = cv.VideoCapture(self.capture_device)
        self.out = cv.VideoWriter(self.get_video_name(), cv.VideoWriter_fourcc(*'XVID'), fps, (640, 480))

        # This records the video
        self.currently_recording = True
        self.finished_up_recording = False
        while self.cap.isOpened() and self.currently_recording:
            ret, frame = self.cap.read()
            if not ret:
                print("[VIDEO] Can't receive frame (stream end?). Exiting ...") # From the OpenCV tutorial
                break

            #frame = cv.flip(frame, 0) # Flips the video output upside down
            
            # Write the video frames to the VideoCapture
            self.out.write(frame)
            #cv.imshow('frame', frame) # Consider checking if this can be removed to reduce memory/CPU-usage
            if cv.waitKey(1) == ord('q'): # Press 'q' on the Python Window to stop the script
                break
        self.finished_up_recording = True

    def stop_video_recording(self):
        #global cap, out, currently_recording, finished_up_recording
        self.currently_recording = False
        print("[VIDEO] Stopping Recording")
        while not self.finished_up_recording:
            print("[VIDEO] Still stopping")
            time.sleep(0.1)
        # Release everything if job is finished
        self.cap.release()
        self.out.release()
        cv.destroyAllWindows()

    # This function generates a folder for the output of the video with a name for a video, based on the current (date-)time.
    def get_video_name(self):
        # Parameters
        video_output_folder = get_participant_folder(self.participant_id) + '/video_output/'
        now = str(datetime.datetime.now())
        video_plus_date = str(video_output_folder + now.replace(':','_') + "/")
        file_output = video_plus_date + f'{self.participant_id}_{self.trial_set}_output.avi'
        
        # Create the folders
        os.makedirs(video_output_folder, exist_ok=True)
        os.makedirs(video_plus_date)
        
        return file_output