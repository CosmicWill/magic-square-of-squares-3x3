"""A3-S2b: the two-split-prime additive theorem (ROADMAP W10).

For m = 2^s r p^a q^b (p, q distinct split primes, r inert), the
congrua are D(m) = { m^2 |Im(sigma^j tau^k)| } over the exponent box
(j, k) in [-a, a] x [-b, b] minus the origin, modulo conjugation,
with sigma = lambda^4/p^2, tau = mu^4/q^2.  Valuations at lambda,
mu give v(sigma^j tau^k) = (2j, -2j, 2k, -2k): the group <sigma,
tau> is free of rank 2, and a signed additive relation

    sum_i c_i (w_i - w_i^{-1}) = 0,   w_i = sigma^{j_i} tau^{k_i}

is a six-term vanishing sum of monomials.  Three mechanisms:

(1) VALUATION PRUNE: at each of the four valuation directions the
    minimal valuation must be achieved by >= 2 distinct monomials
    (ultrametric; coefficients +-1, +-2 are units at odd places).

(2) TAN-HALF FACTORIZATION: sigma = (1 + i t1)/(1 - i t1) with
    t1 = s1/c1 rational (lambda^2 = c1 + i s1).  Clearing
    (1+t1^2)^J (1+t2^2)^K turns the relation into an integer
    polynomial N(t1, t2); if N factors into the CANDIDATE factors
      t1, t2, (t1 +- t2), (1 +- t1 t2), (1 + t1^2), (1 + t2^2)
    then every real zero forces some sigma^alpha tau^beta = +-1
    with (alpha, beta) != 0 — impossible in the free group.  Such
    patterns are PROVEN-dead.

(3) INCOHERENT RESIDUALS: otherwise the unfactored residual R gives,
    after t = s/c and clearing, an integer form G(c1,s1,c2,s2) that
    must vanish on Pythagorean data (c odd, s even, c^2 + s^2 = p^2).
    A congruence kill (no solutions mod M under those side
    conditions) closes the pattern; survivors are explicit open
    Diophantine equations, searched exactly over real prime data.

Pure stdlib; all polynomial arithmetic on dicts {(d1, d2): int}.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, product
from math import gcd

# ---------------------------------------------------------------- poly core
# Z[i][t1, t2]: dict {(e1, e2): (re, im)}; plain Z[t1, t2] uses im = 0


def padd(A, B, s=1):
    out = dict(A)
    for k, (re, im) in B.items():
        r0, i0 = out.get(k, (0, 0))
        v = (r0 + s * re, i0 + s * im)
        if v == (0, 0):
            out.pop(k, None)
        else:
            out[k] = v
    return out


def pmul(A, B):
    out = {}
    for (a1, a2), (ar, ai) in A.items():
        for (b1, b2), (br, bi) in B.items():
            k = (a1 + b1, a2 + b2)
            r0, i0 = out.get(k, (0, 0))
            v = (r0 + ar * br - ai * bi, i0 + ar * bi + ai * br)
            if v == (0, 0):
                out.pop(k, None)
            else:
                out[k] = v
    return out


def ppow(A, n):
    r = {(0, 0): (1, 0)}
    for _ in range(n):
        r = pmul(r, A)
    return r


ONE_P_IT1 = {(0, 0): (1, 0), (1, 0): (0, 1)}    # 1 + i t1
ONE_M_IT1 = {(0, 0): (1, 0), (1, 0): (0, -1)}   # 1 - i t1
ONE_P_IT2 = {(0, 0): (1, 0), (0, 1): (0, 1)}
ONE_M_IT2 = {(0, 0): (1, 0), (0, 1): (0, -1)}


def relation_poly(pattern):
    """pattern: list of ((j, k), c).  Returns N(t1, t2) in Z[t1,t2]
    (real integer coefficients) = (1+t1^2)^J (1+t2^2)^K *
    sum c (w - w^{-1}) / (2i), where J = max|j|, K = max|k|."""
    J = max(abs(j) for (j, k), c in pattern)
    K = max(abs(k) for (j, k), c in pattern)
    tot = {}
    for (j, k), c in pattern:
        term = pmul(pmul(ppow(ONE_P_IT1, J + j), ppow(ONE_M_IT1, J - j)),
                    pmul(ppow(ONE_P_IT2, K + k), ppow(ONE_M_IT2, K - k)))
        conj = pmul(pmul(ppow(ONE_P_IT1, J - j), ppow(ONE_M_IT1, J + j)),
                    pmul(ppow(ONE_P_IT2, K - k), ppow(ONE_M_IT2, K + k)))
        tot = padd(tot, term, c)
        tot = padd(tot, conj, -c)
    # tot is purely imaginary (2i * real); divide by 2i
    out = {}
    for k, (re, im) in tot.items():
        assert re == 0, "relation polynomial not purely imaginary"
        if im:
            assert im % 2 == 0
            out[k] = im // 2
    return out


# ------------------------------------------------------- valuation prune

def monomial_terms(pattern):
    """Merged monomial -> coefficient over the six-term expansion."""
    terms = {}
    for (j, k), c in pattern:
        terms[(j, k)] = terms.get((j, k), 0) + c
        terms[(-j, -k)] = terms.get((-j, -k), 0) - c
    return {v: c for v, c in terms.items() if c}


def valuation_pruned(pattern):
    """True if the relation is impossible by the ultrametric at one
    of the four valuation directions (min achieved only once)."""
    terms = monomial_terms(pattern)
    if not terms:
        return False  # empty sum: degenerate cancellation, not ours
    for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        vals = [direction[0] * j + direction[1] * k for j, k in terms]
        mn = min(vals)
        if sum(1 for v in vals if v == mn) == 1:
            return True
    return False


# ------------------------------------------------- candidate factorization

CANDIDATES = [
    ("t1", {(1, 0): 1}, "w-component sigma-part trivial: sigma^a tau^b = 1"),
    ("t2", {(0, 1): 1}, "tau-part trivial"),
    ("t1+t2", {(1, 0): 1, (0, 1): 1}, "sigma tau = 1 type"),
    ("t1-t2", {(1, 0): 1, (0, 1): -1}, "sigma tau^{-1} = 1 type"),
    ("1-t1t2", {(0, 0): 1, (1, 1): -1}, "sigma tau = -1 type"),
    ("1+t1t2", {(0, 0): 1, (1, 1): 1}, "sigma tau^{-1} = -1 type"),
    ("1+t1^2", {(0, 0): 1, (2, 0): 1}, "no real zero"),
    ("1+t2^2", {(0, 0): 1, (0, 2): 1}, "no real zero"),
]


def try_divide(N, D):
    """Exact division N / D in Z[t1, t2] with D from CANDIDATES
    (each has an extreme monomial usable as division leader).
    Returns quotient dict or None."""
    if not N:
        return None
    # leader: lexicographically largest monomial of D
    lead = max(D)
    lc = D[lead]
    Q = {}
    R = {k: (v, 0) for k, v in N.items()}
    Dg = {k: (v, 0) for k, v in D.items()}
    guard = 0
    while R:
        guard += 1
        if guard > 20000:
            return None
        # pick the lexicographically largest monomial of R
        rk = max(R)
        rc = R[rk][0]
        e = (rk[0] - lead[0], rk[1] - lead[1])
        if e[0] < 0 or e[1] < 0 or rc % lc:
            return None
        qc = rc // lc
        Q[e] = qc
        R = padd(R, pmul({e: (qc, 0)}, Dg), -1)
    return Q


def peel(N):
    """Peel candidate factors greedily; returns (factors, residual)."""
    factors = []
    cur = dict(N)
    changed = True
    while changed and cur:
        changed = False
        for name, D, meaning in CANDIDATES:
            q = try_divide(cur, D)
            while q is not None:
                factors.append(name)
                cur = q
                q = try_divide(cur, D)
                changed = True
    # strip integer content
    if cur:
        g = 0
        for v in cur.values():
            g = gcd(g, abs(v))
        if g > 1:
            cur = {k: v // g for k, v in cur.items()}
    return factors, cur


def is_constant(P):
    return not P or set(P) == {(0, 0)}


# ------------------------------------------------- incoherent residuals

def residual_cs_form(R):
    """Substitute t1 = s1/c1, t2 = s2/c2 and clear: integer form in
    (c1, s1, c2, s2) as dict {(a, b, c, d): coeff} with a + b = deg1,
    c + d = deg2 (homogenized per variable pair)."""
    d1 = max(k[0] for k in R)
    d2 = max(k[1] for k in R)
    out = {}
    for (e1, e2), v in R.items():
        key = (d1 - e1, e1, d2 - e2, e2)  # c1^, s1^, c2^, s2^
        out[key] = out.get(key, 0) + v
    return {k: v for k, v in out.items() if v}


def congruence_kill(G, M):
    """True if G(c1,s1,c2,s2) = 0 mod M has NO solutions with the
    Pythagorean side conditions mod M: c odd, s even, gcd(c*s, M)
    unconstrained, and c^2 + s^2 = P^2 for some P with gcd(P, M) = 1
    (odd prime not dividing M)."""
    pairs = []
    for c in range(M):
        for s in range(M):
            if c % 2 == 1 and s % 2 == 0:
                cs2 = (c * c + s * s) % M
                if any((P * P) % M == cs2 for P in range(1, M)
                       if gcd(P, M) == 1 and P % 2 == 1):
                    pairs.append((c, s))
    for c1, s1 in pairs:
        for c2, s2 in pairs:
            tot = 0
            for (a, b, cc, dd), v in G.items():
                tot += (v * pow(c1, a, M) * pow(s1, b, M)
                        * pow(c2, cc, M) * pow(s2, dd, M))
            if tot % M == 0:
                return False
    return True


# ------------------------------------------------------- the a=b=1 sweep

CLASSES_11 = [(1, 0), (0, 1), (1, 1), (1, -1)]


def enumerate_patterns_11():
    """All sign/exponent patterns for a = b = 1: distinct triples
    (coefficients +-1, not all equal up to overall sign) and repeated
    pairs 2 d_x = d_y (coefficient patterns (2, -1) and (2, 1) — the
    latter killable by positivity but kept for completeness).
    Orientation of each w is absorbed into the coefficient, and the
    class list is taken modulo inversion, so coefficient sign
    patterns must run over all combinations."""
    pats = []
    for trip in combinations(CLASSES_11, 3):
        for signs in product((1, -1), repeat=3):
            if len(set(signs)) == 1:
                continue  # positivity: some sign differs
            pats.append((tuple(zip(trip, signs)), "distinct"))
    for x in CLASSES_11:
        for y in CLASSES_11:
            if x == y:
                continue
            for sy in (1, -1):
                pats.append((((x, 2), (y, sy)), "doubled"))
    return pats


def classify_all_11(mods=(16, 32, 64, 9, 5, 7, 11, 13, 8, 3)):
    """The full a = b = 1 pattern sweep.  Returns a report list:
    (pattern, verdict, detail)."""
    report = []
    seen = set()
    for pattern, kind in enumerate_patterns_11():
        # canonical form modulo overall sign and global conjugation
        def canon(p):
            forms = []
            for gs in (1, -1):
                for cj in (1, -1):
                    f = tuple(sorted(((cj * j, cj * k), gs * c)
                                     for (j, k), c in p))
                    forms.append(f)
            return min(forms)
        key = canon(pattern)
        if key in seen:
            continue
        seen.add(key)
        if valuation_pruned(pattern):
            report.append((pattern, kind, "VALUATION", None))
            continue
        N = relation_poly(pattern)
        if not N:
            report.append((pattern, kind, "IDENTITY-ZERO", None))
            continue
        factors, residual = peel(N)
        if is_constant(residual):
            report.append((pattern, kind, "FACTORED", factors))
            continue
        G = residual_cs_form(residual)
        kill = None
        for M in mods:
            if congruence_kill(G, M):
                kill = M
                break
        if kill:
            report.append((pattern, kind, f"CONGRUENCE mod {kill}", G))
        else:
            report.append((pattern, kind, "OPEN", G))
    return report


def search_real_data(G, bound=500):
    """Exact search of a residual form over real split-prime data:
    all pairs of distinct split primes p, q <= bound, lambda^2 =
    c + i s both orientations and both sign choices of s.  Returns
    hits [(p, q, c1, s1, c2, s2)]."""
    from .zi_additive import gaussian_prime_over

    prs = [n for n in range(5, bound, 4) if _isprime(n)]
    data = []
    for p in prs:
        e, f = gaussian_prime_over(p)
        c, s = e * e - f * f, 2 * e * f
        data.append((p, [(c, s), (c, -s), (-c, s), (-c, -s)]))
    hits = []
    for (p, or1) in data:
        for (q, or2) in data:
            if p == q:
                continue
            for c1, s1 in or1:
                for c2, s2 in or2:
                    tot = 0
                    for (a, b, cc, dd), v in G.items():
                        tot += (v * c1 ** a * s1 ** b
                                * c2 ** cc * s2 ** dd)
                    if tot == 0:
                        hits.append((p, q, c1, s1, c2, s2))
    return hits


def _isprime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def main():
    rep = classify_all_11()
    from collections import Counter
    cnt = Counter(v for _, _, v, _ in
                  [(p, k, ver.split()[0], d) for p, k, ver, d in rep])
    print(f"{len(rep)} canonical patterns:")
    for p, kind, verdict, detail in rep:
        tag = " ".join(f"{jk}x{c}" for jk, c in p)
        extra = ""
        if verdict == "FACTORED":
            extra = " = " + " * ".join(detail)
        print(f"  [{verdict:>16}] ({kind}) {tag}{extra}")
    print(dict(cnt))
    open_pats = [(p, d) for p, k, v, d in rep if v == "OPEN"]
    for p, G in open_pats:
        hits = search_real_data(G, 500)
        print(f"OPEN pattern {p}: real-data hits to p,q <= 500: "
              f"{hits[:5]} ({len(hits)})")


if __name__ == "__main__":
    main()


# ---------------------------------------------------- descent corroboration

def search_fermat_quartic(bound):
    """x^4 - y^4 = z^2, 0 < y < x <= bound, z != 0 (Fermat: none)."""
    hits = []
    for x in range(2, bound + 1):
        x4 = x ** 4
        for y in range(1, x):
            d = x4 - y ** 4
            r = int(d ** 0.5)
            for rr in (r - 1, r, r + 1):
                if rr > 0 and rr * rr == d:
                    hits.append((x, y, rr))
    return hits


def search_2b2(bound):
    """m n (m-n)(m+n) = 2 b^2, m > n >= 1, gcd = 1, opposite parity
    (the '2 is not congruent' descent equation): none."""
    hits = []
    for mm in range(2, bound + 1):
        for nn in range(1, mm):
            if gcd(mm, nn) != 1 or (mm - nn) % 2 == 0:
                continue
            P = mm * nn * (mm - nn) * (mm + nn)
            if P % 2 == 0:
                b2 = P // 2
                r = int(b2 ** 0.5)
                for rr in (r - 1, r, r + 1):
                    if rr > 0 and rr * rr == b2:
                        hits.append((mm, nn, rr))
    return hits


def search_3w2_sandwich(bound):
    """x^2 - 3w^2 and x^2 + 3w^2 both squares, w >= 1 ('3 is not
    congruent'): none."""
    hits = []
    for x in range(2, bound + 1):
        x2 = x * x
        w = 1
        while 3 * w * w < x2:
            a = x2 - 3 * w * w
            b = x2 + 3 * w * w
            ra, rb = int(a ** 0.5), int(b ** 0.5)
            ok_a = any(t * t == a for t in (ra - 1, ra, ra + 1) if t >= 0)
            ok_b = any(t * t == b for t in (rb - 1, rb, rb + 1))
            if ok_a and ok_b:
                hits.append((x, w))
            w += 1
    return hits


def search_quartic_3T2(bound):
    """x^4 - y^4 = 3 T^2, 0 < y < x <= bound, T != 0: none."""
    hits = []
    for x in range(2, bound + 1):
        x4 = x ** 4
        for y in range(1, x):
            d = x4 - y ** 4
            if d % 3 == 0:
                T2 = d // 3
                r = int(T2 ** 0.5)
                for rr in (r - 1, r, r + 1):
                    if rr > 0 and rr * rr == T2:
                        hits.append((x, y, rr))
    return hits


# ------------------------------------------------ general-box machinery
# (the (a, b) = (2, 1) rung and beyond)

from fractions import Fraction


def imre_poly(alpha, beta):
    """(Im, Re) of (1 + i t1)^alpha (1 + i t2)^beta for beta of either
    sign (negative beta uses (1 - i t2)); returns two Z[t1,t2] dicts."""
    A = ppow(ONE_P_IT1, alpha)
    B = ppow(ONE_P_IT2 if beta >= 0 else ONE_M_IT2, abs(beta))
    P = pmul(A, B)
    im = {k: v[1] for k, v in P.items() if v[1]}
    re = {k: v[0] for k, v in P.items() if v[0]}
    return im, re


def _strip_content(P):
    if not P:
        return P
    g = 0
    for v in P.values():
        g = gcd(g, abs(v))
    if g > 1:
        P = {k: v // g for k, v in P.items()}
    # normalize sign by lex-max monomial
    if P[max(P)] < 0:
        P = {k: -v for k, v in P.items()}
    return P


def candidates_for_box(amax, bmax):
    """All candidate factors for the [-amax, amax] x [-bmax, bmax]
    box: Im/Re[(1+it1)^alpha (1+-it2)^|beta|] for 1-vector-sums of
    box exponents, plus the no-real-zero quadratics."""
    cands = []
    seen = set()
    for alpha in range(0, 2 * amax + 1):
        for beta in range(-2 * bmax, 2 * bmax + 1):
            if (alpha, beta) == (0, 0):
                continue
            if alpha == 0 and beta < 0:
                continue
            im, re = imre_poly(alpha, beta)
            for tag, P in (("Im", im), ("Re", re)):
                P = _strip_content(P)
                if not P or set(P) == {(0, 0)}:
                    continue
                key = tuple(sorted(P.items()))
                if key in seen:
                    continue
                seen.add(key)
                cands.append((f"{tag}({alpha},{beta})", P))
    cands.append(("1+t1^2", {(0, 0): 1, (2, 0): 1}))
    cands.append(("1+t2^2", {(0, 0): 1, (0, 2): 1}))
    return cands


def qdivide(N, D):
    """Exact division over Q (Fraction coefficients); N, D integer
    dicts.  Returns integer-content-stripped quotient or None."""
    if not N or not D:
        return None
    lead = max(D)
    lc = Fraction(D[lead])
    R = {k: Fraction(v) for k, v in N.items()}
    Q = {}
    guard = 0
    while R:
        guard += 1
        if guard > 40000:
            return None
        rk = max(R)
        e = (rk[0] - lead[0], rk[1] - lead[1])
        if e[0] < 0 or e[1] < 0:
            return None
        qc = R[rk] / lc
        Q[e] = Q.get(e, Fraction(0)) + qc
        for dk, dv in D.items():
            kk = (e[0] + dk[0], e[1] + dk[1])
            nv = R.get(kk, Fraction(0)) - qc * dv
            if nv == 0:
                R.pop(kk, None)
            else:
                R[kk] = nv
    # clear denominators, strip content
    den = 1
    for v in Q.values():
        den = den * v.denominator // gcd(den, v.denominator)
    out = {k: int(v * den) for k, v in Q.items() if v != 0}
    return _strip_content(out)


def peel_general(N, cands):
    factors = []
    cur = _strip_content(dict(N))
    changed = True
    while changed and cur and set(cur) != {(0, 0)}:
        changed = False
        for name, D in cands:
            if len(D) > len(cur):
                continue
            q = qdivide(cur, D)
            if q is not None:
                factors.append(name)
                cur = q
                changed = True
                break
    return factors, cur


def enumerate_patterns(classes):
    pats = []
    for trip in combinations(classes, 3):
        for signs in product((1, -1), repeat=3):
            if len(set(signs)) == 1:
                continue
            pats.append((tuple(zip(trip, signs)), "distinct"))
    for x in classes:
        for y in classes:
            if x == y:
                continue
            for sy in (1, -1):
                pats.append((((x, 2), (y, sy)), "doubled"))
    return pats


def classify_box(classes, amax, bmax,
                 mods=(16, 32, 64, 9, 5, 7, 11, 13, 8, 3)):
    cands = candidates_for_box(amax, bmax)
    report = []
    seen = set()
    for pattern, kind in enumerate_patterns(classes):
        def canon(p):
            forms = []
            for gs in (1, -1):
                for cj in (1, -1):
                    f = tuple(sorted(((cj * j, cj * k), gs * c)
                                     for (j, k), c in p))
                    forms.append(f)
            return min(forms)
        key = canon(pattern)
        if key in seen:
            continue
        seen.add(key)
        if valuation_pruned(pattern):
            report.append((pattern, kind, "VALUATION", None))
            continue
        N = relation_poly(pattern)
        if not N:
            report.append((pattern, kind, "IDENTITY-ZERO", None))
            continue
        factors, residual = peel_general(N, cands)
        if is_constant(residual):
            report.append((pattern, kind, "FACTORED", factors))
            continue
        G = residual_cs_form(residual)
        kill = None
        for M in mods:
            if congruence_kill(G, M):
                kill = M
                break
        if kill:
            report.append((pattern, kind, f"CONGRUENCE mod {kill}",
                           (factors, G)))
        else:
            report.append((pattern, kind, "OPEN", (factors, residual)))
    return report


CLASSES_21 = [(1, 0), (2, 0), (0, 1), (1, 1), (1, -1), (2, 1), (2, -1)]


# ------------------------------------- Gaussian-collapse representation
# polys in Z[c1,s1,c2,s2]: dict {(a,b,c,d): int}

def p4add(A, B, s=1):
    out = dict(A)
    for k, v in B.items():
        nv = out.get(k, 0) + s * v
        if nv:
            out[k] = nv
        else:
            out.pop(k, None)
    return out


def p4mul(A, B):
    out = {}
    for ka, va in A.items():
        for kb, vb in B.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            nv = out.get(k, 0) + va * vb
            if nv:
                out[k] = nv
            else:
                out.pop(k, None)
    return out


def gauss_pow(re, im, n):
    """(re, im) as poly dicts -> (re, im) of the n-th power."""
    R, I = {(0, 0, 0, 0): 1}, {}
    for _ in range(n):
        R, I = (p4add(p4mul(R, re), p4mul(I, im), -1),
                p4add(p4mul(R, im), p4mul(I, re)))
    return R, I


ELL = ({(1, 0, 0, 0): 1}, {(0, 1, 0, 0): 1})       # c1 + i s1
W = ({(0, 0, 1, 0): 1}, {(0, 0, 0, 1): 1})         # c2 + i s2
Q2 = {(0, 0, 2, 0): 1, (0, 0, 0, 2): 1}            # q^2


def im_ell_w(a, weps):
    """Im(ell^a w^2) for weps=+1, Im(ell^a wbar^2) for weps=-1."""
    Rl, Il = gauss_pow(*ELL, a)
    Rw, Iw = gauss_pow(*W, 2)
    if weps < 0:
        Iw = {k: -v for k, v in Iw.items()}
    # Im(X Y) = ReX ImY + ImX ReY
    return p4add(p4mul(Rl, Iw), p4mul(Il, Rw))


P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}             # p^2


def im_monomial(j, k):
    """Im(ell^{2j} w^{2k}) in Z[c1,s1,c2,s2]; negative exponents by
    conjugation (Im(zbar) = -Im(z))."""
    Rl, Il = gauss_pow(*ELL, 2 * abs(j))
    if j < 0:
        Il = {kk: -v for kk, v in Il.items()}
    Rw, Iw = gauss_pow(*W, 2 * abs(k))
    if k < 0:
        Iw = {kk: -v for kk, v in Iw.items()}
    return p4add(p4mul(Rl, Iw), p4mul(Il, Rw))


def cleared_relation(pattern):
    """The signed relation sum c Im(sigma^j tau^k), cleared by
    p^{2J} q^{2K} (J = max|j|, K = max|k|), as an exact polynomial in
    Z[c1,s1,c2,s2]:  sum c p^{2(J-|j|)} q^{2(K-|k|)} Im(l^{2j} w^{2k})."""
    J = max(abs(j) for (j, k), c in pattern)
    K = max(abs(k) for (j, k), c in pattern)
    tot = {}
    for (j, k), c in pattern:
        T = im_monomial(j, k)
        for _ in range(J - abs(j)):
            T = p4mul(T, P2)
        for _ in range(K - abs(k)):
            T = p4mul(T, Q2)
        tot = p4add(tot, T, c)
    return tot


def tspace_to_cs(N, J, K):
    """Homogenize the tan-half polynomial N(t1, t2) (from
    relation_poly, cleared by (1+t1^2)^J (1+t2^2)^K) into
    Z[c1,s1,c2,s2] via t = s/c:  t1^a t2^b -> c1^{2J-a} s1^a
    c2^{2K-b} s2^b.  Under c^2 + s^2 = p^2 (resp. q^2) this equals
    cleared_relation exactly."""
    out = {}
    for (a, b), v in N.items():
        assert a <= 2 * J and b <= 2 * K
        out[(2 * J - a, a, 2 * K - b, b)] = v
    return out


def collapse_form(G, amax=6, mdeg=3):
    """Try to write G = q^2 * P1 + sum over single term
    Im(ell^a w^{+-2}) * monomial: exact integer linear algebra via
    sampled evaluations, verified symbolically.  Returns
    (a, weps, monomial, coeff, P1) for the SINGLE-Im representation
    or None."""
    from fractions import Fraction as Fr
    d1 = max(k[0] + k[1] for k in G)
    for a in range(1, amax + 1):
        for weps in (1, -1):
            IM = im_ell_w(a, weps)
            for ma in range(0, mdeg + 1):
                for mb in range(0, mdeg + 1 - ma):
                    if a + ma + mb != d1:
                        continue
                    mono = {(ma, mb, 0, 0): 1}
                    T = p4mul(IM, mono)
                    for coeff_sign in (1, -1):
                        # G - sign*T must be divisible by q^2 with
                        # quotient in Z[c1,s1] x {const in c2,s2}?
                        # general: G - sT = q^2 * P1, P1 poly.
                        R = p4add(G, T, -coeff_sign)
                        # divide by q^2 = c2^2 + s2^2: treat as poly
                        # in c2 with coeffs in Z[c1,s1,s2]
                        P1 = _div_q2(R)
                        if P1 is not None:
                            return (a, weps, (ma, mb), coeff_sign, P1)
    return None


def _div_q2(R):
    """Exact division of R by (c2^2 + s2^2) in Z[c1,s1,c2,s2]."""
    if not R:
        return {}
    cur = dict(R)
    out = {}
    guard = 0
    while cur:
        guard += 1
        if guard > 10000:
            return None
        k = max(cur, key=lambda t: (t[2], t[3], t[0], t[1]))
        a, b, c, d = k
        v = cur[k]
        if c >= 2:
            e = (a, b, c - 2, d)
        elif d >= 2:
            e = (a, b, c, d - 2)
        else:
            return None
        out[e] = out.get(e, 0) + v
        cur = p4add(cur, p4mul({e: v}, Q2), -1)
    return out


# --------------------------- (2,1)-box hand-kill identity forms (A3.8)

def box21_kill_form(kind, sgn, c1, s1, c2, s2):
    """The verified integer forms of the closed (2,1)-box families.
    Each returns an integer that vanishes iff the pattern's relation
    holds (up to nonvanishing factors)."""
    p2, q2 = c1 * c1 + s1 * s1, c2 * c2 + s2 * s2
    C, S = c1 * c1 - s1 * s1, 2 * c1 * s1
    u, v = c2 * c2 - s2 * s2, 2 * c2 * s2
    C4, S4 = C * C - S * S, 2 * C * S
    if kind == "alpha":     # sinA +- 2cos2A sinB
        return S * p2 * q2 + sgn * 2 * v * C4
    if kind == "FC":        # sin2A +- 2cos2A sinB
        return C * S * q2 + sgn * C4 * v
    if kind == "FD":        # sinB - 2sin2A cosB
        return v * p2 * p2 - 4 * C * S * u
    if kind == "beta1":     # Im(ell^3 w^{+-2}) = 2 q^2 s1 C
        l3r = c1 * (c1 * c1 - 3 * s1 * s1)
        l3i = s1 * (3 * c1 * c1 - s1 * s1)
        vv = sgn * v
        return (l3r * vv + l3i * u) - 2 * q2 * s1 * C
    if kind == "FF1":       # 2sin(2A+B) + sin(2A-B): C4 v + 3 S4 u
        return C4 * v + 3 * S4 * u
    if kind == "FF2":       # 2sin(2A+B) - sin(2A-B): 3 C4 v + S4 u
        return 3 * C4 * v + S4 * u
    raise ValueError(kind)


# ---------------------------------------- the q-unit collapse template

def trig_ell_w(kind, a, beta):
    """Im or Re of ell^a w^{2 beta} as a Z[c1,s1,c2,s2] poly
    (beta in {-2,-1,1,2}; w-power = 2|beta| with conjugation for
    beta < 0)."""
    Rl, Il = gauss_pow(*ELL, a)
    Rw, Iw = gauss_pow(*W, 2 * abs(beta))
    if beta < 0:
        Iw = {k: -v for k, v in Iw.items()}
    if kind == "Im":
        return p4add(p4mul(Rl, Iw), p4mul(Il, Rw))
    return p4add(p4mul(Rl, Rw), p4mul(Il, Iw), -1)


def qunit_collapse(G, amax=8, consts=(1, -1, 2, -2, 3, -3, 4, -4, 6, -6)):
    """Search for G = q^2 * H + c * Trig(ell^a w^{2 beta}) with a
    CONSTANT c (no c1,s1-monomial).  Such a representation certifies
    the pattern dead: on solutions the Trig term is a q-unit times c
    (q coprime to c), while the rest carries q^2; and Trig = 0 is
    impossible by the lambda-valuation mismatch (a >= 1).
    Returns (kind, a, beta, c) or None."""
    for kind in ("Im", "Re"):
        for a in range(1, amax + 1):
            for beta in (1, -1, 2, -2):
                T = trig_ell_w(kind, a, beta)
                if not T:
                    continue
                for c in consts:
                    R = p4add(G, {k: c * v for k, v in T.items()}, -1)
                    if _div_q2(R) is not None:
                        return (kind, a, beta, c)
    return None


def kreplicate(pat):
    """If all k-exponents are even, the halved pattern over
    (sigma, tau^2); else None."""
    if all(k % 2 == 0 for (j, k), c in pat):
        return tuple(((j, k // 2), c) for (j, k), c in pat)
    return None


def jreplicate(pat):
    """If all j-exponents are even, the halved pattern over
    (sigma^2, tau); else None."""
    if all(j % 2 == 0 for (j, k), c in pat):
        return tuple(((j // 2, k), c) for (j, k), c in pat)
    return None


# ------------------------------------------------- N1: completeness audit

def normclass_signed(jk, c):
    """Per-class normalization to the representative set (j > 0, or
    j = 0 and k > 0), flipping the coefficient: Im(w^{-1}) = -Im(w)."""
    j, k = jk
    if j < 0 or (j == 0 and k < 0):
        return ((-j, -k), -c)
    return ((j, k), c)


def canon_full(p):
    """Canonical form modulo global sign, global conjugation, and
    per-class normalization."""
    p = tuple(normclass_signed(jk, c) for jk, c in p)
    forms = []
    for gs in (1, -1):
        for cj in (1, -1):
            f = tuple(sorted(normclass_signed((cj * j, cj * k), gs * c)
                             for (j, k), c in p))
            forms.append(f)
    return min(forms)


def enumerate_patterns_complete(classes):
    """The CORRECTED enumeration: distinct triples with all four
    sign classes modulo global negation (including all-plus), plus
    doubled patterns 2 d_x = +- d_y."""
    pats = []
    for trip in combinations(classes, 3):
        for signs in product((1, -1), repeat=3):
            pats.append((tuple(zip(trip, signs)), "distinct"))
    for x in classes:
        for y in classes:
            if x == y:
                continue
            for sy in (1, -1):
                pats.append((((x, 2), (y, sy)), "doubled"))
    return pats


def brute_canonical_set(amax, bmax):
    """Enumeration-INDEPENDENT construction of the full canonical
    pattern space: every ordered triple of nonzero exponent pairs in
    the full signed box (repeats allowed), every sign vector; merge
    equal monomial classes; classify into distinct / doubled /
    degenerate; return the canonical sets."""
    full = [(j, k) for j in range(-amax, amax + 1)
            for k in range(-bmax, bmax + 1) if (j, k) != (0, 0)]
    distinct, doubled = set(), set()
    impossible = 0
    for v1 in full:
        for v2 in full:
            for v3 in full:
                for cs in product((1, -1), repeat=3):
                    # merge by VALUE-class: normalize each term, then
                    # combine coefficients of equal classes
                    merged = {}
                    for v, c in zip((v1, v2, v3), cs):
                        (vv, cc) = normclass_signed(v, c)
                        merged[vv] = merged.get(vv, 0) + cc
                    merged = {v: c for v, c in merged.items() if c}
                    coeffs = sorted(abs(c) for c in merged.values())
                    if coeffs == [1, 1, 1]:
                        distinct.add(canon_full(tuple(merged.items())))
                    elif coeffs == [1, 2]:
                        doubled.add(canon_full(tuple(merged.items())))
                    elif coeffs == [3] or coeffs == [1] or coeffs == [2]:
                        impossible += 1  # 3d=0 / d=0 / 2d=0: dead by
                        # positivity of the congrua
                    elif coeffs in ([1, 1], [2, 2], []):
                        impossible += 1  # cancellations: degenerate
                        # (equal-congrua) cases, covered by A3.5
                    else:
                        raise AssertionError(coeffs)
    return distinct, doubled, impossible


# ---------------------------------------- N2: the G1 same-k collapse kill

def p4div_by_cs(P, D):
    """Exact division of a 4-var poly P by a (c1,s1)-only poly D
    (dict over 2-exponent keys).  Returns quotient or None."""
    if not P:
        return {}
    lead2 = max(D)
    lc = D[lead2]
    R = dict(P)
    Q = {}
    guard = 0
    while R:
        guard += 1
        if guard > 60000:
            return None
        rk = max(R, key=lambda t: (t[0], t[1], t[2], t[3]))
        rc = R[rk]
        e = (rk[0] - lead2[0], rk[1] - lead2[1], rk[2], rk[3])
        if e[0] < 0 or e[1] < 0 or rc % lc:
            return None
        Q[e] = Q.get(e, 0) + rc // lc
        for dk, dv in D.items():
            kk = (e[0] + dk[0], e[1] + dk[1], e[2], e[3])
            nv = R.get(kk, 0) - (rc // lc) * dv
            if nv:
                R[kk] = nv
            else:
                R.pop(kk, None)
    return Q


CS_FACTORS = [
    ("c1", {(1, 0): 1}),
    ("s1", {(0, 1): 1}),
    ("C", {(2, 0): 1, (0, 2): -1}),
    ("3C2-S2", None),  # filled below
]


def _mk_3c2s2():
    C = {(2, 0): 1, (0, 2): -1}
    S = {(1, 1): 2}
    def mul2(A, B):
        out = {}
        for ka, va in A.items():
            for kb, vb in B.items():
                k = (ka[0] + kb[0], ka[1] + kb[1])
                out[k] = out.get(k, 0) + va * vb
        return {k: v for k, v in out.items() if v}
    C2 = mul2(C, C)
    S2 = mul2(S, S)
    out = {k: 3 * v for k, v in C2.items()}
    for k, v in S2.items():
        out[k] = out.get(k, 0) - v
    return {k: v for k, v in out.items() if v}


CS_FACTORS[3] = ("3C2-S2", _mk_3c2s2())


def strip_cs_factors(P):
    """Divide out (c1,s1)-only factors greedily; return
    (stripped poly, factor names)."""
    cur = dict(P)
    names = []
    changed = True
    while changed and cur:
        changed = False
        # monomial factors first
        if all(k[0] >= 1 for k in cur):
            cur = {(a - 1, b, c, d): v for (a, b, c, d), v in cur.items()}
            names.append("c1")
            changed = True
            continue
        if all(k[1] >= 1 for k in cur):
            cur = {(a, b - 1, c, d): v for (a, b, c, d), v in cur.items()}
            names.append("s1")
            changed = True
            continue
        for nm, D in CS_FACTORS[2:]:
            q = p4div_by_cs(cur, D)
            if q is not None:
                cur = q
                names.append(nm)
                changed = True
                break
    # integer content
    g = 0
    for v in cur.values():
        g = gcd(g, abs(v))
    if g > 1:
        cur = {k: v // g for k, v in cur.items()}
    return cur, names


def g1_branch_kill(pat):
    """The G1 certifier: raw relation -> strip (c1,s1)-only common
    factors (never zero on nondegenerate data) -> test whether the
    residue has the form q^2 * A + const * Trig(ell^a w^{2beta})
    via the (c2,s2) = (1,i) branch: if the branch equals a constant
    times a single Trig branch, the relation forces q^2 | const *
    (q-unit): INSTANT DEAD.  Returns certificate or None."""
    N = relation_poly(pat)
    G = residual_cs_form(N)
    G, names = strip_cs_factors(G)

    def branch(P):
        out = {}
        I = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for (a, b, x, y), v in P.items():
            re, im = I[y % 4]
            k = (a, b)
            r0, i0 = out.get(k, (0, 0))
            nv = (r0 + v * re, i0 + v * im)
            if nv == (0, 0):
                out.pop(k, None)
            else:
                out[k] = nv
        return out

    gb = branch(G)
    if not gb:
        return None

    def gmul(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    for kind in ("Im", "Re"):
        for a in range(1, 13):
            for beta in (1, -1, 2, -2):
                T = trig_ell_w(kind, a, beta)
                tb = branch(T)
                if not tb or set(tb) != set(gb):
                    continue
                k0 = max(tb)
                # projective equality: gb[k] * tb[k0] == gb[k0] * tb[k]
                if not all(gmul(gb[k], tb[k0]) == gmul(gb[k0], tb[k])
                           for k in tb):
                    continue
                # the constant gb[k0]/tb[k0] as a reduced Gaussian
                # rational: numerator must be a {2,3}-unit times a
                # Gaussian unit so that q (a prime = 1 mod 4, >= 5)
                # can never divide it
                num, den = gb[k0], tb[k0]
                d2 = den[0] * den[0] + den[1] * den[1]
                ure = num[0] * den[0] + num[1] * den[1]
                uim = num[1] * den[0] - num[0] * den[1]
                from math import gcd as _g
                g = _g(_g(abs(ure), abs(uim)), d2)
                ure, uim, d2 = ure // g, uim // g, d2 // g
                unorm = ure * ure + uim * uim
                t = unorm
                for pr in (2, 3):
                    while t % pr == 0:
                        t //= pr
                if t != 1 or unorm == 0:
                    continue
                return (kind, a, beta, (ure, uim, d2), tuple(names))
    return None
