"""THE SYMMETRY TOWER (entries 135-137): quotients of a class's elimination component Phi(g, h) by its sign-and-inversion
symmetries, the hyperelliptic and elliptic endpoints, and the lift of an endpoint's rational points back to the frame
ratios.  A class dies when a route ends on a curve whose rational points are completely known (an elliptic curve of rank 0
with its torsion points, or one of the genus-2 curves decided in entries 118-132) and none of those points lifts to an
admissible pair (g, h).

Steps (each records its forward map; an endpoint's points are pulled back as fibers of the composed map, entry 138):
  joint(a, b)            X = a^2, Y = a b            when Phi is invariant up to sign under (a, b) -> (-a, -b)
  inversion(a; s)        U = a + s/a                 when Phi is invariant under a -> s/a (s = +-1)
  double_inversion       U = a + s1/a, V = b + s2/b  when Phi is invariant under (a, b) -> (s1/a, s2/b) (fiber 2) or under
                                                     both single inversions (fiber 4)
  hyperelliptic(a, b)    a curve quadratic in one variable q: y^2 = D(o) = S(o)^2 core(o), core squarefree
  even(o)                z = o^2 for an even core;  reciprocal(o; kappa)  w = o + kappa/o for a (twisted) reciprocal core
  twists (entry 140)     y^2 = core(o) f(o) for the square classes f(o) that rational points (the fiber discriminants of the
                         quotient steps) or admissible points (g^2 + 1, h^2 + 1) must make squares; their classical quotients
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
# and the complete list of affine rational points (the points at infinity are always among the fiber values)
KNOWN_GENUS2 = {
    "G1": ([25, 0, -29, 0, 11, 0, 1], [(0, 1), (0, -1)], "entry 118 (bielliptic QC + the E1 x E2 sieve)"),
    "F1": ([1, 0, 11, 0, -5, 0, 1], [(0, 1), (0, -1)], "entry 130 (bielliptic QC + the E1 x E2 sieve)"),
    "C_a": ([25, -36, -18, 44, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4), (Fraction(-1, 5), Fraction(32, 25)), (Fraction(-1, 5), Fraction(-32, 25))], "entry 132 (Magma: rank 1, Chabauty + the Mordell-Weil sieve)"),
    "C_b": ([25, -4, -18, 12, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4), (Fraction(-1, 5), Fraction(16, 25)), (Fraction(-1, 5), Fraction(-16, 25))], "entry 132 (Magma)"),
    "C_c": ([1, -4, 6, 12, 1, 0], [(0, 0), (-1, 0), (1, 4), (1, -4)], "entry 131 (LMFDB 1408.b.180224.2, rank 0)"),
    # K: the odd companion of the frame-1/2 quotients of the last sixteen (1,1,1) classes (entry 138); J(K)(Q) = Z/2 + Z proved,
    # Chabauty on the generator: K(Q) = {(0, 0), oo} (Magma, compute/qc/magma_tower138.out.txt)
    "K": ([1, 80, 126, -16, 1, 0], [(0, 0)], "entry 138 (Magma: rank 1, the Mordell-Weil group proved, Chabauty)"),
    # the genus-2 endpoints of the open shape classes decided by Magma in entry 139 (compute/qc/magma_tower139.m, .out.txt):
    # blocks B, C, G, H -- rank <= 1, the Mordell-Weil group proved, Chabauty; G and H have only their two points at infinity
    "B139": ([-16384, 0, 2560, 0, -100, 0, 1], [(0, 1), (0, -1), (Fraction(1, 8), 0), (Fraction(-1, 8), 0)], "entry 139 (Magma block B: rank 1, MW group Z/2 + Z/2 + Z proved, Chabauty)"),
    "C139": ([-1024, 0, 512, 0, -48, 0, 1], [(0, 1), (0, -1)], "entry 139 (Magma block C: rank 1, MW group Z proved, Chabauty)"),
    "G139": ([1, 0, -52, 0, 128, 0, 3072], [], "entry 139 (Magma block G: rank 1, MW group Z/2 + Z proved, Chabauty: the two points at infinity only)"),
    "H139": ([1, 0, -36, 0, 176, 0, 320], [], "entry 139 (Magma block H: rank 1, MW group Z proved, Chabauty: the two points at infinity only)"),
    # block J: rank 1, torsion Z/2, the group found up to an index prime to 3 (IsDivisibleBy on the generator and on generator + torsion,
    # magma_tower139b.m); Chabauty with index primes {3}: C(Q) = {(0, 0), oo} unconditionally
    "J139": ([1, 688, 3808, -10496, 6400, 0], [(0, 0)], "entry 139 (Magma block J: rank 1, the index prime to 3 certified, Chabauty)"),
    # block D of magma_tower140.m (entry 141): y^2 = x Q(x), Q = 25x^4 - 656x^3 + 3808x^2 + 11008x + 256; rank 1, torsion Z/2, the index prime to 3
    # certified by IsDivisibleBy (magma_tower140b.m), Chabauty: C(Q) = {(0, 0), oo}
    "D140": ([25, -656, 3808, 11008, 256, 0], [(0, 0)], "entry 141 (Magma block D of 140: rank 1, the index prime to 3 certified, Chabauty)"),
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
    return Q, {"kind": "double_inversion", "old": (a, b), "new": (U, V), "relations": [a ** 2 - U * a + s1, b ** 2 - V * b + s2], "fiber": 4 if both else 2, "s1": s1, "s2": s2}


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
        # the odd companion: w^2 = z Qz(z) with w = o y (entry 138)
        W2 = sp.Symbol("W2")
        out.append(("odd", sp.expand(z * Qz), z, {"kind": "odd", "old": (o, yy), "new": (z, W2), "relations": [o ** 2 - z, o * yy - W2]}))
    d = P.degree()
    if d % 4 == 0:
        for kappa in twisted_kappas(core, o):
            Pw = reciprocal_quotient(core, o, w, kappa)
            if Pw is not None:
                # core(o) = o^{d/2} Pw(w): y = o^{d/4} Y
                Y2 = sp.Symbol("Y2")
                strec = {"kind": "reciprocal", "old": (o, yy), "new": (w, Y2), "relations": [o ** 2 - w * o + kappa, yy - o ** (d // 4) * Y2], "kappa": kappa}
                out.append(("reciprocal", Pw, w, strec))
                # the rationality twist of the reciprocal quotient: o rational forces w^2 - 4 kappa = (o - kappa/o)^2 a square (entry 140)
                Ptw = twisted_core(Pw, w ** 2 - 4 * kappa, w)
                if Ptw is not None:
                    out.append(("reciprocal twist[w^2-4k]", Ptw, w, dict(strec, twist="w^2-4k")))
    return out


def twisted_core(core, fac, o):
    """The squarefree part of core(o) * fac(o): the model y^2 = core twisted by the square class of fac (entry 140); None when
    the product is constant."""
    P = sp.Poly(sp.expand(core * fac), o)
    if P.degree() <= 0:
        return None
    fl = sp.factor_list(P.as_expr())
    c = sp.Rational(fl[0])
    cc = c.p * c.q                      # the same square class as c, an integer (a rational content is not truncated)
    sq = 1
    for p_, e_ in sp.factorint(abs(cc)).items():
        sq *= p_ ** (2 * (e_ // 2))
    out = sp.Integer(cc // sq) if cc > 0 else -sp.Integer((-cc) // sq)
    for f, m in fl[1]:
        out *= f.as_expr() ** (m % 2)
    out = sp.expand(out)
    if not out.has(o):
        return None
    return out


def twist_root_values(fac, o):
    """The rational roots of a twist factor: at such an o-value the reduction of core * fac may have removed a double root, so the
    fibers over these values are added to every twisted endpoint's lift set (the audit of entry 140)."""
    return rational_roots(sp.expand(fac), o)


