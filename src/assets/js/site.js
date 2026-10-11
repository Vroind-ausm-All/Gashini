/* Gashini Dienstleistungen — Interaktionen
   Jede Funktion ist eine Verbesserung: Ohne JavaScript bleiben Navigation,
   Formular, Galerie und Vergleich vollständig nutzbar. */
(function () {
  'use strict';

  /* ---------- Navigation ---------- */
  var html = document.documentElement;
  var kopf = document.querySelector('.kopf');
  var knopf = document.querySelector('.menue-knopf');
  var nav = document.getElementById('hauptnav');
  var mobil = window.matchMedia('(max-width: 959px)');

  // Mobiles Menü: Vollbild unter dem Kopf. Die Oberkante folgt dem Kopf, auch wenn darüber
  // noch etwas steht (z. B. der Vorschau-Streifen).
  if (knopf && nav) {
    var oberkante = function () { html.style.setProperty('--menue-oben', Math.max(0, Math.round(kopf.getBoundingClientRect().bottom)) + 'px'); };
    var schliessen = function (fokusZurueck) {
      nav.classList.remove('offen');
      knopf.setAttribute('aria-expanded', 'false');
      knopf.querySelector('.text').textContent = 'Menü';
      document.body.classList.remove('menue-offen');
      if (fokusZurueck) knopf.focus();
    };
    knopf.addEventListener('click', function () {
      if (nav.classList.contains('offen')) return schliessen(false);
      kopf.classList.remove('kopf--weg'); html.classList.remove('kopf-weg');
      oberkante();
      nav.classList.add('offen');
      knopf.setAttribute('aria-expanded', 'true');
      knopf.querySelector('.text').textContent = 'Schließen';
      document.body.classList.add('menue-offen');
      var erster = nav.querySelector('a');
      if (erster) erster.focus({ preventScroll: true });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('offen')) schliessen(true);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('offen')) schliessen(false);
    });
    // Tab-Fokus bleibt im offenen Menü: vom letzten Element zurück zum Menü-Knopf
    nav.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !nav.classList.contains('offen')) return;
      var ziele = nav.querySelectorAll('a, button:not(.unter-knopf)');
      if (!e.shiftKey && document.activeElement === ziele[ziele.length - 1]) { e.preventDefault(); knopf.focus(); }
    });
    window.addEventListener('resize', function () { if (nav.classList.contains('offen')) oberkante(); });
    mobil.addEventListener('change', function (m) { if (!m.matches) schliessen(false); });
  }

  // Untermenü Leistungen (Desktop): Knopf, Hover und Fokus öffnen; Escape und Klick daneben schließen
  document.querySelectorAll('.hat-unter').forEach(function (eintrag) {
    var unterKnopf = eintrag.querySelector('.unter-knopf');
    if (!unterKnopf) return;
    var zu = function (fokus) {
      unterKnopf.setAttribute('aria-expanded', 'false');
      eintrag.classList.add('zu');
      if (fokus) unterKnopf.focus();
    };
    unterKnopf.addEventListener('click', function () {
      var offen = unterKnopf.getAttribute('aria-expanded') === 'true';
      if (offen) return zu(false);
      eintrag.classList.remove('zu');
      unterKnopf.setAttribute('aria-expanded', 'true');
    });
    eintrag.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !mobil.matches) { e.stopPropagation(); zu(true); } });
    eintrag.addEventListener('mouseleave', function () { eintrag.classList.remove('zu'); if (document.activeElement !== unterKnopf) unterKnopf.setAttribute('aria-expanded', 'false'); });
    eintrag.addEventListener('focusout', function (e) { if (!eintrag.contains(e.relatedTarget)) { eintrag.classList.remove('zu'); unterKnopf.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('click', function (e) { if (!eintrag.contains(e.target)) unterKnopf.setAttribute('aria-expanded', 'false'); });
  });

  // Kopf auf kleinen Bildschirmen beim Herunterscrollen ausblenden, beim Hochscrollen zeigen
  if (kopf) {
    var letzte = window.scrollY, geplant = false;
    window.addEventListener('scroll', function () {
      if (geplant) return;
      geplant = true;
      window.requestAnimationFrame(function () {
        geplant = false;
        var y = window.scrollY, delta = y - letzte;
        if (Math.abs(delta) < 6) return;
        var weg = mobil.matches && y > 160 && delta > 0 &&
          !document.body.classList.contains('menue-offen') && !kopf.contains(document.activeElement);
        kopf.classList.toggle('kopf--weg', weg);
        html.classList.toggle('kopf-weg', weg);
        letzte = y;
      });
    }, { passive: true });
  }

  var jahr = document.getElementById('jahr');
  if (jahr) jahr.textContent = String(new Date().getFullYear());

  /* ---------- Vorschau: Kundenansicht blendet Redaktionshinweise aus ----------
     Nur in der gekennzeichneten Vorschau vorhanden; der veröffentlichte Auftritt speichert nichts. */
  var schalter = document.querySelector('[data-kundenansicht]');
  if (schalter) {
    var setzeAnsicht = function (an) {
      document.documentElement.classList.toggle('kundenansicht', an);
      schalter.setAttribute('aria-pressed', String(an));
    };
    var gespeichert = false;
    try { gespeichert = window.localStorage.getItem('gashini-kundenansicht') === '1'; } catch (e) {}
    setzeAnsicht(gespeichert);
    schalter.addEventListener('click', function () {
      var an = schalter.getAttribute('aria-pressed') !== 'true';
      setzeAnsicht(an);
      try { window.localStorage.setItem('gashini-kundenansicht', an ? '1' : '0'); } catch (e) {}
    });
  }

  /* ---------- Anfrageformular ---------- */
  var form = document.querySelector('form[data-anfrage]');
  if (form) anfrageformular(form);

  function anfrageformular(form) {
    var geladen = Date.now();
    var status = form.querySelector('.formular-status');
    var senden = form.querySelector('button[type="submit"]');
    var sendetext = senden.querySelector('.text');
    var laeuft = false;
    var MAX_FOTOS = 3, MAX_BYTES = 12 * 1024 * 1024, TYPEN = ['image/jpeg', 'image/png', 'image/webp'];

    function feld(name) { return form.elements[name]; }
    var fotos = form.querySelector('input[type="file"]');
    var rueckruf = feld('rueckruf');
    var rueckrufZeit = form.querySelector('[data-rueckruf-zeit]');

    // Vorauswahl aus der Adresse: ?leistung=reparatur&anliegen=Tür+schleift
    var parameter = new URLSearchParams(window.location.search);
    var schluessel = parameter.get('leistung');
    if (schluessel) {
      var option = form.querySelector('#f-leistung option[data-schluessel="' + schluessel.replace(/[^a-z-]/g, '') + '"]');
      if (option) option.selected = true;
    }
    var anliegen = (parameter.get('anliegen') || '').replace(/[^\wäöüÄÖÜß .,\-]/g, '').slice(0, 80);
    if (anliegen && !feld('nachricht').value) feld('nachricht').value = anliegen + ': ';

    // Rückruf: Zeitfenster nur zeigen, wenn gewünscht
    function rueckrufAnzeigen() { if (rueckrufZeit) rueckrufZeit.hidden = !rueckruf.checked; }
    if (rueckruf) { rueckruf.addEventListener('change', rueckrufAnzeigen); rueckrufAnzeigen(); }

    // Fotos: Liste der gewählten Dateien
    var liste = form.querySelector('[data-dateiliste]');
    function fotoFehler() {
      if (!fotos || !fotos.files) return '';
      var dateien = Array.prototype.slice.call(fotos.files);
      if (dateien.length > MAX_FOTOS) return 'Bitte wählen Sie höchstens ' + MAX_FOTOS + ' Fotos aus.';
      if (dateien.some(function (d) { return TYPEN.indexOf(d.type) < 0; })) return 'Bitte nur Fotos als JPEG, PNG oder WebP hochladen.';
      var summe = dateien.reduce(function (s, d) { return s + d.size; }, 0);
      if (summe > MAX_BYTES) return 'Die Fotos sind zusammen zu groß (höchstens 12 MB). Bitte wählen Sie weniger oder kleinere Bilder.';
      return '';
    }
    if (fotos && liste) fotos.addEventListener('change', function () {
      liste.textContent = '';
      Array.prototype.slice.call(fotos.files || []).forEach(function (d) {
        var li = document.createElement('li');
        li.textContent = d.name + ' · ' + (d.size / 1024 / 1024).toFixed(1).replace('.', ',') + ' MB';
        liste.appendChild(li);
      });
      setzeFehler('fotos', fotoFehler());
    });

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
    var FELDER = ['name', 'email', 'telefon', 'rueckruf', 'leistung', 'nachricht', 'fotos', 'ort', 'zeitraum'];

    function fehlerElement(name) { return form.querySelector('[data-fehler-fuer="' + name + '"]'); }
    function setzeFehler(name, text) {
      var el = name === 'fotos' ? fotos : feld(name), ziel = fehlerElement(name);
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
      if (rueckruf && rueckruf.checked && !feld('telefon').value.trim()) {
        fehler.telefon = fehler.telefon || 'Für einen Rückruf brauchen wir Ihre Telefonnummer.';
      }
      var f = fotoFehler(); if (f) fehler.fotos = f;
      return fehler;
    }

    function zeigeFehler(fehler, meldung) {
      FELDER.forEach(function (n) { setzeFehler(n, fehler[n]); });
      var namen = FELDER.filter(function (n) { return fehler[n]; });
      if (!namen.length) return;
      status.className = 'formular-status formular-status--fehler';
      status.textContent = meldung || (namen.length === 1
        ? 'Ein Feld muss noch korrigiert werden.'
        : namen.length + ' Felder müssen noch korrigiert werden.');
      var erstes = namen[0] === 'fotos' ? fotos : feld(namen[0]);
      if (erstes) erstes.focus();
    }

    ['name', 'email', 'telefon', 'leistung', 'nachricht'].forEach(function (n) {
      var el = feld(n); if (!el) return;
      el.addEventListener('blur', function () {
        if (el.getAttribute('aria-invalid') === 'true' || el.value) setzeFehler(n, regeln[n](el.value.trim()));
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
      status.textContent = fotos && fotos.files && fotos.files.length ? 'Ihre Anfrage und die Fotos werden übertragen …' : 'Ihre Anfrage wird übertragen …';
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

  /* ---------- Projektfilter (mit Flip, wenn bewegung.js es bereitstellt) ---------- */
  var filter = document.querySelector('.filter');
  if (filter) {
    var karten = Array.prototype.slice.call(document.querySelectorAll('[data-projekt]'));
    var ansage = document.getElementById('filter-ansage');
    filter.addEventListener('change', function (e) {
      var wert = e.target.value;
      var sichtbar = function (k) { return wert === 'alle' || k.getAttribute('data-kategorie') === wert; };
      if (typeof window.gashiniUmordnen === 'function') window.gashiniUmordnen(karten, sichtbar);
      else karten.forEach(function (k) { k.hidden = !sichtbar(k); });
      var n = karten.filter(sichtbar).length;
      if (ansage) ansage.textContent = n === 1 ? '1 Projekt angezeigt' : n + ' Projekte angezeigt';
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
    var zeige = function (i) {
      aktuell = (i + ausloeser.length) % ausloeser.length;
      var a = ausloeser[aktuell];
      bild.src = a.getAttribute('data-gross');
      bild.alt = a.getAttribute('data-alt') || '';
      text.textContent = a.getAttribute('data-text') || '';
      zaehler.textContent = (aktuell + 1) + ' / ' + ausloeser.length;
    };
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
