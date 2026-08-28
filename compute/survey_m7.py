"""A8.18 scope closure, m = 7 (background job): the nontrivial-character
mod-p survey of H^0(X^o, S^7 Omega^1) eigenspaces, orbit-checkpointed.

The trivial character at m = 7 is settled exactly (A8.18: 7 -> 0 on the
resolution).  This job surveys the 255 NONTRIVIAL characters (50
D4-orbits, sizes 2/4/6/8) with the saturated mod-p ambient computation
of compute.descent_differentials: mod-p nullity 0 PROVES the ambient
eigenspace (hence the resolution subspace) vanishes; positive values
are upper bounds queued for exact/tau follow-up, exactly the m = 6
protocol.

Checkpoint: compute/data_survey_m7.json after every orbit; safe to
kill and rerun.  Run:  python -m compute.survey_m7
"""

import json
import os
import time

from compute.descent_differentials import character_orbits, eigenspace_dim

STATE = os.path.join(os.path.dirname(__file__), "data_survey_m7.json")
M = 7


def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"m": M, "done": {}, "candidates": {}}


def save(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(st, fh)
    os.replace(tmp, STATE)


def main():
    st = load()
    orbits = character_orbits((2, 4, 6, 8))
    todo = [(key, osize) for key, osize in orbits
            if repr(sorted(key)) not in st["done"]]
    print(f"m = {M} survey: {len(orbits)} nontrivial orbits, "
          f"{len(todo)} remaining", flush=True)
    for key, osize in todo:
        name = repr(sorted(key))
        t0 = time.time()
        d = eigenspace_dim(key, M, modp=True)
        # saturation check at a larger degree bound (m = 6 protocol):
        dD = sum((M - (1 if ab in key else 0)) // 2 for ab in
                 [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)])
        d2 = eigenspace_dim(key, M, dN=dD + M + 3, modp=True)
        assert d == d2, (name, d, d2)
        dt = time.time() - t0
        st["done"][name] = {"orbit": osize, "nullity": d,
                            "seconds": round(dt, 1)}
        if d:
            st["candidates"][name] = {"orbit": osize, "nullity": d}
        save(st)
        print(f"orbit {name} (x{osize}): mod-p nullity {d} "
              f"[{dt:.0f}s]", flush=True)
    zero = all(v["nullity"] == 0 for v in st["done"].values())
    print(f"SURVEY COMPLETE: {len(st['done'])} orbits; "
          f"all-zero (h^0 = 0 proven for every nontrivial character "
          f"at m = 7): {zero}; candidates: {st['candidates']}",
          flush=True)


if __name__ == "__main__":
    main()
