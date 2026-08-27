"""The discrete-sphere model (A9): dictionary and tension checks."""

from ..framework import check, require

DOC = "docs/attacks/A9-discrete-spheres.md"

# the Lucas layout: square position -> (a, b) label; the 8 MAGIC
# lines (rows, columns, diagonals of the square) are the eight
# ZERO-SUM triples of labels
LAYOUT = [[(-1, 0), (1, 1), (0, -1)],
          [(1, -1), (0, 0), (-1, 1)],
          [(0, 1), (-1, -1), (1, 0)]]
LINES = ([LAYOUT[i] for i in range(3)] +
         [[LAYOUT[i][j] for i in range(3)] for j in range(3)] +
         [[LAYOUT[i][i] for i in range(3)],
          [LAYOUT[i][2 - i] for i in range(3)]])


@check("a9.dictionary", DOC)
def _(ctx):
    """The exact dictionary: in the Lucas parametrization (entries
    c + a u + b v) every one of the 8 lines sums to 3c (symbolic), so
    with center entry m^2 all 8 lines are points of the single
    discrete sphere S(3 m^2); the trivial point (m, m, m) is always
    on it; the slice of points with a coordinate equal to m bijects
    EXACTLY with A3's congrua set D(m) via d = 2ef <-> (|e-f|, m,
    e+f) — verified for every m up to the bound; and 3 squares
    summing to 3 (mod 8) are all odd (exhaustive residues)."""
    require(len(LINES) == 8 and all(len(L) == 3 for L in LINES))
    require(len({ab for L in LINES for ab in L}) == 9)
    for L in LINES:
        # sum of entries (c + a u + b v) over the line = 3c + (sum a) u
        # + (sum b) v: the linear parts must cancel
        require(sum(a for (a, _) in L) == 0)
        require(sum(b for (_, b) in L) == 0)
    # the center label lies on 4 magic lines, the axis labels on 3,
    # the diagonal labels on 2
    from collections import Counter
    cnt = Counter(ab for L in LINES for ab in L)
    require(cnt[(0, 0)] == 4)
    require(all(cnt[ab] == 3 for ab in
                ((1, 0), (-1, 0), (0, 1), (0, -1))))
    require(all(cnt[ab] == 2 for ab in
                ((1, 1), (1, -1), (-1, 1), (-1, -1))))
    # the magic/oblique split of the 8 grid-collinear triples (the
    # triple points of A8): the {a=0}, {b=0} and two diagonal pencils
    # are zero-sum (magic lines); the outer {a = +-1}, {b = +-1}
    # pencils are not
    for pencil, magic in ((([(0, b) for b in (-1, 0, 1)]), True),
                          (([(a, 0) for a in (-1, 0, 1)]), True),
                          (([(t, t) for t in (-1, 0, 1)]), True),
                          (([(t, -t) for t in (-1, 0, 1)]), True),
                          (([(1, b) for b in (-1, 0, 1)]), False),
                          (([(-1, b) for b in (-1, 0, 1)]), False),
                          (([(a, 1) for a in (-1, 0, 1)]), False),
                          (([(a, -1) for a in (-1, 0, 1)]), False)):
        zs = (sum(a for (a, _) in pencil) == 0
              and sum(b for (_, b) in pencil) == 0)
        require(zs == magic)
    from compute.discrete_spheres import all_odd_residue_fact, survey
    require(all_odd_residue_fact())
    bound = 200 if ctx.profile == "FULL" else 80
    rows = survey(bound)  # asserts trivial point + slice bijection
    require(len(rows) == bound)
    ctx.note(f"8 lines on one sphere (symbolic); slice = D(m) exactly "
             f"for every m <= {bound}; all-odd parity fact")


@check("a9.tension", DOC)
def _(ctx):
    """Abundance without compatibility, pinned: by m <= 200 the
    sphere S(3 m^2) reaches 64 points (and grows like a class
    number), while the additive ladder on the slice — whose level
    L4 >= 1 is REQUIRED for a magic square of squares with that
    center — stays at L3 = L4 = 0 throughout (consistent with A3's
    far larger desert bounds)."""
    from compute.discrete_spheres import survey
    bound = 200 if ctx.profile == "FULL" else 80
    rows = survey(bound)
    require(max(r["L3"] for r in rows) == 0)
    require(max(r["L4"] for r in rows) == 0)
    big = max(r["sphere"] for r in rows)
    require(big >= (64 if ctx.profile == "FULL" else 24),
            f"sphere sizes changed: max {big}")
    ctx.note(f"max sphere size {big} vs L3 = L4 = 0 for all "
             f"m <= {bound}: abundance without compatibility")


@check("a9.class_numbers", DOC)
def _(ctx):
    """The Eisenstein anchor: the ring class number h(-3 m^2)
    (conductor-m order of Q(sqrt-3)) computed two independent ways —
    primitive reduced-form enumeration vs the conductor formula
    (m/3) prod_(p|m) (1 - chi_-3(p)/p) with h(-3) = 1 — agrees for
    every valid m in range; sample values pinned."""
    from compute.sphere_classes import h_disc, h_eisenstein
    bound = 60 if ctx.profile == "FULL" else 30
    for m in range(1, bound):
        D = -3 * m * m
        if D % 4 in (0, 1):
            require(h_disc(D) == h_eisenstein(m),
                    f"class-number mismatch at m = {m}")
    require(h_eisenstein(5) == 2 and h_eisenstein(13) == 4
            and h_eisenstein(25) == 10 and h_eisenstein(9) == 3)
    ctx.note(f"conductor formula == reduced-form count for m < "
             f"{bound}; h(-75) = 2, h(-507) = 4, h(-1875) = 10")


@check("a9.gauss_map", DOC)
def _(ctx):
    """The Gauss orthogonal-lattice map on the magic-square spheres:
    (i) the counting identity r3*(3 m^2) = 24 h(-3 m^2) (8 = 24/3 at
    m = 1, the extra units) — asserted inside analyze() for every
    sampled m: the sphere's size IS an Eisenstein ring class number;
    (ii) fibers are uniform (torsor behavior); (iii) SLICE
    CONCENTRATION: the primitive through-center points (the A3
    congrua slice) are nonempty iff every odd prime factor of m is
    == 1 (mod 4), and then number 48 * 2^(w-1) in at most 2^w
    classes (w = count of such prime factors) — exponentially
    class-confined while the ambient class number grows linearly.
    FAST: m in {1, 5, 13}; FULL adds {9, 17, 25, 29, 65}."""
    from compute.sphere_classes import analyze
    expect = {1: (1, [8], 8, 1), 5: (1, [48], 48, 1),
              13: (2, [48], 48, 2), 9: (3, [24], 0, 0),
              17: (3, [48], 48, 2), 25: (5, [48], 48, 2),
              29: (5, [48], 48, 2), 65: (6, [96], 96, 4)}
    sample = ((1, 5, 13, 9, 17, 25, 29, 65) if ctx.profile == "FULL"
              else (1, 5, 13))
    for m in sample:
        r = analyze(m)  # asserts r3* = 24 h internally
        hit, fib, spts, scls = expect[m]
        require(r["classes_hit"] == hit and r["fibers"] == fib,
                f"class profile moved at m = {m}: {r}")
        require((r["slice_points"], r["slice_classes"]) == (spts, scls),
                f"slice profile moved at m = {m}: {r}")
    ctx.note(f"{len(sample)} spheres: r3* = 24 h verified, fibers "
             "uniform, slice exponentially class-confined")
