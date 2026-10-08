# -*- coding: utf-8 -*-
"""Macht aus dem gebauten Ordner eine klar gekennzeichnete, nicht indexierbare Vorschau.

Aufruf:  python3 scripts/vorschau-markieren.py dist/web

Drei Aufgaben:
1. brand/ in den Vorschauordner kopieren und die Pfade anpassen – die Seiten
   verweisen mit ../brand/ eine Ebene nach oben, was beim Hochladen nur des
   Webordners ins Leere liefe.
2. In jeder Seite noindex/nofollow setzen und robots.txt auf Disallow stellen.
3. Einen Hinweisstreifen einblenden, damit niemand die Vorschau für die
   fertige Website hält.
"""
import io, os, re, shutil, sys

ziel = sys.argv[1] if len(sys.argv) > 1 else "dist/web"
wurzel = os.path.dirname(os.path.dirname(os.path.abspath(ziel)))
quelle_brand = os.path.join(os.path.dirname(os.path.abspath(ziel)), "brand")
if not os.path.isdir(quelle_brand):
    quelle_brand = "brand"

# 1. Markenzeichen in den Vorschauordner holen
ziel_brand = os.path.join(ziel, "brand")
os.makedirs(ziel_brand, exist_ok=True)
for f in os.listdir(quelle_brand):
    if f.endswith(".svg"):
        shutil.copy(os.path.join(quelle_brand, f), os.path.join(ziel_brand, f))

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
BANNER = (
  '<div style="background:#FBEFEB;border-bottom:1px solid #E7C4B8;color:#7A2E14;'
  'font:400 14px/1.5 Inter,Segoe UI,system-ui,sans-serif;padding:10px 20px;text-align:center">'
  'Vorschau – dies ist noch nicht die veröffentlichte Website. Angaben in '
  '<b>{{…}}</b> oder mit Nullen sind Platzhalter.</div>'
)

seiten = 0
for root, _, files in os.walk(ziel):
    for f in files:
        p = os.path.join(root, f)
        if f.endswith(".html"):
            s = io.open(p, encoding="utf-8").read()
            s = s.replace("../brand/", "brand/" if root == ziel else "../brand/")
            if NOINDEX not in s:
                s = s.replace("</head>", NOINDEX + "\n</head>", 1)
            if "Vorschau – dies ist noch nicht" not in s:
                s = s.replace("<body>", "<body>\n" + BANNER, 1)
            io.open(p, "w", encoding="utf-8").write(s)
            seiten += 1
        elif f.endswith((".css", ".js", ".xml", ".txt")):
            s = io.open(p, encoding="utf-8").read()
            io.open(p, "w", encoding="utf-8").write(s.replace("../brand/", "brand/"))

io.open(os.path.join(ziel, "robots.txt"), "w", encoding="utf-8").write(
    "# Vorschau – bewusst nicht für Suchmaschinen freigegeben.\n"
    "User-agent: *\nDisallow: /\n")
if os.path.exists(os.path.join(ziel, "sitemap.xml")):
    os.remove(os.path.join(ziel, "sitemap.xml"))

print("Vorschau markiert: %d Seiten, noindex gesetzt, robots.txt gesperrt." % seiten)
