"""Helpers for writing a career-ladder reel script (skill edlintics-ladder-reel, 13 Nov 2026).

A reel's gen.py imports this file, describes the career (five outfits, five rung tags, the slider words), writes the rung scenes
by hand and lets the helpers draw the parts that are the same in every ladder reel: the room, the ladder shots (hook, climbs,
the "all five Ledgers" payoff) and the closing call-to-action scene. See example-audit-intern-to-cfo.py for a full reel.

Layout (meta.layout "ladder", meta.ladder_style "bleed"): frame [0, 0, 1080, 1920], so art coordinates are screen pixels.
  You compose with: rung title y 452-522 | duty chips y 534-670 | ground line y 1500 | UI zones: top 220, bottom 380, right 140 px
  rung scenes: keep faces, text and props in x 30-940, y 690-1500. Ladder scenes have no header, so they may start at y 450.
  Captions (13 Nov 2026): write() defaults to caption_pos "low": captions y 1320-1530, and it lifts every scene but the title and closing
  scenes by LIFT (220), so on screen the header is at y 240-310, chips y 322-458, content y 470-1280. write(..., caption_pos="top") keeps captions at y 228-438.
"""
import json, os

F = [0, 0, 1080, 1920]; GY = 1500; FEET = 1496
WALLS = {0: "#E8F0FC", 1: "#E3F3EA", 2: "#E6EEFD", 3: "#FDF0D9", 4: "#ECE7FA", 5: "#DCE4F3"}   # 0 = ladder shots, 1-5 = one wall per rung
LX = 230; RY = [1400, 1210, 1020, 830, 640]; LS = 0.8                 # ladder x, rung ys, Ledger scale on the ladder
SX = 30; SW_ = 180; RISE = 44; CS = 0.82                              # the steps of the title and closing scenes: left edge, step width, rise, Ledger scale
CTA = "To climb your own career ladder, learn technical business concepts at Edlintics"


def room(k):
    """The full-bleed wall and floor (wall colour k) with the light floor decoration. Always the first two items of a scene."""
    return [{"p": "backdrop", "x": 540, "y": GY, "w": 1400, "wall": WALLS[k], "up": 1700, "down": 600},
            {"p": "floor_deco", "x": 540, "y": GY}]


def led(x, s, outfit, **kw):
    """Ledger standing on the ground at x. s: 3.0-3.4 alone, 2.3-2.5 with small props, 1.9-2.0 beside a big prop."""
    return dict({"p": "ledger", "x": x, "y": FEET, "s": s, "outfit": outfit, "mood": "smile", "arm": "down"}, **kw)


def scene(k, *items):
    return {"bg": "none", "frame": F, "items": room(k) + [it for it in items if it]}


def B(role, img, text, chunks, rung=None, chips=None, **kw):
    """One beat. chunks: "words" or ("words", "key word"). chips: [("LABEL", chunk index in this beat)]."""
    b = {"role": role, "img": img, "text": text, "chunks": [({"text": c[0], "key": c[1]} if isinstance(c, tuple) else {"text": c}) for c in chunks]}
    if rung: b["rung"] = rung
    if chips: b["chips"] = [{"label": l, "at": a} for l, a in chips]
    b.update(kw); return b


