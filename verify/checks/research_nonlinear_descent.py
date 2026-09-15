"""Exact controls for the nonlinear descent candidates; no point exclusion."""

from fractions import Fraction as Q
from itertools import product
from math import gcd, isqrt

from ..framework import check, require
from ..targets import LINES_3, is_magic
from compute import arithmetic_descent_probe as a
from compute import nonlinear_descent_probe as n
from compute import universal_twist_probe as u
from compute.formal_boundary_probe import rational_root

DOC = "docs/research/nonlinear-descent-fibers.md"


@check("nlf.reciprocity_normalization", DOC)
def reciprocity_normalization(ctx):
    for nn, r, s in product(range(1, 6), repeat=3):
        old = n.half_sums(nn, r, s)
        rec = n.reciprocity(nn, r, s)
        new = n.half_sums(rec["n"], r, s)
        scale = rec["scale"]
        x, y, z, w = old
        require(new == (scale*z, -scale*w, scale*x, -scale*y))
        require(n.reciprocity(rec["n"], r, s)["n"] == nn)
        require(rec["n"]**2 == scale*scale*nn*nn)
    bound = ctx.bound(full=24, fast=10)
    count = 0
    for denominator in range(2, bound+1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) != 1:
                continue
            roots = u.canonical_twists(u.primitive_ap_grid(numerator, denominator))["roots"]
            aa, _, cc, _, m, _, gg, _, ii = roots
            nn = rational_root(Q(aa*ii+cc*gg, 2)).numerator
            x, y = abs((aa+ii)//2), abs((aa-ii)//2)
            z, w = abs((cc+gg)//2), abs((cc-gg)//2)
            r, s = x-w, z-y
            data = a.divisor_model(nn, r, s)
            ca, cc, cg, ci = data["corner_roots"]
            b, d, f, h = map(isqrt, data["sides"])
            original = ca, b, cc, d, m, f, cg, h, ci
            require(tuple(v*v for v in original) == data["entries"])
            rec = n.reciprocity(nn, r, s)
            transformed = tuple(rec["scale"]*original[j] for j in n.REFLECTION)
            xx, yy, zz, ww = n.half_sums(rec["n"], r, s)
            require(tuple(transformed[j] for j in (0, 2, 6, 8)) == (xx+yy, zz+ww, zz-ww, xx-yy))
            require(is_magic(tuple(v*v for v in transformed), LINES_3))
            require(0 < rec["n"] < nn)
            require(n.primitive_roots(transformed) == tuple(original[j] for j in n.REFLECTION))
            require(n.primitive_roots(transformed)[4] == m)
            count += 1
    require(n.reciprocity(399, 147, 19)["n"] == 7)
    require(n.reciprocity(399, 147, 19)["scale"] == Q(1, 57))
    ctx.note(f"125 rational reciprocity controls; {count} full AP grids shrink rational n but keep the same primitive center")


@check("nlf.divisor_fiber_compatibility", DOC)
def divisor_fiber_compatibility(ctx):
    bound = ctx.bound(full=35, fast=15)
    count = 0
    for nn in range(1, bound+1, 2):
        divisors = [d for d in range(1, nn+1, 2) if nn*nn % d == 0]
        for r, s in product(divisors, repeat=2):
            k, t = Q(r, s), Q(nn, s)
            data = a.divisor_model(nn, r, s)
            targets = (data["center_squared"],)+data["sides"]
            require(n.fiber_values(k, t) == tuple(4*k*k*v/(s*s) for v in targets))
            require(n.fiber_values(k, t) == tuple(Q(v, s**6) for v in a.scaled_square_targets(nn, r, s)))
            reciprocal = n.fiber_values(k, k/t)
            expected = n.fiber_values(k, t)
            require(tuple(t**4*v for v in reciprocal) == tuple(k*k*expected[j] for j in n.RECIPROCAL_SLOTS))
            count += 1
    ctx.note(f"{count} divisor inputs retain all five square tests after s=1 normalization; reciprocal slot permutation verified")


@check("nlf.branch_certificates", DOC)
def branch_certificates(ctx):
    # All quartic coefficients have k-degree <=4. Sylvester determinants
    # have degree <=32 (resultants), <=28 (f versus f'); all displayed
    # factorizations, including disc(f)*leading(f), obey the same bound.
    # Thus 33 distinct integer evaluations prove the polynomial identities.
    for k in range(2, 35):
        polynomials = n.fiber_polynomials(k)
        require(tuple(n.discriminant(f) for f in polynomials) == n.discriminant_factors(k))
        for (i, j), expected in n.resultant_factors(k).items():
            require(n.resultant(polynomials[i], polynomials[j]) == expected)
    # A separate sign-sensitive determinant control, not an even-quartic case.
    require(n.resultant((-2, 1), (-3, 1)) == -1)
    require(n.resultant((-3, 1), (-2, 1)) == 1)
    for k in (0, 1, -1):
        try:
            n.cover_data(k)
        except ValueError:
            pass
        else:
            require(False, "exceptional ratio incorrectly assigned the generic genus")
    ctx.note("495 exact determinants certify five discriminants and ten resultants as polynomial identities; k=0,+/-1 rejected")


@check("nlf.cover_degree_and_genus", DOC)
def cover_degree_and_genus(ctx):
    quadratics = ((1, 0, 1), (1, -4, 1), (1, 4, 1),
                  (1, 0, -3), (3, 0, -1), (1, -2, -1), (1, 2, -1))
    for aa, bb, cc in quadratics:
        disc = bb*bb-4*aa*cc
        require(disc < 0 or isqrt(disc)**2 != disc)
    # Each polynomial has four private simple zeros. The five independent
    # parity columns make 32 sheets; infinity has five even valuations.
    valuations = tuple(1 << j for j in range(5) for _ in range(4))
    branch_counts = []
    for mask in range(1, 32):
        number = sum((mask & row).bit_count() % 2 for row in valuations)
        require(number == 4*mask.bit_count() and number > 0)
        branch_counts.append(number)
    require(sum((number-2)//2 for number in branch_counts) == 129)
    for k in (Q(1, 3), Q(2), Q(3), Q(147, 19), Q(-2)):
        data = n.cover_data(k)
        require(data == {"rank": 5, "degree": 32, "branch_points": 20,
                         "infinity_ramifies": False, "genus": 129, "center_quotient_degree": 16})
        require(2*data["genus"]-2 == -2*data["degree"]+data["branch_points"]*(data["degree"]//2))
    # This is degree bookkeeping for the cited Riemann--Hurwitz deduction,
    # not a finite test establishing the theorem for all morphisms.
    require(2*129-2 == 256)
    require(256-4*256 == -768)
    require(Q(16, 4*16).denominator != 1, "a global rational halving lift would have nonintegral degree")
    ctx.note("all seven extra quadratic factors have no rational roots; 32 sheets, 20 simple branch points, genus 129; doubling would require negative ramification")


@check("nlf.rational_boundary_sections", DOC)
def rational_boundary_sections(ctx):
    # The unsigned section identities have k-degree <=6, so seven k-values
    # also give a polynomial identity certificate for their displayed forms.
    for k in range(2, 9):
        points = tuple(n.boundary_sections(k))
        require(len(points) == len(set(points)) == 128)
        for t, lifts in points:
            require(all(lifts) and tuple(v*v for v in lifts) == n.fiber_values(k, t))
            roots = n.reconstruct(k, t, lifts)
            entries = tuple(v*v for v in roots)
            require(is_magic(entries, LINES_3) and min(entries) > 0)
            require(len(set(entries)) == 3)
            m2 = entries[4]
            uu, vv = entries[0]-m2, entries[2]-m2
            require(not uu*vv)
    # Finite t=0 and infinity both have U=V !=0; rational full lifts
    # there would give a nonconstant arithmetic progression of squares.
    for k in (Q(2), Q(3), Q(147, 19)):
        x, y, z, w = n.half_sums(0, k, 1)
        require(2*x*y == 2*z*w == -k/2)
        infinity_m2 = (k*k+1)/(4*k*k)
        infinity_u = infinity_v = Q(1)/(2*k)
        entries = tuple(infinity_m2+i*infinity_u+j*infinity_v for i, j in u.GRID)
        require(len(set(entries)) == 5)
    ctx.note("128 distinct rational AP points on each of seven fibers; finite-zero and infinity charts retained; boundary completeness uses the classical four-square theorem")


@check("nlf.elliptic_quotient_lift", DOC)
def elliptic_quotient_lift(ctx):
    for k in range(2, 9):
        aa = k*k+1
        for t in range(1, 8):
            f0 = n.fiber_values(k, t)[0]
            xx = aa*t*t
            # Y=aa*t*sqrt(f0), so this checks the quotient without
            # assuming that the center-only quartic has a rational point.
            require(aa*aa*t*t*f0 == xx**3+k*k*aa*aa*xx)
        point = n.elliptic_quotient(k, 1, aa)
        require(point == (aa, aa*aa))
        doubled = n.double_on_quotient(k, point)
        require(doubled == (Q((k*k-1)**2, 4), Q(-(k*k-1)*(k**4+6*k*k+1), 8)))
        xx, yy = doubled
        require(yy*yy == xx**3+k*k*aa*aa*xx)
    doubled = n.double_on_quotient(3, (10, 100))
    require(doubled == (16, -136))
    require(doubled[0]/10 == Q(8, 5))
    try:
        rational_root(Q(8, 5))
    except ValueError:
        pass
    else:
        require(False, "quotient doubling incorrectly treated as preserving the t-square lift")
    ctx.note("quartic-to-elliptic quotient identity; exact duplication formula; (10,100) -> (16,-136) loses rational t because t^2=8/5")


@check("nlf.nonboundary_local_fiber", DOC)
def nonboundary_local_fiber(ctx):
    precision = ctx.bound(full=8, fast=4)
    data = n.local_fiber(precision)
    p, k, t = data["p"], data["k"], data["t"]
    modulus = p**precision
    residue = lambda q, mod: Q(q).numerator*pow(Q(q).denominator, -1, mod) % mod
    require(all((y*y-value) % modulus == 0 for y, value in zip(data["lifts"], data["values"])))
    roots = data["roots"]
    entries = tuple(residue(v*v, modulus) for v in roots)
    m2, uu, vv = entries[4], entries[0]-entries[4], entries[2]-entries[4]
    require(all((entry-m2-i*uu-j*vv) % modulus == 0 for entry, (i, j) in zip(entries, u.GRID)))
    require((residue(roots[0]*roots[8]+roots[2]*roots[6], modulus)-2*t*t) % modulus == 0)
    require(len({v % p for v in entries}) == 9 and all(v % p for v in entries))
    rec_t = Q(k, t)
    rec_lifts = tuple(Q(k, t*t)*data["lifts"][j] for j in n.RECIPROCAL_SLOTS)
    reflected = n.reconstruct(k, rec_t, rec_lifts)
    require(reflected == tuple(Q(k, t*t)*roots[j] for j in n.REFLECTION))
    require(all(residue(y*y-value, modulus) == 0 for y, value in zip(rec_lifts, n.fiber_values(k, rec_t))))
    ctx.note(f"k=3,t=13: all five square lifts and nine distinct nonzero entries to 401^{precision}; reciprocal lift verified; no rational interior point asserted")
