from .API_utils import read_json_no_code, format_for_json, write_file_no_code, write_json_no_code
from urllib.request import urlopen
import json
import os


def edit_book_data(folder, book, authors, date, publisher, isbn, isbn13, thumbnail, validated):
    # Input validation
    if (folder == "" or book == "" or authors == "" or date == "" or publisher == "" or isbn == "" or thumbnail == "" or validated == ""):
        return "400"
    if not date.replace("-", "").isdigit() or not "-" in date:
        return "406"
    if not isbn.isdigit():
        return "406"
    print(len(isbn13))
    if not isbn13.isdigit() and len(isbn13) > 0:
        return "406"
    thumbnail.replace("http://", "WEB-").replace("https://", "WEB-")

    if validated.upper() != "TRUE" and validated.upper() != "FALSE":
        return "406"

    stored_json = json.loads(read_json_no_code("./Assets/Book_info.json"))
    if stored_json == "":
        return "404"
    # Note: the thumb path should be local, use a , to substitute /, cut off the :// part of https from a web url for safety (should be done in handler)
    #   example url: test&&New&&[a,b]&&1-2-3&&hi&&987&&654&&httpsfake&&True
    # Find the book
    for json_folder in stored_json["Folders"]:
        if json_folder["Folder_name"] == folder:
            for json_book in json_folder["Books"]:
                if json_book["Title"] == book:
                    # Use the jsonString to update the books info
                    json_book["Authors"] = authors
                    json_book["Date"] = date
                    json_book["Publisher"] = publisher
                    json_book["isbn"] = isbn
                    json_book["isbn13"] = isbn13
                    json_book["Thumbnail"] = thumbnail
                    json_book["Validated"] = validated
                    break
    # Save the updated data
    try:
        write_json_no_code("./Assets/Book_info.json", stored_json)
    except:
        return "404"
    return "200"


def generate_book_data(mainDir):
    stored_data = read_json_no_code("./Assets/Book_info.json")
    stored_json = json.loads(stored_data)

    lib_data = "{\"Folders\": ["
    for folder in os.listdir(mainDir):
        folder_data = '{{"Folder_name":"{0}","Books":['.format(folder)
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            # print("had: " + book + ", checking")
            # Check if we already have info on this book and skip it if so
            if os.path.splitext(book)[0] in stored_data:
                for folder in stored_json["Folders"]:
                    if folder["Folder_name"] != "Included Public domain" or folder["Folder_name"]:
                        for json_book in folder["Books"]:
                            try:
                                if json_book['Title'] == book:
                                    if json_book["Validated"] or (json_book["isbn"].upper() != "NA" and json_book["isbn"] != "" and json_book["Thumbnail"].upper != "NA" and json_book["Thumbnail"] != ""):
                                        # print("already had: " +
                                        #     json_book["Title"] + " with data")
                                        folder_data += str(json_book).replace("'", "\"").replace(
                                            "'", "\"").replace("'", "\"") + ","
                                        continue
                            except:
                                pass

            # Get book info and parse the result
            # 'https://www.googleapis.com/books/v1/volumes?q=isbn:{0}'.format(ISBN)  #ISBN approach
            try:
                with urlopen('https://www.googleapis.com/books/v1/volumes?q=title={0}'.format(
                        book)) as r:
                    text = r.read()
                    data = json.loads(text)
                    title = authors = date = publisher = isbn10 = isbn13 = thumbnail = authorlist = ""
                    try:
                        title = format_for_json(
                            data["items"][0]["volumeInfo"]["title"])
                    except:
                        title = ""
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
                        authorlist += '"{0}",'.format(format_for_json(author))
                    authorlist = authorlist[:-1]

                    book_data = '{{"Title":"{0}","Authors":[{1}],"Date":"{2}","Publisher":"{3}","isbn":"{4}","isbn13":"{5}","Thumbnail":"{6}","Validated":"False"}},'.format(title, authorlist, date, publisher, isbn10, isbn13, thumbnail
                                                                                                                                                                             )
                    folder_data += book_data

            except:
                book_data = '{{"title":"{0}","Authors":["NA"],"Date":"NA","Publisher":"NA","isbn":"NA","isbn13":"NA","Thumbnail":"NA","Validated":"False"}},'.format(
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
    write_file_no_code("../../Book_info.json", lib_data)
    return lib_data
