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

  // Kopf auf kleinen Bildschirmen beim Herunterscrollen ausblenden, beim Hochscrollen zeigen.
  // Ab 960 px verdichtet er sich stattdessen: Kompakt-Logo statt Hauptvariante, flachere Leiste.
  if (kopf) {
    var letzte = window.scrollY, geplant = false;
    var verdichten = function () {
      var klein = !mobil.matches && window.scrollY > 72;
      kopf.classList.toggle('kopf--klein', klein);
      html.classList.toggle('kopf-klein', klein);
    };
    verdichten();
    mobil.addEventListener('change', verdichten);
    window.addEventListener('scroll', function () {
      if (geplant) return;
      geplant = true;
      window.requestAnimationFrame(function () {
        geplant = false;
        verdichten();
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

  // Seiten beginnen oben (frueh.js schaltet die Wiederherstellung durch den Browser ab). Auch eine aus dem
  // Zurück-Cache wiederhergestellte Seite springt nach oben. Mit Sprungmarke bleibt das Ziel erhalten.
  var nachOben = function () {
    if (window.location.hash && window.location.hash.length > 1) return;
    try { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, 0); }
  };
  // Eingebettete Vorschauen (z. B. claude.ai) stellen nach dem Laden die Scroll-Position der vorigen Seite wieder
  // her – die neue Seite stünde dann unten. Deshalb hält die Seite dort kurz die Position oben bzw. an der
  // Sprungmarke, bis der Besucher selbst scrollt, tippt oder eine Taste drückt (spätestens 4 s nach dem Laden).
  // Als eigenständige Website nicht nötig.
  var eingebettet = false;
  try { eingebettet = window.self !== window.top; } catch (e) { eingebettet = true; }
  var obenHalten = function () {
    if (!eingebettet) return;
    var marke = window.location.hash && window.location.hash.length > 1 ? window.location.hash.slice(1) : '';
    var eingaben = ['wheel', 'touchstart', 'pointerdown', 'keydown'];
    var pruefen = function () {
      if (!marke) { if ((window.scrollY || window.pageYOffset) > 0) nachOben(); return; }
      var ziel = null;
      try { ziel = document.getElementById(decodeURIComponent(marke)); } catch (e) {}
      if (!ziel) return;
      try { ziel.scrollIntoView({ block: 'start', behavior: 'instant' }); } catch (e) { ziel.scrollIntoView(true); }
    };
    var ende = function () {
      window.removeEventListener('scroll', pruefen);
      eingaben.forEach(function (n) { window.removeEventListener(n, ende, true); });
    };
    window.addEventListener('scroll', pruefen, { passive: true });
    eingaben.forEach(function (n) { window.addEventListener(n, ende, { capture: true, passive: true }); });
    var spaeter = function () { window.setTimeout(ende, 4000); };
    if (document.readyState === 'complete') spaeter(); else window.addEventListener('load', spaeter);
    window.setTimeout(ende, 12000);
  };
  nachOben();
  obenHalten();
  window.addEventListener('pageshow', function (e) { if (e.persisted) { nachOben(); obenHalten(); } });

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
    // Link für Kunden: …/?ansicht=kunde schaltet die Kundenansicht ein und merkt sie sich für die weiteren Seiten
    // (…/?ansicht=intern schaltet sie wieder aus).
    var gewuenscht = (window.location.search.match(/[?&]ansicht=(kunde|intern)\b/) || [])[1];
    if (gewuenscht) {
      gespeichert = gewuenscht === 'kunde';
      try { window.localStorage.setItem('gashini-kundenansicht', gespeichert ? '1' : '0'); } catch (e) {}
    }
    setzeAnsicht(gespeichert);
    schalter.addEventListener('click', function () {
      var an = schalter.getAttribute('aria-pressed') !== 'true';
      setzeAnsicht(an);
      try { window.localStorage.setItem('gashini-kundenansicht', an ? '1' : '0'); } catch (e) {}
    });
  }

  /* ---------- Einsatzgebiet: Auswahl auf Karte und Liste, Landkreise, Ortssuche, PLZ-Prüfung ----------
     Ohne JavaScript sind Kartenpunkte und Liste normale Links ins Formular. Mit JavaScript wählt ein Klick (oder die
     Eingabetaste) einen Ort bzw. Landkreis aus, hebt ihn hervor und zeigt die passende Anfrage. Eine Postleitzahl wird
     nur vorbelegt, wenn sie eindeutig und geprüft ist – sonst wählt der Besucher sie selbst. Alles per textContent. */
  var karte = document.querySelector('[data-einsatzkarte]');
  var auswahl = document.querySelector('[data-ort-auswahl]');
  var kreisFilter = document.querySelector('[data-kreis-filter]');
  var element = function (tag, klasse, text) { var el = document.createElement(tag); if (klasse) el.className = klasse; if (text) el.textContent = text; return el; };
  var pfeil = function (a) { var s = element('span', 'pfeil', '→'); s.setAttribute('aria-hidden', 'true'); a.appendChild(document.createTextNode(' ')); a.appendChild(s); return a; };
  var kontaktLink = function (werte) {
    var ziel = new URL((auswahl && auswahl.getAttribute('data-kontakt')) || '../kontakt/#anfrage', window.location.href);
    Object.keys(werte).forEach(function (k) { if (werte[k]) ziel.searchParams.set(k, werte[k]); });
    return ziel.href;
  };

  if (karte && auswahl) {
    var gebiet = { kreise: {} };
    try { gebiet = JSON.parse(auswahl.getAttribute('data-gebiet')) || gebiet; } catch (e) {}
    var punkte = Array.prototype.slice.call(karte.querySelectorAll('.ek-ort, .ek-mitte'));
    var leer = auswahl.innerHTML;

    var markieren = function (fn) {
      punkte.forEach(function (p) { p.classList.remove('ist-gewaehlt', 'im-kreis'); });
      karte.classList.remove('kreis-gewaehlt');
      if (fn) fn();
    };
    var kreisKnoepfe = function (id) {
      if (!kreisFilter) return;
      kreisFilter.querySelectorAll('button').forEach(function (k) { k.setAttribute('aria-pressed', String(k.getAttribute('data-kreis') === id)); });
    };
    var aufheben = function () {
      markieren(); kreisKnoepfe('');
      auswahl.innerHTML = leer;
      auswahl.classList.remove('hat-auswahl');
    };
    var auswahlKopf = function (art, titel) {
      auswahl.textContent = '';
      auswahl.classList.add('hat-auswahl');
      auswahl.appendChild(element('p', 'auswahl-art', art));
      auswahl.appendChild(element('p', 'auswahl-titel', titel));
    };
    var fuss = function () {
      var weg = element('button', 'auswahl-weg', 'Auswahl aufheben');
      weg.type = 'button';
      weg.addEventListener('click', function () { aufheben(); var erster = punkte[0]; if (erster) erster.focus({ preventScroll: true }); });
      auswahl.appendChild(weg);
    };
    var sichtbarMachen = function () {
      // Auswahl liegt unter der Karte (Handy) oder daneben (Desktop): nur scrollen, wenn sie kaum sichtbar ist –
      // dann so, dass sie in der oberen Hälfte steht (unten liegt auf dem Handy die Schnellkontakt-Leiste)
      var r = auswahl.getBoundingClientRect();
      if (r.top > window.innerHeight - 180 || r.bottom < 60) {
        window.scrollBy({ top: r.top - window.innerHeight * 0.35, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      }
    };

    var waehleOrt = function (punkt, ohneScroll) {
      var name = punkt.getAttribute('data-ort');
      var plzListe = (punkt.getAttribute('data-plz') || '').split(' ').filter(Boolean);
      var geprueft = punkt.getAttribute('data-geprueft') === '1';
      var km = parseInt(punkt.getAttribute('data-km'), 10);
      var kreisId = punkt.getAttribute('data-kreis') || '';
      var kreis = gebiet.kreise[kreisId];
      markieren(function () { punkt.classList.add('ist-gewaehlt'); });
      kreisKnoepfe('');
      var istStadt = punkt.classList.contains('ek-mitte');
      auswahlKopf(istStadt ? 'Alle Stadtbezirke' : [kreis ? kreis.name : '', km > 0 ? 'etwa ' + km + ' km ab Stuttgart-Mitte' : ''].filter(Boolean).join(' · '), name);
      var link = pfeil(element('a', 'knopf knopf--primaer auswahl-anfrage', 'Projekt in ' + name + ' anfragen'));
      var gewaehltePlz = plzListe.length === 1 && geprueft ? plzListe[0] : '';
      var setzeLink = function () { link.href = kontaktLink({ ort: name, plz: gewaehltePlz }); };
      if (!istStadt && plzListe.length && !(plzListe.length === 1 && geprueft)) {
        auswahl.appendChild(element('p', 'auswahl-text', plzListe.length > 1 ? 'Ihre Postleitzahl (optional):' : 'Postleitzahl übernehmen (optional):'));
        var gruppe = element('div', 'auswahl-plz');
        gruppe.setAttribute('role', 'group');
        gruppe.setAttribute('aria-label', 'Postleitzahl für ' + name);
        plzListe.forEach(function (z) {
          var b = element('button', '', z);
          b.type = 'button';
          b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () {
            gewaehltePlz = gewaehltePlz === z ? '' : z;
            gruppe.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x.textContent === gewaehltePlz)); });
            link.textContent = 'Projekt in ' + (gewaehltePlz ? gewaehltePlz + ' ' : '') + name + ' anfragen'; pfeil(link);
            setzeLink();
          });
          gruppe.appendChild(b);
        });
        auswahl.appendChild(gruppe);
      } else if (gewaehltePlz) {
        auswahl.appendChild(element('p', 'auswahl-text', 'Postleitzahl ' + gewaehltePlz + ' wird eingetragen.'));
      } else if (istStadt) {
        var bezirke = element('a', 'textlink', 'Stadtbezirk in der Liste wählen');
        bezirke.href = '#kreis-stuttgart';
        auswahl.appendChild(bezirke);
      }
      setzeLink();
      auswahl.appendChild(link);
      fuss();
      if (!ohneScroll) sichtbarMachen();
    };

    var waehleKreis = function (id) {
      var kreis = gebiet.kreise[id];
      if (!kreis) return aufheben();
      markieren(function () {
        karte.classList.add('kreis-gewaehlt');
        punkte.forEach(function (p) { if (p.getAttribute('data-kreis') === id) p.classList.add('im-kreis'); });
      });
      kreisKnoepfe(id);
      auswahlKopf(kreis.kreis ? 'Landkreis · ' + kreis.orte.length + ' Orte' : kreis.orte.length + ' Orte', kreis.name);
      auswahl.appendChild(element('p', 'auswahl-text', 'Ihren Ort wählen:'));
      var liste = element('ul', 'auswahl-orte');
      kreis.orte.forEach(function (name) {
        var punkt = punkte.filter(function (p) { return p.getAttribute('data-ort') === name; })[0];
        if (!punkt) return;
        var li = element('li'), b = element('button', '', name);
        b.type = 'button';
        b.addEventListener('mouseenter', function () { punkt.classList.add('ist-vorschau'); });
        b.addEventListener('mouseleave', function () { punkt.classList.remove('ist-vorschau'); });
        b.addEventListener('click', function () { punkt.classList.remove('ist-vorschau'); waehleOrt(punkt, true); var a = auswahl.querySelector('.auswahl-plz button, .auswahl-anfrage'); if (a) a.focus(); });
        li.appendChild(b); liste.appendChild(li);
      });
      auswahl.appendChild(liste);
      if (kreis.kreis) {
        var a = pfeil(element('a', 'knopf knopf--sekundaer auswahl-anfrage', 'Projekt im ' + kreis.name + ' anfragen'));
        a.href = kontaktLink({ kreis: kreis.name });
        auswahl.appendChild(a);
      }
      fuss();
    };

    // Karte: Klick wählt aus (statt sofort zu springen); Pfeiltasten wechseln den Punkt (roving tabindex)
    var fokus = function (i) {
      var n = (i + punkte.length) % punkte.length;
      punkte.forEach(function (p, j) { p.setAttribute('tabindex', j === n ? '0' : '-1'); });
      punkte[n].focus();
    };
    karte.addEventListener('click', function (e) {
      var punkt = e.target.closest('.ek-ort, .ek-mitte');
      if (!punkt) return;
      e.preventDefault();
      punkte.forEach(function (p) { p.setAttribute('tabindex', p === punkt ? '0' : '-1'); });
      waehleOrt(punkt);
    });
    karte.addEventListener('keydown', function (e) {
      var punkt = e.target.closest('.ek-ort, .ek-mitte');
      if (!punkt) return;
      var i = punkte.indexOf(punkt);
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); fokus(i + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); fokus(i - 1); }
      else if (e.key === 'Home') { e.preventDefault(); fokus(0); }
      else if (e.key === 'End') { e.preventDefault(); fokus(punkte.length - 1); }
      else if (e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); waehleOrt(punkt); }
      else if (e.key === 'Escape') { aufheben(); }
    });

    if (kreisFilter) {
      kreisFilter.addEventListener('click', function (e) {
        var knopf = e.target.closest('button');
        if (!knopf) return;
        var id = knopf.getAttribute('data-kreis');
        if (knopf.getAttribute('aria-pressed') === 'true') aufheben(); else waehleKreis(id);
      });
      // Vorschau beim Überfahren der Kreis-Knöpfe
      kreisFilter.addEventListener('mouseover', function (e) {
        var knopf = e.target.closest('button'); if (!knopf) return;
        var id = knopf.getAttribute('data-kreis');
        punkte.forEach(function (p) { p.classList.toggle('kreis-vorschau', p.getAttribute('data-kreis') === id); });
      });
      kreisFilter.addEventListener('mouseleave', function () { punkte.forEach(function (p) { p.classList.remove('kreis-vorschau'); }); });
    }
  }

  // Ortssuche über der Liste
  var suche = document.querySelector('[data-ort-suche]');
  var gruppen = document.querySelector('[data-ortsgruppen]');
  if (suche && gruppen) {
    suche.hidden = false;
    var feldSuche = suche.querySelector('input');
    var stand = suche.querySelector('.ort-suche-stand');
    var keinTreffer = suche.querySelector('.ort-suche-leer');
    var keinLink = suche.querySelector('[data-ort-suche-anfrage]');
    var normal = function (s) {
      return s.toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
    };
    var eintraege = Array.prototype.slice.call(gruppen.querySelectorAll('.ort-eintrag'));
    var filtern = function () {
      var q = normal(feldSuche.value);
      var treffer = 0;
      eintraege.forEach(function (li) { var ja = !q || li.getAttribute('data-suche').indexOf(q) > -1; li.hidden = !ja; if (ja) treffer++; });
      gruppen.querySelectorAll('.ortsgruppe').forEach(function (g) { g.hidden = !!q && !g.querySelector('.ort-eintrag:not([hidden])'); });
      stand.textContent = q ? (treffer === 1 ? '1 Ort gefunden' : treffer + ' Orte gefunden') : '';
      keinTreffer.hidden = !q || treffer > 0;
      if (q && !treffer) {
        var roh = feldSuche.value.trim();
        keinLink.href = kontaktLink(/^\d{5}$/.test(roh) ? { plz: roh } : /^[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß .()\-]{1,59}$/.test(roh) ? { ort: roh } : {});
      }
    };
    feldSuche.addEventListener('input', filtern);
  }

  // PLZ-Prüfung
  var pruefer = document.querySelector('[data-plz-pruefer]');
  if (pruefer) {
    var orte = {};
    try { orte = JSON.parse(pruefer.getAttribute('data-orte')) || {}; } catch (e) {}
    var eingabe = pruefer.querySelector('input');
    var ergebnis = pruefer.querySelector('[data-plz-ergebnis]');
    pruefer.noValidate = true; // eigene, verständlichere Meldung statt der Browser-Blase
    var knopfLink = function (href, text) { var a = pfeil(element('a', 'knopf knopf--primaer', text)); a.href = href; return a; };
    pruefer.addEventListener('submit', function (e) {
      e.preventDefault();
      var plz = eingabe.value.replace(/\D/g, '');
      ergebnis.textContent = '';
      if (karte) karte.querySelectorAll('.ist-markiert').forEach(function (p) { p.classList.remove('ist-markiert'); });
      if (plz.length !== 5) {
        ergebnis.appendChild(element('p', 'plz-hinweis', 'Bitte geben Sie eine fünfstellige Postleitzahl ein.'));
        eingabe.focus();
        return;
      }
      var t = orte[plz];
      if (t) {
        ergebnis.appendChild(element('p', 'plz-ok', plz + ' (' + t[0] + ') gehört zu unserem Einsatzgebiet' + (t[1] > 0 ? ' – etwa ' + t[1] + ' km Luftlinie ab Stuttgart-Mitte.' : '.')));
        // Die eingegebene PLZ stammt vom Besucher; den Ortsnamen dazu nur, wenn die Zuordnung geprüft ist
        ergebnis.appendChild(knopfLink(kontaktLink(t[2] ? { ort: t[0], plz: plz } : { plz: plz }), 'Projekt in ' + plz + ' ' + t[0] + ' anfragen'));
        if (karte) karte.querySelectorAll('[data-plz]').forEach(function (p) {
          if ((' ' + p.getAttribute('data-plz') + ' ').indexOf(' ' + plz + ' ') > -1) p.classList.add('ist-markiert');
        });
      } else {
        ergebnis.appendChild(element('p', 'plz-hinweis', 'Die Postleitzahl ' + plz + ' steht nicht in unserer Liste. Fragen Sie trotzdem an – wir sagen Ihnen, ob wir zu Ihnen kommen.'));
        ergebnis.appendChild(knopfLink(kontaktLink({ plz: plz }), 'Anfrage mit PLZ ' + plz + ' stellen'));
      }
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
    // Seite „Einsatzgebiet“: ?ort=Kornwestheim&plz=70806 bzw. ?kreis=Landkreis%20Ludwigsburg füllen „PLZ oder Ort“.
    // Nur gültige Werte: PLZ fünfstellig, Ort aus Buchstaben (auch Bindestrich, Klammern), Kreis in bekannter Form.
    // Die alte Form ?ort=73760%20Ostfildern bleibt lesbar. Der Besucher kann alles ändern.
    var lese = function (n) { return (parameter.get(n) || '').replace(/\s+/g, ' ').trim(); };
    var plzVorgabe = lese('plz');
    var ortVorgabe = lese('ort');
    var altform = ortVorgabe.match(/^(\d{5}) (.+)$/);
    if (altform) { if (!plzVorgabe) plzVorgabe = altform[1]; ortVorgabe = altform[2]; }
    if (!/^\d{5}$/.test(plzVorgabe)) plzVorgabe = '';
    if (!/^[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß .()\-]{0,59}$/.test(ortVorgabe)) ortVorgabe = '';
    var kreisVorgabe = lese('kreis');
    if (!/^(Landkreis [A-ZÄÖÜ][A-Za-zäöüß\-]{2,30}|[A-ZÄÖÜ][A-Za-zäöüß]+(-[A-ZÄÖÜ][A-Za-zäöüß]+)*-Kreis)$/.test(kreisVorgabe)) kreisVorgabe = '';
    var ortWert = [plzVorgabe, ortVorgabe].filter(Boolean).join(' ') || kreisVorgabe;
    if (ortWert && feld('ort') && !feld('ort').value) {
      feld('ort').value = ortWert;
      var ortHinweis = form.querySelector('#f-ort-hinweis');
      if (ortHinweis) ortHinweis.hidden = false;
    }

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

  /* ---------- Bewegtbilder: stumme Kurzclips über einem Standbild ----------
     Spielen nur im Sichtbereich, nie bei reduzierter Bewegung oder Datensparen. Das Standbild darunter bleibt
     sichtbar, bis der Clip läuft. Ein Knopf hält an (WCAG 2.2.2); angehalten bleibt angehalten. */
  var clips = document.querySelectorAll('video[data-bewegtbild]');
  var netz = navigator.connection || {};
  var sparen = netz.saveData === true || /2g$/.test(netz.effectiveType || '');
  if (clips.length && !sparen && 'IntersectionObserver' in window) {
    var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)');
    var abspielen = function (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    var knopfFuer = function (v) {
      if (v.nextElementSibling && v.nextElementSibling.classList.contains('bewegtbild-knopf')) return;
      var k = document.createElement('button');
      k.type = 'button';
      k.className = 'bewegtbild-knopf';
      k.setAttribute('aria-label', 'Video anhalten');
      k.addEventListener('click', function () {
        var halt = !v.paused;
        if (halt) { v.dataset.angehalten = 'ja'; v.pause(); } else { delete v.dataset.angehalten; abspielen(v); }
        k.classList.toggle('pausiert', halt);
        k.setAttribute('aria-label', halt ? 'Video abspielen' : 'Video anhalten');
      });
      v.insertAdjacentElement('afterend', k);
    };
    var sicht = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting && !ruhig.matches && !v.dataset.angehalten) abspielen(v); else v.pause();
      });
    }, { threshold: .25 });
    clips.forEach(function (v) {
      v.addEventListener('playing', function () { v.classList.add('laeuft'); knopfFuer(v); });
      sicht.observe(v);
    });
    ruhig.addEventListener('change', function () {
      if (ruhig.matches) clips.forEach(function (v) { v.pause(); v.classList.remove('laeuft'); });
    });
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
