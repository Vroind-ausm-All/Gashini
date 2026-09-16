# -*- coding: utf-8 -*-
"""Erzeugt die Seiten von web/ aus einer Quelle. Nach Änderungen: python3 build2.py"""
import os, io
OUT = "/home/user/Gashini/web"

NAV = [("wohnungsuebergabe.html","Wohnungsübergabe"),
       ("haushaltsaufloesung.html","Haushaltsauflösung"),
       ("leistungen.html","Leistungen"),
       ("preise.html","Preise"),
       ("kontakt.html","Kontakt")]

def header(cur):
    items = "\n".join('        <li><a href="%s"%s>%s</a></li>' %
        (h, ' aria-current="page"' if h==cur else '', t) for h,t in NAV)
    return f"""<a class="skiplink" href="#inhalt">Zum Inhalt springen</a>
<div class="topbar">
  <div class="wrap">
    <span>Mo–Sa 7–20 Uhr · Rückmeldung am selben Werktag</span>
    <span><a href="tel:{{{{TELEFON_LINK}}}}">{{{{TELEFON}}}}</a> · <a href="mailto:{{{{EMAIL}}}}">{{{{EMAIL}}}}</a></span>
  </div>
</div>
<header class="site">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="../brand/logo.svg" width="320" height="80" alt="Gashini Dienstleistungen – Startseite"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="hauptmenue"><span class="balken"><span></span></span>Menü</button>
    <nav class="main" id="hauptmenue" aria-label="Hauptnavigation">
      <ul>
{items}
      </ul>
    </nav>
    <div class="header-cta"><a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a></div>
  </div>
</header>"""

FOOTER = """<footer class="site">
  <div class="wrap">
    <div class="footgrid">
      <div>
        <img src="../brand/logo-invers.svg" width="320" height="80" alt="Gashini Dienstleistungen" style="height:58px;width:auto">
        <p style="margin-top:16px">Wir räumen, renovieren und reinigen Ihre Immobilie bis zum vereinbarten Übergabetermin – ein Auftrag, ein Festpreis, ein Ansprechpartner.</p>
      </div>
      <div>
        <h4>Anlässe</h4>
        <ul>
          <li><a href="wohnungsuebergabe.html">Wohnungsübergabe</a></li>
          <li><a href="haushaltsaufloesung.html">Haushaltsauflösung</a></li>
          <li><a href="leistungen.html#reinigung">Gebäudereinigung</a></li>
          <li><a href="leistungen.html#hausmeister">Hausmeisterservice</a></li>
          <li><a href="leistungen.html#renovierung">Renovierung &amp; Maler</a></li>
        </ul>
      </div>
      <div>
        <h4>Unternehmen</h4>
        <ul>
          <li><a href="preise.html">Preise</a></li>
          <li><a href="ablauf.html">Ablauf &amp; Fragen</a></li>
          <li><a href="referenzen.html">Referenzen</a></li>
          <li><a href="ueber-uns.html">Über uns</a></li>
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutz</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>
        <ul>
          <li>{{STRASSE}}<br>{{PLZ_ORT}}</li>
          <li><a href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a></li>
          <li><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>
          <li><a href="{{MYHAMMER_URL}}" rel="noopener">MyHammer-Profil ↗</a></li>
          <li><a href="{{GOOGLE_PROFIL_URL}}" rel="noopener">Google-Profil ↗</a></li>
        </ul>
      </div>
    </div>
    <div class="copy">
      <span>© <span id="jahr">2026</span> Gashini Dienstleistungen · Inhaber {{INHABER}}</span>
      <span>Einsatzgebiet: {{EINSATZGEBIET}}</span>
    </div>
  </div>
</footer>
<div class="callbar">
  <a href="tel:{{TELEFON_LINK}}">Anrufen</a>
  <a href="kontakt.html">Festpreis anfragen</a>
</div>
<script src="assets/main.js"></script>"""

def page(fn, title, desc, body, extra_head=""):
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://{{{{DOMAIN}}}}/{fn}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/style.css">{extra_head}
</head>
<body>
{header(fn)}
<main id="inhalt">
{body}
</main>
{FOOTER}
</body>
</html>
"""
    io.open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)
    print("geschrieben:", fn)

# ---------- wiederverwendbare Bausteine ----------
VERTRAUEN = """<section class="vertrauensband">
  <div class="wrap">
    <ul>
      <li><strong>Festpreis</strong> nach kostenloser Besichtigung</li>
      <li><strong>Termin</strong> schriftlich zugesagt</li>
      <li><strong>Betriebshaftpflicht</strong> versichert</li>
      <li><strong>Rückmeldung</strong> am selben Werktag</li>
    </ul>
  </div>
</section>"""

def beweis(titel="Warum Kunden uns glauben"):
    return f"""<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Beweis statt Behauptung</span><h2>{titel}</h2></div>
    <div class="grid g3">
      <div class="card">
        <h3>Bewertungen, die wir nicht selbst schreiben</h3>
        <p class="mh-note-klein">{{{{MYHAMMER_NOTE}}}} <span class="mh-sterne" aria-hidden="true">★★★★★</span></p>
        <p>aus {{{{MYHAMMER_BEWERTUNGEN}}}} Bewertungen auf MyHammer – jede davon stammt aus einem tatsächlich vermittelten Auftrag.</p>
        <a class="more" href="{{{{MYHAMMER_URL}}}}" rel="noopener">Profil ansehen →</a>
      </div>
      <div class="card">
        <h3>Vorher und nachher</h3>
        <div class="bildplatz"><span>Platz für ein eigenes Vorher-/Nachher-Foto<br><small>Vorgaben: Dokument 03, Abschnitt 3.2</small></span></div>
        <p>Eigene Aufnahmen aus abgeschlossenen Aufträgen – keine gekauften Bilder.</p>
      </div>
      <div class="card">
        <h3>Hier sind wir unterwegs</h3>
        <p>{{{{EINSATZGEBIET}}}}</p>
        <p>Liegt Ihr Objekt außerhalb? Rufen Sie an – wenn wir es nicht übernehmen können, sagen wir es sofort und nennen Ihnen jemanden, der es kann.</p>
        <a class="more" href="tel:{{{{TELEFON_LINK}}}}">{{{{TELEFON}}}} →</a>
      </div>
    </div>
  </div>
