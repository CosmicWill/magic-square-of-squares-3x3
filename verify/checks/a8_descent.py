"""Descent of symmetric differentials to the Lucas plane (A8, M11-A).

Verifies the structural facts, the engine's controls, and the two
headline computations: q = 0 (m = 1) and h^0(X - nodes, S^2 Omega^1)
= 0 (m = 2, all 256 characters).
"""

from fractions import Fraction as F
from itertools import combinations

from ..framework import Skip, check, require
from compute.descent_differentials import (GRID, character_orbits,
                                           eigenspace_dim,
                                           grid_symmetries, survey,
                                           validate_solution)

DOC = "docs/attacks/A8-descent-differentials.md"


@check("a8.structure", DOC)
def _(ctx):
    """The arrangement's structure: 8 triple points = the 8 grid
    lines-of-three; column/row pencil base points lie on v=0 / u=0;
    both '6 tangent lines of a smooth conic + 3-line pencil' splits."""
    # triples of concurrent lines <=> collinear grid triples
    coll = []
    for trip in combinations(GRID, 3):
        (a1, b1), (a2, b2), (a3, b3) = trip
        det = (a2 - a1) * (b3 - b1) - (a3 - a1) * (b2 - b1)
        if det == 0:
            coll.append(trip)
    require(len(coll) == 8, f"{len(coll)} grid lines-of-three")

    def common_point(lines):
        (l1, l2) = lines[:2]
        p = (l1[1] * l2[2] - l1[2] * l2[1],
             l1[2] * l2[0] - l1[0] * l2[2],
             l1[0] * l2[1] - l1[1] * l2[0])
        for L in lines:
            require(sum(x * y for x, y in zip(L, p)) == 0)
        return p

    for t in (-1, 0, 1):
        A = common_point([(1, a, b) for (a, b) in GRID if a == t])
        require(A[2] == 0, "column pencil base point off v=0")
        B = common_point([(1, a, b) for (a, b) in GRID if b == t])
        require(B[1] == 0, "row pencil base point off u=0")
    # conic splits (dual conics through six grid points)
    for sgn, pencil in ((1, [(0, 0), (1, -1), (-1, 1)]),
                        (-1, [(0, 0), (1, 1), (-1, -1)])):
        pts = [(1, a, b) for (a, b) in GRID if (a, b) not in pencil]
        require(len(pts) == 6)
        for (X, Y, Z) in pts:
            require(X * X - Y * Y - Z * Z + sgn * Y * Z == 0,
                    f"conic split fails at {(X, Y, Z)}")
        det = F(1) * (F(-1) * F(-1) - F(sgn, 2) * F(sgn, 2))
        require(det != 0, "dual conic not smooth")
    ctx.note("8 grid triples; pencils based on v=0/u=0; two conic splits")


@check("a8.quadric_control", DOC)
def _(ctx):
    """Two-line sub-cover = P^1 x P^1: no symmetric differentials in any
    character at m = 1, 2 (the engine's exactness control)."""
    L2 = [(1, 0), (-1, 0)]
    for m in (1, 2):
        require(eigenspace_dim((), m, lines=L2) == 0)
        require(eigenspace_dim(tuple(L2), m, lines=L2) == 0)
    ctx.note("quadric: all characters 0 at m=1,2")


@check("a8.infinity_trap", DOC)
def _(ctx):
    """The near-trap eta = dl_1 dl_2 (pullback 4 dx_1 dx_2, affinely
    regular) is rejected for exactly the right reason: an order-4 pole
    over u = 0, detected by the chart-2 side of the independent
    validator."""
    L2 = [(1, 0), (0, 1)]
    S = tuple(L2)
    dim, basis, unknowns, dN = eigenspace_dim(S, 2, return_basis=True,
                                              lines=L2)
    require(dim == 0, "quadric character unexpectedly nonzero")
    b1, b2 = 0, 1          # slopes of the two lines
    vec = [F(0)] * len(unknowns)
    coeffs = {2: F(1), 1: F(b1 + b2), 0: F(b1 * b2)}
    for t, (i, mono) in enumerate(unknowns):
        if mono == (0, 0) and coeffs.get(i, 0) != 0:
            vec[t] = coeffs[i]
    ok, reason = validate_solution(S, 2, vec, unknowns, dN, lines=L2)
    require(not ok, "validator accepted a form with a pole at infinity")
    require("u=0" in reason, f"wrong rejection reason: {reason}")
    ctx.note("dl1*dl2 rejected: pole over u=0 (validator chart-2 path)")


