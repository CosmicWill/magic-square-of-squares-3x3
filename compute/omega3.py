"""THE omega = 3 ENGINE (entries 97-98): the (1,1,1) box's quadruples as curves.

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
    rational tau must avoid {0, +-1, inf}); a GENUS-0 factor is parametrized
    (entry 98) and decided by:
      - THE MONOMIAL LEMMA: with w = (1 + i tau)/(1 - i tau) = pi/pibar the
        prime's own circle point, w_g^a = eps w_h^b (a >= 1, b != 0, eps a
        unit) is impossible for distinct primes: pi_g^a pibar_h^b = eps
        pibar_g^a pi_h^b makes the prime pi_g divide pibar_g^a pi_h^b (b > 0)
        or pibar_g^a pibar_h^|b| (b < 0), so pi_g ~ pibar_g (p = 2) or
        pi_g ~ pi_h / pibar_h (p = q).  A family satisfying such a relation
        identically is DEAD;
      - THE THIRD-FRAME LIFT otherwise: substitute the family into R1, R2, take
        the common root t_f (gcd), and impose 1 + t_f^2 = square -- a curve in
        the family parameter, decided by its genus (PARI for genus 1).
    Rational points the parametrization can miss (roots of the square part of
    the discriminant, of the leading coefficient, a base point with y0 = 0)
    are kept as CANDIDATES unless degenerate.
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
lam, T = sp.symbols("lam T")
ORDER = {"dead": 0, "finite": 1, "candidate": 2, "infinite": 3, "unknown": 4}


def elem_box(lab, exps):
    """Element of D(m) for split part p^a q^b r^c (exps = (a, b, c)) with label
    (j, k, l), |j| <= a etc.: the (2a, 2b, 2c)-form
    (c1^2+s1^2)^(a-|j|) (c2^2+s2^2)^(b-|k|) (c3^2+s3^2)^(c-|l|) Im(l^{2j} w^{2k} v^{2l})."""
    R, I = sp.Integer(1), sp.Integer(0)
    W = sp.Integer(1)
    for (c, s), e, a in zip(FR, lab, exps):
        z = sp.expand((c + sp.I * s) ** (2 * abs(e)))
        r, i = z.as_real_imag()
        if e < 0:
            i = -i
        R, I = sp.expand(R * r - I * i), sp.expand(R * i + I * r)
        W *= (c ** 2 + s ** 2) ** (a - abs(e))
    return sp.expand(W * I)


def elem(lab):
    return elem_box(lab, (1, 1, 1))


def _build_box(exps):
    labs = [lab for lab in itertools.product(*[range(-a, a + 1) for a in exps])
            if any(lab) and next(x for x in lab if x != 0) > 0]
    Ebox = {lab: elem_box(lab, exps) for lab in labs}
    perms = [p for p in itertools.permutations(range(3)) if all(exps[p[i]] == exps[i] for i in range(3))]
    G = [(perm, conj) for perm in perms for conj in itertools.product((1, -1), repeat=3)]
    return labs, Ebox, G


BOX = (1, 1, 1)
LABELS, E, GROUP = _build_box(BOX)


def set_box(exps):
    """Switch the engine to the box p^a q^b r^c: rebuilds the elements, the labels
    and the symmetry group (conjugations x permutations of frames with EQUAL
    exponents).  The (1,1,1) box is the default."""
    global BOX, LABELS, E, GROUP
    exps = tuple(int(x) for x in exps)
    if exps != BOX:
        BOX = exps
        LABELS, E, GROUP = _build_box(BOX)
    return BOX


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
    """The quadruple candidate classes of the current box ((1,1,1): 2944)."""
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


def pyth(tau):
    return 2 * tau / (1 - tau ** 2)


SAME = [sp.expand(x) for x in (tg - th, tg + th, tg * th - 1, tg * th + 1, th - tg, -tg - th, 1 - tg * th, -1 - tg * th)]


def relations(cand):
    A, B, C, D, eA, eB, eC, eD = cand
    A, B, C, D = tuple(A), tuple(B), tuple(C), tuple(D)
    return (sp.expand(eA * E[A] + eB * E[B] - eC * E[C]), sp.expand(eA * E[A] - eB * E[B] - eD * E[D]))


def _ratio_form(fe, g, h):
    """A polynomial in the frames g, h as a polynomial in the ratios (tg, th):
    s_g = tg c_g, s_h = th c_h, the monomial in c_g, c_h stripped."""
    (cg, sg), (ch, sh) = FR[g], FR[h]
    phi = sp.expand(fe.subs({sg: tg * cg, sh: th * ch}, simultaneous=True))
    return sp.expand(sp.Mul(*[q ** m2 for q, m2 in sp.factor_list(phi)[1] if q.free_symbols & {tg, th}]))


def classify_common_factor(fac):
    """An irreducible COMMON factor of the two relations is a condition in its
    own right, whichever frame is eliminated (R1 = R2 = 0 iff G = 0 or the
    reduced pair vanishes).  Returns (verdict, kind, frames, phi):
    'dead' for a monomial in the c's and s's (a degenerate frame), a norm
    c_f^2 + s_f^2 (never zero) or a same-prime factor in two frames
    (t_g = +-t_h, t_g t_h = +-1: the (2,+-2) monomial relation w_g^2 = eps
    w_h^2, impossible for distinct primes by the monomial lemma of entry 98);
    'curve' for any other factor in exactly two frames (phi in (tg, th) with
    (g, h) the frames, to be decided as a component); 'unknown' otherwise."""
    fe = sp.expand(fac)
    if len(sp.Add.make_args(fe)) == 1:
        return "dead", "monomial", None, None
    for cf, sf in FR:
        if sp.expand(fe - (cf ** 2 + sf ** 2)) == 0 or sp.expand(fe + (cf ** 2 + sf ** 2)) == 0:
            return "dead", "norm", None, None
    frames = [i for i, (cf, sf) in enumerate(FR) if {cf, sf} & fe.free_symbols]
    if len(frames) == 1:                        # a ONE-frame factor: a condition on one ratio (entry 108: c +- s, i.e. t = +-1)
        cf, sf = FR[frames[0]]
        q = sp.expand(fe.subs({sf: tg * cf}, simultaneous=True).subs(cf, 1))
        if not (q.free_symbols & {tg}):
            return "dead", "one-frame (c-power)", tuple(frames), q
        roots = [r for r in sp.Poly(q, tg).ground_roots() if r.is_rational]
        live = [r for r in roots if not degenerate(r) and is_frame_ratio(r)]
        if live:
            return "candidate", "one-frame root " + str(live), tuple(frames), q
        return "dead", "one-frame " + str(q), tuple(frames), q
    if len(frames) == 2:
        g, h = frames
        phi = _ratio_form(fe, g, h)
        if phi in SAME or sp.expand(-phi) in SAME:
            return "dead", "same-prime", (g, h), phi
        if phi.free_symbols & {tg, th}:
            return "curve", "curve", (g, h), phi
    mono = frame_monomial_factor(fe)
    if mono is not None:
        return "dead", "three-frame monomial " + mono, tuple(frames), fe
    return "unknown", "three-frame", tuple(frames), fe


def frame_monomial_factor(fe, emax=2):
    """Is fe (up to a constant) the real or imaginary part of a monomial
    prod_i (c_i + i s_i)^{e_i} in the frames, exponents |e_i| <= emax (negative
    = the conjugate)?  Such a factor is an ANGLE RELATION among the frames,
    sum_i e_i theta_i = 0 or 90 degrees (mod 180): in the circle group,
    prod w_i^{2 e_i} = +-1 -- a monomial relation among distinct primes,
    impossible by unique factorization in Z[i] (the monomial lemma of entry 98,
    with three frames).  Returns a description or None (entry 105)."""
    import itertools
    fe = sp.expand(fe)
    syms = fe.free_symbols
    idx = [i for i, (cf, sf) in enumerate(FR) if {cf, sf} & syms]
    if not idx:
        return None
    for exps in itertools.product([e for e in range(-emax, emax + 1) if e != 0], repeat=len(idx)):
        z = sp.Integer(1)
        for i, e in zip(idx, exps):
            cf, sf = FR[i]
            z *= (cf + sp.I * sf) ** abs(e) if e > 0 else (cf - sp.I * sf) ** abs(e)
        z = sp.expand(z)
        zb = sp.expand(z.subs(sp.I, -sp.I))
        for part, name in ((sp.expand((z + zb) / 2), "Re"), (sp.expand((z - zb) / (2 * sp.I)), "Im")):
            if part == 0:
                continue
            q = sp.cancel(fe / part)
            if q.is_number and q != 0:
                return name + "(" + " ".join(f"l{i+1}^{e}" for i, e in zip(idx, exps)) + ")"
    return None


def reduced_relations(cand):
    """(R1/G, R2/G, common): the relations with their common factor G divided
    out, and the classification of G's irreducible factors (entry 103; three
    classes of the (1,1,1) box have G depending on every frame, so every
    resultant vanished and the engine called them degenerate)."""
    R1, R2 = relations(cand)
    if R1 == 0 or R2 == 0:
        return R1, R2, []
    G = sp.gcd(R1, R2)
    if not G.free_symbols:
        return R1, R2, []
    common = [classify_common_factor(fac) for fac, _m in sp.factor_list(G)[1]]
    A = sp.expand(sp.cancel(R1 / G))
    B = sp.expand(sp.cancel(R2 / G))
    assert sp.expand(A * G - R1) == 0 and sp.expand(B * G - R2) == 0
    return A, B, common


FACTOR_BACKEND = "bivariate"         # "bivariate" (entry 104): dehomogenize, then a bivariate resultant and factorization;
                                     # "sympy": the entry-97 six-variable route; "pari": gp's factor (too slow on six variables)


def _resultant_factors_bivariate(R1, R2, cf, sf, g, h):
    """The relations are bihomogeneous in every frame, so with c_f = c_g = c_h = 1,
    s_g = t_g, s_h = t_h they become polynomials in s_f over Q[t_g, t_h]; their
    resultant is the dehomogenized resultant (the substitution is a ring map on
    the coefficients and keeps the degrees in s_f), and its irreducible factors
    are the ratio forms of the non-monomial factors of the six-variable
    resultant.  A bivariate factorization instead of a six-variable one: the
    step that took 95% of the remaining time.  Returns None when a degree in
    s_f drops (the caller falls back) or the resultant vanishes."""
    (cg, sg), (ch, sh) = FR[g], FR[h]
    sub = {cf: 1, cg: 1, ch: 1, sg: tg, sh: th}
    Q1 = sp.Poly(sp.expand(R1.subs(sub, simultaneous=True)), sf)
    Q2 = sp.Poly(sp.expand(R2.subs(sub, simultaneous=True)), sf)
    if Q1.degree() != sp.Poly(R1, sf).degree() or Q2.degree() != sp.Poly(R2, sf).degree():
        return None
    Res = sp.expand(sp.resultant(Q1, Q2))
    if Res == 0:
        return None
    return [sp.expand(fac) for fac, m in sp.factor_list(Res)[1]]


def _resultant_factors_pari(R1, R2, sf, g, h):
    """The irreducible factors of Res_{s_f}(R1, R2) as polynomials in the frame
    ratios (tg, th) of the two other frames, through gp: polresultant, factor.
    Every factor of the bihomogeneous resultant is bihomogeneous in (c_g, s_g)
    and (c_h, s_h), so its ratio form is the substitution c = 1, s = t --
    no second factorization.  Returns None when the resultant vanishes."""
    import subprocess as _sub
    from compute.pari_genus1 import GP
    (cg, sg), (ch, sh) = FR[g], FR[h]
    body = "c1; s1; c2; s2; c3; s3; tg; th;\n"
    body += "R1 = " + str(R1).replace("**", "^") + ";\nR2 = " + str(R2).replace("**", "^") + ";\n{\n"
    body += "Res = polresultant(R1, R2, %s); if(Res == 0, print(\"ZERO\"), F = factor(Res);\n" % sf
    body += "  for(i = 1, #F~, q = subst(subst(subst(subst(F[i,1], %s, tg * %s), %s, th * %s), %s, 1), %s, 1);\n" % (sg, cg, sh, ch, cg, ch)
    body += "    print(\"FAC \", q)));\n}\n"
    cp = _sub.run([GP, "-q", "-f"], input='default(parisize,"512M");\n' + body, capture_output=True, text=True, timeout=600)
    out = cp.stdout
    if "ZERO" in out:
        return None
    if "FAC" not in out and "***" in (out + cp.stderr):
        raise RuntimeError("gp resultant failed: " + (out + cp.stderr)[-300:])
    loc = {"tg": tg, "th": th, "c1": c1, "s1": s1, "c2": c2, "s2": s2, "c3": c3, "s3": s3}
    phis = []
    for line in out.splitlines():
        if line.startswith("FAC "):
            phis.append(sp.expand(sp.sympify(line[4:].strip().replace("^", "**"), locals=loc)))
    return phis


def frame_factors(cand, f):
    """Eliminate frame f.  Returns None (degenerate: no s_f dependence or Res = 0,
    or a common factor of the relations that is not decided) or (curves,
    live_univariate): curves = [(phi, dg, dh)] the genuine curve components of
    Res in (tg, th), plus any common factor of the relations that is a curve in
    the frames (g, h); live_univariate = frame-ratio roots of linear univariate
    factors (candidates).  Monomials, univariate factors without a frame-ratio
    root, the same-prime factors and the dead common factors are dropped."""
    R1, R2, common = reduced_relations(cand)
    cf, sf = FR[f]
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh) = FR[g], FR[h]
    if R1 == 0 or R2 == 0:
        return None
    extra = []
    for verdict, kind, frames, phi in common:
        if verdict == "dead":
            continue
        if verdict == "curve" and frames == (g, h):
            Pg = sp.Poly(phi, tg, th)
            extra.append((phi, Pg.degree(tg), Pg.degree(th)))
            continue
        return None
    P1, P2 = sp.Poly(R1, sf), sp.Poly(R2, sf)
    if P1.degree() < 1 or P2.degree() < 1:
        return None
    if FACTOR_BACKEND == "bivariate":
        phis = _resultant_factors_bivariate(R1, R2, cf, sf, g, h)
        if phis is None:
            Res = sp.expand(sp.resultant(P1, P2))
            if Res == 0:
                return None
            phis = []
            for fac, mult in sp.factor_list(Res)[1]:
                fe = sp.expand(fac)
                if len(sp.Add.make_args(fe)) == 1:
                    continue
                phi = sp.expand(fe.subs({sg: tg * cg, sh: th * ch}))
                phi = sp.expand(sp.Mul(*[q ** m2 for q, m2 in sp.factor_list(phi)[1] if q.free_symbols & {tg, th}]))
                phis.append(phi)
    elif FACTOR_BACKEND == "pari":
        phis = _resultant_factors_pari(R1, R2, sf, g, h)
        if phis is None:
            return None
    else:
        Res = sp.expand(sp.resultant(P1, P2))
        if Res == 0:
            return None
        phis = []
        for fac, mult in sp.factor_list(Res)[1]:
            fe = sp.expand(fac)
            if len(sp.Add.make_args(fe)) == 1:
                continue
            phi = sp.expand(fe.subs({sg: tg * cg, sh: th * ch}))
            phi = sp.expand(sp.Mul(*[q ** m2 for q, m2 in sp.factor_list(phi)[1] if q.free_symbols & {tg, th}]))
            phis.append(phi)
    curves, live = list(extra), []
    for phi in phis:
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


# ------------------------------------------------------------------ PARI models
_cache = {}


def squarefree_part(c):
    """The squarefree part of a nonzero rational, sign included: c = squarefree_part(c) * (square)."""
    c = sp.Rational(c)
    out = sp.Integer(-1) if c < 0 else sp.Integer(1)
    for pr, e in sp.factorint(abs(c.p) * c.q).items():
        if e % 2:
            out *= pr
    return out


def square_part_of_gcd(cs):
    """The largest square dividing gcd(cs) (1 if the gcd is 0)."""
    g = 0
    for c in cs:
        g = sp.igcd(g, c)
    if not g:
        return 1
    sq = 1
    for pr, e in sp.factorint(int(g)).items():
        sq *= pr ** (2 * (e // 2))
    return sq


def gp_model(poly, var):
    """The PARI model of y^2 = poly(var): the coefficients are divided only by the largest SQUARE
    dividing their gcd (entry 117: dividing by the whole gcd twisted the curve by a non-square)."""
    P = sp.Poly(poly, var)
    cs = [sp.Rational(c) for c in P.all_coeffs()]
    L = 1
    for c in cs:
        L = sp.ilcm(L, c.q)
    cs = [int(c * L * L) for c in cs]          # entry 119: denominators cleared by L^2 (a square, no twist); int() had truncated
    sq = square_part_of_gcd(cs)
    cs = [c // sq for c in cs]
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
    # entry 117: the constant's squareclass is part of the curve (disc = c * sqf * h^2, and a
    # rational root needs c * sqf to be a square): keep the squarefree part of c, sign included
    sqf = sp.expand(squarefree_part(dfl[0]) * sp.Mul(*[q for q, m2 in dfl[1] if m2 % 2 == 1]))
    dd = sp.Poly(sqf, oth).degree() if sqf.free_symbols else 0
    return sqf, dfl, ((dd - 1) // 2 if dd >= 1 else 0)


# ------------------------------------------------------------------ genus 0 (entry 98)
def sqrt_rational(C):
    C = sp.nsimplify(C)
    if not C.is_rational or C <= 0:
        return None
    p, q = sp.integer_nthroot(int(C.p), 2), sp.integer_nthroot(int(C.q), 2)
    if p[1] and q[1]:
        return sp.Rational(p[0], q[0])
    return None


def conic_point(a, b, c, bound=60):
    """A rational point (u0, y0) on y^2 = a u^2 + b u + c, by search."""
    for den in range(1, bound + 1):
        for num in range(-bound * den, bound * den + 1):
            u0 = sp.Rational(num, den)
            v = a * u0 ** 2 + b * u0 + c
            if v >= 0:
                r = sqrt_rational(v)
                if r is not None:
                    return u0, r
    return None


def _rational_roots(poly, var):
    out = []
    if poly == 0 or not poly.free_symbols:
        return out
    for q, m2 in sp.factor_list(poly)[1]:
        if q.free_symbols and sp.Poly(q, var).degree() == 1:
            cs = sp.Poly(q, var).all_coeffs()
            out.append(sp.Rational(-cs[1], cs[0]))
    return out


def parametrize(fe, var, oth):
    """Rational parametrizations of the irreducible genus-0 factor fe(ug, uh)
    (linear or quadratic in var): returns (branches, how, candidates) with
    branches = [(ug(lam), uh(lam))] and candidates = the rational points the
    branches can miss, as (oth value, var value) pairs."""
    P = sp.Poly(fe, var)
    dv = P.degree()
    cands = []
    if dv == 1:
        a1, a0 = P.all_coeffs()
        expr = sp.cancel(-a0 / a1)
        sol = {oth: lam, var: expr.subs(oth, lam)}
        return [(sol[ug], sol[uh])], "linear", cands
    if dv != 2:
        return [], f"degree {dv}", cands
    a2, a1, a0 = P.all_coeffs()
    # points where the leading coefficient vanishes: fe is linear in var there
    for r0 in _rational_roots(sp.expand(a2), oth):
        b1, b0 = sp.expand(a1).subs(oth, r0), sp.expand(a0).subs(oth, r0)
        if b1 != 0:
            cands.append((r0, sp.Rational(-b0, b1) if b0 != 0 else sp.Integer(0)))
    disc = sp.expand(a1 ** 2 - 4 * a2 * a0)
    if disc == 0:
        expr = sp.cancel(-a1 / (2 * a2))
        sol = {oth: lam, var: expr.subs(oth, lam)}
        return [(sol[ug], sol[uh])], "double root", cands
    dfl = sp.factor_list(disc)
    C = dfl[0]
    sqf, h = sp.Integer(1), sp.Integer(1)
    for q, m in dfl[1]:
        if m % 2 == 1:
            sqf *= q
        h *= q ** (m // 2)
    # square-part roots: disc = 0 there with a double rational root of the quadratic
    for r0 in _rational_roots(sp.expand(h), oth):
        aa2 = sp.expand(a2).subs(oth, r0)
        if aa2 != 0:
            cands.append((r0, sp.cancel(-sp.expand(a1).subs(oth, r0) / (2 * aa2))))
    if not sqf.free_symbols:                       # disc = C h^2
        r = sqrt_rational(C * sqf)
        if r is None:
            return [], "disc = nonsquare * square", cands
        out = []
        for sgn in (1, -1):
            expr = sp.cancel((-a1 + sgn * r * h) / (2 * a2))
            sol = {oth: lam, var: expr.subs(oth, lam)}
            out.append((sol[ug], sol[uh]))
        return out, "disc square", cands
    Q = sp.Poly(sp.expand(C * sqf), oth)
    if Q.degree() > 2:
        return [], f"disc squarefree degree {Q.degree()}", cands
    cs = Q.all_coeffs()
    while len(cs) < 3:
        cs = [0] + cs
    qa, qb, qc = cs
    if qa == 0:
        u_of, y_of = (lam ** 2 - qc) / qb, lam
    else:
        pt = conic_point(qa, qb, qc)
        if pt is None:
            return [], "conic: no rational point found", cands
        u0, y0 = pt
        if y0 == 0:                                   # vertical tangent: the base point is missed
            aa2 = sp.expand(a2).subs(oth, u0)
            if aa2 != 0:
                cands.append((u0, sp.cancel(-sp.expand(a1).subs(oth, u0) / (2 * aa2))))
        u = sp.Symbol("u_")
        eq = sp.expand(qa * u ** 2 + qb * u + qc - (y0 + lam * (u - u0)) ** 2)
        quo = sp.cancel(eq / (u - u0))
        sol = sp.solve(quo, u)
        if not sol:
            return [], "conic parametrization failed", cands
        u_of = sp.cancel(sol[0])
        y_of = sp.cancel(y0 + lam * (u_of - u0))
    out = []
    for sgn in (1, -1):
        expr = sp.cancel(sp.cancel((-a1 + sgn * y_of * h.subs(oth, u_of)) / (2 * a2)).subs(oth, u_of))
        sol = {oth: u_of, var: expr}
        out.append((sp.cancel(sol[ug]), sp.cancel(sol[uh])))
    return out, "conic", cands


def _monomial_relation_sympy(taug, tauh, amax=8):
    """The entry-98 implementation (sympy simplify on the rational functions):
    kept for cross-validation only -- it took up to 24 s per call."""
    wg = sp.cancel((1 + sp.I * taug) / (1 - sp.I * taug))
    wh = sp.cancel((1 + sp.I * tauh) / (1 - sp.I * tauh))
    for a in range(1, amax + 1):
        for b in range(-amax, amax + 1):
            if b == 0:
                continue
            r = sp.simplify(sp.cancel(sp.expand(wg ** a) / sp.expand(wh ** b)))
            if r.free_symbols:
                continue
            if sp.simplify(r ** 4) == 1:
                return (a, b, str(r))
    return None


_MONO_CACHE = {}
_UNITS = {1: "1", -1: "-1", sp.I: "I", -sp.I: "-I"}


def _gauss_parts(tau):
    """tau = P/Q (a rational function of lam) -> (Q + iP, Q - iP) as polynomials
    over Q(i); w = (1 + i tau)/(1 - i tau) = (Q + iP)/(Q - iP).  No reduction is
    needed: a common factor of P and Q multiplies both sides of the identity."""
    N, D = sp.fraction(sp.together(tau))
    P = sp.Poly(sp.expand(N), lam, domain="QQ_I")
    Q = sp.Poly(sp.expand(D), lam, domain="QQ_I")
    iP = P * sp.Poly(sp.I, lam, domain="QQ_I")
    return Q + iP, Q - iP


def monomial_relation(taug, tauh, amax=8):
    """(a, b, eps) with w_g^a = eps w_h^b identically on the family, or None
    (entry 104: an EXACT polynomial identity over Q(i) -- with w = A/B, A = Q + iP,
    B = Q - iP, the relation is A_g^a B_h^b = eps B_g^a A_h^b for b > 0 and
    A_g^a A_h^|b| = eps B_g^a B_h^|b| for b < 0; eps = the ratio of leading
    coefficients, a fourth root of unity.  Same search order as entry 98.)"""
    key = (str(taug), str(tauh), amax)
    if key in _MONO_CACHE:
        return _MONO_CACHE[key]
    res = None
    Ag, Bg = _gauss_parts(taug)
    Ah, Bh = _gauss_parts(tauh)
    if not (Ag.is_zero or Bg.is_zero or Ah.is_zero or Bh.is_zero):
        pw = {}
        def power(Pp, n):
            k = (id(Pp), n)
            if k not in pw:
                pw[k] = Pp ** n
            return pw[k]
        for a in range(1, amax + 1):
            for b in range(-amax, amax + 1):
                if b == 0:
                    continue
                if b > 0:
                    L, R = power(Ag, a) * power(Bh, b), power(Bg, a) * power(Ah, b)
                else:
                    L, R = power(Ag, a) * power(Ah, -b), power(Bg, a) * power(Bh, -b)
                if L.degree() != R.degree():
                    continue
                eps = sp.nsimplify(sp.expand(L.LC() / R.LC()))
                if eps not in _UNITS:
                    continue
                if (L - R * sp.Poly(eps, lam, domain="QQ_I")).is_zero:
                    res = (a, b, _UNITS[eps])
                    break
            if res:
                break
    _MONO_CACHE[key] = res
    return res


def lift(cand, f, taug, tauh):
    """Third frame: the common root t_f of R1, R2 on the family (frame g = tau_g,
    frame h = tau_h), and the frame condition 1 + t_f^2 = square as a curve
    in the family parameter."""
    R1, R2 = relations(cand)
    g, h = [i for i in range(3) if i != f]
    subs = {FR[g][0]: 1, FR[g][1]: pyth(taug), FR[h][0]: 1, FR[h][1]: pyth(tauh), FR[f][0]: 1, FR[f][1]: T}
    P1 = sp.expand(sp.numer(sp.together(R1.subs(subs))))
    P2 = sp.expand(sp.numer(sp.together(R2.subs(subs))))
    if P1 == 0 or P2 == 0:
        return {"status": "a relation vanishes identically on the family", "verdict": "unknown"}
    G = sp.Poly(sp.gcd(P1, P2), T)
    dT = G.degree()
    if dT < 1:
        return {"status": "no common root in T", "verdict": "dead"}
    if dT > 1:
        return {"status": f"common root of degree {dT}", "verdict": "unknown"}
    a, b = G.all_coeffs()
    tf = sp.cancel(-b / a)
    N, D = sp.fraction(sp.together(tf))
    S = sp.expand(N ** 2 + D ** 2)
    if S == 0:
        return {"status": "t_f undefined", "verdict": "unknown"}
    dfl = sp.factor_list(S)
    sqf = sp.expand(sp.Mul(*[q for q, m in dfl[1] if m % 2 == 1]))
    dd = sp.Poly(sqf, lam).degree() if sqf.free_symbols else 0
    genus = (dd - 1) // 2 if dd >= 1 else 0
    rec = {"status": "linear", "tf": str(tf)[:80], "sqf_deg": dd, "genus": genus}
    if genus == 0:
        if dd == 0 and sqrt_rational(dfl[0]) is None:
            rec["verdict"] = "candidate"                # only the square-part roots remain (not enumerated here)
        else:
            rec["verdict"] = "infinite"
    elif genus == 1:
        cs = [int(c) for c in sp.Poly(sp.expand(dfl[0] * sqf), lam).all_coeffs()]
        r = quartic_points(cs)
        rec["pari"] = {k: r[k] for k in r if k != "points"}
        if "error" in r:
            rec["verdict"] = "unknown"
        elif r["rank_hi"] > 0:
            rec["verdict"] = "infinite"
        elif r["complete"]:
            rec["verdict"] = "candidate" if r["tvals"] else "dead"
        else:
            rec["verdict"] = "unknown"
    else:
        rec["verdict"] = "finite"
    return rec


def decide_genus0(fe, var, oth, cand=None, f=None):
    """A genus-0 factor of the Pythagorean pullback: parametrize, then the
    monomial lemma, else the third-frame lift."""
    pars, how, cands = parametrize(fe, var, oth)
    live_c = [(str(a), str(b)) for a, b in cands if not (degenerate(a) or degenerate(b))]
    info = {"how": how, "candidates": live_c}
    worst = "candidate" if live_c else "dead"
    if not pars:
        if how == "disc = nonsquare * square":
            return worst, info
        return "unknown", dict(info, note=how)
    branches = []
    for taug, tauh in pars:
        br = {"tau_g": str(taug)[:60], "tau_h": str(tauh)[:60]}
        mono = monomial_relation(taug, tauh)
        if mono:
            br.update({"monomial": mono, "verdict": "dead"})
        elif cand is not None:
            lf = lift(cand, f, taug, tauh)
            br.update({"lift": lf, "verdict": lf["verdict"]})
        else:
            br["verdict"] = "infinite"
        branches.append(br)
        if ORDER[br["verdict"]] > ORDER[worst]:
            worst = br["verdict"]
    info["branches"] = branches
    return worst, info


_GENUS_CACHE = {}
_PULLBACK_CACHE = {}
RESOLVE_TIMEOUT = 300
HIGH_DEGREE_ROUTE = "genus"          # "genus": bound then resolution; "skip": leave high-degree components unknown
NF_SECONDS = 0                       # alarm (s) on each branch-value field's nfinit in the bound; 0 = none (entries 102-103)
BOUND_DEGMAX = 40                    # branch-value fields above this degree are skipped in the bound (valid; the sweep uses 20)
PROVISIONAL_FINITE = False           # the sweep only: an exact genus >= 2 without its cross-check counts as finite, flagged 'provisional'


def exact_genus_verdict(phi, dg, dh):
    """(verdict, info) for a component by its genus, in rigorous steps
    (entries 102-104).  (1) The corrected Riemann-Hurwitz LOWER BOUND
    (degree-40 cap; with NF_SECONDS > 0 an alarm skips a branch-value field
    whose nfinit is slow -- skipping only lowers the bound): g_lb >= 2 certifies.
    (2) Else the EXACT genus by resolution (entry 103), certified only when its
    Riemann-Hurwitz cross-check completes with no skipped factor and agrees;
    an exact genus >= 2 without the cross-check is recorded as PROVISIONAL and
    the verdict stays 'unknown' (the sweep's census counts it; a rigorous pass
    can finish it).  'finite' also needs the absolute-irreducibility
    certificate.  Genus <= 1 components are left to the pullback machinery.
    Memoized per polynomial AND per decision policy / settings (entry 117: a cached
    provisional verdict must not be returned in strict mode)."""
    key = (str(phi), dg, dh, bool(PROVISIONAL_FINITE), int(BOUND_DEGMAX), int(NF_SECONDS), int(RESOLVE_TIMEOUT), str(HIGH_DEGREE_ROUTE))
    if key in _GENUS_CACHE:
        return _GENUS_CACHE[key]
    from compute.omega3_genus import genus_lower_bound, ramification_bound, absolutely_irreducible
    inf = {}
    try:
        g_lb, binfo = genus_lower_bound(phi, dg, dh, degmax=BOUND_DEGMAX, timeout=RESOLVE_TIMEOUT, nf_seconds=NF_SECONDS)
    except Exception as e:                      # pragma: no cover
        g_lb, binfo = None, {"error": repr(e)[:160]}
    inf["g_lb"] = g_lb
    inf["bound"] = {k: {kk: vv for kk, vv in v.items() if kk != "notes"} for k, v in binfo.items() if isinstance(v, dict)}
    certified_by = "bound" if (g_lb is not None and g_lb >= 2) else None
    if certified_by is None:
        from compute.omega3_resolve import exact_genus
        try:
            g, det = exact_genus(phi, dg, dh, timeout=RESOLVE_TIMEOUT)
        except Exception as e:                  # pragma: no cover
            g, det = None, {"error": repr(e)[:160]}
        inf.update(exact_genus=g, p_a=det.get("p_a"), sum_delta=det.get("sum_delta"))
        if det.get("error"):
            inf["error"] = str(det["error"])[-200:]
        if g is not None and g >= 2:
            # the cross-check needs every discriminant factor: hopeless when the capped bound already skipped one
            hopeless = BOUND_DEGMAX < 40 and inf["bound"].get("direct", {}).get("skipped_factors", 0) > 0
            R, rinfo = (None, {}) if hopeless else ramification_bound(
                phi, dg, dh, swap=False, degmax=(400 if BOUND_DEGMAX >= 40 else BOUND_DEGMAX), timeout=RESOLVE_TIMEOUT, nf_seconds=NF_SECONDS)
            if R is not None and rinfo.get("skipped_factors", 0) == 0:
                two_g = 2 - 2 * dh + R + det["branch_correction"]
                inf["consistent"] = (two_g == 2 * g)
                if inf["consistent"]:
                    certified_by = "resolution"
            else:
                inf["consistent"] = None
                inf["provisional"] = True
                if PROVISIONAL_FINITE:
                    certified_by = "resolution-provisional"
    if certified_by:
        pr = absolutely_irreducible(phi)
        inf["abs_irred_p"] = pr
        inf["route"] = certified_by
        # the certificate is not needed for FINITENESS (entry 108): the component is irreducible over Q
        # (a factor of the resultant); if it is absolutely irreducible its genus is >= 2 (finitely many
        # points, Faltings), and if it is reducible over the closure every rational point lies on all its
        # conjugate components at once -- a finite intersection.  The certificate only says which case.
        v = "finite"
        if pr is None:
            inf["note"] = "certificate failed: finite by the dichotomy (genus >= 2, or the intersection of conjugates)"
    else:
        v = "unknown"
    _GENUS_CACHE[key] = (v, inf)
    return v, inf


def decide_component(phi, dg, dh, cand=None, f=None, pullback_max_degree=6):
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
        if HIGH_DEGREE_ROUTE == "skip":
            return "unknown", dict(info, note="high degree, genus route skipped")
        v, ginf = exact_genus_verdict(phi, dg, dh)              # entry 104: the genus tools, in the engine
        info["genus"] = ginf
        return v, (info if v == "finite" else dict(info, note="high degree: genus not certified >= 2"))
    pkey = (str(phi), dg, dh)
    if pkey not in _PULLBACK_CACHE:
        psi = sp.expand(phi.subs({tg: pyth(ug), th: pyth(uh)}) * (1 - ug ** 2) ** dg * (1 - uh ** 2) ** dh)
        psi = sp.expand(sp.cancel(psi))
        _PULLBACK_CACHE[pkey] = sp.factor_list(psi)[1]
    worst, facs = "dead", []
    for fac, mult in _PULLBACK_CACHE[pkey]:
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
            if eh == 1 or eg == 1:                              # genus 0: linear in a variable
                var, oth = (uh, ug) if eh == 1 else (ug, uh)
                v, ginf = decide_genus0(fe, var, oth, cand, f)
                finf.update(genus=0, **ginf)
            else:
                done = False
                for var, oth, dv in ((uh, ug, eh), (ug, uh, eg)):
                    if dv == 2:
                        dm = _disc_model(fe, var, oth)
                        if dm is None:
                            v, ginf = decide_genus0(fe, var, oth, cand, f)
                            finf.update(genus=0, **ginf)
                        else:
                            sqf, dfl, genus = dm
                            finf["genus"] = genus
                            if genus == 0:
                                v, ginf = decide_genus0(fe, var, oth, cand, f)
                                finf.update(ginf)
                            elif genus == 1:
                                v, minf = decide_model(sqf, oth, "tau", square_part_roots(dfl, oth))
                                finf["model"] = minf
                            else:
                                v = "finite"
                        done = True
                        break
                if not done:                                    # degree >= 3 in both variables: the exact genus
                    v, ginf = exact_genus_verdict(sp.expand(fe.subs({ug: tg, uh: th}, simultaneous=True)), eg, eh)
                    finf["genus"] = ginf
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
        v, info = decide_component(phi, dg, dh, cand, f)
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


def decide_class_fast(cand):
    """The sweep's decision (entry 104): pass 1 decides every frame with the
    high-degree components skipped (cheap: resultants, models, pullbacks) --
    a dead frame ends it; pass 2 certifies the high-degree components by
    genus, frame by frame in order of the largest bidegree met, stopping at
    the first frame that is finite or dead.  Same verdicts as decide_class
    on every class where a dead frame exists or one certified frame suffices."""
    global HIGH_DEGREE_ROUTE
    saved = HIGH_DEGREE_ROUTE
    HIGH_DEGREE_ROUTE = "skip"
    try:
        frames = {f: decide_frame(cand, f) for f in range(3)}
    finally:
        HIGH_DEGREE_ROUTE = saved
    vs = [fr["verdict"] for fr in frames.values() if fr["verdict"] != "degenerate"]
    best = min(vs, key=lambda v: ORDER[v]) if vs else "degenerate"
    if best in ("dead", "finite", "candidate", "infinite", "degenerate"):
        return best, frames
    def size(f):
        return max((max(c["deg"]) for c in frames[f].get("components", []) if c.get("verdict") == "unknown"), default=0)
    for f in sorted([f for f in frames if frames[f]["verdict"] == "unknown"], key=size):
        frames[f] = decide_frame(cand, f)
        if frames[f]["verdict"] in ("dead", "finite"):
            break
    vs = [fr["verdict"] for fr in frames.values() if fr["verdict"] != "degenerate"]
    best = min(vs, key=lambda v: ORDER[v]) if vs else "degenerate"
    return best, frames
