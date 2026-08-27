"""A9: the discrete-sphere model of the magic square of squares.

In root coordinates a 3x3 magic square of squares with center entry
m^2 has every line (row, column, diagonal) summing to 3 m^2, so each
of the 8 lines is a LATTICE POINT ON THE SINGLE SPHERE

    S(3 m^2) = {(x, y, z) in Z^3 : x^2 + y^2 + z^2 = 3 m^2},

and the whole square is 8 points of S(3 m^2) glued by shared
coordinates (center in 4 lines, corners in 3, edge-centers in 2).
The sphere always contains the TRIVIAL point (m, m, m) — the
all-equal square.  Exact dictionary facts implemented here:

  * the m-SLICE: through-center lines are the points with a
    coordinate equal to m, and these biject with the congrua set
    D(m) of A3 via

        e^2 + f^2 = m^2,  d = 2ef   <-->   (|e - f|, m, e + f),

    since (e-f)^2 + m^2 + (e+f)^2 = 3 m^2 identically: the A3
    machinery IS the discrete-circle slice of this sphere.
  * for odd m, 3 m^2 == 3 (mod 8), and every representation of a
    number == 3 (mod 8) as three squares has ALL coordinates odd
    (exhaustive residue check) — the sphere-side shadow of the F4
    parity facts.
  * the TENSION, quantified: |S(3 m^2)| grows (Gauss: class-number
    size; Duke: equidistribution), while the compatibility ladder on
    the slice (A3's L2/L3/L4: pairs, additive triples, additive
    quadruples in D(m) — a magic square of squares needs an
    additive quadruple) collapses: abundance without compatibility.

Run:  python3 -m compute.discrete_spheres [BOUND]
"""

import sys
from math import isqrt

from compute.congrua_search import congrua_sets


def sphere_points(n):
    """All (x, y, z), 0 <= x <= y <= z, x^2 + y^2 + z^2 = n."""
    out = []
    x = 0
    while 3 * x * x <= n:
        y = x
        rest = n - x * x
        while 2 * y * y <= rest:
            z2 = rest - y * y
            z = isqrt(z2)
            if z * z == z2 and z >= y:
                out.append((x, y, z))
            y += 1
        x += 1
    return out


def slice_points(pts, m):
    """Points with some coordinate equal to m, other than the trivial
    (m, m, m)."""
    return [p for p in pts if m in p and p != (m, m, m)]


def congrua_bijection(m, D):
    """The exact slice <-> D(m) bijection: d = 2ef -> (|e-f|, m, e+f)
    (sorted).  Returns the set of sphere points it produces."""
    pts = set()
    for d in D:
        # e > f > 0, e^2 + f^2 = m^2, 2ef = d:
        # (e+f)^2 = m^2 + d, (e-f)^2 = m^2 - d
        s2, t2 = m * m + d, m * m - d
        s, t = isqrt(s2), isqrt(t2)
        assert s * s == s2 and t * t == t2, (m, d)
        pts.add(tuple(sorted((t, m, s))))
    return pts


def all_odd_residue_fact():
    """x^2+y^2+z^2 == 3 (mod 8) forces x, y, z all odd: exhaustive
    over the 512 residue triples."""
    for x in range(8):
        for y in range(8):
            for z in range(8):
                if (x * x + y * y + z * z) % 8 == 3:
                    if not (x % 2 and y % 2 and z % 2):
                        return False
    return True


def ladder(D):
    """A3's compatibility ladder on the slice: L2 = pairs, L3 =
    additive triples (d1, d2, d1+d2 in D), L4 = additive quadruples
    (u, v, u+v, u-v in D) — an MSS3 with this center needs L4 >= 1."""
    Ds = sorted(D)
    L2 = len(Ds) * (len(Ds) - 1) // 2
    L3 = sum(1 for i, d1 in enumerate(Ds) for d2 in Ds[i + 1:]
             if d1 + d2 in D)
    L4 = sum(1 for u in Ds for v in Ds
             if v < u and u + v in D and u - v in D)
    return L2, L3, L4


def survey(bound):
    """Per-center table: m, |S(3 m^2)| (sphere abundance), slice size
    (= |D(m)|), and the compatibility ladder.  Asserts the slice
    bijection exactly for every m."""
    Dmap = dict(congrua_sets(bound))
    rows = []
    for m in range(1, bound + 1):
        n = 3 * m * m
        pts = sphere_points(n)
        assert (m, m, m) in pts, "trivial point missing?!"
        sl = set(slice_points(pts, m))
        D = Dmap.get(m, set())
        assert congrua_bijection(m, D) == sl, f"slice mismatch at {m}"
        L2, L3, L4 = ladder(D)
        rows.append({"m": m, "sphere": len(pts), "slice": len(sl),
                     "L2": L2, "L3": L3, "L4": L4})
    return rows


def main():
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    assert all_odd_residue_fact()
    rows = survey(bound)
    big = max(rows, key=lambda r: r["sphere"])
    print(f"bound {bound}: slice bijection exact for every m; "
          f"trivial point on every sphere; all-odd residue fact holds")
    print(f"max sphere size |S(3 m^2)| = {big['sphere']} at m = "
          f"{big['m']} (abundance grows)")
    print(f"max L3 = {max(r['L3'] for r in rows)}, "
          f"max L4 = {max(r['L4'] for r in rows)} "
          "(compatibility desert: an MSS3 needs L4 >= 1)")
    top = sorted(rows, key=lambda r: -r["slice"])[:5]
    for r in top:
        print(f"  m = {r['m']}: sphere {r['sphere']}, slice "
              f"{r['slice']}, L2 = {r['L2']}, L3 = {r['L3']}, "
              f"L4 = {r['L4']}")


if __name__ == "__main__":
    main()
