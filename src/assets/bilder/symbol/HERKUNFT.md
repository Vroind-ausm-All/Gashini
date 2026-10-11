# Herkunft der Symbolbilder

Alle Bilder in diesem Verzeichnis zeigen typische Situationen, **keine Aufträge von Gashini Dienstleistungen**. Sie
stehen deshalb nur auf Leistungsseiten, der Startseite, „Netzwerk“ und der 404-Seite – nie bei den Projekten und nie
auf „Über uns“.

Es gibt zwei Lieferungen:

1. **11.10.2026, fünf Bilder** (obere Tabelle): Ob sie KI-generiert sind oder aus einer Bildagentur stammen, ist noch
   nicht dokumentiert. Sie tragen die Marke „Symbolbild“.
2. **12.10.2026, sechs Bilder** (untere Tabelle, ZIP „Gashini-Bilder“): Motive S1, S3 und S7–S10 aus
   `docs/MEDIENLISTE.md`. **Nachweislich KI-generiert:** Jede Originaldatei (PNG, 1536 px) enthält einen
   C2PA-Herkunftsnachweis mit Erzeuger „ChatGPT“ (OpenAI) und dem Quelltyp `trainedAlgorithmicMedia`. Sie tragen die
   Marke „Symbolbild · KI“ und den Alt-Text-Anfang „Symbolbild (KI-generiert):“. Die WebP-Varianten enthalten den
   Nachweis nicht mehr (beim Umrechnen entfallen alle Metadaten) – die Kennzeichnung auf der Seite ersetzt ihn.
   Noch zu bestätigen: Nutzungsbedingungen von OpenAI für die gewerbliche Verwendung.

Bis beides geklärt ist, steht `SYMBOLBILD_QUELLE` in `data/firmendaten.env` in eckigen Klammern; der
Produktions-Build bricht dann ab.

| Datei | Inhalt | Verwendet auf |
|---|---|---|
| trockenbau-beplankung | Gipsplatten werden mit dem Akkuschrauber auf das Ständerwerk geschraubt | Trockenbau, Titelbild · Startseite, Karte 01 |
| innenausbau-altbau | Altbauwohnung mit beplankten, gespachtelten Wänden | Leistungen, Zeile Trockenbau |
| dachgeschoss-beplankt | Dachgeschoss mit verkleideten Schrägen und Dachfenster | Trockenbau, „Wofür“ (Freigabe offen: nur, wenn Dachschrägen angeboten werden) |
| fuge-streiflicht | Frisch gespachtelte Fuge im Streiflicht, Nahaufnahme | Startseite, „Auch kleine Aufträge“ |
| ablauf-beplanken-spachteln | Drei Schritte nebeneinander: Platte ansetzen, verschrauben, spachteln | Trockenbau, „Auf der Baustelle“ |

| Datei | Inhalt | Herkunft | Medienliste | Verwendet auf |
|---|---|---|---|---|
| wand-ausbessern-spachteln | Loch in einer Innenwand wird mit Spachtel und Spachtelmasse ausgebessert | KI-generiert | S1 | Reparatur, Titelbild · Startseite, Karte 02 |
| treppenhaus-mehrfamilienhaus | Gepflegtes Treppenhaus mit Briefkastenanlage, Steintreppe und Geländer | KI-generiert | S3 | Hausmeisterservice, Titelbild · Startseite, Karte 03 |
| abstimmung-grundriss | Zwei Personen zeigen auf einen Grundriss, daneben Zollstock und Laser-Entfernungsmesser | KI-generiert | S7 | Netzwerk, „Ablauf“ |
| abgehaengte-decke-montage | Abgehängte Decke im Bau, Metallprofile zur Hälfte beplankt | KI-generiert | S8 | Trockenbau, „Wofür“ |
| kontrollgang-kellerflur | Kontrollgang im Kellerflur, Taschenlampe am Wandsockel | KI-generiert | S9 | Hausmeisterservice, „Für wen“ · Leistungen, Zeile Hausmeisterservice |
| loch-in-der-wand | Loch in heller Wand über der Sockelleiste, Gipsreste am Boden | KI-generiert | S10 | Leistungen, Zeile Reparatur · 404-Seite |

Varianten: 640, 1280 und 1536 px breit (WebP). Die Quellen sind höchstens 1536 px breit, deshalb gibt es keine
1920er Variante. Die Dateien enthalten keine Metadaten (EXIF, Ort, Prompt). Die Dateinamen beschreiben das Motiv, weil
Suchmaschinen auch den Dateinamen lesen.

Regeln:

- Einbinden nur über den Baustein `[[symbolbild datei="symbol/…" alt="…"]]`, bei KI-Bildern mit `ki="ja"`. Er setzt
  „Symbolbild:“ bzw. „Symbolbild (KI-generiert):“ vor den Alt-Text und eine sichtbare Marke ins Bild. Die
  Bildunterschrift endet mit „Kein Projektfoto.“
- Alt-Texte beschreiben, was zu sehen ist – sachlich, in einem Satz, ohne Ortsnamen und ohne Aufzählung von
  Suchbegriffen. Ein Ortsname im Alt-Text eines Symbolbilds würde einen Einsatz vor Ort vortäuschen.
- Nie als Projektbild in `data/projekte.json`, nie auf „Über uns“ oder den Projektseiten. `tests/pruefen.py` prüft
  das, ebenso, dass die Kennzeichnung „KI-generiert“ im Build mit der Spalte „Herkunft“ oben übereinstimmt.
- Stellt sich heraus, dass auch die erste Lieferung KI-generiert ist: in der oberen Tabelle eine Spalte „Herkunft“ mit
  „KI-generiert“ ergänzen, auf den Seiten `ki="ja"` setzen und die Unterschriften anpassen.
