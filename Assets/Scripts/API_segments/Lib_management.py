import os
from .Book_data_endpoint_methods import BD_move_book, BD_create_folder, BD_create_thumb_folder


def Create_folder(folder_name, mainDir):
    if (folder_name == ""):
        return "400"
    target = "{0}/{1}".format(mainDir, folder_name)
    if not os.path.exists(target):
        try:
            result = BD_create_folder(folder_name)
            if result == "200":
                os.makedirs(target)
                # Make thumbnail folder
                thumb_folder = "./Assets/Images/Thumbnail_cache/"+folder_name
                if not os.path.isdir(thumb_folder):
                    os.makedirs(thumb_folder)
                result = BD_create_thumb_folder(folder_name)
                return result
            else:
                raise Exception(result)
        except Exception as e:
            return "500:" + str(e)
    else:
        return "409"


def Move_book_to_folder(book_name, ext, old_folder_name, new_folder_name, mainDir):
    if (book_name == "" or ext == "" or old_folder_name == "" or new_folder_name == ""):
        return "400"
    oldPath = "{0}/{1}/{2}.{3}".format(mainDir,
                                       old_folder_name, book_name, ext)
    newPath = "{0}/{1}/{2}.{3}".format(mainDir,
                                       new_folder_name, book_name, ext)
    if os.path.exists(oldPath):
        if not os.path.exists(newPath):
            try:
                result = BD_move_book(
                    old_folder_name, new_folder_name, book_name)
                if result == "200":
                    os.rename(oldPath, newPath)
                    return result
                else:
                    raise Exception(result)
            except Exception as e:
                return "500:" + str(e)
        else:
            return "409"
    else:
        return "404"
