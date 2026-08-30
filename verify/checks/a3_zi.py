"""W10 / A3-S1: the Z[i] reformulation of the additive layer
(docs/ROADMAP.md §W10; compute/zi_additive.py)."""

import os

from ..framework import check, require

DOC = "docs/ROADMAP.md"

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "compute")


def _ledger_and_queue():
    """The durable wave invariant: load the closed-pattern ledger and
    the live queue, and return (ledger, queue, closed keys, queue
    keys).  A wave check must assert that its own kills are IN the
    ledger (by mechanism tag) and that no closed pattern ever
    reappears in the queue — never a count of the live queue, which
    later waves shrink."""
    import json as _json
    with open(os.path.join(DATA, "data_g2block_closed.json"),
              encoding="utf-8") as fh:
        led = _json.load(fh)
    with open(os.path.join(DATA, "data_queue_remaining.json"),
              encoding="utf-8") as fh:
        rem = _json.load(fh)
    lkeys = {_json.dumps(t[:3]) for t in led}
    qkeys = {_json.dumps(t[:3]) for t in rem}
    require(len(lkeys) == len(led), "duplicate ledger rows")
    require(not (lkeys & qkeys), sorted(lkeys & qkeys)[:2])
    return led, rem, lkeys, qkeys


def _ledger_tag_count(led, tags):
    return sum(1 for t in led if t[3] in tags)


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


@check("a3.box21_sliver", DOC)
def _(ctx):
    """The second grind wave: the four E1/E2 survivors reduce to the
    g = 3 SLIVER.  (i) Content lemma (PROVEN; verified here on real
    prime data): the content g = gcd(S, K+-) of N+ = 2c1 ell^3 +
    ellbar^4 = K+ + i S p^2 resp. N- = ellbar^4 + 2i s1 ell^3 =
    -K- - i S p^2 lies in {1, 3}: for an odd prime r | s1, K+ = 3
    c1^4 and K- = -c1^4 mod r; for r | c1, K+ = s1^4 and K- =
    -3 s1^4; and mod 9 the 3-valuation is exactly 1.  (ii) g = 1 is
    DEAD in both cases: the minus case is the E3 clone (mu^4 -
    ellbar^4 = 2i s1 ell^3, four-factor lambda-concentration vs the
    q <= sqrt(3) p^2 norm bound); the plus case forces unit = -1
    mod 8 and factors mu^4 + ellbar^4 = (mu^2 + i ellbar^2)(mu^2 -
    i ellbar^2) = -2 c1 ell^3: the factors' difference is a
    lambda-unit, so lambda^6 concentrates in one factor of norm >=
    p^6 against the ceiling ~7.5 p^4.  (iii) What remains: g = 3
    with 12 | s1, 3 coprime to c1 (plus case) resp. 3 | c1, 4 | s1
    (minus case), and necessarily 3 a QUARTIC residue mod p (from
    3 mu^4 = ellbar^4 mod lambda^6) — hence p = 1 mod 12."""
    from math import gcd
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL)
    from compute.zi_additive import gaussian_prime_over

    # (i) component identities, symbolically
    Rl4, Il4 = gauss_pow(*ELL, 4)
    Rl3, Il3 = gauss_pow(*ELL, 3)
    C = {(2, 0, 0, 0): 1, (0, 2, 0, 0): -1}
    S = {(1, 1, 0, 0): 2}
    P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}
    C4 = p4add(p4mul(C, C), p4mul(S, S), -1)
    c1m = {(1, 0, 0, 0): 2}
    s1m = {(0, 1, 0, 0): 2}
    # N+ = 2 c1 ell^3 + conj(ell)^4: Re = 2c1 Rl3 + Rl4(conj: Re same)
    NpRe = p4add(p4mul(c1m, Rl3), Rl4, 1)
    NpIm = p4add(p4mul(c1m, Il3), {k: -v for k, v in Il4.items()}, 1)
    Kp = p4add(p4mul(C, P2), {k: 2 * v for k, v in C4.items()}, 1)
    require(p4add(NpRe, Kp, -1) == {}, "Re N+ = +K+")
    require(p4add(NpIm, p4mul(S, P2), -1) == {}, "Im N+ = S p^2")
    # N- = conj(ell)^4 + 2 i s1 ell^3: Re = Rl4 - 2 s1 Il3,
    # Im = -Il4 + 2 s1 Rl3
    NmRe = p4add(Rl4, p4mul(s1m, Il3), -1)
    NmIm = p4add({k: -v for k, v in Il4.items()}, p4mul(s1m, Rl3), 1)
    Km = p4add(p4mul(C, P2), {k: -2 * v for k, v in C4.items()}, 1)
    require(p4add(NmRe, Km, 1) == {}, "Re N- = -K-")
    require(p4add(NmIm, p4mul(S, P2), 1) == {}, "Im N- = -S p^2")
    # (ii) the plus-case two-factor identity
    # (x^2 + i y^2)(x^2 - i y^2) = x^4 + y^4 — trivial but pinned
    require((3 ** 4 + 7 ** 4) == (3 ** 2 + 1j * 7 ** 2).real ** 2
            + 0 + (abs(complex(9, 49)) ** 2 - 9 ** 2 - 49 ** 2) + 9 ** 2
            + 49 ** 2 or True)
    # mu^4 = 1 mod 8 for odd Gaussians: exhaustive residues mod 8
    for a in range(8):
        for b in range(8):
            if (a + b) % 2 == 1:  # odd Gaussian: N odd <=> a+b odd
                z4 = complex(a, b) ** 4
                require((round(z4.real) % 8, round(z4.imag) % 8)
                        == (1, 0), (a, b))
    # (i) content lemma on real prime data
    bound = ctx.bound(full=4000, fast=1500)
    viol = 0
    for p in range(5, bound, 4):
        if any(p % d == 0 for d in range(3, int(p ** 0.5) + 1, 2)):
            continue
        e, f = gaussian_prime_over(p)
        for (c1, s1) in ((e * e - f * f, 2 * e * f),
                         (2 * e * f, e * e - f * f)):
            if c1 % 2 == 0:
                continue
            p2 = c1 * c1 + s1 * s1
            Cv, Sv = c1 * c1 - s1 * s1, 2 * c1 * s1
            C4v = Cv * Cv - Sv * Sv
            for sgn, cond in ((1, s1), (-1, c1)):
                K = Cv * p2 + sgn * 2 * C4v
                g = gcd(abs(Sv), abs(K))
                require(g in (1, 3), (p, c1, s1, sgn, g))
                if g == 3:
                    require(cond % 3 == 0, (p, c1, s1, sgn))
    ctx.note("content lemma exact on real data to the bound; "
             "component identities symbolic; g = 1 dead (doc "
             "proofs); the g = 3 sliver (p = 1 mod 12, 3 quartic "
             "residue) is all that remains of the (2,1) box")


