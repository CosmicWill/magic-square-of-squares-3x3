"""Minimal stdlib check framework for the magic-square-of-squares repository.

Every mathematical document in docs/ names the checks that mechanically verify
its computationally checkable content.  A check is a plain function registered
with @check; the runner (``python3 -m verify``) executes them and reports
PASS / FAIL / SKIP.

Contract for checks:

    @check("f4.mod72", doc="docs/foundations/F4-congruences-mod-72.md")
    def _(ctx):
        n = ctx.bound(full=10**6, fast=10**4)   # profile-scaled bound
        require(some_condition, "what failed")
        ctx.note("anything worth printing in the report")

* ``require(cond, msg)`` raises Failure -> check FAILS.
* ``raise Skip(reason)``  -> check SKIPS (e.g. optional dependency missing).
* Bounds requested through ctx.bound() are printed in the report so documents
  can cite the FULL bound while CI runs the FAST one.

Profiles: FULL (default, the bounds cited in the docs), FAST (pre-commit
gate), CI (FAST bounds + machine-readable summary).  The runner exits nonzero
on any FAIL in every profile.
"""

from __future__ import annotations

import time
import traceback
from dataclasses import dataclass, field


class Failure(Exception):
    """A mathematical requirement of a check did not hold."""


class Skip(Exception):
    """The check cannot run in this environment (reason in args)."""


def require(cond, msg="requirement failed"):
    if not cond:
        raise Failure(msg)


@dataclass
class Ctx:
    profile: str  # "FULL" | "FAST" | "CI"
    notes: list = field(default_factory=list)

    def bound(self, full, fast):
        """Return the profile-appropriate bound and record it for the report."""
        b = full if self.profile == "FULL" else fast
        self.notes.append(f"bound={b} (FULL={full}, FAST={fast})")
        return b

    def note(self, msg):
        self.notes.append(str(msg))


@dataclass
class Result:
    name: str
    doc: str
    status: str  # "PASS" | "FAIL" | "SKIP"
    seconds: float
    detail: str
    notes: list


REGISTRY: list[tuple[str, str, object]] = []


def check(name, doc):
    """Register a check.  ``name`` is dotted (module.short), ``doc`` the
    document whose claims it verifies."""

    def deco(fn):
        REGISTRY.append((name, doc, fn))
        return fn

    return deco


def run_all(profile="FULL", only=None):
    results = []
    for name, doc, fn in REGISTRY:
        if only and only not in name:
            continue
        ctx = Ctx(profile=profile)
        t0 = time.perf_counter()
        try:
            fn(ctx)
            status, detail = "PASS", ""
        except Skip as e:
            status, detail = "SKIP", str(e)
        except Failure as e:
            status, detail = "FAIL", str(e)
        except Exception:
            status, detail = "FAIL", "unexpected error:\n" + traceback.format_exc()
        results.append(
            Result(name, doc, status, time.perf_counter() - t0, detail, ctx.notes)
        )
    return results
