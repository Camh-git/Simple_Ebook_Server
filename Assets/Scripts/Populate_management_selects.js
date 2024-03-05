import { Set_server_address } from "./Server_IP.js";
import { get_data } from "./Get_data.js";

//const delay = (ms) => new Promise((res) => setTimeout(res, ms));

async function Pop_management_selects() {
  //Get the thumnail and book lists
  const BOOK_DATA = await get_data(
    `http://${document.cookie.split("=")[1]}:5000/get-book-and-thumb-data`
  );
  try {
    console.log(
      "Total number of folders found: " +
        BOOK_DATA.Books.Folders.length +
        ", thumbs: " +
        BOOK_DATA.Thumbs.Folders.length
    );
  } catch {
    document.getElementById("Management_pannel").innerHTML =
      "<h1>Management</h1>" +
      "<h3>Sorry, the call to the API to fetch the folders failed. The controls have been hidden to prevent any incorrect comands from being sent.</h3>" +
      "<h4>Please make sure the book API is active and that you can contact the server.</h4>" +
      `<p>The server's IP is currently listed as: ${
        document.cookie.split("=")[1]
      }, if this is incorrect you can change it below, then reload the page.</p> ` +
      `<form method="POST" enctype="multipart/form-data" id="set_IP_form""> <h3>IP input</h3>
       <input type="text" name="addr" id="addr"><input name="submit" type="submit" value = "update"><br><br></form>`;

    document
      .getElementById("set_IP_form")
      .addEventListener("submit", (event) => {
        event.preventDefault();
        let ip = event.target.children[1].value;
        console.log(ip);
        Set_server_address(ip);
        window.location.href = "./Management.html";
      });
    return;
  }
  //Set the update watchers
  //set_form_update_listeners();

  //Set the selects and handle the folder selects
  const SELECT_LIST = document.querySelectorAll("select");

  for (let select of SELECT_LIST) {
    select.innerHTML = "<option>No selection</option>";
    //Populate the folder lists
    if (
      select.getAttribute("name").includes("folder") ||
      select.getAttribute("name").includes("TH_fold")
    ) {
      for (const folder of BOOK_DATA.Books.Folders) {
        const option = document.createElement("option");
        option.value = option.textContent = folder.Folder_name;
        select.appendChild(option);
      }
      if (select.getAttribute("name").includes("folder")) {
        //Add listener for book selects, and for thumb selects
        select.addEventListener("change", function () {
          let targetBookSelect = document.getElementsByName(
            this.getAttribute("name").substring(0, 2) + "_book_select"
          );
          if (typeof targetBookSelect[0] !== "undefined") {
            //Find the right folder and add the books
            targetBookSelect[0].innerHTML = "<option>No selection</option>";
            for (const folder of BOOK_DATA.Books.Folders) {
              if (this.options[this.selectedIndex].text == folder.Folder_name) {
                for (const book of folder.Books) {
                  try {
                    if (book.Title.length > 1) {
                      const option = document.createElement("option");
                      option.value = option.textContent =
                        book.Title + book.Extension;
                      targetBookSelect[0].appendChild(option);
                    }
                  } catch {
                    console.log(
                      "Tried to read invalid title for book: " + book.Title
                    );
                  }
                }
              }
            }
          }
        });
      } else if (select.getAttribute("name").includes("TH_fold")) {
        select.addEventListener("change", function () {
          let targetThumbSelect = document.getElementsByName(
            "TH_img_select_" + this.getAttribute("name").slice(-2)
          )[0];
          targetThumbSelect.innerHTML = "<option>No selection</option>";
          for (const folder of BOOK_DATA.Thumbs.Folders) {
            if (this.options[this.selectedIndex].text == folder.Folder_name) {
              for (const img of folder.Images) {
                if (img != "NA" && img != "" && !img.includes("http")) {
                  const option = document.createElement("option");
                  option.value = option.textContent = img.split(/[/]+/).pop();
                  targetThumbSelect.appendChild(option);
                }
              }
            }
          }
        });
      } else {
        console.log(
          "select: " +
            select.getAttribute("name") +
            " is not a thumb or book select"
        );
      }
    }
  }
}

Pop_management_selects();
