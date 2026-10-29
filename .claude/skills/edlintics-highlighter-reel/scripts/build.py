"""Edlintics highlighter reel builder: a printed Edlintics sheet on a desk, a drawn hand highlights it in time with the voice.
9:16 1080x1920, 24 fps, H.264 + AAC, voice ElevenLabs v3 (word timings from the with-timestamps API), -14 LUFS.

Usage (build.sh wraps this):  build.sh <script.json> <outdir>
  STILLS_ONLY=1 build.sh ...   timeline, audio, stills and contact sheet only (quick layout check)
Outputs in <outdir>: <slug>.mp4, <slug>-contact-sheet.png, <slug>-poster.jpg, stills/, timeline.json, audio.wav, script.txt
"""
import json, os, re, shutil, subprocess, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing"
NODE_PATH = f"{REPO}/.claude/skills/edlintics-explainer-reel/scripts/node_modules"
sys.path.insert(0, HERE)
import tts_align, imageio_ffmpeg
sys.path.insert(0, f"{REPO}/.claude/skills/edlintics-explainer-reel/scripts")
import scene_lib   # Ledger is drawn by the explainer engine's scene library, never redrawn here
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 24000
GAP = float(os.environ.get("VO_GAP", "0.25")); LEAD = 0.45
norm = lambda w: re.sub(r"[^\w$%']", "", w).lower()


def validate(S):
    E = []
    alltext = [b["text"] for b in S["beats"]] + [c["text"] for b in S["beats"] for c in b["chunks"]] + list(S["endcard"].values())
    for s in alltext:
        if "!" in s: E.append(f"exclamation point: {s}")
        if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", s): E.append(f"emoji: {s}")
        if "€" in s: E.append(f"euro sign (use US dollars): {s}")
    for b in S["beats"]:
        words = b["text"].split(); n = sum(c.get("n", len(c["text"].split())) for c in b["chunks"])
        if n != len(words): E.append(f"chunk word counts ({n}) do not match the spoken words ({len(words)}): {b['text']}")
        for c in b["chunks"]:
            if c["text"].rstrip()[-1:] in ".,;:": E.append(f"caption chunk ends in punctuation: {c['text']}")
            if len(c["text"].split()) > 4: E.append(f"caption chunk over 4 words: {c['text']}")
            if c.get("key") and c["key"] not in c["text"]: E.append(f"key '{c['key']}' not in chunk '{c['text']}'")
        if not b.get("do"): E.append(f"beat has no highlight: {b['text']}")
    sheet = open(os.path.join(S["_base"], S["sheet"])).read()
    fams = set(re.findall(r'font-family="([^"]+)"', sheet)) | set(re.findall(r"font-family:\s*([^;\"]+)", sheet))
    if fams - {"Inter"}: E.append(f"sheet uses fonts other than Inter: {sorted(fams - {'Inter'})} (house style is Inter only)")
    for b in S["beats"]:
        for a in b.get("ledger", []):
            for k in a:
                if k not in ("at", "shift", "arm", "mood", "pick", "drop", "hop"): E.append(f"unknown ledger key '{k}' in: {b['text']}")
            if a.get("arm") and a["arm"] not in scene_lib.ARM_POSES: E.append(f"unknown Ledger arm pose '{a['arm']}'")
            if a.get("mood") and a["mood"] not in scene_lib.MOODS: E.append(f"unknown Ledger mood '{a['mood']}'")
    for k in ("term", "keypoint", "follow"):
        if S["endcard"][k].rstrip().endswith("."): E.append(f"end card {k} ends with a full stop")
    wc = sum(len(b["text"].split()) for b in S["beats"]) + len(S["endcard"]["say"].split())
    print("words:", wc)
    if not 70 <= wc <= 115: E.append(f"{wc} spoken words; aim for 75-105 (30-40 s)")
    for e in E: print("FAIL", e)
    if E: sys.exit(1)


