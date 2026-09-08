"""THE ORIENTATION READING of the height system (entry 129; docs/attacks/A12-orientation.md).

For a class with every exponent 1, write w_X = eps_X e_X in {-1, 0, 1}^N (the signed exponent vectors: the
relations depend only on Z_X = prod_j rho_j^{2 w_{X,j}}).  Arithmetically w_{X,j} = 0 means p_j^2 divides the
offset d_X, and w_{X,j} = +-1 records which of pi_j, pibar_j the offset's Gaussian factor uses: its ORIENTATION
at p_j.  For two labels X, Y both nonzero at j, the binomial exponent at another column k is
    |d_k| = 2 if the pair FLIPS (w_{X,k} w_{Y,k} = -w_{X,j} w_{Y,j}: opposite relative orientation at k),
           = 1 if exactly one of them vanishes at k,
           = 0 if they agree (or both vanish),
so the row (B1) reads  2^t p_j^2 <= prod_{flip} p_k^2 prod_{one zero} p_k.  For three labels of a circuit, all
nonzero at j, the (T') coefficient at k is
    c_k = -2 if the three keep their mutual orientations at k and none vanishes (p_k joins p_j on the LEFT),
        = +2 if two of them flip relative to each other at k,
        =  0 otherwise,
so the row reads  p_j^2 prod_{agree} p_k^2 <= K prod_{flip} p_k^2.

THEOREM T1 (three never-disagreeing offsets).  If three labels of a circuit are all nonzero at column j and at
no other column do two of them flip relative to each other, the class is impossible: the row has no term on the
right, p_j^2 prod_{agree} p_k^2 <= K <= 4, while p_j >= 5.  Uniform in the number of primes and, with f-signs in
place of orientations, in the exponent shape.  Corollary: if no pair of labels ever flips, the class is
impossible (at any column three labels are nonzero by the prime-column lemma, and they form a circuit)."""
from itertools import combinations

from compute.height_system import system, CIRCUITS


def signed(cand):
    A, B, C, D, eA, eB, eC, eD = cand
    return [tuple(int(e) * int(x) for x in lab) for lab, e in ((A, eA), (B, eB), (C, eC), (D, eD))]


def flips(cand):
    """Per pair of labels: (columns where both are nonzero with relative sign +1, with relative sign -1)."""
    W = signed(cand)
    N = len(W[0])
    out = {}
    for X, Y in combinations(range(4), 2):
        pos = [j for j in range(N) if W[X][j] * W[Y][j] == 1]
        neg = [j for j in range(N) if W[X][j] * W[Y][j] == -1]
        out[(X, Y)] = (pos, neg)
    return out


def orientation_rows(cand):
    """The homogeneous coefficients of every row predicted from the orientations alone (all-ones boxes), keyed
    like system()'s relations: (column, circuit) -> {k: coefficient}."""
    W = signed(cand)
    N = len(W[0])
    pred = {}
    for j in range(N):
        col = [W[X][j] for X in range(4)]
        maximal = [X for X in range(4) if col[X] != 0]
        deficient = [X for X in range(4) if col[X] == 0]
        E = deficient[0] if deficient else None
        for name, c in CIRCUITS.items():
            involved = [X for X in range(4) if c[X] != 0]
            if E is not None and E in involved:
                X, Y = [Z for Z in involved if Z != E]
                aX, aY = c[X] * col[X], c[Y] * col[Y]       # the effective coefficients (sigma_X = eps_X s_X = w_{X,j} here)
                lam = -max(aX, aY, key=abs) / min(aX, aY, key=abs) if abs(aX) != abs(aY) else -aX / aY
                rel = col[X] * col[Y]
                coeff = {j: 2}
                for k in range(N):
                    if k == j:
                        continue
                    if W[X][k] and W[Y][k]:
                        dk = 2 if W[X][k] * W[Y][k] == -rel else 0
                    elif W[X][k] or W[Y][k]:
                        dk = 1
                    else:
                        dk = 0
                    coeff[k] = -(2 * dk) if abs(lam) == 2 else -dk
                pred[(j, name)] = ("binomial", coeff, int(abs(lam)))
            else:
                trip = involved
                coeff = {j: 2}
                for k in range(N):
                    if k == j:
                        continue
                    f = [-col[X] * W[X][k] for X in trip]
                    if all(v == f[0] for v in f) and f[0] != 0:
                        coeff[k] = 2
                    elif 1 in f and -1 in f:
                        coeff[k] = -2
                    else:
                        coeff[k] = 0
                pred[(j, name)] = ("trinomial", coeff, None)
    return pred


def check_reading(cand):
    """The orientation prediction against the height system's actual rows (version 3): True iff identical."""
    cols, ineqs, lower = system(cand, 3)
    pred = orientation_rows(cand)
    for c in cols:
        for r in c["relations"]:
            kind, coeff, lam = pred[(c["j"], r["circuit"])]
            if kind != r["kind"]:
                return False
            actual = {k: v for k, v in r["coeff"].items() if v}
            predicted = {k: v for k, v in coeff.items() if v}
            if actual != predicted:
                return False
            if kind == "binomial" and lam != abs(r["lam"]):
                return False
    return True


def t1(cand):
    """Theorem T1: some trinomial row has no flip column (no negative coefficient)."""
    for (j, name), (kind, coeff, lam) in orientation_rows(cand).items():
        if kind == "trinomial" and all(v >= 0 for v in coeff.values()):
            return True
    return False


def no_pair_flips(cand):
    return all(not (pos and neg) for pos, neg in flips(cand).values())
