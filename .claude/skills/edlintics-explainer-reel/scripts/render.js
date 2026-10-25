// Usage: node render.js stills 1.2,5,9   -> PNG stills in out/
//        node render.js video out.mp4 audio.wav  -> MP4 via bundled ffmpeg
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const puppeteer = require('puppeteer-core');
const D = __dirname;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const FF = process.env.FFMPEG; // path to ffmpeg (imageio-ffmpeg binary)
const FPS = 24;
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => {
  const f = path.join(D, decodeURIComponent(q.url.split('?')[0]));
  if (!f.startsWith(D) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const port = srv.address().port;
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${port}/render.html`, { waitUntil: 'networkidle0' });
  const dur = await p.evaluate(() => window.init());
  const mode = process.argv[2];
  if (mode === 'stills') {
    fs.mkdirSync(path.join(D, 'out'), { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) {
      await p.evaluate(t => window.render(t), t);
      await p.screenshot({ path: path.join(D, 'out', `still-${t}.png`) });
    }
  } else {
    const out = process.argv[3], audio = process.argv[4];
    const ff = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', audio,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', String(FPS),
      '-c:a', 'aac', '-ar', '48000', '-b:a', '160k', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'ignore', 'pipe'] });
    let err = ''; ff.stderr.on('data', d => err = (err + d).slice(-2000));
    const N = Math.ceil(dur * FPS);
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
