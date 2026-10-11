# Bild- und Medienbriefing

Drei Gruppen mit klar getrennten Regeln. Die wichtigste: **Ein Bild, das nicht aus einem echten Gashini-Auftrag stammt,
darf nie so wirken, als stamme es daraus.**

## A · Echte Projektfotos – Pflicht für die Galerie

**Verwendung:** Projektgalerie, Projektdetailseiten, Projektvorschau auf der Startseite, später Social Media.
**Ablage:** `src/assets/bilder/projekte/<slug>/` · Eintrag in `data/projekte.json`

| Motiv je Projekt | Format | Dateiname | Rolle in `projekte.json` |
|---|---|---|---|
| Titelbild: fertiger Raum, Totale | Querformat 3:2 oder 16:9, ≥ 2400 px Breite | `titel.jpg` | `titel` |
| Vorher, fester Standpunkt | 4:3, ≥ 1600 px | `vorher.jpg` | `vorher` |
| Nachher, **derselbe Standpunkt** | 4:3, ≥ 1600 px | `nachher.jpg` | `nachher` |
| 2–4 Prozessbilder: Ständerwerk offen, Anschluss Decke/Boden, Fuge, Türzarge | 1:1 oder 4:3, ≥ 1200 px | `prozess-1.jpg` … | `prozess` |

**Aufnahmeregeln** (ausführlich in `strategie/03-marke-und-medienstandards.md`, Abschnitt 3.2):
- Tageslicht, Lampen an, kein Blitz · Kamera auf Brusthöhe, gerade
- Vorher/Nachher: Vorher-Bild vor der Nachher-Aufnahme auf dem Telefon öffnen und Ausschnitt nachstellen
- Aufräumen vor dem Nachher-Bild: kein Werkzeug, keine Kabel, keine Becher
- Keine Hausnummern, Klingelschilder, Familienfotos, Dokumente, Bildschirme
- Personen nur mit schriftlicher Einwilligung

**Rechte – Pflichtfelder je Bild in `projekte.json`:**
`fotograf` (wer hat fotografiert), `freigabe_kunde` (true nur mit schriftlicher Zustimmung), `nutzungsrecht`
(z. B. „eigene Aufnahme, uneingeschränkt“), `ki_generiert` (muss `false` sein). Ohne diese Angaben veröffentlicht der
Generator das Projekt nicht und meldet eine Warnung.

**Bildaufbereitung:** Originale ablegen; Varianten `name-640.webp`, `name-1280.webp`, `name-1920.webp` daneben legen,
dann erzeugt der Generator automatisch ein `srcset`. Ein Hilfsskript dafür ist als P1 vorgesehen (Pillow); bis dahin
genügt ein Export aus einem Bildprogramm.

## B · Bildsystem der Website (Stand Relaunch)

Die Website arbeitet mit drei Bildebenen (Begründung: `docs/CREATIVE-DIRECTION.md`, Abschnitt 4):

| Ebene | Quelle | Wo | Kennzeichnung |
|---|---|---|---|
| **Plan** – technische Zeichnungen | `scripts/zeichnungen.py` (SVG, im Build erzeugt) | Explosionsdarstellung, Anwendungen, Ausbesserung, Rundgang, Netzwerk, Symbole | „Schematische Darstellung“ |
| **Material** – Visualisierungen | `scripts/werkzeuge/3d` → `src/assets/bilder/visualisierung/` | Startseite, Trockenbau, Leistungsübersicht | „Visualisierung – … Kein Projektfoto.“ |
| **Wirklichkeit** – eigene Fotos | Betrieb (Abschnitte A und C) | Projekte, Über uns | Bildnachweis, Freigabe in `projekte.json` |
| **Symbolbilder** – fremde Fotos | vom Betreiber bereitgestellt → `src/assets/bilder/symbol/` | Startseite, Leistungsübersicht, Trockenbau | Marke „Symbolbild“ im Bild, Alt-Text „Symbolbild: …“, Unterschrift „… Kein Projektfoto.“ |

Fehlt ein Foto, zeigt die Vorschau ein **Fotobriefing** (Motiv, Format, Licht, Dateiname); in Produktion erscheint das
Ersatzmotiv. Neue Fotos werden mit dem passenden Namen unter `src/assets/bilder/fotos/` abgelegt
(`inhaber-640.webp`, `inhaber-1280.webp`, `inhaber-1920.webp`) und ersetzen das Briefing beim nächsten Build automatisch.

## C1 · KI-Symbolbilder – optional, mit Prompts

**Stand:** Für den Relaunch waren bis zu 10 KI-Bilder über Figma freigegeben. Ein Bild wurde erzeugt, konnte aber nicht
heruntergeladen werden, weil die Netzwerkrichtlinie der Entwicklungsumgebung `www.figma.com` sperrt. Deshalb verwendet
die Website **kein** selbst erzeugtes KI-Bild. Am 11.10.2026 hat der Betreiber fünf Fotos bereitgestellt; sie sind als
Symbolbilder eingebunden, ihre Quelle (KI-generiert oder Bildagentur) ist noch zu bestätigen. Die Prompts unten sind so
formuliert, dass weitere Ergebnisse zur Bildsprache passen.

**Erlaubt für:** Atmosphäre, Materialdetails, Open-Graph-Bild. **Nie für:** Projekte, Projektvorschau, Über uns,
alles in der Nähe von Ortsangaben oder Kundenaussagen. **Kennzeichnung:** Bildunterschrift „Symbolbild (KI-generiert)“.
**Herkunft:** Werkzeug, Datum, Prompt und Lizenzbedingungen in `src/assets/bilder/symbol/HERKUNFT.md` eintragen.

