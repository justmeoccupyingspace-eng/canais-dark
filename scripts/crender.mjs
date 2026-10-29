// Renderiza um corte vertical. uso: node scripts/crender.mjs <props.json> <out.mp4> [still.jpg segundos]
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const [propsPath, out, stillOut, stillT] = process.argv.slice(2);
const inputProps = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
const browserExecutable = process.env.CHROME_PATH || undefined;
const chromiumOptions = {gl: 'angle'};
const composition = await selectComposition({serveUrl, id: 'Clip', inputProps, browserExecutable, chromiumOptions});
const t0 = Date.now();
if (out && out !== '-') {
  await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps, browserExecutable, chromiumOptions, crf: 20,
    concurrency: Math.min(Number(process.env.CONC || 3), (await import('node:os')).cpus().length), x264Preset: 'medium'});
  console.log('corte ok', out, composition.durationInFrames, 'frames em', ((Date.now() - t0) / 1000).toFixed(0), 's');
}
if (stillOut) {
  await renderStill({composition, serveUrl, frame: Math.round(Number(stillT || 3) * 30), output: stillOut, imageFormat: 'jpeg', jpegQuality: 85, inputProps, browserExecutable, chromiumOptions, scale: 0.5});
  console.log('still ok', stillOut);
}
