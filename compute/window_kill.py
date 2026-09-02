"""The WINDOW finisher (entry 86): levers, size windows, exact pins, the
pincer, and the Fermat-quartic endpoint -- the mechanisms of the H3
double lever (A3 section 2.10) and the G3 double pincer (entry 63)
made mechanical.

Levers.  For each pair collapse of an OPEN pattern,
      2 s p^{2a} q^{2b} T1(D) T2(M) = -c p^{2wp} q^{2wq} Trig(third)
the surplus ep = wp - a, eq = wq - b of the third term is what the
product side must absorb: a mixed factor is a unit at both primes and an
l-side Lucas value is a p-unit, a w-side value a q-unit (structural),
so a positive surplus p^{2ep} divides the pure-w factor of the product
(q^{2eq} the pure-l factor); a negative surplus is absorbed by the third
term's own Trig value, which must then be pure of the right side.  A
pattern may carry its two levers on two different collapses (G3).

Frame facts (classical; pinned in the suite as frame facts):
  * Trig(X^n), X = l (prime p) or w (prime q): C_n^2 + S_n^2 = P^{2n},
    both legs nonzero and coprime, so 0 < |C_n|, |S_n| < P^n.
  * Even index n = 2h: C_{2h} = (C_h - S_h)(C_h + S_h) with coprime ODD
    factors of modulus <= sqrt2 P^h; S_{2h} = 2 C_h S_h with the coprime
    legs of the index-h frame.  For h even: C_h odd, S_h even.  An odd
    prime power dividing a product of coprime factors divides exactly
    one of them (case split = the lever's targets, a disjunction).
  * WINDOW: R^e | X, X != 0, |X| < B  =>  X = +-R^e t, 0 < |t| < B/R^e.
    B/R^e <= 2  =>  t = +-1 (exact pin); X even with R^e odd => no t.
  * PINCER: p^al <= ka q^be and q^ga <= kb p^de combine to
    p^{al ga - be de} <= ka^ga kb^be; false for p >= 5 is a kill.
  * FERMAT: a leg pinned to +-R^e in a frame of even index h, e even:
    (other leg)^2 = (P^{h/2})^4 - (R^{e/2})^4, a nontrivial solution of
    Fermat's X^4 - Y^4 = Z^2 (classical: none).  Odd h or odd e is NOT
    a Fermat endpoint (25^2 + 312^2 = 313^2) and is refused.

Logic: levers are conjunctive, a lever's targets disjunctive.  The
pattern dies iff every tuple of targets is killed by a pincer, a
window parity kill, an empty window, or a Fermat pin.
"""
from __future__ import annotations

import itertools

import sympy as sp

from compute.lucas_endpoints import (cleared_terms, find_collapse, is_pure_w, is_pure_l)

SQRT2 = sp.sqrt(2)
PMIN = 5


def _targets(kind, n):
    """Coprime-factor cases for an odd prime power dividing Trig_kind(X^n)."""
    if n % 2 == 0 and n >= 2:
        h = n // 2
        if kind == "Re":
            return [{"name": f"({kind}{n}: C{h}-+S{h})", "bexp": h, "bconst": SQRT2, "parity": "odd", "leg": False, "index": h}]
        return [{"name": f"({kind}{n}: Re_{h})", "bexp": h, "bconst": 1, "parity": "odd" if h % 2 == 0 else "unknown", "leg": True, "index": h},
                {"name": f"({kind}{n}: Im_{h})", "bexp": h, "bconst": 1, "parity": "even" if h % 2 == 0 else "unknown", "leg": True, "index": h}]
    if n == 3:
        # Re(X^3) = X1 (4 X1^2 - 3 P^2),  Im(X^3) = Y1 (4 X1^2 - P^2)  (X1 = Re X, Y1 = Im X, X1^2 + Y1^2 = P^2);
        # gcd(leg, cofactor) | 3, so an odd prime power R^e (R >= 5) divides exactly one factor.
        # cofactor 4 X1^2 - a P^2 lies strictly in (-a P^2, (4-a) P^2): odd, |.| < 3 P^2.
        a = 3 if kind == "Re" else 1
        return [{"name": f"({kind}3: leg)", "bexp": 1, "bconst": 1, "parity": "unknown", "leg": True, "index": 1},
                {"name": f"({kind}3: 4X1^2-{a}P^2)", "bexp": 2, "bconst": 3, "parity": "odd", "leg": False, "index": 1, "cof": a}]
    return [{"name": f"({kind}{n})", "bexp": n, "bconst": 1, "parity": "unknown", "leg": True, "index": n}]


