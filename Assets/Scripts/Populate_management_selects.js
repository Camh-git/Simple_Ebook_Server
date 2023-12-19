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
  const BOOK_MAP = await get_map(`http://192.168.1.110:5000/json-list-books`);
  console.log(BOOK_MAP);

  //Reset the selects and handle the folder selects
  const SELECT_LIST = document.querySelectorAll("select"); //TODO: check this works

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
          this.getAttribute("name").substring(0, 2) + "_book_select" //TODO: investigate why using the select var here instead of this allways results in TH
        );
        if (typeof targetBookSelect !== "undefined") {
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
  //Case by case handling for the misc selects
  const Thumb_select = document.getElementById("TH_new_select");
  for (image in THUMB_MAP.Images) {
    const option = document.createElement("option");
    option.value = option.textContent = image.Name + image.ext;
    Thumb_select.appendChild(option);
  }
}

Pop_management_selects();
