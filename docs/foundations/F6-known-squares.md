# F6 — The known landscape: near-misses and anchors

**Status:** the two anchor objects are **VERIFIED** (re-checked from raw
integers by the script, nothing trusted); the surrounding landscape claims
are **CITED** with provenance flags per
[references.md](../references.md).
Verification: `python3 -m verify --only f6`.

## 1. The Bremner–Sallows square AB1 (seven squares — the world record)

Found independently by A. Bremner and L. Sallows (~1997), labeled **AB1**
in Boyer's census:

$$\begin{pmatrix} 373^2 & 289^2 & 565^2 \\ 360721 & 425^2 & 23^2 \\ 205^2 & 527^2 & 222121 \end{pmatrix}
\qquad\text{magic sum } S = 541875.$$

**VERIFIED by `f6.ab1`:** all eight lines sum to $541875$; the seven
indicated entries are perfect squares; $360721$ and $222121$ are *not*
squares ($600^2 = 360000 < 360721 < 361201 = 601^2$;
$471^2 = 221841 < 222121 < 222784 = 472^2$); all nine entries distinct;
center $= 425^2 = S/3$ as [F1](F1-parametrization.md) forces.

**Structure in the coordinates of this repository** (verified in
`f1.anchor_ab1` and `f2.anchor_ab1`): AB1 $= L(c, u, v)$ with
$$c = 425^2, \qquad u = 373^2 - 425^2 = -41496, \qquad v = 565^2 - 425^2 = 138600,$$
and of the four offsets, exactly **two are congrua of 425**
($|v| = 138600 = 2\cdot180\cdot385$ and $|u+v| = 97104 = 2\cdot119\cdot408$,
from the decompositions $180^2+385^2 = 119^2+408^2 = 425^2$), while
$|u| = 41496$ and $|u-v| = 180096$ are *not* congrua — each of those two
offsets has exactly one square endpoint, which is precisely why AB1 has
$1 + 2\cdot2 + 2\cdot1 = 7$ squares and not 9. In the language of
[F2.5](F2-aps-and-pythagorean.md): AB1 realizes two of the four required
APs and half of each remaining one. Note $425 = 5^2 \cdot 17$ has
$\prod(2a_i+1) = 5\cdot3 = 15$, i.e. $|D(425)| = 7$ congrua available —
the failure is not for lack of congrua but because the *additive relations*
$d_3 = d_1+d_2$, $d_4 = d_1-d_2$ cannot be completed inside $D(425)$
(exhaustively confirmed by `f6.d425`).

**CITED landscape:** AB1 is, up to the $D_4$ symmetry and $k^2$-scaling,
the **only known** 3×3 magic square with $\ge 7$ square entries (Boyer's
census; Rathbun's enumeration of $> 1.16\times10^8$ squares with $\ge 6$
square entries found no other; Morgenstern's elliptic-curve point searches
likewise). The **eight-square case is open** — no example, no impossibility
proof; it is attacked in [A4](../attacks/A4-eight-squares.md).

## 2. Euler's 4×4 magic square of squares (1770)

From Euler's letter to Lagrange:

$$\begin{pmatrix} 68^2 & 29^2 & 41^2 & 37^2 \\ 17^2 & 31^2 & 79^2 & 32^2 \\ 59^2 & 28^2 & 23^2 & 61^2 \\ 11^2 & 77^2 & 8^2 & 49^2 \end{pmatrix}
\qquad\text{magic sum } 8515.$$

**VERIFIED by `f6.euler4`:** all ten lines (4 rows, 4 columns, both main
diagonals) sum to $8515$; all sixteen entries are distinct perfect squares.

Its role here is as a **falsification anchor**
([protocol/sanity-checks.md](../protocol/sanity-checks.md)): $n \times n$
magic squares of squares exist for $n = 4$ (Euler) and indeed for every
$n \ge 4$ (Rome–Yamagishi 2024, CITED). Therefore any candidate
impossibility argument for $n = 3$ **must use 3×3-specific structure** —
if an argument would apply equally to $n = 4$, it is wrong, full stop.

## 3. Known bounds (CITED)

- Any MSS3 has all entries $\ge 10^{14}$, equivalently all roots
  $\ge 10^7$ (L. Morgenstern 2007, reported on multimagie.com;
  SUMMARY-ONLY — treated as a search fact, never load-bearing).
- Our own first-party exhaustive micro-bound is established in
  [A6](../attacks/A6-search-bounds.md) with a reproducible certificate.

## 4. What the verify script proves mechanically

`verify/checks/f6_known_squares.py`: full re-verification of AB1 and
Euler's square from raw integers (line sums, squareness, non-squareness of
the two AB1 cells, distinctness); the $|D(425)| = 7$ computation; and the
exhaustive confirmation that no choice of $(u, v)$ with all four offsets in
$D(425) \cup -D(425)$ satisfies the additive relations (i.e. the center
$425^2$ admits **no** MSS3 at all, not just "AB1 barely fails").
