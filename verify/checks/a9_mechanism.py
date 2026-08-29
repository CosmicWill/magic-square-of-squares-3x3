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
    pinned = {"data_actuarial_smallm.json": (40, 6000),
              "data_actuarial_sample.json": (120, 30000)}
    for name, (nrows, mcap) in pinned.items():
        with open(os.path.join(DATA, name), encoding="utf-8") as fh:
            art = json.load(fh)
        rows = art["rows"]
        require(len(rows) == nrows, name)
        for m, U, V, kt, kc, ko in rows:
            require(m <= mcap)
            require(kt == kc + ko, "count split")
            require(1 <= kc <= 2, f"center cap violated: kc={kc} at {m}")
            require(0 <= ko <= 4 and kt <= 6)
    rows = json.load(open(os.path.join(
        DATA, "data_actuarial_smallm.json"), encoding="utf-8"))["rows"]
    # live re-verification of the first sampled row
    from compute.actuarial_model import killed_line_count
    m, U, V, kt, kc, ko = rows[0]
    require(tuple(killed_line_count(m, U, V)) == (kt, kc, ko),
            "live recount mismatch")
    ctx.note("center cap (kc in {1,2}) holds on all 160 sampled kills (both artifacts, m to 29725); "
             "outer <= 4; k <= 6; first row re-verified live")