@check("a8.q_zero", DOC)
def _(ctx):
    """Theorem A8.2: q(X~) = h^0(X - nodes, Omega^1) = 0 -- every one of
    the 256 characters vanishes at m = 1 (saturation-checked).  This
    matches the classical Zariski/Esnault-Viehweg prediction (no even
    pencil sub-arrangements) and pins b_2 = 766, h^{1,1} = 544."""
    total, rows = survey(1, verbose=False)
    require(sum(o for _, o, _ in rows) == 256, "character count")
    require(total == 0, f"q = {total} != 0")
    ctx.note("q = 0: b_1=0, b_2 = 766, h^{1,1} = 544")


@check("a8.m2_survey", DOC)
def _(ctx):
    """Theorem A8.3: h^0(X - nodes, S^2 Omega^1) = 0 -- all 256
    characters vanish at m = 2.  FULL: all 51 orbits with saturation;
    FAST/CI: a fixed sample of orbits (zero-dimensionality pinned)."""
    if ctx.profile == "FULL":
        total, rows = survey(2, verbose=False)
        require(sum(o for _, o, _ in rows) == 256, "character count")
        require(total == 0, f"h^0(S^2) = {total} != 0")
        ctx.note("all 51 orbits: h^0(X-nodes, S^2 Omega^1) = 0 "
                 "(vs cuboid's 13)")
    else:
        sample = [(), ((0, 0), (1, 1)), ((1, 0), (-1, 0)),
                  ((1, 0), (-1, 0), (0, 1), (0, -1)),
                  ((0, 0), (1, 0), (0, 1), (1, 1)),
                  tuple(ab for ab in GRID if ab != (0, 0))]
        for S in sample:
            require(len(S) % 2 == 0)
            require(eigenspace_dim(S, 2) == 0, f"V_S != 0 at {S}")
        ctx.note(f"sampled {len(sample)} characters: all zero at m=2")


@check("a8.orbit_equivariance", DOC)
def _(ctx):
    """The solver is equivariant: dims agree across an entire symmetry
    orbit of characters (catches any line-indexing asymmetry)."""
    S0 = frozenset({(0, 0), (1, 1)})
    orbit = sorted({frozenset(f(ab) for ab in S0)
                    for f in grid_symmetries()}, key=str)
    members = orbit if ctx.profile == "FULL" else orbit[:3]
    dims = {eigenspace_dim(tuple(sorted(Sm)), 2) for Sm in members}
    require(len(dims) == 1, f"orbit dims differ: {dims}")
    require(len(orbit) > 1)
    ctx.note(f"orbit of size {len(orbit)}: constant dim {dims.pop()}")


@check("a8.character_bookkeeping", DOC)
def _(ctx):
    """51 orbits cover exactly the 256 even characters."""
    orbs = character_orbits()
    require(len(orbs) == 51, f"{len(orbs)} orbits")
    require(sum(o for _, o in orbs) == 256)
    require(all(len(k) % 2 == 0 for k, _ in orbs))
    ctx.note("51 symmetry orbits covering all 256 even characters")


