# Gashini Dienstleistungen – Website und Firmenauftritt

Statische Website mit einem kleinen PHP-Formular-Backend, dazu Logo, Druckvorlagen und Strategiepapiere.
Keine Frameworks, keine Laufzeit-Abhängigkeiten.

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
src/assets/        Stylesheet (Design-Tokens), Skripte, Schriften, Bilder
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
| [`docs/RELAUNCH-PLAN.md`](docs/RELAUNCH-PLAN.md) | Bestandsaufnahme, Risiken, Architekturentscheidung, Prioritäten, Rückfragen |
| [`docs/CONTENT-PLAN.md`](docs/CONTENT-PLAN.md) | Headlines, Positionierung, Texte, CTAs, offene Freigaben |
| [`docs/SEO-PLAN.md`](docs/SEO-PLAN.md) | Suchintentionen, Seitenzuordnung, Titel und Beschreibungen |
| [`docs/LEGAL-CHECKLIST.md`](docs/LEGAL-CHECKLIST.md) | Datenschutz, Impressum, Gewerberecht, Bildrechte, Barrierefreiheit |
| [`docs/ASSET-BRIEFS.md`](docs/ASSET-BRIEFS.md) | Bildgruppen, Motivlisten, Formate, Rechte |
| [`docs/TESTREPORT.md`](docs/TESTREPORT.md) | was geprüft wurde – und was nicht |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Hosting, Formular einrichten, Weiterleitungen, nginx |
| [`docs/PFLEGE.md`](docs/PFLEGE.md) | Texte ändern, Projekte veröffentlichen, Fragen ergänzen |
| [`brand/styleguide.md`](brand/styleguide.md) | Farben, Schriften, Logo, Bewegung |

## Tests

```
python3 tests/pruefen.py                          # Build, Drift, Links, SEO-Grundlagen, CSP, Geheimnisse
python3 tests/formular_test.py                    # Formular-Backend gegen php -S
cd tests && npm ci && node e2e.mjs                # Browser: 5 Breiten, axe-core, Tastatur, Formular, ohne JS
```
Alle drei laufen auch in GitHub Actions (`.github/workflows/vorschau.yml`).

## Private Daten

Nie ins Repository: `data/firmendaten.privat.env` (Bank, Steuernummer) und die Formular-Konfiguration mit
SMTP-Passwort. Beide stehen in `.gitignore`; die Testsuite schlägt fehl, falls sie doch eingecheckt werden.
Das Repository ist öffentlich – alles andere hier ist für jeden lesbar.
