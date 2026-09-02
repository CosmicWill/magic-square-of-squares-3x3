"""L-values of the congruent-number curves E_n: y^2 = x^3 - n^2 x (n odd,
squarefree) -- the certificate that turns a 2-Selmer bound of 3 into
rank exactly 1 (entry 78).

E_n is the quadratic twist by n of the CM curve E_1: y^2 = x^3 - x, so
    a_p(E_1) = 0                       for p = 3 mod 4,
    a_p(E_1) = 2 Re(pi)                for p = 1 mod 4, pi = a + bi the
                                       PRIMARY Gaussian prime over p
                                       (a odd, b even, a + b = 1 mod 4),
    a_p(E_n) = (n/p) a_p(E_1)          for p !| 2n,   a_p(E_n) = 0 for p | 2n.
Conductor N = 32 n^2; root number w = +1 for n = 1,2,3 mod 8 and -1 for
n = 5,6,7 mod 8.  The standard rapidly convergent series
    w = +1:  L(E,1)  = 2 sum a_m/m exp(-2 pi m / sqrt N)
    w = -1:  L'(E,1) = 2 sum a_m/m E1(2 pi m / sqrt N)
need ~4 sqrt N terms; the truncation tail is bounded explicitly
(|a_m| <= d(m) sqrt m).  Gross-Zagier-Kolyvagin: L'(E,1) != 0 implies
rank E(Q) = 1, unconditionally.

Controls (self_test): a_p(E_1) against point counts; L'(37a,1) =
0.30599977383405...; Tunnell's finite formula L(E_n,1) = beta (A_n -
2B_n)^2 / (16 sqrt n) on rank-0 twists; L(E_5,1) = L(E_7,1) = 0 with
L' != 0.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.special import exp1

BETA = 2.6220575542921198104648395898911194136827549514316  # int_1^inf dx/sqrt(x^3-x) = Gamma(1/4)^2/(2 sqrt(2 pi))


# ---------------------------------------------------------------- primes

def prime_sieve(M):
    """Boolean array is_prime[0..M]."""
    s = np.ones(M + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(M**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return s


# ------------------------------------------------- a_p of E_1: y^2 = x^3 - x

def ap_E1_table(M, is_prime=None):
    """int64 array ap[0..M] with ap[p] = a_p(E_1) for primes p <= M
    (0 at non-primes and at p = 3 mod 4, and at p = 2).  Enumerates
    a^2 + b^2 <= M with a odd, b even and fixes the PRIMARY sign."""
    if is_prime is None:
        is_prime = prime_sieve(M)
    ap = np.zeros(M + 1, dtype=np.int64)
    r = int(M**0.5) + 1
    a = np.arange(1, r + 1, 2, dtype=np.int64)
    b = np.arange(0, r + 1, 2, dtype=np.int64)
    A, B = np.meshgrid(a, b, indexing="ij")
    S = A * A + B * B
    mask = (S <= M)
    A, B, S = A[mask], B[mask], S[mask]
    pm = is_prime[S]
    A, B, S = A[pm], B[pm], S[pm]
    # primary representative: a + b = 1 mod 4 (flip a's sign if needed)
    sign = np.where((A + B) % 4 == 1, 1, -1)
    ap[S] = 2 * A * sign
    return ap


def count_points_E1(p):
    """#E_1(F_p) by brute force (projective), for the self-test."""
    sq = {}
    for y in range(p):
        sq[(y * y) % p] = sq.get((y * y) % p, 0) + 1
    n = 1
    for x in range(p):
        n += sq.get((x**3 - x) % p, 0)
    return n


# ------------------------------------------------- a_m of E_n, multiplicative

