"""THE omega = 3 ENGINE (entry 97): the (1,1,1) box's quadruples as curves.

Split part p q r (three first-power split primes) with frames l = pi^2 = c1 +
i s1, w = rho^2 = c2 + i s2, v = sigma^2 = c3 + i s3.  An element of D(m) has a
label (j,k,l) in {-1,0,1}^3 minus 0 (mod global sign -- a label and its
negative are the same element with Im negated), and equals
    E = (c1^2+s1^2)^(1-|j|) (c2^2+s2^2)^(1-|k|) (c3^2+s3^2)^(1-|l|) Im(l^{2j} w^{2k} v^{2l})
(negative exponent = conjugate; the common factor R^2 of the non-split part
cancels); every E is a (2,2,2)-form.  A quadruple d_A + d_B = d_C, d_A - d_B =
d_D with d_X = eps_X E_X gives two relations on ONE frame:
    R1 = eA E_A + eB E_B - eC E_C = 0,    R2 = eA E_A - eB E_B - eD E_D = 0.
Eliminating frame f: Res_{s_f}(R1, R2) = (monomial) * Phi_f, Phi_f a
bihomogeneous form in the two other frames, i.e. the PLANE CURVE
Phi_f(t_g, t_h) = 0 in the frame ratios t = s/c -- which depends only on the
pattern, NOT on the primes.  A frame is a point with t = 2 tau/(1 - tau^2),
tau = b/a rational (pi = a + bi), of three DISTINCT primes.

THE DECISION (sound kills only):
  * Res = 0 is necessary, so some irreducible factor vanishes at the frame.
    Monomials never (c, s != 0); a univariate factor only at a rational root
    that is a frame ratio (|t| = n/m, m^2 + n^2 a square); the four factors
    t_g = +-t_h, t_g t_h = +-1 force the same prime (unique factorization in
    Z[i]) -- dead.  What remains are genuine curve components.
  * A component quadratic in one variable: a rational point needs the
    discriminant (a polynomial in the other ratio t) to be a rational square,
    i.e. a rational point on y^2 = disc(t) -- on its squarefree model, or a
    root of the square part.  Genus 1: PARI rank 0 + a complete enumeration
    (pari_genus1) gives ALL rational t; if none is a non-degenerate frame ratio
    (t not in {0, +-1, inf}) the component is DEAD.  Genus >= 2: finitely many
    rational points (Faltings) -- 'finite', not yet effective.
  * Otherwise the PYTHAGOREAN PULLBACK t = 2 tau/(1 - tau^2) in both
    variables: Psi(tau_g, tau_h) = 0 is the curve of Pythagorean frame pairs
    (composite norms allowed).  Its factors are decided the same way (a
    rational tau must avoid {0, +-1, inf}); a genus-0 factor is an INFINITE
    Pythagorean family (the primality of the norms is then the only obstruction).
Frame verdict = worst component; class verdict = best frame.  Order:
dead < finite < candidate < infinite < unknown.
"""
from __future__ import annotations
import itertools
import sympy as sp

from compute.pari_genus1 import quartic_points, gp_available

c1, s1, c2, s2, c3, s3 = sp.symbols("c1 s1 c2 s2 c3 s3", real=True)
FR = [(c1, s1), (c2, s2), (c3, s3)]
tg, th = sp.symbols("tg th")
ug, uh = sp.symbols("ug uh")
ORDER = {"dead": 0, "finite": 1, "candidate": 2, "infinite": 3, "unknown": 4}


def elem(lab):
    R, I = sp.Integer(1), sp.Integer(0)
    W = sp.Integer(1)
    for (c, s), e in zip(FR, lab):
        z = sp.expand((c + sp.I * s) ** (2 * abs(e)))
        r, i = z.as_real_imag()
        if e < 0:
            i = -i
        R, I = sp.expand(R * r - I * i), sp.expand(R * i + I * r)
        W *= (c ** 2 + s ** 2) ** (1 - abs(e))
    return sp.expand(W * I)


LABELS = [lab for lab in itertools.product((-1, 0, 1), repeat=3)
          if lab != (0, 0, 0) and next(x for x in lab if x != 0) > 0]
E = {lab: elem(lab) for lab in LABELS}
GROUP = [(perm, conj) for perm in itertools.permutations(range(3))
         for conj in itertools.product((1, -1), repeat=3)]


def canon_lab(lab, eps):
    fn = next(x for x in lab if x != 0)
    if fn < 0:
        return tuple(-x for x in lab), -eps
    return tuple(lab), eps


def act(g, lab, eps):
    perm, conj = g
    return canon_lab(tuple(conj[i] * lab[perm[i]] for i in range(3)), eps)


