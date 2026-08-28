"""M12-C opening (M11-J-2): the eta*-web at degree 3 — the GRAPH
slices, closed exactly.

TARGET.  By A8.15/A8.16 a new rational curve on X has an irreducible
eta*-integral Lucas image of degree >= 3 passing through >= 3 of the
eight triple points of the branch arrangement:

    A-points (finite, on v = 0):   (c, v) = (-1, 0), (0, 0), (1, 0)
    B-points (at infinity, u = 0): (C:U:V) = (-b : 0 : 1), b = -1,0,1
    D-points:                      (c, v) = (0, 1), (0, -1)

This module closes the two GRAPH slices of the cubic level — curves
whose defining polynomial is linear in c (c = f(v)) or linear in v
(v = g(c)), automatically irreducible and rational:

  * a c-graph cubic meets each v-level once and misses every B-point
    (its only point at infinity is (1:0:0), a double point of the
    arrangement), so >= 3 triple points forces ONE A-point plus BOTH
    D-points: the closed 1-parameter families
        c = (1 - v^2)(a0 + b v),   a0 in {-1, 0, 1};
  * a v-graph cubic automatically passes B0 = (0:0:1) (triply) and
    meets each c-level once, giving
      - 1-parameter families  v = (1 - c^2)(v0 + b c), v0 in {-1,0,1}
        (three finite points), and
      - 2-parameter families through B0 + two finite triple points:
        g(1) = g(-1) = 0  (the same (1-c^2)(a + b c) with a free), or
        g(0) = v0 and g(±1) = 0 (one condition each).

For each family the restriction of eta* gives an exact polynomial
system in the parameters; univariate families are decided by an
exact gcd over Q (stdlib), two-parameter families by nonzero
resultants + factor-complete peeling (sympy), in the pattern of
Theorem A8.17.  Run:  python -m compute.web_cubics
"""

from fractions import Fraction as F
from math import comb

from compute.special_locus import poly_gcd_1var
from compute.web_lines import eta_star

M = 4


# --------------------------------------------------------------- poly core
# polynomials in (t, x, y): dict {(dt, dx, dy): int}

def pmul(A, B):
    out = {}
    for ka, va in A.items():
        for kb, vb in B.items():
            k = (ka[0] + kb[0], ka[1] + kb[1], ka[2] + kb[2])
            v = out.get(k, 0) + va * vb
            if v:
                out[k] = v
            elif k in out:
                del out[k]
    return out


def padd(A, B, s=1):
    out = dict(A)
    for k, v in B.items():
        w = out.get(k, 0) + s * v
        if w:
            out[k] = w
        elif k in out:
            del out[k]
    return out


def ppow(A, n, cache):
    if n in cache:
        return cache[n]
    if n == 0:
        return {(0, 0, 0): 1}
    r = pmul(ppow(A, n - 1, cache), A)
    cache[n] = r
    return r


def restriction_system(c_t, v_t):
    """t-coefficients of  sum_k N_k(c(t), v(t)) c'(t)^k v'(t)^(4-k),
    as polynomial dicts {(dx, dy): int} in the parameters."""
    Ns = eta_star()

    def ddt(P):
        out = {}
        for (dt, dx, dy), v in P.items():
            if dt:
                out[(dt - 1, dx, dy)] = v * dt
        return out

    cp, vp = ddt(c_t), ddt(v_t)
    ccache, vcache, cpc, vpc = {}, {}, {}, {}
    Ftot = {}
    for k in range(M + 1):
        if not Ns[k]:
            continue
        dk = pmul(ppow(cp, k, cpc), ppow(vp, M - k, vpc))
        for (i, j), val in Ns[k].items():
            term = pmul(ppow(c_t, i, ccache), ppow(v_t, j, vcache))
            term = pmul(term, dk)
            Ftot = padd(Ftot, {kk: val * vv for kk, vv in term.items()})
    eqs = {}
    for (dt, dx, dy), v in Ftot.items():
        eqs.setdefault(dt, {})[(dx, dy)] = v
    return [eqs[t] for t in sorted(eqs)]


# ---------------------------------------------------------- slice builders

def cgraph_family(a0):
    """c = (1 - t^2)(a0 + x t), v = t   (x = the free parameter)."""
    c_t = {(0, 0, 0): a0, (1, 1, 0): 1, (2, 0, 0): -a0, (3, 1, 0): -1}
    c_t = {k: v for k, v in c_t.items() if v}
    v_t = {(1, 0, 0): 1}
    return restriction_system(c_t, v_t)