def twist_factors(steps, hm):
    """The square-class conditions on the model variable o (entry 140): kind "rational" -- the discriminant of a quotient step's
    fiber, which is a square at the image of every rational point (joint: X; inversion: U^2 - 4s; double inversion: U^2 - 4s1,
    V^2 - 4s2), carried through later coordinate changes and kept when it is a function of o alone; kind "admissible" -- g^2 + 1
    or h^2 + 1, which is a square at every admissible point, when o is g, 1/g, h, 1/h, g^2, h^2, 1/g^2 or 1/h^2.  Each factor is
    a polynomial in o, its square class the condition."""
    o = hm["o"]
    conds = []          # (name, expression in the step's new variables, index of the step)
    for i, st in enumerate(steps):
        k = st["kind"]
        if k == "joint":
            conds.append(("X", st["new"][0], i))
        elif k == "inversion":
            conds.append(("U^2-4s", st["new"][0] ** 2 - 4 * st["s"], i))
        elif k == "double_inversion":
            U, V = st["new"]
            conds.append(("U^2-4s1", U ** 2 - 4 * st["s1"], i))
            conds.append(("V^2-4s2", V ** 2 - 4 * st["s2"], i))
    out = []
    for name, expr, i in conds:
        e = expr
        for st in steps[i + 1:]:
            if st["kind"] == "change":
                e = e.subs(st["sol"], simultaneous=True)      # the old variables in terms of the new ones
        e = sp.cancel(sp.together(e))
        if e.free_symbols and e.free_symbols <= {o}:
            N, D = sp.fraction(e)
            fac = sp.expand(N * D)                              # N/D and N*D have the same square class
            if fac.has(o):
                out.append((name, fac, "rational"))
    v = endpoint_variable(steps, o)
    for expr, name, fac in ((g, "g", o ** 2 + 1), (1 / g, "1/g", o ** 2 + 1), (h, "h", o ** 2 + 1), (1 / h, "1/h", o ** 2 + 1),
                            (g ** 2, "g^2", o + 1), (h ** 2, "h^2", o + 1), (1 / g ** 2, "1/g^2", o * (o + 1)), (1 / h ** 2, "1/h^2", o * (o + 1))):
        for sign in (1, -1):        # o = -g etc. carry the same square class (o^2 + 1 is even; o + 1 -> 1 - o for o = -g^2)
            if sp.simplify(v - sign * expr) == 0:
                out.append(("adm " + ("-" if sign < 0 else "") + name, sp.expand(fac.subs(o, sign * o)), "admissible"))
                break
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

