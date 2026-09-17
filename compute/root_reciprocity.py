"""Universal root functions and an exact reciprocity evaluator (entry 149).

This computes necessary local compatibility data, NOT a nonexistence verdict.
See docs/research/root-functions-and-reciprocity.md for proofs and limitations.

    python -m compute.root_reciprocity
    python -m compute.root_reciprocity --candidate -41496/180625 138600/180625
    python -m compute.root_reciprocity --circle 1/5 1/15
    python -m compute.root_reciprocity --symbol 113/114 17/114
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from math import gcd, isqrt, lcm

from sympy import factorint, isprime


LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def entries(c, u, v):
    return (c + u, c - u - v, c + v, c - u + v, c,
            c + u - v, c - v, c + u + v, c - u)


def rational_sqrt(value):
    """The nonnegative rational square root, or None (no floating point)."""
    value = Q(value)
    if value < 0:
        return None
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    return Q(a, b) if a * a == value.numerator and b * b == value.denominator else None


def circle_pair(t):
    """All rational points of x^2+y^2=2 except (-1,-1); t=None adds it."""
    if t is None:
        return Q(-1), Q(-1)
    t = Q(t)
    return (1 + 2*t - t*t) / (1 + t*t), (1 - 2*t - t*t) / (1 + t*t)


def circle_offset(t):
    x, _ = circle_pair(t)
    return x*x - 1


def candidate_report(u, v):
    """Inspect a normalized Lucas grid. Missing roots stay explicitly missing."""
    u, v = Q(u), Q(v)
    values = entries(Q(1), u, v)
    roots = tuple(rational_sqrt(x) for x in values)
    report = {
        "u": str(u), "v": str(v),
        "entries": [str(x) for x in values],
        "positive": all(x > 0 for x in values),
        "nonnegative": all(x >= 0 for x in values),
        "distinct": len(set(values)) == 9,
        "rational_roots": [None if x is None else str(x) for x in roots],
        "rational_root_count": sum(x is not None for x in roots),
        "missing_root_indices": [i for i, x in enumerate(roots) if x is None],
    }
    if all(x is not None for x in roots):
        denominator = lcm(*(x.denominator for x in roots))
        integer_roots = [int(denominator*x) for x in roots]
        common = gcd(*integer_roots)
        report["primitive_integer_roots"] = [x // common for x in integer_roots]
    return report


def _place(p):
    if not isinstance(p, int) or (p != 0 and not isprime(p)):
        raise ValueError("place must be a prime or 0 for the real place")
    return p


def _valuation_unit(value, p):
    value = Q(value)
    if not value:
        raise ValueError("Hilbert symbols require nonzero slots")
    numerator, denominator, valuation = value.numerator, value.denominator, 0
    while numerator % p == 0:
        numerator //= p
        valuation += 1
    while denominator % p == 0:
        denominator //= p
        valuation -= 1
    return valuation, Q(numerator, denominator)


def _unit_mod(unit, modulus):
    return unit.numerator * pow(unit.denominator, -1, modulus) % modulus


def hilbert(a, b, p):
    """Exact quadratic Hilbert symbol in {+1,-1}; p=0 means infinity.

    +1 is a split quaternion (invariant 0), -1 invariant 1/2.
    Rational arguments also represent p-adic square classes at enough precision.
    """
    p = _place(p)
    a, b = Q(a), Q(b)
    if not a or not b:
        raise ValueError("Hilbert symbols require nonzero slots")
    if p == 0:
        return -1 if a < 0 and b < 0 else 1
    av, au = _valuation_unit(a, p)
    bv, bu = _valuation_unit(b, p)
    if p == 2:
        u, v = _unit_mod(au, 8), _unit_mod(bu, 8)
        exponent = ((u - 1)//2)*((v - 1)//2) + av*((v*v - 1)//8) + bv*((u*u - 1)//8)
        return -1 if exponent % 2 else 1
    u, v = _unit_mod(au, p), _unit_mod(bu, p)
    sign = -1 if (av*bv*((p - 1)//2)) % 2 else 1
    if bv % 2 and pow(u, (p - 1)//2, p) == p - 1:
        sign = -sign
    if av % 2 and pow(v, (p - 1)//2, p) == p - 1:
        sign = -sign
    return sign


def symbol_profile(a, b):
    """All possible ramified places of two specified rational numbers.

    Reciprocity ALWAYS holds for nonzero rational a,b. This routine cannot
    reject a rational pair; the unsolved work is constraining local profiles
    using all the magic-square equations before a rational pair is known.
    """
    a, b = Q(a), Q(b)
    if not a or not b:
        raise ValueError("Hilbert symbols require nonzero slots")
    primes = {2}
    for n in (a.numerator, a.denominator, b.numerator, b.denominator):
        primes.update(int(p) for p in factorint(abs(n)))
    values = {str(p) if p else "infinity": hilbert(a, b, p) for p in [0, *sorted(primes)]}
    return {
        "slots": [str(a), str(b)], "symbols": values,
        "nonzero_invariant_places": [p for p, sign in values.items() if sign == -1],
        "reciprocity_product": (-1)**sum(sign == -1 for sign in values.values()),
        "scope": "rational-slot identity; not a magic-square exclusion",
    }


def local_root_symbol(roots, p, precision):
    """Evaluate (r11/r22, r13/r22) from roots modulo p^precision.

    Requires a distinct, nonzero square grid modulo p^precision. This checks
    the finite congruences, NOT existence of a lift. For the three slots,
    their unit parts must be known modulo p (odd p), or modulo 8 (p=2).
    """
    _place(p)
    if p == 0 or not isinstance(precision, int) or precision < 1:
        raise ValueError("local root data need a finite prime and positive precision")
    if len(roots) != 9 or any(not isinstance(x, int) for x in roots):
        raise ValueError("need nine integer residue representatives")
    modulus = p**precision
    roots = tuple(x % modulus for x in roots)
    if any(x == 0 for x in roots):
        raise ValueError("precision does not certify all roots are nonzero")
    needed = 3 if p == 2 else 1
    for i in (0, 2, 4):
        valuation, _ = _valuation_unit(roots[i], p)
        if precision - valuation < needed:
            raise ValueError("insufficient precision to fix the slot's square class")
    values = tuple(x*x % modulus for x in roots)
    if len(set(values)) != 9:
        raise ValueError("precision does not certify nine distinct entries")
    if any((sum(values[i] for i in line) - 3*values[4]) % modulus for line in LINES):
        raise ValueError("roots do not satisfy all magic equations modulo p^precision")
    return hilbert(Q(roots[0], roots[4]), Q(roots[2], roots[4]), p)


def _lift_unit_root(value, seed, power, p, precision):
    """Hensel lift when the derivative is a unit (odd p in our uses)."""
    x, modulus = seed % p, p
    if (pow(x, power, p) - value) % p or gcd(power*x, p) != 1:
        raise ValueError("Hensel seed must be a simple root")
    for _ in range(1, precision):
        digit = ((value - x**power)//modulus * pow(power*x**(power - 1), -1, p)) % p
        x += digit*modulus
        modulus *= p
    return x


def nontrivial_control(precision=8):
    """A genuine Q_113 point by Hensel; alpha has invariant 1/2.

    Its nine underlying integer entries are also positive and distinct.
    Only three are integer squares; the remaining roots here are 113-adic.
    """
    if not isinstance(precision, int) or precision < 3:
        raise ValueError("the control needs precision >= 3")
    p, c, u, v = 113, 114**2, -227, -12707
    values = entries(c, u, v)
    known = {0: 113, 2: 17, 4: 114}
    roots = tuple(known[i] if i in known else _lift_unit_root(
        e, next(x for x in range(1, p) if x*x % p == e % p), 2, p, precision)
        for i, e in enumerate(values))
    return {"p": p, "precision": precision, "c": c, "u": u, "v": v,
            "entries": list(values), "roots_mod_prime_power": list(roots),
            "hilbert_symbol": local_root_symbol(roots, p, precision),
            "lift_reason": "three exact roots; six simple unit roots lift by Hensel"}


def fourth_power_control(p, precision=8):
    """Distinct Q_p configurations whose chosen roots are themselves squares."""
    _place(p)
    if p == 0 or not isinstance(precision, int) or precision < 6:
        raise ValueError("fourth-power controls need a prime and precision >= 6")
    t = 16 if p == 2 else p*p
    values = entries(1, t, 3*t)
    fourth_roots = []
    for value in values:
        if p != 2:
            x = _lift_unit_root(value, 1, 4, p, precision)
        else:
            x = 1
            for n in range(4, precision):
                if (x**4 - value) % (1 << (n + 1)):
                    x += 1 << (n - 2)
        fourth_roots.append(x)
    roots = [x*x % p**precision for x in fourth_roots]
    return {"p": p, "precision": precision, "entries": list(values),
            "fourth_roots": fourth_roots, "roots_mod_prime_power": roots,
            "hilbert_symbol": local_root_symbol(roots, p, precision)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--candidate", nargs=2, type=Q, metavar=("U", "V"))
    modes.add_argument("--circle", nargs=2, type=Q, metavar=("S", "T"))
    modes.add_argument("--symbol", nargs=2, type=Q, metavar=("A", "B"))
    args = parser.parse_args()
    if args.candidate:
        result = candidate_report(*args.candidate)
    elif args.circle:
        result = candidate_report(*(circle_offset(t) for t in args.circle))
    elif args.symbol:
        result = symbol_profile(*args.symbol)
    else:
        result = {
            "status": "evaluator; no new magic-square exclusion",
            "five_rational_root_control": candidate_report(circle_offset(Q(1, 5)), circle_offset(Q(1, 15))),
            "nontrivial_local_evaluation": nontrivial_control(),
            "rational_slots_compensate": symbol_profile(Q(113, 114), Q(17, 114)),
            "split_local_controls": [fourth_power_control(p) for p in (2, 3, 113)],
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
