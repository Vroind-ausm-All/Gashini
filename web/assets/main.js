/* Gashini Dienstleistungen — Website-Interaktionen */
(function () {
  /* ---------- Navigation ---------- */
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

  /* ---------- Spamschutz ----------
     Formulare, die in unter drei Sekunden ausgefüllt wurden, stammen
     praktisch immer von einem Skript. Der Wert wird mitgesendet und
     kann serverseitig ausgewertet werden. */
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

  /* ================================================================
     Material und Bewegung
     Erst ab hier wird animiert. Die Klasse js-motion schaltet die
     Ausgangszustände im Stylesheet frei – ohne JavaScript bleibt
     jeder Text von Anfang an sichtbar.
     ================================================================ */
  var wurzel = document.documentElement;

  /* Wörter in eigene Hüllen legen, damit sie einzeln aufsteigen können.
     Es werden ausschließlich Textknoten angefasst; <br> und farbige
     <span> im Inneren bleiben erhalten. */
  var zaehler;
  function woerterHuellen(el) {
    zaehler = 0;
    (function gehe(knoten) {
      var kinder = Array.prototype.slice.call(knoten.childNodes);
      kinder.forEach(function (k) {
        if (k.nodeType === 3) {
          var teile = k.nodeValue.split(/(\s+)/);
          if (!teile.join('').trim()) return;
          var frag = document.createDocumentFragment();
          teile.forEach(function (t) {
            if (!t.trim()) { frag.appendChild(document.createTextNode(t)); return; }
            var huelle = document.createElement('span');
            huelle.className = 'wort';
            huelle.style.setProperty('--i', zaehler++);
            var innen = document.createElement('i');
            innen.textContent = t;
            huelle.appendChild(innen);
            frag.appendChild(huelle);
          });
          knoten.replaceChild(frag, k);
        } else if (k.nodeType === 1 && k.tagName !== 'BR') {
          gehe(k);
        }
      });
    })(el);
  }

  /* Welche Elemente bewegen sich – ohne dafür das HTML anzufassen */
  var heroTitel = document.querySelector('.hero h1');
  if (heroTitel) heroTitel.classList.add('bewegt', 'anriss');
  document.querySelectorAll('.section-head h2, .abschluss h2').forEach(function (h) {
    h.classList.add('bewegt');
  });
  document.querySelectorAll('.hero .lead, .hero-actions, .hero-fuss, .abschluss p, .abschluss-aktionen')
    .forEach(function (e) { e.classList.add('nachzug'); });
  document.querySelectorAll('.grid, .paket, .zeitplan, .anlaesse').forEach(function (g) {
    g.classList.add('staffel');
    Array.prototype.forEach.call(g.children, function (kind, i) {
      kind.style.setProperty('--k', i);
    });
  });

  document.querySelectorAll('.bewegt').forEach(woerterHuellen);
  document.querySelectorAll('.fuell').forEach(function (f) {
    f.setAttribute('data-text', f.textContent);
  });

  wurzel.classList.add('js-motion');

  /* Sichtbar schalten, sobald der Abschnitt ins Bild kommt */
  var beobachtet = document.querySelectorAll(
    '.bewegt, .nachzug, .staffel, .fuell, .hero, .material, .anriss');

  if (!('IntersectionObserver' in window)) {
    beobachtet.forEach(function (e) { e.classList.add('sichtbar'); });
    return;
  }

  var beobachter = new IntersectionObserver(function (eintraege) {
    eintraege.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('sichtbar');
      beobachter.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

  beobachtet.forEach(function (e) { beobachter.observe(e); });
})();
