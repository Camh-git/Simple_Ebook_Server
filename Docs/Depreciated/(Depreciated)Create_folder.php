<?php
if(isset($_POST["New_folder"]))
{
  try{
    mkdir("../../Books/" . $_POST["New_folder"]);
    readfile("../Confirmations,modals,popups/Create_folder_success_page.html");
  } catch (Exception $e){
    echo("Error creating directory, please try again, if the problem persists let the developer know.");
    echo("Error message:" . $e->getMessage());
  }

}else{
  echo("No new folder name set, please go to the management page to add a new folder.");
}
?>