import os


def list_books(mainDir):
    data = '{"Books":['
    for folder in os.listdir(mainDir):
        data += '{"Folder":"'+folder + '","Content":['
        emptyDir = True
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            emptyDir = False
            components = os.path.splitext(book)
            data += '{"Name":"' + components[0] + \
                '","ext":"' + components[1]+'"},'
        if not emptyDir:
            data = data[:-1]
        data += "]},"
    data = data[:-1]
    data += ']}'
    return data


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {
            'pdf', 'txt', 'epub', 'mobi', 'azw3'}


def Remove_book(book_name, ext, folder, mainDir):
    if (book_name == "" or ext == "" or folder == ""):
        return "400"
    target = "{0}/{1}/{2}.{3}".format(mainDir, folder, book_name, ext)
    if os.path.exists(target):
        try:
            os.remove(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"


def Rename_book(book_name, ext, folder, new_name, mainDir):
    if (book_name == "" or ext == "" or folder == "" or new_name == ""):
        return "400"
    # Make sure the book exists and that a file with a matching name doesn't already exist
    target = "{0}/{1}/{2}.{3}".format(mainDir, folder, book_name, ext)
    renamed = "{0}/{1}/{2}.{3}".format(mainDir, folder, new_name, ext)
    if os.path.exists(renamed):
        return "409"
    if os.path.exists(target):
        try:
            os.rename(
                target, renamed)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"