def forward_map(step):
    """The new variables of a step as rational functions of its old variables."""
    k = step["kind"]
    a, b = step["old"]
    if k == "joint":
        X, Y = step["new"]
        return {X: a ** 2, Y: a * b}
    if k == "inversion":
        return {step["new"][0]: a + step["s"] / a}
    if k == "double_inversion":
        U, V = step["new"]
        return {U: a + step["s1"] / a, V: b + step["s2"] / b}
    if k == "change":
        ex = {"a": a, "1/a": 1 / a, "b": b, "1/b": 1 / b, "b/a": b / a, "a/b": a / b, "a*b": a * b}
        return {step["new"][0]: ex[step["a2"]], step["new"][1]: ex[step["b2"]]}
    if k == "hyperelliptic":
        return {step["new"][0]: step["new"][0]}          # o is a variable of the level itself; q is dropped
    if k in ("even", "odd"):
        return {step["new"][0]: a ** 2}                  # old = (o, yy): z = o^2
    if k == "reciprocal":
        return {step["new"][0]: a + step["kappa"] / a}   # w = o + kappa / o
    raise ValueError(k)


def endpoint_variable(steps, var):
    """The endpoint variable as an explicit rational function of (g, h): the forward maps composed, last step first."""
    e = var
    for st in reversed(steps):
        e = e.subs(forward_map(st), simultaneous=True)
    return sp.cancel(sp.together(e))


