# Vom Erstkontakt zum Bestandskunden
Senior CRM & Marketing Automation

**Ausgangsbefund:** Bei Betrieben dieser Größe verliert sich der größte Teil des Potenzials nicht bei der Akquise, sondern **nach** dem Erstkontakt: Angebote werden geschrieben und nie nachgefasst, zufriedene Kunden werden nie wieder angesprochen. Diese Strecke kostet kein Werbebudget — nur Verbindlichkeit.

## 6.1 Die Strecke

```
Anfrage → Qualifizierung → Besichtigung → Angebot → Nachfassen → Auftrag → Abschluss → Bestandskunde
```

| Stufe | Auslöser | Was passiert | Frist | Womit |
|---|---|---|---|---|
| **1 Anfrage** | Formular, Anruf, WhatsApp, Portal | In die Anfragetabelle eintragen: Datum, Quelle, Anlass, Objekt, Wunschtermin | sofort | Tabelle |
| **2 Qualifizierung** | Eintrag steht | Drei Fragen klären: Wo? Was genau? Bis wann? Passt es nicht, **sofort und freundlich absagen** — eine schnelle Absage ist besser als ein verschlepptes Angebot | ≤ 1 Werktag | Telefon |
| **3 Besichtigung** | Auftrag ist relevant | Termin binnen 3 Werktagen. Bei kleinen Aufträgen ersetzen Fotos + Quadratmeter die Fahrt | ≤ 3 Werktage | Kalender |
| **4 Angebot** | Besichtigung erfolgt | Schriftlich, Festpreis, Leistungen einzeln aufgeführt, **Gültigkeit 14 Tage**, Termin reserviert bis Datum X | ≤ 2 Werktage | Vorlage |
| **5 Nachfassen** | Angebot raus | **Tag 3:** kurzer Anruf — „Sind Fragen offen?" · **Tag 10:** letzte Nachricht mit Terminhinweis | Tag 3 / Tag 10 | Erinnerung |
| **6 Auftrag** | Zusage | Auftragsbestätigung mit Termin, Ansprechpartner, Handynummer | ≤ 1 Werktag | Vorlage |
| **7 Abschluss** | Arbeit fertig | Gemeinsame Abnahme, Fotos, Rechnung binnen 3 Tagen, **am selben Tag** Bitte um Bewertung | Tag 0–3 | Vorlage |
| **8 Bestandskunde** | 6 Monate später | Ein Kontakt mit passendem Anschlussangebot | Monat 6 | Wiedervorlage |

**Die beiden wirksamsten Stufen sind 5 und 8** — beide kosten zusammen etwa 20 Minuten pro Woche und erschließen Umsatz aus bereits bezahlten Leads.

## 6.2 Warum „Tag 3 und Tag 10"

Ein einzelnes Nachfassen ist der häufigste blinde Fleck kleiner Betriebe. Begründung der beiden Zeitpunkte:
- **Tag 3:** Das Angebot ist noch präsent, Vergleichsangebote sind meist noch nicht alle da. Hier wird die Entscheidung tatsächlich beeinflusst.
- **Tag 10:** Vier Tage vor Ablauf der Gültigkeit. Der Hinweis auf den reservierten Termin ist ein legitimer Anlass, kein Drängen.
- **Kein drittes Nachfassen.** Danach ist die Antwort Nein — auch wenn sie nicht ausgesprochen wurde.

## 6.3 Werkzeug

**Phase 1 — Tabelle genügt.** Eine Tabellenkalkulation mit diesen Spalten schlägt jedes CRM, das nicht gepflegt wird:

`Datum · Quelle · Name · Telefon · Ort · Anlass · Status · Angebotssumme · Wiedervorlage · Ergebnis`

Filter auf „Status = Angebot" + „Wiedervorlage ≤ heute" ergibt die tägliche Nachfassliste. Mehr braucht es unterhalb von etwa 30 Anfragen im Monat nicht.

**Phase 2 — ab etwa 30 Anfragen/Monat oder ab dem zweiten Mitarbeiter im Büro:** ein schlankes CRM mit Wiedervorlagen, Vorlagen und gemeinsamem Zugriff. Auswahlkriterien in dieser Reihenfolge: Bedienbarkeit auf dem Telefon, Serverstandort EU/AV-Vertrag, Import aus der bestehenden Tabelle, Kosten. **Nicht** nach Funktionsumfang auswählen — der Grund für gescheiterte CRM-Einführungen in kleinen Betrieben ist fast immer Überforderung, nie fehlende Funktion.

