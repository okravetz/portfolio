// 2001: the DHTML. An intro that plays the GIF loader and skips itself (or is skipped, or replayed; once per
// browser tab, and never with reduced motion), image-swap rollovers on the tabs (Dreamweaver's MM_swapImage, by hand), and sections switched
// in place. It runs right after the stage markup, before the first paint, so the stage never flashes up first.
// Without it: no intro, and every section shows in the scrolling panel, with the tabs jumping to them.
(function () {
  var intro = document.getElementById("intro");
  var stage = document.getElementById("stage");
  var panel = document.getElementById("panel");
  var loader = document.getElementById("loader");
  var skip = document.getElementById("skip");
  var tabs = document.querySelectorAll(".tabs a[data-section]");
  var sections = document.querySelectorAll(".panel .section");
  if (!stage || !tabs.length) return;

  var INTRO_MS = 3200;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = null;
  var timer = null;

  // Preload the rollover images (MM_preloadImages).
  var cache = [];
  for (var p = 0; p < tabs.length; p++) {
    var im = tabs[p].getElementsByTagName("img")[0];
    var a = new Image(); a.src = im.getAttribute("data-over"); cache.push(a);
    var b = new Image(); b.src = im.getAttribute("data-on"); cache.push(b);
  }

  function paint(link, state) {
    var im = link.getElementsByTagName("img")[0];
    im.src = im.getAttribute("data-" + state);
  }

  function show(name) {
    current = name;
    for (var i = 0; i < sections.length; i++) {
      sections[i].style.display = sections[i].id === name ? "block" : "none";
    }
    for (var j = 0; j < tabs.length; j++) {
      var on = tabs[j].getAttribute("data-section") === name;
      paint(tabs[j], on ? "on" : "off");
      if (on) tabs[j].setAttribute("aria-current", "true");
      else tabs[j].removeAttribute("aria-current");
    }
    if (panel) panel.scrollTop = 0;
  }

  function hover(link, over) {
    if (link.getAttribute("data-section") !== current) paint(link, over ? "over" : "off");
  }

  for (var k = 0; k < tabs.length; k++) {
    tabs[k].onclick = function () {
      show(this.getAttribute("data-section"));
      return false;
    };
    tabs[k].onmouseover = tabs[k].onfocus = function () { hover(this, true); };
    tabs[k].onmouseout = tabs[k].onblur = function () { hover(this, false); };
  }

  function endIntro(focusTabs) {
    clearTimeout(timer);
    intro.className = intro.className.replace(" is-on", "");
    stage.style.display = "";
    if (focusTabs) {
      // The first tab that is showing (wide or narrow layout).
      for (var t = 0; t < tabs.length; t++) {
        if (tabs[t].offsetParent) { tabs[t].focus(); break; }
      }
    }
  }

  function playIntro(focusSkip) {
    if (!intro || reduce) return;
    stage.style.display = "none";
    intro.className += " is-on";
    if (loader) loader.src = loader.src.split("#")[0] + "#" + new Date().getTime(); // restart the GIF
    if (focusSkip && skip) skip.focus();
    timer = setTimeout(function () {
      var hadFocus = document.activeElement === skip;
      endIntro(hadFocus);
    }, INTRO_MS);
  }

  if (skip) {
    skip.onclick = function () {
      endIntro(true);
      return false;
    };
  }

  var replays = document.querySelectorAll(".replay a");
  for (var r = 0; r < replays.length; r++) {
    replays[r].onclick = function () {
      playIntro(true);
      return false;
    };
  }

  var start = (location.hash || "").replace("#", "");
  var known = false;
  for (var s = 0; s < sections.length; s++) if (sections[s].id === start) known = true;
  show(known ? start : sections[0].id);
  // The intro plays once per browser tab (Replay still plays it on demand).
  var SEEN = "intro-2001";
  var seen = false;
  try { seen = sessionStorage.getItem(SEEN) === "1"; sessionStorage.setItem(SEEN, "1"); } catch (e) {}
  if (!known && !seen) playIntro(false);
})();
