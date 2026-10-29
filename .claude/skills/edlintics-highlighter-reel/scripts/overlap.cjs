// Ledger overlap check for a highlighter reel (29 Oct 2026). For every frame (default 12 per second) it measures, in screen
// pixels, Ledger and his coin pile against: every <text> on the sheet, the chart curve, the hand with the highlighter, and the
// caption band (y 1425-1565). It prints each clash with its time and exits 1 if there is any.
// Usage: TIMELINE=<work>/timeline.json NODE_PATH=<explainer scripts/node_modules> node overlap.cjs [fps=12]
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const D = __dirname, CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', TL = process.env.TIMELINE;
const FPS = Number(process.argv[2] || 12);
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]); const f = u === '/timeline.json' ? TL : path.join(D, u);
  if ((f !== TL && !f.startsWith(D)) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${srv.address().port}/render.html`, { waitUntil: 'networkidle0' });
  const dur = await p.evaluate(() => window.init());
  const hasLedger = await p.evaluate(() => !!document.querySelector('#ledger').firstChild);
  if (!hasLedger) { console.log('no Ledger in this reel; nothing to check'); await b.close(); srv.close(); return; }
  const bad = [];
  for (let k = 0; k < Math.round(dur * FPS); k++) {
    const t = k / FPS;
    const r = await p.evaluate(t => {
      window.render(t);
      const inter = (a, b, m = 0) => a.x < b.x + b.w + m && b.x < a.x + a.w + m && a.y < b.y + b.h + m && b.y < a.y + a.h + m;
      const R = e => { const q = e.getBoundingClientRect(); return { x: q.left, y: q.top, w: q.width, h: q.height }; };
      if (Number(getComputedStyle(document.querySelector('#end')).opacity) > 0.5) return [];
      const lg = document.querySelector('#ledger');   // Ledger part by part (legs, arms, body, held coin): tighter than one box
      const parts = ['.legs', '.la', '.b1', '.ra'].map(s => R(lg.querySelector(s)));
      if (Number(lg.querySelector('.hc').style.opacity) > 0.05) parts.push(R(lg.querySelector('.hc')));
      const coins = [...document.querySelectorAll('#pile > g')].filter(c => Number(c.style.opacity) > 0.05).map(R);
      const bodies = [...parts.map(b => ['Ledger', b]), ...coins.map(c => ['coin', c])];
      const out = [];
      const texts = [...document.querySelectorAll('#sheet text')].map(e => [e.id || e.textContent.slice(0, 24), R(e)]);
      const curve = document.querySelector('#sheet #curve');
      for (const [n, bb] of bodies) {
        for (const [tn, tb] of texts) if (inter(bb, tb, 2)) out.push(`${n} touches text "${tn}"`);
        if (bb.y + bb.h > 1425) out.push(`${n} reaches the caption band`);
      }
      // the hand: sample its shapes in local coords and map them to the screen
      const hand = document.querySelector('#hand'), M = hand.getCTM(), pts = [];
      const rect = (x, y, w, h) => { for (let u = x; u <= x + w; u += 8) for (let v = y; v <= y + h; v += 8) pts.push([u, v]); };
      rect(0, -23, 314, 46); rect(98, -96, 122, 124); rect(208, -88, 40, 108); rect(244, -82, 700, 96); rect(50, -48, 92, 32); rect(58, 8, 84, 32);
      let hits = 0;
      for (const [u, v] of pts) { const x = M.a * u + M.c * v + M.e, y = M.b * u + M.d * v + M.f;
        for (const [n, bb] of bodies) if (x > bb.x - 4 && x < bb.x + bb.w + 4 && y > bb.y - 4 && y < bb.y + bb.h + 4) { hits++; break; } }
      if (hits) out.push(`hand overlaps Ledger or the pile (${hits} sample points)`);
      if (curve) { /* the traced curve: test sampled points against Ledger and the coins */
        const Lc = curve.getTotalLength(), m = curve.getScreenCTM(); let c = 0;
        for (let s = 0; s <= Lc; s += 6) { const q = curve.getPointAtLength(s), x = m.a * q.x + m.c * q.y + m.e, y = m.b * q.x + m.d * q.y + m.f;
          for (const [n, bb] of bodies) if (x > bb.x && x < bb.x + bb.w && y > bb.y && y < bb.y + bb.h) c++; }
        if (c) out.push(`Ledger or the pile covers the curve (${c} points)`);
      }
      return [...new Set(out)];
    }, t);
    for (const m of r) bad.push(`${t.toFixed(2)} s  ${m}`);
  }
  // collapse runs of the same message
  const seen = {}; for (const l of bad) { const m = l.slice(l.indexOf('  ') + 2); (seen[m] = seen[m] || []).push(l.split(' ')[0]); }
  for (const [m, ts] of Object.entries(seen)) console.log(`CLASH ${m}: ${ts.length} frames, ${ts[0]}-${ts[ts.length - 1]} s`);
  console.log('OVERLAP', bad.length ? 'NOT OK' : 'OK', `(${Math.round(dur * FPS)} frames at ${FPS} fps)`);
  await b.close(); srv.close(); process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
