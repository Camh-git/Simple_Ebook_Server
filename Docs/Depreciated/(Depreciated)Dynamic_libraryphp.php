<?php 
#Fetch every folder in books   
$path = "\Books\\".DIRECTORY_SEPARATOR."*";
$Folders = glob($path,GLOB_ONLYDIR);
	
$Collumn_num = 1;
$Missing_spaces = "";
#Show the contents of every book folder
foreach ($Folders as $dir){
	$Output = "<div class ='Book_folder'>";
	#Get and print the folder name
	$Title = substr($dir,6);
	$Output .='<h2>'.$Title.':</h2>';
	$content = glob("".$dir."/{*.*}",GLOB_BRACE);
		
	#List the books
	$Output .='<ul>';
	foreach($content as $book)
	{
		#Get the books name from it's filepath and tidy it up.
		$Name = str_replace('_',' ', pathinfo($book,PATHINFO_FILENAME));	
		try
		{
			$Name[0] = strtoupper($Name[0]);
		}
		catch(Exception $e) {
			echo "<script>console.log('Failed to capitalise a title with error:".$e->getMessage()."')</script>";
		}
		#Warn user if the title doesn't have many spaces
		if(substr_count($Name,' ') < strlen($Name)/9)
		{
			if(substr_count($Name," ") < 2) #So that short titles don't get caught
			{
				$Missing_spaces .= "  ".$Name."  ";
			}
		}
			
		#Lines 60 and 61 should not be merged, end needs a pointer reference, which should be from a var rather then itself, this will throw notices if done on 1 line   
		$type_raw = explode('.',$book); 
		$type = strtolower(end($type_raw));	
			
		#Getting the thumbnail and setting the header line to show the appropriate reader and placeholder thumbnail, both based on filetype
		#Note: most of these have the same header line as the default, this will change as readers are introduced
		#Note: The thumbnail is handled here so that if a unique image cannot be generated a placeholder appropriate to it's file type can be assigned.
		$Thumbnail = getThumb($book);
		$Thumbnail_alt = "";
		$Header_line = "";
		switch(pathinfo($book,PATHINFO_EXTENSION))
		{
			case "pdf":
				$Header_line = '<a class="List_title" href = "'.$book.'"target="_blank">'.$Name.'</a>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/Icon_pdf_file.png';
					$Thumbnail_alt = "Generic PDF thumbnail";
				}
				break;
			case "txt":
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/Text-txt.png';
					$Thumbnail_alt = "Generic TXT thumbnail";
				}
				break;
				
			case "epub":
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/Epub_logo.png';
					$Thumbnail_alt = "Generic EPUB thumbnail";
				}
				break;

			case "mobi":
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/Icon_mobi_file.png';
					$Thumbnail_alt = "Generic MOBI thumbnail";
				}
				break;

			case "azw3":
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/logo-azw3-2101145464.png';
					$Thumbnail_alt = "Generic AZW3 thumbnail";
				}
				break;

			case "html":
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				if ($Thumbnail == "Placeholder"){
					$Thumbnail = 'Assets/Images/Icons/HTML5_logo_black.png';
					$Thumbnail_alt = "Generic HTML thumbnail";
				}
				break;

			default:
				$Header_line = '<p1 class=List_title>'.$Name.'</p1>';
				$Thumbnail_alt = 'Generic' . pathinfo($book,PATHINFO_EXTENSION) . 'thumbnail';
				break;

			}
			#Set up the thumbnail
			$Output .= 
			'<li>
				<div class = "Thumb"><img src = "'.$Thumbnail.'" alt ="'.$Thumbnail_alt.'"></div>
				<div class = "Details">'.$Header_line.'<br><p1 class="LS_Type_ind">'.$type.'</p1>&emsp;<a href ="'.$book.'" download="'.$Name.'">Download</a></div>
			</li>';
			//$Output .= '<li><a class="List_title" href = "'.$book.'"target="_blank">'.$Name.'</a><br><p1 class="List_Type_indicator">'.$type.'</p1><a href = "'.$book.'"></a></li>';
		}
		$Output .="</ul></div>";
		#This output is echoed onto the screen so it can be manipulated by JS
		echo($Output);
	}
	if(strlen($Missing_spaces) > 10)
	{
		echo("<p5 id = 'Title_spaces_missing'></p5>");
		echo("<script>console.log('The following titles might be missing some spaces: " .$Missing_spaces."')</script>");
	}

/**
* Take the path to a book, checks the chache and creates a thumbnail if needed, stores them in the thumbnail cache, returns the path to the file.
*/
function getThumb($Target){
	$Thumbnail = "Assets/Images/Thumbnail_cache/";
    try{
		throw new Exception("Not implemented");
    } 
    catch(Exception $e){
     	//echo "<script>console.log('Failed to get thumbnail for: ".$Target." with error:".$e->getMessage()."')</script>";
		$Thumbnail = "Placeholder";
    }
    return($Thumbnail);
}

?>