import macro
import json

#MAcro Messgaes
initMessage = "##The MAcro starts here##"
textMessage = "This step print this message: \"{}\""
keyMessage = "This step tap's this key \"{}\""
timeMessage = "This step waits for: {}ms"
finalMessage = "##The MAcro ends here##"

#Config Messages
pathToMacro = "Path used for macro files --> {}"
pauseKeyBind = "Keybing used to pause all macros --> {}"

def main():
    ...

#This function lists the properties of a macro these being 
#The caller keybind the stopper keybind
#And the steps the macro takes
def list_macro_properties(line):
    file = line.split()[1]
    with open(macro.macroPath + file) as file:
        data = json.load(file)

    print("Bind--> {}".format(data[macro.macro_bind]))
    print("Bind to Stop--> {}\n".format(data[macro.macro_stopBind]))

    print("Steps--> ")
    for i in data[macro.macro_macro]:
        macro.resolve_step(i, lambda s : print(initMessage),
                           lambda s : print(textMessage.format(i[1])),
                           lambda s : print(keyMessage.format(i[1])),
                           lambda s : print("###TODO###"),
                           lambda s : print(timeMessage.format(i[1])),
                           lambda s : print(finalMessage),
                           lambda s : print("Unrecognized macro action {} :(", i[1])
                           )
        
#List the attributes of the config file and their values (Unused)        
def list_config_file():
    with open(macro.conf) as file:
        data = json.load(file)

    print(pathToMacro.format(macro.macroPath))
    print(pauseKeyBind.format(data[macro.conf_macroPause]))





