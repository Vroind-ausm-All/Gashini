/* Gashini – Wandaufbau-Szene (Three.js)
 *
 * Beispielhafter, vereinfachter Aufbau einer nichttragenden Metallständerwand:
 *   1 Ständerwerk  UW-Profile an Boden und Decke, CW-Ständer im Achsabstand 625 mm
 *   2 Dämmung      Mineralwolle 60 mm zwischen den Ständern (Rückseite bereits beplankt)
 *   3 Beplankung   Gipsplatten 12,5 mm, verschraubt
 *   4 Oberfläche   Fugen und Schraubköpfe gespachtelt, fertige Fläche
 *
 * Keine Aussage zu Brand- oder Schallschutz. Maße in Metern, x entlang der Wand,
 * y nach oben, z durch die Wand (Vorderseite +z).
 *
 * Dieselbe Szene erzeugt die Visualisierungen (renderings.mjs) und das
 * interaktive Modell auf der Website (einbindung.js). Zufall ist geseedet,
 * damit jede Darstellung reproduzierbar ist.
 */
import {
  Scene, Color, Fog, PerspectiveCamera, WebGLRenderer, Group, Mesh, BoxGeometry, PlaneGeometry,
  CylinderGeometry, MeshStandardMaterial, HemisphereLight, DirectionalLight, AmbientLight,
  CanvasTexture, RepeatWrapping, SRGBColorSpace, ACESFilmicToneMapping, PCFShadowMap, Plane, Vector3,
  MathUtils, EdgesGeometry, LineSegments, LineBasicMaterial
} from 'three';

export const MASSE = { achs: 0.625, felder: 4, hoehe: 2.6, profil: 0.075, flansch: 0.05, platte: 0.0125, blech: 0.0018 };
const B = MASSE.achs * MASSE.felder;          // Wandlänge 2,50 m
const H = MASSE.hoehe;
const T = MASSE.profil / 2;                   // halbe Ständertiefe

export const FARBEN = {
  hintergrund: 0xF2F1ED, beton: 0xB9B5AE, stahl: 0xC3C6C8, wolle: 0xCDBB8E, platte: 0xE7E4DD,
  kern: 0xD8D3C8, spachtel: 0xF3F1EC, oberflaeche: 0xF6F5F1, schraube: 0x3A3B3D, linie: 0x0E0E0E, ziegel: 0xB5391C
};

