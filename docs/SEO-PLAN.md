# SEO-Plan: Raum Stuttgart (30 km)

Stand: 12.10.2026. Ziel: gefunden werden von Menschen in Stuttgart und im Umkreis von etwa 30 Kilometern, die eine
konkrete Arbeit an ihrer Immobilie vergeben wollen. Es geht nicht um möglichst viele Suchbegriffe, sondern um die
richtigen – und um Anfragen aus dem Gebiet, das der Betrieb tatsächlich anfährt.

> **Ehrlich vorweg:** Niemand kann Platzierungen garantieren. Für „Trockenbau Stuttgart“ oder „Hausmeisterservice
> Stuttgart“ gibt es viele etablierte Anbieter. Die Website ist jetzt technisch und inhaltlich so aufgestellt, dass sie
> für diese Suchen in Frage kommt. Ob und wie schnell sie nach oben kommt, entscheiden vor allem drei Dinge außerhalb des
> Codes: das **Google-Unternehmensprofil**, **Bewertungen** und **überall gleiche Firmendaten** (Abschnitte 7 und 8).
> Realistisch sind erste Effekte nach einigen Wochen, stabile Platzierungen nach mehreren Monaten.

## 1. Ausgangslage

- Es gibt noch **keine Live-Domain und keine Suchmaschinen-Historie**.
- Das **Einsatzgebiet ist bestätigt**: Stuttgart und etwa 30 km Umkreis (Vorgabe des Betreibers, 12.10.2026).
  Es steht in `data/firmendaten.env` (`REGION`, `EINSATZGEBIET`) und mit allen Orten in `data/einsatzgebiet.json`.
- **Offen** sind Anschrift, Telefonnummer und Domain. Ohne Anschrift gibt es keinen Eintrag in Google Maps. Die
  Platzierung dort hängt laut Google von *Relevanz*, *Entfernung* und *Bekanntheit* ab, die Entfernung wird ab der
  Adresse im Unternehmensprofil gemessen. Liegt der Firmensitz nicht in Stuttgart selbst, ist das kein Hindernis für die
  Website, wohl aber für die Kartenergebnisse in weiter entfernten Stadtteilen.
- `{{ORT}}` bleibt der **Firmensitz** (Impressum, „Über uns“). „Stuttgart“ in Titeln und Überschriften beschreibt das
  **Einsatzgebiet** und steht deshalb direkt in den Seitenquellen.

## 2. Was umgesetzt ist

| Bereich | Umsetzung | Wo |
|---|---|---|
| Titel und H1 | „Stuttgart“ im Titel jeder Leistungsseite und der Startseite, in der H1 aller drei Leistungsseiten | `src/seiten/*.html` |
| Beschreibungen | jede Seite mit eigener Beschreibung (130–160 Zeichen), Ortsbezug, wo er passt | Kopfdaten der Seiten |
| Seite „Einsatzgebiet“ | `/einsatzgebiet/`: Karte (eigene Zeichnung, Ringe 10/20/30 km), alle 23 Stadtbezirke, 47 Orte nach Landkreis, Leistungen, Fragen | `src/seiten/einsatzgebiet.html`, `data/einsatzgebiet.json` |
| Abschnitt „Einsatzgebiet“ | auf Startseite und den drei Leistungsseiten mit **eigener** Überschrift („Trockenbau in Stuttgart und Umgebung“ …) und eigenem Satz, dazu neun größere Orte und der Link zur Gebietsseite | Baustein `[[einsatzgebiet-band]]` |
| Interne Links | Fußbereich („Einsatzgebiet Stuttgart & Umgebung“) auf jeder Seite, mobiles Menü, Kontaktseite, FAQ | `scripts/build-site.py` |
| Strukturierte Daten | Unternehmen mit Einsatzgebiet, je Leistungsseite ein `Service`, Brotkrumen, FAQ (Abschnitt 5) | Generator und `scripts/firmendaten.py` |
| Bilder | sprechende Dateinamen, beschreibende Alt-Texte, Kennzeichnung der Symbolbilder (Abschnitt 6) | `src/assets/bilder/symbol/` |
| Sitemap | neue Seite automatisch enthalten, `lastmod` aus `STAND_ISO` | `sitemap.xml` |
| Prüfung | `tests/pruefen.py` → „Lokale SEO“: Stuttgart in Titeln und H1, gültiges JSON-LD, Gebietsseite überall verlinkt, keine Ortsnamen in Alt-Texten von Symbolbildern; der Generator bricht ab, wenn ein Ort außerhalb von 30 km eingetragen wird | |

