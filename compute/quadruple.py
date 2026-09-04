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


def _normalize(pat):
    """The survey NORMAL FORM of a pattern: labels with j >= 0, and k > 0 when
    j = 0.  A label (j,k) and its negative (-j,-k) are the SAME D-element with
    Im negated (full conjugation of z^2), so flipping a label flips its
    coefficient.  Global sign: first coefficient positive."""
    out = []
    for (j, k), c in pat:
        if j < 0 or (j == 0 and k < 0):
            j, k, c = -j, -k, -c
        out.append(((j, k), c))
    out = tuple(sorted(out))
    if out and out[0][1] < 0:
        out = tuple((jk, -c) for jk, c in out)
    return out


def _partial_conj(pat):
    """The w -> wbar image (j,k) -> (j,-k), normalized.  The l -> lbar image
    (j,k) -> (-j,k) is the same pattern (each is the full conjugate of the
    other), so a pattern has exactly two images under the frame symmetries:
    itself and this one."""
    return _normalize(tuple(((j, -k), c) for (j, k), c in pat))


def _orbit_key(P, Q):
    """Unordered pair modulo simultaneous partial conjugation (and global signs)."""
    a = tuple(sorted([_normalize(P), _normalize(Q)]))
    b = tuple(sorted([_partial_conj(P), _partial_conj(Q)]))
    return min(a, b)


def _sym(pat, sj, sk):
    return tuple(((sj * j, sk * k), c) for (j, k), c in pat)


def quadruple_pairs(triples):
    """All DISTINCT quadruple pairs (T1, T2) among the open triples.  T2 ranges
    over every triple and its partial conjugate (the only two images of a
    pattern under the frame symmetries); labels are compared in the survey
    NORMAL FORM -- a raw-label comparison after the conjugation images (the
    entry-95 version) can never match a j > 0 label under l -> lbar and turns a
    shared j = 0 element (0,k) into (0,-k), so it was blind to pairs sharing a
    j = 0 element (harmless for the entry-95 boxes, whose 92 open triples have
    no j = 0 label -- entry 96 audit) and listed each orbit four times (56 =
    4 x 14).  A pair must share exactly two elements with OPPOSITE relative
    sign (u opposite, v same) and have distinct thirds.  One representative per
    orbit under simultaneous partial conjugation.  Returns a list of dicts."""
    out = {}
    N = [_normalize(t) for t in triples]
    for P in N:
        cP = _labels(P)
        for Q0 in N:
            for Q in (Q0, _partial_conj(Q0)):
                if Q == P:
                    continue
                cQ = _labels(Q)
                shared = sorted(set(cP) & set(cQ))
                if len(shared) != 2:
                    continue
                A, B = shared
                # opposite relative sign on the shared pair (quadruple)
                if cP[A] * cP[B] != -(cQ[A] * cQ[B]):
                    continue
                cc = [jk for jk in cP if jk not in shared]
                ee = [jk for jk in cQ if jk not in shared]
                if len(cc) != 1 or len(ee) != 1 or cc[0] == ee[0]:
                    continue
                out.setdefault(_orbit_key(P, Q), {"T1": P, "T2": Q, "shared": shared,
                                                   "third1": cc[0], "third2": ee[0]})
    return list(out.values())


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


# ------------------------------------------------- the joint residual solver (entry 95)
import sympy as _spj

_c1j, _s1j, _c2j, _s2j = _spj.symbols("c1j s1j c2j s2j")


def _cleared_poly(T):
    """The cleared relation of triple T as a sympy polynomial in the frame
    coordinates (c1, s1 = Re, Im of l; c2, s2 = Re, Im of w), = 0."""
    from compute.lucas_endpoints import cleared_terms
    expr = 0
    for cc, wp, wq, ec, poly in cleared_terms(T):
        for (a, b, c_, d_), v in poly.items():
            expr += v * _c1j ** a * _s1j ** b * _c2j ** c_ * _s2j ** d_
    return _spj.expand(expr)


def _is_frame_ratio(r):
    """A rational r = c1/s1 is realized by a frame iff, in lowest terms |r| =
    m/n, m^2 + n^2 is a perfect square (then (c1, s1) = t (m, n) up to signs on
    the circle c1^2 + s1^2 = p^2).  EITHER SIGN counts: the frame l = pi^2 can
    be any of +-pi^2, +-pibar^2 (associates and the conjugate of the Gaussian
    prime), so c1/s1 = +-(a^2 - b^2)/(2ab) -- the entry-95 version rejected
    negative ratios, a soundness gap closed by the entry-96 audit (no joint
    form has a negative frame-ratio root either, so the results stand)."""
    r = _spj.nsimplify(r)
    if not r.is_rational or r == 0:
        return False
    m, n = abs(int(r.p)), abs(int(r.q))
    return bool(_spj.integer_nthroot(m * m + n * n, 2)[1])


def joint_residual_kill(T1, T2):
    """Eliminate the w-frame between the two cleared relations of a quadruple
    pair.  A quadruple forces R1 = R2 = 0 on one frame, so the resultant
    Res_{s2}(R1, R2) vanishes; dropping the degenerate factors (c1, s1, c2 = 0
    or c1 = +-s1, all impossible on a real frame) leaves a homogeneous
    'joint form' Phi(c1, s1) that must vanish.  Phi = 0 needs c1/s1 to be a
    rational root of Phi that is a frame ratio; if none is, no quadruple.
    Returns dict(degrees, phi_degree, rational_roots, frame_roots, kills)."""
    R1 = _cleared_poly(T1)
    R2 = _cleared_poly(T2)
    if _spj.Poly(R1, _s2j).degree() < 1 or _spj.Poly(R2, _s2j).degree() < 1:
        return {"kills": False, "reason": "not degree>=1 in s2"}
    Res = _spj.resultant(_spj.Poly(R1, _s2j), _spj.Poly(R2, _s2j))
    if Res == 0:
        return {"kills": False, "reason": "R1, R2 share a factor (resultant 0)"}
    # Res = 0 is one equation in (c1, s1, c2).  Factor it; the quadruple makes one
    # irreducible factor vanish at the frame point.  SOUND kill: every non-constant
    # factor is either a MONOMIAL in {c1, s1, c2} (vanishes only at a zero coordinate --
    # impossible, frame legs are nonzero) or PURE in (c1, s1) with no frame-ratio root.
    # A factor still involving c2 non-trivially means s2-elimination did not decouple the
    # frames -- the method is then inconclusive for that pair.
    frame_roots, rational_roots, pure_forms = [], [], []
    for fac, mult in _spj.factor_list(Res)[1]:
        vs = fac.free_symbols & {_c1j, _s1j, _c2j}
        if len(_spj.Add.make_args(_spj.expand(fac))) == 1:
            continue                                   # monomial: only a zero coordinate
        if _c2j in vs:
            return {"kills": False, "reason": "c2-mixing factor (frames not decoupled)",
                    "factor": str(fac)}
        # pure in (c1, s1): every rational frame-ratio root must be absent
        pf = _spj.Poly(fac, _c1j, _s1j)
        pure_forms.append(pf.total_degree())
        phi = _spj.Poly(fac.subs(_s1j, 1), _c1j)
        for r in _spj.roots(phi, filter="Q"):
            rational_roots.append(str(r))
            if _is_frame_ratio(r):
                frame_roots.append(str(r))
    return {"kills": not frame_roots, "degrees": sorted(pure_forms),
            "rational_roots": rational_roots, "frame_roots": frame_roots}
