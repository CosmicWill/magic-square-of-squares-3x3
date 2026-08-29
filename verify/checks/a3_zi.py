"""W10 / A3-S1: the Z[i] reformulation of the additive layer
(docs/ROADMAP.md §W10; compute/zi_additive.py)."""

import os

from ..framework import check, require

DOC = "docs/ROADMAP.md"

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "compute")


@check("a3.zi_reformulation", DOC)
def _(ctx):
    """A3-S1: D(m) = {|Im(z^2)| : z in Z[i], |z|^2 = m^2} exactly
    (pinned against congrua_sets over the profile range), and the
    additive-triple condition is the six-term vanishing sum
    sum eps_j (w_j - m^4/w_j) = 0 on the norm-m^4 torus (w_j = z_j^2)
    — verified equivalent to the direct D(m) scan on rich sample
    centers (both empty: the desert), with exact positive and
    soundness controls on synthetic torus points."""
    from compute.congrua_search import congrua_sets
    from compute.zi_additive import (D_from_zi, six_term_is_zero,
                                     triples_direct, triples_via_zi)

    bound = ctx.bound(full=1500, fast=600)
    ref = dict(congrua_sets(bound))
    for m in range(1, bound + 1):
        require(D_from_zi(m) == ref.get(m, set()), m)
    for m in (325, 425, 725, 845, 925, 1025, 4225):
        require(triples_via_zi(m) == [], m)
        require(triples_direct(m) == [], m)
    # positive control: 1 + 1 = 2 on the norm-5 circle
    require(six_term_is_zero(((2, 1), (2, 1), (1, 2)), (1, 1, -1), 5))
    require(not six_term_is_zero(((2, 1), (2, 1), (2, 1)),
                                 (1, 1, -1), 5))
    # soundness on a rotated circle (norm 65): criterion == direct Im
    def mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
    g = (3, 2)
    w1, w3 = mul((2, 1), g), mul((1, 2), g)
    require(six_term_is_zero((w1, w1, w3), (1, 1, -1), 65)
            is (w1[1] + w1[1] - w3[1] == 0))
    ctx.note(f"Z[i] parametrization exact to {bound}; six-term "
             "criterion sound (controls) and desert-consistent on "
             "the sample — the additive layer is an S-unit problem")


@check("a3.degenerate_subsums", DOC)
def _(ctx):
    """Proposition A3.5: every vanishing proper subsum of the
    six-term sum has size 2 or 4 with paired equal congrua (d_i =
    d_j); sizes 1, 3, 5 are impossible (size 3 by the equal-modulus
    rigidity lemma: alpha + beta = 1 with |alpha| = |beta| = 1 forces
    alpha = zeta_6, not in Q(i)).  Hence genuine additive triples of
    distinct positive congrua give NONDEGENERATE vanishing sums.
    Exhaustive exact scan over ordered point triples (repeats
    allowed), all sign patterns, all 62 proper subsums."""
    from compute.zi_additive import subsum_scan

    centers = (325, 725, 925, 1025) if ctx.bound(full=1, fast=0) \
        else (325, 925)
    for m in centers:
        n_cfg, n_van, bad = subsum_scan(m)
        require(bad == [], (m, bad[:2]))
        require((n_cfg, n_van) == (1372, 924), (m, n_cfg, n_van))
    ctx.note(f"{len(centers)} centers x 1372 configs: all 924 "
             "vanishing subsums per center are size-2/4 with paired "
             "equal congrua — A3.5 exact")


