export async function Populate_support_table() {
  //Get the format data
  const table_data = await fetch("../Assets/File_type_support.json").then(
    (res) => {
      return res.json();
    }
  );
  console.log(table_data);
  // Desktop table(s)
  try {
    const tables = document.getElementsByClassName(
      "Format-support-table Desktop"
    );
    for (let table of tables) {
      table.innerHTML = "";
      const EXT_ROW = document.createElement("tr");
      EXT_ROW.innerHTML = "<th>Format</th>";
      const SUPPORT_ROW = document.createElement("tr");
      SUPPORT_ROW.innerHTML = "<th>Status</th>";

      for (let format of table_data.fileTypes) {
        const ext = document.createElement("td");
        ext.textContent = `${format.extension}`;
        EXT_ROW.appendChild(ext);

        const status = document.createElement("td");
        status.textContent = `${format.support}`;
        SUPPORT_ROW.appendChild(status);
      }

      table.appendChild(EXT_ROW);
      table.appendChild(SUPPORT_ROW);
    }
  } catch {
    console.log("No desktop table");
  }
  //Mobile table(s)
  try {
    const tables = document.getElementsByClassName(
      "Format-support-table Mobile"
    );
    for (let table of tables) {
      table.innerHTML = "";
      const HEADER_ROW = document.createElement("tr");
      HEADER_ROW.innerHTML = "<th>Format</th><th>Status</th>";
      table.appendChild(HEADER_ROW);

      for (let format of table_data.fileTypes) {
        const format_row = document.createElement("tr");

        const ext = document.createElement("td");
        ext.textContent = `${format.extension}`;
        format_row.appendChild(ext);

        const status = document.createElement("td");
        status.textContent = `${format.support}`;
        format_row.appendChild(status);

        table.appendChild(format_row);
      }
    }
  } catch {
    console.log("No mobile table");
  }
}
Populate_support_table();
