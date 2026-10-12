// Website-Icon nur aus dem „G“ des Signets (brand/svg/signet.svg). Aufruf: npm run icon
//
// Die G-Glyphe wird unverändert aus dem Logo-Paket übernommen (gleicher Pfad) – keine Schrift, kein nachgebauter
// Buchstabe. Ohne den Schriftzug und ohne das gelbe Band, auf einer Fläche in Anthrazit (#1E2124), das G in
// Kalkweiß (#F4F2ED). Das G ist größer gesetzt als im Signet, damit es bei 16 und 32 px lesbar bleibt.
//
//   src/assets/icon/icon-g.svg       Browser-Tab (Kachel mit abgerundeten Ecken wie das Signet)
//   src/assets/icon/favicon.ico      16, 32 und 48 px (Kachel)
//   src/assets/icon/icon-g-32.png    32 × 32
//   src/assets/icon/icon-g-180.png   Apple-Touch-Icon (vollflächig – iOS rundet selbst ab)
//   src/assets/icon/icon-g-192.png   Web-Manifest (vollflächig, G innerhalb der sicheren Zone für runde Masken)
//   src/assets/icon/icon-g-512.png   Web-Manifest, Teilen-Vorschau
//
// Die Maße der Glyphe misst der Browser (getBBox), nicht eine Schätzung.
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const WURZEL = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const ZIEL = join(WURZEL, 'src', 'assets', 'icon');
const ANTHRAZIT = '#1E2124', KALK = '#F4F2ED';

const signet = readFileSync(join(WURZEL, 'brand', 'svg', 'signet.svg'), 'utf8');
const m = signet.match(/<g fill="#F4F2ED"><path transform="translate\(([^)]+)\)" d="([^"]+)"/);
if (!m) throw new Error('G-Glyphe im Signet nicht gefunden');
const [verschiebung, pfad] = [m[1], m[2]];

const b = await chromium.launch(process.env.CHROMIUM_PFAD ? { executablePath: process.env.CHROMIUM_PFAD } : {});
const p = await b.newPage();
await p.setContent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path id="g" transform="translate(${verschiebung})" d="${pfad}"/></svg>`);
const box = await p.evaluate(() => {
  const el = document.getElementById('g'), r = el.getBBox(), t = el.transform.baseVal.consolidate().matrix;
  return { x: r.x + t.e, y: r.y + t.f, w: r.width, h: r.height };
});

// Kachel: Seite so gewählt, dass das G einen festen Anteil der Höhe einnimmt, optisch mittig
const kachel = (anteil, ecke) => {
  const seite = box.h / anteil;
  const x = box.x + box.w / 2 - seite / 2, y = box.y + box.h / 2 - seite / 2;
  const f = v => +v.toFixed(3);
  const rx = ecke ? ` rx="${f(seite * 0.1)}"` : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${f(x)} ${f(y)} ${f(seite)} ${f(seite)}">`
    + `<rect x="${f(x)}" y="${f(y)}" width="${f(seite)}" height="${f(seite)}"${rx} fill="${ANTHRAZIT}"/>`
    + `<path transform="translate(${verschiebung})" d="${pfad}" fill="${KALK}"/></svg>`;
};
const tab = kachel(0.66, true);      // Tab und kleine Größen: großes G
const flaeche = kachel(0.5, false);  // Home-Bildschirm und Manifest: mehr Luft, vollflächig

mkdirSync(ZIEL, { recursive: true });
writeFileSync(join(ZIEL, 'icon-g.svg'), tab.replace('<svg ', '<svg ').replace('>', '><title>Gashini Dienstleistungen</title>') + '\n');

const png = async (px, svg) => {
  await p.setViewportSize({ width: px, height: px });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${px}" height="${px}" `)}</body></html>`);
  return p.screenshot({ omitBackground: true, clip: { x: 0, y: 0, width: px, height: px } });
};
writeFileSync(join(ZIEL, 'icon-g-32.png'), await png(32, tab));
for (const g of [180, 192, 512]) writeFileSync(join(ZIEL, `icon-g-${g}.png`), await png(g, flaeche));

// ICO mit PNG-Einträgen (seit Windows Vista und in allen aktuellen Browsern)
const groessen = [16, 32, 48];
const bilder = [];
for (const g of groessen) bilder.push(await png(g, tab));
const kopf = Buffer.alloc(6 + 16 * bilder.length);
kopf.writeUInt16LE(0, 0); kopf.writeUInt16LE(1, 2); kopf.writeUInt16LE(bilder.length, 4);
let versatz = kopf.length;
bilder.forEach((bild, i) => {
  const o = 6 + 16 * i, g = groessen[i];
  kopf.writeUInt8(g % 256, o); kopf.writeUInt8(g % 256, o + 1); kopf.writeUInt8(0, o + 2); kopf.writeUInt8(0, o + 3);
  kopf.writeUInt16LE(1, o + 4); kopf.writeUInt16LE(32, o + 6);
  kopf.writeUInt32LE(bild.length, o + 8); kopf.writeUInt32LE(versatz, o + 12);
  versatz += bild.length;
});
writeFileSync(join(ZIEL, 'favicon.ico'), Buffer.concat([kopf, ...bilder]));
await b.close();
console.log('Icon erzeugt →', ZIEL);