</section>"""

def abschluss(titel="Sagen Sie uns, bis wann es fertig sein muss"):
    return f"""<section class="abschluss">
  <div class="wrap">
    <h2>{titel}</h2>
    <p>Besichtigung und Kostenvoranschlag sind kostenlos und unverbindlich. Sie erhalten Ihren Festpreis in der Regel innerhalb von 24 Stunden.</p>
    <div class="abschluss-aktionen">
      <a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a>
      <a class="btn btn-ghost" href="tel:{{{{TELEFON_LINK}}}}">Anrufen: {{{{TELEFON}}}}</a>
    </div>
  </div>
</section>"""

LD_LOCAL = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Gashini Dienstleistungen",
  "description": "Wohnungsauflösung, Entrümpelung, Übergaberenovierung und Endreinigung aus einer Hand – zum Festpreis und bis zum vereinbarten Übergabetermin.",
  "url": "https://{{DOMAIN}}/",
  "telephone": "{{TELEFON}}",
  "email": "{{EMAIL}}",
  "image": "https://{{DOMAIN}}/brand/logo.svg",
  "priceRange": "{{PREISNIVEAU}}",
  "address": { "@type": "PostalAddress", "streetAddress": "{{STRASSE}}", "postalCode": "{{PLZ}}", "addressLocality": "{{ORT}}", "addressCountry": "DE" },
  "areaServed": { "@type": "GeoCircle", "geoMidpoint": { "@type": "GeoCoordinates", "address": "{{PLZ_ORT}}" }, "description": "{{EINSATZGEBIET}}" },
  "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "07:00", "closes": "20:00" }],
  "founder": { "@type": "Person", "name": "{{INHABER}}" },
  "sameAs": ["{{MYHAMMER_URL}}", "{{GOOGLE_PROFIL_URL}}"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog", "name": "Leistungen",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Wohnungsauflösung und Entrümpelung" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Übergaberenovierung und Malerarbeiten" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Gebäudereinigung und Endreinigung" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Hausmeisterservice" } }
    ]
  }
}
</script>"""

