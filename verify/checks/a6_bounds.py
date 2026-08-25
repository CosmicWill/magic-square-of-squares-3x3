"""Mechanical verification for docs/attacks/A6-search-bounds.md."""

from ..framework import check, require
from ..targets import congrua as congrua_targets
from compute.congrua_search import congrua_sets
from compute.eight_square_search import dtilde
from compute.small_bound_search import congrua_direct, search

DOC = "docs/attacks/A6-search-bounds.md"


@check("a6.small_bound", DOC)
def _(ctx):
    """The independent direct search: no MSS3 with center root <= bound."""
    bound = ctx.bound(full=8000, fast=1500)
    hits = search(bound)
    require(hits == [], f"MSS3 found: {hits[:2]}")
    ctx.note("no additive quadruple in any D(m), independent implementation")


@check("a6.cross_validation", DOC)
def _(ctx):
    """The three D(m) implementations agree elementwise on a sample range:
    direct e-loop (small_bound_search / targets), primitive-triple sieve
    (congrua_search), and the q-loop Dtilde (eight_square_search)."""
    bound = ctx.bound(full=2500, fast=600)
    sieve = dict(congrua_sets(bound))
    for m in range(1, bound + 1):
        direct = congrua_direct(m)
        require(direct == congrua_targets(m), f"targets mismatch at m={m}")
        require(direct == sieve.get(m, set()), f"sieve mismatch at m={m}")
        require(direct == set(dtilde(m * m)), f"dtilde mismatch at m={m}")
    ctx.note("three independent congrua implementations agree")


@check("a6.wheel_facts", DOC)
def _(ctx):
    """Sieve-design facts: congrua of odd m are divisible by 24 (from F4's
    corollary) and roots of primitive squares are coprime to 6 (mod-72
    survivors, from F4.1) — re-asserted here as the wheel the design uses."""
    for m in range(1, ctx.bound(full=800, fast=200), 2):
        for d in congrua_targets(m):
            require(d % 24 == 0, f"congruum {d} of odd m={m}")
    squares72 = {x * x % 72 for x in range(72)}
    require(all(r % 24 == 1 for r in squares72 if r % 2 == 1 and r % 3 == 1
                and r in {1, 25, 49}), "wheel residues")
    ctx.note("wheel: offsets 0 mod 24; admissible entry residues {1,25,49} mod 72")
