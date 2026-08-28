"""A3 additive-desert extension (background job): no additive triple
d1, d2, d1+d2 in D(m) for any m up to BOUND (previously VERIFIED to
3x10^5 by compute.congrua_search / a6.small_bound).

Same mathematics as congrua_search.stats, engineered for 10^6: the
per-block multiples sieve replaces the per-m divisor scan, memory
stays bounded, and progress checkpoints to
compute/data_additive_desert.json per block.

Run:  python -m compute.additive_desert_ext [BOUND=1000000]
"""

import json
import os
import sys
import time
from math import gcd, isqrt

STATE = os.path.join(os.path.dirname(__file__),
                     "data_additive_desert.json")
BLOCK = 50_000


def primitive_leg_products(bound):
    prim = {}
    for m in range(2, isqrt(bound) + 1):
        for n in range(1 + (m % 2), m, 2):
            if gcd(m, n) != 1:
                continue
            h = m * m + n * n
            if h > bound:
                break
            prim.setdefault(h, []).append((m * m - n * n) * 2 * m * n)
    return prim


def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"done_upto": 0, "triples": [], "quads": [],
            "centers_ge2": 0, "pair_count": 0}


def save(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(st, fh)
    os.replace(tmp, STATE)


def run(bound):
    st = load()
    prim = primitive_leg_products(bound)
    hs = sorted(prim)
    print(f"additive desert: m in {st['done_upto'] + 1}..{bound}, "
          f"{len(hs)} primitive hypotenuses", flush=True)
    t0 = time.time()
    lo = st["done_upto"] + 1
    while lo <= bound:
        hi = min(lo + BLOCK - 1, bound)
        block = {}
        for h in hs:
            if h > hi:
                break
            first = max(h, ((lo + h - 1) // h) * h)
            for m in range(first, hi + 1, h):
                g = m // h
                gg2 = 2 * g * g
                bl = block.setdefault(m, set())
                for p in prim[h]:
                    bl.add(gg2 * p)
        for m in sorted(block):
            D = block[m]
            if len(D) < 2:
                continue
            st["centers_ge2"] += 1
            Ds = sorted(D)
            for i, d1 in enumerate(Ds):
                for d2 in Ds[:i]:
                    st["pair_count"] += 1
                    if d1 + d2 in D:
                        st["triples"].append([m, d1, d2])
                        print(f"*** ADDITIVE TRIPLE at m={m}: "
                              f"{d1}, {d2}", flush=True)
                        if d1 - d2 in D:
                            st["quads"].append([m, d1, d2])
                            print(f"*** ADDITIVE QUADRUPLE (MSS3 "
                                  f"CANDIDATE) at m={m} ***", flush=True)
        st["done_upto"] = hi
        save(st)
        print(f"  block done to m={hi} "
              f"[{time.time() - t0:.0f}s, centers>=2: "
              f"{st['centers_ge2']}, pairs: {st['pair_count']}, "
              f"triples: {len(st['triples'])}]", flush=True)
        lo = hi + 1
    print(f"DONE to {bound}: triples {len(st['triples'])}, "
          f"quads {len(st['quads'])}", flush=True)


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000)
