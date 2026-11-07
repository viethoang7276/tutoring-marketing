// Picture props for the animated puzzle explanation (Hoang, 7 Nov 2026: "too dry with only number, may be we should use graphic to explain as well").
// The puzzle's situation told as a picture: its people and objects move with the voice, with numbers as labels on them. Opt-in: used only by "explain_anim" items
// with "p": "sprite", "walker", "flow" or "dots". Pure functions of time, like explain_anim.js. Coordinates and every font size are screen pixels (text does not scale with the art).
(function () {
  const { DRAW, TONE, clamp, ramp, ease, back, lerp, esc, money, text, pill, INK, GREY, BLUE, PAPER } = window.EXPLAIN_KIT;
  const SK = `stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;
  const SKY = '#dbe6fb', SAND = '#f6ead6', WOOD = '#d9b27c', GOLD = '#f0b429', CORAL = TONE.red, TEAL = TONE.green;
  const col = c => TONE[c] || c;
  const num = (v, d) => (v === undefined ? d : v);

  // Position after "moves" [{at, to: [x, y], dur, arc, scale, rot, ease}], played in order
  function place(it, t) {
    let x = it.x, y = it.y, s = num(it.s, 1), rot = it.rot || 0, moving = false;
    (it.moves || []).forEach(m => { const d = m.dur || .8, q = (m.ease === 'back' ? back : ease)(clamp(ramp(t, m.t, m.t + d))); if (t <= m.t) return;
      if (t < m.t + d) moving = true; const to = m.to || [x, y];
      const nx = lerp(x, to[0], q), ny = lerp(y, to[1], q) - (m.arc || 0) * 4 * q * (1 - q); s = lerp(s, num(m.scale, s), q); rot = lerp(rot, num(m.rot, rot), q); x = nx; y = ny; });
    return { x, y, s, rot, moving };
  }
  const pulseK = (it, t) => (it.pulse || []).reduce((k, p) => k * (1 + (p.amp || .1) * Math.sin(Math.PI * clamp(ramp(t, p.t, p.t + (p.dur || .6))))), 1);
  function valueText(v, t) { let a = v.start; (v.keys || []).forEach(k => { a = lerp(a, k.to, ease(clamp(ramp(t, k.t, k.t + (k.dur || .6))))); });
    return (v.prefix || '') + money(v.dec ? a : Math.round(a), v.unit === undefined ? '$' : v.unit, v.dec || 0) + (v.suffix || ''); }
  function textOf(it, t) { if (it.value) return valueText(it.value, t); let s = it.text; (it.texts || []).forEach(x => { if (t >= x.t) s = x.text; }); return s; }

  // ---------- the drawings. (0, 0) is the centre unless noted ----------
  const ART = {
    // The room seen from the door side, (0, 0) = top left: back wall with lamps, a floor to seat people on, an entrance on the left and an exit on the right
    cafe(it) { const w = it.w, h = it.h, stripes = Array.from({ length: Math.round(w / 90) }, (_, k) => `<path d="M${k * w / Math.round(w / 90)} 0 h${w / Math.round(w / 90)} l-5 56 q-${w / Math.round(w / 90) / 2 - 5} 18 -${w / Math.round(w / 90) - 10} 0 Z" fill="${k % 2 ? PAPER : BLUE}" ${SK}/>`).join('');
      const lamp = x => `<path d="M${x} 56 V112" ${SK} fill="none"/><path d="M${x - 30} 142 Q${x} 92 ${x + 30} 142 Z" fill="${GOLD}" ${SK}/>`;
      return `<rect x="0" y="40" width="${w}" height="${h - 40}" fill="${SAND}" ${SK}/><rect x="0" y="40" width="${w}" height="120" fill="#fbf3e4" ${SK}/>${lamp(w * .25)}${lamp(w * .5)}${lamp(w * .75)}${stripes}`
        + `<rect x="-8" y="${h - 190}" width="30" height="190" fill="${BLUE}" ${SK}/><rect x="${w - 22}" y="${h - 190}" width="30" height="190" fill="${TEAL}" ${SK}/><path d="M-130 ${h} H${w + 130}" ${SK} fill="none" stroke-width="7"/>`; },
    card(it) { const w = it.w || 480, h = it.h || 300; return `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="28" fill="${BLUE}" ${SK}/><rect x="${-w / 2}" y="${-h / 2 + 46}" width="${w}" height="46" fill="${INK}"/>`
        + `<rect x="${-w / 2 + 34}" y="${-h / 2 + 112}" width="70" height="52" rx="9" fill="${GOLD}" ${SK}/><path d="M${-w / 2 + 34} ${-h / 2 + 138} h70 M${-w / 2 + 69} ${-h / 2 + 112} v52" ${SK} stroke-width="3" fill="none"/>`; },
    bank(it) { const w = it.w || 320, h = it.h || 300, cols = [-.36, -.12, .12, .36].map(c => `<rect x="${c * w - 16}" y="${-h * .16}" width="32" height="${h * .54}" fill="${PAPER}" ${SK}/>`).join('');
      return `<path d="M${-w / 2 - 14} ${-h * .16} L0 ${-h / 2} L${w / 2 + 14} ${-h * .16} Z" fill="${SKY}" ${SK}/>${cols}<rect x="${-w / 2}" y="${h * .38}" width="${w}" height="${h * .12}" fill="${WOOD}" ${SK}/><circle cx="0" cy="${-h * .28}" r="22" fill="${GOLD}" ${SK}/>`; },
    note(it) { const w = it.w || 240, h = it.h || 120, c = col(it.tone || 'green'); return `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="10" fill="${c}" ${SK}/><rect x="${-w / 2 + 11}" y="${-h / 2 + 11}" width="${w - 22}" height="${h - 22}" rx="6" fill="none" stroke="${PAPER}" stroke-width="3" opacity=".55"/>`; },
    tag(it) { const w = it.w || 220, h = it.h || 92, c = col(it.tone || 'blue'); return `<path d="M${-w / 2 + 34} ${-h / 2} H${w / 2} V${h / 2} H${-w / 2 + 34} L${-w / 2} 0 Z" fill="${c}" ${SK}/><circle cx="${-w / 2 + 28}" cy="0" r="8" fill="${PAPER}" ${SK} stroke-width="3"/>`; },
    // Solid block, (0, 0) = top left; "wkeys" [{at, to, dur}] change its width; "grow" {at, dur} raises it from its base
    block(it, t) { const w = blockW(it, t), g = it.grow ? ease(clamp(ramp(t, it.grow.t, it.grow.t + (it.grow.dur || .8)))) : 1, h = it.h * g; return `<rect x="0" y="${it.h - h}" width="${w}" height="${h}" rx="8" fill="${col(it.tone || 'blue')}" ${SK}/>`; },
    // (0, 0) = centre; s scales. Basket faces right
    cart() { return `<path d="M-190 -120 H-150 L-110 60 H130" fill="none" ${SK} stroke-width="9"/><path d="M-145 -90 H170 L135 30 H-118 Z" fill="${PAPER}" ${SK}/><path d="M-92 -90 L-74 30 M-30 -90 L-20 30 M34 -90 L34 30 M98 -90 L86 30 M-134 -50 H158 M-124 -10 H146" fill="none" ${SK} stroke-width="3"/><circle cx="-80" cy="92" r="24" fill="${INK}"/><circle cx="100" cy="92" r="24" fill="${INK}"/><circle cx="-80" cy="92" r="9" fill="${PAPER}"/><circle cx="100" cy="92" r="9" fill="${PAPER}"/>`; },
    shirt(it) { return `<path d="M-40 -62 L-96 -28 L-72 14 L-50 2 V70 H50 V2 L72 14 L96 -28 L40 -62 Q0 -38 -40 -62 Z" fill="${col(it.tone || CORAL)}" ${SK}/>`; },
    pants(it) { return `<path d="M-48 -72 H48 L58 74 H14 L0 -8 L-14 74 H-58 Z" fill="${col(it.tone || BLUE)}" ${SK}/><path d="M-48 -52 H48" fill="none" ${SK} stroke-width="3"/>`; },
    phone(it) { return `<rect x="-50" y="-88" width="100" height="176" rx="18" fill="${col(it.tone || GOLD)}" ${SK}/><rect x="-34" y="-72" width="38" height="46" rx="10" fill="${INK}"/><circle cx="-22" cy="-59" r="7" fill="${PAPER}"/><circle cx="-14" cy="-40" r="6" fill="${PAPER}"/>`; },
    jacket(it) { const c = col(it.tone || BLUE); return `<path d="M0 -180 q0 -24 18 -24 q16 0 14 16 q-2 12 -32 26 L-94 -118 H94 L0 -162" fill="none" ${SK} stroke="${GREY}"/><path d="M-60 -122 L-132 -80 L-158 100 L-104 110 L-90 -8 V150 H90 V-8 L104 110 L158 100 L132 -80 L60 -122 L0 -60 Z" fill="${c}" ${SK}/><path d="M0 -60 V150" ${SK} fill="none"/><path d="M-60 -122 L-26 -32 L0 -60 L26 -32 L60 -122" fill="${SKY}" ${SK}/><circle cx="16" cy="10" r="7" fill="${PAPER}" ${SK} stroke-width="3"/><circle cx="16" cy="60" r="7" fill="${PAPER}" ${SK} stroke-width="3"/><circle cx="16" cy="110" r="7" fill="${PAPER}" ${SK} stroke-width="3"/>`; },
    wheat() { const ear = (x, r) => `<g transform="translate(${x} 30) rotate(${r})"><path d="M0 70 V-60" stroke="#c28f2c" stroke-width="7" fill="none"/>${[-60, -38, -16, 6].map(y => `<ellipse cx="-13" cy="${y}" rx="11" ry="17" fill="${GOLD}" stroke="${INK}" stroke-width="3.5" transform="rotate(-24 -13 ${y})"/><ellipse cx="13" cy="${y}" rx="11" ry="17" fill="${GOLD}" stroke="${INK}" stroke-width="3.5" transform="rotate(24 13 ${y})"/>`).join('')}<ellipse cx="0" cy="-76" rx="10" ry="17" fill="${GOLD}" stroke="${INK}" stroke-width="3.5"/></g>`;
      return ear(-34, -16) + ear(34, 16) + ear(0, 0) + `<rect x="-30" y="56" width="60" height="16" rx="5" fill="${CORAL}" ${SK} stroke-width="3.5"/>`; },
    bread() { return `<path d="M-120 44 Q-136 -48 -60 -56 Q0 -84 60 -56 Q136 -48 120 44 Q0 62 -120 44 Z" fill="#dda15e" ${SK}/><path d="M-60 -30 q14 26 8 52 M-6 -38 q14 28 8 60 M50 -30 q14 26 8 52" fill="none" stroke="#8a5a2b" stroke-width="7" stroke-linecap="round"/>`; },
    hat() { return `<path d="M-44 10 Q-74 -6 -56 -38 Q-40 -60 -18 -46 Q0 -72 22 -46 Q44 -60 58 -38 Q74 -6 44 10 Z" fill="${PAPER}" ${SK}/><rect x="-44" y="8" width="88" height="24" rx="4" fill="${PAPER}" ${SK}/>`; },
    // (0, 0) = centre of the ground; w wide, h tall
    store(it) { const w = it.w || 340, h = it.h || 300, c = col(it.tone || BLUE), n = 6, sw = w / n, stripes = Array.from({ length: n }, (_, k) => `<path d="M${-w / 2 + k * sw} ${-h * .78} h${sw} l-3 ${h * .16} q-${sw / 2 - 3} 12 -${sw - 6} 0 Z" fill="${k % 2 ? PAPER : c}" ${SK}/>`).join('');
      return `<rect x="${-w / 2 + 12}" y="${-h}" width="${w - 24}" height="${h}" fill="#fbf3e4" ${SK}/><rect x="${-w / 2 + 34}" y="${-h * .5}" width="${w * .42}" height="${h * .36}" rx="4" fill="${SKY}" ${SK}/><rect x="${w * .12}" y="${-h * .52}" width="${w * .26}" height="${h * .52}" rx="4" fill="${c}" ${SK}/><circle cx="${w * .33}" cy="${-h * .24}" r="6" fill="${GOLD}" stroke="${INK}" stroke-width="3"/>${stripes}<path d="M${-w / 2 - 16} 0 H${w / 2 + 16}" fill="none" ${SK} stroke-width="6"/>`; },
    clock(it, t) { const r = it.r || 110, f = 1 - 0, sw = it.sweep, q = sw ? sw.to * ease(clamp(ramp(t, sw.t, sw.t + (sw.dur || 1)))) : 0, a = -Math.PI / 2 + 2 * Math.PI * q, big = q > .5 ? 1 : 0;
      const wedge = q > 0 ? `<path d="M0 0 L0 ${-r + 8} A${r - 8} ${r - 8} 0 ${big} 1 ${(r - 8) * Math.cos(a)} ${(r - 8) * Math.sin(a)} Z" fill="${TEAL}" opacity=".75"/>` : '';
      const ticks = Array.from({ length: 12 }, (_, k) => { const b = k * Math.PI / 6; return `<path d="M${(r - 20) * Math.sin(b)} ${-(r - 20) * Math.cos(b)} L${(r - 8) * Math.sin(b)} ${-(r - 8) * Math.cos(b)}" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`; }).join('');
      return `<circle r="${r}" fill="${PAPER}" ${SK} stroke-width="7"/>${wedge}${ticks}<path d="M0 0 L${(r - 26) * Math.cos(a)} ${(r - 26) * Math.sin(a)}" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0 0 L0 ${-r * .46}" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><circle r="9" fill="${INK}"/>`; },
    // A dial from bad (left, -1) to good (right, 1). "keys" [{at, to, dur}] swing the needle
    gauge(it, t) { const r = it.r || 150; let v = it.start || 0; (it.keys || []).forEach(k => { v = lerp(v, k.to, ease(clamp(ramp(t, k.t, k.t + (k.dur || .5))))); });
      const P = (a, R) => `${R * Math.cos(a)} ${R * Math.sin(a)}`, seg = (a, b, c) => `<path d="M${P(a, r)} A${r} ${r} 0 0 1 ${P(b, r)}" fill="none" stroke="${INK}" stroke-width="44"/><path d="M${P(a, r)} A${r} ${r} 0 0 1 ${P(b, r)}" fill="none" stroke="${c}" stroke-width="34"/>`, a = -Math.PI / 2 + v * Math.PI / 2 * .92;
      return seg(-Math.PI, -Math.PI * 2 / 3, CORAL) + seg(-Math.PI * 2 / 3, -Math.PI / 3, GOLD) + seg(-Math.PI / 3, 0, TEAL) + `<path d="M0 0 L${P(a, r - 34)}" stroke="${INK}" stroke-width="11" stroke-linecap="round"/><circle r="17" fill="${BLUE}" ${SK}/>`; },
    receipt(it) { const w = it.w || 300, h = it.h || 220, n = 8, sw = w / n; let z = `M${-w / 2} ${-h / 2} H${w / 2} V${h / 2} `; for (let k = 0; k < n; k++) z += `l${-sw / 2} 16 l${-sw / 2} -16 `; return `<path d="${z}Z" fill="${PAPER}" ${SK}/>`; },
    board(it) { const w = it.w || 300, h = it.h || 130; return `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="10" fill="${it.fill || '#fbf3e4'}" ${SK}/>`; },
    cross(it, t) { const sw = it.sw || 16, w = (it.w || 200) / 2, h = (it.h || w * 2) / 2, g = it.t === undefined ? 1 : ease(clamp(ramp(t, it.t, it.t + .3))); return `<path d="M${-w} ${-h} L${lerp(-w, w, g)} ${lerp(-h, h, g)}" stroke="${CORAL}" stroke-width="${sw}" stroke-linecap="round"/>` + (g > .5 ? `<path d="M${w} ${-h} L${lerp(w, -w, (g - .5) * 2)} ${lerp(-h, h, (g - .5) * 2)}" stroke="${CORAL}" stroke-width="${sw}" stroke-linecap="round"/>` : ''); },
  };
  const blockW = (it, t) => { let w = it.w; (it.wkeys || []).forEach(k => { w = lerp(w, k.to, ease(clamp(ramp(t, k.t, k.t + (k.dur || .6))))); }); return w; };
  const LOCAL_TOPLEFT = { cafe: 1, block: 1 };

  // One drawn object. kind: see ART. Optional: moves, pop (grows in), pulse [{at, dur, amp}], text / texts [{at, text}] / value {start, keys, unit, prefix, suffix, dec}, fs, tc, tpos [dx, dy],
  // lines (several centred rows), label {text, dx, dy, fs, tone, at, until}, flip, plain (skips the hand-drawn wobble)
  DRAW.sprite = function (it, t) {
    if (!ART[it.kind]) throw new Error('sprite: unknown kind ' + it.kind);
    const p = place(it, t), pop = it.pop && it.t !== undefined ? .55 + .45 * back(clamp(ramp(t, it.t, it.t + .35))) : 1, k = p.s * pop * pulseK(it, t), art = ART[it.kind](it, t);
    let s = `<g transform="translate(${p.x} ${p.y}) rotate(${p.rot}) scale(${it.flip ? -k : k} ${k})"><g${it.plain ? '' : ' filter="url(#pr)"'}>${art}</g></g>`;
    const fs = it.fs || 44, w = it.kind === 'block' ? blockW(it, t) : 0, base = LOCAL_TOPLEFT[it.kind] ? [p.x + w / 2, p.y + (it.h || 0) / 2] : [p.x, p.y];
    const tp = it.tpos || [0, 0], tv = it.grow && t < it.grow.t + (it.grow.dur || .8) * .7 ? undefined : textOf(it, t);
    if (tv !== undefined && tv !== null) s += text(base[0] + tp[0], base[1] + tp[1] + fs * .35, tv, fs, { fill: it.tc || PAPER, w: it.tw || 800 });
    if (it.lines && !(it.grow && t < it.grow.t + (it.grow.dur || .8) * .7)) { const gap = fs * 1.22, y0 = base[1] + tp[1] - (it.lines.length - 1) * gap / 2 + fs * .35; it.lines.forEach((l, i) => { s += text(base[0] + tp[0], y0 + i * gap, l, fs, { fill: it.tc || INK, w: it.tw || 800 }); }); }
    const L = it.label; if (L && (L.t === undefined || t >= L.t) && (L.t_until === undefined || t < L.t_until)) { const a = L.t === undefined ? 1 : ramp(t, L.t, L.t + .25), lv = L.value ? valueText(L.value, t) : L.text, ly = p.y + (L.dy || 0), lx = p.x + (L.dx || 0);
      s += `<g opacity="${a}">` + (L.pill === false ? text(lx, ly, lv, L.fs || 44, { fill: col(L.tone || 'ink'), w: 800 }) : pill(lx, ly, lv, L.fs || 44, col(L.tone || 'blue'))) + '</g>'; }
    return s;
  };

  // The explainer engine's person with moves: walks with a little bob. Same fields as "person" plus moves
  DRAW.walker = function (it, t) { const p = place(it, t), bob = p.moving ? Math.abs(Math.sin(t * 13)) * 11 : 0, r = p.moving ? 3.5 * Math.sin(t * 13) : 0;
    return `<g transform="rotate(${r} ${p.x} ${p.y})">${DRAW.person(Object.assign({}, it, { x: p.x, y: p.y - bob, s: p.s }), t)}</g>`; };

  // People who come in, take a seat and leave. grid {x, y, cols, rows, dx, dy} = seats, (x, y) = the first person's feet. enter / exit = [door point, ...] in walking order.
  // arrive [{at, n, dur}] spreads n arrivals over dur seconds. When every seat has been taken, each arrival sends out the person in that seat, so the room stays full.
  // count {x, y, fs, tone, suffix} prints how many are inside
  const WHO = ['#dbe6fb', '#f6c9c4', '#bfe6cf', '#ffe2a8', '#c9d6f5', '#f4d3e5'], WALK = .95, LEAVE = .85;
  function along(pts, q) { const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; } let u = q * tot;
    for (let i = 0; i < L.length; i++) { if (u <= L[i]) { const p = L[i] ? u / L[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], p), lerp(pts[i][1], pts[i + 1][1], p)]; } u -= L[i]; } return pts[pts.length - 1]; }
  DRAW.flow = function (it, t) {
    const g = it.grid, N = g.cols * g.rows, s = it.s || .5, arr = [];
    it.arrive.forEach(a => { for (let i = 0; i < a.n; i++) arr.push(a.t + (a.dur || 0) * i / Math.max(1, a.n)); });
    const order = []; for (let r = g.rows - 1; r >= 0; r--) for (let c = 0; c < g.cols; c++) order.push([g.x + c * g.dx, g.y + r * g.dy]);   // front row first, so nobody walks through a seated person
    let out = '', walkers = '', inside = 0;
    const tb = ([x, y]) => `<ellipse cx="${x}" cy="${y - 22 * s}" rx="${70 * s}" ry="${20 * s}" fill="${WOOD}" stroke="${INK}" stroke-width="3.5"/>`;
    const rows = order.map(() => '');
    arr.forEach((a, i) => { if (t < a) return; const k = i % N, seat = order[k], lv = arr[i + N], gone = lv !== undefined && t >= lv + LEAVE; inside += 1; if (lv !== undefined && t >= lv) inside -= 1; if (gone) return;
      const c = WHO[(i * 5 + (i >> 2)) % WHO.length];
      if (t < a + WALK) { const q = ease((t - a) / WALK), [x, y] = along(it.enter.concat([seat]), q); walkers += `<g transform="translate(0 ${-Math.abs(Math.sin(t * 13 + i)) * 7})">${DRAW.person({ x, y, s, color: c }, t)}</g>`; }
      else if (lv !== undefined && t >= lv) { const q = ease((t - lv) / LEAVE), [x, y] = along([seat].concat(it.exit), q); walkers += `<g transform="translate(0 ${-Math.abs(Math.sin(t * 13 + i)) * 7})">${DRAW.person({ x, y, s, color: c }, t)}</g>`; }
      else rows[k] = DRAW.person({ x: seat[0], y: seat[1], s, color: c, mood: 'smile' }, t); });
    // back rows first; a table sits in front of each seated person
    for (let k = order.length - 1; k >= 0; k--) { out += rows[k] + tb(order[k]) + (rows[k] ? `<path d="M${order[k][0] - 11} ${order[k][1] - 40 * s} h22 v-${28 * s} h-22 Z" fill="${PAPER}" stroke="${INK}" stroke-width="3"/>` : ''); }
    let cnt = ''; if (it.count) cnt = pill(it.count.x, it.count.y, `${Math.min(inside, N)}${it.count.suffix || ''}`, it.count.fs || 48, col(it.count.tone || 'blue'));
    return out + walkers + cnt;
  };

  // A crowd as simple heads and shoulders or dots. n, cols, x, y (first one), dx, dy, r, tone. flips [{at, idx: [..], tone, until}] recolour some; "mini": true draws plain dots
  DRAW.dots = function (it, t) { let s = ''; for (let i = 0; i < it.n; i++) { const x = it.x + (i % it.cols) * it.dx, y = it.y + Math.floor(i / it.cols) * (it.dy || it.dx); let c = col(it.tone || 'blue'), pop = 1;
      (it.flips || []).forEach(f => { if (f.idx.includes(i) && t >= f.t && (f.t_until === undefined || t < f.t_until)) { c = col(f.tone || 'red'); pop = 1 + .28 * Math.sin(Math.PI * clamp((t - f.t) / .35)); } });
      s += it.mini ? `<circle cx="${x}" cy="${y}" r="${it.r * pop}" fill="${c}"/>` : `<g transform="translate(${x} ${y}) scale(${pop})"><circle cx="0" cy="${-it.r * .9}" r="${it.r * .7}" fill="${PAPER}" stroke="${INK}" stroke-width="3.5"/><path d="M${-it.r} ${it.r} V${it.r * .3} Q${-it.r} ${-it.r * .2} 0 ${-it.r * .2} Q${it.r} ${-it.r * .2} ${it.r} ${it.r * .3} V${it.r} Z" fill="${c}" stroke="${INK}" stroke-width="3.5"/></g>`; }
    return s; };
})();
