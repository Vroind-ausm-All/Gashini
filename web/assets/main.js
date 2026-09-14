/* Gashini Dienstleistungen — Website-Interaktionen */
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('hauptmenue');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
      toggle.textContent = open ? '✕' : '☰';
    });
  }
  var jahr = document.getElementById('jahr');
  if (jahr) jahr.textContent = String(new Date().getFullYear());
})();
