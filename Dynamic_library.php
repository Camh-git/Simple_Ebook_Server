<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">	
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>	
		<link rel="stylesheet" href="Assets/StyleSheet.css"/>
		<link rel="icon" href="Assets/Images/favicon.ico" />	
		<title>EBook Library</title>    
</head>
<div id = "header_container"> </div>

<body>
<!--TODO: 
    Implement thumbnail extractions and readers for each file format
    un-comment the failed to get thumbnail console logs once implemented
-->
<div id = "Landing-segment">
	<h1>Dynamic library</h1>
	<p>
		File formats are displayed for each title, green means full
		functionality (download and browser based reader), yellow means 
		supported but no reader, red means not supported (will still download).
	</p>
    <h4 class = 'Missing-space-warning'>Some books may be missing spaces in their titles, check the console for a list.</h4>
</div>
<div id="Library-collumns">
	<div id = "Col_1" class = "collumn"></div>
	<div id = "Col_2" class = "collumn"></div>
	<div id = "Col_3" class = "collumn"></div>
	<div id = "Col_4" class = "collumn"></div>
</div>

</body>
<div id = "Book_content" class = "Display-none"></div>
<div id = "Thumb_collection" class = "Display-none"></div>
<script src = "Assets/Scripts/Populate_library_entries.js"></script>
<div id = "footer_container"></div>
<script src = "Assets/Scripts/Append_H&F.js"> </script>
</html>