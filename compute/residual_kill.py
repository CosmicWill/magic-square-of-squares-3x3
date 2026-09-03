"""The RESIDUAL finisher (entry 88, build B, v1): single-lever patterns
whose collapse equation is LINEAR in the legs of one w-index.

Mechanism (the H2 tree of the (3,1) campaign, made mechanical).  A
collapse equation of an OPEN pattern, in Lucas symbols, that involves the
w-frame only through U_k, V_k (one index k) and is homogeneous of degree
one in them reads
        A * U_k + B * V_k = 0,        A, B in Z[C_x, S_x, ...][p].
The legs U_k = Re(w^k), V_k = Im(w^k) are coprime and not both zero, so
        (U_k, V_k) = +-(B, -A) / g,   g = gcd(A, B)     (the RIGID FORM),
and therefore
        w^k = U_k + i V_k = +-(B - iA) / g,
a coincidence of the pinned-system type: the frame value w^k equals an
explicit Gaussian polynomial in l, lbar divided by a bounded content.
Kills, all reused from the pinned-system layer (entries 83-84):
  * parity: U_k is odd and V_k = 0 mod 4 (Gaussian squares), so A/g = 0
    mod 4 -- an odd A is dead at once;
  * content: g | gcd(A, B) is bounded by the content lemma (cyclotomic
    resultants against Lucas symbols, angle-polynomial resultants against
    polynomial atoms, structural units against prime powers);
  * concentration: for every d | bound, sign and conjugation,
    concentration_kill certifies w^k = +-(B - iA)/d impossible (the
    residual against +-l^{2j} or +-lbar^{2j} is a small cofactor times a
    high power of the other prime), or sliver_kill does for d > 1.
Levers are not needed: the linear relation alone carries the lever's
information (a p-power in A or B lands in the rigid form).

v1 scope: exactly one w-index in the equation, degree one, no q-weight
in the coefficients.  Everything else is reported, not claimed.
"""
from __future__ import annotations

import sympy as sp

from compute.lucas_endpoints import (all_collapses, endpoint_identity, concentration_kill, sliver_kill,
                                     lucas_to_L, content_bound, content_bound_poly, is_unit_at,
                                     _parity_poly, _abs_coeff_bound, _P, _Q, _L, _LB)
from compute.window_kill import _targets, PMIN


def _size_kill(side, k, A, B, Z, N):
    """The rigid-form SIZE kill (entry 89): frame^k = +-(B - iA)/g gives
    q^k = |B - iA|/g <= M(p)/g with M the coefficient bound of the Gaussian
    polynomial Z, and the Im-leg Y_k = -+A/g carries the p-power of A:
    p^{2m} | Y_k where m is the (L LB)-content of A (g is prime to p).  An
    odd prime power dividing Y_k = Im(rho^{2k}) divides one coprime factor
    of it, the deepest being the legs u, v, u -+ v of rho itself (u^2 + v^2
    = q), each < sqrt(2q): the window finisher's targets of Im(X^k) with the
    deep index-1 level.  Every target gives  p^{2m} < c q^h;  with
    q <= (M/g)^{1/k} this reads  p^{2mk/h} < c^{k/h} M(p)/g,  a polynomial
    inequality false for all p >= 5 (exact Sturm count) -- a kill when it
    fails for EVERY target and every content d | N.  (The roles of p and q
    swap for the mirror; the bound uses the same letters.)"""
    m = None
    ZA = sp.expand(lucas_to_L(A, "l" if side == "w" else "w"))
    if ZA == 0:
        return None
    PA = sp.Poly(ZA, _L, _LB)
    m = min(min(mon) for mon in PA.monoms())
    if m < 1:
        return None
    M = _abs_coeff_bound(sp.expand(Z))            # |Z| <= M(p) as a polynomial in the coefficient prime
    if M == 0:
        return None
    msgs = []
    for d in [x for x in range(1, N + 1) if N % x == 0]:
        for tgt in _targets("Im", k, 2 * m):
            h, c = sp.nsimplify(tgt["bexp"]), tgt["bconst"]
            ee = tgt.get("e", 2 * m)
            # p^{ee} < c q^h  and  q^k <= M/d   =>   p^{ee k / h} < c^{k/h} M / d
            lhs_exp = sp.nsimplify(ee * k / h)
            rhs = sp.nsimplify(c ** (k / h)) * M / d
            if not lhs_exp.is_integer:
                return None
            cnd = sp.expand(_P ** int(lhs_exp) - rhs)          # must be > 0 for all p >= PMIN
            poly = sp.Poly(cnd, _P)
            if poly.LC() <= 0 or cnd.subs(_P, PMIN) <= 0 or poly.count_roots(inf=PMIN) != 0:
                return None
            msgs.append(f"d={d}: {tgt['name']} gives p^{ee} < {c} q^{h} against q^{k} <= {sp.factor(M)}/{d}")
    return ("rigid-form size: the Im-leg carries p^%d (the (L LB)-content of A); its deep coprime "
            "targets are all below sqrt(2q)-scale, while |frame^k| = |B - iA|/g bounds q above; " % (2 * m)
            + "; ".join(msgs[:4]) + (" ..." if len(msgs) > 4 else ""))


