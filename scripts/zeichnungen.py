# -*- coding: utf-8 -*-
"""Gashini Dienstleistungen – technische Zeichnungen (Bildebene „Plan“).

Alle Zeichnungen entstehen hier als SVG, ohne Fremdbibliothek. Gestaltungsregeln:
Linien 1 px (non-scaling), Flächen in Papiertönen, genau ein Ziegelrot-Akzent pro
Zeichnung, Beschriftung über nummerierte Marken mit HTML-Legende (lesbar auf jedem
Bildschirm). Elemente mit data-linie werden von bewegung.js nachgezeichnet.
"""
import math

def _f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")

def _pfad(punkte, schliessen=True):
    return "M" + " L".join("%s,%s" % (_f(x), _f(y)) for x, y in punkte) + (" Z" if schliessen else "")

def _marke(nr, x, y, r=11):
    return ('<g class="zg-marke"><circle cx="%s" cy="%s" r="%s"/><text x="%s" y="%s" text-anchor="middle">%s</text></g>'
            % (_f(x), _f(y), r, _f(x), _f(y + 4.2), nr))

def _svg(viewbox, titel, beschreibung, inhalt, klasse="", id_basis="zg"):
    return ('<svg class="zg %s" viewBox="%s" role="img" aria-labelledby="%s-t %s-d" xmlns="http://www.w3.org/2000/svg">'
            '<title id="%s-t">%s</title><desc id="%s-d">%s</desc>%s</svg>'
            % (klasse, viewbox, id_basis, id_basis, id_basis, titel, id_basis, beschreibung, inhalt))

SCHRAFFUR = ('<defs>'
             '<pattern id="%(id)s-wolle" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><path d="M0,0 v8" class="zg-schraffur"/></pattern>'
             '<pattern id="%(id)s-mauer" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0 v7" class="zg-schraffur zg-schraffur--dicht"/></pattern>'
             '</defs>')

