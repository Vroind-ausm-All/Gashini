/* Gashini Dienstleistungen — Website-Interaktionen */
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('hauptmenue');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var offen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(offen));
      toggle.setAttribute('aria-label', offen ? 'Menü schließen' : 'Menü öffnen');
    });
  }
  var jahr = document.getElementById('jahr');
  if (jahr) jahr.textContent = String(new Date().getFullYear());
})();
