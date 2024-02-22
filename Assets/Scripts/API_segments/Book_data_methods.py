from .API_utils import read_json_no_code, format_for_json, write_file_no_code, write_json_no_code
from urllib.request import urlopen
import json
import os


def edit_book_data(folder, book, authors, date, publisher, isbn, isbn13, thumbnail, extension, validated, newFolder="", newTitle=""):
    # Input validation
    if (folder == "" or book == "" or authors == "" or date == "" or publisher == "" or isbn == "" or thumbnail == "" or validated == ""):
        return "400"
    if not date.replace("-", "").isdigit() or not "-" in date:
        return "406"
    if not isbn.isdigit():
        return "406"
    if not isbn13.isdigit() and len(isbn13) > 0:
        return "406"
    thumbnail = thumbnail.replace(
        "http://", "WEB-").replace("https://", "WEB-").replace("-@", "/")
    if validated.upper() != "TRUE" and validated.upper() != "FALSE":
        return "406"

    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    # Note: the thumb path should be local, use a , to substitute /, cut off the :// part of https from a web url for safety (should be done in handler)
    #   example url: test&&New&&[a,b]&&1-2-3&&hi&&987&&654&&httpsfake&&True
    # Find the book
    if newFolder != "":
        result = move_book_to_folder(folder, newFolder, book)
        return result

    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book:
                    # Use the jsonString to update the books info
                    if newTitle != "":
                        json_book["Title"] = newTitle
                    json_book["Authors"] = authors
                    json_book["Date"] = date
                    json_book["Publisher"] = publisher
                    json_book["isbn"] = isbn
                    json_book["isbn13"] = isbn13
                    json_book["Thumbnail"] = thumbnail
                    json_book["Extension"] = extension
                    json_book["Validated"] = validated
                    break
    # Save the updated data
    try:
        write_json_no_code("./Assets/Book_info.json", stored_json)
    except:
        return "404"
    return "200"


def move_book_to_folder(old_folder, new_folder, book_name):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    # get the book data
    book_data = ""
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == old_folder:
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book_name:
                    book_data = json_book

    # Copy the book data into the new folder
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == new_folder:
            pass

    remove_book_data(old_folder, book_name)

    return "501"


def remove_book_data(folder, book):
    return "200"
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book:
                    pass
                    # remove the book data
    return "501"


def get_specific_book_data(folder, book_name):
    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"

    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book_name:
                    return json_book


def generate_book_data(mainDir):
    stored_json = ""
    stored_data = ""  # See if the scope on this can be reduced
    try:
        stored_data = read_json_no_code("./Assets/Book_info.json")
        stored_json = json.loads(stored_data)
    except:
        return "404"

    lib_data = "{\"Folders\": ["
    for folder in os.listdir(mainDir):
        folder_data = '{{"Folder_name":"{0}","Books":['.format(folder)
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            # Check if we already have info on this book and skip it if so
            found_data = False
            if os.path.splitext(book)[0] in stored_data:
                for json_folder in stored_json["Folders"]:
                    for json_book in json_folder["Books"]:
                        try:
                            if json_book['Title'] == book or json_book['Title'] == os.path.splitext(book)[0]:
                                if json_book["Validated"] or (json_book["isbn"].upper() != "NA" and json_book["isbn"] != "" and json_book["Thumbnail"].upper != "NA" and json_book["Thumbnail"] != ""):
                                    # print("already had: " + json_book["Title"])
                                    found_data = True
                                    folder_data += str(json_book).replace("'", "\"").replace(
                                        "'", "\"").replace("'", "\"") + ","
                                    continue  # Not sure why this is being ignored
                        except:
                            pass

            # Get book info and parse the result
            # 'https://www.googleapis.com/books/v1/volumes?q=isbn:{0}'.format(ISBN)  #ISBN approach
            try:
                if len(os.path.splitext(book)[0]) > 1 and not found_data:
                    with urlopen('https://www.googleapis.com/books/v1/volumes?q=title={0}'.format(
                            book)) as r:
                        text = r.read()
                        data = json.loads(text)
                        title = authors = date = publisher = isbn10 = isbn13 = thumbnail = authorlist = ""
                        title = os.path.splitext(book)[0]
                        extension = os.path.splitext(book)[1]
                        try:
                            authors = format_for_json(
                                data["items"][0]["volumeInfo"]["authors"])
                        except:
                            authors = ""
                        try:
                            date = format_for_json(
                                data["items"][0]["volumeInfo"]["publishedDate"])
                        except:
                            date = ""
                        try:
                            publisher = format_for_json(
                                data["items"][0]["volumeInfo"]["publisher"])
                        except:
                            publisher = ""
                        try:
                            isbn10 = format_for_json(
                                data["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"])
                        except:
                            isbn10 = ""
                        try:
                            isbn13 = format_for_json(
                                data["items"][0]["volumeInfo"]["industryIdentifiers"][1]["identifier"])
                        except:
                            isbn13 = ""
                        try:
                            thumbnail = format_for_json(
                                data["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"])
                        except:
                            thumbnail = ""

                        for author in authors:
                            authorlist += '"{0}",'.format(
                                format_for_json(author))
                        authorlist = authorlist[:-1]

                        book_data = '{{"Title":"{0}","Authors":[{1}],"Date":"{2}","Publisher":"{3}","isbn":"{4}","isbn13":"{5}","Thumbnail":"{6}","Extension":"{7}","Validated":"False"}},'.format(
                            title, authorlist, date, publisher, isbn10, isbn13, thumbnail, extension)
                        folder_data += book_data

            except:
                book_data = '{{"title":"{0}","Authors":["NA"],"Date":"NA","Publisher":"NA","isbn":"NA","isbn13":"NA","Thumbnail":"NA","Extension":"{1}","Validated":"False"}},'.format(
                    book, extension)
                folder_data += book_data

        # Format the folder data and add it to the library
        if folder_data[len(folder_data)-1] != "[":
            folder_data = folder_data[:-1]
        folder_data += "]},"
        lib_data += folder_data

    lib_data = lib_data[:-1]
    lib_data += "]}"
    # Convert the libdata to json and save
    lib_data = lib_data
    status = write_file_no_code("./Assets/Book_info.json", lib_data)
    return status
