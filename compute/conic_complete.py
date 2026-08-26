"""Completeness sweep for conic-image curves on X (M10-B, A7 section 4).

Together with the M9 tangent-to-5 sweep this proves Theorem A7.6: no
genus <= 1 curve on X has conic image (characteristic 0).

The sharp budget lemma (Lemma A7.5 in the doc) says: for a smooth conic
C in the Lucas plane and a point p of C on the arrangement, EVERY entry
line through p meets C at p either transversally (multiplicity 1) or as
the unique tangent line of C at p (multiplicity 2).  Writing mu(p) for
the number of entry lines through p (1, 2 or 3), s_p for the transversal
count and t_p <= 1 for the tangency count, this forces

    (s_p, t_p) in { (mu,0), (mu-1,1) },      sum_p (s_p + 2 t_p) = 18,

p is branch-effective iff s_p >= 1, and genus <= 1 of a component over C
forces r_eff <= 4 effective Qbar-points.  Since s_p <= 3, the transversal
total 18 - 2T (T = number of tangent entry lines) satisfies
18 - 2T <= 3 r_eff, so

    genus 0  ==>  r_eff <= 3  ==>  T >= 5   (closed: tangent-to-5 sweep),
    genus 1  ==>  r_eff  = 4  and  T in {3, 4}  (T >= 5 again closed),

and the T in {3,4} solutions fall into exactly six classes:

    C1: four transversal triple points        + 3 free tangencies,
    C2: three transversal triples             + 4 free tangencies,
    C3: three transversal triples + a tangent-at-double + 3 free,
    C4: two transversal triples + two doubles + 4 free tangencies,
    C5: two transversal triples + a double + a tangent-at-triple + 3 free,
    C6: two transversal triples + two tangent-at-triples + 2 free.

("free" tangency = tangent at a simple point of the arrangement;
"tangent-at-double/triple" = the tangent line at that rational multiple
point is one of the entry lines through it.)  Classes C1 and C4 are
pencils (4 point conditions) whose members are cut out by common roots
of restriction discriminants -- degree <= 2 over Q, so quadratic fields
suffice; C3, C5, C6 are linear systems with >= 5 conditions; C2 is a net
(3 point conditions) needing common zeros of four ternary quadrics --
handled by exact resultant/gcd elimination with an emptiness
certificate.

Everything is exact: Fractions, an explicit Q(sqrt(D)) arithmetic layer,
and a field-generic conic analyzer cross-validated against the M9
analyzer (compute.conic_pullbacks.analyze_conic) on rational conics.

Run:  python3 -m compute.conic_complete
"""

from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt

from compute.curve_pullbacks import ENTRY_LINES, cross, multiple_points
from compute.conic_pullbacks import (analyze_conic, conic_det, conic_eval,
                                     restrict_to_line)


# ---------------------------------------------------------------------------
# exact arithmetic in K = Q(sqrt(D)); elements are pairs (a, b) = a + b sqrt(D)

def qsqrt(q):
    """Exact square root of a nonnegative Fraction, or None."""
    q = F(q)
    if q < 0:
        return None
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return None


def k_el(a, b=0):
    return (F(a), F(b))


