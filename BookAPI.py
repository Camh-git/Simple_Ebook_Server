from flask import Flask, abort, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import json
from datetime import datetime
from Assets.Scripts.API_segments.Help_pages import help, file_support, show_site_map
from Assets.Scripts.API_segments.Folder_methods import list_folders, list_folder_content, Delete_folder, Rename_folder
from Assets.Scripts.API_segments.Book_methods import list_books, Remove_book, Rename_book, Upload_book
from Assets.Scripts.API_segments.Lib_management import Create_folder, Move_book_to_folder
from Assets.Scripts.API_segments.Management_control import Toggle_management
from Assets.Scripts.API_segments.API_utils import read_json_no_code
from Assets.Scripts.API_segments.Misc_management import Show_settings, Toggle_dls, Toggle_readers, Toggle_lists, Manage_acls
from Assets.Scripts.API_segments.Thumb_management import List_Thumbs, show_thumb_map, generate_thumbs, Reasign_thumb, Clear_thumbs, rename_thumb, delete_thumb, populate_thumb_data
from Assets.Scripts.API_segments.Book_data_methods import generate_book_data, edit_book_data


app = Flask(__name__)
mainDir = "./Books"
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "./Books/Uploads"

print("started at: " + str(datetime.now()))


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

    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":  # The actual request following the preflight
        response = ""
        if "/post-book" in request.path:
            response = Upload_book(
                request, generate_thumbs, populate_thumb_data)
        return _corsify_actual_response(jsonify(response))


def _build_cors_preflight_response():
    # from: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# Book methods

@app.route("/list-books")
def list_books_endpoint():
    return list_books(mainDir)


# note: not technically needed since this passes through the cors stuff
@app.route("/post-book/<book>", methods=["GET", "POST"])
def Upload_book_endpoint():
    return Upload_book(request, generate_thumbs, populate_thumb_data)


@app.route("/delete-book/<book_name>&&<ext>&&<folder>", methods=["GET"])
@cross_origin()
def Remove_book_endpoint(book_name, ext, folder):
    return Remove_book(book_name, ext, folder, mainDir)


@app.route("/rename-book/<book_name>&&<ext>&&<folder>&&<new_name>")
def Rename_book_endpoint(book_name, ext, folder, new_name):
    return Rename_book(book_name, ext, folder, new_name, mainDir)


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
def Create_folder_endpoint(folder_name):
    return Create_folder(folder_name, mainDir)


@app.route("/move-book-to-folder/<book_name>&&<ext>&&<old_folder_name>&&<new_folder_name>", methods=["GET"])
def Move_book_to_folder_endpoint(book_name, ext, old_folder_name, new_folder_name):
    return Move_book_to_folder(book_name, ext, old_folder_name,
                               new_folder_name, mainDir)

# Thumbnail management functions


@app.route("/list-thumbs")
def List_Thumbs_endpoint():
    return List_Thumbs()


@app.route("/thumb-map")
def show_thumb_map_endpoint():
    return show_thumb_map()


@app.route("/generate-thumbs")
@app.route("/generate-thumbnails")
@app.route("/gen-thumbs")
def generate_thumbs_endpoint():
    return generate_thumbs()


@app.route("/reassign-thumb/<folder_name>&&<book_name>&&<thumb_folder>&&<thumb>")
def Reasign_thumb_endpoint(folder_name, book_name, thumb_folder, thumb):
    return Reasign_thumb(folder_name, book_name, thumb_folder, thumb)


@app.route("/upload-thumb/<image>")
def Upload_thumb(image):
    return 501


@app.route("/clear-thumbs/<regen>&&<rmManual>")
def Clear_thumbs_endpoint(regen, rmManual):
    return Clear_thumbs(regen, rmManual)


@app.route("/rename-thumb/<folder>&&<target>&&<new_name>")
def rename_thumb_endpoint(folder, target, new_name):
    return rename_thumb(folder, target, new_name)


@app.route("/delete-thumb/<folder>&&<target>")
def delete_thumb_endpoint(folder, target):
    return delete_thumb(folder, target)

# Misc option functions
# TODO: implement the password check


@app.route("/fetch-settings/<code>")
def Show_settings_endpoint(code):
    return Show_settings(code, app)


@app.route("/toggle-dl/<option>&&<code>")
def Toggle_dls_endpoint(option, code):
    return Toggle_dls(option, code)


@app.route("/toggle-readers/<option>&&<code>")
def Toggle_readers_endpoint(option, code):
    return Toggle_readers(option, code)


@app.route("/toggle-lists/<option>&&<code>")
def Toggle_lists_endpoint(option, code):
    return Toggle_lists(option, code)


@app.route("/manage-acls/<address>&&<list>&&<option>&&<code>")
def Manage_acls_endpoint(address, list, option, code):
    return Manage_acls(address, list, option, code)


@app.route("/toggle-management/<option>&&<function>&&<code>")
def Toggle_management_endpoint(option, function, code):
    return Toggle_management(option, function, code)


# Help options

@app.route("/help")
@app.route("/api-help")
def help_endpoint():
    return help()


@app.route("/file_support")
@app.route("/file-support")
def file_support_endpoint():
    return file_support()


@app.route("/map")
@app.route("/map/<format>")
def show_site_map_endpoint(format="XML"):
    return show_site_map(format)


# Data methods


@app.route("/gen-book-data")
def generate_book_data_endpoint():
    return generate_book_data(mainDir)


@app.route("/gen-thumb-data")
def generate_thumb_data_endpoint():
    return populate_thumb_data()


@app.route("/edit-book-data/<folder>&&<book>&&<authors>&&<date>&&<publisher>&&<isbn>&&<isbn13>&&<thumbnail>&&<extension>&&<validated>")
def edit_book_data_endpoint(folder, book, authors, date, publisher, isbn, isbn13, thumbnail, extension, validated):
    return edit_book_data(folder, book, authors, date, publisher, isbn, isbn13, thumbnail, extension, validated)


@app.route("/get-book-data")
def show_book_data():
    return read_json_no_code("./Assets/Book_info.json")


@app.route("/get-thumb-data")
@app.route("/get-thumbnail-data")
def show_thumb_data():
    return read_json_no_code("./Assets/Thumbnail_info.json")


@app.route("/get-book-and-thumb-data")
def show_book_and_thumb_data():
    book_info = "{" + read_json_no_code("./Assets/Book_info.json")
    thumb_info = "{" + read_json_no_code("./Assets/Thumbnail_info.json") + "}"
    data = '{{"Books": {0}, "Thumbs": {1}}}'.format(book_info, thumb_info)

    data = str(data.replace("{{", "{").replace("}}", "}"))
    return data


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def Catch_all(path):
    return "Invalid path: " + path, 400


if __name__ == "__main__":
    app.run(debug=True)

# To launch on raspberry pi os: cd into this dir, export FLASK_APP="BookAPI.py" , flask run --host=0.0.0.0
