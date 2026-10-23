# Traveling Ledger

An animated carousel and Reel: Ledger walks a dotted line that draws itself across the slides, climbing up and down (route from Hoang's sketch, 23 Oct 2026). There's nothing to install: Chrome renders the frames and macOS AVFoundation encodes them.

```
node motion/traveling-ledger/render.mjs motion/traveling-ledger/scenes/<name> <framesDir> 30   # frames: panel-1..n and reel
swiftc -O -o /tmp/encode motion/traveling-ledger/encode.swift  # once
/tmp/encode <framesDir>/panel-1 assets/renders/traveling-ledger/<name>-panel-1.mp4 30
```

- **One post = one scene folder:** `scenes/<name>/scene.json` holds the slides (title, body, example in US dollars, image) and `moves`, one route step per slide: `start`, `flat`, `up`, `down`, `loop`, `end`. Put the slide images (560×560 PNG, brand style) in the same folder.
- **Layout:** the copy sits at the top, the illustration in the middle and the path along the bottom. Ledger is drawn at 0.6 scale.
- **Canva:** Canva's API upload takes no video. Upload the clips in Canva's web UI (folder › Add new › Upload files), then put one clip per page in a 1080×1350 design that ends with the standard call-to-action page. Example: DAHY0ZI83Go.
- **Panel clips** (`panel-n`): each one starts as Ledger walks in and ends as he walks out. Posted together as a carousel, swiping looks like one continuous walk.
- **Reel** (`reel`): the camera holds on each slide and pans as Ledger crosses into the next.
- **Ledger:** rebuilt from `assets/brand/ledger.svg` with swinging legs and arms. The tie stays as drawn. Ledger never talks.
- **Output:** renders go to `assets/renders/` (gitignored).
