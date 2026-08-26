# A2 — The function-field analogue: magic squares of squares over $k[t]$

**Status:** §1 transfer results **PROVEN**; §2 Mason–Stothers
**PROVEN-CLASSICAL** (complete proof); §3 Theorem A2.3 **PROVEN**
(effective, Mason-based); §4 Lemma A2.L and Theorems A2.4/A2.5 **PROVEN**
(complete degree-descent proofs); §5 the full function-field conjecture
**OPEN**, with **VERIFIED** exhaustive small-field evidence and a precise
statement of the geometric frontier.
Verification: `python3 -m verify --only a2`.

## 0. Why function fields

$\mathbb{Z}$ and $k[t]$ are the two great Euclidean rings of number
theory, and the classical dictionary (size ↔ degree, descent-on-size ↔
descent-on-degree) usually makes the $k[t]$ side *strictly easier*: the
abc-inequality is a theorem there (Mason–Stothers), and "no rational
points" questions become "no rational curves" questions. **No treatment
of the magic square of squares problem over $k[t]$ appears in the
literature we could find** (SUMMARY-ONLY caveat, references.md). This
document sets the problem up, proves the analogues of our foundational
obstructions unconditionally, and isolates exactly what remains.

## 1. Formulation and transfer

Fix a field $k$ with $\operatorname{char} k \notin \{2, 3\}$. An MSS3
over $k[t]$ is a 3×3 magic square with nine entries that are squares in
$k[t]$, pairwise distinct; it is **nonconstant** if some entry is
nonconstant. F1 (Lucas) holds verbatim (its proof only divides by 3), so
an MSS3 is $L(c,u,v)$ with $c = M^2$ and, as in F2, four relations
$$P_i^2 + Q_i^2 = 2M^2, \qquad
\{Q_i^2 - M^2\}_{i=1..4} = \{u, v, u{+}v, u{-}v\}.$$

**Proposition A2.1 (constant center ⇒ constant square). PROVEN.** If
$M \in k$ (constant) then every solution of $P^2 + Q^2 = 2M^2$ has
$P, Q \in k$, hence the whole square is constant. *Proof.* Over
$\bar k$, $(P + iQ)(P - iQ) = 2M^2 \in \bar k^\times$ (the case $M = 0$
forces $P = \pm iQ$, giving $P^2+Q^2 = 0$ and all entries equal — not
admissible). A product of two polynomials lying in $\bar k^\times$ forces
both factors constant, so $P, Q$ are constant. ∎ Consequently a
nonconstant MSS3 has **nonconstant center root $M$**, and the F2-style
search over centers is exhaustive degree by degree.

**Transfer of F4/F5.** The mod-8/mod-3 congruence layer does *not*
transfer ($k[t]$ has no parity), consistent with F5's moral: those were
never going to be the load-bearing obstructions. What does transfer is
the multiplicative layer: $k[t]$ is a UFD, $k(i)[t]$ plays the role of
$\mathbb{Z}[i]$, and decomposition-counting becomes factorization
combinatorics of $M$ in $k(i)[t]$.

## 2. The Mason–Stothers theorem (complete proof)

**Theorem (Mason–Stothers).** Let $a + b + c = 0$ with $a, b, c \in
k[t]$ pairwise coprime, not all constant, and not all of $a', b', c'$
zero. Then
$$\max(\deg a, \deg b, \deg c) \;\le\; \deg \operatorname{rad}(abc) - 1,$$
where $\operatorname{rad}$ is the product of the distinct monic
irreducible factors.

*Proof.* Let $W = a b' - a' b$ (Wronskian). From $c = -(a+b)$:
$W(b, c) = W(c, a) = W(a, b) = W$ (direct computation using bilinearity
and $W(x,x) = 0$). If $W = 0$: $ab' = a'b$ with $\gcd(a,b) = 1$ forces
$a \mid a'$ and $b \mid b'$, so (degrees) $a' = b' = 0$, hence
$c' = 0$ — excluded. So $W \neq 0$. If $\pi^e \,\|\, a$ then
$\pi^{e-1} \mid a'$, so $\pi^{e-1}$ divides both terms of $W$; likewise
for $b$ (using $W = W(a,b)$) and $c$ (using $W = W(b,c)$). By pairwise
coprimality,
$$\frac{a}{\operatorname{rad} a} \cdot \frac{b}{\operatorname{rad} b}
\cdot \frac{c}{\operatorname{rad} c} \;\Big|\; W,$$
and $\deg W \le \deg a + \deg b - 1$. Hence
$\deg a + \deg b + \deg c - \deg\operatorname{rad}(abc) \le
\deg a + \deg b - 1$, i.e. $\deg c \le \deg\operatorname{rad}(abc) - 1$;
by the symmetry of $W$ the same bound holds for $\deg a$ and $\deg b$. ∎