def build(sp, out):
    S = json.load(open(sp)); base = os.path.dirname(os.path.abspath(sp)); slug = S["slug"]; S["_base"] = base
    validate(S); os.makedirs(out, exist_ok=True)
    clips, chunks, actions, beats, lkeys = [], [], [], [], []
    t = LEAD
    for bi, b in enumerate(S["beats"]):
        a, words = tts_align.say_words(b["text"]); dur = len(a) / SR
        spoken = b["text"].split()
        if len(words) != len(spoken):   # alignment splits differently (for example "8%"): fall back to proportional timing
            print(f"WARN beat {bi+1}: {len(words)} aligned words vs {len(spoken)} spoken; using proportional timing")
            L = sum(len(w) for w in spoken); acc = 0; words = []
            for w in spoken: words.append((w, dur * acc / L, dur * (acc + len(w)) / L)); acc += len(w) + 1
        W = [(norm(w), t + s, t + e) for w, s, e in words]
        clips.append((t, a)); beats.append({"text": b["text"], "start": round(t, 3), "end": round(t + dur, 3)})
        k = 0
        for c in b["chunks"]:
            n = c.get("n", len(c["text"].split()))
            chunks.append({"text": c["text"], "key": c.get("key"), "t": round(W[k][1] - 0.06, 3)}); k += n
        def when(x, default):
            if x is None: return default
            if isinstance(x, (int, float)): return t + x
            for w, s, e in W:
                if w == norm(x): return s
            raise SystemExit(f"word '{x}' not found in beat {bi+1}: {b['text']}")
        for d in b["do"]:
            t0 = when(d.get("at"), t) + d.get("shift", 0)
            if "until" in d: t1 = when(d["until"], None)
            else: t1 = t0 + d.get("dur", 0.55 if "mark" in d else 1.0)
            actions.append({**{k2: v for k2, v in d.items() if k2 not in ("at", "until", "dur", "shift")}, "t0": round(t0, 3), "t1": round(max(t1, t0 + 0.3), 3)})
        for d in b.get("ledger", []):   # Ledger's acting, timed from the same real word times
            lkeys.append({**{k2: v for k2, v in d.items() if k2 not in ("at", "shift")}, "t": round(when(d.get("at"), t) + d.get("shift", 0), 3)})
        t += dur + GAP
    # captions end where the next one starts (or at the end of their beat + 0.25 s)
    for i, c in enumerate(chunks):
        nxt = chunks[i + 1]["t"] if i + 1 < len(chunks) else 1e9
        bend = next(bb["end"] for bb in beats[::-1] if bb["start"] <= c["t"] + 0.07)
        c["t_end"] = round(min(nxt, bend + 0.25), 3)
    # the hand needs time to travel: keep at least 0.22 s between actions
    for p, q in zip(actions, actions[1:]):
        if q["t0"] < p["t1"] + 0.22:
            p["t1"] = round(max(p["t0"] + 0.3, q["t0"] - 0.22), 3)
            if q["t0"] < p["t1"] + 0.22: print(f"WARN actions too close at {q['t0']} s")
    end_t = t + 0.15
    ea, _ = tts_align.say_words(S["endcard"]["say"]); es = end_t + 0.45; clips.append((es, ea))
    dur = round(round((es + len(ea) / SR + 1.6) * 24) / 24, 4)
    T = {"dur": dur, "end_t": round(end_t, 3), "end_kp_t": round(es + 0.75, 3), "beats": beats, "chunks": chunks, "actions": actions,
         "endcard": S["endcard"], "sheet_svg": re.sub(r"<!--.*?-->", "", open(os.path.join(base, S["sheet"])).read(), flags=re.S)}
    if S.get("ledger"): T["ledger"] = {**S["ledger"], "keys": sorted(lkeys, key=lambda k: k["t"]), "parts": ledger_parts(S["ledger"].get("outfit", "suit"))}
    tp = f"{out}/timeline.json"; json.dump(T, open(tp, "w"), indent=1)
    print(f"duration {dur} s, end card at {T['end_t']} s, {len(actions)} highlights")
    if not 30 <= dur <= 41: print(f"WARN duration {dur} s is outside 30-40 s; try ELEVEN_TEMPO=1.16 or trim words")
    audio = make_audio(T, clips, out)
    open(f"{out}/script.txt", "w").write("\n".join(f"{b['start']:5.2f}  {b['text']}" for b in beats) + f"\n{es:5.2f}  {S['endcard']['say']}\n")
    times = sorted({round(a["t1"] + 0.12, 2) for a in actions} | {0.2, round(T["end_t"] + 2.0, 2), round(dur - 0.05, 2)})
    shutil.rmtree(f"{out}/stills", ignore_errors=True)
    node(["stills", ",".join(f"{x:.2f}" for x in times), f"{out}/stills"], tp)
    contact(out, times, f"{out}/{slug}-contact-sheet.png")
    from PIL import Image
    Image.open(f"{out}/stills/still-{times[0]:.2f}.png").convert("RGB").save(f"{out}/{slug}-poster.jpg", quality=90)
    if not os.environ.get("STILLS_ONLY"):
        mp4 = f"{out}/{slug}.mp4"; node(["video", mp4, audio], tp); check(mp4, dur)


