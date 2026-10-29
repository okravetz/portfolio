// Sun/moon toggle at the end of the main nav. The head script has already set data-theme.
(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme-toggle");
  if (!button) return;

  var dark = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function saved() {
    try {
      var t = localStorage.getItem("theme");
      return t === "light" || t === "dark" ? t : null;
    } catch (e) {
      return null;
    }
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }

  apply(root.getAttribute("data-theme") === "dark" ? "dark" : "light");

  button.addEventListener("click", function () {
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    apply(next);
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
  });

  // With no saved choice, keep following the system setting.
  if (dark && dark.addEventListener) {
    dark.addEventListener("change", function (e) {
      if (!saved()) apply(e.matches ? "dark" : "light");
    });
  }
})();
