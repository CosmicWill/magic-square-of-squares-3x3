"""Additive structure of congrua sets D(m), for all m up to a bound
(docs/attacks/A3-simultaneous-congrua.md).

D(m) = {2ef : e^2+f^2 = m^2, e,f > 0}.  An MSS3 with center m^2 requires
u, v, u+v, u-v all in D(m) ("additive quadruple").  Three of the four
("additive triple": d1, d2, d1+d2 in D(m)) would already give a magic
square with >= 7 square entries of a configuration type never seen (the
unique known 7-square example AB1 realizes only a pair).  This script
counts, exhaustively per m:

  L2(m): pairs {d1 != d2} in D(m)                    (>= 5-square configs)
  L3(m): triples d1, d2, d1+d2 in D(m)               (>= 7-square configs)
  L4(m): quadruples u, v, u+v, u-v in D(m)           (MSS3!)

Enumeration of D(m) by sieve over primitive triples: every e^2+f^2 = m^2
with e,f > 0 is g*(primitive triple with hypotenuse m/g), so
D(m) = { 2 g^2 ab : g*h = m, (a,b,h) primitive }.

Run:  python3 -m compute.congrua_search [BOUND]
"""

import sys
from math import gcd, isqrt


def primitive_leg_products(bound):
    """prim[h] = list of a*b over primitive triples (a,b,h), h <= bound."""
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


def congrua_sets(bound):
    """Yield (m, D(m)) for all 1 <= m <= bound with D(m) nonempty."""
    prim = primitive_leg_products(bound)
    hyps = sorted(prim)
    for m in range(1, bound + 1):
        D = set()
        for h in hyps:
            if h > m:
                break
            if m % h == 0:
                g = m // h
                gg2 = 2 * g * g
                for p in prim[h]:
                    D.add(gg2 * p)
        if D:
            yield m, D


def stats(bound, verbose=True):
    n_pairs = n_triples = n_quads = 0
    m_ge4 = 0
    triples_found = []
    quads_found = []
    for m, D in congrua_sets(bound):
        if len(D) >= 4:
            m_ge4 += 1
        if len(D) >= 2:
            n_pairs += 1
        Ds = D
        for d1 in Ds:
            for d2 in Ds:
                if d2 >= d1:
                    continue
                if d1 + d2 in Ds:
                    n_triples += 1
                    triples_found.append((m, d1, d2))
                    if d1 - d2 in Ds:
                        n_quads += 1
                        quads_found.append((m, d1, d2))
    if verbose:
        print(f"bound={bound}")
        print(f"  m with |D(m)| >= 2 : {n_pairs}")
        print(f"  m with |D(m)| >= 4 : {m_ge4}")
        print(f"  additive TRIPLES d1,d2,d1+d2 in D(m): {len(triples_found)}"
              f"  {triples_found[:5]}")
        print(f"  additive QUADRUPLES (= MSS3):        {len(quads_found)}"
              f"  {quads_found[:5]}")
    return triples_found, quads_found


if __name__ == "__main__":
    stats(int(sys.argv[1]) if len(sys.argv) > 1 else 100000)