@check("a8.cuboid_control", DOC)
def _(ctx):
    """THE POSITIVE CONTROL: the same descent methodology, run on the
    perfect-cuboid surface (a (Z/2)^4 cover of P^2 branched on four
    Q-irreducible conics), reproduces BTVA's Magma-computed
    h^0(X_pc, hat-S^2 Omega^1) = 13 -- including the full 16-character
    fingerprint read off their Table 1, and element-level membership of
    their descended generators omega_4, omega_7, x_2 omega_7,
    x_3 omega_7."""
    from compute.descent_cuboid import (EXPECTED_M2, _in_space,
                                        cuboid_eigenspace_dim, spectrum,
                                        table1_membership)
    if ctx.profile == "FULL":
        spec = spectrum(2, saturate=True)
        require(sum(spec.values()) == 13, f"total {sum(spec.values())}")
        want = {T: EXPECTED_M2.get(T, 0) for T in spec}
        require(spec == want, "character fingerprint mismatch")
        # extra control: q(cuboid resolution) = 0
        require(all(cuboid_eigenspace_dim(T, 1) == 0 for T in spec),
                "cuboid q != 0")
        note = "all 16 characters"
    else:
        for T, d in EXPECTED_M2.items():
            require(cuboid_eigenspace_dim(tuple(sorted(T)), 2) == d,
                    f"V_{sorted(T)} != {d}")
        for T in ((1,), (1, 4), (2, 3, 4)):
            require(cuboid_eigenspace_dim(T, 2) == 0, f"V_{T} != 0")
        note = "7 nonzero + 3 zero characters"
    for name, T, nums in table1_membership():
        ok, dim = _in_space(T, 2, nums)
        require(ok, f"{name} not in computed V_{sorted(T)}")
    ctx.note(f"cuboid: h^0 = 13 EXACTLY as BTVA ({note}); "
             "Table-1 memberships verified")


@check("a8.modp_soundness", DOC)
def _(ctx):
    """The mod-p fast path (a zero nullity mod p proves the exact
    dimension is zero, since rank only drops under reduction) agrees
    with the exact engine on discriminating cases: the cuboid's full
    16-character fingerprint (nonzero dims included) and X's m = 2
    samples."""
    from compute.descent_cuboid import (EXPECTED_M2,
                                        cuboid_eigenspace_dim)
    subsets = ([tuple(sorted(T)) for T in EXPECTED_M2]
               + [(1,), (2, 4), (1, 2, 4)])
    for T in subsets:
        want = EXPECTED_M2.get(frozenset(T), 0)
        require(cuboid_eigenspace_dim(T, 2, modp=True) == want,
                f"cuboid mod-p mismatch at {T}")
    for S in ((), ((0, 0), (1, 1))):
        require(eigenspace_dim(S, 2, modp=True) == eigenspace_dim(S, 2))
    ctx.note("mod-p nullities == exact dims on cuboid fingerprint "
             "(incl. nonzero) and X samples")


@check("a8.m3_survey", DOC)
def _(ctx):
    """h^0(X - nodes, S^3 Omega^1) = 0: every character has mod-p
    nullity zero (a proof of exact vanishing at the stabilized degree
    bound).  First nonzero symmetric degree now bracketed in
    {4, ..., 7}.  FULL: all 51 orbits, saturated; FAST: samples."""
    from compute.descent_differentials import survey_modp
    if ctx.profile == "FULL":
        zero, cands = survey_modp(3, verbose=False)
        require(zero, f"unexpected m=3 candidates: {cands}")
        ctx.note("all 51 orbits: h^0(S^3) = 0; first nonzero m in {4..7}")
    else:
        for S in ((), ((0, 0), (1, 1)), ((1, 0), (-1, 0)),
                  ((1, 0), (-1, 0), (0, 1), (0, -1))):
            require(eigenspace_dim(S, 3, modp=True) == 0)
        ctx.note("sampled characters: zero at m=3")


