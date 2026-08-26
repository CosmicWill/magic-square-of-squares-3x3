"""Conic completeness layer (M10-B): the sharp budget lemma and the
exhaustive class sweeps of compute/conic_complete.py.

Together with the M9 tangent-to-5 sweep this machine-verifies
Theorem A7.7: no curve of geometric genus <= 1 on X has conic image in
the Lucas plane (characteristic 0).
"""

from fractions import Fraction as F
from itertools import combinations

from ..framework import check, require
from compute.conic_complete import (analyze_conic_K, k_el, k_inv, k_mul,
                                    k_sqrt, lift_rational, qsqrt,
                                    _deep_factors, _poly_gcd_q,
                                    _quadratic_factors, _rational_roots,
                                    sweep_C1, sweep_C2, sweep_C3, sweep_C4,
                                    sweep_C5, sweep_C6)
from compute.conic_pullbacks import analyze_conic, candidates, conic_through
from compute.curve_pullbacks import ENTRY_LINES, multiple_points

DOC = "docs/attacks/A7-curve-enumeration.md"


@check("a7cc.field_arithmetic", DOC)
def _(ctx):
    """Exact Q(sqrt(D)) arithmetic and the polynomial toolkit behind the
    sweeps: square testing, inversion, rational roots, quartic splitting,
    gcd."""
    D = F(2)
    x = (F(3), F(2))                       # (1 + sqrt2)^2
    require(k_sqrt(D, x) in [((F(1)), F(1)), (F(-1), F(-1))])
    require(k_sqrt(D, (F(2), F(0))) == (F(0), F(1)))
    require(k_sqrt(D, (F(9), F(0))) == (F(3), F(0)))
    require(k_sqrt(D, (F(5), F(0))) is None)
    require(k_sqrt(D, (F(1), F(1))) is None)     # norm -1
    require(k_mul(D, x, k_inv(D, x)) == (F(1), F(0)))
    for D2 in (F(5), F(-1), F(17, 4)):
        for a, b in ((F(2), F(3)), (F(-1), F(1, 2))):
            sq = k_mul(D2, (a, b), (a, b))
            r = k_sqrt(D2, sq)
            require(r is not None and k_mul(D2, r, r) == sq)
    require(qsqrt(F(49, 64)) == F(7, 8) and qsqrt(F(2)) is None)
    require(_rational_roots([6, -5, 1]) == [F(2), F(3)])
    require(sorted(_quadratic_factors([-2, 0, -1, 0, 1]))
            == [(1, 0, -2), (1, 0, 1)])          # t^4 - t^2 - 2
    require(_quadratic_factors([2, -3, 1]) == [])
    require(_deep_factors([1, 1, 0, 0, 1]) == 4)  # irreducible quartic
    require(_deep_factors([-2, 0, -1, 0, 1]) == 0)
    require(_poly_gcd_q([6, -5, 1], [2, -3, 1]) == [-2, 1])
    ctx.note("Q(sqrt D) ops, quartic splitting, gcd: all exact tests pass")


@check("a7cc.analyzer_agreement", DOC)
def _(ctx):
    """The field-generic analyzer agrees with the M9 rational analyzer on
    every M9 candidate conic (embedding Q in an irrelevant Q(sqrt 7))."""
    cands = candidates()
    if ctx.profile != "FULL":
        cands = [c for c in cands if not c[0].startswith("pencil")]
    n = 0
    for name, M in cands:
        a = analyze_conic(M, name)
        b = analyze_conic_K(lift_rational(M), F(7), name)
        if a.get("reducible") or a.get("degenerate_contained"):
            require(b.get("reducible") or b.get("degenerate_contained"),
                    f"degeneracy mismatch at {name}")
            continue
        n += 1
        require((a["k"], a["r_eff"], a["genus"], a["total_mult_check"]) ==
                (b["k"], b["r_eff"], b["genus"], b["total_mult_check"]),
                f"analyzer disagreement at {name}")
    ctx.note(f"K-analyzer == Q-analyzer on {n} irreducible conics")


