import { Call_and_display } from "./Call_and_display.js";
let BOOK_INFO = await get_data(
  `http://${document.cookie.split("=")[1]}:5000/get-book-data`
);

async function get_data(url) {
  const req = await fetch(url);
  const data = await req.json();
  return data;
}

function search_format(string) {
  try {
    return string
      .replace(/\.[^/.]+$/, "")
      .replace(" ", "")
      .toUpperCase();
  } catch {
    return string;
  }
}
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
    New_name.value = "";
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
    New_name.value = "";
  });

  //Manage Library
  document.getElementById("CF_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let Name = event.target.children[1];
    Call_and_display(`${ADDRESS}create-folder/${Name.value}`, true);
    Name.value = "";
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
      let Book_folder = event.target.children[2];
      let Book = event.target.children[5];
      let Img_folder = event.target.children[8];
      let Image = event.target.children[11];
      console.log(
        "folder: " + Img_folder.options[Img_folder.selectedIndex].innerHTML
      );
      console.log("img: " + Image.options[Image.selectedIndex].innerHTML);
      Call_and_display(
        `${ADDRESS}reassign-thumb/${
          Book_folder.options[Book_folder.selectedIndex].innerHTML
        }&&${Book.options[Book.selectedIndex].innerHTML}&&${
          Img_folder.options[Img_folder.selectedIndex].innerHTML
        }&&${Image.options[Image.selectedIndex].innerHTML}`
      );
      Update_thumb_list(Image);
    });
  document
    .getElementById("TH_upload_form")
    .addEventListener("submit", (event) => {});
  document
    .getElementById("TH_rename_form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      let folder = event.target.children[3];
      let target = event.target.children[6];
      let New_name = event.target.children[8];
      console.log(folder);
      Call_and_display(
        `${ADDRESS}rename-thumb/${
          folder.options[folder.selectedIndex].innerHTML
        }&&${target.options[target.selectedIndex].innerHTML}&&${New_name.value}`
      );
      //Update_thumb_list(target);
      New_name.value = "";
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

  document.getElementById("TH_del_form").addEventListener("submit", (event) => {
    event.preventDefault();
    let folder = event.target.children[3];
    let target = event.target.children[7];
    Call_and_display(
      `${ADDRESS}delete-thumb/${
        folder.options[folder.selectedIndex].innerHTML
      }&&${target.options[target.selectedIndex].innerHTML}`
    );
    Update_thumb_list(target);
    target.value = "";
  });

  //Manage book data
  document.getElementById("EBD_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const folder = event.target.children[3];
    const book = event.target.children[6];
    const authors = event.target.children[9];
    const date = event.target.children[11];
    const publisher = event.target.children[14];
    const isbn = event.target.children[17];
    const isbn13 = event.target.children[20];
    const thumbnail = event.target.children[23];
    const ext = event.target.children[26];
    const authorlist = "[" + authors.value + "]";

    Call_and_display(
      `${ADDRESS}edit-book-data/${
        folder.options[folder.selectedIndex].innerHTML
      }&&${book.options[book.selectedIndex].innerHTML.replace(
        /\.[^/.]+$/,
        ""
      )}&&${authorlist}&&${date.value.replace("/", "-")}&&${publisher.value}&&${
        isbn.value
      }&&${isbn13.value}&&${thumbnail.value.replaceAll("/", "-@")}&&${
        ext.value
      }&&True`
    );
    //call the book info update
    BOOK_INFO = get_data(
      `http://${document.cookie.split("=")[1]}:5000/get-book-data`
    );
  });

  document
    .getElementById("BD_book_select")
    .addEventListener("change", (event) => {
      //Fill in the inputs with the book's existing data
      const folder = event.target.parentElement.children[3];
      const book = event.target.parentElement.children[6];
      const authors = event.target.parentElement.children[9];
      const date = event.target.parentElement.children[11];
      const publisher = event.target.parentElement.children[14];
      const isbn = event.target.parentElement.children[17];
      const isbn13 = event.target.parentElement.children[20];
      const thumbnail = event.target.parentElement.children[23];
      const validated_box = event.target.parentElement.children[26];
      //Find the right book
      for (let info_folder of BOOK_INFO.Folders) {
        if (folder.value == info_folder.Folder_name) {
          for (let info_book of info_folder.Books) {
            if (search_format(info_book.Title) == search_format(book.value)) {
              //fill in the data
              authors.value = info_book.Authors.toString()
                .replace("[", "")
                .replace("]", "");
              date.value = info_book.Date;
              publisher.value = info_book.Publisher;
              isbn.value = info_book.isbn;
              if (info_book.isbn13.length > 0) {
                isbn13.value = info_book.isbn13;
              } else {
                isbn13.value = "0";
              }
              thumbnail.value = info_book.Thumbnail;
              if (info_book.Validated.toUpperCase() == "TRUE") {
                validated_box.checked = true;
              } else {
                validated_box.checked = false;
              }
            }
          }
        }
      }
    });

  document.getElementById("GBD_form").addEventListener("submit", (event) => {
    event.preventDefault();
    Call_and_display(`${ADDRESS}gen-book-data`);
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
      Code.value = "";
    });

  document.getElementById("TOGR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[7];
    const Toggle = document.querySelector(
      "input[type='radio'][name=Reader_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}toggle-readers/${Toggle}&&${Code.value}`);
    Code.value = "";
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
    IP.value = "";
    Code.value = "";
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
    Code.value = "";
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
    Code.value = "";
  });

  document.getElementById("MNU_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNU_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&UPLOAD&&${Code}`);
    Code.value = "";
  });

  document.getElementById("MND_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MND_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&DELETE&&${Code}`);
    Code.value = "";
  });

  document.getElementById("MNR_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNR_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&RENAME&&${Code}`);
    Code.value = "";
  });

  document.getElementById("MNM_form").addEventListener("submit", (event) => {
    event.preventDefault();
    const Code = event.target.children[8];
    const Toggle = document.querySelector(
      "input[type='radio'][name=MNM_toggle]:checked"
    ).value;
    Call_and_display(`${ADDRESS}/toggle-management/${Toggle}&&MOVE&&${Code}`);
    Code.value = "";
  });

  //Allow the user to close the response popup
  DISPLAY.addEventListener("click", (event) => {
    DISPLAY.style.display = "none";
  });
}
async function Update_thumb_list(select) {
  try {
    const req = await fetch(
      `http://${document.cookie.split("=")[1]}:5000/thumb-map`
    );
    const data = await req.json();
    if (typeof select.innerHTML !== "undefined") {
      select.innerHTML = "<option>No selection</option>";
      for (let thumb of data.Images) {
        const option = document.createElement("option");
        option.value = option.textContent = thumb.Name + thumb.ext;
        select.appendChild(option);
      }
    }
  } catch {
    console.log(`Failed to call thumb list, will use placeholders if possible`);
    return 500;
  }
}

const ADDRESS = `http://${document.cookie.split("=")[1]}:5000/`;
const DISPLAY = document.getElementById("Req_status_modal");
Assign_submit_actions();