# --------------------------------------------------------------------------- Explosionsdarstellung
def explosion(id_basis="ex"):
    """Isometrische Explosionsdarstellung eines Wandabschnitts (2 Felder, 1,25 m).
    Schichten: 1 Ständerwerk, 2 Rückseite und Dämmung, 3 Beplankung, 4 Spachtel und Oberfläche."""
    s = 104.0
    ox, oy = 40.0, 322.0
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    def P(x, y, z):
        return (ox + (x * c30 + z * c30) * s, oy + (-x * s30 + z * s30) * s - y * s)
    W, H = 1.25, 2.0
    def flaeche(x0, x1, y0, y1, z):
        return _pfad([P(x0, y0, z), P(x1, y0, z), P(x1, y1, z), P(x0, y1, z)])
    teile = [SCHRAFFUR % {"id": id_basis}]
    ebenen = {"rueck": 0.0, "staender": 0.62, "daemm": 1.18, "platte": 1.82, "fertig": 2.42}
    # Fluchtlinien zwischen den Ebenen
    for (x, y) in ((0, 0), (0, H), (W, H)):
        teile.append('<path class="zg-flucht" d="%s"/>' % _pfad([P(x, y, 0), P(x, y, ebenen["fertig"])], False))
    # 2a Rückseitige Beplankung
    teile.append('<g class="ex-schicht ex-2">')
    teile.append('<path class="zg-platte" data-linie d="%s"/>' % flaeche(0, W, 0, H, ebenen["rueck"]))
    teile.append('</g>')
    # 1 Ständerwerk: UW unten/oben, drei CW-Ständer
    z = ebenen["staender"]
    teile.append('<g class="ex-schicht ex-1">')
    for (y0, y1) in ((0, .05), (H - .05, H)):
        teile.append('<path class="zg-profil" data-linie d="%s"/>' % flaeche(0, W, y0, y1, z))
    for x in (0, .625, 1.25):
        x0 = min(max(x - .025, 0), W - .05)
        teile.append('<path class="zg-profil" data-linie d="%s"/>' % flaeche(x0, x0 + .05, .05, H - .05, z))
        # Tiefe des Profils andeuten
        teile.append('<path class="zg-duenn" d="%s"/>' % _pfad([P(x0 + .05, H - .05, z), P(x0 + .05, H - .05, z - .075), P(x0 + .05, .05, z - .075)], False))
    teile.append('</g>')
    # 2b Dämmung zwischen den Ständern
    z = ebenen["daemm"]
    teile.append('<g class="ex-schicht ex-2">')
    for x0 in (.03, .655):
        teile.append('<path class="zg-wolle" fill="url(#%s-wolle)" data-linie d="%s"/>' % (id_basis, flaeche(x0, x0 + .565, .06, H - .06, z)))
    teile.append('</g>')
    # 3 Beplankung mit Schrauben
    z = ebenen["platte"]
    teile.append('<g class="ex-schicht ex-3">')
    teile.append('<path class="zg-platte" data-linie d="%s"/>' % flaeche(0, W, 0, H, z))
    for x in (.02, .625, 1.23):
        for j in range(1, 9):
            px, py = P(x, j * H / 9, z)
            teile.append('<circle class="zg-schraube" cx="%s" cy="%s" r="1.3"/>' % (_f(px), _f(py)))
    teile.append('</g>')
    # 4 Spachtel und Oberfläche
    z = ebenen["fertig"]
    teile.append('<g class="ex-schicht ex-4">')
    teile.append('<path class="zg-fertig" data-linie d="%s"/>' % flaeche(0, W, 0, H, z))
    teile.append('<path class="zg-akzent-flaeche" d="%s"/>' % flaeche(0, .09, 0, H, z))
    teile.append('</g>')
    # Marken
    marken = [(1, P(1.25, H * .78, ebenen["staender"]), (34, -6)),
              (2, P(.95, H * .55, ebenen["daemm"]), (34, -4)),
              (3, P(1.25, H * .62, ebenen["platte"]), (34, 0)),
              (4, P(1.25, H * .46, ebenen["fertig"]), (34, 4))]
    for nr, (x, y), (dx, dy) in marken:
        teile.append('<path class="zg-hinweis" d="M%s,%s L%s,%s"/>' % (_f(x), _f(y), _f(x + dx - 11), _f(y + dy)))
        teile.append('<circle class="zg-punkt" cx="%s" cy="%s" r="2.2"/>' % (_f(x), _f(y)))
        teile.append(_marke(nr, x + dx, y + dy))
    # Achsmaß 625 an der Rückseite unten
    a, b = P(0, -.16, 0), P(.625, -.16, 0)
    teile.append('<path class="zg-mass zg-mass--akzent" d="%s"/>' % _pfad([a, b], False))
    for q in (a, b):
        teile.append('<path class="zg-mass" d="M%s,%s l-4,4 M%s,%s l4,-4"/>' % (_f(q[0]), _f(q[1]), _f(q[0]), _f(q[1])))
    m = P(.3125, -.3, 0)
    teile.append('<text class="zg-text zg-text--akzent" x="%s" y="%s" text-anchor="middle" transform="rotate(-30 %s %s)">625</text>' % (_f(m[0]), _f(m[1]), _f(m[0]), _f(m[1])))
    return _svg("0 0 480 500", "Explosionsdarstellung einer Metallständerwand",
                "Schichten eines beispielhaften Wandaufbaus, auseinandergezogen: 1 Ständerwerk aus UW- und CW-Profilen im Achsabstand 625 Millimeter, "
                "2 rückseitige Beplankung und Mineralwolle zwischen den Ständern, 3 Gipsplatten mit Schrauben, 4 gespachtelte, fertige Oberfläche.",
                "".join(teile), "zg--explosion", id_basis)

