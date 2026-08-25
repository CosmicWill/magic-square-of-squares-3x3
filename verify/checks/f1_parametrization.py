"""Mechanical verification for docs/foundations/F1-parametrization.md."""

from fractions import Fraction
from itertools import combinations, product

from ..framework import check, require
from .. import targets

DOC = "docs/foundations/F1-parametrization.md"


def lucas(c, u, v):
    """The Lucas grid L(c,u,v), row-major (F1.1)."""
    return [
        c + u, c - u - v, c + v,
        c - u + v, c, c + u - v,
        c - v, c + u + v, c - u,
    ]


@check("f1.identity", DOC)
def _(ctx):
    """(<=) direction: every line of L(c,u,v) sums to 3c, as a polynomial
    identity.  Each line sum minus 3c has degree <= 1 in each of c,u,v, and a
    polynomial of degree <= d_i in variable i that vanishes on a grid with
    d_i+1 points per variable is identically zero (Lagrange interpolation on
    product grids).  We evaluate on {0,1,2}^3 — more points than needed."""
    for c, u, v in product(range(3), repeat=3):
        sq = lucas(c, u, v)
        for line in targets.LINES_3:
            require(
                sum(sq[i] for i in line) == 3 * c,
                f"line {line} fails at (c,u,v)=({c},{u},{v})",
            )
    ctx.note("8 line identities vanish on {0,1,2}^3 => identically zero")


@check("f1.necessity", DOC)
def _(ctx):
    """(=>) direction over Q, by exact linear algebra: the 8 homogeneous magic
    equations in (a11..a33, S) have solution space of dimension exactly 3,
    spanned by the three Lucas directions."""
    # rows of the system: for each line, sum(entries) - S = 0.
    rows = []
    for line in targets.LINES_3:
        r = [Fraction(0)] * 10
        for i in line:
            r[i] = Fraction(1)
        r[9] = Fraction(-1)
        rows.append(r)

    # exact row-reduction
    mat = [row[:] for row in rows]
    rank, pivot_col = 0, 0
    while rank < len(mat) and pivot_col < 10:
        piv = next((r for r in range(rank, len(mat)) if mat[r][pivot_col] != 0), None)
        if piv is None:
            pivot_col += 1
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        mat[rank] = [x / mat[rank][pivot_col] for x in mat[rank]]
        for r in range(len(mat)):
            if r != rank and mat[r][pivot_col] != 0:
                f = mat[r][pivot_col]
                mat[r] = [a - f * b for a, b in zip(mat[r], mat[rank])]
        rank += 1
        pivot_col += 1
    require(rank == 7, f"magic system has rank {rank}, expected 7 (=> nullity 3)")

    # the three Lucas directions solve the system and are independent
    dirs = [
        lucas(1, 0, 0) + [3],   # dC (S = 3c)
        lucas(0, 1, 0) + [0],   # dU
        lucas(0, 0, 1) + [0],   # dV
    ]
    for d in dirs:
        for row in rows:
            require(sum(a * b for a, b in zip(row, d)) == 0, "Lucas direction not in kernel")
    # independence: entries (a22, a11, a13) of the three directions form
    # the matrix [[1,1,1],[0,1,0],[0,0,1]] (columns c,u,v), visibly invertible.
    require(dirs[0][4] == 1 and dirs[1][4] == 0 and dirs[2][4] == 0, "independence")
    require(dirs[1][0] == 1 and dirs[2][2] == 1, "independence")
    ctx.note("rank 7 of 10 unknowns => 3-dim kernel, spanned by Lucas directions")


@check("f1.distinctness", DOC)
def _(ctx):
    """Lemma F1.3: entries pairwise distinct iff
    u*v*(u-v)*(u+v)*(u-2v)*(u+2v)*(2u-v)*(2u+v) != 0.
    Verified by enumerating all 36 offset differences symbolically as integer
    vectors (alpha, beta) meaning alpha*u + beta*v, and checking the set of
    differences equals (up to sign and, for the pair {(1,1),(1,-1)} arising
    twice, multiplicity) the factor list; plus randomized cross-check."""
    offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
               (1, 1), (-1, -1), (1, -1), (-1, 1)]
    factors = {(1, 0), (0, 1), (1, -1), (1, 1), (1, -2), (1, 2), (2, -1), (2, 1)}

    def normalize(a, b):
        if a < 0 or (a == 0 and b < 0):
            a, b = -a, -b
        from math import gcd
        g = gcd(abs(a), abs(b)) or 1
        return (a // g, b // g)

    diffs = {normalize(x1 - x2, y1 - y2)
             for (x1, y1), (x2, y2) in combinations(offsets, 2)}
    require(diffs == factors, f"difference directions {diffs} != factors {factors}")

    # randomized: distinctness of the 9 entries <=> product of factors nonzero
    import random
    rng = random.Random(20260825)
    for _ in range(2000):
        u = rng.randint(-6, 6)
        v = rng.randint(-6, 6)
        prod = u * v * (u - v) * (u + v) * (u - 2 * v) * (u + 2 * v) * (2 * u - v) * (2 * u + v)
        distinct = len(set(lucas(0, u, v))) == 9
        require((prod != 0) == distinct, f"F1.3 fails at (u,v)=({u},{v})")
    ctx.note("36 pairwise differences reduce exactly to the 8 factors")


@check("f1.anchor_ab1", DOC)
def _(ctx):
    """AB1 is exactly L(c,u,v) with c=425^2, u=373^2-c, v=565^2-c."""
    p = targets.AB1_LUCAS
    require(lucas(p["c"], p["u"], p["v"]) == targets.AB1, "AB1 != L(c,u,v)")
    ctx.note(f"AB1 = L({p['c']}, {p['u']}, {p['v']})")
