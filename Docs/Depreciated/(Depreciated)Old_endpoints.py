@app.route("/list-books")
def list_books():
    list = ''
    for folder in os.listdir(mainDir):
        list += '<div class = "Book_folder"><h5 class="book_list_title">{0}</h5><ul>'.format(
            folder)
        for book in os.listdir("{0}/{1}".format(mainDir, folder)):
            list += '<li>{0}</li>'.format(book)
        list += '</ul></div>'
    response = app.response_class(response=json.dumps(
        list), status=200, mimetype='application/json')
    return response


@app.route("/list-thumbs")
def List_Thumbs():
    list = '<ul id = "Thumb_list">'
    for image in os.listdir("./Assets/Images/Thumbnail_cache/"):
        list += '<li>{0}</li>'.format(image)
    list += '</ul>'
    response = app.response_class(response=json.dumps(
        list), status=200, mimetype='application/json')
    return response
