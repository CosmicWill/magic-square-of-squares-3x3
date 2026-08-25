"""Mechanical verification for docs/attacks/A5-surface-geometry.md."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd

from ..framework import check, require
from ..targets import LINES_3

DOC = "docs/attacks/A5-surface-geometry.md"

# the nine entry lines as covectors on (c, u, v), row-major Lucas order
ENTRY_LINES = [(1, 1, 0), (1, -1, -1), (1, 0, 1),
               (1, -1, 1), (1, 0, 0), (1, 1, -1),
               (1, 0, -1), (1, 1, 1), (1, -1, 0)]


@check("a5.model", DOC)
def _(ctx):
    """The seven line-sum difference quadrics span rank exactly 6."""
    vecs = []
    for k in range(1, 8):
        v = [0] * 9
        for i in LINES_3[0]:
            v[i] += 1
        for i in LINES_3[k]:
            v[i] -= 1
        vecs.append([Fraction(x) for x in v])
    rows = [r[:] for r in vecs]
    rank = 0
    for col in range(9):
        piv = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        rows[rank] = [x / rows[rank][col] for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    require(rank == 6, f"quadric rank {rank} != 6")
    ctx.note("X is cut by exactly 6 independent quadrics; dim X = 8-6 = 2")


@check("a5.arrangement", DOC)
def _(ctx):
    """The branch arrangement of the nine entry lines has exactly 8 triple
    points and 12 double points, the triples as listed in the doc."""
    def norm(p):
        g = 0
        for x in p:
            g = gcd(g, abs(x))
        p = tuple(x // g for x in p)
        for x in p:
            if x:
                return p if x > 0 else tuple(-y for y in p)
        return p

    pts = {}
    n = len(ENTRY_LINES)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = ENTRY_LINES[i], ENTRY_LINES[j]
            cr = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                  a[0] * b[1] - a[1] * b[0])
            pts.setdefault(norm(cr), set()).update((i, j))
    mult = Counter(len(s) for s in pts.values())
    require(dict(mult) == {3: 8, 2: 12}, f"arrangement {dict(mult)}")
    triples = {p for p, s in pts.items() if len(s) == 3}
    expect = {(0, 0, 1), (0, 1, 0), (0, 1, -1), (0, 1, 1),
              (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1)}
    require(triples == expect, f"triple points {triples}")


@check("a5.fp_counts", DOC)
def _(ctx):
    """The F_p point counts of X, 64-divisibility, and (via F5.3) the
    emptiness of the nondegenerate locus for p < 59."""
    expected = {5: 320, 7: 384, 11: 1280, 13: 1344}
    if ctx.profile == "FULL":
        expected.update({17: 1536, 19: 2304, 23: 2944})
    for p, want in expected.items():
        chi = [0] * p
        for x in range(1, p):
            chi[x * x % p] = 1
        N = 0
        for c, u, v in product(range(p), repeat=3):
            prod_ = 1
            for (a, b, d) in ENTRY_LINES:
                e = (a * c + b * u + d * v) % p
                prod_ *= 1 if e == 0 else (2 if chi[e] else 0)
                if not prod_:
                    break
            N += prod_
        count = (N - 1) // (p - 1)
        require(count == want, f"#X(F_{p}) = {count} != {want}")
        require(count % 64 == 0, f"64 does not divide #X(F_{p})")
    ctx.note(f"counts confirmed: {expected}; nondegenerate locus empty for "
             "p < 59 per f5.fp_scan")
