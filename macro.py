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
unrecognized_cmd = "Unrecognized command try \"help\" in order to learn more"
exit = "EXIT"
help = "HELP"
run = "RUN"
helpMenu = """Help --> show this menu
Exit --> exit the program
Run (macro text file) --> run a macro"""
prompt = "?>>"

#Load the configuration file
def loadConf():
    with open(conf, "r") as file:
        data : dict = json.load(file)
    global macroPath
    macroPath = data[conf_macroPath]

def main():
    loadConf()
    cmd : str= ""
    line : str = []

    while cmd.upper() != exit.upper():
        line = input(prompt)
        cmd = line.split()[0].upper()
        if cmd == help:
            print(helpMenu)
        elif cmd == run:
            prepare_macro(line)
        else:
            print(unrecognized_cmd)



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
        action = get_action(i)
        if action == initMacro:
            initMacroFun(i)
        elif action == textMacro:
            textMacroFun(i)
        elif action == keyMacro:
            keyMacroFun(i)
        elif action == timeMacro:
            timeMacroFun(i)
        elif action == finalMacro:
            finalMacroFun(i)
        else:
            print("Unrecognized macro action {} :(", action)
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


main()