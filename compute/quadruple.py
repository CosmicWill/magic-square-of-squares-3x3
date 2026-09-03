"""The QUADRUPLE ENGINE (entry 94): a direct attack on MSS3.

MSS3 <=> an additive QUADRUPLE u, v, u+v, u-v in one D(m) (doc 2, the
9-square row of the reduction table).  Such a quadruple contains two
additive triples on the shared pair {u, v}:
      T1 = {u, v, u+v}   with signs (+, +, -)   [u + v - (u+v) = 0]
      T2 = {u, v, u-v}   with signs (-, +, +)   [v + (u-v) - u = 0]
so u's sign is OPPOSITE between T1 and T2 and v's is the same; the two
triples SHARE the two elements u, v (same D-elements, hence same (j,k)
labels up to the conjugation symmetry the pattern canon already folds).
Both relations hold for the SAME center (same primes p, q and the same
frame), so the quadruple carries TWO relations -- and each relation, run
through the window finisher, forces a divisibility (a LEVER, a disjunction
of coprime-factor target bounds).  The frame must satisfy one target of
every lever of T1 AND of T2 at once; the quadruple is DEAD iff every such
selection is internally contradictory (a pincer p^e < const, e > 0,
impossible for p, q >= 5).

Soundness.  A lever of a single triple is a genuine forced divisibility
(the window finisher's `_levers`); pooling the levers of T1 and T2 is
valid because both relations hold for the quadruple.  The pincer over
EVERY target selection (not merely some) is the sound kill: the true
frame realizes one target per lever, unknown to us, so the contradiction
must hold for all.  Completeness: survey_box enumerates every OPEN triple
of the box (a triple killed on its own makes the quadruple dead a
fortiori), and we enumerate every pair sharing the quadruple structure.

This gives, per box (a, b): NO quadruple in any D(m) of split part
p^a q^b -- i.e. NO MSS3 with center split part p^a q^b -- whenever every
enumerated pair dies.
"""
from __future__ import annotations

import sympy as sp

from compute.lucas_endpoints import survey_box, kill_pattern
from compute.window_kill import _levers, _ineq, _pincer, PMIN


def open_triples(a, b):
    """The distinct OPEN triples of box (a, b): patterns that survive the
    full machine (kill_pattern).  A quadruple whose triple is machine-dead
    is dead, so only these can take part in a live quadruple."""
    verdict, opens = survey_box(a, b)
    out = []
    for pattern, kind in opens:
        if kind != "distinct":
            continue
        pat = tuple((tuple(jk), c) for jk, c in pattern)
        v, _c = kill_pattern(pat)
        if not v.startswith("DEAD"):
            out.append(pat)
    return out


def _labels(pat):
    return {jk: c for jk, c in pat}


def _sym(pat, sj, sk):
    return tuple(((sj * j, sk * k), c) for (j, k), c in pat)


def quadruple_pairs(triples):
    """All (T1, T2) among the open triples that share two elements with the
    quadruple sign structure (u opposite, v same).  T2 is taken over all
    conjugation images so that 'same element' is matched up to the symmetry
    (j,k) ~ (-j,-k).  Returns a list of dicts."""
    out = []
    n = len(triples)
    for i in range(n):
        P1 = triples[i]
        c1 = _labels(P1)
        for j2 in range(i, n):
            for sj in (1, -1):
                for sk in (1, -1):
                    if j2 == i and (sj, sk) == (1, 1):
                        continue
                    Q = _sym(triples[j2], sj, sk)
                    c2 = _labels(Q)
                    shared = sorted(set(c1) & set(c2))
                    if len(shared) != 2:
                        continue
                    A, B = shared
                    # opposite relative sign on the shared pair (quadruple)
                    if c1[A] * c1[B] != -(c2[A] * c2[B]):
                        continue
                    cc = [jk for jk in c1 if jk not in shared]
                    ee = [jk for jk in c2 if jk not in shared]
                    if len(cc) != 1 or len(ee) != 1 or cc[0] == ee[0]:
                        continue
                    out.append({"T1": P1, "T2": Q, "shared": shared,
                                "third1": cc[0], "third2": ee[0]})
    return out


def _lever_disjunctions(T):
    """List of levers of triple T; each lever is (prime, [ineqs]) -- a
    disjunction of target inequalities (alpha, kappa, beta)."""
    lv = _levers(T)
    if not isinstance(lv, list):
        return None
    out = []
    for L in lv:
        out.append((L["prime"], [_ineq(L, tgt) for tgt in L["targets"]]))
    return out


def pooled_kill(T1, T2):
    """SOUND pooled pincer: the quadruple carries every lever of T1 and T2.
    For every selection of one target per lever, some p-inequality and some
    q-inequality must pincer.  Returns (True, exponent_min) if every
    selection pincers, else (False, surviving_selection)."""
    L1 = _lever_disjunctions(T1)
    L2 = _lever_disjunctions(T2)
    if L1 is None or L2 is None:
        return None, "no-levers"
    levers = L1 + L2
    if not levers:
        return None, "no-levers"
    import itertools
    worst = None
    for sel in itertools.product(*[range(len(ineqs)) for _, ineqs in levers]):
        ps = [levers[t][1][si] for t, si in enumerate(sel) if levers[t][0] == "p"]
        qs = [levers[t][1][si] for t, si in enumerate(sel) if levers[t][0] == "q"]
        best_e = None
        for ip in ps:
            for iq in qs:
                w = _pincer(ip, iq)
                if w:
                    al, ka, be = ip
                    ga, kb, de = iq
                    e = sp.nsimplify(al * ga - be * de)
                    best_e = e if best_e is None else max(best_e, e)
        if best_e is None:
            return False, {"selection": [levers[t][1][si] for t, si in enumerate(sel)],
                           "primes": [levers[t][0] for t in range(len(levers))]}
        worst = best_e if worst is None else min(worst, best_e)
    return True, worst


def box_no_quadruple(a, b, triples=None):
    """Every quadruple pair of box (a, b) dies by the pooled pincer.
    Returns dict(box, n_open, n_pairs, all_dead, min_exponent, survivors)."""
    if triples is None:
        triples = open_triples(a, b)
    pairs = quadruple_pairs(triples)
    survivors = []
    min_e = None
    for pr in pairs:
        ok, info = pooled_kill(pr["T1"], pr["T2"])
        if ok:
            min_e = info if min_e is None else min(min_e, info)
        else:
            survivors.append({"T1": pr["T1"], "T2": pr["T2"], "why": info})
    return {"box": (a, b), "n_open": len(triples), "n_pairs": len(pairs),
            "all_dead": not survivors, "min_exponent": min_e, "survivors": survivors}