## 3. Suchbegriffe und Zielseiten

Eine Suchintention, eine Seite. Keine Seite bedient zwei Intentionen, keine zwei Seiten dieselbe.

| Prio | Suchintention | Typische Suchanfragen | Zielseite |
|---|---|---|---|
| 1 | Trockenbau vor Ort | „trockenbau stuttgart“, „trockenbauer stuttgart“, „trockenbau firma stuttgart“ | `/leistungen/trockenbau/` |
| 1 | Hausmeisterservice vor Ort | „hausmeisterservice stuttgart“, „hausmeister mehrfamilienhaus stuttgart“, „objektbetreuung stuttgart“ | `/leistungen/hausmeisterservice/` |
| 1 | Kleinreparaturen | „kleinreparaturen stuttgart“, „handwerker für kleine arbeiten stuttgart“, „loch in der wand reparieren stuttgart“ | `/leistungen/reparatur-und-instandhaltung/` |
| 2 | Konkrete Trockenbauarbeit | „trennwand einziehen stuttgart“, „decke abhängen lassen“, „vorsatzschale bad“ | `/leistungen/trockenbau/` |
| 2 | Mieterwechsel | „wohnung für neue mieter herrichten stuttgart“ | `/leistungen/hausmeisterservice/#mieterwechsel` |
| 2 | Umlandorte | „trockenbau esslingen“, „hausmeisterservice ludwigsburg“, „handwerker böblingen“ … | `/einsatzgebiet/` und die Leistungsseiten (Ort im Text) |
| 3 | Alles aus einer Hand | „handwerker koordination gewerke stuttgart“ | `/netzwerk/` |
| – | Marke | „gashini“, „gashini dienstleistungen“ | `/` – Fahrzeug, Flyer und Profil erzeugen genau diese Suche |

**Bewusst nicht:** eigene Seiten je Umlandort mit ausgetauschtem Ortsnamen („Trockenbau Esslingen“, „Trockenbau
Ludwigsburg“ …). Google wertet solche Seiten als *Doorway Pages* ab, und bei einem Radius von 30 km bringen sie kaum
Anfragen. Die Umlandorte stehen stattdessen **einmal, vollständig und nützlich** auf der Seite „Einsatzgebiet“.
Ortsbezogene Inhalte entstehen später auf natürliche Weise über Projektseiten (Abschnitt 9).

## 4. Titel, Überschriften, Beschreibungen

Aus den Quellen in `src/seiten/` gelesen. `{{ORT}}` = Firmensitz (noch offen); Zeichenzahl Titel / Beschreibung.

