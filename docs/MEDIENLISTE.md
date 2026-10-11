# Medienliste: fehlende Bilder und Kurzvideos

Stand: 12.10.2026, nach der zweiten Bildlieferung (S1, S3, S7–S10 eingebaut). Diese Liste sagt für jedes fehlende Motiv, **wo** es auf der Website erscheint, **wie wichtig** es
ist, **wie die Datei heißen muss** und – wo zulässig – **welcher Prompt** eine passende KI-Version erzeugt.

| Priorität | Bedeutung |
|---|---|
| **A** | großer Effekt oder vor dem Livegang nötig |
| **B** | macht die Seite deutlich lebendiger |
| **C** | Kür |

## 0 · Drei Arten von Material – und eine feste Regel

| Art | Woher | Kennzeichnung | Wo |
|---|---|---|---|
| **F – echte Fotos und Videos** | selbst aufnehmen (Smartphone genügt) | keine; Bildnachweis im Impressum | Über uns, Projekte, Google-Profil |
| **S – KI-Symbolbilder** | Bild-KI mit den Prompts unten | Marke „Symbolbild · KI“ im Bild, Alt-Text „Symbolbild (KI-generiert): …“, Unterschrift „Kein Projektfoto.“ (Baustein-Attribut `ki="ja"`) | Leistungsseiten, Startseite, Netzwerk |
| **V – Kurzvideos** | Video-KI, **aus einem Symbolbild animiert** („Bild zu Video“) | wie das Standbild darunter | über einem Symbolbild |

**Regel:** Was für den echten Betrieb steht – Inhaber, Fahrzeug, Team, ausgeführte Aufträge – wird **nie** per KI
erzeugt. Eine KI-Darstellung würde dort täuschen und widerspricht den Vorgaben des Relaunchs. Alles unter F daher
selbst fotografieren; das Briefing steht in Abschnitt 1.

## Überblick