def canon_cand(cand):
    """cand = ((A,eA),(B,eB),(C,eC),(D,eD)); min over the frame group (S3 x
    conjugations), the global sign, and the A<->B swap (which flips eD)."""
    best = None
    for g in GROUP:
        (A, eA), (B, eB), (C, eC), (D, eD) = [act(g, lab, e) for lab, e in cand]
        for swap in (False, True):
            a, ea, b, eb, ed = (A, eA, B, eB, eD) if not swap else (B, eB, A, eA, -eD)
            key = (a, b, C, D, ea, eb, eC, ed)
            if ea < 0:
                key = (a, b, C, D, -ea, -eb, -eC, -ed)
            if best is None or key < best:
                best = key
    return best


def all_candidates():
    """The quadruple candidate classes of the (1,1,1) box (2944)."""
    seen = set()
    for A, B in itertools.combinations(LABELS, 2):
        rest = [x for x in LABELS if x not in (A, B)]
        for C, D in itertools.permutations(rest, 2):
            for eB, eC, eD in itertools.product((1, -1), repeat=3):
                seen.add(canon_cand(((A, 1), (B, eB), (C, eC), (D, eD))))
    return sorted(seen)


def is_frame_ratio(r):
    r = sp.nsimplify(r)
    if not r.is_rational or r == 0:
        return False
    m, n = abs(int(r.p)), abs(int(r.q))
    return bool(sp.integer_nthroot(m * m + n * n, 2)[1])


def degenerate(v):
    return v in (0, 1, -1)


SAME = [sp.expand(x) for x in (tg - th, tg + th, tg * th - 1, tg * th + 1, th - tg, -tg - th, 1 - tg * th, -1 - tg * th)]


def relations(cand):
    A, B, C, D, eA, eB, eC, eD = cand
    A, B, C, D = tuple(A), tuple(B), tuple(C), tuple(D)
    return (sp.expand(eA * E[A] + eB * E[B] - eC * E[C]), sp.expand(eA * E[A] - eB * E[B] - eD * E[D]))


def frame_factors(cand, f):
    """Eliminate frame f.  Returns None (degenerate: no s_f dependence or Res = 0)
    or (curves, live_univariate): curves = [(phi, dg, dh)] the genuine curve
    components of Res in (tg, th); live_univariate = frame-ratio roots of linear
    univariate factors (candidates).  Monomials, univariate factors without a
    frame-ratio root and the same-prime factors are dropped (dead)."""
    R1, R2 = relations(cand)
    cf, sf = FR[f]
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh) = FR[g], FR[h]
    P1, P2 = sp.Poly(R1, sf), sp.Poly(R2, sf)
    if R1 == 0 or R2 == 0 or P1.degree() < 1 or P2.degree() < 1:
        return None
    Res = sp.expand(sp.resultant(P1, P2))
    if Res == 0:
        return None
    curves, live = [], []
    for fac, mult in sp.factor_list(Res)[1]:
        fe = sp.expand(fac)
        if len(sp.Add.make_args(fe)) == 1:
            continue
        phi = sp.expand(fe.subs({sg: tg * cg, sh: th * ch}))
        phi = sp.expand(sp.Mul(*[q ** m2 for q, m2 in sp.factor_list(phi)[1] if q.free_symbols & {tg, th}]))
        if phi == 0 or not (phi.free_symbols & {tg, th}):
            continue
        Pg = sp.Poly(phi, tg, th)
        dg, dh = Pg.degree(tg), Pg.degree(th)
        if dg == 0 or dh == 0:
            if max(dg, dh) == 1:                        # irreducible: a rational root only if linear
                var = tg if dh == 0 else th
                cs = sp.Poly(phi, var).all_coeffs()
                r = sp.Rational(-cs[1], cs[0])
                if is_frame_ratio(r):
                    live.append(str(r))
            continue
        if phi in SAME:
            continue
        curves.append((phi, dg, dh))
    return curves, live


_cache = {}


