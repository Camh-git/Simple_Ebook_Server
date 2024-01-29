from .API_utils import read_json_no_code, format_for_json, write_file_no_code
from urllib.request import urlopen
import json
import os


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
