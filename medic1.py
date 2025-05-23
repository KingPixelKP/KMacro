from script_library import *

bind : str = "e"
stop_bind : str = "+"

sleepTime = 50

def run():
    init()
    tapKey("r")
    sleep(sleepTime)
    tapKey("p")
    for _ in range(2):
        sleep(sleepTime)
        tapKey("r")
    final()


