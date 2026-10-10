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
  scripts/zeichnungen.py  technische Zeichnungen (SVG)

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
import html, io, json, os, re, shutil, struct, sys, urllib.parse

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zeichnungen as zg  # noqa: E402

SRC = os.path.join(WURZEL, "src")
BILDER = os.path.join(SRC, "assets", "bilder")
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
# Leistungsauswahl im Formular – Schlüssel für ?leistung=… und die Werte, die das Backend erwartet
LEISTUNGEN = [("trockenbau", "Trockenbau & Innenausbau"), ("reparatur", "Reparatur & Instandhaltung"),
              ("hausmeister", "Hausmeisterservice"), ("mehrere", "Mehrere Arbeiten / noch unklar")]
NAV = [("leistungen/", "Leistungen"), ("projekte/", "Projekte"), ("netzwerk/", "Netzwerk"),
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
def rel(von, ziel):
    """Relativer Link von Seite `von` (z. B. 'leistungen/trockenbau/') zu `ziel`."""
    anker = ""
    if "#" in ziel:
        ziel, anker = ziel.split("#", 1)
        anker = "#" + anker
    abfrage = ""
    if "?" in ziel:
        ziel, abfrage = ziel.split("?", 1)
        abfrage = "?" + abfrage
    praefix = "../" * von.count("/")
    ist_verzeichnis = ziel == "" or ziel.endswith("/")
    if LINKSTIL == "dateien" and ist_verzeichnis:
        ziel = ziel + "index.html"
    ergebnis = praefix + ziel
    if ergebnis == "":
        ergebnis = "./"
    return ergebnis + abfrage + anker

def links_aufloesen(text, von):
    return re.sub(r'(href|src|action|data-gross|data-modul)="@/([^"]*)"',
                  lambda m: '%s="%s"' % (m.group(1), rel(von, m.group(2))), text)

def srcset_aufloesen(text, von):
    return re.sub(r'(srcset|imagesrcset)="([^"]*)"',
                  lambda m: '%s="%s"' % (m.group(1), re.sub(r"@/(\S+)", lambda n: rel(von, n.group(1)), m.group(2))), text)

def kontakt_link(leistung=None, anliegen=None):
    teile = []
    if leistung: teile.append("leistung=" + urllib.parse.quote_plus(leistung))
    if anliegen: teile.append("anliegen=" + urllib.parse.quote_plus(anliegen))
    return "@/kontakt/" + ("?" + "&amp;".join(teile) if teile else "") + "#anfrage"

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
            return 1 + int.from_bytes(kopf[24:27], "little"), 1 + int.from_bytes(kopf[27:30], "little")
        if art == b"VP8 ":
            w, h = struct.unpack("<HH", kopf[26:30]); return w & 0x3FFF, h & 0x3FFF
        if art == b"VP8L":
            b = kopf[21:25]
            return 1 + (((b[1] & 0x3F) << 8) | b[0]), 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
    if kopf[:2] == b"\xff\xd8":
        i = 2
        while i < len(kopf) - 9:
            if kopf[i] != 0xFF: i += 1; continue
            marker = kopf[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", kopf[i + 5:i + 9]); return w, h
            i += 2 + struct.unpack(">H", kopf[i + 2:i + 4])[0]
    raise ValueError("Bildformat nicht erkannt: " + pfad)

def bildvarianten(datei):
    """Vorhandene Breitenvarianten name-640/-1280/-1920.webp zu einem Bildnamen."""
    basis, _ = os.path.splitext(datei)
    return [(b, "%s-%d.webp" % (basis, b)) for b in (640, 1280, 1920)
            if os.path.exists(os.path.join(BILDER, "%s-%d.webp" % (basis, b)))]

def bild_vorhanden(datei):
    return os.path.exists(os.path.join(BILDER, datei)) or bool(bildvarianten(datei))

def bild_html(von, datei, alt, klasse="", laden="lazy", groessen="(min-width: 900px) 50vw, 100vw", prioritaet=False):
    """<img> mit festen Maßen und srcset. Gibt es nur Varianten (ohne Grunddatei), dient -1280 als src."""
    varianten = bildvarianten(datei)
    if os.path.exists(os.path.join(BILDER, datei)):
        src, w, h = datei, *bildmasse(os.path.join(BILDER, datei))
    elif varianten:
        mittel = dict(varianten).get(1280) or varianten[-1][1]
        src = mittel
        w, h = bildmasse(os.path.join(BILDER, mittel))
    else:
        raise SystemExit("Bild fehlt: " + datei)
    srcset = (' srcset="%s" sizes="%s"' % (", ".join("@/assets/bilder/%s %dw" % (v, b) for b, v in varianten), groessen)
              if varianten else "")
    return ('<img src="@/assets/bilder/%s"%s width="%d" height="%d" alt="%s" loading="%s" decoding="%s"%s%s>'
            % (esc(src), srcset, w, h, esc(alt), laden, "sync" if prioritaet else "async",
               ' fetchpriority="high"' if prioritaet else "", ' class="%s"' % klasse if klasse else ""))

def vorlade_html(datei, groessen):
    varianten = bildvarianten(datei)
    return ('<link rel="preload" as="image" type="image/webp" imagesrcset="%s" imagesizes="%s" fetchpriority="high">\n'
            % (", ".join("@/assets/bilder/%s %dw" % (v, b) for b, v in varianten), groessen))

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

PROJEKTE = projekte_laden()
FAQ_DATEN = json.loads(lesen(os.path.join(WURZEL, "data", "faq.json")))
FAQ = FAQ_DATEN["fragen"]
ANKER = json.loads(lesen(os.path.join(BILDER, "visualisierung", "anker.json")))

# ------------------------------------------------------------------ Bühne: Visualisierung mit Beschriftung
HERO_BESCHRIFTUNG = [   # Schlüssel in anker.json, Legendentext, Versatz der Nummer (Bildpunkte bei 1920 × 1600)
    ("uw", "UW-Profil an Boden und Decke", (-90, 60)),
    ("cw", "CW-Ständer, Achsmaß 625 mm", (-120, -90)),
    ("daemmung", "Mineralwolle zwischen den Ständern", (-40, -150)),
    ("platte", "Gipsplatte 12,5 mm, verschraubt", (70, -140)),
    ("spachtel", "Fugen und Schrauben gespachtelt", (110, 120)),
    ("oberflaeche", "Fertige Oberfläche", (130, 90)),
]

def visual_schnitt(von):
    b, h = 1920, 1600
    anker = ANKER["wand-schnitt"]
    marken = []
    for i, (schluessel, _, (dx, dy)) in enumerate(HERO_BESCHRIFTUNG, start=1):
        x0, y0 = anker[schluessel][0] * b, anker[schluessel][1] * h
        x1, y1 = min(max(x0 + dx, 40), b - 40), min(max(y0 + dy, 40), h - 40)
        akzent = schluessel == "cw"
        marken.append(
            '<g class="vl-gruppe" data-beschriftung>'
            '<path class="vl-linie" data-linie d="M%.0f,%.0f L%.0f,%.0f"/>'
            '<circle class="vl-punkt%s" cx="%.0f" cy="%.0f" r="7"/>%s'
            '<circle class="vl-nr" cx="%.0f" cy="%.0f" r="34"/><text class="vl-nr-text" x="%.0f" y="%.0f" text-anchor="middle">%d</text></g>'
            % (x0, y0, x1, y1, " vl-punkt--akzent" if akzent else "", x0, y0,
               '<circle class="vl-ring" cx="%.0f" cy="%.0f" r="16"/>' % (x0, y0) if akzent else "",
               x1, y1, x1, y1 + 13, i))
    svg = ('<svg class="visual-ueberlagerung" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true" focusable="false" '
           'xmlns="http://www.w3.org/2000/svg">%s</svg>' % (b, h, "".join(marken)))
    legende = '<ol class="legende" aria-label="Schichten im Bild">%s</ol>' % "".join(
        "<li>%s</li>" % esc(t) for _, t, _ in HERO_BESCHRIFTUNG)
    return ('<figure class="buehne-bild"><div class="visual">%s%s</div>%s'
            '<figcaption>Visualisierung – beispielhafter Wandaufbau, vereinfacht. Kein Projektfoto.</figcaption></figure>'
            % (bild_html(von, "visualisierung/wand-schnitt.webp",
                         "Visualisierung einer Metallständerwand im Schnitt: links offenes Ständerwerk, dann Mineralwolle, "
                         "Gipsplatten mit Schrauben, gespachtelte Fuge und rechts die fertige Oberfläche.",
                         laden="eager", groessen="(min-width: 1000px) 46vw, 100vw", prioritaet=True), svg, legende))

# ------------------------------------------------------------------ Wandaufbau (Signature 2)
WAND_SCHRITTE = [
    ("Ständerwerk", "UW-Profile an Boden und Decke, dazwischen CW-Ständer im Achsabstand von 625 mm. Hier entscheidet sich, ob die Wand gerade wird."),
    ("Dämmung", "Eine Seite ist beplankt, in die Felder kommt Mineralwolle. Leitungen und Dosen werden vorher vom Fachbetrieb gesetzt."),
    ("Beplankung", "Gipsplatten werden an den Ständern verschraubt – mit versetzten Stößen und gleichmäßigen Schraubabständen."),
    ("Spachtel & Oberfläche", "Fugen und Schraubköpfe werden gespachtelt und geschliffen. Danach ist die Fläche bereit für Anstrich oder Tapete."),
]

def wandaufbau(von, titel="Wie eine Trockenbauwand entsteht", ebene="h2"):
    schritte = "".join(
        '<li><button class="wandaufbau-schritt" type="button" data-schritt="%d" aria-pressed="%s">'
        '<span class="nr">%02d</span><span class="titel">%s</span><span class="text">%s</span></button></li>'
        % (i, "true" if i == 4 else "false", i, esc(t), esc(x)) for i, (t, x) in enumerate(WAND_SCHRITTE, start=1))
    return ('<section class="wandaufbau" id="wandaufbau" data-wandaufbau data-schritt="4" aria-labelledby="wandaufbau-titel" data-modul="@/assets/js/wandaufbau.js">'
            '<div class="rahmen wandaufbau-innen">'
            '<div class="kopfzeile"><div><p class="label">Wandaufbau</p><{e} id="wandaufbau-titel" data-zeilen>{titel}</{e}>'
            '<p class="einleitung">Vier Schritte vom Profil zur fertigen Fläche – an einem vereinfachten Beispiel. '
            'Wählen Sie einen Schritt oder scrollen Sie weiter.</p></div></div>'
            '<div class="wandaufbau-raster">'
            '<div class="wandaufbau-buehne" data-wand-buehne>'
            '<figure class="wandaufbau-rueckfall">{zeichnung}<figcaption class="nur-screenreader">Explosionsdarstellung des Wandaufbaus</figcaption></figure>'
            '<p class="wandaufbau-plakette" aria-hidden="true"><span>Beispielaufbau</span><span class="nur-3d">Ziehen zum Drehen</span></p>'
            '</div>'
            '<div class="wandaufbau-steuerung">'
            '<ol class="wandaufbau-schritte">{schritte}</ol>'
            '<div class="wandaufbau-werkzeuge"><button type="button" data-schnitt aria-pressed="false">Schichten im Schnitt zeigen</button></div>'
            '<p class="nur-screenreader" aria-live="polite" data-wand-ansage></p>'
            '</div></div>'
            '<p class="wandaufbau-vorbehalt">Vereinfachter Beispielaufbau zur Veranschaulichung. Welche Konstruktion bei Ihnen passt – '
            'Profilgröße, Plattentyp, Dämmung –, klären wir am Objekt. Aussagen zu Brand- oder Schallschutz sind mit dieser Darstellung nicht verbunden.</p>'
            '</div></section>').format(e=ebene, titel=esc(titel), zeichnung=zg.explosion(), schritte=schritte)

# ------------------------------------------------------------------ Tafeln
def tafel(svg, legende, unterschrift, klasse=""):
    li = "".join("<li>%s</li>" % esc(x) for x in legende)
    return ('<figure class="tafel %s"><div class="tafel-flaeche">%s</div>%s<figcaption>%s</figcaption></figure>'
            % (klasse, svg, '<ol class="legende">%s</ol>' % li if li else "", esc(unterschrift)))

ANWENDUNGEN = [
    ("trennwand", "Trennwände", "Einen Raum teilen, ein Arbeitszimmer abtrennen – nichttragend, mit oder ohne Tür."),
    ("vorsatzschale", "Vorsatzschalen", "Unruhige Wände begradigen und Leitungen verschwinden lassen."),
    ("decke", "Abgehängte Decken", "Neue Deckenebene unter der Rohdecke, Raum für Leitungen und Leuchten."),
    ("schacht", "Verkleidungen & Schächte", "Rohre, Steigleitungen und Ecken sauber umbauen."),
]

def anwendungen(von):
    return '<ul class="anwendungen">%s</ul>' % "".join(
        '<li class="anwendung" data-zeigen><div class="zeichen">%s</div><h3>%s</h3><p>%s</p></li>' % (zg.anwendung(a), esc(t), esc(x))
        for a, t, x in ANWENDUNGEN)

FAELLE = [
    ("tuer", "Tür schleift oder schließt nicht", "Bänder nachstellen, Schließblech anpassen, Zarge prüfen.", "Tür schleift"),
    ("wand", "Loch oder Riss in der Wand", "Dübellöcher, Stoßstellen, Risse – ausbessern, bis man nichts mehr sieht.", "Loch oder Riss in der Wand"),
    ("trockenbau", "Delle in der Trockenbauwand", "Beschädigtes Stück ausschneiden, neu einsetzen, spachteln.", "Trockenbauwand beschädigt"),
    ("silikon", "Silikonfuge erneuern", "Alte Fuge in Bad oder Küche entfernen und neu ziehen.", "Silikonfuge erneuern"),
    ("montage", "Regal, Spiegel oder Garderobe", "Fachgerecht befestigen – passend zum Untergrund.", "Montage an der Wand"),
    ("moebel", "Möbel aufbauen", "Schränke und Regale aufbauen, ausrichten, sichern.", "Möbel aufbauen"),
    ("sockel", "Sockelleiste lose oder fehlt", "Befestigen, ersetzen, Übergänge sauber schließen.", "Sockelleiste"),
    ("wasser", "Wand nach Wasserschaden", "Wenn die Ursache behoben ist: trocknen lassen, ausbessern, schließen.", "Wand nach Wasserschaden"),
]

def faelle(von):
    return '<ul class="faelle">%s</ul>' % "".join(
        '<li class="fall" data-zeigen>%s<h3>%s</h3><p>%s</p><a href="%s">Das ist mein Fall <span class="pfeil" aria-hidden="true">→</span>'
        '<span class="nur-screenreader">: %s anfragen</span></a></li>'
        % (zg.ikon(ik), esc(t), esc(x), kontakt_link("reparatur", anl), esc(t)) for ik, t, x, anl in FAELLE)

# ------------------------------------------------------------------ Leistungskarten
def leistungskarten(von, ebene="h3"):
    karten = [
        ("leistungen/trockenbau/", "01", "Trockenbau & Innenausbau", "Trennwände, Vorsatzschalen, Decken und Anpassungen im Bestand.",
         bild_html(von, "visualisierung/wand-staender.webp", "Visualisierung: Ständerwerk aus Metallprofilen, von unten gesehen.",
                   groessen="(min-width: 760px) 33vw, 100vw"), False),
        ("leistungen/reparatur-und-instandhaltung/", "02", "Reparatur & Instandhaltung", "Die Tür, die klemmt. Das Loch in der Wand. Die Fuge im Bad. Auch einzeln.",
         zg.flicken_einzeln(), True),
        ("leistungen/hausmeisterservice/", "03", "Hausmeisterservice", "Regelmäßige Rundgänge, kleine Arbeiten sofort, Mieterwechsel vorbereitet.",
         zg.rundgang(), True),
    ]
    return '<ul class="leistungskarten">%s</ul>' % "".join(
        '<li class="leistungskarte" data-zeigen><div class="leistungskarte-bild%s"><span class="leistungskarte-nr" aria-hidden="true">%s</span>%s</div>'
        '<%s><a href="@/%s">%s</a></%s><p>%s</p><span class="mehr" aria-hidden="true">Mehr erfahren <span class="pfeil">→</span></span></li>'
        % (" leistungskarte-bild--zeichnung" if zeichnung else "", nr, bild, ebene, ziel, esc(titel), ebene, esc(text))
        for ziel, nr, titel, text, bild, zeichnung in karten)

# ------------------------------------------------------------------ Projekte
def projektkarte(p, von, ueberschrift="h3", laden="lazy"):
    titelbild = next((b for b in p["bilder"] if b.get("rolle") == "titel"), p["bilder"][0])
    meta = [KATEGORIEN.get(p["kategorie"], p["kategorie"])]
    if p.get("region"): meta.append(p["region"])
    abzeichen = '<span class="abzeichen">Beispieldaten – kein echtes Projekt</span>' if p["_entwurf"] else ""
    return ('<article class="projekt" data-kategorie="%s" data-projekt>'
            '<div class="projekt-bild" data-enthuellen>%s%s</div>'
            '<p class="projekt-meta">%s</p>'
            '<%s><a href="@/projekte/%s/">%s</a></%s>'
            '<p>%s</p></article>'
            % (esc(p["kategorie"]), abzeichen, bild_html(von, titelbild["datei"], titelbild["alt"], laden=laden,
                                                       groessen="(min-width: 1000px) 33vw, (min-width: 640px) 50vw, 100vw"),
               "".join("<span>%s</span>" % esc(m) for m in meta),
               ueberschrift, esc(p["slug"]), esc(p["titel"]), ueberschrift, esc(p["kurztext"])))

BERICHT_SCHEMA = [("Ausgangssituation", "Wie es vorher war"), ("Aufgabenstellung", "Was erreicht werden sollte"),
                  ("Ausgeführte Arbeiten", "Was wir gemacht haben"), ("Prozessbilder", "Zwischenstände, eigene Fotos"),
                  ("Ergebnis", "Wie es jetzt ist"), ("Vorher / Nachher", "Gleicher Standpunkt, gleiches Licht")]

def leerzustand(von, ebene="h3"):
    schema = "".join("<li><div><strong>%s</strong><span>%s</span></div></li>" % (esc(a), esc(b)) for a, b in BERICHT_SCHEMA)
    return ('<div class="leerzustand" data-zeigen><div><p class="label">Projektberichte</p>'
            '<{e}>Die ersten Projektberichte entstehen gerade.</{e}>'
            '<p>Wir zeigen hier nur Arbeiten, die wir selbst fotografiert haben und deren Veröffentlichung die Auftraggeber freigegeben haben – '
            'ohne Adressen, ohne private Details. Bis die ersten Berichte stehen, erzählen wir Ihnen gern am Telefon, woran wir zuletzt gearbeitet haben.</p>'
            '<p class="leerzustand-aktion"><a class="textlink" href="@/leistungen/">Leistungen ansehen <span class="pfeil" aria-hidden="true">→</span></a></p></div>'
            '<div><p class="label">So ist jeder Bericht aufgebaut</p><ol class="bericht-schema">%s</ol></div></div>'
            ).format(e=ebene) % schema

def projekte_vorschau(von, anzahl=3):
    if not PROJEKTE:
        return leerzustand(von)
    return '<div class="projektraster">%s</div>' % "".join(projektkarte(p, von) for p in PROJEKTE[:anzahl])

def projekte_galerie(von):
    if not PROJEKTE:
        return leerzustand(von, "h2")
    teile = []
    kategorien = sorted({p["kategorie"] for p in PROJEKTE}, key=lambda k: list(KATEGORIEN).index(k) if k in KATEGORIEN else 99)
    if len(PROJEKTE) >= 4 and len(kategorien) > 1:
        optionen = ['<label><input type="radio" name="kategorie" value="alle" checked><span>Alle</span></label>']
        for k in kategorien:
            optionen.append('<label><input type="radio" name="kategorie" value="%s"><span>%s</span></label>' % (esc(k), esc(KATEGORIEN.get(k, k))))
        teile.append('<fieldset class="filter"><legend class="label">Nach Leistung filtern</legend>%s</fieldset>'
                     '<p id="filter-ansage" class="nur-screenreader" aria-live="polite"></p>' % "".join(optionen))
    teile.append('<div class="projektraster" data-projektraster>%s</div>' % "".join(projektkarte(p, von, ueberschrift="h2") for p in PROJEKTE))
    return "".join(teile)

# ------------------------------------------------------------------ Fragen
FAQ_THEMEN = [("anfrage", "Anfrage & Ablauf"), ("kosten", "Kosten & Abrechnung"),
              ("leistungen", "Leistungen & Partner"), ("daten", "Daten & Sicherheit")]

def faq_html(kategorie=None):
    fragen = [f for f in FAQ if kategorie is None or kategorie in f.get("seiten", [])]
    return '<div class="fragen">%s</div>' % "".join(
        '<details id="%s"><summary>%s</summary><div class="antwort"><p>%s</p></div></details>'
        % (esc(f["id"]), esc(f["frage"]), f["antwort"]) for f in fragen)

def faq_gruppen():
    themen = '<ul class="themen" aria-label="Themen">%s</ul>' % "".join(
        '<li><a href="#thema-%s">%s</a></li>' % (k, esc(t)) for k, t in FAQ_THEMEN)
    gruppen = []
    for k, t in FAQ_THEMEN:
        fragen = [f for f in FAQ if f.get("thema") == k]
        if not fragen: continue
        gruppen.append('<section class="fragen-gruppe raster" aria-labelledby="thema-%s"><div class="sp-kopf"><h2 id="thema-%s">%s</h2></div>'
                       '<div class="sp-inhalt"><div class="fragen">%s</div></div></section>'
                       % (k, k, esc(t), "".join('<details id="%s"><summary>%s</summary><div class="antwort"><p>%s</p></div></details>'
                                                 % (esc(f["id"]), esc(f["frage"]), f["antwort"]) for f in fragen)))
    return themen + "".join(gruppen)

def faq_jsonld(kategorie=None):
    fragen = [f for f in FAQ if kategorie is None or kategorie in f.get("seiten", [])]
    daten = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["frage"],
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["antwort"])}} for f in fragen]}
    return '<script type="application/ld+json">%s</script>' % json.dumps(daten, ensure_ascii=False)

