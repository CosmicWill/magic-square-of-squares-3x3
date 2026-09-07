"""Read-only census for the prime-column lemma in docs/PROOF-DIRECTIONS-2026-09-06.md.

Run: python -m compute.valuation_signature_probe
The written proof is universal. The integer checks below are independent
consistency checks; the census applies its label criterion to recorded classes.
This script does not update campaign verdicts.
"""
from collections import Counter
import gzip
from itertools import product
import json
from math import prod
from pathlib import Path


def column_failure(labels):
    """A nonzero column maximum occurring fewer than three times is impossible."""
    for column in zip(*labels):
        magnitudes = [abs(e) for e in column]
        if magnitudes.count(max(magnitudes)) < 3:
            return True
    return False


def original_equation_failure(labels):
    for column in zip(*labels):
        for indices in ((0, 1, 2), (0, 1, 3)):
            magnitudes = [abs(column[i]) for i in indices]
            if magnitudes.count(max(magnitudes)) < 2:
                return True
    return False


def valuation(n, p):
    if not n:
        return None
    n = abs(n)
    exponent = 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def gaussian_mul(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def gaussian_power(z, n):
    result = (1, 0)
    for _ in range(n):
        result = gaussian_mul(result, z)
    return result


def independent_checks():
    # No imports from the curve or congrua engines.
    primes = (5, 13, 17)
    frames = ((3, 4), (5, 12), (15, 8))
    frame_checks = 0
    for box in ((1, 1, 1), (2, 1, 1), (3, 2, 1)):
        for label in product(*(range(-a, a + 1) for a in box)):
            if not any(label):
                continue
            z = (1, 0)
            for e, (c, s) in zip(label, frames):
                z = gaussian_mul(z, gaussian_power((c, s if e >= 0 else -s), 2 * abs(e)))
            d = z[1] * prod(p ** (2 * (a - abs(e))) for p, a, e in zip(primes, box, label))
            for p, a, e in zip(primes, box, label):
                observed = valuation(d, p)
                lower = 2 * (a - abs(e))
                assert (observed == lower) if e else (observed is None or observed >= lower)
                frame_checks += 1
    offset_checks = 0
    for p in (3, 5, 7, 13, 17):
        for u in range(1, 101):
            for v in range(1, u):
                values = [valuation(d, p) for d in (u, v, u + v, u - v)]
                assert None not in values and values.count(min(values)) >= 3
                offset_checks += 1
    return {"frame_valuation_checks": frame_checks, "offset_checks": offset_checks}


def census(data):
    tally = Counter()
    finite_routes = Counter()
    free_frames = Counter()
    for record in data["classes"]:
        labels = record["cand"][:4]
        assert len(labels) == 4 and all(len(label) == 3 for label in labels)
        verdict = record.get("verdict", record.get("v"))
        fails = column_failure(labels)
        tally[f"{verdict}: {'excluded' if fails else 'survives'}"] += 1
        if verdict == "finite":
            route = ("original equations" if original_equation_failure(labels)
                     else "combined equations" if fails else "survives")
            finite_routes[route] += 1
        if any(sum(e != 0 for e in column) == 1 for column in zip(*labels)):
            assert fails
            free_frames[verdict] += 1
    return {"tally": dict(tally), "finite_routes": dict(finite_routes),
            "free_frames_excluded": dict(free_frames)}


def main():
    base = Path(__file__).resolve().parent
    result = {"independent_checks": independent_checks()}
    with (base / "data_omega3_box111.json").open(encoding="utf-8") as handle:
        data = json.load(handle)
    result["111"] = census(data)
    # Entry 118 closed these independently; their labels still pass A3.PC.
    c2 = [r for r in data["quotients"]["genus0"]["classes"] if r.get("entry118")]
    assert len(c2) == 16 and all(r["verdict"] == "dead" and not column_failure(r["cand"][:4]) for r in c2)
    result["C2_closed_classes_passing_column_rule"] = len(c2)
    with gzip.open(base / "data_omega3_box211.json.gz", "rt", encoding="utf-8") as handle:
        result["211_incremental"] = census(json.load(handle))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
