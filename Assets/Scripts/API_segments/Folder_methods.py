import os
import shutil
from .Book_data_endpoint_methods import BD_rename_folder, BD_delete_folder, BD_create_thumb_folder, BD_upload_folder


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


def Upload_folder(request):

    folder_name = request.path.split("/upload-folder/")[1]
    files = request.files.getlist('files[]')

    # Check that the folder does not exist
    target = "./Books/" + folder_name
    thumb_folder = "./Assets/Images/Thumbnail_cache/"+folder_name
    if not os.path.exists(target) and not os.path.exists(thumb_folder):
        # Add the new folder to book data.json, thumb_info.json and the file system
        result = BD_create_thumb_folder(folder_name)
        if result == "200":
            os.makedirs(target)
            os.makedirs(thumb_folder)

            # Upload each book
            book_list = []
            for file in files:
                filetype = file.content_type

                if "text/plain" in filetype:
                    with open("./Books/{0}/".format(folder_name) + file.filename, "w") as f:
                        f.write(str(file.read()))
                elif "/pdf" or "/epub" or "application/" in filetype:
                    with open("./Books/{0}/".format(folder_name) + file.filename, "wb") as f:
                        f.write(file.read())
                else:
                    os.rmdir(target)
                    os.rmdir(thumb_folder)
                    return "403"

                book_list.append(file.filename)

            # Create an entry for the new folder in book_info.json and populate it
            status = BD_upload_folder(folder_name, book_list)
            return status
        else:
            return status
    else:
        return "409"


def Delete_folder(folder_name, delete_content, mainDir):
    if (folder_name == "" or delete_content == ""):
        return "400"
    if (folder_name.upper() == "MISC" or folder_name.upper() == "UPLOADS"):
        return "403"

    target = "{0}/{1}".format(mainDir, folder_name)
    changed_dirs = []
    notifyChange = False
    if os.path.exists(target):
        try:
            if delete_content.upper() != "TRUE":
                # If we are saving the books go through each and move them to misc folder, or the uploads folder if there is a conflict, warn user if so.
                # Safety check, before moving any books check there is a space in one of the two available folders
                for book in os.listdir(target):
                    destination = "{0}/Misc/MOVED:{1}".format(mainDir, book)
                    if os.path.exists(destination):
                        destination = "{0}/Uploads/MOVED:{1}".format(
                            mainDir, book)
                        if os.path.exists(destination):
                            return "409"

                for book in os.listdir(target):
                    start = "{0}/{1}".format(target, book)
                    destination = "{0}/Misc/MOVED:{1}".format(mainDir, book)
                    if os.path.exists(destination):
                        destination = "{0}/Uploads/MOVED:{1}".format(
                            mainDir, book)
                        os.rename(start, destination)
                        changed_dirs.append(os.path.splitext(book)[0])
                        notifyChange = True

                    else:
                        os.rename(start, destination)

            # Update the book data
            result = BD_delete_folder(
                folder_name, delete_content, "", changed_dirs)
            if result == "200":
                shutil.rmtree(target)
                if (notifyChange):
                    return "428"
                return result
            else:
                raise Exception(result)

        except Exception as e:
            return "500: " + str(e)
    else:
        return "404"


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
