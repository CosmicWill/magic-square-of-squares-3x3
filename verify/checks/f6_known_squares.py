"""Mechanical verification for docs/foundations/F6-known-squares.md."""

from math import isqrt

from ..framework import check, require
from .. import targets
from ..targets import congrua, is_square

DOC = "docs/foundations/F6-known-squares.md"


@check("f6.ab1", DOC)
def _(ctx):
    """AB1: 8 equal lines, exactly 7 squares, the 2 named non-squares,
    9 distinct entries, center = S/3."""
    sq = targets.AB1
    sums = targets.line_sums(sq, targets.LINES_3)
    require(all(s == targets.AB1_MAGIC_SUM for s in sums), f"line sums {sums}")
    require(len(set(sq)) == 9, "entries not distinct")
    for i, x in enumerate(sq):
        if i in targets.AB1_NONSQUARE_INDICES:
            require(not is_square(x), f"index {i} unexpectedly square")
        else:
            require(is_square(x), f"index {i} not a square")
    require(sq[4] * 3 == targets.AB1_MAGIC_SUM, "center != S/3")
    r = isqrt(360721)
    ctx.note(f"360721 between {r}^2={r*r} and {r+1}^2={(r+1)**2}")


@check("f6.euler4", DOC)
def _(ctx):
    """Euler's 4x4: 10 equal lines, 16 distinct squares."""
    sq = targets.EULER4
    sums = targets.line_sums(sq, targets.LINES_4)
    require(all(s == targets.EULER4_MAGIC_SUM for s in sums), f"line sums {sums}")
    require(len(set(sq)) == 16, "entries not distinct")
    require(all(is_square(x) for x in sq), "non-square entry")


@check("f6.d425", DOC)
def _(ctx):
    """|D(425)| = 7, and the center 425^2 admits NO magic square of squares:
    no pair d1, d2 in D(425) has both |d1+d2| and |d1-d2| in D(425)."""
    D = congrua(425)
    require(len(D) == 7, f"|D(425)| = {len(D)}")
    require(138600 in D and 97104 in D and 41496 not in D and 180096 not in D)
    for d1 in D:
        for d2 in D:
            if d1 == d2:
                continue
            require(not (abs(d1 + d2) in D and abs(d1 - d2) in D),
                    f"center 425^2 would admit an MSS3 via ({d1},{d2})!")
    ctx.note("D(425) supports no additive quadruple => no MSS3 with center 425^2")
