async function get_data(url) {
  try {
    const req = await fetch(url);
    const data = await req.json();
    return data;
  } catch {
    console.log(`Failed to call:${url}, will use placeholders if possible`);
    return 500;
  }
}

function fetch_placeholder_thumb(ext) {
  try {
    ext = ext.toUpperCase();
  } catch {}

  switch (ext) {
    case ".PDF":
      return "../Assets/Images/Icons/Icon_pdf_file.png";
    case ".TXT":
      return "../Assets/Images/Icons/Text-txt.png";
    case ".EPUB":
      return "../Assets/Images/Icons/Epub_logo.png";
    case ".MOBI":
      return "../Assets/Images/Icons/Icon_mobi_file.png";
    case ".AZW3":
      return "../Assets/Images/Icons/kindle_app_icon.png";
    case ".HTML":
      return "../Assets/Images/Icons/HTML5_logo_black.png";
    default:
      return "../Assets/Images/Icons/library_books_FILL0.svg";
  }
}

function check_and_format_data(data) {
  if (
    data == "" ||
    data == "." ||
    data == "/" ||
    data.toUpperCase() == "NA" ||
    data.toUpperCase() == "UNDEFINED"
  ) {
    return "????";
  } else {
    return data;
  }
}

async function Populate_library_entries() {
  //Get the thumnail and book lists
  const LIB_DATA = await get_data(
    `http://${document.cookie.split("=")[1]}:5000/get-book-and-thumb-data`
  );

  const FILE_SUPPORT_DATA = await fetch(
    "../Assets/File_type_support.json"
  ).then((res) => {
    return res.json();
  });

  //Check that the books where found, display count if so, or notice if not
  try {
    console.log(
      "Total number of folders found: " + LIB_DATA.Books.Folders.length
    );
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

  for (book_folder of LIB_DATA.Books.Folders) {
    //Create the folder and it's toogle button
    const FOLDER_CONTAINER = document.createElement("ul");
    FOLDER_CONTAINER.classList.add("Lib_folder");
    const header = document.createElement("h2");
    header.innerHTML = book_folder.Folder_name;
    FOLDER_CONTAINER.appendChild(header);

    const toggle_img = document.createElement("img");
    toggle_img.src = "../Assets/Images/expand_more_white_24dp.svg";
    toggle_img.alt = "Expand/retract book list";
    header.appendChild(toggle_img);

    header.addEventListener("click", function (e) {
      toggle_entries(e);
    });

    //Add the books
    for (let book of book_folder.Books) {
      const BOOK_CONTAINER = document.createElement("li");
      BOOK_CONTAINER.Name = "Book_entry";
      BOOK_CONTAINER.classList.add("Lib_entry");

      //Add the thumb div and thumbnail (or placeholder if not available)
      const thumb_div = document.createElement("div");
      thumb_div.classList.add("Thumb");
      const thumb_image = document.createElement("img");
      thumb_image.alt = `Thumbnail for: ${book_folder.Folder}/${book.Title}`;

      //Set the book's thumbnail, or select an appropriate the placeholder if not found
      thumb_image.onerror = fetch_placeholder_thumb(book.Extension);

      let thumb_url = "." + book.Thumbnail;
      if (
        thumb_url != "." &&
        thumb_url != ".NA" &&
        !thumb_url.toUpperCase().includes(".UNDEFINED") &&
        !thumb_url.toUpperCase().includes("HTTP")
      ) {
        thumb_image.src = thumb_url;
      } else {
        thumb_image.src = fetch_placeholder_thumb(book.Extension);
      }
      thumb_div.appendChild(thumb_image);
      BOOK_CONTAINER.appendChild(thumb_div);

      //Add details div and it's content
      const details_div = document.createElement("div");
      details_div.classList.add("Details");

      const book_title = document.createElement("h4");
      book_title.innerHTML = book.Title;
      details_div.appendChild(book_title);

      const date_author_and_pub_display = document.createElement("p");
      date = check_and_format_data(book.Date.slice(0, 4));
      publisher = check_and_format_data(book.Publisher);

      authors = "";
      try {
        switch (book.Authors.length) {
          case 0:
            authors = "Unknown";
            break;
          case 1:
            authors = book.Authors[0];
            break;
          case 2:
            authors = `${book.Authors[0]}, ${book.Authors[1]}`;
            break;
          default:
            authors = `${book.Authors[0]} et al.`;
            break;
        }
      } catch {
        authors = "Unknown";
      }

      if (publisher == authors) {
        date_author_and_pub_display.innerHTML = `${date}, ${authors}<br>`;
      } else {
        date_author_and_pub_display.innerHTML = `${date}, ${authors}, ${publisher}<br>`;
      }

      details_div.appendChild(date_author_and_pub_display);

      //Add the file type display and colour it acording to support level
      const type_display = document.createElement("p");
      type_display.innerHTML = book.Extension;

      //Check the book's extension against the file support table
      for (let format of FILE_SUPPORT_DATA.fileTypes) {
        if (format.extension == book.Extension) {
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
      details_div.appendChild(type_display);

      //Add the isbn
      const ISBN_display = document.createElement("p");
      isbn = check_and_format_data(book.isbn13);
      if (isbn == "????") {
        isbn = check_and_format_data(book.isbn);
      }
      ISBN_display.innerHTML = book.isbn;
      details_div.appendChild(ISBN_display);

      //Add the download button
      const download_button = document.createElement("a");
      download_button.href = `../Books/${book_folder.Folder_name}/${book.Title}${book.Extension}`;
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
