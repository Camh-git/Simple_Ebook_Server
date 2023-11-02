from flask import Flask, request, jsonify
import os
import shutil
import json

app = Flask(__name__)
mainDir = "./Books"


@app.route("/")
def welcome():
    return "Hello from basic ebook server"

# TODO: modify methods to handle not having optional values

# Book methods


@app.route("/list-books")
def list_books():
    response = ""
    for folder in os.listdir(mainDir):
        response += "->" + folder
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            response += ">>" + book
    return response


@app.route("/post-book/<book_name>", methods=["POST"])
def Upload_book(book_name):
    return 501


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {
            'pdf', 'txt', 'epub', 'mobi', 'azw3'}


@app.route("/delete-book/<book_name>&&<ext>&&<folder>", methods=["GET"])
def Remove_book(book_name, ext, folder):
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
    target = "{0}/{1}/{2}.{3}".format(mainDir, folder, book_name, ext)
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
    target = "{0}/{1}".format(mainDir, folder_name)
    if os.path.exists(target):
        try:
            if (delete_content.upper() != "TRUE"):
                # If we are saving the books go through each and move them to misc folder,
                # add a "MOVED:" prefix if misc already contains a book of the same name
                for book in os.listdir(target):
                    start = "{0}/{1}".format(target, book)
                    destination = "{0}/Misc/{1}".format(mainDir, book)

                    if os.path.exists(destination):
                        os.rename(
                            start, "{0}/Misc/MOVED:{1}".format(mainDir, book))
                    else:
                        os.rename(start, destination)

            shutil.rmtree(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


@app.route("/rename-folder/<folder_name>&&<new_name>", methods=["GET"])
def Rename_folder(folder_name, new_name):
    target = "{0}/{1}".format(mainDir, folder_name)
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
    target = "{0}/{1}".format(mainDir, folder_name)
    if not os.path.exists(target):
        try:
            os.makedirs(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "409"
    return "200"


@app.route("/move-book-to-folder/<book_name>&&<ext>&&<old_folder_name>&&<new_folder_name>", methods=["GET"])
# example: http://192.168.1.110:5000/move-book-to-folder/MoveTest&&pdf&&TestFolder&&Misc
def Move_book_to_folder(book_name, ext, old_folder_name, new_folder_name, ):
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


@app.route("/reassign-thumb/<folder_name>&&<book_name>&&<thumb>", methods=["PUT"])
def Reasign_thumb(folder_name, book_name, thumb):
    return 501


@app.route("/clear-thumbs/<option>", methods=["PUT"])
def Clear_thumbs(option):
    return 501

# Misc option functions
# TODO: add password authentication to these endpoints


def fetch_settings():
    with open("settings.json", "r") as json_file:
        data = json_file.read()
        return data


def check_password():
    return True


@app.route("/toggle-dl/<option>&&<code>")
def Toggle_dls(option, code):
    if (check_password()):
        if os.path.exists("./settings.json"):
            settings = fetch_settings()
            json_data = json.loads(settings)
            if (option.upper() == "TRUE"):
                json_data["EnableDownloads"] = True
            else:
                json_data["EnableDownloads"] = False
            return "Settings:" + str(json_data)
        return "404"
    else:
        return "401"


@app.route("/toggle-readers/<option>&&<code>")
def Toggle_readers(option, code):
    if (check_password()):
        if os.path.exists("./settings.json"):
            settings = fetch_settings()
            json_data = json.loads(settings)
            if (option.upper() == "TRUE"):
                json_data["EnableReaders"] = True
            else:
                json_data["EnableReaders"] = False
            return "Settings:" + str(json_data)
        else:
            return "404"
    else:
        return "401"


@app.route("/toggle-lists/<option>")
def Toggle_lists(option):
    if (check_password()):
        if os.path.exists("./settings.json"):
            settings = fetch_settings()
            json_data = json.loads(settings)
            if (option.upper() == "WHITELIST"):
                json_data["EnableWhiteList"] = True
                json_data["EnableBlackList"] = False
            elif (option.upper() == "BLACKLIST"):
                json_data["EnableWhiteList"] = False
                json_data["EnableBlackList"] = True
            elif (option.upper() == "NONE"):
                json_data["EnableWhiteList"] = False
                json_data["EnableBlackList"] = False
            else:
                return "406"
            return "Settings:" + str(json_data)
        else:
            return "404"
    else:
        return "401"
# http://127.0.0.1:5000/lists?address=1.1.1.1&list=whitelist&option=add


@app.route("/lists/<address>&&<list>&&<option>", methods=["PUT"])
def Manage_ip_list(address, list, option):
    # TODO: double check this since it was written a while ago and the design has changed since

    # Get data from the right list
    data = ""
    if list.upper() == "WHITELIST":
        with open("Assets/Whitelist.txt", "r") as file:
            data = file.read()

    elif list.upper() == "BLACKLIST":
        with open("Assets/Blacklist.txt", "r") as file:
            data = file.read()
    else:
        return "Bad list option: " + list

    # If adding and adress check it exists then add if not, or remove if selected
    if (option.upper == "ADD"):
        if address not in data:
            data += ("\n" + str(address))
    elif (option.upper == "REMOVE"):
        data = data.replace(address, "")
    else:
        return "Bad whitelist action: " + option

    # Write the newly changed data to the correct file
    if list.upper() == "WHITELIST":
        with open("Assets/Whitelist.txt", "w") as file:
            file.write(data)
    elif list.upper() == "BLACKLIST":
        with open("Assets/Blacklist.txt", "w") as file:
            file.write(data)
    else:
        return "Bad list option: " + list

    return 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def Catch_all(path):
    return "Invalid path: " + path, 400


if __name__ == "__main__":
    app.run(debug=True)

# To launch on raspberry pi os: cd into this dir, export FLASK_APP="BookAPI.py" , flask run --host=0.0.0.0
