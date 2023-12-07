async function Populate_library_entries() {
  //Get the thumnail list
  const Thumb_list = document.getElementById("Thumb_collection");
  const Thumb_content = await fetch(`http://192.168.1.110:5000/list-thumbs`);
  const Thumb_info = await Thumb_content.json();
  Thumb_list.innerHTML = Thumb_info;

  //Getting the book list from the API
  const Book_list = document.getElementById("Book_content");
  const lib_content = await fetch(`http://192.168.1.110:5000/list-books`);
  let Book_info = await lib_content.json();

  //Manipulate the returned book lists to match the expected formatting, fetch the thumbnails, write and colour the file type and add the download button
  Book_info = Book_info.replaceAll("h5", "h2")
    .replaceAll("/h5", "/h2")
    .replaceAll("<ul", "<ul name = 'Book_folder'")
    .replaceAll("<li", "<li name = 'Book_entry'");
  Book_list.innerHTML = Book_info;

  const Lists = document.getElementsByName("Book_entry");
  for (item of Lists) {
    //Save the filename, clear the div and add it's class
    const parent_folder =
      item.parentElement.parentElement.children[0].innerHTML;
    const content = item.innerHTML;
    item.innerHTML = "";
    item.classList.add("Lib_entry");

    //Add thumb div
    const Thumb_div = document.createElement("div");
    Thumb_div.classList.add("Thumb");
    item.appendChild(Thumb_div);

    //Add details div, add the name back
    const Details_div = document.createElement("div");
    Details_div.classList.add("Details");
    item.appendChild(Details_div);

    const header = document.createElement("h4");
    header.innerHTML = content;
    Details_div.appendChild(header);

    //Add file type and colour it
    const file_type = item.children[1].innerHTML.slice(
      item.children[1].innerHTML.lastIndexOf("."),
      item.children[1].innerHTML.lastIndexOf("<")
    );
    const type_display = document.createElement("p");
    type_display.innerHTML = file_type;
    switch (file_type.toUpperCase()) {
      case ".PDF":
        type_display.style.color = "green";
        break;
      case ".TXT":
      case ".EPUB":
      case ".MOBI":
      case ".AZW3":
        type_display.style.color = "yellow";
        break;
      case ".HTML":
        type_display.style.color = "red";
        break;
      default:
        type_display.style.color = "white";
    }
    item.children[1].appendChild(type_display);

    //Add the download button
    const download_button = document.createElement("a");
    download_button.href = `./Books/${parent_folder}/${content}`;
    download_button.textContent = "Download";
    item.children[1].appendChild(download_button);

    //Add thumnail image
    const thumb_image = document.createElement("img");
    thumb_image.alt = `Thumbnail for: ${content}`;
    //check the thumbnail list for the book's specific thumbnail, use a generic image if not found

    if (1 == 2) {
    } else {
      switch (file_type.toUpperCase()) {
        case ".PDF":
          thumb_image.src = "./Assets/Images/Icons/Icon_pdf_file.png";
          break;
        case ".TXT":
          thumb_image.src = "./Assets/Images/Icons/Text-txt.png";
          break;
        case ".EPUB":
          thumb_image.src = "./Assets/Images/Icons/Epub_logo.png";
          break;
        case ".MOBI":
          thumb_image.src = "./Assets/Images/Icons/Icon_mobi_file.png";
          break;
        case ".AZW3":
          thumb_image.src = "./Assets/Images/Icons/logo-azw3-2101145464.png";
          break;
        case ".HTML":
          thumb_image.src = "./Assets/Images/Icons/HTML5_logo_black.png";
          break;
        default:
          thumb_image.src = "./Assets/Images/Icons/library_books_FILL0.svg";
          break;
      }
    }
    item.children[0].appendChild(thumb_image);
  }
  const FOLDERS = document.getElementsByClassName("Book_folder");
  console.log("Total number of folders found: " + FOLDERS.length);

  const COL_1 = document.getElementById("Col_1");
  const COL_2 = document.getElementById("Col_2");
  const COL_3 = document.getElementById("Col_3");
  const COL_4 = document.getElementById("Col_4");
  let Col_num = 0;

  //Distributing the lists we stored in 'Folders' into the collumns
  for (let item of FOLDERS) {
    switch (Col_num) {
      case 0:
        COL_1.innerHTML += item.innerHTML;
        break;

      case 1:
        COL_2.innerHTML += item.innerHTML;
        break;

      case 2:
        COL_3.innerHTML += item.innerHTML;
        break;
      case 3:
        COL_4.innerHTML += item.innerHTML;
        break;

      default:
        console.log("Error, tried writting to collumn: " + Col_num);
    }
    Col_num += 1;
    if (Col_num > 3) {
      Col_num = 0;
    }
  }

  //Removing the lists left by php
  while (FOLDERS.length > 0) {
    FOLDERS[0].parentNode.removeChild(FOLDERS[0]);
  }

  //Add colour coding to show the support levels of each file type
  let types = document.getElementsByClassName("LS_Type_ind");
  for (let t of types) {
    if (t.innerHTML === "pdf") {
      t.style.color = "green";
    } else if (t.innerHTML === "epub") {
      t.style.color = "yellow";
    } else {
      {
        t.style.color = "red";
      }
    }
  }

  //Hide the missing spaces in titles warning, if one has not been applied
  const MissingTitleSpaces = document.getElementById("Title_spaces_missing");
  if (MissingTitleSpaces == null) {
    let Warnings = document.getElementsByClassName("Missing_space_warning");
    for (let warning of Warnings) {
      warning.innerHTML = "";
    }
  } else {
    let Parent = MissingTitleSpaces.parentElement;
    Parent.removeChild(MissingTitleSpaces);
  }
  console.log("Library setup complete");
}
Populate_library_entries();
