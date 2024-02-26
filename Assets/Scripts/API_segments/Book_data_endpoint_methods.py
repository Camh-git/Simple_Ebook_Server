import json
from .API_utils import read_json_no_code, write_json_no_code
from .Book_data_methods import get_specific_book_data


def BD_delete_book(folder, book, book_data=""):
    stored_json = ""
    if book_data != "":
        stored_json = book_data
    else:
        stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            bookIndex = 0
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book:
                    del json_folder["Books"][bookIndex]
                else:
                    bookIndex += 1
    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


def BD_rename_book():
    # Implemented in edit_book_data, since it was simpler
    return "501"


def BD_delete_folder():
    return "501"


def BD_rename_folder():
    return "501"


def BD_create_folder():
    return "501"


def BD_move_book(old_folder, new_folder, book_name):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    book_data = get_specific_book_data(old_folder, book_name)

    # Copy the book data into the new folder
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == new_folder:
            if len(json_folder["Books"]) > 0:
                json_folder["Books"].append(book_data)
            else:
                json_folder["Books"].append(book_data)
    BD_delete_book(old_folder, book_name, stored_json)

    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


def BD_reassign_thumb():
    return "501"


def BD_rename_thumb():
    return "501"


def BD_delete_thumb_cache():
    return "501"


def BD_delete_thumb():
    return "501"
