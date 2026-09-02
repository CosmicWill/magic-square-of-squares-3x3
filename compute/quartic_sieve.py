"""The quartic-residue sieve for the frame rigidity lemma (P1 core).

Setting (docs/attacks/A3-simultaneous-congrua.md section 2.11).  Prime
frames pi over p, rho over q; the endpoint Re(rho^8) = p^2 A4 with
A4 = c1^2 - s1^2 splits, for a divisor D of A4 coprime to E = A4/D,
into the Z[i] equation

    (1+i) rho^4 = E + i p^2 D,      rho^4 = R4 + i I4,
    R4 = (p^2 D + E)/2,  I4 = (p^2 D - E)/2.

rho^4 is a FOURTH POWER, so reducing modulo any Gaussian prime lam
that divides D, E, R4 or I4 turns the equation into a quartic-residue
condition.  With chi_lam(z) = z^{(N lam - 1)/4} in {1,i,-1,-i}
(written as an exponent mod 4) and eps = i^j the unknown unit:

    [D] lam | D :  chi(E) + chi(1+i) = chi(2) + j*chi(i)
    [E] lam | E :  chi(p^2 D)        = j*chi(i) + chi(1+i)
    [R] lam | R4:  chi(i) + chi(I4)  = 0        (rho^4 = i I4 mod lam)
    [I] lam | I4:  chi(R4)           = 0        (rho^4 = R4 mod lam)
    [K] natural split D = +-(c1 +- s1) only:  rho^4 = pi^2 + K(1+i),
        K = (p^2-1) D/2, so lam | K :  2 chi(pi) = 0.

With SIGNED (D, E) the equation is exact -- there is no unit, j = 0
-- so every condition is a fixed equality; two further natural
families:  [2] rho^4 mod 32 and mod 64 lies in a fixed small set;
[C] lam | u R4 + v I4 gives rho^4 = I4 (u i - v)/u, i.e.
chi(I4) + chi(u i - v) - chi(u) = 0.  If any condition fails the
(p, D) case is PROVABLY dead.  Two closed-form consequences: an inert
prime l = 7 mod 16 dividing A4 kills every D (chi_l(1+i) = -1 there,
+1 for l = 15 mod 16); and in the natural split 3 | K always, forcing
p to be a quadratic residue mod 3, i.e. p = 1 mod 3.

The sieve is a NECESSARY-condition filter: synthetic true solutions
(1+i) rho^4 must pass [D][E][R][I] with eps = 1 (self_test()).
"""

from math import gcd, isqrt


