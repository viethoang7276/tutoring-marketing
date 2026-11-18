// Record one take of a scripted, human-paced interaction on a PUBLIC edlintics.com page, headless, as crisp JPEG frames.
// Usage: node record_demo.js SPEC.json TIMINGS.json OUT_DIR
//   SPEC     the demo spec (url, viewport, dsf, lines[].actions), see examples/pilot-journal-entry.json
//   TIMINGS  timings.json from demo_voice.py, so every action lands on its voice line
//   OUT_DIR  gets frames/*.jpg, frames.json (frame times in s from the start), events.json (actions, rects, network log)
// Signed out, never types personal data, never submits a form. The consent banner is hidden with CSS (no click, so no
// consent call is sent). Every non-GET request and every main-frame navigation is logged; the run fails if one appears.
// Playwright is used only as a browser driver, from the tutoring-web install (no app code is imported).
const fs = require('fs'), path = require('path');
const PW = process.env.PLAYWRIGHT_PATH ||
  '/Users/hoangtruong/Desktop/WebDevelopment/tutoring/tutoring-web/node_modules/.pnpm/playwright@1.60.0/node_modules/playwright';
const { chromium, devices } = require(PW);

const [specPath, timingsPath, out] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const timings = JSON.parse(fs.readFileSync(timingsPath, 'utf8'));
fs.mkdirSync(path.join(out, 'frames'), { recursive: true });

// In-page helpers: a soft blue finger dot, a tap ripple and eased scrolling. All pointer-events none.
const HELPERS = `(() => {
  const st = document.createElement('style');
  st.textContent = '[data-consent-banner]{display:none!important}' +
    '#__finger{position:fixed;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;z-index:2147483647;pointer-events:none;' +
    'background:rgba(70,125,227,.30);border:2px solid rgba(70,125,227,.95);box-shadow:0 4px 14px rgba(2,8,23,.25);opacity:0;transition:opacity .25s, transform .12s}' +
    '.__ripple{position:fixed;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;z-index:2147483646;pointer-events:none;' +
    'border:4px solid rgba(70,125,227,1);background:rgba(96,165,250,.38);animation:__rip .85s ease-out forwards}' +
    '@keyframes __rip{from{transform:scale(1);opacity:1}60%{opacity:.75}to{transform:scale(4.6);opacity:0}}';
  document.head.appendChild(st);
  const f = document.createElement('div'); f.id = '__finger'; document.body.appendChild(f);
  const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
  const anim = (dur, step) => new Promise(res => { const t0 = performance.now();
    const tick = now => { const k = Math.min(1, (now - t0) / dur); step(ease(k)); k < 1 ? requestAnimationFrame(tick) : res(); };
    requestAnimationFrame(tick); });
  let fx = innerWidth * .72, fy = innerHeight * .8;
  const place = (x, y) => { fx = x; fy = y; f.style.left = x + 'px'; f.style.top = y + 'px'; };
  window.__demo = {
    show(x, y) { if (x != null) place(x, y); f.style.opacity = 1; },
    hide() { f.style.opacity = 0; },
    moveTo(x, y, dur) { const x0 = fx, y0 = fy; f.style.opacity = 1; return anim(dur, k => place(x0 + (x - x0) * k, y0 + (y - y0) * k)); },
    scrollTo(y, dur, swipe) {
      const s0 = scrollY, H = innerHeight, X = innerWidth * .72;
      if (swipe) { place(X, H * .82); f.style.opacity = 1; }
      return anim(dur, k => { scrollTo(0, s0 + (y - s0) * k); if (swipe) place(X, H * .82 - H * .5 * k); })
        .then(() => { if (swipe) setTimeout(() => f.style.opacity = 0, 150); });
    },
    press(x, y) { place(x, y); f.style.opacity = 1; f.style.transform = 'scale(.82)';
      const r = document.createElement('div'); r.className = '__ripple'; r.style.left = x + 'px'; r.style.top = y + 'px';
      document.body.appendChild(r); setTimeout(() => r.remove(), 950); setTimeout(() => f.style.transform = '', 160); }
  };
})()`;

