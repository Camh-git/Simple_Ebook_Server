<?php 
    #Fetch every folder in books   
    $path = "\Books\\".DIRECTORY_SEPARATOR."*";
	$Folders = glob($path,GLOB_ONLYDIR);
	print_r($Folders);
	#$path = __dir__.DIRECTORY_SEPARATOR."*.{pdf,epub}";	
	
	$Collumn_num = 1;
	#Show the contents of every book folder
	foreach ($Folders as $dir)
	{
		#Get and print the folder name
		$Title = substr($dir,6);
		Print_r("<h3>".$Title.":</h3>");
		$content = glob("".$dir."/{*.*}",GLOB_BRACE);
		
		#List the books
		echo('<ul>');
		foreach($content as $book)
		{
			$Name = str_replace('_',' ', pathinfo($book,PATHINFO_FILENAME));			
			echo('<li><a href = "'.$book.'">'.$Name.'</a></li>');
		}
		echo('</ul>');
		
		#Increment through collumns to spread the lists out, reset if @ limit
		$collumn_num++;
		if ($Collumn_num >=4)
		{
			$Collumn_num = 0;
		}		
	}
?>