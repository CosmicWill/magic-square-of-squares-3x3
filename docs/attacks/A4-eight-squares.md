# A4 — The eight-square case (the open sub-problem)

**Status:** §1 taxonomy **PROVEN**; §2 class-by-class reductions
**PROVEN**, with the class-E kill **VERIFIED** deep into the range via
A3.3; §3 first-party sweep **VERIFIED** (no 8-square square with center
$\le 10^6$; AB1 re-found as unique ≥7 configuration; a structurally
significant *non-square-center* additive triple discovered); §4 the AB1
fiber curve **computed** (certified rank 3) and the 8-square finiteness
question posed precisely. Verification: `python3 -m verify --only a4`.

Whether a 3×3 magic square can have **eight** distinct square entries is
open (Boyer's prize; no example, no impossibility proof; CITED). It is
the natural stepping stone: strictly easier than the full problem,
strictly harder than anything currently proven.

## 1. Taxonomy (PROVEN)

**Theorem A4.1.** Up to the $D_4$ symmetry (Prop. 0.4), an 8-square
magic square belongs to exactly one of three classes, by the cell of its
unique non-square entry: **C** (center), **E** (edge midpoint), **K**
(corner). *Proof.* $D_4$ acting on the nine cells has orbits
$\{\text{center}\}$, the four corners, the four edge midpoints (orbit
sizes $1, 4, 4$ — verified mechanically), and preserves squareness of
entries. ∎

In Lucas coordinates $L(c, u, v)$, with
$\widetilde D(c) = \{d > 0 : c - d \text{ and } c + d \text{ both
squares}\}$ (so $\widetilde D(m^2) = D(m)$ by F2.2):

| class | center $c$ | forced pattern in $\widetilde D(c)$ | extra condition |
|---|---|---|---|
| C | **non-square** | full quadruple $u, v, u{+}v, u{-}v$ | — |
| E | square $m^2$ | triple $u, v, u{+}v \in D(m)$ | exactly one of $m^2 \pm (u{-}v)$ square |
| K | square $m^2$ | $v,\ u{-}v,\ u{+}v \in D(m)$, i.e. $d, e, 2d{+}e$ with $(d,e) = (v, u{-}v)$ | $m^2 + u$ square, $m^2 - u$ not |

*Proof.* Read off which $\pm$-pairs of offsets must be fully realized
when the unique non-square sits in the given cell; each line through the
center pairs an offset $w$ with $-w$, and a fully realized pair means
$c \pm w$ both square, i.e. $w \in \widetilde D(c)$ (F2.2 for square
centers; the same two-squares-averaging identity verbatim for non-square
$c$, where $c = (p^2+q^2)/2$). ∎

**Corollary A4.2 (class E is dead in range — VERIFIED).** A class-E
square requires an additive triple inside $D(m)$: by Theorem A3.3 (the
additive desert), none exists for $m \le 300{,}000$, i.e. **no class-E
8-square square has center $\le 9 \times 10^{10}$**. Conjecture A3.C
(no additive triple at square centers, ever) implies class E is empty.

## 2. The sweep (first-party, VERIFIED) and a structural discovery

`compute/eight_square_search.py` sweeps **all** centers $c \le 10^6$
(square and non-square), computes $\widetilde D(c)$, tests the three
class-enabling patterns, and runs a direct census of ≥7-square
configurations over all congrua pairs and slot assignments. Results
(re-run in reduced form by `a4.sweep` on every FULL pass):

1. **No additive quadruple** at any center $\le 10^6$: no MSS3 *and* no
   class-C 8-square in that range.
2. **No class-K pattern with its half-condition** at any square center
   $\le 10^6$.
3. With Corollary A4.2: **no 8-square magic square of any class with
   center $\le 10^6$** — by the taxonomy, this covers everything.
4. **AB1 is re-found** (validation) at $c = 425^2$, $(u, v) =
   (-41496, 138600)$, with **exactly 7** squares — and the census's only
   other $\ge 7$ hit in the entire sweep is $c = 850^2$ with
   $(u,v) = 4\cdot(-41496, 138600)$: **AB1's own $2^2$-scaling**,
   exactly as Prop. 0.5 predicts. So up to scaling, AB1 is the unique
   $\ge 7$-square configuration with center $\le 10^6$ — an independent
   confirmation, by different machinery, of its uniqueness in range.
5. **Discovery: the additive desert is a square-center phenomenon.**
   The sweep found exactly four additive triples to $10^6$ — **every one
   at a non-square center** (consistent, via an independent
   implementation, with A3.3): the primitive
   $$c = 157441:\quad 19800,\ 135240,\ 155040 \qquad (19800 + 135240 = 155040),$$
   its $4\times$ scaling at $c = 629764$, and another primitive triple at
   $c = 411625$. The first gives the fully magic square
   $L(157441,\, 135240,\, 19800)$ with **six** square entries
   ($c \pm 19800 = 371^2, 421^2$; $c \pm 135240 = 149^2, 541^2$;
   $c \pm 155040 = 49^2, 559^2$) and non-squares exactly at the center
   and the $u{-}v$ pair. So the additive pattern that never fires at
   square centers (A3.3, to $3\times10^5$) *does* fire at non-square
   centers — the desert is not a density accident but something about
   **square** centers specifically. This sharpens Conjecture A3.C and
   ties it directly to the arithmetic that keeps the main problem open.

## 3. The corner class and the AB1 fiber (computed)

Rational decompositions of $m^2$ are parametrized by
$e/m = \frac{1-t^2}{1+t^2}$, $f/m = \frac{2t}{1+t^2}$, with congruum
$$d(t) = 2ef = \frac{4t(1-t^2)}{(1+t^2)^2}\, m^2 .$$
Fix one realized congruum $v = d(t_1)$ and vary the second slot
$u + v = d(t_2)$: the *single* extra condition of the AB1-type
7-square configuration, $m^2 + u = m^2 + d(t_2) - d(t_1) = \square$,
becomes, after clearing $(1+t_2^2)^2$,
$$Y^2 \;=\; A\,(1+x^2)^2 + 4x(1-x^2), \qquad
A = 1 - \frac{4t_1(1-t_1^2)}{(1+t_1^2)^2},\qquad x = t_2$$
— an elliptic quartic over $\mathbb{Q}$ for each $t_1$, with the
built-in rational point $x = t_1$ ($Y = 1$; the degenerate
$u = 0$ slot). **The AB1 fiber**: $t_1 = 7/11$ (from
$425^2 = 180^2 + 385^2$, $t = f/(m+e) = 385/605$), where
$A = (41/85)^2 = (205/425)^2$ (the value $m^2 - v = 205^2$ in
disguise), giving after scaling by $85^2$:
$$(85Y)^2 = 1681x^4 - 28900x^3 + 3362x^2 + 28900x + 1681 .$$
AB1 itself is the point $x = 3/4$ (from $425^2 = 119^2 + 408^2$,
$t = 408/544$), with $q(3/4) = (1865/16)^2$, $1865 = 5 \cdot 373$
— machine-verified. PARI (`ellfromeqn` + `ellrank`, SKIP-cleanly
checked): the Jacobian is
$$y^2 = x^3 + 3362x^2 - 846513044\,x + 2769975186072,$$
minimal model $y^2 = x^3 - 53142545x + 58165355025$, torsion
$(\mathbb{Z}/2)^2$, **certified rank 3** with explicit generators. So
the AB1-type 7-square configurations over this fiber form an infinite
(rank-3) family of candidates, on which the *second* condition
($m^2 + (u - 2v)\cdot$… the eighth square) is an independent
square-condition — a second 2-cover, generically of genus $\ge 2$ over
the fiber. **Open Task A4-T1:** write the eighth-square condition on
this fiber explicitly as a curve and determine its genus; if $\ge 2$,
Faltings gives finiteness of 8-square candidates *on the AB1 fiber* —
which would be the first finiteness theorem specific to the 8-square
problem (conditional on nothing).

## 4. Verdict and targets

- Class E: dead to center $9 \times 10^{10}$ (A3.3), conjecturally
  empty (A3.C) — **the most promising impossibility sub-target in the
  whole program**, since it is a pure statement about additive structure
  of congrua at square centers.
- Classes C, K: dead to center $10^6$ (sweep); each reduces to a
  precise Diophantine pattern (quadruple at non-square centers; the
  $d, e, 2d{+}e$ pattern + half-condition) that future sweeps or descent
  attempts can attack in isolation.
- The 157441 example is the sharpest known witness that these patterns
  are *possible* in principle — impossibility proofs must use the
  square-ness of the center, not mere scarcity.

## 5. What the verify script proves mechanically

`verify/checks/a4_eight_squares.py`: the $D_4$ orbit computation
$\{1,4,4\}$; the sweep re-run to a bound with all three class-enablers
empty; AB1 re-found with exactly 7 squares and matching Lucas data; the
157441 triple verified digit by digit (all six squares named above);
fiber algebra: $A = (41/85)^2$, the quartic's values at $x = 7/11$ and
$x = 3/4$ are rational squares (exact `Fraction` arithmetic),
$d(3/4)\cdot 425^2 = 97104$; PARI: `ellfromeqn` reproduces the stated
Weierstrass model and `ellrank` certifies rank 3, torsion
$(\mathbb{Z}/2)^2$.
