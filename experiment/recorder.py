# The functions in this file are mostly based from the OpenVC VideoCapture tutorial, which can be found here:
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

import os
import cv2 as cv
import time
from auxillary import get_participant_folder, save_dataframe_to_csv, append_info_to_list
from threader import write_single_frame

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
    def set_capture_device(self, _capture_device):
        self.capture_device = _capture_device
    def set_currently_recording(self, _currently_recording):
        self.currently_recording = _currently_recording

    # FUNCTIONS TO RECORD
    def start_video_recording(self):
        ### Record_in_4K
        self.cap = cv.VideoCapture(self.capture_device)
        self.cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # Check if the camera is opened correctly
        if not self.cap.isOpened():
            print("ERROR: Can't initialize camera capture")
            exit(1)

        # Set properties: frame width, frame height, and frames per second (FPS)
        resolutions = { 0:{'w':4096, 'h': 2160, 'fps':30},
                        1:{'w':3840, 'h': 2160, 'fps':24},
                        2:{'w':1920, 'h': 1080, 'fps':30},
                        3:{'w':1920, 'h': 1080, 'fps':60},
                        4:{'w':1280, 'h': 720, 'fps':30}               
                    }
        resolution_choice = 3
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, resolutions[resolution_choice]['w'])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolutions[resolution_choice]['h'])
        self.cap.set(cv.CAP_PROP_FPS, resolutions[resolution_choice]['fps'])

        # Get the resolution
        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv.CAP_PROP_FPS))
        print(f"Resolution W: {width} - H: {height} - FPS: {fps}")
        if width < 1920 or height < 1080:
            res_low = input("RESOLUTION IS NOT FULL QUALITY. CONFIRM CONTINUATION? [Y/n]")
            if str.lower(res_low) != 'y':
                raise Exception

        # Only start when it is actually recording
        self.currently_recording = True
        self.finished_up_recording = False
        frameless = []
        frame_buffer = []
        i = 0
        num_frames = 0
        start_time = time.time()

        # The actual recording loop
        while self.cap.isOpened() and self.currently_recording:
            ret, frame = self.cap.read()
            if not ret:
                print("[VIDEO] Can't receive frame (stream end?). Exiting ...") # From the OpenCV tutorial
                break
        
            # Get the current time.
            frameless, i = append_info_to_list(frameless, i)
            #frame_buffer.append(frame)
            write_single_frame(i, frame, self.get_video_name(), True)


            # if len(frame_buffer) == 4:
            #     write_frame_buffer(i, frame_buffer, self.get_video_name())
            #     frame_buffer = []
            if cv.waitKey(1) == ord('q'): # Press 'q' on the Python Window to stop the script
                break
            
            # Calculate FPS every second
            num_frames += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1.0:
                fps = num_frames / elapsed_time
                print("[4K] FPS:", fps)

                # Reset variables for the next FPS calculation
                start_time = time.time()
                num_frames = 0

        # Finish up recording and save the data to IO
        print("[VIDEO] Ended video recording loop 4K")
        self.finished_up_recording = True
        self.stop_video_recording()
        cv.destroyAllWindows()
        print(f'[VIDEO] Starting to write the 4K dataframe to IO ({len(frameless)} items)')
        save_dataframe_to_csv(frameless, self.get_video_name() + '4K')
        print("[VIDEO] Finished saving images from 4K")

    # Stop recording the video
    def stop_video_recording(self):
        self.currently_recording = False
        print("[VIDEO] Stopping Recording 4K")
        while not self.finished_up_recording:
            print("[VIDEO] Still stopping 4K")
            time.sleep(1)
        
        # Release everything if job is finished
        print("[VIDEO] Finished stopping 4K")
        self.cap.release()
        cv.destroyAllWindows()
        self.currently_recording = False

    # This function generates a folder for the output of the video with a name for a video, based on the current (date-)time.
    def get_video_name(self):
        video_output_folder = get_participant_folder(self.participant_id)
        file_output = video_output_folder + f'part_{self.participant_id}_trialset_{self.trial_set}_'
        file_output += 'calibration_' if self.get_is_calibration else 'experiment_'
        os.makedirs(video_output_folder, exist_ok=True)
        return file_output
