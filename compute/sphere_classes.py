"""A9-T1, first layer: the class-group structure of the magic-square
spheres S(3 m^2).

THE EISENSTEIN ANCHOR.  Every sphere in the vertical family has
n = 3 m^2, so the binary quadratic theory attached to it lives in the
single field Q(sqrt(-3)): the relevant order is Z[m sqrt(-3)] of
discriminant -3 m^2 (conductor m), whose ring class number is
computed by the classical conductor formula

    h(-3 m^2) = (m / 3) * prod_{p | m} (1 - chi(p)/p),   m > 1,
    chi(p) = (-3 | p)  (+1 iff p == 1 mod 3, -1 iff p == 2 mod 3,
    0 for p = 3),

with h(-3) = 1 (the extra units).  Both sides are implemented
first-party (reduced-form enumeration vs the formula) and must agree.

THE GAUSS MAP.  A primitive sphere point v maps to the class of the
binary quadratic form induced on the orthogonal lattice
v^perp cap Z^3 (determinant n, discriminant -4n, even Gram
convention) — Gauss's correspondence, the object of
Aka-Einsiedler-Shapira.  Verified structure (`a9.gauss_map`):

  * the COUNTING IDENTITY  r3*(3 m^2) = 24 h(-3 m^2)  for odd m > 1
    (8 = 24/3 at m = 1, the unit correction) — the sphere's size IS
    an Eisenstein ring class number;
  * fibers of the map are uniform on the sampled range (48 = the
    signed-permutation orbit generically; 24 when 3 | m or for
    self-symmetric points);
  * SLICE CONCENTRATION: the through-center points (the A3 congrua
    slice) occupy only a few classes — e.g. at m = 25 the sphere
    meets 5 classes but the 48 slice points land in just 2 (an
    inverse pair).  Through-center lines are class-constrained;
    outer lines are not: the first genuinely class-group-level
    restriction on magic configurations.

Run:  python3 -m compute.sphere_classes
"""

from math import gcd, isqrt

from compute.discrete_spheres import sphere_points


# --- class numbers of imaginary quadratic discriminants ---------------------

