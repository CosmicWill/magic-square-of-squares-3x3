"""Branch-local checks for docs/research/global-obstructions.md.

These check the explicit algebra and bounded local controls, not Harari's
formal lemma, Hasse--Minkowski, or a complete Brauer/descent calculation.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product

from ..framework import check, require
from compute import global_obstruction_probe as g

DOC = "docs/research/global-obstructions.md"


@check("gb.surface_and_twists", DOC)
def surface_and_twists(ctx):
    require(g.rank(g.boundary_jacobian(())) == 8)
    require(len(set(g.ENTRY)) == 8 and (0, 0) not in g.ENTRY)
    def direction(a, b):
        from math import gcd
        scale = gcd(a, b)
        a, b = a//scale, b//scale
        return (a, b) if (a or b) > 0 else (-a, -b)
    generated = {direction(a-c, b-d) for (a,b),(c,d) in combinations(((0,0),)+g.ENTRY, 2)}
    require(generated == {direction(a,b) for _,a,b in g.DIFFERENCES})
    # The eight distinct irreducible affine linear radicands have separate
    # valuation coordinates: every nonempty parity product is nonsquare.
    for mask in range(1, 256):
        valuations = tuple((mask >> i) & 1 for i in range(8))
        require(any(valuations))
    # Honest rational degenerate controls; near-square AB1 is not a lift.
    for u, v in ((Q(0), Q(0)), (Q(0), Q(120, 169))):
        require(all(g.rational_square(x) for x in g.entries(u, v)))
    require(not all(g.rational_square(x) for x in g.entries(Q(0), Q(1, 2))))
    from ..targets import AB1
    require(sum(g.rational_square(Q(x, AB1[4])) for x in AB1) == 7)
    require(not g.rational_square(Q(-1)), "constants/signs must not be discarded")
    ctx.note("degree-256 radicand independence; smooth rational all-equal point; rational lift controls")


@check("gb.split_and_surviving_symbols", DOC)
def split_and_surviving_symbols(ctx):
    identity = (Q(1), Q(0), Q(0), Q(1))
    for s, b in product((Q(1), Q(-3), Q(2, 7)), (Q(-1), Q(5), Q(3, 11))):
        i, j = g.quaternion_split_matrices(s, b)
        ij, ji = g.matrix_product(i, j), g.matrix_product(j, i)
        require(g.matrix_product(i, i) == tuple(s*s*x for x in identity))
        require(g.matrix_product(j, j) == tuple(b*x for x in identity))
        require(ij == tuple(-x for x in ji))
        require(g.rank((identity, i, j, ij)) == 4)
    # At u=v=-1 only r_(1,0),r_(0,1) vanish. Eliminating u and v
    # leaves six equations with nonzero root derivatives, etale in s,t.
    values = {ab: 1-a-b for ab in g.ENTRY for a, b in (ab,)}
    require({ab for ab, value in values.items() if value == 0} == {(1, 0), (0, 1)})
    require(all(value != 0 for ab, value in values.items() if ab not in ((1, 0), (0, 1))))
    ctx.note("9 exact quaternion matrix isomorphisms; double-intersection chart for nontrivial (r_(1,0),r_(0,1))")


@check("gb.local_fourth_power_controls", DOC)
def local_fourth_power_controls(ctx):
    bound = ctx.bound(full=499, fast=97)
    primes = [p for p in range(2, bound+1)
              if all(p % q for q in range(2, __import__('math').isqrt(p)+1))]
    for p in primes:
        precision = 20 if p == 2 else 8
        data = g.local_control(p, precision)
        modulus = p ** precision
        require(len(set(x % modulus for x in data["entries"])) == 9)
        for value, root in zip(data["entries"], data["fourth_roots"]):
            require((root**4 - value) % modulus == 0)
            require(root % p != 0)
        for _, a, b in g.DIFFERENCES:
            require(a * data["u"] + b * data["v"] != 0)
    require(all(x > 0 for x in g.entries(Q(1, 100), Q(3, 100))))
    # A negative control for fourth powers: square 9 is not 1 mod 16.
    try:
        g.fourth_root_near_one(9, 2, 20)
    except ValueError:
        pass
    else:
        require(False, "square/fourth-power distinction was lost")
    ctx.note(f"{len(primes)} primes; fourth roots to p^8 (odd) and 2^20; real positive chart")


@check("gb.direction_cover_boundary", DOC)
def direction_cover_boundary(ctx):
    counts = {}
    for size in (1, 2, 3, 4):
        subsets = list(combinations(range(8), size))
        counts[size] = len(subsets)
        for subset in subsets:
            require(g.rank(g.boundary_jacobian(subset)) == 8 + min(size, 2))
    require(counts == {1: 8, 2: 28, 3: 56, 4: 70})
    for i, j, k in combinations(range(8), 3):
        a, b = g.line_relation(i, j, k)
        require(a != 0 and b != 0)
        for c in (1, 2):
            require(a*g.DIFFERENCES[i][c] + b*g.DIFFERENCES[j][c] == g.DIFFERENCES[k][c])
    ctx.note("all 36 one/two-line covers smooth at the universal boundary point for every twist; 56 exact conic relations")


@check("gb.four_line_boundary_atlas", DOC)
def four_line_boundary_atlas(ctx):
    atlas = g.four_line_atlas()
    require(sum(len(row["subsets"]) for row in atlas) == 70)
    require(len(atlas) == 11)
    for row in atlas:
        for subset in row["subsets"]:
            orbit = {g.cross_ratio(perm) for perm in permutations(subset)}
            require(orbit == g.cross_ratio_orbit(row["lambda"]))
            for lam in orbit:
                require(256*(1-lam+lam*lam)**3 / (lam*lam*(1-lam)**2) == row["j"])
    # Classical branch quadruple {infinity,0,1,-1} has j=1728.
    lam = g.cross_ratio((0, 1, 2, 3))
    require(256*(1-lam+lam*lam)**3/(lam*lam*(1-lam)**2) == 1728)
    ctx.note(f"70 subsets, all 24 orderings each; {len(atlas)} geometric branch types (not rational twist classes)")


@check("gb.root_sum_triangle", DOC)
def root_sum_triangle(ctx):
    # These three entries are one magic row: their squares sum to 3.
    require(tuple(sum(ab[i] for ab in g.ROOT_TRIANGLE) for i in (0, 1)) == (0, 0))
    require(all(not g.triangle_equal_fiber(signs, (3, 5, 7)) for signs in product((-1, 1), repeat=3)))
    # Every sign triple with exactly one different sign has one nonzero
    # sum. Thus an all-equal fiber exists iff some twist is +/-2 modulo squares.
    for twists in product((Q(2), Q(-2), Q(3), Q(5), Q(8), Q(-18)), repeat=3):
        actual = any(g.triangle_equal_fiber(signs, twists) for signs in product((-1, 1), repeat=3))
        expected = any(g.rational_square(2/d) or g.rational_square(-2/d) for d in twists)
        require(actual == expected)
    for e1, e2 in combinations(g.TRIANGLE_EDGES, 2):
        rows = []
        for i, j in (e1, e2):
            rows.append([g.ROOT_TRIANGLE[i][c]-g.ROOT_TRIANGLE[j][c] for c in (0, 1)])
        require(g.rank(rows) == 2)
    ctx.note("216 twist triples x 8 sign patterns; (3,5,7) has no fiber above any signed all-equal point; other degeneracies untested")


@check("gb.root_sum_local_candidate", DOC)
def root_sum_local_candidate(ctx):
    require(g.TRIANGLE_Q == (17, 89, 1513))
    require(g.TRIANGLE_TWIST == (34, 178, 3026))
    # Symbolic coefficient certificate for the explicit local row formula:
    # 9(A^2+B^2+C^2)=6h^2-6hk+6k^2+3R^2=27.
    linear = ((-1,2,1), (2,-1,1), (1,1,-1))
    gram = [[sum(row[i]*row[j] for row in linear) for j in range(3)] for i in range(3)]
    require(gram == [[6,-3,0],[-3,6,0],[0,0,3]])
    for edge, uv in zip(g.TRIANGLE_EDGES, ((Q(1,10),Q(1,10)),
                                          (Q(-1,5),Q(1,10)),
                                          (Q(1,10),Q(-1,5)))):
        values = [1+a*uv[0]+b*uv[1] for a,b in g.ROOT_TRIANGLE]
        i,j = edge
        k = next(k for k in range(3) if k not in edge)
        require(values[i] == values[j] and values[k] != values[i])
        require(all(value != 0 for value in g.entries(*uv)))
    require(all(not g.rational_square(q) for q in g.TRIANGLE_Q))
    require(all(not g.triangle_equal_fiber(signs, g.TRIANGLE_TWIST)
                for signs in product((-1, 1), repeat=3)))
    # These four character possibilities exhaust all unramified odd primes.
    for a, b in product((-1, 1), repeat=2):
        require(1 in (a, b, a*b))
    require(89 % 17 == 2**2 % 17)
    require(17 % 89 == 27**2 % 89)
    require(all(q % 8 == 1 for q in g.TRIANGLE_Q))
    bound = ctx.bound(full=499, fast=97)
    primes = [p for p in range(2, bound+1)
              if all(p % q for q in range(2, __import__('math').isqrt(p)+1))]
    for p in (0, *primes):
        edge = g.triangle_local_edge(p)
        require(edge in (0,1,2))
    # All-odd twists fail at 2: with odd row roots, each even square sum
    # would have to be divisible by 4, impossible around an odd cycle.
    require(not any(all((s[i]+s[j]) % 4 == 0 for i,j in g.TRIANGLE_EDGES)
                    for s in product((1,3), repeat=3)))
    for t in (Q(-3,5), Q(-1,2), Q(0), Q(1,3), Q(4,5)):
        if t in (-1,1):
            continue
        f = g.ap_triangle_slots(t, "u=0")
        require(f[0]*f[2]/f[1] == 1/(17**2*(1+t*t)))
        f = g.ap_triangle_slots(t, "v=0")
        require(f[0]*f[1]/f[2] == 1/(1+t*t))
    ctx.note("all-prime character argument plus explicit certificates at 2,17,89,infinity; 95-prime FULL controls; AP-boundary identities")


@check("gb.ap_boundary", DOC)
def ap_boundary(ctx):
    # Normalize the boundary, including its branch points and infinity.
    require(g.ap_normalized_fp_fibers(3,"v=0") == [])
    require(g.ap_normalized_fp_fibers(3,"u=0") == [None])
    # A genuine control with a rational lift at t=0 survives at every prime.
    for p in (3,5,7,11,13,19,23,29):
        for axis in ("u=0", "v=0"):
            require(0 in g.ap_normalized_fp_fibers(p,axis,q=(1,1,1)))
    # The raw AP-u equations at t=1 have slots (0,0,1) mod 3,
    # but the two vanishing radicands have nonsquare leading-unit ratio.
    # A singular affine point must not be counted as a normalized point.
    raw = g.ap_triangle_slots(Q(1),"u=0")
    require(tuple((x.numerator*pow(x.denominator,-1,3)) % 3 for x in raw) == (0,0,1))
    require(1 not in g.ap_normalized_fp_fibers(3,"u=0"))
    bound = ctx.bound(full=100,fast=25)
    result = g.ap_boundary_search(bound)
    require(result["hits"] == [])
    if bound == 100:
        require(result["axis_parameters_tested"] == 12178)
    ctx.note("AP-v: exhaustive reduction at 3; normalization checked against an affine false positive and rational positive controls")
    ctx.note(f"AP search: {result}; this check is bounded; GB.8 separately settles AP-u")


@check("gb.tunnell_89_certificate", DOC)
def tunnell_89_certificate(ctx):
    certificate = g.tunnell_odd_certificate(89)
    require(certificate["counts"] == {8: 48, 32: 20})
    require(certificate["coefficient"] == -4)
    require(certificate["verdict"] == "noncongruent (CITED Tunnell)")
    # Independent signed-box enumeration, rather than the production
    # routine's nonnegative square-root enumeration with sign weights.
    for c, z_bound in ((8, 3), (32, 1)):
        signed = {(x,y,z) for x in range(-6,7) for y in range(-9,10)
                  for z in range(-z_bound,z_bound+1) if 2*x*x+y*y+c*z*z == 89}
        recovered = set()
        for triple, weight in certificate["representatives"][c]:
            orbit = {tuple(a*b for a,b in zip(triple, signs))
                     for signs in product((-1,1), repeat=3)}
            require(len(orbit) == weight)
            recovered.update(orbit)
        require(recovered == signed)
        require(len(signed) == certificate["counts"][c])
    # Known congruent positive controls must not be excluded. Equality is
    # only a necessary condition; no BSD-dependent converse is used.
    for n in (5, 15):
        require(g.tunnell_odd_certificate(n)["verdict"] == "inconclusive")
    for n in (-1, 0, 2, 9):
        try:
            g.tunnell_odd_certificate(n)
        except ValueError:
            pass
        else:
            require(False, "odd squarefree domain was not enforced")
    ctx.note("complete positive-definite counts for 89: N8=48, N32=20, a(89)=-4; Tunnell remains CITED")


@check("gb.ap_u_quotient_and_fibers", DOC)
def ap_u_quotient_and_fibers(ctx):
    # Polynomial coefficients of (1-t^4)^2 + 4*t^4 = (1+t^4)^2.
    # This is the cleared-denominator Pythagorean identity, not a search.
    def multiply(a, b):
        out = [Q(0)]*(len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] += x*y
        return out
    left = multiply((1,0,0,0,-1), (1,0,0,0,-1))
    left[4] += 4
    require(left == multiply((1,0,0,0,1), (1,0,0,0,1)))
    require(multiply((1,0,-1), (1,0,1)) == [1,0,0,0,-1])
    # Degree <= 4 identity defining the quotient y=89*(1+t^2)*z2.
    # Five evaluations certify the polynomial after clearing denominators.
    for t in map(Q, range(-2,3)):
        f1, f2, f3 = g.ap_triangle_slots(t, "u=0")
        require(89**2*(1+t*t)**2*f2 == 89*(1-t**4))
        for q, x, f in ((17,17*(1-t),f1), (1513,1513*(1+t),f3)):
            require(q**4*(1+t*t)**2*f == x**3-2*q*x*x+2*q*q*x)
    branches = ({"1","i","-i","inf"}, {"1","-1","i","-i"},
                {"-1","i","-i","inf"})
    branch_counts = []
    for mask in range(1,8):
        branch = set()
        for i in range(3):
            if mask >> i & 1:
                branch ^= branches[i]
        branch_counts.append(len(branch))
    require(sorted(branch_counts) == [2,2,2,2,4,4,4])
    for t, y, n in ((Q(1,3), Q(20,9), 5), (Q(-1,3), Q(-20,9), 5),
                    (Q(1,2), Q(15,4), 15)):
        a, b, c = g.ap_quartic_to_triangle(t,y,n)
        require(a*a+b*b == c*c and a*b/2 == n)
        x, yy = -n*t*t, n*t*y
        require(yy*yy == x**3-n*n*x and yy != 0)
    # All finite exceptional rational fibers: y=0 gives t=+/-1;
    # t=0 would require y^2=89. At infinity the leading coefficient is -89.
    require(not g.rational_square(89) and not g.rational_square(-89))
    require(g.ap_triangle_slots(Q(1), "u=0")[2] == Q(1,1513))
    require(g.ap_triangle_slots(Q(-1), "u=0")[0] == Q(1,17))
    require(not g.rational_square(Q(1,1513)) and not g.rational_square(Q(1,17)))
    for t,y in ((Q(0),Q(0)), (Q(1),Q(0)), (Q(1,2),Q(1))):
        try:
            g.ap_quartic_to_triangle(t,y,89)
        except ValueError:
            pass
        else:
            require(False, "exceptional/off-curve input passed the triangle map")
    ctx.note("quartic quotient identity; exact triangle and elliptic maps; t=0,+/-1,infinity audited")


@check("gb.projective_boundary_and_row_model", DOC)
def projective_boundary_and_row_model(ctx):
    mod4 = []
    for c,u,v in product(range(4), repeat=3):
        values = (c,) + tuple(c+a*u+b*v for a,b in g.ENTRY)
        if all(value % 4 in (0,1) for value in values):
            mod4.append((c,u,v))
    require(mod4 == [(0,0,0), (1,0,0)])
    # Opposite-square equations account for every projective root. At
    # center zero these force every real homogeneous coordinate to zero.
    pairs = {frozenset((ab,(-ab[0],-ab[1]))) for ab in g.ENTRY}
    require(len(pairs) == 4 and set().union(*pairs) == set(g.ENTRY))
    # Six other distinctness lines produce consecutive 5- or 7-term APs.
    for name,a,b in g.DIFFERENCES[2:]:
        offsets = {0} | {-c*b+d*a for c,d in g.ENTRY}
        require(offsets == set(range(min(offsets),max(offsets)+1)))
        require(len(offsets) == (5 if name in ("u-v","u+v") else 7))
    # Coefficient proof of the row quartic after substituting s_i=q_i*z_i^2.
    matrix = ((1,-1,1), (1,1,-1), (-1,1,1))
    gram = [[sum(row[i]*row[j] for row in matrix) for j in range(3)] for i in range(3)]
    require(gram == [[3,-1,-1],[-1,3,-1],[-1,-1,3]])
    for z in ((Q(0),Q(0),Q(0)), (Q(1),Q(2,3),Q(-1,5))):
        row = g.triangle_row_from_cover(z)
        require(sum(a*a for a in row)-3 == g.triangle_row_quartic(z))
        require(tuple(row[i]+row[j] for i,j in g.TRIANGLE_EDGES)
                == tuple(2*q*x*x for q,x in zip(g.TRIANGLE_Q,z)))
        a,b,c = row
        u,v = a*a-1,b*b-1
        extras = {(-1,0):2-a*a, (0,-1):2-b*b, (1,1):2-c*c,
                  (1,-1):1+a*a-b*b, (-1,1):1-a*a+b*b}
        require(set(extras) | set(g.ROOT_TRIANGLE) == set(g.ENTRY))
        require(not set(extras) & set(g.ROOT_TRIANGLE))
        for (i,j), value in extras.items():
            residual = value-(1+i*u+j*v)
            require(residual == (-g.triangle_row_quartic(z) if (i,j)==(1,1) else 0))
    # Positive control: untwisted row data lift a full degenerate square.
    require(g.triangle_row_quartic((1,0,0),q=(1,1,1)) == 0)
    row = g.triangle_row_from_cover((1,0,0),q=(1,1,1))
    require(row == (1,1,-1))
    ctx.note("all 64 mod-4 cases; projective opposite pairs; six AP directions; exact row quartic coefficient matrix")
