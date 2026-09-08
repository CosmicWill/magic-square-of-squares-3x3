"""PATH 3 (R.13): THE HIERARCHY OF AN OPEN CLASS AND THE PEELING IDENTITY (entry 134).

Setting (A11/A12, all-ones boxes): labels with signed entries w_X in {-1, 0, 1}^N, split primes p_j = pi_j pibar_j,
z_X = prod_j pi_j^{2 w_{X,j}} (w = 0: the factor p_j), |z_X| = m = prod p_j.  The offsets are Im(z_X^2) and a class
is a solution iff, for the circuits F = (1, 1, -1, 0) and G = (1, -1, 0, -1), the Gaussian integer
    Y_c = sum_X c_X z_X^2
is real.  PEELING a prime p = p_j: with y_X = z_X^2 / pi_j^{4 w_{X,j}} (the configuration with p_j removed) and
P_+ = sum_{w_{X,j} = +1} c_X y_X, P_- = sum_{w_{X,j} = -1} c_X y_X, P_0 = sum_{w_{X,j} = 0} c_X y_X,
    Y_c = pi^4 P_+ + pibar^4 P_- + p^2 P_0,        and with W = P_+ - conj(P_-):
    Y_c - conj(Y_c) = pi^4 W - pibar^4 conj(W) + p^2 (P_0 - conj(P_0)),
an identity for every choice of frames (peeling_identity_tests).  Hence, for a solution,
  * four maxima at j (P_0 = 0): pi^4 W = pibar^4 conj(W), so W = r pibar^4 with r a NONZERO rational integer
    (the (T') statement of A11): the configuration with p_j removed, its labels of negative orientation at p_j
    conjugated and negated, has circuit sums r_F pibar^4, r_G pibar^4 -- a TWISTED configuration on N - 1 primes
    (Problem(N-1, pibar^4)); eliminating pi: W_F and W_G are rationally proportional, Im(W_F conj(W_G)) = 0;
  * a deficient label E at j (P_0 = c_E y_E): pibar^2 | W and Im(pi^2 W_1) = -c_E Im(y_E) with W_1 = W / pibar^2
    exactly (the first-order part is the height system's binomial; the second-order part is the deficient label's
    descended offset Im(y_E) = Im(z_E^2)/p^2, an element of the smaller support's D-set).
Peeling a second prime from the twisted configuration re-inserts the first (the twist pibar^4 = (pibar^2)^2 is a
square and distributes over the labels by the second prime's orientations), so the naive descent in the number of
primes stops after one step; what remains is the elimination (the class curve of the smaller frames, path 2).

The HIERARCHY of an open class: the linear programme of A11 admits an unbounded feasible region; forced_ratio is the
least value of max_j p_j / min_j p_j over it (entry 129), forcing_rows the rows binding at that optimum, rigid_rows
the rows whose slack log K - a.x is bounded on the region (an exact equation with finitely many values would
follow; expected none, the recession cone being full-dimensional), and frame_divisibilities the binomial rows
whose d-vector is supported on a single other column k: p_j^{2g} divides Im or Re of pi_k^{2d}, i.e. a component
c_k, s_k, c_k - s_k or c_k + s_k of the frame of p_k (they are pairwise coprime), so pi_k is a unit times a
rational integer modulo p_j^{2g}; chains of such divisibilities are what force the large ratios."""
import math
from fractions import Fraction
from itertools import combinations

from compute.height_system import system, _rows, CIRCUITS


def _lp(cand, version=3):
    import numpy as np
    cols, ineqs, lower = system(cand, version)
    n = len(lower)
    rows = _rows(n, ineqs, lower)
    A = np.array([a for a, K, name in rows], dtype=float)
    b = np.array([math.log(K) for a, K, name in rows], dtype=float)
    return cols, ineqs, lower, rows, A, b