class Ladder:
    """outfits: five Ledger outfits, bottom rung first. tags: five short rung labels for the ladder ("INTERN" ... "CFO").
    brackets: [(label, first rung, last rung, color)] groups beside the tags, or [] for none. dial: the slider's two words."""

    def __init__(self, outfits, tags, brackets=(), dial=("Counts", "Decides"), tag_w=None, tag_fs=46):
        assert len(outfits) == 5 and len(tags) == 5
        self.out = list(outfits); self.tags = list(tags); self.brackets = list(brackets); self.dial = tuple(dial)
        # with brackets the tags are 440 wide (the brackets need the room on the right); without, up to 540. Long labels need a smaller tag_fs:
        # "PORTFOLIO MANAGER" fits at tag_w 540, tag_fs 36. The build stops with a message if a label does not fit
        self.tag_w = tag_w or (440 if self.brackets else 540); self.tag_fs = tag_fs

    def tag(self, i, state, **kw):
        return dict({"p": "rung_tag", "x": LX + 162 + self.tag_w / 2, "y": RY[i], "label": self.tags[i], "state": state, "w": self.tag_w, "h": 96, "fs": self.tag_fs}, **kw)

    def base(self, pulses=None):
        """The ladder and its brackets. pulses: {bracket index: "chunk:N"} makes a bracket pulse on that chunk."""
        items = [{"p": "career_ladder", "x": LX, "y": RY[0], "n": 5, "gap": 190, "w": 220}]
        for n, (label, a, b, color) in enumerate(self.brackets):
            it = {"p": "side_bracket", "x": 856, "y": (RY[a] + RY[b]) / 2, "h": RY[a] - RY[b] + 96, "label": label, "color": color, "fs": 36}
            if pulses and n in pulses: it["pulse"] = {"at": pulses[n], "dur": 0.5, "amp": 0.09}
            items.append(it)
        return items

    def dial_item(self, x, y, w, fs=44, **kw):
        return dict({"p": "dial", "x": x, "y": y, "w": w, "fs": fs, "left": self.dial[0], "right": self.dial[1]}, **kw)

    def hook(self, top_chunk, sweep_chunk, wave_chunk, counter=None):
        """The opening ladder shot, used by the two hook beats. top_chunk: the chunk that names the top role (its tag pulses);
        sweep_chunk: the chunk on which the tags pulse one by one, bottom to top; wave_chunk: Ledger waves from the bottom rung.
        counter: {"to": 20, "unit": "years", "chunk": 1} ticks a number the voice says, or None."""
        items = self.base() + [self.tag(0, "now")]
        items += [self.tag(i, "todo", pulse={"at": f"chunk:{sweep_chunk}", "delay": 0.22 * i, "dur": 0.45, "amp": 0.1}) for i in (1, 2, 3)]
        items.append(self.tag(4, "todo", pulse=[{"at": f"chunk:{top_chunk}", "dur": 0.5, "amp": 0.12}, {"at": f"chunk:{sweep_chunk}", "delay": 0.88, "dur": 0.45, "amp": 0.1}]))
        if counter:
            items.append({"p": "counter", "x": 545, "y": 514, "start": 0, "to": counter["to"], "unit": counter.get("unit", ""), "fs": 76, "color": "blue", "at": f"chunk:{counter['chunk']}", "dur": 1.0})
        items += [{"p": "ledger", "x": LX, "y": RY[0], "s": LS, "outfit": self.out[0], "mood": "smile", "arm": "down", "until": f"chunk:{wave_chunk}"},
                  {"p": "ledger", "x": LX, "y": RY[0], "s": LS, "outfit": self.out[0], "mood": "happy", "arm": "wave", "at": f"chunk:{wave_chunk}", "pop": "cut"}]
        return scene(0, *items)

    def climb(self, k, go=0, name=1, pulses=None):
        """Ledger climbs from rung k to rung k + 1 (k = 0-3) and changes clothes on arrival. go: the chunk he starts on
        (the move takes about 1 s); name: the chunk that names the next role (its tag lights up, the old one gets its tick)."""
        y0, y1 = RY[k], RY[k + 1]; g = f"chunk:{go}"; nm = f"chunk:{name}"
        mv = [{"at": g, "delay": 0.15, "dur": 0.42, "to": [LX + 14, (y0 + y1) / 2], "ease": "inout", "rot": 4},
              {"at": g, "delay": 0.6, "dur": 0.42, "to": [LX, y1], "ease": "inout", "rot": 0}]
        items = self.base(pulses)
        for i in range(5):
            if i < k: items.append(self.tag(i, "done"))
            elif i == k: items += [self.tag(i, "now", until=nm), self.tag(i, "done", at=nm, pop="cut")]
            elif i == k + 1: items += [self.tag(i, "todo", until=nm), self.tag(i, "now", at=nm)]
            else: items.append(self.tag(i, "todo"))
        items += [{"p": "burst", "x": LX, "y": y1 - 92, "s": 1.3, "color": "amber", "at": g, "delay": 1.0},   # listed before Ledger, so it never covers him
                  {"p": "ledger", "x": LX, "y": y0, "s": LS, "outfit": self.out[k], "mood": "smile", "arm": "both_up", "move": mv, "out": {"at": g, "delay": 1.0, "dur": 0.1}},
                  {"p": "ledger", "x": LX, "y": y0, "s": LS, "outfit": self.out[k + 1], "mood": "happy", "arm": "up", "move": mv, "appear": {"at": g, "delay": 0.98}}]
        return scene(0, *items)

    def all(self, slide_chunk=1):
        """The payoff shot: all five Ledgers on the ladder, every tag ticked, the slider running from one end to the other."""
        items = self.base() + [self.tag(i, "done") for i in range(4)] + [self.tag(4, "now")]
        items.append(self.dial_item(540, 524, 420, 36, start=0.06, slide={"at": f"chunk:{slide_chunk}", "to": 0.95, "dur": 1.8}))
        items += [{"p": "ledger", "x": LX, "y": RY[i], "s": LS, "outfit": self.out[i], "mood": "happy" if i == 4 else "smile", "arm": "wave" if i == 4 else "down",
                   "appear": {"at": "chunk:0", "delay": 0.05 + 0.28 * i}} for i in range(5)]
        return scene(0, *items)

    def cta(self):
        """The closing scene: the five Ledgers side by side on rising wooden steps; the renderer puts the full-width message card and logo above them (y 560-1070)."""
        items = [{"p": "steps", "x": SX, "y": GY, "n": 5, "step_w": SW_, "rise": RISE}]
        items += [{"p": "ledger", "x": SX + (i + 0.5) * SW_, "y": GY - (i + 1) * RISE - 6, "s": CS, "outfit": self.out[i], "mood": "happy", "arm": "wave" if i == 4 else "down",
                   "pulse": {"at": "chunk:0", "delay": 0.3 + 0.18 * i, "dur": 0.45, "amp": 0.1}} for i in range(5)]
        return scene(0, *items)

    def title(self):
        """The opening scene (beat 1): a ladder rising behind the steps (it runs up behind the title card) and the first Ledger waving from the lowest step; the renderer puts the title card above, complete on frame 1."""
        return scene(0, {"p": "career_ladder", "x": SX + 4.5 * SW_, "y": GY - 5 * RISE - 70, "n": 4, "gap": 150, "w": 150},
                     {"p": "steps", "x": SX, "y": GY, "n": 5, "step_w": SW_, "rise": RISE},
                     {"p": "ledger", "x": SX + 0.5 * SW_, "y": GY - RISE - 6, "s": CS, "outfit": self.out[0], "mood": "happy", "arm": "wave"},
                     {"p": "arrow", "x": SX + 1.3 * SW_, "y": GY - 2.6 * RISE - 150, "dx": 2.3 * SW_, "dy": -2.3 * RISE, "color": "blue", "s": 1.0, "dashed": True})

    def title_beat(self, frm, to, seconds_word="ninety seconds", tag="IN 90 SECONDS", chunks=None):
        """Beat 1 (Hoang, 13 Nov 2026: no hook, say what the video is). Voice: "From <frm> to <to>, the career ladder explained with Ledger in ninety seconds."
        The card shows the same sentence without the length, and the tag pill carries the length. Only claim a length the video really has:
        if timing.json says more than 90 s, use seconds_word="under two minutes", tag="IN UNDER 2 MINUTES"."""
        msg = f"From {frm} to {to}, the career ladder explained with Ledger"
        return B("title", "title", f"{msg} in {seconds_word}.", chunks or [f"From {frm}", f"to {to}", "the career ladder", ("explained with Ledger", "Ledger")], message=msg, tag=tag, gap=0.3)

    def cta_beat(self):
        """The closing beat, the same sentence in every ladder reel. "say" spells the name so the voice reads ED-lin-tiks."""
        return B("cta", "cta", CTA + ".", ["To climb your own", "career ladder", "learn technical", "business concepts", ("at Edlintics", "Edlintics")],
                 say=CTA.replace("Edlintics", "Ed-lin-tics") + ".", message=CTA)