# ------------------------------------------------------------------ Ablauf und Abschluss
ABLAUF = [
    ("Anfrage", "Per Formular, Telefon oder E-Mail. Ein paar Sätze und – wenn möglich – Fotos genügen."),
    ("Beratung", "Wir klären, was genau ansteht, und sehen uns die Situation bei Bedarf vor Ort an."),
    ("Planung & Angebot", "Sie erhalten ein schriftliches Angebot. Ist ein Partnerbetrieb beteiligt, steht das darin."),
    ("Umsetzung", "Wir führen die Arbeiten aus, stimmen Termine mit Ihnen ab und gehen das Ergebnis mit Ihnen durch."),
]

def ablauf_html():
    return ('<ol class="schritte" data-schritte>%s</ol>'
            % "".join('<li data-zeigen><h3>%s</h3><p>%s</p></li>' % (esc(t), esc(x)) for t, x in ABLAUF))

def abschluss_html(titel="Was steht bei Ihnen an?", text="Erzählen Sie uns von Ihrem Vorhaben – auch wenn es nur eine kleine Arbeit ist.",
                   knopf="Unverbindlich anfragen", leistung="", variante="hell", schnellwahl="nein", label="Kontakt"):
    wahl = ""
    if schnellwahl == "ja":
        wahl = '<ul class="schnellwahl" aria-label="Direkt zur passenden Anfrage">%s</ul>' % "".join(
            '<li><a href="%s">%s <span class="pfeil" aria-hidden="true">→</span></a></li>' % (kontakt_link(k), esc(t))
            for k, t in [("trockenbau", "Trockenbau"), ("reparatur", "Reparatur"), ("hausmeister", "Hausmeisterservice"), ("mehrere", "Noch unklar")])
    return ('<section class="abschluss%s" aria-labelledby="abschluss-titel"><div class="rahmen">'
            '<p class="label">%s</p><h2 id="abschluss-titel" data-zeilen>%s</h2><p class="einleitung">%s</p>%s'
            '<div class="knopf-reihe"><a class="knopf %s" href="%s">%s <span class="pfeil" aria-hidden="true">→</span></a></div>'
            '<p class="abschluss-kontakt"><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></p>'
            '</div></section>' % (" abschluss--dunkel" if variante == "dunkel" else "", esc(label), esc(titel), esc(text), wahl,
                                  "knopf--hell" if variante == "dunkel" else "knopf--primaer", kontakt_link(leistung or None), esc(knopf)))