## 6.4 Automatisierung — was sich lohnt, was nicht

| Automatisierung | Empfehlung | Begründung |
|---|---|---|
| **Eingangsbestätigung** nach Formularabsendung | ✅ sofort | Bestätigt Eingang und Reaktionszeit, kostet nach Einrichtung nichts |
| **Erinnerung** an Nachfasstermine | ✅ sofort | Der Kalender erinnert zuverlässiger als das Gedächtnis |
| **Bewertungsbitte** nach Abschluss | ✅ sofort | Direkter Hebel auf die Leitkennzahl |
| **Wiedervorlage** nach 6 Monaten | ✅ ab Phase 2 | Günstigster Zweitauftrag, den es gibt |
| Mehrstufige E-Mail-Strecken | ❌ | Bei Einzelaufträgen mit Fristdruck entscheidet der Anruf, nicht die dritte Mail |
| Newsletter | ❌ | Kein Nachrichtenbedarf, hoher Pflegeaufwand, Einwilligungsthematik |
| Chatbot | ❌ | Ersetzt bei dieser Auftragsart kein Gespräch, schafft aber eine zusätzliche Fehlerquelle |

## 6.5 Textbausteine

**Eingangsbestätigung (automatisch)**
> Guten Tag {{Name}},
> Ihre Anfrage ist bei uns eingegangen. Wir melden uns am nächsten Werktag mit einer Einschätzung oder einem Terminvorschlag für die kostenlose Besichtigung.
> Wenn es eilt, rufen Sie uns gern direkt an: {{TELEFON}}.
> Freundliche Grüße, {{INHABER}} — Gashini Dienstleistungen

**Absage bei Nichtpassung (Stufe 2)**
> Guten Tag {{Name}},
> vielen Dank für Ihre Anfrage. Das können wir in diesem Fall leider nicht übernehmen — {{Grund, z. B. außerhalb unseres Einsatzgebiets}}. Damit Sie nicht weitersuchen müssen: {{Empfehlung}}.
> Freundliche Grüße

**Nachfassen Tag 3 (Telefon, sonst Mail)**
> Guten Tag {{Name}},
> unser Angebot vom {{Datum}} liegt Ihnen vor. Sind dazu Fragen offen, oder soll ich etwas anpassen?
> Den Termin am {{Datum}} halten wir Ihnen bis {{Datum + 11 Tage}} frei.

**Nachfassen Tag 10**
> Guten Tag {{Name}},
> unser Angebot gilt noch bis {{Datum}}. Danach kann ich den reservierten Termin nicht länger frei halten. Eine kurze Rückmeldung genügt — auch wenn Sie sich anders entschieden haben.

**Bewertungsbitte (Tag des Abschlusses)**
> Guten Tag {{Name}},
> vielen Dank für Ihren Auftrag. Wenn Sie zufrieden waren, würde ich mich über eine kurze Bewertung freuen — zwei Sätze genügen: {{Bewertungslink}}
> Falls etwas nicht gepasst hat, sagen Sie es bitte zuerst mir, dann kümmere ich mich darum.

**Wiedervorlage nach 6 Monaten**
> Guten Tag {{Name}},
> vor einem halben Jahr haben wir für Sie {{Leistung}} übernommen. Falls jetzt {{passende Anschlussleistung}} ansteht, melden Sie sich gern — Bestandskunden bekommen den Termin zuerst.

## 6.6 Kennzahlen dieser Strecke

| Kennzahl | Zielrichtung | Warum |
|---|---|---|
| Reaktionszeit auf Anfragen | ≤ 1 Werktag | Bei Fristsachen gewinnt oft schlicht der Schnellste |
| Anteil Anfragen mit Besichtigung | steigend | Zeigt Qualität der Anfragen |
| **Anteil Angebote mit Nachfassen** | 100 % | Die einzige Zahl in dieser Liste, die vollständig selbst steuerbar ist |
| Abschlussquote | steigend | Wirkung von Positionierung und Nachfassen |
| Bewertungen je 10 Aufträge | steigend | Speist den Direktkanal |
| Anteil Zweitaufträge | steigend | Zahlt direkt auf die Unabhängigkeit vom Portal ein |
