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
| Farben, Abstände, Schriftgrößen | `src/assets/css/site.css` (Abschnitt „Tokens“ am Anfang) |

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
| `[[kontaktformular]]`, `[[kontaktwege]]`, `[[ablauf]]`, `[[zeichnung]]` | wie auf den bestehenden Seiten |

Redaktionelle Hinweise stehen in `<p class="redaktion">[FREIGABE ERFORDERLICH: …]</p>`. Sie sind in der Vorschau
sichtbar und verhindern die Veröffentlichung. Wenn der Punkt geklärt ist: Text anpassen und den Absatz löschen.

## Ein Projekt veröffentlichen

1. Fotos aufnehmen (Regeln: `docs/ASSET-BRIEFS.md`, Gruppe A) und Freigabe des Auftraggebers **schriftlich** einholen.
2. Ordner anlegen: `src/assets/bilder/projekte/<kurzname>/` und Fotos hineinlegen (`titel.jpg`, `vorher.jpg`,
   `nachher.jpg`, `detail-1.jpg` …). Dateien vorher auf höchstens ~2400 px Breite verkleinern.
3. In `data/projekte.json` den Beispieleintrag kopieren und ausfüllen. Pflicht für die Veröffentlichung:
   - `"status": "freigegeben"`
   - `"freigabe": {"kunde": true, "datum": "2026-…", …}`
   - bei **jedem** Bild: `"freigabe_kunde": true`, `"ki_generiert": false`, `fotograf` und `nutzungsrecht` ausgefüllt
   - `slug`: nur Kleinbuchstaben, Ziffern und Bindestriche – wird zur Adresse `/projekte/<slug>/`
4. Bauen. Fehlt eine Freigabe, meldet der Generator eine Warnung und lässt das Projekt weg.
5. Die drei Beispielprojekte können gelöscht werden, sobald das erste echte Projekt steht.

Ab sechs veröffentlichten Projekten mit mindestens zwei Kategorien erscheint automatisch ein Filter.

**Vorschau mit Beispielprojekten** (nur intern, nie veröffentlichen):
```
ENTWUERFE=1 AUSGABE=/tmp/vorschau python3 scripts/build-site.py
```

## Eine Frage ergänzen

In `data/faq.json` einen Eintrag kopieren:
```json
{"id": "kurzer-name", "seiten": ["kontakt"], "frage": "…?", "antwort": "…"}
```
`seiten` bestimmt, wo die Frage zusätzlich erscheint (`trockenbau`, `hausmeisterservice`, `reparatur`,
`kontakt`). Auf der Seite „Ablauf & Fragen“ erscheinen immer alle.
