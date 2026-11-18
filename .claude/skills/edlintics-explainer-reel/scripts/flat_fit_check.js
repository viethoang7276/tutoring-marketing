// Flat-style fit check (18 Nov 2026; Hoang, on the flat reels: "avoid spill over text over box like the video above").
// Usage: SCENES=<work>/scenes.json node flat_fit_check.js <work> [step=0.25]   (make_reel.sh runs it for meta.style "flat"; run it through tools/render-slot.sh)
// Samples the real renderer every `step` s and, with the browser's own text and box geometry (render.html fitReport), reports:
//   text-spill  a text runs outside its own card or pill, or keeps less than 20 px (cards) / 12 px (pills) to its edge
//   overlap     two cards, pills or loose labels of different items overlap, or one crosses a board's posts or edge
//   edge        a card, pill or label is cut by the frame edge while it is held still (camera moves and pop-ins are allowed)
//   ledger      a card or label covers Ledger's body; caption: it runs under the caption pill; logo: it touches the logo pill (6 px)
// Only items that are still (the same box 0.125 s before and after) are judged. Writes <work>/fitcheck.json; exit 1 on any finding
// (FLAT_FIT=warn prints them and exits 0).
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const D = __dirname, CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const W = process.argv[2], STEP = +(process.argv[3] || 0.25), SCENES = process.env.SCENES || path.join(W, 'scenes.json');
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]);
  const f = u === '/scenes.json' ? SCENES : path.join(D, u);
  if ((!f.startsWith(D) && f !== SCENES) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${srv.address().port}/render.html`, { waitUntil: 'networkidle0' });
  const dur = await p.evaluate(() => window.init());
  if (!(await p.evaluate(() => !!D.flat))) {
    if (process.env.FIT_ANY !== '1') { console.log('flat fit check: not a flat script, skipped'); await b.close(); srv.close(); return; }
    // FIT_ANY=1 (18 Nov 2026): a paper script with boxed props (paper_card, paper_tag, paper_sentence, sd_graph carry data-fb). The texts are
    // assigned to their boxes on every rendered frame (pop-ins scale), without the flat auto-shrink, so a spill in the real paper render is reported
    await p.evaluate(() => { const r0 = window.render; window.render = t => { r0(t); fitAssign(); }; });
  }
  const runs = new Map();   // one entry per (kind, a, b), with its time ranges
  for (let t = STEP; t < dur - 0.05; t += STEP) {
    const F = await p.evaluate((t) => window.fitReport(t), +t.toFixed(3));
    for (const f of F) {
      const k = `${f.kind}|${f.a}|${f.b || ''}`; if (!runs.has(k)) runs.set(k, { ...f, spans: [] });
      const R = runs.get(k), last = R.spans[R.spans.length - 1];
      if (last && t - last[1] <= STEP * 1.5) last[1] = +t.toFixed(2); else R.spans.push([+t.toFixed(2), +t.toFixed(2)]);
    }
  }
  await b.close(); srv.close();
  const out = [...runs.values()].sort((x, y) => x.spans[0][0] - y.spans[0][0]);
  fs.writeFileSync(path.join(W, 'fitcheck.json'), JSON.stringify(out, null, 1));
  const WARN = process.env.FLAT_FIT === 'warn';
  for (const f of out) console.log(`${WARN ? 'WARN' : 'FAIL'}  ${f.kind}: ${f.a}${f.b ? '  x  ' + f.b : ''}  at ${f.spans.map(s => s[0] === s[1] ? `${s[0]}s` : `${s[0]}-${s[1]}s`).join(', ')}  box ${JSON.stringify(f.box)}`);
  console.log(`FLAT FIT ${out.length ? (WARN ? 'WARN' : 'NOT OK') : 'OK'}: ${out.length} finding(s), sampled every ${STEP} s over ${dur.toFixed(1)} s`);
  process.exit(out.length && !WARN ? 1 : 0);
})();
