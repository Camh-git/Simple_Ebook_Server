<?php
  if(isset($_FILES['New_thumb_inp']))
  {
    //var_dump($_FILES); #For debug, disable in production
    try{
      $file = $_FILES["New_thumb_inp"];
      $targetPath="../../Assets/Images/Thumbnail_cache/".basename($file["name"]);
    
      if(copy($file['tmp_name'],$targetPath))
      {
        echo("Thumbnail uploaded to: /".basename($_FILES["New_thumb_inp"]["name"]));
      }
      //Send the user to the success screen
      readfile("../Confirmation_messages/Upload_thumb_success.html");
    }
    catch(Exception $e) {
      echo $e->getMessage();
    }
  } else {
    echo("Input file not set, this is likely because the file is too large, the limit is ~30MB");
  }
?>