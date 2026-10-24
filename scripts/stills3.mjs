// uso: node scripts/stills3.mjs spec.json out_prefix f1 f2 ...  (gl angle, escala 0.5)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const pre = process.argv[3];
const frames = process.argv.slice(4).map(Number);
const serveUrl = await bundle({entryPoint: '/home/claude/canais-dark/src/index.jsx', publicDir: '/home/claude/canais-dark/public'});
const browserExecutable = process.env.CHROME_PATH;
const chromiumOptions = {gl: 'angle'};
const composition = await selectComposition({serveUrl, id: 'Short', inputProps: {spec}, browserExecutable, chromiumOptions});
for (const f of frames) await renderStill({composition, serveUrl, frame: f, output: `${pre}_${f}.png`, inputProps: {spec}, browserExecutable, chromiumOptions, scale: 0.5});
console.log('ok', composition.durationInFrames);
