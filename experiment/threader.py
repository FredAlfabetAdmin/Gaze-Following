import time
from pynput import keyboard
import threading
from threading import Thread
import cv2
import queue
import os

class Threader():
    resulting_output = {}
    key_pressed = None
    #thread_stop = True
    def set_resulting_output(self, value):
        self.resulting_output = value
    def get_resulting_output(self):
        return self.resulting_output

    ############# PARALLELIZATION #############
    # This function runs two events in parallel.
    def parallel(self, first_event, second_event, first_args = None, second_args = None):
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
    
    # This function runs three threads at the same time.
    # Consider changing this to accept lists as inputs with a loop to enable scaling.
    def triple_parallel(self, first_event, second_event, third_event, first_args = None, second_args = None, third_args = None):
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

    ############# KEY PRESS RECORDER #############
    # This function if for listening to the keystrokes.
    def start_listening(self):
        '''
        global thread_stop
        thread_stop = True
        #thread_stop = threading.Event()

        # while not video_recorder.get_is_currently_recording():
        #     print("[THREADING] Awaiting Start of Recording")
        #     time.sleep(1)
        
        # Create threads for script logic and timer, passing the shared flag
        #self.triple_parallel(self.listen_to_key, self.await_keypress, self.timer)

        # script_thread = threading.Thread(target=self.await_keypress)
        # timer_thread = threading.Thread(target=self.timer)

        # script_thread.start()
        # timer_thread.start()
        # script_thread.join()
        # timer_thread.join()
        '''
        self.listen_for_keys()
        
    def show_press(self, _key):
        lr = (_key == keyboard.Key.left or _key == keyboard.Key.right)
        print(f'Key: {_key} - LR: {lr}')

        if lr:
            self.key_pressed = _key
            #print('stopped?')
            return False

    def listen_for_keys(self):
        self.set_resulting_output({'valid':False, 'reason': 'initialization', 'duration':-1})

        l = keyboard.Listener(on_press = self.show_press, suppress = True)
        l.start()        
        start_time = time.time()
        while l.is_alive() and time.time() - start_time < 4:
            time.sleep(0.001)
        
        if l.is_alive():
            self.set_resulting_output({'valid':False, 'reason': 'overtime', 'duration':time.time() - start_time})
            print('Response time exceeded 4 seconds')
            l.stop()
        else:
            if self.key_pressed == keyboard.Key.left:
                reason = 'left'
            else:
                reason = 'right'
            self.set_resulting_output({'valid':True, 'reason': reason, 'duration':time.time() - start_time})
            #print('key was pressed')
    
    '''
    # This function awaits the actual key pressed
    def await_keypress(self):#, thread_stop):
        global thread_stop
        start_time = time.time()
        print(f'Start time: {start_time}')
        output = {'valid':False, 'reason': 'initialization', 'duration':-1}
        self.set_resulting_output(output)
        #while not thread_stop.is_set():
        #self.listen_to_key()
        while thread_stop:
            #print('hi')
            # Check if the time limit is reached
            elapsed_time = time.time() - start_time
            max_duration = 4
            if elapsed_time >= max_duration:
                print(f"[THREADING] Time limit of {max_duration} seconds exceeded")
                output = {'valid':False, 'reason': 'overtime', 'duration':time.time() - start_time}
                self.set_resulting_output(output)
                #thread_stop = False #thread_stop.set()
                break
        thread_stop=False
        output = self.get_resulting_output()
        print(f"[THREADING] Keystroke: {output['reason']} - Took: {output['duration']}")

    def timer(self):
        i = 0
        global thread_stop, start_time
        start_time = time.time()
        #while not thread_stop.is_set():
        while thread_stop:
            print(f"Time passed: {str(time.time() - start_time)[:5]}")
            time.sleep(0.05)
            i+=1
        print(f"[THREADING] I's: {i}")
        
    # This function checks which key was pressed
    def on_press(self, _key):
        global thread_stop
        lr = (_key == keyboard.Key.left or _key == keyboard.Key.right)
        #self.check_key_left_right(_key)
        if lr:
            global key
            thread_stop = False
            key = _key.name
            self.on_release(_key)
                        
            output = {'valid':True, 'reason': key, 'duration':time.time() - start_time}
            self.set_resulting_output(output)
            #keyboard.Listener.stop(self)
        return not lr

    # Required function for the keyboard Listener
    def on_release(self, _key):
        pass

    # This function enables keypresses to be recorded.
    def listen_to_key(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release,
                suppress=True) as listener:
            listener.join()
        print('still here')
        # enums
        #Key.left:  65361
        #Key.right: 65363
        return key
    '''

############# IMAGE PROCESSING #############

# This function is a small passthrough wrapper for writing images 
def wsf(arguments):
    i, frame, video_name, _4K = arguments
    device = '4K' if _4K else 'Pepper'
    os.makedirs(video_name + '/' + device+ '/', exist_ok=True)
    video_name += '/' + device + '/'
    output_file = f'{video_name}{i}.jpg'
    cv2.imwrite(output_file, frame) # Update this to contain the get_video_name()
    
# This is the main function that gets called when saving a single frame to the disk.
# Note: beware of overloading the amount of Threads that can be started.
def write_single_frame(i, frame, video_name,_4K = True):
    #print(threading.active_count())
    #q.put([i, frame, video_name, _4K])
    Thread(target=wsf, args=((i, frame, video_name,_4K),)).start()

def process():
    global q, activearguments
    while active or len(q) != 0:
        if len(q) != 0:
            wsf([q.get()])

q = queue.Queue()
active = False
def start_processing_images():
    global q, active
    active = True
    #Thread(target=process).start()

def set_active(_active):
    global active
    if active: start_processing_images()
    active = _active