| ID | Motiv | Platz auf der Website | Art | Prio | Datei | Stand |
|---|---|---|---|---|---|---|
| F1 | Inhaber, Porträt bei der Arbeit | Über uns, Inhaber-Abschnitt | Foto | **A** | `fotos/inhaber-*.webp` | Fotobriefing in der Vorschau |
| F2 | Projektfotos (Titel, Vorher, Nachher, Prozess) | Projekte, Projektvorschau Startseite | Foto | **A** | `projekte/<slug>/…` | Galerie zeigt Leerzustand |
| F3 | Werkzeug und Material, ordentlich ausgelegt | Über uns, Einblicke | Foto | B | `fotos/einblick-werkzeug-*.webp` | Fotobriefing |
| F4 | Firmenfahrzeug vor einem Objekt | Über uns, Einblicke | Foto | B | `fotos/einblick-fahrzeug-*.webp` | Fotobriefing |
| F5 | eigene Fuge im Streiflicht | Über uns, Einblicke | Foto | B | `fotos/einblick-detail-*.webp` | Fotobriefing |
| F6 | Inhaber stellt sich vor (30–45 s) | Über uns | Video | C | `videos/vorstellung.mp4` | Abspieler mit Untertiteln nötig |
| S1 | Loch in der Wand wird gespachtelt | Reparatur, Seitenkopf · Startseite Karte 02 | KI-Bild | **A** | `symbol/wand-ausbessern-spachteln` | **eingebaut** (Marke „Symbolbild · KI“) |
| S2 | Türband wird eingestellt | Leistungsübersicht Zeile 02 (statt `loch-in-der-wand`) | KI-Bild | B | `symbol/reparatur-tuer` | offen – nicht mehr nötig, bringt aber Abwechslung |
| S3 | gepflegtes Treppenhaus | Hausmeister Seitenkopf · Startseite Karte 03 | KI-Bild | **A** | `symbol/treppenhaus-mehrfamilienhaus` | **eingebaut** |
| S4 | Teilen-Vorschau (Open Graph) | jede Seite, wenn sie geteilt wird | KI-Bild + Logo | **A** | `og/teilen.jpg` | fehlt ganz |
| S5 | Schaden mit dem Smartphone fotografieren | Reparatur „Drei Schritte bis zur Antwort“ | KI-Bild | B | `symbol/schaden-fotografieren` | Platz wird beim Einbau angelegt |
| S6 | Wohnung nach Auszug, bereit zur Übergabe | Hausmeister „Zwischen zwei Mietverhältnissen“ | KI-Bild | B | `symbol/mieterwechsel-wohnung` | Platz wird beim Einbau angelegt |
| S7 | Abstimmung am Grundriss | Netzwerk „So läuft ein Vorhaben …“ | KI-Bild | B | `symbol/abstimmung-grundriss` | **eingebaut** |
| S8 | abgehängte Decke im Bau | Trockenbau „Wofür“ (neben dem Dachgeschoss) | KI-Bild | B | `symbol/abgehaengte-decke-montage` | **eingebaut** |
| S9 | Kontrollgang im Keller | Hausmeister „Für wen“ · Leistungsübersicht Zeile 03 | KI-Bild | C | `symbol/kontrollgang-kellerflur` | **eingebaut** |
| S10 | kleines Loch in heller Wand | 404-Seite · Leistungsübersicht Zeile 02 | KI-Bild | C | `symbol/loch-in-der-wand` | **eingebaut** |
| V1 | Licht wandert über die Fuge | Startseite, Bildband „Auch kleine Aufträge“ | Video aus Bild | **A** | `videos/fuge-licht` | **Platz fertig** – Datei ablegen genügt |
| V2 | Schraube wird eingedreht | Trockenbau, Seitenkopf | Video aus Bild | **A** | `videos/trockenbau-schrauben` | **Platz fertig** |
| V3 | langsame Fahrt durch den Altbau | Leistungsübersicht, Zeile Trockenbau | Video aus Bild | B | `videos/altbau-durchgang` | **Platz fertig** |
| V4 | Sonne wandert über die Dachschrägen | Trockenbau „Wofür“ | Video aus Bild | C | `videos/dachgeschoss-licht` | **Platz fertig** (Freigabe Dachschrägen offen) |
| V5 | Spachtel zieht über die Ausbesserung | Reparatur, Seitenkopf | Video aus S1 | **A** | `videos/reparatur-spachteln` | **Platz fertig** |
| V6 | Licht im Treppenhaus | Hausmeister, Seitenkopf | Video aus S3 | B | `videos/treppenhaus-licht` | **Platz fertig** |
| V7 | Tür schließt sauber | Leistungsübersicht, Zeile Reparatur | Video aus S2 | C | `videos/tuer-einstellen` | nach S2 |

In der Vorschau markiert ein roter Hinweis **„Video geplant · Name“**, wo ein Clip vorgesehen ist (V1–V6). Die
Kundenansicht blendet ihn aus; in Produktion erscheint er nie.

**Empfohlene Reihenfolge (aktualisiert):** F1 und F2 anstoßen (brauchen Termine) · S4 (Teilen-Vorschau) erzeugen ·
V1, V2, V5 aus den vorhandenen Bildern animieren · danach S5, S6, V6, V3 · S2 nur bei Bedarf.

**Zweite Lieferung (12.10.2026):** Die sechs Bilder aus „Gashini-Bilder.zip“ entsprechen S1, S3, S7, S8, S9 und S10.
Sie sind KI-generiert (die Originaldateien tragen einen C2PA-Nachweis von ChatGPT/OpenAI) und deshalb mit „Symbolbild · KI“ im Bild und „Symbolbild (KI-generiert): …“ im Alt-Text
gekennzeichnet. Die Dateinamen beschreiben das Motiv (statt `reparatur-spachteln` jetzt `wand-ausbessern-spachteln`
usw.), weil Suchmaschinen sie mitlesen. Bei den **Projekten** erscheinen sie bewusst nicht: Dort stehen nur echte,
freigegebene Aufträge – KI-Bilder würden dort einen Auftrag vortäuschen.

---

## 1 · Echte Fotos und Videos (F) – nicht per KI

