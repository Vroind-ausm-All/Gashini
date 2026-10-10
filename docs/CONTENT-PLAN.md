# Content-Plan

Alle Texte der Website stehen in `src/seiten/*.html` (Seiten) und `data/faq.json` (Fragen). Dieses Dokument enthält die
Varianten, Vorlagen und Begründungen dazu – und die Liste aller Aussagen, die noch bestätigt werden müssen.

**Tonalität:** persönlich, direkt, sachlich. Kurze Sätze, aktive Verben, konkrete Arbeiten statt Adjektive.
Keine Superlative, kein „kompetenter Partner“, keine Versprechen ohne Beleg.

## 1. Hero-Headlines – fünf Varianten

| # | Headline | Wann sinnvoll |
|---|---|---|
| **1** | **Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner.** *(umgesetzt)* | Trägt das Netzwerk als Unterschied. Funktioniert, wenn die Zusammenarbeit mit Partnern tatsächlich gelebt wird. |
| 2 | Von der kleinen Reparatur bis zum abgestimmten Ausbau. | Betont die Bandbreite; neutraler, weniger einprägsam. |
| 3 | Wände, Decken, Kleinigkeiten. Und jemand, der sich kümmert. | Konkreter, handwerklicher, persönlicher – stärker Richtung Privatkunden. |
| 4 | Was an Ihrer Immobilie ansteht, landet bei einer Person. | Spricht Vermieter und Verwaltungen an, die sonst koordinieren müssen. |
| 5 | Trockenbau und Hausmeisterservice in {{ORT}}. Auch für kleine Aufträge. | Suchbegriff in der Überschrift; nüchtern, aber für die Startseite als Landingpage stärker. |

## 2. Positionierung – drei Varianten

**A · Der eine Ansprechpartner** *(Grundlage der Umsetzung)*
Für Eigentümer, Vermieter und kleinere Gewerbebetriebe, die rund um ihre Immobilie nicht mehrere Betriebe koordinieren
wollen, ist Gashini der feste Ansprechpartner: Trockenbau, Hausmeisterservice und Reparaturen selbst, alles Weitere
über bekannte Fachbetriebe – mit klarer Aussage, wer was ausführt und wer Vertragspartner ist.

**B · Der Spezialist für das Kleine**
Für Arbeiten, die für größere Betriebe zu klein sind: eine Wand, eine Decke, ein Raum, eine Wohnung zwischen zwei
Mietern. Schnell eingeschätzt, ordentlich erledigt. – *Risiko:* zieht kleine Aufträge an, ohne den Wert pro Auftrag zu
heben. Nur sinnvoll, wenn die Auslastung das Ziel ist.

**C · Der Betreuer für Vermieter und Verwaltungen**
Laufende Objektbetreuung mit Trockenbau-Kompetenz: Mieterwechsel vorbereiten, Schäden beheben, Fachbetriebe
koordinieren. – *Risiko:* engt die Zielgruppe ein; stark, wenn Rahmenverträge das Geschäftsmodell sind.

> Die frühere Positionierung „Räumen, renovieren, reinigen bis zum Übergabetermin“ (`strategie/01-strategie.md`) passt
> nicht mehr zum jetzt beschriebenen Leistungsumfang ohne Reinigung und Entrümpelung. Sie bleibt als Dokument erhalten.

## 3. Startseite – Aufbau und Texte

Umgesetzt in `src/seiten/startseite.html`. Reihenfolge entlang der Fragen eines Besuchers:

| Abschnitt | Frage des Besuchers | Kernaussage |
|---|---|---|
| A · Einstieg | Bin ich hier richtig? | Kleine Arbeiten. Großes Netzwerk. Ein Ansprechpartner. |
| B · Leistungen | Macht ihr, was ich brauche? | Vier Bereiche, offen benannt, was nicht |
| C · Kleine Projekte | Lohnt sich meine kleine Anfrage? | Nicht jedes Vorhaben braucht eine Großbaustelle. |
| D · Projekte | Kann ich das sehen? | Nur freigegebene, eigene Arbeiten – sonst ehrlicher Leerzustand |
| E · Netzwerk | Wer macht was, wer haftet? | Drei Formen der Zuständigkeit mit Vertragspartner |
| F · Ablauf | Was passiert nach meiner Anfrage? | Vier Schritte ohne Zeitversprechen |
| G · Abschluss | Wie fange ich an? | Was steht bei Ihnen an? – auch wenn es nur eine kleine Arbeit ist. |

