// 2013: the phone menu button (Bootstrap's "collapse", without jQuery). Without the script the menu links
// simply stay visible.
(function () {
  var button = document.querySelector(".burger");
  var links = document.getElementById("navlinks");
  if (!button || !links) return;

  function setOpen(open) {
    links.className = open ? "navlinks open" : "navlinks";
    button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  button.addEventListener("click", function () {
    setOpen(button.getAttribute("aria-expanded") !== "true");
  });

  // Choosing a section closes the menu.
  links.addEventListener("click", function (e) {
    if (e.target.tagName === "A") setOpen(false);
  });
})();
