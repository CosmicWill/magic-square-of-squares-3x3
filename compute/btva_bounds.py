"""BTVA symmetric-differential bounds, reimplemented exactly (M10-A).

Source (READ, in-repo): papers/1912.08908/BTVA.tex — Bruin, Thomas,
Várilly-Alvarado, "Explicit computation of symmetric differentials and
its application to quasi-hyperbolicity", Algebra & Number Theory 16
(2022) 1377-1405, arXiv:1912.08908v3.

Everything here is exact rational arithmetic (fractions.Fraction); no
floats.  The formulas implemented, with the paper's own labels:

* ``chi_sym``   — chi(Y, S^m Omega^1_Y) for a smooth surface Y with
  invariants K^2 = c_1(Y)^2 and chi = c_2(Y)   [appendix, E:chiYSm].
* ``chi0_A1``   — Wahl local chi^0(s, S^m Omega^1_Y) at an A_1 point
  (codimension of sections extending over the node), piecewise cubic in
  m by residue mod 6   [Proposition P:codim_E_regular, eq:localTerms].
* ``chi1_A1``   — local chi^1(s, S^m Omega^1_Y) at an A_1 point,
  piecewise cubic by residue mod 3   [Proposition P:local_chi,
  E:local_chi1].
* ``chi_local_A1`` — their sum chi(s, .)   [eq:locsymEuler]; the
  identity chi0 + chi1 == chi_local is a nontrivial consistency check
  between three independently stated piecewise families.
* ``bound_chi`` — the main lower bound  h^0(Y, S^m Omega^1_Y) >=
  chi_sym + ell * chi1_A1  for a surface with ell A_1 nodes, m >= 3
  [Theorem thm:main, E:h0Yestimate_chi].
* ``bound_r``   — the refinement allowing poles along r exceptional
  curves:  h^0(Y - (E_1 u...u E_r), S^m Omega^1_Y) >=
  chi_sym + ell*chi1 + r*chi0   [Prop C:regdif_lowerbound_quasiproj,
  E:h0Yestimate_chi_r].  When this grows ~ C m^3 with C > 0, the paper
  concludes there are only finitely many genus 0 or 1 curves on X
  passing through at most ell - r of the nodes (they demonstrate it on
  the cuboid surface: ell = 48, r = 35, "at most 13").
* ``bound_serre`` — the older Bogomolov-Deschamps/Serre-duality route
  h^0 >= chi_sym + ell * chi0   [Remark rem:BORR,
  E:h0Yestimate_serre_duality]; weaker for A_1 since chi0 has smaller
  leading term (11/108 < 4/27).
* ``ci_quadrics_invariants`` / ``ci_invariants`` — resolution Chern
  numbers of nodal complete intersections (section s:QuadricCIs and
  Lemma L:atiyah's smooth-CI reduction): these are the formulas that
  independently confirm our branched-cover computation
  (K^2, c_2) = (576, 768) for the magic-square surface at n = 8.

Rigorous threshold search: each bound is, on a fixed residue class of m
mod 6, a genuine cubic polynomial.  ``threshold`` computes, per class,
the Cauchy root bound of that cubic and scans past it, so its output
"positive for ALL m >= M" is a proved statement, not a scan to an
arbitrary horizon.

Paper targets reproduced (see verify/checks/a7_btva.py):
  * chi^0 first-values table m=1..12: 0,3,5,12,21,34,49,75,98,134,174,222
  * ell_min(n) table for quadric CIs: 73, 145, 217, 145, 0 (n=6..>=10)
  * X_ms (n=8, ell=256): threshold m >= 47, bound value 8448 at m=47
  * cuboid (n=6, ell=48, r=35): leading coefficient 1/108, threshold 862
  * Barth decic (d=10, ell=345): threshold 160, value 15755
  * Sarti (d=12, ell=600): threshold 28, value 7646
"""

from fractions import Fraction as F
from math import comb, prod

# ----------------------------------------------------------------------
# Global Euler characteristic (appendix E:chiYSm)

def chi_sym(K2, chi, m):
    """chi(Y, S^m Omega^1_Y) = (2(K^2-chi)m^3 - 6chi m^2 - (K^2+3chi)m
    + K^2 + chi)/12."""
    return F(2 * (K2 - chi) * m**3 - 6 * chi * m**2 - (K2 + 3 * chi) * m
             + K2 + chi, 12)


# ----------------------------------------------------------------------
# Local Euler characteristics at an A_1 node

