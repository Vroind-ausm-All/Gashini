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

  /* Spamschutz: Formulare, die in unter drei Sekunden ausgefüllt wurden,
     stammen praktisch immer von einem Skript. Der Wert wird mitgesendet
     und kann serverseitig ausgewertet werden. */
  var formular = document.querySelector('form.kontakt');
  if (formular) {
    var geladen = Date.now();
    var feld = document.createElement('input');
    feld.type = 'hidden';
    feld.name = 'ausfuellzeit';
    formular.appendChild(feld);
    formular.addEventListener('submit', function () {
      feld.value = String(Math.round((Date.now() - geladen) / 1000));
    });
  }
})();
