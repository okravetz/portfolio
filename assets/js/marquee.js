// 1996 marquee: stop it for visitors who ask for reduced motion. (Hovering also pauses it.)
(function () {
  if (!window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var marquees = document.getElementsByTagName("marquee");
  for (var i = 0; i < marquees.length; i++) {
    if (marquees[i].stop) marquees[i].stop();
  }
})();
