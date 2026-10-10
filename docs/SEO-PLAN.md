# SEO-Plan

Ziel: gefunden werden von Menschen in {{REGION}}, die eine konkrete Arbeit an ihrer Immobilie vergeben wollen –
nicht für möglichst viele Begriffe, sondern für die richtigen.

## 1. Ausgangslage

- Es gibt **keine Live-Domain und keine Suchmaschinen-Historie**. Neue URLs kosten nichts.
- Der wichtigste Kanal für lokale Dienstleister ist das **Google-Unternehmensprofil** – vor jeder Onpage-Maßnahme.
  Die Website ist die Beweisfläche dahinter. (Begründung: `strategie/05-kanaele.md`)
- Ort und Einsatzgebiet sind noch nicht bestätigt; alle ortsbezogenen Angaben stehen als `{{ORT}}`, `{{REGION}}`
  und `{{EINSATZGEBIET}}` in `data/firmendaten.env`.

## 2. Suchintentionen und Seitenzuordnung

Eine Suchintention, eine Seite. Keine Seite soll zwei Intentionen bedienen, keine zwei Seiten dieselbe.

| Priorität | Suchintention | Typische Suchanfrage | Zielseite |
|---|---|---|---|
| 1 | Trockenbau vor Ort | „trockenbau {{ORT}}“, „trockenbauer {{ORT}}“ | `/leistungen/trockenbau/` |
| 1 | Hausmeisterservice vor Ort | „hausmeisterservice {{ORT}}“, „hausmeister für mehrfamilienhaus {{ORT}}“ | `/leistungen/hausmeisterservice/` |
| 2 | Konkrete Trockenbauarbeit | „trennwand einziehen lassen“, „decke abhängen lassen kosten“ | `/leistungen/trockenbau/` |
| 2 | Kleinere Reparaturen | „kleinreparaturen wohnung {{ORT}}“, „handwerker für kleine arbeiten {{REGION}}“ | `/leistungen/reparatur-und-instandhaltung/` |
| 2 | Mieterwechsel | „wohnung renovieren zwischen mietern“, „wohnung für neue mieter herrichten“ | `/leistungen/hausmeisterservice/#mieterwechsel` |
| 3 | Objektbetreuung | „objektbetreuung {{REGION}}“ | `/leistungen/hausmeisterservice/` |
| 3 | Innenausbau | „innenausbau {{REGION}}“ – **nur wenn tatsächlich angeboten** | `/leistungen/trockenbau/` |
| – | Marke | „gashini dienstleistungen“ | `/` – muss zwingend funktionieren, Fahrzeug und Flyer erzeugen genau diese Suche |

**Bewusst nicht:** eigene Seiten je Umlandort mit ausgetauschtem Ortsnamen. Das bringt bei lokalem Radius kaum
Anfragen und riskiert eine Abwertung als Doorway-Seiten. Das Einsatzgebiet steht als Text in Kontakt- und FAQ-Bereich.

## 3. Titel, Überschriften, Beschreibungen

Automatisch aus den Quellen in `src/seiten/` gelesen (Stand dieses Dokuments). Platzhalter werden beim Build ersetzt.

| URL | Title | H1 | Meta-Description | Index |
|---|---|---|---|---|
| `/404.html` | Seite nicht gefunden | Gashini | Diese Seite gibt es nicht | Diese Seite existiert nicht. | nein |
| `/ablauf/` | Ablauf und häufige Fragen | Gashini | Von der Anfrage bis zum fertigen Ergebnis | Wie eine Anfrage bei Gashini Dienstleistungen abläuft – von der ersten Nachricht bis zum Abschluss – und Antworten auf häufige Fragen zu Kosten, Partnern und Gebiet. | ja |
| `/kontakt/danke/` | Anfrage übermittelt | Gashini | Danke für Ihre Anfrage | Ihre Anfrage an Gashini Dienstleistungen. | nein |
| `/datenschutz/` | Datenschutzerklärung | Gashini | Datenschutzerklärung | Wie Gashini Dienstleistungen personenbezogene Daten auf dieser Website verarbeitet – Hosting, Anfrageformular, E-Mail und Ihre Rechte. | ja |
| `/leistungen/hausmeisterservice/` | Hausmeisterservice in {{ORT}} | Gashini | Hausmeisterservice in {{ORT}} | Objektbetreuung, kleinere Instandhaltung und Vorbereitung von Mieterwechseln in {{REGION}} – für Vermieter, Hausverwaltungen und Gewerbe. | ja |
| `/impressum/` | Impressum | Gashini | Impressum | Impressum und Anbieterkennzeichnung von Gashini Dienstleistungen nach § 5 DDG. | ja |
| `/kontakt/` | Projekt anfragen | Gashini | Erzählen Sie uns, was ansteht | Anfrage an Gashini Dienstleistungen: Formular, Telefon oder E-Mail. Auch für kleine Arbeiten – unverbindlich. | ja |
| `/leistungen/` | Leistungen: Trockenbau, Hausmeister, Reparaturen | Gashini | Was wir übernehmen – und was nicht | Trockenbau und Innenausbau, Hausmeisterservice sowie Reparatur und Instandhaltung in {{REGION}} – und was wir bewusst nicht selbst ausführen. | ja |
| `/projekte/` | Projekte aus Trockenbau und Objektbetreuung | Gashini | Unsere Arbeiten | Ausgewählte, freigegebene Arbeiten von Gashini Dienstleistungen: Trockenbau, Hausmeisterservice, Reparatur und koordinierte Gewerke. | ja |
| `/leistungen/reparatur-und-instandhaltung/` | Reparaturen & Instandhaltung in {{REGION}} | Gashini | Reparatur und Instandhaltung | Kleinere Reparaturen, Ausbesserungen und Montagen rund um Wohnung, Haus und Gewerbeobjekt in {{REGION}} – auch einzelne Arbeiten. | ja |
| `/` | Trockenbau & Hausmeisterservice in {{ORT}} | Gashini Dienstleistungen | Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner. | Trockenbau, Hausmeisterservice und Reparaturen rund um Ihre Immobilie in {{REGION}}. Auch kleine Arbeiten – persönlich betreut, bei Bedarf mit Partnerbetrieben abgestimmt. | ja |
| `/leistungen/trockenbau/` | Trockenbau & Innenausbau in {{ORT}} | Gashini | Trockenbau und Innenausbau in {{ORT}} | Nichttragende Trennwände, Vorsatzschalen, abgehängte Decken und Reparaturen im Bestand in {{REGION}}. Auch einzelne Räume und kleine Arbeiten. | ja |
| `/ueber-uns/` | Über uns und unser Netzwerk | Gashini | Ein Betrieb, ein Ansprechpartner | Gashini Dienstleistungen ist ein inhabergeführter Betrieb in {{ORT}}. Wie wir arbeiten und wie die Zusammenarbeit mit Partnerbetrieben geregelt ist. | ja |

