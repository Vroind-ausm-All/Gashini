# Inhalte pflegen

Für alles hier reichen ein Texteditor und drei Befehle. Programmierkenntnisse sind nicht nötig.

> **Wichtig:** Nie in `web/` oder `dist/` ändern. Diese Ordner werden bei jedem Lauf neu erzeugt.
> Jede Datei dort beginnt mit dem Hinweis, aus welcher Quelle sie stammt.

## Wo steht was?

| Ich möchte … | Datei |
|---|---|
| Telefon, Adresse, E-Mail, Einsatzgebiet ändern | `data/firmendaten.env` |
| einen Text auf einer Seite ändern | `src/seiten/<seite>.html` |
| eine häufige Frage ergänzen oder ändern | `data/faq.json` |
| ein Projekt veröffentlichen | `data/projekte.json` + Bilder in `src/assets/bilder/projekte/<slug>/` |
| ein eigenes Foto statt eines Fotobriefings einsetzen | `src/assets/bilder/fotos/<name>-640/-1280/-1920.webp` |
| ein Symbolbild austauschen | `src/assets/bilder/symbol/<name>-640/-1280/-1536.webp` + `HERKUNFT.md` |
| Farben, Abstände, Schriftgrößen | `src/assets/css/site.css` (Abschnitt „Tokens“ am Anfang) |
| Animationen anpassen | `src/assets/js/bewegung.js` |
| Zeichnungen ändern | `scripts/zeichnungen.py` |
| 3D-Modell oder Visualisierungen ändern | `scripts/werkzeuge/3d/` (siehe unten) |

## Nach jeder Änderung

```
python3 scripts/build-site.py          # Seiten erzeugen
python3 tests/pruefen.py               # Links, Titel, Überschriften prüfen
python3 scripts/firmendaten.py         # Vorschau in dist/web/ ansehen
```
Für die Veröffentlichung statt der letzten Zeile `python3 scripts/firmendaten.py --produktion` – siehe `docs/DEPLOYMENT.md`.

## Einen Text ändern

Jede Seite in `src/seiten/` beginnt mit Kopfdaten:
```
<!--
titel: Trockenbau & Innenausbau in {{ORT}} | Gashini
beschreibung: Text für die Google-Ergebnisliste, höchstens 155 Zeichen.
pfad: leistungen/trockenbau/
-->
```
Darunter steht normales HTML. Links auf andere Seiten beginnen mit `@/`, z. B. `href="@/kontakt/"` – der Generator
macht daraus den richtigen relativen Pfad. Platzhalter in doppelten geschweiften Klammern (`{{TELEFON}}`) werden aus
`data/firmendaten.env` gefüllt.

Wiederkehrende Bausteine werden mit doppelten eckigen Klammern eingefügt:

| Baustein | Ergebnis |
|---|---|
| `[[abschluss]]` | Kontaktbereich am Seitenende |
| `[[abschluss titel="…" text="…"]]` | derselbe mit eigenem Text |
| `[[faq seite="trockenbau"]]` | Fragen, die in `faq.json` der Seite zugeordnet sind |
| `[[projekte-vorschau]]`, `[[projekte-galerie]]` | Projektkarten bzw. vollständige Galerie |
| `[[abschluss … knopf="…" leistung="reparatur" variante="dunkel" schnellwahl="ja"]]` | Abschluss mit eigenem Knopf, vorausgewählter Leistung, dunkler Variante oder Schnellwahl |
| `[[kontakt-link leistung="trockenbau" anliegen="…"]]` | Link ins Formular mit Vorauswahl (in `href="…"` verwendbar) |
| `[[wandaufbau]]` | interaktiver Wandaufbau (3D mit Zeichnung als Rückfall) |
| `[[visual-schnitt]]`, `[[bild datei="…" alt="…"]]` | Visualisierung der Startseite bzw. ein Bild mit `srcset` |
| `[[symbolbild datei="symbol/…" alt="…"]]` | fremdes Foto mit Marke „Symbolbild“ und Alt-Präfix (Herkunft in `src/assets/bilder/symbol/HERKUNFT.md` eintragen) |
| `[[anwendungen]]`, `[[faelle]]`, `[[flicken]]`, `[[rundgang]]`, `[[netzwerk]]`, `[[zeichnung art="…"]]` | Zeichnungen und Tafeln der Leistungsseiten |
| `[[foto id="…" motiv="…" format="…" licht="…"]]` | eigenes Foto, sonst Ersatzbild plus Fotobriefing (nur Vorschau) |
| `[[faq-gruppen]]` | alle Fragen nach Thema (Seite „Fragen & Ablauf“) |
| `[[kontaktformular]]`, `[[kontaktwege]]`, `[[ablauf]]` | wie auf den bestehenden Seiten |

Kopfdaten für Skripte: `bewegung: nein` lädt keine Animationsbibliothek (Rechtstexte, Danke, 404),
`skripte: flip` lädt zusätzlich den Flip-Filter (Projektübersicht), `vorladen: visualisierung/wand-schnitt`
lädt das Bild der Bühne vor.

