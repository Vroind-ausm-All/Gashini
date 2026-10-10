// Bündelt das Wandaufbau-Modell (Three.js) und kopiert GSAP nach src/assets/js/.
// Das Ergebnis wird eingecheckt – die Website selbst baut ohne Node (scripts/build-site.py).
//   npm ci && npm run bauen
import { build } from 'esbuild';
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = dirname(fileURLToPath(import.meta.url));
const JS = join(HIER, '../../../src/assets/js');
const VENDOR = join(JS, 'vendor');
mkdirSync(VENDOR, { recursive: true });

const three = JSON.parse(readFileSync(join(HIER, 'node_modules/three/package.json'), 'utf8')).version;
const gsap = JSON.parse(readFileSync(join(HIER, 'node_modules/gsap/package.json'), 'utf8')).version;

await build({
  entryPoints: [join(HIER, 'quelle/einbindung.js')],
  outfile: join(JS, 'wandaufbau.js'),
  bundle: true, format: 'esm', minify: true, target: 'es2020', legalComments: 'none',
  banner: { js: `/* Generiert durch scripts/werkzeuge/3d (npm run bauen) – nicht von Hand ändern.\n   Enthält three.js ${three} (MIT-Lizenz, Copyright 2010-2026 three.js authors, https://threejs.org). */` },
});

const PLUGINS = ['gsap', 'ScrollTrigger', 'SplitText', 'DrawSVGPlugin', 'Flip'];
for (const p of PLUGINS) copyFileSync(join(HIER, 'node_modules/gsap/dist', p + '.min.js'), join(VENDOR, p + '.min.js'));
writeFileSync(join(VENDOR, 'LIZENZEN.txt'), `Fremdbibliotheken in diesem Verzeichnis
=======================================

GSAP ${gsap} (${PLUGINS.join(', ')})
  Copyright (c) 2008-2026, GreenSock. All rights reserved.
  Lizenz: GSAP Standard "No Charge" License – https://gsap.com/standard-license
  Kostenlose Nutzung auch auf kommerziellen Websites; nicht für Werkzeuge,
  die mit Webflow konkurrieren. Die Dateien bleiben unverändert.

three.js ${three} – gebündelt in ../wandaufbau.js
  MIT-Lizenz, Copyright 2010-2026 three.js authors – https://github.com/mrdoob/three.js/blob/dev/LICENSE

Aktualisieren: scripts/werkzeuge/3d/package.json anpassen, dann
  cd scripts/werkzeuge/3d && npm install && npm run bauen
`);
console.log(`wandaufbau.js (three ${three}) und GSAP ${gsap} nach src/assets/js/ geschrieben`);
