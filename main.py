from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello from basic ebook server"

#Book methods
@app.route("/post-book/<book_name>", methods = ["POST"])
def Upload_book(book_name):
    return 501

@app.route("/delete-book/<book_name>", methods = ["DELETE"])
def Remove_book(book_name):
    return 501

@app.route("/rename-book/<book_name>&&<new_name>", methods = ["PUT"])
def Rename_book(book_name, new_name):
    if request.method == "POST":
        return 405
    return 501

#Folder methods
@app.route("/post-folder/<folder_name>&&<content>", methods = ["POST"])
def Upload_folder(folder_name, contents):
    return 501

@app.route("/delete-folder/<folder_name>&&<delete_content>", methods = ["DELETE"])
def Delete_folder():
    return 501

@app.route("/rename-folder/<folder_name>&&<new_name>", methods = ["PUT"])
def Rename_folder(folder_name, new_name):
    return 501

#Library management functions
@app.route("/create-folder/<folder_name>", methods = ["POST"])
def Create_folder(folder_name):
    return 501

@app.route("/move-book-to-folder/<old_folder_name>&&<new_folder_name>&&<book_name>", methods = ["PUT"])
def Move_book_to_folder(old_folder_name, new_folder_name, book_name):
    return 501

#Thumbnail management functions
@app.route("/reassign-thumb/<folder_name>&&<book_name>&&<thumb>", methods = ["PUT"])
def Reasign_thumb(folder_name, book_name, thumb):
    return 501

@app.route("/clear-thumbs/<option>", methods = ["PUT"])
def Clear_thumbs(option):
    return 501

#Misc option functions
@app.route("/toggle-dl/<option>&&<code>", methods = ["PUT"])
def Toggle_dls(option, code):
    return 501

@app.route("/toggle-readers/<option>&&<code>", methods = ["PUT"])
def Toggle_readers(option, code):
    return 501

#http://127.0.0.1:5000/lists?address=1.1.1.1&list=whitelist&option=add
@app.route("/lists/<address>&&<list>&&<option>", methods = ["PUT"])
def Manage_ip_list(address, list, option):

    #Get data from the right list
    data = ""
    if list.upper() == "WHITELIST":
        with open("Assets/Whitelist.txt","r") as file:
            data = file.read()
    
    elif list.upper() == "BLACKLIST":
        with open("Assets/Blacklist.txt","r") as file:
            data = file.read()
    else:
        return "Bad list option: " + list  
     
    #If adding and adress check it exists then add if not, or remove if selected
    if(option.upper == "ADD"):
        if address not in data:
            data += ("\n" + str(address))
    elif(option.upper == "REMOVE"):
        data = data.replace(address,"")
    else:
        return "Bad whitelist action: " + option
            
    #Write the newly changed data to the correct file
    if list.upper() == "WHITELIST":
        with open("Assets/Whitelist.txt","w") as file:
            file.write(data)
    elif list.upper() == "BLACKLIST":
        with open("Assets/Blacklist.txt","w") as file:
            file.write(data)
    else:
        return "Bad list option: " + list  

    return 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def Catch_all(path):
    return "Invalid path: " + path, 400

if __name__ == "__main__":
    app.run(debug = True)
