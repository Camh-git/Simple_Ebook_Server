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
async function Pop_management_selects() {
  //Get the thumnail and book lists
  const THUMB_MAP = await get_map(`http://192.168.1.110:5000/thumb-map`);
  const BOOK_MAP = await get_map(`http://192.168.1.110:5000/list-books`);
  try {
    console.log("Total number of folders found: " + BOOK_MAP.Books.length);
  } catch {
    document.getElementById("Management_pannel").innerHTML =
      "<h1>Management</h1>" +
      "<h3>Sorry, the call to the API to fetch the folders failed. The controls have been hidden to prevent any incorrect comands from being sent.</h3>" +
      "<h4>Please make sure the book API is active and that you can contact the server.</h4>";
    return;
  }

  //Reset the selects and handle the folder selects
  const SELECT_LIST = document.querySelectorAll("select");

  for (select of SELECT_LIST) {
    select.innerHTML = "<option>No selection</option>";
    //Populate the folder list
    if (select.getAttribute("name").includes("folder")) {
      for (folder of BOOK_MAP.Books) {
        const option = document.createElement("option");
        option.value = option.textContent = folder.Folder;
        select.appendChild(option);
      }
      //Add listener
      select.addEventListener("change", function () {
        let targetBookSelect = document.getElementsByName(
          this.getAttribute("name").substring(0, 2) + "_book_select"
        );
        if (typeof targetBookSelect !== "undefined") {
          //Find the right folder and add the books
          targetBookSelect[0].innerHTML = "<option>No selection</option>";
          for (folder of BOOK_MAP.Books) {
            if (this.options[this.selectedIndex].text == folder.Folder) {
              for (book of folder.Content) {
                const option = document.createElement("option");
                option.value = option.textContent = book.Name + book.ext; //TODO: drop the ext from the displayed text once the handlers are re- configured
                targetBookSelect[0].appendChild(option);
              }
            }
          }
        }
      });
    }
  }
  //Case by case handling for the misc selects
  const Thumb_selects = document.getElementsByName("TH_select");
  for (image of THUMB_MAP.Images) {
    for (select of Thumb_selects) {
      const option = document.createElement("option");
      option.value = option.textContent = image.Name + image.ext;
      select.appendChild(option);
    }
  }
}

Pop_management_selects();
