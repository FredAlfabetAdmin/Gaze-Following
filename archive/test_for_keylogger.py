import time
from pynput import keyboard
import threading
from experiment.threader import Threader

#mykb = keyboard.Controller()


t = Threader()
t.start_listening()

print(t.get_resulting_output())


'''
def show_press(_key):
    lr = (_key == keyboard.Key.left or _key == keyboard.Key.right)
    print(f'Key: {_key} - LR: {lr}')

    if lr:
        #l.stop()
        print('stopped?')
        return False

def listen_for_keys():
    l = keyboard.Listener(on_press=show_press, suppress=True)
    l.start()
    start_time = time.time()
    while l.is_alive() and time.time() - start_time < 4:
        time.sleep(0.001)
    
    if l.is_alive():
        print('4 seconds passed and still alive LOL')
        l.stop()
    else:
        print('key was pressed')

def main():
    t = threading.Thread(target=listen_for_keys)
    t.start()

    t.join()


main()
'''

'''
import time
from pynput import keyboard

#mykb = keyboard.Controller()
exit_script = False
def action_press(_key):
    global exit_script

    # Do a check for the END key, since that is a special character to break out of the Keyboard listener
    if _key == keyboard.Key.end:
        exit_script = True
        return False

    # Check if the Left or Right arrow was pressed. If so, break.
    lr = (_key == keyboard.Key.left or _key == keyboard.Key.right)
    if lr:
        print('LA or RA pressed.')
        exit_script = True
    return False

start_time = time.time()
with keyboard.Listener(on_press=action_press, suppress=True) as l:
    while exit_script == False:
        if time.time() > start_time + 4:
            print('took too long!')
            exit_script = True
            l.stop()
    l.join()
'''
print('fin')