def linear_forms(pattern):
    """(side, k, A, B, detail) for every collapse equation that is linear
    homogeneous in the legs of a single index k of ONE side: the w-legs
    (U_k, V_k) with A, B in l-symbols and p (side 'w'), or the mirror,
    the l-legs (C_k, S_k) with A, B in w-symbols and q (side 'l')."""
    out = []
    for d in all_collapses(pattern):
        if d["dead"]:
            return "DEAD-no-pure-factor"
        expr, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if not ok:
            continue
        for side, letters, other_prime in (("w", "UV", _Q), ("l", "CS", _P)):
            syms = [s for s in expr.free_symbols if str(s)[0] in letters]
            ks = {int(str(s)[1:]) for s in syms}
            if len(ks) != 1:
                continue
            k = ks.pop()
            X, Y = sp.Symbol(f"{letters[0]}{k}"), sp.Symbol(f"{letters[1]}{k}")
            P = sp.Poly(expr, X, Y)
            if P.total_degree() != 1 or P.coeff_monomial(1) != 0:
                continue
            A, B = sp.expand(P.coeff_monomial(X)), sp.expand(P.coeff_monomial(Y))
            if A == 0 or B == 0:
                continue
            if other_prime in A.free_symbols or other_prime in B.free_symbols:
                continue
            # entry 90: cancel the POLYNOMIAL gcd of A and B -- a common factor F(C1, S1)
            # that never vanishes on a frame is not content, it is a factor of the
            # relation (A U + B V = F (A' U + B' V) = 0 with F != 0)
            A, B, F = _cancel_polynomial_gcd(A, B, side)
            if A is None:
                continue
            out.append((side, k, A, B, d))
    return out


def _frame_zero_of(G, cs):
    """Does the homogeneous polynomial G(C, S) vanish on some frame?  A zero
    needs C/S = x rational with C odd, S even and C^2 + S^2 a prime square
    (C, S the legs of pi^2, p = a^2 + b^2): from the rational roots x = m/n of
    G(x, 1), (C, S) = +-(m, n) up to a scalar t, p^2 = t^2 (m^2 + n^2), so
    m^2 + n^2 must be a perfect square s^2 and p = t s prime forces t = 1,
    p = s.  Returns the list of such primes (usually empty)."""
    C, S = cs
    x = sp.Symbol("x")
    g = sp.Poly(sp.expand(G.subs({C: x * S})).subs(S, 1), x) if S in G.free_symbols else None
    if g is None:
        # G depends on C only: G(C) = 0 has finitely many C; each fixes C, and S ranges over
        # frames with that C -- infinitely many in principle; refuse to cancel
        return None
    found = []
    for r in sp.roots(g, filter="Q"):
        r = sp.Rational(r)
        m, n = int(r.p), int(r.q)
        if m % 2 == 0 or n % 2 == 1:
            continue
        s2 = m * m + n * n
        sq = sp.integer_nthroot(s2, 2)
        if sq[1] and sp.isprime(int(sq[0])) and int(sq[0]) % 4 == 1:
            found.append(int(sq[0]))
    if g.degree() == 0 and g.LC() == 0:
        return None
    return found


def _cancel_polynomial_gcd(A, B, side):
    """Divide A and B by their polynomial gcd F when F is a product of factors
    that never vanish on a frame.  Returns (A', B', F) or (None, None, F)
    when a factor may vanish (conservative)."""
    F = sp.gcd(A, B)
    if F.is_number:
        return A, B, F
    letters = ("C", "S") if side == "w" else ("U", "V")
    syms = [sy for sy in F.free_symbols if str(sy)[0] in letters]
    ks = {int(str(sy)[1:]) for sy in syms}
    if len(ks) != 1:
        return None, None, F
    k = ks.pop()
    C, S = sp.Symbol(f"{letters[0]}{k}"), sp.Symbol(f"{letters[1]}{k}")
    for fac, mult in sp.factor_list(F)[1]:
        if fac.is_number:
            continue
        if fac.free_symbols - {C, S}:
            return None, None, F          # a prime symbol or other index inside the gcd: refuse
        z = _frame_zero_of(fac, (C, S))
        if z is None or z:
            return None, None, F
    return sp.expand(sp.cancel(A / F)), sp.expand(sp.cancel(B / F)), F


