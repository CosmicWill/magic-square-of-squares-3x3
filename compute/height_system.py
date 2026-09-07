"""THE HEIGHT SYSTEM of an open class (entry 123): the unit congruences of A10 (CP.3) turned into
exact divisibilities and prime inequalities, sharpened in three ways over CP.4.

Setting (doc 2.49, A10 section 1).  Labels A, B, C, D with entries e_{X,j}, signs eps_X; primes
p_j = pi_j pibar_j, rho_j = pi_j / pibar_j, Z_X = prod_j rho_j^{2 eps_X e_{X,j}}, s(Z) = Z - 1/Z; the
additive relations are F = s(Z_A) + s(Z_B) - s(Z_C) = 0 and G = s(Z_A) - s(Z_B) - s(Z_D) = 0.
Fix a column j (prime p = p_j, pi = pi_j), M = max_X |e_{X,j}|; a deficient label E has |e_{E,j}| = M - g
(g >= 1), the others are maximal.  For a maximal X put s_X = sgn(e_{X,j}), sigma_X = eps_X s_X and
U_X = prod_{k != j} rho_k^{2 f_{X,k}} with f_{X,k} = -s_X e_{X,k}.  Then (CP.3, both signs of eps e)
    pi^{2M} s(Z_X) = -sigma_X pibar^{2M} U_X + O(pi^{4M})        (X maximal),
    pi^{2M} s(Z_E) in (pi^{2g})                                   (E deficient),
so each circuit F, G, F+G, F-G of the two relations gives, after division by -pibar^{2M},
    sum_X c_X sigma_X U_X = 0   modulo pi^{4M} (three maximal labels: a TRINOMIAL)
                          or   modulo pi^{2g}  (the deficient label dropped: a BINOMIAL).

Binomial (X, Y), coefficients a_X, a_Y in {+-1, +-2}, |a_X| >= |a_Y|:  U_Y / U_X = lambda := -a_X / a_Y
modulo pi^{2g}.  With d = f_Y - f_X,  U_Y / U_X = A / Abar,  A = prod_{d_k > 0} pi_k^{2 d_k} prod_{d_k < 0}
pibar_k^{2 |d_k|},  |A| = P = prod p_k^{|d_k|}; A is neither real nor imaginary (else U_Y = +-U_X, all
d_k = 0 by unique factorization in Z[i], and X = +-Y).
  lambda = +1:  A - Abar = 2i Im(A) in (pi^{2g}) with Im(A) a rational integer, so p^{2g} | Im(A);
                every pi_k^2 is +-1 mod 4, so A is +-1 mod 4 and 4 | Im(A) (8 | Im(A) when every d_k is
                even).  Hence  2^t p^{2g} <= |Im A| <= P,  t = 2 or 3.                            (B1)
  lambda = -1:  A + Abar = 2 Re(A): p^{2g} | Re(A) != 0,  p^{2g} <= P.                           (B1')
  lambda = +-2: p^{2g} | N(A - lambda Abar) = 5 P^2 - 2 lambda Re(A^2), nonzero,  <= 9 P^2.      (B2)
Trinomial (X, Y, Z), coefficients a with sum |a| = K in {3, 4}: multiply by the common denominator and
remove the common Gaussian factor: T_X = prod_{k != j} pi_k^{2(f_{X,k} - min f)} pibar_k^{2(max f - f_{X,k})},
all of absolute value Q = prod p_k^{r_k}, r_k = max_Y f_{Y,k} - min_Y f_{Y,k}; S = sum a_X T_X = 0 mod
pi^{4M}.  S != 0: with coefficients +-1, +-1, +-1 a vanishing sum of three numbers of equal modulus is
an equilateral triangle, a ratio e^{+-i pi/3} outside Q(i); with 2, +-1, +-1 it forces the two unit-
coefficient terms to coincide, i.e. two labels equal up to sign.  Hence  p^{2M} <= |S| <= K Q.     (T)
Coupling: |lambda| = 1 binomials of DIFFERENT columns that constrain the same integer (same kind Im/Re
and the same d up to global sign) multiply: prod_j p_j^{2 g_j} divides it.                          (C)
CP.2 lower bounds: an A/B-deficit prime is >= 5, a C/D-deficit prime is 1 mod 8 hence >= 17, a
four-maxima prime admits t with t, 1+t, 1-t nonzero squares, which 5, 13, 17 do not, hence >= 29.

Every inequality is  prod_j p_j^{a_j} <= K  with integers a_j and a rational K, i.e. sum a_j x_j <= log K
in x_j = log p_j.  The linear programme in x decides, per class and per prime: INFEASIBLE (no primes
satisfy the necessary conditions: the class is impossible), CAPPED (an explicit bound on p_j), or
UNBOUNDED (a positive recession direction: these inequalities alone give no cap).  Every verdict
carries an exact rational certificate (Farkas multipliers or the direction) verified in exact
arithmetic; only the reported cap value is a floating-point evaluation of an exact expression.
"""
import math
from fractions import Fraction
from itertools import combinations

