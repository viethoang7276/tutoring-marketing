#!/usr/bin/env python3
"""Daily clean-up of old local renders (Hoang, 18 Nov 2026: "make it the rules with every day session to delete old files").

Input: a folder of hub `slots` documents saved as JSON (ArtifactData list collection=slots out_dir=<dir>).
Moves to ~/.Trash/edlintics-renders-cleanup-<date>/ (repo tree kept, MANIFEST.tsv written), never rm:
  A  media of posts that are fully posted (status posted/published, no thPending/ttPending/igManual true)
  B  check images (stills/ mid/ review/ v0/ v1/ frames/ tiles/ spill/ contact/ previous/, contact sheets, fps tiles)
     and mixed audio.wav / audio-yt.wav in folders whose posts are all scheduled or posted
Kept always: final mp4s of anything not fully posted or not yet archived off the hub (step 7), voiceover.wav, thumbnails, scripts/json/md, and the
protected folders below. Anything modified in the last 48 h is kept (it may be mid-build).
Usage: cleanup_renders.py <slots_json_dir>            (dry run, prints the summary)
       cleanup_renders.py <slots_json_dir> --apply    (moves the files)
"""
import json, os, re, sys, glob, shutil, time, collections, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RENDERS = 'assets/renders'
MEDIA = ('.mp4', '.mov', '.wav', '.mp3', '.m4a', '.png', '.jpg', '.jpeg', '.webm', '.gif', '.webp', '.aac')
PROTECT = ['assets/renders/lessons/', 'assets/renders/ads/', 'assets/renders/social/', 'assets/renders/cover-templates/',
           'assets/renders/thumbnails-v2/', 'assets/renders/hub/', 'assets/renders/hub-archive/']
INTER = {'stills', 'mid', 'review', 'frames', 'sheets', 'v0', 'v1', 'tiles', 'spill', 'contact', 'previous', '_fps', '_thumb'}
RECENT_S = 48 * 3600


def walk_refs(o, out):
    if isinstance(o, dict):
        for v in o.values(): walk_refs(v, out)
    elif isinstance(o, list):
        for v in o: walk_refs(v, out)
    elif isinstance(o, str):
        for m in re.findall(r'assets/renders/[^\s"\',;)]+', o): out.add(m)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    slots_dir, apply = sys.argv[1], '--apply' in sys.argv
    os.chdir(REPO)
    st, refs, on_hub = {}, [], set()
    for f in glob.glob(os.path.join(slots_dir, '**', '*.json'), recursive=True):
        d = json.load(open(f)); d = d.get('data', d)
        sid = os.path.basename(f)[:-5]
        pend = any(d.get(k) is True for k in ('thPending', 'ttPending', 'igManual'))
        st[sid] = (d.get('status'), pend)
        if d.get('videoUrl') and not d.get('videoArchived'):
            on_hub.add(sid)
        s = set(); walk_refs(d, s)
        refs += [(p, sid) for p in s]
    if not st:
        print('no slot documents found'); sys.exit(1)
    leaves = set(r for r, _, fs in os.walk(RENDERS) if any(x.endswith('.mp4') for x in fs))
    def top(r):
        parts = r.split('/')
        for i in range(4, len(parts) + 1):
            c = '/'.join(parts[:i])
            if c in leaves: return c
        return r
    groups = collections.defaultdict(list)
    for l in leaves: groups[top(l)].append(l)
    now = time.time()
    man = collections.defaultdict(list)
    def prot(p): return any(p.startswith(x) for x in PROTECT)
    def add(cat, p):
        if prot(p) or now - os.path.getmtime(p) < RECENT_S: return
        man[cat].append((p, os.path.getsize(p)))
    for L in sorted(groups):
        if prot(L + '/'): continue
        ids = {sid for p, sid in refs if p == L or p.startswith(L + '/')}
        b = os.path.basename(L)
        ids |= {i for i in st if len(i) > 8 and (i == b or i == re.sub(r'-v\d+$', '', b) or i in b)}
        if not ids: continue  # unreferenced: left for a person to judge
        sts = [st[i] for i in ids if i in st]
        fully_posted = all(s in ('posted', 'published') and not pend for s, pend in sts)
        all_sched = all(s in ('scheduled', 'posted', 'published') for s, _ in sts)
        for r, _, fs in os.walk(L):
            rel = os.path.relpath(r, L).split('/')
            for f in fs:
                if not f.lower().endswith(MEDIA): continue
                p = os.path.join(r, f)
                if fully_posted:
                    # Keep the top-level final mp4s until the step-7 archive has taken the hub video
                    # (19 Nov 2026: three posts lost their only copies when the hub blob was already gone).
                    if rel == ['.'] and f.lower().endswith('.mp4') and ids & on_hub:
                        continue
                    add('A_posted', p)
                elif all_sched:
                    if rel[0] in INTER: add('B_checks', p)
                    elif rel == ['.'] and f in ('audio.wav', 'audio-yt.wav'): add('B_mixwav', p)
                    elif rel == ['.'] and f.endswith('.png') and re.search(r'contact|sheet|fps|tile', f): add('B_checks', p)
    seen, tot = set(), {}
    for k in sorted(man):
        man[k] = [x for x in man[k] if not (x[0] in seen or seen.add(x[0]))]
        tot[k] = (len(man[k]), round(sum(s for _, s in man[k]) / 1e9, 2))
    print('summary (files, GB):', tot, 'total GB', round(sum(v[1] for v in tot.values()), 2))
    if not apply:
        return
    T = os.path.expanduser('~/.Trash/edlintics-renders-cleanup-' + datetime.date.today().isoformat())
    os.makedirs(T, exist_ok=True)
    n = 0
    with open(os.path.join(T, 'MANIFEST.tsv'), 'a') as fh:
        for k in sorted(man):
            for p, s in man[k]:
                if not os.path.isfile(p): continue
                os.makedirs(os.path.join(T, os.path.dirname(p)), exist_ok=True)
                shutil.move(p, os.path.join(T, p)); n += 1
                fh.write(f'{k}\t{s}\t{p}\n')
    print('moved', n, 'files to', T)


if __name__ == '__main__':
    main()
