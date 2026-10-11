// Browser-Tests für den Webauftritt.
//   cd tests && npm ci && node e2e.mjs
// Voraussetzungen: PHP ≥ 8.1, Chromium (Pfad über CHROMIUM_PFAD, sonst Playwright-Standard).
// Baut dist/web (Vorschau) und einen Entwurfs-Build mit Beispielprojekten, startet
// php -S mit einer Test-Konfiguration (Mails werden als Datei abgelegt) und prüft
// Darstellung, Bedienung, Barrierefreiheit und Formularstrecke.
import { chromium } from 'playwright';
import { spawn, execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readdirSync, existsSync, mkdirSync, readFileSync, cpSync } from 'node:fs';
import zlib from 'node:zlib';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import net from 'node:net';

const WURZEL = join(dirname(fileURLToPath(import.meta.url)), '..');
const TMP = mkdtempSync(join(tmpdir(), 'gashini-e2e-'));
const BERICHT = process.env.BERICHT_VERZEICHNIS || join(TMP, 'bericht');
mkdirSync(BERICHT, { recursive: true });
const AXE = readFileSync(join(WURZEL, 'tests/node_modules/axe-core/axe.min.js'), 'utf8');

const ergebnisse = [];
const pruefe = (name, ok, detail = '') => ergebnisse.push({ name, ok: !!ok, detail });

function freierPort() {
  return new Promise(r => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
}
async function phpServer(wurzel, konfig) {
  const port = await freierPort();
  const proc = spawn('php', ['-d', 'upload_max_filesize=8M', '-d', 'post_max_size=14M', '-S', `127.0.0.1:${port}`, '-t', wurzel],
    { env: { ...process.env, GASHINI_KONFIG: konfig }, stdio: 'ignore' });
  for (let i = 0; i < 50; i++) {
    try { await new Promise((ok, nein) => { const c = net.connect(port, '127.0.0.1', () => { c.end(); ok(); }); c.on('error', nein); }); break; }
    catch { await new Promise(r => setTimeout(r, 100)); }
  }
  return { proc, basis: `http://127.0.0.1:${port}/` };
}
function testKonfig(name, postVerz) {
  const pfad = join(TMP, name + '.php');
  writeFileSync(pfad, `<?php return ['empfaenger'=>'anfragen@test.invalid','absender'=>'website@test.invalid','transport'=>'datei',
    'datei_verzeichnis'=>'${postVerz}','speicher_verzeichnis'=>'${join(TMP, name + '-limit')}','geheimnis'=>str_repeat('e',40),
    'erlaubte_herkunft'=>[],'limit_pro_ip'=>1000,'limit_gesamt_pro_stunde'=>1000];`);
  return pfad;
}
const post = verz => existsSync(verz) ? readdirSync(verz).filter(f => f.endsWith('.eml')) : [];

// ------------------------------------------------------------------ Builds
execFileSync('python3', ['scripts/build-site.py'], { cwd: WURZEL });
execFileSync('python3', ['scripts/firmendaten.py'], { cwd: WURZEL });
const entwurf = join(TMP, 'entwurf-web');
execFileSync('python3', ['scripts/build-site.py'], { cwd: WURZEL, env: { ...process.env, ENTWUERFE: '1', AUSGABE: entwurf } });
execFileSync('python3', ['scripts/build-site.py'], { cwd: WURZEL });   // web/ wiederherstellen
const vorschau = join(TMP, 'vorschau-web');
cpSync(join(WURZEL, 'dist/web'), vorschau, { recursive: true });
execFileSync('python3', ['scripts/vorschau-markieren.py', vorschau], { cwd: WURZEL });

const POST = join(TMP, 'post');
const haupt = await phpServer(join(WURZEL, 'dist/web'), testKonfig('haupt', POST));
const entw = await phpServer(entwurf, testKonfig('entwurf', join(TMP, 'post2')));
const vors = await phpServer(vorschau, testKonfig('vorschau', join(TMP, 'post3')));
const STARTOPTIONEN = { args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  ...(process.env.CHROMIUM_PFAD ? { executablePath: process.env.CHROMIUM_PFAD } : {}) };
const browser = await chromium.launch(STARTOPTIONEN);

// Gültiges Mini-PNG für den Upload-Test
function png() {
  const crc = b => { let c, t = []; for (let n = 0; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    let r = 0xffffffff; for (const x of b) r = t[(r ^ x) & 0xff] ^ (r >>> 8); return (r ^ 0xffffffff) >>> 0; };
  const chunk = (typ, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(typ), d]);
    const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(4, 0); ihdr.writeUInt32BE(3, 4); ihdr[8] = 8; ihdr[9] = 2;
  const roh = Buffer.concat(Array.from({ length: 3 }, () => Buffer.from([0, 181, 57, 28, 181, 57, 28, 181, 57, 28, 181, 57, 28])));
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(roh)), chunk('IEND', Buffer.alloc(0))]);
}
async function durchscrollen(p) {
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += 300) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(40); }
  await p.waitForTimeout(1500);
}

