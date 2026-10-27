// Vídeo longo. uso:
//   node scripts/lrender.mjs <timeline.json> video <chunk> <nchunks> <out.mp4>   (pedaço mudo)
//   node scripts/lrender.mjs <timeline.json> audio <out.wav>                       (só áudio)
//   node scripts/lrender.mjs <timeline.json> stills <prefix> <t1,t2,...> [scale]  (quadros em segundos)
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const [specPath, mode, ...rest] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
const browserExecutable = process.env.CHROME_PATH || undefined;
const chromiumOptions = {gl: 'angle'};
const inputProps = {spec};
const composition = await selectComposition({serveUrl, id: 'Long', inputProps, browserExecutable, chromiumOptions});
const N = composition.durationInFrames;
const t0 = Date.now();
if (mode === 'video') {
  const [ci, nc, out] = [Number(rest[0]), Number(rest[1]), rest[2]];
  const a = Math.floor((N * ci) / nc), b = Math.floor((N * (ci + 1)) / nc) - 1;
  await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps, browserExecutable, chromiumOptions, frameRange: [a, b], muted: true, crf: 19,
    concurrency: Number(process.env.CONC || 3), x264Preset: 'medium', onProgress: ({progress}) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`\r${Math.round(progress * 100)}%`); }});
  console.log(`\nchunk ${ci}/${nc} frames ${a}-${b} em ${((Date.now() - t0) / 1000).toFixed(0)}s`);
} else if (mode === 'audio') {
  await renderMedia({composition, serveUrl, codec: 'wav', outputLocation: rest[0], inputProps, browserExecutable, chromiumOptions});
  console.log('audio ok', N, 'frames');
} else if (mode === 'stills') {
  const pre = rest[0];
  const ts = rest[1].split(',').map(Number);
  const scale = Number(rest[2] || 0.5);
  for (const t of ts) {
    const fr = Math.min(N - 1, Math.round(t * 30));
    await renderStill({composition, serveUrl, frame: fr, output: `${pre}_${String(t).replace('.', '_')}.jpg`, imageFormat: 'jpeg', jpegQuality: 85, inputProps, browserExecutable, chromiumOptions, scale});
  }
  console.log('stills ok', ts.length, 'em', ((Date.now() - t0) / 1000).toFixed(0), 's');
}
