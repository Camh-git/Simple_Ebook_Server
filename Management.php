<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">	
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>	
    <link rel="stylesheet" href="Assets/StyleSheet.css"/>		
  </head>
	
<div id = "header_container"> </div>
<?php
    #Fetch every folder in books   
  	$path = "\Books\\".DIRECTORY_SEPARATOR."*";
	  $Folders = glob($path,GLOB_ONLYDIR);
	
	  $Collumn_num = 1;
    $Output = '<div id = "Book_collection">';
    #Show the contents of every book folder
  	foreach ($Folders as $dir){
      $Output .= "<div class ='Book_folder'>";
		  #Get and print the folder name
		  $Title = substr($dir,6);
		  $Output .='<h5>'.$Title.':</h5>';
		  $content = glob("".$dir."/{*.*}",GLOB_BRACE);

      #List the books
		  $Output .='<ul>';
		  foreach($content as $book)
		  {
        #Get the books name from it's filepath and tidy it up. 
        #TODO: consider re-implementing this, but having it tidy up the source files aswell so they can still be manipulated
        $Name = pathinfo($book,PATHINFO_BASENAME);
        /*
		    $Name = str_replace('_',' ', pathinfo($book,PATHINFO_BASENAME ));	
			  {
				  $Name[0] = strtoupper($Name[0]);
			  }
			  catch(Exception $e) {
				  echo "<script>console.log('Failed to capitalise a title with error:".$e->getMessage()."')</script>";
			  }*/
        $Output .= '<li>'.$Name.'</li>';
      }
      $Output .='</ul></div>';

    }
    $Output .="</div>";
		#This output is echoed onto the screen so it can be manipulated by JS
		echo($Output);
?>

