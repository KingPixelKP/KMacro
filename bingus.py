import subprocess
import os
os.environ['PYNPUT_BACKEND_KEYBOARD'] = 'uinput'

device_paths = "/dev/input/event2"

from pynput import keyboard

def on_press(key):
    try:
        k = keyboard.Controller()
        subprocess.run(["ydotool", "type", "dingus"])
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release, uinput_device_paths = [device_paths]) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release, uinput_device_paths = [device_paths])
listener.start()
