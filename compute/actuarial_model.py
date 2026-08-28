"""W6 actuarial model v1 (ROADMAP): is the desert's perfect record
surprising?

The model prices the three sieves from measured data and extrapolates
the expected number of GOLDEN CENTERS (three-sieve survivors) up to a
bound M, under an explicit independence heuristic — the honest
Cramer-style baseline the roadmap asked for.

Calibration inputs (from the frozen desert artifacts):
  * stage flow: ordered pairs -> positivity -> coherence -> stage 3;
  * line-level kill statistics on a stratified sample of the stage-3
    corpus: for each sampled pair, the number k of its 8 lines whose
    co-norm triple no single class represents (ground truth, full
    scan — no early exit), split center-lines vs outer-lines.

Model: each line of a stage-3 pair is representation-killed
independently with probability p (fitted per m-band by truncated-
binomial MLE from the k-sample, k >= 1 by corpus construction);
P(pair survives) = (1 - p)^8; E[golden <= M] = sum over m-bands of
(stage-3 pairs per band) * (1 - p_band)^8, with the stage-3 density
and p extrapolated by the fitted trends.

Run:  python -m compute.actuarial_model [SAMPLE=120]
"""

import json
import os
import sys
from math import comb

from compute.sphere_composition import prims, strata
from compute.sphere_gluing import pair_lines, represents

STATE = os.path.join(os.path.dirname(__file__), "data_desert_30k.json")


def killed_line_count(m, U, V):
    """(k_total, k_center, k_outer) for the pair — full scan."""
    n = 3 * m * m
    kc = ko = 0
    for i, tri in enumerate(pair_lines(2 * m * m, U, V)):
        killed = True
        for g, ct, D, th in strata(tri, n):
            pf = prims(D)
            if pf and any(all(represents(f, t) for t in th) for f in pf):
                killed = False
                break
        if killed:
            if i < 4:
                kc += 1
            else:
                ko += 1
    return kc + ko, kc, ko


def truncated_binomial_mle(ks, n=8):
    """MLE of p for k ~ Binomial(n, p) conditioned on k >= 1."""
    lo, hi = 1e-6, 1 - 1e-6
    kbar = sum(ks) / len(ks)
    for _ in range(80):
        p = (lo + hi) / 2
        mean = n * p / (1 - (1 - p) ** n)
        if mean < kbar:
            lo = p
        else:
            hi = p
    return (lo + hi) / 2


def sample_lines(sample_target, mcap=None, dump=None):
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
    corpus = st["rep_killed_pairs"]
    if mcap:
        corpus = [r for r in corpus if r[0] <= mcap]
    stride = max(1, len(corpus) // sample_target)
    sample = corpus[::stride][:sample_target]
    rows = []
    for m, U, V in sample:
        kt, kc, ko = killed_line_count(m, U, V)
        rows.append((m, U, V, kt, kc, ko))
    if dump:
        with open(dump, "w", encoding="utf-8") as fh:
            json.dump({"mcap": mcap, "rows": rows}, fh)
    return st, rows


def model(st, rows, bands=((0, 5000), (5000, 15000), (15000, 30000))):
    print(f"line-kill sample: {len(rows)} stage-3 pairs")
    out = []
    for lo, hi in bands:
        band = [r for r in rows if lo < r[0] <= hi]
        if not band:
            continue
        ks = [r[3] for r in band]
        p = truncated_binomial_mle(ks)
        kc = sum(r[4] for r in band)
        ko = sum(r[5] for r in band)
        surv = (1 - p) ** 8
        p0 = surv / (surv + (1 - surv))     # unconditional P(k = 0)
        out.append((lo, hi, len(band), sum(ks) / len(ks), p, surv,
                    kc, ko))
        print(f"  m in ({lo},{hi}]: n={len(band)}, mean k = "
              f"{sum(ks)/len(ks):.2f}, p_line = {p:.3f}, "
              f"P(survive) = (1-p)^8 = {surv:.2e}   "
              f"[center-line kills {kc}, outer {ko}]")
    # binomial shape check on the pooled sample
    ks = [r[3] for r in rows]
    p_all = truncated_binomial_mle(ks)
    dist = {k: ks.count(k) for k in range(0, 9)}
    exp = {k: len(ks) * comb(8, k) * p_all ** k * (1 - p_all) ** (8 - k)
           / (1 - (1 - p_all) ** 8) for k in range(1, 9)}
    print(f"pooled p_line = {p_all:.3f}; k-distribution observed "
          f"{ {k: v for k, v in dist.items() if v} } vs truncated-"
          f"binomial expectation { {k: round(v, 1) for k, v in exp.items() if v >= 0.5} }")
    # expected golden centers to 3e4 under the model
    t = st["totals"]
    stage3 = t["rep"]
    surv_all = (1 - p_all) ** 8
    print(f"stage-3 pairs observed to 3e4: {stage3}; model "
          f"E[golden <= 3e4] = {stage3 * surv_all:.3f}")
    # crude extrapolation: stage-3 pairs per center grow ~ linearly in
    # log m (measured 22 to 1200 -> 5292 to 3e4); assume stage-3 count
    # scales ~ M^gamma with gamma fitted from (1200, 22) -> (3e4, 5292):
    from math import log
    gamma = log(5292 / 22) / log(30000 / 1200)
    for M in (10 ** 5, 10 ** 6, 10 ** 7):
        s3 = 5292 * (M / 30000) ** gamma
        # p_line trend: fit p across bands as p(m) = a + b log m
        e = s3 * surv_all
        print(f"  extrapolated E[golden <= {M:.0e}] ~ {e:.2f}  "
              f"(stage-3 ~ {s3:.0f}, survive ~ {surv_all:.1e}; "
              f"gamma = {gamma:.2f}, p_line held at pooled value)")
    return p_all, surv_all, gamma


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = int(args[0]) if args else 120
    mcap = int(args[1]) if len(args) > 1 else None
    dump = None
    for a in sys.argv[1:]:
        if a.startswith("--dump="):
            dump = a.split("=", 1)[1]
    st, rows = sample_lines(target, mcap=mcap, dump=dump)
    joint = {}
    for _, _, _, kt, kc, ko in rows:
        joint[(kc, ko)] = joint.get((kc, ko), 0) + 1
    print("joint (center-kills, outer-kills) distribution:",
          {f"{k[0]}c+{k[1]}o": v for k, v in sorted(joint.items())})
    model(st, rows)


if __name__ == "__main__":
    main()
