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
  document.getElementById("RS_form").addEventListener("submit", (event) => {});

  //Manage folders
  document.getElementById("DF_form").addEventListener("submit", (event) => {});
  document.getElementById("RF_form").addEventListener("submit", (event) => {});

  //Manage Library
  document.getElementById("CF_form").addEventListener("submit", (event) => {});
  document
    .getElementById("MV_folder_form")
    .addEventListener("submit", (event) => {});

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
    .addEventListener("submit", (event) => {});
  document
    .getElementById("TOGR_form")
    .addEventListener("submit", (event) => {});
  document.getElementById("IP_form").addEventListener("submit", (event) => {});
  document.getElementById("IPR_form").addEventListener("submit", (event) => {});
}

//Manage books
function Call_upload_book(bookName) {}
function Call_delete_book(folder, book, ext) {
  fetch(
    "http://192.168.1.110:5000/delete-book/" + book + "&&" + ext + "&&" + folder
  );
}
function Call_rename_book(name, ext, folder, newName) {}

//Manage folders
function Call_upload_folder(folderName, contents) {}
function Call_delete_folder(folderName, RMContent) {}
function Call_rename_folder(oldName, newName) {}

//Manage library
function Call_create_folder(name) {}
function Call_MV_folder(name, ext, oldFolder, newFolder) {}

//Manage thumbnails
function Call_re_assign_thumb(folder, book, thumb) {}
function Call_upload_thumb(image) {}
function Call_clear_or_repop_thumb_cache(option) {}

//Misc options
function Call_toggle_downloads(option, code) {}
function Call_toggle_readers(option, code) {}
function Call_manage_ip_lists(option, code) {}
function Call_toggle_ip_lists(address, list, option, code) {}

Assign_submit_actions();
