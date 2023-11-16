<?php
    #This code was originaly found in Management.php
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
        #TODO: consider re-implementing this, but having it tidy up the source files aswell so they can still be manipulated
        $Name = pathinfo($book,PATHINFO_BASENAME);
        /*
		    $Name = str_replace('_',' ', pathinfo($book,PATHINFO_BASENAME ));	
			  {
				  $Name[0] = strtoupper($Name[0]);
			  }
			  catch(Exception $e) {
				  echo "<script>console.log('Failed to capitalise a title with error:".$e->getMessage()."')</script>";
			  }*/
        $Output .= '<li>'.$Name.'</li>';
      }
      $Output .='</ul></div>';

    }
    $Output .="</div>";
		#This output is echoed onto the screen so it can be manipulated by JS
		echo($Output);
?>