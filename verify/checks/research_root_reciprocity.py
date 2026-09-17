"""Exact controls for the root-function reciprocity evaluator (RR.1--RR.4); no point exclusion."""

from fractions import Fraction as Q
from itertools import product
from math import gcd

from ..framework import check, require
from compute import root_reciprocity as rr

DOC = "docs/research/root-functions-and-reciprocity.md"


@check("rr.circle_cross_grids", DOC)
def circle_cross_grids(ctx):
    """RR.1: circle points give grids with square cross entries; the five-root control; the parametrization covers the circle."""
    bound = ctx.bound(full=40, fast=12)
    seen = set()
    for den in range(1, bound + 1):
        for num in range(-bound, bound + 1):
            if gcd(abs(num), den) != 1:
                continue
            t = Q(num, den)
            x, y = rr.circle_pair(t)
            require(x * x + y * y == 2)
            u = rr.circle_offset(t)
            require(1 + u == x * x and 1 - u == y * y)
            seen.add((x, y))
    x, y = rr.circle_pair(None)
    require((x, y) == (-1, -1) and x * x + y * y == 2)
    require(len(seen) == sum(1 for den in range(1, bound + 1) for num in range(-bound, bound + 1) if gcd(abs(num), den) == 1))
    for t1, t2 in ((Q(1, 5), Q(1, 15)), (Q(2, 3), Q(1, 7))):
        rep = rr.candidate_report(rr.circle_offset(t1), rr.circle_offset(t2))
        roots = rep["rational_roots"]
        require(all(roots[i] is not None for i in (0, 2, 4, 6, 8)), "the five cross roots are rational")
        require(rep["missing_root_indices"] == [1, 3, 5, 7] or rep["rational_root_count"] >= 5)
    rep = rr.candidate_report(rr.circle_offset(Q(1, 5)), rr.circle_offset(Q(1, 15)))
    require(rep["u"] == "120/169" and rep["v"] == "3360/12769" and rep["rational_root_count"] == 5 and rep["positive"] and rep["distinct"])
    require(rep["rational_roots"] == ["17/13", None, "127/113", None, "1", None, "97/113", None, "7/13"])
    values = rr.entries(Q(1), Q(120, 169), Q(3360, 12769))
    require(all(sum(values[i] for i in line) == 3 for line in rr.LINES), "the five-root control is magic")
    ctx.note(f"{len(seen)} circle points with square cross entries; the classical five-square control replayed")


