# What's This?

A macro script i created in python that works in wayland.  
This is not optimized, and is a the moment untested.
The language accepted by the macros is in a little comment in macro.py every macro needs to be made in a .json file as the one provided as an example.

# How to use

Need to install pynput first

```
pip install pynput
```
Now download all .py and the config.json files

```
python3 main.py
```

# Warning

## 1

Due to some limitations of Wayland (Restricting keyboard events), uinput is used as the backend for pynput  
this means that the script either as to be ran as the root user (not recomended) or the currently running user  
must be allowed to acess /dev/input/ 

```
sudo chmod 666 /dev/input/
```

## 2

On some systems pynput might recognise the keyboard as some other device in /dev/input/ to solve this at the moment  
a variable called uinput_device_paths was added to restrict uiput from searching all the events and only listening to  
those specified by the user 

## Dependencies

This requires ydotool to run as it is much simpler to use it as a input simulator than the one in pynput that uses a kernel layout instead of a xkb 