def forced_ratio(cand, version=3):
    """(ratio, binding row names): the least max_j p_j / min_j p_j over the feasible region, None if infeasible."""
    import numpy as np
    from scipy.optimize import linprog
    cols, ineqs, lower, rows, A, b = _lp(cand, version)
    n = A.shape[1]
    m = len(rows)
    # variables x_0..x_{n-1}, u, l; minimise u - l; A x <= b; x_j - u <= 0; -x_j + l <= 0
    A2 = np.zeros((m + 2 * n, n + 2))
    A2[:m, :n] = A
    b2 = np.concatenate([b, np.zeros(2 * n)])
    for j in range(n):
        A2[m + j, j] = 1; A2[m + j, n] = -1
        A2[m + n + j, j] = -1; A2[m + n + j, n + 1] = 1
    c = np.zeros(n + 2); c[n] = 1; c[n + 1] = -1
    res = linprog(c, A_ub=A2, b_ub=b2, bounds=[(None, None)] * (n + 2), method="highs")
    if res.status == 2:
        return None, []
    if res.status != 0:
        return math.inf, []
    marg = res.ineqlin.marginals[:m]
    binding = [rows[i][2] for i in range(m) if abs(marg[i]) > 1e-9]
    return math.exp(res.fun), binding


def rigid_rows(cand, version=3):
    """{row name: exact-ish maximal slack} for the rows whose slack is bounded on the feasible region."""
    import numpy as np
    from scipy.optimize import linprog
    cols, ineqs, lower, rows, A, b = _lp(cand, version)
    n = A.shape[1]
    out = {}
    for i, (a, K, name) in enumerate(rows[:len(ineqs)]):
        res = linprog(np.array(a, dtype=float), A_ub=A, b_ub=b, bounds=[(None, None)] * n, method="highs")
        if res.status == 0:
            out[name] = math.log(K) - res.fun
        elif res.status == 2:
            return None
    return out


def frame_divisibilities(cand, version=3):
    """[(j, k, d_k, integer, lam, g)]: binomial rows of column j whose d is supported on column k alone."""
    cols, ineqs, lower = system(cand, version)
    out = []
    for c in cols:
        for r in c["relations"]:
            if r["kind"] != "binomial":
                continue
            support = [k for k, v in r["d"].items() if v]
            if len(support) == 1:
                k = support[0]
                out.append((c["j"], k, r["d"][k], r["integer"], r["lam"], c["g"]))
    return out


def chains(cand, version=3):
    """The longest chain j_0 -> j_1 -> ... in the frame-divisibility digraph (edge j -> k: p_j^{2g} divides a
    component of pi_k's frame), and the digraph's edges."""
    edges = {}
    for j, k, dk, integer, lam, g in frame_divisibilities(cand, version):
        edges.setdefault(j, set()).add(k)
    best = []

    def walk(path):
        nonlocal best
        if len(path) > len(best):
            best = list(path)
        for k in edges.get(path[-1], ()):
            if k not in path:
                walk(path + [k])
    for j in edges:
        walk([j])
    return best, {j: sorted(v) for j, v in edges.items()}


# ---------------------------------------------------------------- the peeling identity, on genuine frames

def _gmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def _gpow(z, n):
    r = (1, 0)
    for _ in range(n):
        r = _gmul(r, z)
    return r


def _gconj(z):
    return (z[0], -z[1])


def _gadd(z, w):
    return (z[0] + w[0], z[1] + w[1])


def _gscale(c, z):
    return (c * z[0], c * z[1])


def configuration(W, pis, ps):
    """z_X^2 for signed labels W (rows w_X) and frames pis (pi_j = (c, s)), ps the primes."""
    out = []
    for w in W:
        z2 = (1, 0)
        for j, wj in enumerate(w):
            if wj == 1:
                z2 = _gmul(z2, _gpow(pis[j], 4))
            elif wj == -1:
                z2 = _gmul(z2, _gpow(_gconj(pis[j]), 4))
            else:
                z2 = _gscale(ps[j] ** 2, z2)
        out.append(z2)
    return out