Allgemein: Smartphone-Hauptkamera (1×, kein Digitalzoom), Raster einschalten, Tageslicht, Lampen an, **kein Blitz**.
Objektiv vorher abwischen. Keine Hausnummern, Klingelschilder, Kennzeichen, Dokumente oder Bildschirme im Bild.
Personen nur mit schriftlicher Einwilligung. Originale unverändert schicken – Zuschnitt und Komprimierung übernimmt die
Entwicklung.

| ID | Briefing |
|---|---|
| **F1** Inhaber | Hochformat 4:5, mindestens 1600 px hoch. Bei einer echten Arbeit (z. B. Platte ansetzen) oder am Fahrzeug, Arbeitskleidung, ruhiger Hintergrund, Blick zur Kamera **oder** natürlich bei der Arbeit. Kamera auf Augenhöhe, 2–3 m Abstand. Fünf bis zehn Varianten, wir wählen gemeinsam aus. |
| **F2** Projekte | je Auftrag: Titelbild (fertiger Raum, Totale, quer), Vorher und Nachher **vom selben Standpunkt** (4:3), 2–4 Prozessbilder (Ständerwerk offen, Anschluss Decke/Boden, Fuge, Türzarge). Vor dem Nachher-Bild aufräumen. Schriftliche Freigabe des Kunden, siehe `docs/ASSET-BRIEFS.md`, Abschnitt A. Ziel: mindestens drei Projekte vor dem Livegang. |
| **F3** Werkzeug | quer 3:2. Richtlatte, Spachtel, Wasserwaage, Akkuschrauber auf einer Platte oder einem Bock, ordentlich nebeneinander, seitliches Tageslicht. Gern von schräg oben. |
| **F4** Fahrzeug | quer 3:2, bedeckter Himmel. Firmenlogo lesbar, **Kennzeichen nicht** (Winkel wählen oder abdecken), keine Hausnummer im Hintergrund. |
| **F5** Fuge | quer 3:2, eine eigene, frisch gespachtelte Fuge, Licht flach von der Seite (Fenster oder Baustrahler seitlich halten). |
| **F6** Vorstellung | quer 16:9, 30–45 s, Smartphone auf Stativ, Ansteckmikrofon, ruhiger Raum oder Baustelle ohne Lärm. Inhalt: wer Sie sind, was Sie machen, was Kunden von Ihnen erwarten können – ohne Superlative. Für die Website braucht es Untertitel (lassen sich aus der Tonspur erstellen) und einen eigenen Abspieler mit Bedienelementen; dieses Video startet **nie** von selbst. |

---

## 2 · KI-Symbolbilder (S)

### So geht's

1. Prompt **auf Englisch** einfügen (die Bild-KIs verstehen ihn so am zuverlässigsten), dahinter den **Stil-Zusatz**.
   Wo das Werkzeug ein Feld für Ausschlüsse hat („negative prompt“), den **Ausschluss-Zusatz** dort eintragen.
2. Seitenverhältnis einstellen (steht beim Motiv). Mindestgröße 1536 px Breite; mehr ist besser.
3. Drei bis vier Varianten erzeugen, mit der **Prüfliste** unten aussortieren.
4. Für die Herkunft notieren: Werkzeug, Datum, Prompt, Konto bzw. Lizenz (für `symbol/HERKUNFT.md` und das Impressum).
5. Datei mit dem Namen aus der Tabelle schicken (PNG oder JPG in voller Größe). Die Entwicklung erzeugt die Varianten
   640/1280/1536, baut das Bild ein und kennzeichnet es.

Werkzeuge: Figma (Bilderzeugung), Midjourney, Adobe Firefly, ChatGPT oder Gemini. Vor der Nutzung prüfen, ob der
Tarif **kommerzielle Nutzung** erlaubt. Sind die Bilder KI-generiert, lautet die Kennzeichnung
**„Symbolbild (KI-generiert)“** – das wird beim Einbau umgestellt.

### Stil-Zusatz (an jeden Bild-Prompt anhängen)

Abgestimmt auf die fünf bereits eingebundenen Symbolbilder: warmes, flaches Morgenlicht, helle Gipsflächen, Hände statt
Gesichter.

