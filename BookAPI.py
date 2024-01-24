from flask import Flask, abort, request
from flask_cors import CORS, cross_origin
import os
import shutil
import json
from urllib.request import urlopen
from Assets.Scripts.API_segments.Help_pages import help, file_support, show_site_map
from Assets.Scripts.API_segments.Folder_methods import list_folders, list_folder_content, Delete_folder, Rename_folder

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
    if (request.remote_addr[:8] != "192.168."):
        return "421"
    if settings["EnableWhiteList"] == True:
        if request.remote_addr not in settings["WhiteList"]:
            return "401"
    elif settings["EnableBlackList"] == True:
        if request.remote_addr in settings["BlackList"]:
            return "401"
    # print(request.remote_addr[:8])

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
    renamed = "{0}/{1}/{2}.{3}".format(mainDir, folder, new_name, ext)
    if os.path.exists(renamed):
        return "409"
    if os.path.exists(target):
        try:
            os.rename(
                target, renamed)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


# Folder methods

@app.route("/list-folders", methods=["GET"])
def list_folders_endpoint():
    return list_folders(mainDir)


@app.route("/list-folder-content/<folder_name>")
def list_folder_content_endpoint(folder_name):
    return list_folder_content(folder_name, mainDir)


@app.route("/post-folder/<folder_name>&&<content>", methods=["POST"])
def Upload_folder(folder_name, contents):
    return 501


@app.route("/delete-folder/<folder_name>&&<delete_content>")
def Delete_folder_endpoint(folder_name, delete_content):
    return Delete_folder(folder_name, delete_content, mainDir)


@app.route("/rename-folder/<folder_name>&&<new_name>", methods=["GET"])
def Rename_folder_endpoint(folder_name, new_name):
    return Rename_folder(folder_name, new_name, mainDir)


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
    data += "," + List_Thumbs()[1:]
    return data


