<?php
  //TODO: fix path compliation, add rename
  if(isset($_POST["RF_select"], $_POST["RF_RF_New_name"]))
  {
    try
    {
      //Extract the path from the old address
      $path_components = explode("\\",$_POST["RF_select"]);
      $file_path = "";
      $i = count($path_components) - 1;
      echo("<script>console.log('parts: '".$i.")</script>");
      foreach($path_components as $part)
      {
        if ($i > 0)
        {
          $file_path += $part;
          --$i;
        }
      }
      echo("<script>console.log('path: '".$file_path.")</script>");

      //Add the path to the new address and rename the folder
      $Final_name = $path + $_POST["RF_New_name"];

    }
    catch(Exception $e)
    {
      echo("Folder rename failed with the following exception: " .$e);
    }
  }
  else
  {
    echo("Missing either the target folder or the new name, please go to the management page to rename a folder.");
    try{
      echo($_POST["RF_select"]);
    } 
    catch(Exception $e){}
    try{
      echo($_POST["RF_New_name"]);
    } 
    catch(Exception $e){}
  }
?>
