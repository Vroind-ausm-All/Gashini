# Creative Direction – Gashini Dienstleistungen

**Leitidee: „Vom Plan zur fertigen Fläche.“**
Gashini arbeitet dort, wo aus einem Plan eine fertige, ruhige Oberfläche wird. Die Website erzählt genau
das. Technische Linien, Maße und Schichten werden Schritt für Schritt zu Material und Raum. Der Stil ist
*Quiet Industrial Luxury*: präzise wie eine Werkzeichnung, ruhig wie eine frisch gespachtelte Wand.
Teuer wirkt sie durch Weglassen, nicht durch Effekte.

---

## 1. Farbe

| Token | Wert | Rolle | Anteil (Richtwert) |
|---|---|---|---|
| `--c-papier` | #FAFAF8 | Grundfläche, „frische Wand“ | ~60 % |
| `--c-papier-2` | #F2F1ED | ruhige Wechselfläche | ~12 % |
| `--c-beton` | #E4E2DD / Rauschen `--beton` | Bühne für Zeichnungen und Visualisierungen | ~8 % |
| `--c-schwarz` | #0E0E0E | Text, dunkle Bühnen (Netzwerk, Fuß) | ~16 % |
| `--c-grau` | #55534F / #6B6863 | Sekundärtext, Bemaßung | – |
| `--c-ziegel` | #B5391C | **Signal**: Maßkette, aktiver Schritt, Fokus, Markierung | ≤ 2 % |
| `--c-ziegel-dunkel` | #8E2A12 | Ziegelrot für Text auf Hell (Kontrast 7,4 : 1) | – |

Regeln: Ziegelrot ist nie Flächenfarbe für große Bereiche und nie Fließtext. Es markiert *eine*
Stelle pro Ansicht: das, worauf das Auge als Nächstes soll. Auf Schwarz wird es zu #E2876B aufgehellt
(Kontrast ≥ 4,5 : 1).

## 2. Typografie

- **Instrument Sans (variabel, lokal):** Überschriften schmal (`font-stretch` 76–84 %, Gewicht 520–580) und
  leicht negativ gesperrt; Fließtext normal breit, Gewicht 400, 17 px, Zeilenhöhe 1,65.
- **IBM Plex Mono (lokal):** Labels, Maße, Nummerierungen, Bildunterschriften. Sie ist die Stimme der
  Zeichnung, nie für längere Texte.
- Display-Größen bis 6,5 rem nur in Bühnen (Startseite, Seitenköpfe); sonst gilt die Skala `--t-*`.
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
| **Plan** | Technische Zeichnungen: Ansicht, Schnitt, Grundriss, Detail. Linien 1 px, Maße in Plex Mono, ein Ziegelrot-Akzent. | „Schematische Darstellung“ | überall, wo Abläufe und Aufbauten erklärt werden |
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
| Scroll-Kopplung | nur in den drei Signature Motions (`scrub`) |
| Engine | GSAP 3.15 (Core, ScrollTrigger, SplitText, DrawSVG, Flip) – lokal ausgeliefert |

**Drei Signature Motions:**

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
| Netzwerk | dunkle Bühne mit Diagramm | Zuständigkeiten · Vertragsmodelle · Ablauf mit Partnern | „Sie wissen vorher, wer was macht“ | Vorhaben mit mehreren Gewerken |
| Kontakt | Seitenkopf | Formular · Direktwege · Einsatzgebiet | FAQ vor der Anfrage | – |
| Fragen | Seitenkopf | Themengruppen · Ablauf | – | Frage nicht dabei? |
| Danke, 404, Rechtliches | ruhig | – | ganz | – |

## 8. Barrierefreiheit und Leistung (Budgets)

- WCAG 2.2 AA: Kontraste ≥ 4,5 : 1, Fokus immer sichtbar (2 px Ziegelrot), Zielgrößen ≥ 44 px, alle
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
| **GSAP** (ScrollTrigger, SplitText, DrawSVG, Flip) | deckt alle drei Signature Motions ab, robust, CSP-tauglich (kein `eval`), seit 3.13 kostenlos | ca. 52 KB gzip (Flip nur auf der Projektseite) | **eingesetzt** |
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