# ------------------------------------------------------------------ Fotos und Fotobriefings
def foto(von, id, motiv, format="Querformat 3:2", licht="Tageslicht", ersatz="signet", alt=""):
    """Echtes Foto, falls vorhanden (src/assets/bilder/fotos/<id>-*.webp), sonst Ersatz + Briefing (nur Vorschau)."""
    datei = "fotos/%s.webp" % id
    if bild_vorhanden(datei):
        return '<figure class="portrait"><div class="portrait-flaeche">%s</div></figure>' % bild_html(von, datei, alt or motiv)
    if ersatz == "signet":
        flaeche = ('<div class="portrait-flaeche portrait-flaeche--signet">'
                   '<img src="@/assets/marke/signet.svg" width="72" height="72" alt="" loading="lazy"></div>')
    else:
        flaeche = '<div class="portrait-flaeche">%s</div>' % bild_html(von, ersatz, "")
    notiz = ('<!--vorschau--><p class="fotobriefing-notiz"><strong>Fotobriefing</strong>Motiv: %s · Format: %s · Licht: %s. '
             'Datei als <span class="mono">src/assets/bilder/fotos/%s-1280.webp</span> ablegen (zusätzlich -640 und -1920).</p><!--/vorschau-->'
             % (esc(motiv), esc(format), esc(licht), esc(id)))
    return '<figure class="portrait">%s%s</figure>' % (flaeche, notiz)

