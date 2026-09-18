"""The rational-cubic campaign through Lemma T, replayed in pure Python (sympy), for the verify suite.

A rational curve on X with cubic Lucas image is a birational map phi = (p:q:r): P^1 -> P^2 of degree 3 whose image is
eta*-integral (A8.11) and passes through >= 3 triple points (A8.15).  Move three of them to t = 0, 1, infinity; by Lemma T
(entry 151) the branch tangents there are integral lines through the points.  Point and tangency conditions are linear in
the 12 coefficients of (p, q, r) and the scalars lambda_1, lambda_inf (lambda_0 = 1); integrality is the identity
E(t) = T(p, q, r; p', q', r') = 0 with T the coordinate-free form of eta* times the nine lines.  For each D4-orbit
representative of (3-subset, admissible tangents) the theorem needs: every point of the integrality locus V(I) is a map of
rank <= 2 (onto a line), i.e. every 3x3 minor m of the coefficient matrix lies in the radical of I (Rabinowitsch:
1 in I + (1 - y m)), or I = 0 and the minors vanish identically, or the linear system is inconsistent.  All arithmetic is
over Q(sqrt3) realized as Q[r]/(r^2 - 3)."""
import itertools
from fractions import Fraction

import sympy as sp

r, t, y = sp.symbols("r t y")
AVARS = sp.symbols("a0:12")
c, u, v, dc, du, dv = sp.symbols("c u v dc du dv")
SQ3 = r  # the symbol r stands for sqrt(3); every polynomial is reduced modulo r^2 - 3

PTS = {"A0": (0, 1, 0), "A+": (-1, 1, 0), "A-": (1, 1, 0), "D+": (0, 1, 1), "D-": (0, 1, -1),
       "B0": (0, 0, 1), "B+": (1, 0, -1), "B-": (1, 0, 1)}


def dirs(name):
    """the admissible tangent lines at a triple point (Lemma T), each given by a second point on the line"""
    if name in ("A0", "A+", "A-"):
        return {"vert": (0, 0, 1), "diag+": (1, 0, 1), "diag-": (-1, 0, 1), "carrier": (1, 0, 0)}
    if name in ("B0", "B+", "B-"):
        return {"vert": (0, 1, 0), "diag+": (1, 1, 0), "diag-": (-1, 1, 0), "carrier": (1, 0, 0)}
    return {"vert": (0, 0, 1), "diag+": (1, 0, 1), "diag-": (-1, 0, 1), "s3+": (SQ3, 0, 3), "s3-": (-SQ3, 0, 3)}


def red(expr):
    """reduce a polynomial expression modulo r^2 - 3 (r = sqrt 3)"""
    return sp.rem(sp.Poly(sp.expand(expr), r), sp.Poly(r ** 2 - 3, r)).as_expr() if expr.has(r) else sp.expand(expr)


def T_form():
    """T(c,u,v; dc,du,dv) = Q_hom(c,u,v; u dc - c du, u dv - v du) / u^2, the coordinate-free form of eta* times the nine lines"""
    X = u * dc - c * du
    Y = u * dv - v * du
    Qh = 3 * c * v ** 2 * X ** 4 - 2 * v * (3 * c ** 2 + v ** 2 - u ** 2) * X ** 3 * Y + 3 * c * (c ** 2 + v ** 2 - u ** 2) * X ** 2 * Y ** 2 + c * (u ** 2 - c ** 2) * Y ** 4
    q, rem = sp.div(sp.Poly(sp.expand(Qh), u), sp.Poly(u ** 2, u))
    assert rem.is_zero
    return sp.Poly(q.as_expr(), c, u, v, dc, du, dv)


# D4 symmetry on the sub-cases
def _normalize(vec):
    vec = [sp.nsimplify(x) for x in vec]
    for x in vec:
        if x != 0:
            return tuple(red(sp.cancel(w / x)) if w != 0 else sp.Integer(0) for w in vec)
    return tuple(vec)


