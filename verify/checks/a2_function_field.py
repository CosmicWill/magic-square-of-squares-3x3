"""Mechanical verification for docs/attacks/A2-function-field.md.

All proof-critical checks are stdlib-only; polynomial arithmetic comes
from compute.ff_search (pure Python).
"""

from fractions import Fraction
from itertools import product

from ..framework import check, require
from compute.ff_search import (add, all_polys, deg, gcd_poly, mul, neg,
                               scale, search, square_table, sub, trim)

DOC = "docs/attacks/A2-function-field.md"


# --- integer-coefficient polynomial helpers (for Mason instances over Q) ---

def zmul(a, b):
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def zadd(a, b):
    n = max(len(a), len(b))
    out = [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
           for i in range(n)]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def zscale(a, s):
    out = [x * s for x in a]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def zderiv(a):
    out = [i * a[i] for i in range(1, len(a))]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


@check("a2.mason_instances", DOC)
def _(ctx):
    """Mason's setup on the nonconstant 3-AP of squares family
    A = t^2-2t-1, B = t^2+1, C = t^2+2t-1:
    (i) A^2 + C^2 = 2B^2 identically (3-term APs of squares DO exist
        nonconstantly, so the four-term theorem A2.4 is sharp);
    (ii) the Wronskian W = a b' - a' b is nonzero and the Mason bound
        max deg <= deg rad - 1 holds for (a,b,c) = (A^2, C^2, -2B^2)."""
    A, B, C = (-1, -2, 1), (1, 0, 1), (-1, 2, 1)
    a, b, c = zmul(A, A), zmul(C, C), zscale(zmul(B, B), -2)
    require(zadd(zadd(a, b), c) == (), "A^2 + C^2 - 2B^2 != 0")
    W = zadd(zmul(a, zderiv(b)), zscale(zmul(zderiv(a), b), -1))
    require(W != (), "Wronskian vanished")
    # A, B, C squarefree (nonzero discriminants) => rad(abc) = 2ABC
    for P in (A, B, C):
        disc = P[1] ** 2 - 4 * P[2] * P[0]
        require(disc != 0, "not squarefree")
    max_deg = max(len(a), len(b), len(c)) - 1
    rad_deg = (len(A) - 1) + (len(B) - 1) + (len(C) - 1)
    require(max_deg <= rad_deg - 1, "Mason inequality fails on instance")
    ctx.note(f"max deg {max_deg} <= rad deg {rad_deg} - 1; W has deg {len(W)-1}")


@check("a2.descent_identities", DOC)
def _(ctx):
    """Lemma A2.L's algebra, proven by complete-grid evaluation over Q:
    with a = s^2, b = -r^2 (so sqrt(a) = s, sqrt(-b) = r),
    X = (R^2+S^2)/(2s), Y = (S^2-R^2)/(2r):
      cX^2 + dY^2 == alpha R^4 + 2 beta R^2 S^2 + alpha S^4,
      alpha = c/(4a) - d/(4b),  beta = c/(4a) + d/(4b);
    Vieta form of the factorization; degeneracy equivalences."""
    for s, r, cc, dd, R, S in product((1, 2, 3), (1, 2), (-2, 1, 3),
                                      (-1, 2), (0, 1, 2), (1, 2)):
        a, b = Fraction(s * s), Fraction(-r * r)
        c, d = Fraction(cc), Fraction(dd)
        X = Fraction(R * R + S * S, 2 * s)
        Y = Fraction(S * S - R * R, 2 * r)
        alpha = c / (4 * a) - d / (4 * b)
        beta = c / (4 * a) + d / (4 * b)
        lhs = c * X * X + d * Y * Y
        rhs = alpha * R ** 4 + 2 * beta * R * R * S * S + alpha * S ** 4
        require(lhs == rhs, f"substitution identity fails at {(s,r,cc,dd,R,S)}")
        # Vieta: alpha(R^2 - th S^2)(R^2 - thb S^2) with th+thb = -2beta/alpha,
        # th*thb = 1 equals the quartic — checked via symmetric functions:
        if alpha != 0:
            e1, e2 = -2 * beta / alpha, Fraction(1)
            vieta = alpha * (R ** 4 - e1 * R * R * S * S + e2 * S ** 4)
            require(vieta == rhs, "Vieta factorization identity")
        # degeneracy equivalences: alpha = 0 <=> ad = bc;
        # beta - alpha = d/(2b) = 0 <=> d = 0; beta + alpha = c/(2a) = 0 <=> c=0
        require((alpha == 0) == (a * d == b * c))
        require(beta - alpha == d / (2 * b) and beta + alpha == c / (2 * a))
    ctx.note("substitution, Vieta, and degeneracy identities verified on grids")


