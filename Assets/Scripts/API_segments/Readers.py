
def run_epub_reader(book, folder):

    try:
        with open("./Pages/Epub_viewer.html", "r") as viewer_page:
            data = viewer_page.read()
            data = data.replace('"placeholder"',
                                '"./Books/{0}/{1}"'.format(folder, book))
            data = data.replace("epub_reader.js", "Pages/epub_reader.js")
            return data
    except Exception as e:
        return "500: " + str(e)