@check("rr.hilbert_symbol_identities", DOC)
def hilbert_symbol_identities(ctx):
    """RR.3: the exact Hilbert symbol satisfies symmetry, bilinearity, (a,-a) = (a,1-a) = 1, the product formula, and the tables."""
    bound = ctx.bound(full=30, fast=12)
    places = [0, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    rationals = sorted({Q(n, d) for n in range(-bound, bound + 1) for d in range(1, bound + 1) if n} , key=lambda q: (abs(q), q))
    rationals = rationals[: ctx.bound(full=140, fast=60)]
    checked = 0
    for a, b in product(rationals, repeat=2):
        for p in places:
            s = rr.hilbert(a, b, p)
            require(s in (1, -1) and rr.hilbert(b, a, p) == s, (a, b, p, "symmetry"))
            require(rr.hilbert(a * a, b, p) == 1, (a, b, p, "squares split"))
        require(rr.hilbert(a, -a, 2) == 1 and rr.hilbert(a, -a, 3) == 1 and rr.hilbert(a, -a, 0) == 1, (a, "(a,-a)"))
        if a != 1:
            require(rr.hilbert(a, 1 - a, 2) == 1 and rr.hilbert(a, 1 - a, 5) == 1, (a, "(a,1-a)"))
        checked += 1
    for a, b, c in product(rationals[:20], repeat=3):
        for p in (0, 2, 3, 7):
            require(rr.hilbert(a * b, c, p) == rr.hilbert(a, c, p) * rr.hilbert(b, c, p), (a, b, c, p, "bilinearity"))
    # the product formula on every pair of small rationals: an even number of -1 among all places
    for a, b in product(rationals[:40], repeat=2):
        prof = rr.symbol_profile(a, b)
        require(prof["reciprocity_product"] == 1, (a, b, "reciprocity"))
    # tabulated values: (-1,-1) is -1 at 2 and infinity only; (2,3)_3 = -1 (2 is not a square mod 3); (5,7)_5 = (7/5) = -1
    require(rr.hilbert(-1, -1, 2) == -1 and rr.hilbert(-1, -1, 0) == -1 and rr.hilbert(-1, -1, 3) == 1)
    require(rr.hilbert(2, 3, 3) == -1 and rr.hilbert(2, 3, 2) == -1 and rr.hilbert(5, 7, 5) == -1 and rr.hilbert(5, 7, 7) == -1)
    require(rr.symbol_profile(Q(3), Q(5))["symbols"] == {"infinity": 1, "2": 1, "3": -1, "5": -1})
    require(rr.symbol_profile(Q(113, 114), Q(17, 114))["nonzero_invariant_places"] == ["3", "113"])
    ctx.note(f"{checked} rational pairs at 16 places; bilinearity, squares, (a,-a), (a,1-a), the product formula and the tables agree")


@check("rr.local_controls", DOC)
def local_controls(ctx):
    """RR.4: the full Q_113 point with symbol -1 and the fourth-power controls with symbol +1; the precision guards."""
    precision = ctx.bound(full=12, fast=8)
    n = rr.nontrivial_control(precision)
    require(n["p"] == 113 and n["hilbert_symbol"] == -1, "the 113-adic control has invariant 1/2")
    values = n["entries"]
    require(all(v > 0 for v in values) and len(set(values)) == 9, "positive distinct entries")
    require(all(sum(values[i] for i in line) == 3 * values[4] for line in rr.LINES), "magic")
    require(values[0] == 113 ** 2 and values[2] == 17 ** 2 and values[4] == 114 ** 2, "three exact roots")
    modulus = 113 ** precision
    roots = n["roots_mod_prime_power"]
    require(all((r * r - v) % modulus == 0 for r, v in zip(roots, values)), "the residues are square roots modulo 113^precision")
    require(roots[0] == 113 and roots[2] == 17 and roots[4] == 114 and all(roots[i] % 113 for i in (1, 3, 5, 6, 7, 8)), "the slot roots and six unit roots")
    require(rr.local_root_symbol(roots, 113, precision) == -1)
    # the symbol is stable under raising the precision and under changing the six lifted roots' signs
    for i in (1, 3, 5, 6, 7, 8):
        alt = list(roots)
        alt[i] = (-alt[i]) % modulus
        require(rr.local_root_symbol(alt, 113, precision) == -1, (i, "sign of a non-slot root is irrelevant"))
    for p in (2, 3, 113):
        f = rr.fourth_power_control(p, precision if p != 2 else max(precision, 8))
        require(f["hilbert_symbol"] == 1, (p, "square slots split"))
        m = p ** f["precision"]
        require(all((x ** 4 - v) % m == 0 for x, v in zip(f["fourth_roots"], f["entries"])), (p, "fourth roots"))
        require(all(sum(f["entries"][i] for i in line) == 3 * f["entries"][4] for line in rr.LINES), (p, "magic"))
        require(len(set(f["entries"])) == 9 and any(v < 0 for v in f["entries"]), (p, "distinct; a local, not a real, configuration"))
    # precision guards refuse insufficient data
    for bad in (lambda: rr.local_root_symbol(roots, 113, 0), lambda: rr.local_root_symbol(roots[:8], 113, precision),
                lambda: rr.local_root_symbol([0] + roots[1:], 113, precision), lambda: rr.local_root_symbol(roots, 0, precision)):
        try:
            bad()
        except ValueError:
            pass
        else:
            require(False, "a precision guard did not fire")
    ctx.note("full Q_113 point with symbol -1 (three exact roots, six Hensel lifts); fourth-power controls at 2, 3, 113 with symbol +1; guards fire")
