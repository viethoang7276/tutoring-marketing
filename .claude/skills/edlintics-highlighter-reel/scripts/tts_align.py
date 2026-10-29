"""ElevenLabs v3 voice WITH word timings, for the highlighter reel (captions and highlights follow the real words).
Same voice, model, tempo and key lookup as the explainer engine's eleven_tts.py. Cached per line in
tools/tts/cache-eleven/<hash>-ts.json (audio + character alignment), so a rebuild costs no credits.
say_words(text) -> (float32 audio at 24 kHz, trimmed; [(word, start_s, end_s), ...] on the trimmed, tempo-adjusted clip)
"""
import base64, hashlib, json, os, re, sys, urllib.request, urllib.error
import numpy as np
REPO = "/Users/hoangtruong/Desktop/WebDevelopment/tutoring/edlintics-marketing"
sys.path.insert(0, f"{REPO}/.claude/skills/edlintics-explainer-reel/scripts")
import eleven_tts as E   # VOICE, MODEL, TEMPO, SR, CACHE, _key, _tempo

def _fetch(text):
    os.makedirs(E.CACHE, exist_ok=True)
    f = os.path.join(E.CACHE, hashlib.sha1(f"{E.MODEL}|{E.VOICE}|{text}|ts".encode()).hexdigest()[:16] + "-ts.json")
    if os.path.exists(f): return json.load(open(f))
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{E.VOICE}/with-timestamps?output_format=pcm_24000",
        data=json.dumps({"text": text, "model_id": E.MODEL}).encode(), headers={"xi-api-key": E._key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r: d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"ElevenLabs {e.code}: {e.read()[:300].decode(errors='replace')}")
    json.dump(d, open(f, "w")); return d

def say_words(text):
    d = _fetch(text)
    a = np.frombuffer(base64.b64decode(d["audio_base64"]), dtype="<i2").astype(np.float32) / 32768.0
    al = d.get("alignment") or d.get("normalized_alignment")
    if E.TEMPO != 1.0: a = E._tempo(a)
    nz = np.where(np.abs(a) > 0.01)[0]; s0 = max(0, nz[0] - 600) if len(nz) else 0
    a = a[s0: (nz[-1] + 1200) if len(nz) else len(a)]; off = s0 / E.SR
    words, cur, ws = [], "", None
    for ch, st, en in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        st, en = st / E.TEMPO - off, en / E.TEMPO - off
        if re.match(r"[\w$%'-]", ch):
            if not cur: ws = st
            cur += ch; we = en
        elif cur:
            words.append((cur, round(max(0, ws), 3), round(we, 3))); cur = ""
    if cur: words.append((cur, round(max(0, ws), 3), round(we, 3)))
    return a, words

if __name__ == "__main__":
    a, w = say_words(sys.argv[1]); print(round(len(a) / E.SR, 2), w)