def einblick(von, id, motiv, format="Querformat 3:2", licht="Tageslicht"):
    datei = "fotos/%s.webp" % id
    if bild_vorhanden(datei):
        return '<li><figure class="tafel">%s<figcaption>%s</figcaption></figure></li>' % (bild_html(von, datei, motiv), esc(motiv))
    return ('<li class="fotobriefing-notiz"><strong>Fotobriefing</strong>Motiv: %s<br>Format: %s · Licht: %s<br>'
            'Datei: <span class="mono">fotos/%s-1280.webp</span></li>' % (esc(motiv), esc(format), esc(licht), esc(id)))

# ------------------------------------------------------------------ Formular
def kontaktformular():
    opt = "".join('<option value="%s" data-schluessel="%s">%s</option>' % (esc(t), k, esc(t)) for k, t in LEISTUNGEN)
    quellen = ["Google-Suche", "Google-Profil / Karte", "MyHammer", "Empfehlung", "Fahrzeug oder Flyer", "Sonstiges"]
    qopt = "".join('<option>%s</option>' % esc(x) for x in quellen)
    return ('''<form class="formular" id="anfrage" action="@/api/anfrage.php" method="post" enctype="multipart/form-data" data-anfrage novalidate>
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
    <label class="wahl" for="f-rueckruf"><input id="f-rueckruf" name="rueckruf" type="checkbox" value="ja" aria-describedby="f-rueckruf-fehler"><span>Bitte rufen Sie mich zurück<small>Dafür brauchen wir Ihre Telefonnummer.</small></span></label>
    <p class="fehlertext" id="f-rueckruf-fehler" data-fehler-fuer="rueckruf"></p>
    <div class="feld rueckruf-zeit" data-rueckruf-zeit>
      <label for="f-rueckrufzeit">Am besten erreichbar<span class="optional">optional</span></label>
      <select id="f-rueckrufzeit" name="rueckrufzeit"><option value="">Egal</option><option>Vormittags (8–12 Uhr)</option><option>Mittags (12–14 Uhr)</option><option>Nachmittags (14–18 Uhr)</option></select>
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
  <div class="feld">
    <label for="f-fotos">Fotos<span class="optional">optional</span></label>
    <p class="hilfe" id="f-fotos-hilfe">Bis zu 3 Bilder (JPEG, PNG oder WebP), zusammen höchstens 12 MB. Bitte keine Personen fotografieren. Ortsangaben in den Bilddaten können Sie vorher in der Galerie-App entfernen.</p>
    <input id="f-fotos" name="fotos[]" type="file" accept="image/jpeg,image/png,image/webp" multiple aria-describedby="f-fotos-hilfe f-fotos-fehler">
    <ul class="dateiliste" data-dateiliste aria-live="polite"></ul>
    <p class="fehlertext" id="f-fotos-fehler" data-fehler-fuer="fotos"></p>
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
  <p class="datenschutz-hinweis">Wir verwenden Ihre Angaben und Fotos ausschließlich, um Ihre Anfrage zu beantworten. Details, Speicherdauer und Ihre Rechte stehen in der <a href="@/datenschutz/#anfragen">Datenschutzerklärung</a>.</p>
  <div><button class="knopf knopf--primaer" type="submit"><span class="laedt" aria-hidden="true"></span><span class="text">Anfrage senden</span> <span class="pfeil" aria-hidden="true">→</span></button></div>
</form>''' % (opt, qopt))

