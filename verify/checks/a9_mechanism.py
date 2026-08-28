"""M12-B and M12-D: the mechanism of the beyond-genus kills, the
desert extension to m <= 10^4, and the additive desert to 10^7
(docs/attacks/A9-discrete-spheres.md §5; A3/A6 bound updates)."""

import json
import os

from ..framework import check, require

DOC = "docs/attacks/A9-discrete-spheres.md"

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "compute")


@check("a9.kill_mechanism", DOC)
def _(ctx):
    """The fourth-sieve mechanism verdicts (M12-B): the ideal-product
    model is EXACT on every conductor-coprime value (zero mismatches);
    no odd-order character ever separates (the inverse-closure lemma,
    verified on data); every m = 725 GLOBAL kill is ARC (no character
    certificate of any order); on the full 11-passer sweep the census
    is 30 ARC + 6 CHARACTER, the CHARACTER kills sitting exactly at
    m = 481 and m = 962 = 2*481 (lines 4, 6, 7) with every separator
    of order exactly 4 — the Redei/4-rank layer."""
    from compute.redei_probe import analyze
    from compute.sphere_composition import PASSERS_1200

    n = ctx.bound(full=11, fast=3)
    if n >= 11:
        pairs = PASSERS_1200
    else:
        pairs = [p for p in PASSERS_1200 if p[0] in (425, 481)] \
            + [p for p in PASSERS_1200 if p[0] == 725][:1]
        pairs = pairs[:n] if len(pairs) > n else pairs
    rows, stats, model_stats = analyze(pairs, verbose=False)
    require(model_stats["MISMATCH"] == 0, "ideal-product model mismatch")
    for r in rows:
        for o, _ in r.get("separators", []):
            require(o % 2 == 0, "odd-order separator (lemma violated)")
        if r["pair"][0] == 725 and r.get("verdict") == "GLOBAL":
            require(r["mechanism"] == "ARC", "m=725 kill not ARC")
    if len(pairs) == 11:
        require(stats == {"CHARACTER": 6, "ARC": 30, "L0": 21,
                          "GENUS": 0}, stats)
        chars = sorted((r["pair"][0], r["line"]) for r in rows
                       if r.get("mechanism") == "CHARACTER")
        require(chars == [(481, 4), (481, 6), (481, 7),
                          (962, 4), (962, 6), (962, 7)], chars)
        for r in rows:
            if r.get("mechanism") == "CHARACTER":
                require(all(o == 4 for o, _ in r["separators"]),
                        "separator order != 4")
        require(model_stats == {"EXACT": 62, "MISMATCH": 0,
                                "entangled": 46}, model_stats)
    ctx.note("fourth sieve = quartic (Redei) layer where 4-rank bites "
             "(6/36, all at 481/962, separators exactly order 4) + "
             "prime-class alignment everywhere else (30/36); model "
             "EXACT on all coprime values")


