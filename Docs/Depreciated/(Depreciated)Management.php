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
		    $Name = str_replace('_',' ', pathinfo($book,PATHINFO_FILENAME));	
			  try
			  {
				  $Name[0] = strtoupper($Name[0]);
			  }
			  catch(Exception $e) {
				  echo "<script>console.log('Failed to capitalise a title with error:".$e->getMessage()."')</script>";
			  }
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
  <h1>This page is currently under construction</h1>
  <!--Note on input names: Each input name has a prefix related to it's form eg: inputs for delete single have the prefix DS_-->
  <!-- TODO: 
    form actions, see each form
    Add thumbnail management form(auto fetch and manualy assgin/upload thumbs)
    Investigate adding a completion popup
  -->

  <!--Manage books-->
  <h2>Manage individual books</h2>
  <div class = "flex-container Management_row">
    <!--upload single, todo:Add a folder select-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Upload_single.php">
      <h3>Upload book</h3>
      <input type = "file" name = "US_file_inp" accept = ".epub,.pdf,.txt,.doc,.docx"/>
	    <input type = "submit" value = "upload" />
	    <p class = "Warning">Max upload size: 30MB</p>
    </form>

    <!--Delete single-->
    <!--TODO: make this send a variable with the filename-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Delete_single.php">
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
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Rename_file.php">
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
      <br>
      <input type = "submit" value = "Submit" />
    </form>
  </div>

  <!--Manage folders-->
  <h2>Manage folders</h2>
  <div class="flex-container Management_row">
    <!--Upload folder TODO: make this take a name for the folder, fix upload -->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Upload_folder.php">
      <h3>Upload folder</h3>
      <input type = "text" name = "UF_name" placeholder = "name">
	    <p>Please add each file you want to upload(if none please use create folder)</p>
	    <input type = "file" name = "UF_inp_Files[]" multiple = "multiple" accept = ".epub,.pdf,.txt,.doc,.docx"/>
      <input type = "submit" value = "upload" />
    </form>

    <!--Delete folder TODO:double check this works with new naming-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Delete_folder.php">
      <h3>Delete folder</h3>
      <label for = "DF_folder_select">Select folder</label>
      <select name = "DF_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <br>
      <input type = "submit" value = "Submit" />
      <br>
      <input type = "checkbox" name = "DS_Delete_content" value = "DS_Delete_content"/>
      <label for = "DS_Delete_content">Delete folder content?(will move contents to misc if not checked)</label>
    </form>

    <!--Rename folder TODO: fix the path compilation, add the rename function-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Rename_folder.php"> 
      <h3>Rename folder</h3>
      <label for = "RR_folder_select">Select folder</label>
      <!--
      <select name = "RF_folder_select">
        <option Value = "None">No selection</option>
      </select>
      -->
      <br>
      <input type = "text" name = "RF_folder_select" placeholder = "Temp_target"/>
      <input type = "text" name = "RF_New_name" placeholder = "New name"/>
      <br>
      <input type = "submit" value = "Submit" />
    </form>

  </div>

  <!--Manage libray-->
  <h2>Manage library</h2>
  <div class = "flex-container Management_row">
    <!--Create empty folder TODO:find a way to fix the permissions issue-->
    <form method = "POST"  enctype = "multipart/form-data" action = "Assets/Scripts/Create_folder.php">
      <h3>Create new folder</h3>
      <input type = "text" name = "CF_Name" placeholder = "Enter name here"/>
      <br>
      <input type = "submit" value = "Submit">
    </form>
    
    <!--Move book between folders-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Move_book.php">
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

  </div>

  <!--Manage thumbnails-->
  <h2>Manage Thumbnails</h2>
  <div class = "flex-container Management_row">
    <!--Manage thumbnails TODO:write this-->
    <form method = "POST" enctype="multipart/form-data" action = "Assets/Scripts/Set_thumbnail.php">
      <h3>Re-assign Thumbnails</h3>
      <label for = "TH_folder_select">Folder</label>
      <select name = "TH_folder_select">
        <option Value = "None">No selection</option>
      </select>
      <label for = "TH_book_select">Book</label>
      <select name = "TH_book_select">
        <option Value = "None">No selection</option>
      </select>
      <br>

      <h4>Select an existing thumbnail or upload a new one.</h4>
      <select name = "Thumb_new_select">
        <option Value = "None">No selection</option>
      </select>
      <input type = "file" name = "Thumb_upload" accept = ".png,.jpg,.jpeg,.svg,.gif,.webp,.xcf,.psd"/>
      <br>

      <input type = "submit" value = "Change"/>
    </form>

    <!--Format thumbnail cache TODO:write this-->
    <form method = "POST" enctype="multipart/form-data" action = "">
      <h3>Delete/populate thumbnail cache</h3>
      <p>
        Clearing the cache will remove all thumbnails, they will be 
        re-generated when you next visit the libary page.
        <br>
        Re-populate will automaticaly empty and then refill the folder 
      </p>
      <label for = "Thumb_delete_all">Clear cache</label>
      <input type = "Radio" name = "Thumb_cache_format" id = "Thumb_delete_all"/>
      <br>
      <label for = "Thumb_regen">Repopulate cache</label>
      <input type = "Radio" name = "Thumb_cache_format" id = "Thumb_regen"/>
      <h4 class = "Warning">
        WARNING:<br> This action removes files and cannot be undone.
      </h4>
      <input type = "submit" value = "Start"/>
    </form>

  </div>

  <!--Misc options-->
  <h2>Misc options</h2>
  <div class = "flex-container Management_row">
    <!--Enable or disable downloads-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Toggle_downloads.php">
      <h3>Enable downloads?</h3>
      <p name = "Downloads enabled display">Downloads are currently: </p>
      <br>
      <label for = "DL_toggle_enable">Enabled</label>
      <input type = "checkbox" name = "DL_toggle_enable" value = "DL_toggle_enable"/>
      <label for = "DL_toggle_disable">Disabled</label>
      <input type = "checkbox" name = "DL_toggle_disable" value="DL_toggle_disable"/>
      <br>
      <input type = "password" name = "DL_toggle_PW" placeholder = "Password"/>      
      <h3 class="Warning">Note: this function is solely for personal use, do not enable if server is shared</h3>
      <input type = "submit" value = "Apply">
    </form>

    <!--Enable or disable online readers-->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Toggle_readers.php">
      <h3>Enable online readers?</h3>
      <p name = "Downloads enabled display">Readers are currently: </p>
      <br>
      <label for = "TOGR_toggle_enable">Enabled</label>
      <input type = "checkbox" name = "TOGR_toggle_enable" value = "DL_toggle_enable"/>
      <label for = "TOGR_toggle_disable">Disabled</label>
      <input type = "checkbox" name = "TOGR_toggle_disable" value="DL_toggle_disable"/>
      <br>
      <input type = "password" name = "TOGR_toggle_PW" placeholder = "Password"/>
      <br>   
      <input type = "submit" value = "Apply">
    </form>

    <!--Add an IP to either the black or white list-->
    <form method = "POST" enctype="multipart/form-data" action = "Assets/Scripts/Add_to_list.php">
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

  </div>
