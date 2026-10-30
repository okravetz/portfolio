// 1983: the menu's buttons show one section at a time, like a bulletin board's menu. The script runs at the
// end of the page and adds the "bbs" class; without it every section stays visible and the menu stays hidden.
(function () {
  var buttons = document.querySelectorAll(".bbs-menu button[data-section]");
  var sections = document.querySelectorAll(".sections section");
  var promptKey = document.querySelector(".prompt-key");
  if (!buttons.length || !sections.length) return;

  function show(name) {
    for (var i = 0; i < sections.length; i++) {
      sections[i].classList.toggle("is-on", sections[i].id === "sec-" + name);
    }
    for (var j = 0; j < buttons.length; j++) {
      var on = buttons[j].getAttribute("data-section") === name;
      buttons[j].setAttribute("aria-pressed", on ? "true" : "false");
      if (on && promptKey) promptKey.textContent = buttons[j].getAttribute("data-key");
    }
  }

  for (var k = 0; k < buttons.length; k++) {
    buttons[k].addEventListener("click", function () {
      show(this.getAttribute("data-section"));
    });
  }

  document.documentElement.classList.add("bbs");
  show(buttons[0].getAttribute("data-section"));
})();