(In characteristic $p$, "not all derivatives zero" fails only when
$a, b, c$ are all $p$-th powers, and one descends by Frobenius; our
applications below run this descent explicitly where needed.)

## 3. Theorem A2.3 — the $k[t]$ congruum theorem, effectively (Mason)

**Theorem A2.3. PROVEN.** Let $k$ have $\operatorname{char} k \notin
\{2,3\}$ and suppose $-1$ is **not** a square in $k$. Then no
nonconstant three-term AP of squares in $k[t]$ has a perfect-square
common difference: there is no coprime nonconstant solution of
$$A^2 + C^2 = 2B^2, \qquad C^2 - B^2 = T^2 .$$

*Proof.* Assume a solution with $n := \max(\deg A, \deg B, \deg C)
\ge 1$, pairwise coprime (a common irreducible of two of $A,B,C$ divides
the third, then all — normalize). Because $-1$ is not a square in $k$,
leading terms in $A^2 + C^2$ cannot cancel, so $\max(\deg A, \deg C) =
\deg B = n$. From the two relations, $B^4 = (AC)^2 + T^4$: indeed
$A^2 = B^2 - T^2$ and $C^2 = B^2 + T^2$, so
$(AC)^2 = B^4 - T^4$. The three terms $B^4, (AC)^2, T^4$ are pairwise
coprime, not all constant, and (char 0 or the Frobenius descent
below) Mason applies:
$$\max\big(4n,\; 2(\deg A + \deg C),\; 4\deg T\big) \;\le\;
\deg\operatorname{rad}(B \cdot AC \cdot T) - 1 \;\le\;
n + \deg A + \deg C + \deg T - 1 .$$
Again since $-1$ is not a square, $(AC)^2 + T^4$ has no leading
cancellation, so $4n = \max(2(\deg A + \deg C), 4\deg T)$. Two cases:

- $4n = 4\deg T$: then $\deg T = n$, and the display gives
  $4n \le n + \deg A + \deg C + n - 1 \le 4n - 1$ (using $\deg A, \deg C
  \le n$) — contradiction.
- $4n = 2(\deg A + \deg C) > 4 \deg T$: then $\deg A = \deg C = n$, and
  the display gives $4n \le 3n + \deg T - 1$, i.e. $\deg T \ge n + 1$,
  contradicting $4\deg T < 4n$.

In characteristic $p > 3$: if Mason is inapplicable then $B^4, (AC)^2,
T^4$ all have zero derivative, i.e. $B, AC, T$ are $p$-th powers (k
perfect; in general after a finite extension, which is harmless), and
since $A, C$ are coprime each is a $p$-th power; replacing
$(A,B,C,T)$ by the $p$-th roots gives a solution of the same system of
smaller degree — descend to the minimal one, where Mason applies. ∎

**Corollary.** Over $\mathbb{Q}[t]$: in any MSS3 (constant or not), no
offset $u, v, u\pm v$ is a nonzero perfect square — the function-field
mirror of F3.2b, with an *effective* proof for the nonconstant layer.
(*Proof:* a square offset's AP-triple $(P, Q, M)$, after dividing by its
gcd $g$ — note $g^2$ divides the offset, so the scaled difference is
still a square — is either nonconstant-coprime, killed by A2.3, or
constant, giving a rational 3-AP of distinct squares with square
difference, killed by F3.2b.* For general constant fields $k$ the
statement holds "modulo constants": square-offset APs are square
multiples of constant ones, and constant counterexamples genuinely occur,
e.g. $(0, 4, 1) = (0^2, 2^2, 1^2)$ with difference $2^2$ in
$\mathbb{F}_7$.)

## 4. The descent lemma, and the two unconditional theorems

Over $\bar k$ the unit headache vanishes (every constant is a square),
and Fermat's descent runs on degrees with remarkable smoothness:

**Lemma A2.L (pairs of conics; PROVEN — statement classical via genus
theory, proof here elementary and self-contained).** Let $\bar k$ be an
algebraically closed field, $\operatorname{char} \bar k \ne 2$, and let
$a, b, c, d \in \bar k^\times$ with $ad - bc \ne 0$. Then every solution
of
$$a X^2 + b Y^2 = P^2, \qquad c X^2 + d Y^2 = Q^2,
\qquad X, Y \in \bar k[t],\ \gcd(X, Y) = 1$$
has $X, Y$ (hence $P, Q$) constant.

*Proof.* Induct on $n = \max(\deg X, \deg Y)$; suppose $n \ge 1$ with
$n$ minimal over all admissible $(a,b,c,d)$-systems... more precisely we
show any nonconstant solution yields a nonconstant solution of another
admissible system with strictly smaller $n$ — infinite descent.

Factor the first conic over $\bar k$: choosing $\sqrt a, \sqrt{-b}$,
$$P^2 = aX^2 + bY^2 = (\sqrt a X - \sqrt{-b}\, Y)(\sqrt a X + \sqrt{-b}\, Y).$$
The two factors are coprime: a common irreducible would divide their sum
$2\sqrt a X$ and difference $2\sqrt{-b}Y$, contradicting
$\gcd(X, Y) = 1$ (note $a, b \ne 0$). In the UFD $\bar k[t]$, two
coprime polynomials whose product is a square are each a unit times a
square, and units of $\bar k[t]$ are squares: so
$$\sqrt a X - \sqrt{-b} Y = R^2, \qquad \sqrt a X + \sqrt{-b} Y = S^2,
\qquad \gcd(R, S) = 1,$$
whence $X = \dfrac{R^2 + S^2}{2\sqrt a}$, $Y = \dfrac{S^2 -
R^2}{2\sqrt{-b}}$, and $\deg R,\ \deg S \le n/2$ (each of $R^2, S^2$ is
a linear combination of $X, Y$).

Substitute into the second conic:
$$Q^2 = c X^2 + d Y^2 = \alpha R^4 + 2\beta R^2 S^2 + \alpha S^4,
\qquad \alpha = \frac{c}{4a} - \frac{d}{4b},\quad
\beta = \frac{c}{4a} + \frac{d}{4b}.$$
Here $\alpha \neq 0$: $\alpha = 0 \iff bc = ad$, excluded. Factor the
binary quartic: $\alpha x^2 + 2\beta x + \alpha$ has roots
$\theta, \bar\theta$ with $\theta\bar\theta = 1$ (so both nonzero) and
$\theta \ne \bar\theta$ unless $\beta^2 = \alpha^2$; but
$\beta = \alpha \iff d = 0$ and $\beta = -\alpha \iff c = 0$, both
excluded. So
$$Q^2 = \alpha\,(R^2 - \theta S^2)(R^2 - \bar\theta S^2)$$
with the two factors coprime (a common irreducible divides
$(\theta - \bar\theta)S^2$ and $(\theta - \bar\theta)R^2$). As before
each factor is a square:
$$1\cdot R^2 + (-\theta) S^2 = U^2, \qquad 1 \cdot R^2 + (-\bar\theta)S^2 = V^2 .$$
This is again a system of the Lemma's shape, with parameters
$(a', b', c', d') = (1, -\theta, 1, -\bar\theta)$ — and its
admissibility is **automatic**:
$a'd' - b'c' = \theta - \bar\theta \neq 0$ and
$a'b'c'd' = \theta\bar\theta = 1 \neq 0$.
Finally $(R, S)$ is nonconstant — otherwise $X, Y$ would be constant —
and $\max(\deg R, \deg S) \le n/2 < n$. Descent. ∎

**Theorem A2.4 ($k[t]$ four-square theorem). PROVEN.** For any field
$k$ with $\operatorname{char} k \notin \{2,3\}$: every four-term
arithmetic progression of squares in $k[t]$ is a square multiple of a
**constant** one — equivalently, a *primitive* 4-AP of squares
($\gcd$ of the roots $= 1$) is constant. In particular over $k[t]$ the
problem reduces entirely to 4-APs of squares in the constant field $k$
itself.