@check("a8.m4_generators", DOC)
def _(ctx):
    """Theorem A8.5 (first sections): the six stored generators of
    V_empty(m = 4) -- the first explicit symmetric differentials on the
    magic-square surface -- satisfy the exact rational condition system
    (dim >= 6), are linearly independent, and the mod-p nullity is 6
    (dim <= 6): dim V_empty(4) = 6 exactly.  m <= 3 vanishes
    identically (a8.m2_survey, a8.m3_survey), so m = 4 is the FIRST
    nonzero symmetric degree on X - nodes."""
    from compute.data_m4_generators import DN, GENERATORS
    from compute.descent_differentials import (_assemble_rows,
                                               _row_apply,
                                               nullspace_dim_modp)
    require(len(GENERATORS) == 6)
    rows, unknowns, dN = _assemble_rows((), 4, DN, None)
    idx = {u: t for t, u in enumerate(unknowns)}
    vecs = []
    for g in GENERATORS:
        vec = [F(0)] * len(unknowns)
        for i, part in g.items():
            for mono, val in part.items():
                vec[idx[(int(i), (int(mono[0]), int(mono[1])))]] = F(val)
        vecs.append(vec)
    todo = vecs if ctx.profile == "FULL" else vecs[:2]
    for gi, vec in enumerate(todo):
        for row in rows:
            require(_row_apply(row, vec) == 0,
                    f"generator {gi} fails an exact condition row")
    # independence over F_p (implies independence over Q)
    p = 1_000_003_919
    mat = [[x.numerator % p * pow(x.denominator, p - 2, p) % p
            for x in vec] for vec in vecs]
    basis = []
    for row in mat:
        row = row[:]
        for b in basis:
            piv = next(j for j, x in enumerate(b) if x)
            if row[piv]:
                fac = row[piv] * pow(b[piv], p - 2, p) % p
                row = [(x - fac * y) % p for x, y in zip(row, b)]
        if any(row):
            basis.append(row)
    require(len(basis) == 6, "generators not independent")
    if ctx.profile == "FULL":
        require(nullspace_dim_modp(rows, len(unknowns)) == 6,
                "mod-p upper bound changed")
        note = "all 6 verified exactly; dim == 6 certified"
    else:
        note = "2 of 6 verified exactly (FULL does all + upper bound)"
    ctx.note(f"first sections at m = 4: {note}")


@check("a8.m4_spectrum", DOC)
def _(ctx):
    """The complete m = 4 spectrum: the stored 51-orbit survey record
    says only the trivial character is nonzero (total 6); its
    bookkeeping is validated and a sample of nontrivial orbits is
    recomputed mod p (each zero being a proof of exact vanishing)."""
    import json
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "..",
                        "compute", "data_m4_spectrum.json")
    data = json.load(open(path))
    require(len(data) == 51 and sum(r["orbit"] for r in data) == 256)
    nz = [r for r in data if r["d"]]
    require(len(nz) == 1 and nz[0]["S"] == [] and nz[0]["d"] == 6,
            f"spectrum record changed: {nz}")
    require(sum(r["orbit"] * r["d"] for r in data) == 6)
    sample = [((0, 0), (1, 1)), ((1, 0), (-1, 0)),
              ((1, 0), (-1, 0), (0, 1), (0, -1))]
    if ctx.profile == "FULL":
        sample += [((0, 0), (1, 0), (0, 1), (1, 1)),
                   tuple(ab for ab in GRID if ab != (0, 0)),
                   ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)),
                   ((1, 1), (1, -1), (-1, 1), (-1, -1))]
    for S in sample:
        require(eigenspace_dim(S, 4, modp=True) == 0,
                f"nontrivial character {S} nonzero at m=4?!")
    ctx.note(f"h^0(S^4) = 6, all invariant; {len(sample)} nontrivial "
             "orbits re-proved zero")


@check("a8.chi_hat_bracket", DOC)
def _(ctx):
    """chi(X, hat-S^m Omega^1) = chi(Y, S^m) + 256 chi_loc(m) is
    negative for m = 2..6 (near-miss -560 at m = 6) and turns positive
    at m = 7 with value 384; with the classical h^2-vanishing (m >= 3)
    this guarantees sections at m = 7, so the first nonzero symmetric
    degree on X - nodes lies in {3, ..., 7} (m = 2 excluded by
    a8.m2_survey)."""
    from compute.btva_bounds import XMS, chi_hat
    K2, chi, ell = XMS["K2"], XMS["chi"], XMS["ell"]
    vals = {m: chi_hat(K2, chi, ell, m) for m in range(2, 12)}
    require(vals[2] == -624 and vals[6] == -560, "chi-hat changed")
    require(all(vals[m] < 0 for m in range(2, 7)))
    require(vals[7] == 384 and all(vals[m] > 0 for m in range(7, 12)))
    ctx.note("chi-hat < 0 for m <= 6, = +384 at m = 7: "
             "first nonzero m is in {3..7}")


