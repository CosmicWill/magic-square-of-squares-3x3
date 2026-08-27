"""The node-extension layer (M11-F): behavior of the six m = 4
differentials along the 256 exceptional (-2)-curves.

Local model.  Every one of the 8 triple points of the arrangement is
the base of a 3-term arithmetic progression of lines: its pencil
{l_A, l_B, l_C} satisfies l_A + l_C = 2 l_B (rows, columns and
diagonals of the grid are APs).  The local (Z/2)^3 subcover is
therefore always the SAME cone

    z_3^2 = (z_1^2 + z_2^2)/2,   z_1^2 = l_A, z_2^2 = l_C,

with the rational parametrization (the smooth double cover C^2_(s,t))

    q_1 = s^2 + 2st - t^2,  q_2 = -s^2 + 2st + t^2,  q_3 = s^2 + t^2,
    q_1^2 + q_2^2 = 2 q_3^2   (identity),

and the residual (Z/2)^5 acts freely (32 nodes per triple point).
An invariant S^4-differential germ omega on C^2_(s,t) \\ 0 extends
over 0 (Hartogs) and has even coefficient orders; writing tau(omega)
for the minimal coefficient order, the resolution chart
(xi, w) = (s^2, t/s) gives the component bounds

    ord_xi(B_j) >= ceil((tau + 4 - 2j)/2)   (dxi^j dw^(4-j)-part),

so omega extends across the exceptional curve E iff tau >= 4, and in
general has pole order <= 2 - tau/2 along E (tau even, >= 0 by
regularity).

For eta in the 6-space, tau at a node over the triple point P is
computed EXACTLY: substitute the local coordinates (l_A, l_C) =
(q_1^2, q_2^2) into the numerator differential and read off the
minimal (s,t)-order of its components minus ord(denominator) = 24
(= 4 x deg (l_A l_B l_C)^2; the other six lines are units at P).

Results (all exact, re-verified by `a8.node_tau` etc.):

  * at every one of the 8 triple points the filtration is
        dim V_(tau>=0) = 6,  V_(tau>=2) = V_(tau>=4) = 4,
        V_(tau>=6) = 0:
    a 4-dimensional subspace extends over the 32 nodes there, the
    rest have pole order exactly 2;
  * the intersection of all eight extension subspaces is
    ONE-dimensional, spanned by eta_4 — and since restriction to
    X - nodes is injective on H^0(Ytilde, S^4 Omega^1),

        h^0(Ytilde, S^4 Omega^1) = 1        (Ytilde = the resolution)

    — the resolution itself carries a (unique) symmetric quartic
    differential, at m = 4 against BTVA's resolution-level guarantee
    m >= 47.  Every rational curve on Ytilde not inside the
    exceptional locus is an integral curve of eta* := eta_4; the
    classical AP families comply: u = 0 and v = 0 are eta*-integral
    (and are NOT integral for the full 6-space).
  * the 6-space is a D4-representation (grid symmetries); eta* spans
    an invariant line.

Run:  python3 -m compute.node_extension
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb

from compute.descent_differentials import GRID
from compute.special_locus import (is_zero, numerator_forms,
                                   restrict_line, restrict_u0)

M = 4
DENOM_ORD = 24  # ord_(s,t) of (l_A l_B l_C)^2 pulled back: 3 x 2 x 4

# ---------------------------------------------------------------------------
# small exact bivariate-dict helpers  {(i, j): Fraction}


def padd(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
        if not out[k]:
            del out[k]
    return out


def pscal(p, c):
    return {k: c * v for k, v in p.items()} if c else {}


def pmul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i + k, j + l)
            out[ij] = out.get(ij, F(0)) + a * b
    return {k: v for k, v in out.items() if v}


def psub(poly, cx, cy):
    """poly(c, v) with c -> cx, v -> cy (cx, cy poly dicts)."""
    mi = max((i for (i, _) in poly), default=0)
    mj = max((j for (_, j) in poly), default=0)
    xp = [{(0, 0): F(1)}]
    for _ in range(mi):
        xp.append(pmul(xp[-1], cx))
    yp = [{(0, 0): F(1)}]
    for _ in range(mj):
        yp.append(pmul(yp[-1], cy))
    out = {}
    for (i, j), val in poly.items():
        out = padd(out, pscal(pmul(xp[i], yp[j]), val))
    return out


def dpoly(p):
    ds, dt = {}, {}
    for (i, j), v in p.items():
        if i:
            ds[(i - 1, j)] = ds.get((i - 1, j), F(0)) + i * v
        if j:
            dt[(i, j - 1)] = dt.get((i, j - 1), F(0)) + j * v
    return ds, dt


def ordmin(p):
    return min((i + j for (i, j) in p), default=None)


# ---------------------------------------------------------------------------
# the eight triple points; five are visible in the chart u = 1, the
# three B's (on u = 0) are handled through the transpose symmetry

VISIBLE = {
    # tag: (chart point (c, v), pencil [(a,b)] ordered outer/mid/outer)
    "A0": ((F(0), F(0)), [(0, -1), (0, 0), (0, 1)]),      # col a = 0
    "A+": ((F(-1), F(0)), [(1, -1), (1, 0), (1, 1)]),     # col a = 1
    "A-": ((F(1), F(0)), [(-1, -1), (-1, 0), (-1, 1)]),   # col a = -1
    "D+": ((F(0), F(-1)), [(-1, -1), (0, 0), (1, 1)]),    # diag a = b
    "D-": ((F(0), F(1)), [(-1, 1), (0, 0), (1, -1)]),     # diag a = -b
}
SIGMA_PAIRS = (("B0", "A0"), ("B+", "A+"), ("B-", "A-"))
ALL_TAGS = ("A0", "A+", "A-", "B0", "B+", "B-", "D+", "D-")

Q1 = {(2, 0): F(1), (1, 1): F(2), (0, 2): F(-1)}
Q2 = {(2, 0): F(-1), (1, 1): F(2), (0, 2): F(1)}
Q3 = {(2, 0): F(1), (0, 2): F(1)}
assert padd(pmul(Q1, Q1), pmul(Q2, Q2)) == pscal(pmul(Q3, Q3), F(2))


def local_pullback(Ns, tag):
    """The numerator S^4-differential of eta (5 numerator dicts Ns in
    chart-u coordinates) pulled back through l_A = q_1^2, l_C = q_2^2
    at the visible triple point `tag`; returns 5 exact (s,t)-poly
    dicts, indexed by the power of dt."""
    (c0, v0), lines = VISIBLE[tag]
    (aA, bA), (aB, bB), (aC, bC) = lines
    assert c0 + aA + bA * v0 == 0 and c0 + aC + bC * v0 == 0
    QA, QC = pmul(Q1, Q1), pmul(Q2, Q2)
    # l_A = c + aA + bA v, l_C = c + aC + bC v  =>  local solve
    vloc = pscal(padd(QC, pscal(QA, F(-1))), F(1) / (bC - bA))
    cpoly = padd(padd(QA, pscal(vloc, -bA)), {(0, 0): c0})
    vpoly = padd(vloc, {(0, 0): v0})
    # the middle line must pull back to q_3^2 (the AP identity)
    lB = padd(padd(cpoly, {(0, 0): F(aB)}), pscal(vpoly, F(bB)))
    assert lB == pmul(Q3, Q3), "AP pencil structure broken"
    dc = dpoly(cpoly)
    dv = dpoly(vpoly)

    def form_mul(f, g):
        out = [{} for _ in range(len(f) + len(g) - 1)]
        for i, a in enumerate(f):
            for j, b in enumerate(g):
                out[i + j] = padd(out[i + j], pmul(a, b))
        return out

    def form_pow(f, n):
        out = [{(0, 0): F(1)}]
        for _ in range(n):
            out = form_mul(out, list(f))
        return out

    total = [{} for _ in range(M + 1)]
    for k in range(M + 1):
        piece = form_mul(form_pow(dc, k), form_pow(dv, M - k))
        comp = psub(Ns[k], cpoly, vpoly)
        for i in range(M + 1):
            total[i] = padd(total[i], pmul(comp, piece[i]))
    return total


def tau_of(Ns, tag):
    """tau of eta at (each of the 32 nodes over) the triple point;
    asserts parity and regularity."""
    P = local_pullback(Ns, tag)
    assert any(P), "identically zero pullback?!"
    assert not any((i + j) % 2 for c in P for (i, j) in c), "odd terms"
    tau = min(ordmin(c) for c in P if c) - DENOM_ORD
    assert tau >= 0, f"regularity violated at {tag}: tau = {tau}"
    return tau


# ---------------------------------------------------------------------------
# exact linear algebra over Q (RREF, nullspace of row lists)


def _rref(rows, ncols):
    aug = [row[:] for row in rows]
    piv_cols, rank = [], 0
    for col in range(ncols):
        piv = next((r for r in range(rank, len(aug))
                    if aug[r][col] != 0), None)
        if piv is None:
            continue
        aug[rank], aug[piv] = aug[piv], aug[rank]
        pv = aug[rank][col]
        aug[rank] = [x / pv for x in aug[rank]]
        for r in range(len(aug)):
            if r != rank and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[rank])]
        piv_cols.append(col)
        rank += 1
    return aug, piv_cols, rank


def nullspace(rows, ncols=6):
    aug, piv_cols, rank = _rref(rows, ncols)
    basis = []
    for fc in (c for c in range(ncols) if c not in piv_cols):
        v = [F(0)] * ncols
        v[fc] = F(1)
        for r, pc in enumerate(piv_cols):
            v[pc] = -aug[r][fc]
        basis.append(v)
    return basis


def filtration(tag, forms=None, upto=8):
    """{w: dim V_(tau >= w)} at a visible triple point, plus the basis
    of V_(tau >= 4) in generator coordinates."""
    forms = forms or numerator_forms()
    pulls = [local_pullback(Ns, tag) for Ns in forms]
    dims, basis4 = {}, None
    for w in range(0, upto + 1, 2):
        rows = {}
        for gi, P in enumerate(pulls):
            for ci, c in enumerate(P):
                for (i, j), v in c.items():
                    if i + j < DENOM_ORD + w:
                        key = (ci, i, j)
                        rows.setdefault(key, [F(0)] * 6)[gi] = v
        ns = nullspace(list(rows.values()))
        dims[w] = len(ns)
        if w == 4:
            basis4 = ns
    return dims, basis4


# ---------------------------------------------------------------------------
# the grid symmetry representation on the 6-space

def _solve_in_span(target, basis_forms):
    keys = set()
    for comp in range(M + 1):
        for B in basis_forms:
            keys |= {(comp, ij) for ij in B[comp]}
        keys |= {(comp, ij) for ij in target[comp]}
    rows, rhs = [], []
    for (comp, ij) in sorted(keys):
        rows.append([B[comp].get(ij, F(0)) for B in basis_forms])
        rhs.append(target[comp].get(ij, F(0)))
    aug = [row + [r] for row, r in zip(rows, rhs)]
    red, piv_cols, rank = _rref(aug, 6)
    for r in range(rank, len(red)):
        assert all(x == 0 for x in red[r]), "not in the 6-space!"
    x = [F(0)] * 6
    for r, col in enumerate(piv_cols):
        x[col] = red[r][6]
    return x


def sigma_numerators(Ns):
    """Transpose (c:u:v) -> (c:v:u): on the chart, (c, v) ->
    (c/v, 1/v); sigma* eta has numerators
    v^-4 [sum_k (-1)^(4-k) Ntilde_k (v dc - c dv)^k dv^(4-k)]
    over the same denominator (the lines are permuted (a,b) ->
    (b,a)), with Ntilde_k(c,v) = v^14 N_k(c/v, 1/v).  Requires (and
    asserts) v^4 | bracket, i.e. membership in the space."""
    out = [dict() for _ in range(M + 1)]
    for k in range(M + 1):
        Nt = {}
        for (i, j), val in Ns[k].items():
            key = (i, 14 - i - j)
            Nt[key] = Nt.get(key, F(0)) + val
        for r in range(k + 1):
            term = pmul(Nt, {(k - r, r): F(comb(k, r) * (-1) ** (k - r))})
            out[r] = padd(out[r], pscal(term, F((-1) ** (M - k))))
    res = []
    for compo in out:
        assert all(j >= 4 for (_, j) in compo), "v^4 does not divide"
        res.append({(i, j - 4): v for (i, j), v in compo.items()})
    return res


def flip_numerators(Ns, sc, sv):
    """(c, v) -> (sc*c, sv*v) with sc, sv in {1, -1}: the grid
    symmetries (a,b) -> (-a,-b) [(c,v) -> (-c,v)] ... realized here as
    the two chart substitutions (c,v) -> (sc c, sv v)."""
    res = []
    for k in range(M + 1):
        d = {(i, j): v * sc ** i * sv ** j * sc ** k * sv ** (M - k)
             for (i, j), v in Ns[k].items()}
        res.append({ij: v for ij, v in d.items() if v})
    return res


def rep_matrix(transform):
    """Matrix of eta_a -> transform(eta_a) in the generator basis:
    row a holds the coordinates of the transformed eta_a."""
    forms = numerator_forms()
    return [_solve_in_span(transform(Ns), forms) for Ns in forms]


def rep_matrices():
    """The three generating grid involutions: sigma (transpose),
    r: v -> -v (i.e. (a,b) -> (a,-b)), s: (c,v) -> (-c,-v) (i.e.
    (a,b) -> (-a,b))."""
    return {
        "sigma": rep_matrix(sigma_numerators),
        "r": rep_matrix(lambda Ns: flip_numerators(Ns, 1, -1)),
        "s": rep_matrix(lambda Ns: flip_numerators(Ns, -1, -1)),
    }


def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def is_identity(A):
    return all(A[i][j] == (1 if i == j else 0)
               for i in range(len(A)) for j in range(len(A)))


# ---------------------------------------------------------------------------
# extension subspaces at all 8 points, intersections, the W-space

def annihilator(basis, ncols=6):
    return nullspace([b[:] for b in basis], ncols)


def extension_spaces():
    """{tag: basis of V_(tau>=4)(tag)} for all 8 triple points; the
    B-points via the transpose: V(B) = {x : M_sigma^T x in V(A)}."""
    forms = numerator_forms()
    Ms = rep_matrix(sigma_numerators)
    spaces = {}
    for tag in VISIBLE:
        _, b4 = filtration(tag, forms)
        spaces[tag] = b4
    for btag, atag in SIGMA_PAIRS:
        rows = []
        for row in annihilator(spaces[atag]):
            rows.append([sum(Ms[a][b] * row[b] for b in range(6))
                         for a in range(6)])
        spaces[btag] = nullspace(rows)
    return spaces


def intersect(spaces, tags):
    rows = []
    for t in tags:
        rows += annihilator(spaces[t])
    return nullspace(rows)


def wstar_vector(spaces=None):
    """The generator of W = the intersection of all eight extension
    subspaces, certified DIRECTLY: tau = 4 at the five visible points
    for omega*, and for sigma* omega* (covering the three B-points).
    Returns integer, content-free coordinates."""
    from math import gcd
    spaces = spaces or extension_spaces()
    W = intersect(spaces, ALL_TAGS)
    assert len(W) == 1, f"dim W = {len(W)} != 1"
    den = 1
    for x in W[0]:
        den = den * x.denominator // gcd(den, x.denominator)
    w = [int(x * den) for x in W[0]]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    w = [x // g for x in w]
    if next(x for x in w if x) < 0:
        w = [-x for x in w]
    # direct certification, independent of the lattice algebra
    forms = numerator_forms()
    Wn = [dict() for _ in range(M + 1)]
    for a, Ns in enumerate(forms):
        for k in range(M + 1):
            for ij, v in Ns[k].items():
                Wn[k][ij] = Wn[k].get(ij, F(0)) + w[a] * v
    Wn = [{ij: v for ij, v in c.items() if v} for c in Wn]
    for tag in VISIBLE:
        assert tau_of(Wn, tag) >= 4, f"omega* fails to extend at {tag}"
    sWn = sigma_numerators(Wn)
    for tag in VISIBLE:
        assert tau_of(sWn, tag) >= 4, f"sigma*omega* fails at {tag}"
    # the AP-family consistency: u=0 and v=0 must be omega*-integral
    assert is_zero(restrict_line(Wn, (F(0), F(0)), (F(1), F(0)))), \
        "v = 0 not integral for omega* — theory broken!"
    assert is_zero(restrict_u0(Wn)), \
        "u = 0 not integral for omega* — theory broken!"
    return w, Wn


# ---------------------------------------------------------------------------
# arbitrary symmetric degree m (M11-K): the same local calculus with
# denominator order 12*floor(m/2) (pole depth floor(m/2) on the three
# pencil lines, each pulling back with order 4), parity tau == m mod 2,
# and extension across E iff tau >= m (chart bound ord_xi(B_j) >=
# ceil((tau + m - 2j)/2), worst j = m).  Trivial character only: the
# germ is honestly invariant there.


def local_pullback_m(Ns, tag, m):
    """As `local_pullback` for a degree-m invariant differential with
    numerators Ns (m+1 dicts, chart u = 1, denominator
    prod l^floor(m/2))."""
    (c0, v0), lines = VISIBLE[tag]
    (aA, bA), (aB, bB), (aC, bC) = lines
    assert c0 + aA + bA * v0 == 0 and c0 + aC + bC * v0 == 0
    QA, QC = pmul(Q1, Q1), pmul(Q2, Q2)
    vloc = pscal(padd(QC, pscal(QA, F(-1))), F(1) / (bC - bA))
    cpoly = padd(padd(QA, pscal(vloc, -bA)), {(0, 0): c0})
    vpoly = padd(vloc, {(0, 0): v0})
    lB = padd(padd(cpoly, {(0, 0): F(aB)}), pscal(vpoly, F(bB)))
    assert lB == pmul(Q3, Q3)
    dc = dpoly(cpoly)
    dv = dpoly(vpoly)

    def form_mul(f, g):
        out = [{} for _ in range(len(f) + len(g) - 1)]
        for i, a in enumerate(f):
            for j, b in enumerate(g):
                out[i + j] = padd(out[i + j], pmul(a, b))
        return out

    def form_pow(f, n):
        out = [{(0, 0): F(1)}]
        for _ in range(n):
            out = form_mul(out, list(f))
        return out

    total = [{} for _ in range(m + 1)]
    for k in range(m + 1):
        piece = form_mul(form_pow(dc, k), form_pow(dv, m - k))
        comp = psub(Ns[k], cpoly, vpoly)
        for i in range(m + 1):
            total[i] = padd(total[i], pmul(comp, piece[i]))
    return total


def tau_of_m(Ns, tag, m):
    """tau at the triple point `tag` for a degree-m invariant
    differential; asserts parity (tau == m mod 2 via even/odd
    coefficient orders) and regularity (tau >= 0)."""
    P = local_pullback_m(Ns, tag, m)
    assert any(P), "identically zero pullback"
    par = m % 2
    assert not any((i + j) % 2 != par
                   for c in P for (i, j), v in c.items() if v), \
        "parity violated"
    tau = min(ordmin(c) for c in P if c) - 12 * (m // 2)
    assert tau >= 0, f"regularity violated at {tag}: tau = {tau}"
    return tau


def filtration_m(tag, forms, m, upto=None):
    """{w: dim V_(tau >= w)} at a visible triple point for a list of
    degree-m numerator tuples, plus the basis of V_(tau >= m) (the
    subspace extending across the 32 exceptional curves there)."""
    upto = upto if upto is not None else m + 2
    dord = 12 * (m // 2)
    n = len(forms)
    pulls = [local_pullback_m(Ns, tag, m) for Ns in forms]
    dims, basism = {}, None
    for w in range(m % 2, upto + 1, 2):
        rows = {}
        for gi, P in enumerate(pulls):
            for ci, c in enumerate(P):
                for (i, j), v in c.items():
                    if i + j < dord + w:
                        rows.setdefault((ci, i, j), [F(0)] * n)[gi] = v
        ns = nullspace(list(rows.values()), n)
        dims[w] = len(ns)
        if w == m:
            basism = ns
    return dims, basism


def sigma_numerators_m(Ns, m, degb):
    """Transpose pullback for a degree-m invariant differential whose
    numerators have total degree <= degb (= dN - (2m + 1), the chart-2
    regularity bound, asserted); requires and asserts v^m dividing."""
    for N in Ns:
        assert all(i + j <= degb for (i, j), v in N.items() if v), \
            "degree bound violated for sigma at this m"
    out = [dict() for _ in range(m + 1)]
    for k in range(m + 1):
        Nt = {}
        for (i, j), val in Ns[k].items():
            key = (i, degb - i - j)
            Nt[key] = Nt.get(key, F(0)) + val
        for r in range(k + 1):
            term = pmul(Nt, {(k - r, r): F(comb(k, r) * (-1) ** (k - r))})
            out[r] = padd(out[r], pscal(term, F((-1) ** (m - k))))
    res = []
    for compo in out:
        assert all(j >= m for (_, j) in compo), "v^m does not divide"
        res.append({(i, j - m): v for (i, j), v in compo.items()})
    return res


def resolution_dim_m(forms, m, degb):
    """dim of the subspace of span(forms) extending across ALL 256
    exceptional curves: tau >= m at the five visible triple points,
    and at the three B-points via tau(sigma* eta, A-tag) >= m — the
    B-conditions are built DIRECTLY from the pulled-back
    sigma*-numerators of the basis (linear in the same coordinates),
    so the span need not be sigma-stable (a partially reconstructed
    basis usually is not).  A lower-bound contribution to
    h^0(Ytilde, S^m Omega^1) from this (trivial-character) space,
    exact for the span."""
    n = len(forms)
    dord = 12 * (m // 2)
    conds = []
    for tag in VISIBLE:
        _, bm = filtration_m(tag, forms, m, upto=m)
        conds += annihilator(bm, n) if bm is not None else []
    sig_forms = [sigma_numerators_m(Ns, m, degb) for Ns in forms]
    for _btag, atag in SIGMA_PAIRS:
        pulls = [local_pullback_m(sN, atag, m) for sN in sig_forms]
        rows = {}
        for gi, P in enumerate(pulls):
            for ci, c in enumerate(P):
                for (i, j), v in c.items():
                    if i + j < dord + m:
                        rows.setdefault((ci, i, j), [F(0)] * n)[gi] = v
        conds += list(rows.values())
    return len(nullspace(conds, n))


def _solve_in_span_n(target, basis_forms, m):
    keys = set()
    for comp in range(m + 1):
        for B in basis_forms:
            keys |= {(comp, ij) for ij in B[comp]}
        keys |= {(comp, ij) for ij in target[comp]}
    rows, rhs = [], []
    for (comp, ij) in sorted(keys):
        rows.append([B[comp].get(ij, F(0)) for B in basis_forms])
        rhs.append(target[comp].get(ij, F(0)))
    n = len(basis_forms)
    aug = [row + [r] for row, r in zip(rows, rhs)]
    red, piv_cols, rank = _rref(aug, n)
    for r in range(rank, len(red)):
        assert all(x == 0 for x in red[r]), "sigma leaves the space!"
    x = [F(0)] * n
    for r, col in enumerate(piv_cols):
        x[col] = red[r][n]
    return x


def main():
    forms = numerator_forms()
    print("tau table (rows = generators, columns = visible points):")
    for gi, Ns in enumerate(forms):
        taus = [tau_of(Ns, tag) for tag in VISIBLE]
        print(f"  eta_{gi + 1}: " +
              "  ".join(f"{t}:{v}" for t, v in zip(VISIBLE, taus)))
    print("filtration at each visible point:")
    for tag in VISIBLE:
        dims, _ = filtration(tag, forms)
        print(f"  {tag}: " + ", ".join(f"dim V_(tau>={w}) = {d}"
                                       for w, d in dims.items()))
    mats = rep_matrices()
    print("grid representation: involutions verified:",
          all(is_identity(mat_mul(m, m)) for m in mats.values()))
    spaces = extension_spaces()
    pair_dims = {}
    for t1, t2 in combinations(ALL_TAGS, 2):
        pair_dims[(t1, t2)] = len(intersect(spaces, [t1, t2]))
    from collections import Counter
    print("pairwise extension-space intersection dims:",
          dict(Counter(pair_dims.values())))
    print("  dim-3 pairs:", sorted(k for k, v in pair_dims.items()
                                   if v == 3))
    print("A-triple:", len(intersect(spaces, ["A0", "A+", "A-"])),
          " B-triple:", len(intersect(spaces, ["B0", "B+", "B-"])),
          " D-pair:", len(intersect(spaces, ["D+", "D-"])))
    w, _ = wstar_vector(spaces)
    print("W = intersection of all 8:  dim 1, omega* =", w)
    print("=> h^0(resolution, S^4 Omega^1) = 1 exactly;")
    print("   every rational curve on the resolution (not in the")
    print("   exceptional locus) is an integral curve of eta*;")
    print("   u = 0 and v = 0 are eta*-integral (AP families comply).")


if __name__ == "__main__":
    main()
