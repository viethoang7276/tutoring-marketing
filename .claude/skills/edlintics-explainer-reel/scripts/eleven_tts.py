# ElevenLabs v3 voice for Edlintics reels (Hoang picked it 29 Oct 2026; voice gPiEpcKoaZywgOzc0Zn9).
# Used by vo.py and the puzzle-reel build.py when TTS_ENGINE=eleven. Returns float32 mono at 24 kHz, like Kokoro.
# Key: ELEVEN_LABS_TOKEN from the environment, else from the repo .env, else tutoring-content/.env.local. Never printed.
# Clips are cached by text, model and voice in tools/tts/cache-eleven/, so a rebuild never pays twice for the same line.
import hashlib, json, os, re, ssl, urllib.request, urllib.error
import numpy as np

VOICE = os.environ.get("ELEVEN_VOICE", "gPiEpcKoaZywgOzc0Zn9")
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_v3")
SR = 24000
# v3 ignores voice_settings.speed (tested 29 Oct 2026), so pace is set here with a pitch-preserving stretch.
# 1.12 keeps explainer reels near 40-47 s. The cache holds the untouched audio, so changing it costs no credits
TEMPO = float(os.environ.get("ELEVEN_TEMPO", "1.12"))
# v3 stability (18 Nov 2026, opt-in): 0.0 Creative, 0.5 Natural, 1.0 Robust. Left unset, the request and the cache key are exactly as before
STABILITY = os.environ.get("ELEVEN_STABILITY")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
CACHE = os.path.join(REPO, "tools/tts/cache-eleven")


def _ssl_ctx():
    """A TLS context that verifies ElevenLabs on any Python here (18 Nov 2026): the python.org framework Python has no CA store, so
    without SSL_CERT_FILE it failed with CERTIFICATE_VERIFY_FAILED. Order: SSL_CERT_FILE, certifi's bundle, the macOS system bundle"""
    ctx = ssl.create_default_context()
    if os.environ.get("SSL_CERT_FILE") or ctx.cert_store_stats().get("x509_ca"): return ctx
    cands = []
    try:
        import certifi; cands.append(certifi.where())
    except ImportError: pass
    cands += ["/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem", "/usr/local/etc/openssl/cert.pem", "/opt/homebrew/etc/openssl@3/cert.pem"]
    for f in cands:
        if os.path.exists(f):
            try: ctx.load_verify_locations(cafile=f); return ctx
            except ssl.SSLError: continue
    return ctx


def _key():
    if os.environ.get("ELEVEN_LABS_TOKEN"): return os.environ["ELEVEN_LABS_TOKEN"].strip()
    for p in (os.path.join(REPO, ".env"), os.path.join(REPO, "../tutoring-content/.env.local")):
        if os.path.exists(p):
            m = re.search(r"^ELEVEN_LABS_TOKEN=(.*)$", open(p).read(), re.M)
            if m: return m.group(1).strip().strip("\"'")
    raise SystemExit("ELEVEN_LABS_TOKEN not found (env, .env or ../tutoring-content/.env.local)")

def _tempo(a, tempo):
    import subprocess, imageio_ffmpeg
    p = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", f"atempo={tempo}", "-f", "f32le", "-"], input=a.tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()

def say(text, tempo=None, voice=None, stability=None):
    """One line of voice as float32 at 24 kHz, trimmed of leading and trailing silence. tempo overrides ELEVEN_TEMPO for this line;
    voice overrides ELEVEN_VOICE; stability (0.0 Creative, 0.5 Natural, 1.0 Robust) overrides ELEVEN_STABILITY. Audio tags such as
    [calm] or [warm] and pauses ("..." or an em dash) go in the text itself"""
    tp = TEMPO if tempo is None else float(tempo)
    vc = voice or VOICE
    st = stability if stability is not None else STABILITY
    st = None if st in (None, "") else float(st)
    os.makedirs(CACHE, exist_ok=True)
    key = f"{MODEL}|{vc}|{text}" + ("" if st is None else f"|st={st:g}")   # no stability = the same cache key as before
    f = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest()[:16] + ".pcm")
    if not os.path.exists(f):
        body = {"text": text, "model_id": MODEL}
        if st is not None: body["voice_settings"] = {"stability": st}
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vc}?output_format=pcm_24000",
            data=json.dumps(body).encode(), headers={"xi-api-key": _key(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120, context=_ssl_ctx()) as r: data = r.read()
        except urllib.error.HTTPError as e:
            raise SystemExit(f"ElevenLabs {e.code}: {e.read()[:300].decode(errors='replace')}")
        open(f, "wb").write(data)
    a = np.frombuffer(open(f, "rb").read(), dtype="<i2").astype(np.float32) / 32768.0
    if tp != 1.0: a = _tempo(a, tp)
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 600): nz[-1] + 3600] if len(nz) else a   # 25 ms before, 150 ms after the voiced part
