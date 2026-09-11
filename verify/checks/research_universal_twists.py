"""Exact checks for the universal twist reduction; no MSS3 exclusion."""

from fractions import Fraction as Q
from functools import reduce
from itertools import product
from math import gcd, isqrt

from ..framework import check, require
from compute import global_obstruction_probe as g
from compute import universal_twist_probe as u

DOC = "docs/research/universal-twist-reduction.md"


def primes_dividing(n):
    n = abs(n)
    if not n:
        raise ValueError("zero has no finite prime support")
    result, p = set(), 2
    while p*p<=n:
        if n%p==0:
            result.add(p)
            while n%p==0:
                n//=p
        p+=1
    if n>1:
        result.add(n)
    return result


@check("ut.sign_orbit", DOC)
def sign_orbit(ctx):
    rows = ((Q(1),Q(7,5),Q(1,5)), (Q(1),Q(23,17),Q(7,17)),
            (Q(2),Q(3),Q(5)), (Q(-2,3),Q(3,7),Q(5,2)))
    for row in rows:
        slots = u.root_sum_slots(row)
        differences = tuple(row[i]**2-row[j]**2 for i,j in u.EDGES)
        actual_products = set()
        for signs,changed in u.sign_orbit(row).items():
            for e,(i,j) in enumerate(u.EDGES):
                cut = int(signs[i]!=signs[j])
                predicted = signs[i]*slots[e]*differences[e]**cut
                ratio = changed[e]/predicted
                require(ratio == (1/(4*slots[e]**2) if cut else 1))
                require(g.rational_square(ratio))
            actual_products.add(u.squareclass(reduce(lambda x,y:x*y,changed)))
        base = reduce(lambda x,y:x*y,slots)
        factors = (Q(1),differences[0]*differences[1],differences[1]*differences[2],
                   differences[2]*differences[0])
        predicted_products = {u.squareclass(sign*base*f) for sign,f in product((-1,1),factors)}
        require(actual_products == predicted_products)
    ctx.note("exact sign-change identities and all eight product classes; signs and square factors retained")


@check("ut.canonical_universal_family", DOC)
def canonical_universal_family(ctx):
    residues = set()
    for row in product((1,5,9,13),repeat=3):
        if sum(x*x for x in row)%32==3:
            residues.add(tuple(int(x)%8 for x in u.root_sum_slots(row)))
    expected = {q for q in product((1,3,5,7),repeat=3) if sum(q)%8==3}
    require(residues == expected and len(expected)==16)
    bound = ctx.bound(full=30,fast=12)
    tested = 0
    for b in range(2,bound+1):
        for a in range(1,b):
            if gcd(a,b)!=1:
                continue
            roots = u.primitive_ap_grid(a,b)
            data = u.canonical_twists(roots)
            require(all((r-data["m"])%4==0 for r in data["roots"]))
            for frame in data["frames"]:
                q,z = frame["q"],frame["z"]
                require(all(n%2 for n in q) and sum(q)%8==3)
                require(all(x.numerator%2 and x.denominator%2 for x in z))
                row = tuple(Q(data["roots"][i],data["m"]) for i in frame["indices"])
                require(u.root_sum_slots(row) == tuple(n*x*x for n,x in zip(q,z)))
            tested += 1
    for roots in ((1,)*8, (2,)*9, (1,2,3,4,1,6,7,8,9)):
        try:
            u.canonical_twists(roots)
        except ValueError:
            pass
        else:
            require(False,"invalid/full-grid condition was dropped")
    ctx.note(f"16 exhaustive residue triples; {tested} rational AP controls x 4 frames; canonical lift coordinates are 2-adic units")


@check("ut.two_adic_family", DOC)
def two_adic_family(ctx):
    precision = ctx.bound(full=24,fast=16)
    cases = [q for q in product((1,3,5,7),repeat=3) if sum(q)%8==3]
    cases += [(17,89,1513),(-5,-15,15),(-7,3,7)]
    for q in cases:
        data = u.canonical_two_adic_control(q,precision)
        modulus = 1<<precision
        require(g.triangle_row_quartic(data["z"],q)%modulus==0)
        require(all((r*r-x)%modulus==0 for r,x in zip(data["roots"],data["entries"])))
        require(all(r%4==1 for r in data["roots"][:3]))
        require(all(x%2 for x in data["z"]))
    # Exhaustive mod-16 necessity when every z is odd: only sums 3 or 5
    # mod 8 are possible; 3 selects row roots 1 mod 4, and 5 their negatives.
    for q in product((1,3,5,7),repeat=3):
        for z in product((1,3),repeat=3):
            require((g.triangle_row_quartic(z,q)%16==0) == (sum(q)%8 in (3,5)))
    ctx.note(f"19 exact lifts to 2^{precision}, retaining all nine squares; complete odd-unit mod-16 classification")


