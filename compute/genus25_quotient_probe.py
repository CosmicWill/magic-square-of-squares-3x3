"""Exact quotient probe for the eight remaining (1,1,1) tower records.

python -m compute.genus25_quotient_probe --ranks --write
python -m compute.genus25_quotient_probe --ranks --check

This verifies rational maps on their stated affine charts, not complete point
sets or exclusions.  (Entry 134: the eight classes are dead by Theorem A3.SQ; the
maps are kept as the template for the surviving classes' joint-sign quotients.) Exceptional fibers and the original frame lifts remain
to be checked. No campaign ledger is modified. PARI is needed only for --ranks.
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

from compute import omega3 as O

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "compute/data_genus25_quotients.json"
CASES = {
    2841: ("plus", False), 2843: ("plus", True),
    2845: ("minus", False), 2847: ("minus", True),
    2892: ("minus", False), 2893: ("minus", True),
    2896: ("plus", False), 2897: ("plus", True),
}
COEFFS = {"plus": [12, -44, 40, 1], "minus": [-12, 28, -8, 1]}
x, y, z, w = sp.symbols("x y z w")


def build(with_ranks=False):
    ledger = json.loads((ROOT / "compute/data_omega3_box111.json").read_text(encoding="utf-8"))
    result = {"schema": 1, "date": "2026-09-08", "is_exclusion": False,
              "scope": "affine quotient identities; exceptional fibers and complete lifts pending",
              "models": {}, "classes": []}
    for name, cs in COEFFS.items():
        a6, a4, a2, a0 = cs
        h = a6*z**6 + a4*z**4 + a2*z**2 + a0
        assert sp.degree(h, z) == 6 and sp.gcd(h, sp.diff(h, z)) == 1
        e1 = [0, a4, 0, a2*a6, a0*a6*a6]
        e2 = [0, a2, 0, a0*a4, a0*a0*a6]
        # Elliptic quotient maps (X,Y) = (a6*z^2,a6*w),
        # respectively (a0/z^2,a0*w/z^3), on w^2 = h(z).
        assert sp.expand(a6*a6*h - ((a6*z*z)**3 + e1[1]*(a6*z*z)**2 + e1[3]*a6*z*z + e1[4])) == 0
        assert sp.cancel(a0*a0*h/z**6 - ((a0/z**2)**3 + e2[1]*(a0/z**2)**2 + e2[3]*a0/z**2 + e2[4])) == 0
        model = {"polynomial": str(h), "even_coefficients_descending": cs,
                 "genus": 2, "elliptic_weierstrass": [e1, e2]}
        if with_ranks:
            from compute.pari_genus1 import gp_available, quartic_points
            from compute.omega3_towers import identify
            if not gp_available():
                raise RuntimeError("PARI/GP is required for --ranks")
            model["elliptic_arithmetic"] = []
            for cubic in (cs, cs[::-1]):
                arithmetic = quartic_points(cubic, H=30)
                identity = identify(cubic)
                assert arithmetic.get("rank_lo") == arithmetic.get("rank_hi") == 1, arithmetic
                assert identity[1] is not None, identity
                model["elliptic_arithmetic"].append({
                    "label": identity[1], "rank_bounds": [arithmetic["rank_lo"], arithmetic["rank_hi"]],
                    "torsion_order": arithmetic["torsion_order"]})
        result["models"][name] = model

    old_box = O.BOX
    try:
        O.set_box((1, 1, 1))
        for index, (name, invert) in CASES.items():
            record = ledger["classes"][index]
            assert "towers" in record      # entry 134 killed these eight classes (A3.SQ); the maps remain valid maps
            components, live = O.frame_factors(record["cand"], record["frame"])
            assert len(components) == 1 and not live
            phi, dg, dh = components[0]
            assert (dg, dh) == (3, 3)
            # h' = 1/h where necessary; multiply by h'^3 on h' != 0.
            p = sp.expand(sp.cancel(O.th**3 * phi.subs(O.th, 1/O.th))) if invert else phi
            q = 0
            for (a, b), coefficient in sp.Poly(p, O.tg, O.th).terms():
                assert (a + b) % 2 == 0 and a - b + 2 >= 0
                q += coefficient * x**((a-b+2)//2) * y**b
            q = sp.expand(q)
            assert sp.expand(q.subs({x: O.tg**2, y: O.tg*O.th}) - O.tg**2*p) == 0
            assert sp.degree(q, x) == 2
            a, b, c = sp.Poly(q, x).all_coeffs()
            disc = sp.expand(b*b - 4*a*c)
            assert sp.expand((2*a*x+b)**2 - disc - 4*a*q) == 0
            even = sp.cancel((z-1)**6 * disc.subs(y, (z+1)/(z-1)) / 64)
            h = sp.sympify(result["models"][name]["polynomial"], locals={"z": z})
            expected = sp.cancel(z**6*h.subs(z, 1/z)) if invert else h
            assert sp.expand(even - expected) == 0
            result["classes"].append({
                "id": f"111:{index}", "candidate": record["cand"], "frame": record["frame"],
                "source_record_sha256": hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "phi": str(phi), "invert_second_ratio": invert,
                "quadratic_quotient": str(q), "discriminant": str(disc),
                "model": name, "reciprocal_even_model": invert,
                "map": "x=g^2, y=g*h_prime, W=2*a(y)*x+b(y), z=(y+1)/(y-1), v=(z-1)^3*W/8"
                       + ("; then (z,v) -> (1/z,v/z^3)" if invert else ""),
            })
    finally:
        O.set_box(old_box)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ranks", action="store_true")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.ranks)
    raw = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        ARTIFACT.write_text(raw, encoding="utf-8", newline="\n")
    elif args.check:
        assert json.loads(ARTIFACT.read_text(encoding="utf-8")) == result, "stale quotient artifact"
    else:
        print(raw)
    print("Verified eight affine quotient maps, two smooth genus-2 models, and four elliptic quotient identities.")
    if args.ranks:
        print("PARI: all four elliptic quotients have rank 1; the common 123a1 factor has rational 5-torsion.")
    print("No complete rational-point enumeration or class exclusion is claimed.")


if __name__ == "__main__":
    main()
