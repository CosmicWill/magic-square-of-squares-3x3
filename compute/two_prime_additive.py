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
