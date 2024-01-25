from .API_utils import fetch_settings, check_password, write_settings
import json
import os


def Show_settings(code, app):
    if os.path.exists("./settings.json"):
        settings = fetch_settings(code)
        json_data = json.loads(settings)

        response = app.response_class(
            response=json.dumps(json_data), status=200, mimetype='application/json')
        return response
    else:
        return "404"


def Toggle_dls(option, code):
    if (option == "" or code == ""):
        return "400"
    if check_password(code):
        if os.path.exists("./settings.json"):
            settings = fetch_settings(code)
            json_data = json.loads(settings)
            if option.upper() == "TRUE":
                json_data["EnableDownloads"] = True
            else:
                json_data["EnableDownloads"] = False
            return write_settings(json_data, code)
        return "404"
    else:
        return "401"


def Toggle_readers(option, code):
    if (option == "" or code == ""):
        return "400"
    if check_password(code):
        if os.path.exists("./settings.json"):
            settings = fetch_settings(code)
            json_data = json.loads(settings)
            if option.upper() == "TRUE":
                json_data["EnableReaders"] = True
            else:
                json_data["EnableReaders"] = False
            return write_settings(json_data, code)
        else:
            return "404"
    else:
        return "401"


def Toggle_lists(option, code):
    if (option == "" or code == ""):
        return "400"
    if check_password(code):
        if os.path.exists("./settings.json"):
            settings = fetch_settings(code)
            json_data = json.loads(settings)
            if option.upper() == "WHITELIST":
                json_data["EnableWhiteList"] = True
                json_data["EnableBlackList"] = False
            elif option.upper() == "BLACKLIST":
                json_data["EnableWhiteList"] = False
                json_data["EnableBlackList"] = True
            elif option.upper() == "NONE":
                json_data["EnableWhiteList"] = False
                json_data["EnableBlackList"] = False
            else:
                return "406"
            return write_settings(json_data, code)
        else:
            return "404"
    else:
        return "401"


def Manage_acls(address, list, option, code):
    if (address == "" or list == "" or option == "" or code == ""):
        return "400"
    status = "0"
    if check_password(code):
        if os.path.exists("./settings.json"):
            settings = fetch_settings(code)
            json_data = json.loads(settings)

            # Manage whitelist
            if list.upper() in ("WHITELIST"):
                if option.upper() == "ADD":
                    if address not in json_data["WhiteList"] and address not in json_data["BlackList"]:
                        json_data["WhiteList"].append(address)
                    else:
                        status = "409"
                elif option.upper() == "REMOVE":
                    if address in json_data["WhiteList"]:
                        json_data["WhiteList"].remove(address)
                    else:
                        status = "410"
                else:
                    status = "406"

            # Manage blacklist
            elif list.upper() in ("BLACKLIST"):
                if option.upper() == "ADD":
                    if address not in json_data["BlackList"] and address not in json_data["WhiteList"]:
                        json_data["BlackList"].append(address)
                    else:
                        status = "409"
                elif option.upper() == "REMOVE":
                    if address in json_data["BlackList"]:
                        json_data["BlackList"].remove(address)
                    else:
                        status = "410"
                else:
                    status = "406"
            else:
                status = "406"

            # Write to settings
            if status != "0":
                return status
            return write_settings(json_data, code)
        else:
            return "404"
    else:
        return "401"
