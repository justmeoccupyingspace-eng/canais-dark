// uso: node scripts/render.mjs specs/<arquivo>.json out/<arquivo>.mp4
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [specPath, outPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.jsx'), publicDir: path.join(root, 'public')});
const inputProps = {spec};
const browserExecutable = process.env.CHROME_PATH || undefined;
const composition = await selectComposition({serveUrl, id: 'Short', inputProps, browserExecutable});
await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: outPath, inputProps, browserExecutable, concurrency: 2});
console.log('ok', outPath, composition.durationInFrames / composition.fps + 's');
