"""The eta*-web at degree 1 (M11-J opening): ALL integral lines.

By Theorem A8.16 every complete genus-0 curve on X beyond the 128
classical AP components has its Lucas image on the single web
eta* = eta_4 (the resolution's unique symmetric quartic
differential).  This module classifies the web's ALGEBRAIC INTEGRAL
LINES completely:

  THEOREM A8.17.  The eta*-integral lines in P^2 over Qbar are
  exactly FIFTEEN: the nine entry lines, the two pencil carriers
  u = 0 and v = 0, and the four Q(sqrt3)-lines

      sqrt3 * c = +-u +- v,

  each passing through exactly one diagonal triple point D+- (and
  through no other triple point).  In particular (Theorem A7.3) the
  components of X over the four new lines all have genus >= 2: the
  web's line-level integral curves carry no rational curves beyond
  the classical families — consistent with A8.15/A8.16.

Method (exact, sympy only for two resultants — the check Skips
without it):

  * every affine line is c = a + b v (family II, verticals included)
    or v = k (family I); the only line outside the chart is u = 0.
  * Family II: the restriction of eta* to c = a + bt, v = t is
    sum_k N_k(a + bt, t) b^k; its t-coefficients give a polynomial
    system E in Z[a, b] whose solutions are the integral lines.
    Completeness: the exact univariate gcd of two a-resultants of
    the system peels EXACTLY as b^e0 (b^2-1)^e1 (3b^2-1)^e2 down to
    a constant, so every solution has b in {0, +-1, +-1/sqrt3}; for
    each candidate b the exact gcd of {E_i(a, b)} over Q resp.
    Q(sqrt3) pins the a-values.  The resulting 13 points are
    verified integral by exact substitution.
  * Family I: only the dc^4-coefficient N_4(c, k) survives; the gcd
    of its c-coefficients as polynomials in k is k^2: only v = 0.
  * u = 0: integral by the exact chart-2 slice (M11-F).

Run:  python3 -m compute.web_lines
"""

from fractions import Fraction as F
from functools import reduce
from math import comb, gcd

from compute.conic_complete import k_add, k_el, k_inv, k_is_zero, k_mul
from compute.special_locus import (is_zero, numerator_forms,
                                   poly_gcd_1var, restrict_u0)

M = 4
D = 3  # the field Q(sqrt 3)


