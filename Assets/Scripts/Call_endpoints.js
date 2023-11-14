function Assign_submit_actions() {
  //Get the submit btns/forms and assign their actions to the functions

  //Manage books
  document.getElementById("DS_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[2];
    let Book = event.target.children[5];
    Call_and_display(
      `${ADDRESS}delete-book/${
        Book.options[Book.selectedIndex].innerHTML.split(".")[0]
      }&&${Book.options[Book.selectedIndex].innerHTML.split(".")[1]}&&${
        Folder.options[Folder.selectedIndex].innerHTML
      }`
    );
  });
  document.getElementById("RS_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[2];
    let Book = event.target.children[5];
    let New_name = event.target.children[7];
    Call_and_display(
      `${ADDRESS}rename-book/${
        Book.options[Book.selectedIndex].innerHTML.split(".")[0]
      }&&${Book.options[Book.selectedIndex].innerHTML.split(".")[1]}&&${
        Folder.options[Folder.selectedIndex].innerHTML
      }&&${New_name.value}`
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
    Call_and_display(
      `${ADDRESS}delete-folder/${
        Folder.options[Folder.selectedIndex].innerHTML
      }&&${Delete}`
    );
  });

  document.getElementById("RF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[1];
    let New_name = event.target.children[2];
    Call_and_display(
      `${ADDRESS}rename-folder/${
        Folder.options[Folder.selectedIndex].innerHTML
      }&&${New_name.value}`
    );
  });

  //Manage Library
  document.getElementById("CF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Name = event.target.children[1];
    Call_and_display(`${ADDRESS}create-folder/${Name.value}`, true);
  });

  document
    .getElementById("MV_folder_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let Book = event.target.children[5];
      let Old_folder = event.target.children[2];
      let New_folder = event.target.children[8];

      Call_and_display(
        `${ADDRESS}move-book-to-folder/${
          Book.options[Book.selectedIndex].innerHTML.split(".")[0]
        }&&${Book.options[Book.selectedIndex].innerHTML.split(".")[1]}&&${
          Old_folder.options[Old_folder.selectedIndex].innerHTML
        }&&${New_folder.options[New_folder.selectedIndex].innerHTML}`
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
      Call_and_display(`${ADDRESS}toggle-dl/${Toggle}&&${Code.value}`);
    });

  document.getElementById("TOGR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[7];
    const Toggle = document.querySelector(
      "input[type='radio'][name=Reader_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}toggle-readers/${Toggle}&&${Code.value}`);
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
    Call_and_display(
      `${ADDRESS}manage-acls/${IP.value}&&${List}&&${Action}&&${Code.value}`
    );
  });

  document.getElementById("IPR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[11];
    const List = document.querySelector(
      "input[type='radio'][name=IPR_list_choice]:checked"
    ).value;
    Call_and_display(
      `${ADDRESS}toggle-lists/${List}&&${Code.value}`,
      false,
      true
    );
  });

  //Allow the user to close the response popup
  DISPLAY.addEventListener("click", (event) => {
    DISPLAY.style.display = "none";
  });
}

//sending the requests and handling the responses
async function Call_and_display(
  requestString,
  update_lib_selects = false,
  show_ip_lists = false
) {
  const result = await fetch(requestString);
  const data = await result.json();

  DISPLAY.style.display = "block";
  let response = "Response:<br>";
  switch (data) {
    case 200:
      response += "Success, the changes you requested have been made.";
      break;
    case 400:
      response +=
        "Request error: Please make sure all required fields are filled in.";
      break;
    case 401:
      response +=
        "Unathorised: This action requires authentication, please enter the correct password.";
      break;
    case 403:
      response +=
        "Forbidden: Users are not allowed to rename or delete the Misc and upload folders";
      break;
    case 404:
      response +=
        "Not found: Please make sure that the book or folder you are accessing exists and hasn't been moved or renamed." +
        "<br> If this error occured when using any of the forms in the 'Misc options' row please let the developer know.";
      break;
    case 406:
      response +=
        "Not acceptable: Please use documentation or the forms to ensure you send the correct arguments.";
      break;
    case 409:
      response +=
        "Conflict: Please make sure there isn't a book or folder that already has that name.<br> If you saw this while editing the ACLs then this ip is probably already on a list.";
      break;
    case 410:
      response +=
        "Gone: The value you wish to remove is not in the targeted list.";
      break;
    case 428:
      response +=
        "Warning: One or more of the books moved to /Misc had the MOVED tag applied, meaning a book with an identical name was already present" +
        ", please resolve the conflict and remove the MOVED tag to avoid potential book loss in future merges.";
      break;
    case 500:
      response +=
        "Server error: please contact the developer with the following data:" +
        data;
      break;
    case 501:
      response +=
        "Not implemented: This feature isn't ready yet, but you can always check " +
        "<a href='https://github.com/Camh-git/Simple_Ebook_Server'>Our github</a> for updates";
      "";
      break;
    default:
      response += "No pre-prepared message, status: " + data;
  }
  DISPLAY.children[0].innerHTML = "<h2>click to close<h2><br>" + response;

  //Handle optional params
  if (update_lib_selects) {
    Book_folder = document.getElementById("Book_collection");
    const lib_content = await fetch(`${ADDRESS}list-books`);
    Book_folder.innerHTML = await lib_content.json();
  }
  if (show_ip_lists) {
    //Get settings
    //Show lists in tables
    //Show which list is active
  }
}

const ADDRESS = "http://192.168.1.110:5000/";
const DISPLAY = document.getElementById("Req_status_modal");
Assign_submit_actions();
