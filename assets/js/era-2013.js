// 2013: the phone menu button and the "Show all work" button (Bootstrap's "collapse", without jQuery).
// Without the script the menu links stay visible and every project is listed.
(function () {
  var more = document.getElementById("more-list");
  var toggle = document.querySelector(".more-toggle");
  if (more && toggle) {
    toggle.addEventListener("click", function () {
      var open = more.className.indexOf("open") === -1;
      more.className = open ? "more open" : "more";
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.firstChild.nodeValue = toggle.getAttribute(open ? "data-less" : "data-more");
    });
  }

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
