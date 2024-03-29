import json
from .API_utils import read_json_no_code, write_json_no_code, search_google_books
from .Book_data_methods import get_specific_book_data
import os
# Note: These dont have much in the way of validation, since this is handled in the endpoint functions that call these ones.


def BD_upload_book(book):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    book_data = ""
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == "Uploads":
            book_data = json.loads(search_google_books(book))
            json_folder["Books"].append(book_data)

    status = write_json_no_code(
        "./Assets/Book_info.json", stored_json)
    return status


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

# Folder data


def BD_upload_folder(folder_name, book_list):
    # Create the folder, then copy in the book data
    BD_create_folder(folder_name)
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder_name:
            for book in book_list:
                book_data = json.loads(search_google_books(book))
                json_folder["Books"].append(book_data)

    status = write_json_no_code("./Assets/Book_info.json", stored_json)
    return status


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
def BD_upload_thumb(Thumb_title):
    stored_json = json.loads(read_json_no_code("./Assets/Thumbnail_info.json"))
    if stored_json == "":
        return "404"

    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == "Uploads":
            json_folder["Images"].append(Thumb_title)

    status = write_json_no_code(
        "./Assets/Thumbnail_info.json", stored_json)
    return status


def BD_create_thumb_folder(folder_name):
    stored_json = json.loads(read_json_no_code("./Assets/Thumbnail_info.json"))
    if stored_json == "":
        return "404"
    new_folder = json.loads(
        '{"Folder_name":"' + folder_name + '","Images":[]}')

    stored_json["Folders"].append(new_folder)

    status = write_json_no_code("./Assets/Thumbnail_info.json", stored_json)
    return status


def BD_reassign_thumb(thumb_folder, thumb, book_folder, book):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    target = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(
        thumb_folder, thumb)

    if os.path.exists(target):
        # find the book
        for json_folder in stored_json["Folders"]:
            if json_folder["Folder_name"] == book_folder:
                for json_book in json_folder["Books"]:
                    if json_book["Title"] == book:
                        json_book["Thumbnail"] = target

        status = write_json_no_code("./Assets/Book_info.json", stored_json)
        return status
    else:
        return "404"


def BD_rename_thumb(folder, current_name, new_name):
    # Step 1 - rename the thumb
    stored_json = json.loads(read_json_no_code("./Assets/Thumbnail_info.json"))
    if stored_json == "":
        return "404"

    # find the thumb and update it
    found_thumb = False
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for image in json_folder["Images"]:
                if image == current_name:
                    json_folder["Images"][json_folder["Images"].index(
                        image)] = new_name
                    found_thumb = True

    if found_thumb:
        status = write_json_no_code(
            "./Assets/Thumbnail_info.json", stored_json)
        if status == "200":
            status = BD_rename_thumb_refrences(folder, current_name, new_name)
            return status
        else:
            return status
    else:
        return "404"


def BD_rename_thumb_refrences(folder, old_name, new_name):
    # Step 2 - Update book data to update any book with a renamed thumbnail
    stored_json = json.loads(
        read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    old_path = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(
        folder, old_name)
    new_path = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(
        folder, new_name)

    changedData = False
    for json_folder in stored_json["Folders"]:
        for json_book in json_folder["Books"]:
            if json_book["Thumbnail"] == old_path:
                json_book["Thumbnail"] = new_path
                changedData = True
    if changedData:
        status = write_json_no_code(
            "./Assets/Book_info.json", stored_json)
        return status
    else:
        return "200"


def BD_delete_thumb_cache():

    data = {"Folders": [{"Folder_name": "Uploads", "Images": []}, {
        "Folder_name": "Misc", "Images": []}]}

    return "200"
    status = write_json_no_code("./Assets/Thumbnail_info.json", data)
    return status


def BD_delete_thumb(folder, thumb):
    # Step 1 - Remove the thumbnail from thumbnail info
    stored_json = json.loads(read_json_no_code("./Assets/Thumbnail_info.json"))
    if stored_json == "":
        return "404"

    # Find and remove the thumb
    found_thumb = False
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for image in json_folder["Images"]:
                if "./Assets/Images/Thumbnail_cache/{0}/{1}".format(folder, image) == thumb:
                    json_folder["Images"].remove(image)
                    found_thumb = True

    if found_thumb:
        status = write_json_no_code(
            "./Assets/Thumbnail_info.json", stored_json)
        if status == "200":
            status = BD_delete_thumb_refrences(thumb)
            return status
        else:
            return status
    else:
        return "404"


def BD_delete_thumb_refrences(name):
    # Step 2 - Set any books with the given thumbnail to "NA"
    stored_json = json.loads(
        read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    changedData = False
    for json_folder in stored_json["Folders"]:
        for json_book in json_folder["Books"]:
            if json_book["Thumbnail"] == name:
                json_book["Thumbnail"] = "NA"
                changedData = True

    if changedData:
        status = write_json_no_code(
            "./Assets/Book_info.json", stored_json)
        return status
    else:
        return "200"