def reduced_forms(D):
    """All reduced positive definite binary forms (a, b, c) of
    discriminant D = b^2 - 4ac < 0: the conditions are
    |b| <= a <= c, with b >= 0 whenever |b| = a or a = c."""
    assert D < 0 and D % 4 in (0, 1)
    out = []
    for b in range(abs(D) % 2, isqrt(-D // 3) + 1, 2):
        ac = (b * b - D) // 4
        a = max(b, 1)
        while a * a <= ac:
            if ac % a == 0:
                c = ac // a
                out.append((a, b, c))
                if 0 < b < a < c:
                    out.append((a, -b, c))
            a += 1
    return sorted(set(out))


def h_disc(D):
    """Class number of the order of discriminant D: PRIMITIVE reduced
    forms only (the orthogonal-lattice forms of the Gauss map may
    well be imprimitive — e.g. (2,2,2) at m = 1 — but the class
    count is over primitive ones)."""
    return sum(1 for (a, b, c) in reduced_forms(D)
               if gcd(gcd(a, abs(b)), c) == 1)


def chi3(p):
    if p == 3:
        return 0
    return 1 if p % 3 == 1 else -1


def h_eisenstein(m):
    """Ring class number h(-3 m^2) by the conductor formula."""
    if m == 1:
        return 1
    h = m
    mm = m
    p = 2
    seen = []
    while p * p <= mm:
        if mm % p == 0:
            seen.append(p)
            while mm % p == 0:
                mm //= p
        p += 1
    if mm > 1:
        seen.append(mm)
    num, den = m, 3
    for p in seen:
        num *= (p - chi3(p))
        den *= p
    assert num % den == 0, (m, num, den)
    return num // den


# --- the Gauss orthogonal-lattice map ---------------------------------------

def reduce_form(a, b, c):
    """Gauss reduction of a positive definite (a, b, c)."""
    while True:
        if c < a:
            a, b, c = c, -b, a
            continue
        if b > a or b <= -a:
            k = (a - b) // (2 * a)
            b, c = b + 2 * a * k, a * k * k + b * k + c
            continue
        if a == c and b < 0:
            b = -b
        return (a, b, c)


def _prim(w):
    g = gcd(gcd(abs(w[0]), abs(w[1])), abs(w[2]))
    return tuple(t // g for t in w) if g else w


def orthogonal_form(v):
    """Reduced form of (v^perp cap Z^3, standard inner product), for
    primitive v; the final determinant assertion det = |v|^2 is the
    saturation certificate."""
    (x, y, z) = v
    n = x * x + y * y + z * z
    def cross(u, w):
        return (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2],
                u[0] * w[1] - u[1] * w[0])

    cands = [c for c in ((0, -z, y), (z, 0, -x), (-y, x, 0)) if any(c)]
    w1 = _prim(cands[0])
    w2 = next(_prim(c) for c in cands[::-1] if any(cross(w1, c)))

    def gram(u, w):
        return (sum(a * a for a in u),
                sum(a * b for a, b in zip(u, w)),
                sum(a * a for a in w))

    a, b, c = gram(w1, w2)
    det = a * c - b * b
    idx = isqrt(det // n)
    while idx > 1:
        progressed = False
        for k in range(2, idx + 1):
            for t in range(k):
                for (u, w, swap) in ((w1, w2, False), (w2, w1, True)):
                    cand = tuple(u[i] + t * w[i] for i in range(3))
                    if all(ci % k == 0 for ci in cand):
                        un = tuple(ci // k for ci in cand)
                        aa, bb, cc = (gram(un, w) if not swap
                                      else gram(w, un))
                        d2 = aa * cc - bb * bb
                        if d2 * k * k == det:
                            if swap:
                                w2 = un
                            else:
                                w1 = un
                            a, b, c, det = aa, bb, cc, d2
                            idx = isqrt(det // n)
                            progressed = True
                            break
                if progressed:
                    break
            if progressed:
                break
        assert progressed, ("saturation stuck", v)
    assert a * c - b * b == n, ("not saturated", v)
    return reduce_form(a, 2 * b, c)


def signed_perm_orbit(p):
    from itertools import permutations
    out = set()
    for q in permutations(p):
        for sx in (1, -1):
            for sy in (1, -1):
                for sz in (1, -1):
                    out.add((sx * q[0], sy * q[1], sz * q[2]))
    return out


def primitive_points_full(n):
    out = set()
    for (x, y, z) in sphere_points(n):
        if gcd(gcd(x, y), z) == 1:
            out |= signed_perm_orbit((x, y, z))
    return sorted(out)


def analyze(m):
    """The class-map data of S(3 m^2): counting identity, fiber
    profile, hit classes, slice classes."""
    from collections import Counter
    n = 3 * m * m
    pts = primitive_points_full(n)
    h = h_eisenstein(m)
    expected = 8 if m == 1 else 24 * h
    assert len(pts) == expected, (m, len(pts), expected)
    cls = Counter(orthogonal_form(v) for v in pts)
    slc = Counter(orthogonal_form(v) for v in pts if m in v or -m in v)
    return {"m": m, "r3star": len(pts), "h": h,
            "classes_hit": len(cls),
            "fibers": sorted(set(cls.values())),
            "slice_classes": len(slc),
            "slice_points": sum(slc.values())}


def main():
    # the two class-number implementations agree
    for m in range(1, 40):
        D = -3 * m * m
        if D % 4 in (0, 1):
            assert h_disc(D) == h_eisenstein(m), (m, h_disc(D),
                                                  h_eisenstein(m))
    print("h(-3 m^2): conductor formula == reduced-form count "
          "for all m < 40 with -3 m^2 a discriminant")
    for m in (1, 5, 9, 13, 17, 25, 29, 33):
        r = analyze(m)
        print(f"m={r['m']:3d}: r3* = {r['r3star']:4d} = 24 h "
              f"(h = {r['h']}), classes hit {r['classes_hit']}, "
              f"fibers {r['fibers']}, slice: {r['slice_points']} pts "
              f"in {r['slice_classes']} classes")
    print("counting identity r3*(3 m^2) = 24 h(-3 m^2) holds "
          "(8 = 24/3 at m = 1); slice concentration visible "
          "(e.g. m = 25: 5 classes hit, slice in 2)")


if __name__ == "__main__":
    main()
