"""Mechanical verification for docs/foundations/F3-no-four-term-ap.md."""

from itertools import product
from math import gcd, isqrt

from ..framework import check, require
from ..targets import congrua, is_square

DOC = "docs/foundations/F3-no-four-term-ap.md"


@check("f3.no_four_ap", DOC)
def _(ctx):
    """Theorem F3.3, exhaustively: no 4 distinct squares in AP with roots
    up to the bound."""
    bound = ctx.bound(full=3000, fast=400)
    for q in range(2, bound + 1):
        q2 = q * q
        for p in range(1, q):
            delta = q2 - p * p
            r2 = q2 + delta
            if not is_square(r2):
                continue
            if is_square(r2 + delta):
                require(False, f"4-AP found: p={p}, q={q}, delta={delta}")
    ctx.note("no 4-term AP of distinct squares with roots <= bound")


@check("f3.identities", DOC)
def _(ctx):
    """The reduction chain's polynomial identities, proved by complete-grid
    evaluation (degree <= 4 per variable => evaluating on 5 points per
    variable, e.g. {0..4}, is a proof; we use {0..4}^4)."""
    R = range(5)
    # F3.3a parametrization identity
    for a, b in product(R, repeat=2):
        require((a * a - b * b - 2 * a * b) ** 2 + (a * a - b * b + 2 * a * b) ** 2
                == 2 * (a * a + b * b) ** 2, "parametrization identity")
    for w, al, ga, ta in product(R, repeat=4):
        # Case epsilon = +1 identity (F3.3b)
        a, c = w * al, w * ga
        b, d = ga * ta - w * al, w * ga - al * ta
        lhs = b * (a - b) - d * (c + d)
        rhs = 6 * w * al * ga * ta - (al * al + ga * ga) * (2 * w * w + ta * ta)
        require(lhs == rhs, "case +1 identity")
        # Case epsilon = -1 identity (F3.3b), variables (x,y,z) := (al,ga,ta)
        x, y, z = al, ga, ta
        dd, aa = w * x, w * y
        cc, bb = y * z - w * x, x * z - w * y
        lhs2 = cc * (cc - dd) - bb * (aa - bb)
        rhs2 = (x * x + y * y) * (2 * w * w + z * z) - 6 * w * x * y * z
        require(lhs2 == rhs2, "case -1 identity")
        # F3.3d consequence identities (unconditional forms)
        E1 = al * al + ga * ga - 2 * w * ta
        E2 = 3 * al * ga - (2 * w * w + ta * ta)
        require(3 * (al + ga) ** 2 - 2 * (w + ta) * (2 * w + ta) == 3 * E1 + 2 * E2,
                "s' identity")
        require(3 * (al - ga) ** 2 - 2 * (ta - w) * (2 * w - ta) == 3 * E1 - 2 * E2,
                "t' identity")
    ctx.note("all reduction identities vanish on complete grids")


@check("f3.diamond_box", DOC)
def _(ctx):
    """(diamond) box search: the only pairwise-coprime positive solutions of
    (alpha^2+gamma^2)(2w^2+tau^2) = 6 w alpha gamma tau in the box are
    (1,1,1,1) and (1,1,1,2), both violating the side conditions."""
    B = ctx.bound(full=40, fast=16)
    found = []
    for al in range(1, B + 1):
        for ga in range(al, B + 1):
            if gcd(al, ga) != 1:
                continue
            s2 = al * al + ga * ga
            p6 = 6 * al * ga
            for w in range(1, B + 1):
                if gcd(w, al) != 1 or gcd(w, ga) != 1:
                    continue
                for ta in range(1, B + 1):
                    if s2 * (2 * w * w + ta * ta) == p6 * w * ta:
                        if gcd(ta, w) == 1 and gcd(ta, al) == 1 and gcd(ta, ga) == 1:
                            found.append((al, ga, w, ta))
    require(set(found) == {(1, 1, 1, 1), (1, 1, 1, 2)}, f"unexpected: {found}")
    # side conditions: (1,1,1,1) has b = gamma*tau - w*alpha = 0 (degenerate);
    # (1,1,1,2) has tau even (parity violation).
    require(1 * 1 - 1 * 1 == 0 and 2 % 2 == 0)
    ctx.note("only degenerate solutions in box; each violates side conditions")


@check("f3.concordant_and_quartic", DOC)
def _(ctx):
    """F3.3d/e targets: no nontrivial concordant pair a^2+b^2 = square,
    4a^2+b^2 = square (a even, b odd, coprime); no nontrivial point on
    r^4 - r^2 s^2 + s^4 = square (coprime, opposite parity)."""
    B = ctx.bound(full=2000, fast=300)
    for a in range(2, B + 1, 2):
        a2 = a * a
        for b in range(1, B + 1, 2):
            if gcd(a, b) == 1 and is_square(a2 + b * b):
                require(not is_square(4 * a2 + b * b),
                        f"concordant pair a={a}, b={b}")
    BQ = ctx.bound(full=600, fast=150)
    for r in range(1, BQ + 1):
        for s in range(r + 1, BQ + 1):
            if (r + s) % 2 == 1 and gcd(r, s) == 1:
                require(not is_square(r ** 4 - r * r * s * s + s ** 4),
                        f"(Q) solution r={r}, s={s}")
    ctx.note("no concordant pair, no (Q) point, in boxes")


@check("f3.frt_chain", DOC)
def _(ctx):
    """F3.2 chain, searched: no x^4 - y^4 = z^2; no primitive Pythagorean
    triangle with square area; no square congruum."""
    B = ctx.bound(full=400, fast=120)
    for x in range(2, B + 1):
        x4 = x ** 4
        for y in range(1, x):
            require(not is_square(x4 - y ** 4), f"FRT fails: x={x}, y={y}")
    Bm = ctx.bound(full=150, fast=60)
    for m in range(2, Bm + 1):
        for n in range(1, m):
            if (m + n) % 2 == 1 and gcd(m, n) == 1:
                require(not is_square(m * n * (m - n) * (m + n)),
                        f"square area: m={m}, n={n}")
    Bc = ctx.bound(full=500, fast=150)
    for m in range(1, Bc + 1):
        for d in congrua(m):
            require(not is_square(d), f"square congruum d={d} of m={m}")
    ctx.note("FRT, square-area, square-congruum all confirmed absent")


@check("f3.collinear_kill", DOC)
def _(ctx):
    """Corollary F3.4 mechanics: v = 3u makes the nine Lucas offsets the
    full 9-term AP -4u..4u."""
    u = 7  # arbitrary nonzero; the offset structure is linear in u
    v = 3 * u
    offsets = {0, u, -u, v, -v, u + v, -(u + v), u - v, -(u - v)}
    require(offsets == {k * u for k in range(-4, 5)}, "collinear offsets")
