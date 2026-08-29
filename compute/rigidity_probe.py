"""P2: measuring the rigidity invariant (ROADMAP §R, A9.14 follow-up).

The rigid seed B4 = (925, 79464, 501600) — the m = 925 three-sieve
passer — stays at ~6 dead lines through two decades of scaling with
no local, character, or congruence lock anywhere (a9.local_locks,
a9.joint_locks).  This probe measures WHERE in the A9.12 system the
death lives, rung by rung, for the rigid seed against the broad
fertile control F2 = (725, 171600, 282576):

per rung q, per line, per admissible stratum:
  - pairwise: does each of the three pair equations have a witness
    (t, k), and how many (capped);
  - joint: among the pair-witness combinations, how close does the
    syzygy det_3 = 0 come (record whether it ever hits, and the
    minimum |b3 -+ 2 t12 t13 t23| normalized witness distance);
  - the verdict shape: PAIR-DEAD (some pair equation empty) vs
    SYZYGY-DEAD (pairs alive, coupling never closes) vs ALIVE.

If B4's dead lines are systematically SYZYGY-DEAD across rungs while
F2's convert to ALIVE, the rigidity invariant lives in the coupling
variety — spinor-norm / compatibility territory, not representability.

Artifact: data_rigidity_probe.json
Run:  python -m compute.rigidity_probe
"""

from __future__ import annotations

import json
import os
from math import gcd, isqrt

from .sphere_gluing import pair_lines
from .gram_sieve import pair_witnesses_fast

SEEDS = [("B4-rigid", 925, 79464, 501600),
         ("F2-broad", 725, 171600, 282576)]

QS = (1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 19, 25)

CAP = 40  # witnesses per pair equation, per stratum

OUT = os.path.join(os.path.dirname(__file__), "data_rigidity_probe.json")


def line_autopsy(tri, n):
    """Per-stratum autopsy of one line.  Returns a list of stratum
    records and the line verdict."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    recs = []
    verdict = "PAIR-DEAD"
    for g in range(1, isqrt(min(G, n)) + 1):
        if G % (g * g) or n % (g * g):
            continue
        w = [t // (g * g) for t in tri]
        N = n // (g * g)
        pw = []
        empty = False
        for i, j in ((0, 1), (0, 2), (1, 2)):
            ws_ = pair_witnesses_fast(w[i], w[j], N)
            if not ws_:
                empty = True
                pw.append(0)
            else:
                pw.append(min(len(ws_), CAP))
        if empty:
            recs.append({"g": g, "pairs": pw, "syzygy": None})
            continue
        # pairs all alive at this stratum: search the syzygy
        W12 = pair_witnesses_fast(w[0], w[1], N)[:CAP]
        W13 = pair_witnesses_fast(w[0], w[2], N)[:CAP]
        W23 = pair_witnesses_fast(w[1], w[2], N)[:CAP]
        w123 = w[0] * w[1] * w[2]
        best = None
        hit = False
        for t12, _ in W12:
            for t13, _ in W13:
                for t23, _ in W23:
                    b3 = (w123 - w[0] * t23 * t23 - w[1] * t13 * t13
                          - w[2] * t12 * t12)
                    for s in (1, -1):
                        d = abs(b3 - s * 2 * t12 * t13 * t23)
                        if best is None or d < best:
                            best = d
                        if d == 0:
                            hit = True
        recs.append({"g": g, "pairs": pw, "syzygy": bool(hit),
                     "min_defect_digits": len(str(best)) if best
                     is not None else None})
        if hit:
            verdict = "ALIVE"
        elif verdict != "ALIVE":
            verdict = "SYZYGY-DEAD"
    return verdict, recs


def main():
    rows = []
    for tag, m0, U0, V0 in SEEDS:
        for q in QS:
            m, U, V = q * m0, q * q * U0, q * q * V0
            n = 3 * m * m
            for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
                if i in (0, 1):
                    continue  # real lines never die (A9.6)
                verdict, recs = line_autopsy(tri, n)
                rows.append({"seed": tag, "q": q, "m": m, "line": i,
                             "verdict": verdict, "strata": recs})
                print(f"{tag} q={q} line {i}: {verdict} "
                      f"({len(recs)} strata)", flush=True)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(rows, fh)
    # summary
    from collections import Counter
    for tag, *_ in SEEDS:
        c = Counter(r["verdict"] for r in rows if r["seed"] == tag)
        print(f"{tag}: {dict(c)}")
    print(f"DONE -> {OUT}")


if __name__ == "__main__":
    main()
