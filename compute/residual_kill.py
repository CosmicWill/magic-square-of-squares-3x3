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
                                     _parity_poly, _P, _Q, _L, _LB)


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
            out.append((side, k, A, B, d))
    return out


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
    'DEAD-residual-concentration', 'OPEN' (with the surviving branches),
    'NO-LINEAR-FORM', or 'DEAD-no-pure-factor'."""
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
