"""Prime-column integration, cancellation identities, and survivor provenance."""
from collections import Counter
import gzip
from itertools import product
import json
from unittest.mock import patch

from ..framework import check, require

DOC = "docs/attacks/A10-cancellation-descent.md"


@check("a3.prime_column_engine", DOC)
def prime_column_engine(ctx):
    from compute import omega3 as O
    from compute.prime_column import column_certificate
    from compute.research_inventory import ROOT, SOURCES, load_source
    rows = load_source(ROOT / SOURCES["111"])["classes"]
    dead = next(r["cand"] for r in rows if column_certificate(r["cand"][:4]))
    survivor = next(r["cand"] for r in rows if r["verdict"] == "finite")
    saved = O.HIGH_DEGREE_ROUTE
    for decide in (O.decide_class, O.decide_class_fast):
        with patch.object(O, "decide_frame", side_effect=AssertionError("curve engine entered on excluded class")):
            verdict, frames = decide(dead)
        require(verdict == "dead" and len(frames) == 3)
        require(all(f["route"] == "prime_column" and
                    f["prime_column"] == column_certificate(dead[:4]) for f in frames.values()))
        for cand, kwargs in ((survivor, {}), (dead, {"prime_filter": False})):
            with patch.object(O, "decide_frame", return_value={"verdict": "finite"}) as geometry:
                verdict, frames = decide(cand, **kwargs)
                require(verdict == "finite" and geometry.call_count == 3, "survivor or explicit geometry replay was blocked")
        require(O.HIGH_DEGREE_ROUTE == saved, "decision policy leaked")
    ctx.note("both decision entry points reject before geometry, preserve certificates, and delegate survivors; historical geometry replay remains explicit")


@check("a3.cancellation_patterns", DOC)
def cancellation_patterns(ctx):
    import sympy as sp
    from compute.cancellation_patterns import (LEADING_ROWS, LEADING_RAYS, additive_witness,
                                               column_pattern, square_residue_parameters)
    from compute.prime_column import column_certificate
    bound = ctx.bound(full=5, fast=3)
    checked = 0
    for weights in product(range(-bound, bound + 1), repeat=4):
        fails = column_certificate([[w] for w in weights]) is not None
        if fails:
            try:
                additive_witness(weights)
            except ValueError:
                continue
            require(False, ("invalid weight accepted", weights))
        ys = additive_witness(weights)
        for w, y in zip(weights, ys):
            require(y and (min(y) == -abs(w) if w else min(y) >= 0), (weights, y))
        # Independent coefficient-by-coefficient replay of both Laurent identities.
        for row in LEADING_ROWS["*"]:
            for power in set().union(*(y.keys() for y in ys)):
                require(sum(c*y.get(power, 0) for c, y in zip(row, ys)) == 0, (weights, row, power))
        pattern = column_pattern(weights)
        if pattern["role"] not in ("zero", "*"):
            g = pattern["gap"]
            require(pattern["unit_congruence_power"] == 2*g)
            require(4*pattern["maximum"] >= 2*g)
        checked += 1
    # Every three-maximum row follows from the original two equations after
    # discarding only the deficient coordinate; no extra relation is assumed.
    matrix = sp.Matrix(LEADING_ROWS["*"])
    for role, ray in LEADING_RAYS.items():
        missing = "ABCD".index(role)
        basis = matrix.col_join(sp.eye(4)[missing, :])
        require(basis.rank() == 3)
        for row in LEADING_ROWS[role]:
            require(sum(a*b for a, b in zip(row, ray)) == 0)
            require(row[missing] == 0 and basis.col_join(sp.Matrix([row])).rank() == 3)
    # Exact identity behind CP.3, including the sign from inversion.
    t, h = sp.symbols("t h", nonzero=True)
    for b in (-3, -2, -1, 1, 2, 3):
        m = abs(b)
        z = t**(2*b)*h
        q = -1/h if b > 0 else h
        error = t**(4*m)*h if b > 0 else -t**(4*m)/h
        require(sp.cancel(t**(2*m)*(z-1/z)-q-error) == 0, (b, "unit identity"))
    # Exhaustive leading-square solutions, compared against the role formulas.
    finite_field_checks = 0
    for p in (5, 13, 17, 29, 37, 41, 73, 89, 97):
        squares = {x*x % p for x in range(p)}
        observed = {role: set() for role in "ABCD*"}
        for u, v in product(range(p), repeat=2):
            vals = (u, v, (u+v) % p, (u-v) % p)
            if not any(vals) or not all(x in squares for x in vals):
                continue
            zeros = [i for i, x in enumerate(vals) if not x]
            require(len(zeros) <= 1)
            role = "ABCD"[zeros[0]] if zeros else "*"
            observed[role].add(v*pow(u, -1, p) % p if role == "*" else 1)
            finite_field_checks += 1
        for role in observed:
            require(observed[role] == set(square_residue_parameters(role, p)), (p, role, observed))
        require(bool(observed["C"]) == (p % 8 == 1), (p, "C/D mod 8"))
    ctx.note(f"{checked} signed Laurent weight controls; exact unit/error identities and all role syzygies; {finite_field_checks} finite-field square vectors")


