import json

# TODO: implement the password check


def check_password(password):
    return True


def fetch_settings(password):
    if check_password(password):
        try:
            with open("settings.json", "r") as json_file:
                data = json_file.read()
                return data
        except Exception as e:
            return "500: " + str(e)
    else:
        return "401"


def write_settings(data, password):
    if check_password(password):
        try:
            with open("settings.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
                return "200"
        except Exception as e:
            return "500: " + str(e)
    else:
        return "401"


def read_json_no_code(file):
    try:
        with open(file, "r") as json_file:
            data = json_file.read()
            return data
    except Exception as e:
        return "500: " + str(e)


def write_json_no_code(file, data):
    try:
        with open(file, "w") as json_file:
            json.dump(data, json_file, indent=4)
            return "200"
    except Exception as e:
        return "500: " + str(e)


def write_file_no_code(file, data):
    try:
        with open(file, "w") as target_file:
            target_file.write(data)
            return "200"
    except Exception as e:
        return "500: " + str(e)


def format_for_json(input):
    return input.replace("/", "").replace("\\", "").replace("'", "").replace(",", "").replace("\"", "").replace("'", "\"").replace("'", "\"")