| URL | Title | H1 | Meta-Description | Index | Zeichen |
|---|---|---|---|---|---|
| `/` | Trockenbau, Reparaturen & Hausmeisterservice in Stuttgart \| Gashini | Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner. | Trockenbau, Reparaturen und Hausmeisterservice in Stuttgart und 30 km Umkreis. Auch kleine Arbeiten – persönlich betreut, bei Bedarf mit Fachbetrieben. | ja | 67 / 154 |
| `/leistungen/` | Leistungen in Stuttgart: Trockenbau, Reparatur, Hausmeister \| Gashini | Was wir übernehmen – und was nicht. | Trockenbau und Innenausbau, Reparatur und Instandhaltung sowie Hausmeisterservice in Stuttgart und Umgebung – und was wir bewusst nicht selbst ausführen. | ja | 69 / 153 |
| `/leistungen/trockenbau/` | Trockenbau & Innenausbau in Stuttgart und Umgebung \| Gashini | Trockenbau und Innenausbau in Stuttgart | Trockenbau in Stuttgart, Esslingen, Ludwigsburg und Böblingen: Trennwände, Vorsatzschalen, abgehängte Decken, Reparaturen im Bestand – auch kleine Arbeiten. | ja | 60 / 156 |
| `/leistungen/reparatur-und-instandhaltung/` | Kleinreparaturen & Instandhaltung in Stuttgart \| Gashini | Reparatur und Instandhaltung in Stuttgart | Tür schleift, Loch in der Wand, Silikonfuge, Montage: kleinere Reparaturen rund um Wohnung, Haus und Gewerbe in Stuttgart und Umgebung – auch einzeln. | ja | 56 / 150 |
| `/leistungen/hausmeisterservice/` | Hausmeisterservice in Stuttgart und Umgebung \| Gashini | Hausmeisterservice in Stuttgart | Hausmeisterservice in Stuttgart und Umgebung: Objektkontrollen mit Protokoll, kleinere Instandhaltung, Mieterwechsel – für Vermieter und Hausverwaltungen. | ja | 54 / 154 |
| `/einsatzgebiet/` | Einsatzgebiet: Stuttgart und 30 km Umkreis \| Gashini | Im Einsatz in Stuttgart und Umgebung. | Trockenbau, Reparaturen und Hausmeisterservice in Stuttgart und im Umkreis von 30 km – von Ludwigsburg bis Nürtingen, von Leonberg bis Schorndorf. | ja | 52 / 146 |
| `/netzwerk/` | Netzwerk & Zusammenarbeit mit Fachbetrieben \| Gashini | Ein Ansprechpartner. Viele Gewerke im Blick. | Ein Ansprechpartner für Ihr Vorhaben im Raum Stuttgart: Was Gashini selbst ausführt, wann Fachbetriebe dazukommen und wer Ihr Vertragspartner ist. | ja | 53 / 146 |
| `/projekte/` | Projekte aus Trockenbau und Objektbetreuung \| Gashini | Unsere Arbeiten | Ausgewählte, freigegebene Arbeiten von Gashini Dienstleistungen: Trockenbau, Reparatur, Hausmeisterservice und koordinierte Gewerke. | ja | 53 / 132 |
| `/ueber-uns/` | Über uns – inhabergeführt in {{ORT}} \| Gashini | Ein Betrieb. Ein Ansprechpartner. | Gashini Dienstleistungen ist ein inhabergeführter Betrieb in {{ORT}}. Wer wir sind, wie wir arbeiten und woran Sie uns messen können. | ja | 46 / 133 |
| `/fragen/` | Fragen & Ablauf \| Gashini | Was Sie vorher wissen sollten. | Wie eine Anfrage bei Gashini Dienstleistungen abläuft – von der ersten Nachricht bis zum Abschluss – und Antworten zu Kosten, Partnern, Einsatzgebiet und Daten. | ja | 25 / 160 |
| `/kontakt/` | Anfrage stellen – Stuttgart und Umgebung \| Gashini | Erzählen Sie uns, was ansteht. | Anfrage an Gashini in Stuttgart und Umgebung: Formular mit Fotos und Rückrufwunsch, Telefon oder E-Mail. Auch für kleine Arbeiten – unverbindlich. | ja | 50 / 146 |
| `/impressum/` | Impressum \| Gashini | Impressum | Impressum und Anbieterkennzeichnung von Gashini Dienstleistungen nach § 5 DDG. | ja | 19 / 78 |
| `/datenschutz/` | Datenschutzerklärung \| Gashini | Datenschutzerklärung | Wie Gashini Dienstleistungen personenbezogene Daten auf dieser Website verarbeitet – Hosting, Anfrageformular, E-Mail und Ihre Rechte. | ja | 30 / 134 |
| `/kontakt/danke/` | Anfrage übermittelt \| Gashini | Danke für Ihre Anfrage. | Ihre Anfrage an Gashini Dienstleistungen. | nein | 29 / 41 |
| `/404.html` | Seite nicht gefunden \| Gashini | Diese Seite gibt es nicht. | Diese Seite existiert nicht. | nein | 30 / 28 |

Google kürzt Titel nach etwa 600 Pixeln (rund 60 Zeichen). Bei Startseite und Leistungsübersicht fällt dann höchstens
„| Gashini“ weg – die Suchbegriffe stehen vorne.

**Startseite, H1:** Sie bleibt das Markenversprechen *„Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner.“* Den
Ortsbezug tragen Title, das Label direkt darüber („Gashini Dienstleistungen · Stuttgart und Umgebung“), die Unterzeile
und der Abschnitt „In Stuttgart und Umgebung für Sie da“. Für die Suche nach einer Leistung rankt ohnehin die jeweilige
Leistungsseite, deren H1 den Ort trägt.

## 5. Strukturierte Daten (JSON-LD)

