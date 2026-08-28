"""M12-A: the H^{2,0} character atlas (docs/attacks/A8-descent-differentials.md §10)."""

from ..framework import check, require

DOC = "docs/attacks/A8-descent-differentials.md"


@check("a8.h20_atlas", DOC)
def _(ctx):
    """The canonical-bundle character decomposition of the resolution:
    h^{2,0}(chi_S) = C(|S|/2 - 1, 2); every sub-arrangement point has
    multiplicity <= 3 (all singularities negligible/ADE); the total is
    111 = chi(O) - 1 with q = 0 (the independently pinned invariants);
    the 84 K3 + 9 Horikawa census with its t3 distribution and
    D4-orbit structure is pinned."""
    from compute.h20_atlas import atlas, orbit_atlas

    rows = atlas()          # asserts total == 111 internally
    require(len(rows) == 256, "256 characters")
    by_size = {}
    t3_dist = {}
    for S, size, d2, t3, mm, h, typ in rows:
        require(mm <= 3, "point of multiplicity >= 4 in a sub-arrangement")
        require(d2 + 3 * t3 == size * (size - 1) // 2, "node count")
        by_size.setdefault(size, [0, 0])
        by_size[size][0] += 1
        by_size[size][1] += h
        if size == 6:
            require(typ == "K3" and h == 1)
            t3_dist[t3] = t3_dist.get(t3, 0) + 1
        elif size == 8:
            require(typ.startswith("Horikawa") and h == 3)
            require(t3 in (4, 5, 6), "octic t3")
        else:
            require(h == 0 and typ == "rational")
    require({s: tuple(v) for s, v in by_size.items()} == {
        0: (1, 0), 2: (36, 0), 4: (126, 0), 6: (84, 84), 8: (9, 27)},
        "size census")
    require(t3_dist == {0: 2, 1: 20, 2: 46, 3: 16}, "K3 t3 distribution")
    # the full 9-line arrangement: (t2, t3) = (12, 8) — matches A5
    full = [r for r in rows if r[1] == 8]
    require(sorted((d2, t3) for _, _, d2, t3, _, _, _ in full) ==
            sorted([(16, 4)] + [(13, 5)] * 4 + [(10, 6)] * 4),
            "octic census (omit center/corner/edge)")
    orb = orbit_atlas()
    require(len(orb[6]) == 16 and len(orb[8]) == 3, "D4-orbit counts")
    require(sum(o for _, o, _, _ in orb[6]) == 84)
    ctx.note("H^{2,0} fragments: 84 K3 characters (t3-census 2/20/46/16, "
             "rho >= 16 + t3) + 9 Horikawa characters (K^2 = 2, chi = 4); "
             "sum = 111 = chi(O) - 1: the abelian-cover formula confirmed "
             "against Noether")


@check("a8.web_cubics", DOC)
def _(ctx):
    """Theorem A8.19 (M11-J-2 opening): the eta*-web has NO integral
    graph cubic (linear in c or in v) through >= 3 triple points —
    the six univariate incidence families have constant-or-x^k gcds
    (exact, stdlib), and (FULL, sympy) the seven 2-parameter
    families' eliminations are Qbar-complete with every solution a
    known integral line."""
    from compute.web_cubics import (finish_two_param,
                                    gcd_roots_rational,
                                    run_univariate_slices,
                                    classify_solution)
    uni = run_univariate_slices()
    for name, (deg, roots) in uni.items():
        require(roots is not None, f"{name}: system vanished?!")
        if "a0=0" in name or "v0=0" in name:
            require(deg == 2 and roots == [__import__(
                "fractions").Fraction(0)], (name, deg, roots))
        else:
            require(deg == 0, f"{name}: nonconstant gcd {deg}")
    if ctx.bound(full=1, fast=0):
        try:
            import sympy  # noqa: F401
        except ImportError:
            from ..framework import Skip
            raise Skip("sympy needed for the 2-parameter families")
        res = finish_two_param(verbose=False)
        require(len(res) == 7)
        for name, (complete, sols) in res.items():
            require(complete, f"{name}: irrational y-candidates")
            for entry in sols:
                y0, roots = entry[0], entry[1]
                require(roots != "ALL x", f"{name}: degenerate family")
                require(entry[2], f"{name}: x-gcd not split")
                for x0 in roots:
                    deg, g = classify_solution(name, y0, x0)
                    require(deg <= 1, f"{name}: nonlinear solution!")
    ctx.note("A8.19: no integral graph cubics through >= 3 triple "
             "points — all thirteen incidence families contain only "
             "the known integral lines as degenerate members")
