"""M12-A (ROADMAP W2): the H^{2,0} character atlas of the magic-square
surface — the motive fragments into 84 K3 pieces and 9 Horikawa pieces.

THE POINT.  X -> P^2 is the (Z/2)^8 cover branched on the nine entry
lines l_(a,b): c + a u + b v = 0, (a,b) in GRID = {-1,0,1}^2 (the same
descent setup as compute/descent_differentials.py; characters <-> EVEN
subsets S of the nine lines).  Standard abelian-cover Hodge theory
(Pardini; equivalently the double-cover formula through the quotient
Y_S = X / ker(chi_S), which is the double cover of P^2 branched on the
sub-arrangement S) gives the character eigenspace of the canonical
bundle on the SMOOTH MODEL:

    H^{2,0}(Xtilde)_chi_S  =  H^0(P^2, O(|S|/2 - 3) )        (*)

PROVIDED every singular point of the sub-arrangement S is negligible
(ADE) for the double cover — true here because the maximum number of
concurrent entry lines is 3 (the 8 grid-line triples: 3 rows, 3 columns,
2 diagonals; an ordinary node of the branch gives A_1, an ordinary
triple point gives D_4, both canonical, neither imposing adjoint
conditions).  Hence

    h^{2,0}(chi_S) = C(|S|/2 - 1, 2) = 0, 0, 0, 1, 3
                     for |S| = 0, 2, 4, 6, 8,

and the atlas total is  C(9,6)*1 + C(9,8)*3 = 84 + 27 = 111, which
must equal (and does equal) h^{2,0}(Xtilde) = chi(O) - 1 = 112 - 1
with q = 0 — the independently pinned A7/A8 invariants.  This is a
genuine cross-check of (*): the naive formula summed over all 256
characters reproduces the Noether-formula value exactly, confirming
en passant that no sub-arrangement has a point of multiplicity >= 4.

THE ATLAS.  The transcendental Hodge structure of X therefore lives in
exactly 93 characters:

  * 84 characters with |S| = 6 — each quotient Y_S is (the canonical
    resolution of) a DOUBLE SEXTIC: a K3 surface with d2(S) A_1 and
    t3(S) D_4 singularities, d2 + 3 t3 = 15.  Its Neron-Severi rank
    satisfies the PROVEN lower bound rho >= 1 + d2 + 4 t3 = 16 + t3
    (hyperplane + exceptional ADE lattice), so the transcendental rank
    is at most 6 - t3.  t3(S) = #{grid lines disjoint from the omitted
    3-point set}; the census below gives the distribution of t3 over
    the 84 (and by D_4-orbit).
  * 9 characters with |S| = 8 (omit one line) — Y_S is a DOUBLE OCTIC:
    minimal general type with K^2 = 2, chi(O) = 4, h^{2,0} = 3 — ON
    the Noether line K^2 = 2 chi - 6: a Horikawa surface (a completely
    classified, well-understood class).  t3(S) = 8 - #(grid lines
    through the omitted point) = 4 (center), 5 (corner), 6 (edge).

CONSEQUENCE FOR W2/W3 (the roadmap): the transcendental motive of X
embeds into the sum of 84 K3 motives (transcendental rank <= 6 - t3
each) and 9 Horikawa motives; the Picard/Brauer/L-function programme
can proceed piece by piece on these classical objects.

Run:  python3 -m compute.h20_atlas
"""

from itertools import combinations
from math import comb

GRID = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]

# the eight grid lines (rows, columns, diagonals) as point sets
GRID_LINES = (
    [frozenset((a, b) for b in (-1, 0, 1)) for a in (-1, 0, 1)] +
    [frozenset((a, b) for a in (-1, 0, 1)) for b in (-1, 0, 1)] +
    [frozenset((t, t) for t in (-1, 0, 1)),
     frozenset((t, -t) for t in (-1, 0, 1))])