@check("a2.four_ap_ff", DOC)
def _(ctx):
    """Theorem A2.4 where checkable: over F_q[t], q in {3,5,7,13}, no
    PRIMITIVE nonconstant 4-AP of squares with roots of deg <= bound; and
    the non-primitive nonconstant 4-AP over F_13[t] (scaled constant AP
    4,10,3,9) exists — the primitivity hypothesis is sharp."""
    plan = ({3: 2, 5: 2, 7: 2, 13: 1} if ctx.profile == "FULL"
            else {3: 1, 5: 1, 7: 1})
    for q, dmax in plan.items():
        sq = square_table(q, dmax + 1)
        found = []
        squares_list = [(g, mul(g, g, q)) for g in all_polys(q, dmax) if g]
        for B, B2 in squares_list:
            for c_, C2 in squares_list:
                A2 = sub(scale(B2, 2, q), C2, q)
                D2 = sub(scale(C2, 2, q), B2, q)
                if A2 in sq and D2 in sq:
                    if deg(gcd_poly(B, c_, q)) >= 1:
                        continue  # non-primitive
                    if max(deg(B), deg(c_), deg(sq[A2]), deg(sq[D2])) < 1:
                        continue  # constant
                    # distinctness of the four squares:
                    terms = {A2, B2, C2, D2}
                    if len(terms) == 4:
                        found.append((q, B, c_))
        require(not found, f"primitive nonconstant 4-AP found: {found[:2]}")
    # sharpness witness over F_13: (2g)^2,(6g)^2,(4g)^2,(3g)^2, g = t
    q = 13
    g = (0, 1)
    roots = [scale(g, k, q) for k in (2, 6, 4, 3)]
    sqs = [mul(x, x, q) for x in roots]
    d1 = sub(sqs[1], sqs[0], q)
    require(sub(sqs[2], sqs[1], q) == d1 and sub(sqs[3], sqs[2], q) == d1
            and d1, "F_13 scaled-constant 4-AP broken")
    require(len(set(sqs)) == 4)
    ctx.note("no primitive nonconstant 4-APs; F_13 non-primitive witness OK")


@check("a2.congruum_ff", DOC)
def _(ctx):
    """Theorem A2.5 where checkable: no primitive nonconstant 3-AP of
    squares with square common difference over F_q[t], q in {3,5,7,13};
    plus the F_7 scaled-constant witness (0, 4g^2, g^2), difference (2g)^2."""
    plan = ({3: 2, 5: 2, 7: 2, 13: 1} if ctx.profile == "FULL"
            else {3: 1, 5: 1, 7: 1})
    for q, dmax in plan.items():
        sq = square_table(q, dmax + 1)
        squares_list = [(g, mul(g, g, q)) for g in all_polys(q, dmax) if g]
        for B, B2 in squares_list:
            for C, C2 in squares_list:
                if deg(gcd_poly(B, C, q)) >= 1:
                    continue
                A2 = sub(scale(B2, 2, q), C2, q)
                T2 = sub(C2, B2, q)
                if A2 in sq and T2 in sq and T2:
                    if max(deg(B), deg(C), deg(sq[A2]), deg(sq[T2])) >= 1:
                        require(False, f"q={q}: primitive square-congruum "
                                       f"3-AP with (B,C)=({B},{C})")
    q, g = 7, (0, 1)
    g2 = mul(g, g, q)
    ap = [(), scale(g2, 4, q), g2]
    d1 = sub(ap[1], ap[0], q)
    require(sub(ap[2], ap[1], q) == d1 and d1 == scale(mul(g, g, q), 4, q))
    # 4g^2 = (2g)^2 is a square, and the three terms are squares 0^2,(2g)^2,g^2
    ctx.note("no primitive nonconstant square-congruum APs; F_7 witness OK")


@check("a2.mss3_ff_search", DOC)
def _(ctx):
    """Conjecture A2.C evidence: exhaustive-over-centers search finds no
    MSS3 with nonconstant center over F_q[t] in the ranges below."""
    table = ([(3, 3), (5, 3), (7, 2), (11, 2), (13, 2)]
             if ctx.profile == "FULL" else [(3, 2), (5, 2), (7, 1)])
    for q, dmax in table:
        hits = search(q, dmax)
        require(not hits, f"MSS3 over F_{q}[t] found: {hits[:2]}")
    ctx.note(f"no MSS3 with nonconstant center: {table}")