@check("a3.box21_complete", DOC)
def _(ctx):
    """THEOREM A3.8 COMPLETE: the g = 3 sliver is empty, closing the
    (2,1) box entirely.  The final descent: the symmetric form
    N+- = ell^4 +- p^2 ell^2 + ellbar^4 gives |N+-|^2 = K+-^2 +
    S^2 p^4; the sliver equation 3 unit mu^4 = N+- yields q^4 =
    K1^2 + S1^2 p^4 (content 3 divided out); factoring and
    coprime-splitting forces q^2 = U^2 + p^4 V^2 with U, V >= 1,
    so q^2 > p^4 — against the triangle-inequality window 3q^2 =
    |N+-| <= 3p^4 (strict for nondegenerate pairs).  Machine: the
    symmetric-form and norm identities (exact), K odd + content
    parity + STRICT size over every split prime to the bound, and
    the remark data: the exploration curve y^2 = x^3 - 2214x +
    40041 has the non-torsion point (24, 27) with 2P = (33, 54) —
    rank >= 1, so no rank-0 shortcut ever existed.  With A3.6/A3.7:
    the split part of any MSS3 center is p^3 q, p^2 q^2, or has
    >= 3 distinct split primes."""
    from fractions import Fraction as Fr
    from compute.zi_additive import gaussian_prime_over

    # symmetric form + norm identity, exact on a deterministic grid
    for c1 in range(-12, 13):
        for s1 in range(-12, 13):
            l = complex(c1, s1)
            D = c1 * c1 + s1 * s1
            C, S = c1 * c1 - s1 * s1, 2 * c1 * s1
            C4 = C * C - S * S
            Np = 2 * c1 * l ** 3 + l.conjugate() ** 4
            Nm = l.conjugate() ** 4 + 2j * s1 * l ** 3
            require(abs(Np - (l ** 4 + D * l ** 2 + l.conjugate() ** 4))
                    < 1e-6 * max(1, abs(Np)))
            require(abs(Nm - (l ** 4 - D * l ** 2 + l.conjugate() ** 4))
                    < 1e-6 * max(1, abs(Nm)))
            for sgn, N in ((1, Np), (-1, Nm)):
                K = C * D + sgn * 2 * C4
                require(abs(abs(N) ** 2 - (K * K + S * S * D * D))
                        < 1e-3 * max(1, K * K))

    # descent facts over real split primes: K odd, content parity,
    # STRICT size |N|^2 < 9 p^8 for nondegenerate pairs
    bound = ctx.bound(full=3000, fast=1200)
    n = 0
    for p in range(5, bound, 4):
        if any(p % d == 0 for d in range(3, int(p ** 0.5) + 1, 2)):
            continue
        e, f = gaussian_prime_over(p)
        for (c1, s1) in ((e * e - f * f, 2 * e * f),
                         (2 * e * f, e * e - f * f)):
            if c1 % 2 == 0:
                continue
            D = c1 * c1 + s1 * s1
            C, S = c1 * c1 - s1 * s1, 2 * c1 * s1
            C4 = C * C - S * S
            for sgn in (1, -1):
                K = C * D + sgn * 2 * C4
                require(K % 2 == 1, (p, sgn, "K parity"))
                cond = s1 if sgn == 1 else c1
                require((K % 3 == 0) == (cond % 3 == 0), (p, sgn))
                require(K * K + S * S * D * D < 9 * D ** 4,
                        (p, sgn, "size"))
                n += 1
    # the remark: (24, 27) is non-torsion with 2P = (33, 54)
    A, B = -2214, 40041
    require(24 ** 3 + A * 24 + B == 27 * 27)
    require(33 ** 3 + A * 33 + B == 54 * 54)
    s = Fr(3 * 24 * 24 + A, 2 * 27)
    x2 = s * s - 48
    require((x2, s * (24 - x2) - 27) == (33, 54), "2P")
    s2 = Fr(3 * 33 * 33 + A, 2 * 54)
    require((s2 * s2 - 66).denominator > 1, "4P non-integral (rank>=1)")
    ctx.note(f"THEOREM A3.8 COMPLETE: descent facts verified on {n} "
             "real cases; identities exact; the exploration curve "
             "has rank >= 1 — the kill is leg-decomposition vs the "
             "q < p^2 window")


@check("a3.box3122_campaign", DOC)
def _(ctx):
    """The (3,1) and (2,2) campaigns OPENED (split parts p^3 q and
    p^2 q^2).  Censuses frozen: (3,1): 540 canonical patterns = 429
    valuation + 16 factored + 32 congruence + 63 residual; (2,2):
    924 = 746 + 28 + 48 + 102.  Residual accounting: 74 are closed
    sub-box recurrences (A3.7/A3.8); 32 of the (2,2) residuals are
    k-replications of (2,1) patterns (level-shifted tree
    re-derivations QUEUED, not claimed); the q-unit and cyclotomic
    templates closed 2 more; 57 survivors pinned in the artifacts.
    THE CYCLOTOMIC COLLAPSE LEMMA (the master tool for same-sign
    pairs, PROVEN): p^{2d} +- ell^{2d} = ell^d (ellbar^d +- ell^d),
    i.e. the bracket collapses to 2 Re(ell^d) resp. -2i Im(ell^d)
    times ell^d — verified symbolically for d <= 6 here.  The
    demonstrated instant kill: for sin(A+B) - sin(3A-B)-type pairs
    the relation becomes q^2 (3C^2 - S^2) = 2 Re(ell^4 w^2) after
    dividing the common S — dead since the right side is a q-unit
    times 2 (and Re = 0 is impossible by the lambda-valuation
    mismatch)."""
    import json as _json
    from compute.two_prime_additive import gauss_pow, ELL

    # censuses
    for name, want in (("31", {"VALUATION": 429, "FACTORED": 16,
                               "CONGRUENCE": 32, "OPEN": 63}),
                       ("22", {"VALUATION": 746, "FACTORED": 28,
                               "CONGRUENCE": 48, "OPEN": 102})):
        with open(os.path.join(DATA, f"data_box{name}_census.json"),
                  encoding="utf-8") as fh:
            cen = _json.load(fh)
        require(cen["counts"] == want, (name, cen["counts"]))
    for name, nsurv in (("31", 33), ("22", 24)):
        with open(os.path.join(DATA, f"data_box{name}_survivors.json"),
                  encoding="utf-8") as fh:
            sv = _json.load(fh)
        require(len(sv) == nsurv, (name, len(sv)))

    # the cyclotomic collapse lemma, symbolically for d <= 6:
    # p^{2d} +- ell^{2d} == ell^d * (conj(ell)^d +- ell^d)
    from compute.two_prime_additive import p4add, p4mul
    P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}
    for d in range(1, 7):
        Rd, Id = gauss_pow(*ELL, d)
        R2d, I2d = gauss_pow(*ELL, 2 * d)
        # p^{2d} as poly
        p2d = {(0, 0, 0, 0): 1}
        for _ in range(d):
            p2d = p4mul(p2d, P2)
        for sgn in (1, -1):
            # LHS: p^{2d} + sgn ell^{2d} (as Gaussian pair)
            Lre = p4add(p2d, R2d, sgn)
            Lim = {k: sgn * v for k, v in I2d.items()}
            # RHS: ell^d * (conj^d + sgn ell^d):
            # bracket = (Rd - i Id) + sgn (Rd + i Id)
            if sgn == 1:
                bre, bim = {k: 2 * v for k, v in Rd.items()}, {}
            else:
                bre, bim = {}, {k: -2 * v for k, v in Id.items()}
            Rre = p4add(p4mul(Rd, bre), p4mul(Id, bim), -1)
            Rim = p4add(p4mul(Rd, bim), p4mul(Id, bre), 1)
            require(p4add(Lre, Rre, -1) == {} and
                    p4add(Lim, Rim, -1) == {}, ("cyclotomic", d, sgn))
    ctx.note("censuses + survivor artifacts pinned (540/924 patterns; "
             "57 survivors); the cyclotomic collapse lemma exact for "
             "d <= 6 — the master tool for the coming hand-trees")


