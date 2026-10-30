// Time-travel bar (_includes/time-travel.html). Every stop is a plain link, so this only adds:
// a GA4 event per stop clicked, the phone picker's close button and Escape key, and on Today the
// footer button and About P.S. link that open the bar (it starts hidden there).
(function () {
  var bar = document.getElementById("time-travel");
  if (!bar) return;

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
    if (link) track("time_travel", { from_era: from, to_era: link.getAttribute("data-tt-to") });
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
    if (opener) opener.setAttribute("aria-expanded", open ? "true" : "false");
    // GA4: time_travel_open { opened_from: "footer" | "about_ps" }
    if (open) track("time_travel_open", { opened_from: source });
  }

  if (opener) {
    opener.addEventListener("click", function () {
      var atBottom = window.innerHeight + window.pageYOffset >= document.documentElement.scrollHeight - 2;
      setOpen(!bar.classList.contains("is-open"), "footer");
      // At the end of the page the newly shown bar would cover the footer; scroll it into view instead.
      if (atBottom && bar.classList.contains("is-open")) window.scrollTo(0, document.documentElement.scrollHeight);
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

  var closers = bar.querySelectorAll(".tt__close");
  for (var j = 0; j < closers.length; j++) {
    closers[j].addEventListener("click", function () {
      setOpen(false);
      if (opener) opener.focus();
    });
  }
})();
