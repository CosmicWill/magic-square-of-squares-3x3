"""THE SYMMETRY TOWER (entries 135-137): quotients of a class's elimination component Phi(g, h) by its sign-and-inversion
symmetries, the hyperelliptic and elliptic endpoints, and the lift of an endpoint's rational points back to the frame
ratios.  A class dies when a route ends on a curve whose rational points are completely known (an elliptic curve of rank 0
with its torsion points, or one of the genus-2 curves decided in entries 118-132) and none of those points lifts to an
admissible pair (g, h).

Steps (each records how to lift a rational point back one level):
  joint(a, b)            X = a^2, Y = a b            when Phi is invariant up to sign under (a, b) -> (-a, -b)
  inversion(a; s)        U = a + s/a                 when Phi is invariant under a -> s/a (s = +-1)
  double_inversion       U = a + s1/a, V = b + s2/b  when Phi is invariant under (a, b) -> (s1/a, s2/b) (fiber 2) or under
                                                     both single inversions (fiber 4)
  hyperelliptic(a, b)    a curve quadratic in one variable q: y^2 = D(o) = S(o)^2 core(o), core squarefree
  even(o)                z = o^2 for an even core;  reciprocal(o; kappa)  w = o + kappa/o for a (twisted) reciprocal core
The quotient polynomials are the repeated factors of resultants; every identity is exact (sympy); the elliptic data is
PARI's (compute.pari_genus1.quartic_points: 2-descent rank bounds, torsion, points, completeness)."""
import itertools
from fractions import Fraction
import sympy as sp

from compute.omega3 import degenerate, is_frame_ratio
from compute.omega3_towers import twisted_kappas, reciprocal_quotient
from compute.pari_genus1 import quartic_points, gp_available

g, h = sp.symbols("g h")
yy = sp.Symbol("yy")

# the genus-2 curves whose rational points are known (entries 118, 130, 131, 132): coefficients highest degree first,
# and the complete list of affine rational points (points at infinity lift only to degenerate ratios)
KNOWN_GENUS2 = {
    "G1": ([25, 0, -29, 0, 11, 0, 1], [(0, 1), (0, -1)], "entry 118 (bielliptic QC + the E1 x E2 sieve)"),
    "F1": ([1, 0, 11, 0, -5, 0, 1], [(0, 1), (0, -1)], "entry 130 (bielliptic QC + the E1 x E2 sieve)"),
    "C_a": ([25, -36, -18, 44, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4), (Fraction(-1, 5), Fraction(32, 25)), (Fraction(-1, 5), Fraction(-32, 25))], "entry 132 (Magma: rank 1, Chabauty + the Mordell-Weil sieve)"),
    "C_b": ([25, -4, -18, 12, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4), (Fraction(-1, 5), Fraction(16, 25)), (Fraction(-1, 5), Fraction(-16, 25))], "entry 132 (Magma)"),
    "C_c": ([1, -4, 6, 12, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4)], "entry 131 (LMFDB 1408.b.180224.2, rank 0)"),
}
LAMBDAS = [sp.Rational(n, d) * s for n in (1, 2, 4, 5, 10, 20, 25, 50, 100) for d in (1, 2, 4, 5, 10, 20, 25, 50, 100) for s in (1, -1)]


def _maps():
    out = {}
    for e1, s1, e2, s2 in itertools.product((1, -1), (1, -1), (1, -1), (1, -1)):
        if (e1, s1, e2, s2) != (1, 1, 1, 1):
            out[("%s%s" % ("-" if e1 < 0 else "", "1/g" if s1 < 0 else "g"), "%s%s" % ("-" if e2 < 0 else "", "1/h" if s2 < 0 else "h"))] = (e1, s1, e2, s2)
    return out


MAPS = _maps()


def is_symmetry(F, a, b, sub):
    num = sp.expand(sp.fraction(sp.together(F.subs(sub, simultaneous=True)))[0])
    q, r = sp.div(sp.Poly(num, a, b), sp.Poly(F, a, b))
    return r.is_zero and q.is_monomial


