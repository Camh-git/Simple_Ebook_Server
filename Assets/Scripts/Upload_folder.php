<?php
    //Create a folder for the books, using the name the user provided
    if(isset($_FILES['UF_inp_Files']))
    {
      try{
        $folder = "../../Books/".$_POST["UF_name"]."/";
        mkdir($folder);

        //upload the files
        $total = count($_FILES['UF_inp_Files']['name']);
        for( $i=0 ; $i < $total ; $i++ ) {

          //Get the temp file path
          $tmpFilePath = $_FILES['UF_inp_Files']['tmp_name'][$i];
      
          //Make sure we have a file path
          if ($tmpFilePath != ""){
            //Setup our new file path
            $newFilePath = $folder . $_FILES['UF_inp_Files']['name'][$i];
      
            //Upload the file to it's dir
            if(move_uploaded_file($tmpFilePath, $newFilePath)) {} 
          }
        }
        readfile("../Confirmation_messages/Upload_folder_success.html");
      }
      catch(Exception $e) {
        echo $e->getMessage();
      }
  }
  else{
    echo("Input file not set, this is likely because the file is too large, the limit is ~30MB");
  }
?>