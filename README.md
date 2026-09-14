# Gashini Dienstleistungen – Firmenauftritt

Kompletter Unternehmensauftritt: Logo, Gestaltungsrichtlinien, Website, Druckvorlagen,
E-Mail-Signatur, Fahrzeug- und Kleidungsbeschriftung sowie die Texte für das MyHammer-Profil.

## Inhalt

```
brand/     Logo (SVG), Signet, Favicon, Gestaltungsrichtlinien
web/       Website: 8 Seiten, Stylesheet, Sitemap, robots.txt
print/     Visitenkarte, Briefbogen, Flyer, E-Mail-Signatur, Fahrzeug-/Kleidungsbeschriftung
content/   Profiltexte und Nachrichtenvorlagen für MyHammer
data/      firmendaten.env – zentrale Datei mit allen Firmenangaben
scripts/   firmendaten.sh – setzt die Firmendaten in alle Vorlagen ein
```

## In drei Schritten einsatzbereit

1. **`data/firmendaten.env` ausfüllen** – Name des Inhabers, Anschrift, Telefon, E-Mail,
   Domain, MyHammer-Profillink, Steuernummer, Versicherung, Bankverbindung.
2. **`bash scripts/firmendaten.sh`** ausführen. Das Skript kopiert alles nach `dist/`
   und ersetzt dort die Platzhalter. Am Ende listet es auf, was noch offen ist.
3. **`dist/web/` hochladen** (jeder einfache Webspace genügt, es wird keine Datenbank
   und kein PHP benötigt) und die Dateien in `dist/print/` im Browser öffnen →
   Drucken → „Als PDF sichern“ für die Druckerei.

Die Vorlagen im Projekt bleiben dabei unverändert; nach jeder Datenänderung einfach
das Skript erneut ausführen.

## Platzhalter

Alles in der Form `{{PLATZHALTER}}` ist noch zu befüllen und stammt aus
`data/firmendaten.env`. Diese Daten kann nur der Betrieb selbst liefern – sie wurden
bewusst nicht erfunden, damit keine falschen Angaben veröffentlicht werden.

## Verzahnung mit MyHammer

- **Website → MyHammer:** Verlinkung in Kopfzeile, Fußzeile, auf Start-, Leistungs-,
  Ablauf-, Referenz- und Kontaktseite sowie in den strukturierten Daten (`sameAs`).
- **MyHammer → Website:** fertige Profiltexte in `content/myhammer-profil.md`,
  inklusive Nachrichtenvorlagen und Checkliste zur Profilpflege.

## Vor dem Livegang bitte prüfen

- [ ] Impressum und Datenschutzerklärung sind Vorlagen – juristisch prüfen lassen und
      an den tatsächlichen Betrieb anpassen (Kammer, Handwerksrolle, Versicherung).
- [ ] Auf der Referenzseite ausschließlich **echte, freigegebene** Kundenstimmen einsetzen.
- [ ] Note und Anzahl der MyHammer-Bewertungen müssen dem Profil entsprechen.
- [ ] Kontaktformular mit einem Formular-Dienst oder eigenem Skript verbinden
      (`FORMULAR_ENDPOINT`) und auf `danke.html` weiterleiten lassen.
- [ ] Optional: Google Fonts lokal ablegen, dann entfällt der entsprechende
      Abschnitt der Datenschutzerklärung.
- [ ] Eigene Fotos einsetzen – keine Stockbilder mit fremden Personen.
