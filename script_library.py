import macro

def init():
    """This function denotes the start of the macro (It doesnt do anything)"""
    macro.initMacroFun()

def final():
    """This function denotes the end of the macro it also does not do anything"""
    macro.finalMacroFun()

def type(text : str, repeat : int = 1, delay = 20):
    """Function called by the user for typing text
    Param:
    text --> text to output
    repeat --> ammount of times to repeat the action"""
    for _ in range(repeat):
        macro.textMacroFun(["",text], delay)

def tapKey(key : str, repeat : int = 1):
    """Function called by the user for tapping a key (up and down)
    Param:
    key --> key to press
    repeat --> ammount of times to repeat the action"""
    for _ in range(repeat):
        macro.keyMacroFun(["",key])

def mouseClick(mouseButton : str, repeat : int = 1):
    """Function called by the user to simulate a mouse key press
    Param:
    mouseButton --> mouse button to press
    repeat --> ammount of times to repeat this action"""
    for _ in range(repeat):
        macro.mouseClickFun(["",mouseButton])

def sleep(miliseconds : int):
    """Function called by the user to wait
    Param:
    miliseconds --> wait time in miliseconds"""
    macro.timeMacroFun(["",miliseconds])