def _syms():
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            for swap in (False, True):
                M = sp.Matrix([[1, 0, 0], [0, e1, 0], [0, 0, e2]])
                if swap:
                    M = M * sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
                out.append(M)
    return out


SYMS = _syms()
PTNAME = {_normalize(P): n for n, P in PTS.items()}


def _line_form(P, W):
    P = sp.Matrix(P)
    W = sp.Matrix(W)
    return _normalize(list(P.cross(W)))


def subcase_key(cfg, choice):
    items = [(sp.Matrix(PTS[n]), sp.Matrix(dirs(n)[ch])) for n, ch in zip(cfg, choice)]
    keys = []
    for M in SYMS:
        lab = []
        for P, W in items:
            Pm = M * P
            Wm = M * W
            lab.append((PTNAME[_normalize(list(Pm))], str(_line_form(list(Pm), list(Wm)))))
        keys.append(tuple(sorted(lab)))
    return min(keys)


def subcases_and_representatives():
    subs = [(cfg, choice) for cfg in itertools.combinations(list(PTS), 3) for choice in itertools.product(*[list(dirs(n)) for n in cfg])]
    seen = {}
    reps = []
    for idx, (cfg, choice) in enumerate(subs):
        k = subcase_key(cfg, choice)
        if k not in seen:
            seen[k] = idx
            reps.append(idx)
    return subs, reps


# the linear family of parametrized maps of degree deg
def _unknowns(deg):
    nc = deg + 1
    names = ["p%d" % i for i in range(nc)] + ["q%d" % i for i in range(nc)] + ["r%d" % i for i in range(nc)] + ["l1", "linf"]
    unk = sp.symbols(names)
    return unk, unk[0:nc], unk[nc:2 * nc], unk[2 * nc:3 * nc], unk[3 * nc], unk[3 * nc + 1]


def _val(coefs, t0):
    return sum(coefs[i] * t0 ** i for i in range(len(coefs)))


def _der(coefs, t0):
    return sum(i * coefs[i] * t0 ** (i - 1) for i in range(1, len(coefs)))


def linear_family(cfg, choice, deg=3):
    """returns None if the linear system is inconsistent; else (particular solution, kernel basis) as lists over Q(sqrt3)"""
    UNK, P_, Q_, R_, L1, LINF = _unknowns(deg)
    eqs = []
    P0, P1, Pinf = [sp.Matrix(PTS[n]) for n in cfg]
    W0, W1, Winf = [sp.Matrix(dirs(n)[ch]) for n, ch in zip(cfg, choice)]
    for k, coefs in enumerate((P_, Q_, R_)):
        eqs.append(_val(coefs, 0) - P0[k])
        eqs.append(_val(coefs, 1) - L1 * P1[k])
        eqs.append(coefs[deg] - LINF * Pinf[k])
    eqs.append(sp.Matrix([list(P0), list(W0), [_der(P_, 0), _der(Q_, 0), _der(R_, 0)]]).det())
    eqs.append(sp.Matrix([list(P1), list(W1), [_der(P_, 1), _der(Q_, 1), _der(R_, 1)]]).det())
    eqs.append(sp.Matrix([list(Pinf), list(Winf), [P_[deg - 1], Q_[deg - 1], R_[deg - 1]]]).det())
    eqs = [red(sp.expand(e)) for e in eqs]
    A = sp.Matrix([[sp.Poly(e, *UNK).coeff_monomial(x) for x in UNK] for e in eqs])
    b = sp.Matrix([-sp.Poly(e, *UNK).coeff_monomial(1) for e in eqs])
    A = A.applyfunc(red)
    b = b.applyfunc(red)
    # solve over Q(sqrt3): sympy handles sqrt-free symbolic r as a symbol; use gauss with exact reduction
    aug = A.row_join(b)
    rref, pivots = _rref_q3(aug)
    ncol = A.shape[1]
    if ncol in pivots:
        return None
    part = [sp.Integer(0)] * ncol
    for i, pc in enumerate(pivots):
        part[pc] = rref[i, ncol]
    free = [j for j in range(ncol) if j not in pivots]
    ker = []
    for f in free:
        vec = [sp.Integer(0)] * ncol
        vec[f] = sp.Integer(1)
        for i, pc in enumerate(pivots):
            vec[pc] = red(-rref[i, f])
        ker.append(vec)
    return part, ker


