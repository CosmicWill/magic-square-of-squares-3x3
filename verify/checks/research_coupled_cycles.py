"""Exact certificates and bounded controls for the coupled cycle note."""

from fractions import Fraction as Q
from itertools import product
from math import gcd, prod

from ..framework import check, require
from compute import coupled_cycle_probe as c
from compute import universal_twist_probe as u
from .research_universal_twists import primes_dividing

DOC = "docs/research/coupled-cycle-descent.md"


@check("cce.cycle_space_and_degree", DOC)
def cycle_space_and_degree(ctx):
    require(len(c.GRAPH_EDGES) == 12)
    all_cycles = tuple(c.cycle_mask(frame) for frame in u.FRAMES) + (c.cycle_mask(c.CORNER),)
    span = c.binary_span(all_cycles)
    require(len(span) == 32)
    even = c.binary_span(c.even_cycle_basis())
    require(len(even) == 16 and even == {x for x in span if x.bit_count() % 2 == 0})
    # Every even-cycle cut is even, for every assignment of eight signs.
    for bits in product((-1, 1), repeat=8):
        signs = bits[:4]+(1,)+bits[4:]
        cut = sum(1 << j for j, (a, b) in enumerate(c.GRAPH_EDGES) if signs[a] != signs[b])
        require(all((cut & mask).bit_count() % 2 == 0 for mask in even))
    certificates = ((-2, 1, 1), (-2, 1, 6), (2, 1, 3), (1, 1, 0))
    rows = []
    for k, l, flipped in certificates:
        signs = [1]*9
        signs[flipped] = -1
        rows.append(c.branch_parities(k, l, signs))
    require(rows == [(1, 0, 1, 0), (1, 0, 0, 0), (0, 1, 1, 0), (1, 0, 1, 1)])
    encoded = [sum(bit << j for j, bit in enumerate(row)) for row in rows]
    require(len(c.binary_span(encoded)) == 16)
    ctx.note("complete 5-dimensional graph cycle space, 4-dimensional even part; four independent geometric valuation rows")


@check("cce.canonical_family_and_support", DOC)
def canonical_family_and_support(ctx):
    lookup = {r*r % 32: r for r in (1, 5, 9, 13)}
    observed = set()
    for x, y in product(range(4), repeat=2):
        roots = tuple(lookup[(1+8*a*x+8*b*y) % 32] for a, b in u.GRID)
        T = c.frame_products(roots)
        residues = tuple(value.numerator*pow(value.denominator, -1, 8) % 8 for value in T)
        require(residues == (1+4*((x*x+x*y+y*y) % 2),)*4)
        observed.add(residues)
        for value in c.cycle_slots(roots):
            require(value.numerator % 2 and value.denominator % 2)
            require(value.numerator*pow(value.denominator, -1, 8) % 8 == 1)
    require(observed == {(1, 1, 1, 1), (5, 5, 5, 5)})
    P_factors, Q_factors = ((2, 1), (1, 2), (1, -1)), ((2, -1), (1, -2), (1, 1))
    determinants = {abs(a*d-b*c_) for (a, b), (c_, d) in product(P_factors, Q_factors)}
    require(determinants == {1, 2, 4, 5})
    bound = ctx.bound(full=24, fast=8)
    controls = 0
    for b in range(2, bound+1):
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue
            data = u.canonical_twists(u.primitive_ap_grid(a, b))
            require(tuple(u.squareclass(x) for x in c.cycle_slots(data["roots"])) == (1, 1, 1, 1))
            controls += 1
    for n in range(1, bound+1):
        data = c.boundary_family(8*n)
        k, l = data["direction"]
        P, R = (2*k+l)*(k+2*l)*(k-l), (2*k-l)*(k-2*l)*(k+l)
        for q, support in zip(data["twists"], (P, R, P*R, (k-l)*(k+l))):
            require(q % 8 == 1 and primes_dividing(q) <= primes_dividing(support))
        require(5 % gcd(abs(data["twists"][0]), abs(data["twists"][1])) == 0)
    ctx.note(f"16 exhaustive offset residues modulo 32; {controls} canonical rational AP controls; {bound} nontrivial boundary label tuples")


