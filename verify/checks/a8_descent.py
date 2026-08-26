"""Descent of symmetric differentials to the Lucas plane (A8, M11-A).

Verifies the structural facts, the engine's controls, and the two
headline computations: q = 0 (m = 1) and h^0(X - nodes, S^2 Omega^1)
= 0 (m = 2, all 256 characters).
"""

from fractions import Fraction as F
from itertools import combinations

from ..framework import Skip, check, require
from compute.descent_differentials import (GRID, character_orbits,
                                           eigenspace_dim,
                                           grid_symmetries, survey,
                                           validate_solution)

DOC = "docs/attacks/A8-descent-differentials.md"


@check("a8.structure", DOC)
def _(ctx):
    """The arrangement's structure: 8 triple points = the 8 grid
    lines-of-three; column/row pencil base points lie on v=0 / u=0;
    both '6 tangent lines of a smooth conic + 3-line pencil' splits."""
    # triples of concurrent lines <=> collinear grid triples
    coll = []
    for trip in combinations(GRID, 3):
        (a1, b1), (a2, b2), (a3, b3) = trip
        det = (a2 - a1) * (b3 - b1) - (a3 - a1) * (b2 - b1)
        if det == 0:
            coll.append(trip)
    require(len(coll) == 8, f"{len(coll)} grid lines-of-three")

    def common_point(lines):
        (l1, l2) = lines[:2]
        p = (l1[1] * l2[2] - l1[2] * l2[1],
             l1[2] * l2[0] - l1[0] * l2[2],
             l1[0] * l2[1] - l1[1] * l2[0])
        for L in lines:
            require(sum(x * y for x, y in zip(L, p)) == 0)
        return p

    for t in (-1, 0, 1):
        A = common_point([(1, a, b) for (a, b) in GRID if a == t])
        require(A[2] == 0, "column pencil base point off v=0")
        B = common_point([(1, a, b) for (a, b) in GRID if b == t])
        require(B[1] == 0, "row pencil base point off u=0")
    # conic splits (dual conics through six grid points)
    for sgn, pencil in ((1, [(0, 0), (1, -1), (-1, 1)]),
                        (-1, [(0, 0), (1, 1), (-1, -1)])):
        pts = [(1, a, b) for (a, b) in GRID if (a, b) not in pencil]
        require(len(pts) == 6)
        for (X, Y, Z) in pts:
            require(X * X - Y * Y - Z * Z + sgn * Y * Z == 0,
                    f"conic split fails at {(X, Y, Z)}")
        det = F(1) * (F(-1) * F(-1) - F(sgn, 2) * F(sgn, 2))
        require(det != 0, "dual conic not smooth")
    ctx.note("8 grid triples; pencils based on v=0/u=0; two conic splits")


@check("a8.quadric_control", DOC)
def _(ctx):
    """Two-line sub-cover = P^1 x P^1: no symmetric differentials in any
    character at m = 1, 2 (the engine's exactness control)."""
    L2 = [(1, 0), (-1, 0)]
    for m in (1, 2):
        require(eigenspace_dim((), m, lines=L2) == 0)
        require(eigenspace_dim(tuple(L2), m, lines=L2) == 0)
    ctx.note("quadric: all characters 0 at m=1,2")


@check("a8.infinity_trap", DOC)
def _(ctx):
    """The near-trap eta = dl_1 dl_2 (pullback 4 dx_1 dx_2, affinely
    regular) is rejected for exactly the right reason: an order-4 pole
    over u = 0, detected by the chart-2 side of the independent
    validator."""
    L2 = [(1, 0), (0, 1)]
    S = tuple(L2)
    dim, basis, unknowns, dN = eigenspace_dim(S, 2, return_basis=True,
                                              lines=L2)
    require(dim == 0, "quadric character unexpectedly nonzero")
    b1, b2 = 0, 1          # slopes of the two lines
    vec = [F(0)] * len(unknowns)
    coeffs = {2: F(1), 1: F(b1 + b2), 0: F(b1 * b2)}
    for t, (i, mono) in enumerate(unknowns):
        if mono == (0, 0) and coeffs.get(i, 0) != 0:
            vec[t] = coeffs[i]
    ok, reason = validate_solution(S, 2, vec, unknowns, dN, lines=L2)
    require(not ok, "validator accepted a form with a pole at infinity")
    require("u=0" in reason, f"wrong rejection reason: {reason}")
    ctx.note("dl1*dl2 rejected: pole over u=0 (validator chart-2 path)")


@check("a8.q_zero", DOC)
def _(ctx):
    """Theorem A8.2: q(X~) = h^0(X - nodes, Omega^1) = 0 -- every one of
    the 256 characters vanishes at m = 1 (saturation-checked).  This
    matches the classical Zariski/Esnault-Viehweg prediction (no even
    pencil sub-arrangements) and pins b_2 = 766, h^{1,1} = 544."""
    total, rows = survey(1, verbose=False)
    require(sum(o for _, o, _ in rows) == 256, "character count")
    require(total == 0, f"q = {total} != 0")
    ctx.note("q = 0: b_1=0, b_2 = 766, h^{1,1} = 544")


@check("a8.m2_survey", DOC)
def _(ctx):
    """Theorem A8.3: h^0(X - nodes, S^2 Omega^1) = 0 -- all 256
    characters vanish at m = 2.  FULL: all 51 orbits with saturation;
    FAST/CI: a fixed sample of orbits (zero-dimensionality pinned)."""
    if ctx.profile == "FULL":
        total, rows = survey(2, verbose=False)
        require(sum(o for _, o, _ in rows) == 256, "character count")
        require(total == 0, f"h^0(S^2) = {total} != 0")
        ctx.note("all 51 orbits: h^0(X-nodes, S^2 Omega^1) = 0 "
                 "(vs cuboid's 13)")
    else:
        sample = [(), ((0, 0), (1, 1)), ((1, 0), (-1, 0)),
                  ((1, 0), (-1, 0), (0, 1), (0, -1)),
                  ((0, 0), (1, 0), (0, 1), (1, 1)),
                  tuple(ab for ab in GRID if ab != (0, 0))]
        for S in sample:
            require(len(S) % 2 == 0)
            require(eigenspace_dim(S, 2) == 0, f"V_S != 0 at {S}")
        ctx.note(f"sampled {len(sample)} characters: all zero at m=2")


@check("a8.orbit_equivariance", DOC)
def _(ctx):
    """The solver is equivariant: dims agree across an entire symmetry
    orbit of characters (catches any line-indexing asymmetry)."""
    S0 = frozenset({(0, 0), (1, 1)})
    orbit = sorted({frozenset(f(ab) for ab in S0)
                    for f in grid_symmetries()}, key=str)
    members = orbit if ctx.profile == "FULL" else orbit[:3]
    dims = {eigenspace_dim(tuple(sorted(Sm)), 2) for Sm in members}
    require(len(dims) == 1, f"orbit dims differ: {dims}")
    require(len(orbit) > 1)
    ctx.note(f"orbit of size {len(orbit)}: constant dim {dims.pop()}")


@check("a8.character_bookkeeping", DOC)
def _(ctx):
    """51 orbits cover exactly the 256 even characters."""
    orbs = character_orbits()
    require(len(orbs) == 51, f"{len(orbs)} orbits")
    require(sum(o for _, o in orbs) == 256)
    require(all(len(k) % 2 == 0 for k, _ in orbs))
    ctx.note("51 symmetry orbits covering all 256 even characters")