| Typ | Seiten | Inhalt |
|---|---|---|
| `HomeAndConstructionBusiness` | Startseite, Einsatzgebiet | Name, Logo, Telefon, E-Mail, Anschrift, Inhaber, Profile – **nur aus bestätigten Werten** (`scripts/firmendaten.py`; ohne bestätigte Domain entfällt der Block). `areaServed`: Kreis mit 30 km um Stuttgart-Mitte (48,7758 / 9,1829), dazu Stuttgart und alle 47 Orte als `City`. `knowsAbout`: die vier Leistungsbereiche |
| `Service` | je Leistungsseite | Name mit Ort, Leistungsart, Beschreibung, Anbieter per `@id` auf das Unternehmen, `areaServed`: 30-km-Kreis, Stuttgart und die vier Landkreise |
| `BreadcrumbList` | alle Unterseiten | Pfad wie in den sichtbaren Brotkrumen |
| `FAQPage` | Fragen & Ablauf, Netzwerk, Einsatzgebiet | nur Fragen, die sichtbar auf der Seite stehen |

Nicht ausgezeichnet: Geokoordinaten des Firmensitzes (Anschrift fehlt), Öffnungszeiten (fehlen), Bewertungen
(selbst erhobene Bewertungen zeigt Google bei lokalen Unternehmen nicht als Sterne an; fremde Portalbewertungen dürfen
nicht als eigene ausgezeichnet werden).
Nach dem Livegang jede Seite einmal im **Test für Rich-Suchergebnisse** von Google prüfen.

## 6. Bilder und Alt-Texte

- **Alt-Text = was zu sehen ist**, sachlich, ein Satz, mit dem Fachbegriff, den auch Suchende verwenden
  (z. B. „Abgehängte Decke im Bau: Unterkonstruktion aus Metallprofilen unter der Rohdecke, eine Hälfte bereits mit
  Gipsplatten beplankt.“). Das hilft der Bildersuche und Menschen mit Screenreader gleichermaßen.
- **Kein Ortsname in Alt-Texten von Symbolbildern.** Ein Symbolbild mit „Stuttgart“ im Alt-Text würde einen Einsatz
  vor Ort vortäuschen und gilt bei Google als Keyword-Stuffing. Die Testsuite prüft das.
- **Kennzeichnung bleibt:** „Symbolbild:“ bzw. „Symbolbild (KI-generiert):“ am Anfang des Alt-Texts, sichtbare Marke im
  Bild, Bildunterschrift „Kein Projektfoto.“ Das kostet keine Platzierung, schützt aber vor Irreführung (UWG) und vor
  Vertrauensverlust.
- **Dateinamen** beschreiben das Motiv (`abgehaengte-decke-montage-1280.webp` statt `IMG_4711.png`).
- **Technik:** WebP in drei Breiten mit `srcset`, feste Maße (kein Layoutsprung), Titelbild der Leistungsseiten mit
  `fetchpriority="high"`, alles andere lädt verzögert.
- **Echte Fotos schlagen jedes Symbolbild:** Sobald eigene Aufnahmen vorliegen (`docs/MEDIENLISTE.md`, F1–F5), die
  Symbolbilder an den wichtigsten Stellen ersetzen. Dort dürfen Alt-Texte dann auch den Ort nennen, z. B.
  „Neue Trennwand in einer Altbauwohnung in Stuttgart-West“ – weil es stimmt.

## 7. Google-Unternehmensprofil – der wichtigste Hebel

Für Suchen mit Ortsbezug zeigt Google zuerst die Karte mit drei Betrieben. Dort kommt man nur mit einem gepflegten
Unternehmensprofil hin, nicht über die Website allein.

1. **Profil anlegen oder übernehmen** (business.google.com), Inhaberschaft bestätigen.
2. **Name** exakt wie im Impressum – keine Zusätze wie „Trockenbau Stuttgart“ im Namen (verstößt gegen die Richtlinien
   und kann zur Sperrung führen).
3. **Hauptkategorie** nach dem Schwerpunkt wählen: im Feld „Trockenbau“ eintippen und den Begriff übernehmen, den Google
   vorschlägt. Weitere Kategorien für Hausmeisterdienst und Reparaturen ebenso über die Suche im Feld.
4. **Einzugsgebiet** statt Ladengeschäft: Stuttgart und die Landkreise Ludwigsburg, Esslingen, Böblingen und
   Rems-Murr-Kreis eintragen. Empfängt der Betrieb keine Kunden am Sitz, die Adresse im Profil ausblenden.
