"""M12-E: the Z-transplant autopsy probe (docs/attacks/A2-function-field.md §6)."""

from ..framework import check, require

DOC = "docs/attacks/A2-function-field.md"


@check("a2.abc_probe", DOC)
def _(ctx):
    """The (*-abc) groundwork, pinned: realized additive triples in
    D(c) are abc-cheap (the classical c = 157441 triple has quality
    0.430; none exceeds 1; none at square centers — consistent with
    the desert), while square centers show systematic squarefull
    enrichment of D-elements (ratio > 2) — the measured lever for the
    coupled inequality."""
    from compute.abc_probe import (realized_triples, squarefull_stats,
                                   two_square_reps)
    from math import isqrt
    import random

    cbound = ctx.bound(full=200_000, fast=60_000)
    trips = realized_triples(cbound)
    require(all(not sq for *_, sq in trips),
            "additive triple at a SQUARE center?!")
    require(all(q <= 1 for _, _, _, q, _ in trips),
            "realized triple with abc-quality > 1")
    if cbound >= 200_000:
        require(len(trips) == 1, trips)
        c, d2, d1, q, _ = trips[0]
        require((c, d2, d1) == (157441, 19800, 135240))
        require(abs(q - 0.4301) < 5e-4, q)
    else:
        require(trips == [], trips)
    mbound = 2000 if cbound >= 200_000 else 800
    reps = two_square_reps(mbound * mbound)
    sq_centers = [m * m for m in range(2, mbound + 1) if m * m in reps]
    random.seed(1)
    nonsq = [c for c in reps if isqrt(c) ** 2 != c]
    nonsq = random.sample(nonsq, min(len(nonsq), 4000))
    es, _ = squarefull_stats(reps, sq_centers)
    en, _ = squarefull_stats(reps, nonsq)
    require(es > 2 * en, (es, en))
    require(es > 0.6 and en < 0.35, (es, en))
    ctx.note(f"realized triples abc-cheap (max q <= 0.431); squarefull "
             f"enrichment at square centers {es:.3f} vs {en:.3f} "
             f"(ratio {es/en:.2f}) — the (*-abc) lever, measured")
