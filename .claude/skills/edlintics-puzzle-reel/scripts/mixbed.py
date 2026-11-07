"""Mix a music bed under a puzzle reel voice track the way mix_audio.py does (bed 12 LU under the voice, mix at -17.5 LUFS, limiter), then mux into the video.
Usage: python mixbed.py <work audio.wav> <video.mp4 (silent source ok)> <bed file> <out.mp4>"""
import os, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
voice_in, video, bed_in, out = sys.argv[1:5]
tmp = tempfile.mkdtemp()

def lufs(f):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    r = r[r.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", r)[1]), float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", r)[1])

v48, b48 = f"{tmp}/v.wav", f"{tmp}/b.wav"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", voice_in, "-ar", "48000", "-ac", "2", v48], check=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-i", bed_in, "-ar", "48000", "-ac", "2", b48], check=True)
v, _ = sf.read(v48, dtype="float32"); bed, _ = sf.read(b48, dtype="float32")
n = len(v)
if len(bed) < n: bed = np.concatenate([bed] * (n // len(bed) + 1))
bed = bed[:n].copy(); t = np.arange(n) / 48000
bed *= (np.clip(t / 0.6, 0, 1) * np.clip((t[-1] - t) / 1.0, 0, 1))[:, None]
sf.write(f"{tmp}/bed.wav", bed, 48000)
Iv, _ = lufs(v48); Ib, _ = lufs(f"{tmp}/bed.wav")
sf.write(f"{tmp}/mix.wav", np.clip(v + 10 ** ((Iv - 12 - Ib) / 20) * bed, -1, 1), 48000)
target = -17.5; I, _ = lufs(f"{tmp}/mix.wav"); gain = target - I
for _ in range(5):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{tmp}/mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:attack=4:release=60:level=0", "-ar", "48000", "-ac", "2", f"{tmp}/final.wav"], check=True)
    I2, pk = lufs(f"{tmp}/final.wav")
    if abs(I2 - target) < 0.25: break
    gain += target - I2
subprocess.run([FF, "-y", "-loglevel", "error", "-i", video, "-i", f"{tmp}/final.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True)
print(f"{os.path.basename(out)}: voice {Iv:.1f} LUFS, bed 12 LU under, mix {I2:.1f} LUFS, peak {pk:.1f} dBFS, {os.path.getsize(out)/1e6:.2f} MB")