# ================= Startseite =================
page("index.html",
 "Wohnungsauflösung, Entrümpelung &amp; Übergaberenovierung in {{ORT}} | Gashini Dienstleistungen",
 "Räumen, renovieren, reinigen bis zum Übergabetermin – aus einer Hand und zum Festpreis. Gashini Dienstleistungen für {{EINSATZGEBIET}}. Kostenlose Besichtigung.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Wohnungsauflösung · Übergaberenovierung · Endreinigung in {{ORT}}</span>
    <h1>Räumen, renovieren, reinigen –<br><span>bis zum Übergabetermin</span></h1>
    <p class="lead">Wenn eine Wohnung zu einem festen Termin fertig sein muss, koordinieren Sie normalerweise drei Firmen. Bei uns ist es ein Auftrag, ein Festpreis und ein Ansprechpartner, der auch selbst vor Ort steht.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a>
      <a class="btn btn-ghost" href="tel:{{TELEFON_LINK}}">Anrufen: {{TELEFON}}</a>
    </div>
    <p class="hero-fuss">Kostenlose Besichtigung · Rückmeldung am selben Werktag · {{EINSATZGEBIET}}</p>
  </div>
</section>
"""
 + VERTRAUEN +
"""
<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Wo gehören Sie dazu?</span>
      <h2>Was steht bei Ihnen an?</h2>
      <p>Die meisten Anfragen erreichen uns, weil ein Termin im Kalender steht. Wählen Sie den Fall, der Ihrem am nächsten kommt – dort steht, wie wir vorgehen und was es ungefähr kostet.</p>
    </div>
    <div class="grid g3 anlaesse">
      <a class="anlass" href="wohnungsuebergabe.html">
        <span class="anlass-label">Häufigster Fall</span>
        <h3>Ich muss eine Wohnung übergeben</h3>
        <p>Auszug steht an, der Vermieter erwartet die Wohnung geräumt, gestrichen und sauber. Wir machen alles drei und sind vor dem Übergabetermin fertig.</p>
        <span class="more">Wohnungsübergabe →</span>
      </a>
      <a class="anlass" href="haushaltsaufloesung.html">
        <h3>Ich muss einen Haushalt auflösen</h3>
        <p>Nach einem Todesfall oder einem Umzug ins Heim. Wir räumen vollständig, entsorgen mit Nachweis und übergeben besenrein – Sie müssen nicht dabei sein.</p>
        <span class="more">Haushaltsauflösung →</span>
      </a>
      <a class="anlass" href="leistungen.html">
        <h3>Ich brauche eine einzelne Leistung</h3>
        <p>Treppenhausreinigung, Winterdienst, Fenster, Malerarbeiten oder Hausmeisterservice – auch einzeln und regelmäßig, mit festem Plan.</p>
        <span class="more">Alle Leistungen →</span>
      </a>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Das Paket</span>
      <h2>Vier Gewerke, eine Reihenfolge</h2>
      <p>Der Grund, warum Übergaben schiefgehen, ist selten schlechte Arbeit – es ist die Reihenfolge. Wer streicht, bevor geräumt ist, streicht zweimal. Wir planen die Schritte als einen Ablauf.</p>
    </div>
    <ol class="paket">
      <li><span class="paket-nr">1</span><h3>Räumen</h3><p>Möbel, Hausrat, Keller und Dachboden. Verwertbares wird angerechnet, der Rest fachgerecht entsorgt – mit Nachweis, wenn Sie ihn brauchen.</p></li>
      <li><span class="paket-nr">2</span><h3>Instand setzen</h3><p>Dübellöcher, Silikonfugen, defekte Zargen, lose Fliesen. Das, was im Übergabeprotokoll sonst als Mangel landet.</p></li>
      <li><span class="paket-nr">3</span><h3>Streichen</h3><p>Wände, Decken, Türen und Heizkörper – in der Farbe, die der Mietvertrag verlangt.</p></li>
      <li><span class="paket-nr">4</span><h3>Reinigen &amp; übergeben</h3><p>Endreinigung inklusive Fenster, Bad und Küche. Auf Wunsch sind wir beim Übergabetermin dabei.</p></li>
    </ol>
    <p class="paket-fuss">Sie brauchen nur einen Teil davon? Dann rechnen wir nur den Teil ab. <a href="preise.html">Preisspannen ansehen</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Ehrlich gesagt</span>
      <h2>Dafür sind wir nicht die Richtigen</h2>
    </div>
    <div class="grid g3">
      <div class="card"><h3>Wenn nur der Preis zählt</h3><p>Wir sind nicht der günstigste Anbieter. Wer drei Vergleichsangebote einholt und das billigste nimmt, wird bei uns nicht fündig.</p></div>
      <div class="card"><h3>Bei Kernsanierungen</h3><p>Elektrik, Heizung, Statik und Bäder komplett neu – das ist Sache eines Sanierungsbetriebs. Wir sagen es Ihnen offen und nennen jemanden.</p></div>
      <div class="card"><h3>Bei „heute noch“</h3><p>Wir planen mit Puffer, damit zugesagte Termine halten. Das heißt auch: ganz kurzfristig geht es meistens nicht.</p></div>
    </div>
  </div>
</section>
"""
 + beweis() + abschluss(), extra_head=LD_LOCAL)

# ================= Anlassseite: Wohnungsübergabe =================
page("wohnungsuebergabe.html",
 "Wohnungsübergabe: räumen, streichen, reinigen in {{ORT}} | Gashini Dienstleistungen",
 "Übergaberenovierung zum Festpreis in {{ORT}}: entrümpeln, ausbessern, streichen und besenrein übergeben – fertig vor Ihrem Übergabetermin.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Für Mieter beim Auszug und Vermieter zwischen zwei Mietverhältnissen</span>
    <h1>Wohnung übergeben –<br><span>ohne Abzug von der Kaution</span></h1>
    <p class="lead">Wir räumen, bessern aus, streichen und reinigen, bis der Vermieter unterschreiben kann. Sie nennen uns den Übergabetermin, wir planen rückwärts.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a>
      <a class="btn btn-ghost" href="tel:{{TELEFON_LINK}}">Anrufen: {{TELEFON}}</a>
    </div>
    <p class="hero-fuss">Kostenlose Besichtigung · Festpreis in der Regel binnen 24 Stunden</p>
  </div>
</section>
"""
 + VERTRAUEN +
"""
<section>
  <div class="wrap">
    <div class="grid g2" style="gap:44px;align-items:start">
      <div>
        <span class="eyebrow">Das Problem</span>
        <h2>Zwischen Kündigung und Übergabe liegen selten mehr als drei Wochen</h2>
        <p>In dieser Zeit soll die Wohnung leer, ausgebessert, gestrichen und gereinigt sein. Wer das an drei Betriebe vergibt, koordiniert drei Termine, drei Rechnungen und trägt das Fristrisiko selbst – denn wenn der Maler zwei Tage später kommt, verschiebt sich alles Weitere.</p>
        <p>Wir übernehmen die vier Schritte als einen Auftrag und planen sie vom Übergabetermin rückwärts. Verzögert sich etwas, erfahren Sie es von uns, bevor Sie fragen.</p>
        <p><strong>Häufig unterschätzt:</strong> Nicht jede Schönheitsreparatur darf der Vermieter überhaupt verlangen. Wir sagen Ihnen bei der Besichtigung, was in Ihrem Fall üblicherweise anfällt – eine Rechtsberatung ersetzt das nicht, aber es bewahrt vor unnötigen Arbeiten.</p>
      </div>
      <div class="card karte-hervor">
        <h3>Was wir übernehmen</h3>
        <ul>
          <li>Restmöbel und Hausrat räumen, Keller und Dachboden inklusive</li>
          <li>Dübellöcher schließen, Wände spachteln</li>
          <li>Wände, Decken, Türen und Heizkörper streichen</li>
          <li>Tapeten entfernen oder erneuern</li>
          <li>Silikonfugen in Bad und Küche erneuern</li>
          <li>Bodenbeläge entfernen oder neu verlegen</li>
          <li>Endreinigung inklusive Fenster, Bad und Küche</li>
          <li>Auf Wunsch: Teilnahme am Übergabetermin</li>
        </ul>
        <a class="more" href="preise.html">Was kostet das? →</a>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Zeitplan</span><h2>Rückwärts vom Übergabetermin</h2>
    <p>So sieht ein typischer Ablauf aus, wenn Sie uns drei Wochen vorher anrufen. Bei kürzerer Frist sagen wir Ihnen ehrlich, ob wir sie noch halten können.</p></div>
    <ol class="zeitplan">
      <li><b>Tag 1</b><span>Anruf oder Formular. Wir klären Objekt, Umfang und Termin.</span></li>
      <li><b>Tag 2–3</b><span>Kostenlose Besichtigung vor Ort – oder Fotos per WhatsApp, wenn es schneller gehen soll.</span></li>
      <li><b>Tag 4</b><span>Schriftliches Festpreis-Angebot, 14 Tage gültig, Termin für Sie reserviert.</span></li>
      <li><b>Woche 2</b><span>Räumen und Entsorgen, anschließend Ausbesserungen.</span></li>
      <li><b>Woche 3</b><span>Malerarbeiten, danach Endreinigung.</span></li>
      <li><b>Übergabetag</b><span>Wohnung ist fertig. Auf Wunsch sind wir dabei.</span></li>
    </ol>
  </div>
</section>
"""
 + beweis("Was für uns spricht") + abschluss("Wann ist Ihr Übergabetermin?"))