def symmetry_group(F, a=g, b=h):
    """The sign-and-inversion maps (other than the identity) fixing the curve F = 0."""
    out = []
    for name, (e1, s1, e2, s2) in MAPS.items():
        if is_symmetry(F, a, b, {a: e1 * (a if s1 == 1 else 1 / a), b: e2 * (b if s2 == 1 else 1 / b)}):
            out.append(name)
    return sorted(out)


def repeated_factor(res, v1, v2, mult):
    fl = sp.factor_list(sp.expand(res))
    reps = [f for f, m in fl[1] if m >= mult and (sp.Poly(f, v1, v2).degree(v1) >= 1 or sp.Poly(f, v1, v2).degree(v2) >= 1)]
    if len(reps) != 1:
        return None
    return sp.expand(reps[0])


def rational_roots(expr, var):
    """The rational roots of a univariate polynomial expression (exact)."""
    P = sp.Poly(sp.expand(expr), var)
    if P.degree() <= 0:
        return []
    out = []
    for r, m in sp.roots(P, filter="Q").items():
        if r.is_rational:
            out.append(sp.Rational(r))
    # sp.roots may miss rational roots of high degree; the factor list is exact
    for f, m in sp.factor_list(P.as_expr())[1]:
        Pf = sp.Poly(f, var)
        if Pf.degree() == 1:
            c1, c0 = Pf.all_coeffs()
            out.append(sp.Rational(-c0, c1))
    return sorted(set(out))


# ------------------------------------------------------------------ the steps