LIFT = 220   # low captions: how far write() lifts the rung and ladder scenes, so the ground line sits at y 1280 and captions (y 1320-1530) cover only floor


def lift_scene(spec, dy=LIFT):
    """A copy of a scene moved up by dy: every item's y, every "to" target (moves, coin streams), and a taller floor under the backdrop."""
    def up(v):
        if isinstance(v, dict):
            return {k: ([x[0], x[1] - dy] if k == "to" and isinstance(x, list) and len(x) == 2 and all(isinstance(n, (int, float)) for n in x) else up(x)) for k, x in v.items()}
        if isinstance(v, list): return [up(x) for x in v]
        return v
    items = []
    for it in spec.get("items", []):
        it = up(it); it["y"] = it["y"] - dy
        if it["p"] == "backdrop": it["down"] = it.get("down", 500) + dy
        items.append(it)
    return dict(spec, items=items)


def write(folder, meta, scenes, beats, caption_pos="low"):
    """Write script.json. caption_pos "low" (the default from 13 Nov 2026, Hoang: "make it the rule for all videos now to be at bottom half center"):
    captions sit at y 1320-1530, the rung header, chips and logo move to the top (y 240-460), and every scene except the title and closing scenes
    is lifted by LIFT, so you still compose scenes with the ground at y 1500 (GY) as before. caption_pos "top" keeps the 13 Nov layout (captions y 228-438)
    for reels rendered before the rule."""
    meta = dict({"type": "ladder", "layout": "ladder", "ladder_style": "bleed"}, **meta)
    if caption_pos == "low":
        meta["caption_pos"] = "low"
        fixed = {b.get("img") for b in beats if b.get("role") in ("title", "cta")}   # their cards sit at y 560, with no captions: unchanged
        scenes = {k: (v if k in fixed else lift_scene(v)) for k, v in scenes.items()}
    elif caption_pos != "top": raise ValueError('caption_pos must be "low" or "top"')
    json.dump({"meta": meta, "scenes": scenes, "beats": beats}, open(os.path.join(folder, "script.json"), "w"), indent=1, ensure_ascii=False)
    print("script.json:", len(scenes), "scenes,", len(beats), "beats,", sum(len(b["text"].split()) for b in beats), "words, captions", caption_pos)
