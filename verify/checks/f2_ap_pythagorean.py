"""Mechanical verification for docs/foundations/F2-aps-and-pythagorean.md."""

from math import isqrt

from ..framework import check, require
from ..targets import AB1_LUCAS, congrua, is_square, proper_decompositions

DOC = "docs/foundations/F2-aps-and-pythagorean.md"


def congrua_via_aps(m):
    """D(m) computed from the AP definition: d > 0 with m^2 +- d both square."""
    out = set()
    m2 = m * m
    q = m + 1
    while q * q < 2 * m2:
        d = q * q - m2
        if is_square(m2 - d):
            out.add(d)
        q += 1
    return out


def odd_part_factor_product(m):
    """prod (2a_i + 1) over primes p == 1 (mod 4) dividing m."""
    prod = 1
    n = m
    p = 2
    while p * p <= n:
        if n % p == 0:
            a = 0
            while n % p == 0:
                n //= p
                a += 1
            if p % 4 == 1:
                prod *= 2 * a + 1
        p += 1
    if n > 1 and n % 4 == 1:
        prod *= 3
    return prod


@check("f2.dictionary", DOC)
def _(ctx):
    """F2.2/F2.3: decomposition-congrua equal AP-congrua, exhaustively."""
    bound = ctx.bound(full=2000, fast=300)
    for m in range(1, bound + 1):
        require(congrua(m) == congrua_via_aps(m), f"dictionary fails at m={m}")
    ctx.note("D(m) from 2ef == D(m) from APs for all m <= bound")


@check("f2.counting", DOC)
def _(ctx):
    """F2.4/F2.6: |D(m)| = #proper decompositions = (prod(2a_i+1)-1)/2."""
    bound = ctx.bound(full=2000, fast=300)
    for m in range(1, bound + 1):
        pd = proper_decompositions(m)
        formula = (odd_part_factor_product(m) - 1) // 2
        require(len(congrua(m)) == len(pd) == formula, f"count fails at m={m}")


@check("f2.threshold", DOC)
def _(ctx):
    """F2.7: no m < 65 has four congrua; 65 and 5^4 do."""
    for m in range(1, 65):
        require(len(congrua(m)) < 4, f"m={m} < 65 has 4 congrua")
    require(len(congrua(65)) >= 4, "m=65 should have 4 congrua")
    require(len(congrua(625)) >= 4, "m=5^4 should have 4 congrua")
    ctx.note(f"|D(65)|={len(congrua(65))}, |D(625)|={len(congrua(625))}")


@check("f2.offsets_distinct", DOC)
def _(ctx):
    """Remark after F2.5: F1.3 distinctness implies |u|,|v|,|u+v|,|u-v|
    pairwise distinct (randomized sweep over a full small box)."""
    for u in range(-30, 31):
        for v in range(-30, 31):
            prod = (u * v * (u - v) * (u + v) * (u - 2 * v) * (u + 2 * v)
                    * (2 * u - v) * (2 * u + v))
            if prod != 0:
                four = {abs(u), abs(v), abs(u + v), abs(u - v)}
                require(len(four) == 4, f"offsets collide at (u,v)=({u},{v})")


@check("f2.anchor_ab1", DOC)
def _(ctx):
    """AB1's structure in the F2 dictionary: exactly two of its four offsets
    are congrua of 425 (giving 4 outer squares), the other two offsets each
    have exactly one square endpoint (giving 2 more), plus the center: 7."""
    c, u, v = AB1_LUCAS["c"], AB1_LUCAS["u"], AB1_LUCAS["v"]
    require(c == 425 ** 2)
    D = congrua(425)
    require(abs(v) in D and abs(u + v) in D, "AB1 realized congrua missing")
    require(abs(u) not in D and abs(u - v) not in D, "AB1 unrealized congrua present")
    # one-sided squareness of the two failed offsets:
    require(is_square(c + u) and not is_square(c - u))
    require(is_square(c + (u - v)) and not is_square(c - (u - v)))
    # the Gaussian points on the circle N(z) = 425^2 for the realized congrua:
    for (e, f), d in [((180, 385), abs(v)), ((119, 408), abs(u + v))]:
        require(e * e + f * f == 425 ** 2 and 2 * e * f == d,
                f"Gaussian point ({e},{f}) wrong")
    sq = sum(is_square(x) for x in
             [c, c + u, c - u, c + v, c - v, c + u + v, c - u - v,
              c + u - v, c - u + v])
    require(sq == 7, f"AB1 should have exactly 7 squares, got {sq}")
    ctx.note("AB1: offsets |v|,|u+v| in D(425); |u|,|u-v| half-realized")
