# !!!!! THE PROJECT IS STILL IN DEVELOPMENT, PLEASE SEE TODO.txt FOR MORE INFORMATION !!!!!

# Simple EBook server

<p>This project is designed to be a simple browser based UI for accessing e-books
stored in a folder on the server.</p>

<p>The primary functionality is the library, which automaticaly populates itself
with the contents of the "books" folder.</p>

<p>The library will display each sub-folder and it's content and allow users
to download the files for reading, or view supported file types
(Currently supports PDF, with EPUB on the To-do list)</p>

<p>The project also includes a management page that lets the user interact with 
a python flask management API to manipulate the library and associated software features,
such as the thumbnail data.</p>

### FUTURE DEVELOPMENT

<ul>
	<li>Expand support to more file types</li>
	<li>Finish replacing old php scripts using python and js (will be stored in depreciated)</li>
	<li>Overhaul CSS for better aesthetics and possible mobile use</li>
	<li>Possible react port - better tech and probably much neater</li>
</ul>

### Running the project

To run the server and website you will need to take the following steps:

<ul>
<li>Install a LAMP stack with php (will change in future), I followed this tutorial: https://www.youtube.com/watch?v=ZDcbb_VjIQs
<li>Install python version 3.9 or later</li>
<li>Download the files from github and copy them into the web root, which should be at: /var/www/html/</li>
<li>Open a command prompt and CD into the /var/www/html/Simple_Ebook_Server directory</li>
<li>Run the command: export FLASK_APP="BookAPI.py" to point flask at the correct file.</li>
<li>Run the command: flask run --host=0.0.0.0 to run the API. NOTE: the project is still WIP and this will change</li>
<li>With the API now running, naviagte to: Device IP/Simple_Ebook_Server/Home.html</li>
<li>Enjoy looking around and reading the supplied public domain books.</li>
</ul>