@check("a8.z_properness", DOC)
def _(ctx):
    """The common-direction locus Z of the six m = 4 differentials
    (the plane points where the six binary direction-quartics share a
    projective root) is a PROPER closed subset of the Lucas plane:
    exact computation shows the quartics are coprime at rational base
    points, so dim Z <= 1 and a common integral curve of the 6-system
    must be one of the finitely many curve components of Z (Lemma
    A8.6)."""
    from compute.special_locus import common_direction_gcd
    for pt in ((F(2), F(5, 7)), (F(-4), F(11, 5))):
        g = common_direction_gcd(pt)
        require(len(g) == 1 and g[0] == 1,
                f"common direction at {pt}: gcd {g}")
    ctx.note("six quartics coprime at 2 rational points: Z proper")


@check("a8.z_catalogue", DOC)
def _(ctx):
    """Exact special-line tests against the 6-system: all nine entry
    lines lie in Z (their own direction is a common root of the six
    quartics along them — the consistency floor for the Z-scan), while
    the pencil carriers v = 0 and u = 0 and the six distinctness lines
    are NOT integral curves.  u = 0, invisible in the (c, v)-chart, is
    tested by the chart-2 slice formula (with the regularity degree
    bound deg N_k <= 14 asserted); its verdict must agree with v = 0
    by the transpose symmetry (c:u:v) -> (c:v:u), which preserves the
    invariant 6-space and swaps the two lines."""
    from compute.special_locus import catalogue_tests
    t = catalogue_tests()
    entry = {k: v for k, v in t.items() if k.startswith("entry")}
    require(len(entry) == 9 and all(entry.values()),
            f"entry lines not all in Z: {entry}")
    others = {k: v for k, v in t.items() if not k.startswith("entry")}
    require(len(others) == 8 and not any(others.values()),
            f"a non-branch special line became integral: {others}")
    require(t["u=0 integral"] == t["v=0 integral"],
            "transpose symmetry violated")
    ctx.note("9 entry lines in Z; u=0, v=0 and the 6 distinctness "
             "lines all non-integral (u=0 by the chart-2 slice)")


@check("a8.z_scan", DOC)
def _(ctx):
    """Certificate A8.7 (mod p): along exact generic rational lines
    (nine pairwise-distinct entry-line crossings each, certified
    exactly), the gcd of all 15 pairwise resultants of the six
    direction-quartics has degree exactly 72 = 9 x 8 — the nine
    entry-line crossings with multiplicity 8 each and NOTHING else.
    So mod p the curve part of Z is exactly the nine entry lines, and
    with Lemma A8.6 every complete genus-0 curve on X passes through a
    node (Theorem A8.8).  FAST: first test line at both primes; FULL:
    all 3 lines x 2 primes."""
    from compute.special_locus import (SCAN_PRIMES, TEST_LINES,
                                       z_certificate)
    lines = TEST_LINES if ctx.profile == "FULL" else TEST_LINES[:1]
    cert = z_certificate(lines=lines, primes=SCAN_PRIMES)
    require(cert["ok"], f"Z-scan structure changed: {cert}")
    degs = {r["pair_degs"] for r in cert["runs"].values()}
    require(degs == {(92, 96)}, f"pair resultant degrees moved: {degs}")
    ctx.note(f"{len(cert['runs'])} line/prime scans: gcd degree 72 = "
             "9 crossings x mult 8, zero extra roots")


