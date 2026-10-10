// Erzeugt die Material-Visualisierungen aus der 3D-Szene als WebP-Varianten
// nach src/assets/bilder/visualisierung/ und die Beschriftungsanker als JSON.
//   npm run renderings            (Chromium über CHROMIUM_PFAD oder Playwright-Standard)
import { build } from 'esbuild';
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = dirname(fileURLToPath(import.meta.url));
const ZIEL = join(HIER, '../../../src/assets/bilder/visualisierung');
mkdirSync(ZIEL, { recursive: true });

const AUFTRAEGE = [
  { name: 'wand-schnitt', ansicht: 'gesamt', fortschritt: 4, schnitt: 1, breite: 1920, hoehe: 1600 },
  { name: 'wand-staender', ansicht: 'staender', fortschritt: 1, schnitt: 0, breite: 1920, hoehe: 1280 },
  { name: 'wand-daemmung', ansicht: 'daemmung', fortschritt: 2, schnitt: 0, breite: 1920, hoehe: 1280 },
];
const nur = process.argv.slice(2);

const bundle = await build({ entryPoints: [join(HIER, 'quelle/standbild.js')], bundle: true, write: false, format: 'iife', minify: true });
const code = bundle.outputFiles[0].text;
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PFAD || undefined,
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
});
const seite = await browser.newPage();
seite.on('console', m => console.log('  [browser]', m.text()));
await seite.setContent('<!doctype html><html><body></body></html>');
await seite.addScriptTag({ content: code });
const anker = {};
for (const a of AUFTRAEGE) {
  if (nur.length && !nur.includes(a.name)) continue;
  const t0 = Date.now();
  const erg = await seite.evaluate(auftrag => window.rendere(auftrag), a);
  for (const b of erg.bilder) {
    writeFileSync(join(ZIEL, `${a.name}-${b.breite}.webp`), Buffer.from(b.daten.split(',')[1], 'base64'));
  }
  anker[a.name] = erg.anker;
  console.log(`${a.name}: ${erg.bilder.map(b => b.breite + 'x' + b.hoehe).join(', ')} in ${Date.now() - t0} ms`);
}
if (!nur.length) writeFileSync(join(ZIEL, 'anker.json'), JSON.stringify(anker, null, 1) + '\n');
await browser.close();
