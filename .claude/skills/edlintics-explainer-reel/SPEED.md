# Engine speed: results (7 Nov 2026)

Speed work agreed with the COO for lesson videos (`meta.type: "lesson"`). Every option is opt-in through an environment variable. With none set, the engine runs exactly the same commands as before (see "Identity proof").

## Flags

| Flag | Where | What it does |
|---|---|---|
| `ENGINE_PROFILE=1` | make_reel.sh, build.sh, render.js | Prints `PROFILE ...` lines: seconds per step, and inside the frame loop: page render, screenshot, waiting on the encoder |
| `LESSON_SINGLE_ENCODE=1` | build.sh | Lessons only (ignored for other types). One libx264 crf 20 encode, with the pc-to-tv range conversion in the first pass, straight into `<slug>-voice-only.mp4`. `<slug>.mp4` is still a stream copy plus `audio.wav`. `<slug>-canva-upload.mp4` is a plain copy of the voice-only file, because lessons never go through Canva and postcheck expects the file |
| `ENGINE_ENCODER=videotoolbox` | render.js, build.sh | Apple hardware H.264 for every encode. The first pass uses `ENGINE_VB` kbit/s (default 3000). The Canva copy and the 10 MB re-encode use the same capped bitrate as libx264 |
| `PICTURE_ONLY=1` | make_reel.sh (+ `picture_timing.py`) | Voice-free picture mode: no voice and no credits. Only `beats.json` and the scene art are written in the workdir. Timings come from a real `timing.json` when its beat count matches, otherwise they are estimated at `PICTURE_WPM` (default 165). The output goes to `<workdir>/_picture/`: stills, a contact sheet, framefill and a silent `<slug>-picture.mp4`. Add `STILLS_ONLY=1` to skip the video |
| `LESSON_OVERLAP_CHECK=1` / `=strict` | make_reel.sh (+ `overlap_check.py`) | Before the voice, flags data tables or charts that overlap another item, and tables that start under the title. This is the same rule as `tutoring-content/tools/video/overlap-check.py`, for one workdir. `strict` stops the build on a hit |

`REUSE_AUDIO=1` now refuses a `timing.json` marked `"estimated": true`. The picture mode never writes one in the workdir, so this guard only matters if someone copies one in by hand.

## Benchmark

Lesson FA1 3.9 card 2 (`c02-paid-before-delivery`): 162.9 s, 3911 frames, `REUSE_AUDIO=1`, copied to scratch. Times are the sums of the PROFILE laps. They exclude waiting for a render slot.

**Caveat:** every run shared the laptop with other builders, `tsc` runs and a Zoom call (1-minute load 13 to 37 on 11 cores). With the same code path, the frame loop speed varied from 11 to 16.5 fps between runs, so read single numbers as ±20 %. The savings from dropping encodes are structural, not noise.

### Where the time goes (step 0, default pipeline, load ~25-35)

| Step | Seconds | Share |
|---|---|---|
| validate, scenes, scene data | 0.4 | 0 % |
| stills (28) | 26.4 | 7 % |
| frame loop (3911 frames, 14.4 fps) | 272.5 | 70 % |
|   of which `page.screenshot` (Chrome raster + JPEG q92, ~206 KB/frame) | 254.3 | 66 % |
|   of which `window.render(t)` JS | 11.7 | 3 % |
|   of which waiting on the libx264 encoder (back-pressure) | 6.5 | 2 % |
| encoder flush + mux | 4.7 | 1 % |
| voice-only re-encode (libx264 medium crf 20, range conversion) | 29.0 | 8 % |
| Canva copy re-encode (libx264 slow, 1500k) | 46.4 | 12 % |
| music mux (stream copy), poster, lesson files, postcheck, framefill | 7.3 | 2 % |
| **total** | **~387** | |

Audio is 0 s with `REUSE_AUDIO`. A fresh build adds the ElevenLabs calls (cached per line) and mix_audio.py.

The encoder is not the bottleneck. libx264 keeps up with the screenshot loop: 6.5 s of back-pressure in 272 s. The two re-encodes after the loop (75 s) were the only encode cost that could be removed.

### Options measured

| Run | Frame loop | build.sh | Total work | `<slug>.mp4` | Notes |
|---|---|---|---|---|---|
| Baseline, old code (load ~10) | ~245 s | ~375 s | 464 s wall | 13.7 MB | three libx264 encodes |
| Default + `ENGINE_PROFILE=1` | 272.5 s | 356.0 s | ~387 s | 13.7 MB | same commands as baseline |
| `LESSON_SINGLE_ENCODE=1` | 237.4 s | **242.6 s** | **~263 s** | 13.7 MB | -113 s in build.sh (-32 %); one encode generation fewer |
| `ENGINE_ENCODER=videotoolbox` (3000k) | 352.0 s | 426.2 s | ~469 s | 63.4 MB | load 30-35 during the loop; re-encodes 22 s + 38 s instead of 29 s + 46 s |
| videotoolbox + single encode | 278.9 s | 284.9 s | ~309 s | 64.2 MB | |
| `PICTURE_ONLY=1` (real timing reused) | 325.2 s | n/a | ~383 s | 10.3 MB silent | no voice, no credits; the point is cost, not speed |

