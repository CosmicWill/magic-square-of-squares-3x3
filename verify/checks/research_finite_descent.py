"""Finite exact controls; Demeio's and Harari's theorems remain CITED."""

from fractions import Fraction as Q
from itertools import product
from math import gcd, prod

from ..framework import check, require
from compute import formal_boundary_probe as f
from compute import coupled_cycle_probe as c
from compute import universal_twist_probe as u

DOC = "docs/research/finite-descent-barrier.md"


@check("fdb.formal_full_grid", DOC)
def formal_full_grid(ctx):
    precision = ctx.bound(full=18, fast=10)
    roots = f.square_grid(precision)
    for root, (a, b) in zip(roots, u.GRID):
        expected = (Q(1), Q(a+3*b))+(Q(0),)*(precision-2)
        require(f.multiply(root, root) == expected)
    require(prod((1, 3, -2, 4, -5, 7, -1, 5)) == -4200)
    require(len({a+3*b for a, b in u.GRID}) == 9)
    require(all(root[0] == 1 for root in roots))
    for slots, expected in ((f.root_sum_slots(roots), (1, 1, 1)),
                            (f.cycle_slots(roots), (1, 1, 1, 1))):
        data = tuple(f.twist_series(slot) for slot in slots)
        require(tuple(x["twist"] for x in data) == expected)
        require(all(x["root_order"] == 0 and x["root_unit"][0] == 1 for x in data))
    ctx.note(f"all nine square equations through t^{precision-1}; admissible generic direction; canonical cover constants retained")


@check("fdb.kummer_laurent_lifts", DOC)
def kummer_laurent_lifts(ctx):
    precision = ctx.bound(full=14, fast=8)
    roots = f.square_grid(precision)
    difference = tuple(x/2 for x in f.add(roots[0], roots[2], -1))
    cases = [(slot, 0) for slot in f.root_sum_slots(roots)+f.cycle_slots(roots)]
    cases += [(difference, 0), ((Q(1),), -1), ((0, 0, -18, -54, 9), 0)]
    cases += [((0, coefficient, 0, 0, 0), 0) for coefficient in (1, 3, -2, 4, -5, 7, -1, 5)]
    for coefficients, shift in cases:
        data = f.twist_series(coefficients, shift)
        unit = data["unit_input"]
        expected = tuple(unit[j//2] if j % 2 == 0 else Q(0) for j in range(2*len(unit)-1))
        squared = f.multiply(data["root_unit"], data["root_unit"])
        require(tuple(data["twist"]*x for x in squared) == expected)
        leading_index = next(j for j, x in enumerate(coefficients) if x)
        require(data["root_order"] == shift+leading_index)
    require(f.twist_series(difference)["twist"] == -2)
    require(f.twist_series((1,), -1)["root_order"] == -1)
    # A second ramified stage: t=s^2,z1=s, then z2^2=s+s^2.
    stage2 = f.twist_series((0, 1, 1)+(0,)*(precision-3))
    z2 = (Q(0),)+stage2["root_unit"]
    squared = f.multiply(z2, z2)
    require(squared == tuple(Q(1) if j in (2, 4) else Q(0) for j in range(len(squared))))
    for twist in (17, 89, 1513, -7):
        try:
            f.twist_series(f.root_sum_slots(roots)[0], requested_twist=twist)
        except ValueError:
            pass
        else:
            require(False, "parameter ramification incorrectly erased a constant nonsquare")
    ctx.note(f"{len(cases)} exact Laurent-series lift certificates; two-stage ramification; four prescribed wrong twists rejected")


@check("fdb.canonical_two_adic_domain", DOC)
def canonical_two_adic_domain(ctx):
    precision = ctx.bound(full=24, fast=18)
    cover_precision = precision-4
    modulus = 1 << cover_precision
    # The untwisted three-sum cover needs a sufficiently small neighborhood,
    # not every canonical base point. Orders 3 and 4 have other labels.
    for order in range(5, 11):
        t = 1 << order
        values = tuple(1+(a+3*b)*t for a, b in u.GRID)
        roots = tuple(u.odd_square_root_2(value, precision) for value in values)
        require(all(r % 4 == 1 for r in roots))
        require(all((r*r-value) % (1 << precision) == 0 for r, value in zip(roots, values)))
        require(len({value % (1 << precision) for value in values}) == 9)
        for value in u.root_sum_slots(roots[:3])+c.cycle_slots(roots):
            require(value.numerator % 2 and value.denominator % 2)
            residue = value.numerator*pow(value.denominator, -1, modulus) % modulus
            require(residue % 8 == 1)
            lifted = u.odd_square_root_2(residue, cover_precision)
            require(lifted % 2 and (lifted*lifted-residue) % modulus == 0)
    coarse = tuple(u.odd_square_root_2(1+(a+3*b)*8, precision) for a, b in u.GRID)
    coarse_slots = u.root_sum_slots(coarse[:3])
    require(tuple(x.numerator*pow(x.denominator, -1, 8) % 8 for x in coarse_slots) == (7, 3, 1))
    ctx.note(f"six full admissible grids to 2^{precision}, canonical roots; all seven root-sum/cycle lifts are units to 2^{cover_precision}")


@check("fdb.parameter_symbol_blindness", DOC)
def parameter_symbol_blindness(ctx):
    precision = ctx.bound(full=24, fast=16)
    for w in (8, 16, 24, 32):
        twists = c.boundary_family(w)["twists"]
        for mask in range(16):
            first = prod(q for j, q in enumerate(twists) if mask & (1 << j))
            require(first % 8 == 1)
            root = u.odd_square_root_2(first, precision)
            require((root*root-first) % (1 << precision) == 0)
    norm_residues = {(x*x-2*y*y) % 8 for x, y in product(range(1, 8, 2), range(8))}
    require(norm_residues == {1, 7} and 5 not in norm_residues)
    ctx.note(f"all 16 parameter products for four nontrivial twists split at 2 to precision {precision}; nonsplit (2,5) control retained")


@check("fdb.smaller_integer_is_not_a_map", DOC)
def smaller_integer_is_not_a_map(ctx):
    bound = ctx.bound(full=24, fast=10)
    controls = 0
    for denominator in range(2, bound+1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) != 1:
                continue
            data = u.canonical_twists(u.primitive_ap_grid(numerator, denominator))
            a, b, c_, d, m, ff, g, h, i = data["roots"]
            n = f.rational_root(Q(a*i+c_*g, 2))
            require(n.denominator == 1 and 0 < n < m and n.numerator % 2 == 1)
            x, y, z, w = (a+i)//2, (a-i)//2, (c_+g)//2, (c_-g)//2
            require(x*x == n*n+w*w and z*z == n*n+y*y)
            require(m*m == n*n+y*y+w*w)
            require((b*b, d*d, ff*ff, h*h) ==
                    (m*m-2*x*y-2*z*w, m*m-2*x*y+2*z*w,
                     m*m+2*x*y-2*z*w, m*m+2*x*y+2*z*w))
            controls += 1
    roots = (5, -7, 1, 1, 5, -7, -7, 1, 5)
    require(u.canonical_twists(roots)["roots"] == roots)
    require(tuple(u.squareclass(slot) for slot in c.cycle_slots(roots)) == (1, 1, 1, 1))
    require((roots[0]*roots[8]+roots[2]*roots[6])//2 == 9)
    new_values = tuple(9-24*b for _, b in u.GRID)
    require(any(value < 0 for value in new_values), "replacing the center while retaining offsets is not a full square grid")
    ctx.note(f"{controls} exact degenerate controls for the smaller-integer identities; m=5,n=3 exposes the missing full-grid construction")
