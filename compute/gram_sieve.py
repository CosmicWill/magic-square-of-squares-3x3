"""The Gram sieve (A9.7, ROADMAP W4): a provable pairwise necessity
condition for line representability — and the mechanism hunt for the
k_c >= 1 companion.

THEOREM A9.7 (pairwise Gram necessity; proof in A9 doc).  Let L be a
positive-definite rank-2 lattice with det L = N, and let w1, w2 be
norms of vectors x1, x2 in L.  Then t := <x1, x2> satisfies

    w1 w2 - t^2 = N k^2,   k = [L : Zx1 + Zx2] >= 1,

unless x1, x2 are proportional, in which case w1 w2 = t^2 is a
perfect square.  Hence: if a single class of determinant N represents
all three values of a co-norm triple, then EVERY pairwise product
w_i w_j is expressible as t^2 + N k^2 with k >= 1 (or is a perfect
square).  At the top stratum N = 3 m^2 this reads: w_i w_j is
represented by the PRINCIPAL form x^2 + 3 m^2 y^2 with y >= 1 —
a condition beyond all genus characters, whose local solvability at
odd p | 3m^2 is exactly the chi_p-coherence of Theorem A9.3.

This module implements the per-stratum Gram test (a line is
gram-killed iff at every admissible stratum some pairwise product
fails) and runs the mechanism census:

  * soundness: no representable (alive) line may be gram-killed
    (A9.7 is a theorem — violations would be bugs);
  * explanatory power: how many of the killed lines are gram-killed
    (Gram explains them), overall and for the 36 beyond-genus GLOBAL
    kills of the M12-B anatomy;
  * the companion: per-pair kill patterns (which line indices die),
    and whether lines 2/3's deaths coincide with Gram failures.

Run:  python -m compute.gram_sieve [--corpus N]
"""

import json
import os
import sys
from math import gcd, isqrt

from compute.sphere_composition import PASSERS_1200, killed_lines, strata
from compute.sphere_gluing import pair_lines, represents
from compute.sphere_classes import reduce_form

STATE = os.path.join(os.path.dirname(__file__), "data_desert_30k.json")


def gram_pair_ok(w1, w2, N):
    """Is w1 w2 = t^2 + N k^2 solvable with k >= 1 (or w1 w2 a
    perfect square — the proportional escape)?"""
    P = w1 * w2
    r = isqrt(P)
    if r * r == P:
        return True
    k = 1
    while N * k * k <= P:
        d = P - N * k * k
        t = isqrt(d)
        if t * t == d:
            return True
        k += 1
    return False


def gram_line_ok(tri, n):
    """Does SOME admissible stratum pass all three pairwise Gram
    conditions?  (Necessity: alive => gram_line_ok.)  Strata mirror
    sphere_composition.strata: det of the halved even lattice at
    content g and form-content ct is n/g^2 / (2 ... ) — we work with
    the UNHALVED even lattice: det N = n/g^2, values tri/g^2, and
    fold ct into the vectors (a vector divisible by ct scales its
    norm by ct^2, leaving the Gram identity intact), so the test at
    content g covers all ct."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            N = n // (g * g)
            th = [t // (g * g) for t in tri]
            if (gram_pair_ok(th[0], th[1], N) and
                    gram_pair_ok(th[0], th[2], N) and
                    gram_pair_ok(th[1], th[2], N)):
                return True
        d += 2
    return False


def line_alive(tri, n):
    """The representation sieve's verdict (early-exit copy)."""
    from compute.sphere_composition import prims
    for g, ct, D, th in strata(tri, n):
        pf = prims(D)
        if pf and any(all(represents(f, t) for t in th) for f in pf):
            return True
    return False


def pair_census(m, U, V):
    """Per-line: (alive?, gram_ok?) for all 8 lines."""
    n = 3 * m * m
    out = []
    for tri in pair_lines(2 * m * m, U, V):
        a = line_alive(tri, n)
        gk = gram_line_ok(tri, n)
        out.append((a, gk))
    return out


def main():
    ncorp = 40
    for a in sys.argv[1:]:
        if a.startswith("--corpus"):
            ncorp = int(a.split("=", 1)[1]) if "=" in a else ncorp
    # 1) the 11 passers (includes the 36 GLOBAL kill-lines)
    print("== passers <= 1200 (the M12-B anatomy set) ==")
    viol = 0
    tot_killed = tot_gram = 0
    for m, U, V in PASSERS_1200:
        n = 3 * m * m
        cen = pair_census(m, U, V)
        killed_idx = [i for i, (a, _) in enumerate(cen) if not a]
        gram_idx = [i for i, (_, gk) in enumerate(cen) if not gk]
        for i, (a, gk) in enumerate(cen):
            if a and not gk:
                viol += 1
                print(f"  *** A9.7 VIOLATION (bug!): m={m} line {i}")
        tot_killed += len(killed_idx)
        tot_gram += len([i for i in killed_idx if i in gram_idx])
        print(f"m={m} ({U},{V}): killed {killed_idx}  gram-killed "
              f"{gram_idx}")
    print(f"soundness violations: {viol}; killed lines: {tot_killed}, "
          f"of which gram-explained: {tot_gram}")
    # 2) corpus sample: kill patterns and the companion
    with open(STATE, encoding="utf-8") as fh:
        corpus = json.load(fh)["rep_killed_pairs"]
    corpus = [r for r in corpus if r[0] <= 4000]
    stride = max(1, len(corpus) // ncorp)
    sample = corpus[::stride][:ncorp]
    print(f"== corpus sample ({len(sample)} pairs, m <= 4000) ==")
    patt = {}
    comp_ok = gram_expl = 0
    for m, U, V in sample:
        cen = pair_census(m, U, V)
        killed_idx = tuple(i for i, (a, _) in enumerate(cen) if not a)
        gram_idx = tuple(i for i, (_, g2) in enumerate(cen) if not g2)
        patt[killed_idx] = patt.get(killed_idx, 0) + 1
        if 2 in killed_idx or 3 in killed_idx:
            comp_ok += 1
        if any(i in gram_idx for i in killed_idx if i in (2, 3)):
            gram_expl += 1
        for i, (a, g2) in enumerate(cen):
            if a and not g2:
                print(f"  *** A9.7 VIOLATION: m={m} line {i}")
    print(f"kill patterns: {patt}")
    print(f"companion (2 or 3 killed): {comp_ok}/{len(sample)}; "
          f"phantom kill gram-explained: {gram_expl}/{len(sample)}")


if __name__ == "__main__":
    main()
