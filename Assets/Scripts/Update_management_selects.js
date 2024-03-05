async function get_data(url) {
  //For when the book data is updated, new single source of truth for book info and thumbnails
  const req = await fetch(url);
  const data = await req.json();
  return data;
}

async function Pop_management_selects(regen_books = true, regen_thumbs = true) {
  //Reset the selects and handle the folder selects
  const SELECT_LIST = document.querySelectorAll("select");
  const BOOK_DATA = await get_data(
    `http://${document.cookie.split("=")[1]}:5000/get-book-and-thumb-data`
  );
  if (regen_books) {
    for (let select of SELECT_LIST) {
      select.innerHTML = "<option>No selection</option>";
      //Populate the folder list
      if (select.getAttribute("name").includes("folder")) {
        for (const folder of BOOK_DATA.Books.Folders) {
          const option = document.createElement("option");
          option.value = option.textContent = folder.Folder_name;
          select.appendChild(option);
        }
        //Replace the old listener, this makes sure the latest list/ map is used
        select.removeEventListener("change", function () {});
        select.addEventListener("change", function () {
          let targetBookSelect = document.getElementsByName(
            this.getAttribute("name").substring(0, 2) + "_book_select"
          );
          if (typeof targetBookSelect[0] !== "undefined") {
            //Find the right folder and add the books
            targetBookSelect[0].innerHTML = "<option>No selection</option>";
            for (const folder of BOOK_DATA.Books.Folders) {
              if (this.options[this.selectedIndex].text == folder.Folder_name) {
                for (const book of folder.Books) {
                  try {
                    if (book.Title.length > 1) {
                      const option = document.createElement("option");
                      option.value = option.textContent =
                        book.Title + book.Extension;
                      targetBookSelect[0].appendChild(option);
                    }
                  } catch {
                    console.log(
                      "Tried to read invalid title for book: " + book.Title
                    );
                  }
                }
              }
            }
          }
        });
      }
    }
  }
  //Case by case handling for the misc selects
  if (regen_thumbs) {
    for (let select of SELECT_LIST) {
      if (select.getAttribute("name").includes("TH_fold")) {
        select.innerHTML = "<option>No selection</option>";
        for (const folder of BOOK_DATA.Thumbs.Folders) {
          const option = document.createElement("option");
          option.value = option.textContent = folder.Folder_name;
          select.appendChild(option);
        }

        select.removeEventListener("change", function () {});
        select.addEventListener("change", function () {
          let targetThumbSelect = document.getElementById(
            "TH_img_select_" + select.getAttribute("name").slice(-2)
          );
          targetThumbSelect.innerHTML = "<option>No selection</option>";
          for (const folder of BOOK_DATA.Thumbs.Folders) {
            if (this.options[this.selectedIndex].text == folder.Folder_name) {
              for (const img of folder.Images) {
                if (img != "NA" && img != "" && !img.includes("http")) {
                  const option = document.createElement("option");
                  option.value = option.textContent = img.split(/[/]+/).pop();
                  targetThumbSelect.appendChild(option);
                }
              }
            }
          }
        });
      }
    }
  }
}

Pop_management_selects();