def curve_intersection(phi, F, a=g, b=h):
    """The rational affine points of {phi = 0, F = 0} (exact: a resultant and rational roots); None when the two share a
    component (the intersection is infinite and nothing is certified).  Points at infinity of the (a, b)-plane are not
    listed: a frame ratio is finite by definition."""
    F = sp.expand(F)
    if F == 0:
        return None
    if not F.free_symbols:
        return []
    Pp, PF = sp.Poly(phi, a, b), sp.Poly(F, a, b)
    if PF.degree(b) >= 1 and Pp.degree(b) >= 1:
        R = sp.expand(sp.resultant(phi, F, b))
        if R == 0:
            return None
        avals = rational_roots(R, a) if R.has(a) else []
    elif PF.degree(b) == 0:
        avals = rational_roots(F, a)
    else:
        # F in b only and phi in a only: the product set
        return [(x, y) for x in rational_roots(phi, a) for y in rational_roots(F, b)]
    pts = []
    for a0 in avals:
        pa = sp.expand(phi.subs(a, a0))
        Fa = sp.expand(F.subs(a, a0))
        if pa == 0:
            return None
        if not pa.has(b):
            continue
        for b0 in rational_roots(pa, b):
            if sp.expand(Fa.subs(b, b0)) == 0:
                pts.append((a0, b0))
    return pts