</div>

</body>

<div id = "footer_container"></div>
<script src = "Assets/Scripts/Append_H&F.js"> </script>

<script>
  //This script collects all the book info php left behind and creates an object from it.

    //Get and hide the folders and their associated books, move the pannel to the correct position
    let Folders = document.getElementById("Book_collection");
    Folders.style.display = "none";
    const controls = document.getElementById("Management_pannel");
    document.body.appendChild(controls)
    const footer = document.getElementById("footer_container");
    document.body.appendChild(footer)

    //spilt up the selects into folders and books
    let select_list = document.querySelectorAll('select');
    let folder_selects = [];
    let book_selects = []; //TODO: check if this is redundant
    let misc_folders = [];
    for(let i = 0; i < select_list.length; i++)
    {
      if(select_list[i].getAttribute("name").includes("folder")){
        folder_selects.push(select_list[i]);
      } else if (select_list[i].getAttribute("name").includes("book")){
        book_selects.push(select_list[i]);
      } else{
        misc_folders.push(select_list[i]);
      }
    }
    
    //populate the folders selects with all the folders
    let select_contents = "";
    let folder_titles = document.querySelectorAll('h5');
    for(let i = 0; i < folder_titles.length; i++){
      select_contents +='<option value = ' + folder_titles[i].innerHTML.replace(":","")+ '>' + folder_titles[i].innerHTML.replace(":","") + '</option>';
    }
    for(let i = 0; i < folder_selects.length; i++){
      folder_selects[i].innerHTML += select_contents;
    }

    //Add event listeners to each of the folder selects, to detect changes and populate their book folder acordingly
    for(let i = 0; i < folder_selects.length; i++){
      //Check if the folder select has a matching book folder
      let target_book_select_name = folder_selects[i].getAttribute("name").substring(0,2) + "_book_select";
      let target_book_select =  document.getElementsByName(target_book_select_name); 
      if(target_book_select.length != 0){
        folder_selects[i].addEventListener('change',function(){
          //Find the right folder
          let book_select_contents = "";
          let Folders = document.querySelectorAll('h5');
          for(let x = 0; x < Folders.length; x++){
            if(this.options[this.selectedIndex].text == Folders[x].innerHTML.replace(":","")){
              //Once found, go to it's sibling list and collect the books
              let book_list = Folders[x].nextSibling.childNodes;
              for (y = 0; y < book_list.length; y++){
                book_select_contents +='<option value = ' + book_list[y].innerHTML.replace(":","")+ '>' + book_list[y].innerHTML.replace(":","") + '</option>';
                //console.log(book_list[y].innerHTML);
              }
           }       
          }
          //Add the books to the matching book select
          let book_select_name = this.getAttribute("name").substring(0,2) + "_book_select";
          let Target_book_select = "";
          Target_book_select = document.getElementsByName(book_select_name); 
          Target_book_select[0].innerHTML = book_select_contents;
        });
      }
    }

    //Case by case handling for the misc selects
    

</script>

</html>
