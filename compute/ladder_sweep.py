"""The scaled-pair ladder sweep (A9.13 hunting, ROADMAP W6).

Lemma A9.13: sieve verdicts only soften along
(m, U, V) -> (qm, q^2 U, q^2 V).  Both special pairs of the fresh
range are such scalings of base pairs at the anatomy centers (the
C2-exception = 29 . the 725 passer; the golden = 37 . a coherence-dead
925 pair).  So the thin, motivated hunting family for new golden
centers is the ladder over ALL base positivity pairs at the anatomy
centers — incoherent bases included, since coherence can flip on.

Sweep: base centers = the nine passer centers of PASSERS_1200; base
pairs = all ordered positivity pairs there; q such that the scaled
center lands in (53400, LIMIT] (below 53400 the desert already
verified every pair dead).  For each scaled pair: coherence, then
dead-line count with early exit at 2 (we only care about golden = 0
dead and near = 1 dead).  Pure stdlib.

Run:  python -m compute.ladder_sweep [LIMIT]
"""

from __future__ import annotations

import json
import os
import sys

from .congrua_search import congrua_sets
from .sphere_gluing import coherent_pair, pair_lines
from .gram_sieve import syzygy_line_ok_fast

ANATOMY_CENTERS = (425, 481, 725, 845, 850, 901, 925, 962, 1025)
DESERT_VERIFIED = 53400

OUT = os.path.join(os.path.dirname(__file__), "data_ladder_sweep.json")


def base_pairs(m):
    """All ordered positivity pairs (U, V) at center m."""
    D = sorted(dict(congrua_sets(m)).get(m, set()))
    return [(U, V) for U in D for V in D if U != V and U + V <= m * m]


def sweep(limit=150000, verbose=True):
    hits = []          # (m1, U1, V1, q, m0, U0, V0, ndead)
    tested = coherent = 0
    for m0 in ANATOMY_CENTERS:
        bases = base_pairs(m0)
        if verbose:
            print(f"center {m0}: {len(bases)} base pairs", flush=True)
        q_lo = DESERT_VERIFIED // m0 + 1
        for q in range(max(2, q_lo), limit // m0 + 1):
            m1 = q * m0
            if not (DESERT_VERIFIED < m1 <= limit):
                continue
            n1 = 3 * m1 * m1
            twom2 = 2 * m1 * m1
            for (U0, V0) in bases:
                U1, V1 = q * q * U0, q * q * V0
                tested += 1
                if not coherent_pair(m1, U1, V1):
                    continue
                coherent += 1
                ndead = 0
                for tri in pair_lines(twom2, U1, V1):
                    if not syzygy_line_ok_fast(tri, n1):
                        ndead += 1
                        if ndead >= 2:
                            break
                if ndead <= 1:
                    hits.append((m1, U1, V1, q, m0, U0, V0, ndead))
                    if verbose:
                        tag = "GOLDEN" if ndead == 0 else "NEAR (1 dead)"
                        print(f"  {tag}: m={m1} = {q}.{m0}, "
                              f"(U,V) = {q}^2 . ({U0},{V0})", flush=True)
        if verbose:
            print(f"  cumulative: tested={tested}, coherent={coherent}, "
                  f"hits={len(hits)}", flush=True)
    return {"limit": limit, "window_lo": DESERT_VERIFIED,
            "centers": list(ANATOMY_CENTERS), "tested": tested,
            "coherent": coherent, "hits": hits}


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 150000
    res = sweep(limit)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh)
    print(f"LADDER SWEEP DONE: window ({res['window_lo']}, {limit}], "
          f"tested {res['tested']}, coherent {res['coherent']}, "
          f"hits {len(res['hits'])}")
    for h in res["hits"]:
        print("  HIT:", h)


if __name__ == "__main__":
    main()
