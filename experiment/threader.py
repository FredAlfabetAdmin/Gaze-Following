import threading
import time
import msvcrt

output = ()

def await_keypress(thread_stop):
    global output
    start_time = time.time()
    print("starting to listen")
    # Perhaps run the experimental conditioned code here?
    while not thread_stop.is_set():
        if msvcrt.kbhit():
            #key = msvcrt.getch().decode('utf-8')   
            key = msvcrt.getch()
            arrow_key = msvcrt.getch().decode('utf-8')
            thread_stop.set()

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
    while not thread_stop.is_set():
        time.sleep(0.1)

def start_listening():
    # Create a shared flag between the threads
    thread_stop = threading.Event()

    # Create threads for script logic and timer, passing the shared flag
    script_thread = threading.Thread(target=await_keypress, args=(thread_stop,))
    timer_thread = threading.Thread(target=timer, args=(thread_stop,))

    script_thread.start()
    timer_thread.start()
    script_thread.join()
    timer_thread.join()

    return output