def sieve_primes(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return s


_LIM = 200000
_S = sieve_primes(_LIM)
_SMALL = [i for i in range(2, _LIM) if _S[i]]


def factor(n):
    """Trial division to _LIM; a surviving cofactor below _LIM^2 is
    prime and is included; a larger one is DROPPED (returned flag
    False), which only weakens the sieve, never falsifies a kill."""
    n = abs(n)
    f = {}
    for q in _SMALL:
        if q * q > n:
            break
        while n % q == 0:
            f[q] = f.get(q, 0) + 1
            n //= q
    if n > 1:
        if n < _LIM * _LIM:
            f[n] = f.get(n, 0) + 1
            return f, True
        return f, False
    return f, True


def divisors_from(f):
    ds = [1]
    for q, e in f.items():
        ds = [d * q**k for d in ds for k in range(e + 1)]
    return ds


def sqrt_minus1(l):
    for t in range(2, l):
        r = pow(t, (l - 1) // 4, l)
        if (r * r) % l == l - 1:
            return r
    raise ValueError(l)


def chi_split(x, y, l, iota):
    """exponent k in 0..3 with chi_lam(x + y i) = i^k, lam <-> i -> iota
    mod l (l = 1 mod 4); None if lam | x + y i."""
    z = (x + y * iota) % l
    if z == 0:
        return None
    r = pow(z, (l - 1) // 4, l)
    for k, v in enumerate((1, iota, l - 1, (l - iota) % l)):
        if r == v % l:
            return k
    raise RuntimeError("quartic character not a 4th root of unity")


def chi_inert(x, y, l):
    """exponent k with chi_l(x + y i) = i^k in F_l[i], l = 3 mod 4."""
    e = (l * l - 1) // 4
    rx, ry, bx, by = 1, 0, x % l, y % l
    if bx == 0 and by == 0:
        return None
    while e:
        if e & 1:
            rx, ry = (rx*bx - ry*by) % l, (rx*by + ry*bx) % l
        bx, by = (bx*bx - by*by) % l, (2*bx*by) % l
        e >>= 1
    for k, v in enumerate(((1, 0), (0, 1), (l - 1, 0), (0, l - 1))):
        if (rx, ry) == v:
            return k
    raise RuntimeError("quartic character not a 4th root of unity")


def gaussian_primes_over(l):
    """The quartic characters at the Gaussian primes over l (none for
    l = 2)."""
    if l == 2:
        return []
    if l % 4 == 1:
        io = sqrt_minus1(l)
        return [(lambda x, y, io=io: chi_split(x, y, l, io))
                for io in (io, l - io)]
    return [lambda x, y: chi_inert(x, y, l)]


def _fourth_powers_mod(M):
    """{rho^4 mod M : rho primitive}, as (Re, Im) pairs."""
    out = set()
    for e in range(M):
        for f in range(M):
            if (e - f) % 2 == 0:
                continue
            rx, ry = 1, 0
            for _ in range(4):
                rx, ry = (rx*e - ry*f) % M, (rx*f + ry*e) % M
            out.add((rx, ry))
    return out


_FOURTH32 = _fourth_powers_mod(32)
_FOURTH64 = _fourth_powers_mod(64)
# combination reductions lam | u R4 + v I4:
#   rho^4 = R4 + i I4 = I4 (u i - v)/u  mod lam
_COMBOS = ((1, 2), (1, -2), (1, 3), (1, -3), (1, 4), (1, -4),
           (2, 1), (2, -1), (3, 1), (3, -1))


def kill_reason(p, D, E, c1, s1, combos=True):
    """None if every condition holds (the case SURVIVES the sieve);
    otherwise the tag of a failing family.  With SIGNED (D, E) the
    equation (1+i) rho^4 = E + i p^2 D is exact (no unit), so every
    condition is unit-free."""
    R4, I4 = (p*p*D + E) // 2, (p*p*D - E) // 2
    # 2-adic: rho^4 mod 32 / 64 lies in a fixed small set
    if (R4 % 32, I4 % 32) not in _FOURTH32:
        return "2adic"
    if (R4 % 64, I4 % 64) not in _FOURTH64:
        return "2adic"
    fixed = []
    for l in factor(D)[0]:
        for chi in gaussian_primes_over(l):
            fixed.append(((chi(E, 0) + chi(1, 1) - chi(2, 0)) % 4, "D"))
    for l in factor(E)[0]:
        for chi in gaussian_primes_over(l):
            fixed.append(((chi(p*p*D, 0) - chi(1, 1)) % 4, "E"))
    for l in factor(R4)[0]:
        for chi in gaussian_primes_over(l):
            fixed.append(((chi(0, 1) + chi(I4, 0)) % 4, "R"))
    for l in factor(I4)[0]:
        if l == 2:
            continue
        for chi in gaussian_primes_over(l):
            fixed.append((chi(R4, 0) % 4, "I"))
    if D in (c1 + s1, c1 - s1, -(c1 + s1), -(c1 - s1)):
        K = (p*p - 1) * D // 2
        for l in factor(K)[0]:
            if l == 2:
                continue
            for chi in gaussian_primes_over(l):
                v = chi(c1, s1)
                if v is not None:
                    fixed.append(((2 * v) % 4, "K"))
    if combos:
        for u, v in _COMBOS:
            for l in factor(u*R4 + v*I4)[0]:
                if l == 2:
                    continue
                for chi in gaussian_primes_over(l):
                    cI, cw, cu = chi(I4, 0), chi(-v, u), chi(u, 0)
                    if None in (cI, cw, cu):
                        continue
                    fixed.append(((cI + cw - cu) % 4, "C"))
    for v, tag in fixed:
        if v % 4:
            return tag
    return None


def intermediate_splits(p):
    """(c1, s1, A4, [(D, E)]) for the coprime intermediate divisor
    splits of A4 = c1^2 - s1^2 at the prime frame of p."""
    from compute.zi_additive import gaussian_prime_over
    a, b = gaussian_prime_over(p)
    c1, s1 = abs(a*a - b*b), abs(2*a*b)
    A4 = c1*c1 - s1*s1
    f, _ = factor(A4)
    out = []
    for D in divisors_from(f):
        if D == 1 or D == abs(A4) or gcd(D, abs(A4) // D) != 1:
            continue
        for sD in (D, -D):
            out.append((sD, A4 // sD))
    return c1, s1, A4, out


def self_test(trials=200, seed=7):
    """Synthetic (1+i) rho^4 = ax + i ay must pass [D][E][R][I] with
    eps = 1 (reading E := ax, p^2 D := ay, R4 + i I4 := rho^4)."""
    import random
    rng = random.Random(seed)
    n_ok = n_run = 0
    for _ in range(trials):
        e, f = rng.randint(1, 80), rng.randint(1, 80)
        if gcd(e, f) != 1 or (e - f) % 2 == 0:
            continue
        rx, ry = 1, 0
        for _k in range(4):
            rx, ry = rx*e - ry*f, rx*f + ry*e
        ax, ay = rx - ry, rx + ry
        good = True
        for l in factor(ay)[0]:
            for chi in gaussian_primes_over(l):
                if (chi(ax, 0) + chi(1, 1) - chi(2, 0)) % 4:
                    good = False
        for l in factor(ax)[0]:
            for chi in gaussian_primes_over(l):
                if (chi(ay, 0) - chi(1, 1)) % 4:
                    good = False
        for l in factor(rx)[0]:
            for chi in gaussian_primes_over(l):
                if (chi(0, 1) + chi(ry, 0)) % 4:
                    good = False
        for l in factor(ry)[0]:
            if l == 2:
                continue
            for chi in gaussian_primes_over(l):
                if chi(rx, 0) % 4:
                    good = False
        # and the FULL sieve end to end: reading p = 1, D = ay, E = ax
        # (no natural split), kill_reason must return None
        if kill_reason(1, ay, ax, 0, 0) is not None:
            good = False
        n_run += 1
        n_ok += good
    return n_ok, n_run
