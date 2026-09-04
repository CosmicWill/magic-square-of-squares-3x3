"""QUOTIENT TOWERS for the finite classes of the (1,1,1) box (entry 100).

A finite class has, in some frame, a component whose rational points lie on a
hyperelliptic model y^2 = D(t) of genus >= 2 (Faltings-finite, not effective).
The frame symmetries act on the model: t -> -t is the conjugate frame (every
model is even), t -> +-1/t the associate frame (some models are reciprocal),
and a model may carry a twisted reciprocity t -> kappa/t.  Each involution
gives a QUOTIENT CURVE of lower genus, defined over Q, and the quotient map
sends rational points to rational points:
    u = t^2               : y^2 = G(u),  D(t) = G(t^2)                 (D even)
    w = t + kappa/t       : y^2 = P(w),  D(t) = t^{d/2} P(w)            (t^d D(kappa/t) = D(t))
    odd companion         : an EVEN quotient polynomial Q(x) = Qt(x^2) also gives
                            Y^2 = x Qt(x) (the quotient by x -> -x, y -> -y)
    v = u + kappa/u       : y^2 = H(v),  G(u) = u^{n/2} H(v)            (G twisted-reciprocal)
When a quotient has genus 1 with PARI rank 0 and a complete point enumeration
(pari_genus1: a rank-0 quartic is empty or a torsor under E_tors), every
rational point of the model lies over one of finitely many quotient points;
the preimages are solved exactly and the rational ones kept.  Extra candidates
a model can hide -- roots of the square part of a discriminant, roots of a
square part of a quotient polynomial -- are carried along.  A component is
DEAD when some rank-0 quotient leaves no candidate that is a non-degenerate
frame ratio (level 't': t not in {0,+-1,inf} and |t| = n/m with m^2+n^2 a
square) or a non-degenerate tau (level 'tau').  Otherwise the candidates are
listed, or the quotients' ranks recorded ('finite'), with a height search on
the model as evidence only.

For a component whose Phi-level discriminant has genus 0 but whose Pythagorean
pullback has no hyperelliptic model, the FRAME-CONDITION ROUTE: parametrize
the rational Phi-component, t_g(lam), t_h(lam); each frame condition
1 + t^2 = square is the curve y^2 = N(lam)^2 + D(lam)^2 in the parameter; a
rank-0 one gives finitely many lam, hence finitely many candidate pairs.
"""
from __future__ import annotations
import re
import subprocess
import sympy as sp

from compute.omega3 import (frame_factors, tg, th, ug, uh, lam, pyth, is_frame_ratio, degenerate,
                            _disc_model, square_part_roots, sqrt_rational, conic_point, ORDER)
from compute.pari_genus1 import quartic_points, gp_available, GP

u_, w_, v_, z_ = sp.symbols("u_ w_ v_ z_")
_cache = {}


def identify(coeffs, timeout=120):
    """(j, Cremona label or 'none') of the Jacobian of y^2 = f(t)."""
    key = ("id", tuple(coeffs))
    if key in _cache:
        return _cache[key]
    poly = " + ".join(f"({c})*t^{len(coeffs)-1-i}" for i, c in enumerate(coeffs))
    script = ('default(parisize,"128M");\n' + f'E = ellinit(ellfromeqn(y^2 - ({poly})));\n'
              + 'lab = iferr(ellidentify(E)[1][1], er, "none");\nprint("RES ", E.j, " ", lab, " ", ellglobalred(E)[1]);\n')
    try:
        out = subprocess.run([GP, "-q", "-f"], input=script, capture_output=True, text=True, timeout=timeout).stdout
    except (subprocess.TimeoutExpired, OSError):
        out = ""
    m = re.search(r"RES\s+(\S+)\s+(\S+)\s+(\d+)", out)
    _cache[key] = (m.group(1), m.group(2), int(m.group(3))) if m else (None, None, None)
    return _cache[key]


def pari(coeffs):
    key = ("pts", tuple(coeffs))
    if key not in _cache:
        _cache[key] = quartic_points(list(coeffs))
    return _cache[key]


