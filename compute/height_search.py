"""THE FINITE SEARCH behind a height cap (entry 123).  For a class whose height system caps all its
primes, every prime triple inside the caps is tested against (i) every inequality of the system,
exactly; (ii) the CP.2 residue conditions (a C/D-deficit prime is 1 mod 8; a four-maxima prime admits
t with t, 1+t, 1-t nonzero squares); (iii) every exact divisibility of the system -- for a binomial
p_j^{2g} | Im(A), Re(A) or N(A - lambda Abar), for a trinomial pi_j^{4M} | S -- under every choice of
conjugate frames (pi_k or pibar_k per prime; the class is a representative up to those choices);
(iv) a triple surviving all of that is tested against the ledger's relations R1 = R2 = 0 themselves.
No survivor of (iv) means the class is impossible: an unconditional kill.

Gaussian integers are pairs of Python ints; a prime p = 1 mod 4 is factored as p = c^2 + s^2 with
pi = c + i s (c > s > 0); its conjugate is the other frame."""
import math
from fractions import Fraction
from itertools import product

from compute.height_system import system, _rows


def two_squares(p):
    """c > s > 0 with c^2 + s^2 = p for a prime p = 1 mod 4 (Cornacchia by search: p is small here)."""
    s = 1
    while 2 * s * s < p:
        c2 = p - s * s
        c = math.isqrt(c2)
        if c * c == c2:
            return c, s
        s += 1
    raise ValueError(p)


def split_primes(bound):
    out = []
    for p in range(5, bound + 1, 4):
        if all(p % q for q in range(3, math.isqrt(p) + 1, 2)):
            out.append(p)
    return out


def gmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def gpow(z, n):
    r = (1, 0)
    for _ in range(n):
        r = gmul(r, z)
    return r


def gconj(z):
    return (z[0], -z[1])


def four_maxima_ok(p):
    sq = {x * x % p for x in range(1, p)}
    return any(t in sq and (1 + t) % p in sq and (1 - t) % p in sq for t in range(2, p - 1))


def divisible_by_pi_power(S, pi, p, n):
    """pi^n | S in Z[i]  <=>  p^n | S * pibar^n (both coordinates)."""
    t = gmul(S, gpow(gconj(pi), n))
    q = p ** n
    return t[0] % q == 0 and t[1] % q == 0


def class_conditions(cand, version=2):
    """The exact conditions of a class: rows (inequalities), per-prime residue roles, and the
    divisibility descriptors (binomials and trinomials with their exact data)."""
    cols, ineqs, lower = system(cand, version)
    n = len(lower)
    rows = _rows(n, ineqs, lower)
    return cols, rows, [c["role"] for c in cols]


def check_inequalities(rows, ps):
    for a, K, name in rows:
        lhs = Fraction(1)
        for p, e in zip(ps, a):
            if e:
                lhs *= Fraction(p) ** e
        if lhs > K:
            return False
    return True


def divisibility_ok(cols, ps, pis):
    """Every binomial and trinomial divisibility for the given frames pis (Gaussian integers)."""
    for c in cols:
        j, M = c["j"], c["M"]
        pj, pij = ps[j], pis[j]
        for r in c["relations"]:
            if r["kind"] == "binomial":
                A = (1, 0)
                for k, dk in r["d"].items():
                    A = gmul(A, gpow(pis[k] if dk > 0 else gconj(pis[k]), 2 * abs(dk)))
                q = pj ** (2 * c["g"])
                if r["integer"] == "Im":
                    if A[1] % q:
                        return False
                elif r["integer"] == "Re":
                    if A[0] % q:
                        return False
                else:
                    lam = r["lam"]
                    Ab = gconj(A)
                    diff = (A[0] - lam * Ab[0], A[1] - lam * Ab[1])
                    if (diff[0] * diff[0] + diff[1] * diff[1]) % q:
                        return False
            else:
                trip, a = r["labels"], r["coeffs"]
                ks = list(c["f"][trip[0]].keys())
                fmin = {k: min(c["f"][X][k] for X in trip) for k in ks}
                fmax = {k: max(c["f"][X][k] for X in trip) for k in ks}
                S = (0, 0)
                for X in trip:
                    T = (1, 0)
                    for k in ks:
                        T = gmul(T, gpow(pis[k], 2 * (c["f"][X][k] - fmin[k])))
                        T = gmul(T, gpow(gconj(pis[k]), 2 * (fmax[k] - c["f"][X][k])))
                    S = (S[0] + a[X] * T[0], S[1] + a[X] * T[1])
                if not divisible_by_pi_power(S, pij, pj, 4 * M):
                    return False
    return True


def relations_vanish(cand, pis):
    """The ledger's relations R1, R2 at the frames l_j = pi_j^2 (exact integers)."""
    from compute import omega3 as O
    sub = {}
    for (c, s), pi in zip(O.FR, pis):
        l = gpow(pi, 2)
        sub[c], sub[s] = l[0], l[1]
    A, B, C, D, eA, eB, eC, eD = cand
    box = O.BOX
    e = {X: int(O.elem_box(tuple(lab), box).subs(sub)) for X, lab in zip("ABCD", (A, B, C, D))}
    return eA * e["A"] + eB * e["B"] - eC * e["C"] == 0 and eA * e["A"] - eB * e["B"] - eD * e["D"] == 0


def search(cand, caps, box, version=2):
    """Enumerate the prime triples inside the caps; returns the report (the system version recorded)."""
    from compute import omega3 as O
    O.set_box(tuple(box))
    cols, rows, roles = class_conditions(cand, version)
    n = len(caps)
    bound = int(max(caps)) + 1
    primes = split_primes(bound)
    pinfo = {p: {"pi": two_squares(p), "mod8": p % 8 == 1, "fourmax": None} for p in primes}
    cand_primes = []
    for j in range(n):
        ok = []
        for p in primes:
            if p > caps[j]:
                continue
            if roles[j] in "CD" and not pinfo[p]["mod8"]:
                continue
            if roles[j] == "*":
                if pinfo[p]["fourmax"] is None:
                    pinfo[p]["fourmax"] = four_maxima_ok(p)
                if not pinfo[p]["fourmax"]:
                    continue
            ok.append(p)
        cand_primes.append(ok)
    n_triples = n_ineq = n_div = 0
    survivors = []
    for ps in product(*cand_primes):
        if len(set(ps)) < n:
            continue
        n_triples += 1
        if not check_inequalities(rows, ps):
            continue
        n_ineq += 1
        base = [pinfo[p]["pi"] for p in ps]
        for pattern in product((1, -1), repeat=n):
            pis = [pi if sgn == 1 else gconj(pi) for pi, sgn in zip(base, pattern)]
            if divisibility_ok(cols, ps, pis):
                n_div += 1
                if relations_vanish(cand, pis):
                    survivors.append({"primes": list(ps), "pattern": list(pattern)})
    return {"version": version, "caps": caps, "n_candidate_primes": [len(c) for c in cand_primes], "n_triples": n_triples,
            "n_pass_inequalities": n_ineq, "n_pass_divisibility": n_div, "survivors": survivors}