*Proof.* Let $A^2, B^2, C^2, D^2$ be a 4-AP, $g = \gcd(A,B,C,D)$;
dividing by $g^2$ we may assume the roots have gcd 1, and then they are
pairwise coprime: an irreducible $\pi$ dividing two of them divides a
difference $k\Delta$ with $k \in \{1,2,3\}$ a **unit** of $k[t]$
(char $\nmid 6$), so $\pi \mid \Delta$ and then $\pi$ divides all four
roots. Now view $(X, Y) := (B, C)$:
$$2B^2 - C^2 = A^2, \qquad 2C^2 - B^2 = D^2$$
— exactly Lemma A2.L with $(a, b, c, d) = (2, -1, -1, 2)$ over
$\bar k \supseteq k$: $ad - bc = 4 - 1 = 3 \neq 0$ (char $\ne 3$!),
$abcd = 4 \ne 0$. The Lemma gives $B, C$ constant, then $A^2 = 2B^2 -
C^2$ and $D^2 = 2C^2 - B^2$ are constant, so the primitive AP is
constant. ∎

**Sharpness — the hypothesis is not decoration.** Over
$\mathbb{F}_{13}[t]$ the *non-primitive* nonconstant 4-AP
$$(2g)^2,\ (6g)^2,\ (4g)^2,\ (3g)^2 \qquad (g \text{ nonconstant})$$
exists for any $g$: the constants $4, 10, 3, 9$ are four distinct
squares of $\mathbb{F}_{13}$ in AP (common difference 6). The verify
script exhibits it. Over $k = \mathbb{Q}$ no constant 4-AP of distinct
squares exists (F3.3), so over $\mathbb{Q}[t]$ there is no nonconstant
4-AP of distinct squares at all — at the provenance level of F3.3.

**Theorem A2.5 ($k[t]$ congruum theorem, all $k$). PROVEN.** For any
$k$, $\operatorname{char} k \notin \{2,3\}$: every 3-AP of squares in
$k[t]$ whose common difference is a perfect square in $k[t]$ is a square
multiple of a constant one. *Proof.* Primitivize as above (here the
divisor $g$ of the roots has $g^2 \mid \Delta = T^2$, so $g \mid T$ and
the scaled difference is still a square); the primitive system is
$2B^2 - C^2 = A^2$, $C^2 - B^2 = T^2$ on $(X,Y) = (B,C)$: parameters
$(2, -1, -1, 1)$, $ad - bc = 2 - 1 = 1 \ne 0$, $abcd = 2 \neq 0$; apply
A2.L. ∎ (Over $\mathbb{Q}[t]$, combined with F3.2b for the constant
layer — which is fully PROVEN — this gives outright: **no nonconstant
3-AP of distinct squares in $\mathbb{Q}[t]$ has square common
difference**, unconditionally.)

**Corollary A2.6 (collinear kill, function fields).** As in F3.4, no
nonconstant MSS3 over $k[t]$ has $v = \pm 3u$, $u = \pm 3v$ (nine
squares in AP contain four). With F1.3's exclusions, nonconstant
MSS3 candidates are confined to generic $(u,v)$ — same landscape as over
$\mathbb{Z}$, now unconditionally.

## 5. The frontier: the full nonexistence conjecture over $k[t]$

**Conjecture A2.C.** For $\operatorname{char} k \notin \{2,3\}$, every
MSS3 over $k[t]$ is a square multiple of a constant one — equivalently,
there is no MSS3 with nonconstant entry *ratios*, equivalently no
nonconstant morphism $\mathbb{P}^1 \to X$ through nondegenerate points.
(The "square multiple of constant" escape is real: over
$\mathbb{F}_{59}[t]$, scaling the constant $\mathbb{F}_{59}$-solution of
F5.3 by any $g^2$ gives an MSS3 with nonconstant entries — but constant
ratios, i.e. a constant point of $\mathbb{P}^8$. Over $k = \mathbb{Q}$,
where no constant solution may exist either, A2.C says: no
$\mathbb{Q}[t]$-solutions beyond $\mathbb{Q}$-solutions at all.)

What we know:

1. **It is a rational-curve statement.** A nonconstant MSS3 over
   $k(t)$ is precisely a nonconstant map $\mathbb{P}^1 \to X$ into the
   magic-square-of-squares surface ([A5](A5-surface-geometry.md))
   avoiding the degeneracy locus. Bruin–Thomas–Várilly-Alvarado (CITED)
   prove $X$ is algebraically quasi-hyperbolic — **finitely many** such
   curves exist over $\bar{\mathbb{Q}}$ — but not, as far as we can
   verify, that the nondegenerate count is zero. A2.C over
   $\bar{\mathbb{Q}}$ is exactly "that count is zero".
   **Progress ([A7](A7-curve-enumeration.md), Corollary A7.4, PROVEN):**
   every genus ≤ 1 curve on $X$ whose Lucas-plane image is a *line* is
   classified — the rational ones are entry-degenerate and the sole
   elliptic family (center-zero) has no nondegenerate rational points by
   F3.2. Hence **any nonconstant $k(t)$-MSS3 has plane image of degree
   ≥ 2**, and the systematic conic sweeps of A7 (216 exact candidates)
   found no genus ≤ 1 component either.
2. **Why Lemma A2.L does not finish it.** The lemma's mechanism needs
   binary forms (two variables) so that conics factor into linear
   pieces. The MSS3 system is (after eliminating $u, v$)
   $$Q_3^2 + M^2 = Q_1^2 + Q_2^2, \qquad Q_4^2 - M^2 = Q_1^2 - Q_2^2,
   \qquad P_i^2 = 2M^2 - Q_i^2,$$
   a system of quadrics in $\ge 3$ genuinely independent variables:
   irreducible conics, no factoring, no descent step. This is not an
   accident of our method — the surface has honest geometry (it is not
   dominated by pairs of curves), and the problem is exactly as hard as
   controlling its rational curves.
3. **VERIFIED evidence** (`a2.mss3_ff_search`, via
   `compute/ff_search.py`): for the fields and center-degrees in the
   table below, **no MSS3 with nonconstant center exists over
   $\mathbb{F}_q[t]$** (search is exhaustive over centers by
   Prop. A2.1: every entry-nonconstant MSS3 has nonconstant $M$, and its
   offsets lie in the congrua set
   $D(M) = \{2ef : e^2 + f^2 = M^2\}$, so closure under the additive
   relations is a complete criterion degree by degree). Since these
   $q < 59$ admit no constant solution either
   ([F5.3](../foundations/F5-local-solubility.md)), there is no MSS3 of
   any kind, scaled-constant included, in the searched ranges.

| $q$ | $\deg M \le$ | outcome |
|---|---|---|
| 3 | 5 | none |
| 5 | 4 | none |
| 7, 11, 13 | 3 | none |
| 17, 19, 23 | 2 | none |

(The check re-runs the sub-table $q \le 13$, $\deg M \le 3{-}2$ on every
FULL pass in under a second; the extended rows were produced by the same
generator, `python3 -m compute.ff_search` variants, ~2 min total, on
2026-08-25.)

4. **Open Task A2-T1.** Prove A2.C for $k = \bar{\mathbb{Q}}$ (hence
   for all char-0 $k$): either by enumerating BTVA's finitely many
   low-genus curves and checking degeneracy (needs their symmetric
   differential machinery, or an independent Picard/curve analysis on
   $X$ — see A5's problem list), or by a genuinely new descent adapted
   to three-variable quadric systems. **This is, in our judgment, the
   single most tractable open path to a real theorem in the entire
   problem complex**: every ingredient is unconditional over function
   fields, and the target is a finite computation away from BTVA's
   published result.

## 6. What the verify script proves mechanically

`verify/checks/a2_function_field.py`:

1. `a2.mason_instances` — Mason's inequality holds with the Wronskian
   divisibility exactly as in the proof, on structured families
   (including the nonconstant 3-AP of squares
   $((t^2{-}2t{-}1)^2, (t^2{+}1)^2, (t^2{+}2t{-}1)^2)$, which also
   witnesses that *three*-term APs are genuinely possible — the
   four-term theorem is sharp).
2. `a2.descent_identities` — the algebraic identities of Lemma A2.L
   verified symbolically (sympy): the substitution quartic, the root
   relations $\theta\bar\theta = 1$, the degeneracy equivalences
   $\alpha = 0 \iff ad = bc$, $\beta = \pm\alpha \iff d = 0$ or
   $c = 0$, and admissibility propagation.
3. `a2.four_ap_ff` / `a2.congruum_ff` — exhaustive: no nonconstant
   4-AP of squares, and no nonconstant square-congruum 3-AP, over
   $\mathbb{F}_q[t]$ for the tabulated $(q, \deg)$ ranges (validating
   A2.4/A2.5 where they are checkable).
4. `a2.mss3_ff_search` — the exhaustive center-degree search above.