Redaktionelle Hinweise stehen in `<p class="redaktion">[FREIGABE ERFORDERLICH: …]</p>`. Sie erscheinen in der Vorschau
als aufklappbarer „Offener Punkt“ und verhindern die Veröffentlichung. Wenn der Punkt geklärt ist: Text anpassen und den
Absatz löschen. Für Kundenpräsentationen blendet der Schalter **„Kundenansicht“** im Vorschau-Streifen alle Hinweise
und Fotobriefings aus.

Blöcke zwischen `<!--vorschau-->` und `<!--/vorschau-->` (z. B. Fotobriefings) erscheinen nur in der Vorschau und
entfallen im Produktions-Build automatisch.

## Navigation ändern

Die Hauptpunkte stehen in `NAV`, die Einträge des Untermenüs „Leistungen“ in `UNTERMENUE` (beide in
`scripts/build-site.py`). Die Kopfdaten `nav: leistungen/` markieren den Bereich, zu dem eine Seite gehört. Verhalten:

- **ab 960 px:** volle Navigation mit Untermenü, das sich per Maus, Fokus oder Pfeil-Knopf öffnet und mit Escape schließt.
  Die Telefonnummer im Kopf erscheint erst ab 1240 px.
- **unter 960 px:** Knopf „Menü“ öffnet ein Vollbild-Menü direkt unter dem Kopf. Es enthält zusätzlich „Fragen & Ablauf“,
  „Anfrage stellen“, den Anruf-Knopf und das Einsatzgebiet. Beim Herunterscrollen weicht der Kopf und kommt beim
  Hochscrollen zurück.
- **unter 760 px:** feste Schnellkontakt-Leiste („Anrufen“ / „Anfragen“) am unteren Rand. Auf den Kontaktseiten entfällt
  sie, weil dort das Formular steht.

## Ein Projekt veröffentlichen

1. Fotos aufnehmen (Regeln: `docs/ASSET-BRIEFS.md`, Gruppe A) und Freigabe des Auftraggebers **schriftlich** einholen.
2. Ordner anlegen: `src/assets/bilder/projekte/<kurzname>/` und Fotos hineinlegen (`titel.jpg`, `vorher.jpg`,
   `nachher.jpg`, `prozess-1.jpg` …). Dateien vorher auf höchstens ~2400 px Breite verkleinern.
   Der Bericht hat die Felder `ausgangssituation`, `aufgabenstellung`, `arbeiten` (Liste), optional `vorgehen`,
   und `ergebnis`; Bilder haben die Rollen `titel`, `vorher`, `nachher`, `prozess`.
3. In `data/projekte.json` den Beispieleintrag kopieren und ausfüllen. Pflicht für die Veröffentlichung:
   - `"status": "freigegeben"`
   - `"freigabe": {"kunde": true, "datum": "2026-…", …}`
   - bei **jedem** Bild: `"freigabe_kunde": true`, `"ki_generiert": false`, `fotograf` und `nutzungsrecht` ausgefüllt
   - `slug`: nur Kleinbuchstaben, Ziffern und Bindestriche – wird zur Adresse `/projekte/<slug>/`
4. Bauen. Fehlt eine Freigabe, meldet der Generator eine Warnung und lässt das Projekt weg.
5. Die vier Beispielprojekte können gelöscht werden, sobald das erste echte Projekt steht.

Ab vier veröffentlichten Projekten mit mindestens zwei Kategorien erscheint automatisch ein Filter (mit Flip-Animation).
Visualisierungen aus `bilder/visualisierung/` dürfen nie als Projektbilder eingetragen werden – die Tests prüfen das.

**Vorschau mit Beispielprojekten** (nur intern, nie veröffentlichen):
```
ENTWUERFE=1 AUSGABE=/tmp/vorschau python3 scripts/build-site.py
```

## Eine Frage ergänzen

In `data/faq.json` einen Eintrag kopieren:
```json
{"id": "kurzer-name", "seiten": ["kontakt"], "thema": "anfrage", "frage": "…?", "antwort": "…"}
```
`thema` ordnet die Frage auf der Seite „Fragen & Ablauf“ ein (`anfrage`, `kosten`, `leistungen`, `daten`).
`seiten` bestimmt, wo sie zusätzlich erscheint (`trockenbau`, `hausmeisterservice`, `reparatur`, `netzwerk`, `kontakt`).

## 3D-Modell, Visualisierungen und GSAP aktualisieren

Nur nötig, wenn das Wandmodell, die Renderings oder die Bibliotheksversionen geändert werden sollen. Dafür braucht es
Node.js 20 oder neuer; die Website selbst baut weiterhin nur mit Python.

```
cd scripts/werkzeuge/3d
npm ci                      # three, gsap, esbuild, playwright in festen Versionen
npm run bauen               # → src/assets/js/wandaufbau.js und src/assets/js/vendor/*
npm run renderings          # → src/assets/bilder/visualisierung/*.webp und anker.json (Chromium nötig)
```
Danach wie gewohnt bauen und prüfen. Das 3D-Modell steht in `quelle/szene.js` (Maße in Metern); jede Änderung an der
Kamera der Ansicht „gesamt“ verschiebt die Beschriftung der Startseite – deshalb immer auch `renderings` laufen lassen.
