import macroEditor
import macro

unrecognized_cmd = "Unrecognized command try \"help\" in order to learn more"
exit = "EXIT"
help = "HELP"
run = "RUN"
helpMenu = """Help --> show this menu
Exit --> exit the program
Run (macro text file) --> run a macro"""
prompt = "?>>"

def main():
    macro.loadConf()

    cmd : str= ""
    line : str = []

    while cmd.upper() != exit.upper():
        line = input(prompt)
        cmd = line.split()[0].upper()
        if cmd == help:
            print(macro.helpMenu)
        elif cmd == run:
            macro.prepare_macro(line)
        elif cmd == "LIST":
            macroEditor.list_macro_properties(line)
        elif cmd == exit:
            pass
        else:
            print(unrecognized_cmd)

main()