from compute.prime_column import column_certificate

CIRCUITS = {"F": (1, 1, -1, 0), "G": (1, -1, 0, -1), "F+G": (2, 0, -1, -1), "F-G": (0, 2, -1, 1)}
LOWER_BOUND = {"A": 5, "B": 5, "C": 17, "D": 17, "*": 29}


def sgn(x):
    return (x > 0) - (x < 0)


def column(cand, j, version=2):
    """The relations of column j: the binomials and trinomials with their exact data.
    version 1 = entry 123 (trinomial bound |S_1| >= 1); version 2 = entry 124 (the reality sharpening (T'))."""
    labels, eps = [tuple(int(x) for x in lab) for lab in cand[:4]], [int(x) for x in cand[4:]]
    col = [lab[j] for lab in labels]
    M = max(abs(e) for e in col)
    if M == 0:
        raise ValueError("zero column")
    maximal = [X for X in range(4) if abs(col[X]) == M]
    if len(maximal) < 3:
        raise ValueError("the column violates the prime-column lemma")
    deficient = next((X for X in range(4) if abs(col[X]) < M), None)
    g = None if deficient is None else M - abs(col[deficient])
    role = "*" if deficient is None else "ABCD"[deficient]
    n = len(labels[0])
    others = [k for k in range(n) if k != j]
    s = {X: sgn(col[X]) for X in maximal}
    f = {X: {k: -s[X] * labels[X][k] for k in others} for X in maximal}
    sigma = {X: eps[X] * s[X] for X in maximal}
    rels = []
    for name, c in CIRCUITS.items():
        involved = [X for X in range(4) if c[X] != 0]
        if deficient is not None and deficient in involved:
            X, Y = [Z for Z in involved if Z != deficient]
            aX, aY = c[X] * sigma[X], c[Y] * sigma[Y]
            if abs(aX) < abs(aY):
                X, Y, aX, aY = Y, X, aY, aX
            lam = Fraction(-aX, aY)
            assert lam.denominator == 1 and abs(lam) in (1, 2)
            lam = int(lam)
            d = {k: f[Y][k] - f[X][k] for k in others}
            if not any(d.values()):
                raise ValueError("two maximal labels equal up to sign")
            absd = {k: abs(v) for k, v in d.items()}
            if abs(lam) == 1:
                integer = "Im" if lam == 1 else "Re"
                two_adic = 0 if lam == -1 else (3 if all(v % 2 == 0 for v in d.values()) else 2)
                coeff = {j: 2 * g, **{k: -absd[k] for k in others}}
                K = Fraction(1, 2 ** two_adic)
            else:
                integer, two_adic = "N2", 0
                coeff = {j: 2 * g, **{k: -2 * absd[k] for k in others}}
                K = Fraction(9)
            rels.append(dict(kind="binomial", circuit=name, pair=[X, Y], coeffs=[aX, aY], lam=lam, d=d,
                             modulus=2 * g, integer=integer, two_adic=two_adic, coeff=coeff, K=K))
        else:
            trip = involved
            a = {X: c[X] * sigma[X] for X in trip}
            for X, Y in combinations(trip, 2):
                if all(f[X][k] == f[Y][k] for k in others):
                    raise ValueError("two maximal labels equal up to sign")
            fmax = {k: max(f[X][k] for X in trip) for k in others}
            fmin = {k: min(f[X][k] for X in trip) for k in others}
            r = {k: fmax[k] - fmin[k] for k in others}
            K = sum(abs(v) for v in a.values())
            if version >= 2:
                # (T'): S = pi^{4M} S_1 with S_1 Gbar real (the exact identity pibar^{4M} W = pi^{4M} Wbar), so
                # |S_1| >= prod p_k^{|fmax_k + fmin_k|} and p_j^{2M} <= K prod p_k^{2 min(fmax_k, -fmin_k)}
                coeff = {j: 2 * M, **{k: -2 * min(fmax[k], -fmin[k]) for k in others}}
            else:
                coeff = {j: 2 * M, **{k: -r[k] for k in others}}
            rels.append(dict(kind="trinomial", circuit=name, labels=trip, coeffs=a, r=r, fmax=fmax, fmin=fmin, modulus=4 * M, K=Fraction(K), coeff=coeff))
    return dict(j=j, M=M, g=g, role=role, deficient=deficient, maximal=maximal, s=s, sigma=sigma, f=f, relations=rels)


