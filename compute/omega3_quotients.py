"""QUOTIENTS OF THE CERTIFIED CURVES BY THEIR INVOLUTIONS (entry 105; ROADMAP R.9 attempt B).

Every certified component Phi(t_g, t_h) = 0 of the (1,1,1) box is invariant under
the joint sign change (t_g, t_h) -> (-t_g, -t_h) (the conjugation of every frame), and
944 of the 1264 carry a further involution acting on one coordinate:
    t -> -t      (u = t^2),        t -> 1/t     (u = t + 1/t),
    t -> -1/t    (u = t - 1/t; the frame rotated by a right angle),
and 46 the swap.  The quotient by an involution acting on one coordinate is the
image curve Q(u, t_other) = 0, computed as the squarefree kernel of the resultant
Res_t(Phi, m(t) - u ...) against the invariant's minimal relation (t^2 - u,
t^2 - u t + 1, t^2 - u t - 1), keeping the factor that vanishes on the curve; the
quotient by the joint sign change uses the invariants x = t_g^2, y = t_g t_h.  The
exact genus of the quotient is computed by the resolution tool.

A KILL: a genus-1 quotient that is quadratic in one variable has the hyperelliptic
model y^2 = disc(u); PARI (ellrank + complete enumeration, entry 97's quartic_points)
gives every rational u; each lifts to finitely many rational t_other (the quadratic's
rational roots) and finitely many rational t (the invariant's rational preimages);
if no lift is a pair of non-degenerate Pythagorean frame ratios, the component --
and the class certified through it -- is DEAD.  The square-part roots of the
discriminant are added as extra u-values (a double rational root there, entry 97).
Genus-0 quotients give nothing (infinitely many points); genus >= 2 quotients are
recorded (Chabauty territory).
"""
from __future__ import annotations
import sympy as sp

from compute.omega3 import tg, th, is_frame_ratio, degenerate, _disc_model, square_part_roots, gp_model

U = sp.Symbol("u_q")


def _image_factor(Res, phi, u_expr, var, other):
    """The irreducible factors of Res (in U and `other`) that vanish on the curve:
    Q(u_expr(var), other) is divisible by phi after clearing denominators."""
    out = []
    for fac, m in sp.factor_list(sp.expand(Res))[1]:
        fe = sp.expand(fac)
        if not (fe.free_symbols & {U, other}) or U not in fe.free_symbols:
            continue
        test = sp.numer(sp.together(fe.subs(U, u_expr)))
        q, r = sp.div(sp.Poly(sp.expand(test), var, other), sp.Poly(phi, var, other))
        if r.is_zero:
            out.append(fe)
    return out


def coordinate_quotient(phi, which, kind):
    """The quotient of Phi(tg, th) by the involution `kind` on coordinate `which`:
    returns (Q(U, other), other symbol, u_expr, invariant relation) or None."""
    var, other = (tg, th) if which == "g" else (th, tg)
    if kind == "neg":
        rel, u_expr = var ** 2 - U, var ** 2
    elif kind == "rec":
        rel, u_expr = var ** 2 - U * var + 1, var + 1 / var
    elif kind == "negrec":
        rel, u_expr = var ** 2 - U * var - 1, var - 1 / var
    else:
        raise ValueError(kind)
    Res = sp.resultant(sp.Poly(phi, var), sp.Poly(rel, var))
    facs = _image_factor(Res, phi, u_expr, var, other)
    if len(facs) != 1:
        return None
    return facs[0], other, u_expr, rel


def joint_quotient(phi, dh):
    """The quotient by (tg, th) -> (-tg, -th): invariants x = tg^2, y = tg th;
    returns Q(X = U, Y = th-slot) with th standing for y, or None."""
    Y = th
    # Phi(tg, y/tg) * tg^dh is a polynomial in tg and y; eliminate tg against tg^2 - U
    P = sp.expand(sp.numer(sp.together(phi.subs(th, Y / tg))))
    Res = sp.resultant(sp.Poly(P, tg), sp.Poly(tg ** 2 - U, tg))
    out = []
    for fac, m in sp.factor_list(sp.expand(Res))[1]:
        fe = sp.expand(fac)
        if U not in fe.free_symbols or Y not in fe.free_symbols:
            continue
        test = sp.expand(fe.subs({U: tg ** 2, Y: tg * th}, simultaneous=True))
        q, r = sp.div(sp.Poly(test, tg, th), sp.Poly(phi, tg, th))
        if r.is_zero:
            out.append(fe)
    if len(out) != 1:
        return None
    return out[0]


