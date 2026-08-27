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


@check("a9.gluing_law", DOC)
def _(ctx):
    """Lemma A9.1, the gluing-representation law: for every point
    v = (x, y, z) of S(3 m^2) the three cross-vectors (0, -z, y),
    (z, 0, -x), (-y, x, 0) lie in v-perp with norms EXACTLY the
    co-norms 3 m^2 - x^2 etc. — so the Gauss class of each magic
    line represents the co-norm of each of its three entries.
    Consequences verified on every primitive point of the sample
    spheres: the co-norm triple of an actual point is
    chi_p-coherent for every odd p | 3 m^2 (Theorem A9.3 necessity
    in action — may never fail), and (Lemma A9.4) all coordinates
    are odd, forcing the orthogonal lattice EVEN (the Gauss map
    lands in even-form classes)."""
    from compute.sphere_classes import primitive_points_full
    from compute.sphere_gluing import (even_lattice, gluing_identity,
                                       point_coherence)
    sample = (5, 13, 25, 65) if ctx.profile == "FULL" else (5, 13)
    tot = 0
    for m in sample:
        pts = primitive_points_full(3 * m * m)
        require(pts, f"no points at m = {m}")
        require(all(gluing_identity(v) for v in pts))
        require(all(point_coherence(v, m) for v in pts),
                f"coherence FAILED on an actual point, m = {m}")
        require(all(even_lattice(v) for v in pts),
                f"odd/even structure failed at m = {m}")
        tot += len(pts)
    ctx.note(f"cross-vector law + on-sphere coherence + even "
             f"lattices on {tot} points ({len(sample)} spheres)")


@check("a9.coherence", DOC)
def _(ctx):
    """Theorem A9.3's bite, pinned: chi_p-coherence of the eight
    co-norm triples (center lines (2m^2, 2m^2 +- X) for X in {U, V,
    U+V, U-V}; four outer lines) is NECESSARY for a congrua pair
    (U, V) to extend to a magic square of squares with center m^2
    (each line would be a sphere point, and A9.1 + genus invariance
    force its triple coherent). Kill table pinned: 10/12 ordered
    pairs die at m = 65 (survivors exactly the two imprimitive
    branches together), 6/12 at m = 145 (survivors exactly the
    pairs involving the 5-branch congruum 21000), 0 at the prime
    powers 25, 125 — the first obstruction beyond the classical
    24 | d layer. Window refinement at m = 13: the slice classes
    sit STRICTLY inside the classes representing 2 m^2."""
    from compute.sphere_gluing import pair_obstruction, window_refinement
    expect = {25: (2, 0), 65: (12, 10), 85: (12, 10), 125: (6, 0),
              130: (12, 10), 145: (12, 6)}
    sample = ((25, 65, 85, 125, 130, 145) if ctx.profile == "FULL"
              else (25, 65, 145))
    for m in sample:
        total, killed, alive = pair_obstruction(m)
        require((total, killed) == expect[m],
                f"kill table moved at m = {m}: {(total, killed)}")
    _, _, alive65 = pair_obstruction(65)
    require(set(alive65) == {(3000, 4056), (4056, 3000)},
            f"survivor structure moved at m = 65: {alive65}")
    _, _, alive145 = pair_obstruction(145)
    require(all(21000 in pr for pr in alive145) and len(alive145) == 6,
            f"survivor structure moved at m = 145: {alive145}")
    slc, rep, strict = window_refinement(13)
    require(strict and len(slc) == 2 and len(rep) == 5,
            f"window moved at m = 13: {len(slc)} vs {len(rep)}")
    ctx.note(f"kill table pinned on {len(sample)} centers; survivors "
             "characterized at 65/145; slice STRICTLY inside "
             "Rep(2m^2) at m = 13")