# chi^0: cubic coefficients (a3, a2, a1, a0) per residue of m mod 6
_CHI0 = {
    0: (F(11, 108), F(11, 36), F(1, 6), F(0)),
    1: (F(11, 108), F(11, 36), F(-1, 12), F(-35, 108)),
    2: (F(11, 108), F(11, 36), F(7, 18), F(5, 27)),
    3: (F(11, 108), F(11, 36), F(-1, 12), F(-1, 4)),
    4: (F(11, 108), F(11, 36), F(1, 6), F(-2, 27)),
    5: (F(11, 108), F(11, 36), F(5, 36), F(-7, 108)),
}

# chi^1: cubic coefficients per residue of m mod 3
_CHI1 = {
    0: (F(4, 27), F(4, 9), F(1, 3), F(0)),
    1: (F(4, 27), F(4, 9), F(1, 3), F(2, 27)),
    2: (F(4, 27), F(4, 9), F(1, 9), F(-5, 27)),
}


def _eval_cubic(coeffs, m):
    a3, a2, a1, a0 = coeffs
    return ((a3 * m + a2) * m + a1) * m + a0


def chi0_A1(m):
    """Wahl chi^0 at an A_1 node (eq:localTerms)."""
    return _eval_cubic(_CHI0[m % 6], m)


def chi1_A1(m):
    """Wahl chi^1 at an A_1 node (E:local_chi1)."""
    return _eval_cubic(_CHI1[m % 3], m)


def chi_local_A1(m):
    """chi(s, S^m Omega^1) at an A_1 node (eq:locsymEuler)."""
    if m % 2 == 0:
        return F(m * (m + 1) * (m + 2), 4)
    return F((m + 1) * (m**2 + 2 * m - 1), 4)


# ----------------------------------------------------------------------
# The lower bounds of thm:main / C:regdif_lowerbound_quasiproj / rem:BORR

def bound_chi(K2, chi, ell, m):
    """RHS of E:h0Yestimate_chi: lower bound for h^0(Y, S^m Omega^1_Y),
    valid for m >= 3."""
    return chi_sym(K2, chi, m) + ell * chi1_A1(m)


def bound_r(K2, chi, ell, r, m):
    """RHS of E:h0Yestimate_chi_r: lower bound for sections regular away
    from r chosen exceptional curves, m >= 3."""
    return bound_chi(K2, chi, ell, m) + r * chi0_A1(m)


def bound_serre(K2, chi, ell, m):
    """RHS of E:h0Yestimate_serre_duality (the BO route)."""
    return chi_sym(K2, chi, m) + ell * chi0_A1(m)


def cubic_coeffs(K2, chi, ell, r, cls6):
    """Exact cubic coefficients (a3, a2, a1, a0) of m |-> bound_r(...)
    restricted to the residue class m = cls6 (mod 6)."""
    base = (F(K2 - chi, 6), F(-chi, 2), F(-(K2 + 3 * chi), 12),
            F(K2 + chi, 12))
    c1 = _CHI1[cls6 % 3]
    c0 = _CHI0[cls6]
    return tuple(b + ell * x1 + r * x0 for b, x1, x0 in zip(base, c1, c0))


def leading_coeff(K2, chi, ell, r=0):
    """m^3 coefficient of bound_r: (K^2-chi)/6 + ell*4/27 + r*11/108.
    For r=0 this is (9K^2 - 9chi + 8 ell)/54 (Example ex:hypersurfaces)."""
    return F(K2 - chi, 6) + ell * F(4, 27) + r * F(11, 108)


def threshold(K2, chi, ell, r=0):
    """Smallest M >= 3 with bound_r(...) > 0 for ALL m >= M (proved via
    per-residue-class Cauchy root bounds), or None if the leading
    coefficient is not positive."""
    if leading_coeff(K2, chi, ell, r) <= 0:
        return None
    horizon = 3
    for cls6 in range(6):
        a3, a2, a1, a0 = cubic_coeffs(K2, chi, ell, r, cls6)
        cauchy = 1 + max(abs(a2), abs(a1), abs(a0)) / a3
        horizon = max(horizon, int(cauchy) + 2)
    # every real root of every class cubic has m < horizon, so signs are
    # locked from horizon on; scan downward for the persistence point
    m = horizon
    while m > 3 and bound_r(K2, chi, ell, r, m - 1) > 0:
        m -= 1
    return m


# ----------------------------------------------------------------------
# Chern numbers of resolutions of nodal complete intersections

def ci_invariants(n, degrees):
    """(K^2, c_2) of (a minimal resolution of) a complete intersection
    surface of multidegree ``degrees`` in P^n with isolated du Val
    singularities; by Lemma L:atiyah these equal the smooth values
    (section S:GlobalSymmetricDifferentials-I, display after
    cor:MainLowerBound)."""
    assert len(degrees) == n - 2
    d = prod(degrees)
    s1 = sum(degrees)
    s2 = sum(degrees[i] * degrees[j] for i in range(len(degrees))
             for j in range(i + 1, len(degrees)))
    K2 = (n + 1 - s1) ** 2 * d
    chi = (comb(n + 1, 2) - (n + 1 - s1) * s1 - s2) * d
    return K2, chi