@check("a3.omega1_theorem", DOC)
def _(ctx):
    """Theorem A3.6 (the omega = 1 theorem — the first unconditional
    slice of Conjecture A3.C): for m = 2^s r p^a (r a product of
    primes = 3 mod 4, p = 1 mod 4 the ONLY split prime), D(m) admits
    no signed vanishing relation e1 d1 + e2 d2 + e3 d3 = 0 at all —
    in particular no additive triple, no 7-square three-AP
    configuration, and no MSS3 with such a center root.  Proof in
    the doc (structure D(m) = { m^2 |Im sigma^k| }, sigma =
    lambda^4/p^2, plus the Gauss-content contradiction: R(x) =
    p^2 x^2 - 2Cx + p^2 primitive would have to divide a polynomial
    with coefficients in {0,+-1,+-2,+-3}, impossible for p >= 5).
    Machine: (i) the structure lemma pinned against congrua_sets on
    every single-split m to the bound; (ii) exact nonvanishing of
    all sign/k instances to a = 6 across sample split primes;
    (iii) the direct triple-free corollary re-verified."""
    from compute.zi_additive import (omega1_D_predicted,
                                     omega1_relation_scan,
                                     split_structure, triples_direct)
    from compute.congrua_search import congrua_sets

    bound = ctx.bound(full=3000, fast=1200)
    ref = dict(congrua_sets(bound))
    n_struct = 0
    singles = []
    for m in range(2, bound + 1):
        s, r, split = split_structure(m)
        if len(split) == 1:
            require(omega1_D_predicted(m) == ref.get(m, set()), m)
            n_struct += 1
            if len(ref.get(m, set())) >= 3:
                singles.append(m)
    primes = (5, 13, 17, 29, 37, 41, 53) if ctx.bound(full=1, fast=0) \
        else (5, 13, 29)
    tot = 0
    for p in primes:
        tot += omega1_relation_scan(p, 6)
    require(tot == 224 * len(primes), tot)
    for m in singles:
        require(triples_direct(m) == [], m)
    ctx.note(f"structure exact on {n_struct} single-split m <= "
             f"{bound}; {tot} relation instances nonzero (a <= 6, "
             f"{len(primes)} primes); {len(singles)} rich single-"
             "split centers directly triple-free — Theorem A3.6")


@check("a3.omega2_ab1", DOC)
def _(ctx):
    """Theorem A3.7 (two split primes, first powers): for m = 2^s r
    p q, D(m) admits no signed additive relation.  The machine
    apparatus: all 36 canonical sign/exponent patterns classify as
    20 VALUATION-dead (ultrametric at one of the four directions),
    6 FACTORED (tan-half polynomial factors into candidate factors,
    each forcing sigma^a tau^b = +-1 — impossible in the free
    group), 3 CONGRUENCE-dead (no Pythagorean-compatible residues
    mod 16), and 7 residual patterns closed by hand in the doc via
    coprime-divisibility case trees ending in: q even / consecutive
    squares / mod-3 descents / Fermat's x^4 - y^4 = square / the
    non-congruence of 2 and 3 (self-contained descents).  Pinned:
    the classification table, two factor certificates, the four
    descent-equation searches (empty), and the real-data search on
    every residual pattern (empty)."""
    from compute.two_prime_additive import (classify_all_11,
                                            search_real_data,
                                            search_fermat_quartic,
                                            search_2b2,
                                            search_3w2_sandwich,
                                            search_quartic_3T2)
    from collections import Counter

    rep = classify_all_11()
    require(len(rep) == 36, len(rep))
    cnt = Counter(v.split()[0] for _, _, v, _ in rep)
    require(dict(cnt) == {"VALUATION": 20, "FACTORED": 6,
                          "CONGRUENCE": 3, "OPEN": 7}, dict(cnt))
    # two factor certificates pinned exactly
    certs = {tuple(p): d for p, k, v, d in rep if v == "FACTORED"}
    key1 = (((1, 0), 1), ((0, 1), 1), ((1, 1), -1))
    require(sorted(certs[key1]) == ["t1", "t1+t2", "t2"], certs[key1])
    key2 = (((1, 0), 1), ((0, 1), -1), ((1, -1), 1))
    require(certs[key2] == ["t1-t2"], certs[key2])
    # every congruence kill is mod 16
    require(all(v == "CONGRUENCE mod 16" for _, _, v, _ in rep
                if v.startswith("CONGRUENCE")))
    # residual patterns: real-data search empty
    bound = ctx.bound(full=500, fast=200)
    for p, k, v, G in rep:
        if v == "OPEN":
            require(search_real_data(G, bound) == [], p)
    # descent corroborations
    b = ctx.bound(full=400, fast=150)
    require(search_fermat_quartic(b) == [])
    require(search_2b2(b) == [])
    require(search_3w2_sandwich(5 * b) == [])
    require(search_quartic_3T2(b) == [])
    ctx.note("A3.7 apparatus: 36 patterns = 20 valuation + 6 "
             "factored + 3 mod-16 + 7 hand-descended (doc); all "
             "corroboration searches empty to the profile bounds")


