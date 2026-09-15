"""Exact certificate and scope controls for AD.1--AD.3."""

from fractions import Fraction as Q
from functools import reduce
from itertools import product
from math import gcd, isqrt, lcm

from ..framework import check, require
from ..targets import LINES_3, is_magic
from compute import arithmetic_descent_probe as a
from compute import universal_twist_probe as u
from compute.formal_boundary_probe import rational_root

DOC = "docs/research/arithmetic-descent-audit.md"


@check("ard.divisor_identities", DOC)
def divisor_identities(ctx):
    # Exact polynomial identity certificate: after clearing (2rs)^2,
    # every residual has degree at most 4 in each of n,r,s. Five distinct
    # values in each variable therefore suffice, without symbolic software.
    for n, r, s in product(range(1, 6), repeat=3):
        x, w = Q(n*n+r*r, 2*r), Q(n*n-r*r, 2*r)
        z, y = Q(n*n+s*s, 2*s), Q(n*n-s*s, 2*s)
        m2 = n*n+y*y+w*w
        uu, vv = 2*x*y, 2*z*w
        require(x*x == n*n+w*w and z*z == n*n+y*y)
        require((x+y)**2 == m2+uu and (x-y)**2 == m2-uu)
        require((z+w)**2 == m2+vv and (z-w)**2 == m2-vv)
        require(uu+vv == Q(n**4-r*r*s*s, r*s))
        require(uu-vv == Q(n*n*(r*r-s*s), r*s))
        targets = (m2, m2-uu-vv, m2-uu+vv, m2+uu-vv, m2+uu+vv)
        require(tuple(4*r*r*s*s*t for t in targets) == a.scaled_square_targets(n, r, s))
    ctx.note("5^3 rational evaluations certify all displayed polynomial identities (individual degree <=4 after clearing denominators)")


@check("ard.ap_divisor_roundtrip", DOC)
def ap_divisor_roundtrip(ctx):
    bound = ctx.bound(full=24, fast=10)
    count = 0
    for denominator in range(2, bound+1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) != 1:
                continue
            original = u.canonical_twists(u.primitive_ap_grid(numerator, denominator))
            aa, _, cc, _, m, _, gg, _, ii = original["roots"]
            n = rational_root(Q(aa*ii+cc*gg, 2))
            require(n.denominator == 1)
            n = n.numerator
            x, y = abs((aa+ii)//2), abs((aa-ii)//2)
            z, w = abs((cc+gg)//2), abs((cc-gg)//2)
            data = a.divisor_model(n, x-w, z-y)
            require(tuple(data[k] for k in ("x", "y", "z", "w")) == (x, y, z, w))
            require(data["center_squared"] == m*m and data["primitive"])
            require(sorted(data["entries"]) == sorted(r*r for r in original["roots"]))
            require(all(t >= 0 and isqrt(t)**2 == t for t in data["sides"]))
            require(is_magic(data["entries"], LINES_3))
            require(not (data["y"] and data["w"]), "AP degeneracies must be retained explicitly")
            require(2*m*m <= n**4+1)
            count += 1
    ctx.note(f"{count} canonical primitive AP grids round-trip through the divisor model, including signs and zero half-differences")


@check("ard.five_square_is_not_full", DOC)
def five_square_is_not_full(ctx):
    data = a.divisor_model(399, 147, 19)
    require(tuple(data[k] for k in ("x", "y", "z", "w")) == (615, 4180, 4199, 468))
    require(data["center_squared"] == 4225**2 and data["primitive"])
    require(data["corner_roots"] == (4795, 4667, 3731, -3565))
    entries = data["entries"]
    require(len(set(entries)) == 9 and min(entries) > 0 and is_magic(entries, LINES_3))
    require(tuple(entries[j] for j in (0, 2, 6, 8)) == tuple(t*t for t in data["corner_roots"]))
    require(data["sides"] == (8778961, 16639489, 19061761, 26922289))
    require(all(isqrt(t)**2 != t for t in data["sides"]))
    roots = data["corner_roots"]
    require((roots[0]*roots[3]+roots[1]*roots[2])//2 == 399**2)
    require(2*data["center_squared"] <= 399**4+1)
    ctx.note("n=399,m=4225: nine positive distinct magic entries, exactly five squares; none of its four sides is square")


@check("ard.linear_boundary_span", DOC)
def linear_boundary_span(ctx):
    signs = tuple(a.boundary_signs())
    require(len(signs) == 128)
    for roots in signs:
        require(is_magic(tuple(t*t for t in roots), LINES_3))
        require(roots[0]*roots[8]+roots[2]*roots[6] == 0)
    gram = tuple(tuple(sum(row[j]*row[k] for row in signs) for k in range(9)) for j in range(9))
    require(gram == tuple(tuple(128 if j == k else 0 for k in range(9)) for j in range(9)))
    require(a.exact_rank(signs) == 9)
    ctx.note("128 real n=0 grids; exact Gram matrix 128*I_9 forces the old-root part of every output linear form to vanish")


@check("ard.quadratic_boundary_kernel", DOC)
def quadratic_boundary_kernel(ctx):
    points = tuple(a.boundary_points())
    require(len(points) == 384)
    for roots in points:
        squares = tuple(a.radical_product(t, t) for t in roots)
        require(all(mask == 0 for _, mask in squares))
        require(is_magic(tuple(t for t, _ in squares), LINES_3))
        ai, cg = a.radical_product(roots[0], roots[8]), a.radical_product(roots[2], roots[6])
        require(ai[1] == cg[1] and ai[0]+cg[0] == 0)
    # Independence of the 16 radical basis elements follows from unique
    # prime factorization; the complete squarefree products are distinct.
    radicands = {prod_subset(mask) for mask in range(16)}
    require(len(radicands) == 16)
    rows, quadrics = a.quadratic_boundary_rows(), a.boundary_quadrics()
    require(len(rows) == 284 and len(a.MONOMIALS) == 45)
    require(a.exact_rank(rows) == 38 and a.exact_rank(quadrics) == 7)
    require(all(sum(x*y for x, y in zip(row, q)) == 0 for row in rows for q in quadrics))
    ctx.note("384 real algebraic points -> 284 rational rows, rank 38; kernel is exactly six magic quadrics plus ai+cg")


def prod_subset(mask):
    value = 1
    for j, p in enumerate(a.RADICAL_PRIMES):
        if mask & (1 << j):
            value *= p
    return value


@check("ard.constant_shape_and_normalization", DOC)
def constant_shape_and_normalization(ctx):
    # Projectively constant does NOT mean all entries equal. An unequal
    # degenerate AP grid is an explicit counterexample to that overclaim.
    primitive = (5, -7, 1, 1, 5, -7, -7, 1, 5)
    for n in (1, 3, 9, 17, 399):
        roots = tuple(Q(n*t, 5) for t in primitive)
        require(roots[4] == n and is_magic(tuple(t*t for t in roots), LINES_3))
        multiplier = lcm(*(t.denominator for t in roots))
        integral = tuple(int(multiplier*t) for t in roots)
        content = reduce(gcd, integral)
        require(tuple(t//content for t in integral) == primitive)
        require(len(set(t*t for t in roots)) == 3)
    ctx.note("five n-scalings all normalize to center 5; constant shape is allowed and is not an MSS3 exclusion")
