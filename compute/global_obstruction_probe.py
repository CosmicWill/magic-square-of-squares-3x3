"""Exact, lightweight probes for the independent global-obstruction track.

No MSS3 search, Brauer-group computation, or campaign exclusion is claimed.
The optional AP search is explicitly bounded. GB.8 determines the rational
AP-u boundary using a cited theorem and the exact finite certificate here.
The finite-Brauer limitation in the companion document uses cited theorems;
these routines check its concrete surface geometry and local controls.

Run: python -m compute.global_obstruction_probe
Checks: python -m verify --only gb.
"""

from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from math import comb, gcd, isqrt


ENTRY = tuple((a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)
              if (a, b) != (0, 0))
DIFFERENCES = (
    ("u", 1, 0), ("v", 0, 1),
    ("u-v", 1, -1), ("u+v", 1, 1),
    ("u-2v", 1, -2), ("u+2v", 1, 2),
    ("2u-v", 2, -1), ("2u+v", 2, 1),
)
ROOT_TRIANGLE = ((1, 0), (0, 1), (-1, -1))
TRIANGLE_EDGES = ((0, 1), (1, 2), (2, 0))
TRIANGLE_Q = (17, 89, 17 * 89)
TRIANGLE_TWIST = tuple(2*q for q in TRIANGLE_Q)


def entries(u, v):
    return (Q(1),) + tuple(1 + a * u + b * v for a, b in ENTRY)


def rational_square(value):
    value = Q(value)
    return (value >= 0 and isqrt(value.numerator) ** 2 == value.numerator
            and isqrt(value.denominator) ** 2 == value.denominator)


def rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    pivot = 0
    for col in range(len(rows[0]) if rows else 0):
        found = next((j for j in range(pivot, len(rows)) if rows[j][col]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for j in range(len(rows)):
            if j != pivot:
                scale = rows[j][col]
                rows[j] = [x - scale * y for x, y in zip(rows[j], rows[pivot])]
        pivot += 1
    return pivot


def boundary_jacobian(subset):
    """At u=v=z=0, r_i=1 for d_j*z_j^2=a_j*u+b_j*v.

    Columns: eight r_i, u, v, then the new z_j. The derivative of
    d_j*z_j^2 is zero here, so the result is independent of every twist.
    """
    width = 10 + len(subset)
    rows = []
    for i, (a, b) in enumerate(ENTRY):
        row = [0] * width
        row[i], row[8], row[9] = 2, -a, -b
        rows.append(row)
    for j in subset:
        _, a, b = DIFFERENCES[j]
        row = [0] * width
        row[8], row[9] = -a, -b
        rows.append(row)
    return rows


def line_relation(i, j, k):
    """A,B such that L_k=A*L_i+B*L_j, over Q."""
    _, a, b = DIFFERENCES[i]
    _, c, d = DIFFERENCES[j]
    _, e, f = DIFFERENCES[k]
    determinant = a * d - b * c
    if not determinant:
        raise ValueError("dependent direction lines")
    return Q(e * d - f * c, determinant), Q(a * f - b * e, determinant)


def fourth_root_near_one(value, p, precision):
    """Exact lift modulo p^precision; value=1 mod p (odd), 1 mod 16 (2).

    For p=2, x -> x+2^(n-2) changes x^4 by 2^n mod 2^(n+1).
    This chooses x=1 mod 4; existence for every precision is proved in GB.4.
    """
    if p == 2:
        if precision < 4 or value % 16 != 1:
            raise ValueError("2-adic fourth-root lift needs precision >=4 and 1 mod 16")
        x = 1
        for n in range(4, precision):
            if (x ** 4 - value) % (1 << (n + 1)):
                x += 1 << (n - 2)
        return x % (1 << precision)
    if precision < 1 or value % p != 1:
        raise ValueError("odd-prime fourth-root lift needs 1 mod p")
    x, modulus = 1, p
    for _ in range(1, precision):
        digit = ((value - x ** 4) // modulus * pow(4 * x ** 3, -1, p)) % p
        x += digit * modulus
        modulus *= p
    return x


def local_control(p, precision):
    s = 4 if p == 2 else p
    u, v = s * s, 3 * s * s
    values = tuple(int(x) for x in entries(u, v))
    fourth_roots = tuple(fourth_root_near_one(x, p, precision) for x in values)
    return {"p": p, "precision": precision, "u": u, "v": v,
            "entries": values, "fourth_roots": fourth_roots}


def quaternion_split_matrices(root, second_slot):
    """Images of I,J for (root^2, second_slot) in M_2(Q)."""
    root, second_slot = Q(root), Q(second_slot)
    if not root or not second_slot:
        raise ValueError("quaternion slots must be nonzero")
    return ((root, Q(0), Q(0), -root),
            (Q(0), second_slot, Q(1), Q(0)))


def matrix_product(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def triangle_equal_fiber(signs, twists):
    """Whether d_e*z_e^2=r_i+r_j has Q-points at these root signs.

    Only the fiber above u=v=0 is tested, not other degenerate fibers
    or local/global solubility of the covering surface.
    """
    if len(signs) != 3 or len(twists) != 3 or any(s not in (-1, 1) for s in signs):
        raise ValueError("three root signs and three nonzero twists required")
    if any(not Q(d) for d in twists):
        raise ValueError("zero twist")
    return all(rational_square(Q(signs[i] + signs[j]) / d)
               for (i, j), d in zip(TRIANGLE_EDGES, twists))


def triangle_local_edge(p):
    """An edge with d_e/2 square in Q_p for the chosen (34,178,3026).

    p=0 denotes the real place. The doc proves existence for all primes;
    this function uses the exact unit-square criterion at a supplied prime.
    """
    if p == 0:
        return 0
    if p == 2:
        return next(i for i, q in enumerate(TRIANGLE_Q) if q % 8 == 1)
    return next(i for i, q in enumerate(TRIANGLE_Q)
                if q % p and pow(q, (p-1)//2, p) == 1)


def ap_triangle_slots(t, axis):
    """d_i-divided root sums on the two rational AP boundary families.

    The constant row root is +1; for positive d_i a -1 constant root
    forces the other two roots >1, contradicting their squared sum 2.
    """
    t = Q(t)
    denominator = 1 + t*t
    low = (1 - 2*t - t*t) / denominator
    high = (1 + 2*t - t*t) / denominator
    if axis == "u=0":
        row = (Q(1), low, high)
    elif axis == "v=0":
        row = (low, Q(1), high)
    else:
        raise ValueError("unknown AP axis")
    return tuple((row[i]+row[j])/d for (i, j), d in zip(TRIANGLE_EDGES, TRIANGLE_TWIST))


def ap_boundary_search(bound):
    """Reduced t=a/b, |a|<=b<=bound on each of the two AP axes.

    Positive twists force the constant row root to +1 and |t|<=1.
    The omitted parameter infinity has the other two row roots -1,
    which gives a negative pair sum and cannot lift to this positive twist.
    This is only a bounded necessary-row-condition search.
    """
    if bound < 1:
        raise ValueError("positive denominator bound required")
    tested, hits = 0, []
    for b in range(1, bound+1):
        for a in range(-b, b+1):
            if gcd(a, b) != 1:
                continue
            for axis in ("u=0", "v=0"):
                tested += 1
                slots = ap_triangle_slots(Q(a, b), axis)
                if all(rational_square(value) for value in slots):
                    hits.append((axis, a, b))
    return {"denominator_bound": bound, "axis_parameters_tested": tested, "hits": hits}


def ap_normalized_fp_fibers(p, axis, q=TRIANGLE_Q):
    """F_p-rational fibers of the normalized AP genus-three curve.

    Valid only at odd good primes not dividing q. Includes t=+/-1,
    t^2=-1, and infinity via tame unit residues, not singular affine
    zero-coordinate tests. Each result is a base t, not a point count.
    """
    if p == 2 or any(n % p == 0 for n in q):
        raise ValueError("only odd good primes are supported")
    nums = ((1,-1), (1,0,-1), (1,1)) if axis == "u=0" else ((1,-1), (1,1), (1,0,-1))
    if axis not in ("u=0", "v=0"):
        raise ValueError("unknown AP axis")
    def leading(poly, t):
        if t is None:
            return -len(poly)+1, poly[-1] % p
        for order in range(len(poly)):
            unit = sum(comb(j,order)*poly[j]*pow(t,j-order,p)
                       for j in range(order,len(poly))) % p
            if unit:
                return order, unit
        raise ValueError("zero polynomial")
    fibers = []
    for t in (*range(p), None):
        vals, units = [], []
        for numerator, coefficient in zip(nums,q):
            nv, nu = leading(numerator,t)
            dv, du = leading((coefficient,0,coefficient),t)
            vals.append(nv-dv)
            units.append(nu*pow(du,-1,p) % p)
        possible = True
        for mask in range(1,8):
            chosen = [i for i in range(3) if mask >> i & 1]
            if sum(vals[i] for i in chosen) % 2:
                continue
            unit = 1
            for i in chosen:
                unit = unit*units[i] % p
            if pow(unit,(p-1)//2,p) != 1:
                possible = False
                break
        if possible:
            fibers.append(t)
    return fibers


def ternary_representatives(n, z_coefficient):
    """All nonnegative (x,y,z) with 2*x^2+y^2+c*z^2=n, with sign weights.

    The bounds are exhaustive consequences of positive definiteness, not
    a height cutoff for rational points. Zero coordinates have one sign.
    """
    if n < 0 or z_coefficient <= 0:
        raise ValueError("nonnegative n and positive coefficient required")
    rows = []
    for x in range(isqrt(n//2)+1):
        for z in range(isqrt((n-2*x*x)//z_coefficient)+1):
            y2 = n - 2*x*x - z_coefficient*z*z
            y = isqrt(y2)
            if y*y == y2:
                triple = (x, y, z)
                rows.append((triple, 2**sum(a != 0 for a in triple)))
    return sorted(rows)


def tunnell_odd_certificate(n):
    """Unconditional *necessary* condition for positive odd squarefree n.

    A mismatch certifies noncongruence by the CITED Tunnell theorem.
    Equality is deliberately called inconclusive, never a positive verdict.
    """
    if n <= 0 or n % 2 == 0 or any(n % (p*p) == 0 for p in range(2, isqrt(n)+1)):
        raise ValueError("positive odd squarefree integer required")
    reps = {c: ternary_representatives(n, c) for c in (8, 32)}
    counts = {c: sum(weight for _, weight in reps[c]) for c in reps}
    mismatch = counts[8] != 2*counts[32]
    return {"n": n, "representatives": reps, "counts": counts,
            "coefficient": counts[32] - counts[8]//2,
            "verdict": "noncongruent (CITED Tunnell)" if mismatch else "inconclusive"}


def ap_quartic_to_triangle(t, y, n):
    """A nonexceptional point y^2=n*(1-t^4) gives a rational triangle.

    Used to reduce the AP-u boundary to noncongruence of 89. This map
    retains its denominators; t=0 and y=0 require separate fiber analysis.
    """
    t, y, n = Q(t), Q(y), Q(n)
    if n <= 0 or not t or not y or y*y != n*(1-t**4):
        raise ValueError("nonexceptional rational point on the positive-n quartic required")
    return (abs(y/t), abs(2*n*t/y), abs(n*(1+t**4)/(t*y)))


def triangle_row_from_cover(z, q=TRIANGLE_Q):
    """Inverse of the three root-sum equations, before the row constraint."""
    if len(z) != 3 or len(q) != 3:
        raise ValueError("three coordinates and twists required")
    s1, s2, s3 = (Q(a)*Q(b)**2 for a, b in zip(q, z))
    return (s1-s2+s3, s1+s2-s3, -s1+s2+s3)


def triangle_row_quartic(z, q=TRIANGLE_Q):
    """Zero iff the root-sum row has A^2+B^2+C^2=3 (not all MSS3 conditions)."""
    s = tuple(Q(a)*Q(b)**2 for a, b in zip(q, z))
    return 3*sum(a*a for a in s)-2*sum(a*b for a, b in combinations(s, 2))-3


def cross_ratio(indices):
    """Projective determinant formula, including the direction at infinity."""
    pts = [(DIFFERENCES[i][2], -DIFFERENCES[i][1]) for i in indices]
    def det(p, q):
        return p[0] * q[1] - p[1] * q[0]
    p, q, r, s = pts
    return Q(det(p, r) * det(q, s), det(p, s) * det(q, r))


def cross_ratio_orbit(lam):
    return frozenset((lam, 1-lam, 1/lam, 1/(1-lam),
                      lam/(lam-1), (lam-1)/lam))


def four_line_atlas():
    """70 four-line subsets grouped by geometric branch cross-ratio.

    j is that of the branch double cover. The geometric boundary curve
    has the same j (see GB.6); this does not identify its Q-twist/torsor.
    """
    groups = defaultdict(list)
    for subset in combinations(range(8), 4):
        lam = cross_ratio(subset)
        j = 256 * (1 - lam + lam * lam) ** 3 / (lam * lam * (1-lam) ** 2)
        canonical = min(cross_ratio_orbit(lam))
        groups[(canonical, j)].append(subset)
    return [{"lambda": lam, "j": j, "subsets": subsets}
            for (lam, j), subsets in sorted(groups.items())]


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ap-bound", type=int, help="also search the AP boundary to this denominator")
    parser.add_argument("--boundary-certificate", action="store_true",
                        help="print the complete finite Tunnell certificate used in GB.8")
    args = parser.parse_args()
    print("Independent global-obstruction probe; no new MSS3 exclusions.")
    print("Smooth all-equal point: Jacobian rank", rank(boundary_jacobian(())))
    print("Direction covers: 8 single-line, 28 two-line, 56 three-line, 70 four-line sets.")
    print(f"Root-sum candidate: d={TRIANGLE_TWIST}; no rational all-equal fiber,")
    print("  but a smooth all-equal fiber point over every completion (GB.7).")
    groups = four_line_atlas()
    print(f"Four-line boundary atlas: 70 subsets, {len(groups)} geometric cross-ratio types.")
    for row in groups:
        labels = [DIFFERENCES[i][0] for i in row["subsets"][0]]
        print(f"  count={len(row['subsets']):2}  lambda={row['lambda']}  "
              f"j={row['j']}  representative={labels}")
    print("Exact checks: python -m verify --only gb.")
    if args.ap_bound is not None:
        print("AP boundary (bounded necessary conditions only):", ap_boundary_search(args.ap_bound))
    if args.boundary_certificate:
        print("AP-u exclusion certificate (see GB.8 for map and exceptional fibers):")
        print(tunnell_odd_certificate(89))


if __name__ == "__main__":
    main()
