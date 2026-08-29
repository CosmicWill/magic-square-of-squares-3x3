"""W10 / A3-S1: the Z[i] reformulation of the additive layer
(docs/ROADMAP.md §W10; compute/zi_additive.py)."""

from ..framework import check, require

DOC = "docs/ROADMAP.md"


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