Projektdetailseiten erhalten automatisch Titel `Projektname – Leistung | Gashini Dienstleistungen` und die
Kurzbeschreibung als Meta-Description.

### Entscheidung zur H1 der Startseite

Die H1 lautet wie vorgegeben *„Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner.“* – ein Markenversprechen ohne
Suchbegriff. Der Suchbezug liegt im Title („Trockenbau & Hausmeisterservice in {{ORT}}“), in der Unterzeile und in den
Leistungsseiten, die je eine Intention mit Ort in der H1 tragen. Für eine Startseite, die vor allem über die Marke und
das Google-Profil erreicht wird, ist das vertretbar.
*Alternative, falls die Startseite selbst für „Trockenbau {{ORT}}“ ranken soll:* das Label über der H1 („Gashini
Dienstleistungen · {{REGION}}“) durch „Trockenbau und Hausmeisterservice in {{ORT}}“ ersetzen und als ersten Teil der
H1 auszeichnen. Keine versteckten Texte.

## 4. Technische Grundlagen (umgesetzt)

| Element | Umsetzung |
|---|---|
| Sprechende URLs | Verzeichnisse, z. B. `/leistungen/trockenbau/` |
| Canonical | auf jeder Seite außer 404, absolute URL mit `{{DOMAIN}}` |
| Sitemap | `sitemap.xml`, nur indexierbare Seiten und freigegebene Projekte, `lastmod` aus `STAND_ISO` |
| robots.txt | Produktion: alles erlaubt außer `/api/`; Vorschau: alles gesperrt + `noindex` je Seite |
| `noindex` | Danke-Seite und 404 |
| Open Graph | Titel, Beschreibung, URL, Typ, Sprache je Seite |
| Strukturierte Daten | `HomeAndConstructionBusiness` (nur aus **bestätigten** Werten erzeugt), `Service` je Leistungsseite, `BreadcrumbList`, `FAQPage` auf der Ablaufseite |
| Interne Verlinkung | Leistungsliste, Brotkrumen, Fußbereich, Kontextlinks mit sprechendem Ankertext |
| Bilder | feste Maße, Alt-Text Pflicht (Testsuite prüft), `srcset` sobald Varianten vorliegen |
| Weiterleitungen | alte Vorschau-URLs gezielt per 301 (siehe `docs/DEPLOYMENT.md`) |

Nicht umgesetzt, weil die Angaben fehlen: Öffnungszeiten (`openingHoursSpecification`), Geokoordinaten, Bewertungsdaten.
Bewertungen werden **nicht** als strukturierte Daten ausgezeichnet: Google zeigt selbst erhobene Bewertungen von
lokalen Unternehmen auf deren eigener Website ohnehin nicht als Sterne an, und fremde Portalbewertungen dürfen nicht als
eigene ausgezeichnet werden.

## 5. Offene lokale Unternehmensdaten

Ohne diese Angaben ist lokale Sichtbarkeit nicht erreichbar. Sie müssen **überall identisch** sein
(Website, Google-Profil, MyHammer, Branchenverzeichnisse):

- [ ] Firmenname exakt (mit oder ohne „Dienstleistungen“?)
- [ ] Anschrift
- [ ] Telefonnummer
- [ ] Ort und Einsatzgebiet
- [ ] Domain
- [ ] Google-Unternehmensprofil: angelegt? Hauptkategorie „Trockenbauunternehmen“ oder „Hausmeisterdienst“?
- [ ] MyHammer-Profil-URL (Verlinkung nur, keine Übernahme der Bewertungsnote)

## 6. Nach dem Livegang

1. Domain in der Google Search Console bestätigen, Sitemap einreichen.
2. Google-Unternehmensprofil mit der Website verknüpfen.
3. Nach vier Wochen: Suchanfragen in der Search Console prüfen und mit Abschnitt 2 abgleichen.
4. Mit jedem freigegebenen Projekt wächst die Seite um eine indexierbare Detailseite – das ist der nachhaltigste
   Inhaltszuwachs für diesen Betrieb.
