import os
import shutil
from .Book_data_endpoint_methods import BD_rename_folder


def list_folders(mainDir):
    response = ""
    for folder in os.listdir(mainDir):
        response += folder + ", "
    response = response[:-1]
    return response


def list_folder_content(folder_name, mainDir):
    response = ""
    try:
        for book in os.listdir("{0}/{1}".format(mainDir, folder_name)):
            response += book + ", "
    except:
        return str("Cannot find folder: " + folder_name)
    response = response[:-1]
    return response


def Delete_folder(folder_name, delete_content, mainDir):
    if (folder_name == "" or delete_content == ""):
        return "400"
    if (folder_name.upper() == "MISC" or folder_name.upper() == "UPLOADS"):
        return "403"

    target = "{0}/{1}".format(mainDir, folder_name)
    notifyChange = False
    if os.path.exists(target):
        try:
            if delete_content.upper() != "TRUE":
                # If we are saving the books go through each and move them to misc folder,
                # add a "MOVED:" prefix if misc already contains a book of the same name
                for book in os.listdir(target):
                    start = "{0}/{1}".format(target, book)
                    destination = "{0}/Misc/{1}".format(mainDir, book)

                    if os.path.exists(destination):
                        os.rename(
                            start, "{0}/Misc/MOVED:{1}".format(mainDir, book))
                        notifyChange = True
                    else:
                        os.rename(start, destination)

            shutil.rmtree(target)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    if (notifyChange):
        return "428"
    return "200"


def Rename_folder(folder_name, new_name, mainDir):
    if (folder_name == "" or new_name == ""):
        return "400"
    if (folder_name.upper() == "MISC" or folder_name.upper() == "UPLOADS"):
        return "403"

    # Make sure the folder exists, and stop if a folder with the new name already exists
    target = "{0}/{1}".format(mainDir, folder_name)
    reNamed = "{0}/{1}".format(mainDir, new_name)
    if os.path.exists(reNamed):
        return "409"
    if os.path.exists(target):
        try:
            result = BD_rename_folder(folder_name, new_name)
            if result == "200":
                os.rename(target, reNamed)
                return result
            else:
                raise Exception(result)
        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"
    return "200"
