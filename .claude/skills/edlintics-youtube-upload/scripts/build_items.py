#!/usr/bin/env python3
"""Build the YouTube upload queue (step P0 / S0 of the edlintics-youtube-upload skill).

Usage:
  python3 build_items.py <slots_dir> <posts_dir> <out_dir> [--from 2026-10-25] [--to 2026-11-01] [--only 0,3,4]

<slots_dir>  folder of slot JSON files saved by ArtifactData query (collection "slots").
<posts_dir>  folder with the exported media, named <MMDD>-<HHMM>-<slug>-<n>.png / .mp4.
<out_dir>    gets items.json (the queue, with absolute file paths) and inject.js
             (run once on youtube.com to store the captions in localStorage 'edl_items').

Rules baked in:
- five-concepts videos -> Short (the long MP4 without "clip" in its name).
- everything else (puzzles, definitions, comics, carousels) -> image Post, PNGs in page order.
- skip slots that already have youtube.status in ("scheduled", "published").
- Post text = the approved caption as it is. Short description = caption with
  "This carousel" -> "Ledger walks you through" and "Swipe through and note" -> "Walk through them with Ledger and note" (Hoang, 30 Oct 2026), plus #Shorts.
- Time = the slot's time_vietnam (the browser runs on Asia/Saigon, GMT+7).
"""
import datetime
import glob
import json
import os
import sys


def main():
    slots_dir, posts_dir, out_dir = sys.argv[1:4]
    args = sys.argv[4:]
    lo = args[args.index('--from') + 1] if '--from' in args else '0000'
    hi = args[args.index('--to') + 1] if '--to' in args else '9999'
    files = sorted(os.listdir(posts_dir))
    items = []
    for f in sorted(glob.glob(os.path.join(slots_dir, '*.json'))):
        d = json.load(open(f))
        d = d.get('data', d)
        sid = os.path.basename(f)[:-5]
        if not (lo <= sid[:10] <= hi) or d.get('status') != 'scheduled':
            continue
        if (d.get('youtube') or {}).get('status') in ('scheduled', 'published'):
            continue
        key = sid[5:7] + sid[8:10] + '-' + sid[11:]
        it = {'slot': sid, 'text': d['caption']}
        when = d.get('time_vietnam')
        if when:
            dt = datetime.datetime.strptime(when, '%Y-%m-%d %H:%M')
            it['date'] = dt.strftime('%b ') + str(dt.day) + dt.strftime(', %Y')
            it['time'] = f"{dt.hour % 12 or 12}:{dt.minute:02d}"
            it['ap'] = 'AM' if dt.hour < 12 else 'PM'
        if d.get('format') == 'five-concepts':
            mp4 = [x for x in files if x.startswith(key) and x.endswith('.mp4') and 'clip' not in x]
            if not mp4:
                print('MISSING MP4', sid)
                continue
            it.update(type='short', files=[os.path.join(posts_dir, mp4[0])],
                      title=d['title'].split(' (')[0] + ' #Shorts',
                      text=d['caption'].replace('This carousel gives each one', 'Ledger walks you through each one with').replace('This carousel', 'Ledger walks you through').replace('This video walks through', 'Ledger walks you through')
                      .replace('Swipe through and note', 'Walk through them with Ledger and note').rstrip() + ' #Shorts')
        else:
            pngs = sorted([x for x in files if x.startswith(key) and x.endswith('.png')],
                          key=lambda x: int(x.rsplit('-', 1)[1].split('.')[0]))
            if not pngs:
                print('MISSING PNG', sid)
                continue
            it.update(type='post', files=[os.path.join(posts_dir, x) for x in pngs][:10])
        it['n'] = len(it['files'])
        items.append(it)
    os.makedirs(out_dir, exist_ok=True)
    json.dump(items, open(os.path.join(out_dir, 'items.json'), 'w'), indent=1, ensure_ascii=False)
    only = set(args[args.index('--only') + 1].split(',')) if '--only' in args else None
    store = {str(i): {k: v for k, v in x.items() if k != 'files'} for i, x in enumerate(items) if only is None or str(i) in only}
    open(os.path.join(out_dir, 'inject.js'), 'w').write(
        "localStorage.setItem('edl_items'," + json.dumps(json.dumps(store, ensure_ascii=False), ensure_ascii=False)
        + ");'stored '+Object.keys(JSON.parse(localStorage.getItem('edl_items'))).length;\n")
    for i, x in enumerate(items):
        print(i, x['slot'], x['type'], x.get('date', 'now'), x.get('time', ''), x.get('ap', ''), x['n'])


if __name__ == '__main__':
    main()
