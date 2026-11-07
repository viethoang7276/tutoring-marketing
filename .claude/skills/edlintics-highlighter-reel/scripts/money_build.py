"""Edlintics "Where your money goes" reel builder (a sibling of the highlighter reel, sharing its desk, sheet, captions,
end card, voice and checks). One horizontal price bar on the printed sheet fills slice by slice as the voice names each
slice; the main slice is highlighted at the turn; the takeaway shrinks one slice and counts the total down.
9:16 1080x1920, 24 fps, H.264 + AAC, ElevenLabs v3 with word timings (tts_align.py), optional music bed mixed locally.

Usage (money_build.sh wraps this):  money_build.sh <script.json> <outdir>
  STILLS_ONLY=1 money_build.sh ...   timeline, audio, stills and contact sheet only
Outputs in <outdir>: <slug>.mp4, <slug>-contact-sheet.png (one frame per beat), <slug>-poster.jpg, stills/, timeline.json,
audio-voice.wav (voice only, -14 LUFS), audio.wav (voice + bed), script.txt
Does not change build.py or render.html: the highlighter reel builds exactly as before.
"""
import json, os, re, shutil, subprocess, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as HB   # the highlighter engine: measure(), check(), FF, NODE_PATH, REPO, norm
import tts_align
SR = 24000; FF = HB.FF; REPO = HB.REPO; norm = HB.norm
ACTIONS = ("pulse", "half", "row", "fill", "focus", "unfocus", "bracket", "chain", "chainends", "shrink")


def validate(S):
    E = []
    shown = S["title"] + [S["label"], S["total_label"], S["small_print"]] + [s["name"] for s in S["slices"]] + \
            [S["chain"]["from"], S["chain"]["to"], S["endcard"]["term"], S["endcard"]["keypoint"], S["endcard"]["follow"]]
    caps = [c["text"] for b in S["beats"] for c in b["chunks"]]
    for s in shown + caps + [b["text"] for b in S["beats"]] + [S["endcard"]["say"]]:
        if "!" in s: E.append(f"exclamation point: {s}")
        if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", s): E.append(f"emoji: {s}")
    for s in shown + caps:
        if s.rstrip().endswith("."): E.append(f"on-screen line ends with a full stop: {s}")
    tot = round(sum(s["amount"] for s in S["slices"]), 2)
    if abs(tot - S["total"]) > 0.005: E.append(f"slices add up to {tot}, not the total {S['total']}")
    ids = {s["id"] for s in S["slices"]}
    for b in S["beats"]:
        words = b["text"].split(); n = sum(c.get("n", len(c["text"].split())) for c in b["chunks"])
        if n != len(words): E.append(f"chunk word counts ({n}) do not match the spoken words ({len(words)}): {b['text']}")
        if not b["text"].rstrip().endswith((".", "?")): E.append(f"voice line is not a full sentence: {b['text']}")
        for c in b["chunks"]:
            if c["text"].rstrip()[-1:] in ".,;:": E.append(f"caption chunk ends in punctuation: {c['text']}")
            if len(c["text"].split()) > 4: E.append(f"caption chunk over 4 words: {c['text']}")
            if c.get("key") and c["key"] not in c["text"]: E.append(f"key '{c['key']}' not in chunk '{c['text']}'")
        for d in b["do"]:
            kind = next((k for k in ACTIONS if k in d), None)
            if not kind: E.append(f"unknown action {d}")
            elif kind in ("row", "fill", "focus") and d[kind] not in ids: E.append(f"unknown slice '{d[kind]}' in {d}")
    wc = sum(len(b["text"].split()) for b in S["beats"]) + len(S["endcard"]["say"].split())
    print("words:", wc)
    for e in E: print("FAIL", e)
    if E: sys.exit(1)


def tick(buf, t, amp):
    """Soft wooden tick when a slice lands: a short decaying 900 Hz tone with a little noise"""
    i = int(t * SR); L = int(0.09 * SR)
    if i + L > len(buf): return
    tt = np.arange(L) / SR; rng = np.random.default_rng(int(t * 1000))
    s = (np.sin(2 * np.pi * 900 * tt) + 0.3 * rng.standard_normal(L)) * np.exp(-tt / 0.018)
    buf[i:i + L] += amp * s