@check("a9.pair_desert", DOC)
def _(ctx):
    """The three-sieve pair desert: every ordered congrua pair
    (U, V) at every center m^2 in range is killed by one of three
    PROVEN-NECESSARY conditions — (1) positivity U + V <= m^2 (the
    smallest edge entry m^2 - U - V must be a square, so >= 0);
    (2) chi_p-coherence of the eight co-norm triples (Theorem A9.3);
    (3) REPRESENTATION: each triple must be represented by a single
    even class at an admissible discriminant -4(3m^2)/g^2 (Lemmas
    A9.1 + A9.4; strictly stronger than characters — same genus is
    not same class). Pinned: FULL m <= 1200 — 153 centers, 1782
    pairs, 1608 positivity / 152 coherence / 22 representation
    (passers exactly at m = 425, 481, 725, 845, 850, 901, 925, 962,
    1025), 0 remain; the U+V diagonal line is unrepresentable in
    every passing pair, and lines 0/1 (the ACTUAL U- and V-center
    lines) always have candidates — the machinery never kills a
    line that exists. Round-trip control: the actual center-line
    points' (content, class) lie in their own candidate sets."""
    from compute.sphere_gluing import (center_line_control,
                                       joint_survey, rep_verdict)
    if ctx.profile == "FULL":
        bound, expect = 1200, (153, 1782, 1608, 152, 22)
        centers_expect = {425, 481, 725, 845, 850, 901, 925, 962,
                          1025}
    else:
        bound, expect = 500, (50, 466, 434, 28, 4)
        centers_expect = {425, 481}
    nc, tot, npos, ncoh, passers = joint_survey(bound)
    npass = sum(len(v) for v in passers.values())
    require((nc, tot, npos, ncoh, npass) == expect,
            f"sieve totals moved: {(nc, tot, npos, ncoh, npass)}")
    require(set(passers) == centers_expect,
            f"passer centers moved: {sorted(passers)}")
    for m, prs in passers.items():
        for (U, V) in prs:
            counts, empty = rep_verdict(m, U, V)
            require(empty, f"pair SURVIVES representation: "
                    f"m={m} {(U, V)} — investigate immediately")
            require(2 in empty,
                    f"U+V diagonal representable at m={m} {(U, V)}")
            require(counts[0] > 0 and counts[1] > 0,
                    f"control broken (actual line killed) at m={m}")
    require(center_line_control(425, 54600))
    require(center_line_control(481, 29760))
    if ctx.profile == "FULL":
        # even centers: the point content's 2-part is forced to
        # v_2(m) (the sphere reduces to the odd sphere), and the
        # actual center lines must still land in their candidate
        # sets — guards the content enumeration at even m
        require(center_line_control(850, 218400))
        require(center_line_control(962, 119040))
    ctx.note(f"m <= {bound}: {tot} pairs -> {npos} positivity + "
             f"{ncoh} coherence + {npass} representation = 0 left; "
             "controls pass")


@check("a9.composition", DOC)
def _(ctx):
    """Gauss composition, implemented exactly and verified as a
    group on the Eisenstein-family class groups: identity, inverses,
    closure, and the full element-order multiset pinned
    (Cl(-507) = Z/4; Cl(-3.65^2) = Z/12 x Z/2 by orders). Gauss's
    PRINCIPAL GENUS THEOREM — the squares are exactly the
    trivial-character genus — is machine-checked, so 'invisible to
    every genus character' rigorously means 'inside a coset of
    Cl^2'. The occurring character vectors form an index-2 subgroup
    whose derived annihilator is supported at 3 alone: every class
    value's 3-free part is == 1 (mod 3) (the norm-residue law of
    the family)."""
    from compute.sphere_composition import (genus_relation,
                                            group_check,
                                            principal_genus_check)
    h, orders = group_check(-507)
    require((h, orders) == (4, [1, 2, 4, 4]),
            f"Cl(-507) moved: {(h, orders)}")
    pg, ngen, sizes = principal_genus_check(-507)
    require(pg and (ngen, sizes) == (2, [2, 2]))
    require(genus_relation(-507)[1] == 1)  # annihilator = {chi_3}
    if ctx.profile == "FULL":
        h, orders = group_check(-12675)
        require(h == 24 and orders ==
                [1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6,
                 12, 12, 12, 12, 12, 12, 12, 12],
                f"Cl(-12675) moved: {(h, orders)}")
        pg, ngen, sizes = principal_genus_check(-12675)
        require(pg and (ngen, sizes) == (4, [6, 6, 6, 6]))
        require(genus_relation(-12675)[1] == 1)
    ctx.note("composition group laws + principal genus theorem + "
             "the chi_3 norm-residue relation verified")


