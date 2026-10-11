#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setzt die Firmendaten in den erzeugten Auftritt ein und legt dist/ an.

  python3 scripts/firmendaten.py               Vorschau: offene Angaben bleiben sichtbar
  python3 scripts/firmendaten.py --produktion  Produktion: bricht bei jeder offenen Angabe ab

Liest data/firmendaten.env und – falls vorhanden – data/firmendaten.privat.env.
Quelle ist web/ (vorher scripts/build-site.py ausführen) sowie print/ und brand/.

Regeln
- {{SCHLUESSEL}} wird ersetzt; in HTML mit HTML-Maskierung, in JSON-LD JSON-maskiert.
- <!--opt:SCHLUESSEL-->…<!--/opt:SCHLUESSEL--> entfällt, wenn der Wert leer ist.
- Werte in [eckigen Klammern] gelten als nicht bestätigt.
- <!--@jsonld-firma--> wird durch strukturierte Daten aus bestätigten Werten ersetzt.
- <!--vorschau-->…<!--/vorschau--> (Fotobriefings) bleibt in der Vorschau und entfällt in Produktion.
- In der Vorschau erscheinen nicht bestätigte Werte im Fließtext als <span class="angabe-offen"> ohne Klammern;
  in Attributen, Titeln und Skripten bleiben sie unverändert.
