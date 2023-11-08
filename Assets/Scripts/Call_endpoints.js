function Assign_submit_actions() {
  //Get the submit btns/forms and assign their actions to the functions

  //Manage books
  document.getElementById("DS_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[2];
    let Book = event.target.children[5];
    Call_delete_book(
      Folder.options[Folder.selectedIndex].innerHTML,
      Book.options[Book.selectedIndex].innerHTML.split(".")[0],
      Book.options[Book.selectedIndex].innerHTML.split(".")[1]
    );
  });
  document.getElementById("RS_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[2];
    let Book = event.target.children[5];
    let New_name = event.target.children[7];
    Call_rename_book(
      Book.options[Book.selectedIndex].innerHTML.split(".")[0],
      Book.options[Book.selectedIndex].innerHTML.split(".")[1],
      Folder.options[Folder.selectedIndex].innerHTML,
      New_name.value
    );
  });

  //Manage folders
  document.getElementById("DF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[2];
    let Delete = event.target.children[6];
    if (Delete.checked) {
      Delete = true;
    } else {
      Delete = false;
    }
    Call_delete_folder(Folder.options[Folder.selectedIndex].innerHTML, Delete);
  });
  document.getElementById("RF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[1];
    let New_name = event.target.children[2];
    Call_rename_folder(
      Folder.options[Folder.selectedIndex].innerHTML,
      New_name.value
    );
  });

  //Manage Library
  document.getElementById("CF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Name = event.target.children[1];
    Call_create_folder(Name.value);
  });
  document
    .getElementById("MV_folder_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let Book = event.target.children[5];
      let Old_folder = event.target.children[2];
      let New_folder = event.target.children[8];
      Call_MV_folder(
        Book.options[Book.selectedIndex].innerHTML.split(".")[0],
        Book.options[Book.selectedIndex].innerHTML.split(".")[1],
        Old_folder.options[Old_folder.selectedIndex].innerHTML,
        New_folder.options[New_folder.selectedIndex].innerHTML
      );
    });

  //Manage thumbnails
  document
    .getElementById("TH_select_form")
    .addEventListener("submit", (event) => {});
  document
    .getElementById("TH_upload_form")
    .addEventListener("submit", (event) => {});
  document
    .getElementById("TH_format_form")
    .addEventListener("submit", (event) => {});

  //Misc options
  document
    .getElementById("DL_toggle_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      const Code = event.target.children[7];
      const Toggle = document.querySelector(
        "input[type='radio'][name=DL_toggle]:checked"
      ).value;
      Call_toggle_downloads(Toggle, Code.value);
    });
  document.getElementById("TOGR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[7];
    const Toggle = document.querySelector(
      "input[type='radio'][name=Reader_toggle]:checked"
    ).value;
    Call_toggle_readers(Toggle, Code.value);
  });
  document.getElementById("IP_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const IP = event.target.children[7];
    const Code = event.target.children[8];
    const List = document.querySelector(
      "input[type='radio'][name=IP_list_choice]:checked"
    ).value;
    const Action = document.querySelector(
      "input[type='radio'][name=IP_list_add_or_rm]:checked"
    ).value;
    Call_manage_ip_lists(IP.value, List, Action, Code.value);
  });
  document.getElementById("IPR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[11];
    const List = document.querySelector(
      "input[type='radio'][name=IPR_list_choice]:checked"
    ).value;
    Call_toggle_ip_lists(List, Code.value);
  });
}

/*Calling the API*/
const ADDRESS = "http://192.168.1.110:5000/";

//Manage books
function Call_upload_book(bookName) {}
function Call_delete_book(folder, book, ext) {
  fetch(`${ADDRESS}delete-book/${book}&&${ext}&&${folder}`);
}
function Call_rename_book(name, ext, folder, newName) {
  fetch(`${ADDRESS}rename-book/${name}&&${ext}&&${folder}&&${newName}`);
}

//Manage folders
function Call_upload_folder(folderName, contents) {}
function Call_delete_folder(folderName, RMContent) {
  fetch(`${ADDRESS}delete-folder/${folderName}&&${RMContent}`);
}
function Call_rename_folder(oldName, newName) {
  fetch(`${ADDRESS}rename-folder/${oldName}&&${newName}`);
}

//Manage library
function Call_create_folder(name) {
  fetch(`${ADDRESS}create-folder/${name}`);
}
function Call_MV_folder(name, ext, oldFolder, newFolder) {
  fetch(
    `${ADDRESS}move-book-to-folder/${name}&&${ext}&&${oldFolder}&&${newFolder}`
  );
}

//Manage thumbnails
function Call_re_assign_thumb(folder, book, thumb) {}
function Call_upload_thumb(image) {}
function Call_clear_or_repop_thumb_cache(option) {}

//Misc options
function Call_toggle_downloads(option, code) {
  fetch(`${ADDRESS}toggle-dl/${option}&&${code}`);
}
function Call_toggle_readers(option, code) {
  fetch(`${ADDRESS}toggle-readers/${option}&&${code}`);
}
function Call_manage_ip_lists(target, list, option, code) {
  fetch(`${ADDRESS}manage-acls/${target}&&${list}&&${option}&&${code}`);
}
function Call_toggle_ip_lists(option, code) {
  fetch(`${ADDRESS}toggle-lists/${option}&&${code}`);
}

Assign_submit_actions();