def _levers(pattern):
    """All levers of the pattern: list of dicts(prime, e, targets, where)."""
    terms = cleared_terms(pattern)
    if len(terms) != 3:
        return None
    levers = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            continue
        s, ap, bq, k1, D, k2, M = col
        cc, wpc, wqc, ec, _ = terms[c]
        ep, eq = wpc - ap, wqc - bq
        jc, kc = ec
        for prime, e in (("p", ep), ("q", eq)):
            if e == 0:
                continue
            pure = is_pure_w if prime == "p" else is_pure_l
            idx = 1 if prime == "p" else 0
            if e > 0:
                fac = [(m, k) for m, k in ((D, k1), (M, k2)) if pure(m)]
                if not fac:
                    return "DEAD-no-pure-factor"
                m, k = fac[0]
                levers.append({"prime": prime, "e": 2 * e, "targets": _targets(k, abs(m[idx])),
                               "where": f"pair {(a, b)}: {prime}^{2*e} | {k}({'w' if prime == 'p' else 'l'}^{abs(m[idx])})"})
            else:
                # the third term absorbs: must be pure of the other side
                if not pure(ec):
                    return "DEAD-no-pure-factor"
                levers.append({"prime": prime, "e": -2 * e, "targets": _targets("Im", abs(ec[idx])),
                               "where": f"pair {(a, b)}: third term absorbs {prime}^{-2*e} | Im({'w' if prime == 'p' else 'l'}^{abs(ec[idx])})"})
    return levers


def _ineq(lv, tgt):
    """lever prime^e | target  ->  (alpha, kappa, beta): prime^alpha <= kappa other^beta."""
    return (lv["e"], tgt["bconst"], tgt["bexp"])


def _pincer(ip, iq):
    """p^al <= ka q^be and q^ga <= kb p^de: contradiction for p, q >= PMIN?"""
    al, ka, be = ip
    ga, kb, de = iq
    ex = al * ga - be * de
    if ex <= 0:
        return None
    if sp.Integer(PMIN) ** ex > ka ** ga * kb ** be:
        return f"pincer: p^{al} <= {ka} q^{be} and q^{ga} <= {kb} p^{de} give p^{ex} <= {sp.nsimplify(ka**ga * kb**be)}"
    return None


def _window(lv, tgt, other):
    """Window on lever lv's target using the other prime's inequality
    other = (alpha, kappa, beta): other^alpha <= kappa * lv.prime^beta."""
    al, ka, be = other
    h = tgt["bexp"]
    ratio_const = tgt["bconst"] * ka ** sp.Rational(h, al)
    ratio_exp = sp.Rational(be * h, al) - lv["e"]
    if ratio_exp > 0:
        return "OPEN", None
    ratio = ratio_const * sp.Integer(PMIN) ** ratio_exp
    if ratio < 1 or (ratio == 1 and tgt["bconst"] == 1):
        return "DEAD", f"window on {tgt['name']}: |t| < {sp.nsimplify(ratio)} -- no nonzero t"
    if ratio <= 2:
        if tgt["parity"] == "even":
            return "DEAD", f"window on {tgt['name']}: t = +-1 but the target is even and {lv['prime']}^{lv['e']} odd"
        return "PIN", f"{tgt['name']} = +-{lv['prime']}^{lv['e']} exactly (|t| < {sp.nsimplify(ratio)})"
    return "OPEN", None


def _fermat(lv, tgt):
    if not tgt["leg"]:
        return None
    h, e = tgt["index"], lv["e"]
    if h % 2 == 0 and e % 2 == 0:
        return f"Fermat: (other leg)^2 = P^{2*h} - {lv['prime']}^{2*e} = (P^{h//2})^4 - ({lv['prime']}^{e//2})^4, nontrivial"
    return None


