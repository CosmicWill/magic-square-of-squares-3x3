"""Mechanical verification for docs/attacks/A3-simultaneous-congrua.md."""

import shutil
import subprocess
from itertools import product

from ..framework import Skip, check, require
from ..targets import LINES_3
from compute.congrua_search import stats

DOC = "docs/attacks/A3-simultaneous-congrua.md"


@check("a3.dictionary", DOC)
def _(ctx):
    """Proposition A3.1's maps as polynomial identities (complete grids),
    plus the (3,4,5) |-> (12,36) on E_6 example."""
    # triangle -> curve, parametrized family (degree 18 in m => 19+ points)
    R = range(20)
    for m in R:
        for k in range(8):
            n = m * k * (m * m - k * k)
            x = m * m * (m * m - k * k)
            y = m * m * (m * m - k * k) ** 2
            require(y * y == x ** 3 - n * n * x, f"map1 fails at {(m,k)}")
    # curve -> triangle: a^2+b^2 = c^2 identically; area identity
    for x, n in product(range(9), repeat=2):
        require((x * x - n * n) ** 2 + (2 * n * x) ** 2
                == (x * x + n * n) ** 2, "map2 pythagoras")
        require((x * x - n * n) * (2 * n * x) == 2 * n * (x ** 3 - n * n * x),
                "map2 area")
    require(36 * 36 == 12 ** 3 - 36 * 12, "example (3,4,5) -> (12,36) on E_6")
    ctx.note("both dictionary maps are polynomial identities")


@check("a3.desert", DOC)
def _(ctx):
    """Theorem A3.3: no additive triple d1, d2, d1+d2 inside any D(m),
    m <= bound (the 10^5 statement reproducible via compute.congrua_search)."""
    bound = ctx.bound(full=30000, fast=4000)
    triples, quads = stats(bound, verbose=False)
    require(triples == [] and quads == [], f"additive structure found: "
            f"{triples[:3]} {quads[:3]}")
    ctx.note("no additive triples/quadruples in any D(m) up to bound")


@check("a3.twist_identity", DOC)
def _(ctx):
    """The quadratic-twist change of variables and E_1^{(-1)} = E_1:
    (dx)^3 + A d^2 (dx) == d^3 (x^3 + A x); (-x)^3 - (-x) == -(x^3 - x)."""
    for d, x, A in product(range(6), range(6), range(-4, 5)):
        require((d * x) ** 3 + A * d * d * (d * x)
                == d ** 3 * (x ** 3 + A * x), "twist identity")
    for x in range(7):
        require((-x) ** 3 - (-x) == -(x ** 3 - x), "E1 self-twist")


# --- exact arithmetic in Q(i, sqrt5) = Q[i,s]/(i^2+1, s^2-5) -------------

def qmul(p, q):
    """(a, b, c, d) ~ a + b i + c s + d i s, s^2 = 5, i^2 = -1."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 + 5 * c1 * c2 - 5 * d1 * d2,
            a1 * b2 + b1 * a2 + 5 * c1 * d2 + 5 * d1 * c2,
            a1 * c2 + c1 * a2 - b1 * d2 - d1 * b2,
            a1 * d2 + d1 * a2 + b1 * c2 + c1 * b2)


@check("a3.kominers_witness", DOC)
def _(ctx):
    """Theorem A3.K's explicit witness: L(0, 41^2, 720) is a magic square
    of nine distinct squares of Q(i, sqrt5), verified in exact quartic
    algebra."""
    c, u, v = 0, 41 * 41, 720
    entries = [c + u, c - u - v, c + v,
               c - u + v, c, c + u - v,
               c - v, c + u + v, c - u]
    require(entries == [1681, -2401, 720, -961, 0, 961, -720, 2401, -1681])
    require(len(set(entries)) == 9, "entries not distinct")
    for line in LINES_3:
        require(sum(entries[i] for i in line) == 0, "not magic")
    roots = [(41, 0, 0, 0), (0, 49, 0, 0), (0, 0, 12, 0),
             (0, 31, 0, 0), (0, 0, 0, 0), (31, 0, 0, 0),
             (0, 0, 0, 12), (49, 0, 0, 0), (0, 41, 0, 0)]
    for e, r in zip(entries, roots):
        require(qmul(r, r) == (e, 0, 0, 0), f"root of {e} wrong")
    # the underlying 3-AP with difference 20 and square middle (area-5 triangle)
    require(41 ** 2 - 31 ** 2 == 720 and 49 ** 2 - 41 ** 2 == 720)
    ctx.note("center-zero MSS3 over Q(i, sqrt5) fully verified")


@check("a3.pari_ranks", DOC)
def _(ctx):
    """PARI corroboration (SKIP without gp): certified ranks of E_1..E_7
    are 0,0,0,0,1,1,1; torsion (Z/2)^2; (-4,6) lies on E_5."""
    if not shutil.which("gp"):
        raise Skip("PARI/GP not installed")
    script = ('for(k=1,7, E = ellinit([0,0,0,-k^2,0]); r = ellrank(E);'
              ' t = elltors(E); print(k, ";", r[1], ";", r[2], ";", t[2]));'
              ' print("pt;", ellisoncurve(ellinit([0,0,0,-25,0]), [-4,6]))')
    out = subprocess.run(["gp", "-q"], input=script, text=True,
                         capture_output=True, timeout=300).stdout
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    want = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1}
    seen = {}
    for l in lines:
        parts = l.split(";")
        if parts[0] == "pt":
            require(parts[1] == "1", "(-4,6) not on E_5")
        else:
            k, lo, hi, tors = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
            require(lo == hi == want[k], f"rank of E_{k}: [{lo},{hi}]")
            require(tors == "[2, 2]", f"torsion of E_{k}: {tors}")
            seen[k] = True
    require(len(seen) == 7, f"missing curves in gp output: {out!r}")
    ctx.note("gp certifies ranks 0,0,0,0,1,1,1 and (Z/2)^2 torsion")
