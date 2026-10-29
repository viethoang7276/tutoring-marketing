"""Edlintics puzzle reel builder (9:16, 1080x1920, 24 fps, H.264 + AAC). Everything is code-rendered: no AI images or video.

Usage (from anywhere; build.sh wraps this):
  <repo>/tools/tts/.venv/bin/python build.py <puzzle.json> <outdir> [voice|novoice|both]

puzzle.json (paths relative to the JSON file):
  question      one block, full sentences, *word* = the blue key word
  diagram       SVG in question state. Leaf shapes and texts draw in in document order.
                class="reveal-show" on any element = hidden until the reveal
  options       optional list of up to 4 answer options (A-D); answer = "C"
  reveal        list of ops on the same diagram at the reveal:
                {"sel": "#id", "attr": {"fill": "#2960c7"}} colour change, {"sel","text"} text swap, {"sel","hide": true}
  pulse         optional selector that pulses once at the reveal
  explanation   2-3 lines [{"text", "say"?, "style"?: "takeaway"}], shown in sequence after the reveal
  prompt_text / prompt_say, end_text / end_say, countdown {"voice": 5, "novoice": 6}
  Any line may carry "say" to change what the voice reads (for example to spell out a unit)

The voice is Kokoro af_heart at speed 1.08 (same as the explainer reels). The novoice cut has ticks, chime and pad only.
Audio is normalised to -14 LUFS integrated with a limiter at about -1.6 dBFS.
"""
import hashlib, json, os, re, subprocess, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing"
TTS = f"{REPO}/tools/tts/models"
NODE_PATH = f"{REPO}/.claude/skills/edlintics-explainer-reel/scripts/node_modules"
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 24000
SPEED = float(os.environ.get("SPEED", "1.08"))
CPS = 17.0          # on-screen reading speed used when there is no voice (spec max ~17)


def plain(s): return s.replace("*", "")


def say_of(item, key_text, key_say=None):
    if isinstance(item, dict):
        s = item.get(key_say or "say") or item[key_text]
    else:
        s = item
    s = plain(s).strip()
    return s if s[-1] in ".?" else s + "."


_kokoro = None
def tts(text, cache):
    """Kokoro af_heart clip, trimmed of its own leading and trailing silence. Cached by text and speed."""
    global _kokoro
    if os.environ.get("TTS_ENGINE") == "eleven":  # ElevenLabs v3, cached in tools/tts/cache-eleven/
        sys.path.insert(0, f"{REPO}/.claude/skills/edlintics-explainer-reel/scripts"); import eleven_tts
        return eleven_tts.say(text)
    h = hashlib.sha1(f"{text}|{SPEED}".encode()).hexdigest()[:12]
    f = f"{cache}/vo-{h}.wav"
    if os.path.exists(f):
        return sf.read(f, dtype="float32")[0]
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(f"{TTS}/kokoro-v1.0.onnx", f"{TTS}/voices-v1.0.bin")
    a, sr = _kokoro.create(text, voice="af_heart", speed=SPEED, lang="en-us")
    assert sr == SR
    a = a.astype(np.float32); nz = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a
    sf.write(f, a, SR)
    return a


# ---------- timeline ----------
def timeline(P, voice, cache):
    clips = []   # (start, audio)
    T = {}
    q_say = say_of(P, "question")
    n = P.get("countdown", {}).get("voice" if voice else "novoice", 5 if voice else 6)
    T["draw"] = [0.3, 2.5]
    if voice:
        qa = tts(q_say, cache); clips.append((0.4, qa)); q_end = 0.4 + len(qa) / SR
        T["opt_t"] = 2.3
        pa = tts(say_of(P, "prompt_text", "prompt_say"), cache)
        T["prompt_t"] = q_end + 0.35; clips.append((T["prompt_t"], pa))
        t0 = T["prompt_t"] + len(pa) / SR + 0.3
    else:
        T["opt_t"] = 2.0; T["prompt_t"] = 2.6; t0 = 2.9
    T["countdown"] = {"t0": round(t0, 3), "n": n}
    # after the countdown a hand hovers over an option, then taps the right one (tap at +1.55 s); the reveal follows
    C = t0 + n; T["cd_end"] = round(C, 3); T["tap_t"] = round(C + 1.55, 3)
    R = C + 1.9; T["reveal_t"] = round(R, 3)
    t = R + 0.8; T["ans_t"] = []
    for e in P["explanation"]:
        if voice:
            a = tts(say_of(e, "text"), cache); clips.append((t, a)); T["ans_t"].append(round(t - 0.15, 3))
            t += len(a) / SR + 0.35
        else:
            T["ans_t"].append(round(t, 3)); t += max(2.6, len(plain(e["text"])) / CPS) + 0.3
    T["end_t"] = round(t + (0.35 if voice else 0.2), 3)
    dur = T["end_t"] + 2.6
    if voice:
        ea = tts(say_of(P, "end_text", "end_say"), cache); es = T["end_t"] + 0.4; clips.append((es, ea))
        dur = max(dur, es + len(ea) / SR + 0.9)
    T["dur"] = round(round(dur * 24) / 24, 4)
    T["ticks"] = [round(t0 + k, 3) for k in range(n)]
    return T, clips


