
import json
import threading
from pynput import keyboard
import time

#Remeber to tun --> source "/home/kpgm/.venv/bin/activate.fish"

#Macro formatting 
#[init] --> initialize macro 
#[t, text]
#[k, key to press]
#[ms, time to wait miliseconds]
#[final] --> finalize macro

initMacro = "init"
textMacro = "t"
keyMacro = "k"
timeMacro = "ms"
finalMacro = "final"

#List of all active listeners the key being the bind to stop the macro
#they are associated with
activateListeners : dict[str:list] = {}

#Semaphore will interrupt any macros from running ate the same time (TODO)
#Hopefully this may be removed in order to allow different macros to run in parallel
semaphore : threading.Semaphore = threading.Semaphore()


conf = "./config.json"
conf_macroPath = "macroPath"

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
            on_press=lambda event : update(event, hotkey.press, hotkeyStop.press) ,
            on_release=lambda event : update(event, hotkey.release, hotkeyStop.release))
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

def timeMacroFun(action):
    time.sleep(int(action[1]) / 1000) #convert to msg

def finalMacroFun(action):
    print("Macro Finished Running")

########################################

def get_action(i : list):
    return i[0]

#This function is called by the hotkey that actovates the macro
def on_activate(data : dict):
    steps : list = data[macro_macro]
    semaphore.acquire()
    print("Macro running")
    for i in steps:
        resolve_step(i, initMacroFun, textMacroFun, keyMacroFun, timeMacroFun, finalMacroFun,
                     lambda : print("Unrecognized macro action {} :(", get_action(i)))
        
    semaphore.release()

#This function stops all macros bound to a certain $stopBind
def stop_macro(data : dict):
    global activateListeners
    for i in activateListeners.get(data.get(macro_stopBind)):
        print("Macro Stopped!")
        i.stop()

    activateListeners.pop(data[macro_stopBind])

#This function is called by the listeners to update the state of an hotkey
#This function needs the semaphore to stop the listeners from "listening" the macro itself (bug?)
def update(key : keyboard.Key, fun, stopFun):
    if (semaphore._value != 0):
        fun(key)
        stopFun(key)

#This function accepts a MAcro step and resolves it to an action
#It will pass the argument step as the first parameter
def resolve_step(step : str, fun1, fun2, fun3, fun4, fun5, error):
        action = get_action(step)
        if action == initMacro:
            fun1(step)
        elif action == textMacro:
            fun2(step)
        elif action == keyMacro:
            fun3(step)
        elif action == timeMacro:
            fun4(step)
        elif action == finalMacro:
            fun5(step)
        else:
            error(step)
