# Relaunch-Plan Gashini Dienstleistungen

Stand: Bestandsaufnahme vor dem Relaunch · Branch `claude/relaunch-premium`
Grundlage: tatsächliche Analyse des Repositorys (Commit `fca26a5`), nicht Annahmen.

---

## 1. Ist-Zustand

| Bereich | Befund |
|---|---|
| Website | 13 statische HTML-Seiten in `web/`, ein Stylesheet (358 Zeilen), ein Skript (~150 Zeilen), keine Abhängigkeiten zur Laufzeit |
| Erzeugung | `scripts/build-site.py` schreibt die Seiten nach `web/`; `scripts/firmendaten.sh` ersetzt `{{PLATZHALTER}}` und legt `dist/` an |
| Konfiguration | eine Datei `data/firmendaten.env` mit allen Firmenangaben – öffentlich im Repository |
| Vorschau | `.github/workflows/vorschau.yml` veröffentlicht `dist/web/` über GitHub Pages, mit `noindex` und gesperrter `robots.txt` |
| Live-Betrieb | **existiert nicht.** Es gab nie eine eigene Domain; damit gibt es auch keine Suchmaschinen-Historie, die durch neue URLs verloren gehen könnte |
| Formular | `action="{{FORMULAR_ENDPOINT}}"` – Platzhalter, kein Backend. Abgesendete Anfragen gehen ins Leere |
| Inhalte | Positionierung auf Wohnungsübergabe, Haushaltsauflösung, Reinigung. **Weicht vom jetzt beschriebenen Geschäftsmodell ab** (Trockenbau, Hausmeisterservice, Netzwerk) |

## 2. Tatsächlicher Tech-Stack

- HTML5, CSS (Custom Properties, Grid), Vanilla JavaScript – kein Framework, kein Bundler
- Python 3 (nur Standardbibliothek) für Seitenerzeugung
- Bash + `sed` für das Einsetzen der Firmendaten
- Apache-`.htaccess` (HTTPS-Weiterleitung, Header, Caching) – passend nur, falls der spätere Webspace Apache nutzt
- GitHub Actions + GitHub Pages für die Vorschau
- Schriften: Barlow Condensed + Inter **von Google Fonts geladen**

## 3. Stärken, auf denen aufgebaut wird

1. **Kein Framework-Ballast.** Statische Seiten sind schnell, günstig zu hosten und kaum angreifbar.
2. **Zentrale Datenhaltung.** Firmendaten stehen an einer Stelle und werden beim Build eingesetzt – das Prinzip ist richtig, nur die Umsetzung braucht Schärfung.
3. **Saubere Vorschau-Trennung** über `noindex` und gesperrte `robots.txt` existiert bereits.
4. **Markenkern ist tragfähig:** Signet, Schwarz/Weiß, Ziegelrot als einzige Akzentfarbe.
5. **Bewusste Ehrlichkeit** im bisherigen Inhalt: keine erfundenen Bewertungen, Platzhalter statt Fantasiedaten.

## 4. Technische Probleme

| # | Problem | Schwere |
|---|---|---|
| T1 | **Der Generator liest seine eigene Ausgabe.** `ueber-uns`, `referenzen`, `impressum`, `datenschutz` werden aus dem bereits erzeugten HTML in `web/` „recycelt" (`altes_main()`). Wer diese Seiten von Hand ändert, verändert die Quelle; wer den Generator ändert, erreicht sie nicht. Es gibt keine eindeutige Quelle. | P0 |
| T2 | Formular ohne Backend; keine serverseitige Validierung, kein Rate-Limit, Spam-Schutz nur clientseitig | P0 |
| T3 | Platzhalter-Prüfung ist zu schwach: `firmendaten.sh` meldet nur offene `{{…}}`, nicht aber Beispielwerte wie `+49 000 0000000` oder `info@example.de`. Diese könnten unbemerkt live gehen | P0 |
| T4 | **Logo-Schrift fällt zurück.** Die Logo-SVGs enthalten `<text>` mit Barlow Condensed. Per `<img>` eingebundene SVGs dürfen keine Webfonts laden – die Wortmarke erscheint je nach Gerät in Arial Narrow oder einer Systemschrift. *(bereits behoben: Schrift jetzt als Vektorpfade)* | P0 |
| T5 | Inline-`style`-Attribute in mehreren Seiten verhindern eine strikte Content-Security-Policy | P1 |
| T6 | `.htaccess` setzt HSTS mit `includeSubDomains` – riskant, solange nicht alle Subdomains HTTPS haben; keine CSP, keine Permissions-Policy | P1 |
| T7 | Kein automatisierter Test: Links, Platzhalter, Build-Wiederholbarkeit und Darstellung werden nicht geprüft | P0 |
| T8 | URLs mit `.html`-Endung und flacher Struktur; keine sprechende Leistungshierarchie | P2 (keine SEO-Historie zu schützen) |