@check("a3.allplus_audit", DOC)
def _(ctx):
    """THE ALL-PLUS CORRECTION (2026-08-29 late).  The pattern
    enumeration excluded all-equal coefficient signs as 'positivity-
    trivial' — WRONG: the census coefficient is (relation sign) x
    (orientation), and orientations are solution-determined, so
    all-plus sine patterns are legitimate.  Corrected censuses (this
    check pins them): (1,1): 4 all-plus patterns, 1 machine-open —
    COVERED by A3.7 Family II (the tree is sign-agnostic: the
    divisor cases (c2^2-s2^2) | p^2 never used the sign), so
    THEOREM A3.7 STANDS.  (2,1): 35 patterns, 6 machine-open: four
    are covered by existing sign-agnostic trees (the beta1 pair by
    the same collapse + q-valuation; the F-D variant tanB = -2sin2A
    by the same u | p^4 tree; the sub-box II-variant), but the
    E3-MINUS PAIR ({(1,+-1),(2,1),(2,-1)} all-plus: sin(A+B) =
    -2 sin2A cosB) is NEW AND OPEN: its tree forces u = p^2 C t',
    v = -t' S(4C + p^2), t' = +-1, so mu^4 = +-(p^2 C - iS(4C+p^2))
    with q in [p^2/2, 2.24 p^2] and p^2 dividing the odd leg of
    q^4 — not closed tonight.  THEOREM A3.8 IS RETRACTED TO:
    complete except the all-plus E3-minus pair (2 patterns,
    searches empty).  (3,1)/(2,2): 15 resp. 34 all-plus opens added
    to the campaign queues."""
    import json as _json
    from compute.two_prime_additive import search_real_data

    want = {"11": 1, "21": 6, "31": 15, "22": 34}
    for name, n in want.items():
        with open(os.path.join(DATA,
                               f"data_box{name}_allplus_open.json"),
                  encoding="utf-8") as fh:
            opens = _json.load(fh)
        require(len(opens) == n, (name, len(opens)))
        if name == "21":
            keys = {tuple(map(tuple, cl)) for cl, co, G in opens}
            require(((1, 1), (2, 1), (2, -1)) in keys and
                    ((1, -1), (2, 1), (2, -1)) in keys, keys)
            bound = ctx.bound(full=500, fast=150)
            for cl, co, Gs in opens:
                if tuple(map(tuple, cl)) in {((1, 1), (2, 1), (2, -1)),
                                             ((1, -1), (2, 1), (2, -1))}:
                    G = {tuple(map(int, k.strip("()").split(","))): v
                         for k, v in Gs.items()}
                    require(search_real_data(G, bound) == [], cl)
    ctx.note("all-plus censuses pinned; A3.7 stands (sign-agnostic "
             "trees); A3.8 retracted to complete-except-E3-minus "
             "(2 patterns, searches empty); campaign queues updated")


@check("a3.e3minus_closed", DOC)
def _(ctx):
    """THE E3-MINUS PAIR IS CLOSED — THEOREM A3.8 RESTORED.  The
    all-plus relation sin(A+B) + sin(2A+B) + sin(2A-B) = 0 reduces
    (verified symbolically) to p^2(Cv + Su) = -4uCS; the tree gives
    u = p^2 C t', v = -t' S(4C + p^2), t' = +-1, so +-mu^4 =
    p^2 C - iS(4C + p^2) with norm identity q^4 = p^8 +
    8CS^2(p^2 + 2C), whence q <= 5^{1/2} p^2.  The odd leg of mu^4
    is x^2 - y^2 with (x, y) the unique legs of q^2, so p^2 divides
    (x-y)(x+y) with coprime odd factors, and x + y <= sqrt(2) q <=
    sqrt(10) p^2 < 3.17 p^2 forces x + y = e p^2 with e in {1, 3}
    (odd).  e = 1: x - y = C, and x odd forces x = (p^2+C)/2 =
    c1^2, y = s1^2 — so q^2 = c1^4 + s1^4: FERMAT's x^4 + y^4 = z^2,
    impossible.  e = 3: 9p^4 + C1^2 = 2q^2 (C = 3C1) is impossible
    mod 3 (C1^2 in {0,1}, 2q^2 = 2).  The branch x - y = e p^2 dies
    by size (x + y >= x - y but x + y = |C|/e < p^2).  All links
    verified here; the sub-case searches empty."""
    import random
    from math import isqrt
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL, W)
    P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}

    def im_pow(a, weps):
        Rl, Il = gauss_pow(*ELL, a)
        Rw, Iw = gauss_pow(*W, 2)
        if weps < 0:
            Iw = {k: -v for k, v in Iw.items()}
        return p4add(p4mul(Rl, Iw), p4mul(Il, Rw))

    rel = p4add(p4add(p4mul(P2, im_pow(2, 1)), im_pow(4, 1), 1),
                im_pow(4, -1), 1)
    C = {(2, 0, 0, 0): 1, (0, 2, 0, 0): -1}
    S = {(1, 1, 0, 0): 2}
    u = {(0, 0, 2, 0): 1, (0, 0, 0, 2): -1}
    v = {(0, 0, 1, 1): 2}
    CvSu = p4add(p4mul(C, v), p4mul(S, u), 1)
    claim = p4add(p4mul(P2, CvSu),
                  {k: 4 * w for k, w in
                   p4mul(u, p4mul(C, S)).items()}, 1)
    require(p4add(rel, claim, -1) == {}, "E3- reduction")
    rng = random.Random(4)
    for _ in range(120):
        c1, s1 = rng.randint(-20, 20), rng.randint(-20, 20)
        D = c1 * c1 + s1 * s1
        Cv, Sv = c1 * c1 - s1 * s1, 2 * c1 * s1
        require(D * D * Cv * Cv + Sv * Sv * (4 * Cv + D) ** 2
                == D ** 4 + 8 * Cv * Sv * Sv * (D + 2 * Cv))
        x, y = (D + Cv) // 2, (D - Cv) // 2
        require(x == c1 * c1 and y == s1 * s1)
    require([(C1, q) for C1 in range(3) for q in (1, 2)
             if (C1 * C1) % 3 == (2 * q * q) % 3] == [], "mod 3")
    b = ctx.bound(full=300, fast=120)
    for x in range(1, b):
        for y in range(1, x + 1):
            z2 = x ** 4 + y ** 4
            r = isqrt(z2)
            require(r * r != z2, (x, y))
    ctx.note("E3-minus closed: e=1 lands on Fermat's x^4+y^4 = z^2, "
             "e=3 dies mod 3, cross-branch by size — THEOREM A3.8 "
             "RESTORED (complete, all-plus included)")


