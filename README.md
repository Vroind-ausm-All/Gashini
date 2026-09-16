# Gashini Dienstleistungen – Firmenauftritt und Marketinggrundlage

Vollständiger Unternehmensauftritt plus die strategische Grundlage dahinter:
Positionierung, Fachprüfungen der Website, Marken- und Medienstandards, Texte,
Kanalstrategie, Leadprozess und eine 90-Tage-Roadmap.

## Inhalt

```
strategie/   Strategiepapier, Audits, Marken- und Medienstandards, Texte, Kanäle, CRM
brand/       Logo (SVG), Signet, Favicon, Gestaltungsrichtlinien
web/         Website: 13 Seiten, Stylesheet, Sitemap, robots.txt, .htaccess
print/       Visitenkarte, Briefbogen, Flyer, E-Mail-Signatur, Fahrzeug-/Kleidungsbeschriftung
content/     Profiltexte und Nachrichtenvorlagen für MyHammer
data/        firmendaten.env – zentrale Datei mit allen Firmenangaben
scripts/     build-site.py (erzeugt die Seiten) · firmendaten.sh (setzt die Daten ein)
```

## Zuerst lesen

| Dokument | Beantwortet |
|---|---|
| [`strategie/01-strategie.md`](strategie/01-strategie.md) | Positionierung, Zielgruppen, Nutzenversprechen, Prioritäten, **90-Tage-Roadmap** |
| [`strategie/02-audit-website.md`](strategie/02-audit-website.md) | Getrennte Befunde aus Technik, SEO, UX und Conversion – mit Status |
| [`strategie/03-marke-und-medienstandards.md`](strategie/03-marke-und-medienstandards.md) | Passt das Erscheinungsbild zur Positionierung? Produktionsvorgaben |
| [`strategie/04-texte-und-botschaften.md`](strategie/04-texte-und-botschaften.md) | Informationshierarchie, Headlines, Claims, CTA-Regeln |
| [`strategie/05-kanaele.md`](strategie/05-kanaele.md) | SEO, Social und Paid auf gemeinsamer Grundlage |
| [`strategie/06-leadprozess-crm.md`](strategie/06-leadprozess-crm.md) | Anfrage → Angebot → Nachfassen → Bestandskunde |

**Die wichtigste Erkenntnis aus der Analyse:** Der größte Hebel liegt nicht in mehr Werbung,
sondern in eigener Auffindbarkeit (Google-Unternehmensprofil), einem eigenen Bewertungsbestand
und konsequentem Nachfassen bei bereits vorhandenen Anfragen.

## In drei Schritten einsatzbereit

1. **`data/firmendaten.env` ausfüllen** – Anschrift, Telefon, E-Mail, Domain, MyHammer- und
   Google-Profil, Steuernummer, Versicherung, Bankverbindung sowie die **Preisspannen**.
2. **`bash scripts/firmendaten.sh`** ausführen. Das Skript kopiert alles nach `dist/` und
   ersetzt dort die Platzhalter. Am Ende listet es auf, was noch offen ist.
3. **Inhalt von `dist/web/` hochladen** – jeder einfache Webspace genügt, es wird weder eine
   Datenbank noch PHP benötigt. Die Druckvorlagen in `dist/print/` im Browser öffnen →
   Drucken → „Als PDF sichern“ für die Druckerei.

> **Stolperstein beim Hochladen:** Der *Inhalt* von `dist/web/` gehört in die Wurzel der Domain,
> nicht der Ordner selbst. Sonst liegen `robots.txt`, `sitemap.xml` und `.htaccess` eine Ebene
> zu tief und wirken nicht. Die Datei `.htaccess` beginnt mit einem Punkt und wird von manchen
> FTP-Programmen ausgeblendet – Anzeige versteckter Dateien einschalten.

## Seitenstruktur

| Seite | Aufgabe |
|---|---|
| `index.html` | Einstieg nach Anlass, Paketlogik, Beweis |
| `wohnungsuebergabe.html` | Anlassseite Z1 – Auszug unter Frist |
| `haushaltsaufloesung.html` | Anlassseite Z2 – Erbfall, Räumung |
| `preise.html` | Preisspannen, Beispielrechnungen, Preisfaktoren |
| `leistungen.html` | Alle vier Gewerke einzeln |
| `ablauf.html` | Ablauf in vier Schritten + FAQ (mit FAQ-Auszeichnung für Google) |
| `kontakt.html` | Anfragestrecke mit Quellenerfassung |
| `referenzen.html`, `ueber-uns.html` | Beweis und Betrieb |
| `danke.html`, `404.html`, `impressum.html`, `datenschutz.html` | Pflicht und Randfälle |

Seiten werden aus `scripts/build-site.py` erzeugt. Wer Texte ändert: entweder direkt in den
HTML-Dateien (einfach, aber beim nächsten Generatorlauf überschrieben) **oder** im Generator und
anschließend `python3 scripts/build-site.py` ausführen – das ist der empfohlene Weg.

## Platzhalter

Alles in der Form `{{PLATZHALTER}}` stammt aus `data/firmendaten.env` und ist noch zu befüllen.
Diese Angaben kann nur der Betrieb liefern; sie wurden bewusst nicht erfunden.

## Verzahnung mit MyHammer

- **Website → MyHammer:** Fußzeile jeder Seite, Beweisblock auf Start- und Anlassseiten,
  Referenz- und Kontaktseite sowie `sameAs` in den strukturierten Daten.
- **MyHammer → Website:** fertige Profiltexte, Nachrichtenvorlagen und Pflege-Checkliste in
  [`content/myhammer-profil.md`](content/myhammer-profil.md).

## Vor dem Livegang prüfen

- [ ] Impressum und Datenschutzerklärung sind Vorlagen – juristisch prüfen lassen
- [ ] Preisspannen und Beispielrechnungen stammen aus **eigenen** abgerechneten Aufträgen
- [ ] Auf der Referenzseite ausschließlich **echte, freigegebene** Kundenstimmen
- [ ] Note und Anzahl der MyHammer-Bewertungen entsprechen dem Profil
- [ ] Kontaktformular mit einem Formulardienst verbunden (`FORMULAR_ENDPOINT`), Weiterleitung
      auf `danke.html`, **Testanfrage abgeschickt und Empfang geprüft**
- [ ] Die vier Versprechen im Vertrauensband sind im Betrieb tatsächlich gedeckt
      (siehe Strategiepapier, Abschnitt 5)
- [ ] Eigene Fotos statt der Bildplatzhalter – Vorgaben in `strategie/03`, Abschnitt 3.2
- [ ] Google-Unternehmensprofil angelegt (Roadmap-Maßnahme 1.2 – wichtigster Einzelschritt)
