# -*- coding: utf-8 -*-
"""Erzeugt die Logo-SVGs mit Schrift als Vektorpfaden.

Warum: Ein SVG, das per <img> eingebunden wird, darf keine Webfonts der Seite
nutzen. Mit <text> im Logo fiel die Wortmarke deshalb je nach Gerät auf
Arial Narrow oder eine beliebige Systemschrift zurück. Als Pfade sieht das
Logo überall identisch aus.

Einmaliges Werkzeug – die Ausgabe liegt fertig in brand/. Nur nötig, wenn sich
Wortlaut oder Schrift des Logos ändern.

Voraussetzung:  pip install fonttools brotli
Aufruf:         python3 scripts/werkzeuge/logo-pfade.py <barlow-condensed-700.woff2> <barlow-condensed-500.woff2>
"""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

def textpfad(fontdatei, text, x, y, groesse, sperrung):
    f = TTFont(fontdatei)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    upm = f["head"].unitsPerEm
    s = groesse / upm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        name = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[name].draw(tp)
        cx += f["hmtx"][name][0] * s + sperrung
    return pen.getCommands(), cx - sperrung

def runde(cmd):
    import re
    return re.sub(r"-?\d+\.\d+", lambda m: ("%.2f" % float(m.group())).rstrip("0").rstrip("."), cmd)

fett, mittel = sys.argv[1], sys.argv[2]
wort, b1 = textpfad(fett, "GASHINI", 88, 44, 34, 2.5)
zusatz, b2 = textpfad(mittel, "DIENSTLEISTUNGEN", 89, 64, 14.5, 4.2)
breite = int(max(b1, b2) + 4)

SIGNET = ('<rect x="0" y="4" width="72" height="72" rx="18" fill="{grund}"{rahmen}/>'
          '<path d="M52 27a19 19 0 1 0 0 26" fill="none" stroke="#B5391C" stroke-width="9" stroke-linecap="square"/>'
          '<rect x="36" y="35.5" width="20" height="9" fill="#FFFFFF"/>')

def svg(grund, rahmen, schrift, zusatzfarbe):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 80" width="%d" height="80" role="img" aria-label="Gashini Dienstleistungen">'
            '<title>Gashini Dienstleistungen</title>%s'
            '<path fill="%s" d="%s"/><path fill="%s" d="%s"/></svg>\n'
            % (breite, breite, SIGNET.format(grund=grund, rahmen=rahmen), schrift, runde(wort), zusatzfarbe, runde(zusatz)))

ziel = os.path.join(os.path.dirname(__file__), "..", "..", "brand")
open(os.path.join(ziel, "logo.svg"), "w").write(svg("#0E0E0E", "", "#0E0E0E", "#595959"))
open(os.path.join(ziel, "logo-invers.svg"), "w").write(
    svg("#FFFFFF", ' fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.25"', "#FFFFFF", "#A3A3A3"))
print("Logo-Pfade geschrieben, Breite", breite)
