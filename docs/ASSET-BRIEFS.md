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
| 2–4 Details: Anschluss Decke/Boden, Kante, Fuge, Türzarge | 1:1 oder 4:3, ≥ 1200 px | `detail-1.jpg` … | `galerie` |
| Optional: Zwischenstand (Ständerwerk offen) | 4:3 | `bauzustand.jpg` | `galerie` |

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

## B · KI-generierte atmosphärische Bilder – optional

**Erlaubt für:** Hero-Hintergrund, Materialdetails, Abschnittstrenner, Open-Graph-Bild.
**Nie für:** Galerie, Projektvorschau, Über-uns, alles neben Kundenstimmen oder Ortsangaben.

| Motiv | Prompt-Richtung | Format | Dateiname |
|---|---|---|---|
| Gipskarton-Detail im Streiflicht | „Makroaufnahme einer gespachtelten Gipskartonfuge im seitlichen Tageslicht, neutrale Grautöne, ruhig, keine Personen“ | 3:2, 2400 px | `atmosphaere-gipsfuge.webp` |
| Metallprofile | „CW-Profile aus verzinktem Stahl, gestapelt, weiches Licht, Schwarz-Weiß-Anmutung“ | 3:2 | `atmosphaere-profile.webp` |
| Sichtbeton-Fläche | „glatte Sichtbetonwand, leichte Schalungsstruktur, diffuses Licht, keine Objekte“ | 16:9 | `atmosphaere-beton.webp` |
| Leerer, fertiger Raum | „heller, leerer Raum mit neuer Trennwand und Tür, minimalistisch, Abendlicht“ – **Vorsicht:** wirkt wie ein Projektfoto, deshalb nur mit Bildunterschrift „Symbolbild“ | 16:9 | `symbol-raum.webp` |

**Kennzeichnung:** Jede Verwendung trägt die Bildunterschrift „Symbolbild (KI-generiert)“. Herkunft (Werkzeug, Datum,
Prompt) wird in `brand/material/HERKUNFT.md` dokumentiert. Nutzungsbedingungen des KI-Werkzeugs für kommerzielle
Nutzung vorher prüfen.

**Aktuelle Entscheidung:** Die Startseite nutzt statt eines KI-Bildes eine **technische Zeichnung** einer Ständerwand.
Sie ist fachlich korrekt, eindeutig keine Projektdokumentation und braucht keine Lizenz. Sobald ein starkes eigenes
Titelfoto vorliegt, kann es die Zeichnung ersetzen oder ergänzen.

## C · Eigene Unternehmensfotografie – geplant

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
| Betonstruktur in `site.css` | im Code erzeugtes Rauschen (SVG-Filter) | eigen | Hintergrund der Zeichnung |
