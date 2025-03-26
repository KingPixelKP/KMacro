import macro
import json

initMessage = "##The MAcro starts here##"
textMessage = "This step print this message: \"{}\""
keyMessage = "This step tap's this key \"{}\""
timeMessage = "This step waits for: {}ms"
finalMessage = "##The MAcro ends here##"

def main():
    ...

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
                           lambda s : print(timeMessage.format(i[1])),
                           lambda s : print(finalMessage),
                           lambda s : print("Unrecognized macro action {} :(", i[1])
                           )
