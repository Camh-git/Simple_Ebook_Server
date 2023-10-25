<?php
  #Fetch every folder in books
  $full = true;
  $path = "\Books\\".DIRECTORY_SEPARATOR."*";
	$Folders = glob($path,GLOB_ONLYDIR);
  $output = "<div id=`folder_info_container`>";
  
  for($content as $book){
    
        
  }

  $output .= "</div>";
  echo($output);
?>