def kontaktwege():
    return ('<ul class="kontaktwege">'
            '<li><span class="art">Telefon</span><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a><br><span class="gedaempft mono">{{TELEFONZEITEN}}</span></li>'
            '<li><span class="art">E-Mail</span><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>'
            '<!--opt:WHATSAPP--><li><span class="art">WhatsApp</span><a href="https://wa.me/{{WHATSAPP}}" rel="noopener">Nachricht schreiben</a>'
            '<br><span class="gedaempft mono">Ihre Nachricht wird über WhatsApp (Meta) übertragen.</span></li><!--/opt:WHATSAPP-->'
            '<li><span class="art">Einsatzgebiet</span><span>{{EINSATZGEBIET}}</span></li>'
            '<li><span class="art">Anschrift</span><span>{{STRASSE}}<br>{{PLZ_ORT}}</span></li>'
            '</ul>')

BAUSTEINE = {
    "visual-schnitt": lambda von, a: visual_schnitt(von),
    "wandaufbau": lambda von, a: wandaufbau(von, **a),
    "explosion": lambda von, a: tafel(zg.explosion("ex2"), [t for t, _ in WAND_SCHRITTE], "Explosionsdarstellung, schematisch. Beispielaufbau."),
    "anwendungen": lambda von, a: anwendungen(von),
    "flicken": lambda von, a: tafel(zg.flicken(), ["Beschädigte Stelle", "Sauber ausschneiden und hinterlegen", "Plattenstück einsetzen, verschrauben, spachteln", "Schleifen – fertig für den Anstrich"],
                                    "Ausbesserung einer Wandfläche, schematisch."),
    "rundgang": lambda von, a: tafel(zg.rundgang(), ["Eingang und Briefkästen", "Treppenhaus und Beleuchtung", "Technik- und Kellerraum (Sichtkontrolle)", "Müllplatz", "Außenanlagen"],
                                     "Beispielhafter Rundgang in einem Mehrfamilienhaus, danach ein kurzes Protokoll an Sie. Umfang und Takt legen wir mit Ihnen fest."),
    "netzwerk": lambda von, a: ('<figure class="netzwerk-diagramm" data-netzwerk>%s%s<figcaption>%s</figcaption></figure>'
                                % (zg.netzwerk("breit"), zg.netzwerk("schmal"),
                                   "Schema. Gestrichelt: Beispiele für Gewerke, die bei einem Vorhaben dazukommen können. Welche davon wir koordinieren, klären wir im Einzelfall – eine feste Partnerliste ist damit nicht gemeint.")),
    "faelle": lambda von, a: faelle(von),
    "leistungskarten": lambda von, a: leistungskarten(von, **a),
    "projekte-vorschau": lambda von, a: projekte_vorschau(von),
    "projekte-galerie": lambda von, a: projekte_galerie(von),
    "faq": lambda von, a: faq_html(a.get("seite")),
    "faq-gruppen": lambda von, a: faq_gruppen(),
    "ablauf": lambda von, a: ablauf_html(),
    "abschluss": lambda von, a: abschluss_html(**a),
    "kontaktformular": lambda von, a: kontaktformular(),
    "kontaktwege": lambda von, a: kontaktwege(),
    "foto": lambda von, a: foto(von, **a),
    "einblick": lambda von, a: einblick(von, **a),
    "kontakt-link": lambda von, a: kontakt_link(a.get("leistung"), a.get("anliegen")),
    "zeichnung": lambda von, a: ZEICHNUNGEN[a["art"]](),
    "bild": lambda von, a: bild_html(von, a["datei"], a.get("alt", ""), groessen=a.get("groessen", "(min-width: 900px) 50vw, 100vw"),
                                     laden=a.get("laden", "lazy"), prioritaet=a.get("prioritaet") == "ja"),
}
ZEICHNUNGEN = {"flicken-einzeln": zg.flicken_einzeln, "rundgang": zg.rundgang, "explosion": zg.explosion, "flicken": zg.flicken}