```
Photorealistic editorial interior photograph for a German craftsman's website. Warm, low morning sunlight through
tall windows, soft long shadows, a faint haze of fine gypsum dust in the light. Palette: off-white gypsum, warm light
grey, galvanized steel, dark anthracite workwear (#1E2124), one small signal-yellow accent (#FFC93C), for example a tool handle.
Calm, tidy, precise, generous negative space. Full-frame camera, 35-50 mm lens, f/4, natural colour grading,
realistic textures, high detail. No text, no letters, no logos, no brand names, no watermark. No faces - only hands
and forearms. No house numbers, no name plates, no licence plates.
```

### Ausschluss-Zusatz (negative prompt, wo möglich)

```
text, lettering, numbers, logo, brand name, watermark, face, portrait, extra fingers, deformed hands, wooden studs,
floating boards, exposed electrical wiring, open sockets, plumbing work, messy site, rubbish, HDR look,
oversaturated colours, fisheye distortion
```

### Prüfliste für jedes Ergebnis

- **Handwerklich plausibel:** Ständerwerk aus verzinkten Metallprofilen (nicht Holz, wenn Metall gemeint ist); Platten
  liegen am Ständerwerk an und schweben nicht; Schrauben in geraden Reihen; Spachtelklingen gerade; Akkuschrauber mit
  Bit, nicht mit Bohrkrone.
- **Hände:** fünf Finger, natürliche Haltung, Handschuhe passen.
- **Keine Schrift:** Briefkästen, Klemmbretter, Pläne und Displays ohne lesbare oder Fantasie-Schrift.
- **Keine Leistung, die Gashini nicht anbietet:** keine Arbeiten an Elektro-, Gas-, Wasser- oder Heizungsinstallation,
  keine offenen Kabel.
- **Nichts Erkennbares:** keine Gesichter, Marken, Hausnummern, Straßenschilder.
- **Ruhig:** aufgeräumt, kein Müll, keine grellen Farben – sonst passt es nicht neben die vorhandenen Bilder.

### Die Motive

#### S1 · Reparatur – Loch in der Wand wird gespachtelt · **A** · 3:2 · `symbol/wand-ausbessern-spachteln` · ✓ eingebaut

Platz: Seitenkopf der Reparatur-Seite (dort steht jetzt eine Zeichnung). Ausgangsbild für Video V5.

```
Close-up of two hands in grey work gloves repairing a small, palm-sized patched hole in a white painted interior wall
next to a clean white door frame. The right hand pulls a broad stainless filling knife across the fresh white filler,
the left hand holds a small hawk with filler. The patch is slightly lighter than the wall, edges feathered out. Bright,
empty apartment hallway; morning sun rakes across the wall from the left so the texture of the patch is visible.
Horizontal composition, patch on the right third, calm empty wall on the left.
```
Prüfen: Das Loch ist klein und ordentlich (keine Kabel dahinter), die Klinge liegt flach an.

#### S2 · Reparatur – Türband wird eingestellt · **A** · 3:2 · `symbol/reparatur-tuer`

Platz: Leistungskarte 02 der Startseite und Zeile „Reparatur & Instandhaltung“ der Leistungsübersicht (dort jetzt
Zeichnungen). Ausgangsbild für V7.

```
Close-up of a hand in a grey work glove adjusting the upper hinge of a white interior door with a slim hex key.
The door stands half open in a bright hallway with light oak parquet; a cordless screwdriver with a signal-yellow accent
rests on the floor near the door. Classic two-part door hinge with a visible pin, white door frame, soft daylight
from the side, shallow depth of field on the hinge.
```
Prüfen: Das Band sieht echt aus (zwei Teile, Bolzen), der Schlüssel steckt sinnvoll; keine Beschriftung am Werkzeug.

#### S3 · Hausmeisterservice – gepflegtes Treppenhaus · **A** · 3:2 · `symbol/treppenhaus-mehrfamilienhaus` · ✓ eingebaut

Platz: Seitenkopf der Hausmeister-Seite, Leistungskarte 03 der Startseite, Zeile 03 der Leistungsübersicht.
Ausgangsbild für V6.

