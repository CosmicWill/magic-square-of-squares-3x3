"""Local locks: the p-adic layer of the fertile-seed arithmetic
(Lemma A9.14, docs/attacks/A9-discrete-spheres.md).

Two proven localization facts govern which scaling rungs a seed can
resurrect on:

(a) COHERENCE LOCALIZATION.  chi_p symbols of scaled values are
    invariant for p not dividing q (chi_p(q^2 t) = chi_p(t)) and all
    vanish for p | q.  Hence the scaled pair (qm, q^2 U, q^2 V) is
    coherent iff the base pair passes every chi_p line test at the
    primes p | 3m^2 with p not dividing q.  An incoherent seed's
    certificate primes are therefore forced divisors of q on any
    resurrecting rung.

(b) LINE-LOCK INVARIANCE.  For odd p with p not dividing q, the
    p-adic solvability data of every stratum's pair equations
    (t^2 + N k^2 = w_i w_j) is unchanged by scaling.  A line whose
    every stratum is p-locally insoluble stays dead on every rung
    with p not dividing q.

The functions here compute chi-certificates and local locks; the
verify check a9.local_locks pins the panel table and the soundness
control (alive lines are never locked).
"""

from __future__ import annotations

from math import gcd, isqrt

from .sphere_gluing import pair_lines, odd_primes


def _v(n, p):
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return v


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def chi_certificates(m, U, V):
    """All (p, line) chi_p incoherence certificates of the base pair."""
    certs = []
    for p in odd_primes(3 * m * m):
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            vals = {legendre(t, p) for t in tri}
            vals.discard(0)
            if len(vals) > 1:
                certs.append((p, i))
    return certs


def solvable_Zp(P, N, p, extra=4):
    """t^2 + N k^2 = P solvable over Z_p (lift-BFS, Hensel exit for
    odd p, solution-rich cap)."""
    e_target = 2 * max(_v(P, p), _v(N, p)) + extra + (3 if p == 2 else 1)
    mod = p
    S = {(t, k) for t in range(p) for k in range(p)
         if (t * t + N * k * k - P) % p == 0}
    lvl = 1
    while S and lvl < e_target:
        newS = set()
        for (t, k) in S:
            if p != 2 and ((2 * t) % p or (2 * N * k) % p):
                return True
            for a in range(p):
                for b in range(p):
                    t2, k2 = t + a * mod, k + b * mod
                    if (t2 * t2 + N * k2 * k2 - P) % (mod * p) == 0:
                        newS.add((t2, k2))
        S = newS
        mod *= p
        lvl += 1
        if len(S) > 4000:
            return True
    return bool(S)


def line_locked_at(tri, n, p):
    """True iff EVERY admissible stratum of the line has some pair
    equation Zp-insoluble (a genuine local lock at p)."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    for g in range(1, isqrt(min(G, n)) + 1):
        if G % (g * g) or n % (g * g):
            continue
        w = [t // (g * g) for t in tri]
        N = n // (g * g)
        if all(solvable_Zp(w[i] * w[j], N, p)
               for i, j in ((0, 1), (0, 2), (1, 2))):
            return False
    return True


def local_lock_table(m, U, V, places=None):
    """{line index: [locked places]} over 2 and the odd p | 3 m^2."""
    n = 3 * m * m
    if places is None:
        places = [2] + odd_primes(n)
    out = {}
    for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
        locked = [p for p in places if line_locked_at(tri, n, p)]
        if locked:
            out[i] = locked
    return out


def joint_solvable_modM(w, N, M):
    """The full three-pair + syzygy system solvable mod M.  For
    gcd(q, M) = 1 the change of variables t -> q^2 t, k -> qk makes
    the scaled system mod M equivalent to the base system mod M, so
    a joint lock at M forces gcd(q, M) > 1 on any resurrecting rung."""
    ksq = {(N * k * k) % M for k in range(M)}
    P = [(w[0] * w[1]) % M, (w[0] * w[2]) % M, (w[1] * w[2]) % M]
    ok_t = []
    for idx in range(3):
        s = [t for t in range(M) if (P[idx] - t * t) % M in ksq]
        if not s:
            return False
        ok_t.append(s)
    w123 = (w[0] * w[1] * w[2]) % M
    for t12 in ok_t[0]:
        a = (w123 - w[2] * t12 * t12) % M
        for t13 in ok_t[1]:
            b = (a - w[1] * t13 * t13) % M
            c2 = (2 * t12 * t13) % M
            for t23 in ok_t[2]:
                b3 = (b - w[0] * t23 * t23) % M
                tt = (c2 * t23) % M
                if b3 == tt or b3 == (-tt) % M:
                    return True
    return False


def line_joint_lock(tri, n, M):
    """True iff every admissible stratum's joint system is insoluble
    mod M."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    for g in range(1, isqrt(min(G, n)) + 1):
        if G % (g * g) or n % (g * g):
            continue
        if joint_solvable_modM([t // (g * g) for t in tri],
                               n // (g * g), M):
            return False
    return True
