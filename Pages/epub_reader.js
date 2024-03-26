//Set metadata
const params =
  URLSearchParams && new URLSearchParams(document.location.search.substring(1));
const url =
  params && params.get("url") && decodeURIComponent(params.get("url"));
let currentSectionIndex =
  params && params.get("loc") ? params.get("loc") : undefined;

//Get the book and set up the render
const book = ePub(
  "../Books/Included Public domain/The tale of Peter Rabbit.epub"
);
const book_render = book.renderTo("reader-container", {
  flow: "paginated",
  width: "90%",
  height: 800,
});
book_render.display(currentSectionIndex);

book.ready.then(() => {
  //Wait untill the book is rendered then set the event listeners for the buttons and keys
  const next = document.getElementById("next");
  next.addEventListener(
    "click",
    (e) => {
      book.package.metadata.direction === "rtl"
        ? book_render.prev()
        : book_render.next();
      e.preventDefault();
    },
    false
  );

  const prev = document.getElementById("prev");
  prev.addEventListener(
    "click",
    (e) => {
      book.package.metadata.direction === "rtl"
        ? book_render.next()
        : book_render.prev();
      e.preventDefault();
    },
    false
  );

  const keyListener = (e) => {
    // Left Key
    if ((e.keyCode || e.which) == 37) {
      book.package.metadata.direction === "rtl"
        ? book_render.next()
        : book_render.prev();
    }

    // Right Key
    if ((e.keyCode || e.which) == 39) {
      book.package.metadata.direction === "rtl"
        ? book_render.prev()
        : book_render.next();
    }
  };

  book_render.on("keyup", keyListener);
  document.addEventListener("keyup", keyListener, false);
});

//Hide the next or previous arrow if at the end or start
book_render.on("relocated", (location) => {
  console.log(location);

  let next =
    book.package.metadata.direction === "rtl"
      ? document.getElementById("prev")
      : document.getElementById("next");
  let prev =
    book.package.metadata.direction === "rtl"
      ? document.getElementById("next")
      : document.getElementById("prev");

  if (location.atEnd) {
    next.style.visibility = "hidden";
  } else {
    next.style.visibility = "visible";
  }

  if (location.atStart) {
    prev.style.visibility = "hidden";
  } else {
    prev.style.visibility = "visible";
  }
});

window.addEventListener("unload", function () {
  console.log("unloading epub reader");
  this.book.destroy();
});
