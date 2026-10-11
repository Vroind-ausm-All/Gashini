# Rechtliche Checkliste

> **Keine Rechtsberatung.** Diese Liste ordnet ein, was technisch umgesetzt ist und was noch offen ist. Sie ersetzt
> keine Prüfung durch eine Anwältin, einen Anwalt oder die zuständige Kammer. Die Website wird hier **nicht** als
> „DSGVO-konform“ bezeichnet – das kann nur eine Prüfung des tatsächlichen Betriebs feststellen.

Legende: ✅ technisch umgesetzt · 📄 dokumentiert · 👤 vom Betreiber zu bestätigen · ⚖️ rechtlich zu prüfen

## 1. Datenschutz (DSGVO, TDDDG)

| Thema | Status | Stand |
|---|---|---|
| Keine Cookies, kein lokaler Speicher | ✅ | Im veröffentlichten Auftritt schreibt kein Skript Cookies, `localStorage` oder `sessionStorage`. Nur die gekennzeichnete **Vorschau** merkt sich im Browser den Schalter „Kundenansicht“ (`localStorage`); der Schalter existiert im Produktions-Build nicht. **Ergebnis der Prüfung: Ein Einwilligungsbanner ist nicht erforderlich** (§ 25 TDDDG), solange keine Analyse-, Karten- oder Social-Dienste ergänzt werden. |
| Keine Analysewerkzeuge, keine Tracker | ✅ | Bewusster Verzicht. Lead-Quelle wird freiwillig im Formular abgefragt, nicht gemessen. |
| Schriften und Bibliotheken lokal | ✅ | Instrument Sans und IBM Plex Mono, GSAP und three.js liegen auf dem eigenen Server. Keine Verbindung zu Google oder CDNs. Auch die Druckvorlagen laden keine Google Fonts mehr. Das 3D-Modell wird vollständig im Browser berechnet. |
| Keine externen Skripte, Karten, Videos, Social-Embeds | ✅ | Die Testsuite bricht ab, wenn eine Seite eine externe Ressource lädt. |
| Content-Security-Policy | ✅ | `default-src 'self'`, keine Inline-Skripte, keine Inline-Stile (in `src/server/htaccess`). Gilt nur bei Apache. |
| Rechtsgrundlage Anfrage | 📄 ⚖️ | Art. 6 Abs. 1 lit. b DSGVO (vorvertraglich), hilfsweise lit. f. **Keine Pflicht-Einwilligungs-Checkbox** mehr – sie war rechtlich nicht nötig und vermischte Rechtsgrundlagen. Hinweis mit Link direkt über dem Absendeknopf (Art. 13). |
| Datenminimierung im Formular | ✅ | Pflicht: Name, eine Kontaktmöglichkeit, Leistung, Beschreibung. Alles andere freiwillig und gekennzeichnet (Rückrufwunsch mit Zeitfenster, Fotos, PLZ, Zeitraum, Quelle). |
| Foto-Upload | ✅ 📄 👤 | Bis 3 Bilder, Typ am Inhalt geprüft (finfo, getimagesize), neutrale Dateinamen, Übermittlung nur als E-Mail-Anhang, keine dauerhafte Speicherung auf dem Webserver. Hinweis auf Metadaten (Aufnahmeort) und „keine Personen fotografieren“ im Formular und in der Datenschutzerklärung. 👤 Postfach und Löschfrist gelten auch für die Anhänge. |
| Speicherung Mengenlimit | ✅ 📄 | Nur HMAC-Prüfwert der IP (mit geheimem Schlüssel) und Zeitstempel, Löschung nach spätestens 24 h. Test prüft, dass keine IP im Klartext gespeichert wird. |
| Server-Protokolle des Formulars | ✅ | `error_log` enthält nur Ereignisse („zugestellt“, „als Spam verworfen“), **keine** Inhalte. |
| Weitergabe an Partnerbetriebe | 📄 👤 | Nur nach Rücksprache mit dem Anfragenden. Muss im Betrieb tatsächlich so gehandhabt werden. |
| Auftragsverarbeitung Hoster und Mailanbieter (Art. 28) | 👤 | AV-Verträge abschließen und ablegen. |
| Speicherdauer Server-Logs | 👤 | Beim Hoster erfragen, in `LOG_SPEICHERDAUER` eintragen. |
| Speicherdauer Anfragen | 👤 ⚖️ | Frist festlegen und einhalten (Vorschlag: 6 Monate nach letztem Kontakt), in `ANFRAGE_SPEICHERDAUER`. |
| Drittlandübermittlung | 👤 | Hoster und Mailanbieter mit Verarbeitung ausschließlich in der EU wählen; Text in `DRITTLAND_HINWEIS`. |
| WhatsApp | 👤 ⚖️ | Standardmäßig **aus**. Wird `WHATSAPP` gesetzt, erscheinen Link und Datenschutzabschnitt. Übermittlung an Meta/USA. |
| Zuständige Aufsichtsbehörde | 👤 | Nach Bundesland des Firmensitzes. |
| Verzeichnis von Verarbeitungstätigkeiten (Art. 30) | 👤 | Gilt grundsätzlich auch für kleine Betriebe, wenn Verarbeitung nicht nur gelegentlich erfolgt – Kundenanfragen sind regelmäßig. |
| Repository öffentlich | ⚖️ 👤 | Keine personenbezogenen Daten im Repository (Test prüft IBAN-Muster, Passwörter, private Konfigurationsdateien). Private Werte gehören in `data/firmendaten.privat.env` (nicht versioniert). Strategiepapiere sind öffentlich lesbar – Entscheidung des Betreibers. |

