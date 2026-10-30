// 1996 clients marquee. A plain form button under it (the way 1996 pages wired buttons to JavaScript)
// stops and starts it, so anyone can pause the scrolling (WCAG 2.2.2). Paused, the whole list shows as still text
// in the same strip (a stopped marquee would freeze mid-scroll, mostly off screen). Hovering also pauses it, and it
// starts paused for visitors who ask for reduced motion. Without the script it scrolls and the button stays hidden.
(function () {
  var marquee = document.getElementById("ticker");
  var button = document.getElementById("ticker-toggle");
  if (!marquee || !marquee.stop || !button) return;

  // The still copy: same text, same strip, hidden from screen readers while the marquee is showing (and vice versa).
  var still = document.createElement("div");
  still.className = "m96-still";
  still.innerHTML = marquee.innerHTML;
  marquee.parentNode.insertBefore(still, marquee);

  var paused = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  function update() {
    still.hidden = !paused;
    marquee.hidden = paused;
    if (paused) marquee.stop();
    else marquee.start();
    button.value = button.getAttribute(paused ? "data-play" : "data-pause");
  }

  button.onclick = function () {
    paused = !paused;
    update();
  };
  marquee.onmouseover = function () {
    marquee.stop();
  };
  marquee.onmouseout = function () {
    if (!paused) marquee.start();
  };

  button.parentNode.hidden = false;
  update();
})();
