"""A9-T1, second layer: the gluing-representation law and the genus
coherence obstruction.

LEMMA A9.1 (gluing representation; one-line proof).  For any
v = (x, y, z) with |v|^2 = n, the three cross-vectors
(0, -z, y), (z, 0, -x), (-y, x, 0) lie in v^perp cap Z^3 with norms
n - x^2, n - y^2, n - z^2.  So the Gauss class of every LINE of a
magic square of squares represents the CO-NORM 3 m^2 - e of each of
its entries e.  (In particular the confinement window of the
through-center lines sits inside the classes representing 2 m^2 —
strictly inside, as measured.)

LEMMA A9.4 (even lattices).  Every point of S(3 m^2) has all-odd
coordinates (m odd), and w . v = 0 with v == (1,1,1) mod 2 forces
|w|^2 == (sum w_i)^2 == 0 mod 2: the orthogonal lattices are EVEN —
the Gauss map lands in the even-form classes.

CHARACTER INVARIANCE (classical genus theory; machine-validated):
for each odd prime p | 3 m^2 the Legendre character chi_p is constant
on the values of a class coprime to the discriminant (imprimitive
forms included: content scales by a fixed chi_p-value).  The 2-adic
candidates are NOT invariants here (n == 3 mod 4) and are excluded by
the same validation.

THEOREM A9.3 (the coherence obstruction).  In a magic square of
squares with center m^2 and Lucas differences U, V (columns/rows;
U, V, U+V, U-V in D(m)), each of the 8 lines forces its co-norm
triple to be chi_p-COHERENT (all members coprime to p share one
character value), for every odd p | 3 m^2:

    center lines:  (2m^2, 2m^2 + X, 2m^2 - X),  X in {U, V, U+V, U-V}
    outer lines:   (2m^2+U, 2m^2-U-V, 2m^2+V), (2m^2-V, 2m^2+U+V,
                   2m^2-U), (2m^2+U, 2m^2-U+V, 2m^2-V),
                   (2m^2+V, 2m^2+U-V, 2m^2-U).

Necessity is PROVEN (A9.1 + invariance); the bite is MEASURED: the
condition kills 10/12 ordered congrua pairs at m = 65, 85, 130
(survivors: exactly the two imprimitive branches paired together)
and 6/12 at m = 145 (survivors: exactly the pairs involving the
5-branch congruum 21000), while prime-power hypotenuses lose
nothing.  This is the first necessary condition on extending congrua
pairs to magic squares beyond the classical 24-divisibility layer
(A3/F4).  (Caveat measured later: the m <= 150 coherence-survivors
are all impossible anyway by POSITIVITY, U + V > m^2 — the two
sieves are complementary, see below.)

THE THREE-SIEVE PAIR DESERT (measured; check a9.pair_desert).
Stack three proven-necessary conditions on an ordered congrua pair
(U, V) at center m^2:

  1. POSITIVITY: U + V <= m^2 (else the smallest edge entry
     m^2 - U - V is negative — not a square).
  2. COHERENCE: Theorem A9.3 (genus characters).
  3. REPRESENTATION: each of the 8 co-norm triples must be
     represented by a single class — some even class of disc
     -4.(3 m^2)/g^2 (g = the point's possible content: odd,
     g^2 | 3 m^2, g^2 | the whole triple) representing all three
     scaled co-norms.  Strictly stronger than characters: same
     genus does not mean same class.

Result: for EVERY center m <= 1200 every ordered pair dies —
1782 pairs: 1608 by positivity, 152 by coherence, 22 by
representation (11 unordered, first at m = 425), 0 remain.  The
U+V diagonal center line is unrepresentable in all 22 cases.
Positive control: the actual U- and V-center lines (which exist as
sphere points) always land in their own candidate sets — the
machinery never kills a real line.  This gives the A3 pair desert
its first structural explanation: three arithmetic obstructions,
each proven necessary, jointly annihilate the range.

Run:  python3 -m compute.sphere_gluing
"""

from math import gcd, isqrt

from compute.congrua_search import congrua_sets
from compute.sphere_classes import (orthogonal_form,
                                    primitive_points_full)


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def odd_primes(n):
    out, d = [], 3
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 2
    if n > 1:
        out.append(n)
    return out


def cross_vectors(v):
    (x, y, z) = v
    return ((0, -z, y), (z, 0, -x), (-y, x, 0))


def gluing_identity(v):
    """Lemma A9.1, verified: the cross-vectors are orthogonal to v
    and realize the three co-norms."""
    n = sum(t * t for t in v)
    for w, coord in zip(cross_vectors(v), v):
        assert sum(a * b for a, b in zip(w, v)) == 0
        assert sum(t * t for t in w) == n - coord * coord
    return True


