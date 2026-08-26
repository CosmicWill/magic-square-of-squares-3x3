"""Descent of symmetric differentials to the Lucas plane (M11, A8).

THE POINT.  H^0(X, S^m Omega^1) taken over the smooth locus X-minus-nodes
(equivalently H^0(X, hat-S^m Omega^1_X), the space BTVA declare "out of
range of current computational techniques" for the magic-square surface)
decomposes under the Galois group G = (Z/2)^8 of the cover
pi : X -> P^2 into 256 character eigenspaces.  A character corresponds
to an EVEN subset s of the nine entry lines, and the eigenspace is

    V_S = { eta rational m-symmetric differential on P^2, poles only on
            the arrangement :  pi^*(eta) / prod_{j in S} x_j  is regular
            on X-minus-nodes },

because an invariant rational section descends (pi is generically
etale) and regularity of a rational section of a vector bundle on a
smooth surface is a divisorial condition (poles live in codimension 1;
the nodes and the points over double/triple points of the arrangement
are codimension >= 2).  The divisorial conditions:

  * along a branch line l_j (local model x_j^2 = l_j; adapted
    coordinates (f, v) with f = l_j, so dc = df - b dv):  writing
    eta = sum_k  a_k df^k dv^(m-k),  regularity of pi^* eta / x_j^eps
    (eps = 1 if j in S else 0) at the generic point of l_j is

        ord_{l_j}(a_k)  >=  ceil((eps - k)/2)          for all k,

    since df pulls back to 2w dw with f = w^2.  In particular poles of
    depth floor((m-eps)/2) are permitted in the df^m-direction, and for
    eps = 1 the restriction coefficient a_0 must VANISH on the line.
  * along every other divisor (u = 0 and the rest of the plane): eta is
    regular (pi is etale there).

Everything is exact linear algebra over Q.  Chart 1 is u = 1 with
coordinates (c, v), where all nine lines are affine:
l_(a,b) = c + a + b v, (a,b) in {-1,0,1}^2.  Chart 2 is c = 1 with
coordinates (y, z) = (u/c, v/c); it sees the line u = 0 (at y = 0),
which is chart 1's only invisible divisor; the missing point (0:0:1)
of the two-chart cover is codimension 2.  The chart-2 regularity
conditions are exact coefficient conditions in y.

Run:  python3 -m compute.descent_differentials [m]
"""

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb

GRID = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]


# ---------------------------------------------------------------------------
# polynomials in two variables as {(i, j): Fraction}, exact

def pzero():
    return {}


def padd(p, q, scale=1):
    out = dict(p)
    for k, val in q.items():
        out[k] = out.get(k, F(0)) + F(scale) * val
        if out[k] == 0:
            del out[k]
    return out


def pmul(p, q):
    out = {}
    for (i1, j1), v1 in p.items():
        for (i2, j2), v2 in q.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, F(0)) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


def pscale(p, c):
    c = F(c)
    return {k: v * c for k, v in p.items() if v * c != 0}


def pdeg(p):
    return max((i + j for (i, j) in p), default=-1)


# generic polynomials: coefficients are vectors over the unknowns.
# We represent a "linear polynomial" as {(i,j): row}, row = dict{unk: F}.

def lin_zero():
    return {}


def lin_add(P, Q, scale=1):
    out = {k: dict(r) for k, r in P.items()}
    s = F(scale)
    for k, row in Q.items():
        tgt = out.setdefault(k, {})
        for u, val in row.items():
            tgt[u] = tgt.get(u, F(0)) + s * val
            if tgt[u] == 0:
                del tgt[u]
        if not tgt:
            del out[k]
    return out


def lin_scale_poly(P, q):
    """Multiply a linear-polynomial P by a constant polynomial q."""
    out = {}
    for (i1, j1), row in P.items():
        for (i2, j2), v in q.items():
            k = (i1 + i2, j1 + j2)
            tgt = out.setdefault(k, {})
            for u, val in row.items():
                tgt[u] = tgt.get(u, F(0)) + val * v
    return {k: {u: v for u, v in r.items() if v != 0}
            for k, r in out.items() if any(v != 0 for v in r.values())}


