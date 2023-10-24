<?php
    //$files = array_filter($_FILES['inpFiles'],$_POST['UF_name']); 

    //Create a folder for the books, using the name the user provided
    //TODO: get new folder name, set up try catch
    if(isset($_FILES['UF_inp_Files']))
    {
      $folder = "../../Books/";
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
      
          //Upload the file into the temp dir
          if(move_uploaded_file($tmpFilePath, $newFilePath)) {
            //Handle  here
      
          }
        }
      }
    }
    else{
      echo("Input file not set, this is likely because the file is too large, the limit is ~30MB");
    }
?>