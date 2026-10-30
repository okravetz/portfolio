// Time-travel bar (_includes/time-travel.html). Every stop is a plain link, so this only adds:
// a GA4 event per stop clicked, the phone picker's close button and Escape key, and on Today the
// footer button and About P.S. link that open the bar (it starts hidden there). Once the bar has been
// opened or used to leave Today, it is open again when the visitor returns, until they close it.
(function () {
  var bar = document.getElementById("time-travel");
  if (!bar) return;

  var KEY = "tt-open"; // sessionStorage: "1" while the bar should be open on Today
  function remember(on) {
    try {
      if (on) sessionStorage.setItem(KEY, "1");
      else sessionStorage.removeItem(KEY);
    } catch (e) {}
  }

  function track(name, params) {
    if (typeof window.gtag === "function") {
      params.transport_type = "beacon"; // the page is about to unload
      window.gtag("event", name, params);
    }
  }

  // GA4: time_travel { from_era, to_era } for every stop, arrow, picker row and "Back to today".
  var from = bar.getAttribute("data-tt-from");
  bar.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a[data-tt-to]") : null;
    if (link) {
      remember(true);
      track("time_travel", { from_era: from, to_era: link.getAttribute("data-tt-to") });
    }
  });

  // Phone picker: a <details>, so it opens and closes without the script. This adds the X and Escape.
  var picker = bar.querySelector(".tt-picker");
  if (picker) {
    var summary = picker.querySelector("summary");
    var closePicker = function () {
      picker.open = false;
      summary.focus();
    };
    picker.querySelector(".tt-sheet__close").addEventListener("click", closePicker);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && picker.open) closePicker();
    });
  }

  // Today: the bar starts hidden (CSS, once the script has set the "js" class).
  if (!bar.classList.contains("tt--closable")) return;
  var opener = document.querySelector(".tt-open");

  function setOpen(open, source) {
    bar.classList.toggle("is-open", open);
    document.documentElement.classList.remove("tt-keep"); // the head script's early "open" is now ours
    remember(open);
    if (opener) opener.setAttribute("aria-expanded", open ? "true" : "false");
    // GA4: time_travel_open { opened_from: "footer" | "about_ps" }
    if (open) track("time_travel_open", { opened_from: source });
  }

  // Coming back to Today with the bar open: keep it open (no analytics event; nothing was clicked).
  if (document.documentElement.classList.contains("tt-keep")) {
    bar.classList.add("is-open");
    if (opener) opener.setAttribute("aria-expanded", "true");
  }

  if (opener) {
    opener.addEventListener("click", function () {
      setOpen(!bar.classList.contains("is-open"), "footer");
    });
  }

  var ps = document.querySelectorAll('a[href="#time-travel"]');
  for (var i = 0; i < ps.length; i++) {
    ps[i].addEventListener("click", function (e) {
      e.preventDefault();
      setOpen(true, "about_ps");
      bar.focus();
    });
  }

  // Close: just closes. The page stays where it is, and focus goes back to the floating button (it is
  // fixed to the window, so focusing it never moves the page).
  var closers = bar.querySelectorAll(".tt__close");
  for (var j = 0; j < closers.length; j++) {
    closers[j].addEventListener("click", function () {
      setOpen(false);
      if (opener) opener.focus({ preventScroll: true });
    });
  }
})();
