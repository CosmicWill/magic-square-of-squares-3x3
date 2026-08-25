"""Mechanical verification for docs/attacks/A4-eight-squares.md."""

import shutil
import subprocess
from fractions import Fraction
from math import isqrt

from ..framework import Skip, check, require
from ..targets import AB1, is_square
from compute.eight_square_search import census_entries, dtilde, sweep

DOC = "docs/attacks/A4-eight-squares.md"


@check("a4.taxonomy", DOC)
def _(ctx):
    """Theorem A4.1: D4 orbits on the nine cells are {center}, corners,
    edge-midpoints, of sizes 1, 4, 4."""
    cells = [(i, j) for i in range(3) for j in range(3)]

    def rot(c):
        i, j = c
        return (j, 2 - i)

    def refl(c):
        i, j = c
        return (j, i)

    group = set()
    frontier = [tuple(cells)]
    ident = tuple(cells)
    group.add(ident)
    changed = True
    perms = {ident}
    while changed:
        changed = False
        for g in list(perms):
            for f in (rot, refl):
                ng = tuple(f(c) for c in g)
                if ng not in perms:
                    perms.add(ng)
                    changed = True
    require(len(perms) == 8, f"D4 should have 8 elements, got {len(perms)}")
    orbits = []
    seen = set()
    for c in cells:
        if c in seen:
            continue
        idx = cells.index(c)
        orb = {g[idx] for g in perms}
        seen |= orb
        orbits.append(len(orb))
    require(sorted(orbits) == [1, 4, 4], f"orbit sizes {orbits}")


@check("a4.sweep", DOC)
def _(ctx):
    """The class-enabler sweep: no quadruples, no K-patterns, and every
    additive triple sits at a NON-square center (cross-validating A3.3
    with an independent implementation)."""
    bound = ctx.bound(full=60000, fast=8000)
    quads, triples, kpat, sevens = sweep(bound)
    require(quads == [], f"quadruple found: {quads[:2]}")
    require(kpat == [], f"class-K pattern found: {kpat[:2]}")
    for (c, d1, d2) in triples:
        require(not is_square(c), f"triple at SQUARE center {c} — "
                                  f"contradicts A3.3!")
    require(all(nsq < 7 or c > bound for (c, u, v, nsq) in sevens) or
            sevens == [], "unexpected >=7-square configuration")
    ctx.note(f"triples found: {len(triples)}, all at non-square centers")


@check("a4.ab1_refound", DOC)
def _(ctx):
    """Validation criterion: the census machinery at c = 425^2 re-finds
    AB1 — some pair/form yields exactly 7 squares with AB1's entry set."""
    c = 425 ** 2
    D = dtilde(c)
    require(138600 in D and 97104 in D, "AB1 congrua missing from Dtilde")
    hits = []
    for d_a in D:
        for d_b in D:
            if d_a == d_b:
                continue
            forms = [(d_b, d_a), (d_b - d_a, d_a), (d_a + d_b, d_a)]
            if (d_a + d_b) % 2 == 0:
                forms.append(((d_a + d_b) // 2, (d_a - d_b) // 2))
            for (u, v) in forms:
                ents = census_entries(c, u, v)
                if len(set(ents)) == 9 and min(ents) >= 0:
                    nsq = sum(is_square(e) for e in ents)
                    if nsq >= 7:
                        hits.append((u, v, nsq, sorted(ents)))
    require(hits, "census failed to re-find AB1")
    require(all(nsq == 7 for (_, _, nsq, _) in hits), "impossible 8+ found")
    require(any(ents == sorted(AB1) for (_, _, _, ents) in hits),
            "re-found configuration is not AB1")
    ctx.note(f"AB1 re-found; {len(hits)} (u,v)-presentations, all 7 squares")


@check("a4.triple_157441", DOC)
def _(ctx):
    """The non-square-center additive triple, digit by digit."""
    c = 157441
    require(not is_square(c))
    D = set(dtilde(c))
    require({19800, 135240, 155040} <= D and 19800 + 135240 == 155040)
    for d, (lo, hi) in [(19800, (371, 421)), (135240, (149, 541)),
                        (155040, (49, 559))]:
        require(c - d == lo * lo and c + d == hi * hi, f"d={d}")
    # non-squares exactly at center and the u-v pair:
    u, v = 135240, 19800
    require(not is_square(c - (u - v)) and not is_square(c + (u - v)))
    ents = census_entries(c, u, v)
    require(sum(is_square(e) for e in ents) == 6 and len(set(ents)) == 9)


def qpoly(x):
    return (1681 * x ** 4 - 28900 * x ** 3 + 3362 * x ** 2
            + 28900 * x + 1681)


@check("a4.fiber_algebra", DOC)
def _(ctx):
    """The AB1 fiber: A = (41/85)^2 at t1 = 7/11; the scaled quartic
    identity; q(7/11) and q(3/4) are rational squares; d(3/4)*425^2 =
    97104."""
    t1 = Fraction(7, 11)
    A = 1 - 4 * t1 * (1 - t1 ** 2) / (1 + t1 ** 2) ** 2
    require(A == Fraction(41, 85) ** 2, f"A = {A}")
    for xi in range(-4, 5):  # degree-4 identity: 9 points is ample
        x = Fraction(xi)
        require(qpoly(x) == 85 ** 2 * (A * (1 + x ** 2) ** 2
                                       + 4 * x * (1 - x ** 2)),
                "scaled quartic identity")

    def is_rat_square(f):
        f = Fraction(f)
        return (f >= 0 and isqrt(f.numerator) ** 2 == f.numerator
                and isqrt(f.denominator) ** 2 == f.denominator)

    require(is_rat_square(qpoly(Fraction(7, 11))), "q(7/11) not square")
    q34 = qpoly(Fraction(3, 4))
    require(q34 == Fraction(1865, 16) ** 2 and 1865 == 5 * 373)
    t2 = Fraction(3, 4)
    d = 4 * t2 * (1 - t2 ** 2) / (1 + t2 ** 2) ** 2 * 425 ** 2
    require(d == 97104, f"d(3/4)*425^2 = {d}")


@check("a4.pari_fiber", DOC)
def _(ctx):
    """PARI: the fiber's Jacobian and certified rank 3 (SKIP without gp)."""
    if not shutil.which("gp"):
        raise Skip("PARI/GP not installed")
    script = ("E = ellfromeqn(y^2 - (1681*x^4 - 28900*x^3 + 3362*x^2"
              " + 28900*x + 1681)); print(E); Ei = ellinit(E);"
              " r = ellrank(Ei); print(r[1], \";\", r[2]);"
              " print(elltors(Ei)[2])")
    out = subprocess.run(["gp", "-q"], input=script, text=True,
                         capture_output=True, timeout=600).stdout
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    require(lines[0] == "[0, 3362, 0, -846513044, 2769975186072]",
            f"Weierstrass model changed: {lines[0]}")
    require(lines[1] == "3;3", f"rank not certified 3: {lines[1]}")
    require(lines[2] == "[2, 2]", f"torsion: {lines[2]}")
    ctx.note("Jacobian confirmed; ellrank certifies rank 3, torsion (Z/2)^2")
