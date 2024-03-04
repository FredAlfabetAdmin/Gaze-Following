# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import os
import cv2 as cv
import datetime
import time
from tqdm import tqdm
from auxillary import get_participant_folder, save_dataframe_to_csv, append_info_to_list

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
    def get_currently_recording(self):
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
    def set_currently_recording(self, _currently_recording):
        self.currently_recording = _currently_recording
   

    # FUNCTIONS TO RECORD
    def start_video_recording(self):
        # Some Parameter setup
        self.cap = cv.VideoCapture(self.capture_device, cv.CAP_GSTREAMER) # Capture 4K
        
        set_width_success = self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
        set_height_success =self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)
        print(f"Initial setting went W: {set_width_success} - {cv.CAP_PROP_FRAME_WIDTH} & H: {set_height_success} - {cv.CAP_PROP_FRAME_HEIGHT}")
        if not set_width_success:
            set_width_success = self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        if not set_height_success:
            set_height_success = self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        print(f"If wrong, setting went W: {set_width_success} & H: {set_height_success}")

        self.currently_recording = True
        self.finished_up_recording = False
        with_frames = []
        frameless = []
        i = 0
        print(f"Backend mode: {self.cap.getBackendName()}")

        # Only start when it is actually recording
        while self.cap.isOpened() and self.currently_recording:
            # Get the frame
            ret, frame = self.cap.read()
            if not ret:
                print("[VIDEO] Can't receive frame (stream end?). Exiting ...") # From the OpenCV tutorial
                break
        
            # Get the current time.
            with_frames, frameless, i = append_info_to_list(with_frames, frameless, i, frame)
            if cv.waitKey(1) == ord('q'): # Press 'q' on the Python Window to stop the script
                break
        print("[VIDEO] Done with recording the 4K")
        self.finished_up_recording = True
        self.stop_video_recording()
        cv.destroyAllWindows()
        save_dataframe_to_csv(frameless, self.get_video_name() + '4K')
        self.save_images(with_frames, True)
        print("[VIDEO] Finished saving images from 4K")

    # Save all images to the disk.
    def save_images(self, dictionary_list, _4K = True):
        device = '4K' if _4K else 'Pepper'
        video_name = self.get_video_name() 
        video_name += '_' + device + '_'
        print("[I/O] Starting saving images from 4K")
        for index in tqdm(range(len(dictionary_list))):
            #print(f"Still saving video_recorder ({device}), Amount left : {len(dictionary_list) - index}")
            one_frame_dict = dictionary_list[index]
            image_id = one_frame_dict['ID']
            image_frame = one_frame_dict['frame']
            cv.imwrite(f"./{video_name}_{image_id}.jpg", image_frame)        
        print(f"[I/O] Finished saving images from {device}")

    # Stop recording the video
    def stop_video_recording(self):
        #global cap, out, currently_recording, finished_up_recording
        self.currently_recording = False
        print("[VIDEO] Stopping Recording 4K")
        while not self.finished_up_recording:
            print("[VIDEO] Still stopping 4K")
            time.sleep(1)
        
        # Release everything if job is finished
        print("[VIDEO] Finished stopping 4K")
        self.cap.release()
        #self.out.release()
        cv.destroyAllWindows()
        self.currently_recording = False

    # This function generates a folder for the output of the video with a name for a video, based on the current (date-)time.
    def get_video_name(self):
        # Parameters
        video_output_folder = get_participant_folder(self.participant_id)

        now = str(datetime.datetime.now())
        #video_plus_date = str(video_output_folder + now.replace(':', '_') + "_")
        #video_plus_date = ''
        file_output = video_output_folder + f'part_{self.participant_id}_trialset_{self.trial_set}_'
        file_output += 'calibration_' if self.get_is_calibration else 'experiment_'
        
        # Create the folders
        os.makedirs(video_output_folder, exist_ok=True)
        #os.makedirs(video_plus_date, exist_ok=True)
        
        return file_output