from flask import Flask, abort, request
from flask_cors import CORS, cross_origin
import os
import shutil
import json

app = Flask(__name__)
mainDir = "./Books"
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def welcome():
    return "Hello from basic ebook server"


@app.before_request
def check_ACLS():
    json_data = read_json_no_code("settings.json")
    settings = json.loads(json_data)

    # Check if the caller meets ACL requirements
    if settings["EnableWhiteList"] == True:
        if request.remote_addr not in settings["WhiteList"]:
            return "401"
    elif settings["EnableBlackList"] == True:
        if request.remote_addr in settings["BlackList"]:
            return "401"

    # Check that the requested endpoint is enabled
    if settings["EnableManagement"] != True:
        # Allow the request through if it's heading to one of the non-management endpoings
        if not request.path == "/list-books" and not request.path == "/list-folders" and not request.path == "/list-thumbs" and not "/fetch-settings" in request.path and not "/toggle-management" in request.path:
            return "423"

    if settings["EnableUpload"] != True:
        if "/post-book" in request.path or "/post-folder" in request.path or "/upload-thumb" in request.path:
            return "423"

    if settings["EnableRename"] != True:
        if "/rename-book" in request.path or "/rename-folder" in request.path:
            return "423"

    if settings["EnableReAssign"] != True:
        if "/move-book-to-folder" in request.path or "/reassign-thumb" in request.path:
            return "423"

    if settings["EnableDelete"] != True:
        if "/delete-book" in request.path or "/delete-folder" in request.path or "/clear-thumbs" in request.path:
            return "423"


# Book methods

@app.route("/list-books")
def list_books():
    list = ''
    for folder in os.listdir(mainDir):
        list += '<div class = "Book_folder"><h5 class="book_list_title">{0}</h5><ul>'.format(
            folder)
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            list += '<li>{0}</li>'.format(book)
        list += '</ul></div>'
    response = app.response_class(response=json.dumps(
        list), status=200, mimetype='application/json')
    return response


@app.route("/json-list-books")
def json_list_books():
    data = '{"Books":['
    for folder in os.listdir(mainDir):
        data += '{"Folder":"'+folder + '","Content":['
        emptyDir = True
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            emptyDir = False
            components = os.path.splitext(book)
            data += '{"Name":"' + components[0] + \
                '","ext":"' + components[1]+'"},'
        if not emptyDir:
            data = data[:-1]
        data += "]},"
    data = data[:-1]
    data += ']}'
    return data


@app.route("/post-book/<book_name>", methods=["POST"])
def Upload_book(book_name):
    return 501


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {
            'pdf', 'txt', 'epub', 'mobi', 'azw3'}