def system(cand, version=2):
    """All inequalities of a class: [(coeff dict, K, name)] meaning prod p_j^{coeff_j} <= K, and the
    CP.2 lower bounds per prime.  version 1 reproduces entry 123, version 2 adds the reality sharpening."""
    if column_certificate(cand[:4]) is not None:
        raise ValueError("the class fails the prime-column lemma")
    n = len(cand[0])
    cols = [column(cand, j, version) for j in range(n)]
    ineqs = []
    groups = {}
    for c in cols:
        for r in c["relations"]:
            ineqs.append((r["coeff"], r["K"], f"{c['j']}:{r['circuit']}"))
            if r["kind"] == "binomial" and abs(r["lam"]) == 1:
                key = tuple(sorted((k, v) for k, v in r["d"].items() if v))
                if key[0][1] < 0:
                    key = tuple((k, -v) for k, v in key)
                groups.setdefault((r["integer"], key), {})
                groups[(r["integer"], key)][c["j"]] = max(groups[(r["integer"], key)].get(c["j"], 0), c["g"])
    for (integer, key), byj in groups.items():
        if len(byj) >= 2:
            coeff = {j: 2 * g for j, g in byj.items()}
            for k, v in key:
                coeff[k] = coeff.get(k, 0) - abs(v)
            two_adic = 0 if integer == "Re" else (3 if all(v % 2 == 0 for _, v in key) else 2)
            ineqs.append((coeff, Fraction(1, 2 ** two_adic), "shared:" + integer + ":" + ",".join(f"{k}^{v}" for k, v in key)))
    lower = [LOWER_BOUND[c["role"]] for c in cols]
    return cols, ineqs, lower


def _rows(n, ineqs, lower):
    """Rows (a, K, name) with sum a_j x_j <= log K, the lower bounds included."""
    rows = [([coeff.get(j, 0) for j in range(n)], K, name) for coeff, K, name in ineqs]
    for j in range(n):
        rows.append(([-1 if k == j else 0 for k in range(n)], Fraction(1, lower[j]), f"lower:{j}"))
    return rows


def _exact_product(rows, y):
    """prod K_i^{D y_i} as an exact rational, with D the common denominator of y; returns (D, value)."""
    D = 1
    for v in y:
        D = D * v.denominator // math.gcd(D, v.denominator)
    val = Fraction(1)
    for (a, K, name), v in zip(rows, y):
        if v:
            val *= Fraction(K) ** int(v * D)
    return D, val