def coefficients(n, M, ap1=None, is_prime=None):
    """int64 array a[0..M] with a[m] = a_m(E_n), n odd squarefree."""
    if is_prime is None:
        is_prime = prime_sieve(M)
    if ap1 is None:
        ap1 = ap_E1_table(M, is_prime)
    primes = np.nonzero(is_prime)[0]
    # twist: a_p(E_n) = (n/p) a_p(E_1), 0 at p | 2n
    ap = np.zeros(M + 1, dtype=np.int64)
    n_abs = abs(n)
    for p in primes:
        p = int(p)
        if p == 2 or n_abs % p == 0:
            continue
        v = ap1[p]
        if v == 0:
            continue
        leg = pow(n_abs % p, (p - 1) // 2, p)
        ap[p] = v if leg == 1 else -v
    # int32 throughout: |a_m| <= d(m) sqrt(m) < 2^31 for every m <= 2e9,
    # and every partial product is some a_{m'} with m' | m.
    a = np.ones(M + 1, dtype=np.int32)
    a[0] = 0
    sqrtM = int(M**0.5)
    for p in primes:
        p = int(p)
        if p > sqrtM:
            break
        # a_{p^k} by the Hecke recursion (p !| N) or 0 (p | N)
        bad = (p == 2 or n_abs % p == 0)
        pk_vals = []
        prev2, prev1 = 1, int(ap[p])
        pk = p
        while pk <= M:
            pk_vals.append(prev1)
            pk *= p
            if bad:
                nxt = 0
            else:
                nxt = int(ap[p]) * prev1 - p * prev2
            prev2, prev1 = prev1, nxt
        idx = np.arange(p, M + 1, p, dtype=np.int32)
        v = np.ones(len(idx), dtype=np.int8)
        q = p * p
        k = 2
        while q <= M:
            v[(idx % q) == 0] = k
            q *= p
            k += 1
        a[idx] *= np.asarray(pk_vals, dtype=np.int32)[v - 1]
        del idx, v
    # large primes (p^2 > M): only first powers
    big = primes[primes > sqrtM]
    apv = ap[big]
    for p, c in zip(big.tolist(), apv.tolist()):
        a[p::p] *= c
    return a


# ------------------------------------------------------------------ series

def root_number(n):
    n = abs(n)
    return 1 if n % 8 in (1, 2, 3) else -1


def l_series(a, N, w, M=None):
    """L(E,1) (w=+1) or L'(E,1) (w=-1) from coefficients a[0..M] and
    conductor N.  Returns (value, rigorous_tail_bound)."""
    if M is None:
        M = len(a) - 1
    c = 2 * math.pi / math.sqrt(N)
    total = 0.0
    CH = 1 << 23
    for lo in range(1, M + 1, CH):
        hi = min(M, lo + CH - 1)
        m = np.arange(lo, hi + 1, dtype=np.float64)
        x = c * m
        weight = np.exp(-x) if w == 1 else exp1(x)
        total += float(np.sum(a[lo:hi + 1].astype(np.float64) / m * weight))
    val = 2.0 * total
    # tail: |a_m| <= d(m) sqrt m <= m (d(m) <= 2 sqrt m), so each term is
    # bounded by weight(x_m); the geometric/E1 tail is summed in closed form
    if w == 1:
        tail = 2.0 * math.exp(-c * (M + 1)) / (1 - math.exp(-c))
    else:
        # E1(x) <= exp(-x)/x ; sum_{m>M} exp(-c m)/(c m) <= exp(-c(M+1))/((1-exp(-c)) c (M+1))
        tail = 2.0 * math.exp(-c * (M + 1)) / ((1 - math.exp(-c)) * c * (M + 1))
    return val, tail


def l_value(n, terms_factor=4.0, M=None, verbose=False):
    """(w, value, tail_bound, M) for E_n, n odd squarefree."""
    n = abs(n)
    N = 32 * n * n
    if M is None:
        M = int(terms_factor * math.sqrt(N)) + 10
    is_prime = prime_sieve(M)
    ap1 = ap_E1_table(M, is_prime)
    a = coefficients(n, M, ap1, is_prime)
    w = root_number(n)
    val, tail = l_series(a, N, w, M)
    if verbose:
        print(f"n={n} N={N} w={w:+d} M={M}: {'L' if w == 1 else 'L`'}(E,1) = {val:.12g}  tail <= {tail:.2e}")
    return w, val, tail, M


# ----------------------------------------------------------------- Tunnell

def tunnell_counts(n):
    """A_n = #{2x^2 + y^2 + 8z^2 = n}, B_n = #{2x^2 + y^2 + 32z^2 = n}."""
    A = B = 0
    r = int(n**0.5) + 1
    for x in range(-r, r + 1):
        t = n - 2 * x * x
        if t < 0:
            continue
        for z in range(-r, r + 1):
            for c, which in ((8, 0), (32, 1)):
                u = t - c * z * z
                if u < 0:
                    continue
                y = int(round(u**0.5))
                if y * y == u:
                    cnt = 2 if y else 1
                    if which == 0:
                        A += cnt
                    else:
                        B += cnt
    return A, B


def tunnell_L(n):
    A, B = tunnell_counts(n)
    return BETA * (A - 2 * B) ** 2 / (16 * math.sqrt(n))


# --------------------------------------------------------- 37a control

def l_prime_37a(M=200):
    """L'(37a,1) for y^2 + y = x^3 - x by point counting; 0.3059997738..."""
    N = 37
    is_prime = prime_sieve(M)
    primes = np.nonzero(is_prime)[0]
    ap = {}
    for p in primes:
        p = int(p)
        cnt = 1
        for x in range(p):
            rhs = (x**3 - x) % p
            for y in range(p):
                if (y * y + y - rhs) % p == 0:
                    cnt += 1
        ap[p] = p + 1 - cnt
    a = [0] + [1] * M
    # multiplicative fill
    for m in range(2, M + 1):
        mm = m
        val = 1
        for p in primes:
            p = int(p)
            if p * p > mm:
                break
            if mm % p == 0:
                k = 0
                while mm % p == 0:
                    mm //= p
                    k += 1
                if p == 37:
                    val *= ap[p] ** k
                else:
                    x2, x1 = 1, ap[p]
                    for _ in range(k - 1):
                        x2, x1 = x1, ap[p] * x1 - p * x2
                    val *= x1
        if mm > 1:
            val *= ap[mm]
        a[m] = val
    a = np.asarray(a, dtype=np.int64)
    return l_series(a, N, -1, M)[0]


def self_test():
    # a_p(E_1) against point counts
    ap1 = ap_E1_table(400)
    for p in range(3, 400):
        if all(p % d for d in range(2, int(p**0.5) + 1)):
            assert ap1[p] == p + 1 - count_points_E1(p), p
    # 37a
    v = l_prime_37a()
    assert abs(v - 0.30599977383405) < 1e-9, v
    # Tunnell on rank-0 twists, and L(E_1,1) = 0.6555143885...
    for n in (1, 3, 11, 17, 19, 43):
        w, val, tail, M = l_value(n, terms_factor=6.0)
        assert w == 1, n
        assert abs(val - tunnell_L(n)) < 1e-8 + tail, (n, val, tunnell_L(n))
    w, val, _, _ = l_value(1, terms_factor=6.0)
    assert abs(val - 0.6555143885) < 1e-8, val
    # rank-1 twists: L = 0 (w = -1), L' != 0
    for n in (5, 7, 13, 15, 21, 23):
        w, val, tail, M = l_value(n, terms_factor=6.0)
        assert w == -1 and abs(val) > 0.05, (n, val)
    return True


if __name__ == "__main__":
    print("self_test:", self_test())
