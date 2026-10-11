#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statische Prüfungen des Builds – nur Python-Standardbibliothek.

  python3 tests/pruefen.py

Prüft: Build-Wiederholbarkeit, Drift zwischen Quelle und web/, interne Links und
Anker, Seitengrundlagen (Titel, Beschreibung, H1, Canonical, lang), Bild-Alt-Texte,
externe Ressourcen, Platzhalter, Vorschau-Sperre und Produktions-robots.
Gibt am Ende eine Zusammenfassung aus; Exit-Code 1 bei Fehlern.
"""
import hashlib, html.parser, io, os, re, shutil, subprocess, sys, tempfile

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fehler, hinweise, bestanden = [], [], []

def lauf(*cmd, env=None):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=WURZEL, capture_output=True, text=True, env=e)
    if r.returncode not in (0,):
        raise RuntimeError("%s\n%s%s" % (" ".join(cmd), r.stdout, r.stderr))
    return r

def baum_hash(pfad):
    h = hashlib.sha256()
    for root, _, dateien in sorted(os.walk(pfad)):
        for f in sorted(dateien):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, pfad).encode()); h.update(open(p, "rb").read())
    return h.hexdigest()

def pruefung(name):
    def deko(fn):
        def inner():
            try:
                fn(); bestanden.append(name)
            except AssertionError as e:
                fehler.append("%s: %s" % (name, e))
        inner.__name__ = name
        return inner
    return deko

class Seite(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.h, self.imgs, self.ressourcen = [], set(), [], [], []
        self.title, self.meta, self.lang, self.canonical = "", {}, None, None
        self._im_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "html": self.lang = a.get("lang")
        if tag == "a" and "href" in a: self.links.append(a["href"])
        if tag in ("h1", "h2", "h3", "h4"): self.h.append(int(tag[1]))
        if tag == "img": self.imgs.append(a)
        if tag == "title" and not self.title: self._im_title = True   # nur der Dokumenttitel, nicht <title> in SVG
        if tag == "meta" and a.get("name"): self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        if tag in ("script", "img") and a.get("src"): self.ressourcen.append(a["src"])
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "preload", "icon"): self.ressourcen.append(a["href"])
        if tag == "form" and a.get("action"): self.links.append(a["action"])
    def handle_endtag(self, tag):
        if tag == "title": self._im_title = False
    def handle_data(self, d):
        if self._im_title: self.title += d

def seiten(basis):
    for root, _, dateien in os.walk(basis):
        for f in dateien:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                s = Seite(); s.feed(io.open(p, encoding="utf-8").read())
                yield os.path.relpath(p, basis), p, s

def ziel_aufloesen(basis, seitenpfad, href):
    href, _, anker = href.partition("#")
    if href == "":
        return seitenpfad, anker
    pfad = os.path.normpath(os.path.join(os.path.dirname(seitenpfad), href.split("?")[0]))
    if os.path.isdir(pfad): pfad = os.path.join(pfad, "index.html")
    return pfad, anker

# ---------------------------------------------------------------------------
@pruefung("Build ist wiederholbar (zwei Läufe, identische Ausgabe)")
def t_wiederholbar():
    lauf("python3", "scripts/build-site.py"); a = baum_hash(os.path.join(WURZEL, "web"))
    lauf("python3", "scripts/build-site.py"); b = baum_hash(os.path.join(WURZEL, "web"))
    assert a == b, "Ausgabe unterscheidet sich zwischen zwei Läufen"

@pruefung("web/ entspricht der Quelle (keine Handänderungen)")
def t_drift():
    r = subprocess.run(["git", "status", "--porcelain", "--", "web/"], cwd=WURZEL, capture_output=True, text=True)
    geaendert = [z for z in r.stdout.splitlines() if z.strip()]
    if os.environ.get("CI"):
        assert not geaendert, "web/ weicht vom Generator ab: %s" % geaendert[:5]
    elif geaendert:
        hinweise.append("web/ hat nicht eingecheckte Änderungen – vor dem Commit neu bauen und einchecken.")

@pruefung("firmendaten.py arbeitet mit dem Generator zusammen (Vorschau-Build)")
def t_zusammenspiel():
    lauf("python3", "scripts/firmendaten.py")
    assert os.path.isfile(os.path.join(WURZEL, "dist/web/index.html")), "dist/web/index.html fehlt"
    roh = io.open(os.path.join(WURZEL, "dist/web/index.html"), encoding="utf-8").read()
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", roh), "unersetzte Platzhalter in dist/web/index.html"

@pruefung("Produktions-Build bricht bei offenen Angaben ab")
def t_produktion_sperrt():
    r = subprocess.run(["python3", "scripts/firmendaten.py", "--produktion"], cwd=WURZEL, capture_output=True, text=True)
    assert r.returncode != 0, "Produktions-Build lief trotz offener Angaben durch"
    assert not os.path.exists(os.path.join(WURZEL, "dist")), "dist/ blieb nach abgebrochenem Produktions-Build liegen"
    lauf("python3", "scripts/firmendaten.py")

@pruefung("Interne Links und Anker in dist/web führen zu existierenden Zielen")
def t_links():
    basis = os.path.join(WURZEL, "dist", "web")
    alle = {os.path.normpath(p): s for _, p, s in seiten(basis)}
    kaputt = []
    for rel, p, s in seiten(basis):
        for href in s.links:
            if re.match(r"^(https?:|mailto:|tel:|#$)", href) or href.startswith("{{"):
                continue
            ziel, anker = ziel_aufloesen(basis, p, href)
            if not os.path.exists(ziel):
                kaputt.append("%s → %s" % (rel, href)); continue
            if anker and ziel.endswith(".html") and anker not in alle.get(os.path.normpath(ziel), Seite()).ids:
                kaputt.append("%s → %s (Anker fehlt)" % (rel, href))
        for res in s.ressourcen:
            if res.startswith("http"):
                kaputt.append("%s lädt externe Ressource %s" % (rel, res)); continue
            if not os.path.exists(ziel_aufloesen(basis, p, res)[0]):
                kaputt.append("%s → Ressource %s fehlt" % (rel, res))
    assert not kaputt, "%d Probleme: %s" % (len(kaputt), "; ".join(kaputt[:8]))

@pruefung("Seitengrundlagen: lang, Titel, Beschreibung, genau eine H1, Canonical, Überschriftenfolge")
def t_grundlagen():
    basis = os.path.join(WURZEL, "web")
    titel, beschr, probleme = {}, {}, []
    for rel, p, s in seiten(basis):
        if s.lang != "de": probleme.append("%s: lang fehlt" % rel)
        if not s.title.strip(): probleme.append("%s: Titel fehlt" % rel)
        if len(s.title) > 75: hinweise.append("%s: Titel länger als 75 Zeichen (%d)" % (rel, len(s.title)))
        d = s.meta.get("description", "")
        if not d: probleme.append("%s: Beschreibung fehlt" % rel)
        if s.h.count(1) != 1: probleme.append("%s: %d H1" % (rel, s.h.count(1)))
        for a, b in zip(s.h, s.h[1:]):
            if b > a + 1: probleme.append("%s: Überschrift springt von h%d auf h%d" % (rel, a, b)); break
        if rel != "404.html" and not s.canonical: probleme.append("%s: Canonical fehlt" % rel)
        titel.setdefault(s.title, []).append(rel); beschr.setdefault(d, []).append(rel)
        for img in s.imgs:
            if "alt" not in img: probleme.append("%s: Bild ohne alt" % rel)
            if not (img.get("width") and img.get("height")): probleme.append("%s: Bild ohne feste Maße" % rel)
    doppelt = [v for v in titel.values() if len(v) > 1] + [v for v in beschr.values() if len(v) > 1]
    if doppelt: probleme.append("doppelte Titel/Beschreibungen: %s" % doppelt)
    assert not probleme, "; ".join(probleme[:10])

@pruefung("Keine Inline-Stile und keine Inline-Skripte (Voraussetzung für die CSP)")
def t_csp():
    funde = []
    for rel, p, _ in seiten(os.path.join(WURZEL, "web")):
        roh = io.open(p, encoding="utf-8").read()
        if re.search(r'\sstyle="', roh): funde.append("%s: style-Attribut" % rel)
        for m in re.finditer(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>", roh):
            funde.append("%s: Inline-Skript" % rel)
        if re.search(r"\son[a-z]+=\"", roh): funde.append("%s: Inline-Eventhandler" % rel)
    assert not funde, "; ".join(funde[:8])

@pruefung("Vorschau-Markierung sperrt Suchmaschinen")
def t_vorschau():
    tmp = tempfile.mkdtemp()
    try:
        ziel = os.path.join(tmp, "web"); shutil.copytree(os.path.join(WURZEL, "dist", "web"), ziel)
        lauf("python3", "scripts/vorschau-markieren.py", ziel)
        robots = io.open(os.path.join(ziel, "robots.txt"), encoding="utf-8").read()
        assert "Disallow: /" in robots, "robots.txt nicht gesperrt"
        ohne = [rel for rel, p, s in seiten(ziel) if "noindex" not in s.meta.get("robots", "")]
        assert not ohne, "Seiten ohne noindex: %s" % ohne
        assert not os.path.exists(os.path.join(ziel, "sitemap.xml")), "Sitemap in der Vorschau"
    finally:
        shutil.rmtree(tmp)

@pruefung("Produktiv-Konfiguration ist indexierbar (robots, Sitemap, kein noindex auf Inhaltsseiten)")
def t_indexierbar():
    basis = os.path.join(WURZEL, "web")
    robots = io.open(os.path.join(basis, "robots.txt"), encoding="utf-8").read()
    assert "Allow: /" in robots and "Sitemap:" in robots, "robots.txt der Produktion fehlerhaft"
    sitemap = io.open(os.path.join(basis, "sitemap.xml"), encoding="utf-8").read()
    for rel, p, s in seiten(basis):
        noindex = "noindex" in s.meta.get("robots", "")
        if rel in ("404.html", "kontakt/danke/index.html"):
            assert noindex, "%s sollte noindex sein" % rel
        else:
            assert not noindex, "%s ist fälschlich noindex" % rel
            url = "https://{{DOMAIN}}/" + rel.replace("index.html", "")
            assert url in sitemap, "%s fehlt in der Sitemap" % rel

@pruefung("Keine Beispielprojekte und keine Platzhalterbilder im Standard-Build")
def t_keine_entwuerfe():
    basis = os.path.join(WURZEL, "web")
    assert not os.path.exists(os.path.join(basis, "assets/bilder/platzhalter")), "Platzhalterbilder im Build"
    for rel, p, _ in seiten(basis):
        assert "Beispieldaten" not in io.open(p, encoding="utf-8").read(), "Beispieldaten in %s" % rel

@pruefung("Keine Geheimnisse oder privaten Daten im Repository-Stand")
def t_geheimnisse():
    r = subprocess.run(["git", "ls-files"], cwd=WURZEL, capture_output=True, text=True)
    verboten = [f for f in r.stdout.splitlines() if re.search(r"(firmendaten\.privat\.env|konfiguration\.php$|gashini-konfiguration)", f)]
    assert not verboten, "private Dateien eingecheckt: %s" % verboten
    muster = re.compile(r"(DE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2}|passwort'\s*=>\s*'[^']+'|BEGIN (RSA|OPENSSH) PRIVATE KEY)")
    funde = []
    for f in r.stdout.splitlines():
        if f.endswith((".woff2", ".webp", ".png", ".jpg")) or not os.path.isfile(os.path.join(WURZEL, f)): continue
        try: text = io.open(os.path.join(WURZEL, f), encoding="utf-8").read()
        except UnicodeDecodeError: continue
        if muster.search(text): funde.append(f)
    assert not funde, "verdächtige Inhalte in: %s" % funde

@pruefung("Vorschau-Blöcke entfallen in Produktion, offene Angaben sind in der Vorschau markiert")
def t_vorschau_bloecke():
    sys.path.insert(0, os.path.join(WURZEL, "scripts"))
    import importlib
    fd = importlib.import_module("firmendaten")
    probe = '<title>X {{ORT}}</title><p>in {{ORT}}</p><a href="tel:{{TEL}}">{{TEL}}</a><!--vorschau--><p class="fotobriefing-notiz">B</p><!--/vorschau-->'
    werte = {"ORT": "[Ort]", "TEL": "0123"}
    fd.PRODUKTION = False
    v = fd.einsetzen(probe, werte, True)
    assert '<span class="angabe-offen"' in v and ">Ort</span>" in v, "Vorschau markiert offene Angaben nicht"
    assert "<title>X [Ort]</title>" in v, "Platzhalter im Titel darf nicht als HTML markiert werden"
    assert "fotobriefing-notiz" in v, "Fotobriefing fehlt in der Vorschau"
    fd.PRODUKTION = True
    pr = fd.einsetzen(probe, werte, True)
    assert "fotobriefing-notiz" not in pr and "<!--vorschau" not in pr, "Fotobriefing bleibt im Produktions-Build"
    assert "angabe-offen" not in pr, "Produktion darf keine Vorschau-Markierung enthalten"

@pruefung("Motion- und 3D-Dateien vorhanden, CSP-tauglich (kein eval), Rückfall-Zeichnung im Markup")
def t_bewegung():
    js = os.path.join(WURZEL, "web", "assets", "js")
    for f in ("bewegung.js", "wandaufbau.js", "vendor/gsap.min.js", "vendor/ScrollTrigger.min.js", "vendor/SplitText.min.js",
              "vendor/DrawSVGPlugin.min.js", "vendor/Flip.min.js", "vendor/LIZENZEN.txt"):
        assert os.path.isfile(os.path.join(js, f)), "fehlt: " + f
    for f in ("bewegung.js", "wandaufbau.js", "site.js", "vendor/gsap.min.js", "vendor/ScrollTrigger.min.js", "vendor/SplitText.min.js", "vendor/Flip.min.js"):
        roh = io.open(os.path.join(js, f), encoding="utf-8").read()
        assert not re.search(r"\beval\(|new Function\(", roh), "eval/new Function in " + f
    start = io.open(os.path.join(WURZEL, "web", "index.html"), encoding="utf-8").read()
    assert "data-wandaufbau" in start and 'class="wandaufbau-rueckfall"' in start and "zg--explosion" in start, "Wandaufbau ohne Rückfall-Zeichnung"
    impressum = io.open(os.path.join(WURZEL, "web", "impressum", "index.html"), encoding="utf-8").read()
    assert "gsap.min.js" not in impressum and "wandaufbau.js" not in impressum, "Rechtstexte laden unnötig Bewegungsskripte"

@pruefung("Bildherkunft dokumentiert, keine KI-Bilder als Projektfotos, Symbolbilder gekennzeichnet")
def t_bildherkunft():
    for ordner in ("visualisierung", "symbol"):
        herkunft = os.path.join(WURZEL, "src", "assets", "bilder", ordner, "HERKUNFT.md")
        assert os.path.isfile(herkunft), "HERKUNFT.md fehlt in " + ordner
        text = io.open(herkunft, encoding="utf-8").read()
        for f in os.listdir(os.path.dirname(herkunft)):
            if f.endswith(".webp"):
                assert re.sub(r"-\d+\.webp$", "", f) in text, "Herkunft nicht dokumentiert: " + f
    import json
    for p in json.load(io.open(os.path.join(WURZEL, "data", "projekte.json"), encoding="utf-8"))["projekte"]:
        for b in p.get("bilder", []):
            assert not b["datei"].startswith(("visualisierung/", "symbol/")), "Visualisierung oder Symbolbild als Projektbild: %s" % p["id"]
    # Jedes Symbolbild im Build: Alt-Text beginnt mit „Symbolbild“, sichtbare Marke folgt; nie auf „Über uns“
    web = os.path.join(WURZEL, "web")
    for rel, pfad, _ in seiten(web):
        html = io.open(pfad, encoding="utf-8").read()
        for m in re.finditer(r'<img src="[^"]*assets/bilder/symbol/[^"]*"[^>]*>', html):
            assert re.search(r'alt="Symbolbild: ', m.group(0)), "Symbolbild ohne Kennzeichnung im Alt-Text: " + rel
            assert html[m.end():].startswith('<span class="bild-marke"'), "Symbolbild ohne sichtbare Marke: " + rel
        if rel.startswith("ueber-uns"):
            assert "assets/bilder/symbol/" not in html, "Symbolbild auf „Über uns“"

@pruefung("Bewegtbilder: stumm, ohne Autoplay-Attribut, über einem gekennzeichneten Standbild; Hinweis „Video geplant“ nur in der Vorschau")
def t_bewegtbilder():
    web = os.path.join(WURZEL, "web")
    for rel, pfad, _ in seiten(web):
        html = io.open(pfad, encoding="utf-8").read()
        for m in re.finditer(r"<video\b[^>]*>(.*?)</video>", html, re.S):
            tag = m.group(0)[:m.group(0).index(">") + 1]
            for pflicht in ("muted", "loop", "playsinline", 'preload="none"', 'aria-hidden="true"', "data-bewegtbild"):
                assert pflicht in tag, "Video ohne %s: %s" % (pflicht, rel)
            assert "autoplay" not in tag and "controls" not in tag, "Video startet selbst oder zeigt Bedienelemente: " + rel
            assert html[:m.start()].rstrip().endswith('<span class="bild-marke" aria-hidden="true">Symbolbild</span>'), \
                "Video ohne Standbild mit Marke davor: " + rel
            for src in re.findall(r'<source src="([^"]+)"', m.group(1)):
                assert os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(pfad), src))), "Videodatei fehlt: " + src
        ohne = re.sub(r"<!--vorschau-->.*?<!--/vorschau-->", "", html, flags=re.S)
        assert "video-geplant" not in ohne, "Hinweis „Video geplant“ außerhalb eines Vorschau-Blocks: " + rel

@pruefung("Marke: Logos aus dem Logo-Paket (gleiche Maße), Hausfarben statt Ziegelrot, Archivo als einzige Schrift")
def t_marke():
    web = os.path.join(WURZEL, "web")
    paket = {"logo-hauptvariante-klein.svg": "svg/logo-hauptvariante-klein.svg", "logo-hauptvariante-negativ.svg": "svg/logo-hauptvariante-negativ.svg",
             "logo-kompakt.svg": "svg/logo-kompakt.svg", "signet.svg": "svg/signet.svg", "favicon.svg": "svg/favicon.svg"}
    for ziel, quelle in paket.items():
        a = io.open(os.path.join(WURZEL, "brand", quelle), encoding="utf-8").read()
        b = io.open(os.path.join(web, "assets", "marke", ziel), encoding="utf-8").read()
        assert re.search(r'viewBox="([^"]+)"', a).group(1) == re.search(r'viewBox="([^"]+)"', b).group(1), "Logo-Maße verändert: " + ziel
        assert re.findall(r'fill="(#[0-9A-Fa-f]{6})"', a) == re.findall(r'fill="(#[0-9A-Fa-f]{6})"', b), "Logo-Farben verändert: " + ziel
        assert len(re.findall(r"<path", a)) == len(re.findall(r"<path", b)), "Logo-Pfade verändert: " + ziel
    assert os.path.isfile(os.path.join(web, "favicon.ico")), "favicon.ico fehlt im Wurzelverzeichnis"
    css = io.open(os.path.join(web, "assets", "css", "site.css"), encoding="utf-8").read()
    for alt in ("#B5391C", "#8E2A12", "Instrument Sans", "IBM Plex"):
        assert alt.lower() not in css.lower(), "Alte CI im Stylesheet: " + alt
    for farbe in ("#1E2124", "#FFC93C", "#F4F2ED"):
        assert farbe.lower() in css.lower(), "Hausfarbe fehlt: " + farbe
    schriften = sorted(f for f in os.listdir(os.path.join(web, "assets", "fonts")) if f.endswith(".woff2"))
    assert schriften == ["archivo-var.woff2"], "Unerwartete Schriftdateien: %s" % schriften
    for rel, pfad, _ in seiten(web):
        html = io.open(pfad, encoding="utf-8").read()
        if 'class="kopf"' in html:
            assert "marke/logo-hauptvariante-klein.svg" in html and "marke/logo-kompakt.svg" in html, "Kopf ohne Logo-Varianten: " + rel
        if 'class="fuss"' in html:
            assert "marke/logo-hauptvariante-negativ.svg" in html, "Fuß ohne Negativ-Logo: " + rel

def main():
    for t in (t_wiederholbar, t_drift, t_zusammenspiel, t_produktion_sperrt, t_links, t_grundlagen,
              t_csp, t_vorschau, t_indexierbar, t_keine_entwuerfe, t_geheimnisse, t_vorschau_bloecke, t_bewegung, t_bildherkunft, t_bewegtbilder, t_marke):
        t()
    for b in bestanden: print("  ✓", b)
    for h in hinweise: print("  ·", h)
    for f in fehler: print("  ✗", f)
    print("\n%d bestanden, %d fehlgeschlagen" % (len(bestanden), len(fehler)))
    sys.exit(1 if fehler else 0)

if __name__ == "__main__":
    main()