# --------------------------------------------------------------------------- Anwendungen (klein)
def anwendung(art):
    t, idb = [], "anw-" + art
    t.append(SCHRAFFUR % {"id": idb})
    if art == "trennwand":   # Grundriss: Raum, neue Wand mit Tür
        t.append('<path class="zg-poche" d="M20,20 H220 V160 H20 Z M28,28 V152 H212 V28 Z" fill-rule="evenodd"/>')
        t.append('<path class="zg-neu" data-linie d="M118,28 V92 M118,124 V152 M126,28 V92 M126,124 V152 M118,28 H126 M118,92 H126 M118,124 H126 M118,152 H126"/>')
        t.append('<path class="zg-duenn" data-linie d="M126,92 L160,92 M126,92 A32,32 0 0 1 158,124"/>')
        t.append('<path class="zg-mass" d="M28,172 H118 M118,172 H212"/>')
        titel, besch = "Trennwand im Grundriss", "Ein Raum wird durch eine neue Ständerwand mit Türöffnung in zwei Räume geteilt."
    elif art == "vorsatzschale":   # Schnitt: Bestandswand, Leitungen, Vorsatzschale
        t.append('<path class="zg-mauer" fill="url(#%s-mauer)" d="M20,15 H70 V165 H20 Z"/>' % idb)
        t.append('<path class="zg-linie" d="M70,15 V165"/>')
        t.append('<circle class="zg-duenn" cx="84" cy="60" r="6"/><circle class="zg-duenn" cx="84" cy="112" r="4"/>')
        t.append('<path class="zg-profil" data-linie d="M98,15 V165 M106,15 V165"/>')
        t.append('<path class="zg-neu" data-linie d="M108,15 V165 M112,15 V165 M108,15 H112 M108,165 H112"/>')
        t.append('<path class="zg-duenn" d="M20,165 H220 M20,15 H220"/>')
        t.append('<path class="zg-mass" d="M70,178 H112"/>')
        titel, besch = "Vorsatzschale im Schnitt", "Vor einer bestehenden Wand entsteht eine neue Ebene; Leitungen verschwinden dahinter."
    elif art == "decke":   # Schnitt: Rohdecke, Abhänger, Profile, Platte
        t.append('<path class="zg-mauer" fill="url(#%s-mauer)" d="M15,15 H225 V45 H15 Z"/>' % idb)
        t.append('<path class="zg-linie" d="M15,45 H225"/>')
        for x in (45, 120, 195):
            t.append('<path class="zg-duenn" data-linie d="M%d,45 V116"/>' % x)
        t.append('<path class="zg-profil" data-linie d="M20,116 H220 M20,122 H220"/>')
        t.append('<path class="zg-neu" data-linie d="M20,124 H220 M20,129 H220 M20,124 V129 M220,124 V129"/>')
        t.append('<path class="zg-mass" d="M232,45 V129"/>')
        titel, besch = "Abgehängte Decke im Schnitt", "Unter der Rohdecke hängt eine Unterkonstruktion mit Gipsplatten; dazwischen bleibt Raum für Leitungen."
    else:   # schacht – Grundriss: Raumecke mit Rohren
        t.append('<path class="zg-poche" d="M20,20 H220 V28 H28 V160 H20 Z"/>')
        t.append('<circle class="zg-duenn" cx="52" cy="52" r="10"/><circle class="zg-duenn" cx="80" cy="50" r="7"/><circle class="zg-duenn" cx="52" cy="82" r="6"/>')
        t.append('<path class="zg-neu" data-linie d="M104,28 V106 H28 M112,28 V114 H28"/>')
        t.append('<path class="zg-duenn" d="M104,106 L112,114"/>')
        t.append('<path class="zg-mass" d="M28,128 H112"/>')
        titel, besch = "Installationsschacht im Grundriss", "Rohre in einer Raumecke werden mit einer Trockenbau-Verkleidung umbaut."
    return _svg("0 0 240 190", titel, besch, "".join(t), "zg--anwendung", idb)

