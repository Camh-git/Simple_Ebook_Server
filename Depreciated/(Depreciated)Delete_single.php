<?php
  //TODO: let this take a variable path
  if(isset($_FILES['targetFile']))
  {
    $file = $_FILES["targetFile"];
    $path = include dirname(__FILE__).'../../'.basename($_FILES["targetFile"]["name"]);

    #$path="../../Books/Misc/tonight_will_be_the.pdf";
    try{
      unlink($path);
      echo("File deleted");
      //Send the user to the success screen
      readfile("../Confirmations,modals,popups/Single_delete_success_page.html");
    } catch (Exception $e){
      echo("Delete single failed with error: " . $e->getMessage());
    }
  } else{
    echo("Target file not set");
  }
?>