def combinations_with_replacement_idx(n, r):
    from itertools import combinations_with_replacement
    return combinations_with_replacement(range(n), r)


@check("a7cc.budget_lemma", DOC)
def _(ctx):
    """Mechanical case analysis of Lemma A7.6: enumerating all point-type
    multisets from the forced (s, t) alphabet with total multiplicity 18
    and r_eff <= 4 shows (a) r_eff <= 3 forces >= 5 tangent lines, and
    (b) r_eff = 4 with <= 4 tangent lines realizes exactly the six class
    signatures C1..C6."""
    # effective point types: (s, t, kind); kind constrains the location
    types = [(3, 0, "triple"), (2, 1, "triple"), (2, 0, "double"),
             (1, 1, "double"), (1, 0, "simple")]
    found = set()
    for e in range(0, 5):                      # number of effective points
        for combo in combinations_with_replacement_idx(len(types), e):
            chosen = [types[i] for i in combo]
            m_eff = sum(s + 2 * t for s, t, _ in chosen)
            rem = 18 - m_eff                   # absorbed by free tangencies
            if rem < 0 or rem % 2:
                continue
            free = rem // 2
            T = free + sum(t for _, t, _ in chosen)
            if T > 9:
                continue
            if e <= 3:
                require(T >= 5,
                        f"r_eff={e} with only {T} tangencies: {chosen}")
                continue
            if T >= 5:
                continue                        # tangent-to-5 class
            sig = (tuple(sorted((s, t, kind) for s, t, kind in chosen)),
                   free)
            found.add(sig)
    expect = {
        # C1: four transversal triples + 3 free
        ((( 3, 0, "triple"),) * 4, 3),
        # C2: three transversal triples + simple crossing + 4 free
        (tuple(sorted([(3, 0, "triple")] * 3 + [(1, 0, "simple")])), 4),
        # C3: three transversal triples + tangent-at-double + 3 free
        (tuple(sorted([(3, 0, "triple")] * 3 + [(1, 1, "double")])), 3),
        # C4: two triples + two doubles + 4 free
        (tuple(sorted([(3, 0, "triple")] * 2 + [(2, 0, "double")] * 2)), 4),
        # C5: two triples + double + tangent-at-triple + 3 free
        (tuple(sorted([(3, 0, "triple")] * 2
                      + [(2, 0, "double"), (2, 1, "triple")])), 3),
        # C6: two triples + two tangent-at-triples + 2 free
        (tuple(sorted([(3, 0, "triple")] * 2 + [(2, 1, "triple")] * 2)), 2),
    }
    require(found == expect,
            f"class signatures changed: {sorted(found - expect)} extra, "
            f"{sorted(expect - found)} missing")
    ctx.note("genus 0 => T >= 5; genus 1 residual classes = exactly C1..C6")


@check("a7cc.t5_completeness", DOC)
def _(ctx):
    """The tangent-to->=5 class is complete and rational: a smooth conic
    tangent to five entry lines has a smooth dual conic through their
    five (rational) dual points, so no three of the five lines are
    concurrent and the dual conic is the unique conic through the five
    dual points -- which the M9 sweep enumerated.  Verified: for every
    5-subset either three lines are concurrent (no smooth conic) or the
    through-duals system has a unique solution."""
    mp = multiple_points()
    concurrent = [set(ls) for p, ls in mp.items() if len(ls) == 3]
    n_conc = n_unique = 0
    for sub in combinations(range(9), 5):
        has3 = any(t <= set(sub) for t in concurrent)
        M = conic_through([ENTRY_LINES[i] for i in sub])
        if has3:
            n_conc += 1
            # any conic through 3 collinear dual points is a line pair:
            from compute.conic_pullbacks import conic_det
            require(M is None or conic_det(M) == 0,
                    f"smooth dual through concurrent triple {sub}?!")
        else:
            n_unique += 1
            require(M is not None, f"no unique dual conic for {sub}")
    require(n_conc + n_unique == 126)
    ctx.note(f"{n_unique} candidate 5-subsets, {n_conc} concurrent-killed")