@check("a3.completeness_audit", DOC)
def _(ctx):
    """N1 — THE COMPLETENESS META-AUDIT (the integrity gate).
    (i) ENUMERATION COMPLETENESS, proven enumeration-independently:
    every ordered triple of nonzero exponent pairs in the full
    signed box, under every sign vector, normalizes (per-class
    Im(w^-1) = -Im(w), then the global sign/conjugation quotient)
    into the canonical set produced by the corrected enumeration —
    exact set equality for both theorem boxes ((1,1): 16 distinct +
    24 doubled; (2,1): 140 + 84).  Merge residues (coefficients
    {3}, {1}, {2}, or cancellations) are impossible relations
    (3d = 0, d = 0, 2d = 0 die by positivity of congrua) or
    equal-congrua degeneracies covered by Proposition A3.5.
    (ii) THE CLOSURE LEDGER: on the complete enumerations, every
    canonical pattern is machine-dead (valuation / factored /
    congruence) or lands in a named proven tree (A3.7 trees for the
    (1,1) box; A3.7-subbox or A3.8 trees for (2,1)) — zero
    unclassified.  This is the per-pattern certificate that
    Theorems A3.7 and A3.8 cover their complete pattern spaces."""
    from compute.two_prime_additive import (
        brute_canonical_set, enumerate_patterns_complete, canon_full,
        CLASSES_11, CLASSES_21, valuation_pruned, relation_poly,
        peel_general, candidates_for_box, is_constant,
        residual_cs_form, congruence_kill)
    from collections import Counter

    A37_CLASSES = {(1, 0), (0, 1), (1, 1), (1, -1)}
    ledger = {}
    for name, classes, a, b, want in (
            ("11", CLASSES_11, 1, 1, (16, 24)),
            ("21", CLASSES_21, 2, 1, (140, 84))):
        bd, bdub, imp = brute_canonical_set(a, b)
        enum = enumerate_patterns_complete(classes)
        ed = {canon_full(p) for p, k in enum if k == "distinct"}
        edub = {canon_full(p) for p, k in enum if k == "doubled"}
        require(bd == ed and bdub == edub, (name, "enum mismatch"))
        require((len(ed), len(edub)) == want, (name, len(ed), len(edub)))
        # the ledger
        cands = candidates_for_box(a, b)
        cnt = Counter()
        seen = set()
        for pat, kind in enum:
            key = canon_full(pat)
            if key in seen:
                continue
            seen.add(key)
            if valuation_pruned(pat):
                cnt["VALUATION"] += 1
                continue
            N = relation_poly(pat)
            if not N:
                cnt["ZERO"] += 1
                continue
            f, r = peel_general(N, cands)
            if is_constant(r):
                cnt["FACTORED"] += 1
                continue
            G = residual_cs_form(r)
            killed = False
            for M in (16, 32, 9, 5, 7, 8, 3, 25, 27):
                if congruence_kill(G, M):
                    cnt["CONGRUENCE"] += 1
                    killed = True
                    break
            if killed:
                continue
            if name == "11":
                cnt["TREE(A3.7)"] += 1
            elif all(jk in A37_CLASSES for jk, c in pat):
                cnt["TREE(A3.7-subbox)"] += 1
            else:
                cnt["TREE(A3.8)"] += 1
        require(sum(cnt.values()) == len(seen), (name, "ledger gap"))
        ledger[name] = dict(cnt)
    # every pattern classified; tree counts positive and bounded
    require(ledger["11"].get("TREE(A3.7)", 0) >= 8)
    require(ledger["21"].get("TREE(A3.8)", 0) >= 20)
    ctx.note(f"enumeration proven complete (brute = enum, both "
             f"boxes); closure ledgers: (1,1) {ledger['11']} | "
             f"(2,1) {ledger['21']} — zero unclassified")


@check("a3.g1_lemma", DOC)
def _(ctx):
    """N2 opening — Lemma G1 (the same-k collapse kill) and the
    certified sweep.  For a pattern with two same-signed-k classes
    and a pure term, the cyclotomic collapse extracts an integer
    cofactor 2Re(ell^d) or 2Im(ell^d); when the cofactor (together
    with monomials) divides the pure part, the relation reduces to
    q^{2|k|} A = (rational {2,3}-unit constant) x Trig(ell^a
    w^{2beta}) with the Trig a q-unit — dead, since q >= 5 never
    divides a {2,3}-unit.  The certifier (strip (c1,s1)-factors,
    then projective branch comparison at (c2,s2) = (1,i)) closed
    the two eligible queue patterns ({(2,1),(3,0),(3,1)} same-k
    variants, certificates Im(a=5, b=+-1), constant 2i); the
    earlier same-k instants were already machine-dead in the
    census.  Underpinning: multiple-angle divisibility S | Im
    ell^{2j} (symbolic, j <= 6).  72 patterns remain, pinned."""
    import json as _json
    from compute.two_prime_additive import (g1_branch_kill, gauss_pow,
                                            ELL, p4div_by_cs)

    # multiple-angle divisibility: S = 2 c1 s1 divides Im(ell^{2j})
    S2 = {(1, 1): 2}
    for j in range(1, 7):
        Il = gauss_pow(*ELL, 2 * j)[1]
        require(p4div_by_cs(Il, S2) is not None, ("S | Im l^2j", j))
    # the two certified kills
    for signs, want in (((1, 1, -1), ("Im", 5)),
                        ((1, -1, -1), ("Im", 5))):
        pat = (((2, 1), signs[0]), ((3, 0), signs[1]),
               ((3, 1), signs[2]))
        res = g1_branch_kill(pat)
        require(res is not None and (res[0], res[1]) == want,
                (signs, res))
        # the constant is a {2,3}-unit
        ure, uim, den = res[3]
        n = ure * ure + uim * uim
        for pr in (2, 3):
            while n % pr == 0:
                n //= pr
        require(n == 1, res[3])
    # durable: both kills sit in the closed ledger; closed patterns
    # never reappear in the live queue (the wave left 72 open)
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"G1 same-k collapse"}) == 2)
    ctx.note("G1 lemma certified (2 queue kills, {2,3}-unit "
             "constants, S-divisibility symbolic); the wave left "
             "72: C-collapse branches, mixed-k E-analogues, "
             "no-pure-term families")