/* ------------------------------------------------------------------ Zufall und Texturen */
function zufall(seed) {
  let s = seed >>> 0;
  return () => { s += 0x6D2B79F5; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

function leinwand(groesse, maler) {
  const c = document.createElement('canvas');
  c.width = c.height = groesse;
  maler(c.getContext('2d'), groesse);
  const t = new CanvasTexture(c);
  t.wrapS = t.wrapT = RepeatWrapping;
  t.colorSpace = SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

function rauschen(ctx, g, r, basis, streuung, anzahl, groesse) {
  ctx.fillStyle = basis; ctx.fillRect(0, 0, g, g);
  for (let i = 0; i < anzahl; i++) {
    const v = Math.round((r() - .5) * streuung);
    ctx.fillStyle = `rgba(${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${Math.abs(v) / 255})`;
    const s = groesse * (.4 + r());
    ctx.fillRect(r() * g, r() * g, s, s);
  }
}

const TEXTUREN = {};
function texturen(qualitaet) {
  const g = qualitaet === 'hoch' ? 1024 : 512;
  if (TEXTUREN[g]) return TEXTUREN[g];
  const t = {};
  t.beton = leinwand(g, (ctx, n) => {
    const r = zufall(11);
    rauschen(ctx, n, r, '#C2BEB7', 34, n * 26, n / 420);
    for (let i = 0; i < 60; i++) {           // Wolken
      const x = r() * n, y = r() * n, rad = n * (.08 + r() * .2);
      const grd = ctx.createRadialGradient(x, y, 0, x, y, rad);
      grd.addColorStop(0, `rgba(${r() > .5 ? '255,255,255' : '60,55,50'},.028)`); grd.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = grd; ctx.fillRect(0, 0, n, n);
    }
    for (let i = 0; i < n * .6; i++) {       // Poren
      ctx.fillStyle = `rgba(60,56,50,${.08 + r() * .2})`;
      ctx.beginPath(); ctx.arc(r() * n, r() * n, r() * n / 700 + .3, 0, 7); ctx.fill();
    }
  });
  t.beton.repeat.set(4, 4);
  t.stahl = leinwand(g, (ctx, n) => {         // verzinkt: Zinkblumen als helle und dunkle Flecken
    const r = zufall(23);
    ctx.fillStyle = '#C4C7C9'; ctx.fillRect(0, 0, n, n);
    for (let i = 0; i < 900; i++) {
      const x = r() * n, y = r() * n, s = n * (.01 + r() * .035), v = r();
      ctx.fillStyle = v > .5 ? `rgba(255,255,255,${.05 + r() * .12})` : `rgba(70,75,80,${.04 + r() * .1})`;
      ctx.beginPath(); const ecken = 5 + Math.floor(r() * 3);
      for (let k = 0; k < ecken; k++) { const w = k / ecken * 6.283 + r() * .5, rr = s * (.6 + r() * .5); k ? ctx.lineTo(x + Math.cos(w) * rr, y + Math.sin(w) * rr) : ctx.moveTo(x + Math.cos(w) * rr, y + Math.sin(w) * rr); }
      ctx.fill();
    }
    ctx.globalAlpha = .08; ctx.strokeStyle = '#ffffff';
    for (let y = 0; y < n; y += 3) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(n, y + (r() - .5) * 2); ctx.stroke(); }
    ctx.globalAlpha = 1;
  });
  t.wolle = leinwand(g, (ctx, n) => {
    const r = zufall(37);
    ctx.fillStyle = '#CDBB8E'; ctx.fillRect(0, 0, n, n);
    for (let i = 0; i < n * 9; i++) {         // Fasern
      const x = r() * n, y = r() * n, l = n * (.01 + r() * .05), w = (r() - .5) * .9;
      ctx.strokeStyle = r() > .55 ? `rgba(250,238,205,${.18 + r() * .3})` : `rgba(120,100,60,${.1 + r() * .22})`;
      ctx.lineWidth = .5 + r() * 1.1;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + l * .5, y + (r() - .5) * l * .4, x + Math.cos(w) * l, y + Math.sin(w) * l); ctx.stroke();
    }
    for (let i = 0; i < 140; i++) {
      const x = r() * n, y = r() * n, rad = n * (.02 + r() * .06);
      const grd = ctx.createRadialGradient(x, y, 0, x, y, rad);
      grd.addColorStop(0, 'rgba(90,70,40,.10)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = grd; ctx.fillRect(0, 0, n, n);
    }
  });
  t.platte = leinwand(g, (ctx, n) => {        // Kartonoberfläche
    const r = zufall(41);
    rauschen(ctx, n, r, '#DEDAD1', 22, n * 22, n / 380);
    ctx.globalAlpha = .05;
    for (let i = 0; i < n * 2; i++) { ctx.strokeStyle = r() > .5 ? '#fff' : '#9a958b'; ctx.beginPath(); const x = r() * n, y = r() * n; ctx.moveTo(x, y); ctx.lineTo(x + r() * 18, y + (r() - .5) * 2); ctx.stroke(); }
    ctx.globalAlpha = 1;
  });
  t.spachtel = leinwand(g, (ctx, n) => {      // Spachtelbahnen
    const r = zufall(53);
    rauschen(ctx, n, r, '#F1EFEA', 18, n * 10, n / 300);
    for (let i = 0; i < 70; i++) {
      const y = r() * n, h = n * (.04 + r() * .1);
      const grd = ctx.createLinearGradient(0, y, 0, y + h);
      grd.addColorStop(0, 'rgba(255,255,255,0)'); grd.addColorStop(.5, `rgba(${r() > .5 ? '255,255,255' : '200,195,185'},.22)`); grd.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = grd; ctx.fillRect(0, y, n, h);
    }
  });
  t.oberflaeche = leinwand(g, (ctx, n) => {   // gerollte Farbe, feine Struktur
    const r = zufall(67);
    rauschen(ctx, n, r, '#F5F4F0', 12, n * 40, n / 600);
  });
  TEXTUREN[g] = t;
  return t;
}

/* ------------------------------------------------------------------ Geometrie-Helfer */
function quader(b, h, t, mat, x, y, z) {
  const m = new Mesh(new BoxGeometry(b, h, t), mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

/** U-Profil (UW) entlang x, Öffnung nach oben (unten) oder unten (oben). Ursprung am linken Ende. */
function uwProfil(mat, oben) {
  const g = new Group();
  const s = MASSE.blech, steg = MASSE.profil, fl = 0.04;
  const yb = oben ? fl - s / 2 : s / 2;
  g.add(quader(B, s, steg, mat, B / 2, yb, 0));
  g.add(quader(B, fl, s, mat, B / 2, fl / 2, -steg / 2 + s / 2));
  g.add(quader(B, fl, s, mat, B / 2, fl / 2, steg / 2 - s / 2));
  return g;
}

/** C-Profil (CW) senkrecht. Steg in z-Richtung, Flansche in x-Richtung. Ursprung unten Mitte. */
function cwProfil(mat, laenge, richtung) {
  const g = new Group();
  const s = MASSE.blech, steg = MASSE.profil - 0.004, fl = MASSE.flansch, lippe = 0.008;
  const d = richtung;  // Öffnung nach +x oder -x
  g.add(quader(s, laenge, steg, mat, 0, laenge / 2, 0));
  g.add(quader(fl, laenge, s, mat, d * fl / 2, laenge / 2, -steg / 2 + s / 2));
  g.add(quader(fl, laenge, s, mat, d * fl / 2, laenge / 2, steg / 2 - s / 2));
  g.add(quader(s, laenge, lippe, mat, d * fl, laenge / 2, -steg / 2 + lippe / 2));
  g.add(quader(s, laenge, lippe, mat, d * fl, laenge / 2, steg / 2 - lippe / 2));
  return g;
}

/* ------------------------------------------------------------------ Szene */
export function erstelleSzene(optionen = {}) {
  const qualitaet = optionen.qualitaet || 'mittel';
  const tex = texturen(qualitaet);
  const szene = new Scene();
  szene.background = new Color(optionen.hintergrund ?? FARBEN.hintergrund);
  szene.fog = new Fog(optionen.hintergrund ?? FARBEN.hintergrund, 6, 11.5);

  // Schnittebenen: jede Schicht kann ab einer x-Position abgeschnitten werden (Schnittansicht)
  const schnitt = { daemmung: new Plane(new Vector3(1, 0, 0), 0), platten: new Plane(new Vector3(1, 0, 0), 0),
                    spachtel: new Plane(new Vector3(1, 0, 0), 0), oberflaeche: new Plane(new Vector3(1, 0, 0), 0) };

  const mat = {
    beton: new MeshStandardMaterial({ map: tex.beton, color: 0xffffff, roughness: .92, metalness: 0 }),
    stahl: new MeshStandardMaterial({ map: tex.stahl, color: 0xffffff, roughness: .38, metalness: .55 }),
    wolle: new MeshStandardMaterial({ map: tex.wolle, color: 0xffffff, roughness: 1, metalness: 0, clippingPlanes: [schnitt.daemmung], clipShadows: true }),
    platte: new MeshStandardMaterial({ map: tex.platte, color: 0xffffff, roughness: .85, clippingPlanes: [schnitt.platten], clipShadows: true }),
    platteHinten: new MeshStandardMaterial({ map: tex.platte, color: 0xf2f0ea, roughness: .85 }),
    spachtel: new MeshStandardMaterial({ map: tex.spachtel, color: 0xffffff, roughness: .7, clippingPlanes: [schnitt.spachtel], clipShadows: true }),
    oberflaeche: new MeshStandardMaterial({ map: tex.oberflaeche, color: 0xffffff, roughness: .9, clippingPlanes: [schnitt.oberflaeche], clipShadows: true }),
    schraube: new MeshStandardMaterial({ color: FARBEN.schraube, roughness: .4, metalness: .7, clippingPlanes: [schnitt.platten], clipShadows: true }),
    akzent: new MeshStandardMaterial({ color: FARBEN.ziegel, roughness: .6 })
  };

  // Boden
  const boden = new Mesh(new PlaneGeometry(14, 10), mat.beton);
  boden.rotation.x = -Math.PI / 2; boden.position.set(B / 2, 0, 0); boden.receiveShadow = true;
  szene.add(boden);

  // Anriss: Lage der Wand auf dem Boden, wie vor dem Setzen der Profile angezeichnet
  const anriss = new Group();
  const anrissMat = new MeshStandardMaterial({ color: FARBEN.ziegel, roughness: .8 });
  for (const z of [-T, T]) {
    const l = new Mesh(new BoxGeometry(B + 0.5, 0.0008, 0.005), anrissMat);
    l.position.set(B / 2, 0.0004, z); l.receiveShadow = true; anriss.add(l);
  }
  for (let i = 0; i <= MASSE.felder; i++) {
    const k = new Mesh(new BoxGeometry(0.005, 0.0008, 0.16), anrissMat);
    k.position.set(i * MASSE.achs, 0.0004, 0); anriss.add(k);
  }
  szene.add(anriss);

  const wand = new Group();
  szene.add(wand);

  // 1 Ständerwerk
  const uwUnten = uwProfil(mat.stahl, false);
  const uwOben = uwProfil(mat.stahl, true);
  uwOben.position.y = H - 0.04;
  const staender = [];
  for (let i = 0; i <= MASSE.felder; i++) {
    const richtung = i === MASSE.felder ? -1 : 1;
    const s = cwProfil(mat.stahl, H - 0.02, richtung);
    s.position.set(i * MASSE.achs + (i === 0 ? 0.002 : i === MASSE.felder ? -0.002 : 0), 0.01, 0);
    staender.push(s); wand.add(s);
  }
  const profilKanten = new LineBasicMaterial({ color: FARBEN.linie, transparent: true, opacity: .18 });
  [uwUnten, uwOben].forEach(u => wand.add(u));

  // Rückseitige Beplankung (erscheint mit der Dämmung – erste Seite wird vor dem Dämmen geschlossen)
  const rueckseite = [];
  for (let i = 0; i < 2; i++) {
    const p = quader(1.25 - 0.002, H - 0.01, MASSE.platte, mat.platteHinten, i * 1.25 + 0.625, H / 2, -T - MASSE.platte / 2);
    rueckseite.push(p); wand.add(p);
  }

  // 2 Dämmung
  const daemmung = [];
  for (let i = 0; i < MASSE.felder; i++) {
    const d = quader(MASSE.achs - 0.052, H - 0.09, 0.06, mat.wolle, i * MASSE.achs + MASSE.achs / 2 + 0.002, H / 2, -T + 0.03 + 0.002);
    d.castShadow = false;
    daemmung.push(d); wand.add(d);
  }

  // 3 Beplankung vorn: zwei Platten 1250 mm, Schrauben im Abstand 250 mm
  const platten = [], schrauben = [];
  const schraubGeo = new CylinderGeometry(0.0055, 0.0055, 0.0016, 12);
  for (let i = 0; i < 2; i++) {
    const p = quader(1.25 - 0.002, H - 0.01, MASSE.platte, mat.platte, i * 1.25 + 0.625, H / 2, T + MASSE.platte / 2);
    platten.push(p); wand.add(p);
    const gruppe = new Group();
    for (let k = 0; k <= 2; k++) {
      const x = i * 1.25 + k * MASSE.achs + (k === 0 ? 0.015 : k === 2 ? -0.015 : 0);
      for (let j = 0; j < 10; j++) {
        const sch = new Mesh(schraubGeo, mat.schraube);
        sch.rotation.x = Math.PI / 2;
        sch.position.set(x, 0.15 + j * 0.25, T + MASSE.platte + 0.0004);
        gruppe.add(sch);
      }
    }
    schrauben.push(gruppe); wand.add(gruppe);
  }

  // 4 Spachtel und Oberfläche
  const fuge = quader(0.12, H - 0.02, 0.0012, mat.spachtel, 1.25, H / 2, T + MASSE.platte + 0.0007);
  fuge.castShadow = false;
  const flecken = new Group();
  const fleckGeo = new CylinderGeometry(0.02, 0.02, 0.0008, 16);
  for (let k = 0; k <= MASSE.felder; k++) {
    if (k === 2) continue;
    const x = k * MASSE.achs + (k === 0 ? 0.015 : k === MASSE.felder ? -0.015 : 0);
    for (let j = 0; j < 10; j++) {
      const f = new Mesh(fleckGeo, mat.spachtel); f.rotation.x = Math.PI / 2;
      f.position.set(x, 0.15 + j * 0.25, T + MASSE.platte + 0.0006); flecken.add(f);
    }
  }
  wand.add(fuge, flecken);
  const oberflaeche = quader(B - 0.004, H - 0.012, 0.001, mat.oberflaeche, B / 2, H / 2, T + MASSE.platte + 0.0016);
  oberflaeche.castShadow = false;
  wand.add(oberflaeche);

  // Feine Kanten an den Profilen – Erinnerung an die Zeichnung
  if (optionen.kanten !== false) {
    [...staender, uwUnten, uwOben].forEach(g => g.children.forEach(m => {
      const k = new LineSegments(new EdgesGeometry(m.geometry), profilKanten); m.add(k);
    }));
  }

  // Licht: weiches Tageslicht von links vorn, Aufhellung von rechts
  szene.add(new HemisphereLight(0xffffff, 0xC9C3B8, .88));
  szene.add(new AmbientLight(0xffffff, .1));
  const sonne = new DirectionalLight(0xFFF4E6, 2.55);
  sonne.position.set(5.2, 4.4, 3.1);
  sonne.target.position.set(B / 2, 1, 0);
  sonne.castShadow = optionen.schatten !== false;
  const karte = optionen.schattenKarte || (qualitaet === 'hoch' ? 4096 : 1024);
  sonne.shadow.mapSize.set(karte, karte);
  sonne.shadow.camera.left = -3.5; sonne.shadow.camera.right = 3.5; sonne.shadow.camera.top = 3.5; sonne.shadow.camera.bottom = -3;
  sonne.shadow.camera.near = 1; sonne.shadow.camera.far = 14;
  sonne.shadow.bias = -0.0004; sonne.shadow.normalBias = 0.012; sonne.shadow.radius = 4;
  sonne.shadow.intensity = .6;
  szene.add(sonne, sonne.target);
  const streif = new DirectionalLight(0xEEF2F6, .5);
  streif.position.set(-4, 2.2, 3.5);
  szene.add(streif);

  const teile = { uw: [uwUnten, uwOben], staender, rueckseite, daemmung, platten, schrauben, fuge, flecken, oberflaeche };
  return { szene, wand, teile, schnitt, mat, B, H, T };
}

/* ------------------------------------------------------------------ Zustand: Fortschritt 0 … 4 */
const glatt = t => t <= 0 ? 0 : t >= 1 ? 1 : 1 - Math.pow(1 - t, 3);
function versetzt(a, i, n, staffel = .45) {   // lokaler Fortschritt des i-ten von n Elementen
  const gesamt = 1 + staffel * (n - 1) / Math.max(n - 1, 1);
  return glatt(a * gesamt - staffel * i / Math.max(n - 1, 1));
}
const sichtbar = (o, v) => { o.visible = v > 0.001; };

/** Setzt die Szene auf einen Fortschritt p ∈ [0, 4]. schnittAnteil ∈ [0, 1] staffelt die Schichten von links nach rechts. */
export function setzeFortschritt(s, p, schnittAnteil = 0) {
  const { teile } = s;
  const a1 = MathUtils.clamp(p, 0, 1), a2 = MathUtils.clamp(p - 1, 0, 1), a3 = MathUtils.clamp(p - 2, 0, 1), a4 = MathUtils.clamp(p - 3, 0, 1);

  // Ständerwerk: UW-Profile ziehen sich auf, Ständer senken sich ein
  teile.uw.forEach((u, i) => { const v = versetzt(a1, i, 2, .2); sichtbar(u, v); u.scale.x = Math.max(v, .001); });
  teile.staender.forEach((st, i) => { const v = versetzt(MathUtils.clamp(a1 * 1.25 - .25, 0, 1), i, teile.staender.length); sichtbar(st, v); st.position.y = .01 + (1 - v) * 1.1; });

  // Dämmung mit rückseitiger Beplankung
  teile.rueckseite.forEach((r, i) => { const v = versetzt(MathUtils.clamp(a2 * 1.6, 0, 1), i, 2); sichtbar(r, v); r.position.z = -T - MASSE.platte / 2 - (1 - v) * .5; });
  teile.daemmung.forEach((d, i) => { const v = versetzt(MathUtils.clamp(a2 * 1.4 - .4, 0, 1), i, teile.daemmung.length); sichtbar(d, v); d.position.z = -T + .032 + (1 - v) * .7; });

  // Beplankung vorn
  teile.platten.forEach((pl, i) => { const v = versetzt(MathUtils.clamp(a3 * 1.3, 0, 1), i, 2); sichtbar(pl, v); pl.position.z = T + MASSE.platte / 2 + (1 - v) * .8; });
  teile.schrauben.forEach((g, i) => { const v = MathUtils.clamp(a3 * 3 - 2 - i * .3, 0, 1); sichtbar(g, v); g.scale.setScalar(Math.max(v, .001)); g.position.z = (1 - v) * .02; });

  // Spachtel, dann fertige Oberfläche von links nach rechts
  const vf = glatt(MathUtils.clamp(a4 * 2.2, 0, 1));
  sichtbar(teile.fuge, vf); teile.fuge.scale.y = Math.max(vf, .001); teile.fuge.position.y = (H / 2) * vf + .01;
  sichtbar(teile.flecken, vf); teile.flecken.children.forEach((f, i) => f.scale.setScalar(Math.max(MathUtils.clamp(vf * 2 - (i % 10) / 10, 0, 1), .001)));
  const vo = glatt(MathUtils.clamp(a4 * 1.6 - .6, 0, 1));
  sichtbar(teile.oberflaeche, vo); teile.oberflaeche.scale.x = Math.max(vo, .001); teile.oberflaeche.position.x = (B - .004) * vo / 2 + .002;

  // Schnittansicht: Schichten beginnen gestaffelt (Dämmung ab 0,625 m, Platten ab 1,00 m, Spachtel ab 1,15 m, Oberfläche ab 1,75 m)
  const c = glatt(schnittAnteil);
  s.schnitt.daemmung.constant = -c * MASSE.achs;
  s.schnitt.platten.constant = -c * 1.0;
  s.schnitt.spachtel.constant = -c * 1.15;
  s.schnitt.oberflaeche.constant = -c * 1.75;
}

/* ------------------------------------------------------------------ Renderer und Kamera */
export function erstelleRenderer(canvas, optionen = {}) {
  const r = new WebGLRenderer({ canvas, antialias: optionen.antialias !== false, alpha: false, preserveDrawingBuffer: !!optionen.standbild, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(optionen.pixelRatio || window.devicePixelRatio || 1, optionen.maxPixelRatio || 2));
  r.outputColorSpace = SRGBColorSpace;
  r.toneMapping = ACESFilmicToneMapping;
  r.toneMappingExposure = optionen.belichtung || 1.02;
  r.localClippingEnabled = true;
  r.shadowMap.enabled = optionen.schatten !== false;
  r.shadowMap.type = PCFShadowMap;
  return r;
}

export const ANSICHTEN = {
  // Dreiviertelansicht der ganzen Wand – Hero und interaktives Modell
  gesamt: { pos: [-1.75, 2.75, 4.55], ziel: [1.34, 1.2, 0], fov: 35 },
  // Untersicht entlang des Ständerwerks – Trockenbau-Seitenkopf
  staender: { pos: [-0.8, 0.9, 2.45], ziel: [1.2, 1.45, 0], fov: 47 },
  // Ständer und Dämmung, Rückseite beplankt – Leistungsübersicht
  daemmung: { pos: [-0.55, 1.95, 3.1], ziel: [1.05, 1.22, 0], fov: 38 },
  // Mobil: höher und weiter weg, damit die ganze Wand ins Hochformat passt
  mobil: { pos: [3.5, 1.95, 6.2], ziel: [1.25, 1.2, 0], fov: 34 }
};

export function erstelleKamera(ansicht, seitenverhaeltnis, eigene) {
  const a = (eigene && eigene[ansicht]) || ANSICHTEN[ansicht] || ANSICHTEN.gesamt;
  const k = new PerspectiveCamera(a.fov, seitenverhaeltnis, .05, 40);
  k.position.set(...a.pos);
  k.lookAt(new Vector3(...a.ziel));
  k.userData.ziel = new Vector3(...a.ziel);
  return k;
}

/** Projiziert Weltpunkte in Bildkoordinaten (0 … 1) – für Beschriftungen über den Visualisierungen. */
export function projiziere(kamera, punkte) {
  kamera.updateMatrixWorld();
  const erg = {};
  for (const [name, p] of Object.entries(punkte)) {
    const v = new Vector3(...p).project(kamera);
    erg[name] = [+((v.x + 1) / 2).toFixed(4), +((1 - v.y) / 2).toFixed(4)];
  }
  return erg;
}

/** Ankerpunkte für Beschriftungen (Weltkoordinaten). */
export const ANKER = {
  uw: [0.32, 0.045, T],
  cw: [MASSE.achs + 0.02, 2.05, 0.01],
  daemmung: [MASSE.achs * 1.5, 1.7, 0.0],
  platte: [MASSE.achs * 2.55, 2.1, T + MASSE.platte],
  spachtel: [1.25, 0.75, T + MASSE.platte + .002],
  oberflaeche: [MASSE.achs * 3.5, 1.45, T + MASSE.platte + .002],
  achsmass: [MASSE.achs * 0.5, 0.0, T + 0.1]
};
