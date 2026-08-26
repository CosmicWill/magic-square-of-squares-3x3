"""Singleton-pattern exclusion (M11-G): every complete genus-0 curve
on X meets nodes over at least TWO distinct triple points.

By the pattern dichotomy (Theorem A8.13), a complete genus-0 curve C
whose nodes all sit over ONE triple point P has Lucas image a common
integral curve of the 4-dimensional extension subspace V_P =
V_{tau >= 4}(P) — and the image, being the image of a curve meeting
no other node, must also avoid the other seven triple points (their
pi-fibres consist of nodes).  This module certifies, for EACH of the
eight triple points, that the special locus of the subsystem V_P has
curve part contained in the nine entry lines, by the exact machinery
of Theorem A8.7': for a pair of basis-pair resultants
R = Res(F_i, F_j) in Z[c, v] (provably exact CRT; independently
spot-verified), peel the entry lines exactly and witness the two
peeled cofactors COPRIME over Q.  Then

    curve part of Z(V_P)  <=  V(gcd(R_1, R_2))  =  the entry lines,

and since genus-0 curves have no entry-line images (Theorem A7.3:
the only genus-0 line images are u = 0 and v = 0, whose components
visit three triple points each), singleton patterns are impossible:

    THEOREM A8.14.  Every complete curve of geometric genus 0 on X
    meets nodes over >= 2 distinct triple points of the arrangement;
    in particular it passes through >= 2 distinct nodes.

(The bases of the three B-point subspaces come from the transpose
transfer V(B) = {x : M_sigma^T x in V(A)} — Lemma A8.9's tau is
preserved by the linear automorphism sigma, which maps the
(B, pencil) configuration to the (A, pencil) configuration and the
invariant 6-space to itself.  The certificates below run directly on
those bases, so they need only that the transfer produces a spanning
set, which the exact in-span solve of M_sigma establishes.)

Run:  python3 -m compute.pattern_loci
"""

from fractions import Fraction as F
from functools import reduce
from itertools import combinations
from math import gcd

from compute.node_extension import ALL_TAGS, extension_spaces
from compute.special_locus import numerator_forms
from compute.z_exact import (content, coprime_witness, crt_resultant,
                             peel_lines, spot_check)

M = 4
SPOTS = ((3, 5), (-7, 2), (11, -4))


def combo_int(vec, forms=None):
    """Integer, content-free numerators of sum_a vec[a] eta_a."""
    forms = forms or numerator_forms()
    out = [dict() for _ in range(M + 1)]
    for a, Ns in enumerate(forms):
        if vec[a] == 0:
            continue
        for k in range(M + 1):
            for ij, v in Ns[k].items():
                out[k][ij] = out[k].get(ij, F(0)) + vec[a] * v
    out = [{ij: v for ij, v in c.items() if v} for c in out]
    dens = [v.denominator for c in out for v in c.values()]
    L = reduce(lambda a, b: a * b // gcd(a, b), dens, 1)
    ints = [{ij: int(v * L) for ij, v in c.items()} for c in out]
    g = reduce(gcd, (abs(x) for c in ints for x in c.values()), 0)
    return [{ij: x // g for ij, x in c.items()} for c in ints]


def _peeled_resultant(fa, fb):
    R, n_primes = crt_resultant(fa, fb)
    assert R, "identically zero pair resultant"
    spot_check(R, fa, fb, list(SPOTS))
    c = content(R)
    R = {ij: v // c for ij, v in R.items()}
    exps, cof = peel_lines(R)
    return n_primes, exps, cof


def singleton_certificate(tag, spaces=None, witness_prime=999999937):
    """The exact certificate that Z(V_P) has curve part inside the
    nine entry lines, for the triple point `tag`: two basis-pair
    resultants whose peeled cofactors are coprime over Q.  Tries
    basis pairs in a fixed order until a coprime cofactor pair is
    witnessed.  Returns a summary dict (raises if none found)."""
    spaces = spaces or extension_spaces()
    forms = numerator_forms()
    basis = [combo_int(b, forms) for b in spaces[tag]]
    assert len(basis) == 4, f"V({tag}) is not 4-dimensional?"
    done = {}
    order = list(combinations(range(4), 2))
    for pair in order:
        done[pair] = _peeled_resultant(basis[pair[0]], basis[pair[1]])
        for p1, p2 in combinations(done, 2):
            (_, e1, cof1), (_, e2, cof2) = done[p1], done[p2]
            try:
                w = coprime_witness(cof1, cof2, witness_prime)
            except AssertionError:
                continue
            assert all(v >= 8 for v in e1.values())
            assert all(v >= 8 for v in e2.values())
            return {
                "tag": tag, "pairs": (p1, p2),
                "line_exps": ({str(k): v for k, v in e1.items()},
                              {str(k): v for k, v in e2.items()}),
                "cof_degs": (max((i + j for (i, j) in cof1), default=0),
                             max((i + j for (i, j) in cof2), default=0)),
                "witness": w,
                "n_resultants_computed": len(done),
            }
    raise AssertionError(
        f"no coprime cofactor pair at {tag}: shared curve factors — "
        "the singleton exclusion needs the deeper component analysis")


def all_singletons(tags=ALL_TAGS):
    """Certificates for every requested triple point; the full run
    over all eight proves Theorem A8.14."""
    spaces = extension_spaces()
    return {tag: singleton_certificate(tag, spaces) for tag in tags}


def main():
    certs = all_singletons()
    for tag, c in certs.items():
        print(f"{tag}: pairs {c['pairs']}, cofactor degs "
              f"{c['cof_degs']}, witness Res_v != 0 at "
              f"c0 = {c['witness']['c0']} mod {c['witness']['prime']} "
              f"({c['n_resultants_computed']} resultants computed)")
    print("ALL EIGHT SINGLETON PATTERNS EXCLUDED:")
    print("  Theorem A8.14 — every complete genus-0 curve on X meets")
    print("  nodes over >= 2 distinct triple points (>= 2 nodes).")


if __name__ == "__main__":
    main()
