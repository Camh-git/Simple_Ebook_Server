export async function Call_and_display(
  requestString,
  update_lib_selects = false,
  show_ip_lists = false,
  code = "",
  upload = false
) {
  const ADDRESS = `http://${document.cookie.split("=")[1]}:5000/`;
  const DISPLAY = document.getElementById("Req_status_modal");

  let result = "";
  if (upload) {
    //Get the appropriate input and send it's file
    let upload_input = document.getElementsByName(
      requestString.split("/").pop()
    );
    let book = upload_input[0].value.split("\\").pop();
    //console.log(upload_input[0].files[0]);
    //console.log(`${ADDRESS}${requestString.split("/")[3]}/${book}`);
    result = await fetch(`${ADDRESS}${requestString.split("/")[3]}/${book}`, {
      method: "POST",
      body: upload_input[0].files[0],
    });
  } else {
    //send a normal request
    result = await fetch(requestString);
  }
  const data = await result.json();

  DISPLAY.style.display = "block";
  let response = "Response:<br>";
  switch (data) {
    case 200:
    case 204:
      response += "Success, the changes you requested have been made.";
      break;
    case 201:
      response += "Created, the additions you requested have been made.";
    case 202:
      response +=
        " Accepted, your request is being processed, be sure to check back soon.";
    case 205:
      response += "Success, please reload the page to see your changes.";
    case 218:
      response += "Success, but some errors occured, see error list";
    case 400:
      response +=
        "Request error: Please make sure all required fields are filled in.";
      break;
    case 401:
      response +=
        "Unathorised: This action requires authentication.<br> please make sure you are authorised <br> and ensure you have entered the correct password.";
      break;
    case 403:
      response +=
        "Forbidden: Users are not allowed to rename or delete the Misc and Upload folders, or upload unsupported file types";
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
        "Conflict: Please make sure there isn't a book or folder that already has that name." +
        "<br> If you saw this while editing the ACLs then this ip is probably already on a list." +
        "<br> If you were deleting a folder then there was a book name conflict in the misc and uploads folders." +
        "Please resovle this conflict before deleting the folder, or select the 'delete content' option, no data has been deleted.";
      break;
    case 410:
      response +=
        "Gone: The value you wish to remove is not in the targeted list.";
      break;
    case 418:
      response +=
        "We hope the tea is tasty, just don't leave the lid off next to your books";
    case 421:
      response +=
        "Misdirected Request: Unfortunatly this server cannot accept connections from your current IP address.";
    case 423:
      response +=
        "Locked: The selected Management function is currently disabled, contact an administrator.";
    case 428:
      response +=
        "Warning: One or more of the books moved to /Misc had the MOVED tag applied, meaning a book with an identical name was already present" +
        ", please resolve the conflict and remove the MOVED tag to avoid potential book loss in future merges.";
      break;
    case 451:
      response +=
        "Unavailable For Legal Reasons: We don't know what you did, but apperntly we think it's illegal";
    case 500:
      response +=
        "Server error: please contact the developer with the following data:" +
        data;
      break;
    case 501:
      response +=
        "Not implemented: This feature isn't ready yet, please check back later.<br>you can keep up to date at: " +
        "<a href='https://github.com/Camh-git/Simple_Ebook_Server'>Our github</a> for updates";
      "";
      break;
    default:
      response += "No pre-prepared message, status: " + data;
  }

  //Handle optional params
  if (update_lib_selects) {
    //re-usable no-module way of importing the populate script
    const pop_select_script = document.createElement("script");
    pop_select_script.src = "../Assets/Scripts/Update_management_selects.js";
    document.body.prepend(pop_select_script);
    pop_select_script.remove();
  }
  if (show_ip_lists && data == "200") {
    //Get settings
    const lists = await fetch(`${ADDRESS}fetch-settings/${code}`);
    let list_data = await lists.json();
    let WL_data, BL_data;

    //Show lists in tables
    response += "<table><tr><th>Whitelist</th><th>Blacklist</th></tr>";

    for (
      let i = 0;
      i <
      Math.max(list_data["WhiteList"].length, list_data["BlackList"].length);
      i++
    ) {
      WL_data = list_data["WhiteList"][i];
      BL_data = list_data["BlackList"][i];
      if (WL_data === undefined) {
        WL_data = "";
      }
      if (BL_data === undefined) {
        BL_data = "";
      }
      response += `<tr><td>${WL_data}</td><td>${BL_data}</td></tr>`;
    }
    //Show which list is active
    if (list_data["EnableWhiteList"]) {
      response += "<br>The Whitelist is enabled.";
    } else if (list_data["EnableBlackList"]) {
      response += "<br>The Blacklist is enabled.";
    } else {
      response += "<br>Neither of the ACLs are active.";
    }
  }

  DISPLAY.children[0].innerHTML = "<h2>click to close<h2><br>" + response;
}
