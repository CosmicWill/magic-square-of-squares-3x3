"""The WINDOW finisher (entries 86-87): levers, coprime-factor targets at
every index, size windows, exact pins, the pincer, the Fermat-quartic
endpoint, and the cofactor-pair solver -- the mechanisms of the H3 double
lever (A3 section 2.10) and the G3 double pincer (entry 63) made
mechanical and uniform in the index.

Levers.  For each pair collapse of an OPEN pattern,
      2 s p^{2a} q^{2b} T1(D) T2(M) = -c p^{2wp} q^{2wq} Trig(third)
the surplus ep = wp - a, eq = wq - b of the third term is what the
product side must absorb: a mixed factor is a unit at both primes and an
l-side Lucas value is a p-unit, a w-side value a q-unit (structural),
so a positive surplus p^{2ep} divides the pure-w factor of the product
(q^{2eq} the pure-l factor); a negative surplus is absorbed by the third
term's own Trig value, which must then be pure of the right side.  A
pattern may carry its two levers on two different collapses (G3).

Frame facts (classical; pinned in the suite as frame facts).  The frames
are Gaussian SQUARES, l = pi^2 and w = rho^2, so X^n = (pi^n)^2 with
pi^n = a + bi, a^2 + b^2 = P^n odd:
  * C_n = Re(X^n) = a^2 - b^2 is ODD, S_n = Im(X^n) = 2ab is 0 mod 4;
    C_n^2 + S_n^2 = P^{2n}, both legs nonzero and coprime, so
    0 < |C_n|, |S_n| < P^n.
  * Odd n >= 3 (x = X1/P, u = x^2):  Re(X^n) = X1 P^{n-1} Q_R(u) with
    Q_R = T_n(x)/x,  Im(X^n) = Y1 P^{n-1} Q_I(u) with Q_I = U_{n-1}(x)
    (Chebyshev; both even in x).  |cos n.theta| <= n |cos theta| and
    |sin n.theta| <= n |sin theta| give |cofactor| < n P^{n-1} strictly
    (equality needs a zero leg).  gcd(leg, cofactor) | n.  Termwise
    X1^2 = P^2 = 1 mod 8, so cofactor_R = Q_R(1) = 1 and cofactor_I =
    Q_I(1) = n (mod 8); both odd.
  * Even n = 2h:  C_{2h} = (C_h - S_h)(C_h + S_h), coprime odd factors of
    modulus < sqrt2 P^h;  S_{2h} = 2 C_h S_h with the coprime legs of the
    index-h frame, which factor again (recursion).
  * An odd prime power dividing a product of coprime factors divides
    exactly one of them: a lever's TARGETS are a disjunction.  When the
    lever prime R may divide n, gcd(leg, cofactor) can carry R once, so
    the split cases R^{e-1} | leg (with R | cofactor) and R^{e-1} |
    cofactor are added as targets with the reduced exponent.
  * WINDOW: R^e | X, X != 0, |X| < B  =>  X = +-R^e t, 0 < |t| < B/R^e,
    t odd when X is odd, 4 | t when 4 | X, and t = X R^{-e} mod 8 (mod 4
    when e is odd, R = 1 mod 4) when the residue of X is known.
  * PINCER: p^al <= ka q^be and q^ga <= kb p^de combine to
    p^{al ga - be de} <= ka^ga kb^be; false for p >= 5 is a kill.
  * FERMAT: a leg pinned to +-R^e in a frame of even index h, e even:
    (other leg)^2 = (P^{h/2})^4 - (R^{e/2})^4, a nontrivial solution of
    Fermat's X^4 - Y^4 = Z^2 (classical: none).  Odd h or odd e is NOT
    a Fermat endpoint (25^2 + 312^2 = 313^2) and is refused.
  * COFACTOR PAIR: both levers on cofactors, Q_p(u) q^{n_p-1} = t p^{e_p}
    and Q_q(c) p^{n_q-1} = t' q^{e_q}; when homogeneous (n - 1 = e on
    both sides) the equations read Q_p(u) = t rho^{e_p}, Q_q(c) = t'
    rho^{-e_q} with rho = p/q, and the exact ranges of Q on [0,1], the
    residue filters and the odd/size bounds on t, t' leave an interval
    for rho per (t, t'); empty for all pairs is a kill.

Logic: levers are conjunctive, a lever's targets disjunctive.  The
pattern dies iff every tuple of targets is killed by a pincer, an empty
or parity-dead window, a residue-dead pin, a Fermat pin, or an empty
cofactor pair.  Every certificate lists the case and its kill.
"""
from __future__ import annotations

