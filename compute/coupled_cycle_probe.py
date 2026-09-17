"""Exact controls for the coupled even-cycle descent (CC.1--CC.4).

The universal family is infinite. Its explicit rational boundary points
rule out an unrestricted finite-Brauer exclusion for those twists; they
do not settle the canonical 2-adic subdomain or rational interior points.
"""

from fractions import Fraction as Q
from itertools import product
from math import prod

from compute import universal_twist_probe as u

CORNER = (0, 2, 8, 6)
GRAPH_EDGES = tuple(sorted({tuple(sorted((frame[i], frame[j])))
                           for frame in u.FRAMES for i, j in u.EDGES}))
BOUNDARY_SIGNS = (-1, -1, -1, -1, 1, 1, -1, 1, 1)
LOCAL97 = (86, 90, 67, 95, 1, 80, 84, 70, 50)


def frame_products(roots):
    roots = tuple(map(Q, roots))
    m = roots[4]
    return tuple(prod(u.root_sum_slots(tuple(roots[i]/m for i in frame)))
                 for frame in u.FRAMES)


def cycle_slots(roots):
    """Three pairs of triangle products, and the equivalent corner slot."""
    roots = tuple(map(Q, roots))
    top, bottom, left, right = frame_products(roots)
    a, c, i, g = (roots[j] for j in CORNER)
    corner = (a*i+c*g)/(2*roots[4]**2)
    return top*bottom, left*right, top*left, corner


def cycle_mask(vertices):
    edges = {tuple(sorted((vertices[j], vertices[(j+1) % len(vertices)])))
             for j in range(len(vertices))}
    return sum(1 << j for j, edge in enumerate(GRAPH_EDGES) if edge in edges)


def even_cycle_basis():
    a, b, c, d = (cycle_mask(frame) for frame in u.FRAMES)
    return a ^ b, c ^ d, a ^ c, cycle_mask(CORNER)


def binary_span(vectors):
    result = {0}
    for vector in vectors:
        result |= {x ^ vector for x in tuple(result)}
    return result


def leading_boundary_slots(k, l, signs):
    """Leading coefficients at U=t*k,V=t*l, roots specializing to signs.

    Every cycle slot has even order in t. Return its order and the exact
    nonzero leading coefficient. Directions hitting a further degeneracy
    are rejected; their subsequent blowups require a separate chart.
    """
    signs = tuple(signs)
    if len(signs) != 9 or signs[4] != 1 or any(s not in (-1, 1) for s in signs):
        raise ValueError("nine signs with center +1 required")
    coefficients = tuple(a*k+b*l for a, b in u.GRID)
    orders, leading = [], []
    for frame in u.FRAMES:
        order, value = 0, Q(1)
        for i, j in u.EDGES:
            a, b = frame[i], frame[j]
            if signs[a] == signs[b]:
                value *= signs[a]
            else:
                value *= Q(signs[a]*(coefficients[a]-coefficients[b]), 4)
                order += 1
        orders.append(order)
        leading.append(value)
    r, s = signs[0]*signs[8], signs[2]*signs[6]
    corner_order = 0 if r == s else 2
    corner = Q(r) if r == s else Q(r*(l*l-k*k), 4)
    result = tuple((orders[i]+orders[j], leading[i]*leading[j])
                   for i, j in ((0, 1), (2, 3), (0, 2)))
    result += ((corner_order, corner),)
    if any(not coefficient for _, coefficient in result):
        raise ValueError("direction meets an additional vanishing factor")
    return result


def boundary_family(w):
    """A rational boundary point for every positive w divisible by 8."""
    if w < 8 or w % 8:
        raise ValueError("positive multiple of 8 required")
    leading = leading_boundary_slots(1, w, BOUNDARY_SIGNS)
    twists = tuple(u.squareclass(value) for _, value in leading)
    from math import isqrt
    squares = tuple(value/q for (_, value), q in zip(leading, twists))
    lifts = tuple(Q(isqrt(x.numerator), isqrt(x.denominator)) for x in squares)
    if any(z*z != x for z, x in zip(lifts, squares)):
        raise ArithmeticError("boundary square-class normalization failed")
    return {"direction": (1, w), "signs": BOUNDARY_SIGNS,
            "orders": tuple(order for order, _ in leading),
            "leading": tuple(value for _, value in leading),
            "twists": twists, "lifts": lifts}


def branch_parities(k, l, signs):
    """Orders modulo 2 on a generic direction-line divisor of the base.

    Roots with equal radicands use a common square-root seed, multiplied
    by the supplied sign. An opposite-signed equal pair has a simple zero.
    """
    coefficients = tuple(a*k+b*l for a, b in u.GRID)
    valuations = sum((1 << j) for j, (a, b) in enumerate(GRAPH_EDGES)
                     if coefficients[a] == coefficients[b] and signs[a] != signs[b])
    return tuple((mask & valuations).bit_count() % 2 for mask in even_cycle_basis())


def local97(precision=8):
    values = tuple(1+23*a+26*b for a, b in u.GRID)
    roots = tuple(u.unit_square_root_odd(value, 97, seed, precision)
                  for value, seed in zip(values, LOCAL97))
    residues = set()
    for signs in product((-1, 1), repeat=4):
        a, c, i, g = (roots[j]*s for j, s in zip(CORNER, signs))
        residues.add((a*i+c*g)*pow(2, -1, 97) % 97)
    return {"entries": values, "roots": roots, "residues": sorted(residues),
            "precision": precision}


def main():
    data = boundary_family(8)
    print("Universal even-cycle twists: signed odd squarefree, each 1 mod 8.")
    print("Prime support depends only on the primitive direction; no exclusion.")
    print("Boundary direction:", data["direction"], "twists:", data["twists"])
    print("Rescaled rational lifts:", data["lifts"], "orders:", data["orders"])
    witness = local97()
    print("97-adic corner-slot residues for all signs:", witness["residues"])


if __name__ == "__main__":
    main()
