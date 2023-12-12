# !!!!! THE PROJECT IS STILL IN DEVELOPMENT, PLEASE SEE TODO.txt FOR MORE INFORMATION !!!!!

# Simple EBook server

<p>This project is designed to be a simple browser based UI for accessing e-books
stored in a folder on the server.</p>

<p>The primary functionality is the library, which automaticaly populates itself
with the contents of the "books" folder.</p>

<p>The library will display each sub-folder and it's content and allow users
to download the files for reading, or view supported file types
(Currently PDF, with EPUB on the To-do list)</p>

### FUTURE DEVELOPMENT

<ul>
	<li>
		The next step for the project is to implement file manipulation on the web
		UI via a management page (users can technicaly do this by accessing the 
		books folder directly, but that goes against the spirit of the project).
	</li>
	<li>Implement an API to fetch books from the server and executhe other functions, probably python flask</li>
	<li>Possible react port - better tech and probably much neater</li>
</ul>
<p>The next step for the project is to implement file manipulation on the web
UI via a management page, users can technicaly do this by accessing the
books folder directly, but that goes against the spirit of the project.</p>

Running the project
To run the server and website you will need to take the following steps:

Install a LAMP stack with php (will change in future), I followed this tutorial: https://www.youtube.com/watch?v=ZDcbb_VjIQs
Install python version 3.9 or later
Download the files from github and copy them into the web root, which should be at: /var/www/html/
Open a command prompt and CD into the /var/www/html/Simple_Ebook_Server directory
Run the command: export FLASK_APP="BookAPI.py" to point flask at the correct file.
Run the command: flask run --host=0.0.0.0 to run the API. NOTE: the project is still WIP and this will change
With the API now running, naviagte to: Device IP/Simple_Ebook_Server/Home.html
Enjoy looking around and reading the supplied public domain books.