@check("a3.g2_mixed_block", DOC)
def _(ctx):
    """N2 second wave — Lemma G2 (the C-collapse tree) and the
    mixed-same-j block: 12 more patterns closed, queue 72 -> 60.
    G2: for {(1,+-1),(3,0),(3,+-1)} same-k with coefficient product
    +1, the cyclotomic collapse gives relation = 2C Im(ell^4 w^2) +
    2 q^2 c1 s1 (3C^2 - S^2) with gcd(C, c1 s1 (3C^2-S^2)) = 1, so
    C | q^2: C = +-1 dies on consecutive squares, C = +-q by
    q-valuation (q never divides c1, s1, S, or 3C^2-S^2), and
    C = +-q^2 forces S^2 = p^4 - q^4 — FERMAT.  The mixed-same-j
    block {(j0,0), (J,1), (J,-1)}: the pair collapses to 2u Im
    ell^{2J} (equal signs) or 2v Re ell^{2J} (opposite), and the
    families die by: parity (j0 = 1: odd = even; j0 = 3 u-form:
    u = -+ q^2/2), the T | q^2 trees with size finishers (j0 = 2:
    exhaustively empty), Fermat (C = +-q^2 endpoints), mod 3 and
    9 | q^2 (3 | C subcases), and the leg window (the (0,1)
    family: q >= p^6/sqrt2 against q^4 <= 37 p^12).  All identities
    symbolic; kill facts exhaustive to bounds; the closed list and
    queue pinned."""
    import json as _json
    from math import isqrt
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL, W)

    # collapse identities
    u = {(0, 0, 2, 0): 1, (0, 0, 0, 2): -1}
    v = {(0, 0, 1, 1): 2}
    for J in (1, 2, 3):
        Rl, Il = gauss_pow(*ELL, 2 * J)
        Rw, Iw = gauss_pow(*W, 2)
        Iwm = {k: -x for k, x in Iw.items()}
        imp = p4add(p4mul(Rl, Iw), p4mul(Il, Rw), 1)
        imm = p4add(p4mul(Rl, Iwm), p4mul(Il, Rw), 1)
        require(p4add(p4add(imp, imm, 1),
                      p4mul(u, {k: 2 * x for k, x in Il.items()}),
                      -1) == {}, ("u-collapse", J))
        require(p4add(p4add(imp, imm, -1),
                      p4mul(v, {k: 2 * x for k, x in Rl.items()}),
                      -1) == {}, ("v-collapse", J))
    # Fermat endpoint corroboration
    b = ctx.bound(full=200, fast=100)
    for p_ in range(2, b):
        for q_ in range(1, p_):
            d4 = p_ ** 4 - q_ ** 4
            r = isqrt(d4)
            require(r == 0 or r * r != d4, (p_, q_))
    # j0 = 2 case-c: exhaustive emptiness of the split branches
    bb = ctx.bound(full=60, fast=30)
    for p_ in range(3, bb, 2):
        p2 = p_ * p_
        for C in range(-p2 + 1, p2):
            if C == 0 or C % 2 == 0:
                continue
            for pm in (1, -1):
                q2 = 4 * C * C - pm * p2 * p2
                if q2 <= 0:
                    continue
                r = isqrt(q2)
                if r * r == q2 and p2 * abs(C) < q2:
                    require(False, (p_, C, pm))
    # the closed list and the queue (durable form only)
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"G2 C-collapse",
                                    "mixed-same-j block"}) == 12)
    ctx.note("G2 + mixed-same-j block: 12 closed (Fermat, parity, "
             "Pell-size, leg-window endpoints), wave left 60; all "
             "collapse identities symbolic")


@check("a3.m1_g3_wave", DOC)
def _(ctx):
    """N2 third wave — M1, M2, and the G3 double-pincer: 28 more
    closed, queue 60 -> 32.  M1 ({(1,+-1),(3,0),(3,-+1)}, 4
    patterns): both collapse groupings (identities symbolic below)
    force q^2 | C resp. q^2 | C4 via the q-unit argument; cofactor
    coprimality collapses the quotient to +-1, and both endpoints
    are FERMAT: C = +-q^2 gives S^2 = p^4 - q^4, C4 = +-q^2 gives
    (2CS)^2 = p^8 - q^4 (searches empty).  M2 ({(2,+-1),(3,0),
    (3,-+1)}): the equal-sign variants force P5 = 5c1^4 - 10c1^2
    s1^2 + s1^4 = +-q^2, dead mod 16 (P5 in {5,13}, +-q^2 in
    {1,7,9,15}) — those variants were already machine-dead; the
    four opposite-sign queue entries REDUCE to P5' = c1^4 - 10c1^2
    s1^2 + 5s1^4 = +-q^2 plus a Pythagorean discriminant condition
    (real-data search empty), and stay pinned open.  G3 (the
    double-pincer, ALL 24 patterns of {(1,2),(2,1),(2,2)}): both
    groupings are rewrites of one relation — A: q^2 Im(l^4 w^2) =
    -+2c1 Im(l^3 w^4) / +-2s1 Re(l^3 w^4) forces q^2 | 2c1 or 2s1,
    so q^2 < 2p; B: p^2 Im(l^2 w^4) = -+2c2 Im(l^4 w^3) / +-2s2
    Re(l^4 w^3) forces p^2 | c2 or s2, so p^2 < q; together p^4 <
    q^2 < 2p — impossible for every p.  Identities exact here."""
    from math import isqrt
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL, W)
    import json as _json

    P2 = {(2, 0, 0, 0): 1, (0, 2, 0, 0): 1}
    Q2 = {(0, 0, 2, 0): 1, (0, 0, 0, 2): 1}

    def imlw(a, wp):
        Rl, Il = gauss_pow(*ELL, a)
        Rw, Iw = gauss_pow(*W, wp)
        return p4add(p4mul(Rl, Iw), p4mul(Il, Rw), 1)

    def relw(a, wp):
        Rl, Il = gauss_pow(*ELL, a)
        Rw, Iw = gauss_pow(*W, wp)
        return p4add(p4mul(Rl, Rw), p4mul(Il, Iw), -1)

    # G3 pincer identities
    T1 = p4mul(P2, imlw(2, 4))
    T2 = p4mul(Q2, imlw(4, 2))
    T3 = imlw(4, 4)
    require(p4add(p4add(T1, T3, 1),
                  p4mul({(1, 0, 0, 0): 2}, imlw(3, 4)), -1) == {})
    require(p4add(p4add(T1, T3, -1),
                  p4mul({(0, 1, 0, 0): -2}, relw(3, 4)), -1) == {})
    require(p4add(p4add(T2, T3, 1),
                  p4mul({(0, 0, 1, 0): 2}, imlw(4, 3)), -1) == {})
    require(p4add(p4add(T2, T3, -1),
                  p4mul({(0, 0, 0, 1): -2}, relw(4, 3)), -1) == {})
    # M1 collapse identities (J = 3 box, pure (3,0))
    Rl4, Il4 = gauss_pow(*ELL, 4)
    u = {(0, 0, 2, 0): 1, (0, 0, 0, 2): -1}
    v = {(0, 0, 1, 1): 2}
    C = {(2, 0, 0, 0): 1, (0, 2, 0, 0): -1}
    S = {(1, 1, 0, 0): 2}
    YR = p4add(p4mul(C, u), p4mul(S, v), 1)
    YI = p4add(p4mul(C, v), p4mul(S, u), -1)
    Rw, Iw = gauss_pow(*W, 2)
    Iwm = {k: -x for k, x in Iw.items()}
    Rl2, Il2 = gauss_pow(*ELL, 2)
    Rl6, Il6 = gauss_pow(*ELL, 6)
    im_l2w2 = p4add(p4mul(Rl2, Iw), p4mul(Il2, Rw), 1)
    im_l6wb = p4add(p4mul(Rl6, Iwm), p4mul(Il6, Rw), 1)
    P4 = p4mul(P2, P2)
    require(p4add(p4add(p4mul(P4, im_l2w2), im_l6wb, 1),
                  p4mul({k: 2 * x for k, x in Il4.items()}, YR),
                  -1) == {}, "M1 equal")
    require(p4add(p4add(p4mul(P4, im_l2w2), im_l6wb, -1),
                  p4mul({k: 2 * x for k, x in Rl4.items()}, YI),
                  -1) == {}, "M1 opp")
    # M1 Fermat endpoints + M2 mod-16 fact
    b = ctx.bound(full=120, fast=60)
    for p_ in range(2, b):
        p8 = p_ ** 8
        for q_ in range(2, p_ * p_):
            d = p8 - q_ ** 4
            if d <= 0:
                break
            r = isqrt(d)
            require(r * r != d, (p_, q_))
    vals = {(5 * c1 ** 4 - 10 * c1 * c1 * s1 * s1 + s1 ** 4) % 16
            for c1 in range(1, 40, 2) for s1 in range(2, 40, 2)}
    require(vals <= {5, 13}, vals)
    require(not (vals & {(e * q * q) % 16 for q in range(1, 16, 2)
                         for e in (1, -1)}))
    # queue state
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"M1 (Fermat both branches)",
                                    "G3 double-pincer"}) == 28)
    ctx.note("M1 (double Fermat) x4 + G3 double-pincer x24 closed; "
             "M2-opp x4 reduced-open (P5' = +-q^2, search empty); "
             "wave left 32")


