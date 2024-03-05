import time
import msvcrt
import datetime
import threading
from recorder import Recorder#, get_is_currently_recording, stop_video_recording

class Threader():
    resulting_output = {}
    def set_resulting_output(self, value):
        self.resulting_output = value
    def get_resulting_output(self):
        return self.resulting_output
    
    def start_listening(self, args):
        video_recorder = args[0]
        # Create a shared flag between the threads
        thread_stop = threading.Event()

        while not video_recorder.get_is_currently_recording():
            print("[THREADING] Awaiting Start of Recording")
            time.sleep(1)
        
        # Create threads for script logic and timer, passing the shared flag
        script_thread = threading.Thread(target=self.await_keypress, args=(thread_stop,))
        timer_thread = threading.Thread(target=self.timer, args=(thread_stop,))

        script_thread.start()
        timer_thread.start()
        script_thread.join()
        timer_thread.join()
        
        #return output
    
    def parallel(self, first_event, second_event, first_args = None, second_args = None):
        # Create threads for script logic and timer, passing the shared flag
        if first_args == None:
            first_thread = threading.Thread(target=first_event)
        else:
            first_thread = threading.Thread(target=first_event, args=(first_args,))
        if second_args == None:
            second_thread = threading.Thread(target=second_event)
        else:
            second_thread = threading.Thread(target=second_event, args=(second_args,))

        first_thread.start()
        second_thread.start()
        first_thread.join()
        second_thread.join()
    
    def triple_parallel(self, first_event, second_event, third_event, first_args = None, second_args = None, third_args = None):
        # Create threads for script logic and timer, passing the shared flag
        if first_args == None:
            first_thread = threading.Thread(target=first_event)
        else:
            first_thread = threading.Thread(target=first_event, args=(first_args,))
        if second_args == None:
            second_thread = threading.Thread(target=second_event)
        else:
            second_thread = threading.Thread(target=second_event, args=(second_args,))
        if third_args == None:
            third_event = threading.Thread(target=third_event)
        else:
            third_event = threading.Thread(target=third_event, args=(third_args,))

        first_thread.start()
        second_thread.start()
        third_event.start()
        first_thread.join()
        second_thread.join()
        third_event.join()

    def await_keypress(self, thread_stop):
        start_time = time.time()
        print('Start time: {start_time}')
        output = {'valid':False, 'reason': 'initialization', 'duration':-1}
        #print("[THREADING] Watching Keystrokes")
        while not thread_stop.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch() # Required to be called, but does not actually do anything?
                arrow_key = msvcrt.getch().decode('utf-8')
                thread_stop.set()

                # Consider if the arrow keys here have to be used or not.
                if arrow_key == 'M':
                    output = {'valid': True, 'reason': 'right', 'duration': time.time() - start_time}
                elif arrow_key == 'K':
                    output = {'valid': True, 'reason': 'left', 'duration': time.time() - start_time}
                else:
                    output = {'valid': False, 'reason': 'wrongkey', 'duration': time.time() - start_time}
                break

            # Check if the time limit is reached
            elapsed_time = time.time() - start_time
            max_duration = 4
            if elapsed_time >= max_duration:
                print(f"[THREADING] Time limit of {max_duration} seconds exceeded")
                output = {'valid':False, 'reason': 'overtime', 'duration':time.time() - start_time}
                thread_stop.set()
                break
        print(f"[THREADING] Keystroke: {output['reason']} - Took: {output['duration']}")
        self.set_resulting_output(output)

    def timer(self, thread_stop):
        i = 0
        start_time = time.time()
        while not thread_stop.is_set():
            print(f"Time passed: {str(time.time() - start_time)[:5]}")
            time.sleep(0.05)
            i+=1
        print(f"[THREADING] I's: {i}")