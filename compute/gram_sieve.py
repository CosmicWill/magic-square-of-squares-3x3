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


# --------------------------------------------------------------- A9.8 layer

def gram_pair_k1(w1, w2, N):
    """Index-one sufficiency (Theorem A9.8): exists t with
    w1 w2 - t^2 = N exactly?  If so, the even form (w1, 2t, w2) has
    disc -4N and represents both values: the pair IS representable
    by a single class."""
    d = w1 * w2 - N
    if d < 0:
        return False
    t = isqrt(d)
    return t * t == d


def exact_pair_alive(w1, w2, n):
    """The exact pairwise layer: does some even class at some
    admissible stratum represent BOTH values?  (Strata as in
    gram_line_ok / line_classes.)"""
    from compute.sphere_gluing import even_forms
    G = gcd(w1, w2)
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            t1, t2 = w1 // (g * g), w2 // (g * g)
            for f in even_forms(-4 * (n // (g * g))):
                if represents(f, t1) and represents(f, t2):
                    return True
        d += 2
    return False


def line_k1_ok(tri, n):
    """Some stratum where all three pairs pass at index one."""
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
            if (gram_pair_k1(th[0], th[1], N) and
                    gram_pair_k1(th[0], th[2], N) and
                    gram_pair_k1(th[1], th[2], N)):
                return True
        d += 2
    return False


def sandwich_census():
    """Three-layer pair census over the 11 passers: for every one of
    the 8 lines x 3 pairs, classify (k1, exact, gram) and verify the
    sandwich k1 => exact => gram; locate A9.C2 at each layer."""
    from itertools import combinations
    tot = {"k1": 0, "exact": 0, "gram": 0, "pairs": 0}
    sandwich_viol = 0
    c2_gram = c2_exact = pairs_n = 0
    for m, U, V in PASSERS_1200:
        n = 3 * m * m
        lines = pair_lines(2 * m * m, U, V)
        line_exact_fail = []
        for i, tri in enumerate(lines):
            fail = False
            for w1, w2 in combinations(tri, 2):
                tot["pairs"] += 1
                # per-pair layers, stratum-aware via the line helpers
                # (pair-level strata: reuse exact_pair_alive/gram on
                # the pair's own gcd strata)
                k1 = False
                G = gcd(w1, w2)
                base, nn = 1, n
                while nn % 4 == 0:
                    nn //= 4
                    base *= 2
                dd = 1
                while (base * dd) ** 2 <= n:
                    g = base * dd
                    if n % (g * g) == 0 and G % (g * g) == 0:
                        if gram_pair_k1(w1 // (g * g), w2 // (g * g),
                                        n // (g * g)):
                            k1 = True
                            break
                    dd += 2
                ex = exact_pair_alive(w1, w2, n)
                gr = gram_pair_ok_strata(w1, w2, n)
                tot["k1"] += k1
                tot["exact"] += ex
                tot["gram"] += gr
                if (k1 and not ex) or (ex and not gr):
                    sandwich_viol += 1
                    print(f"  *** SANDWICH VIOLATION m={m} line {i} "
                          f"({w1},{w2}): k1={k1} exact={ex} gram={gr}")
                if not ex:
                    fail = True
            if fail:
                line_exact_fail.append(i)
        pairs_n += 1
        if line_exact_fail:
            if 2 in line_exact_fail or 3 in line_exact_fail:
                c2_exact += 1
        print(f"m={m} ({U},{V}): exact-pairwise-failing lines "
              f"{line_exact_fail}")
    print(f"pairs {tot['pairs']}: k1-pass {tot['k1']}, exact-pass "
          f"{tot['exact']}, gram-pass {tot['gram']}; sandwich "
          f"violations {sandwich_viol}")
    print(f"C2 at exact-pairwise layer: phantom failure present in "
          f"{c2_exact} of the pairs with any failure")


def gram_pair_ok_strata(w1, w2, n):
    G = gcd(w1, w2)
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            if gram_pair_ok(w1 // (g * g), w2 // (g * g),
                            n // (g * g)):
                return True
        d += 2
    return False


# ------------------------------------------------------------ A9.9 syzygy

def pair_witnesses(w1, w2, N):
    """All (t, k) with t >= 0, k >= 0, w1 w2 - t^2 = N k^2 (k = 0
    allowed only when w1 w2 is a perfect square)."""
    out = []
    P = w1 * w2
    r = isqrt(P)
    if r * r == P:
        out.append((r, 0))
    k = 1
    while N * k * k <= P:
        d = P - N * k * k
        t = isqrt(d)
        if t * t == d:
            out.append((t, k))
        k += 1
    return out


def syzygy_line_ok(tri, n):
    """The full Diophantine line test: at some admissible stratum,
    exist integers t12, t13, t23 (with signs) satisfying all three
    pair equations AND the rank-2 syzygy
    det3 = w1 w2 w3 + 2 t12 t13 t23 - w1 t23^2 - w2 t13^2 - w3 t12^2 = 0.
    (Necessity: Theorem A9.9 — three vectors in a rank-2 lattice are
    dependent.)"""
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
            w1, w2, w3 = [t // (g * g) for t in tri]
            W12 = pair_witnesses(w1, w2, N)
            W13 = pair_witnesses(w1, w3, N)
            W23 = pair_witnesses(w2, w3, N)
            for t12, _ in W12:
                for t13, _ in W13:
                    for t23, _ in W23:
                        base3 = (w1 * w2 * w3 - w1 * t23 * t23
                                 - w2 * t13 * t13 - w3 * t12 * t12)
                        # sign freedom: negating vectors flips two t's;
                        # the product t12 t13 t23 changes sign freely
                        if base3 == 2 * t12 * t13 * t23 or \
                           base3 == -2 * t12 * t13 * t23:
                            return True
        d += 2
    return False


def syzygy_census():
    """Does pairwise-Gram + syzygy explain ALL 57 kills (including
    the pairwise exception at m=725 pair 2 line 5)?  And soundness:
    every alive line must pass the syzygy test."""
    viol = killed = explained = 0
    for m, U, V in PASSERS_1200:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            alive = line_alive(tri, n)
            sy = syzygy_line_ok(tri, n)
            if alive and not sy:
                viol += 1
                print(f"*** A9.9 SOUNDNESS VIOLATION m={m} line {i}")
            if not alive:
                killed += 1
                if not sy:
                    explained += 1
                else:
                    print(f"  beyond-syzygy kill: m={m} ({U},{V}) "
                          f"line {i}")
    print(f"soundness violations: {viol}; kills {killed}, "
          f"syzygy-explained {explained}")


# ----------------------------------------------------------- A9.10 q-layer

def _cross(r1, r2):
    return (r1[1]*r2[2] - r1[2]*r2[1],
            r1[2]*r2[0] - r1[0]*r2[2],
            r1[0]*r2[1] - r1[1]*r2[0])


def witness_q(w, T, N):
    """For a syzygy witness (w = (w1,w2,w3), T = (T12,T13,T23) with
    det3 = 0): the primitive kernel vector v of the Gram G and the
    index ratio q with det M = N q^2 (M = the lattice the witness
    generates).  Returns q as a Fraction, or None if degenerate."""
    from fractions import Fraction
    w1, w2, w3 = w
    T12, T13, T23 = T
    G = ((w1, T12, T13), (T12, w2, T23), (T13, T23, w3))
    for i, j in ((0, 1), (0, 2), (1, 2)):
        v = _cross(G[i], G[j])
        if any(v):
            break
    else:
        return None
    g = gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2]))
    v = tuple(x // g for x in v)
    # det(M12) = w1 w2 - T12^2 = N k12^2 ; [M : M12] = |v3| etc.
    if v[2] == 0:
        return None
    k12s = w1 * w2 - T12 * T12
    q2 = Fraction(k12s, N * v[2] * v[2])
    return q2  # = q^2


def syzygy_q1_line_ok(tri, n):
    """The refined (q = 1) Diophantine test: a witness whose
    generated lattice has det exactly N — by Theorem A9.10 such a
    witness PROVES representability (sufficiency direction)."""
    G0 = gcd(gcd(tri[0], tri[1]), tri[2])
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G0 % (g * g) == 0:
            N = n // (g * g)
            w = tuple(t // (g * g) for t in tri)
            W12 = pair_witnesses(w[0], w[1], N)
            W13 = pair_witnesses(w[0], w[2], N)
            W23 = pair_witnesses(w[1], w[2], N)
            for t12, _ in W12:
                for t13, _ in W13:
                    for t23, _ in W23:
                        b3 = (w[0]*w[1]*w[2] - w[0]*t23*t23
                              - w[1]*t13*t13 - w[2]*t12*t12)
                        for s in (1, -1):
                            # det3 = b3 + 2*T12*T13*T23 = 0 with
                            # T = (s*t12, t13, t23) requires
                            # b3 == -s * 2 t12 t13 t23
                            if b3 != -s * 2 * t12 * t13 * t23:
                                continue
                            q2 = witness_q(w, (s*t12, t13, t23), N)
                            if q2 == 1:
                                return True
        d += 2
    return False


def q_census():
    """Do alive lines always admit a q = 1 witness (so that A9.10
    proves their representability constructively)?  And does the
    q = 1 restriction keep explaining all kills?"""
    alive_no_q1 = kills = expl = 0
    for m, U, V in PASSERS_1200:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            alive = line_alive(tri, n)
            q1 = syzygy_q1_line_ok(tri, n)
            if alive and not q1:
                alive_no_q1 += 1
                print(f"  alive WITHOUT q=1 witness: m={m} line {i}")
            if not alive:
                kills += 1
                expl += not q1
    print(f"alive-without-q1: {alive_no_q1}; kills {kills}, "
          f"q1-test-explained {expl}")


# ------------------------------------------------------- A9.11 overlattice

def line_witness_qs(tri, n):
    """All (stratum g, q^2) over the line's syzygy witnesses."""
    from fractions import Fraction
    G0 = gcd(gcd(tri[0], tri[1]), tri[2])
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    out = set()
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G0 % (g * g) == 0:
            N = n // (g * g)
            w = tuple(t // (g * g) for t in tri)
            for t12, _ in pair_witnesses(w[0], w[1], N):
                for t13, _ in pair_witnesses(w[0], w[2], N):
                    for t23, _ in pair_witnesses(w[1], w[2], N):
                        b3 = (w[0]*w[1]*w[2] - w[0]*t23*t23
                              - w[1]*t13*t13 - w[2]*t12*t12)
                        for s in (1, -1):
                            if b3 != -s * 2 * t12 * t13 * t23:
                                continue
                            q2 = witness_q(w, (s*t12, t13, t23), N)
                            if q2 is not None:
                                out.add((g, q2))
        d += 2
    return out


def line_certified(tri, n):
    """Is the line certified representable by A9.10 (q = 1) or A9.11
    (some witness with integer q, gcd(q, 2N) = 1)?"""
    from math import isqrt as _is
    for g, q2 in line_witness_qs(tri, n):
        if q2 == 1:
            return "A9.10"
        if q2.denominator == 1:
            r = _is(q2.numerator)
            if r * r == q2.numerator:
                N = n // (g * g)
                if gcd(r, 2 * N) == 1:
                    return "A9.11"
    return None


def certification_census(sample_corpus=25):
    """Every alive line of the anatomy set (and a corpus sample) must
    be certified by A9.10 or A9.11; killed lines never are."""
    stats = {"A9.10": 0, "A9.11": 0, None: 0}
    bad = 0
    for m, U, V in PASSERS_1200:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            alive = line_alive(tri, n)
            cert = line_certified(tri, n)
            if alive:
                stats[cert] += 1
                if cert is None:
                    bad += 1
                    print(f"  ALIVE UNCERTIFIED: m={m} line {i}")
            else:
                if cert is not None:
                    bad += 1
                    print(f"  KILLED-BUT-CERTIFIED (C4 necessity "
                          f"violated?!): m={m} line {i}")
    print(f"anatomy alive lines: {stats}  (violations: {bad})")
    import json as _json
    with open(STATE, encoding="utf-8") as fh:
        corpus = _json.load(fh)["rep_killed_pairs"]
    corpus = [r for r in corpus if r[0] <= 2500]
    stride = max(1, len(corpus) // sample_corpus)
    cstats = {"A9.10": 0, "A9.11": 0, None: 0}
    cbad = 0
    for m, U, V in corpus[::stride][:sample_corpus]:
        n = 3 * m * m
        for tri in pair_lines(2 * m * m, U, V):
            alive = line_alive(tri, n)
            cert = line_certified(tri, n)
            if alive:
                cstats[cert] += 1
                cbad += cert is None
            elif cert is not None:
                cbad += 1
    print(f"corpus-sample alive lines: {cstats}  (violations: {cbad})")


# --------------------------------------------------- C2 census machinery

_SQ_MODS = (64, 63, 65, 11)
_SQ_SETS = tuple(frozenset((i * i) % M for i in range(M))
                 for M in _SQ_MODS)


def gram_pair_ok_fast(w1, w2, N):
    """Filtered version of gram_pair_ok (same verdict, ~10x faster):
    congruence filters mod 64/63/65/11 before each isqrt."""
    P = w1 * w2
    r = isqrt(P)
    if r * r == P:
        return True
    Pm = [P % M for M in _SQ_MODS]
    Nm = [N % M for M in _SQ_MODS]
    k = 1
    while N * k * k <= P:
        ok = True
        for idx, M in enumerate(_SQ_MODS):
            if (Pm[idx] - Nm[idx] * k * k) % M not in _SQ_SETS[idx]:
                ok = False
                break
        if ok:
            d = P - N * k * k
            t = isqrt(d)
            if t * t == d:
                return True
        k += 1
    return False


def gram_pair_ok_strata_fast(w1, w2, n):
    G = gcd(w1, w2)
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            if gram_pair_ok_fast(w1 // (g * g), w2 // (g * g),
                                 n // (g * g)):
                return True
        d += 2
    return False


PRODUCT_NAMES = None


def named_products(m, U, V):
    """The 24 named pairwise products of the pair's ten co-norm
    values, keyed by role."""
    n2 = 2 * m * m
    up, um, vp, vm = n2 + U, n2 - U, n2 + V, n2 - V
    Ap, Am = n2 + U + V, n2 - U - V
    Bp, Bm = n2 + U - V, n2 - U + V
    return {
        "free:n2,u+": (n2, up), "free:n2,u-": (n2, um),
        "free:u+,u-": (up, um), "free:n2,v+": (n2, vp),
        "free:n2,v-": (n2, vm), "free:v+,v-": (vp, vm),
        "phA:n2,A+": (n2, Ap), "phA:n2,A-": (n2, Am),
        "phA:A+,A-": (Ap, Am), "phB:n2,B+": (n2, Bp),
        "phB:n2,B-": (n2, Bm), "phB:B+,B-": (Bp, Bm),
        "xr:u+,v+": (up, vp), "xr:u-,v-": (um, vm),
        "xr:u+,v-": (up, vm), "xr:u-,v+": (um, vp),
        "rpA:u+,A-": (up, Am), "rpA:v+,A-": (vp, Am),
        "rpA:u-,A+": (um, Ap), "rpA:v-,A+": (vm, Ap),
        "rpB:u+,B-": (up, Bm), "rpB:v-,B-": (vm, Bm),
        "rpB:v+,B+": (vp, Bp), "rpB:u-,B+": (um, Bp)}


def c2_census(sample_size=400, mmax=None, verbose=True):
    """Corpus-scale product-failure census: per pair the 24-product
    verdict vector; tests of candidate transfer laws.  Uses the
    fast Gram test (A9.C3-lossless empirically; the law A9.12 makes
    the pair layer the object of study)."""
    import json as _json
    with open(STATE, encoding="utf-8") as fh:
        corpus = _json.load(fh)["rep_killed_pairs"]
    if mmax:
        corpus = [r for r in corpus if r[0] <= mmax]
    stride = max(1, len(corpus) // sample_size)
    sample = corpus[::stride][:sample_size]
    laws = {
        "free-never-fails": 0,
        "anyfail=>phantom": 0,       # some ph* product fails
        "rpA=>phA": 0,               # rpA failure => some phA failure
        "rpB=>phB": 0,
        "xr=>ph": 0,
        "anyfail": 0,
    }
    viol = {k: [] for k in laws}
    for m, U, V in sample:
        n = 3 * m * m
        f = {name: not gram_pair_ok_strata_fast(w1, w2, n)
             for name, (w1, w2) in named_products(m, U, V).items()}
        freefail = any(v for k, v in f.items() if k.startswith("free"))
        if freefail:
            viol["free-never-fails"].append((m, U, V))
        else:
            laws["free-never-fails"] += 1
        anyf = any(f.values())
        phA = any(v for k, v in f.items() if k.startswith("phA"))
        phB = any(v for k, v in f.items() if k.startswith("phB"))
        rpA = any(v for k, v in f.items() if k.startswith("rpA"))
        rpB = any(v for k, v in f.items() if k.startswith("rpB"))
        xr = any(v for k, v in f.items() if k.startswith("xr"))
        if anyf:
            laws["anyfail"] += 1
            if phA or phB:
                laws["anyfail=>phantom"] += 1
            else:
                viol["anyfail=>phantom"].append((m, U, V))
        if rpA:
            if phA:
                laws["rpA=>phA"] += 1
            else:
                viol["rpA=>phA"].append((m, U, V))
        if rpB:
            if phB:
                laws["rpB=>phB"] += 1
            else:
                viol["rpB=>phB"].append((m, U, V))
        if xr:
            if phA or phB:
                laws["xr=>ph"] += 1
            else:
                viol["xr=>ph"].append((m, U, V))
    if verbose:
        print(f"sample {len(sample)} pairs: {laws}")
        for k, v in viol.items():
            if v:
                print(f"  VIOLATIONS {k}: {v[:6]}"
                      f"{' ...' if len(v) > 6 else ''} "
                      f"({len(v)} total)")
    return laws, viol
