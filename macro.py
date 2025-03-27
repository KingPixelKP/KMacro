
import json
import threading
from pynput import keyboard
from pynput import mouse
import time

#Remeber to tun --> source "/home/kpgm/.venv/bin/activate.fish"

#Macro formatting 
#[init] --> initialize macro 
#[t, text]
#[k, key to press]
#[mp, mouse button to click, times to click]
#[ms, time to wait miliseconds]
#[final] --> finalize macro

initMacro = "init"
textMacro = "t"
keyMacro = "k"
mouseClickMacro = "mc"
timeMacro = "ms"
finalMacro = "final"

#List of all active listeners the key being the bind to stop the macro
#they are associated with
activateListeners : dict[str:list] = {}

#Semaphore will interrupt any macros from running ate the same time (TODO)
#Hopefully this may be removed in order to allow different macros to run in parallel
semaphore : threading.Semaphore = threading.Semaphore()
pauseEvent : threading.Event = threading.Event()


conf = "./config.json"
conf_macroPath = "macroPath"
conf_macroPause = "pauseAllMacroBind"

macro_macro = "macro"
macro_bind = "bind"
macro_stopBind = "stopBind"

macroPath = ""

#Load the configuration file
def loadConf():
    with open(conf, "r") as file:
        data : dict = json.load(file)
    global macroPath
    macroPath = data[conf_macroPath]
    pauseEvent.set()
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

    set_key(data[macro_bind], data[macro_stopBind],lambda : on_activate(data), lambda :stop_macro(data))

#Hotkey setter functions
def set_key(bind : str, stopBind : str,  fun, stopFun):

    #Instantiate the hotkey that will start a macro
    hotkey = keyboard.HotKey(keyboard.HotKey.parse(bind), fun) 
    
    #Instantiate the hotkey that will stop the macro
    hotkeyStop = keyboard.HotKey(keyboard.HotKey.parse(stopBind), stopFun)
    
    global activateListeners
    array : list = activateListeners.get(stopBind)

    if array == None:
        array = []

    l : keyboard.Listener = keyboard.Listener(
            on_press=lambda key, injected : update(key, injected, hotkey.press, hotkeyStop.press) ,
            on_release=lambda key, injected : update(key, injected, hotkey.release, hotkeyStop.release))
    array.append(l)
    activateListeners[stopBind] = array
    l.start()

################################


#Functions that handle the Macro types
def initMacroFun(action):
    print("Macro Startted Running")

def textMacroFun(action):
    controller = keyboard.Controller()
    controller.type(action[1])

def keyMacroFun(action):
    controller = keyboard.Controller()
    key = action[1]
    controller.tap(key)

def mouseClickFun(action):
    controller = mouse.Controller()
    button =  mouse.Button[action[1]]
    times = action[2]
    controller.click(button, times)

def timeMacroFun(action):
    time.sleep(int(action[1]) / 1000) #convert to msg

def finalMacroFun(action):
    print("Macro Finished Running")

########################################

def get_action(i : list):
    return i[0]

#This function is called by the hotkey that actovates the macro
def on_activate(data : dict):
    if pauseEvent.is_set(): #Check if macros are paused
        semaphore.acquire() #Check if other macros are running, this is used to stop the macro calling itself (bug)
        steps : list = data[macro_macro]
        print("Macro running")
        for i in steps:
            resolve_step(i, initMacroFun, textMacroFun, keyMacroFun, mouseClickFun, timeMacroFun, finalMacroFun,
                        lambda : print("Unrecognized macro action {} :(", get_action(i)))
            
        semaphore.release() #finish the macro

#This function stops all macros bound to a certain $stopBind
def stop_macro(data : dict):
    global activateListeners
    for i in activateListeners.get(data.get(macro_stopBind)):
        print("Macro Stopped!")
        i.stop()

    activateListeners.pop(data[macro_stopBind])

#This function is called by the listeners to update the state of an hotkey
#This function needs the semaphore to stop the listeners from "listening" the macro itself (bug?)
def update(key : keyboard.Key, injected : bool, fun, stopFun):
    if injected:
        print("Key is injected") #when a macro creates a key press
    else:
        print("Key is true") #when a is actually created by an input device (user)
        if (semaphore._value != 0):
            fun(key)
            stopFun(key)

#This function accepts a MAcro step and resolves it to an action
#It will pass the argument step as the first parameter
def resolve_step(step : str, initFun, textFun, keyFun, clickFun, timeFun, finalFun, error):
        action = get_action(step)
        if action == initMacro:
            initFun(step)
        elif action == textMacro:
            textFun(step)
        elif action == keyMacro:
            keyFun(step)
        elif action == mouseClickMacro:
            clickFun(step)
        elif action == timeMacro:
            timeFun(step)
        elif action == finalMacro:
            finalFun(step)
        else:
            error(step)
