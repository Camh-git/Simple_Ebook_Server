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


def search_google_books(book):
    if book == "":
        return "404"
    book_data = ""
    try:
        with urlopen('https://www.googleapis.com/books/v1/volumes?q=title={0}'.format(
                os.path.splitext(book)[0])) as r:
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
    return book_data