# ================= Anlassseite: Haushaltsauflösung =================
page("haushaltsaufloesung.html",
 "Haushaltsauflösung &amp; Entrümpelung in {{ORT}} | Gashini Dienstleistungen",
 "Haushaltsauflösung in {{ORT}} zum Festpreis: vollständig räumen, fachgerecht entsorgen mit Nachweis, besenrein übergeben. Auch ohne Ihre Anwesenheit.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Für Erben, Angehörige und Betreuer</span>
    <h1>Eine Wohnung auflösen,<br><span>ohne selbst davorzustehen</span></h1>
    <p class="lead">Wir räumen vollständig, entsorgen fachgerecht mit Nachweis und übergeben die Wohnung besenrein. Auf Wunsch übernehmen wir anschließend auch Renovierung und Endreinigung.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a>
      <a class="btn btn-ghost" href="tel:{{TELEFON_LINK}}">Anrufen: {{TELEFON}}</a>
    </div>
    <p class="hero-fuss">Kostenlose Besichtigung · Auch aus der Ferne beauftragbar</p>
  </div>
</section>
"""
 + VERTRAUEN +
"""
<section>
  <div class="wrap">
    <div class="grid g2" style="gap:44px;align-items:start">
      <div>
        <span class="eyebrow">Wie wir arbeiten</span>
        <h2>Wenn jemand gestorben ist, ist der Zeitdruck das kleinere Problem</h2>
        <p>Meistens kommen mehrere Dinge zusammen: eine Räumungsfrist des Vermieters, ein Haushalt voller persönlicher Dinge und Angehörige, die nicht am selben Ort wohnen. Wir richten uns danach, wie viel Sie dabei sein möchten.</p>
        <p><strong>Vor dem Räumen:</strong> Wir gehen mit Ihnen durch, was aufgehoben werden soll – Dokumente, Fotoalben, Schmuck, Erinnerungsstücke. Diese Dinge werden getrennt gesammelt und übergeben, nicht entsorgt. Wenn Sie nicht dabei sein können, legen wir sie beiseite und schicken Ihnen Fotos, bevor irgendetwas entschieden wird.</p>
        <p><strong>Beim Räumen:</strong> Verwertbares wird angerechnet und senkt den Preis. Was entsorgt werden muss, geht getrennt nach Fraktionen zum Wertstoffhof – Sperrmüll, Elektro, Sondermüll. Den Entsorgungsnachweis bekommen Sie mit der Rechnung.</p>
        <p><strong>Danach:</strong> besenrein, auf Wunsch renoviert und endgereinigt, damit die Wohnung zurückgegeben oder verkauft werden kann.</p>
      </div>
      <div class="card karte-hervor">
        <h3>Gut zu wissen</h3>
        <ul>
          <li>Sie müssen nicht vor Ort sein – Schlüsselübergabe und Abstimmung gehen auch aus der Ferne</li>
          <li>Persönliche Unterlagen werden gesammelt und übergeben, nicht weggeworfen</li>
          <li>Verwertbares wird angerechnet</li>
          <li>Entsorgung getrennt nach Fraktionen, mit Nachweis</li>
          <li>Wir arbeiten auch mit Nachlassverwaltern und Betreuern zusammen</li>
          <li>Diskret: keine beschrifteten Container vor der Tür, wenn Sie das nicht möchten</li>
        </ul>
        <a class="more" href="preise.html">Preisspannen ansehen →</a>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Häufige Fragen</span><h2>Was Angehörige uns meistens fragen</h2></div>
    <div class="grid g2">
      <div class="card"><h3>Wir sind mehrere Erben – wer beauftragt?</h3><p>Eine Person genügt als Ansprechpartner, solange sie beauftragen darf. Wir stellen die Rechnung auf Wunsch auf die Erbengemeinschaft aus.</p></div>
      <div class="card"><h3>Was passiert mit Fundstücken?</h3><p>Geld, Schmuck, Dokumente und persönliche Unterlagen werden gesammelt und Ihnen übergeben. Das ist bei uns kein Entgegenkommen, sondern Teil des Auftrags.</p></div>
      <div class="card"><h3>Wie schnell geht das?</h3><p>Eine durchschnittliche Wohnung räumen wir in ein bis drei Tagen. Zwischen Ihrem Anruf und dem Beginn liegen meist einige Tage für Besichtigung und Planung.</p></div>
      <div class="card"><h3>Was, wenn wir noch nicht alles wissen?</h3><p>Das ist der Normalfall. Rufen Sie an, auch wenn die Frist noch unklar ist – dann wissen Sie zumindest, woran Sie sind.</p></div>
    </div>
  </div>
</section>
"""
 + beweis("Warum Angehörige uns beauftragen") + abschluss("Rufen Sie an, auch wenn noch nichts entschieden ist"))

# ================= Preise =================
page("preise.html",
 "Was kostet Entrümpelung, Renovierung &amp; Endreinigung? | Gashini Dienstleistungen",
 "Preisspannen für Haushaltsauflösung, Übergaberenovierung und Endreinigung in {{ORT}} – mit Beispielrechnungen und den Faktoren, die den Preis bestimmen.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Preise</span>
    <h1>Was kostet das?<br><span>Hier stehen die Spannen.</span></h1>
    <p class="lead">Die meisten Betriebe nennen erst nach der Besichtigung eine Zahl. Wir finden: Sie sollten vor dem ersten Telefonat wissen, ob wir überhaupt in Ihren Rahmen passen.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Orientierung</span>
      <h2>Richtwerte je Leistung</h2>
      <p>Alle Angaben sind Spannen aus abgeschlossenen Aufträgen, inklusive Material, Fahrt und Entsorgung, zuzüglich Umsatzsteuer. Der verbindliche Preis entsteht immer erst nach der Besichtigung – dann aber als Festpreis.</p>
    </div>
    <div class="tabelle-scroll">
      <table class="preise">
        <caption>Preisspannen Gashini Dienstleistungen</caption>
        <thead><tr><th scope="col">Leistung</th><th scope="col">Einheit</th><th scope="col">Spanne</th></tr></thead>
        <tbody>
          <tr><td>Entrümpelung / Haushaltsauflösung</td><td>je m² Wohnfläche</td><td>{{PREIS_ENTRUEMPELUNG}}</td></tr>
          <tr><td>Übergaberenovierung (streichen, ausbessern)</td><td>je m² Wohnfläche</td><td>{{PREIS_RENOVIERUNG}}</td></tr>
          <tr><td>Endreinigung / Bauschlussreinigung</td><td>je m² Wohnfläche</td><td>{{PREIS_ENDREINIGUNG}}</td></tr>
          <tr><td>Unterhaltsreinigung Treppenhaus</td><td>je Einsatz</td><td>{{PREIS_TREPPENHAUS}}</td></tr>
          <tr><td>Hausmeisterservice</td><td>je Stunde</td><td>{{PREIS_HAUSMEISTER}}</td></tr>
          <tr><td>Kleinauftrag / Einzelstunde</td><td>je Stunde und Person</td><td>{{PREIS_STUNDE}}</td></tr>
        </tbody>
      </table>
    </div>
    <p class="hint">Hinweis für die Redaktion: Diese Spannen müssen aus eigenen abgeschlossenen Aufträgen stammen. Werte in <code>data/firmendaten.env</code> eintragen – niemals schätzen oder vom Wettbewerb übernehmen.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Beispiele</span><h2>Drei typische Aufträge</h2>
    <p class="hint">Hinweis für die Redaktion: Durch drei echte, abgerechnete Aufträge ersetzen – das ist der glaubwürdigste Teil dieser Seite.</p></div>
    <div class="grid g3">
      <div class="card beispiel"><span class="eyebrow">Beispiel 1</span><h3>{{BEISPIEL_1_TITEL}}</h3><p>{{BEISPIEL_1_TEXT}}</p><p class="beispiel-preis">{{BEISPIEL_1_PREIS}}</p></div>
      <div class="card beispiel"><span class="eyebrow">Beispiel 2</span><h3>{{BEISPIEL_2_TITEL}}</h3><p>{{BEISPIEL_2_TEXT}}</p><p class="beispiel-preis">{{BEISPIEL_2_PREIS}}</p></div>
      <div class="card beispiel"><span class="eyebrow">Beispiel 3</span><h3>{{BEISPIEL_3_TITEL}}</h3><p>{{BEISPIEL_3_TEXT}}</p><p class="beispiel-preis">{{BEISPIEL_3_PREIS}}</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid g2" style="gap:44px;align-items:start">
      <div>
        <span class="eyebrow">Transparenz</span>
        <h2>Was den Preis nach oben treibt</h2>
        <ul class="faktoren">
          <li><b>Stockwerk ohne Aufzug</b> – jede Etage kostet Tragezeit</li>
          <li><b>Entfernung zur Halteposition</b> – 40 Meter Weg zum Fahrzeug summieren sich</li>
          <li><b>Menge und Art des Sperrmülls</b> – Sondermüll und Elektro werden getrennt berechnet</li>
          <li><b>Zustand der Wände</b> – Raufaser überstreichen ist etwas anderes als Tapeten entfernen</li>
          <li><b>Kurzfristigkeit</b> – wenn wir umplanen müssen, kostet das</li>
        </ul>
      </div>
      <div>
        <span class="eyebrow">Und was ihn senkt</span>
        <h2>Was Sie sparen können</h2>
        <ul class="faktoren">
          <li><b>Verwertbares</b> – gut erhaltene Möbel und Geräte rechnen wir an</li>
          <li><b>Mehrere Gewerke zusammen</b> – ein Anfahrtsweg statt drei</li>
          <li><b>Vorlauf</b> – wer drei Wochen vorher anfragt, zahlt weniger als bei „übermorgen“</li>
          <li><b>Eigenleistung</b> – wenn Sie selbst vorsortieren, rechnen wir weniger Zeit</li>
          <li><b>§ 35a EStG</b> – der Lohnanteil ist auf unserer Rechnung getrennt ausgewiesen; 20 % davon, bis zu 1.200 € im Jahr, können Sie direkt von der Steuer abziehen</li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + abschluss("Wie viel es bei Ihnen wird, sagen wir nach der Besichtigung"))

# ================= Leistungen =================
def leistung(anchor, titel, intro, punkte, fuer, alt=False):
    lis = "".join("<li>%s</li>" % p for p in punkte)
    return f"""<section id="{anchor}"{' class="alt"' if alt else ''}>
  <div class="wrap">
    <div class="grid g2" style="align-items:start;gap:40px">
      <div>
        <h2>{titel}</h2>
        <p>{intro}</p>
        <p class="hint"><strong>Typisch für:</strong> {fuer}</p>
        <p><a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a></p>
      </div>
      <div class="card">
        <h3>Das übernehmen wir</h3>
        <ul>{lis}</ul>
      </div>
    </div>
  </div>
</section>"""

page("leistungen.html",
 "Gebäudereinigung, Hausmeisterservice, Entrümpelung &amp; Renovierung in {{ORT}} | Gashini Dienstleistungen",
 "Alle Leistungen von Gashini Dienstleistungen in {{ORT}}: Gebäudereinigung, Hausmeisterservice, Umzug und Entrümpelung, Renovierung und Malerarbeiten.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Leistungen</span>
    <h1>Einzeln, regelmäßig<br><span>oder als Komplettauftrag</span></h1>
    <p class="lead">Die vier Bereiche greifen ineinander – wir übernehmen sie einzeln, im festen Turnus oder gebündelt für eine Übergabe. Zu den beiden häufigsten Anlässen gibt es eigene Seiten: <a href="wohnungsuebergabe.html">Wohnungsübergabe</a> und <a href="haushaltsaufloesung.html">Haushaltsauflösung</a>.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a></div>
  </div>
</section>"""
 + leistung("reinigung","Gebäudereinigung",
   "Regelmäßig oder einmalig: Wir halten Treppenhäuser, Büros, Praxen und Wohnungen in einem Zustand, für den sich niemand entschuldigen muss. Auf Wunsch mit festem Reinigungsplan und Nachweisliste im Objekt.",
   ["Unterhaltsreinigung nach Plan (wöchentlich oder 14-täglich)","Treppenhaus- und Allgemeinflächenreinigung","Bauschlussreinigung und Feinreinigung","Grundreinigung inklusive Bodenpflege","Glas-, Rahmen- und Fensterbankreinigung","Büro-, Praxis- und Ladenreinigung","Küchen- und Sanitärreinigung","Endreinigung nach Auszug"],
   "Hausverwaltungen, Eigentümergemeinschaften, Büros, Bauträger")
 + leistung("hausmeister","Hausmeisterservice",
   "Ein Objekt braucht jemanden, der regelmäßig hinschaut. Wir übernehmen Kontrollgänge, kleine Reparaturen und die Außenanlagen – und melden uns, wenn etwas Größeres ansteht, bevor es teuer wird.",
   ["Regelmäßige Objektkontrolle mit Protokoll","Kleinreparaturen an Türen, Schlössern, Sanitär","Leuchtmittel- und Filterwechsel","Grünpflege, Rasen- und Heckenschnitt","Laubentfernung und Außenreinigung","Winterdienst inklusive Räum- und Streupflicht","Mülltonnenmanagement und Containerstellung","Handwerkerkoordination vor Ort"],
   "Vermieter, Hausverwaltungen, Gewerbeobjekte", alt=True)
 + leistung("umzug","Umzug, Entrümpelung &amp; Entsorgung",
   "Vom Ein-Zimmer-Umzug bis zur vollständigen Räumung. Wir packen, tragen, transportieren und entsorgen fachgerecht – mit Entsorgungsnachweis, wenn Sie ihn brauchen. Bei kompletten Auflösungen finden Sie die Einzelheiten auf der Seite <a href=\"haushaltsaufloesung.html\">Haushaltsauflösung</a>.",
   ["Privat- und Büroumzüge","Beladen, Transport, Entladen","Möbeldemontage und -montage","Verpackungsmaterial und Umzugskartons","Haushaltsauflösungen","Entrümpelung von Keller, Dachboden, Garage","Fachgerechte Entsorgung inklusive Nachweis","Besenreine Übergabe"],
   "Privatkunden, Erbengemeinschaften, Betreuer, Vermieter")
 + leistung("renovierung","Renovierung &amp; Malerarbeiten",
   "Die Arbeiten, die zwischen Auszug und Neuvermietung anfallen – und die kleinen Modernisierungen dazwischen. Sauber abgeklebt, sauber hinterlassen. Für den kompletten Ablauf vor einer Übergabe siehe <a href=\"wohnungsuebergabe.html\">Wohnungsübergabe</a>.",
   ["Maler- und Tapezierarbeiten","Wände spachteln und ausbessern","Laminat, Vinyl und Teppich verlegen","Trockenbau und Deckenarbeiten","Silikonfugen erneuern","Kleinsanierung Bad und Küche","Übergaberenovierung nach Mietvertrag","Streichen von Fenstern, Türen und Zargen"],
   "Vermieter, Mieter bei Auszug, Eigentümer", alt=True)
 + abschluss())

