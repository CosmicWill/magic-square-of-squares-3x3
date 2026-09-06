"""THE GENUS-0/1 COMPONENTS AT HIGH BIDEGREE (entry 108): the two-step trick one level up.

The (2,1,1) box has components of exact genus 1 (bidegree (4,4), (8,4), (4,8), (4,12),
(12,8), ...) and genus 0 ((5,2), (3,5), ...) above the pullback threshold, which the
engine leaves 'unknown'.  For a GENUS-1 component Phi the quotient by an involution has
genus 0 or 1:
  * genus-0 quotient W, quadratic in a variable: W is parametrized (the conic route) and
    Phi is the double cover y^2 = Delta(lambda), Delta the discriminant of Phi's coordinate
    over W (t^2 - u t - 1: u^2 + 4; t^2 - u t + 1: u^2 - 4; t^2 - u: u; the joint sign
    change: x = t_g^2 itself) -- Phi's OWN genus-1 quartic (or cubic) model: PARI's rank
    (unconditional) with a complete enumeration lists every rational point, each lifts
    exactly to Phi, and if no lift is an admissible frame pair the component is DEAD;
  * genus-1 quotient W, quadratic in a variable: the rank-0 route on W, the finitely many
    preimages on Phi, the same lift;
  * the joint quotient of genus 1: the two-step route of entry 106 (a second involution).
A GENUS-0 component quadratic in a variable goes to the pullback machinery of entry 98
(the monomial lemma, the third-frame lift), which the degree cap had excluded.
"""
from __future__ import annotations
import sympy as sp

from compute.omega3 import (tg, th, ug, uh, lam, is_frame_ratio, degenerate, _disc_model, square_part_roots, gp_model,
                            parametrize, decide_component, frame_factors, ORDER)
from compute.omega3_quotients import (U, XS, ZS, coordinate_quotient, joint_quotient_xz, quotient_genus, try_kill,
                                      two_step_joint, two_step_joint_more, _rational_roots, _lift_xz_to_curve)


def _symmetries(phi, dg, dh):
    def prop(a, b):
        return sp.expand(a - b) == 0 or sp.expand(a + b) == 0
    s = {}
    s["neg_g"] = prop(phi, phi.subs(tg, -tg)); s["neg_h"] = prop(phi, phi.subs(th, -th))
    s["neg_both"] = prop(phi, phi.subs({tg: -tg, th: -th}, simultaneous=True))
    s["rec_g"] = prop(phi, sp.expand(phi.subs(tg, 1 / tg) * tg ** dg)); s["rec_h"] = prop(phi, sp.expand(phi.subs(th, 1 / th) * th ** dh))
    s["rec_both"] = prop(phi, sp.expand(phi.subs({tg: 1 / tg, th: 1 / th}, simultaneous=True) * tg ** dg * th ** dh))
    s["negrec_g"] = prop(phi, sp.expand(phi.subs(tg, -1 / tg) * tg ** dg)); s["negrec_h"] = prop(phi, sp.expand(phi.subs(th, -1 / th) * th ** dh))
    s["swap"] = prop(phi, phi.subs({tg: th, th: tg}, simultaneous=True)) if dg == dh else False
    s["swap_neg"] = prop(phi, phi.subs({tg: -th, th: -tg}, simultaneous=True)) if dg == dh else False
    return s


def _rank0_model_points(D, var):
    """y^2 = D(var): (ok, info, values) -- ok when the model is a genus-1 quartic/cubic of
    rank 0 with a complete enumeration; values = the rational var-values of its points
    plus the square-part roots."""
    dfl = sp.factor_list(D)
    sqf = sp.expand(sp.Mul(*[q for q, m2 in dfl[1] if m2 % 2 == 1]))
    dd = sp.Poly(sqf, var).degree() if sqf.free_symbols else 0
    genus = (dd - 1) // 2 if dd >= 1 else 0
    if genus != 1 or dd not in (3, 4):
        return False, {"note": "not a genus-1 quartic", "model_genus": genus, "deg": dd}, []
    key, r = gp_model(sqf, var)
    info = {"model": key, "rank": (r.get("rank_lo"), r.get("rank_hi")), "torsion": r.get("torsion_order")}
    if "error" in r or r.get("rank_hi", 1) > 0 or not r.get("complete"):
        info["note"] = r.get("error") or ("rank > 0" if r.get("rank_hi", 1) > 0 else "not complete")
        return False, info, []
    vals = [sp.Rational(t) for t in r["tvals"]] + square_part_roots(dfl, var)
    return True, info, vals


