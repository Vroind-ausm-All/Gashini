/* Gashini – interaktives Wandaufbau-Modell auf der Website.
 * Wird erst nachgeladen, wenn der Abschnitt in die Nähe des Sichtbereichs kommt
 * (siehe src/assets/js/bewegung.js). Rendert nur bei Bedarf, pausiert außerhalb
 * des Sichtbereichs und gibt bei Kontextverlust an die Zeichnung zurück.
 */
import { Vector3, Spherical, MathUtils } from 'three';
import { erstelleSzene, setzeFortschritt, erstelleRenderer, erstelleKamera } from './szene.js';

export function starte(buehne, optionen = {}) {
  const schmal = buehne.clientWidth < 640;
  const sparsam = schmal || optionen.sparsam;
  const reduziert = !!optionen.reduziert;

  const canvas = document.createElement('canvas');
  canvas.className = 'wandaufbau-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  buehne.prepend(canvas);

  const renderer = erstelleRenderer(canvas, { maxPixelRatio: sparsam ? 1.5 : 2, schatten: !sparsam, antialias: true });
  const s = erstelleSzene({ qualitaet: sparsam ? 'mittel' : 'hoch', schatten: !sparsam, schattenKarte: 2048 });
  let kamera = erstelleKamera(schmal ? 'mobil' : 'gesamt', 1);
  const ziel = kamera.userData.ziel.clone();
  const basis = new Spherical().setFromVector3(kamera.position.clone().sub(ziel));
  const dreh = { theta: 0, phi: 0, zielTheta: 0, zielPhi: 0 };

  let p = optionen.start ?? 0, pZiel = p, c = 0, cZiel = 0;
  let sichtbar = true, laeuft = false, entsorgt = false;

  function groesse() {
    const b = buehne.clientWidth, h = buehne.clientHeight;
    if (!b || !h) return;
    renderer.setSize(b, h, false);
    kamera.aspect = b / h;
    kamera.updateProjectionMatrix();
    zeichnen();
  }

  function zeichnen() {
    if (entsorgt) return;
    setzeFortschritt(s, p, c);
    const sph = new Spherical(basis.radius, basis.phi + dreh.phi, basis.theta + dreh.theta);
    kamera.position.copy(new Vector3().setFromSpherical(sph).add(ziel));
    kamera.lookAt(ziel);
    renderer.render(s.szene, kamera);
  }

  // Animationsschleife nur, solange sich etwas ändert
  let letzte = 0;
  function bild(t) {
    const dt = Math.min((t - (letzte || t)) / 1000, .05); letzte = t;
    const k = 1 - Math.pow(.0018, dt);                  // gedämpftes Annähern, unabhängig von der Bildrate
    p += (pZiel - p) * k; c += (cZiel - c) * k;
    dreh.theta += (dreh.zielTheta - dreh.theta) * k; dreh.phi += (dreh.zielPhi - dreh.phi) * k;
    const fertig = Math.abs(pZiel - p) < .001 && Math.abs(cZiel - c) < .001 &&
                   Math.abs(dreh.zielTheta - dreh.theta) < .0005 && Math.abs(dreh.zielPhi - dreh.phi) < .0005;
    if (fertig) { p = pZiel; c = cZiel; dreh.theta = dreh.zielTheta; dreh.phi = dreh.zielPhi; }
    zeichnen();
    if (!fertig && sichtbar) requestAnimationFrame(bild); else { laeuft = false; letzte = 0; }
  }
  function anstossen() {
    if (reduziert) { p = pZiel; c = cZiel; dreh.theta = dreh.zielTheta; dreh.phi = dreh.zielPhi; zeichnen(); return; }
    if (!laeuft && sichtbar) { laeuft = true; requestAnimationFrame(bild); }
  }

  // Drehen mit der Maus (nicht per Touch – dort bleibt Wischen fürs Scrollen frei)
  let ziehen = null;
  canvas.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    ziehen = { x: e.clientX, y: e.clientY, t: dreh.zielTheta, f: dreh.zielPhi };
    canvas.setPointerCapture(e.pointerId); canvas.classList.add('zieht');
  });
  canvas.addEventListener('pointermove', e => {
    if (!ziehen) return;
    dreh.zielTheta = MathUtils.clamp(ziehen.t - (e.clientX - ziehen.x) * .004, -.55, .45);
    dreh.zielPhi = MathUtils.clamp(ziehen.f - (e.clientY - ziehen.y) * .003, -.18, .12);
    anstossen();
  });
  const loslassen = () => { ziehen = null; canvas.classList.remove('zieht'); };
  canvas.addEventListener('pointerup', loslassen);
  canvas.addEventListener('pointercancel', loslassen);

  const ro = new ResizeObserver(groesse);
  ro.observe(buehne);
  const io = new IntersectionObserver(([e]) => { sichtbar = e.isIntersecting; if (sichtbar) anstossen(); });
  io.observe(buehne);

  canvas.addEventListener('webglcontextlost', ev => {
    ev.preventDefault();
    entsorgen();
    optionen.beiFehler && optionen.beiFehler();
  });

  function entsorgen() {
    if (entsorgt) return;
    entsorgt = true; ro.disconnect(); io.disconnect();
    renderer.dispose(); canvas.remove();
  }

  groesse();
  return {
    /** Schritt 0 … 4 ansteuern (animiert, außer bei reduzierter Bewegung). */
    schritt(n, sofort) { pZiel = n; if (sofort) { p = n; zeichnen(); } else anstossen(); },
    /** Fortschritt direkt setzen (Scroll-Kopplung). */
    fortschritt(wert) { pZiel = wert; p = wert; zeichnen(); },
    /** Schnittansicht: Schichten gestaffelt zeigen. */
    schnitt(an) { cZiel = an ? 1 : 0; anstossen(); },
    entsorgen
  };
}
