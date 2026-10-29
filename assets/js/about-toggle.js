// On phones the About copy stops after the second paragraph, with a "Read more" row that matches
// the "Show all work" row. Wider screens always show everything (the CSS only collapses at phone
// width), and without JavaScript nothing is collapsed.
(function () {
  var button = document.querySelector(".about-toggle");
  var text = document.querySelector(".about__text");
  if (!button || !text) return;

  text.classList.add("is-collapsible");

  button.addEventListener("click", function () {
    var open = text.classList.toggle("is-open");
    button.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();
