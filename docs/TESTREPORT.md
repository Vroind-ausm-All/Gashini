# Testbericht

Stand: 11.10.2026, Premium-Relaunch mit überarbeiteter Navigation auf `claude/relaunch-premium`. Geprüft in der Entwicklungsumgebung mit
Python 3.11, PHP 8.4, Node 22, Chromium über Playwright 1.56 und axe-core 4.11.

Vier Kategorien, streng getrennt: **automatisch getestet** · **manuell geprüft** · **nicht prüfbar** · **noch offen**.
Kein Ergebnis in diesem Dokument ist geschätzt oder hochgerechnet. Lighthouse wurde **nicht** ausgeführt; die
Leistungswerte unten stammen aus einer eigenen Labormessung und sind als solche gekennzeichnet.

## 1. Automatisch getestet

Alle Tests liegen im Repository und laufen in GitHub Actions bei jedem Push (`.github/workflows/vorschau.yml`).
Lokal liefen alle drei Suiten am 11.10.2026 (nach der Überarbeitung der Navigation) vollständig grün, ebenso auf
einem GitHub-Runner: Workflow-Lauf
[38099016382](https://github.com/Vroind-ausm-All/Gashini/actions/runs/38099016382) für Commit 6eddae7 – Jobs `pruefen`
(statische Prüfungen, Formular-Backend) und `browser` (Abgleich von 3D-Bündel und GSAP mit der Quelle, Browser-Tests)
erfolgreich.

### `tests/pruefen.py` – 15 von 15 bestanden

| Prüfung | Ergebnis |
|---|---|
| Build wiederholbar (byte-identisch), `web/` entspricht dem Generator | ✓ (2) |
| `firmendaten.py` und Generator arbeiten zusammen; Produktions-Build bricht bei offenen Angaben ab | ✓ (2) |
| Interne Links, Anker und Ressourcen existieren; keine externen Ressourcen | ✓ |
| Je Seite: `lang`, Titel, Beschreibung, genau eine H1, keine übersprungene Überschriftenebene, Canonical, eindeutige Titel, Bilder mit Alt-Text und festen Maßen | ✓ |
| Keine Inline-Stile, Inline-Skripte oder Event-Handler (Voraussetzung für die CSP) | ✓ |
| Vorschau gesperrt (`noindex`, `robots.txt`), Produktion indexierbar | ✓ (2) |
| Keine Beispielprojekte und Platzhalterbilder im Standard-Build; keine privaten Daten im Repository | ✓ (2) |
| **neu:** Vorschau-Blöcke (Fotobriefings) entfallen in Produktion; offene Angaben erscheinen in der Vorschau als markierte Spanne, nie im Seitentitel | ✓ |
| **neu:** GSAP-Dateien, Bewegungsskript und 3D-Bündel vorhanden, ohne `eval`/`new Function` (CSP); Wandaufbau hat eine Zeichnung als Rückfall; Rechtstexte laden keine Bewegungsskripte | ✓ |
| **neu:** Kurzvideos: stumm, ohne `autoplay`-Attribut und ohne Bedienleiste, immer über einem gekennzeichneten Standbild, Videodateien vorhanden; Hinweis „Video geplant“ nur in Vorschau-Blöcken | ✓ |
| **neu:** Herkunft jeder Visualisierung und jedes Symbolbilds dokumentiert; keine davon als Projektbild; Symbolbilder im Build mit Alt-Text „Symbolbild: …“ und sichtbarer Marke, nie auf „Über uns“ | ✓ |

### `tests/formular_test.py` – 30 von 30 bestanden

Gegen einen echten `php -S`-Server; Mails werden als Datei abgelegt bzw. an einen lokalen SMTP-Empfänger geschickt.

| Prüfung | Ergebnis |
|---|---|
| Ohne Konfiguration 503, GET 405, gültige Anfrage 200 mit Vorgangsnummer und genau einer Nachricht | ✓ (4) |
| Nachricht mit Vorhaben, `Reply-To`, kodiertem Betreff | ✓ |
| Pflichtfelder, „E-Mail oder Telefon“, Auswahlliste, Längen – serverseitig | ✓ (3) |
| Header-Injection abgewiesen; Zeilenumbruch im Namen erzeugt keinen Mail-Kopf | ✓ (2) |
| Honigtopf und zu schnelle Übermittlung: Antwort wie Erfolg, aber keine Nachricht | ✓ (2) |
| Fremde Herkunft 403, erlaubte 200; Anfrage über 13 MB 413 | ✓ (3) |
| **neu:** Rückruf ohne Telefonnummer 422; unbekanntes Zeitfenster 422; Rückruf mit Zeitfenster steht in der Nachricht | ✓ (3) |
| **neu:** Foto-Upload: `multipart/mixed`, Anhang byte-identisch, neutraler Dateiname statt Originalname | ✓ (2) |
| **neu:** Getarnte Datei (PHP-Code mit `.jpg`) 422; mehr als drei Fotos 422; leeres Dateifeld stört nicht | ✓ (3) |
| Ohne JavaScript 303 bzw. sichere 422-Seite; Header `nosniff`/`no-store` | ✓ (3) |
| Mengenlimit 429, keine IP im Klartext; SMTP-Dialog; SMTP nicht erreichbar → 502 | ✓ (4) |

### `tests/e2e.mjs` – 36 von 36 bestanden

| Prüfung | Ergebnis |
|---|---|
| Kein waagerechter Überlauf auf 14 Seiten bei 320, 375, 768, 1024, 1440 px | ✓ (5) |
| Textvergrößerung 200 % bei 375 px ohne Überlauf (Start, Kontakt, Trockenbau) | ✓ |
| axe-core (WCAG 2.0/2.1/2.2 A+AA, Best Practices) auf 14 Seiten bei 1440 und 375 px, gemessen nach Ende der Einstiegsanimationen | ✓ **0 Funde** jeder Schwere |
| Sprunglink, sichtbarer Fokus, Mobilmenü per Tastatur | ✓ (3) |
| **neu:** Vollbild-Menü bei 390, 768 und 360 × 600 px direkt unter dem Kopf, alle Hauptpunkte sichtbar bzw. im Menü scrollbar, Kontaktknöpfe erreichbar | ✓ (3) |
| **neu:** Desktop (1280 px) ohne Menü-Knopf; Untermenü „Leistungen“ per Hover und Tastatur, Escape schließt mit Fokus zurück, Bereich als aktuell markiert | ✓ |
| **neu:** Kopf weicht auf dem Handy beim Herunterscrollen und kehrt zurück; keine Schnellkontakt-Leiste auf der Kontaktseite | ✓ |
| **neu:** Kurzvideo mit einem im Test erzeugten Clip: lädt erst im Sichtbereich, läuft dann über dem Standbild, Pause-Knopf hält an und es bleibt angehalten; bei „Bewegung reduzieren“ weder Start noch Knopf | ✓ |
| Formular: Feldfehler mit `aria-invalid`/`aria-describedby`, Erfolg, Doppelklick, Serverfehler | ✓ (5) |
| Ohne JavaScript: Inhalt, Navigation, **Wandaufbau-Zeichnung** sichtbar; Formular serverseitig angenommen | ✓ (2) |
| **neu:** Bewegung reduzieren: keine Bewegungsklasse, alle animierten Inhalte sofort sichtbar, kein Scroll-Pinning | ✓ |
| **neu:** GSAP: nach dem Scrollen sind auf acht Seiten alle animierten Inhalte vollständig sichtbar | ✓ |
| **neu:** Three.js lädt erst bei Annäherung, Canvas vorhanden, auf großen Bildschirmen an den Scroll gekoppelt, Schritte per Knopf | ✓ |
| **neu:** Ohne WebGL: Zeichnung bleibt, Schritte steuern deren Ebenen | ✓ |
| **neu:** Alltagsfall-Link füllt Leistung und Anliegen vor; Rückruf-Zeitfenster und Pflicht-Telefonnummer; Anfrage mit Rückruf **und Foto** kommt mit Bildanhang an | ✓ (3) |
| **neu:** Vorschau-Schalter „Kundenansicht“ blendet Redaktionshinweise aus und bleibt beim Seitenwechsel erhalten | ✓ |
| Entwurfs-Build: gekennzeichnete Projektkarten, **Flip-Filter** mit Ansage, Vorher/Nachher-Regler, Bildansicht per Tastatur | ✓ (4) |

Bildschirmfotos aller 14 Seiten bei 390 und 1440 px sowie die axe-Berichte legt die Suite im Bericht-Ordner ab;
in GitHub Actions sind sie als Artefakt `browser-bericht` herunterladbar.

## 2. Manuell geprüft

| Prüfung | Ergebnis |
|---|---|
| Sichtprüfung aller Seiten bei 1440 px, Start/Kontakt/Wandaufbau auch bei 390 px | Gefunden und behoben: Hero-Überschrift brach in fünf Zeilen (Schriftgrad und Spaltenverhältnis angepasst); Beschriftungen im Hero überlagerten sich (jetzt Nummern mit Legende); Zeichnungen in Bildrahmen beschnitten (absolut eingepasst); Kachelkanten in der Betonstruktur (`stitchTiles`); gestrichelte Linien verloren durch DrawSVG ihr Muster (werden jetzt eingeblendet statt nachgezeichnet); Legende des Rundgangs mit sechs statt fünf Punkten; 3D-Bühne verschwand auf Mobilgeräten beim Antippen eines Schritts (jetzt mitlaufend) |
| 3D-Szene fachlich | Achsmaß 625 mm, Platte 1250 mm über zwei Felder, UW oben/unten, CW 75, Mineralwolle 60 mm, GKB 12,5 mm, Schraubabstand 250 mm. Reihenfolge vereinfacht (Rückseite vor der Dämmung). Als „vereinfachter Beispielaufbau“ ohne Brand- oder Schallschutzaussage gekennzeichnet |
| Nahaufnahmen aus der 3D-Szene | verworfen – prozedurale Texturen wirkten aus der Nähe künstlich. Verwendet werden nur drei Totalen; Reparatur und Hausmeister erhalten Zeichnungen |
| **Navigation und Responsive** (11.10.2026) – alle 14 Seiten bei 320, 360, 390, 600, 768, 900, 1024 und 1280 px | Gefunden und behoben: Mobilmenü wurde durch den Unschärfe-Filter des Kopfes beschnitten und war nur teilweise sichtbar (Filter auf eine Hintergrundebene verlegt, Menü jetzt Vollbild unter dem Kopf); Klassenname für offene Angaben kollidierte mit dem Menüzustand (rote Unterstreichung im ganzen Menü); Knopftext im Menü schwarz auf schwarz; Vorschau-Streifen stand vor dem Sprunglink. Neu: Untermenü „Leistungen“ ab 960 px, Kopf weicht auf dem Handy beim Herunterscrollen, Tablet-Raster (600–899 px) für Leistungskarten, Schritte, Projekte und Fußbereich, Schnellkontakt-Leiste entfällt auf den Kontaktseiten |
| **Symbolbilder** (11.10.2026) – Startseite, Leistungsübersicht, Trockenbau bei 1440 und 390 px | Fünf bereitgestellte Fotos eingebunden (640/1280/1536 px, WebP, ohne EXIF). Bildbänder am Desktop auf 21:9 begrenzt, damit sie die Seite nicht dominieren; Marke „Symbolbild“ auf dem Handy verkleinert; Bildunterschrift im Seitenkopf mit Abstand zur Trennlinie |
| **Kurzvideos** (11.10.2026) mit einem Testclip auf der Startseite | Abspielen, Einblenden, Pause per Maus und Tastatur, Pausieren außerhalb des Sichtbereichs und kein Start bei reduzierter Bewegung geprüft. Der erste automatische Test scheiterte an einer zu kurzen Wartezeit, weil die 3D-Szene den Software-Renderer auslastete; der Test läuft jetzt ohne WebGL und wartet auf den Start statt eine feste Zeit. Echte Clips gibt es noch nicht (Prompts: `docs/MEDIENLISTE.md`) |
| Texte | Unbestätigte Leistungsversprechen entfernt („Wenn wir nicht sofort abnehmen, rufen wir zurück“, „halten Termine ein“, „landet bei dem, der auch vorbeikommt“) |

### Labormessung Ladeverhalten (**kein Lighthouse**)

Chromium, 390 × 844 px, Netz 1,6 Mbit/s bei 150 ms Latenz, CPU 4× gedrosselt, Cache aus, **ohne** Serverkompression
(`php -S`), zwei Läufe je Seite. INP-Näherung: längste Interaktion beim Öffnen und Schließen des Mobilmenüs.

| Seite | LCP | CLS | INP (Näherung) | Übertragung bis „load“ |
|---|---|---|---|---|
| Start | 1,81 s / 1,82 s | 0 | 152 / 168 ms | 398 KB |
| Trockenbau | 1,37 s | 0 | 56 ms | 362 KB |
| Reparatur | 1,95 s / 1,97 s | 0,046 | 64 / 72 ms | 342 KB |
| Kontakt | 1,21 s | 0 | 80 ms | 335 KB |

Ziele LCP < 2,5 s, CLS < 0,1 und INP < 200 ms werden im Labor eingehalten. Desktop ungedrosselt: LCP 0,14–0,28 s.
Mit Kompression auf dem Server (in `.htaccess` aktiviert) sinkt die Übertragung deutlich: HTML + CSS + eigene Skripte
der Startseite ≈ 30 KB gzip, GSAP (Core, ScrollTrigger, SplitText, DrawSVG) ≈ 52 KB gzip, Hero-Bild 24 KB.
Das 3D-Bündel (three.js) hat 141 KB gzip und wird **erst geladen, wenn der Wandaufbau in die Nähe des Sichtbereichs
kommt** – es beeinflusst LCP nicht.

## 3. Nicht prüfbar in dieser Umgebung

| Was | Warum |
|---|---|
| Lighthouse-Wert | nicht ausgeführt; Labormessung oben ersetzt ihn nicht |
| INP im Feld | erfordert echte Nutzer; oben nur eine Labornäherung |
| 3D-Darstellung auf echter Grafikhardware und auf iOS/Safari | nur Chromium mit Software-Rendering (SwiftShader). Unter Software-Rendering verlangsamt die Szene den Browser spürbar; Chrome bietet WebGL ohne GPU standardmäßig nicht an, dann greift die Zeichnung |
| Tatsächliche Zustellung an ein echtes Postfach, SMTP mit TLS und Anmeldung | kein Mailserver, keine Zugangsdaten |
| `.htaccess` (Header, CSP, Kompression, Weiterleitungen, Upload-Grenzen per `php_value`) | `php -S` wertet `.htaccess` und `.user.ini` nicht aus; die Upload-Grenzen wurden im Test per `-d` gesetzt |
| Screenreader (NVDA, VoiceOver, TalkBack), Firefox, Safari | nicht verfügbar |
| Kurzvideos als MP4 (H.264) und in Safari/iOS | geprüft nur mit einem WebM-Testclip in Chromium; MP4-Wiedergabe und iOS-Verhalten (Stromsparmodus unterdrückt Autoplay) erst mit echten Clips auf Geräten |
| KI-Bilder aus Figma | generiert, aber nicht abrufbar: Netzwerkrichtlinie sperrt `www.figma.com` |
| Herkunft der bereitgestellten Symbolbilder | aus den Dateien nicht ablesbar (keine Metadaten); muss der Betreiber bestätigen |

## 4. Noch offen

| Punkt | Wer | Blockiert Livegang? |
|---|---|---|
| Firmendaten, Ort, Einsatzgebiet, Domain | Betreiber | **ja** – Produktions-Build bricht ab |
| 7 offene Punkte auf 6 Seiten (Leistungsumfang, Abgrenzung, Alltagsfälle, Pflegeplan, Netzwerk-Gewerke, Erreichbarkeit) | Betreiber | **ja** |
| Hoster, Formular-Konfiguration, **Testanfrage mit Foto und Rückruf über das Live-Formular** | Betreiber | **ja** – bis dahin meldet das Formular „noch nicht eingerichtet“ |
| Header, Kompression, Weiterleitungen und Upload-Grenzen auf dem Live-Server prüfen | Technik | ja |
| Gewerberechtliche Klärung (`docs/LEGAL-CHECKLIST.md`, Abschnitt 3) | Betreiber + Kammer | ja |
| Quelle und Lizenz der Symbolbilder (`SYMBOLBILD_QUELLE`); bei KI-Bildern Kennzeichnung „Symbolbild (KI-generiert)“ | Betreiber | **ja** – Produktions-Build bricht ab |
| Eigene Fotos (Inhaber, Einblicke) nach den Fotobriefings | Betreiber | nein – Ersatzmotive und Briefings vorhanden |
| Echte Projekte mit Freigabe | Betreiber | nein – gestalteter Leerzustand |
| Lighthouse auf dem Live-Server, Screenreader-Test, Safari/Firefox, 3D auf echten Geräten | Technik | nein, empfohlen |
| Bilder und Kurzvideos laut `docs/MEDIENLISTE.md` erzeugen bzw. fotografieren | Betreiber | nein – Plätze vorbereitet, Standbilder vorhanden |

## 5. Tests selbst ausführen

```
python3 scripts/build-site.py
python3 tests/pruefen.py
python3 scripts/firmendaten.py && python3 tests/formular_test.py
cd tests && npm ci && node e2e.mjs        # CHROMIUM_PFAD=… falls kein Playwright-Browser installiert ist
```
Die Browser-Suite dauert wegen der 3D-Szene und der Bildschirmfotos etwa 20 Minuten.
