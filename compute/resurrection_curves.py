"""Resurrection curves: per-line sieve profiles along scaling ladders.

The ladder sweep (A9.13, data_ladder_sweep.json) showed fertility is
seed-intrinsic and bimodal: the 725 seeds resurrect broadly (any large
q), the 925/1025 seeds only along multiples of their own prime (37,
41), and most seeds not at all.  To separate the candidate mechanisms
(local obstruction at a fixed prime vs class-size obstruction), this
job records the FULL profile — coherence + the exact dead-line set —
for a panel of fertile and barren seeds over a designed q-grid:
all q in [2, 44], plus multiples of the relevant primes (17, 29, 37,
41) and a spread of composite/large q, capped at scaled center
m <= 120000.

Artifact: data_resurrection_curves.json
  rows: [tag, m0, U0, V0, q, m, coherent, dead_lines]

Run:  python -m compute.resurrection_curves
"""

from __future__ import annotations

import json
import os

from .sphere_gluing import coherent_pair, pair_lines
from .gram_sieve import syzygy_line_ok_fast

SEEDS = [
    ("F1-broad", 725, 122400, 282576),
    ("F2-broad", 725, 171600, 282576),
    ("N1-37", 925, 79464, 525000),
    ("N2-41", 1025, 130944, 450000),
    ("B1-425", 425, 54600, 72384),
    ("B2-425", 425, 54600, 97104),
    ("B3-425", 425, 72384, 97104),
    ("B4-passer925", 925, 79464, 501600),
    ("B5-1025", 1025, 450000, 564816),
    ("B6-845", 845, 205656, 507000),
]

M_CAP = 120000

OUT = os.path.join(os.path.dirname(__file__),
                   "data_resurrection_curves.json")


def q_grid(m0):
    qs = set(range(2, 45))
    for p in (17, 29, 37, 41):
        qs.update(p * i for i in range(1, M_CAP // (p * m0) + 1))
    qs.update((48, 52, 56, 60, 66, 72, 77, 84, 90, 96, 105, 112, 120,
               128, 133, 140, 145))
    return sorted(q for q in qs if q * m0 <= M_CAP)


def profile(m, U, V):
    coh = coherent_pair(m, U, V)
    n = 3 * m * m
    dead = [i for i, tri in enumerate(pair_lines(2 * m * m, U, V))
            if not syzygy_line_ok_fast(tri, n)]
    return coh, dead


def main():
    rows = []
    for tag, m0, U0, V0 in SEEDS:
        print(f"{tag}: base ({m0}, {U0}, {V0})", flush=True)
        for q in q_grid(m0):
            m, U, V = q * m0, q * q * U0, q * q * V0
            coh, dead = profile(m, U, V)
            rows.append([tag, m0, U0, V0, q, m, coh, dead])
            print(f"  q={q:4d} m={m:6d}: coherent={int(coh)} "
                  f"dead={dead}", flush=True)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump({"m_cap": M_CAP, "rows": rows}, fh)
    print(f"DONE: {len(rows)} profiles -> {OUT}")


if __name__ == "__main__":
    main()