@check("a9.local_criterion", DOC)
def _(ctx):
    """The local representability criterion (inert parity, ramified
    valuation/character laws, the chi_3 norm-residue relation)
    validated EXHAUSTIVELY against brute-force class enumeration:
    criterion(w) == (some class represents w) for every odd w up to
    the bound, at the pinned sample discriminants."""
    from compute.sphere_composition import validate_local_criterion
    if ctx.profile == "FULL":
        n1 = validate_local_criterion(-12675, 6000)
        n2 = validate_local_criterion(-3 * 145 * 145, 6000)
        n3 = validate_local_criterion(-3 * 425 * 425, 6000)
        ctx.note(f"criterion == brute force on {n1 + n2 + n3} odd "
                 "values across discs -12675, -63075, -541875")
    else:
        n1 = validate_local_criterion(-12675, 3000)
        ctx.note(f"criterion == brute force on {n1} odd values "
                 "(disc -12675)")


@check("a9.kill_anatomy", DOC)
def _(ctx):
    """The anatomy of the representation kills behind the pair
    desert, pinned: every killed line is L0 (a single co-norm value
    PROVABLY locally impossible — certified against the validated
    local criterion at every stratum), GENUS, or GLOBAL (a genus
    admits all three values but no class does — beyond every
    character, inside a coset of Cl^2). FULL: all 11 passers — 57
    killed lines = 21 L0 + 0 GENUS + 36 GLOBAL, all 24 L0 values
    locally certified, all 36 GLOBAL lines locally fine; the even
    centers 850/962 reproduce the anatomy of their odd cores
    425/481 at stratum g = 2; at m = 725 BOTH pairs die through
    GLOBAL kills alone — that part of the desert is invisible to
    every congruence argument. FAST: the 425/481 subset."""
    from compute.sphere_composition import PASSERS_1200, anatomy
    if ctx.profile == "FULL":
        rows, totals, cert = anatomy()
        require(totals == {"L0": 21, "GENUS": 0, "GLOBAL": 36},
                f"anatomy moved: {totals}")
        require(cert == (24, 24, 36, 36), f"certification: {cert}")
        by = {(m, U, V): row for m, U, V, row in rows}
        require(all(v == "GLOBAL" for _, v, _ in
                    by[(725, 122400, 282576)] +
                    by[(725, 171600, 282576)]),
                "m = 725 pure-global signature moved")
        require([(i, v) for i, v, _ in by[(850, 218400, 388416)]] ==
                [(i, v) for i, v, _ in by[(425, 54600, 97104)]])
        require([(i, v) for i, v, _ in by[(962, 119040, 567840)]] ==
                [(i, v) for i, v, _ in by[(481, 29760, 141960)]])
        ctx.note("57 kills = 21 L0 (all locally certified) + 0 GENUS "
                 "+ 36 GLOBAL (all locally fine); 725 pure-global; "
                 "850/962 double 425/481")
    else:
        rows, totals, cert = anatomy(PASSERS_1200[:2])
        require(totals == {"L0": 5, "GENUS": 0, "GLOBAL": 5},
                f"anatomy moved: {totals}")
        require(cert[0] == cert[1] and cert[2] == cert[3])
        ctx.note("425/481 subset: 5 L0 + 5 GLOBAL, certifications "
                 "pass")


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