def _inv_q3(x):
    """inverse of a + b r in Q(sqrt3)"""
    x = red(x)
    pa = sp.Poly(x, r)
    b = pa.coeff_monomial(r)
    a = pa.coeff_monomial(1)
    n = a * a - 3 * b * b
    assert n != 0
    return red((a - b * r) / n)


def _rref_q3(M):
    M = M.copy()
    rows, cols = M.shape
    pivots = []
    prow = 0
    for col in range(cols):
        piv = None
        for i in range(prow, rows):
            if red(M[i, col]) != 0:
                piv = i
                break
        if piv is None:
            continue
        M.row_swap(prow, piv)
        inv = _inv_q3(M[prow, col])
        M[prow, :] = (M[prow, :] * inv).applyfunc(red)
        for i in range(rows):
            if i != prow and red(M[i, col]) != 0:
                M[i, :] = (M[i, :] - M[i, col] * M[prow, :]).applyfunc(red)
        pivots.append(col)
        prow += 1
        if prow == rows:
            break
    return M, pivots


def integrality_polys(part, ker, Tp, deg=3):
    """the coefficients of E(t) = T(p,q,r; dp,dq,dr) as polynomials in the family parameters"""
    n = len(ker)
    nc = deg + 1
    avars = list(AVARS[:n])
    coefs = [red(part[i] + sum(avars[k] * ker[k][i] for k in range(n))) for i in range(3 * nc + 2)]
    p = sum(coefs[i] * t ** i for i in range(nc))
    q = sum(coefs[nc + i] * t ** i for i in range(nc))
    rr = sum(coefs[2 * nc + i] * t ** i for i in range(nc))
    dp, dq, dr = sp.diff(p, t), sp.diff(q, t), sp.diff(rr, t)
    E = sp.Integer(0)
    for (ec, eu, ev, edc, edu, edv), cval in Tp.terms():
        E += cval * p ** ec * q ** eu * rr ** ev * dp ** edc * dq ** edu * dr ** edv
    E = red(sp.expand(E))
    eqs = [red(x) for x in sp.Poly(E, t).all_coeffs()]
    eqs = [e for e in eqs if e != 0]
    return coefs, avars, eqs


def minors_of(coefs, deg=3):
    nc = deg + 1
    Mc = sp.Matrix([coefs[0:nc], coefs[nc:2 * nc], coefs[2 * nc:3 * nc]])
    return [red(Mc.extract([0, 1, 2], list(cols)).det()) for cols in itertools.combinations(range(nc), 3)]


def verdict(cfg, choice, Tp, deg=3, modulus=None):
    """'empty' | 'lines' (every integral member has rank <= 2) | 'CANDIDATE' (a rank-3 integral member may exist);
    with modulus = p the Rabinowitsch tests run over GF(p)[r]/(r^2-3) (a diagnostic, exact only over Q)"""
    fam = linear_family(cfg, choice, deg)
    if fam is None:
        return "empty", {"family_dim": -1}
    part, ker = fam
    coefs, avars, eqs = integrality_polys(part, ker, Tp, deg)
    mins = minors_of(coefs, deg)
    info = {"family_dim": len(ker), "n_eqs": len(eqs)}
    if not eqs:
        return ("lines" if all(m == 0 for m in mins) else "CANDIDATE"), info
    gens = eqs + [r ** 2 - 3]
    for m in mins:
        if m == 0:
            continue
        G = sp.groebner(gens + [1 - y * m], y, r, *avars, order="grevlex", **({"modulus": modulus} if modulus else {"domain": "QQ"}))
        if not (len(G.exprs) == 1 and G.exprs[0] == 1):
            return "CANDIDATE", dict(info, minor=str(m))
    return "lines", info