def lin_subs_c(P, a, b):
    """Substitute c -> -a - b*v in a linear polynomial (variables (c, v));
    returns a linear polynomial in v alone (keys (0, j))."""
    out = {}
    for (i, j), row in P.items():
        # c^i v^j -> (-a - b v)^i v^j
        for t in range(i + 1):
            coef = F(comb(i, t)) * F(-a) ** (i - t) * F(-b) ** t
            if coef == 0:
                continue
            k = (0, j + t)
            tgt = out.setdefault(k, {})
            for u, val in row.items():
                tgt[u] = tgt.get(u, F(0)) + coef * val
    return {k: {u: v for u, v in r.items() if v != 0}
            for k, r in out.items() if any(v != 0 for v in r.values())}


def lin_dc(P):
    """d/dc of a linear polynomial."""
    out = {}
    for (i, j), row in P.items():
        if i == 0:
            continue
        out[(i - 1, j)] = {u: v * i for u, v in row.items()}
    return out


def lin_chart2(P, dtot):
    """N(c, v) -> y^dtot * N(1/y, z/y) as a polynomial in (y, z):
    monomial c^i v^j -> y^(dtot - i - j) z^j.  Requires dtot >= deg N."""
    out = {}
    for (i, j), row in P.items():
        k = (dtot - i - j, j)
        assert k[0] >= 0
        tgt = out.setdefault(k, {})
        for u, val in row.items():
            tgt[u] = tgt.get(u, F(0)) + val
    return {k: {u: v for u, v in r.items() if v != 0}
            for k, r in out.items() if any(v != 0 for v in r.values())}


# ---------------------------------------------------------------------------
# the eigenspace computation

def line_poly(a, b):
    """l = c + a + b v as a constant polynomial dict."""
    out = {}
    for k, v in (((1, 0), F(1)), ((0, 0), F(a)), ((0, 1), F(b))):
        if v != 0:
            out[k] = v
    return out


