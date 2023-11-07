import os
import platform

match platform.system():
    case "Windows":
        print("Running on windows")
        os.system("python main.py")
    case "Linux":
        print("Running on linux")
        # this is enough to get us to the TLD from either the normal entry point or this dir
        os.system(" cd ..; cd ..; cd ..; cd ..")
        os.system("cd var; cd www; cd html; cd Simple_Ebook_Server")
        os.system("export FLASK_APP='BookAPI.py'")
        os.system("flask run --host=0.0.0.0")
    case "Darwin":
        print("Running on mac OS")
        os.system("python main.py")
    case _:
        print("OS not recognised, please run on linux, mac or windows")

# This script should actually be implemented in something that doesn't require python, it should then:
    # install appache/python and it's modules if not installed, start the server, start appache, report port number and url for ui.

# The current startup process is to install apache & python if needed, place this folder in htdocs, run this script, go to UI URL