def fiber_points(phi, vexpr, v0):
    """The rational points of the component phi = 0 over the endpoint value v0 (None = the point at infinity) of the
    endpoint variable vexpr = N / D: {phi = 0, N - v0 D = 0}, or {phi = 0, D = 0} for infinity."""
    N, D = sp.fraction(sp.cancel(sp.together(vexpr)))
    F = D if v0 is None else N - v0 * D
    return curve_intersection(phi, F)


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
    # R0: the direct model (a quadratic variable of phi itself; entry 138)
    with_hyperelliptic([], [phi], g, h, "direct")
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
        endpoints = [(label, steps, curves, hm["core"], hm["o"], yy, None)]
        # the classical quotients of the model (one level) as further endpoints
        for name, Pq, var, stc in classical_quotients(hm["core"], hm["o"]):
            yvar = stc["new"][1]
            tw0 = None
            if name == "odd":               # the odd companion is the even quotient's rationality twist by z: its root z = 0 is o = 0
                tw0 = {"factors": ["z"], "kinds": ["rational"], "roots": [sp.Integer(0)], "omap": endpoint_variable(steps, hm["o"])}
            elif stc.get("twist"):          # the reciprocal twist by w^2 - 4 kappa: its rational roots pull back to o-values
                tw0 = {"factors": [stc["twist"]], "kinds": ["rational"], "omap": endpoint_variable(steps, hm["o"]),
                       "roots": [o0 for w0 in rational_roots(sp.expand(var ** 2 - 4 * stc["kappa"]), var) for o0 in rational_roots(sp.expand(hm["o"] ** 2 - w0 * hm["o"] + stc["kappa"]), hm["o"])]}
            endpoints.append((label + " -> " + name, steps + [stc], curves + [yvar ** 2 - Pq], Pq, var, yvar, tw0))
        # the twisted models (entry 140): every nonempty subset of the square-class conditions, with their classical quotients
        tf = twist_factors(steps, hm)
        for r_ in range(1, len(tf) + 1):
            for sub in itertools.combinations(tf, r_):
                fac = sp.Integer(1)
                for _, fexpr, _ in sub:
                    fac *= fexpr
                tcore = twisted_core(hm["core"], fac, hm["o"])
                if tcore is None:
                    continue
                # the factor's rational roots: there the reduction may have removed a double root, so their fibers (through the
                # model variable's own map) join every twisted endpoint's lift set (the audit of entry 140)
                tw = {"factors": [n for n, _, _ in sub], "kinds": sorted({k for _, _, k in sub}), "roots": twist_root_values(fac, hm["o"]), "omap": endpoint_variable(steps, hm["o"])}
                tlabel = label + " twist[" + ",".join(tw["factors"]) + "]"
                endpoints.append((tlabel, steps, curves, tcore, hm["o"], yy, tw))
                for name, Pq, var, stc in classical_quotients(tcore, hm["o"]):
                    yvar = stc["new"][1]
                    tw2 = dict(tw, factors=tw["factors"] + ([stc["twist"]] if stc.get("twist") else []))
                    if stc.get("twist"):        # the reciprocal twist's factor w^2 - 4 kappa: its rational roots w0 = o + kappa/o pull back to o-values
                        w_ = var
                        tw2["roots"] = list(tw["roots"]) + [o0 for w0 in rational_roots(sp.expand(w_ ** 2 - 4 * stc["kappa"]), w_) for o0 in rational_roots(sp.expand(hm["o"] ** 2 - w0 * hm["o"] + stc["kappa"]), hm["o"])]
                    endpoints.append((tlabel + " -> " + name, steps + [stc], curves + [yvar ** 2 - Pq], Pq, var, yvar, tw2))
        for elabel, esteps, ecurves, core, var, yvar, tw in endpoints:
            deg = sp.Poly(core, var).degree()
            e = {"endpoint": elabel, "degree": deg}
            if tw:
                e["twist"] = {"factors": tw["factors"], "kinds": tw["kinds"], "roots": [str(r) for r in tw.get("roots", [])]}
            if deg <= 6:
                e["core"] = str(sp.Poly(core, var).as_expr())      # the endpoint's model, for the atlas (entry 140)
            values = None
            if deg in (3, 4):
                coeffs = [int(c) for c in sp.Poly(core, var).all_coeffs()] if all(sp.Rational(c).is_integer for c in sp.Poly(core, var).all_coeffs()) else None
                if coeffs is None:
                    cont = sp.lcm([sp.Rational(c).q for c in sp.Poly(core, var).all_coeffs()])
                    coeffs = [int(c * cont ** 2) for c in sp.Poly(core, var).all_coeffs()] if sp.sqrt(cont ** 2).is_rational else None
                ed = elliptic_endpoint(coeffs)
                e["elliptic"] = ed
                if ed and ed.get("complete"):
                    values = [sp.Rational(a) for a, b in ed["points"]] + [None]
            elif deg in (5, 6):
                km = match_known_genus2(core, var)
                e["known"] = km
                if km:
                    # the x-values of the known points transported to the endpoint variable; the point at infinity always;
                    # under o = lam / x the known curve's points at infinity land on x = 0
                    values = [sp.Rational(a) for a, b in km["points"]] + [None] + ([sp.Integer(0)] if km["kind"] == "reciprocal" else [])
            if values is not None:
                vexpr = endpoint_variable(esteps, var)
                e["variable"] = str(vexpr)
                fib, lifts, ok = {}, [], True
                for v0 in sorted(set(values), key=str):
                    pts = fiber_points(phi, vexpr, v0)
                    key = "oo" if v0 is None else str(v0)
                    if pts is None:
                        fib[key] = "infinite"
                        ok = False
                        break
                    fib[key] = [(str(a), str(b)) for a, b in pts]
                    lifts += pts
                # a twisted endpoint: the fibers over the twist factor's rational roots, through the model variable's own map
                # (the squarefree reduction may have removed a double root there; the audit of entry 140)
                if ok and tw and tw.get("roots"):
                    for o0 in sorted(set(tw["roots"]), key=str):
                        pts = fiber_points(phi, tw["omap"], o0)
                        key = "root " + str(o0)
                        if pts is None:
                            fib[key] = "infinite"
                            ok = False
                            break
                        fib[key] = [(str(a), str(b)) for a, b in pts]
                        lifts += pts
                e["fibers"] = fib
                lifts = list(dict.fromkeys(lifts))          # the root fibers may repeat a value fiber: one entry per point
                e["lifts"] = [(str(a), str(b)) for a, b in lifts]
                e["admissible"] = [(str(a), str(b)) for a, b in lifts if admissible((a, b))]
                if ok and not e["admissible"]:
                    kill = dict(rec, **e)
            rec.setdefault("endpoints", []).append({k: v for k, v in e.items()})
            if kill and not want_all:
                break
        summary["routes"].append(rec)
        if kill and not want_all:
            break
    summary["kill"] = kill
    return summary