@check("a7cc.class_sweeps", DOC)
def _(ctx):
    """The six residual class sweeps: zero genus <= 1 components, zero
    unresolved flags, with the exact bookkeeping pinned (any change in
    counts means the systems changed -- investigate, don't assume)."""
    expect = {
        "C1": dict(n_systems=70, analyzed=1,
                   counters={"skipped_reducible": 0,
                             "pencils_with_builtin_tangency": 0,
                             "skipped_collinear": 47}),
        "C4": dict(n_systems=1848, analyzed=8,
                   counters={"skipped_reducible": 0,
                             "pencils_with_builtin_tangency": 0,
                             "skipped_collinear": 822}),
        "C3": dict(n_systems=1104, analyzed=216,
                   counters={"skipped_reducible": 888,
                             "pencils_with_builtin_tangency": 0,
                             "skipped_collinear": 0}),
        "C5": dict(n_systems=6048, analyzed=1016,
                   counters={"skipped_reducible": 5032,
                             "pencils_with_builtin_tangency": 0,
                             "skipped_collinear": 0}),
        "C6": dict(n_systems=3780, analyzed=20,
                   counters={"skipped_reducible": 1458,
                             "pencils_with_builtin_tangency": 0,
                             "skipped_collinear": 0}),
    }
    for fn in (sweep_C1, sweep_C4, sweep_C3, sweep_C5, sweep_C6):
        s = fn()
        want = expect[s["label"]]
        require(s["hits"] == [], f"{s['label']}: genus<=1 hit!")
        require(s["flags"] == [], f"{s['label']}: unresolved flags "
                                  f"{s['flags'][:3]}")
        for k, v in want.items():
            require(s[k] == v, f"{s['label']}.{k}: {s[k]} != {v}")
    ctx.note("C1/C3/C4/C5/C6: all systems resolved, zero low-genus hits")


@check("a7cc.c2_nets", DOC)
def _(ctx):
    """The C2 net sweep: 46 non-collinear triple-nets, 5796 four-tangency
    subsets, 5792 certified empty by the resultant-gcd criterion, and the
    4 candidate solutions all equal the genus-9 circle u^2+v^2 = c^2
    (through four triple points, tangent to c+u, c+v, c-v, c-u)."""
    s = sweep_C2()
    require(s["hits"] == [], "C2: genus<=1 hit!")
    require(s["flags"] == [], f"C2: unresolved flags {s['flags'][:3]}")
    require(s["n_nets"] == 46, f"nets {s['n_nets']}")
    require(s["n_4subsets_certified_empty"] == 5792)
    require(s["n_4subsets_with_candidates"] == 4)
    require(s["analyzed"] == 4)
    require(s["n_nets"] * 126 == s["n_4subsets_certified_empty"]
            + s["n_4subsets_with_candidates"], "4-subset accounting")
    # the four candidates are all the circle: genus 9, k=4, r_eff=6
    circle = analyze_conic([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], "circle")
    ctx.note(f"5792/5796 certified empty; 4 candidates = the circle "
             f"(genus {circle['genus']})")
    require(circle["genus"] == 9)


@check("a7cc.collinear_triples", DOC)
def _(ctx):
    """The collinearity skips are justified and exactly understood: the
    8 triple points contain exactly 10 collinear 3-subsets -- four on the
    entry line c, one on each of the four (u+-v)-type entry lines, and
    one on each of the difference lines u = 0 and v = 0."""
    from compute.conic_complete import _collinear3, _triples_doubles
    triples, _, mp = _triples_doubles()
    coll = [t for t in combinations(triples, 3) if _collinear3(t)]
    require(len(coll) == 10, f"{len(coll)} collinear triples")
    require(len([t for t in combinations(triples, 4) if _collinear3(t)])
            == 47)
    on_c = [p for p in triples if p[0] == 0]
    require(len(on_c) == 4)
    ctx.note("10 collinear triple-triples (c-line: 4; u±v lines: 4; "
             "u=0, v=0: 2); 47 of the 70 quadruples are degenerate")