def peel(W, pis, ps, j, c):
    """(Y, P_plus, P_minus, P_0, Wt) for circuit c at column j: Y = sum c_X z_X^2, and the parts with p_j removed."""
    z2 = configuration(W, pis, ps)
    Y = (0, 0)
    for X in range(4):
        Y = _gadd(Y, _gscale(c[X], z2[X]))
    Pp = Pm = P0 = (0, 0)
    for X in range(4):
        w = W[X][j]
        if w == 1:
            y = _gmul(z2[X], _gpow(_gconj(pis[j]), 4)); y = (y[0] // ps[j] ** 4, y[1] // ps[j] ** 4)      # z^2 / pi^4 = z^2 pibar^4 / p^4
            Pp = _gadd(Pp, _gscale(c[X], y))
        elif w == -1:
            y = _gmul(z2[X], _gpow(pis[j], 4)); y = (y[0] // ps[j] ** 4, y[1] // ps[j] ** 4)
            Pm = _gadd(Pm, _gscale(c[X], y))
        else:
            y = (z2[X][0] // ps[j] ** 2, z2[X][1] // ps[j] ** 2)
            P0 = _gadd(P0, _gscale(c[X], y))
    Wt = _gadd(Pp, _gscale(-1, _gconj(Pm)))
    return Y, Pp, Pm, P0, Wt


def peeling_identity_tests(trials=200, seed=1):
    """Checks, on random signed labels and random genuine frames, the exact identities
    Y = pi^4 P_+ + pibar^4 P_- + p^2 P_0  and  Y - conj(Y) = pi^4 W - pibar^4 conj(W) + p^2 (P_0 - conj(P_0)),
    for every column and both circuits.  Returns the number of identities checked."""
    import random
    from compute.height_search import split_primes, two_squares
    rng = random.Random(seed)
    primes = split_primes(400)
    frames = {p: two_squares(p) for p in primes}
    checked = 0
    for _ in range(trials):
        N = rng.choice([2, 3, 4, 5])
        ps = rng.sample(primes, N)
        pis = [frames[p] for p in ps]
        W = [[rng.choice([-1, 0, 1]) for _ in range(N)] for _ in range(4)]
        for cname, c in (("F", (1, 1, -1, 0)), ("G", (1, -1, 0, -1))):
            for j in range(N):
                Y, Pp, Pm, P0, Wt = peel(W, pis, ps, j, c)
                pi4, pib4 = _gpow(pis[j], 4), _gpow(_gconj(pis[j]), 4)
                rhs = _gadd(_gadd(_gmul(pi4, Pp), _gmul(pib4, Pm)), _gscale(ps[j] ** 2, P0))
                if rhs != Y:
                    raise AssertionError(("peeling", W, ps, j, cname))
                lhs2 = _gadd(Y, _gscale(-1, _gconj(Y)))
                rhs2 = _gadd(_gadd(_gmul(pi4, Wt), _gscale(-1, _gmul(pib4, _gconj(Wt)))), _gscale(ps[j] ** 2, _gadd(P0, _gscale(-1, _gconj(P0)))))
                if rhs2 != lhs2:
                    raise AssertionError(("conjugate peeling", W, ps, j, cname))
                checked += 2
    return checked


def analyse(cand, version=3):
    """The hierarchy record of a class."""
    ratio, binding = forced_ratio(cand, version)
    rig = rigid_rows(cand, version)
    fd = frame_divisibilities(cand, version)
    chain, edges = chains(cand, version)
    return {"forced_ratio": ratio, "binding": binding, "rigid": rig, "n_rigid": None if rig is None else len(rig),
            "frame_divisibilities": [list(x) for x in fd], "chain": chain, "chain_length": len(chain), "edges": edges,
            "binding_single_frame": [name for name in binding if any(f"{j}:" in name and name.split(":")[0] == str(j) for j, k, *_ in fd)]}
