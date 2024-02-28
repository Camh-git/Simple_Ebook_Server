import json
from .API_utils import read_json_no_code, write_json_no_code
from .Book_data_methods import get_specific_book_data

# Note: These dont have much in the way of validation, since this is handled in the endpoint functions that call these ones.


def BD_delete_book(folder, book, book_data=""):
    # Load the book data, or accept the provided data
    stored_json = ""
    if book_data != "":
        stored_json = book_data
    else:
        stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    # Find and remove the book's entry
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


def BD_delete_folder(target_folder, delete_content="False", book_data="", changed_dirs=[]):
    # Load the book data, or accept the provided data
    stored_json = ""
    if book_data != "":
        stored_json = book_data
    else:
        stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    # Find and remove the folder, move books to misc if move = true
    folder_index = 0
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == target_folder:
            if str(delete_content).upper() != "TRUE":

                print("Moving books from deleted folder to Misc/ Uploads")
                for json_book in json_folder["Books"]:
                    # Determin the correct DIR
                    if json_book["Title"] in changed_dirs:
                        BD_move_book(target_folder, "Uploads",
                                     json_book["Title"], stored_json, "True")
                    else:
                        BD_move_book(target_folder, "Misc",
                                     json_book["Title"], stored_json, "True")

            del stored_json["Folders"][folder_index]
            break
        else:
            folder_index += 1

    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


def BD_rename_folder(old_folder, new_name):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == old_folder:
            json_folder["Folder_name"] = new_name

    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


def BD_create_folder(folder_name):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    new_folder = json.loads('{"Folder_name":"' + folder_name + '","Books":[]}')

    stored_json["Folders"].append(new_folder)

    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


def BD_move_book(old_folder, new_folder, book_name, provided_data="", tag="False"):
    # Load the book data, or accept the provided data
    stored_json = ""
    if provided_data != "":
        stored_json = provided_data
    else:
        stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    book_data = get_specific_book_data(old_folder, book_name)

    # Add the "MOVED" tag if requested:
    if str(tag).upper() == "TRUE":
        book_data["Title"] = str("MOVED:" + book_data["Title"])

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


# Thumb data
def BD_reassign_thumb():
    stored_json = json.loads(read_json_no_code("./Assets/Thumbnail_info.json"))
    if stored_json == "":
        return "404"
    return "501"


def BD_rename_thumb():
    return "501"


def BD_delete_thumb_cache():

    data = {"Folders": [{"Folder_name": "Uploads", "Images": []}, {
        "Folder_name": "Misc", "Images": []}]}

    print(type(data))
    print(data)
    return "200"

    status = write_json_no_code("./Assets/Thumbnail_info.json", data)
    return status


def BD_delete_thumb():
    return "501"
