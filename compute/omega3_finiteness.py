"""THE BASE LOCUS OF THE ELIMINATION, and the finiteness statement for a closed box
(entry 104).

The engine (compute/omega3.py) decides a quadruple class in a frame f by
eliminating the frame: the two relations R1, R2, as polynomials in s_f (with
c_f = 1), have a resultant whose curve components in the other two frame
ratios (t_g, t_h) carry every solution.  A class is 'dead' when no component
has an admissible point and 'finite' when every component is dead or has
finitely many rational points (Faltings).  ONE GAP separates that from a
statement about squares: at a BASE POINT -- a pair (t_g, t_h) where every
coefficient of R1 and of R2 vanishes -- the relations hold for EVERY t_f,
i.e. for every third prime, and a single admissible base point would give a
magic square for infinitely many centers.  Base points lie on the resultant
curve, so they are among the finitely many points of a finite component;
they must still be listed, because they are the points where the eliminated
frame is unconstrained.

The base locus is a zero-dimensional system in (t_g, t_h) (the resultant is
not identically zero), solved here exactly: a lex Groebner basis, the
rational roots of its univariate element, the rational common roots above
each.  A base point is ADMISSIBLE when both coordinates are non-degenerate
Pythagorean frame ratios.

THE STATEMENT (for a box in which every class is dead or finite and no
finite class has an admissible base point in its certifying frame): a magic
square of squares whose center has that split-part shape gives a quadruple
class, a frame pair (t_g, t_h) on a component of the certifying frame, and
a third ratio t_f that is a root of a nonzero polynomial; each frame ratio
determines its prime (t = 2ab/(a^2 - b^2) with a > b > 0 coprime, p = a^2 +
b^2); so the squares with that shape correspond, up to the scaling by the
inert cofactor, to finitely many prime triples and finitely many quadruples
each: FINITELY MANY, up to scaling.  Ineffective (Faltings gives no bound),
and resting on the engine's verdicts (PARI: factorization over number
fields, unconditional rank bounds; the genus computations).
"""
from __future__ import annotations
import sympy as sp

from compute.omega3 import reduced_relations, FR, tg, th, is_frame_ratio, degenerate


def base_locus(cand, f):
    """The rational base points of the elimination of frame f for the class:
    {'status', 'points': [(t_g, t_h)], 'admissible': [...]}."""
    R1, R2, common = reduced_relations(cand)
    cf, sf = FR[f]
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh) = FR[g], FR[h]
    if R1 == 0 or R2 == 0:
        return {"status": "a relation vanishes identically", "points": None, "admissible": None}
    coeffs = []
    for R in (R1, R2):
        P = sp.Poly(R, sf)
        for c in P.all_coeffs():
            c = sp.expand(c.subs({cf: 1, sg: tg * cg, sh: th * ch}, simultaneous=True))
            if c == 0:
                continue
            # c_g, c_h are never zero for a frame: keep the factors in the ratios only
            c = sp.expand(sp.Mul(*[q ** m for q, m in sp.factor_list(c)[1] if q.free_symbols & {tg, th}]))
            if not (c.free_symbols & {tg, th}):
                return {"status": "a coefficient is a nonzero constant: empty base locus", "points": [], "admissible": []}
            coeffs.append(c)
    if not coeffs:
        return {"status": "all coefficients vanish identically", "points": None, "admissible": None}
    G = sp.groebner(coeffs, tg, th, order="lex")
    if list(G.exprs) == [1]:
        return {"status": "empty (Groebner basis 1)", "points": [], "admissible": []}
    uni = [e for e in G.exprs if not (e.free_symbols - {th})]
    if not uni:
        return {"status": "not zero-dimensional", "basis": [str(e)[:80] for e in G.exprs], "points": None, "admissible": None}
    pts = []
    for th0 in sp.Poly(uni[-1], th).ground_roots():
        if not th0.is_rational:
            continue
        rest = [e for e in (sp.expand(e.subs(th, th0)) for e in G.exprs) if e != 0]
        if not rest:
            continue
        gg = rest[0]
        for e in rest[1:]:
            gg = sp.gcd(gg, e)
        if gg.free_symbols:
            for tg0 in sp.Poly(gg, tg).ground_roots():
                if tg0.is_rational:
                    pts.append((tg0, th0))
    admissible = [(str(a), str(b)) for a, b in pts if not degenerate(a) and not degenerate(b) and is_frame_ratio(a) and is_frame_ratio(b)]
    return {"status": "zero-dimensional", "points": [(str(a), str(b)) for a, b in pts], "admissible": admissible}


def frame_ratio_prime(r):
    """The prime determined by a non-degenerate frame ratio: a frame (c, s) has
    c^2 + s^2 = p^2 and t = s/c = m/n in lowest terms (either sign), so (c, s) =
    lam (n, m) with lam^2 (m^2 + n^2) = p^2; m, n coprime forces lam = p / sqrt(m^2 + n^2)
    integral, hence p = sqrt(m^2 + n^2).  Returns that integer (a prime when the
    ratio comes from a split prime's frame), or None when m^2 + n^2 is not a square."""
    r = sp.nsimplify(r)
    if not r.is_rational or r == 0:
        return None
    m, n = abs(int(r.p)), abs(int(r.q))
    s, ok = sp.integer_nthroot(m * m + n * n, 2)
    return int(s) if ok else None