@check("ut.prime_support", DOC)
def prime_support(ctx):
    bound = ctx.bound(full=25,fast=10)
    tested = 0
    for b in range(2,bound+1):
        for a in range(1,b):
            if gcd(a,b)!=1:
                continue
            data = u.canonical_twists(u.primitive_ap_grid(a,b))
            m,G = data["m"],data["g"]
            require(gcd(m,G)==1)
            require(all(p%4==1 for p in primes_dividing(m)))
            for frame in data["frames"]:
                q = frame["q"]
                row = tuple(data["roots"][i] for i in frame["indices"])
                require(reduce(gcd,row)==1)
                require(u.squareclass(m)%reduce(gcd,q)==0)
                for i,j in u.EDGES:
                    require(primes_dividing(gcd(q[i],q[j])) <= primes_dividing(6*m*G))
                for p in primes_dividing(m):
                    sums = tuple(row[i]+row[j] for i,j in u.EDGES)
                    require(sum(s%p==0 for s in sums)<=1)
                    if p%8==5:
                        require(all(s%p for s in sums))
                        parity = int(u.squareclass(m)%p==0)
                        require(all(int(n%p==0)==parity for n in q))
                differences = tuple((row[i]**2-row[j]**2)//G for i,j in u.EDGES)
                support = primes_dividing(m*reduce(lambda x,y:x*y,differences))
                N = u.squareclass(reduce(lambda x,y:x*y,q))
                require(primes_dividing(N) <= support)
                H = u.squareclass(Q(reduce(lambda x,y:x*y,q),m))
                require(primes_dividing(H) <= primes_dividing(reduce(lambda x,y:x*y,differences)))
                require(g.rational_square(Q(reduce(lambda x,y:x*y,q),m*H)))
            tested += 1
    # Finite-field core of the p=5 mod 8 center-prime argument.
    for p in (5,13,29,37,53,61):
        roots = {}
        for c in range(p):
            roots.setdefault(c*c%p,[]).append(c)
        for a,b in product(range(p),repeat=2):
            for c in roots.get((-a*a-b*b)%p,[]):
                if (a,b,c)==(0,0,0):
                    continue
                require(all(s%p for s in (a+b,b+c,c+a)))
    # At p=1 mod 8 the conclusion is false; retain that distinction.
    require((1+(-1)**2+7**2)%17==0 and (1-1)%17==0)
    # Independent local controls away from the AP boundary: u=p^k,
    # v=3*p^k. None of the primitive row differences 2,5,7 vanishes
    # at these primes. Sign changes give zero or two sums of valuation k.
    for p,k in product((11,13,17,19),(1,2,3)):
        precision = 2*k+3
        values = tuple(1+i*p**k+j*3*p**k for i,j in u.GRID)
        roots = tuple(u.unit_square_root_odd(x,p,1,precision) for x in values)
        require(len({x%(p**precision) for x in values})==9)
        require(all((r*r-x)%(p**precision)==0 for r,x in zip(roots,values)))
        for frame in u.FRAMES:
            for signs in product((-1,1),repeat=3):
                row = tuple(roots[i]*s for i,s in zip(frame,signs))
                valuations = []
                for i,j in u.EDGES:
                    n,order = abs(row[i]+row[j]),0
                    require(n!=0)
                    while n%p==0:
                        n//=p
                        order+=1
                    valuations.append(order)
                require(sorted(valuations) in ([0,0,0],[0,k,k]))
                require(sum(valuations)%2==0)
    ctx.note(f"{tested} primitive AP controls x 4 frames; exact center/common-offset support; six finite-field p=5 mod 8 controls")
    ctx.note("12 admissible local grids x 4 frames x 8 signs check cancellation of the common offset prime")


@check("ut.product_relation_counterexample", DOC)
def product_relation_counterexample(ctx):
    precision = ctx.bound(full=8,fast=4)
    data = u.local_product_counterexample(precision)
    p = data["p"]
    require(p==401 and all(p%d for d in range(2,isqrt(p)+1)))
    require(len({x%p for x in data["entries"]})==9)
    require(all(x%p for x in data["entries"]))
    require(all((r*r-x)%(p**precision)==0 for r,x in zip(data["roots"],data["entries"])))
    require(len(data["product_residues"])==4)
    for frame,residues in zip(u.FRAMES,data["product_residues"]):
        require(len(residues)==8 and all(pow(x,200,p)==400 for x in residues))
        row = tuple(data["roots"][i]%p for i in frame)
        differences = tuple((row[i]**2-row[j]**2)%p for i,j in u.EDGES)
        require(all(pow(x,200,p)==400 for x in differences))
    require(pow(p-1,200,p)==1)
    # Positive control: the product-square pattern exists at the all-equal
    # point and must not be rejected by a broken residue classifier.
    equal = u.product_orbit_mod_p((1,)*9,p)
    require(all(1 in residues for residues in equal))
    ctx.note(f"full local square grid to 401^{precision}; all 4 frames x 8 signs have nonsquare twist product")
