from script_library import * #Every script needs to import this library

bind = "<ctrl>+e" #Every script needs to bind a key or a a key with modifiers 
stop_bind = "+" #Every script needs to bind a stop_bind 

def run(): #Every script needs a function called run to be called by the manager
    init()#Does nothign only sends a message saying the macro is running
    
    for _ in range(10): #A user can use a for loop to repeat actions
        type("Dingus")
    #or
    type("Dingus", 10) #Or a user can just pass the number of times a command as to be repeated

    type("Dingus", delay=1000)#Create artificial delay between key presses

    final() #Also does nothing sends a message saying the macro as ended
