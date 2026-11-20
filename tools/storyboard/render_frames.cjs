// Renders a folder of numbered SVG frames (000000.svg ...) with one headless Chrome page.
//   node render_frames.cjs png <framesDir>                 -> a PNG next to each SVG
//   node render_frames.cjs video <framesDir> <out.mp4> <fps> [audio.wav]
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const puppeteer = require(path.join(__dirname, '../../.claude/skills/edlintics-explainer-reel/scripts/node_modules/puppeteer-core'));
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  const [mode, dir, out, fps, audio] = process.argv.slice(2);
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.setContent('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden}svg{display:block}</style><div id="s"></div>');
  const show = async f => p.evaluate(async svg => { document.getElementById('s').innerHTML = svg;
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, fs.readFileSync(path.join(dir, f), 'utf8'));
  if (mode === 'png') {
    for (const f of files) { await show(f); await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) }); }
  } else {
    const a = audio ? ['-i', audio] : [];
    const ff = spawn(process.env.FFMPEG, ['-y', '-f', 'image2pipe', '-framerate', fps, '-c:v', 'mjpeg', '-i', '-', ...a,
      '-vf', 'scale=in_range=pc:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', fps,
      ...(audio ? ['-c:a', 'aac', '-ar', '48000', '-b:a', '160k'] : ['-an']), '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'pipe'] });
    let err = ''; ff.stderr.on('data', d => err = (err + d).slice(-2000));
    const done = new Promise(ok => ff.on('close', c => { if (c) console.log('ffmpeg exit', c, err); ok(); }));
    let k = 0;
    for (const f of files) { await show(f); const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
      if (!ff.stdin.write(buf)) await new Promise(ok => ff.stdin.once('drain', ok));
      if (++k % 150 === 0) console.log('frame', k, '/', files.length); }
    ff.stdin.end(); await done;
  }
  await b.close();
})();
