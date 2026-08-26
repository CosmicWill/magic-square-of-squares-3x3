"""Reproduction of BTVA (papers/1912.08908) from our verified invariants.

Every number the paper states about the magic-square surface — and its
two calibration surfaces (perfect cuboid, nodal P^3 surfaces) — is
recomputed here in exact rational arithmetic from compute/btva_bounds.py,
using OUR independently derived (K^2, c_2) where applicable.
"""

from fractions import Fraction as F

from ..framework import check, require
from compute.btva_bounds import (CUBOID, XMS, bound_chi, bound_r,
                                 chi0_A1, chi1_A1, chi_local_A1, chi_sym,
                                 ci_invariants, ci_quadrics_invariants,
                                 cubic_coeffs, ell_min_quadrics,
                                 leading_coeff, surface_p3, threshold)

DOC = "docs/attacks/A7-curve-enumeration.md"


@check("a7btva.local_chi", DOC)
def _(ctx):
    """The A_1 local Euler characteristics: chi^0 matches the paper's
    printed first-values table, chi^0 + chi^1 == chi(s,.) holds across
    the three independently stated piecewise families, and all values
    are nonnegative integers."""
    table = [0, 3, 5, 12, 21, 34, 49, 75, 98, 134, 174, 222]
    require([chi0_A1(m) for m in range(1, 13)] == table,
            "chi^0 first-values table mismatch")
    top = 2000 if ctx.profile == "FULL" else 400
    for m in range(1, top + 1):
        c0, c1 = chi0_A1(m), chi1_A1(m)
        require(c0.denominator == 1 and c1.denominator == 1,
                f"non-integer local chi at m={m}")
        require(c0 >= 0 and c1 >= 0, f"negative local chi at m={m}")
        require(c0 + c1 == chi_local_A1(m), f"chi^0+chi^1 != chi at m={m}")
    ctx.note(f"chi^0 table reproduced; splitting identity to m={top}")


@check("a7btva.ci_invariants", DOC)
def _(ctx):
    """The paper's complete-intersection Chern formulas at n=8 equal our
    branched-cover stratification numbers (576, 768) — two fully
    independent routes to the invariants of the resolved X_ms."""
    require(ci_quadrics_invariants(8) == (576, 768))
    from compute.curve_pullbacks import cover_invariants
    inv = cover_invariants()
    require((inv["K2"], inv["chi_top_resolution"]) == (576, 768),
            "cover stratification disagrees with CI formulas")
    require(inv["n_nodes"] == 256, "node count changed")
    for n in range(5, 13):
        require(ci_invariants(n, (2,) * (n - 2)) ==
                ci_quadrics_invariants(n), f"CI formulas disagree at n={n}")
    ctx.note("(K^2, c_2) = (576, 768): cover route == CI route; 256 nodes")


@check("a7btva.chi_sym_display", DOC)
def _(ctx):
    """chi(Y, S^m Omega^1) for quadric CIs matches the paper's section-7
    display once its constant term reads 3n^2 - 27n + 66 (the printed
    '3n^2 - 27 + 66' is a typo: it disagrees for every n >= 2)."""
    for n in range(6, 11):
        K2, chi = ci_quadrics_invariants(n)
        for m in (1, 2, 3, 7, 20, 101):
            display = F(2 ** (n - 5), 3) * (
                2 * (n * n - 13 * n + 34) * m ** 3
                - 6 * (n * n - 7 * n + 16) * m ** 2
                - (5 * n * n - 41 * n + 98) * m
                + (3 * n * n - 27 * n + 66))
            require(chi_sym(K2, chi, m) == display,
                    f"display formula mismatch at n={n}, m={m}")
        require(3 * n * n - 27 * n + 66 != 3 * n * n - 27 + 66)
    ctx.note("display verified with corrected constant term 3n^2-27n+66")


@check("a7btva.ell_min", DOC)
def _(ctx):
    """The quadric-CI node thresholds: ell_min = 73, 145, 217, 145, 0
    for n = 6..10, with exact boundary behavior."""
    want = {6: 73, 7: 145, 8: 217, 9: 145, 10: 0, 11: 0, 12: 0}
    for n, lm in want.items():
        require(ell_min_quadrics(n) == lm, f"ell_min({n}) != {lm}")
        K2, chi = ci_quadrics_invariants(n)
        require(leading_coeff(K2, chi, lm) > 0)
        if lm > 0:
            require(leading_coeff(K2, chi, lm - 1) <= 0,
                    f"ell_min({n}) not minimal")
    ctx.note("ell_min table reproduced; 256 > 217 is the X_ms margin")


