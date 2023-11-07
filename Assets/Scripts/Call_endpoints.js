function Assign_submit_actions() {
  //Get the submit btns/forms and assign their actions to the functions
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
}

//Manage books
function Call_upload_book() {}
function Call_delete_book(Folder, Book, ext) {
  fetch(
    "http://192.168.1.110:5000/delete-book/" + Book + "&&" + ext + "&&" + Folder
  );
}
function Call_rename_book() {}

//Manage folders
function Call_upload_folder() {}
function Call_delete_folder() {}
function Call_rename_folder() {}

//Manage library
function Call_create_folder() {}
function Call_MV_folder() {}

//Manage thumbnails
function Call_re_assign_thumb() {}
function Call_clear_or_repop_thumb_cache() {}

//Misc options
function Call_toggle_downloads() {}
function Call_toggle_readers() {}
function Call_manage_ip_lists() {}

Assign_submit_actions();
