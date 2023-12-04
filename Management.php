<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">	
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>	
    <link rel="stylesheet" href="Assets/StyleSheet.css"/>
    <link rel="icon" href="Assets/Images/favicon.ico" />
  </head>
	
<div id = "header_container"></div>
<body>
<div id = "Management_pannel">
  <h1>Management</h1>
  <!--Note on input names: Each input name has a prefix related to it's form eg: inputs for delete single have the prefix DS_-->
  <!-- TODO: Swap the upload book and folder forms over to the python approach when ready -->

  <section id = "Req_status_modal">
    <div id="Req_status_modal_body">
      <p>Click anywhere in the background to close this popup</P>
    </div>
  </section>

  <!--Manage books-->
  
  <h2>Manage individual books</h2>
  <section class = "Management-row">
    <!--upload single, todo:Add a folder select-->
    <form method = "POST" enctype = "multipart/form-data" id = "US_form" action = "Assets/Scripts/Upload_single.php">
      <h3>Upload book</h3>
      <input type = "file" name = "US_file_inp" accept = ".epub,.pdf,.txt,.doc,.docx"/>
      <br/>
	    <input type = "submit" value = "upload" />
	    <p class = "Warning">Max upload size: 30MB</p>
    </form>

    <!--Delete single-->
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

    <!--Rename single-->
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
      <br>
      <input type = "submit" value = "Submit" />
    </form>
  </section>

  <!--Manage folders-->
  <h2>Manage folders</h2>
  <section class=" Management-row">
    <!--Upload folder -->
    <form method = "POST" enctype = "multipart/form-data" action = "Assets/Scripts/Upload_folder.php">
      <h3>Upload folder</h3>
      <input type = "text" name = "UF_name" placeholder = "name">
	    <p>Please add each file you want to upload(if none please use create folder)</p>
	    <input type = "file" name = "UF_inp_Files[]" multiple = "multiple" accept = ".epub,.pdf,.txt,.doc,.docx"/>
      <br>
      <input type = "submit" value = "upload" />
    </form>

    <!--Delete folder-->
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
      <label for = "DS_Delete_content" class = "alwaysShow">Delete folder content?(Content will be moved to misc if not checked)</label>
    </form>

    <!--Rename folder-->
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
  <section class = "Management-row">
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
  <section class = "Management-row">
    <!--Manage thumbnails-->
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

      <label for = "TH_new_select">Select new image.</label>
      <select name = "TH_new_select" id = "TH_new_select">
        <option Value = "None">No selection</option>
      </select>
      <br>
      <br>

      <input type = "submit" value = "Change"/>
    </form>

    <!--Upload thumbnail -->
    <form method = "POST" enctype="multipart/form-data" id = "TH_upload_form" action = "Assets/Scripts/Upload_thumb.php">
      <h3>Upload a thumbnail</h3>
      <input type = "file" name = "New_thumb_inp" accept = ".png,.jpg,.jpeg,.svg,.gif,.webp,.xcf,.psd"/>
      <br>
      <input type = "submit" value = "Upload"/>
    </form>
    <!-- -->

    <!--Format thumbnail cache-->
    <form method = "POST" enctype="multipart/form-data" id = "TH_format_form">
      <h3>Delete/populate thumbnail cache</h3>
      <p>
        Clearing the cache will remove all thumbnails, they will be 
        re-generated when you next visit the libary page.
      </p>
      <p>Re-populate will automaticaly empty and then refill the folder</p>

      
      <label for = "Thumb_regen" class = "alwaysShow">Repopulate cache</label>
      <input type = "checkbox" name = "Thumb_cache_format" id = "Thumb_regen" checked = "True"/> 
      <br>
      
      <label for = "Thumb_rm_manual" class = "alwaysShow">Remove manual additions</label>
      <input type = "checkbox" name = "Thumb_cache_format" id = "Thumb_rm_manual"/>
      <br>
      
      <input type = "submit" value = "Start"/>
      <h3 class = "Warning">
        WARNING: This action removes files.
      </h3>
    </form>

  </section>

  <!--Misc options-->
  <h2>Misc options</h2>
  <section class = "Management-row">
    <!--Enable or disable downloads-->
    <form method = "POST" enctype = "multipart/form-data" id = "DL_toggle_form">
      <h3>Enable downloads?</h3>

      <p name = "Downloads enabled display">Downloads should be: </p>
      <label for = "DL_toggle_enable" class = "alwaysShow">Enabled</label>
      <input type = "Radio" name = "DL_toggle" value = "True"/>
      <label for = "DL_toggle_disable" class = "alwaysShow">Disabled</label>
      <input type = "Radio" name = "DL_toggle" value = "False"/>
      <br>

      <input type = "password" name = "DL_toggle_PW" placeholder = "Password"/> 
      <input type = "submit" value = "Apply">

      <h3 class="Warning">Note: This function is solely for personal use, do not enable if server is shared</h3>
      
    </form>

    <!--Enable or disable online readers-->
    <form method = "POST" enctype = "multipart/form-data" id = "TOGR_form">
      <h3>Enable online readers?</h3>
      <p name = "Downloads enabled display">Readers should be: </p>
      <label for = "TOGR_toggle_enable" class = "alwaysShow">Enabled</label>
      <input type = "Radio" name = "Reader_toggle" value = "True"/>
      <label for = "TOGR_toggle_disable" class = "alwaysShow">Disabled</label>
      <input type = "Radio" name = "Reader_toggle" value = "False"/>
      <br>
      <input type = "password" name = "TOGR_toggle_PW" placeholder = "Password"/>
      <input type = "submit" value = "Apply">
    </form>

    <!--Add an IP to either the black or white list-->
    <form method = "POST" enctype="multipart/form-data" id = "IP_form">
      <h3>Manage IP lists</h3>
      <p>Please select a list and enter an IP to add.</p>
      <label for = "IP_Whitelist" class = "alwaysShow">Whitelist</label>
      <input type = "Radio" name = "IP_list_choice" value = "Whitelist"/>
      <label for = "IP_Blacklist" class = "alwaysShow">Blacklist</label>
      <input type = "Radio" name = "IP_list_choice" value = "Blacklist"/>
      <br>
      
      <input type = "text" name = "IP_list_add_Target" placeholder = "0.0.0.0"/>
      <input type = "password" name = "IP_list_code" placeholder = "Password"/>
      <br>

      <label for = "IP_list_add" class = "alwaysShow">Add</label>
      <input type = "Radio" name = "IP_list_add_or_rm" value = "ADD"/>
      <label for = "IP_list_rm" class = "alwaysShow">Remove</label>
      <input type = "Radio" name = "IP_list_add_or_rm" value = "REMOVE"/>
      <br>
      
      <input type = "submit" value = "Change">            
    </form>

    <form method = "POST" enctype="multipart/form-data" id = "IPR_form">
      <h3>IP restrictions</h3>
      <p>Activate the whitelist, blacklist or neither</p>
      <label for = "IPR_Whitelist" class = "alwaysShow">Whitelist</label>
      <input type = "Radio" name = "IPR_list_choice" value = "Whitelist"/>
      <br>
      <label for = "IPR_Blacklist" class = "alwaysShow">Blacklist</label>
      <input type = "Radio" name = "IPR_list_choice" value = "Blacklist"/>
      <br>
      <label for = "IPR_None" class = "alwaysShow">None</label>
      <input type = "Radio" name = "IPR_list_choice" value = "None"/>
      
      <br>      
      <input type = "password" name = "IPR_list_code" placeholder = "Password"/>
      <br>
      
      <input type = "submit" value = "Change"> 
      
  </form>
  
  </section>
  
  <!--Toggle management options-->
  <h2>Management options</h2>
  <section class = "Management-row">
    <!-- Main enable or disable of all management forms -->
    <form method = "POST" enctype="multipart/form-data" id = "MNT_form">
      <h3>Enable management</h3>
      <p>Select if the remote management tools can be used or not</p>
      <label for = "MNT_list_choice" class = "alwaysShow"> Enable </label>
      <input type = "Radio" name = "MNT_toggle" value = "True"/>
      <br>
      <label for = "MNT_list_choice" class = "alwaysShow">Disable</label>
      <input type = "Radio" name = "MNT_toggle" value = "False"/>

      <br>
      <input type = "password" name = "MNT_code" placeholder = "Password"/>
      <br>
      <input type = "submit" value = "Change">

    </form>

    <!-- Disable or enable upload forms -->
    <form method = "POST" enctype="multipart/form-data" id = "MNU_form">
      <h3>Enable Upload</h3>
      <p>Select if the Upload forms can be used</p>
      <label for = "MNU_list_choice" class = "alwaysShow"> Enable </label>
      <input type = "Radio" name = "MNU_toggle" value = "True"/>
      <br>
      <label for = "MNU_list_choice" class = "alwaysShow">Disable</label>
      <input type = "Radio" name = "MNU_toggle" value = "False"/>

      <br>
      <input type = "password" name = "MNU_code" placeholder = "Password"/>
      <br>
      <input type = "submit" value = "Change">

    </form>

    <!-- Disable or enable delete forms -->
    <form method = "POST" enctype="multipart/form-data" id = "MND_form">
      <h3>Enable Delete</h3>
      <p>Select if the delete forms can be used</p>
      <label for = "MND_list_choice" class = "alwaysShow"> Enable </label>
      <input type = "Radio" name = "MND_toggle" value = "True"/>
      <br>
      <label for = "MND_list_choice" class = "alwaysShow">Disable</label>
      <input type = "Radio" name = "MND_toggle" value = "False"/>

      <br>
      <input type = "password" name = "MND_code" placeholder = "Password"/>
      <br>
      <input type = "submit" value = "Change">
      
    </form>

     <!-- Disable or enable rename forms -->
     <form method = "POST" enctype="multipart/form-data" id = "MNR_form">
      <h3>Enable rename</h3>
      <p>Select if the rename forms can be used</p>
      <label for = "MNR_list_choice" class = "alwaysShow"> Enable </label>
      <input type = "Radio" name = "MNR_toggle" value = "True"/>
      <br>
      <label for = "MNR_list_choice" class = "alwaysShow">Disable</label>
      <input type = "Radio" name = "MNR_toggle" value = "False"/>

      <br>
      <input type = "password" name = "MNR_code" placeholder = "Password"/>
      <br>
      <input type = "submit" value = "Change">
      
    </form>

     <!-- Disable or enable move forms -->
     <form method = "POST" enctype="multipart/form-data" id = "MNM_form">
      <h3>Enable Move</h3>
      <p>Select if the move book/thumb forms can be used</p>
      <label for = "MNM_list_choice" class = "alwaysShow"> Enable </label>
      <input type = "Radio" name = "MNM_toggle" value = "True"/>
      <br>
      <label for = "MNM_list_choice" class = "alwaysShow">Disable</label>
      <input type = "Radio" name = "MNM_toggle" value = "False"/>

      <br>
      <input type = "password" name = "MNM_code" placeholder = "Password"/>
      <br>
      <input type = "submit" value = "Change">
      
    </form>
  </section>
</div>

</body>
<div id = "footer_container"></div>
<div id = "Thumb_collection" class = "Display-none"></div>
<div id = "Book_collection" class = "Display-none"></div>
<script src = "Assets/Scripts/Append_H&F.js"> </script>
<script src = "./Assets/Scripts/Populate_management_selects.js"></script>
<script src = "Assets/Scripts/Call_endpoints.js"></script>

</html>