def ledger_parts(outfit):
    """Ledger split into legs, one body per mood (face included) and the arm poses, all from scene_lib.ledger(), so the
    renderer can move his arms smoothly between poses and cross-fade faces without redrawing him"""
    L, R = scene_lib.ARM_POSES["down"]["L"], scene_lib.ARM_POSES["down"]["R"]
    arms = scene_lib._arm(*L), scene_lib._arm(*R); legs, bodies = None, {}
    for m in scene_lib.MOODS:
        if m == "talk": continue
        svg = scene_lib.ledger(0, 0, 1, mood=m, arm="down", outfit=outfit)
        for a in arms: assert a in svg; svg = svg.replace(a, "")
        head, rest = svg.split('<g transform="rotate(0 120 198)">', 1)
        legs = head[head.index(">") + 1:]; bodies[m] = rest[:-len("</g></g>")]
    return {"legs": legs, "bodies": bodies, "arms": scene_lib.ARM_POSES, "ink": scene_lib.INK, "paper": scene_lib.PAPER, "gold": scene_lib.GOLD}


def marker_sound(buf, t0, t1, amp):
    """Soft felt-tip squeak: band-limited noise with a slow wobble, faded in and out"""
    L = int((t1 - t0) * SR); i = int(t0 * SR)
    if L <= 0: return
    rng = np.random.default_rng(int(t0 * 1000)); nz = rng.standard_normal(L + 64)
    hp = nz[1:] - 0.97 * nz[:-1]; lp = np.convolve(hp, np.ones(6) / 6, mode="same")[:L]
    tt = np.arange(L) / SR; env = np.clip(tt / 0.05, 0, 1) * np.clip((L / SR - tt) / 0.08, 0, 1) * (0.75 + 0.25 * np.sin(2 * np.pi * 7 * tt))
    buf[i:i + L] += amp * (lp * env)[:len(buf) - i]


def measure(wav):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", s).group(1))


def make_audio(T, clips, out):
    N = int(T["dur"] * SR); vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    for at, a in clips: i = int(at * SR); vo[i:i + len(a)] += a[:N - i]
    ref = np.abs(vo).max()
    for a in T["actions"]: marker_sound(fx, a["t0"], a["t1"], 0.05 * ref)
    mix = vo + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
    raw = f"{out}/audio-raw.wav"; sf.write(raw, mix, SR); I, _ = measure(raw); gain = -14.0 - I; dst = f"{out}/audio.wav"
    for _ in range(4):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", f"aresample=48000,volume={gain:.2f}dB,alimiter=limit=0.74:attack=4:release=60:level=0",
                        "-ar", "48000", dst], check=True)
        I2, pk = measure(dst)
        if abs(I2 + 14) < 0.3: break
        gain += -14 - I2
    print(f"audio {I2:.1f} LUFS, peak {pk:.1f} dBFS"); return dst


def node(args, tp):
    env = dict(os.environ, NODE_PATH=NODE_PATH, FFMPEG=FF, TIMELINE=tp)
    subprocess.run(["node", f"{HERE}/render.cjs", *args], check=True, env=env)


def contact(out, times, dst):
    from PIL import Image, ImageDraw, ImageFont
    w, h, cols = 324, 576, 5; rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 40) + 12), "#e9ecf2"); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except Exception: font = ImageFont.load_default()
    for k, t in enumerate(times):
        im = Image.open(f"{out}/stills/still-{t:.2f}.png").convert("RGB").resize((w, h), Image.LANCZOS)
        x = 12 + (k % cols) * (w + 12); y = 12 + (k // cols) * (h + 40); sheet.paste(im, (x, y)); d.text((x, y + h + 6), f"{t:.2f} s", fill="#0d1523", font=font)
    sheet.save(dst); print("contact sheet", dst)


def check(mp4, dur):
    r = subprocess.run([FF, "-hide_banner", "-i", mp4], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); d = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    E = []
    if "1080x1920" not in r: E.append("not 1080x1920")
    if "Audio:" not in r: E.append("no audio")
    if abs(d - dur) > 0.3: E.append(f"length {d:.2f} s vs timeline {dur} s")
    mb = os.path.getsize(mp4) / 1e6
    if mb >= 10: E.append(f"{mb:.1f} MB (keep under 10 MB for uploads)")
    print(f"{mp4}: {d:.2f} s, {mb:.1f} MB"); [print("FAIL", e) for e in E]; print("CHECK", "OK" if not E else "NOT OK")


if __name__ == "__main__":
    build(sys.argv[1], os.path.abspath(sys.argv[2]))
