from script_library import * 

bind : str = "q"
stop_bind : str = "+"

sleepTime = 50

def run():
    init()
    for _ in range(2):
        tapKey("r")
        sleep(sleepTime)
    tapKey("p")
    sleep(sleepTime)
    tapKey("r")
    final()