<?php
  if(isset($_FILES['US_file_inp']))
  {
    //var_dump($_FILES); #For debug, disable in production
    try{
      $file = $_FILES["US_file_inp"];
      $targetPath="../../Books/Uploads/".basename($file["name"]);
    
      if(copy($file['tmp_name'],$targetPath))
      {
        echo("<br><br><h3>Book uploaded to: Uploads/".basename($_FILES["US_file_inp"]["name"])."</h3>");
      }
      //Send the user to the success screen
      readfile("../Confirmation_messages/Upload_book_success.html");
    }
    catch(Exception $e) {
      echo $e->getMessage();
    }
  } else {
    echo("Input file not set, this is likely because the file is too large, the limit is ~30MB");
  }
?>