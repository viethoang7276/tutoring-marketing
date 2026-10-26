// Usage: SCENES=<workdir>/scenes.json node make_cover.js <time_s> <out.png> "<kicker>" "<title with *keyword* marked>"
// Renders the reel frame at <time_s> with the caption band replaced by a cover title (kicker + big title,
// one *keyword* highlighted in brand yellow). 1080x1920; the title sits inside the 3:4 grid crop (y 240-1680).
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const D = __dirname, CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SCENES = process.env.SCENES;
const [t, out, kicker, title] = process.argv.slice(2);
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]);
  const f = (u === '/scenes.json' && SCENES) ? SCENES : path.join(D, u);
  if ((!f.startsWith(D) && f !== SCENES) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(ok => srv.listen(0, '127.0.0.1', ok));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(`http://127.0.0.1:${srv.address().port}/render.html`, { waitUntil: 'networkidle0' });
  await p.evaluate(() => window.init());
  await p.evaluate(t => window.render(t), Number(t));
  await p.evaluate((kicker, title) => {
    const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
    const cap = document.getElementById('cap');
    cap.style.cssText = 'top:250px;height:300px;flex-direction:column;gap:14px';
    const html = esc(title).replace(/\*(.+?)\*/g, '<span class="k" style="--w:100%">$1</span>');
    cap.innerHTML = `<div style="font:800 40px/1.1 Inter,sans-serif;color:#467DE3;letter-spacing:.06em;text-transform:uppercase">${esc(kicker)}</div>` +
                    `<div class="c" style="font-size:104px;line-height:1.04;transform:none;opacity:1">${html}</div>`;
    document.getElementById('card').style.display = 'none';
    const art = document.getElementById('art'); if (art) { art.style.webkitMaskImage = art.style.maskImage = 'linear-gradient(to bottom,transparent 575px,#000 630px)'; }
    document.getElementById('stage').style.transform = 'translateY(110px)';   // centre the cover in the 3:4 grid crop
  }, kicker, title);
  await p.evaluate(() => document.fonts.ready);
  if (out.endsWith('.pdf')) await p.evaluate(() => { const pp = document.getElementById('paper'); if (pp) pp.style.display = 'none'; });   // the paper texture rasterises huge in PDF
  if (out.endsWith('.pdf')) await p.pdf({ path: out, width: '1080px', height: '1920px', printBackground: true, pageRanges: '1' });   // vector text, editable after a Canva import
  else await p.screenshot({ path: out });
  await b.close(); srv.close();
})();