## 2. Impressum (§ 5 DDG)

| Angabe | Status | Hinweis |
|---|---|---|
| Name, Anschrift, Kontakt | ✅ 👤 | Felder vorhanden, Werte offen |
| Rechtsform / Inhaber | 👤 | Einzelunternehmen mit Inhabernamen? Bei Eintragung ins Handelsregister zusätzlich Registergericht und -nummer. |
| USt-IdNr. | ✅ 👤 | Abschnitt erscheint nur, wenn `USTID` gesetzt ist. **Steuernummer gehört nicht ins Impressum** und wurde aus der E-Mail-Signatur entfernt. |
| Handwerksrolle / Kammer | ✅ 👤 ⚖️ | Kammer und Eintragung angeben, soweit § 5 DDG dies für das ausgeübte Handwerk verlangt – mit der Kammer abstimmen. Abschnitt erscheint, wenn `HANDWERKSROLLE` gesetzt ist. |
| Berufshaftpflichtversicherung | ✅ 👤 ⚖️ | Abschnitt optional. Ob eine Angabepflicht besteht (DL-InfoV), mit Kammer klären. |
| Verbraucherstreitbeilegung (§ 36 VSBG) | 📄 ⚖️ | Hinweis enthalten. Betriebe mit höchstens zehn Beschäftigten sind von der Pflicht ausgenommen; der Hinweis schadet nicht. |
| EU-OS-Plattform | 📄 | **Entfernt.** Die Online-Streitbeilegungsplattform der EU wurde zum 20. Juli 2025 eingestellt (VO (EU) 2024/3228); der Link ist nicht mehr erforderlich. |
| § 18 Abs. 2 MStV (redaktionell Verantwortlicher) | 📄 | Entfernt – gilt für journalistisch-redaktionelle Angebote, nicht für eine reine Firmenwebsite. Sollte ein Blog mit redaktionellen Beiträgen entstehen, wieder aufnehmen. |
| Haftungsausschluss-Textbausteine | 📄 | Entfernt. Sie haben keine eigenständige rechtliche Wirkung und machen das Impressum nur länger. |

## 3. Gewerbe- und Handwerksrecht – vor der Veröffentlichung klären

