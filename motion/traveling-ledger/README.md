# Traveling Ledger

An animated carousel and Reel: Ledger walks a dotted line that draws itself across the slides, climbing up and down (route from Hoang's sketch, 23 Oct 2026). There's nothing to install: Chrome renders the frames and macOS AVFoundation encodes them.

```
node motion/traveling-ledger/render.mjs <framesDir> 30        # frames: panel-1..6 and reel
swiftc -O -o /tmp/encode motion/traveling-ledger/encode.swift  # once
/tmp/encode <framesDir>/panel-1 assets/renders/traveling-ledger/<name>-panel-1.mp4 30
```

- **Text and route:** `panels` and `ROUTE` at the top of `index.html`. Set `window.SCENE` to change them without editing the code. Money is in US dollars.
- **Panel clips** (`panel-n`): each one starts as Ledger walks in and ends as he walks out. Posted together as a carousel, swiping looks like one continuous walk.
- **Reel** (`reel`): the camera holds on each slide and pans as Ledger crosses into the next.
- **Ledger:** rebuilt from `assets/brand/ledger.svg` with swinging legs and arms. The tie stays as drawn. Ledger never talks.
- **Output:** renders go to `assets/renders/` (gitignored).
