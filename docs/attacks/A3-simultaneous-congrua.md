# A3 — Simultaneous congrua: the elliptic dictionary, the additive desert, and the descent gap

**Status:** §1 dictionary **PROVEN** (maps machine-verified; torsion
input PROVEN-CLASSICAL with PARI corroboration); §2 **VERIFIED** (a new
first-party exhaustive fact: the "additive desert"); §3 Theorem A3.K
**PROVEN** (explicit witness machine-verified over $\mathbb{Q}(i,\sqrt5)$,
rank input corroborated by PARI; Mordell–Weil machinery
PROVEN-CLASSICAL); §4 the gap question **OPEN**, sharply posed.
Verification: `python3 -m verify --only a3`.

## 1. The elliptic dictionary (all correspondences explicit)

Recall ([F2](../foundations/F2-aps-and-pythagorean.md)): an MSS3 with
center $m^2$ requires its four offsets to lie in
$D(m) = \{2ef : e^2+f^2 = m^2,\ e,f>0\}$. Over $\mathbb{Q}$, realizable
common differences of 3-APs of squares are exactly the **congruent
numbers** (areas of rational right triangles, up to square scaling), and
the bridge to elliptic curves is classical:

**Proposition A3.1.** For squarefree $n > 0$, the following are
equivalent: (i) $n$ is congruent (some rational right triangle has area
$n$); (ii) some rational 3-AP of squares has common difference $n$;
(iii) the curve $E_n : y^2 = x^3 - n^2 x$ has a rational point with
$y \neq 0$.

*Proof.* (i)⇔(ii): scaling by squares, F2.2 over $\mathbb{Q}$
(difference $d = 2ef = 4\cdot$area; $4$ is a square). (i)⇒(iii): a
triangle $(a,b,c)$, $ab = 2n$, maps to
$$x = \frac{nb}{c-a}, \qquad y = \frac{2n^2}{c-a},$$
which satisfies $y^2 = x^3 - n^2x$ — for the parametrized family
$(a,b,c) = \lambda(m^2{-}k^2,\, 2mk,\, m^2{+}k^2)$ this is the polynomial
identity $\big(m^2(m^2-k^2)^2\big)^2 = \big(m^2(m^2-k^2)\big)^3 -
\big(mk(m^2-k^2)\big)^2\cdot m^2(m^2-k^2)$, machine-verified; the general
case follows by $\lambda$-homogeneity (degrees match: $x, y$ scale by
$\lambda^2, \lambda^3$ and $n$ by $\lambda^2$). (iii)⇒(i): from $(x,y)$,
$y \ne 0$, set
$$a = \frac{x^2 - n^2}{y}, \qquad b = \frac{2nx}{y}, \qquad
c = \frac{x^2 + n^2}{y}:$$
then $a^2 + b^2 = c^2$ *identically*, and $\tfrac{ab}{2} - n =
n\,\frac{x^3 - n^2x - y^2}{y^2} = 0$ on the curve — both machine-verified
identities. (Degenerate $a$ or $b = 0$ forces $y^2 = x^3 - n^2x$ with
$x \in \{0, \pm n\}$, i.e. $y = 0$.) ∎

**Torsion input (PROVEN-CLASSICAL; PARI-verified for samples).**
$E_n(\mathbb{Q})_{\mathrm{tors}} = \{O, (0,0), (\pm n, 0)\}$, so
"$y \neq 0$ rational point" ⇔ $\operatorname{rank} E_n(\mathbb{Q}) > 0$.

**Corollary A3.2 (the four-twist necessary condition).** If an MSS3 has
offsets $u, v$, then the four squarefree kernels of $u, v, u+v, u-v$ are
all congruent numbers, i.e. **four designated quadratic twists in the
family $E_d$ simultaneously have positive rank**. This alone is *not*
scarce — positive-rank twists have positive density — the scarcity lives
in the same-$m$ realization, quantified next.

## 2. The additive desert (first-party VERIFIED)

The same-$m$ requirement is: $u, v, u{+}v, u{-}v \in D(m)$ — an
**additive quadruple** inside one congrua set. Weaker patterns already
have configuration meaning:

| pattern in $D(m)$ | magic-square meaning |
|---|---|
| a pair $d_1 \ne d_2$ | 5 square entries (two full APs + center) |
| a triple $d_1, d_2, d_1{+}d_2$ | **7 square entries** (three full APs + center) |
| a quadruple $u, v, u{+}v, u{-}v$ | 9 = MSS3 |