# ---------- audio ----------
def tick(n_at, buf, amp, high=False):
    L = int(0.09 * SR); tt = np.arange(L) / SR
    f1, f2 = (1900, 3000) if high else (1500, 2400)
    x = (np.sin(2 * np.pi * f1 * tt) + 0.45 * np.sin(2 * np.pi * f2 * tt)) * np.exp(-tt * 55)
    x[:30] *= np.linspace(0, 1, 30)
    i = int(n_at * SR); buf[i:i + L] += amp * x[:len(buf) - i]


def tap(at, buf, amp):
    """Soft UI tap: a short filtered click plus a low thump"""
    L = int(0.06 * SR); tt = np.arange(L) / SR; rng = np.random.default_rng(7)
    nz = rng.standard_normal(L)
    for _ in range(4): nz = np.convolve(nz, np.ones(5) / 5, mode="same")
    x = 0.6 * nz * np.exp(-tt * 140) + np.sin(2 * np.pi * 240 * tt) * np.exp(-tt * 45)
    i = int(at * SR); buf[i:i + L] += amp * x[:len(buf) - i]


def chime(at, buf, amp):
    L = int(2.2 * SR); tt = np.arange(L) / SR
    for j, f in enumerate([1046.5, 1318.5, 1568.0]):
        x = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.0 * f * tt) + 0.12 * np.sin(2 * np.pi * 2.76 * f * tt)) * np.exp(-tt * 2.6)
        x[:120] *= np.linspace(0, 1, 120)
        i = int((at + 0.075 * j) * SR); buf[i:i + L] += amp * 0.6 * x[:len(buf) - i]


def pad(N):
    t = np.arange(N) / SR; dur = N / SR
    chords = [[220, 277.18, 329.63], [196, 246.94, 293.66], [174.61, 220, 261.63], [196, 246.94, 293.66]]
    p = np.zeros(N, dtype=np.float32)
    for k in range(int(dur // 4) + 1):
        t0 = k * 4.0; m = (t >= t0) & (t < t0 + 4.6); tt = t[m] - t0
        env = np.clip(tt / 1.2, 0, 1) * np.clip((4.6 - tt) / 1.4, 0, 1)
        for f in chords[k % 4]:
            p[m] += env * (0.5 * np.sin(2 * np.pi * f * tt) + 0.12 * np.sin(2 * np.pi * 2.002 * f * tt))
    p /= np.abs(p).max() + 1e-9
    return p * np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.0, 0, 1)


def measure(wav):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)); pk = float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", s).group(1))
    return I, pk


