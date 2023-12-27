function get_rows() {
  Rows = document.getElementById("Row_list").children;
  for (group of Rows) {
    //Add the new forms
    const new_row = document.createElement("section");
    new_row.classList += "Management-row";
    $(new_row).load(
      `../Pages/Management_components/${group.children[0].innerHTML.replaceAll(
        " ",
        "_"
      )}.html`
    );
    group.appendChild(new_row);

    //Add the dropdown to the forms
    group
      .getElementsByTagName("img")[0]
      .addEventListener("click", function (e) {
        let section = e.target.parentNode.getElementsByTagName("section")[0];
        if (section.style.display == "inline") {
          section.style.display = "none";
          e.target.src = "../Assets/Images/expand_more_white_24dp.svg";
        } else {
          section.style.display = "inline";
          e.target.src = "../Assets/Images/expand_less_white_24dp.svg";
        }
      });
  }
}
get_rows();
