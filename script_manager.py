import os
os.environ['PYNPUT_BACKEND_KEYBOARD'] = 'uinput'

uinput_device_paths = "/dev/input/event2"

import json
import importlib
from threading import Event

from pynput import keyboard


conf_path = "./config.json"

class Script():

    _run : callable
    _bind : str
    _stop_bind : str
    
    name : str

    def __init__(self, script, name):
        self._run = getattr(script, "run")
        self._bind = getattr(script, "bind")
        self._stop_bind = getattr(script, "stop_bind")
        self.name = name

    def __str__(self):
        return self.name

    def run(self):
        self._run()

class Manager():

    _conf_file : str = ""
    _conf_macro_path : str = "macroPath"
    _conf_macro_pause : str = "pauseAllMacroBind"
    _macros_paused : Event

    active_macros : dict = {}    
    data : dict = {}
    pause_listener : keyboard.Listener    


    def __init__(self, conf_path : str):
        self.loadConfigFile(conf_path)
        self._macros_paused = Event()
        self._macros_paused.clear()
        self.create_pause_listener()

    def loadConfigFile(self, conf_path : str):
        """Loads the global config file"""
        with open(conf_path, "r") as file:
             self.data = json.load(file)

    def create_pause_listener(self):
        hotkey : keyboard.HotKey = keyboard.HotKey(keyboard.HotKey.parse(self.data[self._conf_macro_pause]),
                                                    self.toggle_pause_event)

        listener : keyboard.Listener = keyboard.Listener(on_press=hotkey.press,
                                                     on_release=hotkey.release,
                                                     uinput_device_paths = [uinput_device_paths] )
        listener.start()
        self.pause_listener = listener
        

    def toggle_pause_event(self):
        if self._macros_paused.is_set(): 
            print("Macros enabled!")
            self._macros_paused.clear()
        else:
            print("Macros paused!")
            self._macros_paused.set()


    def load_new_macro(self, macro_name : str):
        """Loads a new macro by importing the module where the macro is stored at"""
        script = importlib.import_module(macro_name, self.data[self._conf_macro_path])
        s = Script(script, macro_name)

        names : dict = self.active_macros.get(s._bind)

        if names is None:
            names = {}
    
        listener = self.create_listener_hotkey(s) #Create a new listener for this macro
        names[s.name] = listener
        self.active_macros[s._bind] = names
        listener.start()

    def unload_macro(self, bind, macro_name):
        names : dict = self.active_macros.get(bind)
        if names is None:
            print("No macro binded to: {}".format(bind))
        elif names.get(macro_name) is None:
            print("No macro named: {}".format(macro_name))
        else:
            names.get(macro_name).stop()
            self.active_macros.get(bind).pop(macro_name)
            if self.active_macros.get(bind).__len__() == 0:
                self.active_macros.pop(bind)
            print("Macro {} unloaded sucessfully".format(macro_name))


    def create_listener_hotkey(self, script : Script):
        hotkey = keyboard.HotKey(keyboard.HotKey.parse(script._bind),
                                  lambda : self.run_macro(script.run)) 
        stop_hotkey = keyboard.HotKey(keyboard.HotKey.parse(script._stop_bind),
                                      lambda : self.unload_macro(script._bind, script.name))
        
        listener = keyboard.Listener(on_press=lambda key : self.update_hotkey_states(key, hotkey.press, stop_hotkey.press),
            on_release=lambda key : self.update_hotkey_states(key, hotkey.release, stop_hotkey.release), 
            uinput_device_paths = [uinput_device_paths])
        
        return listener
        
    def update_hotkey_states(self,key, fun1, fun2):
        if isinstance(key, keyboard.KeyCode):
            #print("Macros updated with key: {}".format(key.char))
            pass
        else:
            pass
            #print("Macros updated with key: {}".format(key.name))
        fun1(key)
        fun2(key)

    def run_macro(self, run_function : callable):
        if self._macros_paused.is_set():
            print("Macros paused ignoring")
        else:
            run_function()

    def list_active_macros(self):
        for bind, dict in self.active_macros.items():
            print("Bind: {}".format(bind))
            for k in dict.keys():
                print("Macro name: {}".format(bind, k))
            print()
