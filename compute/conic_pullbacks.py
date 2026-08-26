"""Conic-image curves on the magic-squares surface X: exact pullback
analysis (docs/attacks/A7-curve-enumeration.md, conic layer).

For a smooth conic C in the Lucas plane, the reduced preimage on X splits
into components; genus bookkeeping needs the collision pattern of C with
the nine entry lines.  Everything is computable over Q:

  * lines i != j collide on C only at the arrangement point L_i ∩ L_j
    (rational), i.e. iff C passes through that multiple point;
  * a line is tangent to C iff disc(Q|_L) = 0, and if C also passes
    through an arrangement point on L, the tangency point is that point;
  * leftover ("free") intersection points come per line, as a rational
    point, a rational tangency, or a conjugate pair (irreducible
    quadratic) — conjugate points carry identical multiplicity vectors
    and count as TWO branch points sharing one matrix column.

Genus of components:  g = 1 + 2^(k-2) (r_eff - 4)  (k >= 2), where k is
the F_2-rank of the even-subset span of the mod-2 multiplicity vectors
and r_eff the number of Qbar-collision-points at which some surviving
character ramifies.

The module also generates candidate conics (through 5-subsets of the 8
triple points; tangent to 5-subsets of the 9 lines, via dual conics;
symmetric families) and reports every genus <= 1 hit.  IMPORTANT: an
irreducible conic lies in no difference line and no entry line, so its
entries are pairwise distinct, nonzero functions — a genus-0 hit would
be a NONDEGENERATE rational curve on X (a function-field magic square of
squares), and a genus-1 hit a nondegenerate elliptic family.

Run:  python3 -m compute.conic_pullbacks
"""

from fractions import Fraction
from itertools import combinations

from compute.curve_pullbacks import (ENTRY_LINES, ENTRY_NAMES, cross,
                                     multiple_points, norm_point)


# ---------------------------------------------------------------------------
# conics as symmetric matrices M (Q(x) = x^T M x), x = (c, u, v)

def conic_eval(M, p):
    return sum(M[i][j] * p[i] * p[j] for i in range(3) for j in range(3))


def conic_det(M):
    a, b, c0 = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c0 * (d * h - e * g)


def restrict_to_line(M, L):
    """Q restricted to the line L (covector): a binary quadratic form in a
    parametrization of L.  Returns (A, B, C) with A s^2 + B s t + C t^2,
    plus the two base points of the parametrization."""
    # find two points spanning the line
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
    A = conic_eval(M, P0)
    C = conic_eval(M, P1)
    B = (sum(M[i][j] * (P0[i] * P1[j] + P1[i] * P0[j])
             for i in range(3) for j in range(3)))
    return (A, B, C), P0, P1


def line_intersection_data(M, L):
    """How the conic meets line L: returns (kind, points) where kind in
    {'transversal-rational', 'tangent', 'conjugate-pair'}, and points are
    the rational intersection points found (as normalized tuples), with
    the tangency point when applicable."""
    (A, B, C), P0, P1 = restrict_to_line(M, L)
    disc = B * B - 4 * A * C
    pts = []

    def pt(s, t):
        s, t = Fraction(s), Fraction(t)
        den = s.denominator * t.denominator
        si, ti = int(s * den), int(t * den)
        return norm_point(tuple(si * a + ti * b for a, b in zip(P0, P1)))

    if disc == 0:
        # double root: rational
        if A == 0 and B == 0:
            return "tangent", [pt(1, 0)] if C != 0 else ("contained", [])
        if A == 0:
            return "tangent", [pt(1, 0)]  # root t/s ... handle below
        # root s/t = -B/(2A)
        return "tangent", [pt(Fraction(-B, 2 * A), 1)]
    # rational roots?
    r = _isqrt_exact(disc)
    if r is not None:
        if A == 0:
            roots = [(1, 0), (Fraction(-C, B), 1)] if B else [(1, 0)]
        else:
            roots = [(Fraction(-B + r, 2 * A), 1), (Fraction(-B - r, 2 * A), 1)]
        return "transversal-rational", [pt(s, t) for (s, t) in roots]
    return "conjugate-pair", []


