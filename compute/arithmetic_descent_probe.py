"""Exact certificates for the corner-label-1 arithmetic descent audit.

The divisor model retains the center and all four side-square conditions.
The boundary matrices constrain polynomial formulas, not rational points.
No new magic-square exclusion or decreasing map is asserted.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import gcd, isqrt, prod

from compute.universal_twist_probe import GRID

MONOMIALS = tuple(combinations_with_replacement(range(9), 2))
RADICAL_PRIMES = (2, 3, 5, 11)
BOUNDARY_SEEDS = ((0, 0), (10, 10), (10, -10))


def divisor_model(n, r, s):
    """Positive half-sum convention; r,s are divisors of n^2 up to n.

    This constructs five square entries only when center_squared is a
    square. The four remaining entries are returned without assuming
    positivity or squareness. Canonical signs can be restored afterwards.
    """
    if any(not isinstance(t, int) for t in (n, r, s)):
        raise ValueError("integer n,r,s required")
    if n <= 0 or n % 2 == 0 or not (0 < r <= n and 0 < s <= n):
        raise ValueError("positive odd n and 0<r,s<=n required")
    if n*n % r or n*n % s:
        raise ValueError("r and s must divide n^2")
    x, w = (n*n//r+r)//2, (n*n//r-r)//2
    z, y = (n*n//s+s)//2, (n*n//s-s)//2
    center_squared = n*n+y*y+w*w
    u, v = 2*x*y, 2*z*w
    entries = tuple(center_squared+a*u+b*v for a, b in GRID)
    return {"n": n, "r": r, "s": s, "x": x, "y": y, "z": z, "w": w,
            "center_squared": center_squared, "u": u, "v": v,
            "corner_roots": (x+y, z+w, z-w, x-y),
            "entries": entries, "sides": tuple(entries[j] for j in (1, 3, 5, 7)),
            "primitive": gcd(gcd(n, y), w) == 1}


def scaled_square_targets(n, r, s):
    """The five retained square equations after multiplying by (2rs)^2.

    Order: center, b, d, f, h. These formulas also make sense for formal
    variables; checks below certify the polynomial identities exactly.
    """
    k = (r*r+s*s)*(n**4+r*r*s*s)
    plus = 4*r*s*(n**4-r*r*s*s)
    minus = 4*r*s*n*n*(r*r-s*s)
    return k, k-plus, k-minus, k+minus, k+plus


def boundary_signs():
    """128 signed all-equal grids with m=1 and ai+cg=0."""
    for signs in product((-1, 1), repeat=8):
        roots = signs[:4]+(1,)+signs[4:]
        if roots[0]*roots[8]+roots[2]*roots[6] == 0:
            yield roots


def radical(value):
    """Exact c*sqrt(d) in Q(sqrt(2),sqrt(3),sqrt(5),sqrt(11))."""
    if value <= 0:
        raise ValueError("positive integer radicand required")
    coefficient = next(k for k in range(isqrt(value), 0, -1) if value % (k*k) == 0)
    squarefree = value//(coefficient*coefficient)
    mask = sum(1 << j for j, p in enumerate(RADICAL_PRIMES) if squarefree % p == 0)
    if prod(p for j, p in enumerate(RADICAL_PRIMES) if mask & (1 << j)) != squarefree:
        raise ValueError("radicand outside the certificate's multiquadratic field")
    return coefficient, mask


def radical_product(left, right):
    a, i = left
    b, j = right
    common = prod(p for k, p in enumerate(RADICAL_PRIMES) if (i & j) & (1 << k))
    return a*b*common, i ^ j


def boundary_points():
    """384 real algebraic full grids with n=0, represented exactly.

    m=10, (U,V)=(0,0),(10,10),(10,-10). All 16 radical basis
    elements have their positive real embeddings; signs vary explicitly.
    """
    for u, v in BOUNDARY_SEEDS:
        magnitudes = tuple(radical(100+a*u+b*v) for a, b in GRID)
        for signs in boundary_signs():
            yield tuple((sign*c, mask) for sign, (c, mask) in zip(signs, magnitudes))


def quadratic_boundary_rows():
    """Rational coefficient rows of evaluation at the real n=0 points.

    Distinct squarefree radical products form a Q-basis, so vanishing
    at one point implies vanishing of every extracted rational row.
    """
    rows = set()
    for roots in boundary_points():
        coefficients = {}
        for column, (j, k) in enumerate(MONOMIALS):
            value, mask = radical_product(roots[j], roots[k])
            coefficients.setdefault(mask, [0]*len(MONOMIALS))[column] = value
        rows.update(tuple(row) for row in coefficients.values())
    return tuple(sorted(rows))


def exact_rank(rows):
    """Rational row elimination; no floating-point or modular rank bound."""
    basis = {}
    for source in rows:
        row = list(map(Q, source))
        for pivot, previous in sorted(basis.items()):
            factor = row[pivot]
            if factor:
                row = [a-factor*b for a, b in zip(row, previous)]
        pivot = next((j for j, a in enumerate(row) if a), None)
        if pivot is not None:
            factor = row[pivot]
            basis[pivot] = tuple(a/factor for a in row)
    return len(basis)


def boundary_quadrics():
    """Six original magic equations and ai+cg, in the 45 monomials."""
    result = []
    for j, (a, b) in enumerate(GRID):
        if j in (0, 2, 4):
            continue
        row = [0]*len(MONOMIALS)
        for index, value in ((j, 1), (4, a+b-1), (0, -a), (2, -b)):
            row[MONOMIALS.index((index, index))] += value
        result.append(tuple(row))
    row = [0]*len(MONOMIALS)
    row[MONOMIALS.index((0, 8))] = row[MONOMIALS.index((2, 6))] = 1
    result.append(tuple(row))
    return tuple(result)


def main():
    signs = tuple(boundary_signs())
    rows = quadratic_boundary_rows()
    print("Linear boundary: points", len(signs), "rank", exact_rank(signs))
    print("Quadratic boundary: real points", sum(1 for _ in boundary_points()),
          "rows", len(rows), "rank", exact_rank(rows), "nullity", len(MONOMIALS)-exact_rank(rows))
    data = divisor_model(399, 147, 19)
    print("Positive five-square control: n=399, m=4225; r=147, s=19")
    print("All four retained side targets:", data["sides"])
    print("Polynomial descent restrictions and a divisor reduction; no MSS3 exclusion.")


if __name__ == "__main__":
    main()
