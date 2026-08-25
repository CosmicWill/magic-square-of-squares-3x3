"""The falsification gauntlet (docs/protocol/sanity-checks.md): every
registered obstruction predicate must be consistent with the anchor targets,
and the harness itself must be able to catch a broken predicate."""

from ..framework import check, require
from ..gauntlet import PREDICATES, TARGETS, Predicate, violations
from ..targets import is_square

DOC = "docs/protocol/sanity-checks.md"


@check("gauntlet.run", DOC)
def _(ctx):
    """No registered predicate rules out any anchor target in its scope."""
    v = violations()
    require(not v, f"gauntlet violations: {v}")
    ctx.note(f"{len(PREDICATES)} predicate(s) x {len(TARGETS)} target(s): clean")


@check("gauntlet.negative_control", DOC)
def _(ctx):
    """A deliberately wrong predicate ('no 3x3 magic square has >= 7 square
    entries') must be CAUGHT against AB1 — a gauntlet that cannot fail is
    not a gauntlet."""
    wrong = Predicate(
        name="negative control: 7+ squares impossible",
        doc=DOC,
        applies_to=lambda t: t.kind == "integer3x3",
        rules_out=lambda t: sum(is_square(x) for x in t.payload["entries"]) >= 7,
    )
    v = violations(preds=[wrong])
    require(any("AB1" in name for _, name in v), f"harness failed to catch: {v}")
    ctx.note("harness correctly flags the broken predicate against AB1")
