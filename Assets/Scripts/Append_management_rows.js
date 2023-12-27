function get_rows() {
  Rows = document.getElementById("Row_list").children;
  for (group of Rows) {
    const new_row = document.createElement("section");
    new_row.classList += "Management-row";
    $(new_row).load(
      `../Pages/Management_components/${group.children[0].innerHTML.replaceAll(
        " ",
        "_"
      )}.html`
    );
    group.appendChild(new_row);
  }
}
get_rows();
