import cv2
import time

# Initialize the video capture
#availableBackends = [cv2.videoio_registry.getBackendName(b) for b in cv2.videoio_registry.getBackends()]
#print(availableBackends) #['FFMPEG', 'GSTREAMER', 'INTEL_MFX', 'MSMF', 'DSHOW', 'CV_IMAGES', 'CV_MJPEG', 'UEYE', 'OBSENSOR']
capture = cv2.VideoCapture(0, cv2.CAP_FFMPEG)
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# Check if the camera is opened correctly
if not capture.isOpened():
    print("ERROR: Can't initialize camera capture")
    exit(1)

# Set properties: frame width, frame height, and frames per second (FPS)
resolutions = { 0:{'w':4096, 'h': 2160, 'fps':30},
                1:{'w':3840, 'h': 2160, 'fps':60},
                2:{'w':1920, 'h': 1080, 'fps':30},
                3:{'w':1280, 'h': 720, 'fps':30}               
               }
resolution_choice = 0
capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolutions[resolution_choice]['w'])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutions[resolution_choice]['h'])
capture.set(cv2.CAP_PROP_FPS, resolutions[resolution_choice]['fps'])

# Get the resolution
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Resolution:", width, "x", height)

# Initialize variables for FPS calculation
start_time = time.time()
num_frames = 0

# Capture loop
while True:
    # Capture frame-by-frame
    ret, frame = capture.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Display the captured frame
    cv2.imshow("Frame", frame)

    # Increment frame count
    num_frames += 1

    # Calculate FPS every second
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        fps = num_frames / elapsed_time
        print("FPS:", fps)

        # Reset variables for the next FPS calculation
        start_time = time.time()
        num_frames = 0

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
capture.release()
cv2.destroyAllWindows()