# --------------------------------------------------------------------------- Ausbesserung in vier Schritten
def flicken():
    t = [SCHRAFFUR % {"id": "fl"}]
    for i in range(4):
        x0 = 10 + i * 180
        t.append('<g class="fl-feld" data-feld="%d">' % (i + 1))
        t.append('<rect class="zg-fertig" x="%d" y="20" width="160" height="150"/>' % x0)
        cx, cy = x0 + 80, 92
        if i == 0:   # Schaden
            t.append('<path class="zg-schaden" data-linie d="M%s,%s l14,-10 l9,7 l13,-4 l6,12 l-5,13 l9,9 l-15,6 l-6,-9 l-12,8 l-8,-12 l-11,-3 l6,-11 z"/>' % (_f(cx - 26), _f(cy - 6)))
            t.append('<path class="zg-duenn" d="M%s,%s l-14,-16 M%s,%s l18,-12" />' % (_f(cx - 20), _f(cy - 12), _f(cx + 16), _f(cy - 10)))
        elif i == 1:   # Ausschneiden, Hinterlegen
            t.append('<rect class="zg-loch" x="%s" y="%s" width="64" height="50"/>' % (_f(cx - 32), _f(cy - 25)))
            t.append('<path class="zg-unsichtbar" data-linie d="M%s,%s h88 M%s,%s h88"/>' % (_f(cx - 44), _f(cy - 18), _f(cx - 44), _f(cy + 18)))
            t.append('<path class="zg-akzent" data-linie d="M%s,%s h64 v50 h-64 z"/>' % (_f(cx - 32), _f(cy - 25)))
        elif i == 2:   # Einsetzen und spachteln
            t.append('<rect class="zg-spachtelband" x="%s" y="%s" width="84" height="70"/>' % (_f(cx - 42), _f(cy - 35)))
            t.append('<rect class="zg-platte" x="%s" y="%s" width="62" height="48"/>' % (_f(cx - 31), _f(cy - 24)))
            for dx, dy in ((-24, -17), (24, -17), (-24, 17), (24, 17)):
                t.append('<circle class="zg-schraube" cx="%s" cy="%s" r="1.4"/>' % (_f(cx + dx), _f(cy + dy)))
            t.append('<path class="zg-akzent" data-linie d="M%s,%s l34,-22 l9,8 l-30,26 z M%s,%s l-12,10"/>' % (_f(cx + 24), _f(cy + 40), _f(cx + 30), _f(cy + 52)))
        else:   # Schleifen, fertig
            t.append('<rect class="zg-spachtelband zg-spachtelband--glatt" x="%s" y="%s" width="84" height="70"/>' % (_f(cx - 42), _f(cy - 35)))
            t.append('<path class="zg-duenn" d="M%s,%s c10,-6 20,6 30,0 s20,6 30,0" />' % (_f(cx - 30), _f(cy)))
            t.append('<rect class="zg-akzent" data-linie x="%s" y="%s" width="44" height="20" rx="2"/>' % (_f(cx + 2), _f(cy + 38)))
        t.append(_marke(i + 1, x0 + 18, 38))
        t.append('</g>')
        if i < 3:
            t.append('<path class="zg-pfeil" d="M%s,95 h10 m-4,-4 l4,4 l-4,4"/>' % _f(x0 + 164))
    return _svg("0 0 730 190", "Ausbesserung einer Wandfläche in vier Schritten",
                "1 beschädigte Stelle, 2 sauber ausgeschnitten und hinterlegt, 3 neues Plattenstück eingesetzt, verschraubt und gespachtelt, "
                "4 geschliffen und bereit für den Anstrich.", "".join(t), "zg--flicken", "fl")

def flicken_einzeln():
    """Kartenmotiv Reparatur: Wandstück mit eingesetztem Flicken, Spachtelband und Spachtel."""
    t = [SCHRAFFUR % {"id": "fe"}]
    t.append('<rect class="zg-fertig" x="20" y="20" width="260" height="300"/>')
    t.append('<path class="zg-duenn" d="M20,286 H280 M20,300 H280"/>')
    t.append('<rect class="zg-spachtelband" x="70" y="88" width="150" height="122"/>')
    t.append('<rect class="zg-platte" data-linie x="96" y="110" width="98" height="78"/>')
    for x, y in ((106, 120), (184, 120), (106, 178), (184, 178)):
        t.append('<circle class="zg-schraube" cx="%d" cy="%d" r="1.6"/>' % (x, y))
    t.append('<path class="zg-unsichtbar" d="M74,124 H216 M74,174 H216"/>')
    t.append('<path class="zg-akzent" data-linie d="M168,236 L232,190 L246,204 L186,254 Z M196,246 L174,268 M178,272 L170,264"/>')
    t.append('<path class="zg-mass" d="M96,226 H194 M96,222 v8 M194,222 v8"/>')
    t.append('<text class="zg-text" x="145" y="244" text-anchor="middle">Flicken</text>')
    return _svg("0 0 300 340", "Ausbesserung einer Wandfläche", "Ein neues Plattenstück ist eingesetzt und verschraubt; das Spachtelband deckt die Ränder; daneben der Spachtel.",
                "".join(t), "zg--flicken-einzeln", "fe")

