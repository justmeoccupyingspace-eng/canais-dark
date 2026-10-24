// uso: node scripts/lab_stills.mjs '<json props m>' out_prefix frame1 frame2 ...
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
const m = JSON.parse(process.argv[2]);
const pre = process.argv[3];
const frames = process.argv.slice(4).map(Number);
const serveUrl = await bundle({entryPoint: '/home/claude/canais-dark/src/index.jsx', publicDir: '/home/claude/canais-dark/public'});
const browserExecutable = process.env.CHROME_PATH;
const chromiumOptions = {gl: 'angle'};
const composition = await selectComposition({serveUrl, id: 'Lab', inputProps: {m}, browserExecutable, chromiumOptions});
for (const f of frames) await renderStill({composition, serveUrl, frame: f, output: `${pre}_${f}.png`, inputProps: {m}, browserExecutable, chromiumOptions, scale: 0.5});
console.log('ok');
