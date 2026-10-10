# Testbericht

Stand: Relaunch-Branch `claude/relaunch-premium`, Prüfung in der Entwicklungsumgebung
(Python 3.11, PHP 8.4, Chromium über Playwright 1.56, axe-core 4.11).

Vier Kategorien, streng getrennt: **automatisch getestet** · **manuell geprüft** · **nicht prüfbar** · **noch offen**.
Kein Ergebnis in diesem Dokument ist geschätzt oder hochgerechnet.

## 1. Automatisch getestet

Alle Tests liegen im Repository und laufen in GitHub Actions bei jedem Push.

### `tests/pruefen.py` – 11 von 11 bestanden

| Prüfung | Ergebnis |
|---|---|
| Build ist wiederholbar (zwei Läufe, byte-identische Ausgabe) | ✓ |
| `web/` entspricht dem Generator (in CI harte Prüfung) | ✓ |
| `build-site.py` und `firmendaten.py` arbeiten zusammen; keine unersetzten Platzhalter in `dist/` | ✓ |
| Produktions-Build bricht bei offenen Angaben ab und hinterlässt kein `dist/` | ✓ |
| Interne Links, Anker und Ressourcen in `dist/web` existieren; keine externen Ressourcen | ✓ |
| Je Seite: `lang="de"`, Titel, Beschreibung, genau eine H1, keine übersprungene Überschriftenebene, Canonical, eindeutige Titel und Beschreibungen, Bilder mit Alt-Text und festen Maßen | ✓ |
| Keine Inline-Stile, Inline-Skripte oder Event-Handler (Voraussetzung für die CSP) | ✓ |
| Vorschau-Markierung: `noindex` auf allen Seiten, `robots.txt` gesperrt, keine Sitemap | ✓ |
| Produktiv-Konfiguration: `robots.txt` erlaubt, alle Inhaltsseiten in der Sitemap, `noindex` nur auf Danke und 404 | ✓ |
| Keine Beispielprojekte, keine Platzhalterbilder im Standard-Build | ✓ |
| Keine privaten Dateien, IBAN-Muster, Passwörter oder Schlüssel im Repository | ✓ |

### `tests/formular_test.py` – 22 von 22 bestanden

Gegen einen echten `php -S`-Server; Mails werden als Datei abgelegt (Transport `datei`) bzw. an einen lokalen
SMTP-Empfänger geschickt.

| Prüfung | Ergebnis |
|---|---|
| Ohne Konfiguration: HTTP 503, Meldung „noch nicht eingerichtet“, keine Scheinannahme | ✓ |
| GET wird abgewiesen (405) | ✓ |
| Gültige Anfrage: 200, Vorgangsnummer, Weiterleitungsziel, genau eine Nachricht | ✓ |
| Nachricht enthält Vorhaben, `Reply-To`, RFC-2047-kodierten Betreff | ✓ |
| Pflichtfelder, „E-Mail oder Telefon“, Auswahlliste, Längenbegrenzung serverseitig | ✓ (4 Tests) |
| Header-Injection über E-Mail-Feld abgewiesen; Zeilenumbruch im Namen erzeugt keinen Mail-Kopf | ✓ (2 Tests) |
| Honigtopf und unplausibel schnelle Übermittlung: Antwort wie Erfolg, aber keine Nachricht | ✓ (2 Tests) |
| Fremde Herkunft 403, eigene/konfigurierte Herkunft 200 | ✓ (2 Tests) |
| Übergroße Anfrage 413 | ✓ |
| Ohne JavaScript: 303 zur Danke-Seite; bei Fehlern 422-Seite ohne ungeschützte Ausgabe von Eingaben | ✓ (2 Tests) |
| Antwort-Header `nosniff`, `no-store` | ✓ |
| Mengenlimit: vierte Anfrage im Fenster → 429; keine IP im Klartext gespeichert | ✓ (2 Tests) |
| SMTP-Versand: Nachricht kommt beim lokalen Mailserver an | ✓ – **ohne TLS und ohne Anmeldung** |
| SMTP nicht erreichbar: 502, keine Erfolgsmeldung | ✓ |

### `tests/e2e.mjs` – 22 von 22 bestanden

| Prüfung | Ergebnis |
|---|---|
| Kein waagerechter Überlauf auf 13 Seiten bei 320, 375, 768, 1024, 1440 px | ✓ (5 Tests) |
| Textvergrößerung 200 % bei 375 px ohne Überlauf | ✓ |
| axe-core (WCAG 2.0/2.1/2.2 A+AA, Best Practices) auf 13 Seiten bei 1440 und 375 px | ✓ **0 Funde** jeder Schwere |
| Erster Tab-Halt ist der Sprunglink; Enter setzt den Fokus auf den Inhalt | ✓ |
| Fokus bei Tastaturbedienung sichtbar (Outline ≥ 2 px) | ✓ |
| Mobilmenü per Tastatur: öffnen, Fokus im Menü, Escape schließt, Fokus zurück | ✓ |
| Formular: leeres Absenden → Feldfehler mit `aria-invalid`, `aria-describedby`, Fokus auf erstem Fehler, Zusammenfassung | ✓ (2 Tests) |
| Formular: erfolgreiche Anfrage → Danke-Seite mit Vorgangsnummer | ✓ |
| Formular: Doppelklick → genau eine Nachricht | ✓ |
| Formular: Serverfehler → Meldung, Eingaben erhalten, Knopf wieder aktiv, keine Weiterleitung | ✓ |
| Ohne JavaScript: Inhalt und Navigation sichtbar; Formular wird angenommen | ✓ (2 Tests) |
| „Bewegung reduzieren“: Zeichnung ohne Animation, sofort vollständig | ✓ |
| Entwurfs-Build: Projektkarten gekennzeichnet; Vorher/Nachher-Regler; Bildansicht per Tastatur inkl. Fokus-Rückgabe | ✓ (3 Tests) |