def _gcd_bound(A, B, prime=_P):
    """A bound on gcd(A, B) over odd primes r != the frame prime (2-powers
    are handled by the parity of the rigid form), from the factors of B:
    prime powers (A a structural unit), Lucas symbols (content lemma),
    polynomial atoms (angle-polynomial resultant).  None when some factor
    is unbounded."""
    fB = sp.factor(B)
    N = 1
    for f in sp.Mul.make_args(fB):
        base, mult = (f.base, int(f.exp)) if f.is_Pow else (f, 1)
        if base.is_number:
            continue
        if base == prime:
            if not is_unit_at(A, prime):
                return None
            continue
        if base.is_Symbol:
            cb = content_bound(A, base)
        else:
            try:
                cb = content_bound_poly(A, base)
            except Exception:
                cb = None
        if cb is None:
            return None
        N *= int(cb) ** mult
    return N


def _residual_branches(P_expr, d, jmax=6, amax=14):
    """All sign / conjugation branches of w^k = +-P/d: certificates or None."""
    certs = []
    ok_all = True
    for sg in (1, -1):
        for cj in (False, True):
            PP = sg * P_expr
            if cj:
                PP = PP.subs({_L: _LB, _LB: _L}, simultaneous=True)
            PP = sp.expand(PP)
            c = None
            if d == 1:
                c = concentration_kill(PP, jmax=jmax, amax=amax)
            if c is None:
                e = sliver_kill(PP, d)
                c = {"sliver": e, "d": d} if e else None
            certs.append((sg, cj, c))
            if c is None:
                ok_all = False
    return ok_all, certs


def residual_kill(pattern):
    """Returns (verdict, details).  Verdicts: 'DEAD-residual-parity',
    'DEAD-residual-size', 'DEAD-residual-concentration', 'OPEN' (with the
    surviving branches), 'NO-LINEAR-FORM', or 'DEAD-no-pure-factor'."""
    forms = linear_forms(pattern)
    if isinstance(forms, str):
        return forms, None
    if not forms:
        return "NO-LINEAR-FORM", None
    report = []
    for side, k, A, B, d in forms:
        prime = _P if side == "w" else _Q          # the prime of the coefficient frame
        coef_side = "l" if side == "w" else "w"
        # parity: the Im-leg is 0 mod 4, so A/g = -+(Im leg) = 0 mod 4 with g | A; an odd A cannot be
        if _parity_poly(A) == "odd":
            return "DEAD-residual-parity", {"side": side, "k": k, "A": str(A), "B": str(B),
                                            "why": "A odd, but A/g = -+(Im leg) = 0 mod 4"}
        N = _gcd_bound(A, B, prime)
        if N is None:
            N = _gcd_bound(B, A, prime)
        if N is None:
            report.append({"side": side, "k": k, "A": str(A), "B": str(B), "status": "content unbounded"})
            continue
        Z = lucas_to_L(B - sp.I * A, coef_side)
        if not sp.expand(Z).is_polynomial(_L, _LB):
            report.append({"k": k, "status": "rigid form not polynomial"})
            continue
        try:
            sz = _size_kill(side, k, A, B, Z, N)
        except Exception:
            sz = None
        if sz:
            return "DEAD-residual-size", {"side": side, "k": k, "A": str(A), "B": str(B), "content_bound": N,
                                         "rigid": f"{side}^{k} = +-(B - iA)/g", "why": sz}
        dead = True
        branches = {}
        for dd in [x for x in range(1, N + 1) if N % x == 0]:
            ok, certs = _residual_branches(Z / dd, dd)
            branches[dd] = certs
            if not ok:
                dead = False
                break
        if dead:
            return "DEAD-residual-concentration", {"side": side, "k": k, "A": str(A), "B": str(B), "content_bound": N,
                                                  "rigid": f"{side}^{k} = +-(B - iA)/g", "branches": branches}
        report.append({"side": side, "k": k, "A": str(A), "B": str(B), "content_bound": N, "status": "some branch open",
                       "branches": branches})
    return "OPEN", report
