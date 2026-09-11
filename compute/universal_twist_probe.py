"""Exact probes for the universal root-sum twist reduction (UT.1--UT.4).

No universal exclusion is asserted. The 401-adic witness refutes a local
or algebraic shortcut to a restricted twist family, not a theorem solely
about rational admissible points. All searches here are small and explicit.
"""

from fractions import Fraction as Q
from functools import reduce
from itertools import product
from math import gcd, isqrt

from compute.global_obstruction_probe import triangle_row_from_cover, triangle_row_quartic

GRID = ((1,0),(-1,-1),(0,1),(-1,1),(0,0),(1,-1),(0,-1),(1,1),(-1,0))
FRAMES = ((0,1,2),(6,7,8),(0,3,6),(2,5,8))
EDGES = ((0,1),(1,2),(2,0))
LOCAL_CONTROL = {"p": 401, "u": 79, "v": 82,
                 "roots": (90,38,22,2,1,143,180,76,137)}


def squareclass(value):
    """Signed squarefree integer representing a nonzero rational value."""
    value = Q(value)
    if not value:
        raise ValueError("square class of zero is undefined")
    n = value.numerator * value.denominator
    sign, n = (-1 if n < 0 else 1), abs(n)
    result, p = sign, 2
    while p*p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            result *= p
        p += 1
    return result*n


def root_sum_slots(row):
    row = tuple(map(Q,row))
    return tuple((row[i]+row[j])/2 for i,j in EDGES)


def sign_orbit(row):
    """Exact q triples for the eight root-sign choices; no symmetry omitted."""
    return {signs: root_sum_slots(tuple(s*x for s,x in zip(signs,row)))
            for signs in product((-1,1),repeat=3)}


def primitive_ap_grid(a,b):
    """Rational degenerate controls, u=0; cleared and primitive integer roots."""
    if b <= 0:
        raise ValueError("positive denominator required")
    m, high, low = a*a+b*b, b*b-2*a*b-a*a, b*b+2*a*b-a*a
    roots = tuple({0:m,1:high,-1:low}[j] for _,j in GRID)
    divisor = reduce(gcd,roots)
    return tuple(x//divisor for x in roots)


def canonical_twists(roots):
    """Canonical signs r_i/m=1 mod 4, then q_i=sqclass((r_i+r_j)/(2m)).

    Accepts full primitive integer root grids, including degeneracies as
    controls. Output covers all four noncentral rows/columns. The rational
    lift coordinates z are 2-adic units; this is part of the normalization.
    """
    roots = tuple(roots)
    if len(roots)!=9 or any(not isinstance(x,int) for x in roots):
        raise ValueError("nine integer roots required")
    if reduce(gcd,roots)!=1 or not roots[4]:
        raise ValueError("primitive roots with nonzero center required")
    m = abs(roots[4])
    u, v = roots[0]**2-m*m, roots[2]**2-m*m
    if any(r*r != m*m+a*u+b*v for r,(a,b) in zip(roots,GRID)):
        raise ValueError("the full nine-entry magic condition is required")
    if any(r % 2 == 0 for r in roots):
        raise ValueError("primitive square grid violates the proven mod-4 condition")
    signed = tuple(r if (r-m)%4==0 else -r for r in roots)
    frames = []
    for frame in FRAMES:
        slots = root_sum_slots(tuple(Q(signed[i],m) for i in frame))
        q = tuple(squareclass(x) for x in slots)
        squares = tuple(x/n for x,n in zip(slots,q))
        if not all(x>0 and isqrt(x.numerator)**2==x.numerator
                   and isqrt(x.denominator)**2==x.denominator for x in squares):
            raise ArithmeticError("squareclass representative lost its rational lift")
        z = tuple(Q(isqrt(x.numerator),isqrt(x.denominator)) for x in squares)
        frames.append({"indices":frame,"q":q,"z":z})
    return {"m":m,"u":u,"v":v,"g":gcd(u,v),"roots":signed,"frames":frames}


def odd_square_root_2(value, precision):
    """Lift the root 1 mod 4 of a value 1 mod 8 to 2^precision."""
    if precision<3 or value%8!=1:
        raise ValueError("need precision >=3 and value=1 mod 8")
    root = 1
    for n in range(3,precision):
        if (root*root-value) % (1<<(n+1)):
            root += 1<<(n-1)
    return root


def canonical_two_adic_control(q, precision=24):
    """For any odd q with sum=3 mod 8, explicitly lift a full local grid.

    The seed z=(1,5,9) is odd. F=0 mod 16 initially, and changing z1 by
    2^(n-2) toggles F's n-th bit. Generic local perturbation, not a bound
    on this seed, supplies admissible points in the 2-adic statement.
    """
    q = tuple(q)
    if len(q)!=3 or any(x%2==0 for x in q) or sum(q)%8!=3 or precision<4:
        raise ValueError("three odd twists summing to 3 mod 8 and precision>=4 required")
    z = [1,5,9]
    for n in range(4,precision):
        if triangle_row_quartic(z,q) % (1<<(n+1)):
            z[0] += 1<<(n-2)
    left,middle,right = map(int,triangle_row_from_cover(z,q))
    u,v = left*left-1,right*right-1
    values = tuple(1+i*u+j*v for i,j in GRID)
    roots = [odd_square_root_2(value,precision) for value in values]
    roots[0],roots[1],roots[2],roots[4] = left,middle,right,1
    return {"q":q,"z":tuple(z),"u":u,"v":v,"roots":tuple(roots),"entries":values,
            "precision":precision}


def unit_square_root_odd(value,p,seed,precision):
    if p%2==0 or precision<1 or seed%p==0 or (seed*seed-value)%p:
        raise ValueError("odd prime, unit square-root seed, positive precision required")
    root, modulus = seed%p,p
    for _ in range(1,precision):
        digit = ((value-root*root)//modulus*pow(2*root,-1,p))%p
        root += digit*modulus
        modulus *= p
    return root


def product_orbit_mod_p(roots,p):
    """All eight product residues in each of the four noncentral frames."""
    result = []
    for frame in FRAMES:
        residues = []
        for signs in product((-1,1),repeat=3):
            row = tuple(roots[i]*s%p for i,s in zip(frame,signs))
            residues.append(reduce(lambda a,b:a*b%p,
                                   ((row[i]+row[j])*pow(2,-1,p)%p for i,j in EDGES),1))
        result.append(tuple(residues))
    return tuple(result)


def local_product_counterexample(precision=8):
    p,u,v = (LOCAL_CONTROL[k] for k in ("p","u","v"))
    values = tuple(1+a*u+b*v for a,b in GRID)
    roots = tuple(unit_square_root_odd(value,p,seed,precision)
                  for value,seed in zip(values,LOCAL_CONTROL["roots"]))
    return {"p":p,"u":u,"v":v,"roots":roots,"entries":values,"precision":precision,
            "product_residues":product_orbit_mod_p(roots,p)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision",type=int,default=8)
    args = parser.parse_args()
    print("Universal family: signed odd squarefree q; sum(q)=3 mod 8; z_i are 2-adic units.")
    print("This is a necessary reduction, not a universal exclusion.")
    data = local_product_counterexample(args.precision)
    print(f"401-adic control: u={data['u']}, v={data['v']}, precision={data['precision']}.")
    for frame,residues in zip(FRAMES,data["product_residues"]):
        print("frame",frame,"products",residues,"Legendre",tuple(pow(x,200,401) for x in residues))


if __name__=="__main__":
    main()
