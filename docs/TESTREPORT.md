# Testbericht

Stand: 12.10.2026, Premium-Relaunch in der neuen CI (Logo-Paket, Anthrazit/Signalgelb/Kalkweiß, Archivo) auf `claude/relaunch-premium`,
mit den KI-Symbolbildern der zweiten Lieferung, lokaler SEO für den Raum Stuttgart und Seitenstart oben. Geprüft in der Entwicklungsumgebung mit
Python 3.11, PHP 8.4, Node 22, Chromium über Playwright 1.56 und axe-core 4.11.

Vier Kategorien, streng getrennt: **automatisch getestet** · **manuell geprüft** · **nicht prüfbar** · **noch offen**.
Kein Ergebnis in diesem Dokument ist geschätzt oder hochgerechnet. Lighthouse wurde **nicht** ausgeführt; die
Leistungswerte unten stammen aus einer eigenen Labormessung und sind als solche gekennzeichnet.

## 1. Automatisch getestet

Alle Tests liegen im Repository und laufen in GitHub Actions bei jedem Push (`.github/workflows/vorschau.yml`).
Auf einem GitHub-Runner liefen alle Suiten grün: Workflow-Lauf
[38183541288](https://github.com/Vroind-ausm-All/Gashini/actions/runs/38183541288) für Commit ff68d11 – Jobs `pruefen`
(statische Prüfungen, Formular-Backend) und `browser` (Abgleich von 3D-Bündel und GSAP mit der Quelle, Browser-Tests)
erfolgreich.
Lokal (12.10.2026, nach Bildern, Stuttgart-SEO und Scroll-Fix): statische Prüfungen 17/17, Formular-Backend 30/30,
Browser-Tests 39/39. Nach dem Fix für eingebettete Vorschauen (12.10.2026, abends): 17/17, 30/30, 40/40. Nach
bedienbarem Einsatzgebiet, G-Icon und Maus-Parallax: 18/18, 30/30, 42/42. Nach Auswahlfeld, Formular-Links mit
`ort`/`plz`/`kreis`, G-Icon als Kachel und gebündelten Hover-Effekten (Zweig `claude/einsatzgebiet-icon-hover`):
**19/19, 30/30, 48/48**, axe ohne Funde. Der erste Browser-Lauf dieses Stands fand waagerechten Überlauf auf
`/einsatzgebiet/` bei 320, 375 und 768 px (PLZ-Reihen von Orten wie Ludwigsburg brachen nicht um) – behoben, zweiter Lauf grün. Der erste Browser-Lauf brach beim Video-Test ab: Der Test setzte seinen Testclip hinter die erste
Marke „Symbolbild“ der Startseite – das ist jetzt die erste Leistungskarte, deren Kartenlink den Pause-Knopf überdeckte.
Der Test zielt jetzt ausdrücklich auf das Bildband; zusätzlich liegt ein Pause-Knopf in Karten über dem Kartenlink.
Der frühere einmalige Überlauf der Kontaktseite bei 375 px trat in beiden Läufen nicht auf.

### `tests/pruefen.py` – 19 von 19 bestanden

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
| **neu:** Marke: Web-Logos entsprechen dem Logo-Paket (viewBox, Farben, Pfadanzahl), `favicon.ico` vorhanden, keine Ziegelrot- oder Altschrift-Reste, Hausfarben gesetzt, Archivo einzige Schriftdatei, Kopf und Fuß mit den richtigen Varianten; **neu:** Website-Icon enthält genau die G-Glyphe des Signets in Hausfarben, `favicon.ico` ist das G-Icon, Farben `#1E2124`/`#F4F2ED`, kein Band, kein Text; PNG 32/180/192/512 in richtiger Größe, ICO mit 16/32/48 px, Manifest-Icons vorhanden, jede Seite bindet ICO, SVG, PNG 32, Apple-Touch-Icon und Manifest ein; keine `unsafe-inline`-Ausnahme mehr | ✓ |
| **neu:** Kurzvideos: stumm, ohne `autoplay`-Attribut und ohne Bedienleiste, immer über einem gekennzeichneten Standbild, Videodateien vorhanden; Hinweis „Video geplant“ nur in Vorschau-Blöcken | ✓ |
| Herkunft jeder Visualisierung und jedes Symbolbilds dokumentiert; keine davon als Projektbild; Symbolbilder im Build mit Alt-Text „Symbolbild: …“ bzw. „Symbolbild (KI-generiert): …“ und passender sichtbarer Marke; **neu:** Kennzeichnung „KI-generiert“ stimmt mit `HERKUNFT.md` überein; nie auf „Über uns“ oder bei den Projekten | ✓ |
| **neu:** Lokale SEO: „Stuttgart“ in Titel und H1 der drei Leistungsseiten und im Titel der Startseite; jedes JSON-LD gültig; genau ein `Service` je Leistungsseite mit 30-km-Gebiet und Verweis auf das Unternehmen; Seite „Einsatzgebiet“ vorhanden und von jeder indexierbaren Seite verlinkt; keine Ortsnamen in Alt-Texten von Symbolbildern; jeder Ort hat einen Formular-Link `?ort=…`, **jede der 97 Postleitzahlen** einen Link `?ort=…&plz=…`, Landkreis-Links nie mit `plz`; PLZ-Prüfung, Landkreis-Filter, Auswahlfeld und Ortssuche vorhanden. Der Generator bricht zusätzlich ab, wenn ein Ort außerhalb von 30 km eingetragen ist | ✓ |
| **neu:** Tiefe (Maus-Parallax): Ebene nur dekorativ (`aria-hidden`), nie auf Kontakt-, Rechts- und Fehlerseiten; im Skript an Maus und erlaubte Bewegung gebunden, Zeigerereignisse pro Bild gebündelt (`requestAnimationFrame`), ohne Dauerschleife | ✓ |
| **neu:** Tätigkeiten (`data/taetigkeiten.json`): Felder und Werte gültig, keine doppelten Einträge, Landingpage nur für veröffentlichte Tätigkeiten und vorhanden, nachgereichte nie veröffentlicht, Datei nicht im Webordner | ✓ |

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

### `tests/e2e.mjs` – 48 von 48 bestanden

| Prüfung | Ergebnis |
|---|---|
| Kein waagerechter Überlauf auf 15 Seiten (neu: Einsatzgebiet) bei 320, 375, 768, 1024, 1440 px | ✓ (5) |
| **neu:** Seiten öffnen oben – nach einem Link, nach „Zurück“ und nach „Neu laden“ jeweils Scrollposition 0; Sprungmarken wie `kontakt/#anfrage` landen weiterhin am Ziel | ✓ |
| **neu:** Einsatzgebiet – Ort wählen hebt ihn hervor und zeigt „Projekt in … anfragen“; PLZ nur auf Wunsch, Waiblingen (mehrere PLZ) zur Auswahl; Landkreis Ludwigsburg bietet seine 14 Orte und eine Anfrage ohne PLZ; Asperg → Formular mit „71679 Asperg“, Hinweis sichtbar, Feld änderbar | ✓ |
| **neu:** Direkte Aufrufe des Formulars: `?ort=Kornwestheim&plz=70806` → „70806 Kornwestheim“, `?kreis=Landkreis Ludwigsburg` und `?kreis=Rems-Murr-Kreis` → Kreisname, `?ort=73760 Ostfildern` → „73760 Ostfildern“, `?plz=70563` → „70563“; HTML im Ort, PLZ mit Buchstaben, sechsstellige PLZ, HTML im Kreis und 80 Zeichen langer Ort werden verworfen | ✓ |
| **neu:** Einsatzgebiet per Tastatur (ein Tab-Halt auf der Karte, Pfeiltasten, Eingabe wählt, Anfrage per Tab erreichbar); Ortssuche „korn“ → Kornwestheim, Korntal-Münchingen, „Atlantis“ → Hinweis mit Anfrage; Handy (Tippen wählt, Anfrage rückt ins Bild); ohne JavaScript ≥ 70 Ortslinks, ≥ 60 PLZ-Links, 47 Kartenlinks, 4 Landkreislinks, Klick auf 73760 → Formular mit Ostfildern und 73760 | ✓ (4) |
| **neu:** Website-Icon: ICO, SVG, PNG 32, Apple-Touch-Icon und Manifest (192/512) eingebunden und abrufbar | ✓ |
| **neu:** Tiefe – Lichtflächen und Linien folgen der Maus und kommen danach zur Ruhe (keine Dauerbewegung), Überschrift und Kartentitel bleiben unbewegt, Bildfläche der Leistungskarte neigt sich, Kontaktseite ohne Ebene; bei „Bewegung reduzieren“ bewegt sich nichts | ✓ |
| **neu:** Eingebettete Vorschau (nachgestellt wie in claude.ai: die einbettende Seite stellt nach jedem Laden die Scroll-Position der vorigen Seite wieder her): neue Seite steht oben, `#anfrage` am Formular, eigenes Scrollen sofort möglich | ✓ |
| Textvergrößerung 200 % bei 375 px ohne Überlauf (Start, Kontakt, Trockenbau) | ✓ |
| axe-core (WCAG 2.0/2.1/2.2 A+AA, Best Practices) auf 15 Seiten bei 1440 und 375 px, gemessen nach Ende der Einstiegsanimationen | ✓ **0 Funde** jeder Schwere |
| Sprunglink, sichtbarer Fokus, Mobilmenü per Tastatur | ✓ (3) |
| **neu:** Vollbild-Menü bei 390, 768 und 360 × 600 px direkt unter dem Kopf, alle Hauptpunkte sichtbar bzw. im Menü scrollbar, Kontaktknöpfe erreichbar | ✓ (3) |
| **neu:** Desktop (1280 px) ohne Menü-Knopf; Untermenü „Leistungen“ per Hover und Tastatur, Escape schließt mit Fokus zurück, Bereich als aktuell markiert | ✓ |
| **neu:** Kopf weicht auf dem Handy beim Herunterscrollen und kehrt zurück; keine Schnellkontakt-Leiste auf der Kontaktseite | ✓ |
| **neu:** Marke im Kopf: ab 960 px Hauptvariante ≥ 220 px, beim Scrollen Kompakt ≥ 180 px ohne Verschiebung des Inhalts; bei 390 und 320 px Kompakt ≥ 180 px | ✓ |
| **neu:** Netzwerk-Geschichte: Schritt 1 nur „Sie“, Schritt 3 mit eigener Leistung, Schritt 5 vollständig mit Legende, aktiver Schritt hervorgehoben; bei reduzierter Bewegung sofort vollständig | ✓ |
| **neu:** Kurzvideo mit einem im Test erzeugten Clip: lädt erst im Sichtbereich, läuft dann über dem Standbild, Pause-Knopf hält an und es bleibt angehalten; bei „Bewegung reduzieren“ weder Start noch Knopf | ✓ |
| Formular: Feldfehler mit `aria-invalid`/`aria-describedby`, Erfolg, Doppelklick, Serverfehler | ✓ (5) |
| Ohne JavaScript: Inhalt, Navigation, **Wandaufbau-Zeichnung** sichtbar; Formular serverseitig angenommen | ✓ (2) |
| **neu:** Bewegung reduzieren: keine Bewegungsklasse, alle animierten Inhalte sofort sichtbar, kein Scroll-Pinning | ✓ |
| **neu:** GSAP: nach dem Scrollen sind auf neun Seiten alle animierten Inhalte vollständig sichtbar | ✓ |
| **neu:** Three.js lädt erst bei Annäherung, Canvas vorhanden, auf großen Bildschirmen an den Scroll gekoppelt, Schritte per Knopf | ✓ |
| **neu:** Ohne WebGL: Zeichnung bleibt, Schritte steuern deren Ebenen | ✓ |
| **neu:** Alltagsfall-Link füllt Leistung und Anliegen vor; Rückruf-Zeitfenster und Pflicht-Telefonnummer; Anfrage mit Rückruf **und Foto** kommt mit Bildanhang an | ✓ (3) |
| **neu:** Vorschau-Schalter „Kundenansicht“ blendet Redaktionshinweise aus und bleibt beim Seitenwechsel erhalten | ✓ |
| Entwurfs-Build: gekennzeichnete Projektkarten, **Flip-Filter** mit Ansage, Vorher/Nachher-Regler, Bildansicht per Tastatur | ✓ (4) |

Bildschirmfotos aller 15 Seiten bei 390 und 1440 px sowie die axe-Berichte legt die Suite im Bericht-Ordner ab;
in GitHub Actions sind sie als Artefakt `browser-bericht` herunterladbar.

## 2. Manuell geprüft

| Prüfung | Ergebnis |
|---|---|
| Sichtprüfung aller Seiten bei 1440 px, Start/Kontakt/Wandaufbau auch bei 390 px | Gefunden und behoben: Hero-Überschrift brach in fünf Zeilen (Schriftgrad und Spaltenverhältnis angepasst); Beschriftungen im Hero überlagerten sich (jetzt Nummern mit Legende); Zeichnungen in Bildrahmen beschnitten (absolut eingepasst); Kachelkanten in der Betonstruktur (`stitchTiles`); gestrichelte Linien verloren durch DrawSVG ihr Muster (werden jetzt eingeblendet statt nachgezeichnet); Legende des Rundgangs mit sechs statt fünf Punkten; 3D-Bühne verschwand auf Mobilgeräten beim Antippen eines Schritts (jetzt mitlaufend) |
| 3D-Szene fachlich | Achsmaß 625 mm, Platte 1250 mm über zwei Felder, UW oben/unten, CW 75, Mineralwolle 60 mm, GKB 12,5 mm, Schraubabstand 250 mm. Reihenfolge vereinfacht (Rückseite vor der Dämmung). Als „vereinfachter Beispielaufbau“ ohne Brand- oder Schallschutzaussage gekennzeichnet |
| Nahaufnahmen aus der 3D-Szene | verworfen – prozedurale Texturen wirkten aus der Nähe künstlich. Verwendet werden nur drei Totalen; Reparatur und Hausmeister erhalten Zeichnungen |
| **Navigation und Responsive** (11.10.2026) – alle 14 Seiten bei 320, 360, 390, 600, 768, 900, 1024 und 1280 px | Gefunden und behoben: Mobilmenü wurde durch den Unschärfe-Filter des Kopfes beschnitten und war nur teilweise sichtbar (Filter auf eine Hintergrundebene verlegt, Menü jetzt Vollbild unter dem Kopf); Klassenname für offene Angaben kollidierte mit dem Menüzustand (rote Unterstreichung im ganzen Menü); Knopftext im Menü schwarz auf schwarz; Vorschau-Streifen stand vor dem Sprunglink. Neu: Untermenü „Leistungen“ ab 960 px, Kopf weicht auf dem Handy beim Herunterscrollen, Tablet-Raster (600–899 px) für Leistungskarten, Schritte, Projekte und Fußbereich, Schnellkontakt-Leiste entfällt auf den Kontaktseiten |
| **Symbolbilder** (11.10.2026) – Startseite, Leistungsübersicht, Trockenbau bei 1440 und 390 px | Fünf bereitgestellte Fotos eingebunden (640/1280/1536 px, WebP, ohne EXIF). Bildbänder am Desktop auf 21:9 begrenzt, damit sie die Seite nicht dominieren; Marke „Symbolbild“ auf dem Handy verkleinert; Bildunterschrift im Seitenkopf mit Abstand zur Trennlinie |
| **Neue CI** (12.10.2026) – alle Seiten bei 390 und 1440 px, Menü, Fuß, Druckvorlagen | Logo-Varianten nach Markenblatt eingesetzt; Archivo läuft breiter als die frühere Schrift – die Startseiten-Überschrift brach in sechs Zeilen, Größenskala neu berechnet (längste Zeile ≈ 9 × Schriftgröße). Web-Logos zunächst samt viewBox gerundet – der neue Markentest fand das, jetzt werden nur Pfadkoordinaten gerundet. Der erste Browser-Lauf (lokal und CI 38179413341) fand drei Fehler: Überlauf bei 200 % Text (lange Wörter in Überschriften und FAQ, automatische Rasterspalten) und zu geringer Kontrast offener Angaben im dunklen Abschluss – behoben. Druckvorlagen: Ziegelrot als Text auf Weiß, nachgesetzter Schriftzug beim Rückendruck und alte CMYK-Angaben ersetzt |
| **Netzwerk-Geschichte** (12.10.2026) bei 1440 × 900, 390 × 844, 360 × 600 sowie mit reduzierter Bewegung und ohne JavaScript | Aufbau je Schritt, Fortschrittsband und Hervorhebung geprüft. Zunächst war das Bild in der Mitte eines Schritts erst halb aufgebaut – Aufbau in die erste Hälfte verlegt. Gedimmte Schritte (anfangs 30 %) und der Leitsatz (anfangs 16 % Deckkraft) unterschritten im Ruhezustand die Kontrastgrenzen – jetzt 62 % bzw. Farbwechsel ab #84888D (3,2 : 1, große Schrift) |
| **Kurzvideos** (11.10.2026) mit einem Testclip auf der Startseite | Abspielen, Einblenden, Pause per Maus und Tastatur, Pausieren außerhalb des Sichtbereichs und kein Start bei reduzierter Bewegung geprüft. Der erste automatische Test scheiterte an einer zu kurzen Wartezeit, weil die 3D-Szene den Software-Renderer auslastete; der Test läuft jetzt ohne WebGL und wartet auf den Start statt eine feste Zeit. Echte Clips gibt es noch nicht (Prompts: `docs/MEDIENLISTE.md`) |
| **KI-Symbolbilder** (12.10.2026) – Startseite, Leistungen, Reparatur, Hausmeister, Trockenbau, Netzwerk, 404 bei 1280 und 390 px | Sechs Bilder eingebunden; Herkunft aus dem C2PA-Nachweis der Originale gelesen (ChatGPT/OpenAI, KI-generiert). Hochformat-Karten der Startseite zeigen mit `fokus="rechts"` den Bildteil mit der Handlung. Eine geplante Formulierung „Protokoll – mit Foto“ wieder entfernt (nicht bestätigte Zusage) |
| **Einsatzgebiet** (12.10.2026) bei 1280 und 390 px | Karte: Beschriftungen „Waiblingen“ und „Schorndorf“ berührten sich, Kilometerangaben kollidierten mit Ortsnamen – Ringbeschriftung nach Westen unter die Achse verlegt. Alte, unvollständige `Service`-Daten im Seitentext gefunden und durch die erzeugten ersetzt (sonst zwei `Service`-Einträge je Seite). Entfernungen aller 47 Orte nachgerechnet (Luftlinie, 7,6–27,6 km); Herrenberg (30,4 km) und Reutlingen (31,7 km) bewusst nicht aufgenommen |
| **Seitenstart in der claude.ai-Vorschau** (12.10.2026) | Rückmeldung: Nach einem Link stand die neue Seite unten. Ursache nachgestellt – die Vorschau-Umgebung stellt nach dem Laden die Scroll-Position der vorigen Seite wieder her (im Test 4891 von 4891 px, also ganz unten). Behoben: In eingebetteten Seiten hält `site.js` die Position kurz oben bzw. an der Sprungmarke, bis der Besucher selbst scrollt (höchstens 4 s nach dem Laden). Als eigenständige Website greift das nicht |
| **Kundenlink auf GitHub Pages** (12.10.2026) – Build unter dem Unterpfad `/Gashini/relaunch/` lokal nachgestellt, alle 15 Seiten geladen, 390 px | Keine fehlenden Dateien, Links funktionieren im Unterordner, `?ansicht=kunde` blendet Redaktionshinweise aus und bleibt beim Seitenwechsel erhalten, `?ansicht=intern` schaltet zurück |
| **Einsatzgebiet bedienbar, G-Icon, Maus-Parallax** (12.10.2026) bei 1280/1440 und 390 px | Bei gewähltem Landkreis Esslingen überlagerten sich die eingeblendeten Ortsnamen – jetzt nur hervorgehobene Punkte, Namen beim Überfahren. Feine Linien liefen auf der Startseite hinter der Bildlegende – nach unten ausgeblendet, hinter Text bewegt sich nichts. Das ICO bekam zunächst eine helle Kontur für dunkle Tabs; das Markenblatt verbietet Konturen, deshalb ohne. Postleitzahlen aus eigenem Wissen eingetragen, nicht amtlich abgeglichen – siehe „Noch offen“ |
| **Auswahlfeld, Formular-Links, G-Kachel, Hover** (12.10.2026) bei 1280 und 375/390 px | Hilfsvariable `kopf` im Skript überdeckte die Kopfzeile (Fehler beim Scrollen) – umbenannt. Auswahlfeld lag auf dem Handy hinter der Schnellkontakt-Leiste – rückt jetzt ins obere Drittel. Überlauf der PLZ-Reihen bei schmalen Bildschirmen (siehe oben) – umbrechend. PLZ nicht amtlich abgeglichen, deshalb `plz_geprueft: false`: Ein Klick auf einen Ort trägt nur den Ort ein |
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
| Herkunft der fünf Symbolbilder der ersten Lieferung | aus den Dateien nicht ablesbar (keine Metadaten); muss der Betreiber bestätigen. Die sechs Bilder der zweiten Lieferung sind per C2PA als KI-generiert belegt |
| Platzierungen bei Google | keine Live-Domain; Wirkung der SEO-Maßnahmen erst nach dem Livegang in der Search Console messbar (`docs/SEO-PLAN.md`, Abschnitt 12) |

## 4. Noch offen

| Punkt | Wer | Blockiert Livegang? |
|---|---|---|
| Firmendaten, Anschrift, Domain (Einsatzgebiet Stuttgart + 30 km ist eingetragen) | Betreiber | **ja** – Produktions-Build bricht ab |
| Google-Unternehmensprofil anlegen, Firmendaten überall gleich (`docs/SEO-PLAN.md`, Abschnitte 7–8) | Betreiber | nein – aber Voraussetzung für Kartenergebnisse |
| Postleitzahlen in `data/einsatzgebiet.json` gegen das amtliche Verzeichnis prüfen, danach `"plz_geprueft": true` | Betreiber | nein – bis dahin wählt der Besucher die PLZ selbst, im Formular änderbar |
| Tätigkeiten: weitere des Auftraggebers noch nicht übermittelt; vorbereitete (Bodenbeläge, Gebäudereinigung, Entrümpelung, Umzugshilfe) und nicht beworbene (Maler, Fliesen, Parkett) klären (`data/taetigkeiten.json`) | Betreiber + Kammer | nein – nichts davon ist veröffentlicht |
| 8 offene Punkte auf 7 Seiten (Leistungsumfang, Abgrenzung, Alltagsfälle, Pflegeplan, Netzwerk-Gewerke, Erreichbarkeit, Ortsliste Einsatzgebiet) | Betreiber | **ja** |
| Hoster, Formular-Konfiguration, **Testanfrage mit Foto und Rückruf über das Live-Formular** | Betreiber | **ja** – bis dahin meldet das Formular „noch nicht eingerichtet“ |
| Header, Kompression, Weiterleitungen und Upload-Grenzen auf dem Live-Server prüfen | Technik | ja |
| Gewerberechtliche Klärung (`docs/LEGAL-CHECKLIST.md`, Abschnitt 3) | Betreiber + Kammer | ja |
| Quelle und Lizenz der Symbolbilder (`SYMBOLBILD_QUELLE`): erste Lieferung klären, für die KI-Bilder die Nutzungsbedingungen von OpenAI bestätigen | Betreiber | **ja** – Produktions-Build bricht ab |
| Eigene Fotos (Inhaber, Einblicke) nach den Fotobriefings | Betreiber | nein – Ersatzmotive und Briefings vorhanden |
| Echte Projekte mit Freigabe | Betreiber | nein – gestalteter Leerzustand |
| Lighthouse auf dem Live-Server, Screenreader-Test, Safari/Firefox, 3D auf echten Geräten | Technik | nein, empfohlen |
| Bilder und Kurzvideos laut `docs/MEDIENLISTE.md` erzeugen bzw. fotografieren | Betreiber | nein – Plätze vorbereitet, Standbilder vorhanden |
| Druckvorlagen inhaltlich abgleichen: Flyer, Visitenkarte und Fahrzeug nennen noch das frühere Angebot (Gebäudereinigung, Umzug, Entrümpelung) und Zusagen wie „Festpreis“, „24 Stunden“, „Termintreu“, die auf der Website bewusst fehlen | Betreiber | nein – betrifft nur den Druck |
| Markenrecherche beim DPMA vor einer Markenanmeldung (Hinweis aus dem Logo-Paket) | Betreiber | nein |

## 5. Tests selbst ausführen

```
python3 scripts/build-site.py
python3 tests/pruefen.py
python3 scripts/firmendaten.py && python3 tests/formular_test.py
cd tests && npm ci && node e2e.mjs        # CHROMIUM_PFAD=… falls kein Playwright-Browser installiert ist
```
Die Browser-Suite dauert wegen der 3D-Szene und der Bildschirmfotos etwa 20 Minuten.
