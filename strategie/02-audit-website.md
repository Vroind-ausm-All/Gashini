# Ist-Analyse der Website — vier Fachperspektiven
Geprüft: Stand vor dieser Überarbeitung (Commit `d48a10f`), statische Website in `web/`

Jede Disziplin hat denselben Stand unabhängig geprüft. Befunde sind nach Schwere sortiert:
**A** = blockiert das Ziel · **B** = kostet messbar Anfragen · **C** = Feinschliff.
Spalte „Status": ✅ in dieser Überarbeitung behoben · ⏳ offen, braucht Daten oder Entscheidung des Betriebs.

---

## 2.1 Senior Web Development

| # | Schwere | Befund | Maßnahme | Status |
|---|---|---|---|---|
| WD-1 | **A** | Das Kontaktformular hat kein Ziel. `action` zeigt auf einen Platzhalter — abgesendete Anfragen gehen ins Leere. | Formulardienst anbinden, Weiterleitung auf `danke.html`, Bestätigungsmail an den Absender | ⏳ braucht Anbieterentscheidung |
| WD-2 | **A** | Kein Schutz gegen Spam. Ein offenes Formular ohne Honeypot oder Rate-Limit ist binnen Tagen zugemüllt — echte Anfragen gehen im Rauschen unter. | Honeypot-Feld + Zeitstempel-Prüfung ergänzt; serverseitig zusätzlich Rate-Limit des Anbieters aktivieren | ✅ / ⏳ |
| WD-3 | **B** | Schriften werden render-blockierend von Google geladen: zwei Verbindungen zu fremden Hosts vor dem ersten Textbild. Auf Mobilfunk verzögert das den sichtbaren Text spürbar. | `display=swap` ist gesetzt, zusätzlich `preload`; mittelfristig Schriften lokal ablegen (löst gleichzeitig DS-1) | ✅ teilweise |
| WD-4 | **B** | Keine Bilder vorhanden — dadurch zwar schnell, aber ohne `width`/`height`-Vorgaben auf dem Logo entsteht beim späteren Einbau von Fotos Layoutversatz. | Feste Maße am Logo, `loading="lazy"` und `decoding="async"` als Vorgabe dokumentiert | ✅ |
| WD-5 | **C** | `robots.txt` und `sitemap.xml` liegen im Ordner `web/`, nicht in der Domainwurzel. Beim Hochladen nur des Ordnerinhalts stimmt das — beim Hochladen des Ordners selbst nicht. | Im README als Stolperstein dokumentiert | ✅ |
| WD-6 | **C** | Keine Fehlerseite. Ein Tippfehler in der URL führt zur Standardseite des Hosters. | `404.html` ergänzt, die zurück in die Anfragestrecke führt | ✅ |
| WD-7 | **B** | Keine Sicherheits-Header und kein erzwungenes HTTPS konfigurierbar, weil rein statisch. | `.htaccess`-Vorlage mit HTTPS-Weiterleitung, HSTS und `X-Content-Type-Options` beigelegt | ✅ |

---

## 2.2 Senior SEO & Organic Growth