## 4. Leistungsbeschreibungen

Jede Leistungsseite folgt derselben Struktur: Problem → für wen → typische Arbeiten → was wir brauchen →
wann eine Besichtigung sinnvoll ist → was wir nicht selbst ausführen → Fragen. Umgesetzt in
`src/seiten/trockenbau.html`, `hausmeisterservice.html`, `reparatur.html`, Übersicht in `leistungen.html`.

## 5. Netzwerk

Kernsatz: *„Das heißt nicht, dass wir jedes Gewerk anbieten – sondern dass wir wissen, wen wir fragen.“*
Drei Formen, je mit Vertragspartner: **Eigene Leistung** (Gashini) · **Koordinierte Gewerke** (steht im Angebot) ·
**Empfehlung** (der Fachbetrieb). Umgesetzt auf Startseite (Kurzform) und Über uns (`#netzwerk`).

## 6. Kontakt-CTAs

| Ort | Text | Begründung |
|---|---|---|
| Kopfbereich, Hero | **Projekt anfragen** | aktiv, ohne Mindestgröße zu suggerieren |
| Abschluss jeder Seite | **Unverbindlich anfragen** | nimmt die letzte Hürde |
| Formular | **Anfrage senden** | beschreibt genau, was passiert |
| Mobil, fest unten | **Anrufen** · **Anfragen** | zwei Wege, gleichwertig |
| Sekundär | **Arbeiten ansehen** · **Vorhaben besprechen** | für Unentschlossene |

## 7. Vorlage für Projektbeschreibungen

Für `data/projekte.json`. Sachlich, ohne Kundendaten, ohne Superlative. 60–120 Wörter je Feld genügen.

```
Titel:              Was ist entstanden? (z. B. „Trennwand für ein zusätzliches Arbeitszimmer“)
Kurztext:           Ein Satz, der in der Karte steht.
Ausgangssituation:  Wie sah es vorher aus, was war das Ziel des Auftraggebers?
Leistungsumfang:    3–6 Stichpunkte, nur tatsächlich ausgeführte Arbeiten.
Vorgehen:           Was wurde in welcher Reihenfolge gemacht? Gab es Besonderheiten im Bestand?
Ergebnis:           Was hat sich für den Auftraggeber verändert?
Ausführung:         eigener-betrieb | partner | gemeinsam – ehrlich angeben.
Region:             nur so genau wie freigegeben („Nordstadt“, nicht Straße).
```

## 8. Häufige Fragen

Zwölf Fragen in `data/faq.json`, jeweils den passenden Seiten zugeordnet; die Ablaufseite zeigt alle und zeichnet sie
als `FAQPage` aus. Neue Fragen dort ergänzen. Antworten ohne Versprechen, die nicht sicher gehalten werden.

## 9. Bild- und Medienliste

Siehe `docs/ASSET-BRIEFS.md`.

## 10. Nicht bestätigte Aussagen – Freigabe erforderlich

Diese Inhalte sind im Quelltext markiert. Die Vorschau zeigt sie sichtbar; der Produktions-Build bricht ab, solange
einer offen ist.

| Wo | Was ist zu bestätigen |
|---|---|
| `leistungen.html` | Werden Reinigung, Entrümpelung, Umzüge weiterhin angeboten? |
| `leistungen.html` | Abgrenzung gegen Gewerbe- und Handwerksrolleneintrag (Maler, Fliesen, Boden) |
| `trockenbau.html` | Leistungsliste gegen Eintrag als Trockenbaumonteur |
| `hausmeisterservice.html` | Winterdienst, Grünpflege, Reinigung von Allgemeinflächen |
| `reparatur.html` | Leistungsliste, Abgrenzung zu zulassungspflichtigen Handwerken |
| `ueber-uns.html` | Gewerke im Netzwerk und Form der Zusammenarbeit |
| `kontakt.html` | verbindliche Telefon- und Reaktionszeiten |
| `data/firmendaten.env` | alle Werte in `[eckigen Klammern]`, u. a. Versicherung, Einsatzgebiet, Inhabertext |
| `data/projekte.json` | echte Projekte mit Freigabe (derzeit nur Beispiele im Status „entwurf“) |
