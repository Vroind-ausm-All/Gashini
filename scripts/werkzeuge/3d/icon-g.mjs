// Website-Icon nur aus dem „G“ des Signets (brand/svg/signet.svg). Aufruf: npm run icon
//
//   src/assets/icon/icon-g.svg      Browser-Tab: G in Anthrazit, bei dunkler Browser-Oberfläche in Kalkweiß
//   src/assets/icon/favicon.ico     16, 32 und 48 px für Browser ohne SVG-Icon: G in Anthrazit auf transparentem Grund
//                                   (ohne Kontur – das Markenblatt verbietet Konturen am Logo)
//   src/assets/icon/icon-g-180.png  Home-Bildschirm (iOS): kalkweißes G auf Anthrazit, vollflächig
//   src/assets/icon/icon-g-512.png  dasselbe groß (Teilen-Vorschau, Verzeichnisse)
//
// Die Glyphe wird unverändert aus dem Logo-Paket übernommen (gleicher Pfad, gleiche Hausfarben); nur der Ausschnitt
// wird so gewählt, dass das G die Fläche füllt. Die Maße misst der Browser (getBBox), nicht eine Schätzung.
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
// quadratischer Ausschnitt, G mittig, 7 % Rand
const seite = Math.max(box.w, box.h) * 1.14;
const vb = [box.x + box.w / 2 - seite / 2, box.y + box.h / 2 - seite / 2, seite, seite].map(v => +v.toFixed(3)).join(' ');
const glyphe = (attr = '') => `<path transform="translate(${verschiebung})" d="${pfad}"${attr}/>`;

mkdirSync(ZIEL, { recursive: true });
const svgTab = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}"><title>Gashini Dienstleistungen</title>`
  + `<style>path{fill:${ANTHRAZIT}}@media (prefers-color-scheme:dark){path{fill:${KALK}}}</style>${glyphe(` fill="${ANTHRAZIT}"`)}</svg>\n`;
writeFileSync(join(ZIEL, 'icon-g.svg'), svgTab);

const png = async (px, svg) => {
  await p.setViewportSize({ width: px, height: px });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${px}" height="${px}" `)}</body></html>`);
  return p.screenshot({ omitBackground: true, clip: { x: 0, y: 0, width: px, height: px } });
};
// klein: G in Anthrazit, transparenter Grund
const klein = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}">${glyphe(` fill="${ANTHRAZIT}"`)}</svg>`;
// Home-Bildschirm: Fläche Anthrazit, G Kalkweiß, etwas mehr Luft
const [vx, vy] = vb.split(' ').map(Number);
const rand = seite * 0.2;
const kachel = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${(vx - rand).toFixed(3)} ${(vy - rand).toFixed(3)} ${(seite + 2 * rand).toFixed(3)} ${(seite + 2 * rand).toFixed(3)}">`
  + `<rect x="${vx - rand}" y="${vy - rand}" width="${seite + 2 * rand}" height="${seite + 2 * rand}" fill="${ANTHRAZIT}"/>${glyphe(` fill="${KALK}"`)}</svg>`;
writeFileSync(join(ZIEL, 'icon-g-180.png'), await png(180, kachel));
writeFileSync(join(ZIEL, 'icon-g-512.png'), await png(512, kachel));

// ICO mit PNG-Einträgen (seit Windows Vista und in allen aktuellen Browsern)
const groessen = [16, 32, 48];
const bilder = [];
for (const g of groessen) bilder.push(await png(g, klein));
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
console.log('Icon erzeugt: viewBox', vb, '→', ZIEL);