def k_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def k_sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def k_mul(D, x, y):
    return (x[0] * y[0] + D * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def k_scale(x, c):
    return (x[0] * c, x[1] * c)


def k_is_zero(x):
    return x[0] == 0 and x[1] == 0


def k_inv(D, x):
    n = x[0] * x[0] - D * x[1] * x[1]
    if n == 0:
        raise ZeroDivisionError("norm zero in Q(sqrt(D))")
    return (x[0] / n, -x[1] / n)


def k_sqrt(D, x):
    """A square root of x in K = Q(sqrt(D)), or None if x is not a square
    in K.  (D a non-square rational.)"""
    a, b = x
    if b == 0:
        r = qsqrt(a)
        if r is not None:
            return (r, F(0))
        r = qsqrt(a / D)
        if r is not None:
            return (F(0), r)
        return None
    n2 = a * a - D * b * b
    n = qsqrt(n2)
    if n is None:
        return None
    for t in ((a + n) / 2, (a - n) / 2):
        p = qsqrt(t)
        if p and p != 0:
            q = b / (2 * p)
            cand = (p, q)
            if k_mul(D, cand, cand) == (a, b):
                return cand
    return None


# ---------------------------------------------------------------------------
# field-generic conic analyzer (K = Q(sqrt(D)); rational conics: any D)

def _k_norm_point(D, p):
    """Normalize a projective K-point: divide by the first nonzero coord."""
    for x in p:
        if not k_is_zero(x):
            inv = k_inv(D, x)
            return tuple(k_mul(D, inv, y) for y in p)
    raise ValueError("zero vector")


def _k_restrict(D, M, L):
    """Restriction of the K-conic M to the rational line L: binary form
    (A, B, C) in K, plus the rational base points P0, P1."""
    pts = []
    for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        w = cross(L, e)
        if not any(w):
            continue
        if not pts:
            pts.append(w)
        elif any(cross(pts[0], w)):
            pts.append(w)
        if len(pts) == 2:
            break
    P0, P1 = pts

    def ev(p, q):
        s = k_el(0)
        for i in range(3):
            for j in range(3):
                s = k_add(s, k_scale(M[i][j], F(p[i] * q[j])))
        return s

    A = ev(P0, P0)
    C = ev(P1, P1)
    B = k_add(ev(P0, P1), ev(P1, P0))
    return (A, B, C), P0, P1


def _k_det(D, M):
    def mul(*xs):
        r = k_el(1)
        for x in xs:
            r = k_mul(D, r, x)
        return r
    a, b, c0 = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    t1 = k_mul(D, a, k_sub(mul(e, i), mul(f, h)))
    t2 = k_mul(D, b, k_sub(mul(d, i), mul(f, g)))
    t3 = k_mul(D, c0, k_sub(mul(d, h), mul(e, g)))
    return k_add(k_sub(t1, t2), t3)


def analyze_conic_K(M, D, name=""):
    """Pullback analysis of an irreducible conic with entries in
    K = Q(sqrt(D)) (pairs (a, b) of Fractions).  Mirrors
    conic_pullbacks.analyze_conic; conjugate pairs OVER K share a
    weight-2 column (their multiplicity vectors agree under Gal(/K))."""
    D = F(D)
    if k_is_zero(_k_det(D, M)):
        return {"name": name, "reducible": True}
    columns = {}

    def add(key, line, mult, weight=1):
        col = columns.setdefault(key, {"weight": weight, "mults": {}})
        col["mults"][line] = col["mults"].get(line, 0) + mult

    for i, L in enumerate(ENTRY_LINES):
        (A, B, C), P0, P1 = _k_restrict(D, M, L)
        disc = k_sub(k_mul(D, B, B), k_scale(k_mul(D, A, C), 4))

        def pt(s, t):
            # point s*P0 + t*P1 with s, t in K
            p = tuple(k_add(k_scale(s, F(P0[i])), k_scale(t, F(P1[i])))
                      for i in range(3))
            return ("pt", _k_norm_point(D, p))

        if k_is_zero(A) and k_is_zero(B) and k_is_zero(C):
            return {"name": name, "degenerate_contained": True}
        if k_is_zero(disc):
            # double root
            if not k_is_zero(A):
                root = pt(k_scale(B, F(-1, 2)), A)   # (-B/2 : A) ~ (-B : 2A)
            elif not k_is_zero(C):
                root = pt(C, k_scale(B, F(-1, 2)))
            else:  # A = C = 0, disc = B^2 = 0 => B = 0: handled above
                return {"name": name, "degenerate_contained": True}
            add(root, i, 2)
            continue
        r = k_sqrt(D, disc)
        if r is not None:
            if k_is_zero(A):
                # roots (1:0) and (-C : B)
                add(pt(k_el(1), k_el(0)), i, 1)
                add(pt(k_scale(C, F(-1)), B), i, 1)
            else:
                add(pt(k_sub(r, B), k_scale(A, F(2))), i, 1)
                add(pt(k_sub(k_scale(r, F(-1)), B), k_scale(A, F(2))), i, 1)
        else:
            add(("pair", i), i, 1, weight=2)

    keys = sorted(columns, key=str)
    vecs = [[columns[k]["mults"].get(i, 0) % 2 for k in keys]
            for i in range(9)]
    rows = [[(vecs[i][j] + vecs[8][j]) % 2 for j in range(len(keys))]
            for i in range(8)]
    basis = []
    for row in rows:
        row = row[:]
        for b in basis:
            piv = next(j for j, x in enumerate(b) if x)
            if row[piv]:
                row = [(x + y) % 2 for x, y in zip(row, b)]
        if any(row):
            basis.append(row)
    k = len(basis)
    ram = [j for j in range(len(keys)) if any(b[j] for b in basis)]
    r_eff = sum(columns[keys[j]]["weight"] for j in ram)
    if k == 0:
        genus = 0
    elif k == 1:
        genus = (r_eff - 2) // 2 if r_eff % 2 == 0 else None
    else:
        genus = 1 + 2 ** (k - 2) * (r_eff - 4)
    total = sum(sum(c["mults"].values()) * c["weight"]
                for c in columns.values())
    return {"name": name, "reducible": False, "k": k, "r_eff": r_eff,
            "genus": genus, "n_columns": len(keys),
            "total_mult_check": total, "n_components": 2 ** (8 - k)}


def lift_rational(M):
    """A rational conic matrix as a K-matrix (b = 0 throughout)."""
    return [[k_el(M[i][j]) for j in range(3)] for i in range(3)]


# ---------------------------------------------------------------------------
# linear condition systems on the 6-dim space of conics
# coordinates (a11, a22, a33, a12, a13, a23);
# Q = a11 c^2 + a22 u^2 + a33 v^2 + 2 a12 cu + 2 a13 cv + 2 a23 uv

def row_through(p):
    c, u, v = p
    return [F(c * c), F(u * u), F(v * v), F(2 * c * u), F(2 * c * v),
            F(2 * u * v)]


def rows_tangent_at(p, L):
    """Tangency to line L at p (p on L required): M p proportional to L,
    i.e. (Mp) x L = 0 -- three rows of rank 2."""
    c, u, v = p
    # (Mp)_1 = a11 c + a12 u + a13 v, etc., as rows in the 6 coords
    g = [[F(c), 0, 0, F(u), F(v), 0],
         [0, F(u), 0, F(c), 0, F(v)],
         [0, 0, F(v), 0, F(c), F(u)]]
    l1, l2, l3 = L
    rows = []
    for (i, j, li, lj) in ((1, 2, l3, l2), (2, 0, l1, l3), (0, 1, l2, l1)):
        rows.append([g[i][t] * li - g[j][t] * lj for t in range(6)])
    return rows


def nullspace(rows):
    """Exact nullspace basis of the 6-column system, as integer conic
    matrices."""
    m = [[F(x) for x in r] for r in rows]
    n = 6
    piv_cols, r = [], 0
    for col in range(n):
        piv = next((i for i in range(r, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        m[r] = [x / m[r][col] for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][col] != 0:
                f = m[i][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv_cols.append(col)
        r += 1
    free = [c for c in range(n) if c not in piv_cols]
    out = []
    for fc in free:
        sol = [F(0)] * n
        sol[fc] = F(1)
        for i, col in enumerate(piv_cols):
            sol[col] = -m[i][fc]
        den = 1
        for x in sol:
            den = den * x.denominator // gcd(den, x.denominator)
        a11, a22, a33, a12, a13, a23 = [int(x * den) for x in sol]
        out.append([[a11, a12, a13], [a12, a22, a23], [a13, a23, a33]])
    return out


# ---------------------------------------------------------------------------
# the pencil engine: members of lam*M0 + mu*M1 tangent to >= threshold lines

def disc_form(M0, M1, L):
    """Integer coefficients (a, b, c) of disc(lam, mu) = a lam^2 + b lam mu
    + c mu^2 for the restriction of lam M0 + mu M1 to line L."""
    (A0, B0, C0), _, _ = restrict_to_line(M0, L)
    (A1, B1, C1), _, _ = restrict_to_line(M1, L)
    a = B0 * B0 - 4 * A0 * C0
    b = 2 * B0 * B1 - 4 * (A0 * C1 + A1 * C0)
    c = B1 * B1 - 4 * A1 * C1
    return int(a), int(b), int(c)


def _norm_rat_root(p, q):
    g = gcd(p, q)
    if g:
        p, q = p // g, q // g
    if q < 0 or (q == 0 and p < 0):
        p, q = -p, -q
    return (p, q)


def _norm_quad(a, b, c):
    g = gcd(gcd(a, b), c)
    a, b, c = a // g, b // g, c // g
    if a < 0:
        a, b, c = -a, -b, -c
    return (a, b, c)


def binary_quadratic_roots(a, b, c):
    """Projective roots of a lam^2 + b lam mu + c mu^2 over Q:
    returns (rational_roots, quad_key) where quad_key is the normalized
    irreducible quadratic or None."""
    if a == 0 and b == 0 and c == 0:
        return None, None       # identically zero: caller handles
    if a == 0:
        # mu (b lam + c mu)
        roots = [(1, 0)]
        if b != 0:
            roots.append(_norm_rat_root(-c, b))
        return sorted(set(roots)), None
    disc = b * b - 4 * a * c
    r = qsqrt(F(disc))
    if r is None:
        return [], _norm_quad(a, b, c)
    if r == 0:
        return [_norm_rat_root(-b, 2 * a)], None
    rn = int(r)  # disc is a perfect square integer here
    return sorted({_norm_rat_root(-b + rn, 2 * a),
                   _norm_rat_root(-b - rn, 2 * a)}), None


def pencil_all_reducible(M0, M1):
    """True iff EVERY member of the pencil is reducible: det(lam M0 +
    mu M1) is a binary cubic, so vanishing at four distinct parameters
    forces identical vanishing."""
    for lam, mu in ((1, 0), (0, 1), (1, 1), (1, -1)):
        M = [[lam * M0[i][j] + mu * M1[i][j] for j in range(3)]
             for i in range(3)]
        if conic_det(M) != 0:
            return False
    return True


def space_all_reducible(basis):
    """True iff every conic in the span of ``basis`` (integer matrices) is
    reducible: det is a cubic in the d coordinates, and a nonzero cubic
    cannot vanish on the full grid {0,1,2,3}^d (degree 3 < 4 in each
    variable)."""
    from itertools import product
    d = len(basis)
    for coeffs in product(range(4), repeat=d):
        if not any(coeffs):
            continue
        M = [[sum(c * B[i][j] for c, B in zip(coeffs, basis))
              for j in range(3)] for i in range(3)]
        if conic_det(M) != 0:
            return False
    return True


def pencil_members(M0, M1, threshold):
    """All members of the pencil tangent to >= threshold entry lines,
    as (descriptor, matrix, D, tangent_line_count); rational members get
    D = None (rational analyzer).  Also returns the list of lines whose
    discriminant vanishes identically on the pencil (each contributes to
    every member's tangency count).  Completeness: a member tangent to
    >= threshold lines has >= threshold - #identical vanishing
    discriminants, hence appears at a common root collected here --
    UNLESS #identical alone reaches the threshold, which the caller must
    handle (all-reducible check or hard flag)."""
    per_root = {}
    identically = []
    for i, L in enumerate(ENTRY_LINES):
        a, b, c = disc_form(M0, M1, L)
        if (a, b, c) == (0, 0, 0):
            identically.append(i)
            continue
        rat, quad = binary_quadratic_roots(a, b, c)
        for root in rat:
            per_root.setdefault(("rat", root), set()).add(i)
        if quad is not None:
            per_root.setdefault(("quad", quad), set()).add(i)
    out = []
    base = len(identically)
    for key, lines in per_root.items():
        if base + len(lines) < threshold:
            continue
        if key[0] == "rat":
            p, q = key[1]
            M = [[p * M0[i][j] + q * M1[i][j] for j in range(3)]
                 for i in range(3)]
            out.append((key, M, None, base + len(lines)))
        else:
            a, b, c = key[1]
            D = F(b * b - 4 * a * c)
            lam = (F(-b), F(1))          # -b + sqrt(D)
            mu = (F(2 * a), F(0))
            M = [[k_add(k_scale(lam, F(M0[i][j])),
                        k_scale(mu, F(M1[i][j]))) for j in range(3)]
                 for i in range(3)]
            out.append((key, M, D, base + len(lines)))
    return out, identically


def _collinear3(points):
    for trip in combinations(points, 3):
        m = [list(p) for p in trip]
        det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
               - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
               + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        if det == 0:
            return True
    return False


def _analyze(desc, M, D):
    if D is None:
        data = analyze_conic(M, str(desc))
    else:
        data = analyze_conic_K(M, D, str(desc))
    return data


def _run_pencil(basis, threshold, desc, label, analyzed, hits, flags,
                counters):
    """Run the pencil engine on span(basis[0], basis[1]) with soundness
    accounting: an all-reducible pencil is skipped (justified: no smooth
    conic in it); a pencil whose identically-vanishing discriminants
    alone reach the threshold, without being all-reducible, would be a
    continuum of eligible smooth conics -- hard flag (none expected)."""
    if pencil_all_reducible(basis[0], basis[1]):
        counters["skipped_reducible"] += 1
        return
    members, ident = pencil_members(basis[0], basis[1], threshold)
    if len(ident) >= threshold:
        flags.append((label, desc,
                      f"continuum: identically tangent {ident}"))
        return
    if ident:
        counters["pencils_with_builtin_tangency"] += 1
    for key, M, D, cnt in members:
        data = _analyze((label, desc, key), M, D)
        if data.get("reducible") or data.get("degenerate_contained"):
            continue
        analyzed.append(data)
        if data["genus"] is not None and data["genus"] <= 1:
            hits.append(data)


def _new_counters():
    return {"skipped_reducible": 0, "pencils_with_builtin_tangency": 0,
            "skipped_collinear": 0}


def _sweep_point_pencils(point_sets, threshold, label):
    """Common driver for C1/C4: 4-point pencils, members with >= threshold
    tangent lines.  Point sets with three collinear points are skipped:
    every conic through three collinear points contains their line."""
    analyzed, hits, flags = [], [], []
    counters = _new_counters()
    for pts in point_sets:
        if _collinear3(pts):
            counters["skipped_collinear"] += 1
            continue
        basis = nullspace([row_through(p) for p in pts])
        if len(basis) != 2:
            flags.append((label, pts, f"unexpected dim {len(basis)}"))
            continue
        _run_pencil(basis, threshold, pts, label, analyzed, hits, flags,
                    counters)
    return {"label": label, "n_systems": len(point_sets),
            "counters": counters, "analyzed": len(analyzed), "hits": hits,
            "flags": flags}


def _sweep_linear(class_specs, label, pencil_threshold):
    """Common driver for C3/C5/C6: >= 5 linear conditions; dim-1 solutions
    analyzed directly, dim-2 solution spaces fall back to the pencil
    engine, and larger spaces are justified-skipped only when provably
    all-reducible (grid vanishing of the det cubic)."""
    analyzed, hits, flags = [], [], []
    counters = _new_counters()
    n = 0
    for desc, rows in class_specs:
        n += 1
        basis = nullspace(rows)
        if len(basis) == 0:
            continue
        if len(basis) == 1:
            M = basis[0]
            if conic_det(M) == 0:
                counters["skipped_reducible"] += 1
                continue
            data = analyze_conic(M, str((label, desc)))
            if data.get("degenerate_contained"):
                continue
            analyzed.append(data)
            if data["genus"] is not None and data["genus"] <= 1:
                hits.append(data)
        elif len(basis) == 2:
            _run_pencil(basis, pencil_threshold, desc, label, analyzed,
                        hits, flags, counters)
        else:
            if space_all_reducible(basis):
                counters["skipped_reducible"] += 1
            else:
                flags.append((label, desc,
                              f"dim {len(basis)} space, not all reducible"))
    return {"label": label, "n_systems": n, "counters": counters,
            "analyzed": len(analyzed), "hits": hits, "flags": flags}


def _triples_doubles():
    mp = multiple_points()
    triples = sorted([p for p, ls in mp.items() if len(ls) == 3], key=str)
    doubles = sorted([p for p, ls in mp.items() if len(ls) == 2], key=str)
    return triples, doubles, mp


def sweep_C1():
    triples, _, _ = _triples_doubles()
    return _sweep_point_pencils(list(combinations(triples, 4)), 3, "C1")


def sweep_C4():
    triples, doubles, _ = _triples_doubles()
    sets = [t2 + d2 for t2 in combinations(triples, 2)
            for d2 in combinations(doubles, 2)]
    return _sweep_point_pencils(sets, 4, "C4")


def sweep_C3():
    triples, doubles, mp = _triples_doubles()
    specs = []
    for t3 in combinations(triples, 3):
        if _collinear3(t3):
            continue
        for d in doubles:
            for li in mp[d]:
                rows = [row_through(p) for p in t3]
                rows += rows_tangent_at(d, ENTRY_LINES[li])
                specs.append(((t3, d, li), rows))
    return _sweep_linear(specs, "C3", 3)


def sweep_C5():
    triples, doubles, mp = _triples_doubles()
    specs = []
    for t2 in combinations(triples, 2):
        for tt in triples:
            if tt in t2:
                continue
            for li in mp[tt]:
                for d in doubles:
                    rows = [row_through(p) for p in t2]
                    rows.append(row_through(d))
                    rows += rows_tangent_at(tt, ENTRY_LINES[li])
                    specs.append(((t2, tt, li, d), rows))
    return _sweep_linear(specs, "C5", 3)


def sweep_C6():
    triples, _, mp = _triples_doubles()
    specs = []
    for t2 in combinations(triples, 2):
        rest = [t for t in triples if t not in t2]
        for ta, tb in combinations(rest, 2):
            for la in mp[ta]:
                for lb in mp[tb]:
                    rows = [row_through(p) for p in t2]
                    rows += rows_tangent_at(ta, ENTRY_LINES[la])
                    rows += rows_tangent_at(tb, ENTRY_LINES[lb])
                    specs.append(((t2, ta, la, tb, lb), rows))
    return _sweep_linear(specs, "C6", 2)


# ---------------------------------------------------------------------------
# C2: three-triple nets; members tangent to >= 4 lines.
# Exact elimination: pairwise resultants in z are binary quartics in (x, y);
# a common projective zero of the four chosen discriminants forces either
# (x, y) = (0, 0) (checked directly) or a common root of all pairwise
# resultants.  gcd(resultants) == 1 certifies emptiness over Qbar.

def _binform_mul(f, g):
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] += a * b
    return out


def _binform_add(f, g):
    n = max(len(f), len(g))
    f = f + [0] * (n - len(f))
    g = g + [0] * (n - len(g))
    return [a + b for a, b in zip(f, g)]


def _binform_scale(f, c):
    return [a * c for a in f]


def _det4(m):
    """Determinant of a 4x4 matrix of binary forms (coefficient lists)."""
    from itertools import permutations
    total = [0]
    for perm in permutations(range(4)):
        sign = 1
        seen = list(perm)
        # parity via inversion count
        inv = sum(1 for i in range(4) for j in range(i + 1, 4)
                  if seen[i] > seen[j])
        sign = -1 if inv % 2 else 1
        term = [1]
        for i in range(4):
            term = _binform_mul(term, m[i][perm[i]])
        total = _binform_add(total, _binform_scale(term, sign))
    return total


def _strip(f):
    while f and f[-1] == 0:
        f.pop()
    return f


def _poly_gcd_q(f, g):
    """gcd of univariate integer polynomial coefficient lists (ascending),
    monic-normalized over Q, returned as primitive integer list."""
    a = [F(x) for x in f]
    b = [F(x) for x in g]

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
            c = p[dp] / q[dq]
            for i in range(dq + 1):
                p[dp - dq + i] -= c * q[i]
            p[dp] = F(0)
        return p

    while deg(b) >= 0:
        a, b = b, rem(a, b)
    d = deg(a)
    if d < 0:
        return [0]
    a = a[:d + 1]
    lead = a[-1]
    a = [x / lead for x in a]
    den = 1
    for x in a:
        den = den * x.denominator // gcd(den, x.denominator)
    return [int(x * den) for x in a]


def _good_net_basis(basis):
    """Change basis of the net so that the third basis member's
    restriction to EVERY entry line has nonzero discriminant.  Then every
    disc quadric has a nonzero (constant) z^2-coefficient, so the formal
    z-resultants have unit leading structure and vanish identically only
    for a genuine shared component.  (A z^2-coefficient that vanished
    spuriously -- N2 tangent to two lines -- would otherwise kill the
    Sylvester determinant identically.)"""
    from itertools import product as iproduct

    def disc_ok(M):
        for L in ENTRY_LINES:
            (A, B, C), _, _ = restrict_to_line(M, L)
            if B * B - 4 * A * C == 0:
                return False
        return True

    for combo in iproduct(range(-3, 4), repeat=3):
        if not any(combo):
            continue
        M = [[sum(c * B[i][j] for c, B in zip(combo, basis))
              for j in range(3)] for i in range(3)]
        if not disc_ok(M):
            continue
        # complete (e_a, e_b, combo) to a basis of the coefficient space
        for a, b in combinations(range(3), 2):
            trip = [[1 if t == a else 0 for t in range(3)],
                    [1 if t == b else 0 for t in range(3)], list(combo)]
            det = (trip[0][0] * (trip[1][1] * trip[2][2]
                                 - trip[1][2] * trip[2][1])
                   - trip[0][1] * (trip[1][0] * trip[2][2]
                                   - trip[1][2] * trip[2][0])
                   + trip[0][2] * (trip[1][0] * trip[2][1]
                                   - trip[1][1] * trip[2][0]))
            if det != 0:
                return [basis[a], basis[b], M]
    return None


def _net_disc_quadric(basis, L):
    """Ternary quadric coefficients of disc(x, y, z) for the net
    x N0 + y N1 + z N2 restricted to L: returns dict of monomial -> int
    with keys (i, j, k), i + j + k = 2."""
    ABC = [restrict_to_line(Nk, L)[0] for Nk in basis]
    A = [int(t[0]) for t in ABC]
    B = [int(t[1]) for t in ABC]
    C = [int(t[2]) for t in ABC]
    q = {}

    def bump(mono, val):
        q[mono] = q.get(mono, 0) + val

    idx = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for i in range(3):
        for j in range(3):
            mono = tuple(a + b for a, b in zip(idx[i], idx[j]))
            bump(mono, B[i] * B[j] - 4 * A[i] * C[j])
    return q


def _quadric_in_z(q):
    """Rewrite the ternary quadric as f2 z^2 + f1(x,y) z + f0(x,y) with
    binary-form coefficient lists (ascending in y)."""
    f2 = [q.get((0, 0, 2), 0)]
    f1 = [q.get((1, 0, 1), 0), q.get((0, 1, 1), 0)]
    f0 = [q.get((2, 0, 0), 0), q.get((1, 1, 0), 0), q.get((0, 2, 0), 0)]
    return f2, f1, f0


def _resultant_z(qa, qb):
    """Resultant in z of two ternary quadrics: binary quartic in (x, y),
    as an ascending coefficient list of length 5 (may be shorter after
    stripping)."""
    a2, a1, a0 = _quadric_in_z(qa)
    b2, b1, b0 = _quadric_in_z(qb)
    Z = [0]
    m = [[a2, a1, a0, Z],
         [Z, a2, a1, a0],
         [b2, b1, b0, Z],
         [Z, b2, b1, b0]]
    return _strip(_det4(m))


def _eval_quadric(q, x, y, z):
    return sum(v * x ** i * y ** j * z ** k for (i, j, k), v in q.items())


def sweep_C2(collect_candidates=False):
    """Nets through 3 non-collinear triples: certify (or refute) emptiness
    of 'tangent to >= 4 entry lines' via resultant gcds; rational and
    quadratic candidate roots are verified and analyzed exactly; deeper
    algebraic candidates are returned as flags (none expected)."""
    triples, _, _ = _triples_doubles()
    analyzed, hits, flags = [], [], []
    n_nets = n_certified_empty = n_candidate_sets = 0
    for t3 in combinations(triples, 3):
        if _collinear3(t3):
            continue
        n_nets += 1
        basis = nullspace([row_through(p) for p in t3])
        if len(basis) != 3:
            flags.append(("C2", t3, f"net dim {len(basis)}"))
            continue
        basis = _good_net_basis(basis)
        if basis is None:
            flags.append(("C2", t3, "no basis with nondegenerate N2"))
            continue
        discs = [_net_disc_quadric(basis, L) for L in ENTRY_LINES]
        res = {}
        for i, j in combinations(range(9), 2):
            res[(i, j)] = _resultant_z(discs[i], discs[j])
        for sub in combinations(range(9), 4):
            cands = []
            # the two loci the finite (1 : t) chart cannot see:
            if all(_eval_quadric(discs[i], 0, 0, 1) == 0 for i in sub):
                cands.append((("C2", t3, sub, "member (0:0:1)"),
                              basis[2], None))
            cands += _c2_point(basis, discs, sub, (F(0), F(1)), flags, t3)
            # finite chart: gcd of the pairwise z-resultants in t = y/x
            g = None
            shared_factor = False
            for i, j in combinations(sub, 2):
                r = res[(i, j)]
                if not r:      # identically zero resultant: shared factor
                    flags.append(("C2", t3, sub, f"res({i},{j}) == 0"))
                    shared_factor = True
                    break
                g = r if g is None else _poly_gcd_q(g, r)
                if len(g) == 1 and g[0] != 0:
                    break
            if not shared_factor:
                if g is not None and len(g) == 1 and g[0] != 0:
                    if not cands:
                        n_certified_empty += 1
                else:
                    cands += _c2_candidates(basis, discs, sub, g, flags, t3)
            if cands:
                n_candidate_sets += 1
            for desc, M, D in cands:
                data = _analyze(desc, M, D)
                if data.get("reducible") or data.get("degenerate_contained"):
                    continue
                analyzed.append(data)
                if data["genus"] is not None and data["genus"] <= 1:
                    hits.append(data)
    return {"label": "C2", "n_nets": n_nets,
            "n_4subsets_certified_empty": n_certified_empty,
            "n_4subsets_with_candidates": n_candidate_sets,
            "analyzed": len(analyzed), "hits": hits, "flags": flags}


def _c2_candidates(basis, discs, sub, g, flags, t3):
    """Resolve the candidate roots of the nonconstant gcd g (a polynomial
    in t = y/x, ascending integer coefficients): rational roots and
    quadratic-irrational ones; deeper factors are flagged.  For each
    finite root (1 : t0), and for the point at infinity (0 : 1)
    (which the t-chart cannot see), find common z-roots of the chosen
    discriminants and build the candidate conics.  Returns triples
    (desc, matrix, D-or-None)."""
    out = []
    for t0 in _rational_roots(g):
        out += _c2_point(basis, discs, sub, (F(1), t0), flags, t3)
    for (a, b, c) in _quadratic_factors(g):
        Dq = F(b * b - 4 * a * c)
        t0 = (F(-b, 2 * a), F(1, 2 * a))     # (-b + sqrt(Dq)) / (2a) in K
        out += _c2_point_K(basis, discs, sub, t0, Dq, flags, t3)
    deep = _deep_factors(g)
    if deep:
        flags.append(("C2", t3, sub, f"degree-{deep} gcd factor unresolved"))
    return out


def _rational_roots(coeffs):
    """Rational roots of an integer polynomial (ascending coeffs)."""
    c = [int(x) for x in coeffs]
    while c and c[-1] == 0:
        c.pop()
    if not c:
        return []
    roots = set()
    # strip zero roots
    k = 0
    while k < len(c) and c[k] == 0:
        k += 1
    if k:
        roots.add(F(0))
        c = c[k:]
    if len(c) <= 1:
        return sorted(roots)
    a0, an = abs(c[0]), abs(c[-1])

    def divisors(n):
        out = []
        d = 1
        while d * d <= n:
            if n % d == 0:
                out += [d, n // d]
            d += 1
        return out

    for p in divisors(a0):
        for q in divisors(an):
            for s in (1, -1):
                r = F(s * p, q)
                if sum(ci * r ** i for i, ci in enumerate(c)) == 0:
                    roots.add(r)
    return sorted(roots)


def _deflate_all(coeffs):
    """Peel every rational root (with multiplicity) off an integer
    polynomial; return the primitive integer cofactor (ascending)."""
    poly = [F(x) for x in coeffs]
    while len(poly) > 1:
        roots = _rational_roots(_clear(poly))
        if not roots:
            break
        poly = _deflate(poly, roots[0])
    return _clear(poly)


def _quadratic_factors(coeffs):
    """Irreducible (over Q) quadratic factors (a, b, c) [a t^2 + b t + c]
    of an integer polynomial of degree <= 4: peel rational roots, then
    factor the remaining quadratic or quartic (Gauss: primitive integer
    quartics factor over Q iff over Z)."""
    poly = _deflate_all(coeffs)
    dd = len(poly) - 1
    if dd == 2:
        a2, a1, a0 = poly[2], poly[1], poly[0]
        if qsqrt(F(a1 * a1 - 4 * a2 * a0)) is None:
            return [_norm_quad(a2, a1, a0)]
        return []
    if dd == 4:
        return _quartic_quadratic_split(poly)
    return []


def _deflate(poly, r):
    """Divide (ascending Fractions) by (t - r); exact synthetic division."""
    d = len(poly) - 1
    out = [F(0)] * d
    acc = F(poly[d])
    out[d - 1] = acc
    for i in range(d - 1, 0, -1):
        acc = poly[i] + acc * r
        out[i - 1] = acc
    return out


def _clear(poly):
    """Fractions (ascending) -> primitive integer list, trailing zeros
    stripped."""
    poly = [F(x) for x in poly]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    den = 1
    for x in poly:
        den = den * x.denominator // gcd(den, x.denominator)
    c = [int(x * den) for x in poly]
    g = 0
    for x in c:
        g = gcd(g, abs(x))
    if g > 1:
        c = [x // g for x in c]
    return c


def _signed_divisors(n):
    n = abs(n)
    out = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out += [d, -d, n // d, -(n // d)]
        d += 1
    return sorted(set(out))


def _quartic_quadratic_split(c):
    """Primitive integer quartic with no rational roots (ascending):
    return its irreducible quadratic factors if it splits over Q into two
    quadratics (Gauss: equivalent to over Z), else [].

    For (A1 t^2 + B1 t + C1)(A2 t^2 + B2 t + C2): A1 A2 = a, C1 C2 = e,
    and with K := cm - A1 C2 - A2 C1 the B's satisfy B1 B2 = K and
    A2 B1 + A1 B2 = b, so B1 solves A2 B1^2 - b B1 + A1 K = 0 -- a
    discriminant square test.  Exhaustive over the divisor pairs."""
    e, d_, cm, b, a = c[0], c[1], c[2], c[3], c[4]
    if e == 0:
        return []              # t = 0 would be a rational root; peeled
    for A1 in _signed_divisors(a):
        A2 = a // A1
        for C1 in _signed_divisors(e):
            C2 = e // C1
            K = cm - A1 * C2 - A2 * C1
            disc = b * b - 4 * A2 * A1 * K
            r = qsqrt(F(disc))
            if r is None:
                continue
            for sgn in (1, -1):
                num = b + sgn * int(r)
                if num % (2 * A2) != 0:
                    continue
                B1 = num // (2 * A2)
                numB2 = b - A2 * B1
                if numB2 % A1 != 0:
                    continue
                B2 = numB2 // A1
                if B1 * B2 != K or B1 * C2 + B2 * C1 != d_:
                    continue
                return _split_result(A1, B1, C1, A2, B2, C2)
    return []


def _split_result(A1, B1, C1, A2, B2, C2):
    out = []
    for (A, B, C) in ((A1, B1, C1), (A2, B2, C2)):
        if qsqrt(F(B * B - 4 * A * C)) is None:
            out.append(_norm_quad(A, B, C))
    return out


def _deep_factors(coeffs):
    """Residual irreducible degree > 2 that the rational/quadratic passes
    cannot resolve (0 if none)."""
    poly = _deflate_all(coeffs)
    dd = len(poly) - 1
    if dd <= 2:
        return 0
    if dd == 4 and _quartic_quadratic_split(poly):
        return 0
    return dd


def _c2_point(basis, discs, sub, xy, flags, t3):
    """Rational (x:y): find common z-roots of the chosen discriminants;
    build and return candidate conics (rational or quadratic field)."""
    x0, y0 = xy
    den = (x0.denominator * y0.denominator)
    xi, yi = int(x0 * den), int(y0 * den)
    zpolys = []
    for i in sub:
        q = discs[i]
        a = q.get((0, 0, 2), 0)
        b = q.get((1, 0, 1), 0) * xi + q.get((0, 1, 1), 0) * yi
        c = (q.get((2, 0, 0), 0) * xi * xi + q.get((1, 1, 0), 0) * xi * yi
             + q.get((0, 2, 0), 0) * yi * yi)
        zpolys.append((a, b, c))
    # common z-roots of all: gcd chain over Q (identically-zero
    # discriminants share every root and drop out; all-zero is flagged)
    g = None
    for (a, b, c) in zpolys:
        p = [c, b, a]
        if p == [0, 0, 0]:
            continue
        g = p if g is None else _poly_gcd_q(g, p)
    if g is None:
        flags.append(("C2", t3, sub, (xi, yi),
                      "all four discriminants vanish on the whole z-line"))
        return []
    if len(g) == 1:
        return []
    out = []
    if len(g) == 2:            # single rational common z
        z0 = F(-g[0], g[1])
        M = _net_member_rat(basis, F(xi), F(yi), z0)
        out.append((("C2", t3, sub, (xi, yi), z0), M, None))
    elif len(g) == 3:          # both roots of a quadratic are common
        a2, a1, a0 = g[2], g[1], g[0]
        Dq = F(a1 * a1 - 4 * a2 * a0)
        r = qsqrt(Dq)
        if r is not None:
            for sign in (1, -1):
                z0 = F(-a1 + sign * int(r), 2 * a2)
                M = _net_member_rat(basis, F(xi), F(yi), z0)
                out.append((("C2", t3, sub, (xi, yi), z0), M, None))
        else:
            z0 = (F(-a1, 2 * a2), F(1, 2 * a2))
            M = _net_member_K(basis, k_el(xi), k_el(yi), z0, Dq)
            out.append((("C2", t3, sub, (xi, yi), "quad-z"), M, Dq))
    return out


def _c2_point_K(basis, discs, sub, t0, Dq, flags, t3):
    """Quadratic-irrational (x:y) = (1 : t0), t0 in K = Q(sqrt(Dq));
    common z-roots over K; conics over K or flagged if degree 4 needed."""
    x0 = k_el(1)
    y0 = t0
    zq = []
    for i in sub:
        q = discs[i]
        a = k_el(q.get((0, 0, 2), 0))
        b = k_add(k_scale(x0, F(q.get((1, 0, 1), 0))),
                  k_scale(y0, F(q.get((0, 1, 1), 0))))
        y2 = k_mul(Dq, y0, y0)
        xy = k_mul(Dq, x0, y0)
        c = k_add(k_add(k_scale(k_mul(Dq, x0, x0), F(q.get((2, 0, 0), 0))),
                        k_scale(xy, F(q.get((1, 1, 0), 0)))),
                  k_scale(y2, F(q.get((0, 2, 0), 0))))
        zq.append((a, b, c))
    # pairwise gcd over K of the z-quadratics: do it by checking shared
    # roots directly (quadratics): z-roots of the first nonzero quadratic,
    # then test the rest.
    first = next(((a, b, c) for (a, b, c) in zq
                  if not (k_is_zero(a) and k_is_zero(b) and k_is_zero(c))),
                 None)
    if first is None:
        flags.append(("C2", t3, sub, "K-point", "all z-polys zero"))
        return []
    a, b, c = first
    out = []
    if k_is_zero(a):
        if k_is_zero(b):
            return []
        roots = [k_mul(Dq, k_scale(c, F(-1)), k_inv(Dq, b))]
    else:
        disc = k_sub(k_mul(Dq, b, b), k_scale(k_mul(Dq, a, c), 4))
        r = k_sqrt(Dq, disc)
        if r is None:
            # z lives in a degree-4 field: flag for manual treatment
            flags.append(("C2", t3, sub, "K-point",
                          "z requires quartic field"))
            return []
        inv2a = k_inv(Dq, k_scale(a, F(2)))
        roots = [k_mul(Dq, k_add(k_scale(b, F(-1)), k_scale(r, F(s))),
                       inv2a) for s in (1, -1)]
    for z0 in roots:
        ok = True
        for (aa, bb, cc) in zq:
            val = k_add(k_add(k_mul(Dq, aa, k_mul(Dq, z0, z0)),
                              k_mul(Dq, bb, z0)), cc)
            if not k_is_zero(val):
                ok = False
                break
        if ok:
            M = _net_member_K(basis, x0, y0, z0, Dq)
            out.append((("C2", t3, sub, "K-root"), M, Dq))
    return out


def _net_member_rat(basis, x, y, z):
    den = x.denominator * y.denominator * z.denominator
    xi, yi, zi = int(x * den), int(y * den), int(z * den)
    return [[xi * basis[0][i][j] + yi * basis[1][i][j] + zi * basis[2][i][j]
             for j in range(3)] for i in range(3)]


def _net_member_K(basis, x, y, z, Dq):
    return [[k_add(k_add(k_scale(x, F(basis[0][i][j])),
                         k_scale(y, F(basis[1][i][j]))),
                   k_scale(z, F(basis[2][i][j]))) for j in range(3)]
            for i in range(3)]


# ---------------------------------------------------------------------------

def sweep_all(include_C2=True):
    out = [sweep_C1(), sweep_C4(), sweep_C3(), sweep_C5(), sweep_C6()]
    if include_C2:
        out.append(sweep_C2())
    return out


def main():
    total_hits = 0
    for s in sweep_all():
        hits = s["hits"]
        total_hits += len(hits)
        extra = {k: v for k, v in s.items()
                 if k not in ("hits", "flags", "label")}
        print(f"{s['label']}: {extra}; hits={len(hits)}; "
              f"flags={len(s['flags'])}")
        for f in s["flags"]:
            print(f"   FLAG: {f}")
        for h in hits:
            print(f"   HIT: {h}")
    print(f"TOTAL genus<=1 hits across classes C1-C6: {total_hits}")


if __name__ == "__main__":
    main()
