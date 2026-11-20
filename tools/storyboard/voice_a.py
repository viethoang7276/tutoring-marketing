#!/usr/bin/env python3
"""Voice for demo video A: one ElevenLabs clip per scene (cached in tools/tts/cache-eleven), written as WAV plus voice.json
with each clip's length. Run with tools/tts/.venv/bin/python voice_a.py <outdir>"""
import json, os, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.claude/skills/edlintics-explainer-reel/scripts'))
import eleven_tts

VOICE, TEMPO, TAG = 'vChnJZ1Cu89g2XXumPfT', 1.0, '[warm] '
LINES = [
    ('A1', 'Languages, coding and science have moved onto your phone, but business is still stuck in books'),
    ('A2', 'So we opened the door. In accounting, you drag a debit and a credit, and watch them balance'),
    ('A3', 'In finance, change one number and watch interest earn interest, from personal savings to corporate decisions'),
    ('A4', 'In statistics, you solve real problems, and get a simple explanation for every answer'),
    ('A5', 'Lessons in accounting, finance, economics and statistics, all in one place'),
    ('A6', 'From your first journal entry in accounting, to complex models like I S and L M in economics'),
    ('A7', 'Every topic starts with a free card'),
    ('A8', 'Get started for free, on Edlintics dot com'),
]
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
meta = []
for name, text in LINES:
    a = eleven_tts.say(TAG + text, tempo=TEMPO, voice=VOICE)
    sf.write(os.path.join(out, f'{name}.wav'), a, eleven_tts.SR)
    meta.append({'scene': name, 'text': text, 'dur': round(len(a) / eleven_tts.SR, 3)})
    print(name, meta[-1]['dur'])
json.dump(meta, open(os.path.join(out, 'voice.json'), 'w'), indent=1)
print('total', round(sum(m['dur'] for m in meta), 2))
