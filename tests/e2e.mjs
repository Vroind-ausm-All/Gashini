// Browser-Tests für den Webauftritt.
//   cd tests && npm ci && node e2e.mjs
// Voraussetzungen: PHP ≥ 8.1, Chromium (Pfad über CHROMIUM_PFAD, sonst Playwright-Standard).
// Baut dist/web (Vorschau) und einen Entwurfs-Build mit Beispielprojekten, startet
// php -S mit einer Test-Konfiguration (Mails werden als Datei abgelegt) und prüft
// Darstellung, Bedienung, Barrierefreiheit und Formularstrecke.
import { chromium } from 'playwright';
import { spawn, execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readdirSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
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
  const proc = spawn('php', ['-S', `127.0.0.1:${port}`, '-t', wurzel], { env: { ...process.env, GASHINI_KONFIG: konfig }, stdio: 'ignore' });
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

const POST = join(TMP, 'post');
const haupt = await phpServer(join(WURZEL, 'dist/web'), testKonfig('haupt', POST));
const entw = await phpServer(entwurf, testKonfig('entwurf', join(TMP, 'post2')));
const browser = await chromium.launch(process.env.CHROMIUM_PFAD ? { executablePath: process.env.CHROMIUM_PFAD } : {});

const SEITEN = ['', 'leistungen/', 'leistungen/trockenbau/', 'leistungen/hausmeisterservice/', 'leistungen/reparatur-und-instandhaltung/',
  'projekte/', 'ueber-uns/', 'ablauf/', 'kontakt/', 'kontakt/danke/', 'impressum/', 'datenschutz/', '404.html'];
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
    pruefe('Ohne JavaScript: Inhalt und Navigation sichtbar', h1 && navLink);
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
    const anim = await p.evaluate(() => [...document.querySelectorAll('.zg-zeichnen, .zg-einblenden')].map(e => getComputedStyle(e).animationName));
    const deckend = await p.evaluate(() => [...document.querySelectorAll('.zg-einblenden')].every(e => getComputedStyle(e).opacity === '1'));
    pruefe('Bewegung reduzieren: Zeichnung ohne Animation und sofort vollständig sichtbar', anim.every(a => a === 'none') && deckend, anim.slice(0, 3));
    await ctx.close();
  }

  // ---------------------------------------------------------------- Galerie (Entwurfs-Build)
  {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(entw.basis + 'projekte/', { waitUntil: 'networkidle' });
    const karten = await p.locator('.projekt').count();
    const abzeichen = await p.locator('.abzeichen').count();
    pruefe('Projektübersicht (Entwurfs-Build): Karten mit Kennzeichnung „Beispieldaten“', karten === 3 && abzeichen === 3, { karten, abzeichen });
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
    await p.screenshot({ path: join(BERICHT, 'projekt-detail-1280.png'), fullPage: true });
    await p.close();
  }
} finally {
  await browser.close();
  haupt.proc.kill(); entw.proc.kill();
}

const ok = ergebnisse.filter(e => e.ok).length;
for (const e of ergebnisse) console.log(`  ${e.ok ? '✓' : '✗'} ${e.name}${e.ok || !e.detail ? '' : '  → ' + (typeof e.detail === 'string' ? e.detail : JSON.stringify(e.detail))}`);
for (const e of ergebnisse.filter(e => e.ok && e.detail && /zur Kenntnis/.test(e.name))) console.log('    ' + e.detail);
console.log(`\n${ok} bestanden, ${ergebnisse.length - ok} fehlgeschlagen · Bilder und axe-Berichte: ${BERICHT}`);
process.exit(ok === ergebnisse.length ? 0 : 1);
