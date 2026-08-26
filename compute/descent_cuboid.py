"""The cuboid positive control for the descent engine (M11-B, A8 §4).

The perfect-cuboid surface X_pc in P^6 (y_i^2 = x_j^2 + x_k^2,
z^2 = x_1^2 + x_2^2 + x_3^2) is a (Z/2)^4 cover of P^2_(x1:x2:x3),
branched over FOUR CONICS, all irreducible over Q:

    chart x_1 = 1, (c, v) := (x_2, x_3):
    Q1 = c^2 + v^2        (y_1; a line pair over Qbar, vertex (1:0:0))
    Q2 = v^2 + 1          (y_2; line pair, vertex (0:1:0))
    Q3 = c^2 + 1          (y_3; line pair, vertex (0:0:1))
    Q4 = c^2 + v^2 + 1    (z;  the smooth conic)

Its 48 A_1 nodes sit over the three line-pair vertices (8 each) and
the six tangency points of Q4 with Q1, Q2, Q3 (4 each) -- all
codimension >= 2, so exactly as in Theorem A8.1 the eigenspace V_T of
a character T <= {1,2,3,4} is cut out by divisorial conditions:

  * along Q_j: with eps_j = [j in T] and adapted coordinates (q, v)
    (or (q, c) for Q2, which is c-free), ord_{Q_j} of the adapted
    coefficient combos >= p_j + ceil((eps_j - k)/2), where
    p_j = floor((m - eps_j)/2) is the permitted pole depth;
  * along x_1 = 0 (etale): a pole of order up to |T| is permitted,
    because the descended form is  omega * prod_T(root_i) / x_1^|T|.

BTVA computed h^0(X_pc, hat-S^2 Omega^1) = 13 by Magma module algebra
and listed the 13 generators (their Table 1).  Their characters give
the fingerprint this engine must reproduce:

    dim V_T  =  3 (T = {}),  3 ({4}),  3 ({1,2,3}),
                1 ({1,2}), 1 ({1,3}), 1 ({2,3}),  1 ({1,2,3,4}),
                0 (the other nine characters);   total 13.

Their generators also descend to explicit plane differentials, giving
element-level membership tests, e.g.

    omega_4 |-> dc^2/Q3 - dv^2/Q2          in V_{4},
    omega_7 |-> (Q2 dc^2 - 2cv dc dv + Q3 dv^2)/Q4   in V_{1,2,3}.

Run:  python3 -m compute.descent_cuboid
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb

from compute.descent_differentials import (ceil_div, lin_add, lin_chart2,
                                           lin_scale_poly, lin_zero,
                                           nullspace_dim,
                                           nullspace_dim_modp)

# branch conics as constant polynomials {(i,j): coeff} in (c, v),
# with (reduction variable, q_c, q_v) data
CONICS = {
    1: ({(2, 0): F(1), (0, 2): F(1)}, "c"),               # c^2 + v^2
    2: ({(0, 2): F(1), (0, 0): F(1)}, "v"),               # v^2 + 1
    3: ({(2, 0): F(1), (0, 0): F(1)}, "c"),               # c^2 + 1
    4: ({(2, 0): F(1), (0, 2): F(1), (0, 0): F(1)}, "c"),  # c^2+v^2+1
}


def _partials(q):
    qc, qv = {}, {}
    for (i, j), val in q.items():
        if i:
            qc[(i - 1, j)] = qc.get((i - 1, j), F(0)) + i * val
        if j:
            qv[(i, j - 1)] = qv.get((i, j - 1), F(0)) + j * val
    return ({k: v for k, v in qc.items() if v},
            {k: v for k, v in qv.items() if v})


def _ppow(p, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        nxt = {}
        for (i1, j1), v1 in out.items():
            for (i2, j2), v2 in p.items():
                k = (i1 + i2, j1 + j2)
                nxt[k] = nxt.get(k, F(0)) + v1 * v2
        out = {k: v for k, v in nxt.items() if v}
        if not out:
            return {}
    return out


def _pneg(p):
    return {k: -v for k, v in p.items()}


def lin_reduce_mod(P, q, var):
    """Remainder of a linear polynomial P modulo the conic q, which is
    monic of degree 2 in ``var`` ('c' or 'v'): q = var^2 + rest."""
    rest = _pneg({k: v for k, v in q.items()
                  if (k[0] if var == "c" else k[1]) < 2})
    # var^2 == rest (mod q)
    P = {k: dict(r) for k, r in P.items()}
    changed = True
    while changed:
        changed = False
        for (i, j) in sorted(P, reverse=True):
            deg = i if var == "c" else j
            if deg < 2:
                continue
            row = P.pop((i, j))
            base = (i - 2, j) if var == "c" else (i, j - 2)
            for (di, dj), val in rest.items():
                k = (base[0] + di, base[1] + dj)
                tgt = P.setdefault(k, {})
                for u, x in row.items():
                    tgt[u] = tgt.get(u, F(0)) + x * val
                    if tgt[u] == 0:
                        del tgt[u]
                if not tgt:
                    del P[k]
            changed = True
            break
    return {k: r for k, r in P.items() if r}


def cuboid_eigenspace_dim(T, m, dN=None, return_basis=False, modp=False):
    """dim V_T on the cuboid surface at symmetric degree m (modp=True:
    nullity mod MODP_PRIME -- an upper bound; 0 proves exact 0)."""
    T = set(T)
    eps = {j: (1 if j in T else 0) for j in CONICS}
    pj = {j: (m - eps[j]) // 2 for j in CONICS}
    dD = 2 * sum(pj.values())            # each conic has degree 2
    if dN is None:
        dN = dD + m + 2
    monos = [(i, j) for i in range(dN + 1) for j in range(dN + 1 - i)]
    unknowns = [(i, mono) for i in range(m + 1) for mono in monos]
    uidx = {u: t for t, u in enumerate(unknowns)}
    N = []
    for i in range(m + 1):
        N.append({mono: {uidx[(i, mono)]: F(1)} for mono in monos})

    rows = []

    def add_zero(linpoly):
        for _, row in linpoly.items():
            if row:
                rows.append(row)

    for j, (q, var) in CONICS.items():
        e, p = eps[j], pj[j]
        qc, qv = _partials(q)
        for k in range(m + 1):
            t = p + ceil_div(e - k, 2)
            if t <= 0:
                continue
            assert t == 1, "m > 3 needs iterated reduction"
            # adapted combo of numerators (multiplied through by the
            # m-th power of the unit partial):
            B = lin_zero()
            if var == "c":
                # B_k = sum_{i>=k} C(i,k) (-qv)^(i-k) qc^(m-i) N_i
                for i in range(k, m + 1):
                    c1 = _ppow(_pneg(qv), i - k)
                    c2 = _ppow(qc, m - i)
                    coefpoly = {}
                    for (a1, b1), v1 in c1.items():
                        for (a2, b2), v2 in c2.items():
                            kk = (a1 + a2, b1 + b2)
                            coefpoly[kk] = coefpoly.get(kk, F(0)) + v1 * v2
                    coefpoly = {kk: vv for kk, vv in coefpoly.items() if vv}
                    if not coefpoly:
                        continue
                    B = lin_add(B, lin_scale_poly(
                        N[i], {kk: F(comb(i, k)) * vv
                               for kk, vv in coefpoly.items()}))
            else:
                # B'_k = sum_{i<=m-k} C(m-i,k)(-qc)^(m-i-k) qv^i N_i
                for i in range(0, m - k + 1):
                    c1 = _ppow(_pneg(qc), m - i - k)
                    c2 = _ppow(qv, i)
                    coefpoly = {}
                    for (a1, b1), v1 in c1.items():
                        for (a2, b2), v2 in c2.items():
                            kk = (a1 + a2, b1 + b2)
                            coefpoly[kk] = coefpoly.get(kk, F(0)) + v1 * v2
                    coefpoly = {kk: vv for kk, vv in coefpoly.items() if vv}
                    if not coefpoly:
                        continue
                    B = lin_add(B, lin_scale_poly(
                        N[i], {kk: F(comb(m - i, k)) * vv
                               for kk, vv in coefpoly.items()}))
            add_zero(lin_reduce_mod(B, q, var))

    # chart-2 regularity along x_1 = 0 with pole allowance |T|
    for t in range(m + 1):
        Phi = lin_zero()
        for i in range(0, m - t + 1):
            Ni2 = lin_chart2(N[i], dN)
            term = lin_scale_poly(Ni2, {(0, m - i - t): F(1)})
            Phi = lin_add(Phi, term,
                          F(comb(m - i, t)) * F(-1) ** (m - i - t)
                          * F(-1) ** i)
        K = 2 * m - t + dN - dD - len(T)
        if K <= 0:
            continue
        for (yi, zj), row in Phi.items():
            if yi < K and row:
                rows.append(row)

    if modp:
        assert not return_basis
        return nullspace_dim_modp(rows, len(unknowns))
    dim, basis = nullspace_dim(rows, len(unknowns),
                               return_basis=return_basis)
    if return_basis:
        return dim, basis, unknowns, dN
    return dim


# ---------------------------------------------------------------------------
# element-level membership tests from BTVA Table 1 (descended forms)

def _in_space(T, m, numerators):
    """Is eta = sum numerators[i] dc^i dv^(m-i) / prod Q_j^(p_j) in V_T?
    Checked by running the same row system on the concrete vector."""
    dim, basis, unknowns, dN = cuboid_eigenspace_dim(T, m,
                                                     return_basis=True)
    vec = {}
    for i, P in enumerate(numerators):
        for mono, val in P.items():
            vec[(i, mono)] = F(val)
    if any(mono[0] + mono[1] > dN for (_, mono) in vec):
        return False, dim
    # solve: is vec in span(basis)?
    idx = {u: t for t, u in enumerate(unknowns)}
    target = [F(0)] * len(unknowns)
    for u, val in vec.items():
        target[idx[u]] = val
    # Gaussian: reduce target against basis vectors
    mat = [b[:] for b in basis]
    piv = []
    for r, b in enumerate(mat):
        col = next((cidx for cidx, x in enumerate(b) if x != 0), None)
        if col is None:
            continue
        piv.append((col, r))
        for r2 in range(len(mat)):
            if r2 != r and mat[r2][col] != 0:
                f = mat[r2][col] / b[col]
                mat[r2] = [x - f * y for x, y in zip(mat[r2], b)]
    for col, r in piv:
        if target[col] != 0:
            f = target[col] / mat[r][col]
            target = [x - f * y for x, y in zip(target, mat[r])]
    return all(x == 0 for x in target), dim


def table1_membership():
    """The descended BTVA Table-1 elements that are cleanly expressible
    in chart 1, as membership tests.  Numerators are over the standard
    denominator prod_{j not in T} Q_j (m = 2, so p_j = 1 - eps_j)."""
    Q1 = {(2, 0): 1, (0, 2): 1}
    Q2 = {(0, 2): 1, (0, 0): 1}
    Q3 = {(2, 0): 1, (0, 0): 1}

    def mul(p, q):
        out = {}
        for (i1, j1), v1 in p.items():
            for (i2, j2), v2 in q.items():
                k = (i1 + i2, j1 + j2)
                out[k] = out.get(k, 0) + v1 * v2
        return {k: v for k, v in out.items() if v}

    tests = []
    # omega_4 -> dc^2/Q3 - dv^2/Q2; denominator Q1 Q2 Q3:
    tests.append(("omega4", (4,),
                  [_neg(mul(Q1, Q3)), {}, mul(Q1, Q2)]))
    # omega_7 -> (Q2 dc^2 - 2cv dc dv + Q3 dv^2)/Q4; denominator Q4:
    tests.append(("omega7", (1, 2, 3),
                  [dict(Q3), {(1, 1): -2}, dict(Q2)]))
    # c*omega_7 and v*omega_7 (x2, x3 times omega_7):
    tests.append(("c*omega7", (1, 2, 3),
                  [_shift(Q3, 1, 0), {(2, 1): -2}, _shift(Q2, 1, 0)]))
    tests.append(("v*omega7", (1, 2, 3),
                  [_shift(Q3, 0, 1), {(1, 2): -2}, _shift(Q2, 0, 1)]))
    return tests


def _neg(p):
    return {k: -v for k, v in p.items()}


def _shift(p, di, dj):
    return {(i + di, j + dj): v for (i, j), v in p.items()}


EXPECTED_M2 = {
    frozenset(): 3, frozenset({4}): 3, frozenset({1, 2, 3}): 3,
    frozenset({1, 2}): 1, frozenset({1, 3}): 1, frozenset({2, 3}): 1,
    frozenset({1, 2, 3, 4}): 1,
}


def spectrum(m, saturate=True):
    out = {}
    for size in range(5):
        for T in combinations((1, 2, 3, 4), size):
            d = cuboid_eigenspace_dim(T, m)
            if saturate:
                pjsum = sum((m - (1 if j in T else 0)) // 2
                            for j in CONICS)
                d2 = cuboid_eigenspace_dim(T, m, dN=2 * pjsum + m + 4)
                assert d == d2, f"not saturated at {T}: {d} vs {d2}"
            out[frozenset(T)] = d
    return out


def main():
    spec = spectrum(2)
    total = sum(spec.values())
    for T, d in sorted(spec.items(), key=lambda kv: (len(kv[0]),
                                                     sorted(kv[0]))):
        if d:
            print(f"  V_{sorted(T) if T else '{}'} = {d}")
    print(f"h^0(X_pc - nodes, S^2 Omega^1) = {total}  (BTVA: 13)")
    want = {T: EXPECTED_M2.get(T, 0) for T in spec}
    print("fingerprint match:", spec == want)
    print("Table-1 membership:")
    for name, T, nums in table1_membership():
        ok, dim = _in_space(T, 2, nums)
        print(f"  {name} in V_{sorted(T)} (dim {dim}): {ok}")


if __name__ == "__main__":
    main()