5. **Leistungen** im Profil anlegen – dieselben Bezeichnungen wie auf der Website.
6. **Website-Link** auf die Startseite, Telefonnummer identisch mit der Website.
7. **Fotos:** nur echte Fotos (Inhaber, Fahrzeug, Arbeiten mit Freigabe). **Keine KI-Bilder** im Profil – sie zeigen
   nicht das Unternehmen.
8. **Bewertungen:** nach jedem abgeschlossenen Auftrag freundlich um eine Bewertung bitten (Link aus dem Profil, z. B.
   per QR-Code auf der Rechnung). Jede Bewertung beantworten. **Keine** Gegenleistung für Bewertungen anbieten, keine
   gekauften Bewertungen – das ist unzulässig und wird von Google entfernt.
9. **Beiträge** gelegentlich veröffentlichen (abgeschlossene Arbeit mit Foto, saisonale Hinweise).
10. Die Profil-URL in `GOOGLE_PROFIL_URL` eintragen – dann erscheint der Link im Fußbereich und in den strukturierten
    Daten (`sameAs`).

## 8. Gleiche Firmendaten überall (NAP)

Name, Anschrift und Telefonnummer müssen **zeichengenau gleich** sein auf: Website, Google-Profil, MyHammer, Bing Places,
Apple Business Connect, den großen Branchenverzeichnissen (z. B. Das Örtliche, Gelbe Seiten, 11880) und – falls
eingetragen – im Verzeichnis der Handwerkskammer. Unterschiedliche Schreibweisen („Str.“/„Straße“, mit/ohne
„Dienstleistungen“) schwächen die Zuordnung. Eine Liste der Einträge mit Zugangsdaten außerhalb des Repositorys führen.

## 9. Inhalte, die mit der Zeit wachsen

- **Projektseiten** sind der nachhaltigste lokale Inhalt: Jede freigegebene Arbeit bekommt eine eigene Seite. Mit
  Zustimmung des Kunden den **Stadtteil** nennen („Trennwand in Stuttgart-Vaihingen“), nie die Adresse.
- **Fragen aus Anfragen** in `data/faq.json` aufnehmen, wenn sie mehrfach kommen.
- Keine Ratgeber-Masse auf Vorrat: lieber wenige Seiten, die eine echte Frage beantworten.

## 10. Bewusst nicht gemacht

- Keine Ortsseiten je Stadt mit ausgetauschtem Namen (Doorway Pages).
- Keine versteckten Texte, keine Ortslisten im Fußbereich jeder Seite.
- Keine `geo.*`-Meta-Angaben – Google wertet sie nicht aus.
- Keine Ortsnamen in Alt-Texten von Symbolbildern, keine KI-Bilder bei den Projekten.
- Keine Bewertungssterne aus eigener Erhebung, keine gekauften Links oder Bewertungen.

## 11. Offen – blockiert die lokale Sichtbarkeit

- [ ] Anschrift (`STRASSE`, `PLZ`, `ORT`, `PLZ_ORT`) – Grundlage für Google-Profil und Kartenergebnisse
- [ ] Telefonnummer und Domain
- [ ] Google-Unternehmensprofil anlegen (Abschnitt 7), danach `GOOGLE_PROFIL_URL` eintragen
- [ ] Liste der Orte auf `/einsatzgebiet/` bestätigen (Randorte Metzingen, Ebersbach an der Fils)
- [ ] Teilen-Vorschau `og/teilen.jpg` (Medienliste S4) – bessere Darstellung bei WhatsApp und Co.
- [ ] Erste echte Projekte mit Freigabe (Medienliste F2)

## 12. Nach dem Livegang

1. Domain in der **Google Search Console** bestätigen, `sitemap.xml` einreichen; dasselbe in den Bing Webmaster Tools.
2. Startseite, eine Leistungsseite und `/einsatzgebiet/` im Test für Rich-Suchergebnisse prüfen.
3. Google-Profil mit der Website verknüpfen.
4. Nach vier Wochen in der Search Console die tatsächlichen Suchanfragen ansehen und mit Abschnitt 3 abgleichen:
   Welche Seite erscheint wofür? Wo fehlen Klicks trotz Einblendungen (Titel/Beschreibung schärfen)?
5. Alle drei Monate wiederholen.