@check("a3.box21", DOC)
def _(ctx):
    """Theorem A3.8 (partial; the (2,1) box = split part p^2 q):
    189 canonical patterns: 136 valuation-dead, 13 factored, 12
    congruence-dead, 28 residual.  Of the residuals: 7 are the
    (1,1)-box recurrences closed by Theorem A3.7; ELEVEN more are
    closed by the Gaussian-collapse trees (doc §2.7): the alpha and
    F-C pairs and F-D via trees ending in Fermat's x^4 - y^4 = z^2
    at level 2 (x = p^2 or y = p^2), the beta1 pair via the exact
    collapse Im(ell^3 w^2) = 2 q^2 s1 C (q-adic valuation kill), and
    the four doubled F-F patterns via level-2 replication of the
    A3.7 Family-III trees (mod 16 and Lemma L2).  TEN equations
    remain open (beta2 x4, F-E x6), pinned in
    data_box21_open.json with empty real-data searches.  FAST
    verifies the eleven kill identities against the machine
    polynomials and the open equations' searches; FULL re-runs the
    full census."""
    import json as _json
    import random
    from compute.two_prime_additive import (box21_kill_form,
                                            search_real_data)

    with open(os.path.join(DATA, "data_box21_census.json"),
              encoding="utf-8") as fh:
        cen = _json.load(fh)
    require(cen["counts"] == {"VALUATION": 136, "FACTORED": 13,
                              "CONGRUENCE": 12, "OPEN": 28}
            and cen["n"] == 189, cen)
    with open(os.path.join(DATA, "data_box21_open.json"),
              encoding="utf-8") as fh:
        data = _json.load(fh)
    require(len(data) == 21, len(data))

    def parse(Gs):
        return {tuple(map(int, k.strip("()").split(","))): v
                for k, v in Gs.items()}

    def geval(G, *x):
        return sum(v * x[0] ** a * x[1] ** b * x[2] ** c * x[3] ** d
                   for (a, b, c, d), v in G.items())

    closed = {
        (((1, 0), (2, 1), (2, -1)), (1, 1, -1)): ("alpha", 1, False),
        (((1, 0), (2, 1), (2, -1)), (1, -1, 1)): ("alpha", -1, False),
        (((2, 0), (2, 1), (2, -1)), (1, 1, -1)): ("FC", 1, False),
        (((2, 0), (2, 1), (2, -1)), (1, -1, 1)): ("FC", -1, False),
        (((0, 1), (2, 1), (2, -1)), (1, -1, -1)): ("FD", None, False),
        (((2, 0), (1, 1), (2, 1)), (1, -1, -1)): ("beta1", 1, False),
        (((2, 0), (1, -1), (2, -1)), (1, -1, -1)): ("beta1", -1, False),
        (((2, 1), (2, -1)), (2, 1)): ("FF1", 1, False),
        (((2, 1), (2, -1)), (2, -1)): ("FF2", 1, False),
        (((2, -1), (2, 1)), (2, 1)): ("FF2", 1, True),
        (((2, -1), (2, 1)), (2, -1)): ("FF1", 1, True),
    }
    rng = random.Random(23)
    n_closed = n_open = 0
    for classes, coeffs, Gs in data:
        key = (tuple(tuple(jk) for jk in classes), tuple(coeffs))
        G = parse(Gs)
        if key in closed:
            kind, sgn, flip = closed[key]
            for _ in range(40):
                x = [rng.randint(-9, 9) for _ in range(4)]
                xs = list(x)
                if flip:
                    xs[3] = -xs[3]
                h = box21_kill_form(kind, sgn, *xs)
                require((geval(G, *x) == 0) == (h == 0),
                        (key, kind, x))
            n_closed += 1
        else:
            bound = ctx.bound(full=500, fast=150)
            require(search_real_data(G, bound) == [], key)
            n_open += 1
    require(n_closed == 11 and n_open == 10, (n_closed, n_open))
    if ctx.bound(full=1, fast=0):
        from collections import Counter
        from compute.two_prime_additive import classify_box, CLASSES_21
        rep = classify_box(CLASSES_21, 2, 1)
        cnt = Counter(v.split()[0] for _, _, v, _ in rep)
        require(dict(cnt) == cen["counts"], dict(cnt))
    ctx.note("(2,1) box: 189 patterns; 7 by A3.7 + 11 closed today "
             "(Fermat at level 2, the Im(ell^3 w^2) collapse, F-F "
             "replication); 10 explicit equations open, searches "
             "empty")


