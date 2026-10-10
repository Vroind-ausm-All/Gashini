# Gashini Dienstleistungen – Gestaltungsrichtlinien

## Logo
| Datei | Verwendung |
|---|---|
| `logo.svg` | Standard, auf hellem Grund |
| `logo-invers.svg` | auf dunklem Grund, Fahrzeug, Arbeitskleidung |
| `signet.svg` | quadratisch: Profilbilder, E-Mail-Signatur, Stempel, Social Media |
| `favicon.svg` | Browser-Tab |

**Schutzraum:** rundum mindestens die Höhe des Signets ÷ 3 freihalten.
**Mindestgröße:** Logo 30 mm Breite im Druck, 120 px am Bildschirm; Signet 10 mm bzw. 32 px.
**Technik:** Die Schrift im Logo liegt als Vektorpfad vor (erzeugt mit `scripts/werkzeuge/logo-pfade.py`), damit das Logo auf jedem Gerät identisch aussieht.
**Nicht erlaubt:** verzerren, drehen, Farben tauschen, Schatten hinzufügen, auf unruhigen Fotos ohne abdunkelnde Fläche platzieren.

## Farben

Schwarz, warmes Off-White und fein abgestufte Grautöne tragen den Auftritt. **Ziegelrot** ist die einzige
Akzentfarbe – die Farbe des Rohbaus und der rot bedruckten Brandschutzplatte – und erscheint nur als Signal.

| Token (`site.css`) | HEX | Einsatz | Kontrast auf Papier |
|---|---|---|---|
| `--c-schwarz` | `#0E0E0E` | Text, Schaltflächen, Fußbereich, Netzwerk-Abschnitt | 18,5 : 1 |
| `--c-schwarz-2` | `#1A1A1A` | Hover dunkler Flächen | – |
| `--c-papier` | `#FAFAF8` | Seitenhintergrund | – |
| `--c-papier-2` | `#F2F1ED` | abgesetzte Abschnitte | – |
| `--c-linie` | `#D9D6D0` | Haarlinien, Rahmen | – |
| `--c-text-2` | `#55534F` | Sekundärtext | 7,3 : 1 |
| `--c-ziegel` | `#B5391C` | Akzentlinie vor Labels, Fokusrahmen, aktive Navigation, erstes Maß der Zeichnung | 5,6 : 1 |
| `--c-ziegel-dunkel` | `#8E2A12` | Link-Hover, Fehlermeldungen | 8,1 : 1 |
| `--c-ziegel-hauch` | `#F8ECE8` | Hintergrund von Fehler- und Redaktionshinweisen | – |

Druck und Folie: Ziegelrot ≈ Pantone 1805 C, RAL 3016, CMYK 0/80/90/25 – vor Auflagendruck Proof anfordern.

**Mengenregel:** Keine roten Flächen, keine roten Schaltflächen, keine roten Überschriften. Rot markiert, wo etwas
gemeint ist – ein Label, der Fokus, die aktuelle Seite, ein Fehler.

## Material und Bewegung

**Material:** Helle Flächen, Haarlinien, eine einzige Materialandeutung – die erzeugte Betonstruktur hinter der
technischen Zeichnung im Einstieg. Die Holztexturen in `brand/material/` werden nicht verwendet, solange ihre Lizenz
nicht geklärt ist (siehe `docs/ASSET-BRIEFS.md`). Echte Projektfotos haben immer Vorrang vor Texturen.

**Bewegung ist Verbesserung, nie Voraussetzung:**
- Die technische Zeichnung zieht ihre Ständer und Maßlinien beim ersten Laden einmal auf (rund 2 Sekunden).
- Hover-Zustände: Unterstreichung wächst, Pfeile rücken 4–6 px nach rechts, Projektbilder skalieren auf 102,5 %.
- Mobilmenü und Bildansicht blenden kurz ein.
- **Keine** Einblendung beim Scrollen: Inhalte sind immer sofort sichtbar, auch ohne JavaScript, beim Drucken und bei
  der Suche im Browser.
- Bei der Systemeinstellung *Bewegung reduzieren* entfällt jede Animation.

## Schriften

| Rolle | Schrift | Einsatz |
|---|---|---|
| Überschriften und Fließtext | **Instrument Sans** (variabel, Breite 75–100 %, Stärke 400–700) | Überschriften schmal (80–90 % Breite, Stärke ~560), Fließtext normal breit, Stärke 400 |
| Technische Beschriftung | **IBM Plex Mono** 400/500 | Labels, Maße, Kategorien, Projektdaten, Bildunterschriften |
| Wortmarke | Barlow Condensed 700/500 | **nur im Logo**, dort als Vektorpfad – nie als Satzschrift |

Alle drei stehen unter der SIL Open Font License und werden lokal ausgeliefert (keine Verbindung zu Google).
Überschriften in normaler Groß-/Kleinschreibung, nicht in Versalien. Versalien nur für kurze Mono-Labels mit
Laufweite +0,08 em. Zeilenlänge im Fließtext höchstens ~66 Zeichen.

**Warum der Wechsel von Barlow Condensed/Inter:** Durchgehende Versalien in schmaler Schrift sind das typische Bild von
Handwerker-Websites. Eine variable Grotesk mit schmalem Schnitt für Überschriften behält die Anmutung der Wortmarke,
wirkt aber ruhiger und architektonischer; die Monospace-Schrift bringt die Präzision technischer Zeichnungen mit.

## Tonalität
Sachlich, konkret, ohne Superlative. Kurze Sätze. Nutzen statt Adjektive:
„Angebot innerhalb von 24 Stunden“ statt „höchste Zuverlässigkeit“.
Keine Versprechen, die im Betrieb nicht gehalten werden können.

## Claim
**Sauber. Gepflegt. Termintreu.** – immer dreizeilig oder mit Punkten getrennt,
das letzte Wort in Ziegelrot.

## Bildsprache
Eigene Fotos vom eigenen Team und den eigenen Objekten. Vorher/Nachher-Paare wirken stärker
als Einzelbilder. Keine Stockfotos mit fremden Personen – sie widersprechen dem Versprechen,
dass der Inhaber selbst vor Ort ist.