def vgraph_family(coeffs):
    """v = g(c) with g given by dicts over (x, y); c = t."""
    v_t = {}
    for cdeg, poly in enumerate(coeffs):
        for (dx, dy), val in poly.items():
            k = (cdeg, dx, dy)
            v_t[k] = v_t.get(k, 0) + val
    v_t = {k: v for k, v in v_t.items() if v}
    c_t = {(1, 0, 0): 1}
    return restriction_system(c_t, v_t)


def univariate_gcd(eqs):
    """Exact gcd over Q of a system univariate in x."""
    g = None
    for E in eqs:
        mx = max((dx for (dx, dy) in E), default=0)
        assert all(dy == 0 for (_, dy) in E)
        lst = [F(0)] * (mx + 1)
        for (dx, _), v in E.items():
            lst[dx] += v
        if all(x == 0 for x in lst):
            continue
        g = lst if g is None else poly_gcd_1var(g, lst)
        if len([x for x in g if x != 0]) and len(g) == 1:
            break
    return g


def gcd_roots_rational(g):
    """Rational roots of an exact Fraction-list polynomial."""
    from fractions import Fraction
    den = 1
    for c in g:
        den = den * c.denominator // __import__("math").gcd(
            den, c.denominator)
    ig = [int(c * den) for c in g]
    while ig and ig[-1] == 0:
        ig.pop()
    roots = []
    if not ig:
        return None  # identically zero
    # strip x^k
    k0 = 0
    while ig[0] == 0:
        ig.pop(0)
        k0 += 1
    if k0:
        roots.append(F(0))
    a0, an = abs(ig[0]), abs(ig[-1])

    def divisors(n):
        out = []
        d = 1
        while d * d <= n:
            if n % d == 0:
                out += [d, n // d]
            d += 1
        return sorted(set(out))

    for p in divisors(a0):
        for q in divisors(an):
            for s in (1, -1):
                r = F(s * p, q)
                if sum(c * r ** i for i, c in enumerate(ig)) == 0 \
                        and r not in roots:
                    roots.append(r)
    return roots, ig, k0


def run_univariate_slices():
    out = {}
    # c-graphs: one A-point + both D-points
    for a0 in (-1, 0, 1):
        eqs = cgraph_family(a0)
        g = univariate_gcd(eqs)
        res = gcd_roots_rational(g)
        deg = len([i for i, c in enumerate(g) if c != 0]) and \
            (len(g) - 1)
        out[f"cgraph a0={a0}"] = (deg, res if res is None else res[0])
    # v-graphs, three finite points: v = (1-c^2)(v0 + x c)
    for v0 in (-1, 0, 1):
        coeffs = [  # g(c) = v0 + x c - v0 c^2 - x c^3
            {(0, 0): v0}, {(1, 0): 1}, {(0, 0): -v0}, {(1, 0): -1}]
        coeffs = [{k: v for k, v in d.items() if v} for d in coeffs]
        eqs = vgraph_family(coeffs)
        g = univariate_gcd(eqs)
        res = gcd_roots_rational(g)
        deg = len(g) - 1
        out[f"vgraph v0={v0}"] = (deg, res if res is None else res[0])
    return out


def two_param_families():
    """The 2-parameter v-graph families through B0 + two finite
    triple points, as (name, coeffs) with parameters (x, y)."""
    fams = []
    # {B0, (1,0), (-1,0)}: g = (1 - c^2)(x + y c)
    fams.append(("B0,+A,-A", [
        {(1, 0): 1}, {(0, 1): 1}, {(1, 0): -1}, {(0, 1): -1}]))
    # {B0, X0, (1,0)}: g = v0 + x c + y c^2 - (v0 + x + y) c^3
    for v0 in (-1, 0, 1):
        fams.append((f"B0,(0,{v0}),+A", [
            {(0, 0): v0}, {(1, 0): 1}, {(0, 1): 1},
            {(0, 0): -v0, (1, 0): -1, (0, 1): -1}]))
    # {B0, X0, (-1,0)}: g(-1) = 0: v0 - x + y - e' = 0 -> e' = v0-x+y
    for v0 in (-1, 0, 1):
        fams.append((f"B0,(0,{v0}),-A", [
            {(0, 0): v0}, {(1, 0): 1}, {(0, 1): 1},
            {(0, 0): v0, (1, 0): -1, (0, 1): 1}]))
    return fams


def main():
    print("== univariate graph slices (exact, stdlib) ==")
    for name, (deg, info) in run_univariate_slices().items():
        print(f"  {name}: gcd degree {deg}; rational roots "
              f"{info if info is not None else 'IDENTICALLY ZERO'}")
    print("== two-parameter v-graph families (sympy elimination) ==")
    try:
        import sympy as sp
    except ImportError:
        print("  sympy unavailable; skipped")
        return
    x, y = sp.symbols("x y")
    for name, coeffs in two_param_families():
        coeffs = [{k: v for k, v in d.items() if v} for d in coeffs]
        eqs = vgraph_family(coeffs)
        exprs = []
        for E in eqs:
            e = sum(v * x ** dx * y ** dy for (dx, dy), v in E.items())
            if e != 0:
                exprs.append(sp.expand(e))
        print(f"  family {name}: {len(exprs)} equations")
        # eliminate x via nonzero resultants; gcd and factor in y
        Rs = []
        for i in range(1, len(exprs)):
            R = sp.resultant(exprs[0], exprs[i], x)
            if R != 0:
                Rs.append(sp.Poly(R, y))
            if len(Rs) == 2:
                break
        if len(Rs) < 2:
            print("    (needs deeper pairing — flagged)")
            continue
        G = sp.gcd(Rs[0], Rs[1])
        fl = sp.factor_list(G.as_expr())
        print(f"    gcd_y degree {sp.degree(G)}: factors "
              f"{[(sp.factor(f), e) for f, e in fl[1]]}")


if __name__ == "__main__":
    main()


def finish_two_param(verbose=True):
    """Per-candidate resolution of the 2-parameter families: for each
    rational y-candidate from the resultant gcd (whose factor lists
    split completely into rational linears — completeness over Qbar),
    the exact univariate gcd in x pins the solutions; each is fully
    verified and classified (line / conic / genuine cubic)."""
    import sympy as sp
    x, y = sp.symbols("x y")
    results = {}
    for name, coeffs in two_param_families():
        coeffs = [{k: v for k, v in d.items() if v} for d in coeffs]
        eqs = vgraph_family(coeffs)
        exprs = []
        for E in eqs:
            e = sum(v * x ** dx * y ** dy for (dx, dy), v in E.items())
            if e != 0:
                exprs.append(sp.expand(e))
        Rs = []
        for i in range(1, len(exprs)):
            R = sp.resultant(exprs[0], exprs[i], x)
            if R != 0:
                Rs.append(sp.Poly(R, y))
            if len(Rs) == 2:
                break
        G = sp.gcd(Rs[0], Rs[1])
        fl = sp.factor_list(G.as_expr())
        cands = set()
        complete = True
        for f, _ in fl[1]:
            pf = sp.Poly(f, y)
            if pf.degree() == 1:
                a1, a0 = pf.all_coeffs()
                cands.add(sp.Rational(-a0, a1))
            else:
                complete = False
        sols = []
        for y0 in sorted(cands):
            sub = [{(dx,): v for (dx, dy), v in E.items()
                    for v in [v * int(y0 ** dy * 1)]}
                   for E in eqs]
            # exact substitution with Fractions
            polys = []
            for E in eqs:
                mx = max(dx for (dx, dy) in E)
                lst = [F(0)] * (mx + 1)
                for (dx, dy), v in E.items():
                    lst[dx] += F(v) * F(y0) ** dy
                if any(c != 0 for c in lst):
                    polys.append(lst)
            g = None
            for p in polys:
                g = p if g is None else poly_gcd_1var(g, p)
            if g is None:
                sols.append((y0, "ALL x"))
                continue
            rr = gcd_roots_rational(g)
            if rr is None:
                sols.append((y0, "ALL x"))
                continue
            roots, ig, k0 = rr
            # completeness of x-roots: factor the gcd fully
            gx = sp.Poly(ig, sp.Symbol("x"))
            flx = sp.factor_list(gx.as_expr())
            xcomplete = all(sp.Poly(f, sp.Symbol("x")).degree() <= 1
                            for f, _ in flx[1])
            sols.append((y0, roots, xcomplete))
        results[name] = (complete, sols)
        if verbose:
            print(f"  {name}: y-candidates complete over Qbar: "
                  f"{complete}; per-candidate: {sols}")
    return results


def classify_solution(name, y0, x0):
    """What curve is (x0, y0) in this family? Returns a tag."""
    # reconstruct g(c) coefficients
    for nm, coeffs in two_param_families():
        if nm != name:
            continue
        g = []
        for d in coeffs:
            val = F(0)
            for (dx, dy), v in d.items():
                val += F(v) * F(x0) ** dx * F(y0) ** dy
            g.append(val)
        while g and g[-1] == 0:
            g.pop()
        deg = len(g) - 1 if g else -1
        return deg, g
