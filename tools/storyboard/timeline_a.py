"""Scene lengths and voice starts of demo video A (30-second cut, 20 Nov 2026). film_a.py and both anim files read this; change lengths only here."""
TIMELINE = [('A1', 5.35), ('T1', 0.35), ('A2', 2.49), ('T2', 0.35), ('A3', 2.62), ('T3', 0.35), ('A4', 2.5), ('T4', 0.35), ('A6', 3.08), ('T6', 0.35), ('A7', 4.75), ('TR', 0.35), ('R', 3.39), ('T7', 0.35), ('A8', 2.76)]
DUR = dict(TIMELINE)
# (voice clip, film second at which it starts); clips run across the short transitions
VOICE = [('A1', 0.2), ('A2', 5.43), ('A3', 8.27), ('A4', 11.24), ('A6', 14.09), ('A7', 17.52), ('R', 22.62), ('A8', 26.36)]