def own_model_via_quotient(phi, dg, dh, which, kind):
    """Phi of genus 1 with the involution `kind` on coordinate `which` whose quotient W has
    genus 0: Phi's own model over W's parameter.  Returns (verdict, info)."""
    var, other = (tg, th) if which == "g" else (th, tg)
    cq = coordinate_quotient(phi, which, kind)
    if cq is None:
        return "unknown", {"note": "no unique image factor"}
    W, oth, u_expr, rel = cq
    gW, cons, Ws, degW = quotient_genus(W, oth)
    info = {"by": kind + "_" + which, "genus_W": gW, "deg_W": degW}
    if gW == 1:
        v, kinfo = try_kill(W, oth, u_expr, var, rel)
        info.update(level="W genus 1", kill=kinfo)
        return v, info
    if gW != 0:
        info["note"] = "W has genus " + str(gW)
        return "unknown", info
    disc = {"negrec": U ** 2 + 4, "rec": U ** 2 - 4, "neg": U}[kind]
    for qvar, ovar in ((oth, U), (U, oth)):
        if sp.Poly(W, qvar).degree() not in (1, 2):
            continue
        Wp = sp.expand(W.subs({U: ug, oth: uh}, simultaneous=True))
        pv, po = (uh, ug) if qvar == oth else (ug, uh)
        pars, how, cands = parametrize(Wp, pv, po)
        info["how"] = how
        if not pars:
            info["note"] = "W genus 0 but no parametrization: " + how
            return "unknown", info
        adm = []; models = []
        for a_l, b_l in pars:                      # (U(lam), other(lam))
            Dl = sp.together(disc.subs(U, a_l))
            Nd, Dd = sp.fraction(Dl)
            ok, minfo, vals = _rank0_model_points(sp.expand(Nd * Dd), lam)
            minfo["branch"] = str(a_l)[:40]
            models.append(minfo)
            if not ok:
                info.update(level="Phi's own model", models=models)
                return "unknown", info
            for l0 in vals:
                u0 = sp.cancel(a_l).subs(lam, l0); o0 = sp.cancel(b_l).subs(lam, l0)
                if not (u0.is_rational and o0.is_rational):
                    continue
                for t0 in _rational_roots(sp.expand(rel.subs(U, u0)), var):
                    if not degenerate(t0) and not degenerate(o0) and is_frame_ratio(t0) and is_frame_ratio(o0):
                        adm.append((str(t0), str(o0)))
        for c0, c1 in cands:                       # (po value, pv value)
            u0, o0 = (c0, c1) if qvar == oth else (c1, c0)
            if u0.is_rational and o0.is_rational:
                for t0 in _rational_roots(sp.expand(rel.subs(U, u0)), var):
                    if not degenerate(t0) and not degenerate(o0) and is_frame_ratio(t0) and is_frame_ratio(o0):
                        adm.append((str(t0), str(o0)))
        info.update(level="Phi's own model", models=models, admissible=adm)
        return ("candidate" if adm else "dead"), info
    info["note"] = "W genus 0 but not quadratic in either variable"
    return "unknown", info


