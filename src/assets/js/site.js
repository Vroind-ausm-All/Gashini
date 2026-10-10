/* Gashini Dienstleistungen — Interaktionen
   Jede Funktion ist eine Verbesserung: Ohne JavaScript bleiben Navigation,
   Formular, Galerie und Vergleich vollständig nutzbar. */
(function () {
  'use strict';

  /* ---------- Mobile Navigation ---------- */
  var knopf = document.querySelector('.menue-knopf');
  var nav = document.getElementById('hauptnav');
  if (knopf && nav) {
    var schliessen = function (fokusZurueck) {
      nav.classList.remove('offen');
      knopf.setAttribute('aria-expanded', 'false');
      knopf.querySelector('.text').textContent = 'Menü';
      document.body.classList.remove('menue-offen');
      if (fokusZurueck) knopf.focus();
    };
    knopf.addEventListener('click', function () {
      var offen = !nav.classList.contains('offen');
      if (!offen) return schliessen(false);
      nav.classList.add('offen');
      knopf.setAttribute('aria-expanded', 'true');
      knopf.querySelector('.text').textContent = 'Schließen';
      document.body.classList.add('menue-offen');
      var erster = nav.querySelector('a');
      if (erster) erster.focus();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('offen')) schliessen(true);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) schliessen(false);
    });
    window.matchMedia('(min-width: 960px)').addEventListener('change', function (m) {
      if (m.matches) schliessen(false);
    });
  }

  var jahr = document.getElementById('jahr');
  if (jahr) jahr.textContent = String(new Date().getFullYear());

  /* ---------- Anfrageformular ---------- */
  var form = document.querySelector('form[data-anfrage]');
  if (form) anfrageformular(form);

  function anfrageformular(form) {
    var geladen = Date.now();
    var status = form.querySelector('.formular-status');
    var senden = form.querySelector('button[type="submit"]');
    var sendetext = senden.querySelector('.text');
    var laeuft = false;

    var regeln = {
      name: function (v) { return !v ? 'Bitte geben Sie Ihren Namen an.' : v.length > 100 ? 'Der Name ist zu lang (höchstens 100 Zeichen).' : ''; },
      email: function (v) {
        if (!v) return '';
        if (v.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Bitte prüfen Sie die E-Mail-Adresse.';
        return '';
      },
      telefon: function (v) {
        if (!v) return '';
        if (v.length > 40 || !/^[0-9+()\/\-\s]{6,}$/.test(v)) return 'Bitte geben Sie eine Telefonnummer mit Ziffern an.';
        return '';
      },
      leistung: function (v) { return v ? '' : 'Bitte wählen Sie aus, worum es geht.'; },
      nachricht: function (v) {
        if (!v) return 'Bitte beschreiben Sie kurz Ihr Vorhaben.';
        if (v.length < 10) return 'Bitte beschreiben Sie Ihr Vorhaben in ein paar Worten mehr.';
        if (v.length > 4000) return 'Die Beschreibung ist zu lang (höchstens 4000 Zeichen).';
        return '';
      }
    };

    function feld(name) { return form.elements[name]; }
    function fehlerElement(name) { return form.querySelector('[data-fehler-fuer="' + name + '"]'); }

    function setzeFehler(name, text) {
      var el = feld(name), ziel = fehlerElement(name);
      if (!el || !ziel) return;
      ziel.textContent = text || '';
      if (text) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid');
    }

    function pruefe() {
      var fehler = {};
      Object.keys(regeln).forEach(function (n) {
        var el = feld(n); if (!el) return;
        var t = regeln[n](el.value.trim());
        if (t) fehler[n] = t;
      });
      if (!feld('email').value.trim() && !feld('telefon').value.trim()) {
        fehler.email = fehler.email || 'Bitte geben Sie eine E-Mail-Adresse oder eine Telefonnummer an.';
      }
      return fehler;
    }

    function zeigeFehler(fehler, meldung) {
      ['name', 'email', 'telefon', 'leistung', 'nachricht', 'ort', 'zeitraum'].forEach(function (n) {
        setzeFehler(n, fehler[n]);
      });
      var namen = Object.keys(fehler);
      if (!namen.length) return;
      status.className = 'formular-status formular-status--fehler';
      status.textContent = meldung || (namen.length === 1
        ? 'Ein Feld muss noch korrigiert werden.'
        : namen.length + ' Felder müssen noch korrigiert werden.');
      var erstes = feld(namen[0]);
      if (erstes) erstes.focus();
    }

    ['name', 'email', 'telefon', 'leistung', 'nachricht'].forEach(function (n) {
      var el = feld(n); if (!el) return;
      el.addEventListener('blur', function () {
        if (el.getAttribute('aria-invalid') === 'true' || el.value) {
          var t = regeln[n](el.value.trim());
          setzeFehler(n, t);
        }
      });
    });

    function sperre(an) {
      laeuft = an;
      senden.setAttribute('aria-disabled', an ? 'true' : 'false');
      sendetext.textContent = an ? 'Wird gesendet …' : 'Anfrage senden';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (laeuft) return;
      var fehler = pruefe();
      if (Object.keys(fehler).length) { zeigeFehler(fehler); return; }
      zeigeFehler({});
      status.className = 'formular-status formular-status--laeuft';
      status.textContent = 'Ihre Anfrage wird übertragen …';
      sperre(true);

      var daten = new FormData(form);
      daten.set('ausfuellzeit', String(Math.round((Date.now() - geladen) / 1000)));

      fetch(form.action, { method: 'POST', body: daten, headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
        .then(function (r) {
          return r.json().catch(function () { return { ok: false, meldung: '' }; })
            .then(function (j) { j._status = r.status; return j; });
        })
        .then(function (antwort) {
          if (antwort.ok && antwort.weiter) {
            status.textContent = 'Anfrage angenommen. Sie werden weitergeleitet …';
            window.location.assign(antwort.weiter);
            return;
          }
          sperre(false);
          if (antwort.fehler && Object.keys(antwort.fehler).length) {
            zeigeFehler(antwort.fehler, antwort.meldung);
          } else {
            status.className = 'formular-status formular-status--fehler';
            status.textContent = antwort.meldung ||
              'Die Anfrage konnte gerade nicht übermittelt werden. Ihre Eingaben bleiben erhalten – bitte versuchen Sie es später erneut oder rufen Sie uns an.';
            status.focus();
          }
        })
        .catch(function () {
          sperre(false);
          status.className = 'formular-status formular-status--fehler';
          status.textContent = 'Keine Verbindung zum Server. Ihre Eingaben bleiben erhalten – bitte prüfen Sie Ihre Internetverbindung oder rufen Sie uns an.';
          status.focus();
        });
    });
  }

  /* ---------- Danke-Seite: Vorgangsnummer anzeigen ---------- */
  var refZiel = document.querySelector('[data-vorgang]');
  if (refZiel) {
    var ref = new URLSearchParams(window.location.search).get('ref');
    if (ref && /^[A-Z0-9]{6,12}$/.test(ref)) {
      refZiel.querySelector('.nummer').textContent = ref;
      refZiel.hidden = false;
    }
  }

  /* ---------- Projektfilter ---------- */
  var filter = document.querySelector('.filter');
  if (filter) {
    var karten = Array.prototype.slice.call(document.querySelectorAll('[data-kategorie]'));
    var ansage = document.getElementById('filter-ansage');
    filter.addEventListener('change', function (e) {
      var wert = e.target.value;
      var sichtbar = 0;
      karten.forEach(function (k) {
        var treffer = wert === 'alle' || k.getAttribute('data-kategorie') === wert;
        k.hidden = !treffer;
        if (treffer) sichtbar++;
      });
      if (ansage) ansage.textContent = sichtbar === 1 ? '1 Projekt angezeigt' : sichtbar + ' Projekte angezeigt';
    });
  }

  /* ---------- Bildansicht ---------- */
  var dialog = document.querySelector('.bildansicht');
  var ausloeser = Array.prototype.slice.call(document.querySelectorAll('[data-gross]'));
  if (dialog && ausloeser.length && typeof dialog.showModal === 'function') {
    var bild = dialog.querySelector('img');
    var text = dialog.querySelector('figcaption');
    var zaehler = dialog.querySelector('.zaehler');
    var aktuell = 0, zuletzt = null;
    function zeige(i) {
      aktuell = (i + ausloeser.length) % ausloeser.length;
      var a = ausloeser[aktuell];
      bild.src = a.getAttribute('data-gross');
      bild.alt = a.getAttribute('data-alt') || '';
      text.textContent = a.getAttribute('data-text') || '';
      zaehler.textContent = (aktuell + 1) + ' / ' + ausloeser.length;
    }
    ausloeser.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        zuletzt = a;
        zeige(i);
        dialog.showModal();
      });
    });
    dialog.querySelector('[data-zurueck]').addEventListener('click', function () { zeige(aktuell - 1); });
    dialog.querySelector('[data-weiter]').addEventListener('click', function () { zeige(aktuell + 1); });
    dialog.querySelector('[data-schliessen]').addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') zeige(aktuell - 1);
      if (e.key === 'ArrowRight') zeige(aktuell + 1);
    });
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', function () { if (zuletzt) zuletzt.focus(); });
  }

  /* ---------- Vorher/Nachher ---------- */
  document.querySelectorAll('.vergleich').forEach(function (v) {
    var regler = v.querySelector('.vergleich-regler');
    var buehne = v.querySelector('.vergleich-buehne');
    if (!regler || !buehne) return;
    var setze = function () {
      buehne.style.setProperty('--pos', regler.value + '%');
      regler.setAttribute('aria-valuetext', regler.value + ' Prozent Vorher-Bild sichtbar');
    };
    regler.addEventListener('input', setze);
    setze();
  });
})();
