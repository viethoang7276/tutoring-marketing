"""Scene lengths and voice starts of demo video A (20 Nov 2026). film_a.py and both anim files read this; change lengths only here.
Version "a" opens on the door with Ledger (A1, T1); version "b" opens on a computer screen with an Open button and no Ledger (B1, TB)."""
TIMELINE = [('A1', 6.13), ('T1', 0.35), ('A2', 2.96), ('T2', 0.35), ('A3', 3.12), ('T3', 0.35), ('A4', 2.96), ('T4', 0.35), ('A6', 3.61), ('T6', 0.35), ('A7', 5.47), ('TR', 0.35), ('R', 3.97), ('T7', 0.35), ('A8', 3.18)]
TIMELINE_B = [('B1', 2.91), ('TB', 0.35), ('A2', 2.96), ('T2', 0.35), ('A3', 3.12), ('T3', 0.35), ('A4', 2.96), ('T4', 0.35), ('A6', 3.61), ('T6', 0.35), ('A7', 5.47), ('TR', 0.35), ('R', 3.97), ('T7', 0.35), ('A8', 3.18)]
DUR = dict(TIMELINE + TIMELINE_B)
# (voice clip, film second at which it starts); clips start just inside the short transitions
VOICE = [('A1', 0.25), ('A2', 6.23), ('A3', 9.54), ('A4', 13.01), ('A6', 16.32), ('A7', 20.28), ('R', 26.1), ('A8', 30.42)]
VOICE_B = [('B1', 0.25), ('A2', 3.01), ('A3', 6.32), ('A4', 9.79), ('A6', 13.1), ('A7', 17.06), ('R', 22.88), ('A8', 27.2)]
