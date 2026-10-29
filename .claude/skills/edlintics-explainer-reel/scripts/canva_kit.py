"""Editable kit for a built reel or ad (29 Oct 2026): the building blocks to assemble the video as layers in Canva or CapCut.

Usage: tools/tts/.venv/bin/python canva_kit.py <workdir> <slug> <outdir>
Run it after make_reel.sh. It writes into <outdir>:
  clips/clip-NN-<scene>.mp4        one silent, caption-free clip per beat (art only, 1080x1920, 24 fps), cut on the same
                                   frames as the full video, so clip NN runs from that beat's cut to the next beat's cut
                                   (the voice line plus its gap); clips/clips.json has the frame-exact times
  clips-4x5/clip-NN-<scene>.mp4    the same clips cropped to the central 4:5 safe area (y 285-1635) for Feed
  clean-9x16.mp4, clean-4x5.mp4    all clips joined with the pure voice, no captions or logo (CapCut "one piece" import)
  voice/voice.wav, voice.mp3       the whole voice track (pure voice, 48 kHz), same length as the video
  voice/voice-with-fx.wav          the voice plus the engine's soft whoosh and tick
  voice/line-NN.wav                each voice line cut to its beat window, so a line can be re-voiced and dropped back in
  captions.srt                     the caption chunks as shown in the video (one key word per beat marked in captions.json)
  lines.srt                        one entry per beat with the full voice line
  endcard/endcard-*.png            the end-card layers as transparent PNGs (term, kp, rule, fn, logo, all) + their boxes
  logo/edlintics-logo.png          the logo (transparent PNG)
  preview-9x16.mp4, preview-4x5.mp4  the flattened preview with burned-in captions, for review only
  kit.json                         everything above with times, boxes and the caption style
  README.md                        import order, timings, caption style, music and AI-disclosure notes
"""
import json, os, shutil, subprocess, sys
import imageio_ffmpeg, numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
CROP = (0, 285, 1080, 1350)   # the central 4:5 safe area that Meta's feed crop keeps
STYLE = {   # from render.html, layout "ad" (1080x1920)
    "caption": {"font": "Inter", "weight": 900, "size_px": 92, "line_height": 1.12, "color": "#0F172A", "letter_spacing_em": -0.01,
                "align": "center", "box": {"x": 60, "y": 300, "w": 960, "h": 220}, "max_lines": 2,
                "highlight": {"color": "#FFD45C", "behind": "the key word, lower 55-93% of the line height, 8 px side padding"},
                "entrance": "scale 0.88 to 1.0 over 0.16 s with a slight overshoot, opacity 0 to 1 over 0.06 s; the highlight wipes in left to right over 0.28 s"},
    "logo": {"file": "logo/edlintics-logo.png", "width_px": 210, "center_x": 540, "y": 1338, "opacity": 0.72},
    "endcard": {"term": {"font": "Inter", "weight": 900, "size_px": 132, "line_height": 1.02, "color": "#0F172A", "letter_spacing_em": -0.02},
                "rule": {"w": 140, "h": 10, "radius": 5, "color": "#467DE3"},
                "keypoint": {"font": "Inter", "weight": 800, "size_px": 64, "line_height": 1.18, "color": "#0F172A", "highlight": "#FFD45C wipes under the whole line"},
                "logo_width_px": 330, "cta_pill": {"font": "Inter", "weight": 800, "size_px": 46, "color": "#FFFFFF", "fill": "#467DE3", "padding": "30px 64px", "radius": "pill"}, "footnote": {"font": "Inter", "weight": 600, "size_px": 30, "color": "#475569"},
                "layout": "a centred column in the box x 70-1010, y 330-1330 with 56 px gaps; term fades in over 0.15 s, key point after 0.35 s, highlight from 0.6 s",
                "background": "#FBFAF6 paper (the end-card clip is plain paper)"},
    "page": {"w": 1080, "h": 1920, "fps": 24, "paper": "#FBFAF6", "safe_4x5": {"y0": 285, "y1": 1635}}}


