# -*- coding: utf-8 -*-
"""Macht aus dist/web eine klar gekennzeichnete, nicht indexierbare Vorschau.

Aufruf:  python3 scripts/vorschau-markieren.py dist/web

- noindex/nofollow in jeder Seite, robots.txt auf Disallow, sitemap.xml entfernt
- Hinweisstreifen über jeder Seite, damit niemand die Vorschau für den Livebetrieb hält;
  der Schalter „Kundenansicht“ blendet Redaktionshinweise und Fotobriefings für Präsentationen aus
Nie auf einen Produktions-Build anwenden.
"""
import io, os, re, sys

ziel = sys.argv[1] if len(sys.argv) > 1 else "dist/web"
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
STREIFEN = ('<div class="vorschau-streifen" role="note"><span class="vs-lang">Vorschau – noch nicht die veröffentlichte Website. '
            'Gestrichelt unterstrichene Angaben sind noch nicht bestätigt. Das Formular sendet hier nichts.</span>'
            '<span class="vs-kurz">Vorschau · unveröffentlicht</span>'
            '<button type="button" data-kundenansicht aria-pressed="false">Kundenansicht</button></div>')

seiten = 0
for root, _, dateien in os.walk(ziel):
    for f in dateien:
        if not f.endswith(".html"):
            continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8").read()
        s = s.replace('<meta name="robots" content="noindex, follow">\n', "")
        if NOINDEX not in s:
            s = s.replace("</head>", NOINDEX + "\n</head>", 1)
        if "vorschau-streifen" not in s:
            # nach dem Sprunglink, damit er der erste Tab-Halt bleibt
            if '<a class="sprunglink"' in s:
                s = re.sub(r'(<a class="sprunglink"[^>]*>.*?</a>)', lambda m: m.group(1) + "\n" + STREIFEN, s, count=1, flags=re.S)
            else:
                s = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + STREIFEN, s, count=1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        seiten += 1

io.open(os.path.join(ziel, "robots.txt"), "w", encoding="utf-8").write(
    "# Vorschau – bewusst nicht für Suchmaschinen freigegeben.\nUser-agent: *\nDisallow: /\n")
if os.path.exists(os.path.join(ziel, "sitemap.xml")):
    os.remove(os.path.join(ziel, "sitemap.xml"))
print("Vorschau markiert: %d Seiten, noindex gesetzt, robots.txt gesperrt." % seiten)
