async function get_map(url) {
  try {
    const req = await fetch(url);
    const data = await req.json();
    return data;
  } catch {
    console.log(`Failed to call:${url}, will use placeholders if possible`);
    return 500;
  }
}

async function Populate_library_entries() {
  //Get the thumnail and book lists
  const BOOK_DATA = await get_map(
    `http://${document.cookie.split("=")[1]}:5000/get-book-data`
  );
  const THUMB_MAP = await get_map(
    `http://${document.cookie.split("=")[1]}:5000/thumb-map`
  );
  const BOOK_MAP = await get_map(
    `http://${document.cookie.split("=")[1]}:5000/list-books`
  );
  //Check that the books where found, display count if so, or notice if not
  try {
    console.log("Total number of folders found: " + BOOK_MAP.Books.length);
  } catch {
    const notice = document.createElement("h2");
    notice.textContent = `Sorry, the book list could not be found. Please make sure the book API is active and that you can contact the server.`;
    const ip_check = document.createElement("h3");
    ip_check.textContent = `Attempted to call the server at the address: ${
      document.cookie.split("=")[1]
    }, if this is incorrect please go to the mangement page and set the correct address.`;
    notice.appendChild(ip_check);
    document.getElementById("Landing-segment").appendChild(notice);
    return;
  }
  //Get the collumns we will be adding the folders to
  const col_1 = document.getElementById("Col_1");
  const col_2 = document.getElementById("Col_2");
  const col_3 = document.getElementById("Col_3");
  const col_4 = document.getElementById("Col_4");
  let col_num = 0;

  for (list of BOOK_MAP.Books) {
    //Create the folder and it's toogle button
    const FOLDER_CONTAINER = document.createElement("ul");
    FOLDER_CONTAINER.classList.add("Lib_folder");
    const header = document.createElement("h2");
    header.innerHTML = list.Folder;
    FOLDER_CONTAINER.appendChild(header);

    const toggle_img = document.createElement("img");
    toggle_img.src = "../Assets/Images/expand_more_white_24dp.svg";
    toggle_img.alt = "Expand/retract book list";
    header.appendChild(toggle_img);

    header.addEventListener("click", function (e) {
      toggle_entries(e);
    });

    //Add the books
    for (let book of list.Content) {
      const BOOK_CONTAINER = document.createElement("li");
      BOOK_CONTAINER.Name = "Book_entry";
      BOOK_CONTAINER.classList.add("Lib_entry");

      //Add the thumb div and thumbnail (or placeholder if not available)
      const thumb_div = document.createElement("div");
      thumb_div.classList.add("Thumb");
      const thumb_image = document.createElement("img");
      thumb_image.alt = `Thumbnail for: ${list.Folder}/${book.Name}`;

      //Set the book's thumbnail, or select an appropriate the placeholder if not found
      let thumb_url = "";
      for (let i of THUMB_MAP.Images) {
        if (book.Name.toUpperCase() == i.Name.toUpperCase()) {
          thumb_url = "../Assets/Images/Thumbnail_cache/" + i.Name + i.ext;
        }
        if (thumb_url != "") {
          thumb_image.src = thumb_url;
        } else {
          switch (book.ext.toUpperCase()) {
            case ".PDF":
              thumb_image.src = "../Assets/Images/Icons/Icon_pdf_file.png";
              break;
            case ".TXT":
              thumb_image.src = "../Assets/Images/Icons/Text-txt.png";
              break;
            case ".EPUB":
              thumb_image.src = "../Assets/Images/Icons/Epub_logo.png";
              break;
            case ".MOBI":
              thumb_image.src = "../Assets/Images/Icons/Icon_mobi_file.png";
              break;
            case ".AZW3":
              thumb_image.src = "../Assets/Images/Icons/kindle_app_icon.png";
              break;
            case ".HTML":
              thumb_image.src = "../Assets/Images/Icons/HTML5_logo_black.png";
              break;
            default:
              thumb_image.src =
                "../Assets/Images/Icons/library_books_FILL0.svg";
              break;
          }
        }
      }
      thumb_div.appendChild(thumb_image);
      BOOK_CONTAINER.appendChild(thumb_div);

      //Add details div and the name
      const details_div = document.createElement("div");
      details_div.classList.add("Details");

      const book_title = document.createElement("h4");
      book_title.innerHTML = book.Name;
      details_div.appendChild(book_title);

      //Add the file type display and colour it acording to support level
      const type_display = document.createElement("p");
      type_display.innerHTML = book.ext;

      //Fetch the file support table and check the book's extension against it
      const table_data = await fetch("../Assets/File_type_support.json").then(
        (res) => {
          return res.json();
        }
      );
      if (JSON.stringify(table_data).includes(book.ext) && book.ext != "") {
        //^Is this check needed?
        for (let format of table_data.fileTypes) {
          if (format.extension == book.ext) {
            //Add the appropriate colour based on the support level, not a switch because includes are needed
            if (format.support.includes("Readable")) {
              type_display.style.color = "green";
            } else if (format.support.includes("Downloadable")) {
              type_display.style.color = "yellow";
            } else if (format.support.includes("Not supported")) {
              type_display.style.color = "red";
            } else {
              type_display.style.color = "white";
            }
          }
        }
      }
      details_div.appendChild(type_display);

      //Add the download button
      const download_button = document.createElement("a");
      download_button.href = `../Books/${list.Folder}/${book.Name}${book.ext}`;
      download_button.textContent = "Download";
      details_div.appendChild(download_button);

      //Append the details to the book and the completed book to the folder
      BOOK_CONTAINER.appendChild(details_div);
      FOLDER_CONTAINER.appendChild(BOOK_CONTAINER);
    }

    //Append the completed folder to the correct collumn and advance the counter
    switch (col_num) {
      case 0:
        col_1.appendChild(FOLDER_CONTAINER);
        break;
      case 1:
        col_2.appendChild(FOLDER_CONTAINER);
        break;
      case 2:
        col_3.appendChild(FOLDER_CONTAINER);
        break;
      case 3:
        col_4.appendChild(FOLDER_CONTAINER);
        break;
      default:
        console.log("Error, tried writting to collumn: " + col_num);
    }
    col_num += 1;
    if (col_num > 3) {
      col_num = 0;
    }
  }

  //Hide the missing spaces in titles warning, if one has not been applied
  const missing_title_spaces = document.getElementById("Title_spaces_missing");
  if (missing_title_spaces == null) {
    let Warnings = document.getElementsByClassName("Missing_space_warning");
    for (let warning of Warnings) {
      warning.innerHTML = "";
    }
  } else {
    let Parent = missing_title_spaces.parentElement;
    Parent.removeChild(missing_title_spaces);
  }

  console.log("Library setup complete");
}

function toggle_entries(e) {
  let list, img, head;
  if (e.target.tagName == "IMG") {
    list = e.target.parentNode.parentNode.getElementsByTagName("li");
    img = e.target;
    head = e.target.parentNode;
  } else {
    list = e.target.parentNode.getElementsByTagName("li");
    img = e.target.getElementsByTagName("img")[0];
    head = e.target;
  }

  if (list[0].style.display == "flex") {
    for (entry of list) {
      entry.style.display = "none";
    }
    img.src = "../Assets/Images/expand_more_white_24dp.svg";
    img.style.background = head.style.background = "#737373";
  } else {
    for (entry of list) {
      entry.style.display = "flex";
    }
    img.src = "../Assets/Images/expand_less_white_24dp.svg";
    img.style.background = head.style.background = "#1e596f";
  }
}

Populate_library_entries();
