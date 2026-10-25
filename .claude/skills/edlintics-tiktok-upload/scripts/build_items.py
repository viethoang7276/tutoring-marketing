#!/usr/bin/env python3
"""Build the TikTok upload queue (step 2 of the edlintics-tiktok-upload skill).

Usage:
  python3 build_items.py <slots_dir> <posts_dir> <out_dir> [--from 2026-10-22] [--to 2026-11-01]
                         [--copy <posts_dir>/copy.json] [--lead 20] [--only 0,3,4]

<slots_dir>  slot JSON files saved by ArtifactData list/query (collection "slots").
<posts_dir>  exported media. Looked up in this order:
               <posts_dir>/<slot id>/fixed/   (corrected exports: 01.png.. or <subject>.mp4)
               <posts_dir>/<slot id>/*.mp4     (explainer reels)
               <posts_dir>/<MMDD>-<HHMM>-<slug>-<n>.png / <MMDD>-<HHMM>-<subject>.mp4
<out_dir>    gets items.json (queue with absolute paths) and inject.js (run once on tiktok.com:
             stores titles, captions, tags and times in localStorage 'edl_tt'), and prints the queue.

Rules baked in:
- format five-concepts / explainer-reel (any .mp4) -> TikTok video. Everything else -> TikTok photo post.
- skip slots whose tiktok.status is scheduled or published; skip status other than scheduled/posted.
- caption = slot caption (or copy.json c<n> for the oldest slots that have no caption field),
  with every line's trailing full stop removed. The last paragraph, if it is only #hashtags,
  is split off into `tags` so they can be typed one by one (TikTok only links tags picked
  from its suggestion list).
- five-concepts captions: "This carousel" -> "This video", "Swipe through and note" -> "Watch and note".
- when: the slot's time_vietnam if it is more than --lead minutes in the future, else "now".
- The queue skips slots whose tiktok.status is scheduled/published, so re-running is safe.
"""
import datetime
import glob
import json
import os
import re
import sys

OLD_COPY = {  # oldest slots kept their captions only in posts/copy.json
    '2026-10-22-1000': 'c1', '2026-10-22-1300': 'c2', '2026-10-22-1800': 'c3',
    '2026-10-23-1000': 'c4', '2026-10-23-1800': 'c5'}
OLD_MEDIA = {  # oldest slots were exported under the day they went live
    '2026-10-23-1000': '1024-1000-', '2026-10-23-1800': '1024-1800-'}


def clean(cap):
    lines = [re.sub(r'\.\s*$', '', l.rstrip()) if not l.rstrip().endswith('...') else l.rstrip()
             for l in cap.replace('\r', '').split('\n')]
    text = '\n'.join(lines).strip()
    paras = text.split('\n\n')
    tags = []
    if paras and all(w.startswith('#') for w in paras[-1].split()):
        tags = paras.pop().split()
    return '\n\n'.join(paras), tags


def media(sid, d, posts_dir, files):
    fx = os.path.join(posts_dir, sid, 'fixed')
    if os.path.isdir(fx):
        f = sorted(os.listdir(fx))
        mp4 = [x for x in f if x.endswith('.mp4') and 'clip' not in x]
        if mp4:
            return 'video', [os.path.join(fx, mp4[0])]
        return 'photo', [os.path.join(fx, x) for x in f if x.endswith('.png')]
    own = os.path.join(posts_dir, sid)
    if os.path.isdir(own):
        mp4 = sorted(glob.glob(os.path.join(own, '*.mp4')))
        if mp4:
            return 'video', mp4[:1]
    key = OLD_MEDIA.get(sid, sid[5:7] + sid[8:10] + '-' + sid[11:] + '-')
    mp4 = [x for x in files if x.startswith(key) and x.endswith('.mp4') and 'clip' not in x]
    if mp4:
        return 'video', [os.path.join(posts_dir, mp4[0])]
    png = sorted([x for x in files if x.startswith(key) and x.endswith('.png')],
                 key=lambda x: int(x.rsplit('-', 1)[1].split('.')[0]))
    return 'photo', [os.path.join(posts_dir, x) for x in png]


def main():
    slots_dir, posts_dir, out_dir = sys.argv[1:4]
    a = sys.argv[4:]
    opt = lambda k, dflt: a[a.index(k) + 1] if k in a else dflt
    lo, hi = opt('--from', '0000'), opt('--to', '9999')
    lead = int(opt('--lead', '20'))
    copy = json.load(open(opt('--copy', os.path.join(posts_dir, 'copy.json'))))
    files = sorted(os.listdir(posts_dir))
    now = datetime.datetime.now()
    items = []
    for f in sorted(glob.glob(os.path.join(slots_dir, '*.json'))):
        d = json.load(open(f))
        d = d.get('data', d)
        sid = os.path.basename(f)[:-5]
        date = d.get('date') or sid[:10]
        if not (lo <= date <= hi) or d.get('status') not in ('scheduled', 'posted'):
            continue
        if (d.get('tiktok') or {}).get('status') in ('scheduled', 'published'):
            continue
        cap = d.get('caption') or copy.get(OLD_COPY.get(sid, '-'))
        if not cap:
            print('NO CAPTION', sid); continue
        if d.get('format') == 'five-concepts':
            cap = cap.replace('This carousel', 'This video').replace('Swipe through and note', 'Watch and note')
        body, tags = clean(cap)
        typ, paths = media(sid, d, posts_dir, files)
        if not paths:
            print('MISSING MEDIA', sid); continue
        tv = d.get('time_vietnam')
        when = 'now'
        if tv and len(tv) == 16:
            dt = datetime.datetime.strptime(tv, '%Y-%m-%d %H:%M')
            if dt > now + datetime.timedelta(minutes=lead):
                when = tv
        sort = tv if (tv and len(tv) == 16) else date + ' ' + (d.get('time') or '00:00')
        items.append({'slot': sid, 'type': typ, 'files': paths, 'body': body, 'tags': tags,
                      'when': when, 'sort': sort, 'version': None, 'title': d.get('title', '')})
    items.sort(key=lambda x: x['sort'])
    os.makedirs(out_dir, exist_ok=True)
    json.dump(items, open(os.path.join(out_dir, 'items.json'), 'w'), indent=1, ensure_ascii=False)
    only = set(opt('--only', '').split(',')) - {''}
    store = {str(i): dict({k: x[k] for k in ('slot', 'body', 'tags', 'when')}, title=x['title'][:90])
             for i, x in enumerate(items) if not only or str(i) in only}
    open(os.path.join(out_dir, 'inject.js'), 'w').write(
        "localStorage.setItem('edl_tt'," + json.dumps(json.dumps(store, ensure_ascii=False), ensure_ascii=False)
        + ");'stored '+Object.keys(JSON.parse(localStorage.getItem('edl_tt'))).length;\n")
    for i, x in enumerate(items):
        print(i, x['slot'], x['type'], x['when'], len(x['files']), 'tags', len(x['tags']), 'chars', len(x['body']))


if __name__ == '__main__':
    main()
