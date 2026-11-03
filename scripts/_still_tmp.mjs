import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const [specPath, outDir, ...times] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
const browserExecutable = process.env.CHROME_PATH;
const chromiumOptions = {gl: 'angle'};
const inputProps = {spec};
const c = await selectComposition({serveUrl, id: 'Long', inputProps, browserExecutable, chromiumOptions});
for (const t of times) {
  const out = `${outDir}/st_${t}.jpg`;
  await renderStill({composition: c, serveUrl, frame: Math.round(+t * 30), output: out, imageFormat: 'jpeg', jpegQuality: 80, inputProps, browserExecutable, chromiumOptions, scale: 0.5});
  console.log('ok', out);
}
