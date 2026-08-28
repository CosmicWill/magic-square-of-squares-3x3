"""M12-E (ROADMAP W5): numeric groundwork for the abc bridge.

Two measured facts feeding the (*-abc) formulation of A2 §6:

1. REALIZED additive triples at GENERAL centers.  For a center value
   c = e^2 + f^2 (any c, not necessarily a square), the offsets
   D(c) = {2ef} make c -+ d squares of integers ((e-f)^2, (e+f)^2);
   the additive-triple pattern d1 + d2 = d3 inside D(c) is the exact
   near-square analogue of the MSS3 requirement, and it OCCURS at
   non-square centers (A3/A4).  For every realized triple we record
   the abc-quality of the (gcd-reduced) relation d1 + d2 = d3:
       q = log(c') / log(rad(a' b' c')).
   These are the "control group": what quality does nature pay where
   the pattern is realizable?

2. SQUAREFULL ENRICHMENT at square centers.  At c = m^2 every
   representation m^2 = e^2 + f^2 comes from a scaled primitive
   Pythagorean triple (g * primitive with hypotenuse m/g), so
   d = 2ef = g^2 * (primitive congruum core): elements of D(m^2)
   carry forced square factors g^2.  We measure the distribution of
   the squarefull part s(d) (the largest divisor all of whose prime
   valuations are >= 2) relative to d, for D at square vs non-square
   centers.  Systematic enrichment at square centers is precisely the
   lever an abc-type inequality on d1 + d2 = d3 would need.

Run:  python -m compute.abc_probe [CBOUND=200000] [MBOUND=2000]
"""

import sys
from math import gcd, isqrt, log


def rad_and_squarefull(n):
    """(radical, squarefull part) of n."""
    r = 1
    s = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            v = 0
            while n % d == 0:
                n //= d
                v += 1
            r *= d
            if v >= 2:
                s *= d ** v
        d += 1 if d == 2 else 2
    if n > 1:
        r *= n
    return r, s


def two_square_reps(bound):
    """reps[c] = list of 2ef over e^2 + f^2 = c, 0 < e < f, c <= bound."""
    reps = {}
    e = 1
    while 2 * e * e < bound:
        f = e + 1
        while (c := e * e + f * f) <= bound:
            reps.setdefault(c, []).append(2 * e * f)
            f += 1
        e += 1
    return reps


def realized_triples(cbound):
    """All additive triples d1 + d2 = d3 in D(c), c <= cbound, with
    the abc-quality of each reduced relation."""
    reps = two_square_reps(cbound)
    out = []
    for c, ds in reps.items():
        if len(ds) < 3:
            continue
        S = set(ds)
        dss = sorted(S)
        for i, d1 in enumerate(dss):
            for d2 in dss[:i]:
                if d1 + d2 in S:
                    g = gcd(d1, d2)
                    a, b, cc = d2 // g, d1 // g, (d1 + d2) // g
                    r, _ = rad_and_squarefull(a * b * cc // gcd(a * b, cc)
                                              * gcd(a * b, cc))
                    q = log(cc) / log(r) if r > 1 else float("inf")
                    sq = isqrt(c) ** 2 == c
                    out.append((c, d2, d1, q, sq))
    return out


def squarefull_stats(reps, centers):
    """Mean of log s(d)/log d over all d in D(c) for c in centers."""
    tot = n = 0.0
    for c in centers:
        for d in reps.get(c, []):
            _, s = rad_and_squarefull(d)
            if d > 1:
                tot += log(max(s, 1)) / log(d)
                n += 1
    return (tot / n if n else 0.0), int(n)


def main():
    cbound = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    mbound = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    trips = realized_triples(cbound)
    sq = [t for t in trips if t[4]]
    print(f"centers c <= {cbound}: realized additive triples: "
          f"{len(trips)}  (at square centers: {len(sq)})")
    if trips:
        qs = sorted(t[3] for t in trips)
        print(f"  abc-quality of realized triples: max {qs[-1]:.4f}, "
              f"median {qs[len(qs)//2]:.4f}, >1: "
              f"{sum(1 for q in qs if q > 1)}")
        top = sorted(trips, key=lambda t: -t[3])[:5]
        for c, d2, d1, q, s in top:
            print(f"    c={c} ({'SQUARE' if s else 'nonsquare'}): "
                  f"{d2} + {d1} = {d2+d1}   q = {q:.4f}")
    reps = two_square_reps(mbound * mbound)
    sq_centers = [m * m for m in range(2, mbound + 1) if m * m in reps]
    import random
    random.seed(1)
    nonsq = [c for c in reps if isqrt(c) ** 2 != c]
    nonsq = random.sample(nonsq, min(len(nonsq), 4000))
    es, ns_ = squarefull_stats(reps, sq_centers)
    en, nn = squarefull_stats(reps, nonsq)
    print(f"squarefull enrichment (mean log s(d)/log d): "
          f"SQUARE centers {es:.4f} (n={ns_}), "
          f"nonsquare centers {en:.4f} (n={nn}), "
          f"ratio {es/en if en else float('nan'):.2f}")


if __name__ == "__main__":
    main()
