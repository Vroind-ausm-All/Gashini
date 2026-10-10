#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gashini Dienstleistungen – Seitengenerator

Liest ausschließlich:
  src/seiten/*.html     Seiteninhalte (HTML-Fragmente mit Kopfdaten)
  src/assets/           Stylesheet, Skripte, Schriften, Bilder
  src/api/              Formular-Backend (PHP)
  src/server/           Serverkonfiguration (.htaccess)
  data/projekte.json    Projektgalerie
  data/faq.json         Häufige Fragen
  brand/*.svg           Logo, Signet, Favicon

Schreibt ausschließlich nach web/ – das Verzeichnis wird bei jedem Lauf
vollständig neu erzeugt. Änderungen direkt in web/ gehen verloren.

Umgebungsvariablen:
  LINKSTIL=dateien   Links auf …/index.html statt …/  (für Vorschauumgebungen
                     ohne Verzeichnis-Index, z. B. die Artefakt-Vorschau)
  ENTWUERFE=1        Projekte im Status "entwurf" mit deutlicher Kennzeichnung
                     ausgeben – nur für interne Vorschauen, nie für Produktion
  AUSGABE=<pfad>     anderes Zielverzeichnis statt web/ (für Tests und Vorschauen)

Nur Python-Standardbibliothek. Ausgabe ist bei gleicher Eingabe byte-identisch.
"""
import html, io, json, os, re, shutil, struct, sys

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(WURZEL, "src")
OUT = os.path.abspath(os.environ.get("AUSGABE", os.path.join(WURZEL, "web")))
LINKSTIL = os.environ.get("LINKSTIL", "sauber")
ENTWUERFE = os.environ.get("ENTWUERFE") == "1"

KATEGORIEN = {
    "trockenbau": "Trockenbau & Innenausbau",
    "hausmeisterservice": "Hausmeisterservice",
    "reparatur": "Reparatur & Instandhaltung",
    "koordination": "Koordination",
}
AUSFUEHRUNG = {
    "eigener-betrieb": "Gashini Dienstleistungen",
    "partner": "Partnerbetrieb, koordiniert durch Gashini",
    "gemeinsam": "Gashini mit Partnerbetrieb",
}
NAV = [("leistungen/", "Leistungen"), ("projekte/", "Projekte"),
       ("ueber-uns/", "Über uns"), ("kontakt/", "Kontakt")]

warnungen = []

def lesen(pfad):
    with io.open(pfad, encoding="utf-8") as f:
        return f.read()

def schreiben(pfad, text):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def esc(s):
    return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ Pfade
def tiefe(seitenpfad):
    if seitenpfad.endswith(".html"):
        return seitenpfad.count("/")
    return seitenpfad.count("/")

def rel(von, ziel):
    """Relativer Link von Seite `von` (z. B. 'leistungen/trockenbau/') zu `ziel`."""
    anker = ""
    if "#" in ziel:
        ziel, anker = ziel.split("#", 1)
        anker = "#" + anker
    praefix = "../" * tiefe(von)
    ist_verzeichnis = ziel == "" or ziel.endswith("/")
    if LINKSTIL == "dateien" and ist_verzeichnis:
        ziel = ziel + "index.html"
    ergebnis = praefix + ziel
    if ergebnis == "":
        ergebnis = "./"
    return ergebnis + anker

def links_aufloesen(text, von):
    return re.sub(r'(href|src|action|data-gross)="@/([^"]*)"',
                  lambda m: '%s="%s"' % (m.group(1), rel(von, m.group(2))), text)

# ------------------------------------------------------------------ Bildgröße (ohne Fremdbibliothek)
def bildmasse(pfad):
    with open(pfad, "rb") as f:
        kopf = f.read(64 * 1024)
    if pfad.endswith(".svg"):
        m = re.search(rb'viewBox="0 0 ([\d.]+) ([\d.]+)"', kopf)
        return (int(float(m.group(1))), int(float(m.group(2)))) if m else (1600, 1200)
    if kopf[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", kopf[16:24])
    if kopf[:4] == b"RIFF" and kopf[8:12] == b"WEBP":
        art = kopf[12:16]
        if art == b"VP8X":
            w = 1 + int.from_bytes(kopf[24:27], "little"); h = 1 + int.from_bytes(kopf[27:30], "little")
            return w, h
        if art == b"VP8 ":
            w, h = struct.unpack("<HH", kopf[26:30]); return w & 0x3FFF, h & 0x3FFF
        if art == b"VP8L":
            b = kopf[21:25]
            w = 1 + (((b[1] & 0x3F) << 8) | b[0]); h = 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
            return w, h
    if kopf[:2] == b"\xff\xd8":
        i = 2
        while i < len(kopf) - 9:
            if kopf[i] != 0xFF: i += 1; continue
            marker = kopf[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", kopf[i + 5:i + 9]); return w, h
            i += 2 + struct.unpack(">H", kopf[i + 2:i + 4])[0]
    raise ValueError("Bildformat nicht erkannt: " + pfad)

def bild_html(von, datei, alt, klasse="", laden="lazy", groessen="(min-width: 900px) 50vw, 100vw"):
    """<img> mit festen Maßen; nutzt vorhandene Varianten name-640/-1280/-1920.webp als srcset."""
    quelle = os.path.join(SRC, "assets", "bilder", datei)
    w, h = bildmasse(quelle)
    basis, endung = os.path.splitext(datei)
    varianten = []
    for breite in (640, 1280, 1920):
        v = "%s-%d.webp" % (basis, breite)
        if os.path.exists(os.path.join(SRC, "assets", "bilder", v)):
            varianten.append("@/assets/bilder/%s %dw" % (v, breite))
    srcset = ' srcset="%s" sizes="%s"' % (", ".join(varianten), groessen) if varianten else ""
    return ('<img src="@/assets/bilder/%s"%s width="%d" height="%d" alt="%s" loading="%s" decoding="async"%s>'
            % (esc(datei), srcset, w, h, esc(alt), laden, ' class="%s"' % klasse if klasse else ""))

# ------------------------------------------------------------------ Daten
def projekte_laden():
    daten = json.loads(lesen(os.path.join(WURZEL, "data", "projekte.json")))
    ergebnis = []
    for p in daten.get("projekte", []):
        bilder = p.get("bilder", [])
        rechte_ok = all(b.get("rechte", {}).get("freigabe_kunde") is True and
                        b.get("rechte", {}).get("ki_generiert") is False for b in bilder)
        freigegeben = (p.get("status") == "freigegeben" and p.get("freigabe", {}).get("kunde") is True
                       and rechte_ok and len(bilder) > 0)
        if p.get("status") == "freigegeben" and not freigegeben:
            warnungen.append("Projekt %s ist als freigegeben markiert, aber Kunden- oder Bildfreigabe fehlt – nicht veröffentlicht." % p.get("id"))
        if freigegeben or (ENTWUERFE and p.get("status") == "entwurf"):
            p["_entwurf"] = not freigegeben
            ergebnis.append(p)
    ergebnis.sort(key=lambda p: (p.get("datum", ""), p.get("id", "")), reverse=True)
    return ergebnis

def faq_laden():
    return json.loads(lesen(os.path.join(WURZEL, "data", "faq.json")))["fragen"]

PROJEKTE = projekte_laden()
FAQ = faq_laden()

# ------------------------------------------------------------------ Bausteine
def zeichnung():
    """Technische Ansicht einer Metallständerwand. Maße in mm, Achsmaß 625."""
    x0, y0, breite, hoehe = 80, 50, 360, 300   # Zeichenfläche
    achs = breite / 4                         # 4 Felder à 625 mm
    teile = []
    # Deckenlinie und Boden
    teile.append('<line class="zg-linie" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0 - 14, y0, x0 + breite + 30, y0))
    teile.append('<line class="zg-linie" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0 - 14, y0 + hoehe, x0 + breite + 30, y0 + hoehe))
    for i in range(0, 12):
        xs = x0 - 6 + i * 34
        teile.append('<line class="zg-duenn" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (xs, y0 + hoehe + 2, xs - 8, y0 + hoehe + 10))
    # UW-Profile oben und unten
    teile.append('<rect class="zg-profil" x="%d" y="%d" width="%d" height="7"/>' % (x0, y0, breite))
    teile.append('<rect class="zg-profil" x="%d" y="%d" width="%d" height="7"/>' % (x0, y0 + hoehe - 7, breite))
    # Dämmung im offenen Bereich (rechte Hälfte)
    teile.append('<defs><pattern id="daemmung" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
                 '<line x1="0" y1="0" x2="0" y2="10" stroke="#9C988F" stroke-width=".7"/></pattern></defs>')
    teile.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="url(#daemmung)" opacity=".55"/>'
                 % (x0 + 2 * achs + 6, y0 + 7, achs * 2 - 12, hoehe - 14))
    # CW-Ständer
    for i in range(5):
        x = x0 + i * achs
        teile.append('<rect class="zg-profil zg-zeichnen" x="%.1f" y="%d" width="6" height="%d"/>' % (x - 3, y0 + 7, hoehe - 14))
    # Beplankung: eine Platte 1250 mm über die linken zwei Felder, rechts offen mit Dämmung
    teile.append('<rect class="zg-platte" x="%.1f" y="%d" width="%.1f" height="%d"/>' % (x0 + .5, y0 + 9, achs * 2 - 1, hoehe - 18))
    # Schrauben auf der Platte (Abstand 250 mm)
    for i in range(3):
        x = x0 + i * achs
        for j in range(1, 11):
            teile.append('<circle cx="%.1f" cy="%.1f" r="1.1" fill="#6B6863"/>' % (x + (2.4 if i == 0 else -2.4 if i == 2 else 0), y0 + 9 + j * (hoehe - 18) / 11))
    # Maßkette unten (Achsmaß 625)
    ym = y0 + hoehe + 34
    teile.append('<line class="zg-mass zg-zeichnen zg-spaet" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0, ym, x0 + breite, ym))
    for i in range(5):
        x = x0 + i * achs
        teile.append('<line class="zg-mass" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, ym - 6, x, ym + 6))
        teile.append('<line class="zg-mass" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x - 4, ym + 4, x + 4, ym - 4))
    for i in range(4):
        x = x0 + i * achs + achs / 2
        klasse = "zg-text zg-text--akzent" if i == 0 else "zg-text"
        teile.append('<text class="%s zg-einblenden" x="%.1f" y="%d" text-anchor="middle">625</text>' % (klasse, x, ym - 8))
    teile.append('<line class="zg-mass zg-mass--akzent" x1="%d" y1="%d" x2="%.1f" y2="%d"/>' % (x0, ym, x0 + achs, ym))
    # Höhenmaß links
    xh = x0 - 30
    teile.append('<line class="zg-mass zg-zeichnen zg-spaet" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (xh, y0, xh, y0 + hoehe))
    teile.append('<line class="zg-mass" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (xh - 4, y0 + 4, xh + 4, y0 - 4))
    teile.append('<line class="zg-mass" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (xh - 4, y0 + hoehe + 4, xh + 4, y0 + hoehe - 4))
    teile.append('<text class="zg-text zg-einblenden" x="%d" y="%d" transform="rotate(-90 %d %d)" text-anchor="middle">2750</text>'
                 % (xh - 10, y0 + hoehe / 2, xh - 10, y0 + hoehe / 2))
    # Beschriftungen mit Hinweislinien
    def notiz(x1, y1, x2, y2, text, anker="start"):
        teile.append('<polyline class="zg-duenn zg-einblenden" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
                     % (x1, y1, x2, y2, x2 + (34 if anker == "start" else -34), y2))
        teile.append('<circle class="zg-einblenden" cx="%.1f" cy="%.1f" r="2" fill="#0E0E0E"/>' % (x1, y1))
        teile.append('<text class="zg-text zg-einblenden" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                     % (x2 + (38 if anker == "start" else -38), y2 + 4, anker, text))
    notiz(x0 + 3 * achs, y0 + 3.5, x0 + 3 * achs + 20, y0 - 22, "UW 75")
    notiz(x0 + 2 * achs + 2, y0 + 120, x0 + 2 * achs + 40, y0 + 92, "CW 75")
    notiz(x0 + 3.3 * achs, y0 + 200, x0 + 3.3 * achs + 18, y0 + 176, "Mineralwolle 60")
    notiz(x0 + achs * .55, y0 + 70, x0 + achs * .55 + 14, y0 + 44, "GKB 12,5")
    svg = ('<svg viewBox="0 0 540 430" role="img" aria-labelledby="zg-titel zg-beschr" xmlns="http://www.w3.org/2000/svg">'
           '<title id="zg-titel">Ansicht einer Metallständerwand</title>'
           '<desc id="zg-beschr">Schematische Zeichnung: UW-Profile an Decke und Boden, CW-Ständer im Achsabstand von 625 Millimetern, '
           'links mit Gipskartonplatten 12,5 Millimeter beplankt, rechts offen mit Mineralwolle. Raumhöhe 2750 Millimeter.</desc>'
           + "".join(teile) + "</svg>")
    return ('<figure class="zeichnung"><div class="zeichnung-flaeche">%s</div>'
            '<figcaption>Abb. — Metallständerwand, Ansicht, Maße in mm. Schematische Darstellung, kein Projektfoto.</figcaption></figure>' % svg)

def projektkarte(p, von, ueberschrift="h3", laden="lazy"):
    titelbild = next((b for b in p["bilder"] if b.get("rolle") == "titel"), p["bilder"][0])
    meta = [KATEGORIEN.get(p["kategorie"], p["kategorie"])]
    if p.get("region"): meta.append(p["region"])
    abzeichen = '<span class="abzeichen">Beispieldaten – kein echtes Projekt</span>' if p["_entwurf"] else ""
    return ('<article class="projekt" data-kategorie="%s">'
            '<div class="projekt-bild">%s%s</div>'
            '<p class="projekt-meta">%s</p>'
            '<%s><a href="@/projekte/%s/">%s</a></%s>'
            '<p>%s</p></article>'
            % (esc(p["kategorie"]), abzeichen, bild_html(von, titelbild["datei"], titelbild["alt"], laden=laden,
                                                       groessen="(min-width: 1000px) 33vw, (min-width: 640px) 50vw, 100vw"),
               "".join("<span>%s</span>" % esc(m) for m in meta),
               ueberschrift, esc(p["slug"]), esc(p["titel"]), ueberschrift, esc(p["kurztext"])))

def leerzustand(von, ebene="h3"):
    return ('<div class="leerzustand"><div><p class="label">Projektgalerie</p>'
            '<{e}>Die ersten Projekte werden gerade dokumentiert.</{e}></div>'
            '<div><p>Wir zeigen hier ausschließlich Arbeiten, die wir selbst fotografiert haben und deren Veröffentlichung '
            'die Auftraggeber freigegeben haben. Bis dahin erzählen wir Ihnen gern am Telefon, woran wir zuletzt gearbeitet haben.</p>'
            '<p class="leerzustand-aktion"><a class="textlink" href="@/kontakt/">Vorhaben besprechen <span class="pfeil" aria-hidden="true">→</span></a></p></div></div>'
            ).format(e=ebene)

def projekte_vorschau(von, anzahl=3):
    if not PROJEKTE:
        return leerzustand(von)
    karten = "".join(projektkarte(p, von) for p in PROJEKTE[:anzahl])
    return '<div class="projektraster">%s</div>' % karten

def projekte_galerie(von):
    if not PROJEKTE:
        return leerzustand(von, "h2")
    teile = []
    kategorien = sorted({p["kategorie"] for p in PROJEKTE}, key=lambda k: list(KATEGORIEN).index(k) if k in KATEGORIEN else 99)
    if len(PROJEKTE) >= 6 and len(kategorien) > 1:
        optionen = ['<label><input type="radio" name="kategorie" value="alle" checked><span>Alle</span></label>']
        for k in kategorien:
            optionen.append('<label><input type="radio" name="kategorie" value="%s"><span>%s</span></label>' % (esc(k), esc(KATEGORIEN.get(k, k))))
        teile.append('<fieldset class="filter"><legend class="label">Nach Leistung filtern</legend>%s</fieldset>'
                     '<p id="filter-ansage" class="nur-screenreader" aria-live="polite"></p>' % "".join(optionen))
    teile.append('<div class="projektraster">%s</div>' % "".join(projektkarte(p, von, ueberschrift="h2") for p in PROJEKTE))
    return "".join(teile)

def faq_html(kategorie=None):
    fragen = [f for f in FAQ if kategorie is None or kategorie in f.get("seiten", [])]
    return '<div class="fragen">%s</div>' % "".join(
        '<details id="%s"><summary>%s</summary><div class="antwort"><p>%s</p></div></details>'
        % (esc(f["id"]), esc(f["frage"]), f["antwort"]) for f in fragen)

def faq_jsonld(kategorie=None):
    fragen = [f for f in FAQ if kategorie is None or kategorie in f.get("seiten", [])]
    daten = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["frage"],
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["antwort"])}} for f in fragen]}
    return '<script type="application/ld+json">%s</script>' % json.dumps(daten, ensure_ascii=False)

def ablauf_html():
    schritte = [
        ("Anfrage senden", "Per Formular, Telefon oder E-Mail. Ein paar Sätze zum Vorhaben genügen – Fotos helfen, sind aber kein Muss."),
        ("Vorhaben besprechen", "Wir klären, was genau ansteht, und sehen uns die Situation bei Bedarf vor Ort an."),
        ("Angebot abstimmen", "Sie erhalten ein Angebot mit den vereinbarten Arbeiten. Wenn ein Partnerbetrieb beteiligt ist, steht das darin."),
        ("Umsetzen und abschließen", "Wir führen die Arbeiten aus, stimmen Termine mit Ihnen ab und gehen das Ergebnis gemeinsam durch."),
    ]
    return '<ol class="schritte">%s</ol>' % "".join('<li><h3>%s</h3><p>%s</p></li>' % s for s in schritte)

def abschluss_html(titel="Was steht bei Ihnen an?", text="Erzählen Sie uns von Ihrem Vorhaben – auch wenn es nur eine kleine Arbeit ist."):
    return ('<section class="abschluss" aria-labelledby="abschluss-titel"><div class="rahmen">'
            '<p class="label">Kontakt</p><h2 id="abschluss-titel">%s</h2><p class="einleitung">%s</p>'
            '<div class="knopf-reihe"><a class="knopf knopf--primaer" href="@/kontakt/">Unverbindlich anfragen <span class="pfeil" aria-hidden="true">→</span></a></div>'
            '<p class="abschluss-kontakt"><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></p>'
            '</div></section>' % (titel, text))

def kontaktformular():
    leistungen = ["Trockenbau & Innenausbau", "Hausmeisterservice", "Reparatur & Instandhaltung", "Mehrere Arbeiten / noch unklar"]
    quellen = ["Google-Suche", "Google-Profil / Karte", "MyHammer", "Empfehlung", "Fahrzeug oder Flyer", "Sonstiges"]
    opt = lambda liste: "".join('<option>%s</option>' % esc(x) for x in liste)
    return ('''<form class="formular" action="@/api/anfrage.php" method="post" data-anfrage novalidate>
  <div class="formular-status" role="alert" tabindex="-1"></div>
  <div class="feld">
    <label for="f-name">Name</label>
    <input id="f-name" name="name" type="text" autocomplete="name" maxlength="100" required aria-describedby="f-name-fehler">
    <p class="fehlertext" id="f-name-fehler" data-fehler-fuer="name"></p>
  </div>
  <fieldset class="feldgruppe">
    <legend>Wie erreichen wir Sie? <span class="gedaempft">Mindestens eine Angabe</span></legend>
    <div class="formular-reihe formular-reihe--zwei">
      <div class="feld">
        <label for="f-email">E-Mail</label>
        <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" maxlength="254" aria-describedby="f-email-fehler">
        <p class="fehlertext" id="f-email-fehler" data-fehler-fuer="email"></p>
      </div>
      <div class="feld">
        <label for="f-telefon">Telefon</label>
        <input id="f-telefon" name="telefon" type="tel" autocomplete="tel" inputmode="tel" maxlength="40" aria-describedby="f-telefon-fehler">
        <p class="fehlertext" id="f-telefon-fehler" data-fehler-fuer="telefon"></p>
      </div>
    </div>
  </fieldset>
  <div class="feld">
    <label for="f-leistung">Worum geht es?</label>
    <select id="f-leistung" name="leistung" required aria-describedby="f-leistung-fehler">
      <option value="">Bitte auswählen</option>%s
    </select>
    <p class="fehlertext" id="f-leistung-fehler" data-fehler-fuer="leistung"></p>
  </div>
  <div class="feld">
    <label for="f-nachricht">Ihr Vorhaben</label>
    <p class="hilfe" id="f-nachricht-hilfe">Was soll gemacht werden, wo, ungefähr in welchem Umfang? Stichworte reichen.</p>
    <textarea id="f-nachricht" name="nachricht" required minlength="10" maxlength="4000" aria-describedby="f-nachricht-hilfe f-nachricht-fehler"></textarea>
    <p class="fehlertext" id="f-nachricht-fehler" data-fehler-fuer="nachricht"></p>
  </div>
  <div class="formular-reihe formular-reihe--zwei">
    <div class="feld">
      <label for="f-ort">PLZ oder Ort<span class="optional">optional</span></label>
      <input id="f-ort" name="ort" type="text" autocomplete="postal-code" maxlength="100" aria-describedby="f-ort-fehler">
      <p class="fehlertext" id="f-ort-fehler" data-fehler-fuer="ort"></p>
    </div>
    <div class="feld">
      <label for="f-zeitraum">Gewünschter Zeitraum<span class="optional">optional</span></label>
      <input id="f-zeitraum" name="zeitraum" type="text" maxlength="100" placeholder="z. B. im März, flexibel" aria-describedby="f-zeitraum-fehler">
      <p class="fehlertext" id="f-zeitraum-fehler" data-fehler-fuer="zeitraum"></p>
    </div>
  </div>
  <div class="feld">
    <label for="f-quelle">Wie sind Sie auf uns aufmerksam geworden?<span class="optional">optional</span></label>
    <select id="f-quelle" name="quelle"><option value="">Keine Angabe</option>%s</select>
  </div>
  <div class="honig" aria-hidden="true">
    <label for="f-webseite">Bitte dieses Feld leer lassen</label>
    <input id="f-webseite" name="webseite" type="text" tabindex="-1" autocomplete="off">
  </div>
  <input type="hidden" name="ausfuellzeit" value="">
  <p class="datenschutz-hinweis">Wir verwenden Ihre Angaben ausschließlich, um Ihre Anfrage zu beantworten. Details, Speicherdauer und Ihre Rechte stehen in der <a href="@/datenschutz/#anfragen">Datenschutzerklärung</a>.</p>
  <div><button class="knopf knopf--primaer" type="submit"><span class="laedt" aria-hidden="true"></span><span class="text">Anfrage senden</span> <span class="pfeil" aria-hidden="true">→</span></button></div>
</form>''' % (opt(leistungen), opt(quellen)))

def kontaktwege():
    return ('<ul class="kontaktwege">'
            '<li><span class="art">Telefon</span><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a><br><span class="gedaempft mono">{{TELEFONZEITEN}}</span></li>'
            '<li><span class="art">E-Mail</span><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>'
            '<!--opt:WHATSAPP--><li><span class="art">WhatsApp</span><a href="https://wa.me/{{WHATSAPP}}" rel="noopener">Nachricht schreiben</a>'
            '<br><span class="gedaempft mono">Ihre Nachricht wird über WhatsApp (Meta) übertragen.</span></li><!--/opt:WHATSAPP-->'
            '<li><span class="art">Anschrift</span><span>{{STRASSE}}<br>{{PLZ_ORT}}</span></li>'
            '</ul>')

BAUSTEINE = {
    "zeichnung": lambda von, a: zeichnung(),
    "projekte-vorschau": lambda von, a: projekte_vorschau(von),
    "projekte-galerie": lambda von, a: projekte_galerie(von),
    "faq": lambda von, a: faq_html(a.get("seite")),
    "ablauf": lambda von, a: ablauf_html(),
    "abschluss": lambda von, a: abschluss_html(**a) if a else abschluss_html(),
    "kontaktformular": lambda von, a: kontaktformular(),
    "kontaktwege": lambda von, a: kontaktwege(),
}

def bausteine_einsetzen(text, von):
    def ersetzen(m):
        name, rest = m.group(1), m.group(2) or ""
        args = dict(re.findall(r'(\w+)="([^"]*)"', rest))
        if name not in BAUSTEINE:
            raise SystemExit("Unbekannter Baustein [[%s]] in Seite %s" % (name, von))
        return BAUSTEINE[name](von, args)
    return re.sub(r"\[\[([\w-]+)((?:\s+\w+=\"[^\"]*\")*)\s*\]\]", ersetzen, text)

# ------------------------------------------------------------------ Seitengerüst
def kopfbereich(aktiv):
    punkte = "".join('<li><a href="@/%s"%s>%s</a></li>' % (z, ' aria-current="page"' if z == aktiv else "", t) for z, t in NAV)
    return '''<a class="sprunglink" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf">
  <div class="rahmen kopf-innen">
    <a class="marke" href="@/" aria-label="Gashini Dienstleistungen – Startseite"><img src="@/assets/marke/logo.svg" width="254" height="80" alt=""></a>
    <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="hauptnav"><span class="striche" aria-hidden="true"></span><span class="text">Menü</span></button>
    <nav class="hauptnav" id="hauptnav" aria-label="Hauptnavigation">
      <ul>%s</ul>
      <div class="hauptnav-fuss">
        <a class="knopf knopf--primaer" href="@/kontakt/">Projekt anfragen <span class="pfeil" aria-hidden="true">→</span></a>
        <a class="knopf knopf--sekundaer" href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a>
      </div>
    </nav>
    <div class="kopf-aktion">
      <a class="kopf-telefon" href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a>
      <a class="knopf knopf--primaer" href="@/kontakt/">Projekt anfragen</a>
    </div>
  </div>
</header>''' % punkte

FUSS = '''<footer class="fuss">
  <div class="rahmen">
    <div class="fuss-raster">
      <div class="fuss-marke">
        <img src="@/assets/marke/logo-invers.svg" width="254" height="80" alt="Gashini Dienstleistungen">
        <p>Trockenbau, Hausmeisterservice und Arbeiten rund um Ihre Immobilie – persönlich betreut, bei Bedarf mit Partnerbetrieben abgestimmt.</p>
      </div>
      <div>
        <h2>Leistungen</h2>
        <ul>
          <li><a href="@/leistungen/trockenbau/">Trockenbau &amp; Innenausbau</a></li>
          <li><a href="@/leistungen/hausmeisterservice/">Hausmeisterservice</a></li>
          <li><a href="@/leistungen/reparatur-und-instandhaltung/">Reparatur &amp; Instandhaltung</a></li>
          <li><a href="@/ueber-uns/#netzwerk">Koordination weiterer Gewerke</a></li>
        </ul>
      </div>
      <div>
        <h2>Unternehmen</h2>
        <ul>
          <li><a href="@/projekte/">Projekte</a></li>
          <li><a href="@/ueber-uns/">Über uns</a></li>
          <li><a href="@/ablauf/">Ablauf &amp; Fragen</a></li>
          <!--opt:MYHAMMER_URL--><li><a href="{{MYHAMMER_URL}}" rel="noopener">Profil auf MyHammer</a></li><!--/opt:MYHAMMER_URL-->
          <!--opt:GOOGLE_PROFIL_URL--><li><a href="{{GOOGLE_PROFIL_URL}}" rel="noopener">Google-Unternehmensprofil</a></li><!--/opt:GOOGLE_PROFIL_URL-->
        </ul>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a></li>
          <li><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>
          <li>{{STRASSE}}<br>{{PLZ_ORT}}</li>
        </ul>
      </div>
    </div>
    <div class="fuss-unten">
      <span>© <span id="jahr">2026</span> Gashini Dienstleistungen · {{INHABER}}</span>
      <span><a href="@/impressum/">Impressum</a> · <a href="@/datenschutz/">Datenschutz</a></span>
    </div>
  </div>
</footer>
<nav class="kontaktleiste" aria-label="Schnellkontakt">
  <a class="knopf knopf--sekundaer" href="tel:{{TELEFON_LINK}}">Anrufen</a>
  <a class="knopf knopf--primaer" href="@/kontakt/">Anfragen</a>
</nav>'''

def brotkrumen_html(kette):
    if not kette:
        return "", ""
    punkte = ['<li><a href="@/">Start</a></li>']
    ld = [{"@type": "ListItem", "position": 1, "name": "Start", "item": "https://{{DOMAIN}}/"}]
    for i, (name, ziel) in enumerate(kette, start=2):
        if ziel:
            punkte.append('<li><a href="@/%s">%s</a></li>' % (ziel, esc(name)))
        else:
            punkte.append('<li aria-current="page">%s</li>' % esc(name))
        eintrag = {"@type": "ListItem", "position": i, "name": name}
        if ziel:
            eintrag["item"] = "https://{{DOMAIN}}/" + ziel
        ld.append(eintrag)
    nav = '<nav class="brotkrumen" aria-label="Brotkrumen"><ol>%s</ol></nav>' % "".join(punkte)
    jsonld = '<script type="application/ld+json">%s</script>' % json.dumps(
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}, ensure_ascii=False)
    return nav, jsonld

def seite_rendern(meta, inhalt, quelle):
    pfad = meta["pfad"]
    indexieren = meta.get("indexieren", "ja") == "ja"
    krumen = []
    if meta.get("brotkrumen"):
        for teil in meta["brotkrumen"].split("|"):
            teil = teil.strip()
            name, _, ziel = teil.partition("=")
            krumen.append((name.strip(), ziel.strip()))
    krumen_nav, krumen_ld = brotkrumen_html(krumen)
    inhalt = inhalt.replace("[[brotkrumen]]", krumen_nav)
    inhalt = bausteine_einsetzen(inhalt, pfad)
    zusatz_kopf = meta.get("_jsonld", "") + krumen_ld
    if "faq_jsonld" in meta:
        zusatz_kopf += faq_jsonld(meta["faq_jsonld"] or None)
    if meta.get("jsonld") == "firma":
        zusatz_kopf += "<!--@jsonld-firma-->"
    kanonisch = "" if pfad == "404.html" else '<link rel="canonical" href="https://{{DOMAIN}}/%s">\n' % ("" if pfad == "" else pfad)
    robots = "" if indexieren else '<meta name="robots" content="noindex, follow">\n'
    dokument = '''<!DOCTYPE html>
<!-- Generiert aus %s durch scripts/build-site.py. Änderungen in dieser Datei gehen beim nächsten Build verloren. -->
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
%s%s<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Gashini Dienstleistungen">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="https://{{DOMAIN}}/%s">
<meta name="theme-color" content="#FAFAF8">
<link rel="icon" href="@/assets/marke/favicon.svg" type="image/svg+xml">
<link rel="preload" href="@/assets/fonts/instrument-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="@/assets/css/site.css">
<script src="@/assets/js/frueh.js"></script>
<script src="@/assets/js/site.js" defer></script>
%s
</head>
<body>
%s
<main id="inhalt" tabindex="-1">
%s
</main>
%s
</body>
</html>
''' % (quelle, esc(meta["titel"]), esc(meta["beschreibung"]), kanonisch, robots,
       esc(meta.get("og_titel", meta["titel"])), esc(meta["beschreibung"]), "" if pfad == "404.html" else pfad,
       zusatz_kopf, kopfbereich(meta.get("nav", "")), inhalt.strip(), FUSS)
    dokument = links_aufloesen(dokument, pfad if pfad != "404.html" else "")
    ziel = os.path.join(OUT, pfad, "index.html") if not pfad.endswith(".html") else os.path.join(OUT, pfad)
    schreiben(ziel, dokument)
    return pfad, indexieren

# ------------------------------------------------------------------ Seiten aus Fragmenten
def fragment_lesen(datei):
    text = lesen(datei)
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    if not m:
        raise SystemExit("Kopfdaten fehlen in " + datei)
    meta = {}
    for zeile in m.group(1).strip().splitlines():
        if ":" in zeile:
            k, _, v = zeile.partition(":")
            meta[k.strip()] = v.strip()
    for pflicht in ("titel", "beschreibung", "pfad"):
        if pflicht not in meta:
            raise SystemExit("Kopfdatum '%s' fehlt in %s" % (pflicht, datei))
    if meta["pfad"] == "/":
        meta["pfad"] = ""
    return meta, text[m.end():]

def projektseite(p):
    pfad = "projekte/%s/" % p["slug"]
    titelbild = next((b for b in p["bilder"] if b.get("rolle") == "titel"), p["bilder"][0])
    vorher = next((b for b in p["bilder"] if b.get("rolle") == "vorher"), None)
    nachher = next((b for b in p["bilder"] if b.get("rolle") == "nachher"), None)
    galerie = [b for b in p["bilder"] if b.get("rolle") == "galerie"]
    hinweis = ('<p class="redaktion">Beispieldaten – dieses Projekt ist ein Entwurf zur Darstellung der Seite und kein '
               'tatsächlich ausgeführter Auftrag. Es erscheint nicht im Produktions-Build.</p>') if p["_entwurf"] else ""
    tabelle = [("Leistung", KATEGORIEN.get(p["kategorie"], p["kategorie"])),
               ("Region", p.get("region") or "—"),
               ("Ausgeführt durch", AUSFUEHRUNG.get(p.get("ausfuehrung"), "—")),
               ("Zeitraum", p.get("datum") or "—")]
    teile = ['<header class="seitenkopf"><div class="rahmen">[[brotkrumen]]<p class="label">%s</p><h1>%s</h1>'
             '<p class="einleitung">%s</p>%s</div></header>'
             % (esc(KATEGORIEN.get(p["kategorie"], "")), esc(p["titel"]), esc(p["kurztext"]), hinweis)]
    teile.append('<section class="abschnitt abschnitt--eng"><div class="rahmen"><figure class="projekt-titelbild">%s<figcaption>%s</figcaption></figure></div></section>'
                 % (bild_html(pfad, titelbild["datei"], titelbild["alt"], laden="eager", groessen="100vw"), esc(titelbild.get("unterschrift", ""))))
    abschnitte = "".join('<h2>%s</h2>%s' % (t, inhalt) for t, inhalt in [
        ("Ausgangssituation", "<p>%s</p>" % esc(p.get("ausgangssituation", ""))),
        ("Leistungsumfang", '<ul class="aufzaehlung">%s</ul>' % "".join("<li>%s</li>" % esc(x) for x in p.get("leistungsumfang", []))),
        ("Vorgehen", "<p>%s</p>" % esc(p.get("vorgehen", ""))),
        ("Ergebnis", "<p>%s</p>" % esc(p.get("ergebnis", ""))),
    ])
    daten = '<table class="datentabelle"><caption class="nur-screenreader">Projektdaten</caption>%s</table>' % "".join(
        '<tr><th scope="row">%s</th><td>%s</td></tr>' % (esc(k), esc(v)) for k, v in tabelle)
    teile.append('<section class="abschnitt abschnitt--eng"><div class="rahmen raster"><div class="sp-text projekt-text">%s</div>'
                 '<aside class="sp-rand-r" aria-label="Projektdaten">%s</aside></div></section>' % (abschnitte, daten))
    if vorher and nachher:
        teile.append('''<section class="abschnitt abschnitt--eng abschnitt--linie"><div class="rahmen raster"><div class="sp-breit">
<h2>Vorher und nachher</h2>
<figure class="vergleich">
  <div class="vergleich-buehne">%s%s<span class="vergleich-linie" aria-hidden="true"></span>
    <span class="vergleich-etikett vergleich-etikett--vorher" aria-hidden="true">Vorher</span><span class="vergleich-etikett vergleich-etikett--nachher" aria-hidden="true">Nachher</span></div>
  <label class="nur-screenreader" for="vergleich-%s">Anteil des Vorher-Bildes</label>
  <input class="vergleich-regler" id="vergleich-%s" type="range" min="0" max="100" value="50">
  <figcaption>Regler verschieben, um Vorher- und Nachher-Zustand zu vergleichen. %s</figcaption>
</figure></div></div></section>''' % (bild_html(pfad, nachher["datei"], "Nachher: " + nachher["alt"], klasse="vergleich-nachher"),
                                  bild_html(pfad, vorher["datei"], "Vorher: " + vorher["alt"], klasse="vergleich-vorher"),
                                  esc(p["slug"]), esc(p["slug"]), esc(nachher.get("unterschrift", ""))))
    if galerie:
        eintraege = "".join('<li><a href="@/assets/bilder/%s" data-gross="@/assets/bilder/%s" data-alt="%s" data-text="%s">%s<span class="nur-screenreader">Bild vergrößern</span></a></li>'
                            % (esc(b["datei"]), esc(b["datei"]), esc(b["alt"]), esc(b.get("unterschrift", "")),
                               bild_html(pfad, b["datei"], b["alt"], groessen="(min-width: 900px) 25vw, 50vw")) for b in galerie)
        teile.append('<section class="abschnitt abschnitt--eng abschnitt--linie"><div class="rahmen"><h2>Bilder aus dem Projekt</h2>'
                     '<ul class="bilderreihe">%s</ul></div></section>' % eintraege)
        teile.append('''<dialog class="bildansicht" aria-label="Bildansicht"><figure><img src="" alt=""><figcaption></figcaption></figure>
<div class="bildansicht-steuerung"><button type="button" data-zurueck>← Vorheriges</button><span class="zaehler mono" aria-live="polite"></span>
<button type="button" data-weiter>Nächstes →</button><button type="button" data-schliessen>Schließen</button></div></dialog>''')
    teile.append("[[abschluss]]")
    meta = {"titel": "%s – %s | Gashini Dienstleistungen" % (p["titel"], KATEGORIEN.get(p["kategorie"], "")),
            "beschreibung": p["kurztext"][:155], "pfad": pfad, "nav": "projekte/",
            "brotkrumen": "Projekte=projekte/ | %s" % p["titel"],
            "indexieren": "nein" if p["_entwurf"] else "ja"}
    return seite_rendern(meta, "\n".join(teile), "data/projekte.json (%s)" % p["id"])

# ------------------------------------------------------------------ Lauf
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # Assets
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"),
                    ignore=None if ENTWUERFE else shutil.ignore_patterns("platzhalter"))
    os.makedirs(os.path.join(OUT, "assets", "marke"))
    for f in ("logo.svg", "logo-invers.svg", "signet.svg", "favicon.svg"):
        shutil.copy(os.path.join(WURZEL, "brand", f), os.path.join(OUT, "assets", "marke", f))
    shutil.copytree(os.path.join(SRC, "api"), os.path.join(OUT, "api"),
                    ignore=shutil.ignore_patterns("konfiguration*.php", "*.log"))
    shutil.copy(os.path.join(SRC, "server", "htaccess"), os.path.join(OUT, ".htaccess"))

    sitemap = []
    for datei in sorted(os.listdir(os.path.join(SRC, "seiten"))):
        if not datei.endswith(".html"):
            continue
        meta, inhalt = fragment_lesen(os.path.join(SRC, "seiten", datei))
        pfad, idx = seite_rendern(meta, inhalt, "src/seiten/" + datei)
        if idx and pfad != "404.html":
            sitemap.append((pfad, meta.get("prioritaet", "0.6")))
    for p in PROJEKTE:
        pfad, idx = projektseite(p)
        if idx:
            sitemap.append((pfad, "0.5"))

    zeilen = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pfad, prio in sorted(sitemap):
        zeilen.append("  <url><loc>https://{{DOMAIN}}/%s</loc><lastmod>{{STAND_ISO}}</lastmod><priority>%s</priority></url>" % (pfad, prio))
    zeilen.append("</urlset>")
    schreiben(os.path.join(OUT, "sitemap.xml"), "\n".join(zeilen) + "\n")
    schreiben(os.path.join(OUT, "robots.txt"), "User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://{{DOMAIN}}/sitemap.xml\n")

    for w in warnungen:
        print("WARNUNG:", w, file=sys.stderr)
    print("web/ erzeugt: %d Seiten, %d Projekte%s, Linkstil: %s"
          % (len(sitemap), len(PROJEKTE), " (inkl. Entwürfe)" if ENTWUERFE else "", LINKSTIL))

if __name__ == "__main__":
    main()