def bausteine_einsetzen(text, von):
    def ersetzen(m):
        name, rest = m.group(1), m.group(2) or ""
        args = dict(re.findall(r'(\w+)="([^"]*)"', rest))
        if name not in BAUSTEINE:
            raise SystemExit("Unbekannter Baustein [[%s]] in Seite %s" % (name, von))
        return BAUSTEINE[name](von, args)
    return re.sub(r"\[\[([\w-]+)((?:\s+\w+=\"[^\"]*\")*)\s*\]\]", ersetzen, text)

def redaktion_umformen(text):
    """<p class="redaktion">…</p> wird zur aufklappbaren Randnotiz. Text und Klasse bleiben für die Produktionssperre erhalten."""
    return re.sub(r'<p class="redaktion">(.*?)</p>',
                  r'<details class="redaktion"><summary>Offener Punkt</summary><p>\1</p></details>', text, flags=re.S)

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
        <a class="knopf knopf--primaer" href="@/kontakt/#anfrage">Anfrage stellen <span class="pfeil" aria-hidden="true">→</span></a>
        <a class="knopf knopf--sekundaer" href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a>
      </div>
    </nav>
    <div class="kopf-aktion">
      <a class="kopf-telefon" href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a>
      <a class="knopf knopf--primaer" href="@/kontakt/#anfrage">Anfrage stellen</a>
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
          <li><a href="@/leistungen/reparatur-und-instandhaltung/">Reparatur &amp; Instandhaltung</a></li>
          <li><a href="@/leistungen/hausmeisterservice/">Hausmeisterservice</a></li>
          <li><a href="@/netzwerk/">Netzwerk &amp; Zusammenarbeit</a></li>
        </ul>
      </div>
      <div>
        <h2>Unternehmen</h2>
        <ul>
          <li><a href="@/projekte/">Projekte</a></li>
          <li><a href="@/ueber-uns/">Über uns</a></li>
          <li><a href="@/fragen/">Fragen &amp; Ablauf</a></li>
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
  <a class="knopf knopf--primaer" href="@/kontakt/#anfrage">Anfragen</a>
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

