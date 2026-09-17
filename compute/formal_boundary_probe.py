"""Exact finite coefficients for the rational formal-boundary argument.

These are power-series certificates, not rational interior points or a
Brauer-group computation. The general finite-torsor lifting theorem is
an external input; the square-root specialization is elementary.
"""

from fractions import Fraction as Q
from math import isqrt

from compute import universal_twist_probe as u


def multiply(a, b, precision=None):
    if precision is None:
        precision = min(len(a), len(b))
    return tuple(sum((a[j]*b[n-j] for j in range(n+1)
                      if j < len(a) and n-j < len(b)), Q(0))
                 for n in range(precision))


def add(a, b, scale=Q(1)):
    if len(a) != len(b):
        raise ValueError("matching precision required")
    return tuple(x+scale*y for x, y in zip(a, b))


def sqrt_unit(coefficients):
    """Unique formal square root with constant coefficient +1."""
    coefficients = tuple(map(Q, coefficients))
    if not coefficients or coefficients[0] != 1:
        raise ValueError("constant coefficient must be 1")
    roots = [Q(1)]
    for n in range(1, len(coefficients)):
        roots.append((coefficients[n]-sum(roots[j]*roots[n-j]
                                         for j in range(1, n)))/2)
    return tuple(roots)


def rational_root(value):
    value = Q(value)
    if value < 0 or isqrt(value.numerator)**2 != value.numerator or isqrt(value.denominator)**2 != value.denominator:
        raise ValueError("leading coefficient has no rational square root")
    return Q(isqrt(value.numerator), isqrt(value.denominator))


def twist_series(coefficients, shift=0, requested_twist=None):
    """After t=s^2, write f(t)=d*z(s)^2 with a rational Laurent root.

    Input is t^shift times the coefficient list. The output root is
    s^root_order times root_unit. A prescribed unsuitable constant twist
    is rejected: parameter ramification cannot remove constant nonsquares.
    """
    coefficients = tuple(map(Q, coefficients))
    first = next((n for n, x in enumerate(coefficients) if x), None)
    if first is None:
        raise ValueError("no nonzero leading coefficient in the supplied jet")
    leading = coefficients[first]
    twist = u.squareclass(leading) if requested_twist is None else Q(requested_twist)
    if not twist:
        raise ValueError("nonzero twist required")
    prefactor = rational_root(leading/twist)
    unit = tuple(x/leading for x in coefficients[first:])
    root = sqrt_unit(unit)
    dilated = tuple(prefactor*root[n//2] if n % 2 == 0 else Q(0)
                    for n in range(2*len(root)-1))
    return {"twist": twist, "root_order": shift+first,
            "root_unit": dilated, "unit_input": coefficients[first:],
            "leading": leading}


def square_grid(precision=12, slope=3):
    if precision < 2 or not slope*(1-slope)*(1+slope)*(1-2*slope)*(1+2*slope)*(2-slope)*(2+slope):
        raise ValueError("precision >=2 and admissible rational slope required")
    return tuple(sqrt_unit((Q(1), Q(a+b*slope))+(Q(0),)*(precision-2))
                 for a, b in u.GRID)


def root_sum_slots(roots):
    return tuple(tuple(x/2 for x in add(roots[i], roots[j]))
                 for i, j in ((0, 1), (1, 2), (2, 0)))


def cycle_slots(roots):
    precision = len(roots[0])
    frame_values = []
    for frame in u.FRAMES:
        value = (Q(1),)+(Q(0),)*(precision-1)
        for i, j in u.EDGES:
            slot = tuple(x/2 for x in add(roots[frame[i]], roots[frame[j]]))
            value = multiply(value, slot)
        frame_values.append(value)
    corner = tuple(x/2 for x in add(multiply(roots[0], roots[8]), multiply(roots[2], roots[6])))
    return (multiply(frame_values[0], frame_values[1]),
            multiply(frame_values[2], frame_values[3]),
            multiply(frame_values[0], frame_values[2]), corner)


def main():
    roots = square_grid()
    top = tuple(twist_series(x)["twist"] for x in root_sum_slots(roots))
    cycles = tuple(twist_series(x)["twist"] for x in cycle_slots(roots))
    difference = tuple(x/2 for x in add(roots[0], roots[2], -1))
    ramified = twist_series(difference)
    pole = twist_series((1,), shift=-1)
    print("Formal base arc: u=t, v=3t, all roots specialize to +1.")
    print("Root-sum twists:", top, "even-cycle twists:", cycles)
    print("Half root difference: twist", ramified["twist"], "root order", ramified["root_order"])
    print("Pole 1/t: twist", pole["twist"], "root order", pole["root_order"])
    print("Formal lifts and boundary points are not rational interior solutions.")


if __name__ == "__main__":
    main()