"""
import html, io, json, os, re, shutil, sys

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST = os.path.join(WURZEL, "dist")
PRODUKTION = "--produktion" in sys.argv

PFLICHT = ["INHABER", "STRASSE", "PLZ", "ORT", "PLZ_ORT", "REGION", "EINSATZGEBIET", "TELEFON", "TELEFON_LINK",
           "TELEFONZEITEN", "EMAIL", "DOMAIN", "INHABER_TEXT", "VERSICHERUNG_ANTWORT", "BILDNACHWEIS", "HOSTER",
           "LOG_SPEICHERDAUER", "MAILVERSAND", "ANFRAGE_SPEICHERDAUER", "DRITTLAND_HINWEIS", "AUFSICHTSBEHOERDE",
           "STAND_DATUM", "STAND_ISO"]
BEISPIELWERTE = re.compile(r"example\.(de|com|org)|ihre-domain|0000000|Musterstadt|Max Mustermann", re.I)

def env_lesen(pfad):
    werte = {}
    if not os.path.exists(pfad):
        return werte
    for zeile in io.open(pfad, encoding="utf-8"):
        m = re.match(r'^\s*([A-Z0-9_]+)\s*=\s*"(.*)"\s*(#.*)?$', zeile.rstrip("\n"))
        if not m:
            m = re.match(r"^\s*([A-Z0-9_]+)\s*=\s*([^#\s]*)\s*(#.*)?$", zeile.rstrip("\n"))
        if m:
            werte[m.group(1)] = m.group(2)
    return werte

def unbestaetigt(wert):
    return wert.startswith("[") and wert.endswith("]")

def jsonld_firma(w):
    ok = lambda k: w.get(k) and not unbestaetigt(w[k])
    if not ok("DOMAIN"):
        return ""
    d = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
         "@id": "https://%s/#firma" % w["DOMAIN"], "name": "Gashini Dienstleistungen",
         "url": "https://%s/" % w["DOMAIN"], "image": "https://%s/assets/marke/logo.svg" % w["DOMAIN"],
         "description": "Trockenbau, Hausmeisterservice sowie Reparatur und Instandhaltung rund um Immobilien."}
    if ok("TELEFON"): d["telephone"] = w["TELEFON"]
    if ok("EMAIL"): d["email"] = w["EMAIL"]
    if ok("STRASSE") and ok("PLZ") and ok("ORT"):
        d["address"] = {"@type": "PostalAddress", "streetAddress": w["STRASSE"], "postalCode": w["PLZ"],
                        "addressLocality": w["ORT"], "addressCountry": "DE"}
    if ok("EINSATZGEBIET"): d["areaServed"] = w["EINSATZGEBIET"]
    if ok("INHABER"): d["founder"] = {"@type": "Person", "name": w["INHABER"]}
    gleich = [w[k] for k in ("MYHAMMER_URL", "GOOGLE_PROFIL_URL") if ok(k)]
    if gleich: d["sameAs"] = gleich
    return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)

ROHTEXT = ("title", "script", "style", "textarea", "option")

def text_einsetzen(teil, werte):
    """Platzhalter im sichtbaren Text: nicht bestätigte Werte in der Vorschau als markierte Spanne."""
    def ersetzen(m):
        if m.group(1) not in werte:
            return m.group(0)
        wert = werte[m.group(1)]
        if not PRODUKTION and unbestaetigt(wert):
            return '<span class="angabe-offen" title="Angabe noch nicht bestätigt">%s</span>' % html.escape(wert[1:-1], quote=True)
        return html.escape(wert, quote=True)
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", ersetzen, teil)

def html_einsetzen(teil, werte):
    """Trennt Tags und Text; ersetzt in Tags und Rohtext-Elementen unverändert, im übrigen Text markiert."""
    roh = lambda t: re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: html.escape(werte[m.group(1)], quote=True) if m.group(1) in werte else m.group(0), t)
    aus, im_roh = [], None
    for stueck in re.split(r"(<[^>]+>)", teil):
        if stueck.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", stueck)
            if m:
                name = m.group(2).lower()
                if not m.group(1) and name in ROHTEXT: im_roh = name
                elif m.group(1) and name == im_roh: im_roh = None
            aus.append(roh(stueck))
        else:
            aus.append(roh(stueck) if im_roh else text_einsetzen(stueck, werte))
    return "".join(aus)

def einsetzen(text, werte, ist_html):
    # optionale Blöcke
    def opt(m):
        return "" if not werte.get(m.group(1), "") else m.group(2)
    text = re.sub(r"<!--opt:([A-Z0-9_]+)-->(.*?)<!--/opt:\1-->", opt, text, flags=re.S)
    # Vorschau-Blöcke (Fotobriefings)
    text = re.sub(r"<!--vorschau-->(.*?)<!--/vorschau-->", "" if PRODUKTION else r"\1", text, flags=re.S)
    text = text.replace("<!--@jsonld-firma-->", jsonld_firma(werte))
    if not ist_html:
        return re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: werte.get(m.group(1), m.group(0)), text)
    # JSON-LD-Blöcke getrennt behandeln
    teile = re.split(r'(<script type="application/ld\+json">.*?</script>)', text, flags=re.S)
    aus = []
    for i, teil in enumerate(teile):
        if i % 2 == 1:
            aus.append(re.sub(r"\{\{([A-Z0-9_]+)\}\}",
                              lambda m: json.dumps(werte[m.group(1)], ensure_ascii=False)[1:-1] if m.group(1) in werte else m.group(0), teil))
        else:
            aus.append(html_einsetzen(teil, werte))
    return "".join(aus)

def main():
    if not os.path.isfile(os.path.join(WURZEL, "web", "index.html")):
        sys.exit("web/ fehlt – zuerst python3 scripts/build-site.py ausführen.")
    werte = env_lesen(os.path.join(WURZEL, "data", "firmendaten.env"))
    werte.update(env_lesen(os.path.join(WURZEL, "data", "firmendaten.privat.env")))

    probleme = []
    if PRODUKTION:
        for k in PFLICHT:
            if not werte.get(k) or unbestaetigt(werte[k]):
                probleme.append("Pflichtangabe offen: %s" % k)
        for k, v in werte.items():
            if v and BEISPIELWERTE.search(v):
                probleme.append("Beispielwert statt echter Angabe: %s" % k)
        if werte.get("TELEFON_LINK") and not re.fullmatch(r"\+?[0-9]{6,20}", werte["TELEFON_LINK"]):
            probleme.append("TELEFON_LINK darf nur + und Ziffern enthalten")
        if "[FREIGABE ERFORDERLICH" in werte.get("VERSICHERUNG_ANTWORT", ""):
            probleme.append("Pflichtangabe offen: VERSICHERUNG_ANTWORT")

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(WURZEL, "web"), os.path.join(DIST, "web"))
    shutil.copytree(os.path.join(WURZEL, "print"), os.path.join(DIST, "print"))
    shutil.copytree(os.path.join(WURZEL, "brand"), os.path.join(DIST, "brand"), ignore=shutil.ignore_patterns("material", "*.md", "*.txt"))

    offen = set()
    for root, _, dateien in os.walk(DIST):
        for f in dateien:
            if not f.endswith((".html", ".css", ".js", ".xml", ".txt", ".php", ".svg")) and f != ".htaccess":
                continue
            p = os.path.join(root, f)
            text = io.open(p, encoding="utf-8").read()
            neu = einsetzen(text, werte, f.endswith(".html"))
            if neu != text:
                io.open(p, "w", encoding="utf-8", newline="\n").write(neu)
            rel = os.path.relpath(p, DIST)
            for m in re.findall(r"\{\{[A-Z0-9_]+\}\}", neu):
                offen.add((rel, m))
            if rel.startswith("web") and PRODUKTION:
                if "[FREIGABE ERFORDERLICH" in neu: probleme.append("Redaktionelle Freigabe offen in %s" % rel)
                if 'class="redaktion"' in neu: probleme.append("Redaktionshinweis sichtbar in %s" % rel)
                if "Beispieldaten" in neu: probleme.append("Beispielprojekte im Build (ENTWUERFE=1?) in %s" % rel)
                if re.search(r'href="[^"]*/index\.html', neu): probleme.append("Vorschau-Linkstil im Build in %s" % rel)
                if 'name="robots" content="noindex' in neu and not rel.endswith(("danke/index.html", "404.html")):
                    probleme.append("noindex auf produktiver Seite %s" % rel)

    for rel, m in sorted(offen):
        probleme.append("Unbekannter Platzhalter %s in %s" % (m, rel))
    unbest = sorted({k for k, v in werte.items() if unbestaetigt(v)})

    print("dist/ erstellt (%s)." % ("Produktion" if PRODUKTION else "Vorschau"))
    if unbest and not PRODUKTION:
        print("Noch nicht bestätigt (%d): %s" % (len(unbest), ", ".join(unbest)))
    if probleme:
        print("\nNICHT VERÖFFENTLICHUNGSREIF – %d Punkt(e):" % len(probleme))
        for p in sorted(set(probleme)):
            print("  –", p)
        if PRODUKTION:
            shutil.rmtree(DIST)
            sys.exit(1)

if __name__ == "__main__":
    main()