def make_audio(T, clips, voice, work):
    N = int(T["dur"] * SR); vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    for at, a in clips:
        i = int(at * SR); vo[i:i + len(a)] += a[:N - i]
    ref = np.abs(vo).max() if voice else 0.5
    for k, at in enumerate(T["ticks"]):
        tick(at, fx, 0.30 * ref, high=(k == len(T["ticks"]) - 1))
    if T.get("tap_t"): tap(T["tap_t"], fx, 0.35 * ref)
    chime(T["reveal_t"], fx, 0.45 * ref)
    # pad: very low bed under the voice; without voice it sits ~24 dB under the tick peaks (music is added later)
    mix = vo + fx + (0.03 if voice else 0.02) * ref * pad(N)
    mix /= max(1.0, np.abs(mix).max() / 0.98)
    raw = f"{work}/audio-raw.wav"; sf.write(raw, mix, SR)
    out = f"{work}/audio.wav"
    if not voice:
        # Voice-free cut: loudness would be set by the pad, so -14 LUFS would push the bed up.
        # Instead peak-normalise: ticks and chime peak at -1.5 dBFS, the pad stays low (report the resulting LUFS).
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", "aresample=48000", "-ar", "48000", f"{work}/tmp48.wav"], check=True)
        a, sr48 = sf.read(f"{work}/tmp48.wav", dtype="float32"); a *= 10 ** (-1.5 / 20) / (np.abs(a).max() + 1e-9)
        sf.write(out, a, sr48); I2, pk = measure(out)
        print(f"audio (peak-normalised, no voice): {I2:.1f} LUFS, sample peak {pk:.1f} dBFS"); return out
    I, _ = measure(raw); gain = -14.0 - I
    for _ in range(4):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af",
                        f"aresample=48000,volume={gain:.2f}dB,alimiter=limit=0.74:attack=4:release=60:level=0",
                        "-ar", "48000", out], check=True)
        I2, pk = measure(out)
        if abs(I2 + 14.0) < 0.3: break
        gain += -14.0 - I2
    print(f"audio: {I2:.1f} LUFS, sample peak {pk:.1f} dBFS")
    return out


# ---------- render ----------
def node(args, T_path):
    env = dict(os.environ, NODE_PATH=NODE_PATH, FFMPEG=FF, TIMELINE=T_path)
    subprocess.run(["node", f"{HERE}/render.cjs", *args], check=True, env=env)


def contact_sheet(work, times, out):
    from PIL import Image, ImageDraw, ImageFont
    w, h = 360, 640; cols = 4; rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols + 1) * 12, rows * (h + 40) + 12), "#e9ecf2"); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except Exception: font = ImageFont.load_default()
    for k, t in enumerate(times):
        im = Image.open(f"{work}/stills/still-{t:.2f}.png").convert("RGB").resize((w, h), Image.LANCZOS)
        x = 12 + (k % cols) * (w + 12); y = 12 + (k // cols) * (h + 40)
        sheet.paste(im, (x, y)); d.text((x, y + h + 6), f"{t:.1f} s", fill="#0d1523", font=font)
    sheet.save(out)


def build(pj, outdir, variant):
    P = json.load(open(pj)); base = os.path.dirname(os.path.abspath(pj)); slug = P["slug"]
    voice = variant == "voice"
    work = f"{outdir}/work-{slug}{P.get('suffix', '')}-{variant}"; cache = f"{outdir}/work-{slug}-vo-cache"
    os.makedirs(work, exist_ok=True); os.makedirs(cache, exist_ok=True)
    T, clips = timeline(P, voice, cache)
    svg = open(os.path.join(base, P["diagram"])).read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    T.update({k: P.get(k) for k in ("question", "options", "answer", "prompt_text", "reveal", "pulse", "explanation", "end_text")})
    T["options"] = T["options"] or []; T["diagram_svg"] = svg
    tp = f"{work}/timeline.json"; json.dump(T, open(tp, "w"), indent=1)
    print(variant, "duration", T["dur"], "reveal", T["reveal_t"], "answers", T["ans_t"], "end", T["end_t"])
    audio = make_audio(T, clips, voice, work)
    name = f"puzzle-reel-{slug}" + ("" if voice else "-novoice") + P.get("suffix", "")
    mp4 = f"{outdir}/{name}.mp4"
    if not os.environ.get("STILLS_ONLY"): node(["video", mp4, audio], tp)
    times = [1.2, T["prompt_t"] + 0.6 if voice else 2.6, T["countdown"]["t0"] + 1.5, T["cd_end"] + 0.85,
             T["tap_t"] + 0.16, T["reveal_t"] + 0.6, T["ans_t"][-1] + 1.0, T["end_t"] + 1.5]
    times = [round(x, 2) for x in times]
    import shutil; shutil.rmtree(f"{work}/stills", ignore_errors=True)
    node(["stills", ",".join(f"{x:.2f}" for x in times), f"{work}/stills"], tp)
    contact_sheet(work, times, f"{outdir}/{name}-contact-sheet.png")
    print("wrote", mp4)


if __name__ == "__main__":
    pj, outdir = sys.argv[1], os.path.abspath(sys.argv[2]); v = sys.argv[3] if len(sys.argv) > 3 else "both"
    for variant in (["voice", "novoice"] if v == "both" else [v]):
        build(pj, outdir, variant)
