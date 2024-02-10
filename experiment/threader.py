import threading
import time
import msvcrt
import datetime
from experiment.recorder import get_is_currently_recording, stop_video_recording

output = ()

def await_keypress(thread_stop):
    global output
    start_time = time.time()
    print("starting to listen")
    # Perhaps run the experimental conditioned code here?
    while not thread_stop.is_set():
        if msvcrt.kbhit():
            key = msvcrt.getch() # Required to be called, but does not actually do anything?
            arrow_key = msvcrt.getch().decode('utf-8')
            thread_stop.set()

            # Consider if the arrow keys here have to be used or not.
            if arrow_key == 'M': output = (True,'right')
            elif arrow_key == 'K': output = (True, 'left')
            else: output = (False, '')
            break

        # Check if the time limit is reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            print("Time limit exceeded. Stopping script logic.")
            thread_stop.set()
            break

def timer(thread_stop):
    i = 0
    while not thread_stop.is_set():
        print(f"I: {i}")
        time.sleep(0.1)
        i+=1

def start_listening():
    # Create a shared flag between the threads
    thread_stop = threading.Event()

    while not get_is_currently_recording():
        print("Not recording yet!")
        time.sleep(0.1)
    # Create threads for script logic and timer, passing the shared flag
    script_thread = threading.Thread(target=await_keypress, args=(thread_stop,))
    timer_thread = threading.Thread(target=timer, args=(thread_stop,))

    script_thread.start()
    timer_thread.start()
    script_thread.join()
    timer_thread.join()

    stop_video_recording()

    return output

def parallel(first_event, second_event):
    # Create threads for script logic and timer, passing the shared flag
    script_thread = threading.Thread(target=first_event)
    timer_thread = threading.Thread(target=second_event)

    script_thread.start()
    timer_thread.start()
    script_thread.join()
    timer_thread.join()