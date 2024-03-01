from .API_utils import read_json_no_code, write_json_no_code, write_file_no_code
import os
import json
import shutil
import requests
from .Book_data_endpoint_methods import BD_rename_thumb, BD_delete_thumb


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
    data = read_json_no_code("./Assets/Images/Thumbnail_info.json")
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
        book_num = 0
        for json_book in json_folder["Books"]:
            book_num = book_num + 1
            if json_book["Thumbnail"][0:4].upper() == "HTTP":
                try:
                    # Add the slashes after the http and replace combookscontent with com/books/content for google books content, (shouldn't hurt anything else)
                    filename = folder_name+"/"+json_book["Title"]+".png"
                    url = json_book["Thumbnail"][:4] + \
                        "s://" + json_book["Thumbnail"][5:]
                    if "books.google" in url and "combookscontent" in url:
                        url = url.replace("combookscontent",
                                          "com/books/content")
                    book_data_changed = True

                    response = requests.get(
                        url, stream=True)
                    with open(filename, "wb") as file:
                        shutil.copyfileobj(response.raw, file)
                        json_book["Thumbnail"] = filename
                    del response
                except Exception as e:
                    try:
                        error_list += "Error retrieving url for: " + \
                            json_book["Title"] + ", url: " + \
                            url + ", Error: " + str(e) + "\n"
                    except Exception as e:
                        error_list += "Error for book number: " + \
                            str(book_num) + " in folder: " + \
                            json_folder["Folder_name"] + \
                            ", Error: " + str(e) + "\n"

            elif json_book["Thumbnail"][0:2] == "./" or json_book["Thumbnail"][0:1] == ".":
                # Thumbnail is already local or a placeholder
                continue
            elif json_book["Thumbnail"][0:2] == "NA" or json_book["Thumbnail"] == "":
                # Book has no thumbnail url
                try:
                    error_list += "Book: " + \
                        json_book["Title"] + " has no thumnail url\n"
                except:
                    error_list += "Error for book number: " + \
                        str(book_num) + " in folder: " + \
                        json_folder["Folder_name"] + "\n"
                continue
            else:
                try:
                    if len(json_book["Title"]) < 1:
                        raise Exception("missing title")
                    error_list += "Book: " + \
                        json_book["Title"] + " has an invalid thumbnail format: " + \
                        json_book["Thumbnail"] + "\n"
                except:
                    error_list += "Error for book number: " + \
                        str(book_num) + " in folder: " + \
                        json_folder["Folder_name"] + "\n"

    # Update the book data if any info was changed
    if book_data_changed:
        write_json_no_code("./Assets/Book_info.json", book_data)
        populate_thumb_data()

    # Return any errors that occured
    if len(error_list) > 40:
        with open("./Assets/Images/Thumbnail_cache/Generator_errors.txt", "w") as file:
            file.write(error_list)
        return "218"
    return "200"


def Reasign_thumb(book_folder, book_name, thumb_folder, thumb):
    if (book_folder == "" or book_name == "" or thumb_folder == "" or thumb == ""):
        return "400"

    # Update the book's data to use the new thumbnail
    image = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(
        thumb_folder, thumb)

    if os.path.exists(image):
        stored_json = json.loads(
            read_json_no_code("./Assets/Book_info.json"))
        if stored_json == "":
            return "404"
        changedData = False

        for json_folder in stored_json["Folders"]:
            if json_folder["Folder_name"] == book_folder:
                for json_book in json_folder["Books"]:
                    if json_book["Title"] == os.path.splitext(book_name)[0]:
                        json_book["Thumbnail"] = image
                        changedData = True

        if changedData:
            status = write_json_no_code(
                "./Assets/Book_info.json", stored_json)
            return status
        else:
            return "410"

    else:
        return "404"

    # Manipulate the map - TODO: delete this section when the thumb map is retired.
    if os.path.exists("./Assets/Images/Thumbnail_map.json"):
        json_map_data = read_json_no_code("./Assets/Images/Thumbnail_map.json")
        map = json.loads(json_map_data)

        bookFound = False
        for book in map["Books"]:
            if book["Folder"] == book_folder and book["Name"] == book_name:
                bookFound = True
                book.update({"Thumb": thumb.replace(" ", "")})
        if not bookFound:
            # Add the book to the map if it doesn't already have an entry
            map["Books"].append(
                {"Folder": book_folder, "Name": book_name, "Thumb": thumb.replace(" ", "")})

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


def rename_thumb(folder, target, new_name):
    if (folder == "" or target == "" or new_name == ""):
        return "400"
    extension = os.path.splitext(target)[1]

    # Make sure the image exists and that a file with a matching name doesn't already exist
    image = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(folder, target)
    reNamed = "./Assets/Images/Thumbnail_cache/{0}/{1}{2}".format(
        folder, new_name, extension)
    if os.path.exists(reNamed):
        return "409"

    if os.path.exists(image):
        try:
            result = BD_rename_thumb(
                folder, target, str(new_name+extension))
            if result == "200":
                os.rename(
                    image, reNamed)
                return result
            else:
                raise Exception(result)

        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"


def delete_thumb(folder, target):
    if (target == "" or folder == ""):
        return "400"
    target = "./Assets/Images/Thumbnail_cache/{0}/{1}".format(folder, target)

    if (os.path.exists(target)):
        try:
            result = BD_delete_thumb(folder, target)
            if result == "200":
                os.remove(target)
                return result
            else:
                raise Exception(result)

        except Exception as e:
            return "500: " + str(e)

    else:
        return "404"


def populate_thumb_data():
    cache = "./Assets/Images/Thumbnail_cache"
    Thumb_data = '{{"Folders":['
    for folder in os.listdir(cache):
        if os.path.isdir("{0}/{1}".format(cache, folder)):
            Thumb_data += '{{"Folder_name":"{0}","Images":['.format(folder)
            for img in os.listdir("{0}/{1}".format(cache, folder)):
                Thumb_data += '"{0}",'.format(img)

            if Thumb_data[len(Thumb_data)-1] != "[":
                Thumb_data = Thumb_data[:-1]
            Thumb_data += ']}},'

    if Thumb_data[len(Thumb_data)-1] != "[":
        Thumb_data = Thumb_data[:-1]
    Thumb_data += ']}}'
    Thumb_data = Thumb_data.replace("{{", "{").replace("}}", "}")
    status = write_file_no_code("./Assets/Thumbnail_info.json", Thumb_data)
    return status