def own_model_via_joint(phi, dg, dh):
    """Phi of genus 1 whose joint quotient (x, z) = (t_g^2, t_h^2) has genus 0 and is
    quadratic in a variable: Phi is the double cover y^2 = X(lambda) (the function t_g
    generates it; t_h follows), its own quartic model."""
    C = joint_quotient_xz(phi)
    if C is None:
        return "unknown", {"note": "no (x, z) model"}
    Cs = sp.expand(C.subs({XS: tg, ZS: th}, simultaneous=True))
    P = sp.Poly(Cs, tg, th)
    from compute.omega3_resolve import exact_genus_checked
    g, det = exact_genus_checked(Cs, P.degree(tg), P.degree(th), degmax=60, timeout=300)
    info = {"by": "joint_xz", "genus_E": g, "deg_E": (P.degree(tg), P.degree(th))}
    if g != 0:
        info["note"] = "joint quotient has genus " + str(g)
        return "unknown", info
    for qvar, ovar in ((th, tg), (tg, th)):
        if P.degree(qvar) not in (1, 2):
            continue
        Cp = sp.expand(Cs.subs({tg: ug, th: uh}, simultaneous=True))
        pv, po = (uh, ug) if qvar == th else (ug, uh)
        pars, how, cands = parametrize(Cp, pv, po)
        info["how"] = how
        if not pars:
            info["note"] = "E genus 0 but no parametrization: " + how
            return "unknown", info
        adm = []; models = []
        for a_l, b_l in pars:                      # (x(lam), z(lam))
            Nx, Dx = sp.fraction(sp.together(a_l))
            ok, minfo, vals = _rank0_model_points(sp.expand(Nx * Dx), lam)
            minfo["branch"] = str(a_l)[:40]
            models.append(minfo)
            if not ok:
                info.update(level="Phi's own model over the joint quotient", models=models)
                return "unknown", info
            for l0 in vals:
                x0 = sp.cancel(a_l).subs(lam, l0); z0 = sp.cancel(b_l).subs(lam, l0)
                if x0.is_rational and z0.is_rational:
                    adm += _lift_xz_to_curve(phi, x0, z0)
        for c0, c1 in cands:
            x0, z0 = (c0, c1) if qvar == th else (c1, c0)
            if x0.is_rational and z0.is_rational:
                adm += _lift_xz_to_curve(phi, x0, z0)
        info.update(level="Phi's own model over the joint quotient", models=models, admissible=adm)
        return ("candidate" if adm else "dead"), info
    info["note"] = "E genus 0 but not quadratic in either variable"
    return "unknown", info


def attack_component(phi, dg, dh, genus, cand=None, f=None):
    """Every route for one unknown component of exact genus 0 or 1; returns (verdict, records).
    cand, f let the genus-0 pullback route run the third-frame lift."""
    recs = []
    best = "unknown"
    if genus in (0, 1):
        try:
            v, info = conjugate_kill(phi, dg, dh)                # absolutely reducible over a quadratic field?
        except Exception as e:                                   # pragma: no cover
            v, info = "unknown", {"by": "conjugate", "error": repr(e)[:160]}
        recs.append(dict(info, verdict=v))
        if v == "dead":
            return "dead", recs
        if v == "candidate":
            best = "candidate"
    if genus == 1:
        sym = _symmetries(phi, dg, dh)
        for which in ("g", "h"):
            for kind in ("neg", "rec", "negrec"):
                if sym.get(kind + "_" + which):
                    try:
                        v, info = own_model_via_quotient(phi, dg, dh, which, kind)
                    except Exception as e:                       # pragma: no cover
                        v, info = "unknown", {"by": kind + "_" + which, "error": repr(e)[:160]}
                    recs.append(dict(info, verdict=v))
                    if v == "dead":
                        return "dead", recs
                    if v == "candidate":
                        best = "candidate"
        try:
            v, info = own_model_via_joint(phi, dg, dh)
        except Exception as e:                                   # pragma: no cover
            v, info = "unknown", {"by": "joint_xz", "error": repr(e)[:160]}
        recs.append(dict(info, verdict=v))
        if v == "dead":
            return "dead", recs
        if v == "candidate":
            best = "candidate"
        if info.get("genus_E") == 1:
            for x in two_step_joint(phi, sym) + two_step_joint_more(phi, sym):
                recs.append(x)
                if x.get("verdict") == "dead":
                    return "dead", recs
                if x.get("verdict") == "candidate":
                    best = "candidate"
    elif genus == 0 and (dg == 2 or dh == 2):
        v, info = decide_component(phi, dg, dh, cand, f, pullback_max_degree=12)
        recs.append({"by": "pullback (cap 12)", "verdict": v, "pullback": [{k: x.get(k) for k in ("kind", "deg", "genus", "verdict", "how", "note")}
                                                                            for x in info.get("pullback", [])]})
        return v, recs
    return best, recs


