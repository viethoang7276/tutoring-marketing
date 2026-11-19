import json,glob,os,re,sys,time,shutil,collections,datetime
SL=sys.argv[1]; apply='--apply' in sys.argv
os.chdir('/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing')
R='assets/renders'
PROTECT=['assets/renders/lessons/','assets/renders/ads/','assets/renders/social/','assets/renders/cover-templates/','assets/renders/thumbnails-v2/','assets/renders/hub/','assets/renders/hub-archive/','assets/renders/demo-reels/','assets/renders/thumbnails/']
MEDIA=('.mp4','.mov','.wav','.mp3','.m4a','.png','.jpg','.jpeg','.webm','.gif','.webp','.aac')
refs=collections.defaultdict(set); st={}; onhub=set()
def walk(o,out):
    if isinstance(o,dict): [walk(v,out) for v in o.values()]
    elif isinstance(o,list): [walk(v,out) for v in o]
    elif isinstance(o,str):
        for m in re.findall(r'(?:/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/)?(assets/renders/[^\s"\',;)]+)',o): out.add(m)
for f in glob.glob(SL+'/*.json'):
    d=json.load(open(f)); sid=os.path.basename(f)[:-5]
    pend=any(d.get(k) is True for k in ('thPending','ttPending','igManual'))
    st[sid]=(d.get('status'),pend)
    if d.get('videoUrl') and not d.get('videoArchived'): onhub.add(sid)
    s=set(); walk(d,s)
    for p in s: refs[p].add(sid)
reffiles=set(refs)
def slots_for(path):
    ids=set()
    for p,s in refs.items():
        if p.startswith(os.path.dirname(path)+'/') or os.path.dirname(p)==os.path.dirname(path): ids|=s
    b=os.path.basename(os.path.dirname(path))
    ids|={i for i in st if len(i)>8 and i in b}
    return ids
now=time.time(); cand=[]
for r,ds,fs in os.walk(R):
    if any((r+'/').startswith(x) for x in PROTECT): continue
    for f in fs:
        if not f.lower().endswith(MEDIA): continue
        p=os.path.join(r,f)
        if now-os.path.getmtime(p)<48*3600: continue
        if p in reffiles: 
            # referenced file: keep unless its slots are all fully posted AND archived off hub
            ids=refs[p]; done=all(st.get(i,(None,True))[0] in('posted','published') and not st[i][1] for i in ids if i in st)
            if not done or ids & onhub: continue
            if f.endswith('.mp4') and any(i not in onhub for i in ids): 
                # posted + archived: hub-archive holds the backup when archived; keep if no archive copy
                if not any(os.path.exists(f'assets/renders/hub-archive/{i}') for i in ids): continue
            cand.append(('ref-posted-archived',p)); continue
        ids=slots_for(p)
        live=[i for i in ids if i in st and (st[i][0] not in ('posted','published') or st[i][1])]
        if f=='voiceover.wav' and live: continue
        if ids and live and f.endswith('.mp4') and r.count('/')<=4 and not re.search(r'(preview|canva|music|contact|-v\d|old|test)',f):
            continue  # possible final of a live post, keep
        cand.append(('unreferenced' if not ids else 'variant/intermediate',p))
tot=collections.Counter(); 
for k,p in cand: tot[k]+=os.path.getsize(p)
print({k:round(v/1e9,2) for k,v in tot.items()}, 'files',len(cand),'GB',round(sum(tot.values())/1e9,2))
top=collections.Counter()
for k,p in cand: top['/'.join(p.split('/')[:3])]+=os.path.getsize(p)
print({k:round(v/1e9,2) for k,v in top.most_common(12)})
import sys as _s
if "--list" in _s.argv:
    [print(k,p) for k,p in cand if p.endswith(".mp4")]
if apply:
    T=os.path.expanduser('~/.Trash/edlintics-renders-cleanup-'+datetime.date.today().isoformat()); os.makedirs(T,exist_ok=True)
    with open(T+'/MANIFEST.tsv','a') as fh:
        for k,p in cand:
            os.makedirs(os.path.join(T,os.path.dirname(p)),exist_ok=True); s=os.path.getsize(p); shutil.move(p,os.path.join(T,p)); fh.write(f'{k}\t{s}\t{p}\n')
    print('moved',len(cand))
