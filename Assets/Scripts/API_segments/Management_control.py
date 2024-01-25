from .API_utils import check_password, fetch_settings, write_settings
import json


def Toggle_management(option, function, code):
    if (option == "" or code == ""):
        return "400"
    # Check if the function is valid, and select the correct json option to change
    setting = ""
    if not (function.upper() == "MANAGEMENT" or function.upper() == "UPLOAD" or function.upper() == "DELETE" or function.upper() == "RENAME" or function.upper() == "MOVE"):
        return "406"
    elif function.upper() == "MANAGEMENT":
        setting = "EnableManagement"
    elif function.upper() == "UPLOAD":
        setting = "EnableUpload"
    elif function.upper() == "DELETE":
        setting = "EnableDelete"
    elif function.upper() == "RENAME":
        setting = "EnableRename"
    elif function.upper() == "MOVE":
        setting = "EnableReAssign"

    if check_password(code):
        settings = fetch_settings(code)
        json_data = json.loads(settings)

        if option.upper() == "TRUE":
            json_data[setting] = True
        elif option.upper() == "FALSE":
            json_data[setting] = False
        else:
            return "406"

        return write_settings(json_data, code)
    else:
        return "401"
