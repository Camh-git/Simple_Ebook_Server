async function Populate_book_collection() {
  const Book_folder = document.getElementById("Book_collection");
  const lib_content = await fetch(`http://192.168.1.110:5000/list-books`);
  Book_folder.innerHTML = await lib_content.json();
}
Populate_book_collection();
