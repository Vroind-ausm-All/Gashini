# Deployment

## Überblick

```
src/ + data/ + brand/ ──► scripts/build-site.py ──► web/          (generiert, eingecheckt, CI prüft Drift)
                                                     │
data/firmendaten*.env ──► scripts/firmendaten.py ───►  dist/web/  (Vorschau oder Produktion)
                                                     │
                          scripts/vorschau-markieren.py ► noindex + gesperrte robots.txt (nur Vorschau)
```

| | Vorschau | Produktion |
|---|---|---|
| Befehl | `python3 scripts/firmendaten.py` | `python3 scripts/firmendaten.py --produktion` |
| Offene Angaben | sichtbar in `[eckigen Klammern]` | **Abbruch**, `dist/` wird gelöscht |
| Suchmaschinen | `vorschau-markieren.py`: `noindex` je Seite, `Disallow: /` | indexierbar, Sitemap, `Disallow: /api/` |
| Beispielprojekte | nur mit `ENTWUERFE=1` beim Generator | **Abbruch**, falls enthalten |
| Ort | GitHub Pages (automatisch aus dem Hauptzweig) | eigener Webspace |

GitHub Pages kann kein PHP ausführen – **in der Vorschau funktioniert das Formular nicht** und meldet das sichtbar.

## Anforderungen an den Webspace

- Apache mit `mod_rewrite`, `mod_headers`, `mod_expires` (bei anderem Server: Abschnitt „nginx“)
- PHP ≥ 8.1 mit `mbstring` und `fileinfo`; Datei-Uploads erlaubt (`file_uploads = On`). Die Grenzen für Fotos setzt `api/.user.ini` (PHP-FPM/CGI) bzw. `api/.htaccess` (mod_php): `upload_max_filesize = 8M`, `post_max_size = 14M`. Greifen beide nicht, beim Hoster einstellen.
- Mailversand: Postfach mit SMTP-Zugang (empfohlen) **oder** funktionierendes PHP-`mail()` mit Absender der eigenen Domain
- HTTPS-Zertifikat (bei deutschen Hostern meist kostenlos über Let's Encrypt)
- Verarbeitung in der EU, Auftragsverarbeitungsvertrag verfügbar

## Erstveröffentlichung – Schritt für Schritt

1. **Daten eintragen:** `data/firmendaten.env` vollständig ausfüllen, Werte ohne eckige Klammern.
   Private Werte (Bank, Steuernummer) nur in `data/firmendaten.privat.env` – nicht einchecken.
2. **Bauen:**
   ```
   python3 scripts/build-site.py
   python3 scripts/firmendaten.py --produktion
   ```
   Läuft das ohne Fehlermeldung durch, liegt der fertige Auftritt in `dist/web/`.
3. **Hochladen:** den **Inhalt** von `dist/web/` in das Wurzelverzeichnis der Domain (nicht den Ordner selbst).
   Versteckte Dateien (`.htaccess`, `api/.htaccess`) mit übertragen – im FTP-Programm „versteckte Dateien anzeigen“.
4. **Formular einrichten:**
   - `src/api/konfiguration.beispiel.php` kopieren nach `gashini-konfiguration.php` **eine Ebene über** dem
     Web-Verzeichnis (dort ist sie von außen nicht abrufbar).
   - Empfänger, Absender, SMTP-Zugang eintragen.
   - Geheimnis erzeugen: `php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'`
   - Prüfen: `https://<domain>/api/anfrage.php` im Browser aufrufen → erwartet ist „Diese Adresse nimmt nur
     Formularübermittlungen an“ (HTTP 405). Steht dort „noch nicht eingerichtet“, wird die Konfiguration nicht gefunden.
5. **Ende-zu-Ende-Test:** echte Anfrage über die Kontaktseite senden. Erst wenn sie im Postfach angekommen ist, gilt das
   Formular als funktionierend. Auch den Spam-Ordner prüfen.
6. **Header prüfen:** `curl -sI https://<domain>/ | grep -iE 'content-security|strict-transport|x-content'`
7. **Search Console** einrichten, Sitemap `https://<domain>/sitemap.xml` einreichen.

## Aktualisieren

Jede Änderung an Texten, Projekten oder Daten:
```
python3 scripts/build-site.py
python3 tests/pruefen.py
python3 scripts/firmendaten.py --produktion
```
dann `dist/web/` hochladen. Die Formular-Konfiguration außerhalb des Web-Verzeichnisses bleibt unberührt.

**Rückweg:** Jeder Stand ist in Git versioniert. Vorherigen Commit auschecken, dieselben drei Befehle, hochladen.

## Weiterleitungen alter Vorschau-Adressen

Stehen in `src/server/htaccess` (Apache). Es gab nie eine Live-Domain – die Weiterleitungen schützen nur bereits geteilte
Vorschau-Links.

| Alt | Neu |
|---|---|
| `/wohnungsuebergabe.html` | `/leistungen/hausmeisterservice/#mieterwechsel` |
| `/haushaltsaufloesung.html` | `/leistungen/` |
| `/preise.html` | `/fragen/#kosten` |
| `/ablauf/`, `/ablauf.html` | `/fragen/` |
| `/referenzen.html` | `/projekte/` |
| `/leistungen.html`, `/ueber-uns.html`, `/kontakt.html`, `/impressum.html`, `/datenschutz.html` | jeweilige Verzeichnis-URL |
| `/danke.html` | `/kontakt/danke/` |

## nginx (falls kein Apache)

```nginx
root /pfad/zu/web;
index index.html;
error_page 404 /404.html;

add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header X-Frame-Options "DENY" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()" always;
add_header Content-Security-Policy "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests" always;
add_header Strict-Transport-Security "max-age=31536000" always;

location ~ /\.            { deny all; }
location ~ \.(md|env|json|log|sh|py)$ { deny all; }
location /api/ {
    location = /api/anfrage.php { include fastcgi_params; fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name; fastcgi_pass unix:/run/php/php-fpm.sock; }
    return 404;
}
location ~* \.woff2$      { add_header Cache-Control "public, max-age=31536000, immutable"; }
location = /wohnungsuebergabe.html { return 301 /leistungen/hausmeisterservice/#mieterwechsel; }
# … weitere Weiterleitungen analog zur Tabelle oben
```

## Sicherheitshinweise

- `gashini-konfiguration.php` enthält das SMTP-Passwort: nie ins Repository, nie in das Web-Verzeichnis.
- HSTS ist bewusst ohne `includeSubDomains` gesetzt. Erst ergänzen, wenn alle Subdomains HTTPS sprechen.
- Das Verzeichnis für das Mengenlimit (`speicher_verzeichnis`) sollte außerhalb des Web-Verzeichnisses liegen.
- Abhängigkeiten der Website: keine. Die Testwerkzeuge (`tests/package.json`) werden nicht ausgeliefert.
