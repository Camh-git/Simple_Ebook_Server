import json
import os
from urllib.request import urlopen
# TODO: implement the password check


def check_password(password):
    return True


def fetch_settings(password):
    if check_password(password):
        try:
            with open("settings.json", "r") as json_file:
                data = json_file.read()
                return data
        except Exception as e:
            return "500: " + str(e)
    else:
        return "401"


def write_settings(data, password):
    if check_password(password):
        try:
            with open("settings.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
                return "200"
        except Exception as e:
            return "500: " + str(e)
    else:
        return "401"


def read_json_no_code(file):
    try:
        with open(file, "r") as json_file:
            data = json_file.read()
            return data
    except Exception as e:
        return "500: " + str(e)


def write_json_no_code(file, data):
    try:
        with open(file, "w") as json_file:
            json.dump(data, json_file, indent=4)
            return "200"
    except Exception as e:
        return "500: " + str(e)


def write_file_no_code(file, data):
    try:
        with open(file, "w") as target_file:
            target_file.write(data)
            return "200"
    except Exception as e:
        return "500: " + str(e)


def format_for_json(input):
    return input.replace("/", "").replace("\\", "").replace("'", "").replace(",", "").replace("\"", "").replace("'", "\"").replace("'", "\"")


def save_book_by_ext(file, folder_name):
    # Checks the book's file type and saves it using the correct method, returns "403" for invalid format
    file_type = file.content_type
    if "text/plain" in file_type:
        with open("./Books/{0}/".format(folder_name) + file.filename, "w") as f:
            f.write(str(file.read()))
    elif "/pdf" or "/epub" or "application/" in file_type:
        with open("./Books/{0}/".format(folder_name) + file.filename, "wb") as f:
            f.write(file.read())
    else:
        return "403"

    return "200"


def search_google_books(book):
    if book == "":
        return "404"
    book_data = ""
    book_path = os.path.splitext(book)
    book_address = book_path[0].replace(" ", "%20")
    print("using Google books API to look up: " + book_address)

    try:
        with urlopen('https://www.googleapis.com/books/v1/volumes?q=title={0}'.format(
                book_address)) as r:
            text = r.read()
            data = json.loads(text)
            authors = date = publisher = isbn10 = isbn13 = thumbnail = authorlist = ""

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

            book_data = '{{"Title":"{0}","Authors":[{1}],"Date":"{2}","Publisher":"{3}","isbn":"{4}","isbn13":"{5}","Thumbnail":"{6}","Extension":"{7}","Validated":"False"}}'.format(
                book_path[0], authorlist, date, publisher, isbn10, isbn13, thumbnail, book_path[1])

    except:
        print('Did not find book: {0}, using placeholder info'.format(
            book_path[0]))
        book_data = '{{"title":"{0}","Authors":["NA"],"Date":"NA","Publisher":"NA","isbn":"NA","isbn13":"NA","Thumbnail":"NA","Extension":"{1}","Validated":"False"}}'.format(
            book_path[0], book_path[1])
    return book_data
