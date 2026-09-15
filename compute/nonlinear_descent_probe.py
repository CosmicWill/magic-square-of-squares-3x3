"""Exact reciprocity, branch, and local certificates for ND.1--ND.5.

The genus and map-degree conclusions use cited curve theory. Neither
high genus nor a failed lift is a rational-point exclusion.
"""

from fractions import Fraction as Q
from functools import reduce
from itertools import product
from math import gcd, lcm

from compute.universal_twist_probe import unit_square_root_odd

NAMES = ("m", "b", "d", "f", "h")
REFLECTION = (6, 7, 8, 3, 4, 5, 0, 1, 2)
RECIPROCAL_SLOTS = (0, 4, 2, 3, 1)


def half_sums(n, r, s):
    n, r, s = map(Q, (n, r, s))
    if not r or not s:
        raise ValueError("nonzero r,s required")
    return ((n*n+r*r)/(2*r), (n*n-s*s)/(2*s),
            (n*n+s*s)/(2*s), (n*n-r*r)/(2*r))


def reciprocity(n, r, s):
    n, r, s = map(Q, (n, r, s))
    if not n*r*s:
        raise ValueError("nonzero n,r,s required")
    return {"n": r*s/n, "r": r, "s": s, "scale": r*s/(n*n)}


def primitive_roots(roots):
    roots = tuple(map(Q, roots))
    multiplier = lcm(*(r.denominator for r in roots))
    integral = tuple(int(multiplier*r) for r in roots)
    content = reduce(gcd, integral)
    if not content:
        raise ValueError("nonzero grid required")
    return tuple(r//content for r in integral)


def fiber_polynomials(k):
    """Ascending coefficients in t; also accepts exceptional k for audits."""
    a = k*k+1
    return ((a*k*k, 0, 0, 0, a),
            (k*k*(a+4*k), 0, 0, 0, a-4*k),
            (a*k*k, 0, -4*k*(k*k-1), 0, a),
            (a*k*k, 0, 4*k*(k*k-1), 0, a),
            (k*k*(a-4*k), 0, 0, 0, a+4*k))


def evaluate(polynomial, t):
    value = 0
    for coefficient in reversed(polynomial):
        value = value*t+coefficient
    return value


def fiber_values(k, t):
    return tuple(evaluate(f, t) for f in fiber_polynomials(k))


def reconstruct(k, t, lifts):
    """Root grid for s=1; caller must verify all five supplied lifts."""
    k, t = Q(k), Q(t)
    if not k or len(lifts) != 5:
        raise ValueError("nonzero ratio and five lifts required")
    x, y, z, w = half_sums(t, k, 1)
    m, b, d, f, h = (Q(v)/(2*k) for v in lifts)
    return x+y, b, z+w, d, m, f, z-w, h, x-y


def boundary_sections(k):
    k = Q(k)
    if k in (0, 1, -1):
        raise ValueError("ratio must avoid 0,+/-1")
    a, plus, minus = k*k+1, k*k+2*k-1, k*k-2*k-1
    at_one = a, plus, minus, plus, minus
    at_k = k*a, k*minus, k*minus, k*plus, k*plus
    for t, roots in ((Q(1), at_one), (Q(-1), at_one), (k, at_k), (-k, at_k)):
        for signs in product((-1, 1), repeat=5):
            yield t, tuple(s*r for s, r in zip(signs, roots))


def determinant(matrix):
    """Fraction-free Bareiss determinant for an integer matrix."""
    a = [list(row) for row in matrix]
    size = len(a)
    previous, sign = 1, 1
    for col in range(size-1):
        pivot_row = next((j for j in range(col, size) if a[j][col]), None)
        if pivot_row is None:
            return 0
        if pivot_row != col:
            a[col], a[pivot_row] = a[pivot_row], a[col]
            sign = -sign
        pivot = a[col][col]
        for row in range(col+1, size):
            for j in range(col+1, size):
                numerator = pivot*a[row][j]-a[row][col]*a[col][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError("Bareiss division was not exact")
                a[row][j] = quotient
            a[row][col] = 0
        previous = pivot
    return sign*a[-1][-1] if size else 1


def resultant(f, g):
    f, g = tuple(reversed(f)), tuple(reversed(g))
    if not f[0] or not g[0]:
        raise ValueError("polynomials must have their stated degree")
    m, n = len(f)-1, len(g)-1
    rows = [(0,)*j+f+(0,)*(n-1-j) for j in range(n)]
    rows += [(0,)*j+g+(0,)*(m-1-j) for j in range(m)]
    return determinant(rows)


def discriminant(f):
    degree = len(f)-1
    derivative = tuple(j*f[j] for j in range(1, len(f)))
    numerator = (-1)**(degree*(degree-1)//2)*resultant(f, derivative)
    quotient, remainder = divmod(numerator, f[-1])
    if remainder:
        raise ArithmeticError("discriminant division was not exact")
    return quotient


def discriminant_factors(k):
    a = k*k+1
    outer = 256*k**6*(a-4*k)**3*(a+4*k)**3
    inner = 256*k**6*(k*k-3)**2*a*a*(3*k*k-1)**2
    return 256*k**6*a**6, outer, inner, inner, outer


def resultant_factors(k):
    a = k*k+1
    opposite = k**8*(k*k-1)**4*a**4
    crossing = 256*k**8*(k*k-2*k-1)**4*(k*k+2*k-1)**4
    return {(0, 1): 4096*k**12*a**4,
            (0, 2): 256*opposite, (0, 3): 256*opposite,
            (0, 4): 4096*k**12*a**4,
            (1, 2): crossing, (1, 3): crossing,
            (1, 4): 65536*k**12*a**4,
            (2, 3): 4096*opposite,
            (2, 4): crossing, (3, 4): crossing}


def cover_data(k):
    """Numerical consequences of the certified characteristic-zero factors."""
    k = Q(k)
    polynomials = fiber_polynomials(k)
    if (any(not f[-1] for f in polynomials)
            or any(not d for d in discriminant_factors(k))
            or any(not r for r in resultant_factors(k).values())):
        raise ValueError("branch collisions or a degree drop require a separate model")
    rank, branch_points = 5, 20
    degree = 1 << rank
    return {"rank": rank, "degree": degree, "branch_points": branch_points,
            "infinity_ramifies": False, "genus": 1+degree*(branch_points-4)//4,
            "center_quotient_degree": degree//2}


def elliptic_quotient(k, t, center_lift):
    a = Q(k)**2+1
    return a*Q(t)**2, a*Q(t)*Q(center_lift)


def double_on_quotient(k, point):
    k = Q(k)
    x, y = map(Q, point)
    if not y:
        return None
    coefficient = k*k*(k*k+1)**2
    slope = (3*x*x+coefficient)/(2*y)
    new_x = slope*slope-2*x
    return new_x, slope*(x-new_x)-y


def local_fiber(precision=8):
    p, k, t = 401, 3, 13
    seeds = (244, 242, 399, 329, 236)
    values = fiber_values(k, t)
    lifts = tuple(unit_square_root_odd(value, p, seed, precision)
                  for value, seed in zip(values, seeds))
    return {"p": p, "k": k, "t": t, "values": values, "lifts": lifts,
            "roots": reconstruct(k, t, lifts), "precision": precision}


def main():
    print("Divisor reciprocity n -> rs/n is a reflected rescaling, not an integer descent.")
    print("Example n=399,r=147,s=19:", reciprocity(399, 147, 19))
    print("Full fiber at k=3:", cover_data(3))
    point = elliptic_quotient(3, 1, 10)
    doubled = double_on_quotient(3, point)
    print("Quotient point", point, "doubles to", doubled, "; t^2 would be", doubled[0]/10)
    print("Known rational AP boundary points per nonexceptional rational fiber:", sum(1 for _ in boundary_sections(3)))
    print("Nonboundary local control: k=3,t=13, all five lifts to 401^8.")
    local_fiber()
    print("No rational interior classification or MSS3 exclusion is asserted.")


if __name__ == "__main__":
    main()