def _isqrt_exact(q):
    """sqrt of a Fraction/int if it is a perfect square, else None."""
    q = Fraction(q)
    if q < 0:
        return None
    from math import isqrt
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fraction(rn, rd)
    return None


def analyze_conic(M, name=""):
    """Full pullback analysis of an irreducible conic (matrix M over Q)."""
    if conic_det(M) == 0:
        return {"name": name, "reducible": True}
    # collision columns: keyed by rational point or ('free', line, tag)
    columns = {}     # key -> {"weight": 1 or 2 (conjugate pair), "mults": {line: m}}

    def add(key, line, mult, weight=1):
        col = columns.setdefault(key, {"weight": weight, "mults": {}})
        col["mults"][line] = col["mults"].get(line, 0) + mult

    mpts = multiple_points()
    onC = {p: lines for p, lines in mpts.items() if conic_eval(M, p) == 0}
    for i, L in enumerate(ENTRY_LINES):
        kind, pts = line_intersection_data(M, L)
        if kind == "contained":
            return {"name": name, "degenerate_contained": True}
        arr_pts = [p for p in onC if i in onC[p]]
        if kind == "tangent":
            p = pts[0]
            add(("pt", p), i, 2)
        elif kind == "transversal-rational":
            for p in pts:
                add(("pt", p), i, 1)
        else:  # conjugate pair: cannot pass through rational arrangement pts
            # each of the two conjugate points gets multiplicity 1; they
            # share one column of weight 2 (identical Galois behavior)
            add(("pair", i), i, 1, weight=2)
    # sanity: arrangement points on C got their lines via the per-line pass
    # (a rational intersection point that is an arrangement point is the
    # same tuple, so columns merge automatically).
    # ---- F_2 analysis
    keys = sorted(columns, key=str)
    vecs = []
    for i in range(9):
        v = [columns[kkey]["mults"].get(i, 0) % 2 for kkey in keys]
        vecs.append(v)
    # even-subset span: row space of v_i + v_8 (i = 0..7)
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
    total_mult = sum(sum(c["mults"].values()) * c["weight"]
                     for c in columns.values())
    return {"name": name, "reducible": False, "k": k, "r_eff": r_eff,
            "genus": genus, "n_columns": len(keys),
            "n_arr_pts_on_C": len(onC), "total_mult_check": total_mult,
            "n_components": 2 ** (8 - k)}


# ---------------------------------------------------------------------------
# candidate generation

def conic_through(points):
    """Nullspace of the 'passes through these points' linear system; returns
    a matrix if the conic is unique (5 independent conditions), else None."""
    rows = []
    for (c, u, v) in points:
        rows.append([c * c, u * u, v * v, 2 * c * u, 2 * c * v, 2 * u * v])
    # exact nullspace over Q
    from fractions import Fraction as F
    m = [[F(x) for x in row] for row in rows]
    n = 6
    piv_cols = []
    r = 0
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
    if len(free) != 1:
        return None
    fc = free[0]
    sol = [F(0)] * n
    sol[fc] = F(1)
    for i, col in enumerate(piv_cols):
        sol[col] = -m[i][fc]
    den = 1
    for x in sol:
        den = den * x.denominator // _gcd(den, x.denominator)
    a, b, cc, d, e, f = [int(x * den) for x in sol]
    return [[a, d, e], [d, b, f], [e, f, cc]]


def _gcd(a, b):
    from math import gcd
    return gcd(a, b)


def adjugate(M):
    def minor(i, j):
        rows = [r for r in range(3) if r != i]
        cols = [c for c in range(3) if c != j]
        return (M[rows[0]][cols[0]] * M[rows[1]][cols[1]]
                - M[rows[0]][cols[1]] * M[rows[1]][cols[0]])
    return [[(-1) ** (i + j) * minor(j, i) for j in range(3)] for i in range(3)]