## 2. Manuell geprüft

| Prüfung | Ergebnis |
|---|---|
| Sichtprüfung Startseite 1440 px und 375 px, Kontaktseite, Trockenbau, Projektdetail | Hierarchie, Raster und Abstände wie geplant. Dabei gefunden und behoben: Beschriftung „Mineralwolle“ lief aus der Zeichnung; Zeichnung zeigte zunächst zwei Platten statt einer – fachlich falsch, korrigiert |
| Technische Zeichnung fachlich | Achsabstand 625 mm bei 1250 mm Plattenbreite, Platte auf drei Ständern verschraubt, UW oben/unten, CW 75, GKB 12,5 mm – plausibel für eine einfach beplankte Metallständerwand. Schematisch, nicht maßstäblich |
| Ladeverhalten (Labormessung, **kein Lighthouse**) | Chromium, 375 px, Netz 1,6 Mbit/s bei 150 ms Latenz, CPU 4× gedrosselt, Cache aus, Median aus 3 Läufen, **ohne** Serverkompression: LCP 1,04–1,11 s, CLS 0 auf Start, Trockenbau, Kontakt. Übertragung ≈ 165–173 KB je Seite, davon 87 KB Schriften |
| Gewicht | HTML+CSS+JS der Startseite gzip-komprimiert 15,9 KB; kein Framework, zwei kleine Skripte |
| E-Mail-Inhalt | Beispielmail gesichtet: Klartext, alle Felder, Vorgangsnummer im Betreff, Löschhinweis im Fuß |

## 3. Nicht prüfbar in dieser Umgebung

| Was | Warum |
|---|---|
| Tatsächliche Zustellung an ein echtes Postfach | kein Mailserver, keine Zugangsdaten; nur lokal simuliert |
| SMTP mit STARTTLS/SSL und Anmeldung | Testserver ohne TLS; der Code-Pfad ist geschrieben, aber nicht ausgeführt |
| `.htaccess`: Sicherheits-Header, CSP, HTTPS-Weiterleitung, 301-Umleitungen | `php -S` wertet `.htaccess` nicht aus; erfordert Apache |
| Lighthouse-Wert | nicht ausgeführt; siehe Labormessung oben |
| INP | erfordert echte Nutzerinteraktion im Feld |
| Screenreader (NVDA, VoiceOver, TalkBack) | nicht verfügbar; axe-core ersetzt keine Prüfung mit Hilfsmitteln |
| Safari / iOS, Firefox | nur Chromium getestet |
| GitHub-Pages-Vorschau | Zugriff auf `github.io` aus dieser Umgebung gesperrt |

## 4. Noch offen

| Punkt | Wer | Blockiert Livegang? |
|---|---|---|
| Firmendaten, Ort, Einsatzgebiet, Domain | Betreiber | **ja** – Produktions-Build bricht ab |
| Freigabemarkierungen auf 6 Seiten (Leistungsumfang, Netzwerk, Erreichbarkeit) | Betreiber | **ja** |
| Hoster wählen, Formular-Konfiguration anlegen, **Testanfrage über das Live-Formular** | Betreiber | **ja** – bis dahin meldet das Formular „noch nicht eingerichtet“ |
| Header und Weiterleitungen auf dem Live-Server prüfen (`docs/DEPLOYMENT.md`, Schritt 6) | Betreiber/Technik | ja |
| Gewerberechtliche Klärung (`docs/LEGAL-CHECKLIST.md`, Abschnitt 3) | Betreiber + Kammer | ja |
| Echte Projekte mit Freigabe | Betreiber | nein – Galerie zeigt ehrlichen Leerzustand |
| Screenreader-Test mit NVDA oder VoiceOver | Technik | nein, empfohlen |
| Test in Safari und Firefox | Technik | nein, empfohlen |
| Lizenz der Holztexturen | Betreiber | nein – Texturen werden nicht verwendet |

## Tests selbst ausführen

```
python3 scripts/build-site.py
python3 tests/pruefen.py
python3 scripts/firmendaten.py && python3 tests/formular_test.py
cd tests && npm ci && node e2e.mjs        # CHROMIUM_PFAD=… falls kein Playwright-Browser installiert ist
```
