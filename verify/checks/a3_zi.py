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