# --------------------------------------------------------------------------- Objektrundgang (Grundriss)
def rundgang():
    t = [SCHRAFFUR % {"id": "rg"}]
    # Gebäude: Außenwände
    t.append('<path class="zg-poche" fill-rule="evenodd" d="M60,40 H440 V300 H60 Z M68,48 V292 H432 V48 Z"/>')
    # Innenwände: Treppenhaus Mitte, zwei Wohnungen
    t.append('<path class="zg-wand" d="M200,48 V180 M200,212 V292 M300,48 V120 M300,152 V292 M200,180 H218 M282,180 H300"/>')
    # Treppe
    for i in range(9):
        t.append('<path class="zg-duenn" d="M%d,200 V284"/>' % (210 + i * 9))
    t.append('<path class="zg-duenn" d="M206,242 H294"/>')
    # Eingang unten (Lücke in der Außenwand)
    t.append('<path class="zg-papier" d="M232,290 H268 V302 H232 Z"/>')
    t.append('<path class="zg-duenn" d="M232,292 A36,36 0 0 1 268,292"/>')
    # Briefkästen
    t.append('<path class="zg-linie" d="M276,304 h30 v8 h-30 z M286,304 v8 M296,304 v8"/>')
    # Keller-/Technikraum, Müllplatz, Garten
    t.append('<path class="zg-duenn" d="M68,200 H200"/>')
    t.append('<text class="zg-text" x="134" y="252" text-anchor="middle">Technik</text>')
    t.append('<text class="zg-text" x="134" y="118" text-anchor="middle">Whg. 1</text>')
    t.append('<text class="zg-text" x="366" y="186" text-anchor="middle">Whg. 2</text>')
    t.append('<rect class="zg-flaeche" x="350" y="322" width="70" height="34"/>')
    t.append('<path class="zg-duenn" d="M360,330 h14 v18 h-14 z M380,330 h14 v18 h-14 z M400,330 h14 v18 h-14 z"/>')
    for (x, y) in ((494, 96), (500, 150), (492, 222), (90, 342), (140, 356)):
        t.append('<circle class="zg-duenn" cx="%d" cy="%d" r="11"/>' % (x, y))
    # Route: Straße → Briefkästen → Treppenhaus → Technik → zurück → Müllplatz → Außenanlagen
    route = [(250, 392), (250, 334), (291, 320), (250, 304), (250, 262), (250, 196), (160, 196), (160, 232),
             (160, 196), (250, 196), (250, 304), (385, 318), (462, 262), (462, 84)]
    t.append('<path class="zg-route" data-linie d="%s"/>' % _pfad(route, False))
    for nr, (x, y) in enumerate([(291, 320), (250, 262), (160, 232), (385, 318), (462, 170)], start=1):
        t.append(_marke(nr, x, y, 10))
    return _svg("0 0 520 400", "Objektrundgang im Grundriss eines Mehrfamilienhauses",
                "Beispielhafte Route einer regelmäßigen Kontrolle: 1 Eingang und Briefkästen, 2 Treppenhaus, 3 Technik- und Kellerraum, "
                "4 Müllplatz, 5 Außenanlagen. Danach erhält der Auftraggeber ein kurzes Protokoll.", "".join(t), "zg--rundgang", "rg")

# --------------------------------------------------------------------------- Netzwerk
NETZ_EIGEN = ["Trockenbau", "Reparatur", "Hausmeister"]
NETZ_GEWERKE = ["Elektro", "Sanitär & Heizung", "Malerarbeiten", "Bodenbeläge", "Fliesen", "Tischler", "Reinigung", "Entsorgung"]