```
Clean, well-kept stairwell of a German multi-family apartment building: light stone stairs, white painted walls,
a simple dark metal handrail, a neat row of grey letterboxes without any names or numbers on the ground floor, a
large stairwell window with soft daylight, warm light pooling on the landing, freshly swept floor, a signal-yellow
doormat as the only accent. No people. View from the bottom of the stairs looking up diagonally.
```
Prüfen: Briefkästen **ohne** Schrift und Namen, keine Hausnummer, nichts beschädigt.

#### S4 · Teilen-Vorschau (Open Graph) · **A** · 1200 × 630 (1,91:1) · `og/teilen.jpg`

Platz: erscheint, wenn jemand einen Link zur Website in WhatsApp, Facebook, LinkedIn o. Ä. teilt. Fehlt derzeit
ganz. Die KI liefert **nur den Hintergrund**; Logo und Schriftzug werden exakt daraufgesetzt (KI verfälscht Logos).

```
Minimal architectural photograph of a smooth off-white freshly filled drywall surface lit by warm raking side light
from the right, one crisp horizontal shadow line across the lower third, very subtle gypsum texture, large calm and
empty area on the left half for a logo. Nothing else in the frame.
```
Alternative ohne KI: Das Bild lässt sich auch aus der vorhandenen Wandschnitt-Visualisierung bauen.

#### S5 · Schaden mit dem Smartphone fotografieren · B · 3:2 · `symbol/schaden-fotografieren`

Platz: Reparatur-Seite, Abschnitt „Drei Schritte bis zur Antwort“ (Schritt „Foto machen“). Unterstützt die
Foto-Funktion im Anfrageformular.

```
Over-the-shoulder close-up: a hand holds a modern smartphone without any logo and photographs a hairline crack and a
small dent in a white plasterboard wall in a bright domestic hallway. The phone screen shows the same wall section as
a photo preview, no interface text, no icons. Soft daylight, shallow depth of field on the phone.
```
Prüfen: Display ohne Schrift oder Symbole, kein Herstellerlogo.

#### S6 · Mieterwechsel – Wohnung bereit zur Übergabe · B · 3:2 · `symbol/mieterwechsel-wohnung`

Platz: Hausmeister-Seite, Abschnitt „Zwischen zwei Mietverhältnissen“.

```
Empty, freshly prepared rental apartment ready for handover: bright living room with white walls, light wooden floor
swept clean, a freshly repaired spot on the wall that is barely visible, a bunch of keys and a closed grey folder on
the window sill, window slightly open, morning sun casting long window shadows across the floor. No furniture, no
people.
```
Prüfen: kein Klemmbrett mit Fantasie-Schrift (deshalb geschlossene Mappe), keine Möbel.

#### S7 · Netzwerk – Abstimmung am Grundriss · B · 3:2 · `symbol/abstimmung-grundriss` · ✓ eingebaut

Platz: Netzwerk-Seite, Abschnitt „So läuft ein Vorhaben mit mehreren Gewerken“.

```
Top-down view onto a simple work table made of a plasterboard sheet on trestles. On it: a printed architectural floor
plan drawn with clean black lines and no readable text or numbers, a yellow folding ruler, a carpenter's pencil, a
small laser distance meter without brand. Two hands point at the same wall on the plan: one in a grey work glove,
one bare hand of a client with a plain shirt cuff. Soft even daylight.
```
Prüfen: Plan ohne Schrift- und Zahlensalat; zwei verschiedene Personen erkennbar (Handschuh / ohne).

#### S8 · Trockenbau – abgehängte Decke im Bau · B · 3:2 · `symbol/abgehaengte-decke-montage` · ✓ eingebaut

Platz: Trockenbau-Seite, „Wofür“. Ersetzt das Dachgeschoss-Bild, falls Dachschrägen nicht zum Angebot gehören –
abgehängte Decken stehen dagegen ausdrücklich im Leistungsumfang.

