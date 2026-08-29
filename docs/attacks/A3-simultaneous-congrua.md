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

## 2.5 The $\mathbb{Z}[i]$ / S-unit front (W10): the six-term equation, degenerate subsums, and the $\omega = 1$ theorem

*(2026-08-28, the realignment's P1. Machine:
`compute/zi_additive.py`; checks `a3.zi_reformulation`,
`a3.degenerate_subsums`, `a3.omega1_theorem`.)*

**The reformulation (A3-S1, pinned).** $D(m) = \{\,|\mathrm{Im}(z^2)|
: z \in \mathbb{Z}[i],\ |z|^2 = m^2\,\}$, and with $w_j = z_j^2$
(so $|w_j| = m^2$ and $\bar w_j = m^4/w_j$), a signed additive
relation $\varepsilon_1 d_1 + \varepsilon_2 d_2 + \varepsilon_3 d_3
= 0$ is exactly the **six-term vanishing sum**
$$\textstyle\sum_j \varepsilon_j\bigl(w_j - m^4/w_j\bigr) = 0$$
on the norm-$m^4$ torus — S-unit-equation habitat.

**Lemma A3.4 (equal-modulus three-term rigidity in $\mathbb{Q}(i)$;
PROVEN).** No three nonzero elements of $\mathbb{Q}(i)$ of equal
absolute value satisfy $\pm a \pm b \pm c = 0$. *Proof.* Absorbing
signs, $a + b = c$; dividing by $c$: $\alpha + \beta = 1$ with
$|\alpha| = |\beta| = 1$, $\alpha, \beta \in \mathbb{Q}(i)$. Then
$1 = (1-\alpha)(1-\bar\alpha) = 2 - (\alpha + \bar\alpha)$, so
$\mathrm{Re}\,\alpha = \tfrac12$ and $\alpha = \tfrac12 \pm
\tfrac{\sqrt{-3}}{2} = \zeta_6^{\pm 1}$ — but $\zeta_6 \notin
\mathbb{Q}(i)$ (it generates $\mathbb{Q}(\sqrt{-3})$, and
$\mathbb{Q}(i) \cap \mathbb{Q}(\sqrt{-3}) = \mathbb{Q}$).
$\blacksquare$

**Proposition A3.5 (degenerate subsums; PROVEN).** Every vanishing
*proper* subsum of the six-term sum has size 2 or 4, and a size-2
vanishing forces its two terms to carry **equal congrua** ($d_i =
d_j$, the terms being $\pm w$ against $\mp w'$ with $w' \in \{w,
\bar w, -w, -\bar w\}$); size-4 vanishings are complements of
size-2. In particular a genuine additive triple of distinct
positive congrua yields a **nondegenerate** vanishing sum — the
right-shaped input for S-unit machinery. *Proof.* All six terms
have modulus $m^2 \ne 0$ (sizes 1, 5 impossible); size 3 is
impossible by Lemma A3.4; a size-2 relation between two terms of
equal modulus forces the stated proportionality, and each of the
four cases gives $|\mathrm{Im}\,w| = |\mathrm{Im}\,w'|$.
$\blacksquare$ (Exhaustive exact scan: 1372 sign/point
configurations per sample center, all 924 vanishing subsums per
center classified — `a3.degenerate_subsums`.)

**Theorem A3.6 (the $\omega = 1$ theorem — the first unconditional
slice of Conjecture A3.C; PROVEN).** Let $m = 2^s r p^a$ where $r$
is a product of primes $\equiv 3 \pmod 4$ and $p \equiv 1 \pmod 4$
is the only split prime dividing $m$. Then **no** signed relation
$\varepsilon_1 d_1 + \varepsilon_2 d_2 + \varepsilon_3 d_3 = 0$
holds with $d_i \in D(m)$ (repetitions allowed). In particular
$D(m)$ contains no additive triple; no 3×3 magic square with seven
square entries in the three-full-AP configuration has such a center
root; and *a fortiori* no MSS3 does. **Corollary: the center of any
MSS3 is divisible by at least two distinct primes $\equiv 1 \bmod
4$.**

