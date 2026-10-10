# Gashini Dienstleistungen – Website und Firmenauftritt

Statische Website mit einem kleinen PHP-Formular-Backend, dazu Logo, Druckvorlagen und Strategiepapiere.
Keine Frameworks. Bewegung mit GSAP, ein interaktives Wandmodell mit three.js – beide lokal ausgeliefert.
Leitidee und Gestaltungsregeln: [`docs/CREATIVE-DIRECTION.md`](docs/CREATIVE-DIRECTION.md).

## Schnellstart

```
python3 scripts/build-site.py          # src/ + data/ → web/
python3 scripts/firmendaten.py         # web/ + Firmendaten → dist/web/ (Vorschau)
php -S 127.0.0.1:8000 -t dist/web      # lokal ansehen
```

Veröffentlichen: `python3 scripts/firmendaten.py --produktion` – bricht ab, solange Angaben offen sind.
Details: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Aufbau

```
src/seiten/        Seiteninhalte – hier werden Texte geändert
src/assets/        Stylesheet (Design-Tokens), Skripte (site.js, bewegung.js, vendor/), Schriften, Bilder
scripts/           Generator, Firmendaten, Zeichnungen (zeichnungen.py), Vorschau-Kennzeichnung
scripts/werkzeuge/3d/  Entwicklungswerkzeug: Wandmodell (three.js), Visualisierungen, GSAP-Kopie
src/api/           Formular-Backend (PHP) und Konfigurationsvorlage
src/server/        .htaccess (Sicherheits-Header, CSP, Weiterleitungen)
data/              firmendaten.env (öffentlich) · projekte.json · faq.json
brand/             Logo, Signet, Favicon, Gestaltungsrichtlinien
web/               GENERIERT – nicht von Hand ändern (CI prüft das)
print/             Visitenkarte, Briefbogen, Flyer, E-Mail-Signatur, Fahrzeug
tests/             statische Prüfungen, Formular-Tests, Browser-Tests
docs/              Relaunch-Plan, Inhalte, SEO, Recht, Bilder, Tests, Deployment, Pflege
strategie/         Strategiepapiere aus der ersten Projektphase
```

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [`docs/CREATIVE-AUDIT.md`](docs/CREATIVE-AUDIT.md) | Die zehn wichtigsten Schwächen vor dem Premium-Relaunch und ihre Behebung |
| [`docs/CREATIVE-DIRECTION.md`](docs/CREATIVE-DIRECTION.md) | Leitidee, Farbe, Typografie, Bildsprache, Motion-System, Komponenten, Technologieentscheidungen |
| [`docs/RELAUNCH-PLAN.md`](docs/RELAUNCH-PLAN.md) | Bestandsaufnahme, Risiken, Architekturentscheidung, Prioritäten, Rückfragen |
| [`docs/CONTENT-PLAN.md`](docs/CONTENT-PLAN.md) | Headlines, Positionierung, Texte, CTAs, offene Freigaben |
| [`docs/SEO-PLAN.md`](docs/SEO-PLAN.md) | Suchintentionen, Seitenzuordnung, Titel und Beschreibungen |
| [`docs/LEGAL-CHECKLIST.md`](docs/LEGAL-CHECKLIST.md) | Datenschutz, Impressum, Gewerberecht, Bildrechte, Barrierefreiheit |
| [`docs/ASSET-BRIEFS.md`](docs/ASSET-BRIEFS.md) | Bildsystem, Motivlisten, Midjourney-Prompts, Content-Briefing, Rechte |
| [`docs/TESTREPORT.md`](docs/TESTREPORT.md) | was geprüft wurde – und was nicht |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Hosting, Formular einrichten, Weiterleitungen, nginx |
| [`docs/PFLEGE.md`](docs/PFLEGE.md) | Texte ändern, Projekte veröffentlichen, Fragen ergänzen |
| [`brand/styleguide.md`](brand/styleguide.md) | Farben, Schriften, Logo, Bewegung |

## Tests

```
python3 tests/pruefen.py                          # Build, Drift, Links, SEO-Grundlagen, CSP, Geheimnisse
python3 tests/formular_test.py                    # Formular-Backend gegen php -S
cd tests && npm ci && node e2e.mjs                # Browser: 5 Breiten, axe-core, Tastatur, Formular, Fotos,
                                                  # Rückruf, ohne JS, reduzierte Bewegung, 3D mit/ohne WebGL, Flip
```
Alle drei laufen auch in GitHub Actions (`.github/workflows/vorschau.yml`).

## Private Daten

Nie ins Repository: `data/firmendaten.privat.env` (Bank, Steuernummer) und die Formular-Konfiguration mit
SMTP-Passwort. Beide stehen in `.gitignore`; die Testsuite schlägt fehl, falls sie doch eingecheckt werden.
Das Repository ist öffentlich – alles andere hier ist für jeden lesbar.
