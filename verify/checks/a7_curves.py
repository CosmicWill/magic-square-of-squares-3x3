"""Mechanical verification for docs/attacks/A7-curve-enumeration.md."""

from itertools import combinations, product

from ..framework import check, require
from ..targets import lucas_entries
from compute.curve_pullbacks import (ENTRY_LINES, analyze_line,
                                     classify_lines, cover_invariants,
                                     multiple_points, norm_point,
                                     scan_double_planes)
from compute.conic_pullbacks import analyze_conic, candidates

DOC = "docs/attacks/A7-curve-enumeration.md"


@check("a7.cross_module", DOC)
def _(ctx):
    """The nine entry-line covectors used by the curve machinery agree with
    the Lucas entries of verify.targets (coefficient extraction)."""
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    derived = list(zip(*[lucas_entries(*e) for e in basis]))
    require([tuple(d) for d in derived] == ENTRY_LINES, "covector mismatch")


@check("a7.lines", DOC)
def _(ctx):
    """Theorem A7.3: the exhaustive 69-line sweep yields exactly u=0, v=0
    (genus 0, 64 components, degenerate) and c=0 (genus 1, 16 components,
    center-zero); entry-line r-profile as stated."""
    low, cands = classify_lines()
    require(len(cands) == 69, f"candidate count {len(cands)}")
    got = {d["line"]: (d["r"], d["k"], d["genus"], d["n_components"],
                       d["degenerate"], tuple(d["zero_entries"]))
           for d in low}
    want = {
        (0, 1, 0): (3, 2, 0, 64, True, ()),      # u = 0
        (0, 0, 1): (3, 2, 0, 64, True, ()),      # v = 0
        (1, 0, 0): (4, 3, 1, 16, False, (4,)),   # c = 0 (center entry zero)
    }
    require(got == want, f"line classification changed: {got}")
    # entry-line profile: c-line r=4; u/v-type r=6; (u+-v)-type r=5
    profile = {}
    for L in ENTRY_LINES:
        d = analyze_line(L)
        profile[L] = (d["r"], d["genus"])
    require(profile[(1, 0, 0)] == (4, 1))
    for L in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1)]:
        require(profile[L] == (6, 17), f"u-type {L}: {profile[L]}")
    for L in [(1, 1, 1), (1, -1, -1), (1, 1, -1), (1, -1, 1)]:
        require(profile[L] == (5, 5), f"mixed-type {L}: {profile[L]}")
    ctx.note("exactly three low-genus lines: u=0, v=0 (g=0), c=0 (g=1)")


@check("a7.k_lemma", DOC)
def _(ctx):
    """Lemma A7.2 (k = r-1) verified by brute force on every candidate
    line: the even-subset span of the collision vectors equals the full
    even-weight subspace."""
    _, cands = classify_lines()
    entry_set = {norm_point(L) for L in ENTRY_LINES}
    for line in cands:
        is_entry = line in entry_set
        from compute.curve_pullbacks import line_points_on
        pattern = line_points_on(line)
        pts = sorted(pattern, key=str)
        idx = {p: i for i, p in enumerate(pts)}
        forms = [i for i in range(9)
                 if not (is_entry and norm_point(ENTRY_LINES[i]) == line)]
        vecs = {i: [0] * len(pts) for i in forms}
        for p, lines_here in pattern.items():
            for i in lines_here:
                vecs[i][idx[p]] ^= 1
        # brute-force even-subset span rank
        span = set()
        flist = list(forms)
        for mask in range(0, 1 << len(flist)):
            if bin(mask).count("1") % 2:
                continue
            v = [0] * len(pts)
            for b, i in enumerate(flist):
                if mask >> b & 1:
                    v = [x ^ y for x, y in zip(v, vecs[i])]
            span.add(tuple(v))
        # rank of the span
        basis = []
        for v in span:
            v = list(v)
            for b in basis:
                piv = next(j for j, x in enumerate(b) if x)
                if v[piv]:
                    v = [x ^ y for x, y in zip(v, b)]
            if any(v):
                basis.append(v)
        require(len(basis) == len(pts) - 1,
                f"k != r-1 on line {line}: {len(basis)} vs r={len(pts)}")
        # and it IS the even-weight subspace
        require(all(sum(v) % 2 == 0 for v in span), "odd vector in span")
    ctx.note("k = r-1 (even-weight span) on all 69 candidate lines")