@app.route("/delete-book/<book_name>&&<ext>&&<folder>", methods=["GET"])
@cross_origin()
def Remove_book(book_name, ext, folder):
    if (book_name == "" or ext == "" or folder == ""):
        return "400"
    target = "{0}/{1}/{2}.{3}".format(mainDir, folder, book_name, ext)
    if os.path.exists(target):
        try:
            os.remove(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


@app.route("/rename-book/<book_name>&&<ext>&&<folder>&&<new_name>")
def Rename_book(book_name, ext, folder, new_name):
    if (book_name == "" or ext == "" or folder == "" or new_name == ""):
        return "400"
    # Make sure the book exists and that a file with a matching name doesn't already exist
    target = "{0}/{1}/{2}.{3}".format(mainDir, folder, book_name, ext)
    if os.path.exists("{0}/{1}/{2}.{3}".format(mainDir, folder, new_name, ext)):
        return "409"
    if os.path.exists(target):
        try:
            os.rename(
                target, "{0}/{1}/{2}.{3}".format(mainDir, folder, new_name, ext))
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


# Folder methods

@app.route("/list-folders", methods=["GET"])
def list_folders():
    response = ""
    for folder in os.listdir(mainDir):
        response += "->" + folder
    return response


@app.route("/list-folder-content/<folder_name>")
def list_folder_content(folder_name):
    response = ""
    for book in os.listdir("{0}/{1}".format(mainDir, folder_name)):
        response += ">>" + book
    return response


@app.route("/post-folder/<folder_name>&&<content>", methods=["POST"])
def Upload_folder(folder_name, contents):
    return 501


@app.route("/delete-folder/<folder_name>&&<delete_content>")
def Delete_folder(folder_name, delete_content):
    if (folder_name == "" or delete_content == ""):
        return "400"
    if (folder_name.upper() == "MISC" or folder_name.upper() == "UPLOADS"):
        return "403"

    target = "{0}/{1}".format(mainDir, folder_name)
    notifyChange = False
    if os.path.exists(target):
        try:
            if delete_content.upper() != "TRUE":
                # If we are saving the books go through each and move them to misc folder,
                # add a "MOVED:" prefix if misc already contains a book of the same name
                for book in os.listdir(target):
                    start = "{0}/{1}".format(target, book)
                    destination = "{0}/Misc/{1}".format(mainDir, book)

                    if os.path.exists(destination):
                        os.rename(
                            start, "{0}/Misc/MOVED:{1}".format(mainDir, book))
                        notifyChange = True
                    else:
                        os.rename(start, destination)

            shutil.rmtree(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    if (notifyChange):
        return "428"
    return "200"


@app.route("/rename-folder/<folder_name>&&<new_name>", methods=["GET"])
def Rename_folder(folder_name, new_name):
    if (folder_name == "" or new_name == ""):
        return "400"
    if (folder_name.upper() == "MISC" or folder_name.upper() == "UPLOADS"):
        return "403"

    # Make sure the folder exists, and stop if a folder with the new name already exists
    target = "{0}/{1}".format(mainDir, folder_name)
    if os.path.exists("{0}/{1}".format(mainDir, new_name)):
        return "409"
    if os.path.exists(target):
        try:
            os.rename(target, "{0}/{1}".format(mainDir, new_name))
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


# Library management functions

@app.route("/create-folder/<folder_name>", methods=["GET"])
def Create_folder(folder_name):
    if (folder_name == ""):
        return "400"
    target = "{0}/{1}".format(mainDir, folder_name)
    if not os.path.exists(target):
        try:
            os.makedirs(target)
            return "200"
        except Exception as e:
            return "500: " + str(e)
    else:
        return "409"


@app.route("/move-book-to-folder/<book_name>&&<ext>&&<old_folder_name>&&<new_folder_name>", methods=["GET"])
# example: http://192.168.1.110:5000/move-book-to-folder/MoveTest&&pdf&&TestFolder&&Misc
def Move_book_to_folder(book_name, ext, old_folder_name, new_folder_name, ):
    if (book_name == "" or ext == "" or old_folder_name == "" or new_folder_name == ""):
        return "400"
    oldPath = "{0}/{1}/{2}.{3}".format(mainDir,
                                       old_folder_name, book_name, ext)
    newPath = "{0}/{1}/{2}.{3}".format(mainDir,
                                       new_folder_name, book_name, ext)
    if os.path.exists(oldPath):
        if not os.path.exists(newPath):
            try:
                os.rename(oldPath, newPath)
            except Exception as e:
                return "500: " + str(e)
        else:
            return "409"
    else:
        return "404"
    return "200"

# Thumbnail management functions


@app.route("/list-thumbs")
def List_Thumbs():
    list = '<ul id = "Thumb_list">'
    for image in os.listdir("./Assets/Images/Thumbnail_cache/"):
        list += '<li>{0}</li>'.format(image)
    list += '</ul>'
    response = app.response_class(response=json.dumps(
        list), status=200, mimetype='application/json')
    return response


@app.route("/list-thumbs-json")
def List_Thumbs_json():
    list = '{"Images":['
    empty_cache = True
    for image in os.listdir("./Assets/Images/Thumbnail_cache/"):
        empty_cache = False
        components = os.path.splitext(image)
        list += '{"Name":"' + components[0] + '","ext":"'+components[1]+'" },'
    if not empty_cache:
        list = list[:-1]
    list += "]}"
    return list


@app.route("/thumb-map")
def show_thumb_map():
    data = read_json_no_code("./Assets/Images/Thumbnail_map.json")
    data = data[:-2]
    data += "," + List_Thumbs_json()[1:]
    return data


def generate_thumbs():
    return "501"


@app.route("/reassign-thumb/<folder_name>&&<book_name>&&<thumb>")
def Reasign_thumb(folder_name, book_name, thumb):
    if os.path.exists("./Assets/Images/Thumbnail_map.json"):
        json_data = read_json_no_code("./Assets/Images/Thumbnail_map.json")
        map = json.loads(json_data)

        # Manipulate the map
        bookFound = False
        for book in map["Books"]:
            if book["Folder"] == folder_name and book["Name"] == book_name:
                bookFound = True
                book.update({"Thumb": thumb.replace(" ", "")})
        if not bookFound:
            # Add the book to the map if it doesn't already have an entry
            map["Books"].append(
                {"Folder": folder_name, "Name": book_name, "Thumb": thumb.replace(" ", "")})

        # return str(map["Books"][0]["Name"] in os.listdir("./Books/"+map["Books"][0]["Folder"]))
        return write_json_no_code("./Assets/Images/Thumbnail_map.json", map)

    else:
        return "404"


@app.route("/upload-thumb/<image>")
def Upload_thumb(image):
    return 501


@app.route("/clear-thumbs/<regen>&&<rmManual>")
def Clear_thumbs(regen, rmManual):
    path = "./Assets/Images/Thumbnail_cache/"

    if os.path.exists(path):
        # Clear the existing cache, execept for manual uploads (unless instructed)
        if (rmManual == "true"):
            for file in os.listdir(path):
                os.remove(path+file)
        else:
            for file in os.listdir(path):
                if not file.startswith("MAN-"):
                    os.remove(path+file)

        if (regen == "true"):
            try:
                generate_thumbs()
            except Exception as e:
                return "500"

        return "200"
    else:
        return "404"


# Misc option functions
# TODO: implement the password check, opt: make settings json handlers not file specific


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


def check_password(password):
    return True


@app.route("/fetch-settings/<code>")
def Show_settings(code):
    if os.path.exists("./settings.json"):
        settings = fetch_settings(code)
        json_data = json.loads(settings)

        response = app.response_class(
            response=json.dumps(json_data), status=200, mimetype='application/json')
        return response
    else:
        return "404"


@app.route("/toggle-dl/<option>&&<code>")
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


@app.route("/toggle-readers/<option>&&<code>")
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


@app.route("/toggle-lists/<option>&&<code>")
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

# http://127.0.0.1:5000/lists?address=1.1.1.1&list=whitelist&option=add


@app.route("/manage-acls/<address>&&<list>&&<option>&&<code>")
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


# Management control options

@app.route("/toggle-management/<option>&&<function>&&<code>")
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def Catch_all(path):
    return "Invalid path: " + path, 400


if __name__ == "__main__":
    app.run(debug=True)

# To launch on raspberry pi os: cd into this dir, export FLASK_APP="BookAPI.py" , flask run --host=0.0.0.0
