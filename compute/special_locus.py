"""The special-curve locus of X from the six m = 4 differentials (M11-D).

Since the whole space H^0(X - nodes, S^4 Omega^1) is Galois-INVARIANT
(Theorem A8.5), BTVA's resultant analysis descends to the Lucas plane:
if C is a complete genus-0 curve on X avoiding all 256 nodes, then
every omega_a = pi^*(eta_a) restricts to zero on C, hence every eta_a
restricts to zero on the plane image of C:

    THE IMAGE OF C IS A COMMON INTEGRAL CURVE OF THE ENTIRE
    SIX-DIMENSIONAL SYSTEM  {eta_1, ..., eta_6}.

(Images inside the branch locus need no differentials at all: every
entry line carries triple points of the arrangement, and the fibre of
pi over a triple point consists of nodes only — Lemma A8.6.)

At a point P off the arrangement, the tangent direction of an integral
curve must be a common projective root of the six binary quartics
F_a(P; dc, dv) = sum_k N_k^(a)(P) dc^k dv^(4-k)  (the shared
denominator D = prod l^2 cancels from the root condition).  Writing Z
for the set of P where such a common root exists (a closed subset:
image of an incidence variety in P^2 x P^1), this module:

  1. builds the six quartic direction-forms from the stored generators;
  2. certifies that Z is a PROPER closed subset — hence of dimension
     <= 1 — by an exact gcd computation at rational points;
  3. tests every catalogued special line by exact restriction:
     the nine entry lines lie in Z, while u = 0, v = 0 and the six
     distinctness lines are NOT integral curves (u = 0, invisible in
     the (c, v)-chart, is tested by the chart-2 slice formula of
     `restrict_u0`);
  4. certifies the curve part of Z mod p (Certificate A8.7): along
     exact generic rational lines, the gcd of all 15 pairwise
     resultants Res_(dc:dv)(F_a, F_b) is supported exactly on the nine
     entry-line crossings, with multiplicity 8 each — so mod p the
     curve components of Z are the nine entry lines and nothing else.

Run:  python3 -m compute.special_locus
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb

from compute.data_m4_generators import GENERATORS
from compute.descent_differentials import GRID

M = 4

# every numerator coefficient N_k of the stored generators has total
# degree <= 14 = dN - 9 (checked by `numerator_forms`); this bounds the
# restricted pair resultants by degree 8 x 14 = 112 and is exactly the
# regularity of eta along u = 0 in the top slot (see `restrict_u0`)
DEG_BOUND = 14


def numerator_forms():
    """The six direction-forms as lists [N_0, ..., N_4] of polynomial
    dicts {(i, j): Fraction}: F_a = sum_k N_k dc^k dv^(4-k)."""
    out = []
    for g in GENERATORS:
        Ns = []
        for k in range(M + 1):
            part = g.get(k, {})
            Ns.append({(int(a), int(b)): F(v)
                       for (a, b), v in part.items()})
        out.append(Ns)
    for Ns in out:
        for N in Ns:
            bad = [ij for ij, val in N.items()
                   if val and sum(ij) > DEG_BOUND]
            assert not bad, f"numerator degree > {DEG_BOUND}: {bad}"
    return out


def eval_poly(P, c, v):
    return sum(val * c ** i * v ** j for (i, j), val in P.items())


def quartic_at(Ns, c, v):
    """[F(dc^0 dv^4-coeff), ..., dc^4-coeff] at the point (c, v):
    ascending in dc."""
    return [eval_poly(Ns[k], c, v) for k in range(M + 1)]


def poly_gcd_1var(f, g):
    """gcd of univariate rational coefficient lists (ascending),
    normalized monic; [1] means coprime."""
    a, b = [F(x) for x in f], [F(x) for x in g]

    def deg(p):
        d = len(p) - 1
        while d >= 0 and p[d] == 0:
            d -= 1
        return d

    def rem(p, q):
        p = p[:]
        dq = deg(q)
        while deg(p) >= dq >= 0:
            dp = deg(p)
            fac = p[dp] / q[dq]
            for i in range(dq + 1):
                p[dp - dq + i] -= fac * q[i]
            p[dp] = F(0)
        return p

    while deg(b) >= 0:
        a, b = b, rem(a, b)
    d = deg(a)
    if d < 0:
        return [F(0)]
    return [x / a[d] for x in a[:d + 1]]


def common_direction_gcd(pt):
    """gcd of the six binary quartics at the rational point pt = (c, v);
    degree 0 (gcd [1]) means NO common direction at pt, certifying that
    the common-root locus Z is a proper closed subset."""
    forms = [quartic_at(Ns, F(pt[0]), F(pt[1]))
             for Ns in numerator_forms()]
    g = forms[0]
    for f in forms[1:]:
        g = poly_gcd_1var(g, f)
        if len(g) == 1 and g[0] != 0:
            break
    return g


# ---------------------------------------------------------------------------
# exact restriction tests on catalogued candidate curves

def restrict_line(Ns, p0, dirv):
    """Restriction of eta (numerator form) to the line p0 + t*dirv:
    the coefficient function g(t) of dt^4, as an ascending list.
    eta restricted = sum_k N_k(c(t), v(t)) c'(t)^k v'(t)^(4-k) dt^4."""
    (c0, v0), (dc, dv) = p0, dirv
    res = [F(0)]
    for k in range(M + 1):
        scal = F(dc) ** k * F(dv) ** (M - k)
        if scal == 0:
            continue
        # N_k(c0 + t dc, v0 + t dv) as ascending t-list
        acc = {}
        for (i, j), val in Ns[k].items():
            # (c0 + t dc)^i (v0 + t dv)^j
            for a in range(i + 1):
                for b in range(j + 1):
                    coef = (val * comb(i, a) * F(c0) ** (i - a)
                            * F(dc) ** a * comb(j, b) * F(v0) ** (j - b)
                            * F(dv) ** b)
                    if coef:
                        acc[a + b] = acc.get(a + b, F(0)) + coef
        deg = max(acc, default=0)
        lst = [acc.get(t, F(0)) * scal for t in range(deg + 1)]
        if len(lst) > len(res):
            res += [F(0)] * (len(lst) - len(res))
        for t, x in enumerate(lst):
            res[t] += x
    return res


def restrict_u0(Ns):
    """Restriction of eta = (sum_k N_k dc^k dv^(4-k)) / prod l^2 to the
    line u = 0, which the (c, v)-chart cannot see.  In the chart c = 1
    with coordinates (y, z) = (u/c, v/c) one has c = 1/y, v = z/y, so
    dc = -dy/y^2 and dv = (y dz - z dy)/y^2; with the dN = 23
    homogenizations Nk~(y, z) = y^23 N_k(1/y, z/y) and D~ = y^18 D =
    prod (1 + a y + b z)^2 this reads

        eta = y^(-13) sum_k (-1)^k Nk~ dy^k (y dz - z dy)^(4-k) / D~ .

    The dz^4-component is y^(-9) N0~ / D~.  X -> P^2 is etale over
    u = 0 away from the three B-triple-points, so eta is REGULAR along
    u = 0: y^9 | N0~, i.e. deg N_0 <= 14 (asserted globally in
    `numerator_forms`).  Pulling back to {y = 0} (set dy = 0) leaves

        eta|_(u=0) = ([y^9] N0~)(z) dz^4 / D~(0, z),
        D~(0, z) = (1 - z^2)^6 != 0 generically,

    so u = 0 is integral iff the total-degree-14 part of N_0 vanishes.
    Returns that part as the ascending z-list [N_0[(14-j, j)]]_j.
    (Cross-check: the transpose symmetry (c:u:v) -> (c:v:u) preserves
    the invariant 6-space and swaps u = 0 with v = 0, so the two lines
    must agree on integrality.)"""
    N0 = Ns[0]
    return [N0.get((DEG_BOUND - j, j), F(0)) for j in range(DEG_BOUND + 1)]


def restrict_param(Ns, cpoly, vpoly):
    """Restriction of eta to the parametrized curve c = cpoly(t),
    v = vpoly(t) (ascending coefficient lists): coefficient of dt^4."""
    def d(p):
        return [i * p[i] for i in range(1, len(p))] or [F(0)]

    def mul(p, q):
        out = [F(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                out[i + j] += a * b
        return out

    def power(p, n):
        out = [F(1)]
        for _ in range(n):
            out = mul(out, p)
        return out

    def peval2(P, cp, vp):
        # P(cpoly(t), vpoly(t)) via Horner-ish expansion
        out = [F(0)]
        for (i, j), val in P.items():
            term = mul(power(cp, i), power(vp, j))
            term = [val * x for x in term]
            if len(term) > len(out):
                out += [F(0)] * (len(term) - len(out))
            for t, x in enumerate(term):
                out[t] += x
        return out

    cp = [F(x) for x in cpoly]
    vp = [F(x) for x in vpoly]
    cd, vd = d(cp), d(vp)
    res = [F(0)]
    for k in range(M + 1):
        term = mul(peval2(Ns[k], cp, vp),
                   mul(power(cd, k), power(vd, M - k)))
        if len(term) > len(res):
            res += [F(0)] * (len(term) - len(res))
        for t, x in enumerate(term):
            res[t] += x
    return res


def is_zero(lst):
    return all(x == 0 for x in lst)


def catalogue_tests():
    """Exact tests of every catalogued special line against the full
    6-system.  Two distinct semantics, labelled accordingly:

    * entry lines (the poles of the eta_a): vanishing of the restricted
      NUMERATOR form means the line's own direction is a common root of
      the six direction-quartics along it — the line lies inside Z
      (this is NOT integrality of eta, which has poles there);
    * non-branch lines (eta_a regular there): honest integrality — the
      restriction of eta_a itself vanishes identically.

    Note l_(0,0) is the central line c = 0, so "c = 0" needs no
    separate test; conic images need no tests at all (Theorem A7.6
    excludes genus <= 1 curves over every conic).  Returns
    {label: bool}."""
    forms = numerator_forms()
    tests = {}
    # the nine entry lines c + a + b v = 0 (chart u = 1)
    for (a, b) in GRID:
        tests[f"entry {(a, b)} in Z"] = all(
            is_zero(restrict_line(Ns, (F(-a), F(0)), (F(-b), F(1))))
            for Ns in forms)
    # the two pencil carriers: v = 0 (A-points) and u = 0 (B-points)
    tests["v=0 integral"] = all(
        is_zero(restrict_line(Ns, (F(0), F(0)), (F(1), F(0))))
        for Ns in forms)
    tests["u=0 integral"] = all(is_zero(restrict_u0(Ns))
                                for Ns in forms)
    # the six distinctness lines u = +-v, u = +-2v, 2u = +-v: in the
    # chart u = 1 these are the horizontal lines v = k
    for k in (F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2)):
        tests[f"v={k} integral"] = all(
            is_zero(restrict_line(Ns, (F(0), k), (F(1), F(0))))
            for Ns in forms)
    return tests


# ---------------------------------------------------------------------------
# Certificate A8.7: the curve part of Z, mod p
#
# Along a line L(t) generic for the arrangement, every point of Z on L
# is a common zero of the 15 pairwise resultants R_ab(t) =
# Res_(dc:dv)(F_a|_L, F_b|_L), hence a root of g_L = gcd_ab(R_ab|_L).
# A curve component of Z other than an entry line would meet L in a
# point NOT on the arrangement (for L generic), producing a root of g_L
# away from the nine entry-line crossings.  The scan computes g_L mod p
# and finds: deg g_L = 72 with the nine crossings of multiplicity
# exactly 8 each — nothing else.  (The entry lines DO lie in Z, whence
# the 9 x 8 = 72; the certificate is that they account for ALL of g_L.)

TEST_LINES = (
    # exact rational (p0, dir); each is certified generic on the fly:
    # its nine entry-line crossings are pairwise distinct rationals
    ((F(1, 3), F(2, 7)), (F(1), F(5, 11))),
    ((F(-2, 5), F(3)), (F(1), F(-7, 3))),
    ((F(7, 2), F(-1, 9)), (F(1), F(13, 4))),
)
SCAN_PRIMES = (999999937, 1000003919)
NPTS = 140  # > 112 = 8 x DEG_BOUND >= deg R_ab, with margin


def _frac_mod(x, p):
    x = F(x)
    assert x.denominator % p != 0
    return x.numerator * pow(x.denominator, p - 2, p) % p


def _compose_line(poly, p0, dirv):
    """{(i,j): Fraction} -> exact ascending t-list of
    poly(c0 + t dc, v0 + t dv), via incremental power tables."""
    (c0, v0), (dc, dv) = [F(x) for x in p0], [F(x) for x in dirv]
    deg = max((i + j for (i, j), val in poly.items() if val), default=0)

    def powers(x0, dx):
        tab = [[F(1)]]
        for _ in range(deg):
            last = tab[-1]
            new = [x0 * x for x in last] + [F(0)]
            for i, x in enumerate(last):
                new[i + 1] += dx * x
            tab.append(new)
        return tab

    cp, vp = powers(c0, dc), powers(v0, dv)
    out = [F(0)] * (deg + 1)
    for (i, j), val in poly.items():
        if not val:
            continue
        for a, x in enumerate(cp[i]):
            if x:
                for b, y in enumerate(vp[j]):
                    if y:
                        out[a + b] += val * x * y
    return out


def _det_mod(mat, p):
    m = [row[:] for row in mat]
    n = len(m)
    det = 1
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col]), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det % p
        det = det * m[col][col] % p
        inv = pow(m[col][col], p - 2, p)
        for r in range(col + 1, n):
            if m[r][col]:
                f = m[r][col] * inv % p
                for cc in range(col, n):
                    m[r][cc] = (m[r][cc] - f * m[col][cc]) % p
    return det


def _res44_mod(f, g, p):
    """Resultant of two binary quartic FORMS (ascending coefficient
    lists in dc), via the 8x8 Sylvester determinant.  Valid without any
    nonvanishing hypothesis on leading coefficients: it is the
    universal Res_(4,4) polynomial in the coefficients, and vanishes
    exactly when the forms share a projective root (or both drop
    degree, i.e. share the root at infinity)."""
    A = f[::-1]
    B = g[::-1]
    rows = [[0] * s + A + [0] * (3 - s) for s in range(4)]
    rows += [[0] * s + B + [0] * (3 - s) for s in range(4)]
    return _det_mod(rows, p)


def _interp_mod(xs, ys, p):
    """Newton interpolation through (xs[i], ys[i]) mod p; ascending
    coefficient list, trailing zeros trimmed."""
    n = len(xs)
    coef = ys[:]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) * pow(
                (xs[i] - xs[i - j]) % p, p - 2, p) % p
    poly = [coef[n - 1]]
    for k in range(n - 2, -1, -1):
        # poly <- poly * (t - xs[k]) + coef[k]
        new = [0] * (len(poly) + 1)
        for i, x in enumerate(poly):
            new[i + 1] = (new[i + 1] + x) % p
            new[i] = (new[i] - x * xs[k]) % p
        new[0] = (new[0] + coef[k]) % p
        poly = new
    return _trim(poly)


def _trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _pmod(a, b, p):
    a = _trim(a[:])
    while a != [0] and len(a) >= len(b):
        f = a[-1] * pow(b[-1], p - 2, p) % p
        off = len(a) - len(b)
        for i in range(len(b)):
            a[off + i] = (a[off + i] - f * b[i]) % p
        _trim(a)
    return a


def _gcd_mod(a, b, p):
    a, b = _trim(a[:]), _trim(b[:])
    while b != [0]:
        a, b = b, _pmod(a, b, p)
    if a != [0]:
        inv = pow(a[-1], p - 2, p)
        a = [x * inv % p for x in a]
    return a


def _div_root(poly, r, p):
    """Synthetic division: poly = (t - r) quot + rem."""
    quot = [0] * (len(poly) - 1)
    acc = 0
    for i in range(len(poly) - 1, 0, -1):
        acc = (acc * r + poly[i]) % p
        quot[i - 1] = acc
    rem = (acc * r + poly[0]) % p
    return quot, rem


def line_crossings(p0, dirv):
    """The nine exact parameters where p0 + t dir crosses the entry
    lines, {(a, b): t}; asserts they are pairwise distinct and finite
    (= the line avoids all multiple points of the arrangement and is
    parallel to no entry line: an exact genericity certificate)."""
    (c0, v0), (dc, dv) = [F(x) for x in p0], [F(x) for x in dirv]
    cross = {}
    for (a, b) in GRID:
        den = dc + b * dv
        assert den != 0, f"test line parallel to entry {(a, b)}"
        cross[(a, b)] = -(c0 + a + b * v0) / den
    assert len(set(cross.values())) == 9, "crossings collide"
    return cross


def zscan_line(p0, dirv, prime, npts=NPTS):
    """One line, one prime: interpolate the 15 pairwise resultants
    restricted to the line, gcd them, and factor the gcd against the
    nine entry-line crossings.  Returns {pair_degs, gcd_deg, mults,
    extra_deg}."""
    forms = numerator_forms()
    coeffs = [[[_frac_mod(x, prime)
                for x in _compose_line(Ns[k], p0, dirv)]
               for k in range(M + 1)] for Ns in forms]
    xs = list(range(1, npts + 1))

    def ev(poly, x):
        acc = 0
        for c in reversed(poly):
            acc = (acc * x + c) % prime
        return acc

    evals = [[[ev(coeffs[a][k], x) for k in range(M + 1)] for x in xs]
             for a in range(6)]
    pair_degs, g = [], None
    for a, b in combinations(range(6), 2):
        ys = [_res44_mod(evals[a][i], evals[b][i], prime)
              for i in range(npts)]
        R = _interp_mod(xs, ys, prime)
        assert R != [0], f"pair ({a},{b}) resultant identically 0"
        assert len(R) - 1 <= 8 * DEG_BOUND, "degree bound violated"
        pair_degs.append(len(R) - 1)
        g = R if g is None else _gcd_mod(g, R, prime)
    mults = {}
    for (ab, t) in line_crossings(p0, dirv).items():
        r, m = _frac_mod(t, prime), 0
        while True:
            quot, rem = _div_root(g, r, prime)
            if rem != 0 or not quot:
                break
            g, m = quot, m + 1
        mults[ab] = m
    return {"pair_degs": (min(pair_degs), max(pair_degs)),
            "gcd_deg": sum(mults.values()) + len(_trim(g)) - 1,
            "mults": mults, "extra_deg": len(_trim(g)) - 1}


def z_certificate(lines=TEST_LINES, primes=SCAN_PRIMES, npts=NPTS):
    """Certificate A8.7: every line/prime scan must give gcd degree
    72 = 9 crossings x multiplicity 8 with NO extra roots."""
    runs, ok = {}, True
    for li, (p0, dirv) in enumerate(lines):
        for p in primes:
            r = zscan_line(p0, dirv, p, npts)
            runs[f"L{li + 1}@{p}"] = r
            ok &= (r["gcd_deg"] == 72 and r["extra_deg"] == 0
                   and sorted(r["mults"].values()) == [8] * 9)
    return {"ok": ok, "runs": runs}


def main():
    g = common_direction_gcd((F(2), F(5, 7)))
    print("gcd of the six quartics at a generic point:",
          "trivial (Z is PROPER)" if len(g) == 1 else g)
    for pt in ((F(1, 3), F(9)), (F(-4), F(11, 5))):
        gg = common_direction_gcd(pt)
        print(f"  at {pt}: gcd degree {len(gg) - 1}")
    print("catalogue (exact):")
    for name, val in catalogue_tests().items():
        print(f"  {name}: {val}")
    print("Z-scan certificate (3 lines x 2 primes, 15 pairs each):")
    cert = z_certificate()
    for key, r in cert["runs"].items():
        print(f"  {key}: pair degs {r['pair_degs']}, "
              f"gcd deg {r['gcd_deg']} = "
              f"{sorted(set(r['mults'].values()))} x 9 crossings "
              f"+ extra {r['extra_deg']}")
    print("CERTIFIED mod p: curve part of Z = the nine entry lines"
          if cert["ok"] else "STRUCTURE CHANGED — investigate!")


if __name__ == "__main__":
    main()