def gp_model(poly, var):
    P = sp.Poly(poly, var)
    cs = [int(c) for c in P.all_coeffs()]
    g = 0
    for c in cs:
        g = sp.igcd(g, c)
    cs = [c // g for c in cs] if g else cs
    key = tuple(cs)
    if key not in _cache:
        _cache[key] = quartic_points(cs) if len(cs) in (4, 5) else {"error": f"degree {len(cs)-1}"}
    return key, _cache[key]


def square_part_roots(dfl, var):
    roots = []
    for q, m2 in dfl[1]:
        if m2 % 2 == 0 and q.free_symbols and sp.Poly(q, var).degree() == 1:
            cs = sp.Poly(q, var).all_coeffs()
            roots.append(sp.Rational(-cs[1], cs[0]))
    return roots


def decide_model(poly, var, level, extra=()):
    key, r = gp_model(poly, var)
    if "error" in r:
        return "unknown", {"model": key, "error": r["error"]}
    if r["rank_hi"] > 0:
        return "infinite", {"model": key, "rank": (r["rank_lo"], r["rank_hi"])}
    if not r["complete"]:
        return "unknown", {"model": key, "note": "rank 0 but points not fully enumerated"}
    vals = [sp.Rational(t) for t in r["tvals"]] + list(extra)
    if level == "t":
        live = [str(v) for v in vals if not degenerate(v) and is_frame_ratio(v)]
    else:
        live = [str(v) for v in vals if not degenerate(v)]
    if not live:
        return "dead", {"model": key, "rank": 0, "tors": r["torsion_order"], "points": r["tvals"]}
    return "candidate", {"model": key, "rank": 0, "candidates": live}


def _disc_model(poly, var, oth):
    """(sqf, dfl, genus) for the discriminant of poly (quadratic in var) as a
    polynomial in oth; None if the discriminant vanishes identically."""
    Q = sp.Poly(poly, var)
    a2, a1, a0 = Q.all_coeffs()
    disc = sp.expand(a1 ** 2 - 4 * a2 * a0)
    if disc == 0:
        return None
    dfl = sp.factor_list(disc)
    sqf = sp.expand(sp.Mul(*[q for q, m2 in dfl[1] if m2 % 2 == 1]))
    dd = sp.Poly(sqf, oth).degree() if sqf.free_symbols else 0
    return sqf, dfl, ((dd - 1) // 2 if dd >= 1 else 0)


def decide_component(phi, dg, dh, pullback_max_degree=6):
    info = {"deg": (dg, dh)}
    for var, oth, dv in ((th, tg, dh), (tg, th, dg)):
        if dv == 2:
            dm = _disc_model(phi, var, oth)
            if dm is None:
                break
            sqf, dfl, genus = dm
            info["phi_model_genus"] = genus
            if genus == 1:
                v, inf = decide_model(sqf, oth, "t", square_part_roots(dfl, oth))
                info["phi_model"] = inf
                if v in ("dead", "finite", "candidate"):
                    return v, info
            elif genus >= 2:
                info["phi_model"] = {"genus": genus}
                return "finite", info
            break
    if dg + dh > pullback_max_degree:
        return "unknown", dict(info, note="high degree, no pullback")
    psi = sp.expand(phi.subs({tg: 2 * ug / (1 - ug ** 2), th: 2 * uh / (1 - uh ** 2)})
                    * (1 - ug ** 2) ** dg * (1 - uh ** 2) ** dh)
    psi = sp.expand(sp.cancel(psi))
    worst, facs = "dead", []
    for fac, mult in sp.factor_list(psi)[1]:
        fe = sp.expand(fac)
        if not fe.free_symbols:
            continue
        P = sp.Poly(fe, ug, uh)
        eg, eh = P.degree(ug), P.degree(uh)
        if eg == 0 or eh == 0:
            var = ug if eh == 0 else uh
            if max(eg, eh) == 1:
                cs = sp.Poly(fe, var).all_coeffs()
                root = sp.Rational(-cs[1], cs[0])
                v = "dead" if degenerate(root) else "candidate"
                facs.append({"kind": "univariate", "root": str(root), "verdict": v})
            else:
                v = "dead"
                facs.append({"kind": "univariate", "deg": max(eg, eh), "verdict": v})
        else:
            v, finf = "unknown", {"deg": (eg, eh)}
            done = False
            for var, oth, dv in ((uh, ug, eh), (ug, uh, eg)):
                if dv == 2:
                    dm = _disc_model(fe, var, oth)
                    if dm is None:
                        v, finf = "infinite", dict(finf, note="disc 0")
                    else:
                        sqf, dfl, genus = dm
                        finf["genus"] = genus
                        if genus == 0:
                            v = "infinite"
                        elif genus == 1:
                            v, minf = decide_model(sqf, oth, "tau", square_part_roots(dfl, oth))
                            finf["model"] = minf
                        else:
                            v = "finite"
                    done = True
                    break
            if not done:
                v = "finite" if (eg - 1) * (eh - 1) >= 2 else "unknown"
                finf["arith_genus"] = (eg - 1) * (eh - 1)
            facs.append(dict(finf, kind="curve", verdict=v))
        if ORDER[v] > ORDER[worst]:
            worst = v
    info["pullback"] = facs
    return worst, info


def decide_frame(cand, f):
    ff = frame_factors(cand, f)
    if ff is None:
        return {"verdict": "degenerate"}
    curves, live_uni = ff
    worst, details = ("candidate" if live_uni else "dead"), []
    for phi, dg, dh in curves:
        v, info = decide_component(phi, dg, dh)
        details.append(dict(info, verdict=v, phi=str(phi)[:80]))
        if ORDER[v] > ORDER[worst]:
            worst = v
    return {"verdict": worst, "components": details, "live_univariate": live_uni}


def decide_class(cand):
    """Best frame verdict for a candidate class, with the per-frame records."""
    frames = {f: decide_frame(cand, f) for f in range(3)}
    vs = [fr["verdict"] for fr in frames.values() if fr["verdict"] != "degenerate"]
    best = min(vs, key=lambda v: ORDER[v]) if vs else "degenerate"
    return best, frames