# ================= Ablauf & FAQ =================
FAQ = [
 ("Was kostet die Besichtigung?","Nichts. Anfahrt, Aufmaß und Kostenvoranschlag sind kostenlos und unverbindlich – auch wenn Sie sich danach gegen uns entscheiden."),
 ("Ist der Preis wirklich fest?","Ja. Was im schriftlichen Angebot steht, steht auf der Rechnung. Zusätzliche Arbeiten führen wir nur aus, wenn Sie sie vorher freigeben."),
 ("Sind Sie versichert?","Ja, wir haben eine Betriebshaftpflichtversicherung. Wenn doch einmal etwas beschädigt wird, ist das geregelt."),
 ("Wie schnell können Sie anfangen?","Kleinere Aufträge oft innerhalb weniger Tage. Bei festen Übergabeterminen planen wir mit Puffer – sagen Sie uns die Frist, dann sagen wir Ihnen ehrlich, ob wir sie halten."),
 ("Arbeiten Sie mit Subunternehmern?","Die Kernleistungen führen unsere eigenen Leute aus. Nur für Gewerke, die wir nicht selbst abdecken, holen wir Fachbetriebe dazu – und sagen Ihnen das vorher."),
 ("Bekomme ich eine Rechnung, die ich absetzen kann?","Ja, mit ausgewiesener Umsatzsteuer und getrennt ausgewiesenem Lohnanteil. 20 % des Lohnanteils, höchstens 1.200 € im Jahr, können Privatkunden als haushaltsnahe Dienstleistung nach § 35a EStG direkt von der Steuerschuld abziehen."),
 ("Was passiert mit dem Müll?","Wir entsorgen getrennt nach Fraktionen über zugelassene Annahmestellen. Den Entsorgungsnachweis bekommen Sie auf Wunsch mit der Rechnung."),
 ("Kann ich auch über MyHammer buchen?","Gerne. Stellen Sie Ihre Anfrage über unser MyHammer-Profil oder direkt bei uns – der Preis ist in beiden Fällen derselbe."),
]
import json
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":f,"acceptedAnswer":{"@type":"Answer","text":a}} for f,a in FAQ]}
faq_cards = "\n".join(
  '      <div class="card"><h3>%s</h3><p>%s</p></div>' % (f,a) for f,a in FAQ)

