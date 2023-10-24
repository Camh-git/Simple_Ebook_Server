//This is the functional version
function getheader() {
  const HEADER_CONTAINER = document.getElementById("header_container");
  const HEADER_FILE = "Assets/Header.html";
  if (HEADER_FILE) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
        /*
        console.log(
          "Header request state/status: ",
          this.readyState,
          this.status
        );
        */
        if (this.status == 200) {
          HEADER_CONTAINER.innerHTML = this.responseText;
        } else if (this.status == 404) {
          HEADER_CONTAINER.innerHTML = "Page not found.";
        } else {
          HEADER_CONTAINER.innerHTML = "Error fetching header.";
        }
      }
    };
    xhttp.open("GET", HEADER_FILE, true);
    xhttp.send();
    return;
  }
}

function getfooter() {
  var FOOTER_CONTAINER = document.getElementById("footer_container");
  var FOOTER_FILE = "Assets/Footer.html";
  if (FOOTER_FILE) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
        /*
        console.log(
          "Footer request state/status: ",
          this.readyState,
          this.status
        );
        */
        if (this.status == 200) {
          FOOTER_CONTAINER.innerHTML = this.responseText;
        } else if (this.status == 404) {
          FOOTER_CONTAINER.innerHTML = "Page not found.";
        } else {
          header_container.innerHTML = "Error fetching footer.";
        }
      }
    };
    xhttp.open("GET", FOOTER_FILE, true);
    xhttp.send();
    return;
  }
}

getheader();
getfooter();
