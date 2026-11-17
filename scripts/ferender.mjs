// Render dos vídeos de oração / histórias bíblicas.
//   node scripts/ferender.mjs <fe.json> video <out.mp4> [chunk nchunks]   (mudo)
//   node scripts/ferender.mjs <fe.json> stills <prefix> <t1,t2,...> [scale]
//   node scripts/ferender.mjs <fe.json> thumb <out.jpg>
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const [specPath, mode, ...rest] = process.argv.slice(2);
const fe = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
process.on('exit', () => { try { if (serveUrl.includes('remotion-webpack-bundle')) fs.rmSync(serveUrl, {recursive: true, force: true}); } catch {} });
const browserExecutable = process.env.CHROME_PATH || undefined;
const chromiumOptions = {gl: 'angle'};
const inputProps = {fe};
const t0 = Date.now();
if (mode === 'thumb') {
  const c = await selectComposition({serveUrl, id: 'FeThumb', inputProps, browserExecutable, chromiumOptions});
  await renderStill({composition: c, serveUrl, frame: 0, output: rest[0], imageFormat: 'jpeg', jpegQuality: 92, inputProps, browserExecutable, chromiumOptions});
  console.log('thumb ok');
} else {
  const composition = await selectComposition({serveUrl, id: 'Fe', inputProps, browserExecutable, chromiumOptions});
  const N = composition.durationInFrames;
  if (mode === 'video') {
    const [out, ci, nc] = [rest[0], Number(rest[1] || 0), Number(rest[2] || 1)];
    const a = Math.floor((N * ci) / nc), b = Math.floor((N * (ci + 1)) / nc) - 1;
    await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps, browserExecutable, chromiumOptions, frameRange: [a, b], muted: true, crf: 20,
      concurrency: Math.min(Number(process.env.CONC || 4), (await import('node:os')).cpus().length), x264Preset: 'veryfast'});
    console.log(`video ${ci}/${nc} frames ${a}-${b} em ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  } else if (mode === 'stills') {
    const ts = rest[1].split(',').map(Number);
    for (const t of ts) {
      await renderStill({composition, serveUrl, frame: Math.min(N - 1, Math.round(t * 30)), output: `${rest[0]}_${String(t).replace('.', '_')}.jpg`, imageFormat: 'jpeg', jpegQuality: 85, inputProps, browserExecutable, chromiumOptions, scale: Number(rest[2] || 0.5)});
    }
    console.log('stills ok', ts.length);
  }
}
