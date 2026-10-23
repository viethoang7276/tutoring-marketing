// Render the traveling-Ledger scene to JPEG frames with headless Chrome (no installs:
// Node 22's built-in WebSocket talks to Chrome's DevTools protocol).
//   node motion/traveling-ledger/render.mjs <outDir> [fps]
// Writes <outDir>/panel-<n>/ (one clip per carousel slide, starting as Ledger enters it)
// and <outDir>/reel/ (camera follows Ledger). Encode with encode.swift.
import { spawn } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] || 'assets/renders/traveling-ledger');
const fps = Number(process.argv[3] || 30);
const port = 9333;
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', `--remote-debugging-port=${port}`, '--hide-scrollbars', '--disable-gpu',
  '--allow-file-access-from-files', '--window-size=1080,1350', `--user-data-dir=${join(out, '.chrome')}`, 'about:blank',
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
let targets;
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); if (targets.length) break; } catch {}
  await sleep(200);
}
const page = targets.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pending = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails)); return r.result?.result?.value; };

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1080, height: 1350, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: 'file://' + join(here, 'index.html') });
await sleep(1500);
await evaluate('READY');
const logo = readFileSync(join(here, '../../assets/brand/edlintics-logo.svg'), 'utf8');
await evaluate(`loadLogo(${JSON.stringify(logo)})`);
const meta = await evaluate('META');
console.log('scene', meta);

async function shoot(dir, t0, t1, mode, panel) {
  mkdirSync(dir, { recursive: true });
  const n = Math.ceil((t1 - t0) * fps);
  for (let f = 0; f < n; f++) {
    await evaluate(`render(${t0 + f / fps}, '${mode}', ${panel})`);
    const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92, clip: { x: 0, y: 0, width: 1080, height: 1350, scale: 1 } });
    writeFileSync(join(dir, `f${String(f).padStart(5, '0')}.jpg`), Buffer.from(r.result.data, 'base64'));
  }
  console.log(dir, n, 'frames');
}

const only = process.env.ONLY; // e.g. ONLY=still to render a preview frame per panel
if (only === 'still') {
  for (let i = 0; i < meta.panels; i++) {
    const [a, b] = await evaluate(`panelWindow(${i})`);
    await shoot(join(out, 'stills', `p${i}`), (a + b) / 2, (a + b) / 2 + 1 / fps, 'panel', i);
  }
} else {
  for (let i = 0; i < meta.panels; i++) {
    const [a, b] = await evaluate(`panelWindow(${i})`);
    await shoot(join(out, `panel-${i + 1}`), Math.max(0, a), b, 'panel', i);
  }
  await shoot(join(out, 'reel'), 0, meta.duration, 'follow', 0);
}
ws.close(); chrome.kill();