@check("a8.z_exact", DOC)
def _(ctx):
    """Theorem A8.7-exact (A8-T3 closed): the EXACT bivariate
    resultants R_12, R_34 in Z[c, v] — proven exact by CRT over 30-bit
    primes whose product exceeds twice the rigorous l1 determinant
    bound, and independently spot-verified against exact integer
    Sylvester determinants — factor as prod l_(a,b)^e x cofactor with
    every entry line appearing to exponent >= 8 in both, gcd exponents
    exactly 8, and the two peeled cofactors certified COPRIME over Q
    (sound direction: nonzero Res_v evaluation mod p with alive
    v-leading coefficients + exact v-content gcd).  Hence
    gcd(R_12, R_34) = prod l^8 up to constant, the curve part of Z is
    contained in the nine entry lines over Q-bar, and Theorem A8.8
    (node passage) is UNCONDITIONAL.  Both profiles recompute the
    whole certificate from the stored generators (~5 s) and compare
    against the committed data file."""
    from compute.z_exact import compute_certificate, load
    cert, Rs = compute_certificate(verbose=False)
    require(cert["ok"], "certificate structure broken")
    require(all(v == 8 for v in cert["gcd_exponents"].values()),
            f"gcd exponents changed: {cert['gcd_exponents']}")
    for pr in cert["pairs"]:
        require(all(e >= 8 for e in
                    (int(x) for x in pr["line_exponents"].values())),
                f"a line exponent dropped below 8: {pr}")
    require(cert["coprime"]["resv_mod"] != 0)
    stored_cert, stored_Rs = load()
    require([R for (R, _, _) in Rs] == stored_Rs,
            "stored resultants differ from the recomputation")
    require(stored_cert["gcd_exponents"] == cert["gcd_exponents"])
    degs = tuple(pr["total_deg"] for pr in cert["pairs"])
    require(degs == (96, 92), f"resultant degrees moved: {degs}")
    ctx.note("exact R_12 (deg 96), R_34 (deg 92); gcd = prod l^8 x "
             "const, cofactors coprime over Q: Z's curve part = the "
             "nine entry lines over Q-bar — Theorem A8.8 unconditional")


@check("a8.node_tau", DOC)
def _(ctx):
    """Lemma A8.9 + the tau table (Theorem A8.10): every triple point
    is an AP-pencil with local cone z3^2 = (z1^2+z2^2)/2, and the
    exact local pullback through q1 = s^2+2st-t^2, q2 = -s^2+2st+t^2
    gives, at EVERY visible triple point, the filtration
    dim V_(tau>=0,2,4,6) = 6,4,4,0: a 4-dimensional subspace of the
    six m = 4 differentials extends across the 32 exceptional
    (-2)-curves there, the rest have pole order exactly 2 (tau jumps
    0 -> 4, no tau = 2).  tau_of asserts parity (even coefficients:
    the invariance) and regularity (tau >= 0) internally.  FAST: two
    representative points; FULL: all five visible."""
    from compute.node_extension import VISIBLE, filtration, tau_of
    from compute.special_locus import numerator_forms
    forms = numerator_forms()
    TABLE = {"A0": [0, 4, 4, 4, 0, 4], "A+": [0, 0, 0, 4, 0, 4],
             "A-": [0, 0, 0, 4, 0, 4], "D+": [0, 0, 0, 4, 4, 0],
             "D-": [0, 0, 0, 4, 4, 0]}
    tags = list(VISIBLE) if ctx.profile == "FULL" else ["A0", "D+"]
    for tag in tags:
        taus = [tau_of(Ns, tag) for Ns in forms]
        require(taus == TABLE[tag], f"tau table moved at {tag}: {taus}")
        dims, _ = filtration(tag, forms)
        require(dims == {0: 6, 2: 4, 4: 4, 6: 0, 8: 0},
                f"filtration moved at {tag}: {dims}")
    ctx.note(f"{len(tags)} triple points: filtration 6/4/4/0, tau in "
             "{0, 4}, pole orders in {2, 0}")


