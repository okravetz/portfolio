// 1983: the bulletin board. The menu's buttons show one section at a time; the commands ([S], [D], [P], [E], [L],
// and [B] on the all-work page) are links. Keyboard: the terminal takes focus when the page opens; typing a
// choice's letter runs it and echoes it at the COMMAND? prompt, and Up / Down move between the choices. The
// letters only work while focus is inside the terminal, so they never get in the way anywhere else (WCAG 2.1.4).
// Without the script every section stays visible, the menu stays hidden, and the commands are ordinary links.
(function () {
  var crt = document.querySelector(".crt");
  if (!crt) return;
  var buttons = crt.querySelectorAll(".bbs-menu button[data-section]");
  var sections = crt.querySelectorAll(".sections section");
  var keys = crt.querySelectorAll(".prompt-key");

  function echo(letter) {
    for (var i = 0; i < keys.length; i++) keys[i].textContent = letter;
  }

  function show(name) {
    for (var i = 0; i < sections.length; i++) {
      sections[i].classList.toggle("is-on", sections[i].id === "sec-" + name);
    }
    for (var j = 0; j < buttons.length; j++) {
      var on = buttons[j].getAttribute("data-section") === name;
      buttons[j].setAttribute("aria-pressed", on ? "true" : "false");
      if (on) echo(buttons[j].getAttribute("data-key"));
    }
  }

  if (buttons.length && sections.length) {
    for (var k = 0; k < buttons.length; k++) {
      buttons[k].addEventListener("click", function () {
        show(this.getAttribute("data-section"));
      });
    }
    document.documentElement.classList.add("bbs");
    show(buttons[0].getAttribute("data-section"));
  }

  // Every choice on screen right now (menu buttons and the commands of the section that is showing).
  function choices() {
    var all = crt.querySelectorAll("[data-key]");
    var out = [];
    for (var i = 0; i < all.length; i++) if (all[i].offsetParent) out.push(all[i]);
    return out;
  }

  crt.addEventListener("keydown", function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var list = choices();
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!list.length) return;
      var at = list.indexOf(document.activeElement);
      var next = e.key === "ArrowDown" ? at + 1 : at - 1;
      if (at === -1) next = e.key === "ArrowDown" ? 0 : list.length - 1;
      list[(next + list.length) % list.length].focus();
      e.preventDefault();
      return;
    }
    if (!e.key || e.key.length !== 1) return;
    var letter = e.key.toUpperCase();
    for (var i = 0; i < list.length; i++) {
      if (list[i].getAttribute("data-key") === letter) {
        e.preventDefault();
        echo(letter);
        list[i].focus();
        list[i].click();
        return;
      }
    }
  });

  // Ready to type, like a terminal that just connected (without moving the page).
  crt.focus({ preventScroll: true });
})();