def conic_pencil(points):
    """2-dim nullspace for 4 point conditions: returns (M0, M1) or None."""
    from fractions import Fraction as F
    rows = [[F(x) for x in [c * c, u * u, v * v, 2 * c * u, 2 * c * v,
                            2 * u * v]] for (c, u, v) in points]
    m = [r[:] for r in rows]
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
    if len(free) != 2:
        return None
    sols = []
    for fc in free:
        sol = [F(0)] * n
        sol[fc] = F(1)
        for i, col in enumerate(piv_cols):
            sol[col] = -m[i][fc]
        den = 1
        for x in sol:
            den = den * x.denominator // _gcd(den, x.denominator)
        a, b, cc, d, e, f = [int(x * den) for x in sol]
        sols.append([[a, d, e], [d, b, f], [e, f, cc]])
    return sols[0], sols[1]


def pencil_tangency_conics(M0, M1):
    """Members of the pencil M0 + lam*M1 (plus M1 itself) that are tangent
    to at least one entry line, for RATIONAL lam: solve disc(lam) = 0."""
    out = []
    for L in ENTRY_LINES:
        (A0, B0, C0), _, _ = restrict_to_line(M0, L)
        (A1, B1, C1), _, _ = restrict_to_line(M1, L)
        # disc(lam) = (B0 + lam B1)^2 - 4 (A0 + lam A1)(C0 + lam C1)
        a = B1 * B1 - 4 * A1 * C1
        b = 2 * B0 * B1 - 4 * (A0 * C1 + A1 * C0)
        c = B0 * B0 - 4 * A0 * C0
        lams = []
        if a == 0:
            if b != 0:
                lams.append(Fraction(-c, b))
        else:
            r = _isqrt_exact(Fraction(b * b - 4 * a * c))
            if r is not None:
                lams += [Fraction(-b + r, 2 * a), Fraction(-b - r, 2 * a)]
        for lam in lams:
            den = lam.denominator
            num = lam.numerator
            M = [[M0[i][j] * den + num * M1[i][j] for j in range(3)]
                 for i in range(3)]
            out.append(M)
    out.append(M1)
    return out


def candidates():
    """Curated candidate conics: (name, matrix)."""
    out = []
    triples = [p for p, ls in multiple_points().items() if len(ls) == 3]
    for sub in combinations(triples, 5):
        M = conic_through(sub)
        if M is not None and conic_det(M) != 0:
            out.append((f"through-5-triples {sub}", M))
    # 4-triple pencils: members tangent to at least one line (rational lam)
    for sub in combinations(triples, 4):
        pen = conic_pencil(sub)
        if pen is None:
            continue
        for j, M in enumerate(pencil_tangency_conics(*pen)):
            if conic_det(M) != 0:
                out.append((f"pencil-4-triples {sub} #{j}", M))
    # tangent to 5 lines: dual conic through the 5 dual points
    for sub in combinations(range(9), 5):
        D = conic_through([ENTRY_LINES[i] for i in sub])
        if D is not None and conic_det(D) != 0:
            M = adjugate(D)
            if conic_det(M) != 0:
                out.append((f"tangent-to-5 {sub}", M))
    # symmetric families: alpha c^2 = u^2 + v^2 and alpha c^2 = u^2 - ...
    for num, den in [(1, 1), (2, 1), (1, 2), (4, 1), (9, 1), (1, 4),
                     (25, 16), (2, 9), (8, 9), (9, 8), (8, 1), (1, 8)]:
        M = [[-num, 0, 0], [0, den, 0], [0, 0, den]]
        out.append((f"u^2+v^2 = ({num}/{den}) c^2", M))
        M2 = [[-2 * num, 0, 0], [0, 2 * den, 0], [0, 0, den]]
        out.append((f"2u^2+v^2 = (2{num}/{den}) c^2", M2))
        M3 = [[-num, 0, 0], [0, 0, den], [0, den, 0]]
        out.append((f"2uv = ({num}/{den}) c^2", M3))
    return out


def main():
    hits = []
    n = 0
    for name, M in candidates():
        data = analyze_conic(M, name)
        if data.get("reducible"):
            continue
        n += 1
        if data["genus"] is not None and data["genus"] <= 1:
            hits.append(data)
            print(f"LOW GENUS: {name}: {data}")
    print(f"analyzed {n} irreducible candidate conics; "
          f"genus<=1 hits: {len(hits)}")
    # show the tangency showcase conic explicitly
    show = analyze_conic([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], "circle")
    print(f"u^2+v^2=c^2 control: {show}")


if __name__ == "__main__":
    main()