const SEITEN = ['', 'leistungen/', 'leistungen/trockenbau/', 'leistungen/hausmeisterservice/', 'leistungen/reparatur-und-instandhaltung/',
  'projekte/', 'netzwerk/', 'ueber-uns/', 'fragen/', 'kontakt/', 'kontakt/danke/', 'impressum/', 'datenschutz/', '404.html'];
const BREITEN = [320, 375, 768, 1024, 1440];

try {
  // ---------------------------------------------------------------- Layout je Breite
  for (const b of BREITEN) {
    const ctx = await browser.newContext({ viewport: { width: b, height: 900 } });
    const p = await ctx.newPage();
    const ueberlauf = [];
    for (const s of SEITEN) {
      await p.goto(haupt.basis + s, { waitUntil: 'networkidle' });
      const w = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (w > 1) ueberlauf.push(`${s || '/'} (+${w}px)`);
    }
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1800);
    await p.screenshot({ path: join(BERICHT, `start-${b}.png`), fullPage: true });
    pruefe(`Kein waagerechter Überlauf bei ${b}px (${SEITEN.length} Seiten)`, ueberlauf.length === 0, ueberlauf.join(', '));
    await ctx.close();
  }

  // ---------------------------------------------------------------- Bildschirmfotos aller Seiten (Bericht)
  for (const b of [390, 1440]) {
    const ctx = await browser.newContext({ viewport: { width: b, height: b < 600 ? 844 : 900 } });
    const p = await ctx.newPage();
    for (const s of SEITEN) {
      await p.goto(vors.basis + s, { waitUntil: 'networkidle' });
      await durchscrollen(p);
      await p.evaluate(() => window.scrollTo(0, 0));
      await p.waitForTimeout(300);
      await p.screenshot({ path: join(BERICHT, `seite-${(s.replace(/\//g, '_').replace(/_$/, '') || 'start')}-${b}.png`), fullPage: true });
    }
    await ctx.close();
  }

  // ---------------------------------------------------------------- Textvergrößerung 200 %
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 800 } });
    const p = await ctx.newPage();
    const ueberlauf = [];
    for (const s of ['', 'kontakt/', 'leistungen/trockenbau/']) {
      await p.goto(haupt.basis + s, { waitUntil: 'networkidle' });
      await p.addStyleTag({ content: 'html{font-size:200%!important}' });
      const w = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (w > 1) ueberlauf.push(`${s || '/'} (+${w}px)`);
    }
    pruefe('Textvergrößerung auf 200 % bei 375px ohne waagerechten Überlauf', ueberlauf.length === 0, ueberlauf.join(', '));
    await ctx.close();
  }

  // ---------------------------------------------------------------- Barrierefreiheit (axe-core)
  for (const b of [1440, 375]) {
    const ctx = await browser.newContext({ viewport: { width: b, height: 900 } });
    const p = await ctx.newPage();
    const funde = [];
    for (const s of SEITEN) {
      await p.goto(haupt.basis + s, { waitUntil: 'networkidle' });
      // erst messen, wenn die Einstiegsanimationen (CSS) fertig sind – sonst misst axe Zwischenstände
      await p.evaluate(() => Promise.all(document.getAnimations().map(a => a.finished.catch(() => {}))));
      await p.waitForTimeout(300);
      await p.addScriptTag({ content: AXE });
      const r = await p.evaluate(async () => (await window.axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] })).violations
        .map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, ziel: v.nodes[0]?.target?.join(' ') })));
      r.forEach(v => funde.push({ seite: s || '/', ...v }));
    }
    const schwer = funde.filter(f => f.impact === 'serious' || f.impact === 'critical');
    pruefe(`axe-core WCAG 2.2 AA bei ${b}px: keine schweren oder kritischen Verstöße`, schwer.length === 0, JSON.stringify(schwer.slice(0, 6)));
    const rest = funde.filter(f => !(f.impact === 'serious' || f.impact === 'critical'));
    if (rest.length) pruefe(`axe-core Hinweise (moderat/gering) bei ${b}px – zur Kenntnis`, true, JSON.stringify(rest.slice(0, 6)));
    writeFileSync(join(BERICHT, `axe-${b}.json`), JSON.stringify(funde, null, 2));
    await ctx.close();
  }

  // ---------------------------------------------------------------- Tastatur und Sprunglink
  {
    const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    await p.keyboard.press('Tab');
    const erster = await p.evaluate(() => document.activeElement.className);
    await p.keyboard.press('Enter');
    const nachher = await p.evaluate(() => document.activeElement.id);
    pruefe('Erster Tab-Halt ist der Sprunglink, Enter springt zum Inhalt', erster.includes('sprunglink') && nachher === 'inhalt', `${erster} → ${nachher}`);
    let sichtbar = true;
    for (let i = 0; i < 6; i++) {
      await p.keyboard.press('Tab');
      const o = await p.evaluate(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; });
      sichtbar = sichtbar && o;
    }
    pruefe('Fokus ist bei Tastaturbedienung sichtbar (Outline ≥ 2px)', sichtbar);
    await p.close();
  }

  // ---------------------------------------------------------------- Mobile Navigation
  {
    const p = await browser.newPage({ viewport: { width: 375, height: 800 } });
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    const knopf = p.locator('.menue-knopf');
    const vorher = await p.locator('#hauptnav').isVisible();
    await knopf.focus(); await p.keyboard.press('Enter');
    await p.waitForTimeout(300);
    const offen = await knopf.getAttribute('aria-expanded');
    const navSichtbar = await p.locator('#hauptnav a').first().isVisible();
    const fokusImMenue = await p.evaluate(() => !!document.activeElement.closest('#hauptnav'));
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);
    const zu = await knopf.getAttribute('aria-expanded');
    const fokusZurueck = await p.evaluate(() => document.activeElement.classList.contains('menue-knopf'));
    pruefe('Mobilmenü: zu → öffnet per Tastatur, Fokus im Menü, Escape schließt, Fokus zurück',
      !vorher && offen === 'true' && navSichtbar && fokusImMenue && zu === 'false' && fokusZurueck,
      { vorher, offen, navSichtbar, fokusImMenue, zu, fokusZurueck });
    await p.close();
  }

  // Vollbild-Menü: beginnt direkt unter dem Kopf, alle Hauptpunkte sichtbar, auf kleinen Höhen scrollbar
  for (const [b, h] of [[390, 844], [768, 1024], [360, 600]]) {
    const p = await browser.newPage({ viewport: { width: b, height: h } });
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    await p.click('.menue-knopf');
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const nav = document.getElementById('hauptnav'), kopf = document.querySelector('.kopf').getBoundingClientRect();
      const q = nav.getBoundingClientRect();
      const punkte = [...nav.querySelectorAll(':scope > ul > li > a')].filter(a => getComputedStyle(a).display !== 'none');
      const verdeckt = punkte.filter(a => { const r = a.getBoundingClientRect(); return r.top < q.top || r.bottom > innerHeight; }).map(a => a.textContent.trim());
      const fuss = nav.querySelector('.hauptnav-fuss .knopf');
      fuss.scrollIntoView({ block: 'nearest' });
      const f = fuss.getBoundingClientRect();
      return {
        abstand: Math.abs(q.top - kopf.bottom), bisUnten: Math.abs(q.bottom - innerHeight),
        punkte: punkte.length, verdeckt,
        fussErreichbar: f.top >= q.top && f.bottom <= innerHeight + 1,
        seiteGescrollt: scrollY,
        leiste: (() => { const l = document.querySelector('.kontaktleiste'); return l ? getComputedStyle(l).display : 'none'; })()
      };
    });
    const ganz = b >= 390 ? r.verdeckt.length === 0 : true;
    pruefe(`Mobilmenü bei ${b}×${h}: direkt unter dem Kopf, bis zum unteren Rand, ${b >= 390 ? 'alle Hauptpunkte sichtbar' : 'Inhalt im Menü scrollbar'}, Kontaktknöpfe erreichbar`,
      r.abstand <= 1 && r.bisUnten <= 1 && r.punkte >= 6 && ganz && r.fussErreichbar && r.seiteGescrollt === 0 && r.leiste === 'none', r);
    await p.close();
  }

  // Desktop: volle Navigation ohne Menü-Knopf, Untermenü „Leistungen“ per Maus und Tastatur
  {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    const knopfSichtbar = await p.locator('.menue-knopf').isVisible();
    const punkte = await p.locator('#hauptnav > ul > li > a:visible').count();
    const unter = p.locator('.untermenue');
    const anfangs = await unter.isVisible();
    await p.hover('.hat-unter > a');
    const hover = await unter.isVisible();
    await p.mouse.move(640, 700);
    await p.waitForTimeout(100);
    const wegNachHover = !(await unter.isVisible());
    await p.focus('.unter-knopf');
    await p.keyboard.press('Enter');
    const ausgeklappt = await p.getAttribute('.unter-knopf', 'aria-expanded');
    await p.keyboard.press('Tab');
    const imUntermenue = await p.evaluate(() => !!document.activeElement.closest('.untermenue'));
    await p.keyboard.press('Escape');
    const zu = !(await unter.isVisible());
    const fokusKnopf = await p.evaluate(() => document.activeElement.classList.contains('unter-knopf'));
    const aktuell = await p.goto(haupt.basis + 'leistungen/trockenbau/', { waitUntil: 'networkidle' }).then(() =>
      p.getAttribute('.hat-unter > a', 'aria-current'));
    pruefe('Desktop-Navigation (1280px): kein Menü-Knopf, Untermenü per Hover und Tastatur, Escape schließt, Fokus zurück, Bereich markiert',
      !knopfSichtbar && punkte >= 5 && !anfangs && hover && wegNachHover && ausgeklappt === 'true' && imUntermenue && zu && fokusKnopf && aktuell === 'true',
      { knopfSichtbar, punkte, anfangs, hover, wegNachHover, ausgeklappt, imUntermenue, zu, fokusKnopf, aktuell });
    await p.close();
  }

  // Kopf auf dem Handy: weicht beim Herunterscrollen, kommt beim Hochscrollen zurück;
  // Schnellkontakt-Leiste fehlt auf der Kontaktseite (dort steht das Formular)
  {
    const p = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await p.goto(haupt.basis + 'leistungen/', { waitUntil: 'networkidle' });
    const kopfOben = () => p.evaluate(() => Math.round(document.querySelector('.kopf').getBoundingClientRect().bottom));
    for (let y = 100; y <= 1200; y += 100) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(40); }
    await p.waitForTimeout(450);
    const runter = await kopfOben();
    for (let y = 1100; y >= 700; y -= 100) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(40); }
    await p.waitForTimeout(450);
    const hoch = await kopfOben();
    const leisteStart = await p.locator('.kontaktleiste').isVisible();
    await p.goto(haupt.basis + 'kontakt/', { waitUntil: 'networkidle' });
    const leisteKontakt = await p.locator('.kontaktleiste').count();
    pruefe('Kopf (390px) weicht beim Herunterscrollen und kehrt beim Hochscrollen zurück; Schnellkontakt-Leiste nicht auf der Kontaktseite',
      runter <= 0 && hoch >= 60 && leisteStart && leisteKontakt === 0, { runter, hoch, leisteStart, leisteKontakt });
    await p.close();
  }

  // ---------------------------------------------------------------- Bewegtbild über einem Symbolbild
  // Noch liegen keine Clips im Repository. Damit die ausgelieferte site.js/site.css trotzdem geprüft wird, erzeugt
  // der Test einen kurzen WebM-Clip (Canvas + MediaRecorder) und fügt ihn beim Ausliefern der Startseite ein.
  {
    const werkstatt = await browser.newPage();
    const clip = Buffer.from(await werkstatt.evaluate(async () => {
      const c = document.createElement('canvas'); c.width = 320; c.height = 180;
      const x = c.getContext('2d');
      const rec = new MediaRecorder(c.captureStream(25), { mimeType: 'video/webm;codecs=vp8' });
      const teile = []; rec.ondataavailable = e => teile.push(e.data); rec.start(100);
      const t0 = performance.now();
      await new Promise(fertig => (function bild() {
        const t = (performance.now() - t0) / 1000;
        x.fillStyle = '#e9e6e0'; x.fillRect(0, 0, 320, 180); x.fillStyle = '#b5391c'; x.fillRect(20 + t * 120, 70, 30, 30);
        if (t < 1.5) requestAnimationFrame(bild); else fertig();
      })());
      rec.stop(); await new Promise(r => { rec.onstop = r; });
      const u = new Uint8Array(await new Blob(teile).arrayBuffer());
      let s = ''; for (let i = 0; i < u.length; i++) s += String.fromCharCode(u[i]);
      return btoa(s);
    }), 'base64');
    await werkstatt.close();
    const ergebnis = {};
    for (const art of ['normal', 'reduziert']) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: art === 'reduziert' ? 'reduce' : 'no-preference' });
      const p = await ctx.newPage();
      await p.route('**/assets/videos/testclip.webm', r => r.fulfill({ status: 200, contentType: 'video/webm', body: clip }));
      await p.route(u => u.pathname === '/', async r => {
        const antwort = await r.fetch();
        const html = (await antwort.text()).replace(/(<span class="bild-marke"[^>]*>Symbolbild<\/span>)/,
          '$1<video class="bewegtbild" muted loop playsinline preload="none" aria-hidden="true" data-bewegtbild><source src="assets/videos/testclip.webm" type="video/webm"></video>');
        await r.fulfill({ response: antwort, body: html });
      });
      await p.goto(haupt.basis, { waitUntil: 'networkidle' });
      const v = p.locator('video[data-bewegtbild]');
      const r = { geladenVorher: await v.evaluate(el => el.readyState) };
      await v.scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
      Object.assign(r, await v.evaluate(el => ({ laeuft: !el.paused && el.classList.contains('laeuft'), sichtbar: getComputedStyle(el).opacity === '1' })));
      r.knopf = await p.locator('.bewegtbild-knopf').count();
      if (r.knopf) {
        await p.locator('.bewegtbild-knopf').click(); await p.waitForTimeout(200);
        r.angehalten = await v.evaluate(el => el.paused && el.nextElementSibling.getAttribute('aria-label') === 'Video abspielen');
        await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
        await v.scrollIntoViewIfNeeded(); await p.waitForTimeout(700);
        r.bleibtAngehalten = await v.evaluate(el => el.paused);
      }
      ergebnis[art] = r;
      await ctx.close();
    }
    const n = ergebnis.normal, z = ergebnis.reduziert;
    pruefe('Bewegtbild: lädt erst im Sichtbereich, läuft dann über dem Standbild, Pause-Knopf hält an und bleibt angehalten; bei reduzierter Bewegung kein Start und kein Knopf',
      n.geladenVorher === 0 && n.laeuft && n.sichtbar && n.knopf === 1 && n.angehalten && n.bleibtAngehalten &&
      z.geladenVorher === 0 && !z.laeuft && !z.sichtbar && z.knopf === 0, ergebnis);
  }

  // ---------------------------------------------------------------- Formular: Validierung
  {
    const p = await browser.newPage({ viewport: { width: 1024, height: 900 } });
    await p.goto(haupt.basis + 'kontakt/', { waitUntil: 'networkidle' });
    await p.click('button[type=submit]');
    const invalid = await p.getAttribute('#f-name', 'aria-invalid');
    const fokus = await p.evaluate(() => document.activeElement.id);
    const fehlertext = await p.textContent('#f-email-fehler');
    const status = await p.textContent('.formular-status');
    pruefe('Leeres Absenden: Fehler am Feld (aria-invalid), Fokus auf erstem Fehler, Zusammenfassung',
      invalid === 'true' && fokus === 'f-name' && /E-Mail-Adresse oder eine Telefonnummer/.test(fehlertext) && /Felder/.test(status), { invalid, fokus, fehlertext, status });
    const beschrieben = await p.getAttribute('#f-name', 'aria-describedby');
    pruefe('Fehlertexte sind per aria-describedby mit dem Feld verknüpft', beschrieben === 'f-name-fehler');
    await p.close();
  }

  // ---------------------------------------------------------------- Formular: Erfolg und Doppelklick
  async function ausfuellen(p) {
    await p.fill('#f-name', 'Erika Beispiel');
    await p.fill('#f-email', 'erika@test.invalid');
    await p.selectOption('#f-leistung', 'Trockenbau & Innenausbau');
    await p.fill('#f-nachricht', 'Wir möchten im Wohnzimmer eine Trennwand mit Tür einziehen lassen.');
    await p.waitForTimeout(3200);   // realistische Ausfüllzeit, sonst greift die Spam-Erkennung
  }
  {
    const p = await browser.newPage({ viewport: { width: 1024, height: 900 } });
    await p.goto(haupt.basis + 'kontakt/', { waitUntil: 'networkidle' });
    const vorher = post(POST).length;
    await ausfuellen(p);
    await Promise.all([p.waitForURL(/kontakt\/danke\/\?ref=/, { timeout: 10000 }), p.click('button[type=submit]', { clickCount: 1 }).then(() => p.click('button[type=submit]').catch(() => {}))]);
    await p.waitForTimeout(500);
    const ref = await p.textContent('[data-vorgang] .nummer');
    const sichtbar = await p.isVisible('[data-vorgang]');
    pruefe('Erfolgreiche Anfrage: Weiterleitung auf Danke-Seite mit Vorgangsnummer', sichtbar && /^[A-Z0-9]{8}$/.test(ref), ref);
    pruefe('Doppelklick auf „Anfrage senden“ erzeugt genau eine Nachricht', post(POST).length - vorher === 1, post(POST).length - vorher);
    await p.close();
  }

  // ---------------------------------------------------------------- Formular: Serverfehler
  {
    const p = await browser.newPage({ viewport: { width: 1024, height: 900 } });
    await p.route('**/api/anfrage.php', r => r.fulfill({ status: 502, contentType: 'application/json',
      body: JSON.stringify({ ok: false, meldung: 'Die Anfrage konnte gerade nicht zugestellt werden.' }) }));
    await p.goto(haupt.basis + 'kontakt/', { waitUntil: 'networkidle' });
    await ausfuellen(p);
    await p.click('button[type=submit]');
    await p.waitForTimeout(600);
    const status = await p.textContent('.formular-status');
    const behalten = await p.inputValue('#f-nachricht');
    const frei = await p.getAttribute('button[type=submit]', 'aria-disabled');
    pruefe('Serverfehler: verständliche Meldung, Eingaben bleiben erhalten, Knopf wieder aktiv, keine Weiterleitung',
      /nicht zugestellt/.test(status) && behalten.includes('Trennwand') && frei === 'false' && p.url().endsWith('/kontakt/'), { status, frei });
    await p.close();
  }

  // ---------------------------------------------------------------- Ohne JavaScript
  {
    const ctx = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 800 } });
    const p = await ctx.newPage();
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    const h1 = await p.isVisible('h1');
    const navLink = await p.locator('#hauptnav a').first().isVisible();
    const zeichnung = await p.isVisible('.wandaufbau-rueckfall svg');
    const inhalte = await p.evaluate(() => [...document.querySelectorAll('[data-zeigen]')].every(e => getComputedStyle(e).opacity === '1'));
    pruefe('Ohne JavaScript: Inhalt, Navigation und Wandaufbau-Zeichnung sichtbar', h1 && navLink && zeichnung && inhalte, { h1, navLink, zeichnung, inhalte });
    await p.goto(haupt.basis + 'kontakt/', { waitUntil: 'networkidle' });
    const vorher = post(POST).length;
    await p.fill('#f-name', 'Ohne Skript');
    await p.fill('#f-telefon', '0123 456789');
    await p.selectOption('#f-leistung', 'Hausmeisterservice');
    await p.fill('#f-nachricht', 'Regelmäßige Objektkontrolle für ein Mehrfamilienhaus.');
    await Promise.all([p.waitForURL(/kontakt\/danke\//), p.click('button[type=submit]')]);
    pruefe('Ohne JavaScript: Formular wird serverseitig angenommen und leitet zur Danke-Seite', post(POST).length - vorher === 1 && p.url().includes('ref='), p.url());
    await ctx.close();
  }

  // ---------------------------------------------------------------- Bewegung reduzieren
  {
    const ctx = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    const klasse = await p.evaluate(() => document.documentElement.className);
    const sichtbar = await p.evaluate(() => [...document.querySelectorAll('[data-zeigen], [data-zeilen], [data-enthuellen]')]
      .every(e => getComputedStyle(e).opacity === '1' && getComputedStyle(e).visibility === 'visible'));
    const zeilen = await p.evaluate(() => [...document.querySelectorAll('.buehne-titel .zeile > span')].map(e => getComputedStyle(e).transform));
    const gepinnt = await p.evaluate(() => !!document.querySelector('.pin-spacer'));
    pruefe('Bewegung reduzieren: keine Bewegungsklasse, alle Inhalte sofort sichtbar, kein Scroll-Pinning',
      !klasse.split(' ').includes('bewegung') && sichtbar && zeilen.every(t => t === 'none') && !gepinnt, { klasse, sichtbar, zeilen, gepinnt });
    await ctx.close();
  }

  // ---------------------------------------------------------------- GSAP: nach dem Scrollen ist alles sichtbar
  // Ohne WebGL: SwiftShader rendert die 3D-Szene in Software und bremst den Testbrowser so stark, dass GSAP
  // (lagSmoothing) Animationen streckt. Das 3D-Modell wird unten gesondert geprüft.
  {
    const b3 = await chromium.launch({ ...STARTOPTIONEN, args: ['--disable-webgl', '--disable-3d-apis'] });
    const p = await b3.newPage({ viewport: { width: 1440, height: 900 } });
    const unsichtbar = [];
    for (const s of ['', 'leistungen/', 'leistungen/trockenbau/', 'leistungen/reparatur-und-instandhaltung/', 'leistungen/hausmeisterservice/', 'netzwerk/', 'ueber-uns/', 'fragen/']) {
      await p.goto(haupt.basis + s, { waitUntil: 'networkidle' });
      await durchscrollen(p);
      // Animationen dürfen unter Last länger brauchen – geprüft wird, dass am Ende alles sichtbar ist
      const pruefen = () => [...document.querySelectorAll('[data-zeigen], main [data-zeilen], [data-enthuellen]')]
        .filter(e => parseFloat(getComputedStyle(e).opacity) < .99 || getComputedStyle(e).visibility !== 'visible').length;
      await p.waitForFunction(() => ![...document.querySelectorAll('[data-zeigen], main [data-zeilen], [data-enthuellen]')]
        .some(e => parseFloat(getComputedStyle(e).opacity) < .99 || getComputedStyle(e).visibility !== 'visible'), null, { timeout: 8000 }).catch(() => {});
      const n = await p.evaluate(pruefen);
      if (n) unsichtbar.push(`${s || '/'}: ${n}`);
    }
    pruefe('Bewegung (GSAP): nach dem Scrollen sind auf allen Seiten alle animierten Inhalte vollständig sichtbar', unsichtbar.length === 0, unsichtbar.join(', '));
    await b3.close();
  }

  // ---------------------------------------------------------------- Wandaufbau: Three.js
  {
    const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const fehler = []; p.on('pageerror', e => fehler.push(e.message));
    await p.goto(haupt.basis + 'leistungen/trockenbau/', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.querySelector('#wandaufbau').scrollIntoView());
    await p.waitForFunction(() => document.querySelector('#wandaufbau').classList.contains('ist-3d'), null, { timeout: 15000 }).catch(() => {});
    const dreiD = await p.evaluate(() => ({ klasse: document.querySelector('#wandaufbau').className, canvas: !!document.querySelector('.wandaufbau-canvas') }));
    const st = await p.evaluate(() => { const r = document.querySelector('.wandaufbau-raster'); return !!r.closest('.pin-spacer'); });
    await p.click('.wandaufbau-schritt[data-schritt="2"]');
    await p.waitForTimeout(1200);
    const gedrueckt = await p.getAttribute('.wandaufbau-schritt[data-schritt="2"]', 'aria-pressed');
    await p.screenshot({ path: join(BERICHT, 'wandaufbau-1440.png') });
    pruefe('Wandaufbau: Three.js lädt bei Annäherung, Canvas vorhanden, auf großen Bildschirmen an den Scroll gekoppelt, Schritt per Knopf wählbar',
      dreiD.klasse.includes('ist-3d') && dreiD.canvas && st && gedrueckt === 'true' && !fehler.length, { dreiD, st, gedrueckt, fehler });
    await p.close();
  }
  {
    const b2 = await chromium.launch({ ...STARTOPTIONEN, args: ['--disable-webgl', '--disable-3d-apis'] });
    const p = await b2.newPage({ viewport: { width: 390, height: 844 } });
    await p.goto(haupt.basis, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.querySelector('#wandaufbau').scrollIntoView());
    await p.waitForTimeout(1500);
    const rueckfall = await p.isVisible('.wandaufbau-rueckfall svg');
    const kein3d = await p.evaluate(() => !document.querySelector('#wandaufbau').classList.contains('ist-3d') && !document.querySelector('.wandaufbau-canvas'));
    await p.click('.wandaufbau-schritt[data-schritt="1"]');
    await p.waitForTimeout(700);   // Übergang der Ebenen (0,45 s)
    const schritt = await p.getAttribute('#wandaufbau', 'data-schritt');
    const gedimmt = await p.evaluate(() => getComputedStyle(document.querySelector('.ex-4')).opacity);
    pruefe('Ohne WebGL: Zeichnung als Rückfall, Schritte steuern die Ebenen der Zeichnung', rueckfall && kein3d && schritt === '1' && parseFloat(gedimmt) < .5, { rueckfall, kein3d, schritt, gedimmt });
    await b2.close();
  }

  // ---------------------------------------------------------------- Formular: Vorauswahl, Rückruf, Fotos
  {
    const p = await browser.newPage({ viewport: { width: 1024, height: 900 } });
    await p.goto(haupt.basis + 'kontakt/?leistung=reparatur&anliegen=T%C3%BCr+schleift#anfrage', { waitUntil: 'networkidle' });
    const leistung = await p.inputValue('#f-leistung');
    const text = await p.inputValue('#f-nachricht');
    pruefe('Alltagsfall-Link füllt Leistung und Anliegen vor', leistung === 'Reparatur & Instandhaltung' && text.startsWith('Tür schleift'), { leistung, text });
    const zeitVorher = await p.isVisible('#f-rueckrufzeit');
    await p.check('#f-rueckruf');
    const zeitNachher = await p.isVisible('#f-rueckrufzeit');
    await p.fill('#f-name', 'Rolf Rückruf');
    await p.fill('#f-email', 'rolf@test.invalid');
    await p.fill('#f-nachricht', 'Tür schleift: Die Wohnungstür schleift unten am Boden.');
    await p.click('button[type=submit]');
    const telFehler = await p.textContent('#f-telefon-fehler');
    pruefe('Rückruf: Zeitfenster erscheint erst bei Wunsch, ohne Telefonnummer klarer Fehler', !zeitVorher && zeitNachher && /Telefonnummer/.test(telFehler), { zeitVorher, zeitNachher, telFehler });
    await p.fill('#f-telefon', '0123 456789');
    await p.selectOption('#f-rueckrufzeit', 'Nachmittags (14–18 Uhr)');
    await p.setInputFiles('#f-fotos', { name: 'tuer.png', mimeType: 'image/png', buffer: png() });
    const liste = await p.textContent('[data-dateiliste]');
    await p.waitForTimeout(3200);
    const bekannt = new Set(post(POST));
    await Promise.all([p.waitForURL(/kontakt\/danke\/\?ref=/, { timeout: 15000 }), p.click('button[type=submit]')]);
    const neu = post(POST).filter(f => !bekannt.has(f));
    const mail = neu.length ? readFileSync(join(POST, neu[neu.length - 1]), 'utf8') : '';
    pruefe('Anfrage mit Rückrufwunsch und Foto: Danke-Seite, Nachricht mit Zeitfenster und Bildanhang',
      /tuer\.png/.test(liste) && /Rückruf:\s+erwünscht, Nachmittags/.test(mail) && /Content-Type: image\/png; name="foto-1\.png"/.test(mail), { liste, laenge: mail.length });
    await p.close();
  }

  // ---------------------------------------------------------------- Vorschau: Kundenansicht
  {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(vors.basis + 'leistungen/', { waitUntil: 'networkidle' });
    const vorher = await p.locator('.redaktion').first().isVisible();
    await p.click('[data-kundenansicht]');
    const nachher = await p.locator('.redaktion').first().isVisible();
    const gedrueckt = await p.getAttribute('[data-kundenansicht]', 'aria-pressed');
    await p.reload({ waitUntil: 'networkidle' });
    const gemerkt = !(await p.locator('.redaktion').first().isVisible());
    pruefe('Vorschau: „Kundenansicht“ blendet Redaktionshinweise aus und bleibt beim Seitenwechsel erhalten', vorher && !nachher && gedrueckt === 'true' && gemerkt, { vorher, nachher, gedrueckt, gemerkt });
    await p.close();
  }

  // ---------------------------------------------------------------- Galerie (Entwurfs-Build)
  {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(entw.basis + 'projekte/', { waitUntil: 'networkidle' });
    const karten = await p.locator('.projekt').count();
    const abzeichen = await p.locator('.abzeichen').count();
    pruefe('Projektübersicht (Entwurfs-Build): Karten mit Kennzeichnung „Beispieldaten“', karten === 4 && abzeichen === 4, { karten, abzeichen });
    await p.click('.filter label:has(input[value="reparatur"])');
    await p.waitForTimeout(1200);
    const sichtbarNach = await p.evaluate(() => [...document.querySelectorAll('[data-projekt]')].filter(k => k.offsetParent !== null).map(k => k.dataset.kategorie));
    const ansage = await p.textContent('#filter-ansage');
    await p.click('.filter label:has(input[value="alle"])');
    await p.waitForTimeout(1200);
    const alle = await p.evaluate(() => [...document.querySelectorAll('[data-projekt]')].filter(k => k.offsetParent !== null && getComputedStyle(k).opacity === '1').length);
    pruefe('Projektfilter (Flip): filtert nach Leistung, sagt das Ergebnis an und stellt alle wieder her',
      sichtbarNach.length === 1 && sichtbarNach[0] === 'reparatur' && /1 Projekt/.test(ansage) && alle === 4, { sichtbarNach, ansage, alle });
    await p.goto(entw.basis + 'projekte/beispiel-trennwand-arbeitszimmer/', { waitUntil: 'networkidle' });
    await p.locator('.vergleich-regler').fill('20');
    const pos = await p.evaluate(() => getComputedStyle(document.querySelector('.vergleich-buehne')).getPropertyValue('--pos').trim());
    pruefe('Vorher/Nachher: Regler steuert den Bildausschnitt', pos === '20%', pos);
    const ausloeser = p.locator('[data-gross]').first();
    await ausloeser.focus(); await p.keyboard.press('Enter');
    const offen = await p.evaluate(() => document.querySelector('.bildansicht').open);
    await p.keyboard.press('ArrowRight');
    const zaehler = await p.textContent('.bildansicht .zaehler');
    await p.keyboard.press('Escape');
    const zu = await p.evaluate(() => !document.querySelector('.bildansicht').open);
    const fokus = await p.evaluate(() => document.activeElement.hasAttribute('data-gross'));
    pruefe('Bildansicht: per Tastatur öffnen, blättern, mit Escape schließen, Fokus zurück', offen && zaehler === '2 / 2' && zu && fokus, { offen, zaehler, zu, fokus });
    await durchscrollen(p);
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.screenshot({ path: join(BERICHT, 'projekt-detail-1280.png'), fullPage: true });
    await p.close();
  }
} finally {
  await browser.close();
  haupt.proc.kill(); entw.proc.kill(); vors.proc.kill();
}

const ok = ergebnisse.filter(e => e.ok).length;
for (const e of ergebnisse) console.log(`  ${e.ok ? '✓' : '✗'} ${e.name}${e.ok || !e.detail ? '' : '  → ' + (typeof e.detail === 'string' ? e.detail : JSON.stringify(e.detail))}`);
for (const e of ergebnisse.filter(e => e.ok && e.detail && /zur Kenntnis/.test(e.name))) console.log('    ' + e.detail);
console.log(`\n${ok} bestanden, ${ergebnisse.length - ok} fehlgeschlagen · Bilder und axe-Berichte: ${BERICHT}`);
process.exit(ok === ergebnisse.length ? 0 : 1);