def netzwerk(format="breit"):
    t = []
    mitte = lambda cx, cy, r: ('<g class="nz-knoten nz-knoten--mitte" data-knoten><circle cx="%s" cy="%s" r="%s"/>'
                               '<text x="%s" y="%s" text-anchor="middle">Gashini</text><text class="nz-klein" x="%s" y="%s" text-anchor="middle">Ihr Kontakt</text></g>'
                               % (_f(cx), _f(cy), r, _f(cx), _f(cy - 1), _f(cx), _f(cy + 16)))
    sie = lambda x, y: ('<g class="nz-knoten nz-knoten--sie" data-knoten><circle cx="%s" cy="%s" r="30"/><text x="%s" y="%s" text-anchor="middle">Sie</text></g>'
                        % (_f(x), _f(y), _f(x), _f(y + 5)))
    if format == "breit":
        cx, cy, r_eigen = 470, 260, 125
        t.append('<path class="nz-linie nz-linie--sie" data-linie d="M70,260 L%s,%s"/>' % (_f(cx), _f(cy)))
        n = len(NETZ_GEWERKE)
        for i, name in enumerate(NETZ_GEWERKE):
            w = math.radians(-90 + 180 / n + i * 360 / n)
            x, y = cx + math.cos(w) * 297, cy + math.sin(w) * 207
            t.append('<path class="nz-linie nz-linie--partner" data-linie d="M%s,%s L%s,%s"/>' % (_f(cx), _f(cy), _f(x), _f(y)))
            t.append('<g class="nz-knoten nz-knoten--partner" data-knoten><circle cx="%s" cy="%s" r="5"/><text x="%s" y="%s" text-anchor="middle">%s</text></g>'
                     % (_f(x), _f(y), _f(x), _f(y - 12 if y < cy else y + 22), name.replace("&", "&amp;")))
        for i, name in enumerate(NETZ_EIGEN):
            w = math.radians(-90 + i * 120)
            x, y = cx + math.cos(w) * r_eigen, cy + math.sin(w) * r_eigen
            t.append('<path class="nz-linie nz-linie--eigen" data-linie d="M%s,%s L%s,%s"/>' % (_f(cx), _f(cy), _f(x), _f(y)))
            t.append('<g class="nz-knoten nz-knoten--eigen" data-knoten><circle cx="%s" cy="%s" r="9"/><text x="%s" y="%s" text-anchor="middle">%s</text></g>'
                     % (_f(x), _f(y), _f(x), _f(y - 18 if y < cy else y + 28), name))
        t.append(sie(70, 260)); t.append(mitte(cx, cy, 52))
        vb = "0 0 900 520"
    else:
        cx, cy = 190, 210
        t.append('<path class="nz-linie nz-linie--sie" data-linie d="M190,52 L190,%s"/>' % _f(cy))
        for i, (name, x) in enumerate(zip(NETZ_EIGEN, (62, 190, 318))):
            t.append('<path class="nz-linie nz-linie--eigen" data-linie d="M%s,%s L%s,330"/>' % (_f(cx), _f(cy), _f(x)))
            t.append('<g class="nz-knoten nz-knoten--eigen" data-knoten><circle cx="%s" cy="330" r="9"/><text x="%s" y="362" text-anchor="middle">%s</text></g>' % (_f(x), _f(x), name))
        t.append('<path class="nz-linie nz-linie--partner" data-linie d="M%s,%s C 360,260 360,380 320,410"/>' % (_f(cx + 40), _f(cy + 30)))
        t.append('<g class="nz-knoten nz-knoten--gruppe" data-knoten><rect x="12" y="410" width="356" height="190" rx="2"/>'
                 '<text class="nz-klein-hell" x="30" y="440">Fachbetriebe – Beispiele</text>')
        for i, name in enumerate(NETZ_GEWERKE):
            x, y = 26 + (i % 2) * 164, 476 + (i // 2) * 34
            t.append('<circle cx="%s" cy="%s" r="4"/><text x="%s" y="%s">%s</text>' % (x + 4, y - 5, x + 16, y, name.replace("&", "&amp;")))
        t.append('</g>')
        t.append(sie(190, 40)); t.append(mitte(cx, cy, 62))
        vb = "0 0 380 620"
    return _svg(vb, "Zusammenarbeit im Netzwerk",
                "Sie haben einen Ansprechpartner: Gashini. Trockenbau, Reparatur und Hausmeisterservice führt Gashini selbst aus. "
                "Weitere Gewerke wie Elektro, Sanitär, Malerarbeiten, Bodenbeläge, Fliesen, Tischler, Reinigung oder Entsorgung können bei einem Vorhaben "
                "hinzukommen; sie werden von Fachbetrieben ausgeführt. Die Darstellung zeigt Beispiele, keine feste Partnerliste.",
                "".join(t), "zg--netzwerk zg--netzwerk-" + format, "nz-" + format)

# --------------------------------------------------------------------------- Symbole für Alltagsfälle
IKONEN = {
    "tuer": '<path d="M12,42 V8 H34 V42"/><path class="ik-akzent" d="M14,10 L28,14 V44 L14,40 Z"/><circle cx="24" cy="28" r="1.4"/><path d="M36,30 a8,8 0 0 1 0,10"/>',
    "wand": '<rect x="6" y="8" width="36" height="32"/><path class="ik-akzent" d="M20,14 l4,6 l-3,5 l5,6 l-2,5"/><path d="M30,26 h8 v8 h-8 z"/>',
    "trockenbau": '<path d="M8,8 h32 v32 h-32 z M24,8 v32"/><path class="ik-akzent" d="M14,22 q4,-5 8,0 q-4,5 -8,0 z"/><circle cx="10" cy="14" r="1"/><circle cx="10" cy="34" r="1"/><circle cx="38" cy="14" r="1"/><circle cx="38" cy="34" r="1"/>',
    "silikon": '<path d="M8,40 h32 M8,8 v32 M16,40 v-6 M24,40 v-6 M32,40 v-6 M8,32 h6 M8,24 h6 M8,16 h6"/><path class="ik-akzent" d="M12,38 l24,-24"/><path d="M30,10 l8,-4 l4,4 l-4,8 z"/>',
    "montage": '<path d="M6,18 h36 M6,22 h36"/><path d="M12,22 v8 l6,-8 M36,22 v8 l-6,-8"/><path class="ik-akzent" d="M14,18 v-8 h6 v8 M26,18 v-12 h8 v12"/><circle cx="12" cy="34" r="1.2"/><circle cx="36" cy="34" r="1.2"/>',
    "moebel": '<path d="M10,12 h28 v28 h-28 z M10,26 h28 M22,19 h4 M22,33 h4"/><path class="ik-akzent" d="M34,6 l8,0 l0,3 l-5,0 l-6,6"/>',
    "sockel": '<path d="M8,8 v32 h32"/><path d="M8,34 h32"/><path class="ik-akzent" d="M8,38 h22 l4,-4"/><path d="M20,30 l2,-4 l2,4"/>',
    "wasser": '<path d="M8,40 h32 v-32 h-32 z"/><path class="ik-akzent" d="M24,14 c-5,7 -7,10 -7,14 a7,7 0 0 0 14,0 c0,-4 -2,-7 -7,-14 z"/>',
    "schloss": '<rect x="12" y="20" width="24" height="20" rx="2"/><path d="M17,20 v-6 a7,7 0 0 1 14,0 v6"/><path class="ik-akzent" d="M24,28 v5"/>',
    "lampe": '<path d="M24,6 v8"/><path d="M14,24 a10,10 0 0 1 20,0 z"/><path class="ik-akzent" d="M20,30 h8 M21,34 h6"/>',
}

def ikon(name):
    return ('<svg class="ikon" viewBox="0 0 48 48" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % IKONEN[name])

# --------------------------------------------------------------------------- Einsatzgebiet
def luftlinie_km(a, b):
    """Großkreisentfernung zweier Punkte (breite, laenge) in Kilometern."""
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[1] - a[1]) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))

