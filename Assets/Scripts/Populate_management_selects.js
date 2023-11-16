async function Pop_management_selects() {
  //This script collects book info and creates an object from it.
  const Book_folder = document.getElementById("Book_collection");
  const lib_content = await fetch(`http://192.168.1.110:5000/list-books`);
  Book_folder.innerHTML = await lib_content.json();

  //Get and hide the folders and their associated books, move the pannel to the correct position
  const FOLDERS = document.getElementById("Book_collection");
  FOLDERS.style.display = "none";
  const controls = document.getElementById("Management_pannel");
  document.body.appendChild(controls);
  const footer = document.getElementById("footer_container");
  document.body.appendChild(footer);

  //clear any existing entries, spilt up the selects into folders, books and misc
  const SELECT_LIST = document.querySelectorAll("select");
  for (let i = 0; i < SELECT_LIST.length; i++) {
    SELECT_LIST[i].innerHTML = "<option>No selection</option>";
  }
  let folderSelects = [];
  let bookSelects = []; //TODO: check if this is redundant
  let miscFolders = [];
  for (let i = 0; i < SELECT_LIST.length; i++) {
    if (SELECT_LIST[i].getAttribute("name").includes("folder")) {
      folderSelects.push(SELECT_LIST[i]);
    } else if (SELECT_LIST[i].getAttribute("name").includes("book")) {
      bookSelects.push(SELECT_LIST[i]);
    } else {
      miscFolders.push(SELECT_LIST[i]);
    }
  }

  //populate the folder selects with all the folders
  let selectContents = "";
  const FOLDER_TITLES = document.getElementsByClassName("book_list_title");
  console.log(FOLDER_TITLES.length);
  for (let i = 0; i < FOLDER_TITLES.length; i++) {
    selectContents +=
      "<option value = " +
      FOLDER_TITLES[i].innerHTML.replace(":", "") +
      ">" +
      FOLDER_TITLES[i].innerHTML.replace(":", "") +
      "</option>";
  }
  for (let i = 0; i < folderSelects.length; i++) {
    folderSelects[i].innerHTML += selectContents;
  }

  //Add event listeners to each of the folder selects, to detect changes and populate their book folder acordingly
  for (let i = 0; i < folderSelects.length; i++) {
    //Check if the folder select has a matching book folder
    let targetBookSelectName =
      folderSelects[i].getAttribute("name").substring(0, 2) + "_book_select";
    let targetBookSelect = document.getElementsByName(targetBookSelectName);

    if (targetBookSelect.length != 0) {
      folderSelects[i].addEventListener("change", function () {
        //Find the right folder
        let bookSelectContents = "";
        let Folders = document.querySelectorAll("h5");
        for (let x = 0; x < Folders.length; x++) {
          if (
            this.options[this.selectedIndex].text ==
            Folders[x].innerHTML.replace(":", "")
          ) {
            //Once found, go to it's sibling list and collect the books
            let bookList = Folders[x].nextSibling.childNodes;
            for (let y = 0; y < bookList.length; y++) {
              bookSelectContents +=
                "<option value = " +
                bookList[y].innerHTML.replace(":", "") +
                ">" +
                bookList[y].innerHTML.replace(":", "") +
                "</option>";
              //console.log(bookList[y].innerHTML);
            }
          }
        }
        //Add the books to the matching book select
        let bookSelectName =
          this.getAttribute("name").substring(0, 2) + "_book_select";
        let targetBookSelect = "";
        targetBookSelect = document.getElementsByName(bookSelectName);
        targetBookSelect[0].innerHTML = bookSelectContents;
      });
    }
  }

  //Case by case handling for the misc selects
}

Pop_management_selects();