@check("a8.node_extension", DOC)
def _(ctx):
    """Theorems A8.10-A8.13: the D4 grid representation on the
    6-space (three involutions pinned; sigma*r of order 4; eta_4
    spans the invariant line), the extension-subspace lattice
    (pairwise dims 22 x 2 + 6 x 3 with the six dim-3 pairs pinned;
    A-/B-triples of dim 2), and the resolution section: the
    intersection of ALL EIGHT extension subspaces is exactly
    <eta_4>, re-certified DIRECTLY (tau = 4 at the five visible
    points for omega* and for sigma* omega*, covering the B-points),
    so h^0(Ytilde, S^4 Omega^1) = 1 and every rational curve on the
    resolution is an eta*-integral curve.  Consistency against the
    classical AP families: u = 0 and v = 0 are integral for omega*
    (asserted inside wstar_vector) AND for the full 2-dimensional
    B-triple resp. A-triple spaces — exactly what the pattern
    dichotomy demands for the genus-0 components over those lines."""
    from compute.node_extension import (ALL_TAGS, extension_spaces,
                                        intersect, is_identity,
                                        mat_mul, rep_matrices,
                                        wstar_vector)
    from compute.special_locus import (is_zero, numerator_forms,
                                       restrict_line, restrict_u0)
    mats = rep_matrices()
    require(all(is_identity(mat_mul(Mx, Mx)) for Mx in mats.values()),
            "grid generators are no longer involutions")
    E4 = [F(0)] * 6
    E4[3] = F(1)
    require(all(Mx[3] == E4 for Mx in mats.values()),
            "eta_4 no longer spans the trivial line")
    sig = mats["sigma"]
    require(sig[0][1] == F(1, 4) and sig[1][0] == 4
            and sig[2][5] == 1 and sig[5][2] == 1 and sig[4][4] == 1,
            "sigma matrix moved")
    sr = mat_mul(sig, mats["r"])
    require(not is_identity(mat_mul(sr, sr))
            and is_identity(mat_mul(mat_mul(sr, sr), mat_mul(sr, sr))),
            "sigma*r must have order 4 (D4)")
    spaces = extension_spaces()
    dims = {(t1, t2): len(intersect(spaces, [t1, t2]))
            for t1, t2 in combinations(ALL_TAGS, 2)}
    vals = sorted(dims.values())
    require(vals.count(2) == 22 and vals.count(3) == 6,
            f"pairwise lattice moved: {dims}")
    require({k for k, v in dims.items() if v == 3} ==
            {("A0", "B0"), ("A0", "B+"), ("A0", "B-"),
             ("A+", "B0"), ("A-", "B0"), ("D+", "D-")},
            "the six dim-3 pairs moved")
    A3 = intersect(spaces, ["A0", "A+", "A-"])
    B3 = intersect(spaces, ["B0", "B+", "B-"])
    require(len(A3) == 2 and len(B3) == 2)
    w, _ = wstar_vector(spaces)  # asserts dim W = 1, direct tau,
    require(w == [0, 0, 0, 1, 0, 0], f"omega* moved: {w}")

    forms = numerator_forms()

    def combo(vec):
        out = [dict() for _ in range(5)]
        for a, Ns in enumerate(forms):
            for k in range(5):
                for ij, v in Ns[k].items():
                    out[k][ij] = out[k].get(ij, F(0)) + vec[a] * v
        return [{ij: v for ij, v in c.items() if v} for c in out]

    for b in A3:
        require(is_zero(restrict_line(combo(b), (F(0), F(0)),
                                      (F(1), F(0)))),
                "v=0 not integral for the A-triple space")
    for b in B3:
        require(is_zero(restrict_u0(combo(b))),
                "u=0 not integral for the B-triple space")
    ctx.note("h^0(resolution, S^4 Omega^1) = 1 = <eta_4>; D4-rep and "
             "lattice pinned; AP-family dichotomy consistent")


@check("a8.pattern_singletons", DOC)
def _(ctx):
    """Theorem A8.14: every complete genus-0 curve on X meets nodes
    over >= 2 distinct triple points (hence passes through >= 2
    distinct nodes).  Certified per triple point by the exact
    A8.7'-machinery applied to the 4-dimensional extension subsystem
    V_P: two basis-pair resultants (provably exact CRT +
    spot-verification), every entry line peeling to order >= 8 in
    both (asserted inside), and the peeled cofactors witnessed
    COPRIME over Q — so the curve part of Z(V_P) is contained in the
    nine entry lines, and a singleton node pattern would force a
    genus-0 curve with an entry-line image (impossible, A7.3).
    FAST: A0 and B0 (the latter exercising the transpose-transferred
    bases); FULL: all eight triple points."""
    from compute.node_extension import ALL_TAGS
    from compute.pattern_loci import all_singletons
    tags = ALL_TAGS if ctx.profile == "FULL" else ("A0", "B0")
    certs = all_singletons(tags)  # raises if any point fails
    require(set(certs) == set(tags))
    for tag, c in certs.items():
        require(c["witness"]["resv_mod"] != 0)
        require(c["pairs"] == ((0, 1), (0, 2)),
                f"certificate shape moved at {tag}: {c['pairs']}")
    ctx.note(f"{len(tags)} triple points: Z(V_P) curve part = entry "
             "lines only; singleton node patterns impossible")