def ci_quadrics_invariants(n):
    """(K^2, c_2) for a CI of n-2 quadrics in P^n (section s:QuadricCIs):
    K^2 = (n-5)^2 2^(n-2),  c_2 = (n^2-7n+16) 2^(n-3)."""
    return (n - 5) ** 2 * 2 ** (n - 2), (n * n - 7 * n + 16) * 2 ** (n - 3)


def ell_min_quadrics(n):
    """Minimal node count for which E:h0Yestimate_chi certifies a big
    cotangent bundle: smallest integer ell >= 0 with
    9K^2 - 9chi + 8ell > 0."""
    K2, chi = ci_quadrics_invariants(n)
    ell = 0
    while leading_coeff(K2, chi, ell) <= 0:
        ell += 1
    return ell


# ----------------------------------------------------------------------
# The surfaces of the paper

XMS = dict(n=8, K2=576, chi=768, ell=256)          # magic squares, P^8
CUBOID = dict(n=6, K2=16, chi=80, ell=48)          # perfect cuboid, P^6


def surface_p3(d):
    """(K^2, c_2) for (the resolution of) a nodal degree-d surface in
    P^3 (Example Ex:NodalInP3)."""
    return ci_invariants(3, (d,))


def chi_hat(K2, chi, ell, m):
    """chi(X, hat-S^m Omega^1_X) for a surface X with ell A_1 nodes and
    resolution invariants (K^2, chi): by Blache's local-global formula
    (BTVA's proof of P:local_chi), chi(X, hat-S^m) = chi(Y, S^m) +
    ell * chi(s, S^m).  For X_ms this first turns positive at m = 7
    (value 384); with h^2(X, hat-S^m) = 0 for m >= 3 (Bogomolov-
    De Oliveira / Deschamps, as used in BTVA's lem:Leray) this gives
    h^0(X - nodes, S^m Omega^1) >= chi_hat(m), hence guaranteed
    sections at m = 7."""
    return chi_sym(K2, chi, m) + ell * chi_local_A1(m)


def main():
    print("== local Euler characteristics at an A_1 node ==")
    row = [int(chi0_A1(m)) for m in range(1, 13)]
    print("chi0, m=1..12:", row, "(paper: 0,3,5,12,21,34,49,75,98,134,174,222)")
    assert all(chi0_A1(m) + chi1_A1(m) == chi_local_A1(m)
               for m in range(1, 500)), "chi0+chi1 != chi at some m"
    print("chi0 + chi1 == chi(s, .) verified for m = 1..499")

    print("\n== quadric complete intersections in P^n ==")
    for n in range(6, 11):
        K2, chi = ci_quadrics_invariants(n)
        print(f"n={n}: K2={K2}, c2={chi}, ell_min={ell_min_quadrics(n)}")

    print("\n== X_ms (magic squares of squares) ==")
    K2, chi, ell = XMS["K2"], XMS["chi"], XMS["ell"]
    t = threshold(K2, chi, ell)
    print(f"K2={K2}, c2={chi}, ell={ell}; "
          f"leading coeff = {leading_coeff(K2, chi, ell)}")
    print(f"bound positive for all m >= {t}; "
          f"value at {t}: {bound_chi(K2, chi, ell, t)}")
    for m in (46, 47, 48, 50, 60, 100):
        print(f"  m={m}: h0 >= {bound_chi(K2, chi, ell, m)}")
    print("Serre-duality route (E:h0Yestimate_serre_duality) leading "
          f"coeff: {leading_coeff(K2, chi, 0) + ell * F(11, 108)} (< 0: "
          "that route would need ell >= 315)")

    print("\n== cuboid surface, partial information ==")
    K2, chi, ell = CUBOID["K2"], CUBOID["chi"], CUBOID["ell"]
    r = 35
    print(f"K2={K2}, c2={chi}, ell={ell}, r={r}: leading coeff = "
          f"{leading_coeff(K2, chi, ell, r)} (paper: 1/108)")
    print(f"threshold: {threshold(K2, chi, ell, r)} (paper: 862)")

    print("\n== nodal surfaces in P^3 ==")
    for name, d, ell, want in (("Barth decic", 10, 345, (160, 15755)),
                               ("Sarti", 12, 600, (28, 7646))):
        K2, chi = surface_p3(d)
        t = threshold(K2, chi, ell)
        print(f"{name}: d={d}, ell={ell}, K2={K2}, c2={chi}: threshold "
              f"{t}, value {bound_chi(K2, chi, ell, t)} (paper: {want})")


if __name__ == "__main__":
    main()
