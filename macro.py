import os
os.environ['PYNPUT_BACKEND_KEYBOARD'] = 'uinput'

uinput_device_paths = "/dev/input/event2"

import time
import subprocess
import mouseKey

ydotool = "ydotool"
ydotool_delay_argument = "--key-delay={}"

initMacro = "init"
textMacro = "type"
keyMacro = "key"
mouseClickMacro = "click"
timeMacro = "sleep"
finalMacro = "final"

#Functions that handle the Macro types
def initMacroFun():
    print("Macro Startted Running")

def textMacroFun(action, delay = 20):
    if delay != 20:
        delay = ydotool_delay_argument.format(delay)
        subprocess.run([ydotool, textMacro, delay, action[1]])
    else:
        subprocess.run([ydotool, textMacro, action[1]])

def keyMacroFun(action):
    subprocess.run([ydotool, textMacro, action[1]])

def mouseClickFun(action):
    if (isinstance(action[1], str)):
        mouseButton = mouseKey.get_hex_from_string(action[1])
    else:
        mouseButton = int(mouseButton)
    subprocess.run([ydotool, mouseButton, mouseButton])

def timeMacroFun(action):
    time.sleep(int(action[1]) / 1000) #convert to ms

def finalMacroFun():
    print("Macro Finished Running")

########################################