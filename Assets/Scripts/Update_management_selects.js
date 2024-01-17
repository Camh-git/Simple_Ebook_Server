async function get_map(url) {
  const req = await fetch(url);
  const data = await req.json();
  return data;
}

async function Pop_management_selects(regen_books = true, regen_thumbs = true) {
  //Reset the selects and handle the folder selects
  const SELECT_LIST = document.querySelectorAll("select");
  if (regen_books) {
    const BOOK_MAP = await get_map(
      `http://${document.cookie.split("=")[1]}:5000/list-books`
    );
    for (let select of SELECT_LIST) {
      select.innerHTML = "<option>No selection</option>";
      //Populate the folder list
      if (select.getAttribute("name").includes("folder")) {
        for (let folder of BOOK_MAP.Books) {
          const option = document.createElement("option");
          option.value = option.textContent = folder.Folder;
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
            for (folder of BOOK_MAP.Books) {
              if (this.options[this.selectedIndex].text == folder.Folder) {
                for (book of folder.Content) {
                  const option = document.createElement("option");
                  option.value = option.textContent = book.Name + book.ext;
                  targetBookSelect[0].appendChild(option);
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
    const THUMB_MAP = await get_map(
      `http://${document.cookie.split("=")[1]}:5000/thumb-map`
    );
    const Thumb_selects = document.getElementsByName("TH_select");
    for (let select of Thumb_selects) {
      for (let image of THUMB_MAP.Images) {
        const option = document.createElement("option");
        option.value = option.textContent = image.Name + image.ext;
        select.appendChild(option);
      }
    }
  }
}

Pop_management_selects();