@check("a3.box21_grind", DOC)
def _(ctx):
    """The grind of the (2,1)-box residual equations: beta2 (x4) and
    E3 (x2) closed — 17 of 21 residuals now down, four E1/E2
    patterns remain.  beta2: the exact collapse relation =
    2(CS q^2 + R3 (c1 v - s1 u)) (verified symbolically) forces
    T3 = c1^2 - 3 s1^2 to divide q^2; T3 = +-1 dies on consecutive
    squares/Pell parity, T3 = +-q dies mod q (c1 v = s1 u with
    u^2 = -v^2 mod q forces q | p^2), T3 = -q^2 dies mod 16, and
    T3 = +q^2 factors 16a^4 + 40a^2b^2 + 9b^4 = p^2 (and the
    144/40/1 mirror) into COPRIME factors (4a^2+9b^2)(4a^2+b^2),
    forcing a factor = 1 — dead.  E3: the tree forces u = p^2 C t',
    v = t' S(4C - p^2), the collapse u + iv = t'(ell^4 + 2i s1
    ellbar^3) (verified symbolically), t' = +-1 by mu-bar valuation,
    sign/unit fixed mod 8 (s1 = 2 mod 4 dies), and then mu^4 -
    ell^4 = 2i s1 ellbar^3: lambda-bar concentrates in ONE of the
    four factors (mu - i^k ell), giving norm >= p^6, while the norm
    identity q^4 = p^8 + 4s1^2 p^6 + 4 s1 Im(ell^7) bounds every
    factor by ~5.4 p^2 — dead for all p.  Searches corroborate."""
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL, W, Q2,
                                            search_real_data)
    import json as _json

    P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}

    def im_pow(a, weps, wpow=2):
        Rl, Il = gauss_pow(*ELL, a)
        Rw, Iw = gauss_pow(*W, wpow)
        if weps < 0:
            Iw = {k: -v for k, v in Iw.items()}
        return p4add(p4mul(Rl, Iw), p4mul(Il, Rw))

    def im_ell(a):
        return gauss_pow(*ELL, a)[1]

    # beta2 collapse: q^2 Im ell^4 + p^2 Im(ell^2 w^2) - Im(ell^4 wbar^2)
    #   == 2 [ CS q^2 + R3 (c1 v - s1 u) ]
    rel = p4add(p4add(p4mul(Q2, im_ell(4)), p4mul(P2, im_pow(2, 1)), 1),
                im_pow(4, -1), -1)
    C = {(2, 0, 0, 0): 1, (0, 2, 0, 0): -1}
    S = {(1, 1, 0, 0): 2}
    R3 = p4mul({(1, 0, 0, 0): 1},
               p4add({(2, 0, 0, 0): 1}, {(0, 2, 0, 0): 3}, -1))
    u = {(0, 0, 2, 0): 1, (0, 0, 0, 2): -1}
    v = {(0, 0, 1, 1): 2}
    Y = p4add(p4mul({(1, 0, 0, 0): 1}, v),
              p4mul({(0, 1, 0, 0): 1}, u), -1)
    claim = p4add(p4mul(p4mul(C, S), Q2), p4mul(R3, Y), 1)
    claim = {k: 2 * vv for k, vv in claim.items()}
    require(p4add(rel, claim, -1) == {}, "beta2 collapse identity")

    # E3 relation: p^2 Im(ell^2 w^2) - Im(ell^4 w^2) - Im(ell^4 wbar^2)
    #   == p^2(Cv + Su) - 4u * CS   (Im ell^4 = 2CS)
    rel3 = p4add(p4add(p4mul(P2, im_pow(2, 1)), im_pow(4, 1), -1),
                 im_pow(4, -1), -1)
    CvSu = p4add(p4mul(C, v), p4mul(S, u), 1)
    claim3 = p4add(p4mul(P2, CvSu),
                   {k: 4 * vv for k, vv in p4mul(u, p4mul(C, S)).items()},
                   -1)
    require(p4add(rel3, claim3, -1) == {}, "E3 reduction identity")

    # E3 collapse: p^2 C + i S(4C-p^2) == ell^4 + 2i s1 ellbar^3
    # (real and imaginary parts as 2-var polys in (c1, s1))
    Rl4, Il4 = gauss_pow(*ELL, 4)
    Rl3, Il3 = gauss_pow(*ELL, 3)
    # conj(ell)^3: (Rl3, -Il3); times 2i s1: re = 2 s1 Il3, im = 2 s1 Rl3
    s1m = {(0, 1, 0, 0): 2}
    Zre = p4add(Rl4, p4mul(s1m, Il3), 1)
    Zim = p4add(Il4, p4mul(s1m, Rl3), 1)
    p2C = p4mul(P2, C)
    S4Cp2 = p4mul(S, p4add({k: 4 * vv for k, vv in C.items()}, P2, -1))
    require(p4add(Zre, p2C, -1) == {} and p4add(Zim, S4Cp2, -1) == {},
            "E3 Gaussian collapse identity")

    # beta2 T3 = +q^2 factorizations and terminal searches
    for a in range(1, 30):
        for b in range(1, 30):
            require(16 * a ** 4 + 40 * a * a * b * b + 9 * b ** 4
                    == (4 * a * a + 9 * b * b) * (4 * a * a + b * b))
            require(144 * a ** 4 + 40 * a * a * b * b + b ** 4
                    == (36 * a * a + b * b) * (4 * a * a + b * b))
    # searches: the four still-open E1/E2 patterns stay empty
    with open(os.path.join(DATA, "data_box21_open.json"),
              encoding="utf-8") as fh:
        data = _json.load(fh)
    still_open = {(((1, 1), (2, 1), (2, -1)), (1, 1, -1)),
                  (((1, 1), (2, 1), (2, -1)), (1, -1, 1)),
                  (((1, -1), (2, 1), (2, -1)), (1, 1, -1)),
                  (((1, -1), (2, 1), (2, -1)), (1, -1, 1))}
    bound = ctx.bound(full=500, fast=150)
    n_open = 0
    for classes, coeffs, Gs in data:
        key = (tuple(tuple(jk) for jk in classes), tuple(coeffs))
        if key in still_open:
            G = {tuple(map(int, k.strip("()").split(","))): vv
                 for k, vv in Gs.items()}
            require(search_real_data(G, bound) == [], key)
            n_open += 1
    require(n_open == 4, n_open)
    ctx.note("beta2 and E3 collapses verified symbolically; "
             "factorizations exact; 17/21 residuals closed, the four "
             "E1/E2 patterns open (searches empty)")
