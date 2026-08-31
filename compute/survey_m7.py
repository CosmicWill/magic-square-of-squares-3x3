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

Concurrency: a stale second instance used to be able to clobber a
first one's results (state was loaded once at startup and the whole
in-memory view rewritten on every save).  Two guards now: record()
re-reads the file and merges before writing, so a save can only ADD
orbits; and a lock file holding the owner pid makes a concurrent
start refuse loudly instead of silently duplicating ~2 h of compute
per orbit.  Pass --force to break a lock whose owner is gone.
"""

import json
import os
import sys
import time

from compute.descent_differentials import character_orbits, eigenspace_dim

STATE = os.path.join(os.path.dirname(__file__), "data_survey_m7.json")
LOCK = STATE + ".lock"
M = 7


def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"m": M, "done": {}, "candidates": {}}


def _pid_alive(pid):
    if pid == os.getpid():
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError, PermissionError) as exc:
        return isinstance(exc, PermissionError)
    return True


def acquire_lock(force=False):
    """Refuse to run beside a live instance (that is how orbits get
    computed twice).  Returns True if the lock is ours."""
    if os.path.exists(LOCK):
        try:
            with open(LOCK, encoding="utf-8") as fh:
                owner = json.load(fh)
            pid = int(owner.get("pid", -1))
        except (ValueError, OSError):
            pid = -1
        if _pid_alive(pid) and not force:
            print(f"REFUSING TO START: survey already running as pid "
                  f"{pid} (since {owner.get('started')}).  Stop it "
                  f"first, or pass --force if you are certain it is "
                  f"dead.", flush=True)
            return False
        print(f"clearing stale lock (pid {pid} not running)", flush=True)
    with open(LOCK, "w", encoding="utf-8") as fh:
        json.dump({"pid": os.getpid(),
                   "started": time.strftime("%Y-%m-%d %H:%M:%S")}, fh)
    return True


def release_lock():
    try:
        with open(LOCK, encoding="utf-8") as fh:
            if int(json.load(fh).get("pid", -1)) != os.getpid():
                return
    except (ValueError, OSError):
        return
    try:
        os.remove(LOCK)
    except OSError:
        pass


def record(name, entry):
    """Merge one orbit result into the checkpoint: re-read, add, write
    atomically.  Never drops another writer's orbits."""
    st = load()
    st["done"][name] = entry
    if entry["nullity"]:
        st.setdefault("candidates", {})[name] = {
            "orbit": entry["orbit"], "nullity": entry["nullity"]}
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(st, fh)
    os.replace(tmp, STATE)
    return st


def main():
    if not acquire_lock(force="--force" in sys.argv):
        return 1
    try:
        st = load()
        orbits = character_orbits((2, 4, 6, 8))
        todo = [(key, osize) for key, osize in orbits
                if repr(sorted(key)) not in st["done"]]
        print(f"m = {M} survey: {len(orbits)} nontrivial orbits, "
              f"{len(st['done'])} done, {len(todo)} remaining",
              flush=True)
        for key, osize in todo:
            name = repr(sorted(key))
            # another instance may have finished it since we listed
            if name in load()["done"]:
                print(f"orbit {name}: already recorded, skipping",
                      flush=True)
                continue
            t0 = time.time()
            d = eigenspace_dim(key, M, modp=True)
            # saturation check at a larger degree bound (m = 6
            # protocol):
            dD = sum((M - (1 if ab in key else 0)) // 2 for ab in
                     [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)])
            d2 = eigenspace_dim(key, M, dN=dD + M + 3, modp=True)
            assert d == d2, (name, d, d2)
            dt = time.time() - t0
            st = record(name, {"orbit": osize, "nullity": d,
                               "seconds": round(dt, 1)})
            print(f"orbit {name} (x{osize}): mod-p nullity {d} "
                  f"[{dt:.0f}s]  ({len(st['done'])}/{len(orbits)})",
                  flush=True)
        st = load()
        zero = all(v["nullity"] == 0 for v in st["done"].values())
        complete = len(st["done"]) == len(orbits)
        print(f"SURVEY {'COMPLETE' if complete else 'PARTIAL'}: "
              f"{len(st['done'])}/{len(orbits)} orbits; "
              f"all-zero (h^0 = 0 proven for every nontrivial "
              f"character at m = 7): {zero and complete}; "
              f"candidates: {st['candidates']}", flush=True)
    finally:
        release_lock()
    return 0


if __name__ == "__main__":
    sys.exit(main())