def concurrency_census(S):
    """(d2, t3, max_mult) of the sub-arrangement of entry lines indexed
    by the point set S: t3 = full grid lines inside S (each an ordinary
    triple point of the line arrangement), d2 = remaining nodes; the
    maximum multiplicity of any arrangement point is 3 iff t3 counts
    every concurrency (proven by max-3-collinear in a 3x3 grid, and
    re-verified here by direct pairwise-intersection clustering)."""
    S = frozenset(S)
    t3 = sum(1 for L in GRID_LINES if L <= S)
    # direct verification via intersection points in P^2(c:u:v):
    # l_(a,b) has coefficients (1, a, b); intersection of two lines by
    # cross product; cluster and count multiplicities exactly.
    pts = {}
    lines = sorted(S)
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a1, b1), (a2, b2) = lines[i], lines[j]
            # cross of (1,a1,b1),(1,a2,b2):
            p = (a1 * b2 - b1 * a2, b1 - b2, a2 - a1)
            g = 0
            for t in p:
                g = abs(t) if g == 0 else __import__("math").gcd(g, abs(t))
            p = tuple(t // g for t in p)
            if next(t for t in p if t) < 0:
                p = tuple(-t for t in p)
            pts.setdefault(p, set()).update((lines[i], lines[j]))
    mults = sorted((len(v) for v in pts.values()), reverse=True)
    max_mult = mults[0] if mults else 0
    n_t3 = sum(1 for v in pts.values() if len(v) == 3)
    n_d2 = sum(1 for v in pts.values() if len(v) == 2)
    assert n_t3 == t3, (S, n_t3, t3)
    assert all(len(v) <= 3 for v in pts.values()), S
    return n_d2, n_t3, max_mult


def h20(S):
    k = len(S) // 2
    return comb(k - 1, 2) if k >= 1 else 0


def quotient_type(S):
    n = len(S)
    if n <= 4:
        return "rational"
    if n == 6:
        return "K3"
    return "Horikawa (K^2=2, chi=4)"


def atlas():
    """Per-character rows and the census; verifies the 111 total and
    the arrangement facts."""
    rows = []
    total = 0
    for size in (0, 2, 4, 6, 8):
        for S in combinations(GRID, size):
            d2, t3, mm = concurrency_census(S)
            h = h20(S)
            total += h
            rows.append((frozenset(S), size, d2, t3, mm, h,
                         quotient_type(S)))
    assert total == 111, total
    return rows


def orbit_atlas():
    """The atlas by D4-orbit (the 8 grid symmetries), for the two
    contributing sizes."""
    from compute.descent_differentials import grid_symmetries
    syms = grid_symmetries()
    out = {6: [], 8: []}
    seen = set()
    for size in (6, 8):
        for S in combinations(GRID, size):
            key = frozenset(S)
            if key in seen:
                continue
            orbit = {frozenset(f(ab) for ab in key) for f in syms}
            seen |= orbit
            d2, t3, _ = concurrency_census(key)
            out[size].append((sorted(key), len(orbit), d2, t3))
    return out


def main():
    rows = atlas()
    by_size = {}
    for _, size, d2, t3, mm, h, typ in rows:
        by_size.setdefault(size, []).append((d2, t3, h))
    print("== M12-A: the H^{2,0} character atlas ==")
    for size in (0, 2, 4, 6, 8):
        entries = by_size.get(size, [])
        hsum = sum(h for _, _, h in entries)
        print(f"|S| = {size}: {len(entries)} characters, "
              f"sum h^{{2,0}} = {hsum}")
    print("TOTAL h^{2,0} = 111  == chi(O) - 1 = 112 - 1 (q = 0): OK")
    print()
    print("the 84 K3 characters (|S| = 6) by t3 (D4 count):")
    t3s = {}
    for _, size, d2, t3, _, _, _ in rows:
        if size == 6:
            t3s[t3] = t3s.get(t3, 0) + 1
    for t3 in sorted(t3s):
        print(f"  t3 = {t3}: {t3s[t3]} characters   "
              f"(rho(K3) >= {16 + t3}, transcendental rank <= {6 - t3})")
    print("the 9 Horikawa characters (|S| = 8) by omitted point:")
    for _, size, d2, t3, _, _, _ in rows:
        if size == 8:
            pass
    for name, t3 in (("center", 4), ("corner", 5), ("edge", 6)):
        n = sum(1 for _, s, _, t, _, _, _ in rows if s == 8 and t == t3)
        print(f"  omit {name}: {n} characters, t3 = {t3}, "
              f"d2 = {28 - 3 * t3}")
    print()
    orb = orbit_atlas()
    print(f"D4-orbits: |S|=6: {len(orb[6])} orbits; "
          f"|S|=8: {len(orb[8])} orbits")
    for size in (6, 8):
        for S, osize, d2, t3 in orb[size]:
            print(f"  |S|={size} orbit x{osize}: omit "
                  f"{sorted(set(GRID) - set(S))}  (d2, t3) = "
                  f"({d2}, {t3})")


if __name__ == "__main__":
    main()