@check("a3.research_inventory", "docs/RESEARCH-INVENTORY.md")
def research_inventory(ctx):
    from compute.cancellation_patterns import LEADING_ROWS
    from compute.prime_column import column_certificate
    from compute.research_inventory import ARTIFACT, REPORT, ROOT, SOURCES, build, digest, load_source, render
    data = build()
    stored = json.loads(gzip.decompress(ARTIFACT.read_bytes()))
    require(stored == data, "survivor artifact is stale")
    require(REPORT.read_text(encoding="utf-8") == render(data), "research report is stale")
    require(Counter(r["shape"] for r in stored["classes"]) == {"111": 154, "211": 1388, "311": 1025})
    require(len({r["id"] for r in stored["classes"]}) == 2567)
    require(Counter(tuple(r["binomial_height_recession_direction"] or []) for r in stored["classes"]) ==
            {(1, 1, 1): 2195, (1, 1, 2): 212, (1, 1, 3): 32, (1, 2, 1): 80, (1, 2, 2): 32, (1, 3, 2): 16})      # entries 123-131: the inventory rebased on the survivors of the three campaigns (entry 131: 4 more (1,1,1) tower kills)
    require(sum(not r["binomial_constraints"] for r in stored["classes"]) == 28)
    for shape, source in SOURCES.items():
        ledger = load_source(ROOT / source)
        expected = {i for i, r in enumerate(ledger["classes"]) if r.get("verdict", r.get("v")) == "finite"}
        actual = {r["source_index"] for r in stored["classes"] if r["shape"] == shape}
        require(actual == expected, (shape, "missing or invented open classes"))
        for r in (r for r in stored["classes"] if r["shape"] == shape):
            original = ledger["classes"][r["source_index"]]
            require(r["cand"] == original["cand"] and r["source_record_sha256"] == digest(original))
            require(column_certificate(r["cand"][:4]) is None)
            # Replay each unit-ratio exponent directly from the original labels,
            # not from candidate_patterns or the construction helper.
            direction = r["binomial_height_recession_direction"]
            require(direction and len(direction) == 3 and all(x > 0 for x in direction))
            labels, signs = original["cand"][:4], original["cand"][4:]
            for constraint in r["binomial_constraints"]:
                j = constraint["column"]
                i, other = constraint["pair"]
                sx = 1 if labels[i][j] > 0 else -1
                sy = 1 if labels[other][j] > 0 else -1
                ds = [sy*y-sx*x for x, y in zip(labels[i], labels[other])]
                require(ds == constraint["half_exponents"] and ds[j] == 0 and any(ds))
                require(constraint["height_powers"] == list(map(abs, ds)))
                require(constraint["height_constant"] == 1+abs(constraint["lambda"]))
                require(constraint["gap"]*direction[j] <= sum(abs(a)*x for a, x in zip(ds, direction)),
                        (r["id"], "height direction fails", constraint, direction))
                # Lambda is precisely the required ratio of leading offset units
                # after removing the two signed monomial prefactors.
                row = next(row for row in LEADING_ROWS[constraint["role"]] if row[i] and row[other])
                require(row[i]*signs[i]*sx*constraint["lambda"] + row[other]*signs[other]*sy == 0)
    ctx.note("all 5,232 open records included exactly once with source hashes; unit binomials and every unbounded height direction verified; generated report replayed")
