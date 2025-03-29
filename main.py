import macroEditor
import macro
import script_manager

unrecognized_cmd = "Unrecognized command try \"help\" in order to learn more"
exit = "EXIT"
help = "HELP"
run = "RUN"
script = "SCRIPT"
active = "ACTIVE"
helpMenu = """Help --> show this menu
Exit --> exit the program
Run (macro text file) --> run a macro"""
prompt = "?>>"


conf_path = "./config.json"

def main():
    macro.loadConf()

    manager = script_manager.Manager(conf_path)

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
        elif cmd == script:
            manager.load_new_macro(line.split()[1])
        elif cmd == active:
            manager.list_active_macros()
        elif cmd == exit:
            pass
        else:
            print(unrecognized_cmd)

main()