@app.route("/generate-thumbs")
def generate_thumbs():
    # set up book info json, with map for titles to isbns/authors/dates ect, have a seperate system to auto pop that(maybe do on upload)
    # scan books for isbns, if found use those, if not use names for search, check either against returned title, reject and use placeholder if bad
    # then search by isbn, dl img and set thumb map accordingly
    # search by name, only include those with a reasonable number of spaces
    with urlopen('https://www.googleapis.com/books/v1/volumes?q=title=Devestationofbaal'.format()) as r:
        text = r.read()
        data = json.loads(text)
        title = data["items"][0]["volumeInfo"]["title"]
        authors = data["items"][0]["volumeInfo"]["authors"]
        date = data["items"][0]["volumeInfo"]["publishedDate"]
        publisher = data["items"][0]["volumeInfo"]["publisher"]
        isbn = isbn10 = data["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
        isbn13 = data["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"]
        thumbnail = data["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"]
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


@app.route("/rename-thumb/<target>&&<new_name>")
def rename_thumb(target, new_name):
    if (target == "" or new_name == ""):
        return "400"
    extension = os.path.splitext(target)[1]
    # Make sure the book exists and that a file with a matching name doesn't already exist
    image = "./Assets/Images/Thumbnail_cache/{0}".format(target)
    reNamed = "./Assets/Images/Thumbnail_cache/{0}{1}".format(
        new_name, extension)
    if os.path.exists(reNamed):
        return "409"

    if os.path.exists(image):
        try:
            os.rename(
                image, reNamed)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


@app.route("/delete-thumb/<target>")
def delete_thumb(target):
    if (target == ""):
        return "400"
    target = "./Assets/Images/Thumbnail_cache/{0}".format(target)
    if (os.path.exists(target)):
        try:
            os.remove(target)
        except Exception as e:
            return "500" + str(e)
    else:
        return "404"
    return "200"

# Misc option functions
# TODO: implement the password check


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


@app.route("/help")
def help_endpoint():
    return help()


@app.route("/file_support")
def file_support_endpoint():
    return file_support()


@app.route("/map")
@app.route("/map/<format>")
def show_site_map_endpoint(format="XML"):
    return show_site_map(format)


def check_book_for_data(stored_json, book, folder):
    book_data = ""
    for jsonFolder in stored_json["Folders"]:
        if folder in jsonFolder["Title"]:
            for jsonBook in jsonFolder["Books"]:
                if book in jsonBook["Title"]:
                    if jsonBook["isbn"].upper() != "NA" and jsonBook["isbn"] != "" and jsonBook["Thumbnail"] != "NA" and jsonBook["Thumbnail"] != "":
                        book_data = jsonBook
                        return True, book_data
    return False, "NA"


@app.route("/gen-book-data")
def generate_book_data():
    stored_data = read_json_no_code("./Assets/Book_info.json")
    stored_json = json.loads(stored_data)

    lib_data = "{\"Folders\": ["
    for folder in os.listdir(mainDir):
        folder_data = '{{"Title":"{0}","Books":['.format(folder)
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):

            # Check if we already have info on this book and skip it if so
            if os.path.splitext(book)[0] in stored_data:
                have_data, data = check_book_for_data(
                    stored_json, os.path.splitext(book)[0], folder)
                if have_data:
                    # print("already had: " + book + " with data")
                    folder_data += str(data).replace("'",
                                                     "\"").replace("'", "\"").replace("'", "\"") + ","
                    continue

            # Get book info and parse the result
            # 'https://www.googleapis.com/books/v1/volumes?q=isbn:{0}'.format(ISBN)  #ISBN approach
            try:
                with urlopen('https://www.googleapis.com/books/v1/volumes?q=title={0}'.format(
                        book)) as r:
                    text = r.read()
                    data = json.loads(text)
                    title = authors = date = publisher = isbn10 = isbn13 = thumbnail = authorlist = ""
                    try:
                        title = data["items"][0]["volumeInfo"]["title"]
                    except:
                        title = ""
                    try:
                        authors = data["items"][0]["volumeInfo"]["authors"]
                    except:
                        authors = ""
                    try:
                        date = data["items"][0]["volumeInfo"]["publishedDate"]
                    except:
                        date = ""
                    try:
                        publisher = data["items"][0]["volumeInfo"]["publisher"]
                    except:
                        publisher = ""
                    try:
                        isbn10 = data["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                    except:
                        isbn10 = ""
                    try:
                        isbn13 = data["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"]
                    except:
                        isbn13 = ""
                    try:
                        thumbnail = data["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"]
                    except:
                        thumbnail = ""

                    for author in authors:
                        authorlist += '"{0}",'.format(author)
                    authorlist = authorlist[:-1]

                    book_data = '{{"Title":"{0}","Authors":[{1}],"Date":"{2}","Publisher":"{3}","isbn":"{4}","isbn13":"{5}","Thumbnail":"{6}"}},'.format(title, authorlist, date, publisher, isbn10, isbn13, thumbnail
                                                                                                                                                         )
                    folder_data += book_data

            except:
                book_data = '{{"title":"{0}","Authors":["NA"],"Date":"NA","Publisher":"NA","isbn":"NA","isbn13":"NA","Thumbnail":"NA"}},'.format(
                    book)
                folder_data += book_data

        # Format the folder data and add it to the library
        if folder_data[len(folder_data)-1] != "[":
            folder_data = folder_data[:-1]
        folder_data += "]},"
        lib_data += folder_data

    lib_data = lib_data[:-1]
    lib_data += "]}"
    # Convert the libdata to json and save
    lib_data = lib_data.replace("/", "").replace("\\", "")
    # json_Data = json.dumps(lib_data)
    # write_json_no_code("./Assets/Book_info.json", lib_data)
    return lib_data


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def Catch_all(path):
    return "Invalid path: " + path, 400


if __name__ == "__main__":
    app.run(debug=True)

# To launch on raspberry pi os: cd into this dir, export FLASK_APP="BookAPI.py" , flask run --host=0.0.0.0