**Theorem A3.3 (VERIFIED to $10^7$, 2026-08-28; previously
$3\times10^5$).** For every $m \le 10^7$: no two elements of $D(m)$
have their sum in $D(m)$ — zero additive triples across 99,288,935
pairs at 3,116,858 centers with $|D(m)| \ge 2$. In particular there is
no "three-full-AP" 7-square magic square with center root $\le 10^7$,
and *a fortiori* no MSS3 of that shape. (The 33× extension is the
block-sieve implementation `compute/additive_desert_ext.py`; frozen
artifact `data_additive_desert.json`, pinned and partially re-run
live by `a3.additive_ext`; the original `a3.desert` sub-bound rerun
stands unchanged. Historical statement to $3\times10^5$:
`compute.congrua_search 300000`, ~40 s.) This despite 69,398 values
of $m \le 3\times10^5$ having $|D(m)| \ge 4$ (the counting constraint
F2.7 satisfied in abundance; 20,806 already below $10^5$).

For calibration: the unique known 7-square square AB1 is **not** of the
three-AP type — it realizes a *pair* plus two half-APs
([F6](../foundations/F6-known-squares.md)). The additive desert says the
pair→triple step, which naive counting would put at density
$\sim |D(m)|^2 \cdot (\text{chance a specific integer is in } D(m))$,
never fires below $10^5$. **Conjecture A3.C (CONJECTURED):** additive
triples do not exist for any $m$; equivalently, no 3×3 magic square has
seven square entries in the three-full-AP configuration. A proof of
A3.C would be a genuinely new partial impossibility theorem — note it is
*implied by* Conjecture 0.3-adjacent heuristics but is strictly weaker
than the full problem, hence a realistic intermediate target. (It does
not follow from Bremner's published classification as summarized to us;
provenance caveats apply.)

## 3. The descent gap: why $\mathbb{Q}(i, \sqrt n)$ succeeds (Theorem A3.K, derived independently)

Center-zero magic squares make the mechanism transparent. With $c = 0$
the Lucas entries are $\{0, \pm u, \pm v, \pm(u{+}v), \pm(u{-}v)\}$.

**Lemma A3.4.** A field $K$ (char 0) admitting a center-zero magic
square of nine distinct squares contains $i = \sqrt{-1}$.
*Proof.* $u \ne 0$ and both $u$ and $-u$ are squares, so $-1 =
(-u)/u$ is a ratio of squares. ∎

**Lemma A3.5 (reduction to congruent-number-1 over $K$).** Center-zero
squares over $K \ni i$ correspond (up to square scaling) to $x \in K$
with $x, x{-}1, x{+}1$ all squares in $K$ — i.e. to 3-APs of squares
with difference 1 *and square middle term*. Over any field this forces a
$K$-point with $y \ne 0$ on $E_1 : y^2 = x^3 - x$ together with a
2-descent condition; over $\mathbb{Q}$ it is dead: $E_1(\mathbb{Q})$ has
rank 0 (Fermat, [F3.2](../foundations/F3-no-four-term-ap.md)).
*Proof sketch of the correspondence:* scale $(u,v) \to (u/v, 1)$;
$u/v, u/v \pm 1$ squares reproduce the offsets; conversely clear
denominators. The 3-AP $(x{-}1, x, x{+}1)$ of squares is the classical
congruent-number-1 configuration. ∎

**Rank bookkeeping over quadratic and biquadratic fields
(PROVEN-CLASSICAL, proof included at the $\otimes\mathbb{Q}$ level).**
For an elliptic curve $E/\mathbb{Q}$ and squarefree $d$:
$$\operatorname{rank} E(\mathbb{Q}(\sqrt d)) =
\operatorname{rank} E(\mathbb{Q}) + \operatorname{rank} E^{(d)}(\mathbb{Q}),$$
where $E^{(d)}$ is the quadratic twist. *Proof.* $V = E(\mathbb{Q}(\sqrt
d)) \otimes \mathbb{Q}$ splits under $\operatorname{Gal} = \{1,\sigma\}$
into $V^+ \oplus V^-$; $V^+ = E(\mathbb{Q})\otimes\mathbb{Q}$; the
explicit isomorphism $\varphi : E \to E^{(d)}$, $(x, y) \mapsto (dx,
d^{3/2} y)$ — for $E: y^2 = x^3 + Ax$ this is the machine-verified
identity $(dx)^3 + Ad^2(dx) = d^3(x^3+Ax)$ — is defined over
$\mathbb{Q}(\sqrt d)$ and anti-commutes with $\sigma$, giving
$V^- \cong E^{(d)}(\mathbb{Q})\otimes\mathbb{Q}$. ∎
For the congruent-number family this reads $E_1^{(d)} = E_d$ (same
machine-verified identity), and for the biquadratic field
$K_n = \mathbb{Q}(i, \sqrt n)$, applying the decomposition over the three
quadratic subfields $\mathbb{Q}(i), \mathbb{Q}(\sqrt n),
\mathbb{Q}(\sqrt{-n})$:
$$\operatorname{rank} E_1(K_n) =
\underbrace{\operatorname{rank} E_1(\mathbb{Q})}_{0}
+ \underbrace{\operatorname{rank} E_1^{(-1)}(\mathbb{Q})}_{0\ (E_1^{(-1)} \cong E_1 \text{ via } x \mapsto -x)}
+ \operatorname{rank} E_n(\mathbb{Q})
+ \operatorname{rank} E_{-n}(\mathbb{Q})
= 2 \operatorname{rank} E_n(\mathbb{Q}),$$
using $E_{-n} = E_n$ (the equation depends on $n^2$). So **for congruent
$n$, $\operatorname{rank} E_1(K_n) \ge 2 > 0$**: congruent-number-1
machinery comes alive over $K_n$, while over $\mathbb{Q}(i)$ alone the
rank is $0 + 0 = 0$ — dead. Combined with Lemma A3.4 (any suitable $K$
contains $i$; a quadratic $K$ must *be* $\mathbb{Q}(i)$):

