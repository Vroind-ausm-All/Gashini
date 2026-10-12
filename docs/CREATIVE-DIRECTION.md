# Creative Direction – Gashini Dienstleistungen

**Leitidee: „Vom Plan zur fertigen Fläche.“**
Gashini arbeitet dort, wo aus einem Plan eine fertige, ruhige Oberfläche wird. Die Website erzählt genau
das. Technische Linien, Maße und Schichten werden Schritt für Schritt zu Material und Raum. Der Stil ist
*Quiet Industrial Luxury*: präzise wie eine Werkzeichnung, ruhig wie eine frisch gespachtelte Wand.
Teuer wirkt sie durch Weglassen, nicht durch Effekte.

---

## 1. Farbe

Seit Oktober 2026 gilt das Logo-Paket mit Markenblatt (`brand/markenblatt.pdf`): Anthrazit, Signalgelb, Kalkweiß.
Ziegelrot und die frühere Wortmarke sind abgelöst. Details und Kontrastwerte: `brand/styleguide.md`.

| Token | Wert | Rolle | Anteil (Richtwert) |
|---|---|---|---|
| `--c-kalk` | #F4F2ED | Grundfläche, „frische Wand“ (Kalkweiß) | ~60 % |
| `--c-kalk-2` | #EBE8E1 | ruhige Wechselfläche, Bühne der Visualisierungen | ~12 % |
| `--c-beton` | #E1DDD5 / Rauschen `--beton` | Bühne für Zeichnungen | ~8 % |
| `--c-anthrazit` | #1E2124 | Text, Schaltflächen, dunkle Bühnen (Netzwerk, Fuß) | ~16 % |
| `--c-text-2` / `--c-text-3` | #4F5358 / #62666B | Sekundärtext, Bemaßung | – |
| `--c-gelb` | #FFC93C | **Signal**: das Band – unter Schaltflächen, vor Labels, unter Nummern, aktive Seite, Flächen in Zeichnungen | ≤ 3 % |