def quotient_genus(Q, other):
    """Exact genus of the plane curve Q(U, other) = 0 (resolution tool, in the
    (tg, th) slots)."""
    from compute.omega3_resolve import exact_genus_checked
    Qs = sp.expand(Q.subs({U: tg, other: th}, simultaneous=True)) if other != th else sp.expand(Q.subs(U, tg))
    P = sp.Poly(Qs, tg, th)
    g, det = exact_genus_checked(Qs, P.degree(tg), P.degree(th), degmax=60, timeout=300)
    return g, det.get("consistent"), Qs, (P.degree(tg), P.degree(th))


def _rational_roots(poly, var):
    if poly == 0 or not poly.free_symbols:
        return []
    return [r for r in sp.Poly(poly, var).ground_roots() if r.is_rational]


def try_kill(Q, other, u_expr, var, rel):
    """A genus-1 quotient quadratic in `other` (or in U): the rank-0 route with a
    complete lift.  Returns (verdict, info): 'dead' when every rational point of the
    quotient lifts only to inadmissible frame pairs."""
    for qvar, ovar in ((other, U), (U, other)):
        P = sp.Poly(Q, qvar)
        if P.degree() != 2:
            continue
        dm = _disc_model(Q, qvar, ovar)
        if dm is None:
            continue
        sqf, dfl, genus = dm
        if genus != 1:
            return "unknown", {"quadratic_in": str(qvar), "model_genus": genus}
        key, r = gp_model(sqf, ovar)
        info = {"quadratic_in": str(qvar), "model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
        if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
            info["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
            return "unknown", info
        vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, ovar)
        admissible = []
        for v0 in vals:
            # the other coordinate of the quotient point
            for w0 in _rational_roots(sp.expand(Q.subs(ovar, v0)), qvar):
                u0, o0 = (v0, w0) if ovar == U else (w0, v0)
                # lift u0 to the original coordinate through the invariant relation
                for t0 in _rational_roots(sp.expand(rel.subs(U, u0)), var):
                    if not degenerate(t0) and not degenerate(o0) and is_frame_ratio(t0) and is_frame_ratio(o0):
                        admissible.append((str(t0), str(o0)))
        info["points_u"] = [str(v) for v in vals]
        info["admissible"] = admissible
        return ("candidate" if admissible else "dead"), info
    return "unknown", {"note": "not quadratic in either variable"}


def analyse(phi, dg, dh, sym):
    """All quotients of one certified component: genera, and kills where possible."""
    out = []
    plans = []
    for which in ("g", "h"):
        for kind in ("neg", "rec", "negrec"):
            flag = {"neg": "neg_", "rec": "rec_", "negrec": "negrec_"}[kind] + which
            if sym.get(flag):
                plans.append((which, kind))
    for which, kind in plans:
        rec = {"by": kind + "_" + which}
        try:
            cq = coordinate_quotient(phi, which, kind)
            if cq is None:
                rec["error"] = "no unique image factor"
                out.append(rec)
                continue
            Q, other, u_expr, rel = cq
            g, cons, Qs, deg = quotient_genus(Q, other)
            rec.update(genus=g, consistent=cons, deg=deg)
            if g is not None and g <= 1 and g == 1:
                var = tg if which == "g" else th
                v, info = try_kill(Q, other, u_expr, var, rel)
                rec.update(verdict=v, kill=info)
        except Exception as e:                       # pragma: no cover
            rec["error"] = repr(e)[:160]
        out.append(rec)
    rec = {"by": "joint_sign"}
    try:
        Q = joint_quotient(phi, dh)
        if Q is None:
            rec["error"] = "no unique image factor"
        else:
            g, cons, Qs, deg = quotient_genus(Q, th)
            rec.update(genus=g, consistent=cons, deg=deg)
    except Exception as e:                           # pragma: no cover
        rec["error"] = repr(e)[:160]
    out.append(rec)
    return out
