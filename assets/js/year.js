// Footer copyright: "<Hebrew year> / <common year>", recalculated on every page load.
// The Hebrew year comes from the browser's built-in Hebrew calendar and rolls over at Rosh Hashanah;
// the common year rolls over on January 1. Both change at local midnight.
(function () {
  var el = document.getElementById("copyright-years");
  if (!el) return;

  var now = new Date();
  var ce = String(now.getFullYear());
  var am = "";

  try {
    var parts = new Intl.DateTimeFormat("en-u-ca-hebrew", { year: "numeric" }).formatToParts(now);
    for (var i = 0; i < parts.length; i++) {
      if (parts[i].type === "year") am = parts[i].value;
    }
  } catch (e) {}

  // Only trust a plain four-digit year (5787); otherwise show the common year alone.
  el.textContent = /^\d{4}$/.test(am) ? am + " / " + ce : ce;
})();