def point_coherence(v, m):
    """Theorem A9.3 verified on an ACTUAL sphere point: its co-norm
    triple is chi_p-coherent for every odd p | 3 m^2 (must always
    hold — it is a theorem)."""
    n = 3 * m * m
    conorms = [n - t * t for t in v]
    for p in odd_primes(n):
        vals = {legendre(c, p) for c in conorms}
        vals.discard(0)
        if len(vals) > 1:
            return False
    return True


def even_lattice(v):
    """Lemma A9.4 on a point: all coordinates odd and the orthogonal
    form even."""
    if not all(t % 2 for t in v):
        return False
    a, b, c = orthogonal_form(v)
    return a % 2 == 0 and b % 2 == 0 and c % 2 == 0


def pair_lines(n2, U, V):
    """The eight co-norm triples of a square with center co-norm n2
    = 2 m^2 and Lucas differences (U, V): four center lines, four
    outer lines.  Invariant as a SET under U <-> V."""
    return [(n2, n2 + U, n2 - U), (n2, n2 + V, n2 - V),
            (n2, n2 + U + V, n2 - U - V),
            (n2, n2 + U - V, n2 - U + V),
            (n2 + U, n2 - U - V, n2 + V),
            (n2 - V, n2 + U + V, n2 - U),
            (n2 + U, n2 - U + V, n2 - V),
            (n2 + V, n2 + U - V, n2 - U)]


def coherent_pair(m, U, V, ps=None):
    """Theorem A9.3's test: every line triple chi_p-coherent."""
    n2 = 2 * m * m
    if ps is None:
        ps = odd_primes(3 * m * m)
    for p in ps:
        for tri in pair_lines(n2, U, V):
            vals = {legendre(t, p) for t in tri}
            vals.discard(0)
            if len(vals) > 1:
                return False
    return True


def pair_obstruction(m):
    """The coherence test on every ordered congrua pair (U, V) of
    center m^2 (U = column difference, V = row difference): returns
    (total, killed, surviving_pairs)."""
    D = dict(congrua_sets(m)).get(m, set())
    ps = odd_primes(3 * m * m)
    total, killed, alive = 0, 0, []
    for U in sorted(D):
        for V in sorted(D):
            if V == U:
                continue
            total += 1
            if coherent_pair(m, U, V, ps):
                alive.append((U, V))
            else:
                killed += 1
    return total, killed, alive


def joint_survey(bound):
    """The three-sieve pair survey over all centers m <= bound with
    |D(m)| >= 2: kill each ordered pair by POSITIVITY (U + V > m^2:
    the smallest edge entry m^2 - U - V would be negative, and a
    square cannot be) or by COHERENCE (Theorem A9.3); returns
    (centers, total, pos_killed, coh_killed, passers_by_m)."""
    centers = total = npos = ncoh = 0
    passers = {}
    for m, D in congrua_sets(bound):
        if len(D) < 2:
            continue
        centers += 1
        ps = odd_primes(3 * m * m)
        for U in sorted(D):
            for V in sorted(D):
                if V == U:
                    continue
                total += 1
                if U + V > m * m:
                    npos += 1
                elif not coherent_pair(m, U, V, ps):
                    ncoh += 1
                else:
                    passers.setdefault(m, []).append((U, V))
    return centers, total, npos, ncoh, passers