@check("a9.center_cap", DOC)
def _(ctx):
    """Theorem A9.6 (the center cap): for every congrua pair, the
    U- and V-center lines carry the ACTUAL sphere points
    v = (e-f, m, e+f), whose saturated orthogonal even forms
    represent their co-norm triples — constructive certificates over
    the representation-kill corpus; plus rep_verdict spot checks that
    killed lines never include indices 0, 1."""
    from math import gcd, isqrt
    from compute.sphere_classes import orthogonal_form
    from compute.sphere_gluing import represents, rep_verdict

    with open(os.path.join(DATA, "data_desert_30k.json"),
              encoding="utf-8") as fh:
        corpus = json.load(fh)["rep_killed_pairs"]
    nmax = ctx.bound(full=2000, fast=400)
    stride = max(1, len(corpus) // nmax)
    checked = 0
    for m, U, V in corpus[::stride][:nmax]:
        n = 3 * m * m
        for X in (U, V):
            s, d = isqrt(m * m + X), isqrt(m * m - X)
            require(s * s == m * m + X and d * d == m * m - X,
                    f"offset {X} not a congruum of {m}?!")
            v = (d, m, s)
            require(sum(t * t for t in v) == n, "not on the sphere")
            g = gcd(d, gcd(m, s))
            vr = tuple(t // g for t in v)
            f = orthogonal_form(vr)
            require(all(t % 2 == 0 for t in f), "orthogonal form not even")
            tri = (2 * m * m + X, 2 * m * m, 2 * m * m - X)
            require(all(t % (g * g) == 0 for t in tri), "content")
            require(all(represents(f, t // (g * g)) for t in tri),
                    f"gluing certificate failed at m={m}, X={X}")
        checked += 1
    # sharp spot check: the sieve itself never kills lines 0, 1
    spots = ctx.bound(full=3, fast=1)
    small = [r for r in corpus if r[0] <= 1400][:spots]
    for m, U, V in small:
        counts, empty = rep_verdict(m, U, V)
        require(0 not in empty and 1 not in empty,
                f"real center line killed at {m}?!")
        require(counts[0] > 0 and counts[1] > 0)
    ctx.note(f"A9.6 certificates verified on {checked} corpus pairs "
             f"(both real center lines each); rep_verdict spot checks "
             f"({len(small)}) confirm killed lines exclude 0, 1")


@check("a9.gram_sieve", DOC)
def _(ctx):
    """Theorem A9.7 (pairwise Gram necessity) and its census: no
    alive line ever fails the Gram test (soundness — the theorem on
    data); the Gram sieve explains 56/57 anatomy kills (the single
    syzygy exception pinned at m=725 pair 2 line 5); every sampled
    corpus pair's phantom kill is a Gram failure (the k_c >= 1
    companion, mechanized)."""
    from compute.gram_sieve import pair_census
    from compute.sphere_composition import PASSERS_1200

    n = ctx.bound(full=11, fast=3)
    passers = PASSERS_1200 if n >= 11 else \
        [p for p in PASSERS_1200 if p[0] in (425, 481, 725)][:n]
    killed = explained = 0
    exceptions = []
    for m, U, V in passers:
        cen = pair_census(m, U, V)
        for i, (alive, gok) in enumerate(cen):
            require(not (alive and not gok),
                    f"A9.7 violated at m={m} line {i}")
            if not alive:
                killed += 1
                if not gok:
                    explained += 1
                else:
                    exceptions.append((m, U, V, i))
        require(any(not cen[i][0] and not cen[i][1] for i in (2, 3)),
                f"companion/Gram fails at m={m}")
    if n >= 11:
        require(killed == 57 and explained == 56, (killed, explained))
        require(exceptions == [(725, 171600, 282576, 5)], exceptions)
    ctx.note(f"A9.7 sound on {len(passers)} passers ({killed} kills, "
             f"{explained} gram-explained); phantom Gram-kill present "
             f"in every pair; syzygy exception(s): {exceptions}")


@check("a9.gram_sandwich", DOC)
def _(ctx):
    """Theorem A9.8 (sandwich) and the A9.C2 session findings, pinned:
    on the passers, k1 => exact-pairwise => gram with zero violations;
    exact and gram layers coincide (losslessness, Conjecture A9.C3);
    free products never fail; ph(A+,A-) fails on every passer; some
    phantom product fails whenever any product fails (A9.C2 at the
    Gram layer)."""
    from itertools import combinations
    from math import gcd as _gcd
    from compute.gram_sieve import (exact_pair_alive, gram_pair_k1,
                                    gram_pair_ok_strata)
    from compute.sphere_composition import PASSERS_1200
    from compute.sphere_gluing import pair_lines

    n_p = ctx.bound(full=11, fast=2)
    passers = PASSERS_1200[:n_p] if n_p < 11 else PASSERS_1200
    k1_t = ex_t = gr_t = pair_t = 0
    aa_fail = c2 = withfail = 0
    for m, U, V in passers:
        n = 3 * m * m
        n2 = 2 * m * m
        # free products never fail; ph(A+,A-) verdict; C2
        for w1, w2 in ((n2, n2 + U), (n2, n2 - U), (n2 + U, n2 - U),
                       (n2, n2 + V), (n2, n2 - V), (n2 + V, n2 - V)):
            require(gram_pair_ok_strata(w1, w2, n), "free product fails?!")
        Ap, Am = n2 + U + V, n2 - U - V
        Bp, Bm = n2 + U - V, n2 - U + V
        if not gram_pair_ok_strata(Ap, Am, n):
            aa_fail += 1
        phantom_fail = any(not gram_pair_ok_strata(w1, w2, n)
                           for w1, w2 in ((n2, Ap), (n2, Am), (Ap, Am),
                                          (n2, Bp), (n2, Bm), (Bp, Bm)))
        any_fail = False
        for tri in pair_lines(n2, U, V):
            for w1, w2 in combinations(tri, 2):
                pair_t += 1
                k1 = False
                G = _gcd(w1, w2)
                base, nn = 1, n
                while nn % 4 == 0:
                    nn //= 4
                    base *= 2
                dd = 1
                while (base * dd) ** 2 <= n:
                    g = base * dd
                    if n % (g * g) == 0 and G % (g * g) == 0 and \
                            gram_pair_k1(w1 // (g * g), w2 // (g * g),
                                         n // (g * g)):
                        k1 = True
                        break
                    dd += 2
                ex = exact_pair_alive(w1, w2, n)
                gr = gram_pair_ok_strata(w1, w2, n)
                require(not (k1 and not ex), "A9.8 left violated")
                require(not (ex and not gr), "A9.7 violated")
                require(ex == gr, "losslessness (A9.C3) violated")
                k1_t += k1
                ex_t += ex
                gr_t += gr
                if not gr:
                    any_fail = True
        if any_fail:
            withfail += 1
            require(phantom_fail, f"A9.C2 violated at m={m}")
            c2 += 1
    if n_p >= 11:
        require((pair_t, k1_t, ex_t, gr_t) == (264, 2, 165, 165))
        require(aa_fail == 11 and c2 == withfail == 11)
    ctx.note(f"A9.8 sandwich + A9.C3 losslessness on {pair_t} pairs; "
             f"free products all pass; ph(A+,A-) fails {aa_fail}/"
             f"{len(passers)}; A9.C2 holds {c2}/{withfail}")


@check("a9.syzygy", DOC)
def _(ctx):
    """Theorem A9.9 + Conjecture A9.C4: the pairwise-Gram + syzygy
    Diophantine system is sound (every alive line has a witness
    system) and explains ALL 57 anatomy kills, including the single
    pairwise-Gram survivor (m=725 pair 2 line 5, killed exactly by
    the syzygy determinant)."""
    from compute.gram_sieve import line_alive, syzygy_line_ok
    from compute.sphere_composition import PASSERS_1200
    from compute.sphere_gluing import pair_lines

    n_p = ctx.bound(full=11, fast=2)
    passers = PASSERS_1200 if n_p >= 11 else \
        [p for p in PASSERS_1200 if p[0] == 725]
    killed = explained = 0
    for m, U, V in passers:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            alive = line_alive(tri, n)
            sy = syzygy_line_ok(tri, n)
            require(not (alive and not sy), f"A9.9 violated m={m} l{i}")
            if not alive:
                killed += 1
                explained += not sy
    require(killed == explained, "beyond-syzygy kill found")
    if n_p >= 11:
        require(killed == 57, killed)
        # the pairwise-Gram survivor is syzygy-killed:
        from compute.gram_sieve import gram_line_ok
        tri5 = pair_lines(2 * 725 * 725, 171600, 282576)[5]
        n725 = 3 * 725 * 725
        require(gram_line_ok(tri5, n725) and
                not syzygy_line_ok(tri5, n725),
                "the syzygy exception no longer behaves as pinned")
    ctx.note(f"A9.9 sound; syzygy system explains {explained}/{killed} "
             f"kills on {len(passers)} passers (full profile pins "
             f"57/57 incl. the pairwise survivor)")


@check("a9.q1_sufficiency", DOC)
def _(ctx):
    """Theorem A9.10 (q = 1 sufficiency) and its census: 28/31 alive
    lines carry constructive q = 1 witnesses (representability proven
    with no class computation); the q = 1 test still fails all 57
    kills; the three q > 1 boundary lines are pinned with their
    witness indices (425/850 line 4: q = 77 with identical reduced
    witness under doubling; 1025 line 6: q = 31)."""
    from compute.gram_sieve import line_alive, syzygy_q1_line_ok
    from compute.sphere_composition import PASSERS_1200
    from compute.sphere_gluing import pair_lines

    n_p = ctx.bound(full=11, fast=3)
    passers = PASSERS_1200 if n_p >= 11 else \
        [p for p in PASSERS_1200 if p[0] in (425, 481, 725)][:n_p]
    boundary = []
    kills = expl = alive_q1 = 0
    for m, U, V in passers:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            alive = line_alive(tri, n)
            q1 = syzygy_q1_line_ok(tri, n)
            if alive:
                if q1:
                    alive_q1 += 1
                else:
                    boundary.append((m, i))
            else:
                kills += 1
                expl += not q1
    require(kills == expl, "q1 test passed on a killed line")
    if n_p >= 11:
        require((alive_q1, kills) == (28, 57), (alive_q1, kills))
        require(sorted(boundary) == [(425, 4), (850, 4), (1025, 6)],
                boundary)
    else:
        require(sorted(boundary) in ([], [(425, 4)]), boundary)
    ctx.note(f"A9.10 certifies {alive_q1} alive lines constructively; "
             f"q=1 test fails all {kills} kills; boundary (q>1) "
             f"lines: {sorted(boundary)}")


@check("a9.c4_theorem", DOC)
def _(ctx):
    """Theorem A9.12 (= C4, both directions): the syzygy test
    reproduces the sieve verdict exactly; the congruence hypotheses
    of the overlattice lemma A9.11 (8 | U; odd-core co-norms == 2
    mod 8) hold with zero exceptions; the 2-adic boundary instance
    (m = 1885 line 4, q = 4) is alive and witnessed."""
    from compute.gram_sieve import STATE as GSTATE
    from compute.gram_sieve import line_alive, syzygy_line_ok
    from compute.sphere_composition import PASSERS_1200
    from compute.sphere_gluing import pair_lines

    with open(os.path.join(DATA, "data_desert_30k.json"),
              encoding="utf-8") as fh:
        corpus = json.load(fh)["rep_killed_pairs"]
    # congruence hypotheses across the corpus
    noff = ctx.bound(full=len(corpus), fast=600)
    for m, U, V in corpus[:noff]:
        require(U % 8 == 0 and V % 8 == 0, "8 | U fails")
    for m, U, V in corpus[:60]:
        if m % 2:
            for tri in pair_lines(2 * m * m, U, V):
                require(all(w % 8 == 2 for w in tri),
                        "odd-core co-norm not 2 mod 8")
    # C4 equivalence on anatomy lines
    n_p = ctx.bound(full=11, fast=2)
    passers = PASSERS_1200 if n_p >= 11 else PASSERS_1200[:n_p]
    for m, U, V in passers:
        n = 3 * m * m
        for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
            require(line_alive(tri, n) == syzygy_line_ok(tri, n),
                    f"C4 equivalence fails at m={m} line {i}")
    # the 2-adic boundary instance
    if n_p >= 11:
        m, U, V = 1885, 827424, 2523000
        tri = pair_lines(2 * m * m, U, V)[4]
        n = 3 * m * m
        require(line_alive(tri, n) and syzygy_line_ok(tri, n),
                "2-adic instance regressed")
    ctx.note("C4 (Theorem A9.12) verified: sieve == Diophantine "
             "system on anatomy lines; A9.11 congruence hypotheses "
             "hold corpus-wide; 2-adic instance covered")


@check("a9.golden", DOC)
def _(ctx):
    """The first golden center (2026-08-28): m = 34225 = 185^2, pair
    (108786216, 718725000) passes positivity, coherence, and — on
    every tested line — representation, with the A9.12 Diophantine
    law agreeing exactly; the additive layer still excludes an actual
    square (U +- V not in D(m); additive desert to 10^7)."""
    from compute.congrua_search import congrua_sets
    from compute.gram_sieve import line_alive, syzygy_line_ok
    from compute.sphere_gluing import coherent_pair, pair_lines

    m, U, V = 34225, 108786216, 718725000
    require(m == 185 ** 2)
    D = dict(congrua_sets(m)).get(m, set())
    require(U in D and V in D and len(D) == 12)
    require(U + V <= m * m and coherent_pair(m, U, V))
    require((U + V) not in D and abs(U - V) not in D,
            "additive quadruple at the golden center?!")
    n = 3 * m * m
    lines = list(pair_lines(2 * m * m, U, V))
    k = ctx.bound(full=8, fast=2)
    for tri in lines[:k]:
        a = line_alive(tri, n)
        s = syzygy_line_ok(tri, n)
        require(a and s and a == s, "golden line dead or A9.12 mismatch")
    ctx.note(f"golden center m = 185^2 verified on {k}/8 lines "
             f"(sieve == A9.12 law); no additive quadruple — "
             f"sieve-transparent, not a square candidate")


@check("a9.c2_refuted", DOC)
def _(ctx):
    """The A9.C2 counterexample, pinned: at m = 21025 = 145^2, pair
    (144315600, 237646416), line 6 is killed (product pi(v-, B-)
    Gram-fails) while BOTH phantom lines are alive at every layer —
    a k_c = 0 kill; the companion k_c >= 1 was a regularity, not a
    law.  The center cap (A9.6) and the law (A9.12) hold here as
    everywhere."""
    from compute.gram_sieve import (gram_pair_ok_strata_fast,
                                    line_alive, named_products,
                                    syzygy_line_ok)
    from compute.sphere_gluing import pair_lines

    m, U, V = 21025, 144315600, 237646416
    require(m == 145 ** 2)
    n = 3 * m * m
    fails = [name for name, (w1, w2) in named_products(m, U, V).items()
             if not gram_pair_ok_strata_fast(w1, w2, n)]
    require(fails == ["rpB:v-,B-"], fails)
    lines = list(pair_lines(2 * m * m, U, V))
    deep = ctx.bound(full=1, fast=0)
    # phantoms alive (syzygy layer is cheap); line 6 dead
    require(syzygy_line_ok(lines[2], n) and syzygy_line_ok(lines[3], n),
            "phantom line not syzygy-alive")
    require(not syzygy_line_ok(lines[6], n), "line 6 not syzygy-dead")
    if deep:
        require(line_alive(lines[2], n) and line_alive(lines[3], n))
        require(not line_alive(lines[6], n))
        for i in (0, 1, 4, 5, 7):
            require(syzygy_line_ok(lines[i], n), f"line {i} dead?!")
    ctx.note("k_c = 0 kill pinned at m = 145^2: line 6 dies alone, "
             "phantoms alive at every layer — A9.C2 refuted; the cap "
             "(A9.6) and the law (A9.12) stand")


@check("a9.square_family", DOC)
def _(ctx):
    """The square-center-root motif, pinned: the m = k^2 family census
    via the PURE A9.12 Diophantine sieve (no class computations)
    reproduces the desert pipeline's verdicts independently — 12
    centers with stage-3 pairs for k <= 200, 156 stage-3, and the
    golden pair exactly at m = 185^2 (both orders); in the full
    verified range all golden pairs are square-family (2/192 vs
    0/11816 nonsquare)."""
    from compute.gram_sieve import square_family_census

    kmax = ctx.bound(full=200, fast=150)
    rows = square_family_census(kmax=kmax, verbose=False)
    golden = [(k, m, g) for k, m, D, s3, kl, g in rows if g]
    if kmax >= 200:
        require(len(rows) == 12 and sum(r[3] for r in rows) == 156,
                (len(rows), sum(r[3] for r in rows)))
        require(golden == [(185, 34225, 2)], golden)
    else:
        require(golden == [], golden)
        require((21025 in [r[1] for r in rows]), "145^2 missing")
    ctx.note(f"A9.12-sieve census, k <= {kmax}: {len(rows)} centers, "
             f"{sum(r[3] for r in rows)} stage-3; golden {golden} — "
             f"the Diophantine law reproduces the desert pipeline "
             f"independently")


@check("a9.square_family_ext", DOC)
def _(ctx):
    """The extended square-family artifact (k <= 316, m ~ 10^5, via
    the A9.12 sieve): 24 centers with stage-3 pairs, golden still
    exactly the 185^2 pair — no new golden centers to nearly twice
    the desert's verified range, even inside the enriched family."""
    with open(os.path.join(DATA, "data_square_family_316.json"),
              encoding="utf-8") as fh:
        rows = json.load(fh)
    require(len(rows) == 24, len(rows))
    golden = [(r[0], r[5]) for r in rows if r[5]]
    require(golden == [[185, 2]] or golden == [(185, 2)], golden)
    require(all(r[4] + r[5] == r[3] for r in rows), "row consistency")
    # live spot re-verification of one late-range killed row
    from compute.gram_sieve import square_family_census
    k_spot = ctx.bound(full=257, fast=113)
    spot = square_family_census(kmax=k_spot, verbose=False)
    art = {r[0]: r for r in rows}
    for row in spot:
        if row[0] in art:
            require(list(row) == art[row[0]], (row, art[row[0]]))
    ctx.note("k <= 316 artifact pinned: 24 centers, golden = {185^2} "
             "only; live rows re-verified to k <= " + str(k_spot))


@check("a9.scaling_law", DOC)
def _(ctx):
    """Lemma A9.13 (scaling monotonicity) and the identification of the
    two special pairs as self-scalings.  (i) The scaling map
    (m,U,V) -> (qm, q^2 U, q^2 V) sends congrua pairs to congrua pairs,
    preserves positivity, scales every co-norm triple by q^2, and sends
    A9.12 witnesses to witnesses (t -> q^2 t, k -> qk) — so alive lines
    stay alive and dead sets only shrink.  (ii) The golden pair is the
    37-self-scaling of (925, 79464, 525000) — coherence-dead at 925
    with dead lines {2..7} — and the C2-exception pair is the
    29-self-scaling of THE m=725 three-sieve passer (171600, 282576),
    dead lines {2..6} shrinking to {6}.  Self-scaling 5^2 q by q lands
    on (5q)^2: the square-family motif is the scaling phenomenon."""
    from math import isqrt
    from compute.sphere_gluing import coherent_pair, pair_lines
    from compute.gram_sieve import syzygy_line_ok_fast
    from compute.sphere_composition import PASSERS_1200

    # (ii) exact identifications
    require((37 * 925, 37**2 * 79464, 37**2 * 525000)
            == (34225, 108786216, 718725000), "golden scaling identity")
    require((29 * 725, 29**2 * 171600, 29**2 * 282576)
            == (21025, 144315600, 237646416), "exception scaling identity")
    require((725, 171600, 282576) in [tuple(p) for p in PASSERS_1200],
            "base of the exception is the m=725 passer")
    require(5 * 5 * 37 == 925 and 5 * 5 * 29 == 725 and
            (5 * 37) ** 2 == 34225 and (5 * 29) ** 2 == 21025,
            "self-scaling lands on the square family")

    # (i) witness scaling on real data: every alive base line of the
    # 725 passer stays alive at the 29-scaling via the SCALED witness
    def dead_set(m, U, V):
        n = 3 * m * m
        return {i for i, tri in enumerate(pair_lines(2 * m * m, U, V))
                if not syzygy_line_ok_fast(tri, n)}
    chains = [((725, 171600, 282576), 29, {2, 3, 4, 5, 6}, {6}, True, True),
              ((925, 79464, 525000), 37, {2, 3, 4, 5, 6, 7}, set(),
               False, True)]
    for (m0, U0, V0), q, want0, want1, coh0, coh1 in chains:
        m1, U1, V1 = q * m0, q * q * U0, q * q * V0
        require(coherent_pair(m0, U0, V0) is coh0, (m0, "coherence"))
        require(coherent_pair(m1, U1, V1) is coh1, (m1, "coherence"))
        d0 = dead_set(m0, U0, V0)
        require(d0 == want0, (m0, d0))
        if ctx.bound(full=1, fast=0) or m0 == 725:
            d1 = dead_set(m1, U1, V1)
            require(d1 == want1, (m1, d1))
            require(d1 <= d0, "monotonicity violated")
        # co-norm triples scale by q^2 (linearity)
        L0 = pair_lines(2 * m0 * m0, U0, V0)
        L1 = pair_lines(2 * m1 * m1, U1, V1)
        require(all(tuple(q * q * x for x in a) == tuple(b)
                    for a, b in zip(L0, L1)), "triple scaling")
    # algebraic witness scaling, spot: w1 w2 - t^2 = N k^2 implies
    # (q^2 w1)(q^2 w2) - (q^2 t)^2 = (q^2 N)(q k)^2 — identity check
    w1, w2, t, N, k, q = 11, 35, 13, 6, 6, 29
    require(w1 * w2 - t * t == N * k * k, "base witness")
    require((q*q*w1) * (q*q*w2) - (q*q*t)**2 == (q*q*N) * (q*k)**2,
            "scaled witness")
    ctx.note("A9.13: sieve verdicts only soften along scalings; golden "
             "= 37.(925 pair), exception = 29.(the 725 passer); "
             "(5q)^2 = self-scaled 5^2 q — the motif is the scaling law")


@check("a9.family_primitivity", DOC)
def _(ctx):
    """The primitivity census of the square family: stage-3 pairs at
    m = k^2 split into proper scalings (q | m, q^2 | U, q^2 | V for
    some q > 1) and primitive pairs.  Pinned counts: k <= 65 gives
    12 scaled + 8 primitive (FAST); k <= 100 gives 24 + 14 (FULL);
    the full k <= 316 run measured 210 + 86 (~71% scaled — logged,
    too slow to re-run here).  The family is heavily scaling-enriched
    but not purely scalings; both SPECIAL pairs (golden, C2-exception)
    are scalings.  Convergence: 65^2 = 4225 = 13*325 = 5*845 receives
    scalings from two distinct anatomy bases."""
    from compute.congrua_search import congrua_sets
    from compute.sphere_gluing import coherent_pair

    def max_scaling(m, U, V):
        best = 1
        for q in range(2, m + 1):
            if m % q == 0 and U % (q*q) == 0 and V % (q*q) == 0:
                best = q
        return best

    kmax = ctx.bound(full=100, fast=65)
    sc = pr = 0
    anc65 = set()
    for k in range(3, kmax + 1):
        m = k * k
        D = sorted(dict(congrua_sets(m)).get(m, set()))
        for U in D:
            for V in D:
                if U == V or U + V > m*m or not coherent_pair(m, U, V):
                    continue
                q = max_scaling(m, U, V)
                if q > 1:
                    sc += 1
                    if k == 65:
                        anc65.add(m // q)
                else:
                    pr += 1
    want = {65: (12, 8), 100: (24, 14)}[kmax]
    require((sc, pr) == want, (sc, pr))
    require({325, 845} <= anc65, anc65)
    ctx.note(f"k <= {kmax}: {sc} scaled + {pr} primitive stage-3 pairs; "
             "65^2 has ancestors at both 325 and 845 (ladder convergence)")


@check("a9.ladder_sweep", DOC)
def _(ctx):
    """The scaled-pair ladder sweep (A9.13 hunting, window
    (53400, 150000]): 7182 scaled pairs from the 56 base positivity
    pairs at the nine anatomy centers; 3314 coherent; 88 hits =
    20 golden + 68 near (1 dead).  Facts pinned from the artifact:
    (i) golden pairs are ABUNDANT on the ladder — seven golden
    centers in the window vs two pair-orders in the whole desert to
    53400; (ii) the golden centers 68450/102675/136900 are the
    2,3,4-multiples of 34225 = upward closure (A9.13 corollary in
    data); the minimal new golden centers are 96425, 105125, 126875,
    147175 — all nonsquare (136900 = (2*185)^2 is square only as an
    upward image), refuting the refined W4 hypothesis
    'sieves total off the square family'; (iii) fertility is
    seed-intrinsic: every hit comes from four unordered seeds, and
    the 925/1025 seeds resurrect ONLY along multiples of their own
    prime (37/41), while the 725 seeds are broad-spectrum; (iv) live
    re-verification: the 96425 golden passes all 8 lines by the
    A9.12 sieve (FAST) and the independent class-group path (FULL),
    and its corners are honestly non-square (golden != magic)."""
    import json as _json
    from math import isqrt
    from compute.sphere_gluing import coherent_pair, pair_lines
    from compute.gram_sieve import syzygy_line_ok_fast

    with open(os.path.join(DATA, "data_ladder_sweep.json"),
              encoding="utf-8") as fh:
        d = _json.load(fh)
    require((d["tested"], d["coherent"], len(d["hits"]))
            == (7182, 3314, 88), "sweep totals")
    hits = d["hits"]
    require(sum(1 for h in hits if h[7] == 0) == 20 and
            sum(1 for h in hits if h[7] == 1) == 68, "golden/near split")
    golden_centers = sorted({h[0] for h in hits if h[7] == 0})
    require(golden_centers == [68450, 96425, 102675, 105125,
                               126875, 136900, 147175], golden_centers)
    # 68450/102675/136900 are the 2,3,4-multiples of 34225 (upward
    # images; 136900 = (2*185)^2 is square for that trivial reason);
    # the four MINIMAL new golden centers are all nonsquare
    minimal = [96425, 105125, 126875, 147175]
    require([c for c in minimal if isqrt(c) ** 2 == c] == [],
            "minimal centers all nonsquare")
    require({(h[4], min(h[5], h[6]), max(h[5], h[6])) for h in hits} ==
            {(725, 122400, 282576), (725, 171600, 282576),
             (925, 79464, 525000), (1025, 130944, 450000)},
            "four unordered fertile seeds")
    require(all(h[3] % 37 == 0 for h in hits if h[4] == 925) and
            all(h[3] % 41 == 0 for h in hits if h[4] == 1025),
            "self-prime directions")
    # upward closure: 68450 = 2 * 34225 with the doubled golden pair
    require([68450, 2 * 2 * 108786216, 2 * 2 * 718725000] in
            [h[:3] for h in hits], "2-image of the 34225 golden")
    # (iv) live: the 96425 golden, both orders in artifact; re-sieve
    m, U, V = 96425, 133 * 133 * 171600, 133 * 133 * 282576
    require([m, U, V, 133, 725, 171600, 282576, 0] in hits)
    require(coherent_pair(m, U, V), "96425 coherent")
    n = 3 * m * m
    require(all(syzygy_line_ok_fast(t, n)
                for t in pair_lines(2 * m * m, U, V)), "96425 all alive")
    for e1 in (1, -1):
        for e2 in (1, -1):
            E = m * m + e1 * U + e2 * V
            require(isqrt(E) ** 2 != E, "a corner is square?!")
    if ctx.bound(full=1, fast=0):
        from compute.desert_extension import pair_killed_by_representation
        require(pair_killed_by_representation(m, U, V) is False,
                "class-group path disagrees at 96425")
    ctx.note("ladder sweep pinned: 20 golden + 68 near from 4 seeds; "
             "minimal new golden centers 96425/105125/126875/147175 all "
             "nonsquare; 925/1025 fertility = self-prime directions; "
             "96425 re-verified live (dual-path on FULL)")


@check("a9.local_locks", DOC)
def _(ctx):
    """Lemma A9.14 (localization) and the fertile-seed classification.
    (a) Scaled coherence == base coherence away from q (symbols
    invariant for p not dividing q, vacuous for p | q) — verified on a
    deterministic (seed, q) grid.  (b) Line locks: a line all of whose
    strata have a p-locally insoluble pair equation stays dead unless
    p | q.  Panel table pinned: the narrow seeds' outer lines are
    locked exactly at the self-prime (925 at 37, 1025 at 41, matching
    their chi-certificates), the 425 seeds are locked at 17 resp. 5,
    the broad-fertile and coherent-barren seeds have NO locks anywhere
    (their kills are class-type) — so fertility = eligibility
    direction (proven) x per-rung class luck (measured).  Soundness:
    alive lines are never locked; locks vacate on-direction in all
    three tested cases."""
    from compute.local_locks import (chi_certificates, line_locked_at,
                                     local_lock_table)
    from compute.resurrection_curves import SEEDS
    from compute.sphere_gluing import coherent_pair, pair_lines
    from compute.gram_sieve import syzygy_line_ok_fast

    want_certs = {
        "F1-broad": set(), "F2-broad": set(),
        "N1-37": {(37, 4), (37, 5), (37, 6), (37, 7)},
        "N2-41": {(41, 4), (41, 5), (41, 6), (41, 7)},
        "B1-425": {(17, 4), (17, 5)},
        "B2-425": set(),
        "B3-425": {(5, 4), (5, 5)},
        "B4-passer925": set(), "B5-1025": set(), "B6-845": set()}
    want_locks = {
        "F1-broad": {}, "F2-broad": {},
        "N1-37": {4: [37], 5: [37], 6: [37], 7: [37]},
        "N2-41": {4: [41], 5: [41], 6: [41], 7: [41]},
        "B1-425": {4: [17], 5: [17]},
        "B2-425": {},
        "B3-425": {4: [5], 5: [5], 6: [5], 7: [5]},
        "B4-passer925": {}, "B5-1025": {}, "B6-845": {}}
    panel = SEEDS if ctx.bound(full=1, fast=0) else \
        [s for s in SEEDS if s[0] in ("F2-broad", "N1-37", "B3-425")]
    for tag, m0, U0, V0 in panel:
        certs = set(chi_certificates(m0, U0, V0))
        require(certs == want_certs[tag], (tag, certs))
        locks = local_lock_table(m0, U0, V0)
        require(locks == want_locks[tag], (tag, locks))
        # soundness: alive lines never locked (implied by table match,
        # asserted directly for the killable lines)
        n = 3 * m0 * m0
        for i, tri in enumerate(pair_lines(2 * m0 * m0, U0, V0)):
            if syzygy_line_ok_fast(tri, n):
                require(i not in locks, (tag, i, "alive but locked"))
        # (a) coherence localization on a deterministic q-grid
        cert_ps = {p for p, _ in certs}
        for q in (2, 3, 5, 7, 17, 29, 37, 41, 10, 21):
            pred = all(q % p == 0 for p in cert_ps)
            got = coherent_pair(q * m0, q * q * U0, q * q * V0)
            require(pred == got, (tag, q, pred, got))
    # (b) locks vacate on-direction (the three tested unlock cases)
    for m0, U0, V0, p, q in ((425, 72384, 97104, 5, 5),
                             (425, 54600, 72384, 17, 17),
                             (925, 79464, 525000, 37, 37)):
        m, U, V = q * m0, q * q * U0, q * q * V0
        n = 3 * m * m
        require(all(not line_locked_at(t, n, p)
                    for t in pair_lines(2 * m * m, U, V)),
                (m0, p, "lock failed to vacate on-direction"))
    ctx.note("A9.14 verified: certificates and locks pinned for the "
             "panel; coherence localization exact on the q-grid; "
             "locks persist off-direction and vacate on-direction")


@check("a9.joint_locks", DOC)
def _(ctx):
    """The joint-system congruence layer and the rigid class.  The
    change of variables t -> q^2 t, k -> qk makes the scaled joint
    system mod M equivalent to the base system whenever gcd(q,M) = 1,
    so joint locks at ANY modulus are scaling-invariant off their own
    direction.  Pinned: B3's outer lines carry joint locks (4,5 at
    mod 5; 6,7 only at mod 25 — invisible to the pair-level test),
    vacating on its 5-rungs; B4 (the m = 925 passer) has NO joint
    lock at any modulus in {3,5,7,8,9,11,13,16,24,25,48,49} (FULL
    extends to 121/125/169) despite a flat ~6-dead resurrection curve
    to m ~ 10^5 — the RIGID class is beyond every congruence and
    local test built here (conjecturally spinor-level; named target).
    Soundness: alive lines never joint-locked."""
    from compute.local_locks import line_joint_lock
    from compute.sphere_gluing import pair_lines
    from compute.gram_sieve import syzygy_line_ok_fast

    # B3: locks and their exact depths
    m0, U0, V0 = 425, 72384, 97104
    n = 3 * m0 * m0
    tris = pair_lines(2 * m0 * m0, U0, V0)
    for i, want5, want25 in ((4, True, True), (5, True, True),
                             (6, False, True), (7, False, True)):
        require(line_joint_lock(tris[i], n, 5) is want5, (i, 5))
        require(line_joint_lock(tris[i], n, 25) is want25, (i, 25))
    # locks vacate on the 5-direction
    q = 5
    m, U, V = q * m0, q * q * U0, q * q * V0
    nq = 3 * m * m
    require(all(not line_joint_lock(t, nq, 25)
                for t in pair_lines(2 * m * m, U, V)), "vacate at q=5")
    # B4: no locks anywhere on the panel
    m0, U0, V0 = 925, 79464, 501600
    n = 3 * m0 * m0
    mods = (3, 5, 7, 8, 9, 11, 13, 16, 24, 25, 48, 49)
    if ctx.bound(full=1, fast=0):
        mods = mods + (121, 125, 169)
    for i, tri in enumerate(pair_lines(2 * m0 * m0, U0, V0)):
        alive = syzygy_line_ok_fast(tri, n)
        locks = [M for M in mods if line_joint_lock(tri, n, M)]
        if alive:
            require(locks == [], (i, "alive but joint-locked"))
        else:
            require(locks == [], (i, "unexpected B4 lock", locks))
    ctx.note("joint locks pinned: B3 outer locks at 5/25 vacate "
             "on-direction; B4 (the passer) lock-free everywhere "
             "tested — the rigid class is beyond congruence locks")


@check("a9.resurrection_curves", DOC)
def _(ctx):
    """The resurrection-curve panel (data_resurrection_curves.json,
    768 full profiles, 10 seeds, m <= 120000): the three measured
    fertility classes.  BROAD (F1/F2): coherent at every rung, kills
    class-type, mean dead count falls with size and both reach golden
    in-grid (F1 at q = 145, matching the ladder sweep).  NARROW
    (N1/N2): eligible only on their self-prime direction; N1 golden
    at every 37-rung, N2 at exactly dead {2} on every 41-rung (a
    golden is predicted higher up its ladder).  RIGID (B3/B4): flat
    at ~6 dead through two decades — B4 with no lock at any tested
    place or modulus: the named open obstruction.  One rung
    re-verified live."""
    import json as _json
    from compute.sphere_gluing import coherent_pair, pair_lines
    from compute.gram_sieve import syzygy_line_ok_fast

    with open(os.path.join(DATA, "data_resurrection_curves.json"),
              encoding="utf-8") as fh:
        d = _json.load(fh)
    rows = d["rows"]
    require(len(rows) == 768 and d["m_cap"] == 120000, len(rows))
    by = {}
    for tag, m0, U0, V0, q, m, coh, dead in rows:
        by.setdefault(tag, []).append((q, m, coh, dead))
    # N1: every coherent rung is a 37-multiple and golden
    n1 = [(q, coh, dead) for q, m, coh, dead in by["N1-37"]]
    require(all(q % 37 == 0 for q, coh, _ in n1 if coh))
    require(all(dead == [] for q, coh, dead in n1 if coh))
    require(sum(1 for _, coh, _ in n1 if coh) == 3)
    # N2: every coherent rung is a 41-multiple with dead exactly [2]
    n2 = [(q, coh, dead) for q, m, coh, dead in by["N2-41"]]
    require(all(q % 41 == 0 for q, coh, _ in n2 if coh))
    require(all(dead == [2] for q, coh, dead in n2 if coh))
    # F1 reaches golden at q = 145; F2 at q = 133
    require([dead for q, m, coh, dead in by["F1-broad"]
             if q == 145] == [[]])
    require([dead for q, m, coh, dead in by["F2-broad"]
             if q == 133] == [[]])
    # rigid: B3/B4 never drop below 5 dead on any rung
    for tag in ("B3-425", "B4-passer925"):
        require(min(len(dead) for _, _, _, dead in by[tag]) >= 5, tag)
    # broad softening: F2 mean dead falls from the small-q band to the
    # large-q band by at least 1
    def band_mean(tag, lo, hi):
        ds = [len(dead) for q, m, coh, dead in by[tag]
              if coh and lo <= q <= hi]
        return sum(ds) / len(ds)
    require(band_mean("F2-broad", 2, 15)
            - band_mean("F2-broad", 91, 150) > 1.0, "no softening?")
    # live spot: one recorded rung recomputed in full
    q, m, coh, dead = [r[4:] for r in rows if r[0] == "N2-41"
                       and r[4] == 82][0]
    require(coh is True and dead == [2])
    require(coherent_pair(m, 82 * 82 * 130944, 82 * 82 * 450000))
    n = 3 * m * m
    live = [i for i, t in enumerate(pair_lines(
        2 * m * m, 82 * 82 * 130944, 82 * 82 * 450000))
        if not syzygy_line_ok_fast(t, n)]
    require(live == [2], live)
    ctx.note("curves pinned: broad softens to golden, narrow rungs "
             "exact, rigid flat >= 5 dead; N2's 41-rung re-verified "
             "live (dead exactly {2})")


@check("a9.predicted_golden", DOC)
def _(ctx):
    """The first theory-predicted golden center: A9.14's narrow-seed
    classification (N2 = (130944, 450000) at 1025, eligible only on
    41-rungs, dead exactly {2} at q = 41, 82, 123, 164) predicted a
    golden up the 41-ladder; q = 205 (m = 210125 = 5^3 41^2) is
    GOLDEN — coherent, all eight lines representable (found by
    prediction, not sweep; beyond the sweep window).  FAST pins the
    arithmetic identities and chain minimality context; FULL
    re-verifies the full profile live."""
    from math import isqrt
    q, m0, U0, V0 = 205, 1025, 130944, 450000
    m, U, V = q * m0, q * q * U0, q * q * V0
    require(m == 210125 and m == 5 ** 3 * 41 ** 2)
    require(q % 41 == 0 and q == 5 * 41, "the 41-direction")
    require(isqrt(m) ** 2 != m, "nonsquare center")
    # corners are honestly non-square (golden != magic)
    for e1 in (1, -1):
        for e2 in (1, -1):
            E = m * m + e1 * U + e2 * V
            require(isqrt(E) ** 2 != E, "corner square?!")
    if ctx.bound(full=1, fast=0):
        from compute.sphere_gluing import coherent_pair, pair_lines
        from compute.gram_sieve import syzygy_line_ok_fast
        require(coherent_pair(m, U, V), "coherence")
        n = 3 * m * m
        dead = [i for i, t in enumerate(pair_lines(2 * m * m, U, V))
                if not syzygy_line_ok_fast(t, n)]
        require(dead == [], dead)
    ctx.note("m = 210125 = 205 * 1025: golden by prediction (the "
             "41-ladder), corners non-square; FULL re-runs the "
             "profile live")