*Proof.* (i) *Structure.* By unique factorization in
$\mathbb{Z}[i]$, every $z$ with $|z|^2 = m^2$ is $z = 2^s r\, u\,
\lambda^j \bar\lambda^{2a-j}$ with $u$ a unit and $\lambda$ a
Gaussian prime over $p$ (inert primes and $1+i$ contribute
scalars). Hence $z^2 = m^2 u^2 \sigma^{k}$ with $\sigma :=
(\lambda/\bar\lambda)^2 = \lambda^4/p^2$, $k = j - a \in [-a, a]$,
$u^2 = \pm 1$, and
$$D(m) = \{\, m^2\,|\mathrm{Im}\,\sigma^k| \;:\; 1 \le k \le a \,\}$$
(pinned exactly against `congrua_sets` on every single-split
$m \le 3000$).
(ii) *Reduction.* A signed relation becomes, after absorbing the
signs of $\mathrm{Im}\,\sigma^{k_i}$ into $\varepsilon_i' = \pm1$,
$$\textstyle\sum_i \varepsilon_i'\,(\sigma^{k_i} - \sigma^{-k_i}) = 0 .$$
If all three $k_i$ are equal this reads $(\varepsilon_1' +
\varepsilon_2' + \varepsilon_3')(\sigma^K - \sigma^{-K}) = 0$: the
first factor is an odd integer, the second is $2i\,\mathrm{Im}\,
\sigma^K \ne 0$ (note $\mathrm{Im}\,\lambda^4 = 2cs \ne 0$ since
$c = e^2 - f^2 \ne 0$ for odd $p$ and $s = 2ef \ne 0$) —
impossible. Otherwise multiply by $x^{K}$ at $x = \sigma$, $K =
\max k_i$: $\sigma$ is a root of the integer polynomial
$$Q(x) = \textstyle\sum_i \varepsilon_i'\,\bigl(x^{K + k_i} - x^{K - k_i}\bigr),$$
whose coefficients lie in $\{0, \pm1, \pm2, \pm3\}$ with
$\mathrm{lc}(Q) = \sum_{k_i = K}\varepsilon_i' \ne 0$ and $Q(0) =
-\mathrm{lc}(Q) \ne 0$.
(iii) *The contradiction.* $\sigma = \lambda^4/p^2$ is nonreal with
$\sigma\bar\sigma = 1$ and $\sigma + \bar\sigma = 2C/p^2$, $C =
\mathrm{Re}\,\lambda^4$; $\gcd(C, p) = 1$ (if $\lambda \mid 2C =
\lambda^4 + \bar\lambda^4$ then $\lambda \mid \bar\lambda^4$,
contradicting coprimality of $\lambda, \bar\lambda$). So the
minimal polynomial of $\sigma$ over $\mathbb{Q}$ is $x^2 -
(2C/p^2)x + 1$, with primitive integer form $R(x) = p^2x^2 - 2Cx +
p^2$. From $Q(\sigma) = 0$: $R \mid p^N Q$ in $\mathbb{Z}[x]$, and
by Gauss's lemma (contents: $R$ primitive, $\mathrm{cont}(Q) =:
\gamma \le 3$) this forces $Q = \gamma\, R\, T$ with $T \in
\mathbb{Z}[x]$. Comparing leading coefficients: $|\mathrm{lc}(Q)|
\le 3 < p^2 \le |\gamma\, p^2\, \mathrm{lc}(T)|$ — impossible for
$p \ge 5$. $\blacksquare$ (Machine: 224 exact sign/exponent
instances per prime, seven primes, all nonzero to $a = 6$;
`a3.omega1_theorem`.)

**Reading.** This is the additive desert's first *theorem*: an
infinite, natural family of center roots is now unconditionally
closed — the entire single-split-prime family, all powers, all
inert cofactors. The obstruction is exactly S-unit-shaped: the
relation would force the degree-2 non-integral unit $\sigma$ to
satisfy a bounded-coefficient polynomial identity, and contents
forbid it. The two-split-prime case ($\sigma_1, \sigma_2$
multiplicatively independent — a genuine rank-2 unit equation) is
the next target (A3-S2b); the desert data says its answer, too,
should be "never".

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
