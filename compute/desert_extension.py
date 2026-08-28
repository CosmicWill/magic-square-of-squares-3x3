"""M12-D (ROADMAP W6): extend the three-sieve pair desert beyond
m = 1200 and hunt the first GOLDEN CENTERS — centers where an ordered
congrua pair survives positivity + coherence + representation.

Pipeline per center m with |D(m)| >= 2 (identical mathematics to
a9.pair_desert, engineering for scale):
  1. positivity:  U + V > m^2 kills;
  2. coherence:   Theorem A9.3 chi_p-coherence on all 8 lines;
  3. representation: a pair dies if ANY line's co-norm triple is
     represented by no single primitive class at any stratum
     (early-exit version of sphere_composition.killed_lines).
Survivors of all three sieves are GOLDEN CENTERS -> reported and
stored; they are the search targets of ROADMAP W6 and the
calibration data of W4.

Checkpointed: state in compute/data_desert_ext.json after every
center that reaches stage 3 (and every CHUNK centers overall);
safe to kill and rerun.  Run:

    python -m compute.desert_extension [BOUND=10000]
"""

import json
import os
import sys
import time
from math import gcd

from compute.congrua_search import congrua_sets
from compute.sphere_gluing import odd_primes, pair_lines, represents, \
    coherent_pair
from compute.sphere_composition import prims, strata

STATE = os.path.join(os.path.dirname(__file__), "data_desert_ext.json")
CHUNK = 25


def pair_killed_by_representation(m, U, V):
    """True iff some line's triple is representable by no class at any
    stratum (early exit on first killed line)."""
    n = 3 * m * m
    for tri in pair_lines(2 * m * m, U, V):
        killed = True
        for g, ct, D, th in strata(tri, n):
            pf = prims(D)
            if not pf:
                continue
            if any(all(represents(f, t) for t in th) for f in pf):
                killed = False
                break
        if killed:
            return True
    return False


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"done_upto": 1200,        # a9.pair_desert covers <= 1200
            "totals": {"centers": 0, "pairs": 0, "pos": 0, "coh": 0,
                       "rep": 0},
            "golden": [], "rep_killed_pairs": [], "log": []}


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(st, fh)
    os.replace(tmp, STATE)


def run(bound):
    st = load_state()
    start = st["done_upto"] + 1
    print(f"desert extension: centers {start}..{bound} "
          f"(state: {STATE})", flush=True)
    t0 = time.time()
    pending = 0
    for m, D in congrua_sets(bound):
        if m < start or len(D) < 2:
            continue
        st["totals"]["centers"] += 1
        ps = odd_primes(3 * m * m)
        stage3 = []
        for U in sorted(D):
            for V in sorted(D):
                if V == U:
                    continue
                st["totals"]["pairs"] += 1
                if U + V > m * m:
                    st["totals"]["pos"] += 1
                elif not coherent_pair(m, U, V, ps):
                    st["totals"]["coh"] += 1
                else:
                    stage3.append((U, V))
        for U, V in stage3:
            t1 = time.time()
            if pair_killed_by_representation(m, U, V):
                st["totals"]["rep"] += 1
                st["rep_killed_pairs"].append([m, U, V])
                verdict = "rep-killed"
            else:
                st["golden"].append([m, U, V])
                verdict = "*** GOLDEN CENTER ***"
            msg = (f"m={m} pair ({U},{V}): {verdict} "
                   f"[{time.time() - t1:.1f}s]")
            print(msg, flush=True)
            st["log"].append(msg)
        st["done_upto"] = m
        pending += 1
        if stage3 or pending >= CHUNK:
            save_state(st)
            pending = 0
    st["done_upto"] = bound
    save_state(st)
    t = st["totals"]
    print(f"DONE to {bound} in {time.time() - t0:.0f}s: "
          f"{t['centers']} centers, {t['pairs']} ordered pairs: "
          f"{t['pos']} positivity + {t['coh']} coherence + "
          f"{t['rep']} representation; GOLDEN: {len(st['golden'])}",
          flush=True)
    for g in st["golden"]:
        print(f"  golden: {g}", flush=True)


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 10000)
