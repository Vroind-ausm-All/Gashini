/* Gashini Dienstleistungen — Bewegung (GSAP) und Wandaufbau (Three.js)
   Prinzip: Bewegung erklärt Aufbau. Ohne JavaScript, ohne GSAP oder bei reduzierter
   Bewegung bleibt jeder Inhalt sichtbar und bedienbar. Siehe docs/CREATIVE-DIRECTION.md.

   Signature Motions:
   1 Architectural Hero      – Zeilen und Wand per CSS (kritischer Pfad), Beschriftung per DrawSVG
   2 Wall Construction       – Three.js-Modell, auf großen Bildschirmen an den Scrollfortschritt gekoppelt
   3 Project Reveal          – Bildmasken entlang der Kante, Filter mit Flip
   4 Netzwerk-Geschichte     – das Schema der Netzwerk-Seite wächst mit dem Scrollen in fünf Stufen
   5 Tiefe                   – Lichtflächen und Linien im Seitenkopf und die Leistungskarten folgen der Maus um wenige Pixel */
(function () {
  'use strict';
  var html = document.documentElement;
  var start = (window.performance && performance.now()) || 0;
  var gsap = window.gsap;
  var ST = window.ScrollTrigger;
  var bewegt = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: no-preference)').matches);
  var skriptUrl = document.currentScript && document.currentScript.src;

  var wand = [];
  document.querySelectorAll('[data-wandaufbau]').forEach(function (s) { wand.push(wandaufbau(s)); });

  if (!gsap || !ST) { html.classList.add('bewegung-bereit'); return; }
  gsap.registerPlugin(ST);
  if (window.SplitText) gsap.registerPlugin(window.SplitText);
  if (window.DrawSVGPlugin) gsap.registerPlugin(window.DrawSVGPlugin);
  if (window.Flip) gsap.registerPlugin(window.Flip);
  gsap.defaults({ ease: 'power3.out', duration: .8 });

  var mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', function () {
    // ---------- Architectural Hero: Beschriftung zeichnet sich nach dem Wandaufbau
    var ueberlagerung = document.querySelector('.visual-ueberlagerung');
    if (ueberlagerung && window.DrawSVGPlugin) {
      var spaet = ((window.performance && performance.now()) || 0) - start > 1300;
      if (!spaet) {
        var gruppen = ueberlagerung.querySelectorAll('[data-beschriftung]');
        var tl = gsap.timeline({ delay: Math.max(.2, 1.35 - start / 1000) });
        tl.set(ueberlagerung, { opacity: 1 });
        gruppen.forEach(function (g, i) {
          var at = i * .12;
          tl.from(g.querySelectorAll('.vl-punkt, .vl-ring'), { scale: 0, transformOrigin: '50% 50%', duration: .4 }, at)
            .from(g.querySelector('.vl-linie'), { drawSVG: '0%', duration: .7, ease: 'power2.inOut' }, at + .1)
            .from(g.querySelectorAll('.vl-nr, .vl-nr-text, .vl-text'), { autoAlpha: 0, duration: .5 }, at + .55);
        });
      }
      var buehne = document.querySelector('.buehne');
      gsap.to('.buehne-bild', { y: 48, ease: 'none', scrollTrigger: { trigger: buehne, start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.buehne-text', { y: -24, ease: 'none', scrollTrigger: { trigger: buehne, start: 'top top', end: 'bottom top', scrub: true } });
    }

    // ---------- Überschriften: Zeilen aus der Maske (nur unterhalb des Seitenkopfs)
    if (window.SplitText) {
      document.querySelectorAll('main [data-zeilen]:not(h1)').forEach(function (el) {
        window.SplitText.create(el, {
          type: 'lines', mask: 'lines', autoSplit: true, linesClass: 'zeile-split',
          onSplit: function (self) {
            return gsap.from(self.lines, { yPercent: 105, duration: .95, stagger: .08,
              scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
          }
        });
      });
    }

    // ---------- Ruhige Reveals
    var zeigen = gsap.utils.toArray('[data-zeigen]');
    gsap.set(zeigen, { autoAlpha: 0, y: 26 });
    ST.batch(zeigen, {
      start: 'top 90%', once: true,
      onEnter: function (els) { gsap.to(els, { autoAlpha: 1, y: 0, stagger: .08, duration: .8, overwrite: true }); }
    });

    // ---------- Project Reveal: Maske entlang der Bildkante
    gsap.utils.toArray('main > section [data-enthuellen]').forEach(function (el) {
      var bild = el.querySelector('img, svg');
      var tl2 = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 86%', once: true } });
      tl2.fromTo(el, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.2, ease: 'power3.inOut' });
      if (bild) tl2.from(bild, { scale: 1.12, duration: 1.6, ease: 'power2.out' }, 0);
    });

    // ---------- Zeichnungen: Linien ziehen sich nach
    if (window.DrawSVGPlugin) {
      gsap.utils.toArray('main svg.zg').forEach(function (svg) {
        if (svg.closest('.seitenkopf') || svg.closest('.leistungskarte-bild') || svg.closest('[data-netzstory]')) return;
        // Gestrichelte Linien (Route, Fluchtlinien) behalten ihr Muster: einblenden statt nachzeichnen
        var linien = Array.prototype.filter.call(svg.querySelectorAll('[data-linie]'), function (l) { return !gestrichelt(l); });
        var strich = Array.prototype.filter.call(svg.querySelectorAll('[data-linie], .zg-flucht'), gestrichelt);
        if (!linien.length && !strich.length) return;
        var tl4 = gsap.timeline({ scrollTrigger: { trigger: svg, start: 'top 85%', once: true } });
        if (linien.length) tl4.from(linien, { drawSVG: '0%', duration: 1.3, stagger: .05, ease: 'power2.inOut' });
        if (strich.length) tl4.from(strich, { autoAlpha: 0, duration: .8 }, linien.length ? .6 : 0);
      });
    }

    // ---------- Netzwerk: vom Ansprechpartner nach außen
    gsap.utils.toArray('[data-netzwerk] svg').forEach(function (svg) {
      var tl3 = gsap.timeline({ scrollTrigger: { trigger: svg, start: 'top 80%', once: true } });
      tl3.from(svg.querySelectorAll('.nz-knoten--mitte, .nz-knoten--sie'), { autoAlpha: 0, scale: .7, transformOrigin: '50% 50%', duration: .6, stagger: .1 });
      if (window.DrawSVGPlugin) tl3.from(svg.querySelectorAll('.nz-linie--sie, .nz-linie--eigen'), { drawSVG: '0%', duration: .9, stagger: .06, ease: 'power2.inOut' }, .2);
      tl3.from(svg.querySelectorAll('.nz-linie--partner'), { autoAlpha: 0, duration: .8, stagger: .04 }, .5);
      tl3.from(svg.querySelectorAll('.nz-knoten--eigen, .nz-knoten--partner, .nz-knoten--gruppe'), { autoAlpha: 0, duration: .5, stagger: .05 }, .7);
    });

    // ---------- Leitsatz: färbt sich Wort für Wort ein (an den Scroll gekoppelt). Startfarbe #84888D hält auf
    // Kalkweiß 3,2 : 1 – genug für große Schrift, auch bevor gescrollt wurde; Endfarbe ist die eigene Farbe des Worts.
    if (window.SplitText) {
      document.querySelectorAll('[data-wortweise]').forEach(function (el) {
        window.SplitText.create(el, {
          type: 'words', wordsClass: 'wort',
          onSplit: function (self) {
            return gsap.from(self.words, { color: '#84888D', ease: 'none', stagger: .12,
              scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 48%', scrub: .5 } });
          }
        });
      });
    }

    // ---------- Ablauf: Fortschrittslinie über den Schritten
    document.querySelectorAll('[data-schritte]').forEach(function (liste) {
      var linie = document.createElement('span');
      linie.className = 'schritte-fortschritt';
      linie.setAttribute('aria-hidden', 'true');
      liste.appendChild(linie);
      gsap.to(linie, { width: '100%', ease: 'none', scrollTrigger: { trigger: liste, start: 'top 80%', end: 'bottom 55%', scrub: .6 } });
    });

  });

  // ---------- Netzwerk-Geschichte: Schema steht, Schritte ziehen vorbei, das Netz wächst mit dem Scrollen.
  // Drei Lagen: breit nebeneinander, breit über den Schritten (Tablet), schmal über den Schritten (Handy).
  // Zu niedrige Bildschirme und reduzierte Bewegung behalten das vollständige Schema ohne Kopplung.
  document.querySelectorAll('[data-netzstory]').forEach(function (sek) {
    var liste = sek.querySelector('.netzstory-schritte');
    var schritte = Array.prototype.slice.call(sek.querySelectorAll('.netzstory-schritt'));
    var band = sek.querySelector('.netzstory-fortschritt');
    var legende = sek.querySelector('.netzstory-legende');
    var lagen = [
      ['(min-width: 900px) and (prefers-reduced-motion: no-preference)', '.zg--netzwerk-breit', '55%'],
      ['(min-width: 700px) and (max-width: 899px) and (min-height: 700px) and (prefers-reduced-motion: no-preference)', '.zg--netzwerk-breit', '78%'],
      ['(max-width: 699px) and (min-height: 700px) and (prefers-reduced-motion: no-preference)', '.zg--netzwerk-schmal', '78%']
    ];
    lagen.forEach(function (lage) {
      mm.add(lage[0], function () {
        var svg = sek.querySelector(lage[1]);
        if (!svg || !liste) return;
        var q = function (sel) { return svg.querySelectorAll(sel); };
        var linie = lage[2];
        sek.classList.add('netzstory--lebendig');
        // Zeitachse in fünf gleich langen Abschnitten (ein Abschnitt je Schritt). Jeder Aufbau ist in der ersten
        // Hälfte fertig – steht ein Schritt mittig an der Auslöselinie, ist sein Bild vollständig.
        var tl = gsap.timeline({ defaults: { ease: 'power2.out', duration: .35 } });
        // 1 Ihr Vorhaben
        tl.from(q('.nz-knoten--sie'), { autoAlpha: 0, scale: .3, transformOrigin: '50% 50%', ease: 'back.out(2)' }, .05);
        // 2 Ein Ansprechpartner
        if (window.DrawSVGPlugin) tl.from(q('.nz-linie--sie'), { drawSVG: '0%', ease: 'power1.inOut' }, 1);
        else tl.from(q('.nz-linie--sie'), { autoAlpha: 0 }, 1);
        tl.from(q('.nz-knoten--mitte'), { autoAlpha: 0, scale: .5, transformOrigin: '50% 50%', ease: 'back.out(1.6)' }, 1.15);
        // 3 Was wir selbst ausführen
        if (window.DrawSVGPlugin) tl.from(q('.nz-linie--eigen'), { drawSVG: '0%', stagger: .06, duration: .25, ease: 'power1.inOut' }, 2);
        else tl.from(q('.nz-linie--eigen'), { autoAlpha: 0, stagger: .06 }, 2);
        tl.from(q('.nz-knoten--eigen'), { autoAlpha: 0, scale: .4, transformOrigin: '50% 50%', stagger: .06, duration: .25, ease: 'back.out(2)' }, 2.15);
        // 4 Wo Fachbetriebe dazukommen
        tl.from(q('.nz-linie--partner'), { autoAlpha: 0, stagger: .02, duration: .25 }, 3)
          .from(q('.nz-knoten--partner, .nz-knoten--gruppe'), { autoAlpha: 0, y: 10, stagger: .02, duration: .25 }, 3.1);
        // 5 Wer Ihr Vertragspartner ist: eigene Leistung leuchtet gelb, die Legende erklärt die Linien
        tl.to(q('.nz-linie--eigen'), { stroke: '#FFC93C', duration: .3 }, 4)
          .to(q('.nz-knoten--eigen circle'), { stroke: '#FFC93C', fill: '#FFC93C', duration: .3 }, 4);
        if (legende) tl.from(legende, { autoAlpha: 0, y: 12, duration: .3 }, 4.1);
        tl.to({}, { duration: .01 }, 4.99);
        ST.create({ trigger: liste, start: 'top ' + linie, end: 'bottom ' + linie, scrub: .7, animation: tl });
        if (band) gsap.fromTo(band, { scaleY: 0 }, { scaleY: 1, ease: 'none',
          scrollTrigger: { trigger: liste, start: 'top ' + linie, end: 'bottom ' + linie, scrub: .3 } });
        schritte.forEach(function (s) {
          ST.create({ trigger: s, start: 'top ' + linie, end: 'bottom ' + linie, toggleClass: { targets: s, className: 'aktiv' } });
        });
        return function () {
          sek.classList.remove('netzstory--lebendig');
          schritte.forEach(function (s) { s.classList.remove('aktiv'); });
        };
      });
    });
  });

  // ---------- Tiefe: Maus-Parallax im Seitenkopf und auf Leistungskarten
  // Nur mit Maus (hover + feiner Zeiger) und erlaubter Bewegung. Es läuft nichts dauerhaft: Jede Bewegung der Maus
  // setzt ein kurzes Nachgleiten (quickTo) in Gang, ruht die Maus, ruht alles. Verschoben werden nur transform-Werte
  // weniger Elemente hinter dem Inhalt; Texte und Formularfelder bewegen sich nie.
  mm.add('(prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine)', function () {
    var aufraeumen = [];
    var folgen = function (el, eigenschaft, dauer) { return gsap.quickTo(el, eigenschaft, { duration: dauer, ease: 'power3.out' }); };

    document.querySelectorAll('[data-tiefe]').forEach(function (tiefe) {
      var kopf = tiefe.parentElement;
      var ebenen = Array.prototype.map.call(tiefe.querySelectorAll('[data-tiefe-ebene]'), function (el) {
        return { f: parseFloat(el.getAttribute('data-tiefe-ebene')) || 0, x: folgen(el, 'x', 1.6), y: folgen(el, 'y', 1.6) };
      });
      var sichtbar = true;
      var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (e) { sichtbar = e[0].isIntersecting; }) : null;
      if (io) io.observe(kopf);
      var bewegen = function (e) {
        if (!sichtbar || e.pointerType !== 'mouse') return;
        var nx = e.clientX / window.innerWidth - .5, ny = e.clientY / window.innerHeight - .5;
        ebenen.forEach(function (l) { l.x(nx * 44 * l.f); l.y(ny * 28 * l.f); });
      };
      var zurueck = function () { ebenen.forEach(function (l) { l.x(0); l.y(0); }); };
      window.addEventListener('pointermove', bewegen, { passive: true });
      document.documentElement.addEventListener('pointerleave', zurueck);
      aufraeumen.push(function () {
        window.removeEventListener('pointermove', bewegen);
        document.documentElement.removeEventListener('pointerleave', zurueck);
        if (io) io.disconnect();
        gsap.set(tiefe.querySelectorAll('[data-tiefe-ebene]'), { clearProps: 'transform' });
      });
    });

    // Leistungskarten: Nur die Bildfläche neigt sich (höchstens 3,5°), das Bild gleitet leicht dagegen – Titel,
    // Text und Link bleiben ruhig. Der Kartenlink liegt weiter über allem und bleibt klickbar.
    document.querySelectorAll('.leistungskarte').forEach(function (karte) {
      var flaeche = karte.querySelector('.leistungskarte-bild');
      var bild = flaeche && flaeche.querySelector('img');
      if (!bild) return;
      gsap.set(flaeche, { transformPerspective: 900 });
      var rx = folgen(flaeche, 'rotationX', .7), ry = folgen(flaeche, 'rotationY', .7), bx = folgen(bild, 'x', .9), by = folgen(bild, 'y', .9);
      var drin = function (e) {
        if (e.pointerType !== 'mouse') return;
        var r = karte.getBoundingClientRect();
        var nx = Math.max(-.5, Math.min(.5, (e.clientX - r.left) / r.width - .5));
        var ny = Math.max(-.5, Math.min(.5, (e.clientY - r.top) / r.height - .5));
        ry(nx * 7); rx(-ny * 7); bx(-nx * 16); by(-ny * 16);
      };
      var rein = function (e) {
        if (e.pointerType !== 'mouse') return;
        karte.classList.add('in-tiefe');
        gsap.to(bild, { scale: 1.07, duration: .8, overwrite: 'auto' });
      };
      var raus = function () {
        karte.classList.remove('in-tiefe');
        rx(0); ry(0); bx(0); by(0);
        gsap.to(bild, { scale: 1, duration: .8, overwrite: 'auto' });
      };
      karte.addEventListener('pointerenter', rein);
      karte.addEventListener('pointermove', drin, { passive: true });
      karte.addEventListener('pointerleave', raus);
      aufraeumen.push(function () {
        karte.removeEventListener('pointerenter', rein);
        karte.removeEventListener('pointermove', drin);
        karte.removeEventListener('pointerleave', raus);
        karte.classList.remove('in-tiefe');
        gsap.set([flaeche, bild], { clearProps: 'transform' });
      });
    });

    return function () { aufraeumen.forEach(function (f) { f(); }); };
  });

  // ---------- Wandaufbau: Scroll-Kopplung nur auf großen Bildschirmen mit erlaubter Bewegung
  mm.add('(min-width: 1000px) and (min-height: 700px) and (prefers-reduced-motion: no-preference)', function () {
    wand.forEach(function (w) { w.scrollKoppeln(); });
    return function () { wand.forEach(function (w) { w.scrollLoesen(); }); };
  });

  // ---------- Flip für den Projektfilter (site.js ruft window.gashiniUmordnen auf)
  if (window.Flip && bewegt) {
    window.gashiniUmordnen = function (karten, sichtbar) {
      var zustand = window.Flip.getState(karten);
      karten.forEach(function (k) { k.hidden = false; k.style.display = sichtbar(k) ? '' : 'none'; });
      window.Flip.from(zustand, {
        duration: .6, ease: 'power3.inOut', absolute: true, scale: true,
        onEnter: function (els) { return gsap.fromTo(els, { autoAlpha: 0, scale: .94 }, { autoAlpha: 1, scale: 1, duration: .45 }); },
        onLeave: function (els) { return gsap.to(els, { autoAlpha: 0, scale: .94, duration: .3 }); }
      });
    };
  }

  html.classList.add('bewegung-bereit');
  window.addEventListener('load', function () { ST.refresh(); });

  function gestrichelt(el) {
    var d = window.getComputedStyle(el).strokeDasharray;
    return !!d && d !== 'none';
  }

  /* ======================================================================= Wandaufbau */
  function wandaufbau(sek) {
    var knoepfe = Array.prototype.slice.call(sek.querySelectorAll('.wandaufbau-schritt'));
    var schnittKnopf = sek.querySelector('[data-schnitt]');
    var ansage = sek.querySelector('[data-wand-ansage]');
    var buehne = sek.querySelector('[data-wand-buehne]');
    var modul = sek.getAttribute('data-modul');
    var raster = sek.querySelector('.wandaufbau-raster');
    var steuerung = null, kopplung = null, schritt = 4, gebaut = false;

    if (schnittKnopf) schnittKnopf.hidden = true;   // nur mit 3D sinnvoll

    function anzeigen(n, ansagen) {
      schritt = n;
      sek.setAttribute('data-schritt', String(n));
      knoepfe.forEach(function (k) { k.setAttribute('aria-pressed', String(Number(k.getAttribute('data-schritt')) === n)); });
      if (ansagen && ansage) {
        var k = knoepfe[n - 1];
        ansage.textContent = 'Schritt ' + n + ' von 4: ' + k.querySelector('.titel').textContent;
      }
    }

    knoepfe.forEach(function (k) {
      k.addEventListener('click', function () {
        var n = Number(k.getAttribute('data-schritt'));
        if (kopplung) {
          var ziel = kopplung.start + (kopplung.end - kopplung.start) * Math.max(0, (n - .15 - .3) / 3.85);
          window.scrollTo({ top: ziel, behavior: bewegt ? 'smooth' : 'auto' });
          anzeigen(n, true);
          return;
        }
        anzeigen(n, true);
        if (steuerung) steuerung.schritt(n);
      });
    });

    if (schnittKnopf) schnittKnopf.addEventListener('click', function () {
      var an = schnittKnopf.getAttribute('aria-pressed') !== 'true';
      schnittKnopf.setAttribute('aria-pressed', String(an));
      if (steuerung) steuerung.schnitt(an);
      if (ansage) ansage.textContent = an ? 'Schnittansicht: Schichten gestaffelt' : 'Schnittansicht aus';
    });

    // Three.js erst laden, wenn der Abschnitt in die Nähe kommt – und nur mit WebGL
    var webgl = (function () {
      try { var c = document.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl'))); }
      catch (e) { return false; }
    })();
    if (webgl && modul && skriptUrl && 'IntersectionObserver' in window && typeof Promise !== 'undefined') {
      var io = new IntersectionObserver(function (eintraege) {
        if (!eintraege[0].isIntersecting) return;
        io.disconnect();
        var url = new URL(modul, document.baseURI).href;
        import(url).then(function (m) {
          steuerung = m.starte(buehne, {
            reduziert: !bewegt, start: kopplung ? Math.min(4, .3 + kopplung.progress * 3.85) : (bewegt ? 0 : schritt),
            beiFehler: function () { steuerung = null; sek.classList.remove('ist-3d'); if (schnittKnopf) schnittKnopf.hidden = true; }
          });
          sek.classList.add('ist-3d');
          if (schnittKnopf) schnittKnopf.hidden = false;
          if (!kopplung) {
            if (!bewegt) steuerung.schritt(schritt, true);
            else baueAuf();
          }
        }).catch(function () { /* Zeichnung bleibt stehen */ });
      }, { rootMargin: '600px 0px' });
      io.observe(sek);
    }

    // Beim ersten Erscheinen (ohne Scroll-Kopplung) baut sich die Wand einmal auf
    function baueAuf() {
      if (gebaut || !steuerung) return;
      var los = function () { gebaut = true; anzeigen(4, false); steuerung.schritt(4); };
      if (!('IntersectionObserver' in window)) return los();
      var io2 = new IntersectionObserver(function (e) { if (e[0].intersectionRatio > .35) { io2.disconnect(); los(); } }, { threshold: [0, .35, .6] });
      io2.observe(buehne);
    }

    return {
      scrollKoppeln: function () {
        if (!window.ScrollTrigger || !raster) return;
        kopplung = window.ScrollTrigger.create({
          trigger: raster, start: 'center center', end: '+=1400', pin: true, scrub: true,
          onUpdate: function (self) {
            var p = Math.min(4, .3 + self.progress * 3.85);
            if (steuerung) steuerung.fortschritt(p);
            var n = Math.max(1, Math.min(4, Math.ceil(p - .02)));
            if (n !== schritt) anzeigen(n, false);
          }
        });
        if (steuerung) steuerung.fortschritt(Math.min(4, .3 + kopplung.progress * 3.85));
      },
      scrollLoesen: function () {
        if (kopplung) { kopplung.kill(); kopplung = null; }
        if (steuerung) steuerung.schritt(schritt);
      }
    };
  }
})();