page("ablauf.html","So läuft ein Auftrag ab – Ablauf und häufige Fragen | Gashini Dienstleistungen",
 "Von der Anfrage über die kostenlose Besichtigung bis zur Abnahme: So arbeitet Gashini Dienstleistungen – mit Antworten auf die häufigsten Fragen.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Ablauf</span>
    <h1>In vier Schritten<br><span>zum fertigen Objekt</span></h1>
    <p class="lead">Sie wissen vor dem ersten Handgriff, was gemacht wird, wer kommt und was es kostet.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="kontakt.html">Festpreis anfragen</a></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid g4">
      <div class="step"><b>01</b><h3>Anfrage</h3><p>Telefonisch, per Formular, per WhatsApp oder über MyHammer. Objekt, Umfang und Wunschtermin genügen für den Einstieg.</p></div>
      <div class="step"><b>02</b><h3>Besichtigung</h3><p>Innerhalb von rund drei Werktagen, kostenlos und unverbindlich. Bei kleinen Aufträgen reichen Fotos und Quadratmeter.</p></div>
      <div class="step"><b>03</b><h3>Festpreis-Angebot</h3><p>Schriftlich, nach Positionen aufgeschlüsselt, 14 Tage gültig. Der Termin bleibt für Sie reserviert.</p></div>
      <div class="step"><b>04</b><h3>Ausführung &amp; Abnahme</h3><p>Zum vereinbarten Termin, mit eigenem Material und Fahrzeug. Am Ende gehen wir gemeinsam durch – erst dann ist der Auftrag fertig.</p></div>
    </div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Häufige Fragen</span><h2>Das werden wir am häufigsten gefragt</h2></div>
    <div class="grid g2">
""" + faq_cards + """
    </div>
  </div>
</section>
""" + abschluss(),
 extra_head="\n<script type=\"application/ld+json\">\n" + json.dumps(faq_ld, ensure_ascii=False, indent=2) + "\n</script>")

# ================= Kontakt =================
page("kontakt.html","Festpreis anfragen – kostenlos und unverbindlich | Gashini Dienstleistungen",
 "Anfrage an Gashini Dienstleistungen in {{ORT}}: kostenlose Besichtigung, Festpreis in der Regel binnen 24 Stunden. Telefon, WhatsApp oder Formular.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Kontakt</span>
    <h1>Festpreis anfragen –<br><span>kostenlos und unverbindlich</span></h1>
    <p class="lead">Beschreiben Sie kurz, was ansteht und bis wann es fertig sein muss. Sie bekommen am selben Werktag eine Rückmeldung – entweder direkt eine Einschätzung oder einen Vorschlag für die Besichtigung.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid g2" style="gap:44px;align-items:start">
      <div>
        <h2>Anfrageformular</h2>
        <p class="hint">Vier Pflichtfelder – mehr brauchen wir für den Anfang nicht.</p>
        <form class="kontakt" action="{{FORMULAR_ENDPOINT}}" method="post">
          <div><label for="name">Name *</label><input id="name" name="name" required autocomplete="name"></div>
          <div><label for="telefon">Telefon *</label><input id="telefon" name="telefon" type="tel" required autocomplete="tel"></div>
          <div><label for="ort">PLZ / Ort des Objekts *</label><input id="ort" name="ort" required autocomplete="postal-code"></div>
          <div><label for="email">E-Mail</label><input id="email" name="email" type="email" autocomplete="email"><span class="hint">Freiwillig – für das schriftliche Angebot</span></div>
          <div class="full"><label for="anlass">Worum geht es?</label>
            <select id="anlass" name="anlass">
              <option>Wohnungsübergabe (räumen, streichen, reinigen)</option>
              <option>Haushaltsauflösung / Entrümpelung</option>
              <option>Gebäudereinigung</option>
              <option>Hausmeisterservice</option>
              <option>Renovierung / Malerarbeiten</option>
              <option>Umzug</option>
              <option>Noch unklar</option>
            </select></div>
          <div class="full"><label for="termin">Bis wann muss es fertig sein?</label>
            <input id="termin" name="termin" type="text" placeholder="z. B. Übergabe am 30.10. oder „noch offen“"></div>
          <div class="full"><label for="nachricht">Was steht an? *</label>
            <textarea id="nachricht" name="nachricht" rows="5" required placeholder="z. B. 3-Zimmer-Wohnung, 78 m², 2. OG ohne Aufzug. Entrümpeln, streichen und Endreinigung."></textarea></div>
          <div class="full"><label for="quelle">Wie sind Sie auf uns aufmerksam geworden?</label>
            <select id="quelle" name="quelle">
              <option value="">Bitte auswählen</option>
              <option>Google-Suche</option>
              <option>Google-Unternehmensprofil / Karte</option>
              <option>MyHammer</option>
              <option>Empfehlung</option>
              <option>Fahrzeug oder Flyer gesehen</option>
              <option>Social Media</option>
              <option>Sonstiges</option>
            </select></div>
          <p class="hp" aria-hidden="true"><label for="website">Dieses Feld bitte frei lassen</label><input id="website" name="website" tabindex="-1" autocomplete="off"></p>
          <div class="full check">
            <input id="dsgvo" name="dsgvo" type="checkbox" required>
            <label for="dsgvo" style="font-weight:400">Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Angaben zur Bearbeitung der Anfrage einverstanden. *</label>
          </div>
          <div class="full">
            <p class="vor-absenden">Kostenlos und unverbindlich. Rückmeldung am selben Werktag. Keine Weitergabe Ihrer Daten.</p>
            <button class="btn btn-primary" type="submit">Anfrage abschicken</button>
          </div>
        </form>
      </div>
      <div>
        <div class="card karte-hervor">
          <h3>Schneller geht es telefonisch</h3>
          <p>Bei Fristsachen ist der Anruf der kürzere Weg – dann klären wir in drei Minuten, ob wir Ihren Termin halten können.</p>
          <p><a class="btn btn-primary" href="tel:{{TELEFON_LINK}}">{{TELEFON}}</a></p>
          <dl class="facts">
            <dt>WhatsApp</dt><dd><a href="https://wa.me/{{WHATSAPP}}" rel="noopener">Fotos direkt schicken</a></dd>
            <dt>E-Mail</dt><dd><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></dd>
            <dt>Anschrift</dt><dd>{{STRASSE}}<br>{{PLZ_ORT}}</dd>
            <dt>Zeiten</dt><dd>Mo–Sa 7:00–20:00 Uhr</dd>
          </dl>
        </div>
        <div class="card" style="margin-top:22px">
          <h3>Angebot ohne Besichtigung</h3>
          <p>Schicken Sie uns per WhatsApp zwei bis drei Fotos je Raum und die ungefähre Quadratmeterzahl. Bei vielen Aufträgen können wir damit direkt kalkulieren – das spart beiden Seiten einen Termin.</p>
        </div>
        <div class="card" style="margin-top:22px">
          <h3>Lieber über ein Portal?</h3>
          <p>Sie können Ihren Auftrag auch über unser <a href="{{MYHAMMER_URL}}" rel="noopener">MyHammer-Profil</a> ausschreiben. Dort sehen Sie zusätzlich unsere Bewertungen aus vermittelten Aufträgen. Der Preis ist derselbe.</p>
        </div>
      </div>
    </div>
  </div>
</section>""")

