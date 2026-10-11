# Herkunft der Symbolbilder

Die Bilder in diesem Verzeichnis hat der Betreiber am 11.10.2026 bereitgestellt. Sie zeigen typische
Trockenbau-Situationen, **keine Aufträge von Gashini Dienstleistungen**. Ob sie KI-generiert sind oder aus einer
Bildagentur stammen, ist noch nicht dokumentiert. Bis das geklärt ist, steht `SYMBOLBILD_QUELLE` in
`data/firmendaten.env` in eckigen Klammern; der Produktions-Build bricht dann ab.

| Datei | Inhalt | Verwendet auf |
|---|---|---|
| trockenbau-beplankung | Gipsplatten werden mit dem Akkuschrauber auf das Ständerwerk geschraubt | Trockenbau, Titelbild |
| innenausbau-altbau | Altbauwohnung mit beplankten, gespachtelten Wänden | Leistungen, Zeile Trockenbau |
| dachgeschoss-beplankt | Dachgeschoss mit verkleideten Schrägen und Dachfenster | Trockenbau, „Wofür“ (Freigabe offen: nur, wenn Dachschrägen angeboten werden) |
| fuge-streiflicht | Frisch gespachtelte Fuge im Streiflicht, Nahaufnahme | Startseite, „Auch kleine Aufträge“ |
| ablauf-beplanken-spachteln | Drei Schritte nebeneinander: Platte ansetzen, verschrauben, spachteln | Trockenbau, „Auf der Baustelle“ |

Varianten: 640, 1280 und 1536 px breit (WebP). Die Quelle ist 1536 px breit, deshalb gibt es keine 1920er Variante.
Die Dateien enthalten keine Metadaten (EXIF, Ort).

Regeln:

- Einbinden nur über den Baustein `[[symbolbild datei="symbol/…" alt="…"]]`. Er setzt „Symbolbild:“ vor den Alt-Text
  und eine sichtbare Marke ins Bild. Die Bildunterschrift endet mit „Kein Projektfoto.“
- Nie als Projektbild in `data/projekte.json`, nie auf „Über uns“ (dort nur eigene Fotos laut Fotobriefing).
  `tests/pruefen.py` prüft beides.
- Wenn die Bilder KI-generiert sind, die Unterschriften auf „Symbolbild (KI-generiert)“ ändern und das im
  Impressum unter `SYMBOLBILD_QUELLE` angeben.
