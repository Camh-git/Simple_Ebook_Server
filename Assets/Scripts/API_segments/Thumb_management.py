from .API_utils import read_json_no_code, write_json_no_code
from urllib.request import urlopen
import os
import json


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
