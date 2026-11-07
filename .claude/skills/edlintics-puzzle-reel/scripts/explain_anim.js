// Animated explanation for puzzle reels (Hoang, 7 Nov 2026: "yes, in the answer explaination"). Opt-in: runs only when the puzzle has "explain_anim".
// A pure function of time, so frames can be seeked: every frame rebuilds the layer's SVG from the items. Coordinates are screen pixels.
// build.py has already turned each "at" / "until" into seconds (fields t and t_until).
(function () {
  const INK = '#0d1523', GREY = '#5b6472', BLUE = '#2960c7', PAPER = '#ffffff';
  const TONE = { red: '#e8604c', green: '#1f9e8f', blue: BLUE, ink: INK, amber: '#f0b429' };   // the colours of the puzzle diagrams
  const FACE = { smile: 'M-12 -168 Q0 -158 12 -168', happy: 'M-14 -170 Q0 -148 14 -170 Z', flat: 'M-11 -164 H11', sad: 'M-12 -158 Q0 -170 12 -158', worried: 'M-12 -160 Q-6 -166 0 -161 Q6 -156 12 -162' };
  const POSE = { down: [[-52, -58], [52, -58]], give: [[-52, -58], [118, -112]], take: [[-118, -112], [52, -58]], raise: [[-52, -58], [78, -188]], cheer: [[-74, -192], [74, -192]], shrug: [[-72, -128], [72, -128]] };
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ramp = (t, a, b) => clamp((t - a) / (b - a));
  const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
  const back = x => { const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const lerp = (a, b, p) => a + (b - a) * p;
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const money = (v, unit = '$', dec = 0) => (v < 0 ? '−' : '') + unit + Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const cv = document.createElement('canvas').getContext('2d');
  const tw = (s, fs, w = 700) => { cv.font = `${w} ${fs}px Inter, sans-serif`; return cv.measureText(String(s)).width; };
  const text = (x, y, s, fs, o = {}) => `<text x="${x}" y="${y}" font-family="Inter, sans-serif" font-size="${fs}" font-weight="${o.w || 700}" fill="${o.fill || INK}" text-anchor="${o.a || 'middle'}">${esc(s)}</text>`;
  const pill = (x, y, s, fs, fill, tc = PAPER) => { const W = tw(s, fs) + 34, H = fs * 1.42; return `<rect x="${x - W / 2}" y="${y - H / 2}" width="${W}" height="${H}" rx="${H / 2}" fill="${fill}" stroke="${INK}" stroke-width="4"/>` + text(x, y + fs * .35, s, fs, { fill: tc }); };
  const alpha = (it, t) => (it.t === undefined ? 1 : ramp(t, it.t, it.t + (it.fade || .25))) * (it.t_until === undefined ? 1 : 1 - ramp(t, it.t_until - .2, it.t_until + .05));

  const DRAW = {
    // Big ticking number in the diagram's blue bar. keys: [{at, to, dur}]
    counter(it, t) {
      let v = it.start; (it.keys || []).forEach(k => { v = lerp(v, k.to, ease(ramp(t, k.t, k.t + (k.dur || .6)))); });
      const fs = it.fs || 64, tick = (it.keys || []).some(k => t >= k.t && t < k.t + (k.dur || .6));
      return `<rect x="${it.x}" y="${it.y}" width="${it.w}" height="${it.h}" rx="6" fill="${BLUE}" stroke="${INK}" stroke-width="4"/>`
        + text(it.x + 32, it.y + it.h / 2 + fs * .28, it.label || '', it.lfs || 42, { a: 'start', fill: PAPER })
        + text(it.x + it.w - 32, it.y + it.h / 2 + fs * .36, money(Math.round(v), it.unit, it.dec), fs, { a: 'end', fill: tick ? '#ffd45c' : PAPER, w: 800 });
    },
    // A line that draws itself, one coloured segment per point, with a value pill riding on its head. points: [{v, at, dur, tone, label, tag: [dx, dy]}]
    line_chart(it, t) {
      const X = i => it.x + it.pad + (it.w - 2 * it.pad) * i / (it.points.length - 1), Y = v => it.y + it.h * (it.max - v) / (it.max - it.min);
      let s = '';
      (it.grid || []).forEach(v => { s += `<line x1="${it.x}" x2="${it.x + it.w}" y1="${Y(v)}" y2="${Y(v)}" stroke="#e3e8f1" stroke-width="3"/>`; });
      if (it.ref) { const a = ramp(t, it.ref.t, it.ref.t + .3); s += `<g opacity="${a}"><line x1="${X(0)}" x2="${it.x + it.w}" y1="${Y(it.ref.v)}" y2="${Y(it.ref.v)}" stroke="${GREY}" stroke-width="4" stroke-dasharray="14 12"/></g>`; }
      let lines = '', tags = '', head = null;
      it.points.forEach((p, i) => {
        if (p.t !== undefined && t < p.t) return;
        const q = i ? ease(ramp(t, p.t, p.t + (p.dur || .7))) : 1, col = TONE[p.tone || 'blue'];
        if (i) { const a = it.points[i - 1], hx = lerp(X(i - 1), X(i), q), hy = lerp(Y(a.v), Y(p.v), q);
          lines += `<line x1="${X(i - 1)}" y1="${Y(a.v)}" x2="${hx}" y2="${hy}" stroke="${col}" stroke-width="10" stroke-linecap="round"/>`;
          if (q < 1) head = [hx, hy, col]; }
        const v = i ? lerp(it.points[i - 1].v, p.v, q) : p.v, [dx, dy] = p.tag || [0, -52];
        const hx = i ? lerp(X(i - 1), X(i), q) : X(0), hy = i ? lerp(Y(it.points[i - 1].v), Y(p.v), q) : Y(p.v);
        tags += `<circle cx="${hx}" cy="${hy}" r="13" fill="${col}" stroke="${INK}" stroke-width="4"/><g opacity="${i ? ramp(q, .15, .35) : 1}">` + pill(hx + dx, hy + dy, money(Math.round(v), it.unit, it.dec), it.fs || 40, col) + '</g>';   // the moving pill waits until it has left the previous value's pill
        if (p.label) s += `<g opacity="${ramp(t, p.t === undefined ? -1 : p.t, (p.t === undefined ? -1 : p.t) + .3)}">${text(X(i), it.y + it.h + (it.lfs || 36) + 8, p.label, it.lfs || 36, { fill: GREY, w: 600 })}</g>`;
      });
      return s + lines + tags;
    },
    // A chunky arrow that grows from its tail. Colour says good or bad, so a rising debt is red. (x, y) = centre
    arrow(it, t) {
      const g = ease(ramp(t, it.t, it.t + (it.dur || .5))), L = (it.length || 160) / 2, w = (it.width || 84) / 2, k = it.dir === 'up' ? -1 : 1, sw = w * .5, hh = w * 1.2;
      const d = `M${-sw} ${-k * L} L${sw} ${-k * L} L${sw} ${k * (L - hh)} L${w} ${k * (L - hh)} L0 ${k * L} L${-w} ${k * (L - hh)} L${-sw} ${k * (L - hh)} Z`;
      return `<g transform="translate(${it.x} ${it.y - k * L}) scale(1 ${Math.max(.01, g)}) translate(0 ${k * L})"><path d="${d}" fill="${TONE[it.tone]}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/></g>`
        + (it.text ? `<g opacity="${ramp(g, .5, 1)}">${text(it.x + w + 14, it.y + (it.fs || 44) * .35, it.text, it.fs || 44, { a: 'start', w: 800 })}</g>` : '');
    },
    // A pill that travels from (x, y) to `to`, bowing upward by `arc`, with an optional fading trail
    chip(it, t) {
      const q = ease(ramp(t, it.t, it.t + (it.dur || .8))), to = it.to || [it.x, it.y], a = it.arc || 0;
      const P = u => [lerp(it.x, to[0], u), lerp(it.y, to[1], u) - a * 4 * u * (1 - u)];
      const [x, y] = P(q); let s = '';
      if (it.trail && q > 0) { let d = ''; for (let i = 0; i <= 16; i++) { const [px, py] = P(q * i / 16); d += (i ? 'L' : 'M') + px.toFixed(1) + ' ' + py.toFixed(1); }
        s += `<path d="${d}" fill="none" stroke="${TONE[it.tone]}" stroke-width="7" stroke-linecap="round" stroke-dasharray="4 16" opacity="${1 - ramp(t, it.t + (it.dur || .8), it.t + (it.dur || .8) + .4)}"/>`; }
      return s + pill(x, y, it.text, it.fs || 44, TONE[it.tone]);
    },
    // Lines of supporting text. An example number needs "example": true, which labels it on screen
    note(it, t) {
      const fs = it.fs || 36, lines = (it.example ? ['Example:'] : []).concat(it.lines || [it.text]), p = back(clamp(ramp(t, it.t, it.t + .35)));
      return `<g transform="translate(0 ${12 * (1 - p)})">` + lines.map((l, i) => text(it.x, it.y + i * fs * 1.22, l, fs, { a: it.a || 'middle', w: it.w || 700, fill: it.tone ? TONE[it.tone] : INK })).join('') + '</g>';
    },
    // The diagram's split bar: a whole amount that breaks into its parts. parts: [{value, text, fill, at, dur, pulse: {at, dur}}], whole: {text, at}
    split_bar(it, t) {
      const total = it.parts.reduce((a, p) => a + p.value, 0); let s = '', x = it.x;
      const wt = it.whole && it.whole.text, frame = `<rect x="${it.x}" y="${it.y}" width="${it.w}" height="${it.h}" rx="6" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`;
      s += frame + (wt ? `<g opacity="${1 - (it.parts[0].t !== undefined ? ramp(t, it.parts[0].t, it.parts[0].t + .25) : 0)}">${text(it.x + it.w / 2, it.y + it.h / 2 + (it.fs || 40) * .35, wt, it.fs || 40, { w: 800, fill: BLUE })}</g>` : '');
      it.parts.forEach(p => {
        const W = it.w * p.value / total, g = ease(ramp(t, p.t, p.t + (p.dur || .4))), k = p.pulse ? 1 + (p.pulse.amp || .07) * Math.sin(Math.PI * ramp(t, p.pulse.t, p.pulse.t + (p.pulse.dur || .7))) : 1;
        if (g > 0) s += `<g transform="translate(${x + W / 2} ${it.y + it.h / 2}) scale(${k}) translate(${-(x + W / 2)} ${-(it.y + it.h / 2)})"><rect x="${x}" y="${it.y}" width="${W * g}" height="${it.h}" rx="6" fill="${TONE[p.fill]}" stroke="${INK}" stroke-width="4"/><g opacity="${ramp(g, .6, 1)}">${text(x + W / 2, it.y + it.h / 2 + (it.fs || 40) * .35, p.text, it.fs || 40, { fill: PAPER })}</g></g>`;
        x += W;
      });
      return s;
    },
    // A person who acts, the same figure as the explainer engine's trader. (x, y) = between the feet. acts: [{at, pose, mood}]
    person(it, t) {
      let pose = POSE.down, mood = it.mood || 'smile', hop = 0;
      let cur = POSE.down;
      (it.acts || []).forEach(a => { const q = ease(ramp(t, a.t, a.t + .3)), to = POSE[a.pose || 'down'] || cur;
        cur = cur.map((h, i) => [lerp(h[0], to[i][0], q), lerp(h[1], to[i][1], q)]);
        if (t >= a.t) { if (a.mood) mood = a.mood; if (a.hop !== false) hop = Math.max(hop, 16 * Math.sin(Math.PI * ramp(t, a.t, a.t + .36))); } });
      pose = cur;
      const c = it.color || '#dbe6fb', arm = (sx, h) => { const d = `M${sx} -110 Q${(sx + h[0]) / 2} ${(h[1] - 110) / 2 + 22} ${h[0]} ${h[1]}`;
        return `<path d="${d}" fill="none" stroke="${INK}" stroke-width="11" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${c}" stroke-width="4" stroke-linecap="round"/><circle cx="${h[0]}" cy="${h[1]}" r="10" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`; };
      const body = `<ellipse cx="0" cy="4" rx="46" ry="7" fill="${INK}" opacity=".1"/><g transform="translate(0 ${-hop})"><path d="M-46 0 V-90 Q-46 -130 0 -130 Q46 -130 46 -90 V0 Z" fill="${c}" stroke="${INK}" stroke-width="5"/>`
        + `<circle cx="0" cy="-178" r="40" fill="${PAPER}" stroke="${INK}" stroke-width="5"/><circle cx="-13" cy="-184" r="5" fill="${INK}"/><circle cx="13" cy="-184" r="5" fill="${INK}"/>`
        + `<path d="${FACE[mood]}" fill="${mood === 'happy' ? PAPER : 'none'}" stroke="${INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>${arm(-44, pose[0])}${arm(44, pose[1])}</g>`;
      const s = it.s || 1;
      return `<g transform="translate(${it.x} ${it.y}) scale(${s})">${body}</g>` + (it.name ? text(it.x, it.y + (it.nfs || 38) + 16, it.name, it.nfs || 38, { w: 800 }) : '');
    },
  };

  window.renderExplainAnim = function (t) {
    const A = T.explain_anim, S = ramp(t, T.steps_in, T.steps_in + 0.4);
    let out = '';
    if (S > 0) for (const it of A.items) {
      if (it.t !== undefined && t < it.t) continue;
      const a = alpha(it, t); if (a <= 0) continue;
      out += `<g opacity="${a}">${DRAW[it.p](it, t)}</g>`;
    }
    document.querySelector('#animlayer').innerHTML = out;
  };
})();