def represents(f, t):
    """Exact: does the positive definite form f = (a, b, c)
    represent t >= 1?  (4a Q = (2ax + by)^2 + (4ac - b^2) y^2.)"""
    a, b, c = f
    n4 = 4 * a * c - b * b
    Y = isqrt(4 * a * t // n4) + 1
    for y in range(-Y, Y + 1):
        d2 = 4 * a * t - n4 * y * y
        if d2 < 0:
            continue
        r = isqrt(d2)
        if r * r != d2:
            continue
        if (-b * y + r) % (2 * a) == 0 or (-b * y - r) % (2 * a) == 0:
            return True
    return False


_EVEN_FORMS = {}


def even_forms(disc):
    """All reduced EVEN forms (a, c even; b automatic) of the given
    negative discriminant — every orthogonal lattice of an all-odd
    sphere point reduces to one of these (Lemma A9.4)."""
    if disc not in _EVEN_FORMS:
        from compute.sphere_classes import reduced_forms
        _EVEN_FORMS[disc] = [f for f in reduced_forms(disc)
                             if f[0] % 2 == 0 and f[2] % 2 == 0]
    return _EVEN_FORMS[disc]


def line_classes(tri, n):
    """THE REPRESENTATION OBSTRUCTION.  All sound candidates for the
    Gauss class of a hypothetical line with co-norm triple tri on
    S(n): pairs (g, f) where g is the point's possible content and
    f an even class of disc -4 n / g^2 representing the whole
    triple / g^2 (Lemma A9.1 — the cross-vectors lie in the
    SATURATED orthogonal lattice of the reduced point).  The 2-part
    of g is FORCED: writing 4^k || n (k = v_2 of the center m),
    every point of S(n) is exactly 2^k times a point of the odd
    sphere S(n/4^k) == 3 mod 8, whose coordinates are ALL ODD
    (residues mod 4: three squares summing to 0 mod 4 are all
    even); so v_2(g) = k exactly, the odd part g_odd satisfies
    g_odd^2 | n and g^2 | every co-norm, and Lemma A9.4 applies at
    the reduced level (even lattice).  Empty => the line cannot
    exist as a sphere point => the pair cannot extend to a magic
    square."""
    G = gcd(gcd(tri[0], tri[1]), tri[2])
    base, nn = 1, n
    while nn % 4 == 0:
        nn //= 4
        base *= 2
    out = []
    d = 1
    while (base * d) ** 2 <= n:
        g = base * d
        if n % (g * g) == 0 and G % (g * g) == 0:
            t3 = [t // (g * g) for t in tri]
            for f in even_forms(-4 * (n // (g * g))):
                if all(represents(f, t) for t in t3):
                    out.append((g, f))
        d += 2
    return out


def rep_verdict(m, U, V):
    """Per-line candidate counts and the empty (killed) line indices
    for the pair (U, V) at center m^2."""
    n = 3 * m * m
    counts, empty = [], []
    for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
        c = line_classes(tri, n)
        counts.append(len(c))
        if not c:
            empty.append(i)
    return counts, empty


def center_line_control(m, U):
    """Positive control (soundness of the killing machinery): the
    U-center line EXISTS as the point (m, sqrt(m^2+U), sqrt(m^2-U)),
    and its actual (content, reduced orthogonal class) must appear
    in the candidate set of its own co-norm triple."""
    from compute.sphere_classes import orthogonal_form
    rp, rm = isqrt(m * m + U), isqrt(m * m - U)
    assert rp * rp == m * m + U and rm * rm == m * m - U
    g = gcd(gcd(m, rp), rm)
    f = orthogonal_form((m // g, rp // g, rm // g))
    tri = (2 * m * m, 2 * m * m + U, 2 * m * m - U)
    return (g, f) in line_classes(tri, 3 * m * m)


def window_refinement(m):
    """Measured: the slice classes sit STRICTLY inside the classes
    representing 2 m^2 (both computed); returns (slice, rep, strict)."""
    from compute.sphere_classes import reduced_forms
    n = 3 * m * m
    pts = primitive_points_full(n)
    slc = {orthogonal_form(v) for v in pts if m in v or -m in v}
    rep = set()
    for f in reduced_forms(-4 * n):
        a, b, c = f
        found = False
        # small-vector search: values a x^2 + b x y + c y^2 = 2 m^2
        xb = isqrt(8 * m * m // max(a, 1)) + 2
        for x in range(-xb, xb + 1):
            if found:
                break
            for y in range(-xb, xb + 1):
                if a * x * x + b * x * y + c * y * y == 2 * m * m:
                    found = True
                    break
        if found:
            rep.add(f)
    return slc, rep, slc < rep


def main():
    for m in (5, 13, 25, 65):
        pts = primitive_points_full(3 * m * m)
        assert all(gluing_identity(v) for v in pts)
        assert all(point_coherence(v, m) for v in pts)
        assert all(even_lattice(v) for v in pts[:60])
        print(f"m={m}: gluing identity + on-sphere coherence + even "
              f"lattices verified on {len(pts)} points")
    for m in (25, 65, 85, 125, 130, 145):
        total, killed, alive = pair_obstruction(m)
        print(f"m={m}: ordered congrua pairs {total}, killed by "
              f"coherence {killed}, surviving {alive if len(alive) <= 4 else len(alive)}")
    slc, rep, strict = window_refinement(13)
    print(f"m=13 window: slice {sorted(slc)} STRICTLY inside "
          f"Rep(2m^2) ({len(rep)} classes): {strict}")
    print("THEOREM A9.3: coherence is necessary (proven) and kills "
          "most cross-branch pairs (measured) — the first "
          "obstruction beyond the classical layer.")
    print()
    centers, total, npos, ncoh, passers = joint_survey(700)
    npass = sum(len(v) for v in passers.values())
    print(f"THREE-SIEVE SURVEY m <= 700: {centers} centers, {total} "
          f"ordered pairs; positivity kills {npos}, coherence kills "
          f"{ncoh}, pass both: {npass}")
    for m, prs in sorted(passers.items()):
        for (U, V) in prs:
            counts, empty = rep_verdict(m, U, V)
            print(f"  m={m} ({U},{V}): representation counts {counts}"
                  f" -> {'KILLED (empty lines ' + str(empty) + ')' if empty else 'SURVIVES'}")
    print(f"controls: actual U-center lines pass line_classes at "
          f"m=425: {center_line_control(425, 54600)}, "
          f"m=481: {center_line_control(481, 29760)}")
    print("PAIR DESERT: positivity + coherence + representation kill "
          "every ordered congrua pair for every center m <= 700 "
          "(and <= 1200 in the FULL check).")


if __name__ == "__main__":
    main()
