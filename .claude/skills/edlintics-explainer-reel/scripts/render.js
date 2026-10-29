// Usage: node render.js stills 1.2,5,9   -> PNG stills in out/
//        node render.js video out.mp4 audio.wav  -> MP4 via bundled ffmpeg
//        CLEAN=1 node render.js clips <outdir>   -> one silent MP4 per beat (frame-exact cuts), art only when CLEAN=1
//        node render.js cardparts <outdir>       -> transparent PNGs of the end-card layers (term, kp, rule, fn, logo, all)
//        CLEAN=1 hides captions, logo and the end-card text (editable ads, 29 Oct 2026); FPS stays 24
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const puppeteer = require('puppeteer-core');
const D = __dirname;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const FF = process.env.FFMPEG; // path to ffmpeg (imageio-ffmpeg binary)
const FPS = 24;
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.js': 'text/javascript' };
const SCENES = process.env.SCENES; // optional: a work folder's scenes.json (lets several reels build at once)
const OUT = process.env.OUT || path.join(D, 'out');
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]);
  const f = (u === '/scenes.json' && SCENES) ? SCENES : path.join(D, u);
  if ((!f.startsWith(D) && f !== SCENES) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const port = srv.address().port;
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${port}/render.html`, { waitUntil: 'networkidle0' });
  const dur = await p.evaluate(clean => { return (async () => { const d = await window.init(); if (clean) document.body.classList.add('clean'); return d; })(); }, process.env.CLEAN === '1');
  const mode = process.argv[2];
  const encode = (out, audio) => {
    const a = audio ? ['-i', audio] : [];
    const ff = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...a,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', String(FPS),
      ...(audio ? ['-c:a', 'aac', '-ar', '48000', '-b:a', '160k'] : ['-an']), '-movflags', '+faststart', ...(audio ? ['-shortest'] : []), out], { stdio: ['pipe', 'ignore', 'pipe'] });
    let err = ''; ff.stderr.on('data', d => err = (err + d).slice(-2000));
    return { ff, done: () => new Promise(ok => ff.on('close', c => { if (c) console.log('ffmpeg exit', c, err); ok(); })) };
  };
  const frame = async (k, enc) => { await p.evaluate(t => window.render(t), k / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!enc.ff.stdin.write(buf)) await new Promise(ok => enc.ff.stdin.once('drain', ok)); };
  if (mode === 'stills') {
    fs.mkdirSync(OUT, { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) {
      await p.evaluate(t => window.render(t), t);
      await p.screenshot({ path: path.join(OUT, `still-${t}.png`) });
    }
  } else if (mode === 'clips') {
    // one clip per beat, cut on the same integer frames as the full video (beat i owns the frames where beatAt() picks it)
    const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
    const beats = await p.evaluate(() => D.beats.map((b, k) => ({ role: b.role, img: b.img || 'endcard', a: k === 0 ? 0 : b.start - 0.08 })));
    const N = Math.ceil(dur * FPS), list = [];
    for (let i = 0; i < beats.length; i++) {
      const k0 = i === 0 ? 0 : Math.ceil(beats[i].a * FPS - 1e-6), k1 = i + 1 < beats.length ? Math.ceil(beats[i + 1].a * FPS - 1e-6) : N;
      const name = `clip-${String(i + 1).padStart(2, '0')}-${beats[i].img}.mp4`, enc = encode(path.join(out, name));
      for (let k = k0; k < k1; k++) await frame(k, enc);
      enc.ff.stdin.end(); await enc.done();
      list.push({ n: i + 1, file: name, role: beats[i].role, img: beats[i].img, start: +(k0 / FPS).toFixed(4), end: +(k1 / FPS).toFixed(4), frames: k1 - k0 });
      console.log('clip', name, k0, '->', k1, ((k1 - k0) / FPS).toFixed(3), 's');
    }
    fs.writeFileSync(path.join(out, 'clips.json'), JSON.stringify({ fps: FPS, duration: dur, clips: list }, null, 1));
  } else if (mode === 'cardparts') {
    const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
    for (const part of ['term', 'kp', 'rule', 'fn', 'logo', 'cta', 'all']) {
      const r = await p.evaluate(pt => window.cardPart(pt), part);
      if (r.w < 10 || r.h < 10) continue;
      await p.screenshot({ path: path.join(out, `endcard-${part}.png`), omitBackground: true, clip: { x: r.x, y: r.y, width: r.w, height: r.h } });
      console.log('part', part, JSON.stringify(r));
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