def run(*a):
    subprocess.run([str(x) for x in a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def srt_time(t):
    ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main(w, slug, out):
    w, out = os.path.abspath(w), os.path.abspath(out)
    T = json.load(open(f"{w}/timing.json")); S = json.load(open(f"{w}/script.json")); D = json.load(open(f"{w}/scenes.json"))
    os.makedirs(out, exist_ok=True)
    for sub in ("clips", "clips-4x5", "voice", "endcard", "logo"):
        shutil.rmtree(f"{out}/{sub}", ignore_errors=True); os.makedirs(f"{out}/{sub}")
    env = dict(os.environ, SCENES=f"{w}/scenes.json", CLEAN="1", FFMPEG=FF)
    print("== clips (art only)"); subprocess.run(["node", "render.js", "clips", f"{out}/clips"], cwd=HERE, env=env, check=True)
    print("== end-card layers"); subprocess.run(["node", "render.js", "cardparts", f"{out}/endcard"], cwd=HERE, env=env, check=True)
    C = json.load(open(f"{out}/clips/clips.json"))
    # 4:5 crops and the joined clean masters
    lst = []
    for c in C["clips"]:
        run(FF, "-y", "-loglevel", "error", "-i", f"{out}/clips/{c['file']}", "-vf", f"crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{out}/clips-4x5/{c['file']}")
        lst.append(f"file '{out}/clips/{c['file']}'")
    open(f"{out}/clips/concat.txt", "w").write("\n".join(lst) + "\n")
    # voice: pure voice (voiceover.wav, 24 kHz) resampled to 48 kHz, plus the per-line windows and the fx version
    a, sr = sf.read(f"{w}/voiceover.wav", dtype="float32"); N = int(round(T["duration"] * sr)); a = np.pad(a, (0, max(0, N - len(a))))[:N]
    sf.write(f"{out}/voice/voice-24k.wav", a, sr)
    run(FF, "-y", "-loglevel", "error", "-i", f"{out}/voice/voice-24k.wav", "-ar", "48000", f"{out}/voice/voice.wav")
    run(FF, "-y", "-loglevel", "error", "-i", f"{out}/voice/voice-24k.wav", "-ar", "48000", "-b:a", "192k", f"{out}/voice/voice.mp3")
    os.remove(f"{out}/voice/voice-24k.wav")
    run(FF, "-y", "-loglevel", "error", "-i", f"{w}/audio-voice.wav", "-ar", "48000", f"{out}/voice/voice-with-fx.wav")
    lines = []
    for c, b in zip(C["clips"], T["beats"]):
        seg = a[int(round(c["start"] * sr)):int(round(c["end"] * sr))]
        f = f"line-{c['n']:02d}.wav"; sf.write(f"{out}/voice/{f}", seg, sr)
        lines.append({"n": c["n"], "file": f"voice/{f}", "role": b["role"], "text": b["text"], "clip": f"clips/{c['file']}", "clip_4x5": f"clips-4x5/{c['file']}",
                      "window": [c["start"], c["end"]], "clip_seconds": round(c["end"] - c["start"], 4), "voice": [b["start"], b["end"]],
                      "chunks": [{"text": x["text"], "key": x.get("key", ""), "t": x["t"]} for x in b.get("chunks", [])],
                      **({k: b[k] for k in ("term", "keypoint", "footnote") if k in b})})
    run(FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/clips/concat.txt", "-i", f"{out}/voice/voice.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", f"{out}/clean-9x16.mp4")
    run(FF, "-y", "-loglevel", "error", "-i", f"{out}/clean-9x16.mp4", "-vf", f"crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", f"{out}/clean-4x5.mp4")
    # captions: chunk k runs from its time to the next chunk (or the beat's end + gap)
    srt, srt2, caps = [], [], []
    k = 0
    for c, b in zip(C["clips"], T["beats"]):
        ch = b.get("chunks", [])
        for i, x in enumerate(ch):
            t0 = max(c["start"], x["t"]); t1 = ch[i + 1]["t"] if i + 1 < len(ch) else c["end"]
            k += 1; srt.append(f"{k}\n{srt_time(t0)} --> {srt_time(t1)}\n{x['text']}\n"); caps.append({"n": k, "start": round(t0, 3), "end": round(t1, 3), "text": x["text"], "key": x.get("key", ""), "beat": c["n"]})
        if b["role"] != "endcard": srt2.append(f"{c['n']}\n{srt_time(b['start'])} --> {srt_time(b['end'])}\n{b['text']}\n")
    open(f"{out}/captions.srt", "w").write("\n".join(srt) + "\n"); open(f"{out}/lines.srt", "w").write("\n".join(srt2) + "\n")
    json.dump({"style": STYLE["caption"], "captions": caps}, open(f"{out}/captions.json", "w"), indent=1)
    shutil.copy(f"{HERE}/logo/edlintics-logo.png", f"{out}/logo/edlintics-logo.png")
    for f, dst in ((f"{w}/{slug}.mp4", "preview-9x16.mp4"),):
        if os.path.exists(f): shutil.copy(f, f"{out}/{dst}")
    if os.path.exists(f"{w}/{slug}.mp4"):
        run(FF, "-y", "-loglevel", "error", "-i", f"{w}/{slug}.mp4", "-vf", f"crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", f"{out}/preview-4x5.mp4")
    parts = {p.replace("endcard-", "").replace(".png", ""): f"endcard/{p}" for p in sorted(os.listdir(f"{out}/endcard"))}
    kit = {"title": S["meta"].get("title"), "slug": slug, "duration": T["duration"], "fps": C["fps"], "style": STYLE, "lines": lines, "endcard_files": parts,
           "files": {"clean_9x16": "clean-9x16.mp4", "clean_4x5": "clean-4x5.mp4", "voice": "voice/voice.wav", "voice_mp3": "voice/voice.mp3", "voice_fx": "voice/voice-with-fx.wav",
                     "captions": "captions.srt", "lines": "lines.srt", "logo": "logo/edlintics-logo.png", "preview": "preview-9x16.mp4", "preview_4x5": "preview-4x5.mp4"}}
    json.dump(kit, open(f"{out}/kit.json", "w"), indent=1)
    open(f"{out}/README.md", "w").write(readme(kit, S))
    print("kit:", out, "|", len(lines), "clips,", T["duration"], "s")


def readme(kit, S):
    c = STYLE["caption"]; e = STYLE["endcard"]; rows = []
    for l in kit["lines"]:
        caps = " / ".join(f"{x['text']} ({x['t']:.2f} s)" for x in l["chunks"]) or "end card: " + l.get("term", "")
        rows.append(f"| {l['n']} | `{l['clip'].split('/')[-1]}` | {l['window'][0]:.3f}-{l['window'][1]:.3f} | {l['clip_seconds']:.3f} | `{l['file'].split('/')[-1]}` | {l['text']} | {caps} |")
    return f"""# {kit['title']} · editable kit (Canva and CapCut)

Built {__import__('datetime').date.today().isoformat()} from `{kit['slug']}` · {kit['duration']} s · 1080x1920 · {kit['fps']} fps · voice ElevenLabs v3 (synthetic)

## Import order (CapCut)
1. New project, 9:16, 1080x1920, {kit['fps']} fps. Import `clips/clip-01…` to `clip-{len(kit['lines']):02d}` and drop them on the main track in number order, no gaps and no transitions (they are cut on the same frames as the full video, so the joined length is exactly {kit['duration']} s; `clean-9x16.mp4` is the same thing as one file)
2. Add `voice/voice.wav` on an audio track at 0:00 (pure voice; `voice/voice-with-fx.wav` adds the engine's soft whoosh at each cut). To re-voice one line, replace that beat's window with the new file: `voice/line-NN.wav` is exactly the window of clip NN
3. Captions: import `captions.srt` (the chunks as shown in the preview) or `lines.srt` (one full line per beat) and restyle them (see the caption style below), or type them as text layers
4. Logo: `logo/edlintics-logo.png` {STYLE['logo']['width_px']} px wide, centred at x {STYLE['logo']['center_x']}, top y {STYLE['logo']['y']}, opacity {int(STYLE['logo']['opacity'] * 100)}%, on every page except the end card
5. End card (last clip, plain paper): `endcard/endcard-all.png` is the whole card as one transparent layer; `endcard-term.png`, `endcard-rule.png`, `endcard-kp.png`, `endcard-logo.png`, `endcard-cta.png`, `endcard-fn.png` are the parts, to rebuild it from editable text (styles below)
6. Export 1080x1920 H.264. For Feed, use `clips-4x5/` (or crop the export to y {STYLE['page']['safe_4x5']['y0']}-{STYLE['page']['safe_4x5']['y1']}) for 1080x1350

Review only: `preview-9x16.mp4` and `preview-4x5.mp4` have the captions burned in.

## Beats
| # | clip | window (s) | length (s) | voice file | voice line | captions (start) |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Caption style (from the engine's ad layout)
- Font {c['font']}, weight {c['weight']}, {c['size_px']} px, line height {c['line_height']}, colour {c['color']}, letter spacing {c['letter_spacing_em']} em, centred, at most {c['max_lines']} lines
- Box: x {c['box']['x']}-{c['box']['x'] + c['box']['w']}, y {c['box']['y']}-{c['box']['y'] + c['box']['h']} (inside the 4:5 safe area and above the Reels UI)
- Key word: {c['highlight']['color']} highlight {c['highlight']['behind']} (the key word per chunk is in `captions.json`)
- Entrance: {c['entrance']}
- No full stop at the end of a caption; no exclamation points; no emoji

## End-card style
- Term: {e['term']['font']} {e['term']['weight']}, {e['term']['size_px']} px, {e['term']['color']}; rule {e['rule']['w']}x{e['rule']['h']} px {e['rule']['color']}; key point {e['keypoint']['weight']} {e['keypoint']['size_px']} px with a {e['keypoint']['highlight']}; logo {e['logo_width_px']} px; CTA pill {e['cta_pill']['font']} {e['cta_pill']['weight']} {e['cta_pill']['size_px']} px white on {e['cta_pill']['fill']}; footnote {e['footnote']['size_px']} px {e['footnote']['color']}
- {e['layout']}
- Keep everything out of the Reels UI zones: the bottom 20% (y over 1536) and the right 120 px

## Music
Use only CapCut's commercial-use library (or Canva's free library when assembling in Canva), or no music. Volume very low: Canva volume 8 with the voice at 100; in CapCut about -22 dB under the voice. Fade in and out over 1 s. No ripped or trending commercial tracks

## Meta AI disclosure
The voice is synthetic (ElevenLabs v3). The animation is code-rendered, no AI-generated images or clips. Switch on Meta's "AI info" for this ad when uploading
"""


if __name__ == "__main__":
    main(*sys.argv[1:4])