def step_joint(F, a, b, X, Y):
    """X = a^2, Y = a b.  F must be invariant up to sign under (a, b) -> (-a, -b)."""
    P = sp.Poly(F, a, b)
    pars = {(i + j) % 2 for (i, j), c in P.terms()}
    if len(pars) != 1:
        return None
    G = F
    if pars == {1}:
        G = sp.expand(F * a)
    P = sp.Poly(G, a, b)
    shift = max(0, max((j - i) // 2 for (i, j), c in P.terms()))
    Q = 0
    for (i, j), c in P.terms():
        Q += c * (X ** ((i - j) // 2 + shift) * Y ** j if i >= j else Y ** j * X ** (shift - (j - i) // 2))
    Q = sp.expand(Q)
    assert sp.expand(Q.subs({X: a ** 2, Y: a * b}, simultaneous=True) - G * a ** (2 * shift)) == 0
    return Q, {"kind": "joint", "old": (a, b), "new": (X, Y), "relations": [a ** 2 - X, a * b - Y]}


def step_inversion(F, a, b, s, U):
    """U = a + s/a.  F must be invariant under a -> s/a."""
    if not is_symmetry(F, a, b, {a: s / a}):
        return None
    res = sp.resultant(F, a ** 2 - U * a + s, a)
    Q = repeated_factor(res, U, b, 2)
    if Q is None:
        return None
    return Q, {"kind": "inversion", "old": (a, b), "new": (U, b), "relations": [a ** 2 - U * a + s], "s": s}


def step_double_inversion(F, a, b, s1, s2, U, V):
    """U = a + s1/a, V = b + s2/b.  The fiber is 4 if both single inversions are symmetries, 2 if only the diagonal is."""
    both = is_symmetry(F, a, b, {a: s1 / a}) and is_symmetry(F, a, b, {b: s2 / b})
    diag = is_symmetry(F, a, b, {a: s1 / a, b: s2 / b})
    if not diag:
        return None
    res = sp.resultant(sp.resultant(F, a ** 2 - U * a + s1, a), b ** 2 - V * b + s2, b)
    Q = repeated_factor(res, U, V, 4 if both else 2)
    if Q is None:
        return None
    return Q, {"kind": "double_inversion", "old": (a, b), "new": (U, V), "relations": [a ** 2 - U * a + s1, b ** 2 - V * b + s2], "fiber": 4 if both else 2}


CHANGES = [("a", "b"), ("1/a", "b"), ("a", "1/b"), ("1/a", "1/b"), ("a", "b/a"), ("1/a", "b/a"), ("a", "a*b"), ("b", "a/b"), ("1/b", "a/b")]


def coordinate_changes(F, a, b, a2, b2):
    """Monomial changes of coordinates (a2, b2) = (m1(a, b), m2(a, b)) with their step records and the transformed polynomial."""
    out = []
    exprs = {"a": a, "1/a": 1 / a, "b": b, "1/b": 1 / b, "b/a": b / a, "a/b": a / b, "a*b": a * b}
    for ea, eb in CHANGES:
        if (ea, eb) == ("a", "b"):
            out.append((F, None))
            continue
        m1, m2 = exprs[ea], exprs[eb]
        sol = sp.solve([sp.Eq(a2, m1), sp.Eq(b2, m2)], [a, b], dict=True)
        if len(sol) != 1:
            continue
        G = sp.expand(sp.fraction(sp.together(F.subs(sol[0], simultaneous=True)))[0])
        if G == 0:
            continue
        out.append((G, {"kind": "change", "old": (a, b), "new": (a2, b2), "relations": [sp.numer(sp.together(a2 - m1)), sp.numer(sp.together(b2 - m2))], "a2": ea, "b2": eb, "sol": sol[0]}))
    return out


def hyperelliptic_model(F, a, b):
    """If F is quadratic in a or in b: (q, o, A, B, C, core, S) with y^2 = D(o) = S(o)^2 core(o), q = (-B +- y)/(2A)."""
    for q, o in ((a, b), (b, a)):
        P = sp.Poly(F, q)
        if P.degree() == 2:
            A, B, C = P.all_coeffs()
            D = sp.expand(B ** 2 - 4 * A * C)
            if D == 0:
                continue
            fl = sp.factor_list(sp.Poly(D, o))
            core, S = sp.Integer(fl[0]), sp.Integer(1)
            # move the square part of the constant too
            c = sp.Integer(fl[0])
            sq = 1
            for p_, e_ in sp.factorint(abs(c)).items():
                sq *= p_ ** (2 * (e_ // 2))
            core, S = sp.Integer(c // sq), sp.Integer(sp.sqrt(sq))
            for f, m in fl[1]:
                core *= f.as_expr() ** (m % 2)
                S *= f.as_expr() ** (m // 2)
            core = sp.expand(core)
            return {"q": q, "o": o, "A": A, "B": B, "C": C, "core": core, "S": sp.expand(S), "degree": sp.Poly(core, o).degree(),
                    "coeffs": [int(v) for v in sp.Poly(core, o).all_coeffs()] if all(sp.Rational(v).is_integer for v in sp.Poly(core, o).all_coeffs()) else None}
    return None


def genus_of_model(deg):
    return (deg - 1) // 2


def classical_quotients(core, o):
    """One level of the classical tower on y^2 = core(o): the even quotient z = o^2 and the twisted reciprocal
    quotients w = o + kappa/o, each as (name, polynomial in z or w, step record)."""
    z, w = sp.symbols("z w")
    out = []
    P = sp.Poly(core, o)
    if all(k % 2 == 0 for (k,), c in P.terms()):
        Qz = sp.expand(sum(c * z ** (k // 2) for (k,), c in P.terms()))
        out.append(("even", Qz, z, {"kind": "even", "old": (o, yy), "new": (z, yy), "relations": [o ** 2 - z]}))
    d = P.degree()
    if d % 4 == 0:
        for kappa in twisted_kappas(core, o):
            Pw = reciprocal_quotient(core, o, w, kappa)
            if Pw is not None:
                # core(o) = o^{d/2} Pw(w): y = o^{d/4} Y
                Y2 = sp.Symbol("Y2")
                out.append(("reciprocal", Pw, w, {"kind": "reciprocal", "old": (o, yy), "new": (w, Y2), "relations": [o ** 2 - w * o + kappa, yy - o ** (d // 4) * Y2], "kappa": kappa}))
    return out


# ------------------------------------------------------------------ endpoints

def elliptic_endpoint(coeffs):
    """PARI: rank bounds, torsion, the small points and whether they are all of them (rank 0 and the count equals the torsion)."""
    if coeffs is None or not gp_available():
        return None
    r = quartic_points(coeffs, H=3000)
    if "error" in r:
        return {"error": r["error"]}
    return {"rank_lo": r["rank_lo"], "rank_hi": r["rank_hi"], "torsion_order": r["torsion_order"], "points": r["points"], "n_inf": r["n_inf"], "complete": r["complete"]}


def match_known_genus2(core, o):
    """Is y^2 = core(o) one of the known genus-2 curves up to o = lam x or o = lam / x and a square scaling of y?
    Returns (name, transform, points in the (o, y) coordinates) or None."""
    P = sp.Poly(core, o)
    d = P.degree()
    x = sp.Symbol("xx")
    for name, (kc, kpts, src) in KNOWN_GENUS2.items():
        K = sum(c * x ** (len(kc) - 1 - i) for i, c in enumerate(kc))
        for lam in LAMBDAS:
            for kind in ("scale", "reciprocal"):
                # o = lam x  (scale)  or  o = lam / x  (reciprocal): core(o(x)) * (x^d if reciprocal) should be c * K(x)
                if kind == "scale":
                    T = sp.expand(core.subs(o, lam * x))
                else:
                    T = sp.expand(sp.cancel(core.subs(o, lam / x) * x ** (6 if len(kc) == 7 else 6)))
                Tp = sp.Poly(T, x)
                Kp = sp.Poly(K, x)
                if Tp.degree() != Kp.degree() and not (kind == "reciprocal"):
                    continue
                q, r = sp.div(Tp, Kp)
                if not r.is_zero or not q.is_ground:
                    continue
                c = sp.Rational(q.as_expr())
                if c == 0 or not sp.sqrt(c).is_rational:
                    continue
                # transform the known points (x, y) -> (o, y * sqrt(c) [* x^3 for reciprocal])
                pts = []
                for (px, py) in kpts:
                    px, py = sp.Rational(px), sp.Rational(py)
                    if kind == "scale":
                        pts.append((lam * px, py * sp.sqrt(c)))
                    else:
                        if px == 0:
                            continue          # o = infinity: degenerate
                        pts.append((lam / px, py * sp.sqrt(c) / px ** 3))
                return {"name": name, "kind": kind, "lambda": str(lam), "c": str(c), "points": [(str(a), str(b)) for a, b in pts], "source": src}
    return None


# ------------------------------------------------------------------ lifting

def lift_point(steps, curves, point):
    """Lift a rational point of the last curve back through the steps (last to first) to pairs (g, h).
    curves[i] is the curve before steps[i] (a polynomial in that level's variables; hyperelliptic levels are yy^2 - core);
    point is a dict {variable: rational value} on the last curve.  Each step's relations are solved one unknown at a time
    (linear or quadratic in that unknown, exactly); an old variable left free by the relations is taken from the rational
    roots of the curve before the step.  Only finite values are lifted: a point at infinity of any level forces a frame
    ratio in {0, oo}."""
    frontier = [dict(point)]
    for step, F_before in zip(reversed(steps), reversed(curves[:len(steps)])):
        nxt = []
        old = list(step["old"])
        for pt in frontier:
            if step["kind"] == "change":
                a, b = old
                vals = {step["new"][0]: pt[step["new"][0]], step["new"][1]: pt[step["new"][1]]}
                try:
                    cand = {a: sp.Rational(sp.simplify(step["sol"][a].subs(vals))), b: sp.Rational(sp.simplify(step["sol"][b].subs(vals)))}
                except Exception:
                    continue
                if yy in pt:
                    cand[yy] = pt[yy]
                nxt.append(cand)
                continue
            partials = [dict((k, v) for k, v in pt.items() if k not in old)]
            rels = list(step.get("relations", []))
            progress = True
            while rels and progress:
                progress = False
                for r in list(rels):
                    new_partials = []
                    handled = False
                    for sd in partials:
                        r_sub = sp.expand(r.subs(sd))
                        unknowns = [v for v in old if r_sub.has(v)]
                        if len(unknowns) == 0:
                            if r_sub == 0:
                                new_partials.append(sd)
                            handled = True
                        elif len(unknowns) == 1:
                            var = unknowns[0]
                            for rv in rational_roots(r_sub, var):
                                new_partials.append({**sd, var: rv})
                            handled = True
                        else:
                            new_partials.append(sd)
                    if handled:
                        partials = new_partials
                        rels.remove(r)
                        progress = True
            for sd in partials:
                free = [v for v in old if v not in sd]
                if len(free) == 1 and F_before is not None:
                    v = free[0]
                    Fv = sp.expand(F_before.subs({k: val for k, val in sd.items() if k != yy or True}))
                    for rv in rational_roots(Fv, v) if Fv.has(v) else []:
                        nxt.append({**sd, v: rv})
                elif not free:
                    nxt.append(sd)
        # keep only the points on the curve before the step
        kept = []
        for p_ in nxt:
            if F_before is None:
                kept.append(p_)
            else:
                val = sp.expand(F_before.subs({k: v for k, v in p_.items()}))
                if val == 0 or (val.free_symbols and all(str(sym) == "yy" for sym in val.free_symbols)):
                    kept.append(p_)
        frontier = kept
    out = []
    for p_ in frontier:
        if g in p_ and h in p_:
            out.append((p_[g], p_[h]))
    return out


def admissible(gh):
    gv, hv = gh
    return (not degenerate(gv)) and (not degenerate(hv)) and is_frame_ratio(gv) and is_frame_ratio(hv)


# ------------------------------------------------------------------ routes

def analyse(phi, want_all=False):
    """Try the routes on Phi(g, h); return the first killing route (endpoint complete, no admissible lift) and the summary."""
    X, Y, U, V, x2, y2 = sp.symbols("X Y U V x2 y2")
    syms = symmetry_group(phi)
    summary = {"group_order": len(syms) + 1, "symmetries": [list(s) for s in syms], "routes": []}
    routes = []
    # route builders: each returns (steps, curves, endpoint variables)
    def with_hyperelliptic(steps, curves, a, b, label):
        F = curves[-1]
        a2, b2 = sp.symbols(str(a) + "c " + str(b) + "c")
        for G, chg in coordinate_changes(F, a, b, a2, b2):
            va, vb = (a, b) if chg is None else (a2, b2)
            hm = hyperelliptic_model(G, va, vb)
            if hm is None:
                continue
            # the hyperelliptic step: (q, o) -> (o, yy) with yy = S(o) y' ... we lift from the CORE model y'^2 = core(o):
            # yy_h = 2 A q + B = S(o) y', so q = (-B + S y')/(2A); relation in the old variables q, o given (o, Y'):
            st = dict(hm, kind="hyperelliptic", old=(hm["q"], hm["o"]), new=(hm["o"], yy),
                      relations=[2 * hm["A"] * hm["q"] + hm["B"] - hm["S"] * yy])
            after = yy ** 2 - hm["core"]
            if chg is None:
                routes.append((label, steps + [st], curves + [after], hm))
            else:
                routes.append((label + " -> (" + chg["a2"] + ", " + chg["b2"] + ")", steps + [chg, st], curves + [G, after], hm))
            return
    # R1: joint
    j = step_joint(phi, g, h, X, Y)
    if j:
        Q, st = j
        with_hyperelliptic([st], [phi, Q], X, Y, "joint")
        # R2: joint then double inversion on (X, Y)
        for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            dd = step_double_inversion(Q, X, Y, s1, s2, U, V)
            if dd:
                Q2, st2 = dd
                with_hyperelliptic([st, st2], [phi, Q, Q2], U, V, f"joint -> double inversion ({s1},{s2})")
                jj = step_joint(Q2, U, V, x2, y2)
                if jj:
                    Q3, st3 = jj
                    with_hyperelliptic([st, st2, st3], [phi, Q, Q2, Q3], x2, y2, f"joint -> double inversion ({s1},{s2}) -> joint")
    # R3: single inversions of g or h
    for a, b, lab in ((g, h, "g"), (h, g, "h")):
        for s in (-1, 1):
            si = step_inversion(phi, a, b, s, U)
            if si:
                Q, st = si
                with_hyperelliptic([st], [phi, Q], U, b, f"inversion {lab} (s={s})")
                jj = step_joint(Q, U, b, x2, y2)
                if jj:
                    Q3, st3 = jj
                    with_hyperelliptic([st, st3], [phi, Q, Q3], x2, y2, f"inversion {lab} (s={s}) -> joint")
    # R4: double inversion on (g, h)
    for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        dd = step_double_inversion(phi, g, h, s1, s2, U, V)
        if dd:
            Q2, st2 = dd
            with_hyperelliptic([st2], [phi, Q2], U, V, f"double inversion ({s1},{s2})")
            jj = step_joint(Q2, U, V, x2, y2)
            if jj:
                Q3, st3 = jj
                with_hyperelliptic([st2, st3], [phi, Q2, Q3], x2, y2, f"double inversion ({s1},{s2}) -> joint")
    kill = None
    for label, steps, curves, hm in routes:
        rec = {"route": label, "model_degree": hm["degree"], "genus": genus_of_model(hm["degree"]), "core": str(hm["core"])}
        endpoints = [(label, steps, curves, hm["core"], hm["o"], yy)]
        # the classical quotients of the model (one level) as further endpoints
        for name, Pq, var, stc in classical_quotients(hm["core"], hm["o"]):
            yvar = stc["new"][1]
            endpoints.append((label + " -> " + name, steps + [stc], curves + [yvar ** 2 - Pq], Pq, var, yvar))
        for elabel, esteps, ecurves, core, var, yvar in endpoints:
            deg = sp.Poly(core, var).degree()
            e = {"endpoint": elabel, "degree": deg}
            if deg in (3, 4):
                coeffs = [int(c) for c in sp.Poly(core, var).all_coeffs()] if all(sp.Rational(c).is_integer for c in sp.Poly(core, var).all_coeffs()) else None
                if coeffs is None:
                    cont = sp.lcm([sp.Rational(c).q for c in sp.Poly(core, var).all_coeffs()])
                    coeffs = [int(c * cont ** 2) for c in sp.Poly(core, var).all_coeffs()] if sp.sqrt(cont ** 2).is_rational else None
                ed = elliptic_endpoint(coeffs)
                e["elliptic"] = ed
                if ed and ed.get("complete"):
                    pts = [(sp.Rational(a), sp.Rational(b)) for a, b in ed["points"]]
                    lifts = []
                    for (ov, yv) in pts:
                        lifts += lift_point(esteps, ecurves, {var: ov, yvar: yv})
                    e["lifts"] = [(str(a), str(b)) for a, b in lifts]
                    e["admissible"] = [(str(a), str(b)) for a, b in lifts if admissible((a, b))]
                    if not e["admissible"]:
                        kill = dict(rec, **e)
            elif deg in (5, 6):
                km = match_known_genus2(core, var)
                e["known"] = km
                if km:
                    pts = [(sp.Rational(a), sp.Rational(b)) for a, b in km["points"]]
                    lifts = []
                    for (ov, yv) in pts:
                        lifts += lift_point(esteps, ecurves, {var: ov, yvar: yv})
                    e["lifts"] = [(str(a), str(b)) for a, b in lifts]
                    e["admissible"] = [(str(a), str(b)) for a, b in lifts if admissible((a, b))]
                    if not e["admissible"]:
                        kill = dict(rec, **e)
            rec.setdefault("endpoints", []).append({k: v for k, v in e.items()})
            if kill and not want_all:
                break
        summary["routes"].append(rec)
        if kill and not want_all:
            break
    summary["kill"] = kill
    return summary
