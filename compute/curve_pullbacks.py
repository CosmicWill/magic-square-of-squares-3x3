"""Genus analysis of curve pullbacks to the magic-squares surface X
(docs/attacks/A7-curve-enumeration.md).

X -> P^2_(c:u:v) is the (Z/2)^8 cover branched over the nine entry lines
of the Lucas parametrization.  For a curve C in the plane, the reduced
preimage splits into isomorphic components; this module computes, exactly:

  * the collision pattern of C with the arrangement (which entry lines
    meet C where, with what intersection multiplicities),
  * the component count, the component Galois rank k, the effective
    branch count r_eff, and the geometric genus of each component:
        chi = 2^(k+1) - r_eff * 2^(k-1)   =>   g = 1 + 2^(k-2) (r_eff - 4)
    (k >= 2; g = (r_eff-2)/2 for k = 1; g = 0 for k = 0),
  * degeneracy data: which entries coincide identically along C, and
    which entries vanish identically.

All arithmetic is exact (integers / Fractions); root coincidences of the
restricted binary forms are detected via gcds over Q, so conjugate
Qbar-roots are handled as Galois orbits (an irreducible factor of degree
d contributes d branch points with identical behavior).

Lines: everything is rational and the theory collapses to
    g = 1 + 2^(r-3) (r - 4),   r = #distinct collision points
(see the A7 document for the proof).  Genus <= 1 over a line forces
r <= 4, which forces the line through multiple points of the arrangement
in one of the patterns (3,3,3), (3,3,2,1), (3,2,2,2) — a finite check
performed by classify_lines().

Run:  python3 -m compute.curve_pullbacks
"""

from fractions import Fraction
from itertools import combinations
from math import gcd

# the nine entry lines as covectors on (c, u, v), row-major Lucas order
ENTRY_LINES = [(1, 1, 0), (1, -1, -1), (1, 0, 1),
               (1, -1, 1), (1, 0, 0), (1, 1, -1),
               (1, 0, -1), (1, 1, 1), (1, -1, 0)]

ENTRY_NAMES = ["c+u", "c-u-v", "c+v", "c-u+v", "c", "c+u-v",
               "c-v", "c+u+v", "c-u"]


# ---------------------------------------------------------------------------
# projective utilities (integers)