| Leistung | Einordnung | Status |
|---|---|---|
| Trockenbau | *Trockenbaumonteur* ist zulassungsfrei (Anlage B1 HwO), aber **eintragungspflichtig** in das Verzeichnis der zulassungsfreien Handwerke | 👤 Eintragung bestätigen |
| Hausmeisterservice | in der Regel Gewerbeanmeldung; handwerkliche Tätigkeiten innerhalb des Hausmeisterservice müssen dem eigenen Eintrag entsprechen | 👤 ⚖️ |
| Malerarbeiten | *Maler und Lackierer* ist **zulassungspflichtig** (Anlage A HwO). Auf der Website deshalb nicht als eigene Leistung beworben, nur „auf Wunsch über einen Partnerbetrieb“ | ⚖️ mit HWK klären, ob Teilleistungen als einfache Tätigkeiten (§ 1 Abs. 2 HwO) zulässig sind |
| Fliesen-, Parkett-, Bodenarbeiten | *Fliesen-, Platten- und Mosaikleger* und *Parkettleger* sind seit 2020 wieder zulassungspflichtig. *Bodenleger* ist zulassungsfrei | ⚖️ |
| Elektro, Gas, Wasser, Heizung | zulassungspflichtig – auf der Website ausdrücklich ausgeschlossen | ✅ |
| Brand- und Schallschutz | nur mit nachgewiesener Qualifikation und geprüften Systemen; auf der Website ausgeschlossen, solange nicht bestätigt | 👤 |
| Netzwerk / Vermittlung | Form der Zusammenarbeit klären: Subunternehmer (Gashini haftet), Koordination, oder Empfehlung (Kunde beauftragt direkt). Bei Subunternehmern muss der Partner selbst die nötige Eintragung haben | 👤 ⚖️ |

## 4. Werbung und Wettbewerb (UWG)

| Thema | Status |
|---|---|
| Keine unbelegten Versprechen | ✅ „Festpreis“, „schriftliche Terminzusage“, „Rückmeldung am selben Werktag“, „alles mit eigenen Leuten“ wurden entfernt. Reaktionszeiten und Telefonzeiten sind als Freigabe markiert. |
| Keine erfundenen Referenzen oder Bewertungen | ✅ Galerie veröffentlicht nur Projekte mit Kunden- und Bildfreigabe; Beispiele erscheinen nur in internen Vorschauen und sind gekennzeichnet. Keine Bewertungsnoten auf der Website. |
| Keine künstliche Verknappung | ✅ |
| Steuerhinweis § 35a EStG | 📄 Sachlich korrekt formuliert (20 % der Arbeitskosten, höchstens 1.200 € jährlich, unbare Zahlung), mit Hinweis auf Steuerberatung. |

## 5. Urheber- und Bildrechte

