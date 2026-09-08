"""Point counts of a genus-2 curve y^2 = f(x) (deg f = 5) over F_p and F_{p^2}, and the order of its Jacobian over F_p
(entries 131-132; pure Python, for the checks).  #J(F_p) = (N_1^2 + N_2)/2 - p with N_i = #C(F_{p^i}); the gcd over good
odd primes bounds the rational torsion (torsion reduces injectively).  Odd-degree model: one point at infinity."""
from math import gcd


def curve_count(coeffs, p, e):
    """#C(F_{p^e}) for e in (1, 2); coeffs highest degree first, degree 5, p odd not dividing the leading coefficient."""
    cs = [c % p for c in coeffs]
    assert len(cs) == 6 and cs[0] != 0
    if e == 1:
        sq = {(x * x) % p for x in range(p)}
        N = 1
        for u in range(p):
            v = 0
            for c in cs:
                v = (v * u + c) % p
            N += 0 if v not in sq else (1 if v == 0 else 2)
        return N
    nr = next(n for n in range(2, p) if pow(n, (p - 1) // 2, p) == p - 1)      # F_{p^2} = F_p[s]/(s^2 - nr)

    def mul(x, y):
        return ((x[0] * y[0] + nr * x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def powq(x, n):
        r = (1, 0)
        while n:
            if n & 1:
                r = mul(r, x)
            x = mul(x, x)
            n >>= 1
        return r

    q = p * p
    N = 1
    for a in range(p):
        for b in range(p):
            u = (a, b)
            v = (0, 0)
            for c in cs:
                v = mul(v, u)
                v = ((v[0] + c) % p, v[1])
            if v == (0, 0):
                N += 1
            elif powq(v, (q - 1) // 2) == (1, 0):
                N += 2
    return N


def jacobian_order(coeffs, p):
    N1, N2 = curve_count(coeffs, p, 1), curve_count(coeffs, p, 2)
    return (N1 * N1 + N2) // 2 - p


def torsion_bound(coeffs, primes):
    g = 0
    for p in primes:
        g = gcd(g, jacobian_order(coeffs, p))
    return g
