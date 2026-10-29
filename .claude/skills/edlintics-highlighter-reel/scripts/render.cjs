// .cjs because the repo package.json sets "type": "module"
// Highlighter reel renderer (copied from the puzzle reel: headless Chrome, 24 fps, frames piped to ffmpeg).
// Usage: TIMELINE=<work>/timeline.json FFMPEG=<ffmpeg> node render.cjs stills 1.2,5,9 <outdir>
//        TIMELINE=... FFMPEG=... node render.cjs video <out.mp4> <audio.wav>
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const puppeteer = require('puppeteer-core');   // resolved via NODE_PATH (explainer-reel scripts/node_modules)
const D = __dirname, FPS = 24;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const FF = process.env.FFMPEG, TL = process.env.TIMELINE;
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]);
  const f = u === '/timeline.json' ? TL : path.join(D, u);
  if ((f !== TL && !f.startsWith(D)) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  p.on('pageerror', e => console.error('page error:', e.message));
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${srv.address().port}/render.html`, { waitUntil: 'networkidle0' });
  const dur = await p.evaluate(() => window.init());
  if (process.argv[2] === 'stills') {
    const out = process.argv[4]; fs.mkdirSync(out, { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) {
      await p.evaluate(t => window.render(t), t);
      await p.screenshot({ path: path.join(out, `still-${t.toFixed(2)}.png`) });
    }
  } else {
    const out = process.argv[3], audio = process.argv[4];
    const ff = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', audio,
      '-vf', 'scale=in_range=pc:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-tune', 'animation',
      '-pix_fmt', 'yuv420p', '-r', String(FPS), '-c:a', 'aac', '-ar', '48000', '-b:a', '160k', '-movflags', '+faststart', '-shortest', out],
      { stdio: ['pipe', 'ignore', 'pipe'] });
    let err = ''; ff.stderr.on('data', d => err = (err + d).slice(-2000));
    const N = Math.round(dur * FPS);
    for (let k = 0; k < N; k++) {
      await p.evaluate(t => window.render(t), k / FPS);
      const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(ok => ff.stdin.once('drain', ok));
      if (k % 120 === 0) console.log('frame', k, '/', N);
    }
    ff.stdin.end();
    await new Promise(ok => ff.on('close', c => { console.log('ffmpeg exit', c); if (c) console.log(err); ok(); }));
  }
  await b.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