QUADRATIC_D = (-1, 2, -2, 3, -3, 5, -5, 6, -6, 7, -7, 10, -10, 11, -11, 13, -13, 14, -14, 15, -15, 21, -21, 22, -22,
               26, 30, -30, 33, 35, -35, 39, 42, 65, 105)


def conjugate_split(phi, ds=QUADRATIC_D):
    """(d, Phi_1) when phi factors over Q(sqrt d) as Phi_1 * conj(Phi_1) (up to a constant),
    else None.  sympy's factor with an algebraic extension."""
    for d in ds:
        try:
            f = sp.factor(phi, extension=sp.sqrt(d))
        except Exception:
            continue
        facs = [a for a in sp.Mul.make_args(f) if a.free_symbols]
        if len(facs) >= 2:
            return d, sp.expand(facs[0])
        if len(facs) == 1 and isinstance(facs[0], sp.Pow):
            return d, sp.expand(facs[0].base)
    return None


def conjugate_kill(phi, dg, dh):
    """A component irreducible over Q that splits over Q(sqrt d): every rational point lies
    on Phi_1 and on its conjugate, i.e. on A = Phi_1 + conj(Phi_1) and B = (Phi_1 -
    conj(Phi_1))/sqrt d, two polynomials over Q with a finite common zero set (the pieces
    are distinct).  Returns (verdict, info): 'dead' when no common rational zero is an
    admissible frame pair."""
    sp_ = conjugate_split(phi)
    if sp_ is None:
        return "unknown", {"by": "conjugate", "note": "no quadratic splitting field found"}
    d, P1 = sp_
    r = sp.sqrt(d)
    P1c = sp.expand(P1.subs(r, -r))
    A = sp.expand(P1 + P1c)
    B = sp.expand(sp.cancel((P1 - P1c) / r))
    info = {"by": "conjugate", "d": d, "deg_piece": (sp.Poly(P1, tg, th).degree(tg), sp.Poly(P1, tg, th).degree(th))}
    if A == 0 or B == 0 or (A.free_symbols & {r}) or (B.free_symbols & {r}):
        info["note"] = "the rational parts are degenerate"
        return "unknown", info
    G = sp.gcd(sp.Poly(A, tg, th), sp.Poly(B, tg, th))
    if G.total_degree() > 0:
        info["note"] = "the pieces share a component"
        return "unknown", info
    pts = set()
    Res = sp.resultant(sp.Poly(A, th), sp.Poly(B, th)) if sp.Poly(A, th).degree() > 0 and sp.Poly(B, th).degree() > 0 else None
    if Res is None or Res == 0:
        info["note"] = "resultant degenerate"
        return "unknown", info
    for t0 in _rational_roots(sp.expand(Res), tg):
        a0, b0 = sp.expand(A.subs(tg, t0)), sp.expand(B.subs(tg, t0))
        if a0 == 0 and b0 == 0:
            info["note"] = "a whole vertical line of common zeros"
            return "unknown", info
        g = sp.gcd(sp.Poly(a0, th), sp.Poly(b0, th)) if (a0 != 0 and b0 != 0) else sp.Poly(a0 if a0 != 0 else b0, th)
        if g.degree() <= 0:
            continue
        for x0 in _rational_roots(g.as_expr(), th):
            if sp.expand(phi.subs({tg: t0, th: x0}, simultaneous=True)) == 0:
                pts.add((t0, x0))
    adm = [(str(a), str(b)) for a, b in pts if not degenerate(a) and not degenerate(b) and is_frame_ratio(a) and is_frame_ratio(b)]
    info["rational_points"] = [(str(a), str(b)) for a, b in sorted(pts, key=str)]
    info["admissible"] = adm
    return ("candidate" if adm else "dead"), info