def skripte(meta):
    """Skripte je Seite. GSAP nur dort, wo Bewegung vorgesehen ist; Flip nur für die Projektübersicht."""
    teile = ['<script src="@/assets/js/frueh.js"></script>', '<script src="@/assets/js/site.js" defer></script>']
    if meta.get("bewegung", "ja") != "nein":
        plugins = ["gsap", "ScrollTrigger", "SplitText", "DrawSVGPlugin"]
        if "flip" in meta.get("skripte", ""):
            plugins.append("Flip")
        teile += ['<script src="@/assets/js/vendor/%s.min.js" defer></script>' % p for p in plugins]
        teile.append('<script src="@/assets/js/bewegung.js" defer></script>')
    return "\n".join(teile)

def seite_rendern(meta, inhalt, quelle):
    pfad = meta["pfad"]
    indexieren = meta.get("indexieren", "ja") == "ja"
    krumen = []
    if meta.get("brotkrumen"):
        for teil in meta["brotkrumen"].split("|"):
            name, _, ziel = teil.strip().partition("=")
            krumen.append((name.strip(), ziel.strip()))
    krumen_nav, krumen_ld = brotkrumen_html(krumen)
    inhalt = inhalt.replace("[[brotkrumen]]", krumen_nav)
    inhalt = bausteine_einsetzen(inhalt, pfad)
    inhalt = redaktion_umformen(inhalt)
    zusatz_kopf = krumen_ld
    if "faq_jsonld" in meta:
        zusatz_kopf += faq_jsonld(meta["faq_jsonld"] or None)
    if meta.get("jsonld") == "firma":
        zusatz_kopf += "<!--@jsonld-firma-->"
    vorladen = vorlade_html(meta["vorladen"] + ".webp", "(min-width: 1000px) 46vw, 100vw") if meta.get("vorladen") else ""
    kanonisch = "" if pfad == "404.html" else '<link rel="canonical" href="https://{{DOMAIN}}/%s">\n' % pfad
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
%s<link rel="stylesheet" href="@/assets/css/site.css">
%s
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
       vorladen, skripte(meta), zusatz_kopf, kopfbereich(meta.get("nav", "")), inhalt.strip(), FUSS)
    von = pfad if pfad != "404.html" else ""
    dokument = srcset_aufloesen(links_aufloesen(dokument, von), von)
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
    bilder = p["bilder"]
    titelbild = next((b for b in bilder if b.get("rolle") == "titel"), bilder[0])
    vorher = next((b for b in bilder if b.get("rolle") == "vorher"), None)
    nachher = next((b for b in bilder if b.get("rolle") == "nachher"), None)
    prozess = [b for b in bilder if b.get("rolle") in ("prozess", "galerie")]
    hinweis = ('<p class="redaktion">Beispieldaten – dieses Projekt ist ein Entwurf zur Darstellung der Seite und kein '
               'tatsächlich ausgeführter Auftrag. Es erscheint nicht im Produktions-Build.</p>') if p["_entwurf"] else ""
    tabelle = [("Leistung", KATEGORIEN.get(p["kategorie"], p["kategorie"])),
               ("Region", p.get("region") or "—"),
               ("Ausgeführt durch", AUSFUEHRUNG.get(p.get("ausfuehrung"), "—")),
               ("Zeitraum", p.get("datum") or "—")]
    teile = ['<header class="seitenkopf"><div class="rahmen">[[brotkrumen]]<p class="label">%s</p><h1 data-zeilen>%s</h1>'
             '<p class="einleitung">%s</p>%s</div></header>'
             % (esc(KATEGORIEN.get(p["kategorie"], "")), esc(p["titel"]), esc(p["kurztext"]), hinweis)]
    teile.append('<section class="abschnitt abschnitt--eng" aria-label="Titelbild"><div class="rahmen"><figure class="projekt-titelbild" data-enthuellen>%s<figcaption>%s</figcaption></figure></div></section>'
                 % (bild_html(pfad, titelbild["datei"], titelbild["alt"], laden="eager", groessen="100vw"), esc(titelbild.get("unterschrift", ""))))
    bericht = []
    def abschnitt(titel, inhalt):
        if inhalt: bericht.append('<section><h2>%s</h2><div>%s</div></section>' % (titel, inhalt))
    abschnitt("Ausgangssituation", "<p>%s</p>" % esc(p["ausgangssituation"]) if p.get("ausgangssituation") else "")
    abschnitt("Aufgabenstellung", "<p>%s</p>" % esc(p["aufgabenstellung"]) if p.get("aufgabenstellung") else "")
    arbeiten = p.get("arbeiten") or p.get("leistungsumfang") or []
    abschnitt("Ausgeführte Arbeiten", '<ul class="aufzaehlung">%s</ul>' % "".join("<li>%s</li>" % esc(x) for x in arbeiten) if arbeiten else "")
    abschnitt("Vorgehen", "<p>%s</p>" % esc(p["vorgehen"]) if p.get("vorgehen") else "")
    if prozess:
        eintraege = "".join('<li><a href="@/assets/bilder/%s" data-gross="@/assets/bilder/%s" data-alt="%s" data-text="%s">%s<span class="nur-screenreader">Bild vergrößern</span></a></li>'
                            % (esc(b["datei"]), esc(b["datei"]), esc(b["alt"]), esc(b.get("unterschrift", "")),
                               bild_html(pfad, b["datei"], b["alt"], groessen="(min-width: 900px) 20vw, 50vw")) for b in prozess)
        abschnitt("Prozessbilder", '<ul class="bilderreihe">%s</ul>' % eintraege)
    abschnitt("Ergebnis", "<p>%s</p>" % esc(p["ergebnis"]) if p.get("ergebnis") else "")
    daten = '<table class="datentabelle"><caption class="nur-screenreader">Projektdaten</caption>%s</table>' % "".join(
        '<tr><th scope="row">%s</th><td>%s</td></tr>' % (esc(k), esc(v)) for k, v in tabelle)
    teile.append('<section class="abschnitt abschnitt--eng" aria-label="Projektbericht"><div class="rahmen raster"><div class="sp-text projektbericht">%s</div>'
                 '<div class="sp-rand-r"><div class="projekt-daten"><p class="label">Projektdaten</p>%s</div></div></div></section>'
                 % ("".join(bericht), daten))
    if vorher and nachher:
        teile.append('''<section class="abschnitt abschnitt--eng abschnitt--linie" aria-labelledby="vergleich-titel"><div class="rahmen raster"><div class="sp-breit">
<h2 id="vergleich-titel">Vorher und nachher</h2>
<figure class="vergleich">
  <div class="vergleich-buehne">%s%s<span class="vergleich-linie" aria-hidden="true"></span>
    <span class="vergleich-etikett vergleich-etikett--vorher" aria-hidden="true">Vorher</span><span class="vergleich-etikett vergleich-etikett--nachher" aria-hidden="true">Nachher</span></div>
  <label class="nur-screenreader" for="vergleich-%s">Anteil des Vorher-Bildes</label>
  <input class="vergleich-regler" id="vergleich-%s" type="range" min="0" max="100" value="50">
  <figcaption>Regler verschieben, um Vorher- und Nachher-Zustand zu vergleichen. %s</figcaption>
</figure></div></div></section>''' % (bild_html(pfad, nachher["datei"], "Nachher: " + nachher["alt"], klasse="vergleich-nachher"),
                                  bild_html(pfad, vorher["datei"], "Vorher: " + vorher["alt"], klasse="vergleich-vorher"),
                                  esc(p["slug"]), esc(p["slug"]), esc(nachher.get("unterschrift", ""))))
    if prozess:
        teile.append('''<dialog class="bildansicht" aria-label="Bildansicht"><figure><img src="" alt=""><figcaption></figcaption></figure>
<div class="bildansicht-steuerung"><button type="button" data-zurueck>← Vorheriges</button><span class="zaehler mono" aria-live="polite"></span>
<button type="button" data-weiter>Nächstes →</button><button type="button" data-schliessen>Schließen</button></div></dialog>''')
    schluessel = {"trockenbau": "trockenbau", "reparatur": "reparatur", "hausmeisterservice": "hausmeister"}.get(p["kategorie"], "mehrere")
    teile.append('[[abschluss titel="Ein ähnliches Vorhaben?" text="Beschreiben Sie kurz, was bei Ihnen ansteht – gern mit Fotos. Wir melden uns mit einer ersten Einschätzung." knopf="Vorhaben beschreiben" leistung="%s"]]' % schluessel)
    meta = {"titel": "%s – %s | Gashini" % (p["titel"], KATEGORIEN.get(p["kategorie"], "")),
            "beschreibung": p["kurztext"][:155], "pfad": pfad, "nav": "projekte/",
            "brotkrumen": "Projekte=projekte/ | %s" % p["titel"],
            "indexieren": "nein" if p["_entwurf"] else "ja"}
    return seite_rendern(meta, "\n".join(teile), "data/projekte.json (%s)" % p["id"])

# ------------------------------------------------------------------ Lauf
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    ignorieren = ["anker.json", "HERKUNFT.md"] + ([] if ENTWUERFE else ["platzhalter"])
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"), ignore=shutil.ignore_patterns(*ignorieren))
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
