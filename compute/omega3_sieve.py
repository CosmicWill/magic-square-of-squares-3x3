"""THE LOCAL SIEVE for omega = 3 quadruple classes (entry 102).

A real quadruple gives three primitive frames (c_i, s_i) = (a_i^2 - b_i^2,
2 a_i b_i) with gcd(a_i, b_i) = 1 and a_i + b_i odd (pi_i = a_i + i b_i a
Gaussian prime of odd norm), so
    c_i odd,  s_i = 0 mod 4,  and (c_i, s_i) != (0, 0) mod every prime l
(l | c_i and l | s_i would force l = p_i and then c_i^2 + s_i^2 = l^2 gives a
degenerate frame), and the two relations R1 = R2 = 0 hold EXACTLY, hence
modulo every m.  R1, R2 are homogeneous of degree 2a_i in each frame pair, so a
frame may be scaled by a unit mod m without changing the vanishing: mod 2^k
normalize c_i = 1 (odd = unit), s_i in {0, 4, 8, ...}; mod an odd prime power
the frame is a point of P^1 -- (1, s) or (c, 1) with l | c.  For a prime
l = 1 mod 4 a frame with c^2 + s^2 = 0 mod l has norm l, and the three primes
are distinct, so at most one frame may lie on that locus.  If no admissible
residue triple satisfies both congruences the class is DEAD -- for every
choice of three distinct split primes.  Sound; independent of the curve
geometry; applies to every class.

NEGATIVE RESULT (entry 102): the sieve is VACUOUS for these relations.  Every
element is an imaginary part, so it vanishes when all three frames are real
(s_1 = s_2 = s_3 = 0), and real frames can have s divisible by any power of 2
and by any odd prime (a = 32, b = 3 gives s = 192 and p = 1033).  The residue
class with all s_i = 0 mod m is therefore admissible for every m and always
solves both congruences: no modulus ever excludes a class (checked on dead,
finite and unknown classes alike -- the solution counts are all positive).  The
omega = 2 ladder's parity kills worked through EXACT 2-adic valuations of the
lever values, not through residues; a valuation layer, not a residue sieve, is
what could transfer.  Kept as the record of the attempt.
"""
from __future__ import annotations
import sympy as sp

from compute.omega3 import relations, FR, c1, s1, c2, s2, c3, s3, BOX

MODULI = (64, 3, 9, 5, 7, 11, 13, 17, 25, 49)


def _factor_primes(m):
    return sorted(sp.factorint(m))


def frame_points(m):
    """Admissible normalized residue pairs mod m, each with a flag 'norm-zero'
    (c^2 + s^2 = 0 mod every prime of m) used for the distinct-primes rule."""
    pts = []
    if m % 2 == 0:
        k = m
        for s in range(0, k, 4):
            pts.append(((1, s), False))
        return pts
    ps = _factor_primes(m)
    for s in range(m):
        pts.append(((1, s), all((1 + s * s) % l == 0 for l in ps)))
    for c in range(m):
        if all(c % l == 0 for l in ps):
            pts.append(((c, 1), all((c * c + 1) % l == 0 for l in ps)))
    return pts


def sieve_class(cand, moduli=MODULI):
    """Returns (verdict, modulus, detail): 'dead' with the first modulus that
    admits no solution, else ('survives', None, {m: number of solutions})."""
    R1, R2 = relations(cand)
    f1 = sp.lambdify((c1, s1, c2, s2, c3, s3), R1, "math")
    f2 = sp.lambdify((c1, s1, c2, s2, c3, s3), R2, "math")
    counts = {}
    for m in moduli:
        pts = frame_points(m)
        ps = _factor_primes(m)
        one_mod_4 = [l for l in ps if l % 4 == 1]
        n = 0
        for (a1, b1), z1 in pts:
            for (a2, b2), z2 in pts:
                for (a3, b3), z3 in pts:
                    if one_mod_4 and (z1 + z2 + z3) > 1:
                        continue                        # at most one frame of norm l
                    if int(f1(a1, b1, a2, b2, a3, b3)) % m == 0 and int(f2(a1, b1, a2, b2, a3, b3)) % m == 0:
                        n += 1
        counts[m] = n
        if n == 0:
            return "dead", m, counts
    return "survives", None, counts
