/* Standbilder der Wandaufbau-Szene – nur für renderings.mjs (headless Chromium). */
import { erstelleSzene, setzeFortschritt, erstelleRenderer, erstelleKamera, projiziere, ANKER } from './szene.js';

async function webp(quelle, breite, qualitaet) {
  const hoehe = Math.round(quelle.height * breite / quelle.width);
  const c = document.createElement('canvas');
  c.width = breite; c.height = hoehe;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  // schrittweise verkleinern – schärfer als ein einzelner großer Schritt
  let zwischen = quelle;
  while (zwischen.width / 2 > breite) {
    const z = document.createElement('canvas');
    z.width = Math.round(zwischen.width / 2); z.height = Math.round(zwischen.height / 2);
    const zc = z.getContext('2d'); zc.imageSmoothingQuality = 'high'; zc.drawImage(zwischen, 0, 0, z.width, z.height);
    zwischen = z;
  }
  ctx.drawImage(zwischen, 0, 0, breite, hoehe);
  return { breite, hoehe, daten: c.toDataURL('image/webp', qualitaet) };
}

window.rendere = async function (auftrag) {
  const { ansicht, fortschritt = 4, schnitt = 0, breite, hoehe, faktor = 2, varianten = [640, 1280, 1920], qualitaet = .86 } = auftrag;
  const canvas = document.createElement('canvas');
  canvas.width = breite * faktor; canvas.height = hoehe * faktor;
  const renderer = erstelleRenderer(canvas, { pixelRatio: 1, maxPixelRatio: 1, standbild: true, antialias: true, belichtung: auftrag.belichtung });
  renderer.setSize(breite * faktor, hoehe * faktor, false);
  const s = erstelleSzene({ qualitaet: 'hoch', kanten: auftrag.kanten });
  setzeFortschritt(s, fortschritt, schnitt);
  const anker = ANKER;
  const kamera = erstelleKamera(ansicht, breite / hoehe);
  renderer.render(s.szene, kamera);
  const ergebnis = { anker: projiziere(kamera, anker), bilder: [] };
  for (const v of varianten) if (v <= breite) ergebnis.bilder.push(await webp(canvas, v, qualitaet));
  renderer.dispose();
  return ergebnis;
};
window.bereit = true;
