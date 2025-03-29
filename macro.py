import os
os.environ['PYNPUT_BACKEND_KEYBOARD'] = 'uinput'

uinput_device_paths = "/dev/input/event2"

import json
import threading
from pynput import keyboard
import time
import subprocess
from enum import Enum
import mouseKey

ydotool = "ydotool"

#Macro formatting 
#[init] --> initialize macro 
#[t, text]
#[k, key to press]
#[mp, mouse button to click, times to click]
#[ms, time to wait miliseconds]
#[final] --> finalize macro

initMacro = "init"
textMacro = "type"
keyMacro = "key"
mouseClickMacro = "click"
timeMacro = "sleep"
finalMacro = "final"

#List of all active listeners the key being the bind to stop the macro
#they are associated with
activateListeners : dict[str:list] = {}

#Semaphore will interrupt any macros from running ate the same time (TODO)
#Hopefully this may be removed in order to allow different macros to run in parallel
semaphore : threading.Semaphore = threading.Semaphore()
pauseEvent : threading.Event = threading.Event()
macroRunning : threading.Event = threading.Event()
macroNoLetRun : threading.Event = threading.Event()


conf = "./config.json"
conf_macroPath = "macroPath"
conf_macroPause = "pauseAllMacroBind"

macro_macro = "macro"
macro_bind = "bind"
macro_stopBind = "stopBind"
macro_run_on_top = "letRunOnTop"
macro_will_run_on_top = "willRunOnTop"

macroPath = ""


#Load the configuration file
def loadConf():
    with open(conf, "r") as file:
        data : dict = json.load(file)
    global macroPath
    macroPath = data[conf_macroPath]
    pauseEvent.set()
    macroRunning.clear()
    macroNoLetRun.clear()
    setup_pause_hotkey(data[conf_macroPause])

def setup_pause_hotkey(hotkey : str):
    hotkey : keyboard.HotKey = keyboard.HotKey(keyboard.HotKey.parse(hotkey), toggle_pause_event)

    listener : keyboard.Listener = keyboard.Listener(on_press=hotkey.press,
                                                     on_release=hotkey.release)
    listener.start()

def toggle_pause_event():
    if pauseEvent.is_set():
        print("Macros paused!")
        pauseEvent.clear()
    else:
        print("Macros enabled!")
        pauseEvent.set()

def prepare_macro(line : str):
    args : list = line.split()
    file = args[1]

    with open(macroPath + file, "r") as file:
        data = json.load(file)

    set_key(data[macro_bind], data[macro_stopBind],data, lambda : on_activate(data), lambda :stop_macro(data))

#Hotkey setter functions
def set_key(bind : str, stopBind : str, data : dict, fun, stopFun):

    #Instantiate the hotkey that will start a macro
    hotkey = keyboard.HotKey(keyboard.HotKey.parse(bind), fun) 
    
    #Instantiate the hotkey that will stop the macro
    hotkeyStop = keyboard.HotKey(keyboard.HotKey.parse(stopBind), stopFun)
    
    global activateListeners
    array : list = activateListeners.get(stopBind)

    if array == None:
        array = []

    l : keyboard.Listener = keyboard.Listener(
            on_press=lambda key, injected : update(key, injected, data, hotkey.press, hotkeyStop.press) ,
            on_release=lambda key, injected : update(key, injected, data, hotkey.release, hotkeyStop.release), 
            uinput_device_paths = [uinput_device_paths])
    array.append(l)
    activateListeners[stopBind] = array
    l.start()

################################


#Functions that handle the Macro types
def initMacroFun():
    print("Macro Startted Running")

def textMacroFun(action):
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

def get_action(i : list):
    return i[0]

#This function is called by the hotkey that actovates the macro
def on_activate(data : dict):
    if pauseEvent.is_set() and not (data[macro_will_run_on_top] == "n" and macroRunning.is_set()): 
        #Check if macros are paused or if a macro
        #cant run while other is running
        if(macroNoLetRun.is_set()): #Ignore for any macro that does not want other running on top of it
            print("A macro doesnt want running on top input ignored")
        else:
            if(data[macro_run_on_top] == "n"): #If a macro does not want other to run it sets the event
                macroNoLetRun.set()
                
            steps : list = data[macro_macro]
            print("Macro running")
            for i in steps:
                resolve_step(i, initMacroFun, textMacroFun, keyMacroFun, mouseClickFun, timeMacroFun, finalMacroFun,
                            lambda : print("Unrecognized macro action {} :(", get_action(i)))
                
            macroNoLetRun.clear() #Stop ignoring any other macros
    else:
        print("Macros are paused or a this macro wont run while other is running")


#This function stops all macros bound to a certain $stopBind
def stop_macro(data : dict):
    global activateListeners
    for i in activateListeners.get(data.get(macro_stopBind)):
        print("Macro Stopped!")
        i.stop()

    activateListeners.pop(data[macro_stopBind])

#This function is called by the listeners to update the state of an hotkey
#This function needs the semaphore to stop the listeners from "listening" the macro itself (bug?)
def update(key : keyboard.Key, injected : bool, data : dict, fun, stopFun):
    if injected:
        print("Key is injected") #when a macro creates a key press
    else:
        print("Key is true") #when a is actually created by an input device (user)
        fun(key)
        stopFun(key)

#This function accepts a MAcro step and resolves it to an action
#It will pass the argument step as the first parameter
def resolve_step(step : str, initFun, textFun, keyFun, clickFun, timeFun, finalFun, error):
        action = get_action(step)
        if action == initMacro:
            initFun()
        elif action == textMacro:
            textFun(step)
        elif action == keyMacro:
            keyFun(step)
        elif action == mouseClickMacro:
            clickFun(step)
        elif action == timeMacro:
            timeFun(step)
        elif action == finalMacro:
            finalFun()
        else:
            error(step)