def search_points(coeffs, H=2000, timeout=300):
    """hyperellratpoints on y^2 = f(t) of any degree (evidence only): finite x-values."""
    key = ("srch", tuple(coeffs), H)
    if key in _cache:
        return _cache[key]
    poly = " + ".join(f"({c})*t^{len(coeffs)-1-i}" for i, c in enumerate(coeffs))
    script = 'default(parisize,"256M");\n' + f'L = hyperellratpoints({poly}, {H});\n' + 'print("RES ", L);\n'
    try:
        out = subprocess.run([GP, "-q", "-f"], input=script, capture_output=True, text=True, timeout=timeout).stdout
    except (subprocess.TimeoutExpired, OSError):
        out = ""
    m = re.search(r"RES\s+(.*)", out, re.S)
    xs = sorted({p[0] for p in re.findall(r"\[\s*(-?\d+(?:/\d+)?)\s*,\s*(-?\d+(?:/\d+)?)\s*\]", m.group(1))}) if m else None
    _cache[key] = xs
    return xs


def int_coeffs(poly, var):
    P = sp.Poly(poly, var)
    cs = [sp.Rational(c) for c in P.all_coeffs()]
    den = sp.ilcm(*[c.q for c in cs]) if cs else 1
    cs = [int(c * den) for c in cs]
    g = 0
    for c in cs:
        g = sp.igcd(g, c)
    return [c // g for c in cs] if g else cs


def squarefree_split(poly, var):
    """poly = (C * sqf) * h^2 : returns (C*sqf, h)."""
    dfl = sp.factor_list(poly)
    sqf, h = sp.Integer(dfl[0]), sp.Integer(1)
    for q, m in dfl[1]:
        if m % 2 == 1:
            sqf *= q
        h *= q ** (m // 2)
    return sp.expand(sqf), sp.expand(h)


def linear_roots(poly, var):
    out = []
    if poly == 0 or not getattr(poly, "free_symbols", None):
        return out
    for q, m in sp.factor_list(poly)[1]:
        if q.free_symbols and sp.Poly(q, var).degree() == 1:
            c1_, c0_ = sp.Poly(q, var).all_coeffs()
            out.append(sp.Rational(-c0_, c1_))
    return out


def is_even(D, t):
    return sp.expand(D.subs(t, -t) - D) == 0


def even_part(D, t, z):
    """D(t) = Dt(t^2): returns Dt(z), or None if D is not even."""
    if not is_even(D, t):
        return None
    P = sp.Poly(D, t)
    return sp.expand(sum(P.coeff_monomial(t ** (2 * k)) * z ** k for k in range(P.degree() // 2 + 1)))


def twisted_kappas(D, t):
    """Rational kappa != 0 with t^d D(kappa/t) = c D(t)."""
    P = sp.Poly(D, t)
    d = P.degree()
    if d % 2:
        return []
    a0, ad = P.all_coeffs()[-1], P.LC()
    if a0 == 0:
        return []
    # product of the roots is a0/ad (up to sign); closed under r -> kappa/r means kappa^{d/2} = +- a0/ad
    n = d // 2
    ratio = sp.Rational(a0, ad)
    out = []
    for sgn in (1, -1):
        val = sgn * ratio
        if val <= 0 and n % 2 == 0:
            continue
        try:
            root = sp.nsimplify(sp.root(abs(val), n))
        except Exception:
            continue
        if not root.is_rational:
            continue
        for kappa in ({root, -root} if val > 0 or n % 2 else {-root if val < 0 else root}):
            if kappa == 0:
                continue
            lhs = sp.expand(t ** d * D.subs(t, kappa / t))
            r = sp.cancel(lhs / D)
            if not r.free_symbols and r != 0:
                out.append(kappa)
    return sorted(set(out), key=lambda k: (abs(k), k))


def reciprocal_quotient(D, t, w, kappa):
    """D(t) = t^{d/2} P(w), w = t + kappa/t.  Returns P(w) or None."""
    P = sp.Poly(D, t)
    d = P.degree()
    if d % 2:
        return None
    n = d // 2
    ps = sp.symbols(f"p0:{n+1}")
    expr = sp.expand(t ** n * sum(ps[k] * (t + kappa / t) ** k for k in range(n + 1)) - D)
    sol = sp.solve(sp.Poly(expr, t).all_coeffs(), ps, dict=True)
    if not sol:
        return None
    return sp.expand(sum(sol[0].get(ps[k], ps[k]) * w ** k for k in range(n + 1)))


def _sqrt_pairs(val):
    val = sp.Rational(val)
    if val < 0:
        return []
    r = sqrt_rational(val) if val > 0 else sp.Integer(0)
    return [r, -r] if r is not None else []


def lift_to_t(chain, xvals):
    """Preimages in t of the quotient points xvals through the chain of maps
    (innermost last).  chain items: ('u',) t = +-sqrt(x); ('w', kappa) t^2 - x t + kappa = 0;
    ('odd',) identity on the coordinate (the odd companion keeps x)."""
    vals = [sp.Rational(x) for x in xvals]
    for step in reversed(chain):
        new = []
        for x in vals:
            if step[0] == "u":
                new += _sqrt_pairs(x)
            elif step[0] == "w":
                kappa = step[1]
                for r in _sqrt_pairs(x * x - 4 * kappa):
                    new.append((x + r) / 2)
            else:
                new.append(x)
        vals = new
    return vals


def genus_of(Q, var):
    sqf, h = squarefree_split(Q, var)
    dd = sp.Poly(sqf, var).degree() if sqf.free_symbols else 0
    return ((dd - 1) // 2 if dd >= 1 else 0), sqf, h


def all_quotients(D, t):
    """Every quotient curve reachable through the symmetries, as
    (name, Q(x), x, chain) with chain the list of maps from t down to x."""
    out = []

    def add_level(Q, x, chain, name, depth):
        out.append((name, Q, x, chain))
        if depth >= 3:
            return
        # even -> u = x^2, and the odd companion
        Qt = even_part(Q, x, z_)
        if Qt is not None and sp.Poly(Q, x).degree() >= 2:
            add_level(Qt.subs(z_, u_ if depth == 0 else z_), u_ if depth == 0 else z_, chain + [("u",)], name + ".u", depth + 1)
            zz = u_ if depth == 0 else z_
            add_level(sp.expand(zz * Qt.subs(z_, zz)), zz, chain + [("odd",)], name + ".odd", depth + 1)
        # (twisted) reciprocal -> w = x + kappa/x
        for kappa in twisted_kappas(Q, x):
            P = reciprocal_quotient(Q, x, w_, kappa)
            if P is not None:
                add_level(P.subs(w_, v_ if depth else w_), v_ if depth else w_, chain + [("w", kappa)], name + f".w({kappa})", depth + 1)

    add_level(D, t, [], "D", 0)
    return out[1:]


def decide_quotient(name, Q, x, chain, level, extra_t):
    genus, sqf, h = genus_of(Q, x)
    rec = {"name": name, "deg": sp.Poly(Q, x).degree(), "genus": genus}
    if genus != 1:
        rec["verdict"] = "finite"
        return rec
    cs = int_coeffs(sqf, x)
    if len(cs) not in (4, 5):
        rec["verdict"] = "finite"
        return rec
    rec["model"] = cs
    r = pari(cs)
    if "error" in r:
        rec.update(verdict="unknown", error=r["error"])
        return rec
    j, label, N = identify(cs)
    rec.update(rank=(r["rank_lo"], r["rank_hi"]), torsion=r["torsion_order"], j=j, label=label, conductor=N)
    if r["rank_hi"] > 0:
        rec["verdict"] = "finite"
        return rec
    if not r["complete"]:
        rec["verdict"] = "unknown"
        return rec
    xvals = [sp.Rational(v) for v in r["tvals"]] + linear_roots(h, x)
    tvals = lift_to_t(chain, xvals) + list(extra_t)
    if level == "t":
        live = sorted({str(v) for v in tvals if not degenerate(v) and is_frame_ratio(v)})
    else:
        live = sorted({str(v) for v in tvals if not degenerate(v)})
    rec.update(quotient_points=[str(v) for v in xvals], candidates=live, verdict="dead" if not live else "candidate")
    return rec


def tower(D, t, level, extra_t=()):
    """(verdict, record) for the model y^2 = D(t)."""
    info = {"deg": sp.Poly(D, t).degree(), "even": is_even(D, t), "kappas": [str(k) for k in twisted_kappas(D, t)], "quotients": []}
    worst = "finite"
    for name, Q, x, chain in all_quotients(D, t):
        r = decide_quotient(name, Q, x, chain, level, extra_t)
        info["quotients"].append(r)
        if r["verdict"] == "dead":
            return "dead", info
        if r["verdict"] == "candidate" and worst == "finite":
            worst = "candidate"
    # evidence: a height search on the model itself
    xs = search_points(int_coeffs(D, t), H=2000)
    if xs is not None:
        if level == "t":
            live = sorted({x for x in xs if not degenerate(sp.Rational(x)) and is_frame_ratio(sp.Rational(x))})
        else:
            live = sorted({x for x in xs if not degenerate(sp.Rational(x))})
        info["search"] = {"H": 2000, "points": xs, "non_degenerate": live}
    return worst, info


def parametrize_xy(fe, var, oth):
    """Rational parametrizations of a genus-0 irreducible fe(var, oth) that is linear
    or quadratic in var: list of dicts {var: expr(lam), oth: expr(lam)}, and the
    candidate points (oth0, var0) the parametrizations can miss."""
    P = sp.Poly(fe, var)
    dv = P.degree()
    cands = []
    if dv == 1:
        a1, a0 = P.all_coeffs()
        return [{oth: lam, var: sp.cancel(-a0 / a1).subs(oth, lam)}], cands
    if dv != 2:
        return [], cands
    a2, a1, a0 = P.all_coeffs()
    for r0 in linear_roots(sp.expand(a2), oth):
        b1, b0 = sp.expand(a1).subs(oth, r0), sp.expand(a0).subs(oth, r0)
        if b1 != 0:
            cands.append((r0, sp.Rational(-b0, b1)))
    disc = sp.expand(a1 ** 2 - 4 * a2 * a0)
    if disc == 0:
        return [{oth: lam, var: sp.cancel(-a1 / (2 * a2)).subs(oth, lam)}], cands
    sqf, h = squarefree_split(disc, oth)
    for r0 in linear_roots(h, oth):
        aa2 = sp.expand(a2).subs(oth, r0)
        if aa2 != 0:
            cands.append((r0, sp.cancel(-sp.expand(a1).subs(oth, r0) / (2 * aa2))))
    Q = sp.Poly(sqf, oth)
    if Q.degree() == 0:
        r = sqrt_rational(sqf)
        if r is None:
            return [], cands
        return [{oth: lam, var: sp.cancel((-a1 + sgn * r * h) / (2 * a2)).subs(oth, lam)} for sgn in (1, -1)], cands
    if Q.degree() > 2:
        return [], cands
    cs = Q.all_coeffs()
    while len(cs) < 3:
        cs = [0] + cs
    qa, qb, qc = cs
    if qa == 0:
        u_of, y_of = (lam ** 2 - qc) / qb, lam
    else:
        pt = conic_point(qa, qb, qc)
        if pt is None:
            return [], cands
        u0, y0 = pt
        if y0 == 0:
            aa2 = sp.expand(a2).subs(oth, u0)
            if aa2 != 0:
                cands.append((u0, sp.cancel(-sp.expand(a1).subs(oth, u0) / (2 * aa2))))
        uu = sp.Symbol("uu_")
        eq = sp.expand(qa * uu ** 2 + qb * uu + qc - (y0 + lam * (uu - u0)) ** 2)
        sol = sp.solve(sp.cancel(eq / (uu - u0)), uu)
        if not sol:
            return [], cands
        u_of = sp.cancel(sol[0])
        y_of = sp.cancel(y0 + lam * (u_of - u0))
    out = []
    for sgn in (1, -1):
        expr = sp.cancel(sp.cancel((-a1 + sgn * y_of * h.subs(oth, u_of)) / (2 * a2)).subs(oth, u_of))
        out.append({oth: u_of, var: expr})
    return out, cands


def frame_condition_route(phi, dg, dh):
    var, oth = (th, tg) if dh in (1, 2) else ((tg, th) if dg in (1, 2) else (None, None))
    if var is None:
        return "finite", {"route": "frame-condition", "note": "no linear/quadratic variable"}
    pars, cands = parametrize_xy(phi, var, oth)
    live = [(str(a), str(b)) for a, b in cands if not (degenerate(a) or degenerate(b)) and is_frame_ratio(a) and is_frame_ratio(b)]
    info = {"route": "frame-condition", "candidates": live, "branches": []}
    if not pars:
        return ("candidate" if live else "finite"), dict(info, note="no parametrization")
    worst = "candidate" if live else "dead"
    for par in pars:
        br = {"tg": str(par[tg])[:60], "th": str(par[th])[:60], "curves": [], "verdict": "finite"}
        for X in (tg, th):
            N, Dn = sp.fraction(sp.together(par[X]))
            S = sp.expand(N ** 2 + Dn ** 2)
            v, tinfo = tower(S, lam, "lam")
            crec = {"frame": str(X), "deg": sp.Poly(S, lam).degree(), "tower": tinfo}
            # a rank-0 quotient of the frame-condition curve gives finitely many lam: check both frames there
            for q in tinfo["quotients"]:
                if q.get("verdict") in ("dead", "candidate") and "quotient_points" in q:
                    lvals = lift_to_t([], q["quotient_points"])
                    pts = []
                    for l0 in lvals:
                        try:
                            a, b = sp.nsimplify(par[tg].subs(lam, l0)), sp.nsimplify(par[th].subs(lam, l0))
                        except Exception:
                            continue
                        if a.is_rational and b.is_rational and not degenerate(a) and not degenerate(b) \
                                and is_frame_ratio(a) and is_frame_ratio(b):
                            pts.append((str(a), str(b)))
                    crec.update(candidates=pts, verdict="dead" if not pts else "candidate", via=q["name"])
                    break
            br["curves"].append(crec)
            if crec.get("verdict") in ("dead", "candidate"):
                br["verdict"] = crec["verdict"]
                break
        info["branches"].append(br)
        if ORDER[br["verdict"]] > ORDER[worst]:
            worst = br["verdict"]
    return worst, info


def component_towers(phi, dg, dh):
    for var, oth, dv in ((th, tg, dh), (tg, th, dg)):
        if dv == 2:
            dm = _disc_model(phi, var, oth)
            if dm is None:
                break
            sqf, dfl, genus = dm
            if genus >= 2:
                v, info = tower(sqf, oth, "t", square_part_roots(dfl, oth))
                return v, dict(info, level="Phi", model_var=str(oth), model_genus=genus)
            break
    psi = sp.expand(phi.subs({tg: pyth(ug), th: pyth(uh)}) * (1 - ug ** 2) ** dg * (1 - uh ** 2) ** dh)
    psi = sp.expand(sp.cancel(psi))
    worst, facs = "dead", []
    for fac, mult in sp.factor_list(psi)[1]:
        fe = sp.expand(fac)
        if not fe.free_symbols:
            continue
        P = sp.Poly(fe, ug, uh)
        eg, eh = P.degree(ug), P.degree(uh)
        if eg == 0 or eh == 0:
            continue
        v, finf = "finite", {"deg": (eg, eh)}
        done = False
        for var, oth, dv in ((uh, ug, eh), (ug, uh, eg)):
            if dv == 2:
                dm = _disc_model(fe, var, oth)
                if dm is not None:
                    sqf, dfl, genus = dm
                    if genus >= 2:
                        v, tinf = tower(sqf, oth, "tau", square_part_roots(dfl, oth))
                        finf.update(tinf, level="Psi", model_genus=genus)
                    else:
                        v = "dead"
                        finf["note"] = "decided at the pullback level"
                    done = True
                break
        if not done:
            v, rinf = frame_condition_route(phi, dg, dh)
            finf.update(rinf)
        facs.append(dict(finf, verdict=v))
        if ORDER[v] > ORDER[worst]:
            worst = v
    return worst, {"level": "Psi", "factors": facs}


def tower_frame(cand, f):
    """Re-decide frame f of a class with towers on its finite components."""
    from compute.omega3 import decide_component
    ff = frame_factors(cand, f)
    if ff is None:
        return {"verdict": "degenerate"}
    curves, live_uni = ff
    worst, details = ("candidate" if live_uni else "dead"), []
    for phi, dg, dh in curves:
        v, info = decide_component(phi, dg, dh, cand, f)
        if v == "finite":
            v2, tinfo = component_towers(phi, dg, dh)
            info = dict(info, towers=tinfo, before="finite")
            v = v2
        details.append(dict(info, verdict=v, phi=str(phi)[:80]))
        if ORDER[v] > ORDER[worst]:
            worst = v
    return {"verdict": worst, "components": details}