def einsatzkarte(daten, ziel=None):
    """Schematische Karte: Ringe in 10-km-Schritten um den Mittelpunkt, Orte als Punkte (für 30 km genau genug:
    Längengrade mit cos(Breite) gestaucht). Dauerhaft beschriftet sind die Orte mit 'karte' in data/einsatzgebiet.json.
    Mit ziel(ort, kreis) wird jeder Ort ein Link (Kontaktformular mit PLZ bzw. Auswahl bei mehreren PLZ); die übrigen
    Namen erscheinen dann beim Überfahren. Die interaktive Karte ist aria-hidden – dieselben Ziele stehen als Liste
    unter der Karte und sind dort per Tastatur und Screenreader erreichbar."""
    m = daten["mittelpunkt"]; radius = daten["radius_km"]
    cx, cy, r_px = 320.0, 320.0, 260.0
    s = r_px / radius
    kx = 111.32 * math.cos(math.radians(m["breite"]))
    pos = lambda o: (cx + (o["laenge"] - m["laenge"]) * kx * s, cy - (o["breite"] - m["breite"]) * 111.2 * s)
    t = ['<circle class="zg-flaeche zg-flaeche--ohne" cx="%s" cy="%s" r="%s"/>' % (_f(cx), _f(cy), _f(r_px))]
    for km in range(10, radius, 10):
        t.append('<circle class="zg-flucht" cx="%s" cy="%s" r="%s"/>' % (_f(cx), _f(cy), _f(km * s)))
    t.append('<circle class="zg-ring" data-linie cx="%s" cy="%s" r="%s"/>' % (_f(cx), _f(cy), _f(r_px)))
    for km in range(10, radius + 1, 10):
        t.append('<text class="zg-text zg-text--klein" x="%s" y="%s" text-anchor="end">%d km</text>' % (_f(cx - km * s - 5), _f(cy + 17), km))
    # Nordpfeil
    t.append('<path class="zg-linie" d="M40,92 V44 M32,58 L40,44 L48,58"/><text class="zg-text" x="40" y="112" text-anchor="middle">N</text>')
    beschriftung = []
    for kreis in daten["kreise"]:
        for o in kreis["orte"]:
            x, y = pos(o)
            name = o.get("kurz", o["name"])
            if o.get("karte"):
                lage = {"r": (x + 10, y + 5, "start"), "l": (x - 10, y + 5, "end"),
                        "o": (x, y - 12, "middle"), "u": (x, y + 22, "middle")}[o["karte"]]
                schild = ('<text class="zg-text zg-text--ort" x="%s" y="%s" text-anchor="%s">%s</text>'
                          % (_f(lage[0]), _f(lage[1]), lage[2], name))
            elif ziel:
                rechts = x < 470
                schild = ('<text class="zg-text zg-text--ort ek-schild" x="%s" y="%s" text-anchor="%s">%s</text>'
                          % (_f(x + 10 if rechts else x - 10), _f(y + 5), "start" if rechts else "end", name))
            else:
                schild = ""
            punkt = '<circle class="zg-punkt" cx="%s" cy="%s" r="4"/>' % (_f(x), _f(y))
            if ziel:
                t.append('<a class="ek-ort" href="%s" tabindex="-1" data-kreis="%s" data-ort="%s" data-plz="%s">'
                         '<circle class="ek-treffer" cx="%s" cy="%s" r="15"/>%s%s</a>'
                         % (ziel(o, kreis), kreis["id"], o["name"], " ".join(o.get("plz", [])), _f(x), _f(y), punkt, schild))
            else:
                t.append(punkt)
                if schild: beschriftung.append(schild)
    t += beschriftung
    t.append('<g class="ek-mitte" data-plz="%s"><circle class="zg-akzent" cx="%s" cy="%s" r="9"/>'
             '<text class="zg-text zg-text--ort zg-text--haupt" x="%s" y="%s" text-anchor="middle">%s</text></g>'
             % (" ".join(m.get("plz", [])), _f(cx), _f(cy), _f(cx), _f(cy + 30), m["name"]))
    anzahl = sum(len(k["orte"]) for k in daten["kreise"])
    if ziel:
        return ('<svg class="zg zg--karte" viewBox="0 0 640 640" aria-hidden="true" focusable="false" '
                'xmlns="http://www.w3.org/2000/svg">%s</svg>' % "".join(t))
    return _svg("0 0 640 640", "Einsatzgebiet: %s und %d km Umkreis" % (m["name"], radius),
                "Schematische Karte. Ringe markieren 10, 20 und %d Kilometer Luftlinie ab %s-Mitte. Punkte zeigen %d Städte und "
                "Gemeinden im Umkreis, beschriftet sind die größeren. Die vollständige Liste steht unter der Karte."
                % (radius, m["name"], anzahl), "".join(t), "zg--karte", "ek")
