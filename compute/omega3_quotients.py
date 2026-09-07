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

from compute.omega3 import tg, th, is_frame_ratio, degenerate, _disc_model, square_part_roots, gp_model, squarefree_part

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


XS, ZS = sp.symbols("x_q z_q")


def joint_quotient_xz(phi):
    """The joint quotient in the model (x, z) = (t_g^2, t_h^2): eliminate t_h against
    t_h^2 - z (the resultant is even in t_g by the joint invariance), substitute
    x = t_g^2, and keep the factor vanishing on the curve.  Birational to the
    (t_g^2, t_g t_h) model when only the joint sign change preserves the curve
    (the map to the (x, z)-plane is then 2:1 on the curve); a further quotient
    when a single sign change does too -- either way a rational point of the
    curve maps to a rational point with x and z rational SQUARES."""
    R = sp.expand(sp.resultant(sp.Poly(phi, th), sp.Poly(th ** 2 - ZS, th)))
    P = sp.Poly(R, tg)
    if any(k % 2 for (k,), c in P.terms()):
        return None
    C = sp.expand(sum(c * XS ** (k // 2) for (k,), c in P.terms()))
    out = []
    for fac, m in sp.factor_list(C)[1]:
        fe = sp.expand(fac)
        if XS not in fe.free_symbols or ZS not in fe.free_symbols:
            continue
        test = sp.expand(fe.subs({XS: tg ** 2, ZS: th ** 2}, simultaneous=True))
        q, r = sp.div(sp.Poly(test, tg, th), sp.Poly(phi, tg, th))
        if r.is_zero:
            out.append(fe)
    return out[0] if len(out) == 1 else None


def try_kill_joint_xz(C, phi):
    """The (x, z)-model quadratic in a variable: the rank-0 route; a rational point
    (x0, z0) lifts only when x0 and z0 are rational squares, to (+-sqrt x0, +-sqrt z0)
    on the curve.  Returns (verdict, info)."""
    for qvar, ovar in ((ZS, XS), (XS, ZS)):
        if sp.Poly(C, qvar).degree() != 2:
            continue
        dm = _disc_model(C, qvar, ovar)
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
            for w0 in _rational_roots(sp.expand(C.subs(ovar, v0)), qvar):
                x0, z0 = (v0, w0) if ovar == XS else (w0, v0)
                if x0 <= 0 or z0 <= 0:
                    continue
                a = sp.sqrt(x0)
                b = sp.sqrt(z0)
                if not (a.is_rational and b.is_rational):
                    continue
                for sa in (a, -a):
                    for sb in (b, -b):
                        if sp.expand(phi.subs({tg: sa, th: sb}, simultaneous=True)) == 0:
                            if not degenerate(sa) and not degenerate(sb) and is_frame_ratio(sa) and is_frame_ratio(sb):
                                admissible.append((str(sa), str(sb)))
        info["points"] = [str(v) for v in vals]
        info["admissible"] = admissible
        return ("candidate" if admissible else "dead"), info
    return "unknown", {"note": "the (x, z) model is not quadratic in either variable"}


def analyse_joint_xz(phi, dg, dh):
    """One record for the (x, z)-model route of the joint quotient."""
    rec = {"by": "joint_xz"}
    try:
        C = joint_quotient_xz(phi)
        if C is None:
            rec["error"] = "no unique image factor"
            return rec
        P = sp.Poly(C, XS, ZS)
        rec["deg"] = (P.degree(XS), P.degree(ZS))
        g, cons, Qs, deg = quotient_genus(sp.expand(C.subs({XS: U, ZS: th}, simultaneous=True)), th)
        rec.update(genus=g, consistent=cons)
        if g == 1:
            v, info = try_kill_joint_xz(C, phi)
            rec.update(verdict=v, kill=info)
    except Exception as e:                       # pragma: no cover
        rec["error"] = repr(e)[:160]
    return rec


def _lift_xz_to_curve(phi, x0, z0):
    """The admissible frame pairs over a rational point (x0, z0) of the (x, z) model."""
    out = []
    if x0 <= 0 or z0 <= 0:
        return out
    a, b = sp.sqrt(x0), sp.sqrt(z0)
    if not (a.is_rational and b.is_rational):
        return out
    for sa in (a, -a):
        for sb in (b, -b):
            if sp.expand(phi.subs({tg: sa, th: sb}, simultaneous=True)) == 0:
                if not degenerate(sa) and not degenerate(sb) and is_frame_ratio(sa) and is_frame_ratio(sb):
                    out.append((str(sa), str(sb)))
    return out


def two_step_joint(phi, sym):
    """E = Phi/sigma in the (x, z) = (t_g^2, t_h^2) model; a second involution tau
    on one coordinate (t -> -1/t or 1/t) induces x -> 1/x (or z -> 1/z) on E; W =
    E/taubar through coordinate_quotient with kind 'rec'.  Returns a list of records
    (one per available tau), each with the genus of W and, when the rank-0 route
    applies, the verdict and the lift."""
    from compute.omega3 import parametrize, ug, uh, lam
    recs = []
    C = joint_quotient_xz(phi)
    if C is None:
        return [{"by": "two_step", "error": "no (x, z) model"}]
    # C in (XS, ZS); present it in the (tg, th) slots for coordinate_quotient
    Cs = sp.expand(C.subs({XS: tg, ZS: th}, simultaneous=True))
    taus = []
    if sym.get("negrec_g") or sym.get("rec_g"):
        taus.append("g")
    if sym.get("negrec_h") or sym.get("rec_h"):
        taus.append("h")
    for which in taus:
        rec = {"by": "two_step_" + which}
        try:
            cq = coordinate_quotient(Cs, which, "rec")
            if cq is None:
                rec["error"] = "no unique image factor for W"
                recs.append(rec)
                continue
            W, other, u_expr, rel = cq                     # W(U, other): U = v = x + 1/x (which = g) or z + 1/z (which = h)
            gW, cons, Ws, degW = quotient_genus(W, other)
            rec.update(genus_W=gW, deg_W=degW)
            var = tg if which == "g" else th               # the coordinate of E on which taubar acts (x or z)
            if gW == 1:
                # W genus 1: the rank-0 route on W, then the preimages on E, then the lift
                for qvar, ovar in ((other, U), (U, other)):
                    if sp.Poly(W, qvar).degree() != 2:
                        continue
                    dm = _disc_model(W, qvar, ovar)
                    if dm is None:
                        continue
                    sqf, dfl, genus = dm
                    if genus != 1:
                        break
                    key, r = gp_model(sqf, ovar)
                    info = {"level": "W genus 1", "model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
                    if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
                        info["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
                        rec.update(verdict="unknown", kill=info)
                        break
                    vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, ovar)
                    adm = []
                    for v0 in vals:
                        for w0 in _rational_roots(sp.expand(W.subs(ovar, v0)), qvar):
                            u0, o0 = (v0, w0) if ovar == U else (w0, v0)
                            for e0 in _rational_roots(sp.expand(rel.subs(U, u0)), var):       # x (or z) on E
                                x0, z0 = (e0, o0) if which == "g" else (o0, e0)
                                adm += _lift_xz_to_curve(phi, x0, z0)
                    info["points"] = [str(v) for v in vals]
                    info["admissible"] = adm
                    rec.update(verdict=("candidate" if adm else "dead"), kill=info)
                    break
                else:
                    rec.update(verdict="unknown", kill={"note": "W not quadratic in either variable"})
            elif gW == 0:
                # W genus 0: parametrize (quadratic in a variable), then E: e^2 - v(lam) e + 1 = 0 -> y^2 = v^2 - 4
                done = False
                for qvar, ovar in ((other, U), (U, other)):
                    if sp.Poly(W, qvar).degree() not in (1, 2):
                        continue
                    Wp = sp.expand(W.subs({U: ug, other: uh}, simultaneous=True))
                    pv, po = (uh, ug) if qvar == other else (ug, uh)
                    pars, how, cands = parametrize(Wp, pv, po)
                    rec["how"] = how
                    if not pars:
                        rec.update(verdict="unknown", kill={"note": "W genus 0 but no parametrization: " + how})
                        done = True
                        break
                    adm = []; models = []; ok = True
                    for a_l, b_l in pars:                   # a_l = ug(lam) = v, b_l = uh(lam) = other
                        v_l = sp.cancel(a_l)
                        Nv, Dv = sp.fraction(sp.together(v_l))
                        D = sp.expand(Nv ** 2 - 4 * Dv ** 2)          # y^2 = v^2 - 4 (times Dv^2)
                        dfl = sp.factor_list(D)
                        sqf = sp.expand(squarefree_part(dfl[0]) * sp.Mul(*[q for q, m2 in dfl[1] if m2 % 2 == 1]))      # entry 119: the constant kept (a twist otherwise)
                        dd = sp.Poly(sqf, lam).degree() if sqf.free_symbols else 0
                        gE = (dd - 1) // 2 if dd >= 1 else 0
                        if gE != 1 or dd not in (3, 4):
                            ok = False
                            models.append({"branch": str(v_l)[:50], "genus_model": gE, "note": "not a genus-1 quartic"})
                            break
                        key, r = gp_model(sqf, lam)
                        m = {"branch": str(v_l)[:50], "model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
                        models.append(m)
                        if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
                            m["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
                            ok = False
                            break
                        vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, lam)
                        for l0 in vals:
                            v0 = v_l.subs(lam, l0)
                            o0 = sp.cancel(b_l).subs(lam, l0)
                            if not (v0.is_rational and o0.is_rational):
                                continue
                            for e0 in _rational_roots(sp.expand(var ** 2 - v0 * var + 1), var):
                                x0, z0 = (e0, o0) if which == "g" else (o0, e0)
                                adm += _lift_xz_to_curve(phi, x0, z0)
                        # the parametrization's missed points (cands: (other0, v0) pairs) -- lift them too
                        for o0, v0 in cands:
                            for e0 in _rational_roots(sp.expand(var ** 2 - v0 * var + 1), var):
                                x0, z0 = (e0, o0) if which == "g" else (o0, e0)
                                adm += _lift_xz_to_curve(phi, x0, z0)
                    rec.update(verdict=("dead" if (ok and not adm) else ("candidate" if adm else "unknown")), kill={"level": "W genus 0", "models": models, "admissible": adm})
                    done = True
                    break
                if not done:
                    rec.update(verdict="unknown", kill={"note": "W genus 0 but not quadratic in either variable"})
            else:
                rec.update(verdict="unknown", kill={"note": "W has genus " + str(gW)})
        except Exception as e:                       # pragma: no cover
            rec["error"] = repr(e)[:200]
        recs.append(rec)
    return recs


def _w_route(W, phi, lift_points, which_label, disc_expr=None):
    """Shared endgame for a quotient W(U, other) of E: genus of W; genus 1 -> rank-0
    points -> preimages; genus 0 -> parametrization -> E as a double cover -> rank 0.
    lift_points(u0, o0) returns the admissible frame pairs over a point of W.
    Returns a record."""
    from compute.omega3 import parametrize, ug, uh, lam
    other = th
    rec = {"by": which_label}
    gW, cons, Ws, degW = quotient_genus(W, other)
    rec.update(genus_W=gW, deg_W=degW)
    if gW == 1:
        for qvar, ovar in ((other, U), (U, other)):
            if sp.Poly(W, qvar).degree() != 2:
                continue
            dm = _disc_model(W, qvar, ovar)
            if dm is None:
                continue
            sqf, dfl, genus = dm
            if genus != 1:
                break
            key, r = gp_model(sqf, ovar)
            info = {"level": "W genus 1", "model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
            if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
                info["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
                rec.update(verdict="unknown", kill=info)
                return rec
            vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, ovar)
            adm = []
            for v0 in vals:
                for w0 in _rational_roots(sp.expand(W.subs(ovar, v0)), qvar):
                    u0, o0 = (v0, w0) if ovar == U else (w0, v0)
                    adm += lift_points(u0, o0)
            info["points"] = [str(v) for v in vals]
            info["admissible"] = adm
            rec.update(verdict=("candidate" if adm else "dead"), kill=info)
            return rec
        rec.update(verdict="unknown", kill={"note": "W not quadratic in either variable"})
        return rec
    if gW == 0:
        for qvar, ovar in ((other, U), (U, other)):
            if sp.Poly(W, qvar).degree() not in (1, 2):
                continue
            Wp = sp.expand(W.subs({U: ug, other: uh}, simultaneous=True))
            pv, po = (uh, ug) if qvar == other else (ug, uh)
            pars, how, cands = parametrize(Wp, pv, po)
            rec["how"] = how
            if not pars:
                rec.update(verdict="unknown", kill={"note": "W genus 0 but no parametrization: " + how})
                return rec
            if disc_expr is None:
                rec.update(verdict="unknown", kill={"note": "W genus 0: parametrization found (" + how + "); no discriminant for this involution"})
                return rec
            # E is the double cover of W cut by a quadratic with discriminant Delta(U, other): over the
            # parameter, y^2 = Delta(u(lam), o(lam)) cleared to a polynomial -- E's own hyperelliptic model
            adm = []; models = []; ok = True
            for a_l, b_l in pars:                                  # a_l = ug(lam) <-> U, b_l = uh(lam) <-> other
                Dl = sp.together(disc_expr.subs({U: a_l, other: b_l}, simultaneous=True))
                Nd, Dd = sp.fraction(Dl)
                D = sp.expand(Nd * Dd)
                if D == 0:
                    ok = False
                    models.append({"branch": str(a_l)[:40], "note": "vanishing discriminant"})
                    break
                dfl = sp.factor_list(D)
                sqf = sp.expand(squarefree_part(dfl[0]) * sp.Mul(*[q for q, m2 in dfl[1] if m2 % 2 == 1]))      # entry 119: the constant kept (a twist otherwise)
                dd = sp.Poly(sqf, lam).degree() if sqf.free_symbols else 0
                gE = (dd - 1) // 2 if dd >= 1 else 0
                if gE != 1 or dd not in (3, 4):
                    ok = False
                    models.append({"branch": str(a_l)[:40], "genus_model": gE, "note": "not a genus-1 quartic"})
                    break
                key, r = gp_model(sqf, lam)
                m = {"branch": str(a_l)[:40], "model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
                models.append(m)
                if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
                    m["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
                    ok = False
                    break
                vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, lam)
                for l0 in vals:
                    u0 = sp.cancel(a_l).subs(lam, l0)
                    o0 = sp.cancel(b_l).subs(lam, l0)
                    if u0.is_rational and o0.is_rational:
                        adm += lift_points(u0, o0)
                for c0, c1 in cands:                                # the parametrization's missed points (po value, pv value)
                    u0, o0 = (c0, c1) if qvar == other else (c1, c0)
                    if u0.is_rational and o0.is_rational:
                        adm += lift_points(u0, o0)
            rec.update(verdict=("dead" if (ok and not adm) else ("candidate" if adm else "unknown")),
                       kill={"level": "W genus 0", "how": how, "models": models, "admissible": adm})
            return rec
        rec.update(verdict="unknown", kill={"note": "W genus 0 but not quadratic in either variable"})
        return rec
    rec.update(verdict="unknown", kill={"note": "W has genus " + str(gW)})
    return rec


def two_step_joint_more(phi, sym):
    """The joint reciprocity (x, z) -> (1/x, 1/z) and the swap (x, z) -> (z, x) on the
    joint quotient E (the (x, z) model), through the invariants (x + 1/x, z + 1/z) and
    (x + z, xz); genus-1 W handled by the rank-0 route with the exact lift."""
    recs = []
    C = joint_quotient_xz(phi)
    if C is None:
        return [{"by": "two_step_more", "error": "no (x, z) model"}]
    Cs = sp.expand(C.subs({XS: tg, ZS: th}, simultaneous=True))       # x in the tg slot, z in the th slot
    if sym.get("rec_both") and not (sym.get("rec_g") or sym.get("negrec_g") or sym.get("rec_h") or sym.get("negrec_h")):
        try:
            cq = coordinate_quotient(Cs, "g", "rec")                     # v = x + 1/x, still with z (th)
            if cq is None:
                recs.append({"by": "two_step_recboth", "error": "no unique image factor (step 1)"})
            else:
                C1, other, u_expr, rel = cq                              # C1(U = v, th = z)
                C1s = sp.expand(C1.subs(U, tg))                          # v in the tg slot
                cq2 = coordinate_quotient(C1s, "h", "rec")               # w = z + 1/z, with v (tg)
                if cq2 is None:
                    recs.append({"by": "two_step_recboth", "error": "no unique image factor (step 2)"})
                else:
                    W, other2, u2, rel2 = cq2                            # W(U = w, tg = v)
                    Wn = sp.expand(W.subs(tg, th))                       # W(U = w, th = v): other = th
                    def lift(w0, v0):
                        out = []
                        for x0 in _rational_roots(sp.expand(tg ** 2 - v0 * tg + 1), tg):
                            for z0 in _rational_roots(sp.expand(th ** 2 - w0 * th + 1), th):
                                out += _lift_xz_to_curve(phi, x0, z0)
                        return out
                    recs.append(_w_route(Wn, phi, lift, "two_step_recboth", disc_expr=th ** 2 - 4))
        except Exception as e:                                           # pragma: no cover
            recs.append({"by": "two_step_recboth", "error": repr(e)[:200]})
    if sym.get("swap") or sym.get("swap_neg"):
        try:
            SS, PP = sp.symbols("s_q p_q")
            R1 = sp.expand(sp.resultant(sp.Poly(Cs, tg), sp.Poly(tg + th - SS, tg)))          # in (th = z, SS)
            R2 = sp.expand(sp.resultant(sp.Poly(R1, th), sp.Poly(th ** 2 - SS * th + PP, th)))  # in (SS, PP)
            facs = []
            for fac, m in sp.factor_list(R2)[1]:
                fe = sp.expand(fac)
                if SS not in fe.free_symbols or PP not in fe.free_symbols:
                    continue
                test = sp.expand(fe.subs({SS: tg + th, PP: tg * th}, simultaneous=True))
                q, r = sp.div(sp.Poly(test, tg, th), sp.Poly(Cs, tg, th))
                if r.is_zero:
                    facs.append(fe)
            if len(facs) != 1:
                recs.append({"by": "two_step_swap", "error": "no unique image factor"})
            else:
                Wn = sp.expand(facs[0].subs({PP: U, SS: th}, simultaneous=True))              # W(U = p, th = s)
                def lift2(p0, s0):
                    out = []
                    roots = _rational_roots(sp.expand(tg ** 2 - s0 * tg + p0), tg)
                    for x0 in roots:
                        z0 = s0 - x0
                        out += _lift_xz_to_curve(phi, x0, z0)
                    return out
                recs.append(_w_route(Wn, phi, lift2, "two_step_swap", disc_expr=th ** 2 - 4 * U))
        except Exception as e:                                           # pragma: no cover
            recs.append({"by": "two_step_swap", "error": repr(e)[:200]})
    return recs
