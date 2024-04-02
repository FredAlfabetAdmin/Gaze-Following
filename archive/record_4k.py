import cv2
import time
import os
import numpy as np
from threading import Thread
import threading

# Initialize the video capture
#availableBackends = [cv2.videoio_registry.getBackendName(b) for b in cv2.videoio_registry.getBackends()]
#print(availableBackends) #['FFMPEG', 'GSTREAMER', 'INTEL_MFX', 'MSMF', 'DSHOW', 'CV_IMAGES', 'CV_MJPEG', 'UEYE', 'OBSENSOR']

capture = cv2.VideoCapture(2)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
#cv2.VideoWriter_fourcc(*'mp4v')
# Check if the camera is opened correctly
if not capture.isOpened():
    print("ERROR: Can't initialize camera capture")
    exit(1)

# Set properties: frame width, frame height, and frames per second (FPS)
resolutions = { 0:{'w':4096, 'h': 2160, 'fps':60},
                1:{'w':4096, 'h': 2160, 'fps':5},
                2:{'w':3840, 'h': 2160, 'fps':30},
                3:{'w':3840, 'h': 2160, 'fps':24},
                4:{'w':1920, 'h': 1080, 'fps':60},
                5:{'w':1280, 'h': 720, 'fps':60}
               }
resolution_choice = 4
capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions[resolution_choice]['w'])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions[resolution_choice]['h'])
capture.set(cv2.CAP_PROP_FPS, resolutions[resolution_choice]['fps'])

# Get the resolution
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(capture.get(cv2.CAP_PROP_FPS))
print("Resolution:", width, "x", height, " - FPS:", fps)

# Initialize variables for FPS calculation
start_time = time.time()
num_frames = 0
batch_status = 0
batch_size = resolutions[resolution_choice]['fps'] * 2

os.makedirs('./output/', exist_ok=True)

# Capture loop
#a = []
a = []
i = 0
def write_frames_to_disk():
    global a, i
    new_a = a
    for x in range(len(new_a)):
        cv2.imwrite(f'./output/{((i-10)+x)}.jpg', new_a[x])
        pass
    print('done with writing to IO')

def write_single_frame(data):
    i, frame = data
    cv2.imwrite(f'./output/{i}.jpg', frame)

#while True:
while i < 1000:
    # Capture frame-by-frame
    ret, frame = capture.read()
    #is_success, im_buf_arr = cv2.imencode(".jpg", frame)
    #byte_im = im_buf_arr.tobytes()
    if not ret:
        print("Error: Failed to capture frame")
        break
    Thread(target=write_single_frame, args=([i, frame],)).start()
    #a.append(frame)

    '''
    # Display the captured frame
    #a[batch_status] = byte_im
    a.append(frame)
    
    # Increment frame count
    num_frames += 1
    i += 1
    batch_status += 1

    if batch_status == batch_size:
        t = Thread(target = write_frames_to_disk)
        t.start()
        #write_frames_to_disk(a)
        batch_status = 0
        a = []
    '''
    # Increment frame count
    num_frames += 1
    i += 1
    batch_status += 1
    
    # Calculate FPS every second
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        fps = num_frames / elapsed_time
        print("FPS:", fps)

        # Reset variables for the next FPS calculation
        start_time = time.time()
        num_frames = 0
        print(f'Amount of threads currently running {len(threading.enumerate())}')

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
capture.release()
cv2.destroyAllWindows()
