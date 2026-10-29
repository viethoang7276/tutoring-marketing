// Usage: TIMELINE=<work>/timeline.json NODE_PATH=<explainer scripts/node_modules> node make_cover.js <time_s> <out.png> "<kicker>" "<title with one *keyword*>"
// Renders the reel frame at <time_s> (pick one where the curve and labels are highlighted) with a white title panel
// over the sheet head, inside the 3:4 grid crop (y 240-1680). Same idea as the explainer engine's make_cover.js.
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const D = __dirname, CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', TL = process.env.TIMELINE;
const [t, out, kicker, title] = process.argv.slice(2);
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]); const f = u === '/timeline.json' ? TL : path.join(D, u);
  if ((f !== TL && !f.startsWith(D)) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${srv.address().port}/render.html`, { waitUntil: 'networkidle0' });
  await p.evaluate(() => window.init()); await p.evaluate(t => window.render(t), Number(t));
  await p.evaluate((k, ti) => window.cover(k, ti), kicker, title); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: out }); await b.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
