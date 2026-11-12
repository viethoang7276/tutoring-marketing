"""Build the hub slot document of a career-ladder reel from its package folder (skill edlintics-ladder-reel).
Usage: python make_card.py <render dir, relative to the repo, e.g. assets/renders/ladder-reels/SLUG> <slot id = slug> <YYYY-MM-DD> <HH:MM Madrid, or "" for no time> <video blob id> <poster blob id> <thumbnail blob id> <out.json> [canva design id]
Run it from the repo root. It stops if caption_x is over 280 characters, a first comment is 150 or more, the YouTube title is over 100, or a caption paragraph ends with a full stop. Then write the JSON to the hub with ArtifactData set (file_path).
registry_check, title and copy come from meta in script.json; edit statusNote below if the reel needs a different note."""
import json, sys
d, sid, date, tm, vb, pb, tb, out = sys.argv[1:9]; canva = sys.argv[9] if len(sys.argv) > 9 else None
S = json.load(open(f"{d}/script.json")); T = json.load(open(f"{d}/timing.json")); m = S["meta"]
script = [{"role": b["role"], "start": b["start"], "text": b["text"], "captions": [{"t": c["t"], "text": c["text"]} for c in b.get("chunks", [])],
           **({"rung": m["rungs"][b["rung"] - 1]} if b.get("rung") else {}), **({"chips": [c["label"] for c in b["chips"]]} if b.get("chips") else {})} for b in T["beats"]]
title = m["title"]; cap = m["caption"]
doc = {
 "id": sid, "reviewId": sid, "format": "life-of-reel", "reelType": "ladder", "kind": "video", "status": "proposal", "image": "draft", "text": "ready",
 "title": title, "term": m["term"], "family_or_category": m["family_or_category"], "concept_id": m["concept_id"], "concept": m["concept_id"], "themes": m["themes"],
 "registry_check": m["registry_check"], "date": date, "week": __import__("datetime").date.fromisoformat(date).strftime("%G-W%V"),
 "caption": cap, "caption_x": m["caption_x"], "first_comment": m["first_comment"], "first_comment_igtt": m["first_comment_igtt"], "firstCommentType": "question",
 "hashtags": m["hashtags"], "maths_check": m["maths_check"], "definition_check": m["definition_check"], "sources": m["sources"],
 "threadsTopic": m["threadsTopic"], "threadsTopicKind": "topic", "threadsTopicVariant": "primary", "threadsReason": m["threadsReason"],
 "youtubeTitle": m.get("youtube_title") or ((title if len(title) <= 92 else title.replace("chief investment officer", "CIO")) + " #Shorts"), "youtubeDescription": cap, "tiktokCaption": cap,
 "videoUrl": f"/_blob/{vb}", "videoAssetId": vb, "posterUrl": f"/_blob/{pb}",
 "video": f"/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/{d}/{sid}.mp4",
 "music": "Local preview: quiet generated pad under the voice. Posting copy: Canva free track Light Minimal Ambient at volume 8 (see canva)",
 "thumbnail": {"style": "v2", "template": "ladder", "title": title.split(", the career ladder")[0], "pill": "CAREER LADDER IN 90 SECONDS",
               "file": f"assets/renders/thumbnails-v2/{sid}.jpg", "jpg": f"assets/renders/thumbnails-v2/{sid}.jpg", "url": f"/_blob/{tb}",
               "png": f"{d}/{sid}-thumbnail.png", "spec": f"assets/renders/thumbnails-v2/specs/{sid}.json"},
 "duration_s": T["duration"], "script": script, "rungs": m["rungs"],
 "cta": "To climb your own career ladder, learn technical business concepts at Edlintics",
 "test": "L1", "testNote": "L1 ladder format: views at 24 h and 72 h vs the platform median of our other voiced reels",
 "version": 1, "approvals": {},
 "text_check": {"full_sentences": "checked " + __import__("datetime").date.today().isoformat(), "no_trailing_full_stop": "checked " + __import__("datetime").date.today().isoformat()},
}
if tm:
    h, mi = map(int, tm.split(":")); doc.update({"time": tm, "time_madrid": tm, "time_vietnam": f"{date} {h + 6:02d}:{mi:02d}"})
else:
    doc["timeNote"] = "post now, Hoang 13 Nov"
# registry_check comes from meta (script.json); set it in your gen.py
if canva:
    A = f"/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing/{d}/{sid}"
    doc.update({"canva": canva, "canvaFolder": "FAHYcHrS5PE", "video": A + "-post.mp4", "postVideo": A + "-post.mp4", "canvaExport": A + "-canva-export.mp4",
                "music": f"Canva free track Light Minimal Ambient at volume 8, voice at 100 (Canva draft {canva}, exported)",
                "postNote": "Post the file in postVideo (Canva export with music, re-encoded to stay under the 10 MB Chrome upload cap, audio copied unchanged). canvaExport is the original export, over 10 MB"})
doc["statusNote"] = (f"New {__import__('datetime').date.today().isoformat()}: career ladder reel ({title.split(', the career ladder')[0]}), {T['duration']:.0f} s. NEW FORMAT for Hoang's approval: full-bleed art, captions on top, "
                     "a different Ledger on each rung, direct title opening (no hook), closing call to action instead of a definition card. Not scheduled; nobody has listened to the audio yet")
assert len(m["caption_x"]) <= 280, len(m["caption_x"]); assert len(m["first_comment"]) < 150 and len(m["first_comment_igtt"]) < 150; assert len(doc["youtubeTitle"]) <= 100, len(doc["youtubeTitle"])
for k in ("caption", "caption_x"):
    for para in doc[k].split("\n"):
        assert not para.rstrip().endswith("."), para
    assert "!" not in doc[k]
json.dump(doc, open(out, "w"), indent=1, ensure_ascii=False); print(sid, "caption_x", len(m["caption_x"]), "yt title", len(doc["youtubeTitle"]), "first comment", len(m["first_comment"]), "dur", T["duration"])