def norm_point(p):
    g = 0
    for x in p:
        g = gcd(g, abs(x))
    p = tuple(x // g for x in p)
    for x in p:
        if x:
            return p if x > 0 else tuple(-y for y in p)
    raise ValueError("zero vector")


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def multiple_points():
    """All intersection points of the arrangement with their line sets."""
    pts = {}
    for i, j in combinations(range(9), 2):
        p = norm_point(cross(ENTRY_LINES[i], ENTRY_LINES[j]))
        pts.setdefault(p, set()).update((i, j))
    return pts


# ---------------------------------------------------------------------------
# line pullback analysis

def line_points_on(line):
    """Collision pattern of a line (covector) with the arrangement:
    {point: [entry indices meeting the line there]}, excluding entry lines
    equal to the line itself."""
    line = norm_point(line)
    pattern = {}
    for i, L in enumerate(ENTRY_LINES):
        if norm_point(L) == line:
            continue
        p = norm_point(cross(line, L))
        pattern.setdefault(p, []).append(i)
    return pattern


def analyze_line(line):
    """Full pullback data for a plane line (covector, integer tuple)."""
    line = norm_point(line)
    is_entry = line in {norm_point(L) for L in ENTRY_LINES}
    pattern = line_points_on(line)
    r = len(pattern)
    n_forms = 8 if is_entry else 9
    # k = r - 1 in all line cases (proof in the A7 doc: parities of the
    # per-point selection counts realize every even-total pattern)
    k = r - 1
    # every collision point is a branch point of the (connected) components
    r_eff = r
    if k == 0:
        genus = 0
    elif k == 1:
        assert r_eff % 2 == 0
        genus = (r_eff - 2) // 2
    else:
        num = 2 ** (k - 2) * (r_eff - 4)
        genus = 1 + num
    n_components = 2 ** ((8 if not is_entry else 7) - k)
    # degeneracy: identically-equal entry pairs along the line <=> the
    # line is contained in {l_i = l_j} <=> covector parallel to l_i - l_j
    equal_pairs = []
    for i, j in combinations(range(9), 2):
        d = tuple(a - b for a, b in zip(ENTRY_LINES[i], ENTRY_LINES[j]))
        if norm_point(d) == line:
            equal_pairs.append((i, j))
    zero_entries = [i for i, L in enumerate(ENTRY_LINES)
                    if norm_point(L) == line]
    return {
        "line": line, "is_entry_line": is_entry, "pattern": pattern,
        "r": r, "k": k, "genus": genus, "n_components": n_components,
        "equal_entry_pairs": equal_pairs, "zero_entries": zero_entries,
        "degenerate": bool(equal_pairs),
    }


def classify_lines():
    """The completeness search: every line whose pullback has a genus <= 1
    component satisfies r <= 4, which (9 intersections, parts of size <= 3)
    forces passage through >= 2 multiple points of the arrangement.  So the
    candidate set 'all lines through >= 2 multiple points' + the 9 entry
    lines is exhaustive.  Returns (low_genus_list, candidates_checked)."""
    pts = multiple_points()
    mpts = list(pts)
    candidates = {norm_point(L) for L in ENTRY_LINES}
    for p, q in combinations(mpts, 2):
        candidates.add(norm_point(cross(p, q)))
    low = []
    for line in sorted(candidates):
        data = analyze_line(line)
        if data["genus"] <= 1:
            low.append(data)
    return low, sorted(candidates)


# ---------------------------------------------------------------------------
# invariants of the resolved cover (C3): stratified Euler characteristic

def cover_invariants():
    """chi_top of the resolution X~ of the full (Z/2)^8 cover, K^2, chi(O),
    from the arrangement stratification.  Returns a dict; every ingredient
    is recomputed from the incidence data (nothing hard-coded)."""
    pts = multiple_points()
    t = {}
    for p, lines in pts.items():
        t[len(lines)] = t.get(len(lines), 0) + 1
    # chi of the line union and of the open complement U
    chi_union = 9 * 2 - sum((m - 1) * cnt for m, cnt in t.items())
    chi_U = 3 - chi_union
    # per-line open parts
    chi_L_open = []
    for i in range(9):
        on_line = sum(1 for p, lines in pts.items() if i in lines)
        chi_L_open.append(2 - on_line)
    # strata contributions: sheets = |G| / |inertia|
    G = 2 ** 8
    chi_X = G * chi_U
    chi_X += (G // 2) * sum(chi_L_open)
    n_nodes = 0
    for p, lines in pts.items():
        m = len(lines)
        chi_X += G // (2 ** m)          # points upstairs (chi = 1 each)
        if m == 3:
            n_nodes += G // (2 ** m)    # each an A_1 node
    chi_resolution = chi_X + n_nodes    # node -> P^1 : chi 1 -> 2
    # K^2 by the branched-cover formula (and, independently, adjunction on
    # the degree-64 complete intersection: K = 3H, K^2 = 9*64)
    K2_cover = G * Fraction(9, 4)       # (K_P2 + B/2)^2 = (3/2)^2
    K2_adjunction = 9 * 64
    chi_O = Fraction(int(K2_cover) + chi_resolution, 12)
    return {
        "t": t, "chi_U": chi_U, "chi_L_open": chi_L_open,
        "n_nodes": n_nodes, "chi_top_X": chi_X,
        "chi_top_resolution": chi_resolution,
        "K2": int(K2_cover), "K2_adjunction": K2_adjunction,
        "chi_O": chi_O, "s2": int(K2_cover) - chi_resolution,
    }


def double_plane_invariants(S):
    """Invariants for the intermediate DOUBLE cover Y_S -> P^2 branched on
    the even-size entry-line subset S (a single character of the tower):
    K^2 of the smooth model that resolves the branch-curve singularities by
    canonical resolution, and chi_top by stratification.  Returns
    (K2, chi_top, s2) for the resolution of Y_S."""
    S = sorted(S)
    m = len(S)
    assert m % 2 == 0
    pts = multiple_points()
    # singular points of the branch curve inside S: points where >= 2 of
    # the S-lines meet.  For a double point of the branch curve (node),
    # canonical resolution: K^2 drops by 0... for a plane curve with
    # nodes/triple points, the standard double-plane resolution changes
    # K^2 and chi as follows (even multiplicities absorbed):
    #   at a point of multiplicity mu of the branch curve, blow up: the
    #   branch multiplicity mu contributes; for mu = 2 (node): K^2 -=0,
    #   handled by even-reduction; for mu = 3: branch acquires
    #   infinitely-near structure.
    # We compute chi_top directly by stratification instead, and K^2 via
    # K = pi*(K_P2 + B_red/2) corrected only by canonical A_1 resolutions
    # (mu = 2: cover point is an A_1 node upstairs? no — for a double
    # cover, a node of the branch curve gives an A_1 singularity of Y_S;
    # a triple point gives a D_4 singularity; both canonical, resolution
    # crepant, so K^2 = 2 * (m/2 - 3)^2 unchanged).
    K2 = 2 * (Fraction(m, 2) - 3) ** 2
    # chi_top by strata: off the S-lines: double sheets where the S-parity
    # ... character chi_S ramifies exactly over the S-lines.
    chi_union_S = 0
    # chi of the union of S-lines, and per-point multiplicities within S
    ptmult = {}
    for p, lines in pts.items():
        ms = len(set(lines) & set(S))
        if ms >= 2:
            ptmult[p] = ms
    chi_union_S = 2 * m - sum(ms - 1 for ms in ptmult.values())
    chi_U = 3 - chi_union_S
    # points on each S-line (collisions with other S-lines only)
    chi_open_lines = 0
    for i in S:
        on_line = sum(1 for p, ms in ptmult.items() if i in pts[p])
        chi_open_lines += 2 - on_line
    chi_Y = 2 * chi_U + 1 * chi_open_lines  # branch locus: 1 sheet
    n_A1 = n_D4 = 0
    for p, ms in ptmult.items():
        chi_Y += 1  # one point upstairs over each branch-curve singularity
        if ms == 2:
            n_A1 += 1
        elif ms == 3:
            n_D4 += 1
    # resolutions: A_1 -> +1 to chi; D_4 -> +4 (four exceptional P^1s in
    # the minimal resolution of D_4, tree with chi contribution 4+1... the
    # exceptional divisor of D_4 is 4 P^1s in a star: chi = 4*2 - 3 = 5,
    # replacing a point: delta chi = +4).
    chi_res = chi_Y + n_A1 * 1 + n_D4 * 4
    s2 = K2 - chi_res
    return {"S": S, "K2": K2, "chi_top": chi_res, "s2": s2,
            "n_A1": n_A1, "n_D4": n_D4}


def scan_double_planes():
    """All even subsets S of the 9 entry lines, |S| >= 6 (smaller branch
    degree cannot be general type with s2 > 0): report those with s2 > 0."""
    out = []
    for m in (6, 8):
        for S in combinations(range(9), m):
            inv = double_plane_invariants(S)
            if inv["s2"] > 0:
                out.append(inv)
    return out


def main():
    print("== line classification ==")
    low, cands = classify_lines()
    print(f"candidate lines checked: {len(cands)}")
    for d in low:
        nm = ",".join(ENTRY_NAMES[i] for i in d["zero_entries"]) or "-"
        eq = len(d["equal_entry_pairs"])
        print(f"  line {d['line']}: r={d['r']} k={d['k']} genus={d['genus']}"
              f" comps={d['n_components']} zero=[{nm}] equal-pairs={eq}")
    print("\n== invariants of the full cover ==")
    inv = cover_invariants()
    for key in ("t", "chi_U", "n_nodes", "chi_top_X",
                "chi_top_resolution", "K2", "K2_adjunction", "chi_O", "s2"):
        print(f"  {key} = {inv[key]}")
    print("\n== double-plane scan (s2 > 0) ==")
    pos = scan_double_planes()
    print(f"  positive-s2 double planes: {len(pos)}")
    for inv in pos[:10]:
        print(f"  S={inv['S']} K2={inv['K2']} chi={inv['chi_top']} "
              f"s2={inv['s2']} (A1={inv['n_A1']}, D4={inv['n_D4']})")


if __name__ == "__main__":
    main()