<body>
<div id = "Management_pannel">
  <h1>Management</h1>
  <h2>This page is currently under construction</h2>
  <!--Note on input names: Each input name has a prefix related to it's form eg: inputs for delete single have the prefix DS_-->
  <!-- TODO: 
    form actions, see each form
    Add thumbnail management form(auto fetch and manualy assgin/upload thumbs)
    Investigate adding a completion popup
    Swap the upload book and folder forms over the the python approach when ready
    consistency pass on the toggles
  -->

  <!--Manage books-->
  <h2>Manage individual books</h2>
  <section class = "flex-container Management-row">
    <!--upload single, todo:Add a folder select-->
    <form method = "POST" enctype = "multipart/form-data" id = "US_form" action = "Assets/Scripts/Upload_single.php">
      <h3>Upload book</h3>
      <input type = "file" name = "US_file_inp" accept = ".epub,.pdf,.txt,.doc,.docx"/>
      <br/>
	    <input type = "submit" value = "upload" />
	    <p class = "Warning">Max upload size: 30MB</p>
    </form>

    <!--Delete single-->
    <!--TODO: make this send a variable with the filename-->
    <form method = "POST" enctype = "multipart/form-data" id = "DS_form">
      <h3>Delete book</h3>
      <label for = "DS_folder_select">Select folder</label>
      <select name = "DS_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <label for = "DS_book_select">Select book</label>
      <select name = "DS_book_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <input type="submit" value = "Submit" />
    </form>

    <!--Rename single TODO:write this-->
    <form method = "POST" enctype = "multipart/form-data" id = "RS_form">
      <h3>Rename book</h3>
      <label for = "RS_folder_select">Select folder</label>
      <select name = "RS_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <label for = "RS_book_select">Select book</label>
      <select name = "RS_book_select">
        <option Value = "None">No selection</option>
      </select>
      <br>
      
      <input type = "text" name = "RS_New_name" placeholder = "New name"/>
      <input type = "submit" value = "Submit" />
    </form>
  </section>

  <!--Manage folders-->
  <h2>Manage folders</h2>
  <section class="flex-container Management-row">
    <!--Upload folder TODO: make this take a name for the folder, fix upload -->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Upload_folder.php">
      <h3>Upload folder</h3>
      <input type = "text" name = "UF_name" placeholder = "name">
	    <p>Please add each file you want to upload(if none please use create folder)</p>
	    <input type = "file" name = "UF_inp_Files[]" multiple = "multiple" accept = ".epub,.pdf,.txt,.doc,.docx"/>
      <br>
      <input type = "submit" value = "upload" />
    </form>

    <!--Delete folder TODO:double check this works with new naming-->
    <form method = "POST" enctype = "multipart/form-data" id = "DF_form">
      <h3>Delete folder</h3>

      <label for = "DF_folder_select">Select folder</label>
      <select name = "DF_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <input type = "submit" value = "Submit" />
      <br>
      <input type = "checkbox" name = "DS_Delete_content" value = "DS_Delete_content"/>
      <label for = "DS_Delete_content">Delete folder content?(Content will be moved to misc if not checked)</label>
    </form>

    <!--Rename folder TODO: fix the path compilation, add the rename function-->
    <form method = "POST" enctype = "multipart/form-data" id = "RF_form"> 
      <h3>Rename folder</h3>

      <select name = "RF_folder_select">
        <option Value = "None">No selection</option>
      </select>

      <input type = "text" name = "RF_New_name" placeholder = "New name"/>
      <br>
      <input type = "submit" value = "Submit" />
    </form>

  </section>

  <!--Manage libray-->
  <h2>Manage library</h2>
  <section class = "flex-container Management-row">
    <!--Create empty folder TODO:find a way to fix the permissions issue-->
    <form method = "POST"  enctype = "multipart/form-data" id = "CF_form">
      <h3>Create new folder</h3>
      <input type = "text" name = "CF_Name" placeholder = "Enter name here"/>
      <br>
      <input type = "submit" value = "Submit">
    </form>
    
    <!--Move book between folders-->
    <form method = "POST" enctype = "multipart/form-data" id = "MV_folder_form">
      <h3>Move book to new folder</h3>

      <label for = "MV_folder_select">Select current folder</label>
      <select name = "MV_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <label for = "MV_book_select">Select book</label>
      <select name = "MV_book_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <!--NOTE: This naming inconsistency is intentional, it prevents the book select from changing when a new target is chosen -->
      <label for = "mv_target_folder_select">Select new folder</label>
      <select name = "mv_target_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>
      <input type = "submit" value = "Submit"/>
    </form>

  </section>

  <!--Manage thumbnails-->
  <h2>Manage Thumbnails</h2>
  <section class = "flex-container Management-row">
    <!--Manage thumbnails TODO:write this-->
    <form method = "POST" enctype="multipart/form-data" id = "TH_select_form">
      <h3>Re-assign Thumbnails</h3>

      <label for = "TH_folder_select">Folder</label>
      <select name = "TH_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <label for = "TH_book_select">Book</label>
      <select name = "TH_book_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <p>Select new image.</p>
      <select name = "Thumb_new_select">
        <option Value = "None">No selection</option>
      </select>

      <input type = "submit" value = "Change"/>
    </form>

    <!--Upload thumbnail -->
    <form method = "POST" enctype="multipart/form-data" id = "TH_upload_form">
      <h3>Upload a thumbnail</h3>
      <input type = "file" name = "Thumb_upload" accept = ".png,.jpg,.jpeg,.svg,.gif,.webp,.xcf,.psd"/>
      <br>
      <input type = "submit" value = "Upload"/>
    </form>

    <!--Format thumbnail cache TODO:write this-->
    <form method = "POST" enctype="multipart/form-data" id = "TH_format_form">
      <h3>Delete/populate thumbnail cache</h3>
      <p>
        Clearing the cache will remove all thumbnails, they will be 
        re-generated when you next visit the libary page.
      </p>
      <p>Re-populate will automaticaly empty and then refill the folder</p>

      <table>
        <tr>
          <label for = "Thumb_delete_all">Clear cache</label>
          <input type = "Radio" name = "Thumb_cache_format" id = "Thumb_delete_all"/>
        </tr>
        <tr>
          <label for = "Thumb_regen">Repopulate cache</label>
          <input type = "Radio" name = "Thumb_cache_format" id = "Thumb_regen"/> 
        </tr>
      </table>
      
      <input type = "submit" value = "Start"/>
      <h3 class = "Warning">
        WARNING: This action removes files.
      </h3>
    </form>

  </section>

  <!--Misc options-->
  <h2>Misc options</h2>
  <section class = "flex-container Management-row">
    <!--Enable or disable downloads-->
    <form method = "POST" enctype = "multipart/form-data" id = "DL_toggle_form">
      <h3>Enable downloads?</h3>

      <p name = "Downloads enabled display">Downloads are currently: </p>
      <label for = "DL_toggle_enable">Enabled</label>
      <input type = "checkbox" name = "DL_toggle_enable" value = "DL_toggle_enable"/>
      <label for = "DL_toggle_disable">Disabled</label>
      <input type = "checkbox" name = "DL_toggle_disable" value="DL_toggle_disable"/>
      <br>

      <input type = "password" name = "DL_toggle_PW" placeholder = "Password"/> 
      <input type = "submit" value = "Apply">

      <h3 class="Warning">Note: this function is solely for personal use, do not enable if server is shared</h3>
      
    </form>

    <!--Enable or disable online readers-->
    <form method = "POST" enctype = "multipart/form-data" id = "TOGR_form">
      <h3>Enable online readers?</h3>
      <p name = "Downloads enabled display">Readers are currently: </p>
      <label for = "TOGR_toggle_enable">Enabled</label>
      <input type = "checkbox" name = "TOGR_toggle_enable" value = "DL_toggle_enable"/>
      <label for = "TOGR_toggle_disable">Disabled</label>
      <input type = "checkbox" name = "TOGR_toggle_disable" value="DL_toggle_disable"/>
      <br>
      <input type = "password" name = "TOGR_toggle_PW" placeholder = "Password"/>
      <input type = "submit" value = "Apply">
    </form>

    <!--Add an IP to either the black or white list-->
    <form method = "POST" enctype="multipart/form-data" id = "IP_form">
      <h3>Manage IP lists</h3>
      <p>Please select a list and enter an IP to add.</p>
      <label for = "IP_Whitelist">Whitelist</label>
      <input type = "Radio" name = "IP_list_choice" id = "IP_Whitelist"/>
      <label for = "IP_Blacklist">Blacklist</label>
      <input type = "Radio" name = "IP_list_choice" id = "IP_Blacklist"/>
      <br>
      
      <input type = "text" name = "IP_list_add_Target" placeholder = "0.0.0.0"/>
      <br>

      <label for = "IP_list_add">Add</label>
      <input type = "Radio" name = "IP_list_add_or_rm" id = "IP_list_add"/>
      <label for = "IP_list_rm">Remove</label>
      <input type = "Radio" name = "IP_list_add_or_rm" id = "IP_list_rm"/>
      <br>
      
      <input type = "submit" value = "Change">            
    </form>

    <form method = "POST" enctype="multipart/form-data" id = "IPR_form">
      <h3>IP restrictions</h3>
      <p>Activate the whitelist, blacklist or neither</p>
      <label for = "IPR_Whitelist">Whitelist</label>
      <input type = "Radio" name = "IPR_list_choice" id = "IPR_Whitelist"/>
      <br>
      <label for = "IPR_Blacklist">Blacklist</label>
      <input type = "Radio" name = "IPR_list_choice" id = "IPR_Blacklist"/>
      <br>
      <label for = "IPR_None">None</label>
      <input type = "Radio" name = "IPR_list_choice" id = "IPR_None"/>
      <br>
      
      <input type = "submit" value = "Change"> 
      
  </form>
  </section>