def eigenspace_dim(S, m, dN=None, return_basis=False, lines=None):
    """dim V_S for the character given by the subset S of GRID (|S| even),
    at symmetric degree m.  dN = numerator degree bound (auto if None;
    correctness requires saturation, checked by the caller)."""
    if lines is None:
        lines = GRID
    S = set(S)
    eps = {ab: (1 if ab in S else 0) for ab in lines}
    pj = {ab: (m - eps[ab]) // 2 for ab in lines}      # denominator power
    dD = sum(pj.values())
    if dN is None:
        dN = dD + m + 1
    # unknowns: coefficients of N_i (i = 0..m; N_i is the numerator of the
    # dc^i dv^(m-i)-coefficient), degrees <= dN
    monos = [(i, j) for i in range(dN + 1) for j in range(dN + 1 - i)]
    unknowns = [(i, mono) for i in range(m + 1) for mono in monos]
    uidx = {u: t for t, u in enumerate(unknowns)}
    N = []
    for i in range(m + 1):
        P = {}
        for mono in monos:
            P[mono] = {uidx[(i, mono)]: F(1)}
        N.append(P)

    rows = []

    def add_zero_rows(linpoly):
        for key, row in linpoly.items():
            if row:
                rows.append(row)

    # ---- per-line conditions (chart 1)
    for (a, b) in lines:
        e = eps[(a, b)]
        p = pj[(a, b)]
        # adapted combos: coefficient of df^k dv^(m-k) is
        #   Ntilde_k = sum_{i>=k} C(i,k) (-b)^(i-k) N_i
        for k in range(m + 1):
            t = p + ceil_div(e - k, 2)
            if t <= 0:
                continue
            Nt = lin_zero()
            for i in range(k, m + 1):
                Nt = lin_add(Nt, N[i], F(comb(i, k)) * F(-b) ** (i - k))
            # l^t | Nt: derivatives 0..t-1 vanish along c = -a - b v
            D = Nt
            for r_ord in range(t):
                add_zero_rows(lin_subs_c(D, a, b))
                D = lin_dc(D)

    # ---- chart-2 regularity along u = 0 (y = 0)
    # coefficient of dy^(m-t) dz^t is, up to sign and unit,
    #   y^(dD + dN - 2m + t) * Phi_t / Dtilde,
    #   Phi_t = sum_{i <= m-t} C(m-i, t) (-z)^(m-i-t) (-1)^i * Ntilde2_i
    # with Ntilde2_i = y^dN N_i(1/y, z/y);  condition: y^(K_t) | Phi_t
    # where K_t = max(0, 2m - t - dD + dN) ... wait: total y-power is
    #   -2m + t - (-dD) - dN ... assembled below explicitly.
    for t in range(m + 1):
        Phi = lin_zero()
        for i in range(0, m - t + 1):
            Ni2 = lin_chart2(N[i], dN)
            zpow = {(0, m - i - t): F(1)}
            term = lin_scale_poly(Ni2, zpow)
            Phi = lin_add(Phi, term,
                          F(comb(m - i, t)) * F(-1) ** (m - i - t)
                          * F(-1) ** i)
        # y-exponent of the coefficient: -2m + t + dD - dN  (from dc/dv
        # factors: y^{-2m} * y^t; numerator y^{-dN}; denominator y^{-dD})
        K = 2 * m - t - dD + dN
        if K <= 0:
            continue
        # need y^K | Phi: kill coefficients of y^0..y^(K-1)
        for (yi, zj), row in Phi.items():
            if yi < K and row:
                rows.append(row)

    dim, basis = nullspace_dim(rows, len(unknowns),
                               return_basis=return_basis)
    if return_basis:
        return dim, basis, unknowns, dN
    return dim


def ceil_div(a, b):
    return -((-a) // b)


def nullspace_dim(rows, nunk, return_basis=False):
    """Exact nullspace dimension (and basis if requested) of the sparse
    row system over Q."""
    # Gaussian elimination on sparse rows
    pivots = {}          # col -> reduced row (dict)
    for row in rows:
        row = dict(row)
        while row:
            col = min(row)
            if col in pivots:
                piv = pivots[col]
                fac = row[col] / piv[col]
                for cc, vv in piv.items():
                    row[cc] = row.get(cc, F(0)) - fac * vv
                    if row[cc] == 0:
                        del row[cc]
            else:
                pivots[col] = row
                break
    rank = len(pivots)
    dim = nunk - rank
    if not return_basis:
        return dim, None
    # back-substitute a basis
    pivcols = sorted(pivots)
    freecols = [cc for cc in range(nunk) if cc not in pivots]
    basis = []
    for fc in freecols:
        vec = [F(0)] * nunk
        vec[fc] = F(1)
        for col in reversed(pivcols):
            row = pivots[col]
            s = sum(row.get(cc, F(0)) * vec[cc]
                    for cc in row if cc != col)
            vec[col] = -s / row[col]
        basis.append(vec)
    return dim, basis


# ---------------------------------------------------------------------------
# symmetry: the grid symmetries (a,b) -> (±a, ±b), (b,a) act on characters

def grid_symmetries():
    syms = []
    for sa in (1, -1):
        for sb in (1, -1):
            for swap in (False, True):
                def f(ab, sa=sa, sb=sb, swap=swap):
                    a, b = ab
                    a, b = sa * a, sb * b
                    return (b, a) if swap else (a, b)
                syms.append(f)
    return syms


def character_orbits(sizes=(0, 2, 4, 6, 8)):
    """Orbits of even subsets of GRID under the 8 grid symmetries."""
    syms = grid_symmetries()
    seen, orbits = set(), []
    for size in sizes:
        for S in combinations(GRID, size):
            key = frozenset(S)
            if key in seen:
                continue
            orbit = {frozenset(f(ab) for ab in key) for f in syms}
            seen |= orbit
            orbits.append((key, len(orbit)))
    return orbits


# ---------------------------------------------------------------------------
# independent validator: brute-force local expansion of pi^* eta / x^S

def validate_solution(S, m, vec, unknowns, dN, lines=None):
    """Check regularity of the solution directly: along each line expand
    pi^* eta / x_j^eps in the double-cover coordinate w (f = w^2) and
    verify no negative powers; along u = 0 verify the chart-2
    coefficients are y-regular.  Independent of the row derivation."""
    if lines is None:
        lines = GRID
    S = set(S)
    # rebuild numerators
    Ns = []
    for i in range(m + 1):
        P = {}
        for t, (ii, mono) in enumerate(unknowns):
            if ii == i and vec[t] != 0:
                P[mono] = vec[t]
        Ns.append(P)
    pjs = {ab: (m - (1 if ab in S else 0)) // 2 for ab in lines}
    for (a, b) in lines:
        e = 1 if (a, b) in S else 0
        # adapted: eta * D_S = sum_k Ntilde_k df^k dv^(m-k)
        # local: f = w^2; denominator D_S = l^p * (unit near generic pt)
        # so eta-coefficient of df^k: Ntilde_k / (l^p unit);
        # pull back: contributes w^(k - 2p - e + 2 ord_l(Ntilde_k)) unit
        for k in range(m + 1):
            Nt = pzero()
            for i in range(k, m + 1):
                q = {mono: val * F(comb(i, k)) * F(-b) ** (i - k)
                     for mono, val in Ns[i].items()}
                Nt = padd(Nt, q)
            # ord_l(Nt): substitute c = f - a - b v, count min f-power
            ordl = _ord_along_line(Nt, a, b)
            if ordl is None:
                continue        # Nt == 0
            wexp = k - 2 * pjs[(a, b)] - e + 2 * ordl
            if wexp < 0:
                return False, f"pole along line {(a, b)} in df^{k}-part"
    # chart-2 side: recompute Phi_t y-orders
    dD = sum(pjs.values())
    for t in range(m + 1):
        Phi = pzero()
        for i in range(0, m - t + 1):
            Ni2 = {(dN - x - y2, y2): val for (x, y2), val in Ns[i].items()}
            term = {(k[0], k[1] + m - i - t): val * F(comb(m - i, t))
                    * F(-1) ** (m - i - t) * F(-1) ** i
                    for k, val in Ni2.items()}
            Phi = padd(Phi, term)
        K = 2 * m - t - dD + dN
        bad = [k for k in Phi if k[0] < K]
        if bad:
            return False, f"pole along u=0 in dz^{t}-part"
    return True, "regular"


def _ord_along_line(P, a, b):
    """min f-adic order of P(c -> f - a - b v) (None if P == 0)."""
    if not P:
        return None
    # expand c^i = (f + (-a - b v))^i: term C(i,t) f^t (-a - bv)^(i-t)
    out = {}
    for (i, j), val in P.items():
        for t in range(i + 1):
            for s in range(i - t + 1):
                cf = (val * F(comb(i, t)) * F(comb(i - t, s))
                      * F(-a) ** (i - t - s) * F(-b) ** s)
                if cf == 0:
                    continue
                key = (t, j + s)
                out[key] = out.get(key, F(0)) + cf
    out = {k: v for k, v in out.items() if v != 0}
    if not out:
        return None
    return min(k[0] for k in out)


# ---------------------------------------------------------------------------

def survey(m, sizes=(0, 2, 4, 6, 8), verbose=True, saturate=True):
    """dim V_S for one representative per character orbit; returns
    (total h^0, list of (representative, orbit size, dim)).  With
    saturate=True every dimension is recomputed at numerator degree
    bound +2 and required to agree (a too-small bound could only
    truncate the space, never enlarge it)."""
    out = []
    total = 0
    for key, orbsize in character_orbits(sizes):
        dD = sum((m - (1 if ab in key else 0)) // 2 for ab in GRID)
        d = eigenspace_dim(key, m)
        if saturate:
            d3 = eigenspace_dim(key, m, dN=dD + m + 3)
            assert d == d3, (f"degree bound not saturated at "
                             f"{sorted(key)}: {d} vs {d3}")
        out.append((sorted(key), orbsize, d))
        total += orbsize * d
        if verbose and d:
            print(f"  S = {sorted(key)} (orbit {orbsize}): dim = {d}")
    return total, out


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(f"== eigenspace survey at m = {m} ==")
    total, rows = survey(m)
    nchars = sum(o for _, o, _ in rows)
    print(f"characters covered: {nchars} (expect 256)")
    print(f"h^0(X - nodes, S^{m} Omega^1) = {total}")


if __name__ == "__main__":
    main()
