"""Obstruction-predicate registry for the falsification gauntlet
(docs/protocol/sanity-checks.md).

Every candidate impossibility argument developed in docs/attacks/ is encoded
as a Predicate here (or in the attack's check module) and run against the
anchor targets by verify/checks/sanity_gauntlet.py.  A predicate that "rules
out" an object that exists is a broken argument, and the suite fails.
"""

from dataclasses import dataclass, field

from . import targets


@dataclass
class Target:
    name: str
    kind: str          # "integer3x3" | "integer4x4" | "fp" | "mod2n"
    payload: dict = field(default_factory=dict)


TARGETS = [
    Target("AB1 (7-square magic square)", "integer3x3",
           {"entries": targets.AB1, "square_count": 7}),
    Target("Euler 4x4 (16 distinct squares)", "integer4x4",
           {"entries": targets.EULER4}),
    Target("F_59 distinct-entry solution", "fp",
           {"p": 59, "cuv": targets.FP_WITNESSES[59]}),
    Target("F_499 distinct-entry solution", "fp",
           {"p": 499, "cuv": targets.FP_WITNESSES[499]}),
    Target("mod-2^32 witness", "mod2n", dict(targets.MOD2N_WITNESS)),
    # center-zero magic square of nine distinct squares over Q(i, sqrt5)
    # (docs/attacks/A3-simultaneous-congrua.md, Theorem A3.K; verified by
    # a3.kominers_witness).  Kills any obstruction argument that is
    # insensitive to the base field.
    Target("Q(i,sqrt5) center-zero solution", "number_field",
           {"field": "Q(i, sqrt5)", "c": 0, "u": 41 ** 2, "v": 720}),
]


@dataclass
class Predicate:
    """An obstruction claim.  `applies_to(target) -> bool` encodes its scope;
    `rules_out(target) -> bool` returns True when the argument would declare
    the target impossible.  For every target in scope, rules_out must be
    False — the targets exist."""
    name: str
    doc: str
    applies_to: object
    rules_out: object


PREDICATES: list[Predicate] = []


def register(pred: Predicate) -> Predicate:
    PREDICATES.append(pred)
    return pred


def violations(preds=None, targs=None):
    out = []
    for pr in (PREDICATES if preds is None else preds):
        for t in (TARGETS if targs is None else targs):
            if pr.applies_to(t) and pr.rules_out(t):
                out.append((pr.name, t.name))
    return out


# ---------------------------------------------------------------------------
# Standing predicates from the foundations layer.

def _f4_applies(t: Target) -> bool:
    # F4.1 constrains integer 3x3 magic squares ALL of whose entries are
    # squares (primitive).  None of the anchor targets is one (that is the
    # open problem), so this predicate is vacuous on the anchors — but its
    # scope encoding documents exactly what F4.1 does NOT claim: nothing
    # about 7-square near-misses, other orders, F_p, or residue rings.
    if t.kind != "integer3x3":
        return False
    from .targets import is_square
    return all(is_square(x) for x in t.payload["entries"])


register(Predicate(
    name="F4.1 congruence conditions (entries == 1 mod 24)",
    doc="docs/foundations/F4-congruences-mod-72.md",
    applies_to=_f4_applies,
    rules_out=lambda t: any(x % 24 != 1 for x in t.payload["entries"]),
))