@check("a9.desert_ext", DOC)
def _(ctx):
    """M12-D: the three-sieve pair desert extends to m <= 3x10^4 with
    ZERO golden centers (frozen artifacts data_desert_10k.json and
    data_desert_30k.json; at 3x10^4: 6101 centers, 146914 ordered
    pairs = 122630 positivity + 18992 coherence + 5292
    representation).  Pinned totals plus a live re-verification of a
    deterministic sample of the representation kills and of the
    artifacts' internal consistency."""
    pinned = {"data_desert_10k.json":
              (10000, 1667, 32850, 28028, 3816, 1006),
              "data_desert_30k.json":
              (30000, 6101, 146914, 122630, 18992, 5292)}
    for name, (upto, c, pr, po, ch, rp) in pinned.items():
        with open(os.path.join(DATA, name), encoding="utf-8") as fh:
            st = json.load(fh)
        require(st["done_upto"] == upto, name)
        t = st["totals"]
        require((t["centers"], t["pairs"], t["pos"], t["coh"],
                 t["rep"]) == (c, pr, po, ch, rp), (name, t))
        require(t["pos"] + t["coh"] + t["rep"] == t["pairs"],
                "partition")
        require(st["golden"] == [], "GOLDEN CENTER recorded?!")
        require(len(st["rep_killed_pairs"]) == rp)
        require(all(m <= upto for m, _, _ in st["rep_killed_pairs"]))
    # live re-verification of sampled representation kills
    from compute.desert_extension import pair_killed_by_representation
    from compute.sphere_gluing import coherent_pair
    k = ctx.bound(full=6, fast=2)
    sample = st["rep_killed_pairs"][:: max(1, len(
        st["rep_killed_pairs"]) // k)][:k]
    for m, U, V in sample:
        require(U + V <= m * m, "sampled pair fails positivity?!")
        require(coherent_pair(m, U, V), "sampled pair incoherent?!")
        require(pair_killed_by_representation(m, U, V),
                f"sampled pair ({m},{U},{V}) not rep-killed on re-run")
    ctx.note(f"pair desert VERIFIED(3x10^4): zero golden centers; "
             f"{len(sample)} representation kills re-verified live")


@check("a3.additive_ext", DOC)
def _(ctx):
    """The A3 additive desert extended: no d1, d2, d1+d2 in any D(m)
    for m <= 10^7 (artifact data_additive_desert.json, pinned counts),
    with a live re-run of the block sieve to the profile bound."""
    path = os.path.join(DATA, "data_additive_desert.json")
    with open(path, encoding="utf-8") as fh:
        st = json.load(fh)
    require(st["done_upto"] == 10_000_000)
    require(st["triples"] == [] and st["quads"] == [])
    require(st["centers_ge2"] == 3116858 and
            st["pair_count"] == 99288935, "pinned counts")
    # live re-run to the profile bound
    from compute.additive_desert_ext import primitive_leg_products
    bound = ctx.bound(full=1_000_000, fast=150_000)
    prim = primitive_leg_products(bound)
    hs = sorted(prim)
    lo, blockn = 1, 200_000
    n_triples = 0
    while lo <= bound:
        hi = min(lo + blockn - 1, bound)
        block = {}
        for h in hs:
            if h > hi:
                break
            first = max(h, ((lo + h - 1) // h) * h)
            for m in range(first, hi + 1, h):
                g = m // h
                gg2 = 2 * g * g
                bl = block.setdefault(m, set())
                for p in prim[h]:
                    bl.add(gg2 * p)
        for m, D in block.items():
            if len(D) < 2:
                continue
            Ds = sorted(D)
            for i, d1 in enumerate(Ds):
                for d2 in Ds[:i]:
                    if d1 + d2 in D:
                        n_triples += 1
        lo = hi + 1
    require(n_triples == 0, "additive triple found in live re-run")
    ctx.note(f"additive desert VERIFIED(10^7) via artifact; live "
             f"re-run clean to {bound}")


@check("a9.actuarial_sample", DOC)
def _(ctx):
    """W6 actuarial v1 regularities, pinned on the small-m sample
    artifact (40 stage-3 pairs, m <= 6000): center-line kills always
    in {1, 2} (the center cap), outer <= 4, total <= 6; one sampled
    row's full line-kill count re-verified live."""
    path = os.path.join(DATA, "data_actuarial_smallm.json")
    with open(path, encoding="utf-8") as fh:
        art = json.load(fh)
    rows = art["rows"]
    require(len(rows) == 40 and art["mcap"] == 6000)
    for m, U, V, kt, kc, ko in rows:
        require(m <= 6000)
        require(kt == kc + ko, "count split")
        require(1 <= kc <= 2, f"center cap violated: kc={kc} at {m}")
        require(0 <= ko <= 4 and kt <= 6)
    # live re-verification of the first sampled row
    from compute.actuarial_model import killed_line_count
    m, U, V, kt, kc, ko = rows[0]
    require(tuple(killed_line_count(m, U, V)) == (kt, kc, ko),
            "live recount mismatch")
    ctx.note("center cap (kc in {1,2}) holds on all 40 sampled kills; "
             "outer <= 4; k <= 6; first row re-verified live")
