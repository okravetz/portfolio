// The Future: scripted questions. All six answers are already in the page (in order); this shows the first two,
// then reveals each of the others when its question is chosen, in the order chosen. "Start over" hides them all.
// The question chips are docked at the bottom of the window (CSS), above the time-travel bar.
// "What an agent sees" opens on wide screens and starts closed on phones. No network calls, nothing typed.
(function () {
  var log = document.getElementById("log");
  var chips = document.querySelectorAll(".chip");
  var reset = document.querySelector(".reset");
  if (!log || !chips.length) return;

  var msgs = log.querySelectorAll(".msg");
  var byId = {};
  var chipById = {};
  var i;
  for (i = 0; i < msgs.length; i++) byId[msgs[i].getAttribute("data-q")] = msgs[i];
  for (i = 0; i < chips.length; i++) chipById[chips[i].getAttribute("data-q")] = chips[i];

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // The docked chips sit just above the time-travel bar: keep --tt-h equal to the bar's height.
  var bar = document.getElementById("time-travel");
  function barHeight() {
    if (bar) document.documentElement.style.setProperty("--tt-h", bar.offsetHeight + "px");
  }
  barHeight();
  window.addEventListener("resize", barHeight);

  function setAsked(id, asked) {
    var chip = chipById[id];
    if (!chip) return;
    if (asked) chip.setAttribute("aria-disabled", "true");
    else chip.removeAttribute("aria-disabled");
  }

  function ask(id) {
    var m = byId[id];
    if (!m || !m.hasAttribute("hidden")) return;
    m.removeAttribute("hidden");
    log.appendChild(m); // newest last
    m.className = "msg is-new";
    setAsked(id, true);
    // Bring the new question to the top of the window; the answer follows below it, above the docked chips.
    if (m.scrollIntoView) m.scrollIntoView({ block: "start", behavior: reduce ? "auto" : "smooth" });
  }

  for (i = 0; i < chips.length; i++) {
    chips[i].addEventListener("click", function () {
      if (this.getAttribute("aria-disabled") === "true") return;
      ask(this.getAttribute("data-q"));
    });
  }

  function start() {
    // The chosen order is forgotten: back to the page's own order, first two answered.
    var order = [];
    for (var k in byId) order.push(byId[k]);
    for (var j = 0; j < msgs.length; j++) {
      var m = msgs[j];
      m.className = "msg";
      if (m.getAttribute("data-start") === "true") {
        m.removeAttribute("hidden");
        setAsked(m.getAttribute("data-q"), true);
      } else {
        m.setAttribute("hidden", "");
        setAsked(m.getAttribute("data-q"), false);
      }
    }
    for (var n = 0; n < msgs.length; n++) log.appendChild(msgs[n]);
  }
  if (reset) reset.addEventListener("click", start);
  start();

  // "What an agent sees": one state, two buttons (the header button on wide screens, the card's on phones).
  var cols = document.querySelector(".cols");
  var toggles = document.querySelectorAll(".agent-toggle");
  var wide = window.matchMedia ? window.matchMedia("(min-width: 900px)") : { matches: true };
  function setAgent(open) {
    cols.className = open ? "cols" : "cols agents-closed";
    for (var t = 0; t < toggles.length; t++) toggles[t].setAttribute("aria-expanded", open ? "true" : "false");
  }
  for (i = 0; i < toggles.length; i++) {
    toggles[i].addEventListener("click", function () {
      setAgent(this.getAttribute("aria-expanded") !== "true");
    });
  }
  setAgent(wide.matches);
})();