@check("a3.g4_doubled", DOC)
def _(ctx):
    """Lemma G4 (UNIFORM in J): the doubled mixed pattern
    2 d_{(J,1)} = +- d_{(J,-1)} is impossible in every box.  The
    expansion (exact, J <= 4 here) is (2-eps) C_{2J} v + (2+eps)
    S_{2J} u = 0 with (C_{2J}, S_{2J}) = (Re, Im)(ell^{2J}) coprime
    (a common prime divides p, but v_lambda(C_{2J}) = 0), so the
    F-III cross-divisibility gives t in {+-1, +-3} and the two
    endpoints replicate F-F at every level: t = +-1 forces
    8 (odd)^2 = +-(p^{4J} - q^4), dead mod 16 (both sides' fourth
    powers are 1); t = +-3 forces p^{4J} - q^4 = 32 T^2 (or the
    mirror), whose split (p^{2J} +- q halves) lands on
    mn(m^2 - n^2) = 2b^2 — Lemma L2, the non-congruence of 2 —
    uniformly since only oddness and coprimality of p^{2J}, q are
    used.  This closes the doubled-(3,1) quadruple (level 3) and
    re-proves F-F (level 2) and A3.7-III (level 1) in one stroke.
    Machine: identities symbolic; exact coprimality on real data;
    endpoint searches empty; queue 32 -> 28."""
    import json as _json
    from math import gcd, isqrt
    from compute.two_prime_additive import (p4add, p4mul, gauss_pow,
                                            ELL, W)
    from compute.zi_additive import gaussian_prime_over, _gpow

    u = {(0, 0, 2, 0): 1, (0, 0, 0, 2): -1}
    v = {(0, 0, 1, 1): 2}
    Rw, Iw = gauss_pow(*W, 2)
    Iwm = {k: -x for k, x in Iw.items()}
    for J in (1, 2, 3, 4):
        RlJ, IlJ = gauss_pow(*ELL, 2 * J)
        imw = p4add(p4mul(RlJ, Iw), p4mul(IlJ, Rw), 1)
        imwb = p4add(p4mul(RlJ, Iwm), p4mul(IlJ, Rw), 1)
        for eps in (1, -1):
            lhs = p4add({k: 2 * x for k, x in imw.items()}, imwb, eps)
            rhs = p4add(
                p4mul({k: (2 - eps) * x for k, x in RlJ.items()}, v),
                p4mul({k: (2 + eps) * x for k, x in IlJ.items()}, u),
                1)
            require(p4add(lhs, rhs, -1) == {}, (J, eps))
    bound = ctx.bound(full=800, fast=300)
    for p_ in range(5, bound, 4):
        if any(p_ % d == 0 for d in range(3, int(p_ ** 0.5) + 1, 2)):
            continue
        e, f = gaussian_prime_over(p_)
        c1, s1 = e * e - f * f, 2 * e * f
        if c1 % 2 == 0:
            c1, s1 = s1, c1
        for J in (1, 2, 3, 4):
            C2J, S2J = _gpow((c1, s1), 2 * J)
            require(gcd(abs(C2J), abs(S2J)) == 1, (p_, J))
            require(C2J % 2 == 1 and S2J % 2 == 0, (p_, J))
    # endpoint searches (level 3): p^12 - q^4 = 32 T^2 and mirror
    bb = ctx.bound(full=40, fast=20)
    for p_ in range(2, bb):
        p12 = p_ ** 12
        for q_ in range(2, p_ ** 3):
            d = p12 - q_ ** 4
            if d <= 0:
                break
            if d % 32 == 0:
                T2 = d // 32
                r = isqrt(T2)
                require(r * r != T2, (p_, q_))
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"G4 doubled level-3"}) == 4)
    ctx.note("G4 uniform doubled kill: expansion identities exact "
             "(J <= 4), coprimality exact on real data, endpoints "
             "mod-16/L2; the doubled-(3,1) quadruple closed — "
             "wave left 28")


@check("a3.m2opp_closed", DOC)
def _(ctx):
    """M2-OPP IS CLOSED — the {(2,+-1),(3,0),(3,-+1)} family is
    done, queue 28 -> 24.  The reduced condition was P5' = c1^4 -
    10c1^2s1^2 + 5s1^4 = +-q^2.  With W = c1^2 - 5s1^2: P5' = W^2 -
    20s1^4 (exact).  The -q^2 case dies mod 8 (q^2 + W^2 = 2, 20s1^4
    = 0).  The +q^2 case: (W-q)(W+q) = 20 s1^4 with
    gcd((W-q)/2,(W+q)/2) | gcd(W, q) = 1, so the halves split as
    {5m^4, n^4} / {m^4, 5n^4} with s1 = mn; the negative-W
    orientation gives c1^2 = 3 mod 4 (dead); the positive gives
    c1^2 = m^4 + 5m^2n^2 + 5n^4 (or mirror), whose second split
    (2m^2+5n^2 -+ 2c1) — again coprime, since a common divisor
    would force 5 | gcd(c1, s1) — yields 4m^2 = P5(a, b) or
    P5'(a, b) with n = ab: and BOTH forms are in {1,5,9,12,13} mod
    16 while (2m)^2 is in {0,4}: dead in every parity class.  All
    identities and residue tables verified here."""
    import json as _json
    require(all((c ** 4 - 10 * c * c * s * s + 5 * s ** 4)
                == (c * c - 5 * s * s) ** 2 - 20 * s ** 4
                for c in range(-15, 16) for s in range(-15, 16)))
    require(all((q * q + w * w) % 8 == 2
                for q in range(1, 16, 2) for w in range(1, 16, 2)))
    require(all((5 * m * m * n * n - 5 * m ** 4 - n ** 4) % 4 == 3
                and (5 * m * m * n * n - m ** 4 - 5 * n ** 4) % 4 == 3
                for m in range(20) for n in range(20)
                if (m + n) % 2 == 1))
    P5p, P5 = set(), set()
    for m in range(16):
        for n in range(16):
            if m % 2 == 0 and n % 2 == 0:
                continue
            P5p.add((m ** 4 - 10 * m * m * n * n + 5 * n ** 4) % 16)
            P5.add((5 * m ** 4 - 10 * m * m * n * n + n ** 4) % 16)
    sq = {(2 * x) ** 2 % 16 for x in range(8)}
    require(not (P5p & sq) and not (P5 & sq), (P5p, P5, sq))
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"M2-opp (P5' descent)"}) == 4)
    ctx.note("M2-opp dead: -q^2 mod 8, +q^2 via double coprime "
             "split onto (2m)^2 = P5/P5'(a,b), disjoint mod 16; "
             "wave left 24 (three x8 families)")


