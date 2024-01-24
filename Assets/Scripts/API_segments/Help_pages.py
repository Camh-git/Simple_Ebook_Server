def help():
    content = ''
    with open("./Pages/API_Help.html") as file:
        content = file.read()
    return content


def file_support():
    content = ''
    with open("./Pages/File_support_table.html") as file:
        content = file.read()
    return content


def show_site_map(format="XML"):
    content = ''
    if format.upper() == "XML":
        with open("./Docs/Sitemap.xml") as file:
            content = file.read()
    else:
        with open("./Docs/Sitemap.txt") as file:
            content = file.read()
    return content