page("danke.html","Anfrage eingegangen | Gashini Dienstleistungen",
 "Vielen Dank für Ihre Anfrage an Gashini Dienstleistungen.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Eingegangen</span>
    <h1>Danke –<br><span>wir melden uns</span></h1>
    <p class="lead">Ihre Anfrage ist bei uns angekommen. Sie hören am selben Werktag von uns: entweder mit einer ersten Einschätzung oder mit einem Vorschlag für den Besichtigungstermin.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:{{TELEFON_LINK}}">Wenn es eilt: {{TELEFON}}</a>
      <a class="btn btn-ghost" href="index.html">Zur Startseite</a>
    </div>
    <p class="hero-fuss">Tipp: Schicken Sie uns per WhatsApp zwei bis drei Fotos des Objekts – damit können wir oft ohne Besichtigung kalkulieren.</p>
  </div>
</section>""")

page("404.html","Seite nicht gefunden | Gashini Dienstleistungen",
 "Diese Seite existiert nicht. Zurück zur Startseite von Gashini Dienstleistungen.",
 """<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Fehler 404</span>
    <h1>Diese Seite<br><span>gibt es nicht</span></h1>
    <p class="lead">Vielleicht hat sich ein Tippfehler eingeschlichen, oder wir haben die Seite umbenannt. Hier kommen Sie weiter:</p>
    <ul class="fehler-links">
      <li><a href="wohnungsuebergabe.html">Wohnungsübergabe</a></li>
      <li><a href="haushaltsaufloesung.html">Haushaltsauflösung</a></li>
      <li><a href="leistungen.html">Alle Leistungen</a></li>
      <li><a href="preise.html">Preise</a></li>
      <li><a href="kontakt.html">Kontakt</a></li>
    </ul>
    <div class="hero-actions"><a class="btn btn-primary" href="tel:{{TELEFON_LINK}}">Anrufen: {{TELEFON}}</a></div>
  </div>
</section>""")

# ================= Übernommene Seiten (neues Gerüst, bestehender Inhalt) =================
import re
def altes_main(fn):
    s = io.open(os.path.join(OUT, fn), encoding="utf-8").read()
    m = s.split('<main id="inhalt">',1)[1].rsplit('</main>',1)[0]
    m = re.sub(r'<section class="alt">\s*<div class="wrap">\s*<div class="mh">.*?</section>', '', m, flags=re.S)
    return m.strip()

ueber = altes_main("ueber-uns.html")
ueber = ueber.replace("Ein Betrieb.<br><span>Ein Wort.</span>", "Wer bei Ihnen<br><span>vor der Tür steht</span>")
ueber = ueber.replace("Handwerk statt Hochglanz", "Vom Reinigungsauftrag zum Komplettpaket")
ueber = ueber.replace('<span class="eyebrow">Über uns</span>\n    <h1>', '<span class="eyebrow">Über uns</span>\n    <h1>')
if "Was wir nicht sind" not in ueber:
  ueber += """
<section class="alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Ehrlich</span><h2>Was wir nicht sind</h2></div>
    <div class="grid g3">
      <div class="card"><h3>Nicht der billigste Anbieter</h3><p>Wir kalkulieren mit Puffer, eigenem Material und ordentlicher Entsorgung. Wer ausschließlich über den Preis entscheidet, findet günstigere Angebote.</p></div>
      <div class="card"><h3>Kein Vermittler</h3><p>Es gibt keine Zentrale und keine Weitergabe an Dritte. Wer den Auftrag annimmt, führt ihn auch aus.</p></div>
      <div class="card"><h3>Kein Sanierungsbetrieb</h3><p>Elektrik, Heizung und Statik sind nicht unser Fach. Wenn Ihr Vorhaben dorthin geht, sagen wir es beim ersten Gespräch.</p></div>
    </div>
  </div>
</section>
""" + abschluss()
page("ueber-uns.html","Über uns – Inhaber {{INHABER}} | Gashini Dienstleistungen",
     "Gashini Dienstleistungen ist ein inhabergeführter Betrieb in {{ORT}}: Entrümpelung, Renovierung, Reinigung und Hausmeisterservice aus einer Hand.",
     ueber)

ref = altes_main("referenzen.html")
if "Ihre Bewertung entsteht" not in ref:
    ref += abschluss("Ihre Bewertung entsteht nach dem Auftrag – nicht davor")
page("referenzen.html","Referenzen und Bewertungen | Gashini Dienstleistungen",
     "Kundenbewertungen von Gashini Dienstleistungen aus abgeschlossenen Aufträgen – unter anderem über das geprüfte MyHammer-Profil.",
     ref)

page("impressum.html","Impressum | Gashini Dienstleistungen",
     "Impressum und Anbieterkennzeichnung von Gashini Dienstleistungen.",
     altes_main("impressum.html"))

page("datenschutz.html","Datenschutzerklärung | Gashini Dienstleistungen",
     "Datenschutzerklärung von Gashini Dienstleistungen nach DSGVO.",
     altes_main("datenschutz.html"))

# ================= robots + sitemap =================
seiten = [("", "1.0"), ("wohnungsuebergabe.html","0.9"), ("haushaltsaufloesung.html","0.9"),
          ("leistungen.html","0.8"), ("preise.html","0.8"), ("kontakt.html","0.9"),
          ("ablauf.html","0.6"), ("referenzen.html","0.6"), ("ueber-uns.html","0.5"),
          ("impressum.html","0.2"), ("datenschutz.html","0.2")]
x = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p_, prio in seiten:
    x.append('  <url><loc>https://{{DOMAIN}}/%s</loc><lastmod>{{STAND_ISO}}</lastmod><priority>%s</priority></url>' % (p_, prio))
x.append('</urlset>')
io.open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8").write("\n".join(x)+"\n")
io.open(os.path.join(OUT,"robots.txt"),"w",encoding="utf-8").write(
    "User-agent: *\nAllow: /\n\nSitemap: https://{{DOMAIN}}/sitemap.xml\n")
print("sitemap + robots geschrieben")
