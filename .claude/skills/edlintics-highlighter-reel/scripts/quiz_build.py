"""Quiz-sheet reel (variant of the highlighter reel, 19 Nov 2026): a printed Edlintics quiz sheet on the desk, a drawn hand
with a blue pen underlines each question while the voice reads it, a 5-second countdown runs, then the pen ticks the answer
on the word that names it. The sheet scrolls up question by question. Ends on "How many did you get?" with Ledger.

Usage:  tools/tts/.venv/bin/python quiz_build.py <quiz.json> <outdir>      (STILLS_ONLY=1 for timeline, audio and stills)
Spec: see assets/renders/explainer-reels/w47/paper-accounting-quiz-7/quiz.json
Outputs in <outdir>: <slug>.mp4 (voice + pen + countdown ticks, no music), <slug>-contact-sheet.png, stills/, timeline.json, script.txt
"""
import json, os, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B          # measure, node, contact, check, marker_sound, scene_lib, norm, FF
import tts_align
SR = 24000


def find(words, key, after=0.0):
    k = B.norm(key)
    for w, s, e in words:
        if B.norm(w) == k and s >= after: return s, e
    raise SystemExit(f"word {key!r} not found in {[w for w, _, _ in words]}")


def tick_sound(n=None):
    """Soft clock tick: a 2.4 kHz blip with a little noise, 40 ms, fast decay"""
    L = int(0.04 * SR); tt = np.arange(L) / SR; rng = np.random.default_rng(7)
    return ((0.6 * np.sin(2 * np.pi * 2400 * tt) + 0.4 * rng.standard_normal(L)) * np.exp(-tt / 0.008)).astype(np.float32)


def build(sp, out):
    Q = json.load(open(sp)); os.makedirs(out, exist_ok=True)
    clips, fx_ticks, acts, lines = [], [], [], []
    def say(text):
        a, w = tts_align.say_words(text); lines.append(text); return a, w, len(a) / SR
    t = 0.8
    a, w, d = say(Q["intro"]); clips.append((t, a))
    s, _ = find(w, Q.get("intro_ul", Q["title"].split()[0]))
    T = {"slug": Q["slug"], "title": Q["title"], "subtitle": Q.get("subtitle", ""), "end_lines": Q["end_lines"],
         "intro": {"t": t, "t_end": t + d, "ul_t0": t + s, "ul_t1": t + s + 1.0}, "questions": []}
    acts.append((t + s, t + s + 1.0)); t += d + 0.45
    for i, q in enumerate(Q["questions"]):
        qd = dict(q, i=i, scroll_t=t)
        t += 0.55                                    # the sheet scrolls to the question first
        a, w, d = say(q["say"]); clips.append((t, a))
        s, _ = find(w, q["q"].split()[0])          # underline starts on the first word of the printed question
        qd.update(q_t=t, ul_t0=t + s, ul_t1=max(t + d - 0.05, t + s + 1.0))
        acts.append((qd["ul_t0"], qd["ul_t1"]))
        t += d + 0.3
        qd.update(cd_t0=t, cd_t1=t + Q.get("countdown", 5))
        for k in range(Q.get("countdown", 5)): fx_ticks.append(t + k)
        t = qd["cd_t1"] + 0.2
        a, w, d = say(q["answer"]); clips.append((t, a))
        s, e = find(w, q["tick_at"])
        qd.update(a_t=t, tick_t0=t + s, tick_t1=t + s + 0.38)
        acts.append((qd["tick_t0"], qd["tick_t1"]))
        t += d + 0.5
        T["questions"].append(qd)
    T["end_scroll_t"] = t; t += 0.8
    a, w, d = say(Q["outro"]); clips.append((t, a))
    T["end_t"] = t; T["end2_t"] = t + find(w, Q["end_lines"][1].split()[0])[0]
    t += d + 1.8; T["dur"] = round(t, 2)
    T["actions"] = [{"t0": x, "t1": y} for x, y in acts]
    T["ledger"] = B.scene_lib.ledger(0, 0, 1.0, mood="happy", arm="wave", outfit="suit")
    tp = f"{out}/timeline.json"; json.dump(T, open(tp, "w"), indent=1)
    open(f"{out}/script.txt", "w").write("\n".join(lines) + "\n")
    print(f"duration {T['dur']} s, {sum(len(x.split()) for x in lines)} words")

    # audio: voice, pen strokes, countdown ticks; -14 LUFS
    N = int(T["dur"] * SR); vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    for at, a in clips: i = int(at * SR); vo[i:i + len(a)] += a[:N - i]
    ref = np.abs(vo).max(); tk = tick_sound()
    for x, y in acts: B.marker_sound(fx, x, y, 0.05 * ref)
    for at in fx_ticks: i = int(at * SR); fx[i:i + len(tk)] += 0.10 * ref * tk[:N - i]
    mix = vo + fx; mix /= max(1.0, np.abs(mix).max() / 0.98)
    raw = f"{out}/audio-raw.wav"; sf.write(raw, mix, SR); I, _ = B.measure(raw); gain = -14.0 - I; dst = f"{out}/audio.wav"
    import subprocess
    for _ in range(4):
        subprocess.run([B.FF, "-y", "-loglevel", "error", "-i", raw, "-af", f"aresample=48000,volume={gain:.2f}dB,alimiter=limit=0.74:attack=4:release=60:level=0",
                        "-ar", "48000", dst], check=True)
        I2, pk = B.measure(dst)
        if abs(I2 + 14) < 0.3: break
        gain += -14 - I2
    print(f"audio {I2:.1f} LUFS, peak {pk:.1f} dBFS")

    os.environ["RENDER_PAGE"] = "quiz.html"
    times = [0.3, T["intro"]["ul_t1"] + 0.2]
    for q in T["questions"]: times += [q["ul_t1"], q["cd_t0"] + 2.5, q["tick_t1"] + 0.4]
    times += [T["end2_t"] + 1.2, T["dur"] - 0.1]
    times = [round(x, 2) for x in times]
    B.node(["stills", ",".join(f"{x:.2f}" for x in times), f"{out}/stills"], tp)
    B.contact(out, times, f"{out}/{T['slug']}-contact-sheet.png")
    if os.environ.get("STILLS_ONLY"): return
    mp4 = f"{out}/{T['slug']}.mp4"
    B.node(["video", mp4, dst], tp)
    B.check(mp4, T["dur"])


if __name__ == "__main__":
    build(sys.argv[1], os.path.abspath(sys.argv[2]))
