from .API_utils import read_json_no_code, write_json_no_code, write_file_no_code
from urllib.request import urlopen, urlretrieve
import os
import json
import shutil
import requests


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


def show_thumb_map():
    data = read_json_no_code("./Assets/Images/Thumbnail_map.json")
    data = data[:-2]
    data += "," + List_Thumbs()[1:]
    return data


def generate_thumbs():
    book_data = json.loads(read_json_no_code("./Assets/Book_info.json"))
    book_data_changed = False
    error_list = "Complete with the following errors:\n"

    for json_folder in book_data["Folders"]:
        # Create a folder for the thumbnails if one does not exist
        folder_name = "./Assets/Images/Thumbnail_cache/" + \
            json_folder["Folder_name"]
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
            print("Created thumbnail folder: " + folder_name)

        # Get each books thumbnail and download it
        for json_book in json_folder["Books"]:
            if json_book["Thumbnail"][0:4].upper() == "HTTP":
                try:
                    filename = folder_name+"/"+json_book["Title"]+".png"
                    book_data_changed = True
                    response = requests.get(
                        json_book["Thumbnail"], stream=True)
                    with open(filename, "wb") as file:
                        shutil.copyfileobj(response.raw, file)
                        json_book["Thumbnail"] = filename
                    del response
                except:
                    error_list += "Error retrieving url for: " + \
                        json_book["Title"] + "\n"

            elif json_book["Thumbnail"][0:2] == "./" or json_book["Thumbnail"][0:1] == ".":
                # Thumbnail is already local or a placeholder
                continue
            elif json_book["Thumbnail"][0:2] == "NA" or "Thumbnail"[0:1] == "":
                # Thumbnail has no thumbnail url
                error_list += "Book: " + \
                    json_book["Title"] + " has no thumnail url\n"
                continue
            else:
                error_list += "Book: " + \
                    json_book["Title"] + " has an invalid thumbnail format: " + \
                    json_book["Thumbnail"] + "\n"

    # Update the book data if any info was changed
    if book_data_changed:
        write_json_no_code("./Assets/Book_info.json", book_data)

    # Return any errors that occured
    if len(error_list) > 40:
        with open("./Assets/Images/Thumbnail_cache/Generator_errors.txt", "w") as file:
            file.write(error_list)
        return "218"
    return "200"


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


def delete_thumb(target, folder):
    if (target == "" or folder == ""):
        return "400"
    target = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(folder, target)
    if (os.path.exists(target)):

        os.remove(target)
        # Update book data
        stored_json = json.loads(
            read_json_no_code("./Assets/Book_info.json"))
        if stored_json == "":
            return "404"
        for json_folder in stored_json["Folders"]:
            if json_folder["Folder_name"] == folder:
                for json_book in json_folder["Books"]:
                    if json_book["Thumbnail"] == target:
                        json_book["Thumbnail"] = "NA"

        status = write_json_no_code(
            "./Assets/Book_info.json", stored_json)
        return status

        # Deleteme.png

    else:
        return "404"
    return "200"
