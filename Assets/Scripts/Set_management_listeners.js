import { Call_and_display } from "./Call_and_display.js";

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
      }`,
      true
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
      }&&${New_name.value}`,
      true
    );
  });

  //Manage folders
  document.getElementById("DF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[1];
    let Delete = event.target.children[5];
    if (Delete.checked) {
      Delete = true;
    } else {
      Delete = false;
    }
    Call_and_display(
      `${ADDRESS}delete-folder/${
        Folder.options[Folder.selectedIndex].innerHTML
      }&&${Delete}`,
      true
    );
  });

  document.getElementById("RF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Folder = event.target.children[1];
    let New_name = event.target.children[2];
    Call_and_display(
      `${ADDRESS}rename-folder/${
        Folder.options[Folder.selectedIndex].innerHTML
      }&&${New_name.value}`,
      true
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
        }&&${New_folder.options[New_folder.selectedIndex].innerHTML}`,
        true
      );
    });

  //Manage thumbnails
  document
    .getElementById("TH_select_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let Folder = event.target.children[2];
      let Book = event.target.children[5];
      let Image = event.target.children[8];
      Call_and_display(
        `${ADDRESS}reassign-thumb/${
          Folder.options[Folder.selectedIndex].innerHTML
        }&&${Book.options[Book.selectedIndex].innerHTML}&&
        ${Image.options[Image.selectedIndex].innerHTML}`
      );
    });
  document
    .getElementById("TH_upload_form")
    .addEventListener("submit", (event) => {});
  document
    .getElementById("TH_rename_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let target = event.target.children[2];
      let newName = event.target.children[5];
      console.log(newName.value);
      Call_and_display(
        `${ADDRESS}rename-thumb/${
          target.options[target.selectedIndex].innerHTML
        }&&${newName.value}`
      );
    });
  document
    .getElementById("TH_format_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let regen = event.target.children[4];
      let rmManual = event.target.children[7];
      if (regen.checked) {
        regen = true;
      } else {
        regen = false;
      }
      if (rmManual.checked) {
        rmManual = true;
      } else {
        rmManual = false;
      }
      Call_and_display(`${ADDRESS}clear-thumbs/${regen}&&${rmManual}`);
    });

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
      `${ADDRESS}manage-acls/${IP.value}&&${List}&&${Action}&&${Code.value}`,
      false,
      true,
      Code
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
      true,
      Code
    );
  });

  //Management options
  document.getElementById("MNT_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNT_toggle]:checked"
    ).value;
    Call_and_display(
      `${ADDRESS}/toggle-management/${Toggle}&&MANAGEMENT&&${Code}`
    );
  });

  document.getElementById("MNU_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNU_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&UPLOAD&&${Code}`);
  });

  document.getElementById("MND_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MND_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&DELETE&&${Code}`);
  });

  document.getElementById("MNR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNR_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&RENAME&&${Code}`);
  });

  document.getElementById("MNM_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNM_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&MOVE&&${Code}`);
  });

  //Allow the user to close the response popup
  DISPLAY.addEventListener("click", (event) => {
    DISPLAY.style.display = "none";
  });
}

const ADDRESS = "http://192.168.1.110:5000/";
const DISPLAY = document.getElementById("Req_status_modal");
Assign_submit_actions();
