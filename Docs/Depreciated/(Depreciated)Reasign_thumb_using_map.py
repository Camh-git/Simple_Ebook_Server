# Manipulate the map - TODO: delete this section when the thumb map is retired.
if os.path.exists("./Assets/Images/Thumbnail_map.json"):
    json_map_data = read_json_no_code("./Assets/Images/Thumbnail_map.json")
    map = json.loads(json_map_data)

    bookFound = False
    for book in map["Books"]:
        if book["Folder"] == book_folder and book["Name"] == book_name:
            bookFound = True
            book.update({"Thumb": thumb.replace(" ", "")})
    if not bookFound:
        # Add the book to the map if it doesn't already have an entry
        map["Books"].append(
            {"Folder": book_folder, "Name": book_name, "Thumb": thumb.replace(" ", "")})

    # return str(map["Books"][0]["Name"] in os.listdir("./Books/"+map["Books"][0]["Folder"]))
    return write_json_no_code("./Assets/Images/Thumbnail_map.json", map)

else:
    return "404"
