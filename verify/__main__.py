"""Runner: python3 -m verify [--fast] [--ci] [--only PATTERN]

FULL (default) runs the bounds cited in the documents; --fast shrinks bounds
for the pre-commit gate; --ci implies fast bounds plus a machine-readable
summary line.  Exits nonzero if any check FAILs.
"""

import argparse
import sys

from . import checks
from .framework import REGISTRY, run_all


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python3 -m verify")
    ap.add_argument("--fast", action="store_true", help="shrunk bounds (< 60 s)")
    ap.add_argument("--ci", action="store_true", help="fast bounds + machine summary")
    ap.add_argument("--only", metavar="PATTERN", help="substring filter on check names")
    args = ap.parse_args(argv)

    profile = "CI" if args.ci else ("FAST" if args.fast else "FULL")
    checks.load()
    results = run_all(profile=profile, only=args.only)

    width = max((len(r.name) for r in results), default=10)
    for r in results:
        print(f"{r.status:4}  {r.name:<{width}}  {r.seconds:8.2f}s  [{r.doc}]")
        for n in r.notes:
            print(f"      | {n}")
        if r.detail:
            for line in r.detail.splitlines():
                print(f"      ! {line}")

    n = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in results:
        n[r.status] += 1
    total = sum(n.values())
    print(
        f"\nprofile={profile}  registered={len(REGISTRY)}  ran={total}  "
        f"pass={n['PASS']}  fail={n['FAIL']}  skip={n['SKIP']}"
    )
    if profile == "CI":
        print(f"::verify-summary:: pass={n['PASS']} fail={n['FAIL']} skip={n['SKIP']}")
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