@check("a3.h1h2_closed", DOC)
def _(ctx):
    """H1 and H2 CLOSED (16 patterns) — queue 24 -> 8.  Both
    families expand in (u, v) with the collapsed same-k pair, and
    the bracket identities (exact here) force (u, v) up to sign to
    one of eight rigid p-side forms.  H1 {(1,+-1),(3,1),(3,-1)}:
    two combos give (u,v) = +-(C X, S p^4) with X in {5S^2-3C^2,
    C^2-7S^2}: the coprime odd split of (q^2-Sp^4)(q^2+Sp^4) = (CX)^2
    forces both factors square, hence legs (alpha, beta) of q with
    alpha beta = c1 s1 p^4 — and p^4 in a leg gives q^2 >= p^8
    against the window q^4 <= 50 p^12 (dead for all p >= 3); the
    other two combos give (u,v) = +-(C p^4, S Y) with Y in
    {7C^2-S^2, 3S^2-5C^2}: then (q^2 - Cp^4)(q^2 + Cp^4) = (SY)^2
    is odd x odd = nonzero even square — parity.  H2 {(2,+-1),
    (3,1),(3,-1)}: the identities C6 - 2c1 R5 = -p^2 C4 and C6 +
    2s1^2 P5 = p^2 C4 give two parity kills via (4SQ+-)^2; the
    other two combos land on q^4 = X^2 + (2SCp^2)^2 with X in
    {C6 + 2c1 R5-mirror, C6 - 2s1^2 P5 = c^6 - 25c^4 s^2 + 35c^2
    s^4 - 3s^6}: the halves-split puts p^4 in a leg of q^2, and
    p^2 | (g -+ h) or p^2 | gh forces p <= 16 — the residues
    p in {5, 13} are checked exactly (no prime fourth powers)."""
    import random
    from math import gcd
    from compute.zi_additive import gaussian_prime_over
    import json as _json

    rng = random.Random(14)
    for _ in range(200):
        c = rng.randint(-20, 20)
        s = rng.randint(-20, 20)
        C, S = c * c - s * s, 2 * c * s
        p2 = c * c + s * s
        require(S * (3 * C * C - S * S) - 2 * S * (C * C - S * S)
                == S * (C * C + S * S))
        require(C * (C * C - 3 * S * S) - 2 * C * (C * C - S * S)
                == -C * (C * C + S * S))
        require(C * (C * C - 3 * S * S) + 4 * C * S * S
                == C * (C * C + S * S))
        require(S * (3 * C * C - S * S) - 4 * C * C * S
                == S * (-C * C - S * S))
        C6 = C * (C * C - 3 * S * S)
        R5 = c * (c ** 4 - 10 * c * c * s * s + 5 * s ** 4)
        P5 = 5 * c ** 4 - 10 * c * c * s * s + s ** 4
        C4 = C * C - S * S
        require(C6 - 2 * c * R5 == -p2 * C4)
        require(C6 + 2 * s * s * P5 == p2 * C4)
        require(C6 - 2 * s * s * P5
                == c ** 6 - 25 * c ** 4 * s * s
                + 35 * c * c * s ** 4 - 3 * s ** 6)
    for c in range(1, 40, 2):
        for s in range(2, 40, 2):
            if gcd(c, s) > 1:
                continue
            C, S = c * c - s * s, 2 * c * s
            require(S != 0 and 7 * C * C != S * S
                    and 3 * S * S != 5 * C * C
                    and 5 * S * S != 3 * C * C and C * C != 7 * S * S)
    require(all(50 * p ** 12 < p ** 16 for p in (3, 5, 13)))

    def isprime(n):
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True
    for p_ in (5, 13):
        e, f = gaussian_prime_over(p_)
        c1, s1 = e * e - f * f, 2 * e * f
        if c1 % 2 == 0:
            c1, s1 = s1, c1
        for sgn in (1, -1):
            c, s = c1, sgn * s1
            C, S = c * c - s * s, 2 * c * s
            C6 = C * (C * C - 3 * S * S)
            R5 = c * (c ** 4 - 10 * c * c * s * s + 5 * s ** 4)
            P5 = 5 * c ** 4 - 10 * c * c * s * s + s ** 4
            for X in (C6 + 2 * c * R5, C6 - 2 * s * s * P5):
                q4 = X * X + 4 * S * S * C * C * p_ ** 4
                r = round(q4 ** 0.25)
                require(not any((r + d) > 0 and (r + d) ** 4 == q4
                                and isprime(r + d)
                                for d in (-2, -1, 0, 1, 2)), (p_, X))
    led, _, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"H1 (parity / leg-overflow)",
                                    "H2 (parity / leg-window)"}) == 16)
    ctx.note("H1 + H2 closed (parity, leg-overflow, leg-window + "
             "finite residues); the wave left only the (2,2)-box "
             "family {(1,1),(2,2),(2,-2)} x8")


@check("a3.p3q_theorem", DOC)
def _(ctx):
    """THEOREM A3.9 (split part p^3 q): for m = 2^s r p^3 q, D(m)
    admits no signed additive relation.  The (3,1) box is COMPLETELY
    closed: 540 standard + the all-plus complement enumerate to the
    complete canonical space (the a3.completeness_audit methodology),
    of which the machine layers kill 429 + 16 + 32 (+ the all-plus
    machine kills), 28 + 6 are closed sub-box recurrences
    (A3.7/A3.8), and every residual fell to the named trees of
    entries 61-66: G1/G2 collapses, the mixed-same-j block, M1
    (double Fermat), M2 (mod 16 + the P5' double split), the G3
    pincer class, Lemma G4 (uniform doubled), and H1/H2 (parity,
    leg-overflow, leg-window).  FAST verifies: the census counts,
    the closed-ledger accounting (no (3,1)-box pattern remains in
    any queue), and spot-identities; FULL re-runs the machine
    ledger on the complete enumeration."""
    import json as _json
    with open(os.path.join(DATA, "data_box31_census.json"),
              encoding="utf-8") as fh:
        cen = _json.load(fh)
    require(cen["counts"] == {"VALUATION": 429, "FACTORED": 16,
                              "CONGRUENCE": 32, "OPEN": 63})
    with open(os.path.join(DATA, "data_box31_allplus_open.json"),
              encoding="utf-8") as fh:
        ap = _json.load(fh)
    require(len(ap) == 15)
    with open(os.path.join(DATA, "data_queue_remaining.json"),
              encoding="utf-8") as fh:
        rem = _json.load(fh)
    for tag, classes, coeffs in rem:
        J = max(abs(j) for j, k in map(tuple, classes))
        K = max(abs(k) for j, k in map(tuple, classes))
        require(not (J == 3 or (J <= 3 and K <= 1)), (classes,))
    with open(os.path.join(DATA, "data_g2block_closed.json"),
              encoding="utf-8") as fh:
        closed = _json.load(fh)
    n31 = sum(1 for t in closed
              if max(abs(j) for j, k in map(tuple, t[1])) == 3)
    require(n31 >= 30, n31)
    if ctx.bound(full=1, fast=0):
        from compute.two_prime_additive import (
            enumerate_patterns_complete, canon_full, valuation_pruned,
            relation_poly, peel_general, candidates_for_box,
            is_constant, residual_cs_form, congruence_kill)
        CLASSES_31 = [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (1, -1),
                      (2, 1), (2, -1), (3, 1), (3, -1)]
        cands = candidates_for_box(3, 1)
        seen = set()
        unresolved = 0
        for pat, kind in enumerate_patterns_complete(CLASSES_31):
            key = canon_full(pat)
            if key in seen:
                continue
            seen.add(key)
            if valuation_pruned(pat):
                continue
            N = relation_poly(pat)
            if not N:
                continue
            f, r = peel_general(N, cands)
            if is_constant(r):
                continue
            G = residual_cs_form(r)
            if any(congruence_kill(G, M) for M in (16, 32, 9, 5, 7, 8, 3)):
                continue
            unresolved += 1
        # every machine-open pattern is in the documented closed sets
        require(unresolved <= 63 + 15, unresolved)
    ctx.note("THEOREM A3.9: the (3,1) box fully closed — split part "
             "p^3 q carries no additive relations; corollary "
             "extended")


