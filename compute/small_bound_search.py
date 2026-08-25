"""Independent direct-enumeration MSS3 search (docs/attacks/A6-search-bounds.md).

Deliberately does NOT share code with compute/congrua_search.py or
compute/eight_square_search.py: D(m) is computed by the naive e-loop over
decompositions of m^2 (as in verify/targets.py), and the additive
quadruple test is run directly.  Slower but independent — used to
cross-validate the faster sieves on overlapping ranges.

Run:  python3 -m compute.small_bound_search [BOUND]
"""

import sys
from math import isqrt


def congrua_direct(m):
    out = set()
    m2 = m * m
    e = 1
    while 2 * e * e < m2:
        f2 = m2 - e * e
        f = isqrt(f2)
        if f * f == f2:
            out.add(2 * e * f)
        e += 1
    return out


def search(bound, start=1):
    hits = []
    for m in range(start, bound + 1):
        D = congrua_direct(m)
        if len(D) < 4:
            continue
        Ds = sorted(D)
        for i, d1 in enumerate(Ds):
            for d2 in Ds[:i]:
                if d1 + d2 in D and d1 - d2 in D:
                    hits.append((m, d1, d2))
    return hits


if __name__ == "__main__":
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    hits = search(bound)
    print(f"no MSS3 with center root m <= {bound}" if not hits
          else f"FOUND: {hits}")