def analyse(cand, version=2):
    """The linear programme of a class: per prime, 'infeasible' (with an exact certificate that no
    primes satisfy the system: the class is impossible), 'capped' (exact certificate + bound) or
    'unbounded' (an exact positive recession direction).  The result records the system version."""
    import numpy as np
    from scipy.optimize import linprog
    cols, ineqs, lower = system(cand, version)
    n = len(lower)
    rows = _rows(n, ineqs, lower)
    A = np.array([a for a, K, name in rows], dtype=float)
    b = np.array([math.log(K) for a, K, name in rows], dtype=float)
    m = len(rows)
    out = {"version": version, "n_inequalities": len(ineqs), "lower": lower, "roles": "".join(c["role"] for c in cols), "per_prime": {}}
    feas = linprog(np.zeros(n), A_ub=A, b_ub=b, bounds=[(None, None)] * n, method="highs")
    if feas.status == 2:
        # Farkas: y >= 0, y^T A = 0, y^T b < 0  <=>  prod K_i^{y_i} < 1
        res = linprog(b, A_eq=A.T, b_eq=np.zeros(n), bounds=[(0, 1)] * m, method="highs")
        y = [Fraction(v).limit_denominator(10 ** 6) for v in res.x]
        ok = all(sum(y[i] * rows[i][0][k] for i in range(m)) == 0 for k in range(n)) and all(v >= 0 for v in y)
        D, val = _exact_product(rows, y)
        out["status"] = "infeasible"
        out["certificate"] = {"multipliers": {rows[i][2]: str(y[i]) for i in range(m) if y[i]}, "D": D, "product": str(val), "verified": bool(ok and val < 1)}
        return out
    out["status"] = "feasible"
    for j in range(n):
        cobj = np.zeros(n)
        cobj[j] = -1
        res = linprog(cobj, A_ub=A, b_ub=b, bounds=[(None, None)] * n, method="highs")
        if res.status in (3, 4):
            H = A[:len(ineqs)]
            res2 = linprog(cobj, A_ub=H, b_ub=np.zeros(len(ineqs)), bounds=[(0, 1)] * n, method="highs")
            x = [Fraction(v).limit_denominator(1000) for v in res2.x]
            ok = (x[j] > 0 and all(v >= 0 for v in x)
                  and all(sum(rows[i][0][k] * x[k] for k in range(n)) <= 0 for i in range(len(ineqs))))
            out["per_prime"][j] = {"status": "unbounded", "direction": [str(v) for v in x], "verified": bool(ok)}
        elif res.status == 0:
            res3 = linprog(b, A_eq=A.T, b_eq=np.eye(n)[j], bounds=[(0, None)] * m, method="highs")
            y = [Fraction(v).limit_denominator(10 ** 6) for v in res3.x]
            ok = all(sum(y[i] * rows[i][0][k] for i in range(m)) == (1 if k == j else 0) for k in range(n)) and all(v >= 0 for v in y)
            D, val = _exact_product(rows, y)          # p_j^D <= val exactly
            cap = float(val) ** (1.0 / D) if val < 10 ** 300 else math.exp(math.log(float(val.numerator)) - math.log(float(val.denominator))) ** (1.0 / D)
            out["per_prime"][j] = {"status": "capped", "cap": cap, "D": D, "product": str(val) if len(str(val)) < 200 else "(large)",
                                   "certificate": {rows[i][2]: str(y[i]) for i in range(m) if y[i]}, "verified": bool(ok)}
        else:
            out["per_prime"][j] = {"status": f"lp status {res.status}"}
    return out


def verify_certificate(cand, result):
    """Re-verify a recorded analysis in exact arithmetic from the class alone (the recorded system version)."""
    cols, ineqs, lower = system(cand, int(result.get("version", 1)))
    n = len(lower)
    rows = _rows(n, ineqs, lower)
    byname = {name: (a, K) for a, K, name in rows}
    if result["status"] == "infeasible":
        y = {name: Fraction(v) for name, v in result["certificate"]["multipliers"].items()}
        if any(v < 0 for v in y.values()) or any(sum(y[nm] * byname[nm][0][k] for nm in y) != 0 for k in range(n)):
            return False
        D = 1
        for v in y.values():
            D = D * v.denominator // math.gcd(D, v.denominator)
        val = Fraction(1)
        for nm, v in y.items():
            val *= Fraction(byname[nm][1]) ** int(v * D)
        return val < 1
    for j, r in result["per_prime"].items():
        j = int(j)
        if r["status"] == "unbounded":
            x = [Fraction(v) for v in r["direction"]]
            if not (x[j] > 0 and all(v >= 0 for v in x) and all(sum(a[k] * x[k] for k in range(n)) <= 0 for a, K, name in rows if not name.startswith("lower:"))):
                return False
        elif r["status"] == "capped":
            y = {name: Fraction(v) for name, v in r["certificate"].items()}
            if any(v < 0 for v in y.values()) or any(sum(y[nm] * byname[nm][0][k] for nm in y) != (1 if k == j else 0) for k in range(n)):
                return False
        else:
            return False
    return True