```
Room with a suspended ceiling under construction, seen from below at an angle: a grid of galvanized steel ceiling
profiles hung from a concrete ceiling with straight metal hangers, about half of the field already closed with gypsum
plasterboards fixed by neat rows of screws, the open part shows the clean profile grid. A stepladder below, bare white
walls, morning light from a window on the left. No cables hanging down, no light fixtures installed yet.
```
Prüfen: Profile parallel, Abhänger senkrecht, keine herabhängenden Kabel.

#### S9 · Hausmeister – Kontrollgang im Keller · C · 3:2 · `symbol/kontrollgang-kellerflur` · ✓ eingebaut

Platz: Hausmeister-Seite, „Was regelmäßig dazugehört“ (Sichtkontrolle Technik- und Kellerräume).

```
Clean basement corridor of an apartment building with painted walls and simple grey storage doors. A hand in a grey
work glove holds a small flashlight and checks a dry wall corner near the floor; the other hand holds a closed grey
folder. Cool daylight from a small basement window mixed with the warm flashlight beam. No electrical cabinets, no
open pipes, no people's faces.
```

#### S10 · 404-Seite – kleines Loch in heller Wand · C · 16:9 · `symbol/loch-in-der-wand` · ✓ eingebaut

Platz: Fehlerseite „Diese Seite gibt es nicht.“ – mit einem Augenzwinkern, passend zur Reparatur.

```
Minimal photograph of a single small, clean round hole in a smooth white drywall wall, a few gypsum crumbs on the
light floor below, soft daylight from the side, lots of calm empty wall around it.
```

---

## 3 · Kurzvideos (V) – aus einem Standbild animiert

### Warum so

Kurze, ruhige Schleifen machen die Seite lebendig, ohne zu lärmen. Sie werden **aus einem vorhandenen Symbolbild**
erzeugt („Bild zu Video“ bzw. „image to video“): Das Bild ist dann das erste Bild des Clips, Licht und Farben passen
genau, und das Standbild bleibt auf der Website als Ersatz stehen, solange der Clip lädt, bei „Bewegung reduzieren“
und im Datensparmodus.

Werkzeuge mit „Bild zu Video“: Runway, Kling, Google Veo, Luma, Sora. Auch hier: kommerzielle Nutzung im Tarif prüfen,
Herkunft notieren.

### Technische Vorgaben

| | Vorgabe |
|---|---|
| Länge | 5–8 Sekunden, ohne Schnitt |
| Bewegung | langsam und klein: Kamera fast fest, höchstens leichte Fahrt; nur **eine** Sache bewegt sich |
| Format | 16:9 erzeugen (z. B. 1920 × 1080). Hauptmotiv mittig – die Website schneidet je nach Platz auf 3:2 oder 21:9 zu |
| Ton | keiner (die Clips laufen stumm) |
| Schleife | Bewegungen wählen, die ohne Sprung wieder anfangen können (Licht, Kamera-Drift). Der Übergang wird bei der Aufbereitung weich überblendet, oder der Clip läuft vor und zurück |
| Abgabe | Rohdatei als MP4 schicken, Dateiname wie in der Tabelle. Daraus entstehen `name.webm` und `name.mp4` (1280 px breit, je höchstens etwa 2,5 MB) unter `src/assets/videos/` – sobald sie dort liegen, erscheint der Clip beim nächsten Build |

Wer selbst umwandelt (ffmpeg):

```
ffmpeg -i roh.mp4 -t 6 -vf "scale=1280:-2,fps=25" -an -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -movflags +faststart name.mp4
ffmpeg -i roh.mp4 -t 6 -vf "scale=1280:-2,fps=25" -an -c:v libvpx-vp9 -crf 36 -b:v 0 -row-mt 1 name.webm
```

So verhält sich ein Clip auf der Website (bereits eingebaut und getestet):

- Er lädt erst, wenn sein Platz sichtbar wird.
- Er läuft nur dort und pausiert außerhalb.
- Er startet nicht bei „Bewegung reduzieren“ oder im Datensparmodus.
- Rechts unten sitzt ein Pause-Knopf, und angehalten bleibt angehalten.

### Video-Zusatz (an jeden Video-Prompt anhängen)

