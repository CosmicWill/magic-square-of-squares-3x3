"""THE PAIR SEARCH (entry 125).  For an open class the height system's divisibilities are congruences
between the primes: at a deficient column j a binomial says p_j^{2g} | I(pi_k, pi_l) with I = Im A or
Re A an explicit integer in the other two frames; at a four-maxima column a trinomial says
pi_j^{4M} | S(pi_k, pi_l).  So a pair (p_k, p_l) determines finitely many candidates for p_j: the
prime-power divisors of I or of N(S).  Enumerating every pair of split primes up to B in every column
therefore finds every solution of the class whose two smallest primes are at most B, whatever the
third prime is; each candidate triple is then tested against every inequality, residue condition and
divisibility of the system under every conjugate-frame choice, and finally against the relations
R1 = R2 = 0 themselves.  No survivor means: the class has no solution whose two smallest primes are
<= B.  A survivor of the divisibilities that fails the relations is recorded as a near miss."""
import math
from functools import lru_cache
from itertools import product

import sympy as sp

from compute.height_search import (check_inequalities, divisibility_ok, four_maxima_ok, gconj, gmul, gpow,
                                   relations_vanish, split_primes, two_squares)
from compute.height_system import LOWER_BOUND, system, _rows


@lru_cache(maxsize=None)
def factor(n):
    return sp.factorint(n)


@lru_cache(maxsize=None)
def four_maxima(p):
    return four_maxima_ok(p)


def prime_ok(p, role, others):
    if p in others or p % 4 != 1 or p < LOWER_BOUND[role]:
        return False
    if role in "CD" and p % 8 != 1:
        return False
    if role == "*" and not four_maxima(p):
        return False
    return True


def binomial_integer(rel, pis_by_index):
    A = (1, 0)
    for k, dk in rel["d"].items():
        A = gmul(A, gpow(pis_by_index[k] if dk > 0 else gconj(pis_by_index[k]), 2 * abs(dk)))
    if rel["integer"] == "Im":
        return abs(A[1])
    if rel["integer"] == "Re":
        return abs(A[0])
    Ab = gconj(A)
    diff = (A[0] - rel["lam"] * Ab[0], A[1] - rel["lam"] * Ab[1])
    return diff[0] * diff[0] + diff[1] * diff[1]


def trinomial_S(col, rel, pis_by_index):
    trip, a = rel["labels"], rel["coeffs"]
    ks = list(col["f"][trip[0]].keys())
    fmin = {k: min(col["f"][X][k] for X in trip) for k in ks}
    fmax = {k: max(col["f"][X][k] for X in trip) for k in ks}
    S = (0, 0)
    for X in trip:
        T = (1, 0)
        for k in ks:
            T = gmul(T, gpow(pis_by_index[k], 2 * (col["f"][X][k] - fmin[k])))
            T = gmul(T, gpow(gconj(pis_by_index[k]), 2 * (fmax[k] - col["f"][X][k])))
        S = (S[0] + a[X] * T[0], S[1] + a[X] * T[1])
    return S


def determining_relation(col):
    """The cheapest relation of a column that determines p_j from the other primes: a binomial with
    |lambda| = 1 if there is one, else any binomial, else the trinomial of smallest spread."""
    bins = [r for r in col["relations"] if r["kind"] == "binomial"]
    if bins:
        unit = [r for r in bins if abs(r["lam"]) == 1]
        return (unit or bins)[0]
    tris = [r for r in col["relations"] if r["kind"] == "trinomial"]
    return min(tris, key=lambda r: sum(r["r"].values()))


def candidates(col, rel, pis_by_index, ps_by_index):
    """Candidate (p_j, pi_j) from the determining relation at the given frames of the other primes."""
    j, role = col["j"], col["role"]
    others = set(ps_by_index.values())
    out = []
    if rel["kind"] == "binomial":
        I = binomial_integer(rel, pis_by_index)
        if I == 0:
            return None                      # cannot happen for a genuine relation; flagged by the caller
        need = 2 * col["g"]
        for p, e in factor(I).items():
            if e >= need and prime_ok(p, role, others):
                c, s = two_squares(p)
                out.extend([(p, (c, s)), (p, (c, -s))])
    else:
        S = trinomial_S(col, rel, pis_by_index)
        N = S[0] * S[0] + S[1] * S[1]
        if N == 0:
            return None
        need = 4 * col["M"]
        for p, e in factor(N).items():
            if e >= need and prime_ok(p, role, others):
                c, s = two_squares(p)
                for pi in ((c, s), (c, -s)):
                    t = gmul(S, gpow(gconj(pi), need))
                    q = p ** need
                    if t[0] % q == 0 and t[1] % q == 0:
                        out.append((p, pi))
    return out


def pair_search(cand, box, bound, version=3):
    """Every pair of split primes <= bound in every pair of columns, every conjugate-frame choice of
    the pair; the third prime from the determining relation; full verification of each candidate."""
    from compute import omega3 as O
    O.set_box(tuple(box))
    cols, ineqs, lower = system(cand, version)
    n = len(lower)
    rows = _rows(n, ineqs, lower)
    roles = [c["role"] for c in cols]
    primes = split_primes(bound)
    frames = {p: two_squares(p) for p in primes}
    rep = {"bound": bound, "version": version, "n_primes": len(primes), "columns": {}, "near_misses": [], "survivors": [], "degenerate_relations": 0}
    for j in range(n):
        col = cols[j]
        rel = determining_relation(col)
        others = [k for k in range(n) if k != j]
        n_pairs = n_cand = n_pass_ineq = n_pass_div = 0
        for pk, pl in product(primes, primes):
            if pk == pl:
                continue
            if not prime_ok(pk, roles[others[0]], {pl}) or not prime_ok(pl, roles[others[1]], {pk}):
                continue
            n_pairs += 1
            for pattern in product((1, -1), repeat=2):
                pis = {others[0]: frames[pk] if pattern[0] == 1 else gconj(frames[pk]),
                       others[1]: frames[pl] if pattern[1] == 1 else gconj(frames[pl])}
                ps = {others[0]: pk, others[1]: pl}
                cs = candidates(col, rel, pis, ps)
                if cs is None:
                    rep["degenerate_relations"] += 1
                    continue
                for pj, pij in cs:
                    n_cand += 1
                    ps_full = [0] * n
                    pis_full = [None] * n
                    for k in others:
                        ps_full[k], pis_full[k] = ps[k], pis[k]
                    ps_full[j], pis_full[j] = pj, pij
                    if not check_inequalities(rows, ps_full):
                        continue
                    n_pass_ineq += 1
                    if divisibility_ok(cols, ps_full, pis_full):
                        n_pass_div += 1
                        if relations_vanish(cand, pis_full):
                            rep["survivors"].append({"primes": ps_full, "frames": pis_full})
                        else:
                            rep["near_misses"].append({"primes": ps_full, "frames": pis_full})
        rep["columns"][j] = {"role": roles[j], "relation": rel["circuit"] + ":" + rel["kind"], "n_pairs": n_pairs, "n_candidates": n_cand,
                             "n_pass_inequalities": n_pass_ineq, "n_pass_divisibility": n_pass_div}
    return rep