@check("a7btva.xms", DOC)
def _(ctx):
    """X_ms with our (K^2, c_2, ell) = (576, 768, 256): the bound turns
    (and stays) positive exactly at m = 47 with value 8448 — the paper's
    numbers — with cubic growth (160/27) m^3; the Serre-duality route
    would have needed ell >= 315 > 256, so BTVA's chi^1 bound is the one
    that works."""
    K2, chi, ell = XMS["K2"], XMS["chi"], XMS["ell"]
    require(leading_coeff(K2, chi, ell) == F(160, 27))
    require(threshold(K2, chi, ell) == 47, "threshold != 47")
    require(bound_chi(K2, chi, ell, 47) == 8448, "value at 47 != 8448")
    require(bound_chi(K2, chi, ell, 46) == -1968)
    require(bound_chi(K2, chi, ell, 3) < 0)
    # Serre-duality (BO) route: chi_sym + ell*chi0 stays cubically negative
    serre_lead = leading_coeff(K2, chi, 0) + ell * F(11, 108)
    require(serre_lead == F(-160, 27), "serre-route leading changed")
    need = min(l for l in range(1000)
               if leading_coeff(K2, chi, 0) + l * F(11, 108) > 0)
    require(need == 315)
    # partial-information refinement is subsumed: already positive at r=0,
    # and adding r*chi0 only increases the leading coefficient
    for r in (0, 1, 128, 255):
        require(leading_coeff(K2, chi, ell, r) >= F(160, 27))
    ctx.note("m>=47, h^0(S^47) >= 8448 reproduced from our invariants")


@check("a7btva.cuboid", DOC)
def _(ctx):
    """Calibration on the perfect-cuboid surface (n=6, ell=48): bare
    quasi-hyperbolicity fails (48 < 73), but with poles at r = 35 nodes
    the bound grows like (1/108) m^3, turning positive exactly at
    m = 862 — the paper's partial-information numbers — and r = 35 is
    minimal."""
    require(ci_quadrics_invariants(6) == (CUBOID["K2"], CUBOID["chi"]))
    K2, chi, ell = CUBOID["K2"], CUBOID["chi"], CUBOID["ell"]
    require(ell < ell_min_quadrics(6))
    require(leading_coeff(K2, chi, ell, 35) == F(1, 108))
    require(leading_coeff(K2, chi, ell, 34) < 0, "r=35 not minimal")
    require(threshold(K2, chi, ell, 35) == 862, "cuboid threshold != 862")
    require(bound_r(K2, chi, ell, 35, 861) <= 0)
    ctx.note("ell=48, r=35: 1/108 m^3, threshold 862 — paper reproduced")


@check("a7btva.p3_surfaces", DOC)
def _(ctx):
    """Calibration on nodal surfaces in P^3: Barth's decic (d=10,
    ell=345) turns positive at m=160 with value 15755; Sarti's surface
    (d=12, ell=600) at m=28 with value 7646.  The paper's *displayed*
    piecewise bound for the decic corresponds to ell = 339 in all four
    coefficients of all three residue classes (a display typo; its
    threshold would be 808): the stated conclusions match ell = 345."""
    for d, ell, m_want, v_want in ((10, 345, 160, 15755),
                                   (12, 600, 28, 7646)):
        K2, chi = surface_p3(d)
        require((K2, chi) == ((d - 4) ** 2 * d, d * (d * d - 4 * d + 6)))
        require(ell > F(9, 4) * (2 * d * d - 5 * d), "ell criterion")
        require(threshold(K2, chi, ell) == m_want, f"d={d} threshold")
        require(bound_chi(K2, chi, ell, m_want) == v_want, f"d={d} value")
    # the erratum: the printed decic display equals the ell=339 cubics
    K2, chi = surface_p3(10)
    printed = {
        0: (F(2, 9), F(-538, 3), F(-82), F(85)),
        1: (F(2, 9), F(-538, 3), F(-82), F(991, 9)),
        2: (F(2, 9), F(-538, 3), F(-472, 3), F(200, 9)),
    }
    for cls in range(3):
        require(cubic_coeffs(K2, chi, 339, 0, cls) == printed[cls],
                f"printed display != ell=339 at class {cls}")
        require(cubic_coeffs(K2, chi, 339, 0, cls) ==
                cubic_coeffs(K2, chi, 339, 0, cls + 3))
        require(cubic_coeffs(K2, chi, 345, 0, cls) != printed[cls])
    require(threshold(K2, chi, 339) == 808)
    ctx.note("decic 160/15755 & Sarti 28/7646 reproduced (display: ell=339 typo)")
