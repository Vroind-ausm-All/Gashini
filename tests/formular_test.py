#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests des Formular-Backends gegen einen echten PHP-Server.

  python3 tests/formular_test.py

Startet `php -S` auf dist/web mit einer Test-Konfiguration (Transport "datei":
Mails werden als .eml-Datei geschrieben statt versendet). Geprüft wird die
serverseitige Annahme – NICHT die tatsächliche Zustellung über einen Mailserver.
"""
import json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.parse, urllib.request, urllib.error

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WEB = os.path.join(WURZEL, "dist", "web")
ergebnisse = []

def freier_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

def server(konfig_pfad):
    port = freier_port()
    env = dict(os.environ, GASHINI_KONFIG=konfig_pfad)
    proc = subprocess.Popen(["php", "-S", "127.0.0.1:%d" % port, "-t", WEB], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=.2).close(); break
        except OSError:
            time.sleep(.1)
    return proc, "http://127.0.0.1:%d/api/anfrage.php" % port

def konfig(verz, **zusatz):
    k = {"empfaenger": "anfragen@test.invalid", "absender": "website@test.invalid", "transport": "datei",
         "datei_verzeichnis": os.path.join(verz, "post"), "speicher_verzeichnis": os.path.join(verz, "limit"),
         "geheimnis": "t" * 40, "erlaubte_herkunft": ["http://erlaubt.test"], "limit_pro_ip": 1000,
         "limit_gesamt_pro_stunde": 1000}
    k.update(zusatz)
    pfad = os.path.join(verz, "konfiguration-%d.php" % len(os.listdir(verz)))
    php = "<?php return " + json_to_php(k) + ";"
    open(pfad, "w").write(php)
    return pfad

def json_to_php(v):
    if isinstance(v, dict): return "[" + ",".join("%s=>%s" % (json_to_php(a), json_to_php(b)) for a, b in v.items()) + "]"
    if isinstance(v, list): return "[" + ",".join(json_to_php(x) for x in v) + "]"
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, int): return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"

class KeinRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
oeffner = urllib.request.build_opener(KeinRedirect)

def senden(url, daten, json_antwort=True, kopf=None, methode="POST"):
    body = urllib.parse.urlencode(daten).encode() if daten is not None else None
    req = urllib.request.Request(url, data=body, method=methode)
    if json_antwort: req.add_header("Accept", "application/json")
    for k, v in (kopf or {}).items(): req.add_header(k, v)
    try:
        r = oeffner.open(req, timeout=10); status, text, hdr = r.status, r.read().decode(), r.headers
    except urllib.error.HTTPError as e:
        status, text, hdr = e.code, e.read().decode(), e.headers
    return status, text, hdr

GUELTIG = {"name": "Erika Beispiel", "email": "erika@test.invalid", "telefon": "", "leistung": "Trockenbau & Innenausbau",
           "nachricht": "Wir möchten im Wohnzimmer eine Trennwand mit Tür einziehen lassen.", "ort": "12345",
           "zeitraum": "Frühjahr", "quelle": "Empfehlung", "webseite": "", "ausfuellzeit": "25"}


def smtp_testserver():
    """Minimaler SMTP-Empfänger (ohne TLS/AUTH) – prüft den SMTP-Dialog des Backends."""
    import warnings, threading
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import smtpd, asyncore
    empfangen = []
    class Empfaenger(smtpd.SMTPServer):
        def process_message(self, peer, von, an, daten, **kw):
            empfangen.append((von, an, daten.decode("utf-8", "replace") if isinstance(daten, bytes) else daten))
    port = freier_port()
    srv = Empfaenger(("127.0.0.1", port), None, decode_data=False)
    threading.Thread(target=asyncore.loop, kwargs={"timeout": .1}, daemon=True).start()
    return srv, port, empfangen

def pruefe(name, bedingung, detail=""):
    ergebnisse.append((name, bool(bedingung), detail))

def post_dateien(verz):
    p = os.path.join(verz, "post")
    return sorted(os.listdir(p)) if os.path.isdir(p) else []

def main():
    if not os.path.isfile(os.path.join(WEB, "api", "anfrage.php")):
        sys.exit("dist/web fehlt – zuerst build-site.py und firmendaten.py ausführen.")
    tmp = tempfile.mkdtemp()
    procs = []
    try:
        # --- ohne Konfiguration ---
        p, url = server(os.path.join(tmp, "gibt-es-nicht.php")); procs.append(p)
        s, t, _ = senden(url, GUELTIG)
        pruefe("Ohne Konfiguration: 503 und klare Meldung, keine Scheinannahme", s == 503 and json.loads(t)["ok"] is False, s)

        # --- Hauptserver ---
        haupt = konfig(tmp)
        p, url = server(haupt); procs.append(p)

        s, t, _ = senden(url, None, methode="GET")
        pruefe("GET wird mit 405 abgewiesen", s == 405, s)

        s, t, _ = senden(url, GUELTIG)
        j = json.loads(t)
        mails = post_dateien(tmp)
        pruefe("Gültige Anfrage: 200, ok, Vorgangsnummer, Weiterleitungsziel", s == 200 and j["ok"] and len(j["ref"]) == 8 and j["weiter"].startswith("../kontakt/danke/?ref="), t)
        pruefe("Gültige Anfrage erzeugt genau eine Nachricht", len(mails) == 1, mails)
        eml = open(os.path.join(tmp, "post", mails[0]), encoding="utf-8").read() if mails else ""
        pruefe("Nachricht enthält Vorhaben und Reply-To, Betreff kodiert", "Trennwand mit Tür" in eml and "Reply-To: <erika@test.invalid>" in eml and "=?UTF-8?B?" in eml.split("Subject:", 1)[1].split("From:", 1)[0])

        s, t, _ = senden(url, dict(GUELTIG, email="", telefon=""))
        j = json.loads(t)
        pruefe("Ohne E-Mail und Telefon: 422 mit Feldfehler", s == 422 and "email" in j.get("fehler", {}), t)

        s, t, _ = senden(url, dict(GUELTIG, name="", leistung="Gibt es nicht", nachricht="kurz"))
        j = json.loads(t)
        pruefe("Pflichtfelder und Auswahlliste werden serverseitig geprüft", s == 422 and {"name", "leistung", "nachricht"} <= set(j.get("fehler", {})), t)

        s, t, _ = senden(url, dict(GUELTIG, nachricht="x" * 4001))
        pruefe("Zu lange Beschreibung: 422", s == 422 and "nachricht" in json.loads(t).get("fehler", {}), s)

        vorher = len(post_dateien(tmp))
        s, t, _ = senden(url, dict(GUELTIG, email="opfer@test.invalid\r\nBcc: ziel@test.invalid"))
        pruefe("Header-Injection in E-Mail wird abgewiesen", s == 422 and len(post_dateien(tmp)) == vorher, s)

        s, t, _ = senden(url, dict(GUELTIG, name="Erika\r\nBcc: ziel@test.invalid", email="ok@test.invalid"))
        neu = [m for m in post_dateien(tmp)][-1]
        inhalt = open(os.path.join(tmp, "post", neu), encoding="utf-8").read()
        kopf = inhalt.split("\r\n\r\n", 1)[0]
        pruefe("Zeilenumbruch im Namen erzeugt keinen zusätzlichen Mail-Kopf", s == 200 and "\nBcc:" not in kopf, kopf[:200])

        vorher = len(post_dateien(tmp))
        s, t, _ = senden(url, dict(GUELTIG, webseite="https://spam.test"))
        pruefe("Honigtopf: Antwort wie Erfolg, aber keine Nachricht", s == 200 and json.loads(t)["ok"] and len(post_dateien(tmp)) == vorher, s)

        s, t, _ = senden(url, dict(GUELTIG, ausfuellzeit="1"))
        pruefe("Unplausibel schnelle Übermittlung: keine Nachricht", s == 200 and len(post_dateien(tmp)) == vorher, s)

        s, t, _ = senden(url, GUELTIG, kopf={"Origin": "https://fremd.test"})
        pruefe("Fremde Herkunft: 403", s == 403, s)
        s, t, _ = senden(url, GUELTIG, kopf={"Origin": "http://erlaubt.test"})
        pruefe("Erlaubte Herkunft: 200", s == 200, s)

        s, t, _ = senden(url, dict(GUELTIG, nachricht="y" * 21000))
        pruefe("Übergroße Anfrage: 413", s == 413, s)

        s, t, h = senden(url, GUELTIG, json_antwort=False)
        pruefe("Ohne JavaScript: 303 auf die Danke-Seite mit Vorgangsnummer", s == 303 and h.get("Location", "").startswith("../kontakt/danke/?ref="), (s, h.get("Location")))

        s, t, _ = senden(url, dict(GUELTIG, name="", email="<script>alert(1)</script>"), json_antwort=False)
        pruefe("Ohne JavaScript, fehlerhaft: 422-Seite, Eingaben nicht ungeschützt ausgegeben", s == 422 and "<script>alert" not in t and "nicht gesendet" in t, s)

        s, t, h = senden(url, GUELTIG)
        pruefe("Antwort trägt nosniff und no-store", h.get("X-Content-Type-Options") == "nosniff" and "no-store" in h.get("Cache-Control", ""), dict(h))

        # --- Mengenlimit ---
        eng = konfig(tmp, limit_pro_ip=3, speicher_verzeichnis=os.path.join(tmp, "limit2"))
        p, url2 = server(eng); procs.append(p)
        codes = [senden(url2, GUELTIG)[0] for _ in range(4)]
        pruefe("Mengenlimit: vierte Anfrage im Zeitfenster wird mit 429 abgewiesen", codes == [200, 200, 200, 429], codes)
        dateien = os.listdir(os.path.join(tmp, "limit2"))
        roh = "".join(open(os.path.join(tmp, "limit2", f)).read() for f in dateien)
        pruefe("Mengenlimit speichert keine IP-Adresse im Klartext", "127.0.0.1" not in roh and all("127" not in f for f in dateien), dateien)

        # --- SMTP-Dialog (ohne TLS und Anmeldung) ---
        try:
            srv, sport, empfangen = smtp_testserver()
            smtpk = konfig(tmp, transport="smtp", smtp={"host": "127.0.0.1", "port": sport, "sicherheit": "keine"},
                           speicher_verzeichnis=os.path.join(tmp, "limit4"))
            p, url4 = server(smtpk); procs.append(p)
            s, t, _ = senden(url4, GUELTIG)
            time.sleep(.3)
            pruefe("SMTP-Versand: Nachricht kommt beim Mailserver an (ohne TLS/Anmeldung getestet)",
                   s == 200 and len(empfangen) == 1 and empfangen[0][1] == ["anfragen@test.invalid"] and "Trennwand" in empfangen[0][2], (s, len(empfangen)))
            srv.close()
        except ImportError:
            ergebnisse.append(("SMTP-Versand (smtpd-Modul nicht verfügbar – nicht geprüft)", True, ""))

        # --- Zustellfehler ---
        kaputt = konfig(tmp, transport="smtp", smtp={"host": "127.0.0.1", "port": freier_port(), "sicherheit": "keine"},
                        speicher_verzeichnis=os.path.join(tmp, "limit3"))
        p, url3 = server(kaputt); procs.append(p)
        s, t, _ = senden(url3, GUELTIG)
        pruefe("Zustellfehler (SMTP nicht erreichbar): 502, keine Erfolgsmeldung", s == 502 and json.loads(t)["ok"] is False, s)
    finally:
        for p in procs: p.terminate()
        shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(1 for _, b, _ in ergebnisse if b)
    for name, b, detail in ergebnisse:
        print("  %s %s%s" % ("✓" if b else "✗", name, "" if b else "  → %s" % (detail,)))
    print("\n%d bestanden, %d fehlgeschlagen" % (ok, len(ergebnisse) - ok))
    sys.exit(0 if ok == len(ergebnisse) else 1)

if __name__ == "__main__":
    main()
