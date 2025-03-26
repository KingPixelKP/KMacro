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

semaphore : threading.Semaphore = threading.Semaphore()

initMacro = "init"
textMacro = "t"
keyMacro = "k"
timeMacro = "ms"
finalMacro = "final"

activateListeners : dict[str:list] = {}


conf = "./config.json"
pathName = "macroPath"
macroPath = ""
exit = "EXIT"
help = "HELP"
run = "RUN"
helpMenu = """Help --> show this menu
Exit --> exit the program
Run (macro text file) --> run a macro"""
prompt = "?>>"

data = 0

def main():
    loadConf()
    cmd : str= ""
    line : str = [""]

    while cmd.upper() != exit.upper():
        line = input(prompt)
        cmd = line.split()[0].upper()
        if cmd == help:
            print(helpMenu)
        elif cmd == run:
            prepare_macro(line)

def loadConf():
    with open(conf, "r") as file:
        data : dict = json.load(file)
    global macroPath
    macroPath = data[pathName]


def prepare_macro(line : str):
    args : list = line.split()
    file = args[1]

    with open(macroPath + file, "r") as file:
        data = json.load(file)

    #print(data)
    macro_thread(data)


def initMacroFun(action):
    print("Macro Ran")

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
    print("Macro finalized")

def get_action(i : list):
    return i[0]

def on_activate(data : dict):
    steps : list = data["macro"]
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

def stop_macro(data : dict):
    global activateListeners
    for i in activateListeners.get(data.get("stopBind")):
        print("Macro Stopped!")
        i.stop()

    activateListeners.pop(data["stopBind"])

def update(key : keyboard.Key, fun, stopFun):
    if (semaphore._value != 0):
        fun(key)
        stopFun(key)


#Hotkey setter functions
def set_key(bind : str, stopBind : str,  fun, stopFun):

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse(bind),
        fun)
    
    hotkeyStop = keyboard.HotKey(
        keyboard.HotKey.parse(stopBind),
        stopFun)
    
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

#Create thread with desired function
def macro_thread(data : dict):
    set_key(data["bind"], data["stopBind"],lambda : on_activate(data), lambda :stop_macro(data))


main()