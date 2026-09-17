"""Replay entry 148's Hodge-index obstruction from the published matrix.

The source is archived byte-for-byte under papers/auel-singer-2026.  The
default audit uses exact arithmetic on the five-row witness.  --full also
asks PARI/GP for an exact rational congruence of the entire matrix, checks
that congruence, and reports its inertia.  No network access is needed.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "papers/auel-singer-2026/IntersectionMatrix.m.gz"
SOURCE_SHA256 = "9e019c79166b152939bb1d57e8f03ff720d5ba88a1b2e39fc15efda57b0af075"
WITNESS_ROWS = (321, 642, 704, 710, 812)  # source uses one-based indexing


def load_matrix():
    raw = gzip.decompress(SOURCE.read_bytes())
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("published matrix checksum mismatch")
    text = raw.decode("ascii")
    blocks = re.findall(r"\[([^\[\]]+)\]", text)
    if re.sub(r"\[[^\[\]]+\]", "", text).strip():
        raise ValueError("unexpected text outside matrix rows")
    rows = [list(map(int, row.split())) for row in blocks]
    if len(rows) != 1204 or any(len(row) != 1204 for row in rows):
        raise ValueError("expected a 1204 by 1204 matrix")
    if any(rows[i][j] != rows[j][i] for i in range(1204) for j in range(i)):
        raise ValueError("published matrix is not symmetric")
    return rows


def witness(rows):
    indices = [i - 1 for i in WITNESS_ROWS]
    return [[rows[i][j] for j in indices] for i in indices]


def full_inertia(rows):
    """PARI's rational square reduction, with the resulting identity checked."""
    from compute.pari_genus1 import GP, gp_available

    if not gp_available():
        raise RuntimeError("--full requires PARI/GP (set MSS3_GP)")
    literal = "[" + ";".join(",".join(map(str, row)) for row in rows) + "]"
    script = (
        'default(parisizemax, "2G");\n'
        'default(parisize, "512M");\n'
        "{\n"
        f"M = {literal};\n"
        "[U, d] = qfgaussred(M, 1);\n"
        'if(U~ * matdiagonal(d) * U != M, error("congruence failed"));\n'
        # Nonzero determinant modulo one prime certifies invertibility over Q,
        # avoiding the much larger exact determinant of this 1204-square U.
        'if(matdet(U * Mod(1, 1000003)) == 0, error("basis not certified"));\n'
        'print("INERTIA ", sum(i=1,#d,d[i]>0), " ", '
        'sum(i=1,#d,d[i]<0), " ", sum(i=1,#d,d[i]==0));\n}\n'
    )
    result = subprocess.run(
        [GP, "-q", "-f"], input=script, text=True, capture_output=True,
        timeout=600,
    )
    match = re.search(r"^INERTIA (\d+) (\d+) (\d+)$", result.stdout, re.M)
    if result.returncode or not match:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return dict(zip(("positive", "negative", "zero"), map(int, match.groups())))


def main():
    import sympy as sp

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="also audit the full matrix in PARI")
    args = parser.parse_args()
    rows = load_matrix()
    gram = sp.Matrix(witness(rows))
    lower, diagonal = gram.LDLdecomposition(hermitian=False)
    assert lower * diagonal * lower.T == gram and lower.det() == 1
    report = {
        "source_sha256": SOURCE_SHA256,
        "witness_rows_1based": WITNESS_ROWS,
        "witness_gram": witness(rows),
        "witness_diagonal_congruence": [str(diagonal[i, i]) for i in range(5)],
        "witness_inertia": {
            "positive": sum(bool(diagonal[i, i] > 0) for i in range(5)),
            "negative": sum(bool(diagonal[i, i] < 0) for i in range(5)),
            "zero": sum(diagonal[i, i] == 0 for i in range(5)),
        },
    }
    if args.full:
        report["full_inertia"] = full_inertia(rows)
        report["full_rank"] = sum(report["full_inertia"][k] for k in ("positive", "negative"))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