def eta_star():
    """Integer-cleared numerators of eta* = eta_4."""
    Ns = numerator_forms()[3]
    dens = [v.denominator for c in Ns for v in c.values()]
    L = reduce(lambda x, y: x * y // gcd(x, y), dens, 1)
    return [{ij: int(v * L) for ij, v in c.items() if v} for c in Ns]


def line_system():
    """The nonzero t-coefficients of the family-II restriction, as
    polynomial dicts {(i, j): int} in (a, b)."""
    Ns = eta_star()
    by_t = {}
    for k in range(M + 1):
        for (i, j), val in Ns[k].items():
            # (a + b t)^i t^j b^k = sum_m C(i,m) a^(i-m) b^(m+k) t^(m+j)
            for m in range(i + 1):
                key = (m + j, (i - m, m + k))
                by_t[key] = by_t.get(key, 0) + val * comb(i, m)
    eqs = {}
    for (tdeg, ab), val in by_t.items():
        if val:
            eqs.setdefault(tdeg, {})[ab] = val
    out = [eqs[t] for t in sorted(eqs) if eqs[t]]
    assert out, "empty system?!"
    return out


# the fifteen lines: affine (a, b) means c = a + b v; entries are
# Q(sqrt3) pairs (r, s) = r + s*sqrt3
GRID_PTS = [(k_el(x), k_el(y)) for x in (-1, 0, 1) for y in (-1, 0, 1)]
SQRT3_PTS = [(k_el(0, F(sx, 3)), k_el(0, F(sy, 3)))
             for sx in (1, -1) for sy in (1, -1)]  # +-1/sqrt3 = sqrt3/3


def eval_system_at(eqs, a_el, b_el):
    """Evaluate every equation at (a, b) in Q(sqrt3); True iff all
    vanish."""
    for E in eqs:
        mi = max(i for (i, _) in E)
        mj = max(j for (_, j) in E)
        ap = [k_el(1)]
        for _ in range(mi):
            ap.append(k_mul(D, ap[-1], a_el))
        bp = [k_el(1)]
        for _ in range(mj):
            bp.append(k_mul(D, bp[-1], b_el))
        acc = k_el(0)
        for (i, j), val in E.items():
            acc = k_add(acc, k_mul(D, (F(val), F(0)),
                                   k_mul(D, ap[i], bp[j])))
        if not k_is_zero(acc):
            return False
    return True


def _k_poly_gcd(polys):
    """gcd of univariate polynomials over Q(sqrt3), coefficients as
    pairs; polys are lists ascending.  Returns monic gcd list."""
    def deg(p):
        d = len(p) - 1
        while d >= 0 and k_is_zero(p[d]):
            d -= 1
        return d

    def rem(p, q):
        p = p[:]
        dq = deg(q)
        lead_inv = k_inv(D, q[dq])
        while deg(p) >= dq >= 0:
            dp = deg(p)
            fac = k_mul(D, p[dp], lead_inv)
            for i in range(dq + 1):
                p[dp - dq + i] = k_add(
                    p[dp - dq + i],
                    k_mul(D, (-fac[0], -fac[1]), q[i]))
            p[dp] = k_el(0)
        return p

    g = None
    for p in polys:
        if deg(p) < 0:
            continue
        if g is None:
            g = p[:]
        else:
            aa, bb = g, p[:]
            while deg(bb) >= 0:
                aa, bb = bb, rem(aa, bb)
            g = aa
        if deg(g) == 0:
            break
    d = deg(g)
    inv = k_inv(D, g[d])
    return [k_mul(D, x, inv) for x in g[:d + 1]]


def _eval_b(eqs, b_el):
    """Substitute b = b_el (Q(sqrt3)): list of univariate a-polys
    (ascending, Q(sqrt3) coefficients)."""
    out = []
    for E in eqs:
        mi = max(i for (i, _) in E)
        mj = max(j for (_, j) in E)
        bp = [k_el(1)]
        for _ in range(mj):
            bp.append(k_mul(D, bp[-1], b_el))
        poly = [k_el(0)] * (mi + 1)
        for (i, j), val in E.items():
            poly[i] = k_add(poly[i],
                            k_mul(D, (F(val), F(0)), bp[j]))
        out.append(poly)
    return out


def candidates_for_b(eqs, b_el):
    """Roots in Q(sqrt3) of the gcd of the system at b = b_el; the
    gcd must split into linear factors over Q(sqrt3) for the listed
    roots (asserted by degree count)."""
    g = _k_poly_gcd(_eval_b(eqs, b_el))
    # find the roots among small Q(sqrt3) candidates by division
    roots = []
    cands = [k_el(x) for x in (-1, 0, 1)] + \
            [k_el(0, F(s, 3)) for s in (1, -1)]
    cur = g
    changed = True
    while changed and len(cur) > 1:
        changed = False
        for r in cands:
            # synthetic division by (a - r)
            q = [k_el(0)] * (len(cur) - 1)
            acc = k_el(0)
            for i in range(len(cur) - 1, 0, -1):
                acc = k_add(k_mul(D, acc, r), cur[i])
                q[i - 1] = acc
            remv = k_add(k_mul(D, acc, r), cur[0])
            if k_is_zero(remv):
                roots.append(r)
                cur = q
                changed = True
                break
    assert len(cur) == 1, "gcd has roots outside the candidate set"
    return roots


def peel_known(g):
    """Divide the integer-coefficient univariate g (ascending) by b,
    (b^2 - 1), (3 b^2 - 1) as often as possible; returns exponents
    and the leftover degree (must be 0 for completeness)."""
    g = [F(x) for x in g]

    def divide(p, q):
        # exact division attempt; returns quotient or None
        p = p[:]
        out = [F(0)] * (len(p) - len(q) + 1)
        for i in range(len(p) - len(q), -1, -1):
            c = p[i + len(q) - 1] / q[-1]
            out[i] = c
            for j in range(len(q)):
                p[i + j] -= c * q[j]
        if any(x != 0 for x in p):
            return None
        return out

    exps = [0, 0, 0]
    for idx, q in enumerate(([F(0), F(1)], [F(-1), F(0), F(1)],
                             [F(-1), F(0), F(3)])):
        while len(g) > len(q) - 1:
            nxt = divide(g, q)
            if nxt is None:
                break
            g, exps[idx] = nxt, exps[idx] + 1
    return exps, len(g) - 1


def classify(res_pair=None):
    """The full Theorem A8.17 certificate.  `res_pair` is the pair of
    exact univariate resultants Res_a(E_1, E_2), Res_a(E_1, E_3)
    (computed by the caller, e.g. with sympy); completeness of the
    b-candidates is certified by peeling their exact gcd down to a
    constant with the known factors only."""
    eqs = line_system()
    out = {"n_equations": len(eqs)}
    # (1) the fifteen lines verified integral by substitution
    for (a_el, b_el) in GRID_PTS + SQRT3_PTS:
        assert eval_system_at(eqs, a_el, b_el), \
            f"listed line not integral: {(a_el, b_el)}"
    # family I: v = k integral iff N_4(c, k) == 0: gcd of the
    # c-coefficients as k-polynomials must be k^2 (only k = 0)
    Ns = eta_star()
    by_i = {}
    for (i, j), val in Ns[4].items():
        by_i.setdefault(i, {})[j] = val
    g = None
    for i, dd in by_i.items():
        lst = [dd.get(j, 0) for j in range(max(dd) + 1)]
        g = lst if g is None else poly_gcd_1var(g, lst)
    assert [F(x) for x in g] == [F(0), F(0), F(1)], f"family I: {g}"
    # u = 0: integral by the chart-2 slice
    Wn = numerator_forms()[3]
    assert is_zero(restrict_u0(Wn)), "u = 0 not integral?!"
    # (2) completeness of family II: `res_pair` must be NONZERO
    # univariate b-resultants Res_a(E_i, E_j) of system pairs — by
    # the Bezout identity Res = u E_i + v E_j, every solution's b is
    # a root of each, unconditionally
    if res_pair is not None:
        R1, R2 = res_pair
        assert any(x != 0 for x in R1) and any(x != 0 for x in R2), \
            "vacuous certificate: a resultant is identically zero"
        gg = poly_gcd_1var(R1, R2)
        assert any(x != 0 for x in gg)
        den = reduce(lambda x, y: x * y // gcd(x, y),
                     (c.denominator for c in gg), 1)
        exps, left = peel_known([int(c * den) for c in gg])
        assert left == 0, f"unknown factor of degree {left} survives!"
        assert exps[2] >= 1, "the sqrt3 factor must appear"
        out["gcd_exponents_b_b2m1_3b2m1"] = exps
        # per-candidate a-roots
        found = set()
        for b_el, tag in ([(k_el(0), "0"), (k_el(1), "1"),
                           (k_el(-1), "-1"),
                           (k_el(0, F(1, 3)), "1/sqrt3"),
                           (k_el(0, F(-1, 3)), "-1/sqrt3")]):
            for r in candidates_for_b(eqs, b_el):
                found.add((r, tuple(b_el)))
        assert len(found) == 13, f"solution count {len(found)} != 13"
        out["n_solutions"] = 13
        out["complete"] = True
    else:
        out["complete"] = False
    return out


def nonzero_resultants(sp, want=2):
    """The first `want` NONZERO resultants Res_a(E_i, E_j) over the
    system's pairs, as ascending Fraction lists.  (Pairs whose
    resultant vanishes identically share an a-factor and certify
    nothing — they are skipped; a nonzero resultant is sound by the
    Bezout identity.)"""
    from itertools import combinations
    a, b = sp.symbols("a b")
    eqs = line_system()

    def to_expr(E):
        return sum(val * a ** i * b ** j for (i, j), val in E.items())

    exprs = [to_expr(E) for E in eqs]
    out = []
    for i, j in combinations(range(len(exprs)), 2):
        R = sp.resultant(exprs[i], exprs[j], a)
        if R == 0:
            continue
        out.append([F(x) for x in sp.Poly(R, b).all_coeffs()[::-1]])
        if len(out) == want:
            return out
    raise AssertionError("fewer than two nonzero resultants")


def main():
    try:
        import sympy as sp
    except ImportError:
        print("sympy unavailable: verifying the 15 lines only "
              "(completeness needs the two resultants)")
        print(classify())
        return
    cert = classify(res_pair=nonzero_resultants(sp))
    print(cert)
    print("THEOREM A8.17: the eta*-integral lines are exactly 15 —")
    print("  the 9 entry lines, u = 0, v = 0, and the four")
    print("  Q(sqrt3)-lines  sqrt3 c = +-u +-v  (through one D-point")
    print("  each; their X-components all have genus >= 2 by A7.3).")


if __name__ == "__main__":
    main()