(async () => {
  // Without this flag headless screencast frames come out at CSS pixels (410x500); with it they are real device pixels
  const browser = await chromium.launch({ headless: true, args: [`--force-device-scale-factor=${spec.dsf || 2.5}`] });
  const ctx = await browser.newContext({
    viewport: { width: spec.viewport[0], height: spec.viewport[1] }, deviceScaleFactor: spec.dsf || 2.5,
    isMobile: true, hasTouch: true, userAgent: devices['iPhone 14 Pro Max'].userAgent, locale: 'en-GB' });
  const page = await ctx.newPage();
  const net = [], navs = [];
  await page.goto(spec.url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForTimeout(3000);
  page.on('request', r => { if (r.method() !== 'GET') net.push(`${r.method()} ${r.url()}`); });
  page.on('framenavigated', fr => { if (fr === page.mainFrame()) navs.push(fr.url()); });
  await page.evaluate(HELPERS);
  await page.evaluate(() => scrollTo(0, 0));
  await page.waitForTimeout(800);

  // Find a target: {text} = first element whose own text starts the match, {buttonText} = the button containing it
  const rectOf = sel => page.evaluate(sel => {
    let el = null;
    if (sel.buttonText) el = [...document.querySelectorAll('main button')].find(b => b.textContent.includes(sel.buttonText));
    else if (sel.text) { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) if (n.data.trim().startsWith(sel.text)) { el = n.parentElement; break; } }
    if (!el) return null;
    if (sel.id) el.setAttribute('data-demo-id', sel.id);
    const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, sy: scrollY };
  }, sel);
  const tagged = () => page.evaluate(() => Object.fromEntries([...document.querySelectorAll('[data-demo-id]')].map(e => {
    const r = e.getBoundingClientRect(); return [e.dataset.demoId, { x: r.x, y: r.y, w: r.width, h: r.height }]; })));

  // Absolute schedule (seconds on the reel timeline; recording time 0 = reel time 0)
  const acts = [];
  spec.lines.forEach((ln, i) => (ln.actions || []).forEach(a => {
    const L = timings.lines[i]; let t;
    if (typeof a.t === 'string' && a.t.startsWith('end')) t = L.end + parseFloat(a.t.slice(3) || 0); else t = L.start + (a.t || 0);
    acts.push({ ...a, at: Math.max(0, t), line: i });
  }));
  acts.sort((a, b) => a.at - b.at);

  const cdp = await ctx.newCDPSession(page);
  const frames = []; let t0 = null, n = 0;
  cdp.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
    cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {});
    if (t0 === null) return;
    const f = String(n++).padStart(5, '0') + '.jpg';
    fs.writeFileSync(path.join(out, 'frames', f), Buffer.from(data, 'base64'));
    frames.push({ f, t: +(metadata.timestamp - t0).toFixed(4) });
  });
  const W = Math.round(spec.viewport[0] * (spec.dsf || 2.5)), H = Math.round(spec.viewport[1] * (spec.dsf || 2.5));
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 94, maxWidth: W, maxHeight: H, everyNthFrame: 1 });
  t0 = Date.now() / 1000;
  const now = () => Date.now() / 1000 - t0;
  const until = async s => { const d = s - now(); if (d > 0) await page.waitForTimeout(d * 1000); };
  // A 1-px nudge so the first frame arrives at t≈0
  await page.evaluate(() => { scrollTo(0, 1); scrollTo(0, 0); });

  const events = [];
  for (const a of acts) {
    await until(a.at);
    const ev = { do: a.do, planned: a.at, started: +now().toFixed(3), line: a.line };
    if (a.do === 'scrollTo' || a.do === 'swipeTo') {
      const r = await rectOf(a);
      if (!r) throw new Error('target not found: ' + JSON.stringify(a));
      await page.evaluate(([y, d, sw]) => window.__demo.scrollTo(y, d, sw), [r.sy + r.y - (a.top || 80), (a.dur || 1) * 1000, a.do === 'swipeTo']);
    } else if (a.do === 'finger') {
      const r = await rectOf(a);
      await page.evaluate(([x, y, d]) => window.__demo.moveTo(x, y, d), [r.x + r.w * (a.fx ?? 0.55), r.y + r.h * (a.fy ?? 0.5), (a.dur || 0.8) * 1000]);
    } else if (a.do === 'tap') {
      const r = await rectOf(a);
      const x = r.x + r.w * (a.fx ?? 0.55), y = r.y + r.h * (a.fy ?? 0.5);   // fx/fy: where on the target the finger lands (keep key words uncovered)
      await page.evaluate(([x, y]) => window.__demo.moveTo(x, y, 250), [x, y]);
      await page.evaluate(([x, y]) => window.__demo.press(x, y), [x, y]);
      await page.touchscreen.tap(x, y);
      ev.tap = { x, y };
      setTimeout(() => page.evaluate(() => window.__demo.hide()).catch(() => {}), 900);
    }
    ev.ended = +now().toFixed(3);
    events.push(ev);
  }
  // Rects of tagged targets after each line's actions settle are what compose uses for zooms: sample them per line
  const rects = [];
  await page.waitForTimeout(400);
  rects.push({ t: +now().toFixed(3), r: await tagged() });
  await until(timings.total + 0.3);
  rects.push({ t: +now().toFixed(3), r: await tagged() });
  await cdp.send('Page.stopScreencast');
  await page.waitForTimeout(300);
  const finalUrl = page.url();
  await browser.close();
  const log = { url: spec.url, finalUrl, viewport: spec.viewport, dsf: spec.dsf || 2.5, events, rects, nonGetRequests: net, navigations: navs, frames: frames.length };
  fs.writeFileSync(path.join(out, 'frames.json'), JSON.stringify(frames));
  fs.writeFileSync(path.join(out, 'events.json'), JSON.stringify(log, null, 1));
  console.log(JSON.stringify({ frames: frames.length, events: events.map(e => `${e.do}@${e.planned.toFixed(2)}→${e.started}`), net, navs }, null, 1));
  if (net.length || navs.length) { console.error('STOP: a non-GET request or navigation happened, see events.json'); process.exit(2); }
})();