@check("a8.pattern_pairs", DOC)
def _(ctx):
    """Theorem A8.15 (SHARP): every complete genus-0 curve on X meets
    nodes over >= 3 distinct triple points — the classical AP
    families attain exactly 3.  All 28 two-point patterns are
    excluded: a pattern-{P,Q} image must contain P and Q, avoid the
    other six triple points, be integral for V_S = V_P cap V_Q, and
    not be an entry line (A7.3).  Certificates: 6 dim-3 pairs by
    coprime peeled cofactors (Z(V_S) curve part = entry lines); 10
    pairs by the peeled cofactor not vanishing at P or Q (no
    component through both); 12 pairs by the PQ-line analysis plus a
    deg-18 cofactor PROVEN irreducible over Q (degree-preserving line
    restrictions, mod-p factor-degree subset-sums empty across
    lines/primes) that hits Q-rational outside triple points — and a
    rational point on a Q-irreducible curve lies on EVERY Galois
    conjugate component, so all its components are excluded.  FAST:
    one representative of each certificate kind; FULL: all 28."""
    from compute.pattern_loci import all_pairs
    pairs = None if ctx.profile == "FULL" else [
        ("A0", "B0"), ("A0", "A+"), ("A0", "D+"), ("A+", "B+")]
    certs = all_pairs(pairs)
    for tagS, cert in certs.items():
        require(cert["excluded"],
                f"pattern {tagS} no longer excluded: {cert}")
        require(not cert["survivors"])
    n = len(certs)
    require(n == (28 if ctx.profile == "FULL" else 4))
    ctx.note(f"{n} two-point patterns excluded; with a8.pattern_"
             "singletons: |S| >= 3 for every genus-0 curve (sharp)")


@check("a8.pattern_spaces", DOC)
def _(ctx):
    """Theorem A8.16: a complete genus-0 curve whose node pattern S
    has dim V_S >= 2 is one of the 128 classical AP components.
    Census (asserted): over ALL patterns |S| >= 3 the subspace V_S
    takes exactly 8 values — seven of dimension 2 (the A-cluster
    <eta4,eta6>, the B-cluster <eta3,eta4>, the central-line space
    <eta3+eta6,eta4>, and four outer-entry-line spaces) and
    <eta_4>.  For each dim-2 space, the integral curves of its locus
    are classified exactly: entry lines always; v = 0 exactly for
    the A-cluster; u = 0 exactly for the B-cluster; and every
    leftover cofactor K (degrees 8/8/12/18x4) is certified
    IRREDUCIBLE over Q with the integrality identity K | F(grad K)
    REFUTED mod p — by Galois conjugacy, integrality of a
    Q-irreducible curve is all-or-none, and all-integral would force
    that identity, so NO component of V(K) is integral.  Hence
    dim V_S >= 2 forces image u=0 or v=0 (classical, with S the
    family triple); the 17 other dim-2 patterns are impossible; the
    200 dim-1 patterns have V_S = <eta*> — the rational-curve
    problem on X is reduced to the eta*-web.  Both profiles run the
    full census and all seven certificates."""
    from compute.pattern_loci import classify_spaces
    scerts, census = classify_spaces()
    require(len(scerts) == 7)
    nA = sum(1 for c in scerts.values() if c["v0_integral"])
    nB = sum(1 for c in scerts.values() if c["u0_integral"])
    require(nA == 1 and nB == 1, "cluster integrality moved")
    degs = sorted(c["leftover_deg"] for c in scerts.values())
    require(degs == [8, 8, 12, 18, 18, 18, 18],
            f"leftover degrees moved: {degs}")
    n1 = sum(len(v) for k, v in census.items() if len(k) == 1)
    n2 = sum(len(v) for k, v in census.items() if len(k) == 2)
    require((n1, n2) == (200, 19), f"pattern counts moved: {(n1, n2)}")
    ctx.note("7 dim-2 spaces classified: integral curves = entry "
             "lines + v=0 (A-cluster) / u=0 (B-cluster) only; "
             "dim V_S >= 2 => classical; 200 patterns reduced to "
             "the eta*-web")