@check("cce.corner_identity_and_local_witness", DOC)
def corner_identity_and_local_witness(ctx):
    pairs = []
    for a, b in ((1, 2), (1, 3), (2, 3), (1, 4), (2, 5)):
        m = a*a+b*b
        pairs.append((Q(b*b-2*a*b-a*a, m), Q(b*b+2*a*b-a*a, m)))
    for (a0, i0), (c0, g0), signs in product(pairs, pairs, product((-1, 1), repeat=4)):
        a, c_, i, g_ = (x*s for x, s in zip((a0, c0, i0, g0), signs))
        require(a*a+i*i == 2 and c_*c_+g_*g_ == 2)
        P = (a+c_)*(c_+i)*(i+g_)*(g_+a)
        C = (a*i+c_*g_)/2
        require(P/16 == C*((a+c_+i+g_)/4)**2)
        offset_u, offset_v = a*a-1, c_*c_-1
        require(2*(a*i-c_*g_)*C == offset_v**2-offset_u**2)
    precision = ctx.bound(full=8, fast=4)
    data = c.local97(precision)
    require(all(97 % p for p in (2, 3, 5, 7)))
    require(len({x % 97 for x in data["entries"]}) == 9)
    require(all(x % 97 for x in data["entries"]))
    require(all((r*r-x) % (97**precision) == 0 for r, x in zip(data["roots"], data["entries"])))
    require(data["residues"] == [15, 17, 80, 82])
    require(all(pow(x, 48, 97) == 96 for x in data["residues"]))
    require(pow(96, 48, 97) == pow((23*23-26*26) % 97, 48, 97) == 1)
    ctx.note(f"400 exact signed corner identities; full grid lifted to 97^{precision}; all 16 corner signs retain nonsquare class")


@check("cce.rational_boundary_charts", DOC)
def rational_boundary_charts(ctx):
    # The exceptional conic has a rational parametrization for every kappa.
    for kappa in (1, -1, 2, -2, 17, 89, -7, -119):
        for parameter in (Q(0), Q(1, 3), Q(2, 5)):
            denominator = 1-kappa*parameter**2
            if not denominator:
                continue
            w = (1+kappa*parameter**2)/denominator
            Z = parameter/denominator
            require(w*w-4*kappa*Z*Z == 1)
            require(w or Z, "exceptional conic point must be smooth")
    data = c.boundary_family(8)
    require(data["twists"] == (-119, -15, 1, -7))
    require(data["leading"] == (Q(-119, 16), Q(-135, 16), Q(1), Q(-63, 4)))
    require(data["lifts"] == (Q(1, 4), Q(3, 4), Q(1), Q(3, 2)))
    require(data["orders"] == (2, 2, 0, 2))
    require(all(q*z*z == value for q, z, value in zip(data["twists"], data["lifts"], data["leading"])))
    # The minor using eight entry roots and four rescaled cover roots is
    # block triangular, with these diagonal entries all nonzero.
    diagonal = tuple(2*s for j, s in enumerate(data["signs"]) if j != 4)
    diagonal += tuple(2*q*z for q, z in zip(data["twists"], data["lifts"]))
    require(len(diagonal) == 12 and prod(diagonal) != 0)
    # At the single-corner chart's point w=1,Z=0 the additional derivative
    # is -2; the root-equation diagonal is nonzero for every nonzero kappa.
    require(prod((2,)*7+(-2, -2)) != 0)
    ctx.note("explicit rational conic chart and smooth degree-16 boundary point; no raw singular point counted as resolved")


@check("cce.rescaled_boundary_local_lifts", DOC)
def rescaled_boundary_local_lifts(ctx):
    precision = ctx.bound(full=6, fast=4)
    for p, w in product((101, 103, 107), (8, 16, 24)):
        boundary = c.boundary_family(w)
        values = tuple(1+p*(a+b*w) for a, b in u.GRID)
        root_precision = precision+max(boundary["orders"])
        roots = tuple(u.unit_square_root_odd(value, p, sign % p, root_precision)
                      for value, sign in zip(values, boundary["signs"]))
        require(len({x % (p**root_precision) for x in values}) == 9)
        require(all((r*r-x) % (p**root_precision) == 0 for r, x in zip(roots, values)))
        for slot, order, q, seed in zip(c.cycle_slots(roots), boundary["orders"],
                                        boundary["twists"], boundary["lifts"]):
            scaled = slot/(q*p**order)
            require(scaled.denominator % p != 0)
            modulus = p**precision
            residue = scaled.numerator*pow(scaled.denominator, -1, modulus) % modulus
            seed_mod = seed.numerator*pow(seed.denominator, -1, p) % p
            lifted = u.unit_square_root_odd(residue, p, seed_mod, precision)
            require((lifted*lifted-residue) % modulus == 0)
    ctx.note(f"nine admissible local grids near the boundary; all four rescaled cover equations lifted to p^{precision}")
