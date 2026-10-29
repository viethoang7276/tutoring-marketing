# ElevenLabs v3 voice for Edlintics reels (Hoang picked it 29 Oct 2026; voice gPiEpcKoaZywgOzc0Zn9).
# Used by vo.py and the puzzle-reel build.py when TTS_ENGINE=eleven. Returns float32 mono at 24 kHz, like Kokoro.
# Key: ELEVEN_LABS_TOKEN from the environment, else from the repo .env, else tutoring-content/.env.local. Never printed.
# Clips are cached by text, model and voice in tools/tts/cache-eleven/, so a rebuild never pays twice for the same line.
import hashlib, json, os, re, urllib.request, urllib.error
import numpy as np

VOICE = os.environ.get("ELEVEN_VOICE", "gPiEpcKoaZywgOzc0Zn9")
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_v3")
SR = 24000
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
CACHE = os.path.join(REPO, "tools/tts/cache-eleven")

def _key():
    if os.environ.get("ELEVEN_LABS_TOKEN"): return os.environ["ELEVEN_LABS_TOKEN"].strip()
    for p in (os.path.join(REPO, ".env"), os.path.join(REPO, "../tutoring-content/.env.local")):
        if os.path.exists(p):
            m = re.search(r"^ELEVEN_LABS_TOKEN=(.*)$", open(p).read(), re.M)
            if m: return m.group(1).strip().strip("\"'")
    raise SystemExit("ELEVEN_LABS_TOKEN not found (env, .env or ../tutoring-content/.env.local)")

def say(text):
    """One line of voice as float32 at 24 kHz, trimmed of leading and trailing silence"""
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, hashlib.sha1(f"{MODEL}|{VOICE}|{text}".encode()).hexdigest()[:16] + ".pcm")
    if not os.path.exists(f):
        body = {"text": text, "model_id": MODEL}
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=pcm_24000",
            data=json.dumps(body).encode(), headers={"xi-api-key": _key(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
        except urllib.error.HTTPError as e:
            raise SystemExit(f"ElevenLabs {e.code}: {e.read()[:300].decode(errors='replace')}")
        open(f, "wb").write(data)
    a = np.frombuffer(open(f, "rb").read(), dtype="<i2").astype(np.float32) / 32768.0
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a