**Theorem A3.K.** No quadratic field admits a center-zero magic square
of nine distinct squares; for every congruent number $n$ the quartic
field $\mathbb{Q}(i, \sqrt n)$ does. **Fully explicit witness for
$n = 5$** (from the area-5 triangle $(3/2, 20/3, 41/6)$, i.e. the 3-AP
$(31/6)^2, (41/6)^2, (49/6)^2$ of difference 20, rescaled):
$$L(0,\ 41^2,\ 720) \;=\;
\begin{pmatrix} 1681 & -2401 & 720 \\ -961 & 0 & 961 \\ -720 & 2401 & -1681 \end{pmatrix},$$
all eight lines summing to 0, with the nine distinct entries equal to the
squares of
$$41,\quad 49i,\quad 12\sqrt5,\quad 31i,\quad 0,\quad 31,\quad
12i\sqrt5,\quad 49,\quad 41i \in \mathbb{Q}(i,\sqrt5).$$
`a3.kominers_witness` verifies every one of these statements by exact
arithmetic in the algebra $\mathbb{Q}[i,s]/(i^2{+}1,\, s^2{-}5)$, and the
witness joins the falsification gauntlet as anchor target (e). (This
recovers, by an independent derivation, the shape of results credited to
Kominers — SUMMARY-ONLY provenance; our proof and witness stand on their
own.)

## 4. The gap, sharply posed

The two lemmas localize exactly what $\mathbb{Q}$ withholds:

1. **The real place**: center-zero (the configuration that decouples the
   four AP conditions into one curve) requires $i \in K$ — over
   $\mathbb{Q}$, entries are nonnegative and the center is forced to
   $S/3 > 0$, re-coupling everything through one hypotenuse $m$.
2. **Rank over $\mathbb{Q}(i)$**: even granting $i$, the driver curve
   $E_1$ stays rank 0 over $\mathbb{Q}(i)$; positivity of rank is bought
   only by the second extension $\sqrt n$ — which simultaneously
   destroys the ring of integers' rigidity that the integer problem
   lives in.

**Open question A3-Q (the descent gap).** The integer problem sits at
the intersection: it needs the additive quadruple *inside one*
$D(m) \subset \mathbb{Z}$ (Theorem A3.3's desert), while every field
large enough to break the desert also breaks the archimedean/integral
structure that defines the problem. Formalize this trade-off: is there a
Galois-cohomological invariant (a Selmer-type obstruction attached to the
four-twist system $\{E_u, E_v, E_{u+v}, E_{u-v}\}$ with the same-$m$
gluing) whose nonvanishing over $\mathbb{Q}$ explains the desert? A
positive answer would upgrade A3.C from conjecture to theorem and would
be the first genuinely global obstruction specific to this problem.

## 5. What the verify script proves mechanically

`verify/checks/a3_congrua.py`: the dictionary identities (both maps, by
complete grids); the $(3,4,5) \mapsto (12, 36) \in E_6$ example; the
additive desert re-run to a bound each FULL pass (the $10^5$ statement
is reproducible via `python3 -m compute.congrua_search 100000`, ~13 s);
the twist identity grid; the $\mathbb{Q}(i,\sqrt5)$ witness in exact
quartic-algebra arithmetic; PARI corroboration (SKIPs cleanly if `gp`
absent) of: ranks $0,0,0,1,1,1$ for $E_{1,2,3,5,6,7}$, torsion
$(\mathbb{Z}/2)^2$, and the point $(-4, 6) \in E_5(\mathbb{Q})$.
