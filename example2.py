from script_library import * #Every script needs to import this library

bind = "<ctrl>+e" #Every script needs to bind a key or a a key with modifiers 
stop_bind = "+" #Every script needs to bind a stop_bind 

def run():
    type("Dingus", repeat=2, delay=100)
    exec("firefox")
    