import itertools

import sympy as sp

from compute.lucas_endpoints import (cleared_terms, find_collapse, is_pure_w, is_pure_l)

SQRT2 = sp.sqrt(2)
PMIN = 5
_x, _u = sp.symbols("x u")


# ------------------------------------------------------------- targets
def cheb_cofactor(kind, n):
    """Q(u) with Trig_kind(X^n) = leg * P^{n-1} * Q(X1^2/P^2), n odd >= 3."""
    poly = sp.chebyshevt(n, _x) / _x if kind == "Re" else sp.chebyshevu(n - 1, _x)
    poly = sp.Poly(sp.expand(sp.cancel(poly)), _x)
    expr = sum(c * _u ** (k // 2) for (k,), c in poly.terms())      # even powers only
    return sp.Poly(expr, _u)


def _big_primes(n):
    """Primes r | n that a lever prime could equal: r >= 5 and r = 1 mod 4
    (a frame prime splits in Z[i]; 7 or 11 can never be p or q)."""
    return [r for r, _ in sp.factorint(n).items() if r >= PMIN and r % 4 == 1]


def _targets(kind, n, e):
    """Coprime-factor cases for a prime power R^e (R >= 5) dividing
    Trig_kind(X^n).  Each: name, bexp, bconst (|target| < bconst P^bexp),
    parity ('odd' | 'even4' | 'unknown'), res8 (residue mod 8 or None),
    leg (bool), index (frame index of a leg), Q (cofactor polynomial in
    u or None), n, e (effective exponent)."""
    if n == 1:
        # THE DEEP LEVEL (entry 89): the frame X = pi^2 is itself a square, pi = a + bi
        # with a^2 + b^2 = P prime, gcd(a, b) = 1, opposite parity.  So
        #   Re(X) = C1 = (a - b)(a + b)   coprime odd factors, each < sqrt(2P);
        #   Im(X) = S1 = 2ab              coprime factors a, b, each < sqrt(P).
        # An odd prime power dividing C1 or S1 divides ONE of these -- bounds in
        # P^{1/2}, the strongest windows the frames allow.
        half = sp.Rational(1, 2)
        if kind == "Re":
            return [{"name": "(C1: a-+b)", "bexp": half, "bconst": SQRT2, "parity": "odd", "res8": None, "leg": False, "index": 1, "Q": None, "n": 1, "e": e, "deep": True}]
        return [{"name": "(S1: a)", "bexp": half, "bconst": 1, "parity": "unknown", "res8": None, "leg": False, "index": 1, "Q": None, "n": 1, "e": e, "deep": True},
                {"name": "(S1: b)", "bexp": half, "bconst": 1, "parity": "unknown", "res8": None, "leg": False, "index": 1, "Q": None, "n": 1, "e": e, "deep": True}]
    if n % 2 == 0:
        h = n // 2
        if kind == "Re":
            return [{"name": f"(Re{n}: C{h}-+S{h})", "bexp": h, "bconst": SQRT2, "parity": "odd", "res8": None,
                     "leg": False, "index": h, "Q": None, "n": n, "e": e}]
        out = []
        for t in _targets("Re", h, e) + _targets("Im", h, e):
            t = dict(t)
            t["name"] = f"(Im{n}->{t['name']})"
            out.append(t)
        return out
    # odd n >= 3
    legs = [dict(t) for t in _targets(kind, 1, e)]
    for lg in legs:
        lg["name"] = f"({kind}{n}: leg {lg['name']})"
    Q = cheb_cofactor(kind, n)
    if kind == "Im" and n == 3:
        # entry 90: the index-3 Im-cofactor 4 X1^2 - P^2 = (2 X1 - P)(2 X1 + P) -- coprime odd
        # factors (gcd | 2P, both odd, P does not divide 2 X1), each of modulus < 3P
        cofs = [{"name": f"(Im3: 2X1{sg}P)", "bexp": 1, "bconst": 3, "parity": "odd", "res8": None,
                 "leg": False, "index": 1, "Q": None, "n": 3, "e": e, "lin3": sg} for sg in ("-", "+")]
    else:
        cofs = [{"name": f"({kind}{n}: cof {Q.as_expr()})", "bexp": n - 1, "bconst": n, "parity": "odd",
                 "res8": 1 if kind == "Re" else n % 8, "leg": False, "index": 1, "Q": Q, "n": n, "e": e}]
    out = legs + cofs
    # split cases when the lever prime may divide n: R^{e-k} may land on ANY of the
    # coprime pieces (every leg and every cofactor piece), with R on another
    for r in _big_primes(n):
        v = sp.multiplicity(r, n)
        for k in range(1, v + 1):
            if e - k >= 1:
                for base in legs + cofs:
                    s = dict(base)
                    s["name"] = f"{base['name']} [split: R={r} | n, R^{e - k}]"
                    s["e"] = e - k
                    out.append(s)
    return out


# -------------------------------------------------------------- levers
def _levers(pattern):
    """All levers of the pattern: list of dicts(prime, e, targets, where),
    or a string verdict, or None."""
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
        for prime, e in (("p", ep), ("q", eq)):
            if e == 0:
                continue
            pure = is_pure_w if prime == "p" else is_pure_l
            idx = 1 if prime == "p" else 0
            side = "w" if prime == "p" else "l"
            if e > 0:
                fac = [(m, k) for m, k in ((D, k1), (M, k2)) if pure(m)]
                if not fac:
                    return "DEAD-no-pure-factor"
                m, k = fac[0]
                kind, nn, ee = k, abs(m[idx]), 2 * e
                where = f"pair {(a, b)}: {prime}^{2*e} | {k}({side}^{abs(m[idx])})"
            else:
                if not pure(ec):
                    return "DEAD-no-pure-factor"
                kind, nn, ee = "Im", abs(ec[idx]), -2 * e
                where = f"pair {(a, b)}: third term absorbs {prime}^{-2*e} | Im({side}^{abs(ec[idx])})"
            tg = _targets(kind, nn, ee)
            if side == "w":
                for t in tg:
                    t["name"] = (t["name"].replace("C1", "U1").replace("S1", "V1")
                                 .replace("a-+b", "u-+v").replace(": a)", ": u)").replace(": b)", ": v)"))
            levers.append({"prime": prime, "e": ee, "targets": tg, "where": where,
                           "side": side, "kind": kind, "n": nn})
    return levers


# ----------------------------------------------------- inequalities
def _ineq(lv, tgt):
    """lever prime^e | target  ->  (alpha, kappa, beta): prime^alpha < kappa other^beta."""
    return (tgt.get("e", lv["e"]), tgt["bconst"], tgt["bexp"])


def _pincer(ip, iq):
    """p^al < ka q^be and q^ga < kb p^de: contradiction for p, q >= PMIN?"""
    al, ka, be = ip
    ga, kb, de = iq
    ex = sp.nsimplify(al * ga - be * de)
    if ex <= 0:
        return None
    if sp.Integer(PMIN) ** ex >= ka ** ga * kb ** be:
        return f"pincer: p^{al} < {ka} q^{be} and q^{ga} < {kb} p^{de} give p^{ex} < {sp.nsimplify(ka**ga * kb**be)}"
    return None


def _t_candidates(tgt, e_eff, ratio):
    """Nonzero integers t with |t| < ratio compatible with the target's
    parity and residue (R^e = 1 mod 8 for e even; R = 1 mod 4 always)."""
    out = []
    par, res8 = tgt["parity"], tgt.get("res8")
    tmax = int(sp.floor(ratio)) if ratio != sp.oo else None
    if tmax is None:
        return None
    for t in range(-tmax, tmax + 1):
        if t == 0 or abs(t) >= ratio:
            continue
        if par == "odd" and t % 2 == 0:
            continue
        if par == "even4" and t % 4 != 0:
            continue
        if res8 is not None:
            if e_eff % 2 == 0:
                if t % 8 != res8 % 8:
                    continue
            elif t % 4 != res8 % 4:
                continue
        out.append(t)
    return out


def _window(lv, tgt, other):
    """Window on lever lv's target using the other prime's inequality
    other = (alpha, kappa, beta): other^alpha < kappa * lv.prime^beta."""
    al, ka, be = other
    h, e_eff = tgt["bexp"], tgt.get("e", lv["e"])
    ratio_const = tgt["bconst"] * ka ** sp.Rational(h, al)
    ratio_exp = sp.Rational(be * h, al) - e_eff
    if ratio_exp > 0:
        return "OPEN", None
    ratio = ratio_const * sp.Integer(PMIN) ** ratio_exp          # |t| < ratio (R >= 5 worst case)
    cands = _t_candidates(tgt, e_eff, ratio)
    if not cands:
        if tgt["parity"] == "even4":
            return "DEAD", f"window on {tgt['name']}: |t| < {sp.nsimplify(ratio)} but the target is even (4 | t)"
        return "DEAD", f"window on {tgt['name']}: |t| < {sp.nsimplify(ratio)} with parity/residue leaves no t"
    if set(cands) <= {1, -1}:
        return "PIN", f"{tgt['name']} = +-{lv['prime']}^{e_eff} exactly (|t| < {sp.nsimplify(ratio)}, t in {cands})"
    return "OPEN", None


def _fermat(lv, tgt):
    if not tgt.get("leg"):
        return None
    h, e = tgt["index"], tgt.get("e", lv["e"])
    if h % 2 == 0 and e % 2 == 0:
        return f"Fermat: (other leg)^2 = P^{2*h} - {lv['prime']}^{2*e} = (P^{h//2})^4 - ({lv['prime']}^{e//2})^4, nontrivial"
    return None


# ------------------------------------------------- cofactor pairs
def _enclose(val, margin=sp.Rational(1, 10**20)):
    """Rational enclosure [lo, hi] of an exact real (conservative)."""
    if val.is_Rational:
        return sp.Rational(val), sp.Rational(val)
    v = sp.Rational(sp.N(val, 40))
    return v - margin, v + margin


def poly_range(Q):
    """Range of the polynomial Q on the OPEN interval (0, 1):
    (lo, lo_attained, hi, hi_attained) with rational enclosures.  An
    extremum at an endpoint u = 0 or 1 is not attained (strict bound); an
    interior critical value is attained."""
    u = Q.gens[0]
    cands = [(sp.Rational(Q.eval(0)), False), (sp.Rational(Q.eval(1)), False)]
    if Q.degree() >= 2:
        for r in sp.Poly(Q.diff(u), u).real_roots():
            if 0 < r < 1:
                cands.append((Q.as_expr().subs(u, r), True))
    lo_v, lo_att = min(cands, key=lambda c: sp.N(c[0], 40))
    hi_v, hi_att = max(cands, key=lambda c: sp.N(c[0], 40))
    return _enclose(lo_v)[0], lo_att, _enclose(hi_v)[1], hi_att


class _Bound:
    """A positive real bound  value^(1/deg), closed or strict, compared
    exactly by cross powers."""
    def __init__(self, value, deg, strict):
        self.value, self.deg, self.strict = sp.Rational(value), deg, strict

    def feasible_below(self, other):
        """Is there a rho with self <= rho <= other (respecting strictness)?"""
        a, b = self.value ** other.deg, other.value ** self.deg
        if a < b:
            return True
        if a == b:
            return not (self.strict or other.strict)
        return False


def _pair_solver(lv_p, tp, lv_q, tq):
    """Homogeneous cofactor pair.  Returns (message, None) on a kill,
    (None, feasible list) when some (t, t') survives, or None when the
    pair is not homogeneous."""
    np_, nq_ = tp["n"], tq["n"]
    ep, eq = tp.get("e", lv_p["e"]), tq.get("e", lv_q["e"])
    if np_ - 1 != ep or nq_ - 1 != eq:
        return None
    mp, mp_att, Mp, Mp_att = poly_range(tp["Q"])
    mq, mq_att, Mq, Mq_att = poly_range(tq["Q"])
    Np = int(np_ * nq_ ** (-(-ep // eq)))          # |t| < n_p / rho^ep, |t'| < n_q rho^eq
    Nq = int(nq_ * np_ ** (-(-eq // ep)))
    feasible = []
    for t in _t_candidates(tp, ep, Np + 1) or []:
        for t2 in _t_candidates(tq, eq, Nq + 1) or []:
            if abs(t) ** eq * abs(t2) ** ep >= np_ ** eq * nq_ ** ep:
                continue
            # rho^ep = Q_p(u)/t in (mp, Mp)/t  (attainment carried; positive part)
            if t > 0:
                a, a_att, b, b_att = mp / t, mp_att, Mp / t, Mp_att
            else:
                a, a_att, b, b_att = Mp / t, Mp_att, mp / t, mp_att
            if b < 0 or (b == 0 and not b_att):
                continue
            lo1 = _Bound(a, ep, not a_att) if a > 0 else None
            hi1 = _Bound(b, ep, not b_att) if b > 0 else None       # b == 0 attained: rho = 0 impossible anyway
            if b == 0:
                continue
            # rho^{-eq} = Q_q(u')/t' in (mq, Mq)/t'  ->  rho^eq in (t'/Mq, t'/mq)
            if t2 > 0:
                c, c_att, d, d_att = mq / t2, mq_att, Mq / t2, Mq_att
            else:
                c, c_att, d, d_att = Mq / t2, Mq_att, mq / t2, mq_att
            if d < 0 or (d == 0 and not d_att) or d == 0:
                continue
            hi2 = _Bound(1 / c, eq, not c_att) if c > 0 else None   # rho^eq <= 1/c
            lo2 = _Bound(1 / d, eq, not d_att)                       # rho^eq >= 1/d
            lo = [x for x in (lo1, lo2) if x is not None]
            hi = [x for x in (hi1, hi2) if x is not None]
            # rho = 1 (p = q) is excluded: a single feasible point at rho = 1 is not feasible
            ok = all(L.feasible_below(H) for L in lo for H in hi)
            if ok:
                one = _Bound(1, 1, False)
                only_one = all(L.value ** 1 == 1 ** L.deg and not L.strict for L in lo) and                            all(H.value ** 1 == 1 ** H.deg and not H.strict for H in hi) and lo and hi
                if only_one:
                    continue
                feasible.append((t, t2))
    if feasible:
        return None, feasible
    tag = f"index-{np_} cofactor pair" if np_ == nq_ else f"index-{np_}x{nq_} cofactor pair"
    return (f"{tag}: {tp['Q'].as_expr()}(u) q^{np_-1} = t p^{ep} and {tq['Q'].as_expr()}(u') p^{nq_-1} = t' q^{eq} "
            f"with the parity/residue filters, |t|^{eq} |t'|^{ep} < {np_}^{eq} {nq_}^{ep}, and the exact ranges of the "
            f"cofactor polynomials on (0,1) admit no (t, t', p/q)"), None


def _cof_pair(lv_p, tp, lv_q, tq):
    """Compatibility wrapper (index 3): tp/tq may be {'cof': a} with
    a in {1, 3} meaning the cofactor 4 X1^2 - a P^2 (the coarse index-3
    cofactor targets of entry 87, kept for the pair-solver control)."""
    def norm(lv, t):
        if "Q" in t:
            return t
        a = t["cof"]
        kind = "Re" if a == 3 else "Im"
        Q = cheb_cofactor(kind, 3)
        return {"name": f"({kind}3: cof {Q.as_expr()})", "bexp": 2, "bconst": 3, "parity": "odd",
                "res8": 1 if kind == "Re" else 3, "leg": False, "index": 1, "Q": Q, "n": 3, "e": lv["e"]}
    return _pair_solver(lv_p, norm(lv_p, tp), lv_q, norm(lv_q, tq))


# ------------------------------------------- bounded primes (entry 90)
def _split_primes_below(bound):
    out = []
    p = 5
    while p < bound:
        if sp.isprime(p):
            out.append(p)
        p += 4
    return out


def _relation_nonzero_on_frames(pattern, fl, fw):
    """The cleared relation evaluated exactly on explicit frames (all sign
    choices of the imaginary legs): True iff it never vanishes."""
    terms = cleared_terms(pattern)
    cP, sP = fl
    cR, sR = fw
    for s1 in (1, -1):
        for s2 in (1, -1):
            tot = 0
            for cc, wp, wq, ec, poly in terms:
                for (a1, b1, c_, d_), v in poly.items():
                    tot += v * cP ** a1 * (s1 * sP) ** b1 * cR ** c_ * (s2 * sR) ** d_
            if tot == 0:
                return False
    return True


def _bounded_prime_kill(pattern, levers, chosen, ineqs):
    """When the two levers' inequalities bound one prime, p^ex < K (ex > 0)
    or the mirror for q, that prime ranges over the explicit finite set of
    split primes below K^{1/ex}; for each, its frame is explicit, every
    lever of the OTHER prime divides an explicit integer value of that
    frame (so the other prime ranges over an explicit finite set), and the
    relation is evaluated exactly on the finitely many frame pairs."""
    cands = {"p": None, "q": None}
    for ip in ineqs["p"]:
        for iq in ineqs["q"]:
            al, ka, be = ip
            ga, kb, de = iq
            ex = sp.nsimplify(al * ga - be * de)
            if ex <= 0:
                continue
            Kp = ka ** ga * kb ** be
            Kq = kb ** al * ka ** de
            bp = sp.N(Kp ** (1 / ex), 30)
            bq = sp.N(Kq ** (1 / ex), 30)
            for key, b in (("p", bp), ("q", bq)):
                if b < 10 ** 6:
                    val = int(sp.ceiling(b)) + 1
                    cands[key] = val if cands[key] is None else min(cands[key], val)
    for key in ("p", "q"):
        if cands[key] is None:
            continue
        primes = _split_primes_below(cands[key])
        others = [lv for lv in levers if lv["prime"] != key]
        if not others:
            continue
        dead_all = True
        detail = []
        for P0 in primes:
            fr = _frame_of(P0)
            if fr is None:
                dead_all = False
                break
            c0, s0 = fr
            # the other prime's levers divide explicit values of THIS prime's frame
            oth_cands = None
            for lv in others:
                val = _gauss_trig(lv["kind"], c0, s0, lv["n"])
                if val == 0:
                    dead_all = False
                    break
                ps = {int(r) for r, m in sp.factorint(abs(val)).items() if r % 4 == 1 and r >= PMIN and r != P0 and m >= lv["e"]}
                oth_cands = ps if oth_cands is None else (oth_cands & ps)
            if not dead_all:
                break
            if oth_cands:
                for Q0 in sorted(oth_cands):
                    fr2 = _frame_of(Q0)
                    if fr2 is None:
                        dead_all = False
                        break
                    fl, fw = ((c0, s0), fr2) if key == "p" else (fr2, (c0, s0))
                    if not _relation_nonzero_on_frames(pattern, fl, fw):
                        dead_all = False
                        break
                if not dead_all:
                    break
            detail.append((P0, sorted(oth_cands) if oth_cands else []))
        if dead_all:
            return (f"bounded prime: the pincer leaves {key} < {cands[key]}; for each such split prime the other "
                    f"lever's value on its explicit frame admits only the partner primes {detail[:4]}"
                    f"{' ...' if len(detail) > 4 else ''}, and the relation is nonzero on every explicit frame pair")
    return None


# ------------------------------------------- pin and substitute
def _pin_substitute(lv_leg, tleg, lv_cof, tcof):
    """A pinned index-1 leg on one frame and a cofactor lever on the other.
    The lv_leg prime (say p) pins the w-leg L1 = +-p^e (window already
    established: t = +-1), so the other w-leg satisfies V1^2 = q^2 - p^{2e}
    > 0, i.e. q^2 = p^{2e} + V1^2.  The q-lever with exponent 2 divides the
    l-frame cofactor: cof_n(C1^2, p^2) = t' q^2 with |t'| < n p^{n-1}/q^2 <
    n p^{n-1-2e} (q^2 > p^{2e}); when n - 1 = 2e this is the constant n, and
    t' is odd with its residue.  Substituting,
          p^{n-1} (Q(u) - t') = t' V1^2,      u = C1^2/p^2 in (0,1).
    Kills: (sign) Q(u) - t' of sign opposite to t' on (0,1) contradicts
    V1^2 > 0;  (two squares) when Q(u) - t' = (u - 1) H(u):
    -S1^2 p^{n-3} H(u) = t' V1^2, so W = -p^{n-3} H(u)/t' is a perfect
    square; W = k^2 (p^2 - a^2 C1^2) with a >= 2 gives p^2 = (a C1)^2 + m^2,
    and the only representations of p^2 as two squares are (p,0) and
    (C1,S1) up to order and sign, forcing p^2 = (1 + a^2) C1^2 -- impossible
    (C1^2 would be 1 or p).  Returns a kill message or None."""
    e = tleg.get("e", lv_leg["e"])
    eq = tcof.get("e", lv_cof["e"])
    if eq != 2 or tcof.get("Q") is None:
        return None
    n = tcof["n"]
    if n - 1 != 2 * e:
        return None
    Q = tcof["Q"]
    u = Q.gens[0]
    kills = []
    cands = _t_candidates(tcof, eq, sp.Integer(n)) or []
    if not cands:
        return f"pin+substitute on {tleg['name']} = +-{lv_leg['prime']}^{e}: |t'| < {n} with the residue leaves no t' for {tcof['name']}"
    for t2 in cands:
        G = sp.Poly(Q.as_expr() - t2, u)
        lo, lo_att, hi, hi_att = poly_range(G)
        if (t2 > 0 and (hi < 0 or (hi == 0 and not hi_att))) or (t2 < 0 and (lo > 0 or (lo == 0 and not lo_att))):
            kills.append(f"t'={t2}: sign (p^{n-1}(Q(u) - t') and t' V1^2 have opposite signs on (0,1))")
            continue
        if G.eval(1) != 0:
            return None
        H = sp.Poly(sp.quo(G.as_expr(), u - 1), u)
        c, P2 = sp.symbols("c P2")
        half = (n - 3) // 2
        W = sp.expand(-sp.Rational(1, t2) * sum(coef * c ** k * P2 ** (half - k) for (k,), coef in H.terms()))
        Wp = sp.Poly(W, c, P2)
        if Wp.total_degree() == 1:
            A = Wp.coeff_monomial(P2)
            B = Wp.coeff_monomial(c)
            if A > 0 and B < 0 and sp.sqrt(A).is_integer and sp.sqrt(-B / A).is_integer and sp.sqrt(-B / A) >= 2:
                a = int(sp.sqrt(-B / A))
                kills.append(f"t'={t2}: (V1/S1)^2 = {A}(p^2 - {a}^2 C1^2) forces p^2 = ({a} C1)^2 + m^2, against the unique "
                             f"two-squares representation of p^2 (only (p,0) and (C1,S1))")
                continue
        return None
    return f"pin+substitute on {tleg['name']} = +-{lv_leg['prime']}^{e} into {tcof['name']}: " + "; ".join(kills)


# ------------------------------------------- explicit frames (split cases)
_FRAMES = {5: (3, 4)}      # X = rho^2 for the split prime R: (Re, Im) up to sign; 5 = 2^2 + 1^2 -> (2+i)^2 = 3+4i


def _gauss_trig(kind, c, s, n):
    """Trig_kind((c + i s)^n) as an integer."""
    z = sp.Integer(1)
    for _ in range(n):
        z = sp.expand(z * (c + sp.I * s))
    return int(sp.re(z)) if kind == "Re" else int(sp.im(z))


def _frame_of(prime):
    """The frame (c, s) = (a^2 - b^2, 2ab) of a split prime p = a^2 + b^2, a > b > 0."""
    for a in range(1, int(sp.sqrt(prime)) + 1):
        b2 = prime - a * a
        b = int(sp.sqrt(b2))
        if b * b == b2 and a > b > 0:
            return a * a - b * b, 2 * a * b
    return None


def _explicit_split_kill(pattern, levers, chosen):
    """A chosen split target belongs to a lever whose prime R divides the
    index n of the value it lands on; R is then the explicit prime named in
    the target (5 for n = 5, 10, ...), whose frame is explicit (3, 4).  Every
    OTHER lever (prime P) divides an explicit integer value of that frame,
    so P ranges over an explicit finite set; for each such P the relation is
    a polynomial identity in the two explicit frames, evaluated exactly (all
    sign choices).  Returns a kill message or None."""
    splits = [(lv, tgt) for lv, tgt in chosen if "[split: R=" in tgt["name"]]
    if not splits:
        return None
    lv_s, tgt_s = splits[0]
    R = int(tgt_s["name"].split("[split: R=")[1].split(" ")[0])
    if R not in _FRAMES:
        return None
    cR, sR = _FRAMES[R]
    others = [lv for lv in levers if lv["prime"] != lv_s["prime"]]
    if not others:
        return None
    # the other lever's value on the explicit frame of R (its side is R's frame)
    cand_primes = None
    for lv in others:
        val = _gauss_trig(lv["kind"], cR, sR, lv["n"])
        if val == 0:
            return None
        ps = {int(r) for r, m in sp.factorint(abs(val)).items() if r % 4 == 1 and r >= PMIN and r != R and m >= lv["e"]}
        cand_primes = ps if cand_primes is None else (cand_primes & ps)
    if cand_primes is None:
        return None
    if not cand_primes:
        return (f"explicit frame: the split target puts the lever prime at {R} (frame ({cR},{sR})); the other lever's "
                f"value {[ _gauss_trig(lv['kind'], cR, sR, lv['n']) for lv in others ]} has no admissible prime-power divisor")
    # evaluate the relation on explicit frames for every candidate P
    terms = cleared_terms(pattern)
    for P in sorted(cand_primes):
        fr = _frame_of(P)
        if fr is None:
            return None
        cP, sP = fr
        for s1 in (1, -1):
            for s2 in (1, -1):
                for s3 in (1, -1):
                    if lv_s["prime"] == "q":      # R = q: w-frame is (cR, sR); l-frame is P's
                        c1, sig1, c2, sig2 = cP * s1, sP * s2, cR, sR * s3
                    else:
                        c1, sig1, c2, sig2 = cR, sR * s3, cP * s1, sP * s2
                    tot = 0
                    for cc, wp, wq, ec, poly in terms:
                        for (a1, b1, c_, d_), v in poly.items():
                            tot += v * c1 ** a1 * sig1 ** b1 * c2 ** c_ * sig2 ** d_
                    if tot == 0:
                        return None
    return (f"explicit frame: lever prime {R} (frame ({cR},{sR})), candidate partner primes {sorted(cand_primes)}; "
            f"the cleared relation is nonzero on every explicit frame pair")


# ------------------------------------------------------------ the kill
def window_kill(pattern):
    """Returns a certificate dict with 'kills': True, or a dict with the
    surviving case tuples, or None (no levers)."""
    levers = _levers(pattern)
    if levers is None:
        return None
    if isinstance(levers, str):
        return {"kills": True, "how": levers}
    if not levers:
        return None
    cases_out = []
    all_dead = True
    for tup in itertools.product(*[range(len(lv["targets"])) for lv in levers]):
        chosen = [(lv, lv["targets"][t]) for lv, t in zip(levers, tup)]
        ineqs = {"p": [], "q": []}
        for lv, tgt in chosen:
            ineqs[lv["prime"]].append(_ineq(lv, tgt))
        why = None
        for ip in ineqs["p"]:
            for iq in ineqs["q"]:
                why = _pincer(ip, iq)
                if why:
                    break
            if why:
                break
        if why is None:
            cof = [(lv, tgt) for lv, tgt in chosen if tgt.get("Q") is not None]
            pc = [x for x in cof if x[0]["prime"] == "p"]
            qc = [x for x in cof if x[0]["prime"] == "q"]
            for (lp, tp) in pc:
                for (lq, tq) in qc:
                    res = _pair_solver(lp, tp, lq, tq)
                    if res is not None and res[0] is not None:
                        why = res[0]
                        break
                if why:
                    break
        pins = []
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
                        pins.append((lv, tgt, msg))
                if why:
                    break
        if why is None and pins:
            for lv, tgt, msg in pins:
                if tgt.get("leg") and tgt.get("index") == 1:
                    for lv2, tgt2 in chosen:
                        if lv2["prime"] != lv["prime"] and tgt2.get("Q") is not None:
                            r = _pin_substitute(lv, tgt, lv2, tgt2)
                            if r:
                                why = f"{msg}; {r}"
                                break
                if why:
                    break
        if why is None:
            try:
                why = _explicit_split_kill(pattern, levers, chosen)
            except Exception:
                why = None
        if why is None:
            try:
                why = _bounded_prime_kill(pattern, levers, chosen, ineqs)
            except Exception:
                why = None
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