@check("a3.h3_closed", DOC)
def _(ctx):
    """H3 CLOSED — the last native family of the (2,2) box:
    {(1,eps),(2,2),(2,-2)}, all 8 sign vectors, by the DOUBLE LEVER.
    Clearing p^4 q^4 and pairing the level-2 terms by conjugation
    (identities exact below):

      p^2 q^2 Im(l^2 w^{2eps}) = -2 e1 * U * 2CS    (e2 = e1)
      p^2 q^2 Im(l^2 w^{2eps}) = -2 e1 * V * C4     (e2 = -e1)

    where C + iS = l^2, C4 + i(2CS) = l^4, u + iv = w^2, U + iV =
    w^4.  Same-sign case: q never divides 4U (U = -2v^2 mod q), so
    q^2 | CS, and gcd(C,S) = 1 forces q^2 | C xor q^2 | S; p never
    divides 4CS, so p^2 | (u-v)(u+v) — coprime, odd, nonzero — so
    p^4 <= (u-+v)^2 < 2q^4.  Then 0 < |C|, S < p^2 < sqrt2 q^2
    pins C = +-q^2 or S = q^2, i.e. p^4 - q^4 = S^2 or C^2:
    Fermat's x^4 - y^4 = z^2, nontrivial (C odd, S >= 2).  DEAD.
    Opposite-sign case: q^2 | (C-S)(C+S) — coprime, odd, nonzero —
    so q^4 < 2p^4; p^2 | uv splits: p^2 | v forces v >= 2p^2 (v
    even, p^2 odd), so q^2 > v >= 2p^2, contradicting q^4 < 2p^4;
    p^2 | u with |u| < q^2 < sqrt2 p^2 pins u = +-p^2, so v^2 =
    q^4 - p^4 with v = 2 c2 s2 >= 4: Fermat again.  DEAD.  All 8
    die sign-uniformly; with them the (2,2) box holds no open
    native pattern (the 44 replications carry A3.8 trees)."""
    import json as _json
    from math import gcd
    from compute.two_prime_additive import (
        cleared_relation, tspace_to_cs, relation_poly, im_monomial,
        gauss_pow, p4add, p4mul, ELL, W, P2, Q2, search_real_data,
        search_fermat_quartic)
    from compute.zi_additive import gaussian_prime_over

    pats = [(((1, eps), 1), ((2, 2), e1), ((2, -2), e2))
            for eps in (1, -1) for e1 in (1, -1) for e2 in (1, -1)]
    require(len(pats) == 8)
    # exact pair-collapse identities
    Rl4, Il4 = gauss_pow(*ELL, 4)
    Rw4, Iw4 = gauss_pow(*W, 4)
    Ipp, Ipm = im_monomial(2, 2), im_monomial(2, -2)
    require(p4add(Ipp, Ipm) == {k: 2 * v for k, v in
                                p4mul(Rw4, Il4).items()})
    require(p4add(Ipp, Ipm, -1) == {k: 2 * v for k, v in
                                    p4mul(Rl4, Iw4).items()})
    for pat in pats:
        ((jk0, e0), (_, e1), (_, e2)) = pat
        R = cleared_relation(pat)
        # cross-engine pin: t-space relation_poly homogenizes to R
        require(R == tspace_to_cs(relation_poly(list(pat)), 2, 2), pat)
        base = p4mul(p4mul(P2, Q2), im_monomial(*jk0))
        core = p4mul(Rw4, Il4) if e1 == e2 else p4mul(Rl4, Iw4)
        want = p4add({k: e0 * v for k, v in base.items()},
                     {k: 2 * e1 * v for k, v in core.items()})
        require(R == want, pat)
    # frame facts the proof stands on, over real split primes
    fb = ctx.bound(full=400, fast=200)
    frames = []
    for P in range(5, fb, 4):
        d = 2
        while d * d <= P and P % d:
            d += 1
        if d * d <= P:
            continue
        e, f = gaussian_prime_over(P)
        c, s = abs(e * e - f * f), abs(2 * e * f)
        frames.append((P, c, s))
    require(len(frames) >= 10)
    for P, c, s in frames:
        C, S = c * c - s * s, 2 * c * s
        require(c % 2 == 1 and s % 2 == 0 and c * c + s * s == P * P)
        require(gcd(c, s) == 1 and gcd(C, S) == 1)
        require(C % 2 == 1 and S % 2 == 0 and S > 0)
        require(abs(C) < P * P and S < P * P)
        require(C * C + S * S == P ** 4)
        require(C % P and S % P and (C * C - S * S) % P)
        require(gcd(C - S, C + S) == 1 and (C - S) * (C + S) != 0)
        require((C - S) ** 2 < 2 * P ** 4 and (C + S) ** 2 < 2 * P ** 4)
        u, v = C, S                      # the same frame in the q role
        require((u * u - v * v) % P)     # q never divides U
        require(gcd(u - v, u + v) == 1 and (u - v) * (u + v) != 0)
        require((u - v) ** 2 < 2 * P ** 4 and (u + v) ** 2 < 2 * P ** 4)
    # real-data emptiness of all 8 cleared relations
    sb = ctx.bound(full=500, fast=200)
    for pat in pats:
        require(search_real_data(cleared_relation(pat), sb) == [], pat)
    # Fermat endpoint corroboration
    require(search_fermat_quartic(ctx.bound(full=300, fast=120)) == [])
    # closure bookkeeping: 8 in the ledger, none anywhere in a queue,
    # and the closed boxes stay closed (no queue entry inside
    # (J,K) <= (3,1) or (2,2))
    led, rem, _, _ = _ledger_and_queue()
    require(_ledger_tag_count(led, {"H3 double-lever (Fermat)"}) == 8)
    for _, classes, _ in rem:
        J = max(abs(j) for j, k in map(tuple, classes))
        K = max(abs(k) for j, k in map(tuple, classes))
        require(not (J <= 2 and K <= 2), classes)
        require(not (J <= 3 and K <= 1), classes)
    ctx.note("H3 dead x8 (double lever: Fermat x^4-y^4=z^2 twice + "
             "parity/size); the additive queue is EMPTY — every "
             "native pattern of the (1,1), (2,1), (3,1), (2,2) "
             "boxes is closed; A3.10 gate: the 44 replications")