</div>

</body>

<div id = "footer_container"></div>
<script src = "Assets/Scripts/Append_H&F.js"> </script>

<script>
//This script collects all the book info php left behind and creates an object from it.

  //Get and hide the folders and their associated books, move the pannel to the correct position
  const FOLDERS = document.getElementById("Book_collection");
  FOLDERS.style.display = "none";
  const controls = document.getElementById("Management_pannel");
  document.body.appendChild(controls)
  const footer = document.getElementById("footer_container");
  document.body.appendChild(footer)

  //spilt up the selects into folders, books and misc
  const SELECT_LIST = document.querySelectorAll('select');
  let folderSelects = [];
  let bookSelects = []; //TODO: check if this is redundant
  let miscFolders = [];
  for(let i = 0; i < SELECT_LIST.length; i++)
  {
    if(SELECT_LIST[i].getAttribute("name").includes("folder")){
      folderSelects.push(SELECT_LIST[i]);
    } else if (SELECT_LIST[i].getAttribute("name").includes("book")){
      bookSelects.push(SELECT_LIST[i]);
    } else{
      miscFolders.push(SELECT_LIST[i]);
    }
  }
    
  //populate the folder selects with all the folders
  let selectContents = "";
  const FOLDER_TITLES = document.querySelectorAll('h5');
  for(let i = 0; i < FOLDER_TITLES.length; i++){
    selectContents +='<option value = ' + FOLDER_TITLES[i].innerHTML.replace(":","")+ '>' + FOLDER_TITLES[i].innerHTML.replace(":","") + '</option>';
  }
  for(let i = 0; i < folderSelects.length; i++){
    folderSelects[i].innerHTML += selectContents;
  }

  //Add event listeners to each of the folder selects, to detect changes and populate their book folder acordingly
  for(let i = 0; i < folderSelects.length; i++){
    //Check if the folder select has a matching book folder
    let targetBookSelectName = folderSelects[i].getAttribute("name").substring(0,2) + "_book_select";
    let targetBookSelect =  document.getElementsByName(targetBookSelectName);

    if(targetBookSelect.length != 0){
      folderSelects[i].addEventListener('change',function(){
        //Find the right folder
        let bookSelectContents = "";
        let Folders = document.querySelectorAll('h5');
        for(let x = 0; x < Folders.length; x++){
          if(this.options[this.selectedIndex].text == Folders[x].innerHTML.replace(":","")){
            //Once found, go to it's sibling list and collect the books
            let bookList = Folders[x].nextSibling.childNodes;
            for (y = 0; y < bookList.length; y++){
              bookSelectContents +='<option value = ' + bookList[y].innerHTML.replace(":","")+ '>' + bookList[y].innerHTML.replace(":","") + '</option>';
              //console.log(bookList[y].innerHTML);
            }
          }       
        }
        //Add the books to the matching book select
        let bookSelectName = this.getAttribute("name").substring(0,2) + "_book_select";
        let targetBookSelect = "";
        targetBookSelect = document.getElementsByName(bookSelectName); 
        targetBookSelect[0].innerHTML = bookSelectContents;
      });
    }
    }

  //Case by case handling for the misc selects
    

</script>
<script src = "Assets/Scripts/Call_endpoints.js"></script>

</html>