**Single encode quality:** compared with the default voice-only file, PSNR is 47.4 dB, the paper colour is identical (242,240,237 at 20, 80 and 140 s, against 243,242,238 in the PNG still), and side-by-side frames look the same. The file size is the same (13.7 MB).

**videotoolbox quality (60 s of the lesson, SSIM against the source):**

| Encoder | Size per 60 s | SSIM | Encode time |
|---|---|---|---|
| libx264 crf 20 | 4.0 MB | 0.998 | 12.2 s |
| videotoolbox 600k | 4.6 MB | 0.983 | 7.2 s |
| videotoolbox 1200k | 9.1 MB | 0.985 | 7.5 s |
| videotoolbox 3000k | 22.7 MB | 0.989 | 8.4 s |

At 600k, which is about what a 2-minute reel gets under the 10 MB cap, videotoolbox text is visibly blocky. At 1200k it is noisy around letters. Even at 3000k it is softer than libx264 crf 20 at a sixth of the size. It saves a few seconds per re-encode, but the frame loop does not need a faster encoder.

### Reel check (videotoolbox, 52 s definition reel `def-externality`)

- **Build:** `REUSE_AUDIO=1 ENGINE_ENCODER=videotoolbox` gave POSTCHECK OK and FRAMEFILL OK. build.sh took 118.6 s; the frame loop ran at 14.6 fps. The voice-only file at 3000k was 19.7 MB, so the existing 10 MB rule re-encoded `<slug>.mp4`.
- **Sizes:** `<slug>.mp4` was 8.4 MB and `<slug>-canva-upload.mp4` 8.4 MB, both at the capped 1302k. Both decode end to end with ffmpeg without errors.
- **2-minute case:** 120 s of video at the 2-minute cap (VB 492k) came to **8.95 MB, under 10 MB**. videotoolbox holds its bitrate, a little under target.
- **What it looks like:** text stays readable, but the paper background shows visible blocking at 492k, and a little at 1302k. This is another reason not to use it for reels.

## Recommended defaults for lessons

- **Use `LESSON_SINGLE_ENCODE=1`** on every lesson build. It saves about 115 s per 2:45 video, with the same size and one encode generation fewer. To make it the lesson default later, flip it in build.sh (one line). It was not flipped here because the rule for this task was opt-in only.
- **Do not use `ENGINE_ENCODER=videotoolbox`.** It gives a 5-6x larger file, or visibly worse text at the same size, and it does not speed up the loop.
- **Use `PICTURE_ONLY=1 STILLS_ONLY=1`** for the first look at a new lesson script, before any voice is paid for. It takes about 25-55 s for stills and a contact sheet. Drop `STILLS_ONLY` for a silent motion check. The estimate came out at 159 s against a real 163 s on this lesson.
- **Use `LESSON_OVERLAP_CHECK=strict`** on lesson builds. It costs nothing and stops before the voice and the render.
- **Use `ENGINE_PROFILE=1`** when a build feels slow. It only adds log lines.

## The next lever (not built)

The screenshot is 66 % of a build and 93 % of the frame loop. The two real wins would be:

1. Render frame ranges in 2-3 pages or Chrome instances at once and concatenate them. This is close to linear, but it raises the load, so it would have to count as more than one render slot.
2. A cheaper capture. Options are `optimizeForSpeed` and a lower JPEG quality (small gains), or CDP screencast or BeginFrame capture (bigger change).

Neither was in the agreed plan.

## Identity proof (no flags)

- **Rendering is not deterministic, even with the old code.** Two builds of `def-externality` with the old engine differ in 902 of 1252 frames (PSNR 49.7 dB, invisible). Chrome's raster varies slightly from run to run. The md5 of the JPEG stream piped to ffmpeg differs between two runs of the same code. So a frame md5 cannot be identical between any two builds, old or new.
- **What was proven instead:** with no flags, the new code runs byte-identical encoder commands. A spawn logger (`NODE_OPTIONS=--require spawnlog.js`) captured render.js's ffmpeg argv, and `bash -x` captured every ffmpeg command line in build.sh. For the old code (an untouched copy of the three files in a scratch mirror) and the new code, the normalised commands are identical.
- **Other checks:** the stills (PNG) are byte-identical between old and new. The new no-flag build gave the same file set, `POSTCHECK OK` and `FRAMEFILL OK`. The new-vs-old frame difference (936 frames, PSNR 49.4 dB) is the same size as old-vs-old.