def _cof_pair(lv_p, tp, lv_q, tq):
    """Both levers land on index-3 cofactors (handled for e = e' = 2):
        p-lever on the w-frame:  4 U1^2 - a q^2  = t  p^2,   0 < U1^2 < q^2
        q-lever on the l-frame:  4 C1^2 - a' p^2 = t' q^2,   0 < C1^2 < p^2
    t, t' odd (the cofactors are odd).  With r = p^2/q^2 > 0:
        -a  < t  r < 4 - a      (from the first line)   -- upper bounds on r
        -a' < t' / r < 4 - a'   (from the second)        -- lower bounds on r
    and |t t'| < 9 (|t| < 3/r, |t'| < 3 r).  Mod 8: p^2 = q^2 = 1 and 4 X^2 in
    {0, 4}, so a + t and a' + t' lie in {0, 4} mod 8.  Kill iff no (t, t')
    admits an r; returns (message, None) or (None, feasible list)."""
    if lv_p["e"] != 2 or lv_q["e"] != 2:
        return None
    a, ap = tp["cof"], tq["cof"]
    feasible = []
    for t in range(-8, 9):
        if t % 2 == 0 or (a + t) % 8 not in (0, 4):
            continue
        for t2 in range(-8, 9):
            if t2 % 2 == 0 or (ap + t2) % 8 not in (0, 4) or abs(t * t2) >= 9:
                continue
            lo, hi = sp.Integer(0), sp.oo
            if t > 0:                       # t r < 4 - a
                hi = min(hi, sp.Rational(4 - a, t))
            if t < 0:                       # t r > -a  <=>  r < a / (-t)
                hi = min(hi, sp.Rational(a, -t))
            if t2 > 0:                      # t' < (4 - a') r  <=>  r > t' / (4 - a')
                lo = max(lo, sp.Rational(t2, 4 - ap))
            if t2 < 0:                      # t' > -a' r  <=>  r > (-t') / a'
                lo = max(lo, sp.Rational(-t2, ap))
            if lo < hi:
                feasible.append((t, t2, lo, hi))
    if feasible:
        return None, feasible
    return (f"index-3 cofactor pair: 4U1^2 = {a}q^2 + t p^2 and 4C1^2 = {ap}p^2 + t' q^2 with t, t' odd, "
            f"|tt'| < 9, mod 8 and the leg windows admit no (t, t', p^2/q^2)"), None


def window_kill(pattern):
    """Returns a certificate dict with 'kills': True, or a dict with the
    surviving case tuples, or a string verdict, or None (no levers)."""
    levers = _levers(pattern)
    if levers is None:
        return None
    if isinstance(levers, str):
        return {"kills": True, "how": levers}
    if not levers:
        return None
    p_lv = [i for i, lv in enumerate(levers) if lv["prime"] == "p"]
    q_lv = [i for i, lv in enumerate(levers) if lv["prime"] == "q"]
    cases_out = []
    all_dead = True
    for tup in itertools.product(*[range(len(lv["targets"])) for lv in levers]):
        chosen = [(lv, lv["targets"][t]) for lv, t in zip(levers, tup)]
        ineqs = {"p": [], "q": []}
        for lv, tgt in chosen:
            ineqs[lv["prime"]].append(_ineq(lv, tgt))
        why = None
        # pincers
        for ip in ineqs["p"]:
            for iq in ineqs["q"]:
                why = _pincer(ip, iq)
                if why:
                    break
            if why:
                break
        # both levers on index-3 cofactors: the pinned-pair solver
        if why is None:
            cof = [(lv, tgt) for lv, tgt in chosen if "cof" in tgt]
            if len(cof) == 2 and {cof[0][0]["prime"], cof[1][0]["prime"]} == {"p", "q"}:
                (lp, tp), (lq, tq) = sorted(cof, key=lambda x: x[0]["prime"])
                res = _cof_pair(lp, tp, lq, tq)
                if res is not None and res[0] is not None:
                    why = res[0]
        # windows (each lever's target, using every inequality of the other prime)
        if why is None:
            for lv, tgt in chosen:
                other = ineqs["q" if lv["prime"] == "p" else "p"]
                for oi in other:
                    st, msg = _window(lv, tgt, oi)
                    if st == "DEAD":
                        why = msg
                        break
                    if st == "PIN":
                        f = _fermat(lv, tgt)
                        if f:
                            why = f"{msg}; {f}"
                            break
                if why:
                    break
        names = [tgt["name"] for lv, tgt in chosen]
        if why is None:
            all_dead = False
            cases_out.append({"targets": names, "verdict": "OPEN"})
        else:
            cases_out.append({"targets": names, "verdict": "DEAD", "why": why})
    cert = {"levers": [lv["where"] for lv in levers], "cases": cases_out}
    if all_dead:
        cert["kills"] = True
    return cert
