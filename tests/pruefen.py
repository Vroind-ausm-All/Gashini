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

def main():
    for t in (t_wiederholbar, t_drift, t_zusammenspiel, t_produktion_sperrt, t_links, t_grundlagen,
              t_csp, t_vorschau, t_indexierbar, t_keine_entwuerfe, t_geheimnisse):
        t()
    for b in bestanden: print("  ✓", b)
    for h in hinweise: print("  ·", h)
    for f in fehler: print("  ✗", f)
    print("\n%d bestanden, %d fehlgeschlagen" % (len(bestanden), len(fehler)))
    sys.exit(1 if fehler else 0)

if __name__ == "__main__":
    main()