| # | Schwere | Befund | Maßnahme | Status |
|---|---|---|---|---|
| SEO-1 | **A** | **Die Seite rankt für nichts, was jemand sucht.** Die H1 lautet „Sauber. Gepflegt. Termintreu." — ein Claim ohne Suchvolumen. Kein Ort, keine Leistung, kein Anlass in der wichtigsten Überschrift. | H1 der Startseite auf Leistung + Ort umgestellt, Claim rückt in die Bildmarke | ✅ |
| SEO-2 | **A** | Keine Seiten für die Anlässe, nach denen tatsächlich gesucht wird („Wohnungsauflösung", „Entrümpelung mit Festpreis", „Wohnung besenrein übergeben"). Alle vier Gewerke teilen sich eine Leistungsseite und konkurrieren dort miteinander. | Zwei Anlassseiten ergänzt: `wohnungsuebergabe.html`, `haushaltsaufloesung.html` — je ein Suchanlass, je eine Seite | ✅ |
| SEO-3 | **A** | Local SEO fehlt vollständig: kein Google Unternehmensprofil verlinkt, keine NAP-Konsistenz definiert, kein Einsatzgebiet in Textform. Für einen lokalen Dienstleister ist das der wichtigste Ranking-Faktor überhaupt — wichtiger als jede Onpage-Maßnahme. | Einsatzgebiet als Textblock mit Ortsliste ergänzt; Google-Profil als Maßnahme 1.2 in die Roadmap | ✅ / ⏳ |
| SEO-4 | **B** | Title-Tags beginnen mit dem Firmennamen. Der Name hat null Suchvolumen; in der Ergebnisliste wird der wichtigste Teil abgeschnitten. | Titles nach Muster `Leistung + Ort \| Gashini Dienstleistungen` | ✅ |
| SEO-5 | **B** | Strukturierte Daten nur auf der Startseite und ohne `areaServed`-Details, ohne `FAQPage`, ohne `priceRange`. | `LocalBusiness` erweitert, FAQ-Auszeichnung auf der Ablaufseite ergänzt | ✅ |
| SEO-6 | **B** | Keine interne Verlinkung mit sprechenden Ankertexten. Die Leistungsseite verlinkt nur über „Mehr erfahren →". | Kontextlinks mit Leistungsbegriffen eingebaut | ✅ |
| SEO-7 | **C** | Keine `lastmod`-Angaben in der Sitemap, Prioritäten willkürlich gesetzt. | Sitemap um `lastmod` ergänzt, Prioritäten an der Anfragestrecke ausgerichtet | ✅ |

> **Wichtigster Satz dieses Abschnitts:** Für einen Handwerks- und Dienstleistungsbetrieb mit lokalem Radius bringt ein vollständig gepflegtes Google-Unternehmensprofil mehr Anfragen als jede Onpage-Optimierung. Die Website ist Beweisfläche — das Profil ist der Kanal.

---

## 2.3 Senior UI/UX & Digital Design

| # | Schwere | Befund | Maßnahme | Status |
|---|---|---|---|---|
| UX-1 | **A** | **Die Startseite beantwortet die Frage des Besuchers nicht.** Wer mit „Ich muss meine Wohnung bis zum 30. räumen" kommt, findet vier gleichwertige Gewerkekacheln und muss selbst zusammensetzen, ob der Betrieb sein Problem löst. | Einstieg nach Anlass („Was steht bei Ihnen an?") vor die Gewerkeliste gesetzt | ✅ |
| UX-2 | **A** | Keine einzige echte Abbildung. Bei einem Gewerk, dessen Ergebnis man *sieht*, ist eine bildlose Website ein Substanzmangel, kein Stilthema. | Bildplätze mit klaren Vorgaben (Vorher/Nachher, Format, Bildunterschrift) angelegt; Fotoroutine als Maßnahme 2.4 | ✅ Struktur / ⏳ Fotos |
| UX-3 | **B** | Vier gleich aussehende Karten nebeneinander erzeugen keine Hierarchie — alles ist gleich wichtig, also nichts. | Primäranlässe hervorgehoben, Einzelleistungen sekundär gesetzt | ✅ |
| UX-4 | **B** | Das Formular fragt sechs Felder ab, bevor irgendein Nutzen erkennbar ist. Jedes Pflichtfeld kostet Abschlüsse. | Auf vier Pflichtfelder reduziert, Alternativwege (Anruf, WhatsApp-Fotos) gleichrangig daneben | ✅ |
| UX-5 | **B** | Kein Hinweis darauf, was nach dem Absenden passiert. Unklarheit an dieser Stelle ist ein klassischer Abbruchgrund. | Erwartung explizit formuliert („Rückmeldung am selben Werktag, dann Besichtigung oder Festpreis per Mail") | ✅ |
| UX-6 | **C** | Die mobile Anrufleiste verdeckt am Seitenende Inhalte. | Abstand am Seitenfuß erhöht | ✅ |
| UX-7 | **C** | Kein Skip-Link zum Inhalt, Navigation nur per Maus gut bedienbar. | Skip-Link ergänzt, Fokusreihenfolge geprüft | ✅ |

---

## 2.4 Senior Analytics & CRO

| # | Schwere | Befund | Maßnahme | Status |
|---|---|---|---|---|
| CRO-1 | **A** | **Es wird nichts gemessen.** Weder Seitenaufrufe noch Anrufe noch Formularabsendungen. Ohne Messung ist die Leitkennzahl „Anteil Direktanfragen" nicht bestimmbar — und das 90-Tage-Ziel damit nicht überprüfbar. | Messkonzept mit datensparsamer Lösung definiert (Abschnitt 2.5), Anfragetabelle als Minimalvariante | ✅ Konzept / ⏳ Einrichtung |
| CRO-2 | **A** | Keine Quellenkennzeichnung. Eine Anfrage, die über MyHammer, den Flyer oder den Transporter kam, ist im Formular nicht unterscheidbar. | Feld „Wie sind Sie auf uns aufmerksam geworden?" ergänzt — die einfachste belastbare Quellenmessung für kleine Betriebe | ✅ |
| CRO-3 | **A** | Kein Preisanker. Ohne jede Orientierung entscheidet der Besucher, beim Portal drei Vergleichsangebote zu holen — genau das Verhalten, das der Betrieb loswerden will. | Preisorientierungsseite mit Spannen und drei Beispielrechnungen ergänzt | ✅ Struktur / ⏳ Zahlen vom Betrieb |
| CRO-4 | **B** | Vier verschiedene Handlungsaufforderungen konkurrieren („Angebot anfordern", „Kostenloses Angebot", „Jetzt anrufen", „Direkt anfragen"). Uneinheitliche CTAs senken die Klickrate. | Auf eine primäre Aktion pro Seite vereinheitlicht: **Festpreis anfragen**. Anrufen bleibt sekundär, aber überall sichtbar | ✅ |
| CRO-5 | **B** | Keine Reibungsentferner an der Entscheidungsstelle: Niemand nennt vor dem Formular, dass die Besichtigung kostenlos und unverbindlich ist. | Vertrauenszeile direkt über dem Absendeknopf | ✅ |
| CRO-6 | **B** | Bewertungen sind auf einer eigenen Unterseite geparkt, die kaum jemand ansteuert. Sozialer Beweis wirkt dort, wo entschieden wird. | Bewertungsbeleg auf Start-, Anlass- und Kontaktseite gezogen | ✅ |
| CRO-7 | **C** | Telefonnummer nicht in der Kopfzeile auf Desktop klickbar hervorgehoben. | Nummer in der Servicezeile prominent, mobil zusätzlich als feste Leiste | ✅ |

---

## 2.5 Messkonzept (Minimalvariante, DSGVO-arm)

Bewusst klein gehalten — passend zu 1–3 Stunden pro Woche:

1. **Anfragetabelle** (Tabellenkalkulation, drei Spalten: Datum · Quelle · Ergebnis). Ersetzt zu Beginn jedes Analysewerkzeug und liefert die Leitkennzahl direkt.
2. **Google-Unternehmensprofil-Statistik** — kostenlos, zeigt Aufrufe, Anrufe und Wegbeschreibungen ohne eigene Einrichtung.
3. **Formularfeld „Wie sind Sie auf uns aufmerksam geworden?"** — verknüpft Online-Anfragen mit ihrer Quelle.
4. **Erst wenn 1–3 laufen:** ein cookiefreies Web-Analysewerkzeug einrichten. Ohne Cookies entfällt das Einwilligungsbanner, was auf einer Seite mit einer einzigen Handlungsaufforderung erheblich Reibung spart.

**Nicht empfohlen in Phase 1:** vollständiges Tag-Management, A/B-Tests, Heatmaps. Bei der zu erwartenden Besucherzahl liefern diese Werkzeuge keine statistisch belastbaren Aussagen, kosten aber Einrichtungszeit.

---

## 2.6 Website Guardian — laufende Kontrolle

Prüfroutine, die dauerhaft gilt. Vorschlag: einmal pro Quartal, 30 Minuten.

| Prüfpunkt | Warum |
|---|---|
| Alle Platzhalter `{{…}}` ersetzt? | Ein sichtbarer Platzhalter zerstört Vertrauen sofort |
| Impressum und Datenschutz aktuell (Kammer, Versicherung, Hoster)? | Abmahnrisiko |
| Telefon, E-Mail, Adresse identisch mit Google-Profil und Portalen? | NAP-Konsistenz ist Local-SEO-Grundlage |
| Formular getestet — kommt eine Testanfrage wirklich an? | Häufigster stiller Totalausfall bei kleinen Websites |
| Bewertungsanzahl auf der Website = tatsächliche Anzahl? | Falsche Zahlen sind wettbewerbsrechtlich angreifbar |
| Schrift- und Bildlizenzen unverändert gültig? | Rechtssicherheit |
| Seite lädt unter 2,5 s auf dem Mobilfunk? | Rankingfaktor und Absprungquelle |
| Backup der Dateien vorhanden? | Der Hoster sichert nicht immer |