| Thema | Status |
|---|---|
| Schriften | ✅ SIL Open Font License, Lizenztexte liegen neben den Dateien (`src/assets/fonts/`, `brand/OFL-barlow-condensed.txt`). |
| Logo | ✅ eigene Gestaltung; Schrift jetzt als Pfad (OFL erlaubt das). |
| Holztexturen `brand/material/` | 👤 **Herkunft und Lizenz unbekannt.** Werden auf der neuen Website nicht verwendet. Vor jeder Nutzung Lizenz nachweisen. |
| Projektfotos | ✅ technisch: Freigabefelder je Bild (`rechte.freigabe_kunde`, `fotograf`, `nutzungsrecht`, `ki_generiert`) – ohne Freigabe keine Veröffentlichung. 👤 Freigabe schriftlich einholen. |
| Personen auf Fotos | 👤 Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, KUG) für Mitarbeitende und Dritte. |
| KI-Bilder | ✅ Regel im Datenmodell: `ki_generiert: true` verhindert die Veröffentlichung als Projekt. Selbst erzeugt wurde **kein** KI-Bild; zu den bereitgestellten Symbolbildern siehe unten. Atmosphärische KI-Bilder nur außerhalb der Galerie und gekennzeichnet (`docs/ASSET-BRIEFS.md`). |
| Symbolbilder `src/assets/bilder/symbol/` | ✅ technisch: im Bild, im Alt-Text und in der Unterschrift als Symbolbild gekennzeichnet; ein Test verhindert ihre Verwendung als Projektbild oder auf „Über uns“. 👤 **Quelle und Nutzungsrecht bestätigen** und als `SYMBOLBILD_QUELLE` eintragen (erscheint im Impressum unter Bildnachweis; Agenturen verlangen oft eine Urhebernennung). Sind die Bilder KI-generiert, die Kennzeichnung auf „Symbolbild (KI-generiert)“ ändern. |
| Kurzvideos `src/assets/videos/` | ✅ technisch: selbst gehostet (keine Einbettung von YouTube o. Ä., keine Datenübermittlung an Dritte), stumm, mit Pause-Knopf, kein Start bei „Bewegung reduzieren“. 👤 Für KI-Clips gelten dieselben Regeln wie für KI-Symbolbilder: Herkunft dokumentieren, als „Symbolbild (KI-generiert)“ kennzeichnen, nie für Projekte oder „Über uns“. |
| Visualisierungen und Zeichnungen | ✅ eigene Erstellung (three.js-Renderings, SVG). Auf der Website als „Visualisierung“ bzw. „schematische Darstellung“ gekennzeichnet; Herkunft in `src/assets/bilder/visualisierung/HERKUNFT.md`. Ein Test verhindert ihre Verwendung als Projektbild. |
| Software-Lizenzen | ✅ GSAP 3.15 (Standard „No Charge“ License, kommerzielle Websites erlaubt), three.js (MIT). Hinweise in `src/assets/js/vendor/LIZENZEN.txt`. |
| Netzwerk ohne erfundene Partner | ✅ 👤 Gewerke sind ausdrücklich als Beispiele gekennzeichnet, keine Partnerzahl. 👤 Tatsächliche Gewerke und Form der Zusammenarbeit bestätigen. |

## 6. Barrierefreiheit (BFSG)

| Thema | Status |
|---|---|
| Anwendbarkeit | ⚖️ Das BFSG gilt seit 28. Juni 2025 für bestimmte Produkte und Dienstleistungen, u. a. für Dienstleistungen im elektronischen Geschäftsverkehr gegenüber Verbrauchern. Kleinstunternehmen (weniger als 10 Beschäftigte **und** höchstens 2 Mio. € Umsatz oder Bilanzsumme), die Dienstleistungen erbringen, sind ausgenommen. Eine reine Informationswebsite mit Kontaktformular ohne Online-Vertragsschluss fällt nach verbreiteter Auffassung nicht darunter. **Im konkreten Fall prüfen lassen.** |
| Technisches Ziel WCAG 2.2 AA | ✅ automatisiert geprüft mit axe-core auf allen Seiten bei 1440 und 375 px: keine schweren oder kritischen Verstöße. Manuelle Prüfung mit Screenreader steht aus (`docs/TESTREPORT.md`). |
| Kein Overlay-Werkzeug | ✅ |

## 7. Vor dem Livegang abzuhaken

- [ ] Alle 👤-Punkte beantwortet und in `data/firmendaten.env` eingetragen
- [ ] `python3 scripts/firmendaten.py --produktion` läuft ohne Fehler
- [ ] Gewerberechtliche Fragen (Abschnitt 3) mit der Handwerkskammer geklärt
- [ ] AV-Verträge mit Hoster und Mailanbieter abgeschlossen
- [ ] Impressum und Datenschutzerklärung anwaltlich oder durch einen Generator eines Kammer-/Verbandsangebots gegengeprüft
- [ ] Bildrechte aller veröffentlichten Fotos dokumentiert
- [ ] Testanfrage über das Live-Formular abgeschickt und im Postfach angekommen – einmal mit Foto und Rückrufwunsch
- [ ] Hinweis: Diese Liste ersetzt keine Rechtsberatung. Eine vollständige DSGVO-Konformität kann erst nach rechtlicher und technischer Freigabe im Betrieb festgestellt werden.