def loud_to(src, dst, target, ch):
    """Normalise a wav to a target integrated loudness (ffmpeg ebur128 measure, gain, soft limiter), 48 kHz"""
    I, _ = HB.measure(src); gain = target - I
    for _ in range(5):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-af", f"aresample=48000,volume={gain:.2f}dB,alimiter=limit=0.89:attack=4:release=60:level=0",
                        "-ac", str(ch), "-ar", "48000", dst], check=True)
        I2, pk = HB.measure(dst)
        if abs(I2 - target) < 0.25: break
        gain += target - I2
    return I2, pk


def make_audio(T, clips, S, out):
    N = int(T["dur"] * SR); vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    for at, a in clips: i = int(at * SR); vo[i:i + len(a)] += a[:N - i]
    ref = np.abs(vo).max()
    for a in T["actions"]:
        if a["kind"] == "fill": tick(fx, a["t1"] - 0.04, 0.10 * ref)
    mix = vo + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
    raw = f"{out}/audio-raw.wav"; sf.write(raw, mix, SR)
    I, pk = loud_to(raw, f"{out}/audio-voice.wav", -14.0, 1); print(f"voice-only {I:.1f} LUFS, peak {pk:.1f} dBFS")
    M = S.get("music") or {}; bedp = os.environ.get("MUSIC_BED") or (M.get("bed") and os.path.join(REPO, M["bed"]))
    if not bedp or not os.path.exists(bedp):
        print("WARN no music bed found: the video has the voice only"); shutil.copy(f"{out}/audio-voice.wav", f"{out}/audio.wav"); return f"{out}/audio.wav", None
    # the bed sits a fixed number of LU under the voice (the 1 Nov list reels: voice -18.5, bed -30.9 LUFS, stereo), then the
    # whole mix is set to the target loudness
    v2, _ = sf.read(f"{out}/audio-voice.wav", dtype="float32"); v2 = np.stack([v2, v2], 1)
    bed, bsr = sf.read(bedp, dtype="float32")
    assert bsr == 48000 and bed.ndim == 2, "bed must be 48 kHz stereo"
    n = len(v2)
    if len(bed) < n: bed = np.concatenate([bed] * (n // len(bed) + 1))
    bed = bed[:n].copy(); tt = np.arange(n) / 48000
    bed *= (np.clip(tt / 0.6, 0, 1) * np.clip((tt[-1] - tt) / 0.8, 0, 1))[:, None]   # short fade in, fade out under the loop point
    sf.write(f"{out}/_v2.wav", v2, 48000); sf.write(f"{out}/_bed.wav", bed, 48000)
    Iv, _ = HB.measure(f"{out}/_v2.wav"); Ib, _ = HB.measure(f"{out}/_bed.wav")
    g = 10 ** ((Iv - M.get("bed_below_voice_lu", 12.4) - Ib) / 20)
    sf.write(f"{out}/_mix.wav", np.clip(v2 + g * bed, -1, 1), 48000)
    I2, pk = loud_to(f"{out}/_mix.wav", f"{out}/audio.wav", M.get("target_lufs", -17.5), 2)
    for f in ("_v2", "_bed", "_mix"): os.remove(f"{out}/{f}.wav")
    print(f"mix {I2:.1f} LUFS, peak {pk:.1f} dBFS, bed {M.get('bed_below_voice_lu', 12.4)} LU under the voice ({os.path.basename(bedp)})")
    return f"{out}/audio.wav", I2


def node(args, tp):
    env = dict(os.environ, NODE_PATH=HB.NODE_PATH, FFMPEG=FF, TIMELINE=tp, RENDER_PAGE="money_render.html")
    subprocess.run(["node", f"{HERE}/render.cjs", *args], check=True, env=env)


def contact(out, shots, dst):
    from PIL import Image, ImageDraw, ImageFont
    w, h, cols = 324, 576, 5; rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 64) + 12), "#e9ecf2"); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except Exception: font = ImageFont.load_default()
    for k, (t, lab) in enumerate(shots):
        im = Image.open(f"{out}/stills/still-{t:.2f}.png").convert("RGB").resize((w, h), Image.LANCZOS)
        x = 12 + (k % cols) * (w + 12); y = 12 + (k // cols) * (h + 64); sheet.paste(im, (x, y))
        d.text((x, y + h + 6), f"{t:.2f} s  {lab}", fill="#0d1523", font=font)
    sheet.save(dst); print("contact sheet", dst)


def build(sp, out):
    S = json.load(open(sp)); slug = S["slug"]; validate(S); os.makedirs(out, exist_ok=True)
    TM = {"lead": 0.45, "gap": 0.25, "end_gap": 0.45, "tail": 1.6, **S.get("timing", {})}
    clips, chunks, actions, beats = [], [], [], []
    t = TM["lead"]
    for bi, b in enumerate(S["beats"]):
        a, words = tts_align.say_words(b["text"]); dur = len(a) / SR; spoken = b["text"].split()
        if len(words) != len(spoken):
            print(f"WARN beat {bi+1}: {len(words)} aligned words vs {len(spoken)} spoken; using proportional timing")
            L = sum(len(w) for w in spoken); acc = 0; words = []
            for w in spoken: words.append((w, dur * acc / L, dur * (acc + len(w)) / L)); acc += len(w) + 1
        W = [(norm(w), t + s, t + e) for w, s, e in words]
        clips.append((t, a)); beats.append({"text": b["text"], "start": round(t, 3), "end": round(t + dur, 3)})
        k = 0
        for c in b["chunks"]:
            n = c.get("n", len(c["text"].split()))
            chunks.append({"text": c["text"], "key": c.get("key"), "t": round(W[k][1] - 0.06, 3)}); k += n
        def when(x):
            if isinstance(x, (int, float)): return t + x
            for w, s, e in W:
                if w == norm(x): return s
            raise SystemExit(f"word '{x}' not found in beat {bi+1}: {b['text']}")
        for d in b["do"]:
            kind = next(k2 for k2 in ACTIONS if k2 in d)
            t0 = when(d.get("at", 0)) + d.get("shift", 0)
            t1 = when(d["until"]) if "until" in d else t0 + d.get("dur", {"fill": 0.6, "row": 0.35, "shrink": 1.6}.get(kind, 0.5))
            actions.append({"kind": kind, "arg": d[kind], "beat": bi, "t0": round(t0, 3), "t1": round(max(t1, t0 + 0.25), 3)})
        t += dur + TM["gap"]
    end_t = t - TM["gap"] + 0.1
    for i, c in enumerate(chunks):
        nxt = chunks[i + 1]["t"] if i + 1 < len(chunks) else 1e9
        bend = next(bb["end"] for bb in beats[::-1] if bb["start"] <= c["t"] + 0.07)
        c["t_end"] = round(min(nxt, bend + 0.25, end_t), 3)
    ea, _ = tts_align.say_words(S["endcard"]["say"]); es = end_t + TM["end_gap"]; clips.append((es, ea))
    dur = round(round((es + len(ea) / SR + TM["tail"]) * 24) / 24, 4)
    T = {"dur": dur, "end_t": round(end_t, 3), "end_kp_t": round(es + 0.6, 3), "beats": beats, "chunks": chunks, "actions": actions,
         "endcard": S["endcard"], "sheet": {k: S[k] for k in ("title", "label", "total_label", "small_print", "total", "slices", "shrink", "chain")}}
    tp = f"{out}/timeline.json"; json.dump(T, open(tp, "w"), indent=1)
    print(f"duration {dur} s, end card at {T['end_t']} s, {len(actions)} actions")
    if not 28 <= dur <= 35.5: print(f"WARN duration {dur} s is outside 28-35 s")
    audio, _ = make_audio(T, clips, S, out)
    open(f"{out}/script.txt", "w").write("\n".join(f"{b['start']:5.2f}  {b['text']}" for b in beats) + f"\n{es:5.2f}  {S['endcard']['say']}\n")
    # one frame per beat (just before the next beat starts, so that beat's animation has finished), the opening frame and the end card
    shots = [(0.2, "opening")] + [(round(min(b["end"] + 0.05, end_t - 0.05), 2), f"beat {i+1}") for i, b in enumerate(beats)] + \
            [(round(es + len(ea) / SR, 2), "end card"), (round(dur - 0.05, 2), "loop frame")]
    shutil.rmtree(f"{out}/stills", ignore_errors=True)
    node(["stills", ",".join(f"{x:.2f}" for x, _ in shots), f"{out}/stills"], tp)
    contact(out, shots, f"{out}/{slug}-contact-sheet.png")
    from PIL import Image
    Image.open(f"{out}/stills/still-{shots[0][0]:.2f}.png").convert("RGB").save(f"{out}/{slug}-poster.jpg", quality=90)
    if not os.environ.get("STILLS_ONLY"):
        mp4 = f"{out}/{slug}.mp4"; node(["video", mp4, audio], tp); HB.check(mp4, dur)


if __name__ == "__main__":
    build(sys.argv[1], os.path.abspath(sys.argv[2]))