```
Use the provided image as the exact first frame. Keep composition, light and colours unchanged. Slow, subtle,
realistic motion only; locked-off camera or a very slow dolly (at most 5 % closer). No cuts, no camera shake, no
text, no logos, no faces, no new people entering the frame, no morphing of hands or tools. 6 seconds, 24 fps,
no audio.
```

### Die Clips

#### V1 · Licht wandert über die Fuge · **A** · aus `symbol/fuge-streiflicht` · `videos/fuge-licht`

Platz: Startseite, Bildband unter „Auch kleine Aufträge“ (fertig vorbereitet).

```
The warm sunlight slowly drifts along the freshly filled drywall joint from left to right, the raking light gradually
reveals the fine texture of the filler, a few dust particles float in the light beam. The camera creeps very slowly
towards the joint. Nothing else moves.
```
Variante (lebendiger, mehr KI-Risiko): `A broad filling knife enters from the right and pulls one thin, even layer of
filler along the joint, then leaves the frame.`

#### V2 · Schraube wird eingedreht · **A** · aus `symbol/trockenbau-beplankung` · `videos/trockenbau-schrauben`

Platz: Trockenbau, Seitenkopf (fertig vorbereitet).

```
The worker drives the screw into the plasterboard with the cordless screwdriver: the bit turns, the screw head sinks
flush with the board surface, a tiny puff of gypsum dust. His left hand keeps pressing the board against the stud.
Camera static with a barely noticeable push-in.
```
Prüfen: Bit dreht, Schraube versinkt bündig, Hand bleibt ruhig; Platte bewegt sich nicht.

#### V3 · Fahrt durch den Altbau · B · aus `symbol/innenausbau-altbau` · `videos/altbau-durchgang`

Platz: Leistungsübersicht, Zeile Trockenbau (fertig vorbereitet).

```
Very slow forward dolly through the room towards the open double door; patches of sunlight on the floor shift
slightly, fine dust particles drift in the light. No objects move, the bucket and tools stay where they are.
```

#### V4 · Sonne über den Dachschrägen · C · aus `symbol/dachgeschoss-beplankt` · `videos/dachgeschoss-licht`

Platz: Trockenbau „Wofür“ (fertig vorbereitet; nur sinnvoll, wenn Dachschrägen angeboten werden).

```
Time-lapse feeling: the sunbeams from the roof window slowly wander across the boarded slopes and the floor, clouds
drift past outside the window. Camera completely static.
```

#### V5 · Spachtel zieht über die Ausbesserung · **A** · aus S1 · `videos/reparatur-spachteln`

Platz: Reparatur, Seitenkopf – angelegt; Datei ablegen genügt.

```
The gloved right hand pulls the filling knife once, smoothly and slowly across the patch, leaving an even, slightly
glossy surface; the left hand with the hawk stays still. Camera static.
```

#### V6 · Licht im Treppenhaus · B · aus S3 · `videos/treppenhaus-licht`

Platz: Hausmeister, Seitenkopf – angelegt; Datei ablegen genügt.

```
Late-afternoon light slowly moves across the stair landing, the ceiling lamp of the stairwell softly switches on,
the camera tilts up very slowly along the handrail. No people.
```

#### V7 · Tür schließt sauber · C · aus S2 · `videos/tuer-einstellen`

Platz: Leistungsübersicht, Zeile Reparatur – wird zusammen mit S2 eingebaut.

```
The hand turns the hex key a quarter turn and withdraws; then the half-open door swings gently closed and sits flush
in its frame. Camera static.
```

---

## 4 · Nach der Lieferung

| Schritt | Wer |
|---|---|
| Dateien mit den Namen aus der Tabelle schicken (Bilder in voller Größe, Videos als Roh-MP4) | Betreiber |
| Herkunft je Datei notieren: Werkzeug, Datum, Prompt, Tarif/Lizenz | Betreiber |
| Varianten erzeugen, einbauen, kennzeichnen, `HERKUNFT.md` ergänzen, Tests laufen lassen | Entwicklung |
| `SYMBOLBILD_QUELLE` in `data/firmendaten.env` setzen (erscheint im Impressum) – erst dann ist der Produktions-Build frei | Betreiber |
