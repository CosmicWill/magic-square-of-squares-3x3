"""THE SECOND-LEVEL QUOTIENT CENSUS (entry 145; feasibility, no kills).  The symmetry tower applies the classical quotients (the even
quotient z = o^2, its odd companion, the reciprocal quotient w = o + kappa/o and its rationality twist) once, to each route's
hyperelliptic model and to the twisted models (level 1).  The curve R3 of entry 144 was decided by applying them a second time by
hand.  Here, for every open class, every live frame and every finite component, the tower is run with want_all=True and every
endpoint core recorded (CORE_RECORD_DEGREE raised to 100), and the classical quotients are applied recursively to every recorded
core (levels 2, 3, 4) until no symmetry remains or the degree drops to <= 6 (genus <= 2).  Per component: the minimal degree at
level 1 and at the deeper levels, and every endpoint of degree <= 6 reached at any level (chain, level, degree, core, normal form
with reciprocals merged).  The records of compute/data_second_level_census_145.json were produced by this code (scratch
sl_census.py, 2026-09-16).
Usage (from the repository root): python -m compute.second_level_census <start> <end> [out=FILE]
  -- the slice [start, end) of the open-class list ((2,1,1) classes first, then (3,1,1)), written to FILE (default
  second_level_census_<start>_<end>.json in the working directory)."""
import gzip, json, os, sys, time
import sympy as sp
from compute import symmetry_tower as ST
from compute import omega3 as O
from compute.omega3 import frame_factors
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXLEVEL = 4


def normal(P, var):
    c0 = [sp.Rational(c) for c in sp.Poly(P, var).all_coeffs()]
    den = 1
    for c in c0:
        den = sp.ilcm(den, c.q)
    c0 = [sp.Integer(c * den ** 2) for c in c0]
    g_ = 0
    for c in c0:
        g_ = sp.igcd(g_, int(c))
    sq = 1
    for p_, e_ in sp.factorint(g_).items():
        sq *= p_ ** (2 * (e_ // 2))
    return [int(c // sq) for c in c0]


def rev(cs, n):
    cs7 = [0] * (n - len(cs)) + list(cs)
    rc = cs7[::-1]
    while len(rc) > 1 and rc[0] == 0:
        rc.pop(0)
    return rc


def hgnormal(P, var):
    cs = normal(P, var)
    d = len(cs) - 1
    d_even = d if d % 2 == 0 else d + 1
    return min(cs, rev(cs, d_even + 1))


def recurse(label, core, var, level, out, seen):
    """Apply the classical quotients to y^2 = core(var); record every quotient; recurse while the degree stays > 6."""
    for name, Pq, v2, stc in ST.classical_quotients(core, var):
        P2 = sp.Poly(Pq, v2)
        if P2.degree() <= 0:
            continue
        d2 = P2.degree()
        key = (label + " -> " + name, d2)
        if key in seen:
            continue
        seen.add(key)
        rec = {"chain": label + " -> " + name, "level": level, "degree": d2, "genus": ST.genus_of_model(d2)}
        if d2 <= 6:
            rec["core"] = str(P2.as_expr())
            rec["normal"] = hgnormal(Pq, v2)
        out.append(rec)
        if d2 > 6 and level < MAXLEVEL:
            recurse(label + " -> " + name, Pq, v2, level + 1, out, seen)


def census(classes, outfile):
    """classes: list of (box, index); writes the records to outfile after every class."""
    ST.CORE_RECORD_DEGREE = 100
    ledgers = {}
    out = []
    t0 = time.time()
    for k, (box, idx) in enumerate(classes):
        if box not in ledgers:
            with gzip.open(os.path.join(ROOT, "compute", "data_omega3_box%s.json.gz" % box), "rt", encoding="utf-8") as fh:
                ledgers[box] = json.load(fh)
        O.set_box({"111": (1, 1, 1), "211": (2, 1, 1), "311": (3, 1, 1)}[box])
        c = ledgers[box]["classes"][idx]
        cand = json.loads(c["cand"]) if isinstance(c["cand"], str) else c["cand"]
        cand = tuple(tuple(t) for t in cand[:4]) + tuple(cand[4:])
        rec = {"box": box, "index": idx, "frames": {}}
        for f in range(3):
            ff = frame_factors(cand, f)
            if ff is None:
                rec["frames"][str(f)] = {"status": "degenerate"}
                continue
            curves, live = ff
            fr = {"live": [str(v) for v in live], "components": []}
            for phi, dg, dh in curves:
                v, info = O.decide_component(phi, dg, dh, cand, f)
                comp = {"deg": [dg, dh], "engine": v}
                if v == "finite":
                    t1 = time.time()
                    s = ST.analyse(phi.subs({O.tg: ST.g, O.th: ST.h}), want_all=True)
                    level1, deeper, seen = [], [], set()
                    for r in s["routes"]:
                        for e in r.get("endpoints", []) or []:
                            d1 = e.get("degree")
                            if not d1 or not e.get("core"):
                                continue
                            core = sp.sympify(e["core"])
                            if not core.free_symbols:
                                continue
                            var = next(iter(core.free_symbols))
                            item = {"chain": e["endpoint"], "level": 1, "degree": d1, "genus": ST.genus_of_model(d1)}
                            if d1 <= 6:
                                item["core"] = e["core"]
                                item["normal"] = hgnormal(core, var)
                            level1.append(item)
                            if d1 > 6:
                                recurse(e["endpoint"], core, var, 2, deeper, seen)
                    comp["min_degree_level1"] = min([it["degree"] for it in level1], default=None)
                    comp["min_degree_deeper"] = min([it["degree"] for it in deeper], default=None)
                    comp["n_level1"] = len(level1)
                    comp["n_deeper"] = len(deeper)
                    comp["small_level1"] = [it for it in level1 if it["degree"] <= 6]
                    comp["small_deeper"] = [it for it in deeper if it["degree"] <= 6]
                    comp["deeper_degrees"] = sorted({it["degree"] for it in deeper})
                    comp["seconds"] = round(time.time() - t1, 1)
                fr["components"].append(comp)
            rec["frames"][str(f)] = fr
        out.append(rec)
        with open(outfile, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1)
        print("[%d/%d] %s %d done, %.0fs" % (k + 1, len(classes), box, idx, time.time() - t0), flush=True)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("out=")]
    outs = [a[4:] for a in sys.argv[1:] if a.startswith("out=")]
    start, end = int(args[0]), int(args[1])
    OPEN = []
    for b in ("211", "311"):
        with gzip.open(os.path.join(ROOT, "compute", "data_omega3_box%s.json.gz" % b), "rt", encoding="utf-8") as fh:
            d = json.load(fh)
        OPEN += [(b, i) for i, c in enumerate(d["classes"]) if c["v"] == "finite"]
    census(OPEN[start:end], outs[0] if outs else "second_level_census_%d_%d.json" % (start, end))
    print("DONE", start, end)