@check("a7.u0_param", DOC)
def _(ctx):
    """The classical 3-AP family parametrizes a rational component over
    u = 0: root polynomials (t^2+1, t^2-2t-1, t^2+2t-1) square to the
    Lucas entries of L((t^2+1)^2, 0, 4t^3-4t) identically (grid proof:
    degree 4 identities, 6+ points)."""
    for t in range(-6, 7):
        c = (t * t + 1) ** 2
        v = 4 * t ** 3 - 4 * t
        ents = lucas_entries(c, 0, v)
        a, b, d = t * t + 1, t * t - 2 * t - 1, t * t + 2 * t - 1
        roots = [a, b, d, d, a, b, b, d, a]
        require([r * r for r in roots] == ents, f"parametrization at t={t}")
        sums = {sum(ents[i] for i in line) for line in
                [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                 (2, 5, 8), (0, 4, 8), (2, 4, 6)]}
        require(sums == {3 * c}, "not magic")
    ctx.note("u=0 genus-0 component: explicit, entries repeat in triples")


@check("a7.c0_curve", DOC)
def _(ctx):
    """The c = 0 component model E: gamma^2 = alpha^2 + beta^2,
    delta^2 = alpha^2 - beta^2 is smooth (genus 1), carries the
    Q(i,sqrt5) witness, and multiplies out to Fermat's right-triangle
    equation (F3.2 territory)."""
    # witness: (alpha^2, beta^2) = (1681, 720), gamma = 49, delta = 31
    require(49 ** 2 == 1681 + 720 and 31 ** 2 == 1681 - 720)
    require(41 ** 4 - 720 ** 2 == (49 * 31) ** 2, "FRT identity at witness")
    # multiplied identity is formal: (a^2+b^2)(a^2-b^2) = a^4 - b^4
    for a, b in product(range(-4, 5), repeat=2):
        require((a * a + b * b) * (a * a - b * b) == a ** 4 - b ** 4)
    # smoothness: the six 2x2 minors of the Jacobian
    #   [[2a, 2b, -2g, 0], [2a, -2b, 0, -2d]]
    # are (up to constants) the six pairwise products of the coordinates,
    # so a singular point has at most ONE nonzero coordinate — i.e. is one
    # of the four coordinate points, none of which lies on the curve:
    for pt_idx in range(4):
        al, be, ga, de = [1 if i == pt_idx else 0 for i in range(4)]
        on_curve = (ga * ga == al * al + be * be
                    and de * de == al * al - be * be)
        require(not on_curve, f"coordinate point {pt_idx} on curve")
    # minor-product identity spot check on a grid:
    for al, be in product(range(-3, 4), repeat=2):
        m1 = (2 * al) * (-2 * be) - (2 * be) * (2 * al)
        require(m1 == -8 * al * be)
    ctx.note("smooth genus-1 model; witness on curve; F3.2 controls Q-points")


@check("a7.invariants", DOC)
def _(ctx):
    """Section 5 invariants, recomputed from incidence data: chi_top(X)=512,
    chi_top(resolution)=768, K^2=576 (two routes), chi(O)=112 (Noether
    integral), s2=-192; and no intermediate double plane has s2>0."""
    inv = cover_invariants()
    require(inv["t"] == {2: 12, 3: 8})
    require(inv["chi_U"] == 13 and inv["n_nodes"] == 256)
    require(inv["chi_top_X"] == 512 and inv["chi_top_resolution"] == 768)
    require(inv["K2"] == 576 and inv["K2_adjunction"] == 576)
    require(inv["chi_O"] == 112 and (576 + 768) % 12 == 0)
    require(inv["s2"] == -192)
    if ctx.profile == "FULL":
        require(scan_double_planes() == [], "positive-s2 double plane?!")
    ctx.note("K^2=576, c2=768, chi(O)=112, s2=-192: hyperbolicity is nodal")


@check("a7.conics", DOC)
def _(ctx):
    """Conic layer: the circle control gives (k, r_eff, genus) = (4, 6, 9)
    with full multiplicity 18; the candidate sweeps yield zero genus <= 1
    components."""
    circle = analyze_conic([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], "circle")
    require((circle["k"], circle["r_eff"], circle["genus"]) == (4, 6, 9),
            f"circle control changed: {circle}")
    require(circle["total_mult_check"] == 18)
    cands = candidates()
    if ctx.profile != "FULL":
        cands = [c for c in cands if not c[0].startswith("pencil")]
    n = hits = 0
    for name, M in cands:
        data = analyze_conic(M, name)
        if data.get("reducible") or data.get("degenerate_contained"):
            continue
        n += 1
        if data["genus"] is not None and data["genus"] <= 1:
            hits += 1
    require(hits == 0, f"genus<=1 conic component found ({hits})!")
    ctx.note(f"{n} irreducible candidate conics, zero low-genus components")
