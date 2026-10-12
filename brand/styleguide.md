# Gashini Dienstleistungen – Gestaltungsrichtlinien

Verbindliche Grundlage ist das **Markenblatt** `brand/markenblatt.pdf` (Version 1.0, Oktober 2026) mit `LIESMICH.txt`.
Dieses Dokument ergänzt, wie die Marke auf der Website und in den Vorlagen dieses Repositorys umgesetzt ist.

## Logo-Paket

| Ordner / Datei | Inhalt |
|---|---|
| `svg/` | Vektoren für Folierer, Sticker, Druckerei, Schilderbau (Buchstaben als Pfade) |
| `png/` | Pixeldateien mit transparentem Grund: `-1000` für Bildschirm, `-3000` für Druck |
| `favicon.ico` | Browser-Tab |
| `markenblatt.pdf` | alle Varianten, Farbwerte und Regeln auf einer Seite – geht an jeden externen Dienstleister mit |

| Variante | Einsatz laut Markenblatt | Auf der Website |
|---|---|---|
| Hauptvariante (`logo-hauptvariante.svg`) | Website, Briefkopf, Angebot, Rechnung, E-Mail-Signatur | Briefbogen, Visitenkarte, E-Mail-Signatur (als PNG `assets/marke/logo-email.png`) |
| Hauptvariante klein (`-klein.svg`) | sehr kleine Anwendung, schmale Leiste | **Kopf ab 960 px**, 236 px breit |
| Hauptvariante negativ | dunkler Hintergrund | **Fuß**, Flyer, Fahrzeug-Seitenfläche |
| Gestapelt (`logo-gestapelt*.svg`) | Fahrzeugheck, Kleidung, Banner | Rückendruck Arbeitskleidung |
| Kompakt (`logo-kompakt*.svg`) | Fahrzeugtür, Stempel, schmale Flächen | **Kopf unter 960 px** und im verdichteten Kopf beim Scrollen |
| Signet (`signet*.svg`) | Profilbild, App-Icon, Aufkleber; gelbe Variante für Auffälliges | Ersatzbild ohne Foto, JSON-LD-Logo |
| Website-Icon (abgeleitet: `src/assets/icon/`, erzeugt mit `npm run icon` in `scripts/werkzeuge/3d/`) | – | Auf Wunsch des Betreibers nur das **G** des Signets, ohne Band und ohne Kachel: Browser-Tab in Anthrazit, bei dunkler Browser-Oberfläche in Kalkweiß; Home-Bildschirm (iOS) kalkweißes G auf Anthrazit. Die Glyphe ist unverändert übernommen. Im Tab zeigt der Browser das Icon mit 16 px – unter der Signet-Mindestgröße von 24 px; das legt der Browser fest |

**Regeln (Markenblatt):** Die Wortmarke steht nie ohne Gewerkezeile – fehlt der Platz, steht das Signet allein.
Schutzraum ringsum mindestens die Höhe des gelben Bandes (0,07 × Signetkante). Mindestgrößen digital: Signet 24 px,
Hauptvariante 220 px, Kompakt 180 px breit; im Druck Signet 8 mm, Hauptvariante 45 mm, Stickerei 25 mm. Nicht
verzerren, drehen, mit Schatten, Verlauf oder Kontur versehen, nicht umfärben, die Schrift nicht nachbauen.
Das gelbe Band ist exakt so breit wie das G.

**Technik auf der Website:** Der Generator legt schlanke Kopien unter `assets/marke/` an
(`scripts/build-site.py`, `MARKE_WEB`): Koordinaten in den Pfaddaten werden auf zwei Nachkommastellen gerundet
(Abweichung unter 0,02 px bei 1000 px Breite), viewBox, Maße und Farben bleiben exakt. `tests/pruefen.py` prüft das,
die Browser-Tests prüfen die Mindestbreiten im Kopf.

## Farben

| Hausfarbe | HEX | RAL (Näherung) | CMYK (Richtwert) | Pantone |
|---|---|---|---|---|
| Anthrazit | `#1E2124` | 9011 Graphitschwarz | 72 / 64 / 59 / 70 | Neutral Black C |
| Signalgelb | `#FFC93C` | 1021 Rapsgelb | 0 / 23 / 85 / 0 | 123 C |
| Kalkweiß | `#F4F2ED` | 9003 Signalweiß | 2 / 2 / 4 / 0 | 11-0601 TCX |

Vor jeder Produktion ein Muster gegen den HEX-Wert prüfen.

**Umsetzung auf dem Bildschirm** (`src/assets/css/site.css`, Abschnitt „Tokens“):