**Prompts:** Die vollständige, nach Priorität geordnete Liste fehlender Motive – mit Platz auf der Website, Dateiname,
Prompt, Stil- und Ausschluss-Zusatz, Prüfliste und Kurzvideos („Bild zu Video“) – steht in
[`docs/MEDIENLISTE.md`](MEDIENLISTE.md). Sie ersetzt die frühere Prompt-Tabelle an dieser Stelle.

## C2 · Content-Briefing für ChatGPT (Texte für neue Projekte und Seiten)

Für Projektberichte und Ergänzungen kann ein Sprachmodell Entwürfe schreiben. Der folgende Auftrag hält Tonalität und
Grenzen ein; das Ergebnis prüft immer der Inhaber.

```
Du schreibst Texte für die Website von Gashini Dienstleistungen, einem inhabergeführten Betrieb für Trockenbau,
Reparatur und Instandhaltung sowie Hausmeisterservice. Zielgruppe: private Eigentümer, Vermieter, Hausverwaltungen.

Ton: ruhig, sachlich, präzise, freundlich. Kurze Sätze. Siezen. Keine Superlative, keine Werbefloskeln
(„Ihr Partner für …“, „höchste Qualität“, „rundum sorglos“), keine Ausrufezeichen.

Grenzen – unbedingt einhalten:
- Erfinde nichts: keine Zahlen, Jahre, Mitarbeiterzahlen, Qualifikationen, Zertifikate, Garantien, Preise,
  Bewertungen, Kundenzitate oder Partnerbetriebe. Fehlt eine Angabe, schreibe [ANGABE FEHLT: …].
- Keine Aussagen zu Brand- oder Schallschutz, Statik oder Normerfüllung.
- Elektro-, Gas-, Wasser- und Heizungsarbeiten führt Gashini nicht selbst aus; das übernehmen Fachbetriebe.
- Keine Adressen, Namen oder privaten Details von Kunden.

Aufgabe: Schreibe aus meinen Stichpunkten einen Projektbericht mit den Abschnitten
Ausgangssituation (2–3 Sätze), Aufgabenstellung (1–2 Sätze), Ausgeführte Arbeiten (3–6 Stichpunkte),
Ergebnis (2 Sätze, ohne Wertung). Dazu ein Kurztext für die Projektkarte (max. 140 Zeichen) und je Foto
einen Alternativtext (max. 120 Zeichen, beschreibt, was zu sehen ist).

Stichpunkte: …
```

## C3 · Eigene Unternehmensfotografie – geplant

| Motiv | Verwendung | Format | Dateiname |
|---|---|---|---|
| Inhaber bei der Arbeit (nicht gestellt in die Kamera blickend) | Über uns, Porträtfläche | 4:5, ≥ 1600 px | `inhaber-arbeit.jpg` |
| Inhaber, ruhiges Porträt vor neutraler Wand | Über uns, Google-Profil, Presse | 4:5 und 1:1 | `inhaber-portrait.jpg` |
| Team bei einem Arbeitsschritt | Über uns | 3:2 | `team-montage.jpg` |
| Fahrzeug vor einem Objekt (Hausnummer nicht erkennbar) | Über uns, Social | 3:2 | `fahrzeug.jpg` |
| Werkzeug-Stillleben: Richtlatte, Spachtel, Schlagschnur | Abschnittstrenner, Social | 1:1, 3:2 | `werkzeug-*.jpg` |
| Hände bei der Arbeit: Schraube setzen, Fuge spachteln | Leistungsseiten | 4:3 | `detail-arbeit-*.jpg` |

**Rechte:** eigene Aufnahmen; Einwilligung aller abgebildeten Personen schriftlich, inkl. Widerrufsweg.

## Vorhandene Dateien und ihr Status

| Datei | Herkunft | Lizenz | Verwendung |
|---|---|---|---|
| `brand/logo*.svg`, `signet.svg`, `favicon.svg` | eigene Gestaltung | eigen | Website, Druck |
| `src/assets/fonts/*` | Fontsource, SIL OFL 1.1 | frei, Lizenztext beiliegend | Website |
| `brand/material/holz-*.webp` (5 Dateien) | **unbekannt** (vom Betreiber bereitgestellt) | **ungeklärt** | **nicht verwendet** – erst nach Lizenznachweis |
| `src/assets/bilder/platzhalter/*.svg` | eigene, neutrale Platzhalter | eigen | nur im Entwurfs-Build |
| Betonstruktur in `site.css` | im Code erzeugtes Rauschen (SVG-Filter) | eigen | Hintergrund der Zeichnungen |
| `src/assets/bilder/visualisierung/*.webp` | eigene Renderings (three.js), siehe `HERKUNFT.md` | eigen | Startseite, Leistungen, Trockenbau |
| `src/assets/bilder/symbol/*.webp` (5 Motive) | vom Betreiber bereitgestellt, siehe `HERKUNFT.md` | **zu bestätigen** – Produktions-Build gesperrt, bis `SYMBOLBILD_QUELLE` gesetzt ist | Startseite, Leistungsübersicht, Trockenbau – als Symbolbild gekennzeichnet |
| Zeichnungen (SVG im HTML) | `scripts/zeichnungen.py` | eigen | alle Leistungsseiten, Netzwerk |
| `src/assets/js/vendor/*` | GSAP 3.15 (Standard „No Charge“ License), three.js 0.186 (MIT) | siehe `LIZENZEN.txt` | Bewegung, 3D |