Regeln: Signalgelb ist auf hellem Grund **nie Textfarbe** (1,4 : 1) – es liegt als Band, Fläche oder Linie unter oder
neben anthrazitfarbenem Text, genau wie das Band unter dem G im Signet. Auf Anthrazit ist Gelb auch als Text
lesbar (10,5 : 1). Fehlermeldungen nutzen ein funktionales Rot (#B3261E), das nicht zur Marke gehört.

## 2. Typografie

- **Archivo (variabel, lokal)** ist die einzige Schrift – dieselbe Familie wie im Logo. Überschriften Gewicht ~560,
  leicht negativ gesperrt; Fließtext 400, 17 px, Zeilenhöhe 1,65. Archivo läuft breiter als die frühere schmale
  Schrift, deshalb ist die Größenskala `--t-2xl` bis `--t-4xl` kleiner angesetzt.
- **Labels** in Versalien mit Laufweite 0,16 em und gelbem Band davor – das Echo von „DIENSTLEISTUNGEN“ im Logo.
- Nummern, Maße und Bildunterschriften ebenfalls in Archivo; Nummern bekommen einen gelben Unterstrich.
- Zeilenlänge im Fließtext höchstens 66 Zeichen.

## 3. Raster und Rhythmus

12 Spalten, maximal 1320 px, Randabstand `clamp(20px, 4.2vw, 56px)`. Abschnitte atmen mit
`clamp(72px, 9vw, 144px)`. Jede Seite wechselt bewusst zwischen drei Dichten:

1. **Bühne:** große Typografie oder großes Bild, wenig Text.
2. **Arbeitsfläche:** Inhalt, Listen, Tafeln, Formulare.
3. **Ruhezone:** ein Satz, viel Weißraum, keine Bewegung.

Kein Abschnittstyp erscheint zweimal direkt hintereinander.

## 4. Bildsprache

Drei Ebenen, die aufeinander aufbauen und sich nie vermischen:

| Ebene | Was | Kennzeichnung | Wo |
|---|---|---|---|
| **Plan** | Technische Zeichnungen: Ansicht, Schnitt, Grundriss, Detail. Linien 1 px in Anthrazit, Maße in Archivo, Akzent als gelbe Fläche oder breite gelbe Linie. | „Schematische Darstellung“ | überall, wo Abläufe und Aufbauten erklärt werden |
| **Material** | Visualisierungen, gerendert aus derselben 3D-Szene wie das interaktive Wandmodell: Stahlprofil, Mineralwolle, Gipsplatte, Spachtel, fertige Fläche. Nahaufnahmen, Streiflicht, gedeckte Farben. | „Visualisierung – kein Projektfoto“ | Hero, Leistungsseiten, Leistungsübersicht |
| **Wirklichkeit** | Eigene Fotos echter Arbeiten (später). Tageslicht, ruhige Ausschnitte, keine Menschen ohne Einwilligung. | Bildnachweis im Impressum, Freigabe in `projekte.json` | Projekte, Über uns |

- **Kein Stockfoto, kein KI-Bild als Projekt.** KI-generierte Symbolbilder sind nur als „Symbolbild
  (KI-generiert)“ zulässig und nie auf Projekt- oder Über-uns-Seiten.
- **Symbolbilder (seit 11.10.2026):** Fünf vom Betreiber bereitgestellte Fotos typischer Trockenbau-Situationen
  ergänzen die Material-Ebene: Titelbild und Bildfolge auf der Trockenbau-Seite, Altbau in der Leistungsübersicht,
  Fugen-Detail auf der Startseite. Sie tragen eine Marke „Symbolbild“ im Bild, „Symbolbild:“ im Alt-Text und
  „Kein Projektfoto.“ in der Unterschrift. Quelle und Lizenz sind noch offen (`SYMBOLBILD_QUELLE`); sind die Bilder
  KI-generiert, lautet die Kennzeichnung „Symbolbild (KI-generiert)“. Herkunft: `src/assets/bilder/symbol/HERKUNFT.md`.
- **Kurzvideos:** stumme Schleifen von 5–8 Sekunden, aus einem Symbolbild animiert, liegen über diesem Standbild.
  Sie bewegen sich langsam und nur in einer Sache (Licht, Schraube, Spachtel), laden erst im Sichtbereich, starten nicht
  bei „Bewegung reduzieren“ oder Datensparen und haben einen Pause-Knopf. Plätze und Prompts: `docs/MEDIENLISTE.md`.
- **Fotobriefings statt Leerstellen:** Wo ein echtes Foto hingehört, steht in der Vorschau ein Briefing
  (Motiv, Format, Licht). In Produktion erscheint stattdessen das passende Material- oder Planbild.
- Prompts für Midjourney und ein Briefing für die Texterstellung stehen in `docs/ASSET-BRIEFS.md`.

## 5. Motion-System

**Prinzip:** Bewegung erklärt Aufbau, sie dekoriert nicht. Alles bewegt sich, wie Material sich bewegt:
gerade, gedämpft, mit Gewicht. Nichts federt, nichts dreht sich um seiner selbst willen.

| Parameter | Wert |
|---|---|
| Hauptkurve | `power3.out` (CSS: `cubic-bezier(.2,.7,.2,1)`) |
| Dauer Reveal | 0,7–0,9 s, Versatz 0,06–0,08 s |
| Dauer Interaktion | 0,2 s |
| Scroll-Kopplung | nur in den Signature Motions (`scrub`) sowie für Fortschrittslinien und den Leitsatz der Netzwerk-Seite |
| Engine | GSAP 3.15 (Core, ScrollTrigger, SplitText, DrawSVG, Flip) – lokal ausgeliefert |

**Vier Signature Motions:**

1. **Architectural Hero (Startseite):** Die Überschrift baut sich zeilenweise aus Masken auf (SplitText).
   Parallel zieht die Bemaßung ihre Linien (DrawSVG) und die Material-Visualisierung öffnet sich von unten
   wie eine Wand, die beplankt wird. Beim Scrollen wandern die Beschriftungen leicht gegeneinander,
   ohne Parallax-Kitsch.
2. **Wall Construction Experience (Startseite und Trockenbau):** Ein interaktives Three.js-Modell zeigt
   einen *beispielhaften* Wandaufbau in vier Schritten: Profile, Dämmung, Beplankung, Spachtel und
   Oberfläche. Steuerung über Schaltflächen und auf großen Bildschirmen zusätzlich über den Scrollfortschritt.
   Ohne WebGL, ohne JavaScript, bei reduzierter Bewegung und als leichte Variante auf Mobilgeräten gibt es
   dieselben Schritte als gezeichnete Explosionsdarstellung.
3. **Project Reveal (Projekte):** Projektbilder öffnen sich mit einer Maske entlang der Bildkante.
   Der Filter ordnet Karten mit Flip um. Vorher/Nachher ist ein echter Regler (Tastatur, Screenreader).
4. **Netzwerk-Geschichte (Netzwerk-Seite):** Das Schema bleibt stehen, fünf Schritte ziehen vorbei – Ihr Vorhaben,
   ein Ansprechpartner, was wir selbst ausführen, wo Fachbetriebe dazukommen, wer Vertragspartner ist. Das Netz
   wächst an den Scrollfortschritt gekoppelt (DrawSVG für eigene Linien, Einblenden für die gestrichelten
   Beispiel-Gewerke), im letzten Schritt leuchtet die eigene Leistung gelb und die Legende erscheint. Ein gelbes
   Band neben den Schritten zeigt den Fortschritt, der aktive Schritt ist hervorgehoben (inaktive auf 62 %,
   damit der Kontrast AA hält). Ohne JavaScript, auf niedrigen Bildschirmen und bei reduzierter Bewegung steht
   das vollständige Schema mit einer gewöhnlichen Liste da. Dazu färbt sich der Leitsatz Wort für Wort ein
   (von #84888D – 3,2 : 1, genug für große Schrift – zur eigenen Farbe) und der Ablauf bekommt eine Fortschrittslinie.

**Tiefe (Maus, ergänzend zu den Signature Motions):** Im Seitenkopf liegen hinter dem Inhalt zwei weiche
Lichtflächen, feine Konstruktionslinien im Achsmaß-Rhythmus mit einer gestrichelten Schräge und ein kurzes gelbes
Band. Sie sind nur rechts der Textspalte und oberhalb von Bildunterschriften sichtbar (CSS-Masken) und verschieben
sich bei Mausbewegung um wenige Pixel gegeneinander (Lichtfläche bis 22 px, Linien bis 8 px). Auf den
Leistungskarten neigt sich nur die Bildfläche (höchstens 3,5°), das Bild gleitet leicht dagegen, ein Schatten
gibt Tiefe; Titel, Text und Link bleiben ruhig. Über der Bildfläche wandert ein weicher Lichtakzent (radialer
Verlauf, nur Deckkraft und Position) mit dem Zeiger. Technik: `gsap.quickTo` auf transform-Werte, ausgelöst nur von
Mausbewegungen und pro Bild gebündelt (`requestAnimationFrame` – mehrere Zeigerereignisse eines Bildes ergeben
eine Rechnung); Fenster- und Kartenmaße werden beim Betreten bzw. nach Scroll und Größenänderung gemessen, nie im
Bewegungspfad. Ruht die Maus, ruht alles; keine Schleife, kein Canvas, kein WebGL, keine neue Bibliothek.

**Karte „Einsatzgebiet“:** Punkte reagieren auf Überfahren und Fokus (vergrößert, dunkleres Gelb, Name erscheint),
der gewählte Ort wird groß und gelb mit anthrazitfarbener Kontur, bei gewähltem Landkreis treten die übrigen Orte
zurück. Alles über `transform` und Farbe, ohne Übergang bei reduzierter Bewegung. Nur bei
`(hover: hover) and (pointer: fine)` und erlaubter Bewegung; auf Touch-Geräten, bei reduzierter Bewegung, auf
Kontakt- und Rechtsseiten gibt es weder Ebene noch Bewegung (Kontaktseiten: keine Ebene).

**Ruhezonen:** Formulare, Rechtstexte, FAQ-Antworten, Fußbereich und jeweils mindestens ein Abschnitt pro
Seite bewegen sich nie.

**Reduzierte Bewegung:** Bei `prefers-reduced-motion: reduce` laufen keine GSAP-Animationen. Inhalte
stehen sofort, das 3D-Modell wechselt ohne Übergang. **Ohne JavaScript** ist jeder Inhalt sichtbar.
Nichts ist per CSS versteckt, solange das Skript nicht geladen ist; nach spätestens 2,5 s greift eine
CSS-Sicherung.

## 6. Komponenten

| Komponente | Zweck |
|---|---|
| `buehne` | Startseiten-Hero: Display-Typografie und Visualisierung mit Beschriftung |
| `seitenkopf` (Varianten: hell, mit Bild, dunkel) | Einstieg der Unterseiten |
| `leistungskarten` | bildgeführte Leistungsübersicht, große Fläche je Leistung |
| `wandaufbau` | Signature 2 – 3D-Modell mit Schritten, SVG-Rückfall |
| `tafel` | Zeichnung oder Visualisierung mit nummerierter Legende |
| `faelle` | Alltagsbeispiele mit direktem Weg ins Formular |
| `pflegeplan` | Hausmeister: Intervalle als Zeitleiste |
| `netzwerk-diagramm` | animierte Zuständigkeiten, ohne Partnerzahlen |
| `vertragsmodelle` | drei Formen der Zusammenarbeit |
| `schritte` | Ablauf in vier Schritten |
| `projektraster`, `projektbericht`, `vergleich` | Projekte, Detail, Vorher/Nachher |
| `leerzustand` | gestaltete Lücke mit Aufgabe |
| `fotobriefing` | nur Vorschau: Briefing für ein fehlendes Foto |
| `abschluss` (seitenspezifisch) | passende nächste Handlung |
| `formular` | Anfrage mit Rückruf und Fotos |
| `randnotiz` (`redaktion`) | offener Punkt zur Freigabe, aufklappbar |

## 7. Seiten-Dramaturgie

| Seite | Bühne | Arbeitsfläche | Ruhezone | Abschluss |
|---|---|---|---|---|
| Start | Architectural Hero | Leistungskarten · Wandaufbau 3D · Projekte · Netzwerk (dunkel) · 4 Schritte | „Auch kleine Arbeiten“ | „Was können wir für Sie umsetzen?“ |
| Leistungen | Seitenkopf | drei große Leistungsflächen mit Bild · Koordination · Abgrenzung | Grundsatz „Wir sagen, was wir nicht machen“ | Leistung wählen |
| Trockenbau | Seitenkopf mit Visualisierung | Wandaufbau 3D · Anwendungen als Tafel · Vorbereitung · Abgrenzung · FAQ | Besichtigung ja/nein | Trockenbau anfragen |
| Reparatur | Seitenkopf mit Detailbild | **Alltagsfälle** mit Direktanfrage · Ablauf in 3 Schritten · Abgrenzung · FAQ | „Lohnt sich das?“ | Foto schicken, Rückruf |
| Hausmeister | Seitenkopf mit Grundriss | Objektrundgang (Grundriss) · Pflegeplan · Mieterwechsel · Abgrenzung · FAQ | Ein Ansprechpartner | Objekt beschreiben |
| Projekte | Seitenkopf | Raster mit Reveal und Flip-Filter oder gestalteter Leerzustand | Dokumentationsgrundsätze | Vorhaben anfragen |
| Projektdetail | Titelbild | Ausgangssituation · Aufgabenstellung · Ausgeführte Arbeiten · Prozessbilder · Ergebnis · Vorher/Nachher | Projektdaten | „Ähnliches Vorhaben?“ |
| Über uns | Editorial-Kopf | Inhaber · Arbeitsweise · Fotobriefings | Zitatfreie Grundsätze | Kennenlernen |
| Netzwerk | dunkler Kopf, Netzwerk-Geschichte (Scroll) | Zuständigkeiten · Vertragsmodelle · Ablauf mit Partnern | „Sie wissen vorher, wer was macht“ | Vorhaben mit mehreren Gewerken |
| Kontakt | Seitenkopf | Formular · Direktwege · Einsatzgebiet | FAQ vor der Anfrage | – |
| Fragen | Seitenkopf | Themengruppen · Ablauf | – | Frage nicht dabei? |
| Danke, 404, Rechtliches | ruhig | – | ganz | – |

## 8. Barrierefreiheit und Leistung (Budgets)

- WCAG 2.2 AA: Kontraste ≥ 4,5 : 1, Fokus immer sichtbar (3 px Anthrazit, auf dunklem Grund Gelb), Zielgrößen ≥ 44 px, alle
  Interaktionen mit Tastatur, 3D-Modell mit gleichwertiger Textfassung.
- Lighthouse ≥ 90 in allen Kategorien, LCP < 2,5 s, CLS < 0,1, INP < 200 ms.
- Startseite ohne 3D: HTML + CSS + JS + Schriften ≤ 200 KB gzip, Hero-Bild ≤ 120 KB.
- Three.js wird erst geladen, wenn das Modell in die Nähe des Sichtbereichs kommt, und blockiert nie das
  erste Rendern.

## 9. Technologieentscheidungen

**Architektur: statischer Python-Generator bleibt.** Ein Wechsel zu Astro, React oder Next.js brächte
Komponenten-Syntax und ein Ökosystem. Er brächte aber auch Node-Abhängigkeiten im Build, Update-Pflege und
Hydration-Code, der nur Gewicht wäre. Alles Geforderte ist ohne Framework umsetzbar: Mehrseitigkeit,
Projekt-Datenmodell, Formular, eine 3D-Szene als Insel, GSAP. Der Wartungsaufwand eines kleinen Betriebs
spricht klar für statische Dateien auf einfachem Hosting. Ergebnis: **kein Wechsel**. Die 3D-Szene wird
mit einem kleinen, versionierten Entwicklungswerkzeug gebündelt (`scripts/werkzeuge/3d`). Ihr Ergebnis
wird eingecheckt, die Website selbst baut weiterhin ohne Node.

**Bewertung zusätzlicher Werkzeuge:**

| Werkzeug | Nutzen hier | Kosten/Risiko | Entscheidung |
|---|---|---|---|
| **GSAP** (ScrollTrigger, SplitText, DrawSVG, Flip) | deckt alle Signature Motions ab, robust, CSP-tauglich (kein `eval`), seit 3.13 kostenlos | ca. 52 KB gzip (Flip nur auf der Projektseite) | **eingesetzt** |
| **Three.js** | eine Szene: der Wandaufbau | ca. 130 KB gzip, nur bei Bedarf nachgeladen | **eingesetzt (einmal)** |
| **Lenis** | weiches Scrollen | verändert natives Scrollverhalten (Tastatur, Anker, Bildschirmlupe, Trägheit auf Touch); widerspricht der Vorgabe, Bedienbarkeit nicht zu verschlechtern | **abgelehnt** |
| **Spline** | 3D-Editor mit Laufzeit | Laufzeit > 500 KB, Szenen auf fremden Servern oder als Blackbox-Export, schwer barrierefrei, keine Kontrolle über Geometrie und Kennzeichnung | **abgelehnt** |
| **Rive** | zustandsbasierte Vektoranimation | WASM-Laufzeit braucht `wasm-unsafe-eval` in der CSP, Animationen außerhalb des Repos, kein Anwendungsfall, den GSAP + SVG nicht lösen | **abgelehnt** |
| **Motion (motion.dev)** | Animationsbibliothek | doppelt zu GSAP, zweites Bewegungsvokabular | **abgelehnt** |

**Bilder:** Die geplante KI-Bildgenerierung (Figma) war technisch nicht abrufbar, weil die Netzwerkrichtlinie
der Entwicklungsumgebung `www.figma.com` sperrt. Deshalb besteht die Material-Ebene aus eigenen Renderings
der 3D-Szene. Ihre Herkunft ist vollständig nachvollziehbar und rechtlich unbedenklich; sie stehen in
`src/assets/bilder/visualisierung/HERKUNFT.md`. Am 11.10.2026 hat der Betreiber fünf Fotos bereitgestellt, die als
gekennzeichnete Symbolbilder eingebunden sind (siehe Abschnitt 4).
