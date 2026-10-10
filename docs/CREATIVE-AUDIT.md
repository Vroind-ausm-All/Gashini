# Creative-Quality-Audit – Gashini Dienstleistungen

Stand: 10.10.2026 · Grundlage: Branch `claude/relaunch-premium`, Commit 9e5bab7 (vor dem Premium-Relaunch).
Geprüft aus Sicht eines anspruchsvollen Auftraggebers: alle Seiten bei 1440 px und 390 px, mit Tastatur,
ohne JavaScript und mit reduzierter Bewegung. Screenshots des Ausgangszustands: lokal erstellt, nicht eingecheckt.

## Ausgangslage in einem Satz

Technisch solide (Formular-Backend, Tests, CSP, Produktionssperre), gestalterisch ein gut gesetztes
Textdokument: Es fehlen Bildsprache, Dramaturgie und Interaktion. So wirkt die Seite eher wie ein sauberer
Prototyp als wie ein Premium-Auftritt.

## Die zehn wichtigsten Schwächen

| # | Schwäche | Wirkung beim Kunden | Priorität | Maßnahme im Relaunch | Status |
|---|----------|---------------------|-----------|----------------------|--------|
| 1 | **Keine Bildsprache.** Unterseiten sind reine Textseiten; der Hero zeigt eine kleine Strichzeichnung. | „Da ist noch nichts fertig.“ Leistungen sind nicht vorstellbar. | sehr hoch | Eigenes Bildsystem aus drei Ebenen: technische Zeichnung, Material-Visualisierung (aus der 3D-Szene gerendert, gekennzeichnet) und später echte Fotos über Fotobriefings. Bilder auf jeder Leistungsseite. | behoben |
| 2 | **Ein einziges Layoutmuster.** Fast jeder Abschnitt ist ein 4/8-Split aus Überschrift links und Liste rechts. | Monoton, keine Führung, alles gleich wichtig. | sehr hoch | Komponentenbibliothek mit klar unterschiedenen Abschnittstypen: Bühne, Tafel mit Legende, Fallkarten, Schichtaufbau, Pflegeplan, Netzwerkdiagramm, Editorial-Spalte, Ruhefläche. Jede Seite hat eine eigene Dramaturgie. | behoben |
| 3 | **Redaktionskästen wirken wie Fehlermeldungen.** Rot gestrichelte Boxen mitten im Inhalt. | In einer Kundenpräsentation sieht es aus wie kaputt. | hoch | Hinweise werden zu dezenten, aufklappbaren Randnotizen „Offener Punkt“. In der Vorschau gibt es den Schalter „Kundenansicht“, der alle Hinweise ausblendet. Die Produktionssperre bleibt bestehen. | behoben |
| 4 | **Identischer Abschluss auf jeder Seite.** Immer „Was steht bei Ihnen an?“ mit demselben Knopf. | Generisch, keine passende nächste Handlung. | mittel | Abschlüsse pro Seite: Text, Knopf und vorausgewählte Leistung (`/kontakt/?leistung=…`) passen zur Seite. Auf der Startseite steht die Frage „Was können wir für Sie umsetzen?“. | behoben |
| 5 | **Platzhalter in eckigen Klammern** ([Ort], [Telefon]) mitten in Überschriften. | Unfertig, unprofessionell. | hoch | Die Vorschau zeigt nicht bestätigte Angaben als neutrale, gestrichelt unterlegte Marke ohne Klammern. Der Produktions-Build bricht weiterhin ab, solange Angaben fehlen. | behoben |
| 6 | **Die Projektseite ist ein Loch.** Leerer Zustand ohne Gestaltung; die Beispielprojekte bestehen nur aus grauen SVG-Flächen. | Größter Vertrauensverlust: „keine Referenzen“. | sehr hoch | Gestalteter Leerzustand, der erklärt, wie dokumentiert wird. Er zeigt den Ablauf eines künftigen Projektberichts und lenkt auf die Leistungen um. Projektdetail mit Titelbild, Ausgangssituation, Aufgabenstellung, ausgeführten Arbeiten, Prozessbildern, Ergebnis, Vorher/Nachher und Anfrage. Flip-Filter ab 6 Projekten. Keine erfundenen Referenzen. | behoben |
| 7 | **Über uns und Netzwerk sind schwach.** Grauer „Porträt folgt“-Kasten; das Netzwerk ist nur ein Textabschnitt. | Kein Gesicht, kein Beleg für das Alleinstellungsmerkmal „ein Ansprechpartner, viele Gewerke“. | hoch | Über uns als Editorial-Seite mit Fotobriefings (nur in der Vorschau sichtbar, Ersatzbild in Produktion). Eigene Seite „Netzwerk & Zusammenarbeit“ mit animierter Netzwerkdarstellung ohne erfundene Partnerzahlen und drei Vertragsmodellen. | behoben |
| 8 | **Keine Bewegungsdramaturgie, kaum Interaktion.** Nur eine CSS-Linienanimation, sonst statisch. | „Template-Website“, keine Premium-Erfahrung. | hoch | GSAP als einziges Animationssystem mit drei Signature Motions: Architectural Hero, Wall Construction Experience (Three.js) und Project Reveal. Dazu ruhige Reveals, bewusst bewegungsfreie Zonen und reduzierte Bewegung vollständig respektiert. | behoben |
| 9 | **Kleinaufträge ohne Alltag, Anfrageweg zu schwer.** Die Reparaturseite listet Kategorien statt konkreter Fälle; das Formular hat weder Fotos noch Rückruf noch Vorauswahl. | Der Kunde mit der klemmenden Tür fühlt sich nicht angesprochen. | sehr hoch | Fallkarten mit Alltagsbeispielen, die jeweils direkt mit vorausgewählter Leistung ins Formular führen. Formular mit Rückrufwunsch (Zeitfenster), Bild-Upload (bis 3 Fotos), PLZ und Wunschzeitraum. | behoben |
| 10 | **Markenbrüche und Struktur.** Druckvorlagen laden Google Fonts (Barlow/Inter) statt der Hausschriften. „Ablauf“ ist als Seite unklar benannt, das Netzwerk fehlt in der Navigation. | Uneinheitlicher Auftritt, Datenschutzrisiko bei den Druckvorlagen. | mittel | Druckvorlagen auf die lokale Instrument Sans und IBM Plex Mono umgestellt. „Ablauf“ wird zu „Fragen & Ablauf“ unter `/fragen/` (301 von `/ablauf/`), das Netzwerk steht in der Hauptnavigation. | behoben |

## Was bewusst so bleibt

- **Statische Architektur mit Python-Generator.** Begründung in `docs/CREATIVE-DIRECTION.md`, Abschnitt 9.
- **Keine erfundenen Inhalte.** Es gibt weder Projekte noch Partnerzahlen, Bewertungen oder Qualifikationen. Fehlt der Inhalt, entsteht eine gestaltete Lücke mit klarer Aufgabe für den Inhaber – kein Füllmaterial.
- **Produktionssperre.** Offene Angaben, Redaktionshinweise und Beispieldaten verhindern weiterhin den Produktions-Build.

## Nachprüfung

Die Behebung ist in `docs/TESTREPORT.md` dokumentiert: Browser-Tests, axe-core, Screenshots bei 390, 768 und 1440 px,
Leistungsmessung. Offene Punkte, die nur der Inhaber lösen kann, stehen in `docs/RELAUNCH-PLAN.md`.
