"""Numeric verification of the height system's algebra with genuine Gaussian primes (entry 123):
the dictionary between the ledger's elements and s(Z_X), the CP.3 congruences at their exact
valuations, the binomial and trinomial constructions.  Exact Gaussian-rational arithmetic; no
floating point.  Used by the check a3.height_system."""
import math
import random
from fractions import Fraction

from compute.height_system import column


class Gi:
    """A Gaussian rational a + b i with Fraction coordinates."""
    __slots__ = ("a", "b")

    def __init__(s, a, b=0):
        s.a, s.b = Fraction(a), Fraction(b)

    def __add__(s, o):
        o = o if isinstance(o, Gi) else Gi(o)
        return Gi(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = o if isinstance(o, Gi) else Gi(o)
        return Gi(s.a - o.a, s.b - o.b)

    def __mul__(s, o):
        o = o if isinstance(o, Gi) else Gi(o)
        return Gi(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def conj(s):
        return Gi(s.a, -s.b)

    def norm(s):
        return s.a * s.a + s.b * s.b

    def inv(s):
        n = s.norm()
        return Gi(s.a / n, -s.b / n)

    def __truediv__(s, o):
        o = o if isinstance(o, Gi) else Gi(o)
        return s * o.inv()

    def __pow__(s, n):
        r = Gi(1)
        base = s if n >= 0 else s.inv()
        for _ in range(abs(n)):
            r = r * base
        return r

    def is_int(s):
        return s.a.denominator == 1 and s.b.denominator == 1

    def __repr__(s):
        return f"({s.a}+{s.b}i)"


def val_pi(z, pi, p, cap=60):
    """v_pi(z) for a Gaussian rational z: v_pi of the numerator minus v_p of the rational denominator."""
    den = 1
    for x in (z.a, z.b):
        den = den * x.denominator // math.gcd(den, x.denominator)
    vden = 0
    while den % p == 0:
        den //= p
        vden += 1
    w = z * (den * p ** vden)
    v = 0
    pb = pi.conj()
    while v <= cap:
        t = w * pb
        if t.a % p == 0 and t.b % p == 0:
            w = Gi(t.a / p, t.b / p)
            v += 1
        else:
            break
    return v - vden


PRIMES = {5: Gi(2, 1), 13: Gi(3, 2), 17: Gi(4, 1), 29: Gi(5, 2), 37: Gi(6, 1), 41: Gi(5, 4), 53: Gi(7, 2), 61: Gi(6, 5)}


def s_of(Z):
    return Z - Z.inv()


def identity_tests(trials=40, seed=1):
    """Random classes of the boxes (1,1,1), (2,1,1), (2,2,1), (3,1,1) at random genuine frames:
    returns the number of exact identities verified (raises on the first failure)."""
    from compute import omega3 as O
    rng = random.Random(seed)
    n_tests = 0
    for _ in range(trials):
        box = rng.choice([(1, 1, 1), (2, 1, 1), (2, 2, 1), (3, 1, 1)])
        ps = rng.sample(sorted(PRIMES), 3)
        pis = [PRIMES[p] for p in ps]
        rho = [pi / pi.conj() for pi in pis]
        while True:
            labels = [tuple(rng.randint(-a, a) for a in box) for _ in range(4)]
            eps = [rng.choice((1, -1)) for _ in range(4)]
            cand = [list(l) for l in labels] + eps
            try:
                cols = [column(cand, j) for j in range(3)]
            except ValueError:
                continue
            break
        Z = [Gi(1) for _ in range(4)]
        for X in range(4):
            for j in range(3):
                Z[X] = Z[X] * rho[j] ** (2 * eps[X] * labels[X][j])
        # (0) the dictionary: m^2 s(Z_X) / (2i) = eps_X elem_box(X) at the frames l_j = pi_j^2
        m2 = 1
        for p, a in zip(ps, box):
            m2 *= p ** (2 * a)
        sub = {}
        for (c, s_), pi in zip(O.FR, pis):
            l = pi * pi
            sub[c], sub[s_] = int(l.a), int(l.b)
        for X in range(4):
            lhs = s_of(Z[X]) * m2 / Gi(0, 2)
            rhs = eps[X] * int(O.elem_box(labels[X], box).subs(sub))
            assert lhs.b == 0 and lhs.a == rhs, ("dictionary", lhs, rhs)
            n_tests += 1
        for j in range(3):
            c = cols[j]
            pi, p, M = pis[j], ps[j], c["M"]
            # (1) CP.3: pi^{2M} s(Z_X) = q_X + O(pi^{4M}) for maximal X; in (pi^{2g}) for the deficient label
            for X in c["maximal"]:
                U = Gi(1)
                for k, fk in c["f"][X].items():
                    U = U * rho[k] ** (2 * fk)
                q = (-c["sigma"][X]) * (pi.conj() ** (2 * M)) * U
                v = val_pi(pi ** (2 * M) * s_of(Z[X]) - q, pi, p)
                assert v >= 4 * M, ("CP.3 maximal", v, 4 * M)
                n_tests += 1
            if c["deficient"] is not None:
                v = val_pi(pi ** (2 * M) * s_of(Z[c["deficient"]]), pi, p)
                assert v >= 2 * c["g"], ("CP.3 deficient", v, 2 * c["g"])
                n_tests += 1
            # (2) binomials: U_Y / U_X = A / Abar with |A| = P, A neither real nor imaginary, 4 | Im A, Re A odd
            #     trinomials: S = sum a_X T_X is a nonzero Gaussian integer equal to (a unit at pi_j) times sum a_X U_X
            for r in c["relations"]:
                if r["kind"] == "binomial":
                    X, Y = r["pair"]
                    UX, UY = Gi(1), Gi(1)
                    for k, fk in c["f"][X].items():
                        UX = UX * rho[k] ** (2 * fk)
                    for k, fk in c["f"][Y].items():
                        UY = UY * rho[k] ** (2 * fk)
                    A = Gi(1)
                    for k, dk in r["d"].items():
                        A = A * ((pis[k] ** (2 * dk)) if dk > 0 else (pis[k].conj() ** (2 * (-dk))))
                    diff = UY / UX - A / A.conj()
                    assert diff.a == 0 and diff.b == 0, "U_Y/U_X = A/Abar"
                    P = 1
                    for k, dk in r["d"].items():
                        P *= ps[k] ** abs(dk)
                    assert A.is_int() and A.norm() == P * P and A.a != 0 and A.b != 0
                    if r["integer"] == "Im":
                        assert A.b % (2 ** r["two_adic"]) == 0, ("2-adic", A, r["two_adic"])
                    if r["integer"] == "Re":
                        assert A.a % 2 == 1, ("Re odd", A)
                    n_tests += 1
                else:
                    trip, a = r["labels"], r["coeffs"]
                    ks = list(c["f"][trip[0]].keys())
                    fmin = {k: min(c["f"][X][k] for X in trip) for k in ks}
                    fmax = {k: max(c["f"][X][k] for X in trip) for k in ks}
                    Q = 1
                    for k in ks:
                        Q *= ps[k] ** (fmax[k] - fmin[k])
                    S = Gi(0)
                    for X in trip:
                        T = Gi(1)
                        for k in ks:
                            T = T * pis[k] ** (2 * (c["f"][X][k] - fmin[k])) * pis[k].conj() ** (2 * (fmax[k] - c["f"][X][k]))
                        assert T.norm() == Q * Q
                        S = S + a[X] * T
                    assert S.is_int() and not (S.a == 0 and S.b == 0), "S a nonzero Gaussian integer"
                    U_sum = Gi(0)
                    for X in trip:
                        U = Gi(1)
                        for k, fk in c["f"][X].items():
                            U = U * rho[k] ** (2 * fk)
                        U_sum = U_sum + a[X] * U
                    ratio = S / U_sum
                    assert val_pi(ratio, pi, p) == 0 and val_pi(ratio.inv(), pi, p) == 0, "S = (unit at pi) * sum a U"
                    n_tests += 1
    return n_tests


def residue_facts():
    """CP.2's lower bounds: for p in 5, 13, 17 no t with t, 1+t, 1-t nonzero squares; for 29 there is;
    2 is a square exactly for p = 1 mod 8 (17, 41), not for 5, 13, 29, 37."""
    out = {}
    for p in (5, 13, 17, 29, 37, 41):
        sq = {x * x % p for x in range(1, p)}
        out[p] = {"four_maxima_t": [t for t in range(2, p - 1) if t in sq and (1 + t) % p in sq and (1 - t) % p in sq], "two_square": 2 in sq}
    return out


def circuit_identity_tests(trials=30, seed=2):
    """The exact decomposition behind the reality sharpening (T'), on random classes at genuine frames:
    for every circuit among maximal labels,  sum_X c_X pi^{2M} s(Z_X) = -pibar^{2M} W + pi^{4M} pibar^{-2M} Wbar
    with W = sum_X c_X sigma_X U_X, and S = sum a_X T_X equals G W with G = prod pi_k^{-2 fmin_k} pibar_k^{2 fmax_k}.
    (A solution has the left side 0, hence pibar^{4M} W = pi^{4M} Wbar and S_1 Gbar real.)"""
    from compute.height_system import CIRCUITS
    rng = random.Random(seed)
    n_tests = 0
    for _ in range(trials):
        box = rng.choice([(1, 1, 1), (2, 1, 1), (2, 2, 1)])
        ps = rng.sample(sorted(PRIMES), 3)
        pis = [PRIMES[p] for p in ps]
        rho = [pi / pi.conj() for pi in pis]
        while True:
            labels = [tuple(rng.randint(-a, a) for a in box) for _ in range(4)]
            eps = [rng.choice((1, -1)) for _ in range(4)]
            cand = [list(l) for l in labels] + eps
            try:
                cols = [column(cand, j) for j in range(3)]
            except ValueError:
                continue
            break
        Z = [Gi(1) for _ in range(4)]
        for X in range(4):
            for j in range(3):
                Z[X] = Z[X] * rho[j] ** (2 * eps[X] * labels[X][j])
        for j in range(3):
            c = cols[j]
            pi, M = pis[j], c["M"]
            U = {}
            for X in c["maximal"]:
                U[X] = Gi(1)
                for k, fk in c["f"][X].items():
                    U[X] = U[X] * rho[k] ** (2 * fk)
            for r in c["relations"]:
                if r["kind"] != "trinomial":
                    continue
                cc = CIRCUITS[r["circuit"]]
                lhs = Gi(0)
                for X in range(4):
                    if cc[X]:
                        lhs = lhs + cc[X] * (pi ** (2 * M)) * s_of(Z[X])
                W = Gi(0)
                for X in r["labels"]:
                    W = W + (cc[X] * c["sigma"][X]) * U[X]
                rhs = (-1) * (pi.conj() ** (2 * M)) * W + (pi ** (4 * M)) * (pi.conj() ** (-2 * M)) * W.conj()
                d = lhs - rhs
                assert d.a == 0 and d.b == 0, ("circuit decomposition", r["circuit"])
                G = Gi(1)
                for k in r["fmax"]:
                    G = G * pis[k] ** (-2 * r["fmin"][k]) * pis[k].conj() ** (2 * r["fmax"][k])
                S = Gi(0)
                for X in r["labels"]:
                    T = Gi(1)
                    for k in r["fmax"]:
                        T = T * pis[k] ** (2 * (c["f"][X][k] - r["fmin"][k])) * pis[k].conj() ** (2 * (r["fmax"][k] - c["f"][X][k]))
                    S = S + r["coeffs"][X] * T
                d = S - G * W
                assert d.a == 0 and d.b == 0, ("S = G W", r["circuit"])
                if sum(abs(v) for v in r["coeffs"].values()) == 4:
                    # version 3: with coefficients 2, +-1, +-1 the Gaussian integer S is even (every pi_k^2 is +-1 mod 4)
                    assert S.a % 2 == 0 and S.b % 2 == 0, ("S even for a 2, +-1, +-1 circuit", r["circuit"], S)
                n_tests += 1
    return n_tests