## 5. Datenschutz- und Rechtsrisiken

| # | Risiko | Schwere |
|---|---|---|
| D1 | **Google Fonts werden vom Google-Server geladen.** Dabei wird die IP-Adresse jedes Besuchers an Google übertragen. Das LG München I hat 2022 hierin einen Verstoß gesehen (Az. 3 O 17493/20). | P0 |
| D2 | **Pflicht-Einwilligungs-Checkbox am Formular.** Die Bearbeitung einer Anfrage stützt sich auf Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen); eine zusätzliche Einwilligung ist dafür nicht nötig und vermischt Rechtsgrundlagen. | P0 |
| D3 | **Konfigurationsdatei ist öffentlich und vorgesehen für IBAN und Steuernummer.** Aktuell stehen dort nur Platzhalter (Git-Historie geprüft: keine echten Daten, keine Zugangsdaten). Sobald der Betrieb aber die Datei wie vorgesehen ausfüllt und pusht, landen Bankverbindung und Steuernummer in einem öffentlichen Repository. | P0 |
| D4 | Die Steuernummer erscheint in der E-Mail-Signatur. Sie ist dort nicht vorgeschrieben und sollte nicht unnötig verbreitet werden. | P1 |
| D5 | Datenschutzerklärung beschreibt Verarbeitungen, die es nicht gibt (Einwilligung, Google Fonts als „berechtigtes Interesse"), und fehlt bei solchen, die kommen (Formular-Backend, Rate-Limit-Speicherung). | P0 |
| D6 | **Leistungsversprechen ohne Bestätigung** auf der Website: „Festpreis", „schriftliche Terminzusage", „Rückmeldung am selben Werktag", „Kernleistungen durch eigene Leute". Unbelegte Werbeaussagen sind nach § 5 UWG angreifbar und widersprechen dem jetzt beschriebenen Netzwerkmodell. | P0 |
| D7 | **Gewerberechtlicher Leistungsumfang ungeprüft.** Die bisherige Website bewirbt Malerarbeiten, Bodenverlegung und Fliesenarbeiten. *Maler und Lackierer*, *Parkettleger* sowie *Fliesen-, Platten- und Mosaikleger* sind zulassungspflichtige Handwerke (Anlage A HwO). Ob und in welchem Umfang diese Arbeiten beworben werden dürfen, muss mit der Handwerkskammer geklärt werden. *Trockenbaumonteur* ist zulassungsfrei (Anlage B1), aber eintragungspflichtig. | P0 – rechtlich zu prüfen |
| D8 | Holztexturen in `brand/material/` ohne dokumentierte Herkunft und Lizenz | P1 |
| D9 | Repository ist öffentlich – Strategiepapiere (Preisüberlegungen, Portalabhängigkeit) für jeden lesbar | Hinweis |

> Diese Liste ist eine technische und organisatorische Einordnung, keine Rechtsberatung.
> Details und Status in `docs/LEGAL-CHECKLIST.md`.

## 6. Visuelle Probleme

1. **Handwerker-Look statt Architektur.** Durchgehende Versalien in schmaler Schrift, Karten mit Icons, gleichförmige Kachelraster – das typische Bild, das vermieden werden soll.
2. **Keine echten Bilder.** Die einzigen Bildflächen sind leere Platzhalter oder Holztexturen. Für eine Ausbaufirma fehlt damit das stärkste Vertrauenssignal.
3. **Zu viel Akzent.** Ziegelrot erscheint in Schaltflächen, Labels, Linien, Ziffern und Hervorhebungen gleichzeitig – es verliert dadurch seine Signalwirkung.
4. **Bewegung versteckt Inhalte.** Texte stehen bis zum Einscrollen auf `opacity: 0` bzw. außerhalb ihrer Maske. Ohne funktionierenden Observer oder beim Drucken/Durchsuchen der Seite fehlen sie.
5. **Holzbänder** wirken eher wohnlich-rustikal als „quiet industrial".

## 7. Notwendige Änderungen

**Architektur**
- Eindeutige Quelle: Seiteninhalte in `src/seiten/*.html` (HTML-Fragmente mit Kopfdaten), Projekte und FAQ in `data/*.json`, Layout und Bausteine im Generator. `web/` wird **reine Ausgabe**, jede Datei mit Hinweis „generiert – nicht bearbeiten". CI prüft, dass `web/` dem Generator entspricht.
- Sprechende URLs als Verzeichnisse (`/leistungen/trockenbau/`), relative Pfade, damit Vorschau unter Unterpfad und Produktion auf eigener Domain identisch funktionieren.
- Formular-Backend als kleines PHP-Skript (siehe Abschnitt 9).
- Firmendaten in öffentlich (`data/firmendaten.env`) und privat (`data/firmendaten.privat.env`, nicht im Repository) trennen.
- Produktions-Build bricht ab, sobald Platzhalter, Freigabe-Markierungen oder Beispielwerte übrig sind.

**Gestaltung**
- Design-Tokens neu: warmes, kaum getöntes Off-White, Schwarz, fein abgestufte Grautöne, Ziegelrot nur für Hinweise und Fokus.
- Typografie: *Instrument Sans* (variable Breite 75–100, OFL) für Überschriften und Text, *IBM Plex Mono* (OFL) für technische Beschriftungen. Barlow Condensed bleibt in der Wortmarke – dort als Pfad.
- 12-Spalten-Raster, asymmetrische Abschnitte, Haarlinien statt Schatten.
- Einstieg mit einer technischen Zeichnung einer Ständerwand (Maße, Profile, Beplankung) statt eines Stockfotos – ehrlich, fachlich, und ersetzbar durch ein echtes Projektfoto, sobald eines vorliegt.

**Inhalt**
- Neue Positionierung: *Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner.*
- Leistungen: Trockenbau, Hausmeisterservice, Reparatur & Instandhaltung, Koordination – mit klarer Trennung zwischen eigener Leistung, Partnerleistung und Vermittlung.
- Alle unbestätigten Aussagen mit `[FREIGABE ERFORDERLICH: …]` markiert; der Produktions-Build lässt sie nicht durch.

## 8. Umgang mit den Altseiten

Es gibt keine Live-Domain und damit keine Rankings. Weiterleitungen dienen nur dazu, dass bereits geteilte Vorschau-Links nicht ins Leere führen. Sie stehen in `web/.htaccess` (bei Apache) und als Liste in `docs/DEPLOYMENT.md`.

| Alte Seite | Entscheidung | Ziel |
|---|---|---|
| `wohnungsuebergabe.html` | zusammengeführt – „Vorbereitung von Mieterwechseln" ist Teil des Hausmeisterservice | `/leistungen/hausmeisterservice/#mieterwechsel` |
| `haushaltsaufloesung.html` | **ruht** bis zur Bestätigung, dass Entrümpelung weiter angeboten wird (Rückfrage 2) | `/leistungen/` |
| `preise.html` | **ruht** – es liegen keine bestätigten Preise vor; Kostenfragen beantwortet die FAQ | `/fragen/#kosten` |
| `referenzen.html` | ersetzt durch Projektgalerie | `/projekte/` |
| `leistungen.html`, `ueber-uns.html`, `kontakt.html`, `impressum.html`, `datenschutz.html` | inhaltlich überarbeitet, neue URL | jeweilige Verzeichnis-URL |
| `ablauf.html`, `/ablauf/` | aufgegangen in „Fragen & Ablauf“ | `/fragen/` |
| `danke.html` | neue URL | `/kontakt/danke/` |

Die Inhalte der ruhenden Seiten bleiben im Repository (`strategie/`, Git-Historie) erhalten und lassen sich reaktivieren.

## 9. Architekturentscheidung

**Entscheidung: bestehendes statisches System weiterentwickeln. Keine Migration zu Next.js, React oder einem CMS.**

Begründung:
- Der Auftritt hat ~12 Seiten und eine Galerie. Dafür braucht es weder clientseitiges Rendering noch eine Datenbank.
- Statische Seiten erfüllen die Performance-Ziele (LCP, CLS, INP) praktisch von selbst; ein Framework müsste erst wieder mühsam auf diesen Stand optimiert werden.
- Der Betreiber soll Projekte und Texte ohne Programmierkenntnisse pflegen. Eine JSON-Datei und HTML-Fragmente sind dafür einfacher und robuster als ein selbst gehostetes CMS, das Updates und Absicherung braucht.
- Betriebskosten: jeder Webspace mit PHP genügt.

**Einziger dynamischer Teil: das Formular.** Entscheidung für ein **eigenes kleines PHP-Skript** statt eines Formulardienstes:

| | PHP-Skript beim Hoster | externer Formulardienst |
|---|---|---|
| Datenfluss | bleibt beim Hoster (ein Auftragsverarbeiter) | zusätzlicher Auftragsverarbeiter, oft mit Drittlandübermittlung |
| Kosten | im Webspace enthalten | meist Abo |
| Kontrolle über Validierung, Rate-Limit, Logs | vollständig | begrenzt |
| Voraussetzung | Webspace mit PHP ≥ 8.1 und Mailversand | keine |

Falls der spätere Hoster kein PHP bietet, ist der Wechsel auf einen Formulardienst mit AV-Vertrag und EU-Verarbeitung möglich – das Formular-Markup bleibt gleich, nur das Ziel ändert sich.

## 10. Priorisierung

### P0 – für den Livegang unverzichtbar
1. Eindeutige Quelle für alle Seiten (T1) und Drift-Prüfung in CI
2. Lokale Schriften statt Google Fonts (D1)
3. Formular-Backend mit serverseitiger Validierung, Rate-Limit, Honeypot, Header-Injection-Schutz (T2)
4. Einwilligungs-Checkbox entfernen, Art.-13-Hinweis am Formular (D2)
5. Firmendaten trennen in öffentlich/privat (D3)
6. Produktions-Build mit harter Platzhalter- und Beispielwert-Prüfung (T3)
7. Unbelegte Versprechen entfernen oder als Freigabe markieren (D6)
8. Neues Design-System, neue Startseite, Leistungsseiten, Projektgalerie mit Datenmodell
9. Datenschutzerklärung entlang der tatsächlichen Verarbeitung neu (D5)
10. Automatisierte Tests: Build, Links, Platzhalter, Viewports, Tastatur, Barrierefreiheit, Formular

### P1 – sinnvolle Erweiterungen
- Vorher-/Nachher-Vergleich, Projekt-Detailseiten, Bildansicht im Dialog
- Strikte Content-Security-Policy, Permissions-Policy (T5, T6)
- Lizenznachweis der Texturen (D8)
- Kategorie-Filter, sobald mindestens sechs veröffentlichte Projekte existieren
- Open-Graph-Bild

### P2 – nur bei nachgewiesenem Nutzen
- Foto-Upload im Formular, CRM-Anbindung, Terminbuchung, Reichweitenmessung

## 11. Was diese Analyse nicht leisten kann

Ohne Antwort auf die Rückfragen in Abschnitt 12 bleiben folgende Punkte **blockiert** und sind im Build als Freigabe markiert:
tatsächlicher Leistungsumfang je Gewerk, Einsatzgebiet, Firmendaten, Hoster, Maildienst, echte Projekte und Fotos.

## 12. Rückfragen an den Betreiber

1. **Einsatzgebiet:** Welcher Ort ist Firmensitz, und in welchem Umkreis wird gearbeitet?
2. **Leistungsumfang:** Welche Leistungen werden *heute* tatsächlich angeboten? Insbesondere: Werden Reinigung, Entrümpelung und Umzüge weiterhin angeboten – oder nur noch Trockenbau, Hausmeisterservice und Reparaturen?
3. **Handwerksrolle:** Liegt eine Eintragung als Trockenbaumonteur (Anlage B1) vor? Gibt es Eintragungen für weitere Gewerke, etwa Maler?
4. **Netzwerk:** Mit welchen Fachbetrieben wird zusammengearbeitet – und in welcher Form: als Subunternehmer unter eigener Rechnung, oder vermittelt mit direktem Vertrag zwischen Kunde und Partner?
5. **Hosting:** Gibt es bereits Domain und Webspace? Bei welchem Anbieter, mit PHP?
6. **E-Mail:** Über welches Postfach sollen Anfragen ankommen, und gibt es SMTP-Zugangsdaten dafür?
7. **Projekte:** Gibt es Fotos abgeschlossener Arbeiten mit Freigabe der Auftraggeber?
8. **Versicherung:** Besteht eine Betriebshaftpflichtversicherung (Name, Geltungsbereich)?
9. **Erreichbarkeit:** Welche Telefonzeiten und Reaktionszeiten können verbindlich zugesagt werden?
10. **Messenger:** Soll WhatsApp als Kontaktweg angeboten werden? (Datenübermittlung an Meta; nur als Link, nicht eingebettet)