| Token | HEX | Einsatz | Kontrast |
|---|---|---|---|
| `--c-kalk` | `#F4F2ED` | Seitenhintergrund | – |
| `--c-kalk-2` | `#EBE8E1` | abgesetzte Abschnitte, Bühnen der Visualisierungen | – |
| `--c-anthrazit` | `#1E2124` | Text, Schaltflächen, dunkle Abschnitte, Fuß | 14,5 : 1 auf Kalkweiß |
| `--c-text-2` / `--c-text-3` | `#4F5358` / `#62666B` | Sekundärtext | 6,9 : 1 / 5,2 : 1 |
| `--c-gelb` | `#FFC93C` | Band unter Schaltflächen und Labels, aktive Navigation, Nummern-Unterstrich, Flächen in Zeichnungen, Text **nur auf Anthrazit** | 10,5 : 1 auf Anthrazit |
| `--c-gelb-dunkel` | `#EDB420` | Linien in Zeichnungen (Rundgang, Maßkette) | – |
| `--c-fehler` | `#B3261E` | **nur** Fehlermeldungen im Formular – Funktionsfarbe, kein Markenakzent | 5,8 : 1 |

**Gelb-Regel:** Signalgelb auf Kalkweiß erreicht nur 1,4 : 1. Deshalb erscheint Gelb auf hellem Grund ausschließlich als
Band, Fläche oder Linie – nie als Textfarbe. Texte bleiben Anthrazit; Gelb markiert darunter (wie das Band unter dem G).
Auf Anthrazit darf Gelb auch Text sein.

## Bausteine mit dem Band

- **Primäre Schaltfläche:** Anthrazit mit 4 px gelbem Band unten; beim Überfahren steigt das Gelb auf.
- **Auf dunklen Flächen:** gelbe Schaltfläche mit anthrazitfarbener Schrift.
- **Label:** gelbes Band (22 × 3 px) vor Versalien mit Laufweite 0,16 em – wie „DIENSTLEISTUNGEN“ im Logo.
- **Nummern** (Schritte, Abläufe): Anthrazit mit gelbem Unterstrich.
- **Fokus:** 3 px Anthrazit auf hellem Grund, Gelb auf dunklem Grund; Eingabefelder bekommen einen gelben Saum.

## Schrift

**Archivo** (SIL Open Font License) – die Schrift des Logos – ist die einzige Schrift der Website und der Vorlagen.
Variable Datei mit Stärke 100–900, Teilmenge Latin, lokal ausgeliefert (`src/assets/fonts/archivo-var.woff2`).
Überschriften Stärke ~560 mit leicht negativer Laufweite, Fließtext 400, Labels 500 in Versalien mit Laufweite
0,16 em. Im Logo liegen die Buchstaben als Pfade vor; die Wortmarke wird nie mit der Webschrift nachgesetzt.

## Material und Bewegung

**Material:** Kalkweiße Flächen, Haarlinien, die erzeugte Betonstruktur hinter Zeichnungen. Visualisierungen sind
eigene Renderings des Wandmodells (gelbe Anrisslinien statt der früheren roten), Symbolbilder sind gekennzeichnet
(`docs/MEDIENLISTE.md`). Echte Projektfotos haben immer Vorrang.

**Bewegung erklärt Aufbau – sie ist Verbesserung, nie Voraussetzung** (vollständig in `docs/CREATIVE-DIRECTION.md`):
- Engine: GSAP (ScrollTrigger, SplitText, DrawSVG, Flip), lokal ausgeliefert.
- Signature Motions: *Architectural Hero*, *Wall Construction Experience*, *Project Reveal* und die
  *Netzwerk-Geschichte* (das Schema der Netzwerk-Seite wächst beim Scrollen in fünf Stufen).
- Der Kopf verdichtet sich am Desktop beim Scrollen von der Hauptvariante zur Kompakt-Variante, ohne den Inhalt zu
  verschieben; auf dem Handy weicht er beim Herunterscrollen.
- Ohne JavaScript, beim Drucken und bei *Bewegung reduzieren* ist jeder Inhalt sofort und vollständig sichtbar.

## Tonalität
Sachlich, konkret, ohne Superlative. Kurze Sätze. Keine Versprechen, die im Betrieb nicht gehalten werden können.

## Claim
**Sauber. Gepflegt. Termintreu.** – in den Druckvorlagen auf Anthrazit, das letzte Wort in Signalgelb.
Vor dem Druck mit dem Betreiber abstimmen: Auf der Website stehen bewusst keine Terminversprechen.

## Rechte
Die Marke wurde für Gashini Dienstleistungen erstellt. Vor der Nutzung als eingetragene Marke sollte eine Recherche
beim DPMA erfolgen (siehe `docs/LEGAL-CHECKLIST.md`).
