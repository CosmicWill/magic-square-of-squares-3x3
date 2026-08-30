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

## 2.6 Theorem A3.7: the two-split-prime theorem ($a = b = 1$)

*(2026-08-29; `compute/two_prime_additive.py`, check
`a3.omega2_ab1`.)*

**Theorem A3.7 (PROVEN).** Let $m = 2^s r\, p\, q$ with $r$ a product
of primes $\equiv 3 \pmod 4$ and $p \ne q$ primes $\equiv 1 \pmod 4$.
Then $D(m)$ admits **no** signed additive relation $\varepsilon_1 d_1
+ \varepsilon_2 d_2 + \varepsilon_3 d_3 = 0$ (repetitions allowed).
Combined with Theorem A3.6: **the split part of any MSS3 center has
at least three prime factors counted with multiplicity** (it is
divisible by $p^2q$ or by $pqr'$ with $p, q, r'$ distinct split
primes).

*Setup.* Here $D(m) = \{ m^2 |\mathrm{Im}(\sigma^j\tau^k)| \}$ over
$(j,k) \in \{(1,0), (0,1), (1,1), (1,-1)\}$, with $\sigma =
\lambda^4/p^2$, $\tau = \mu^4/q^2$, and $v$-data
$v_{\lambda,\bar\lambda,\mu,\bar\mu}(\sigma^j\tau^k) = (2j, -2j, 2k,
-2k)$ — so $\langle\sigma,\tau\rangle$ is free of rank 2 and no
monomial is $\pm 1$ except the identity. A relation is a vanishing
sum of monomials $\sum c_i (w_i - w_i^{-1}) = 0$. The machine
enumerates all sign/exponent patterns modulo symmetry: **36
canonical patterns** (`classify_all_11`).

**Lemma A3.7a (valuation prune).** At each of the four valuation
directions the minimal valuation among the (merged) monomials must
be attained by at least two distinct monomials — coefficients
$\pm1, \pm2$ are units at $\lambda, \mu$. *Twenty* patterns die
here; in particular every doubled pattern $2d_x = d_y$ except
$\{x,y\} = \{\sigma\tau, \sigma\tau^{-1}\}$.

**Lemma A3.7b (tan-half factorization).** Writing $\sigma =
(1+it_1)/(1-it_1)$ with $t_1 = s_1/c_1 \in \mathbb{Q}$
($\lambda^2 = c_1 + is_1$) and likewise $t_2 = s_2/c_2$, the
relation times $(1+t_1^2)^J(1+t_2^2)^K$ is an integer polynomial
$N(t_1, t_2)$. For *six* patterns $N$ factors completely (exact
division, machine-certified) into the candidate factors $t_1$,
$t_2$, $t_1 \pm t_2$, $1 \pm t_1t_2$, $1 + t_i^2$ — e.g.
$\sin A + \sin B - \sin(A{+}B)$ gives $N = 2\,t_1t_2(t_1+t_2)$ —
and each real zero of a candidate factor forces $\sigma^\alpha
\tau^\beta = \pm 1$ with $(\alpha,\beta) \ne 0$: impossible in the
free group. (These are precisely the *coherent* patterns, where one
angle is a $\pm$-sum of the others: the classical sum-to-product
identities.)

**Machine congruences.** Three patterns have no solutions modulo 16
under the Pythagorean side conditions ($c$ odd, $s$ even, $c^2+s^2
\equiv P^2$, $P$ an odd unit) — `congruence_kill`.

**The seven residual patterns** reduce, after clearing, to two
equation families plus mirrors (all with $c_i$ odd, $s_i$ even,
$c_i^2 + s_i^2 = p_i^2$, $\gcd(c_i, s_i) = 1$, so that
$\gcd(c_is_i,\, c_i^2 - s_i^2) = 1$ and $p \nmid c_1s_1$):

*Family I ($\tan A = \mp 2\tan B$, patterns $\{\sigma, \sigma\tau,
\sigma\tau^{-1}\}$):* $c_1s_1(c_2^2 - s_2^2) = \mp 2\,c_2s_2(c_1^2 -
s_1^2)$. Coprimality forces $c_2s_2 \mid c_1s_1 \mid 2c_2s_2$, so
$c_1s_1 = \pm t\,c_2s_2$ with $t \in \{1, 2\}$.
- $t = 1$: substituting gives $q^4 = 4[(c_1^2-s_1^2)^2 +
  (c_1s_1)^2]$ — $q$ even, impossible.
- $t = 2$: gives $c_2^2 - s_2^2 = \pm(c_1^2 - s_1^2)$, hence $p^4 -
  q^4 = 12(c_2s_2)^2$. Writing $p^2+q^2 = 2u$, $p^2 - q^2 = 8v$
  ($u$ odd, $\gcd(u,v)=1$): $uv = 3(\cdot)^2$; $u = 3a^2$ dies mod 3
  ($u$ is a sum of two coprime squares), so $u = a^2$:
  $((p{+}q)/2)^2 + ((p{-}q)/2)^2 = a^2$ with product $6b^2$: the
  primitive parametrization gives pairwise-coprime $m, n, m{-}n,
  m{+}n$ with $mn(m{-}n)(m{+}n) = 3b^2$ — one factor is $3\times$
  square, three are squares. The four branches die by: $x^2+y^2 =
  3d^2$ (mod 3); $x^4 - y^4 = 3T^2$ (**Lemma L5** below); the
  sandwich $x^2 \pm 3w^2$ both squares (**Lemma L3**); and $a^2 +
  b^2 = 6w^2$ (mod-3 descent, **L4**).

*Family II ($\tan B = 2\sin A$, pattern $\{\tau, \sigma\tau,
\sigma\tau^{-1}\}$):* $p^2 c_2s_2 = 2c_1s_1(c_2^2 - s_2^2)$, so
$(c_2^2 - s_2^2) \mid p^2$:
- $c_2^2 - s_2^2 = \pm 1$: $(c_2-s_2)(c_2+s_2) = \pm 1$ forces
  $s_2 = 0$ — impossible.
- $= \pm p$: then $p \mid c_1s_1$, impossible ($c_1^2 + s_1^2 =
  p^2$ with $\gcd = 1$ allows no proper multiple).
- $= \pm p^2$: then $c_2s_2 = \pm 2c_1s_1$ and $q^4 - p^4 =
  16(c_1s_1)^2$, giving $uv = (\cdot)^2$, $u = a^2$, $v = b^2$, and
  the primitive parametrization forces $m, n, m{-}n, m{+}n$ **all**
  squares — i.e. $x^4 - y^4 = \square$: **Fermat (L1)**.

*Family III (doubled: $2\sin(A{+}B) = \pm\sin(A{-}B)$, i.e. $\tan A
= -3\tan B$ up to mirror):* $c_1s_1(c_2^2-s_2^2) = -3c_2s_2(c_1^2 -
s_1^2)$, $t \in \{1, 3\}$.
- $t = 1$: $q^4 - p^4 = 8C^2$ with $C = c_1^2 - s_1^2$ **odd** —
  but $q^4 \equiv p^4 \equiv 1 \pmod{16}$ while $8C^2 \equiv 8$:
  dead (this is the machine's mod-16 class, found by hand here).
- $t = 3$: $p^4 - q^4 = 32(c_2s_2)^2$, leading to $uv = 2(\cdot)^2$
  and $mn(m{-}n)(m{+}n) = 2b^2$: **Lemma L2** (the non-congruence
  of 2).

**Lemma L1 (Fermat).** $x^4 - y^4 = z^2$ has no solutions with
$xyz \ne 0$. *(Classical descent; corroborated by exhaustive search
in-suite.)*

**Lemma L2 ($mn(m^2-n^2) = 2b^2$ is impossible** for coprime $m > n
\ge 1$ of opposite parity, $b \ne 0$**).** The four factors are
pairwise coprime and exactly one (the even one of $m, n$) carries
the 2, as $2t^2$; the rest are squares. If $m = 2t^2$: $n = y^2$,
$m \pm n = z^2, w^2$ with $z, w$ odd and $(z-w)(z+w) = 2y^2 \equiv
2 \pmod 4$ while $z \pm w$ are both even — contradiction. If $n =
2t^2$: $m = x^2$, $m \pm n = z^2, w^2$, so $z^2 + w^2 = 2x^2$,
$z^2 - w^2 = 4t^2$; setting $A = (z{+}w)/2$, $B = (z{-}w)/2$:
$A^2 + B^2 = x^2$, $AB = t^2$ with $AB$ even, and the primitive
parametrization returns $m_2n_2(m_2^2 - n_2^2) = 2t_2^2$ at
strictly smaller size — infinite descent. $\blacksquare$

**Lemma L3 (the sandwich; "3 is not congruent").** $x^2 - 3w^2$ and
$x^2 + 3w^2$ cannot both be nonzero squares. *Proof.* From $y^2 +
z^2 = 2x^2$ and $z^2 - y^2 = 6w^2$: $A = (z{+}y)/2$, $B = (z{-}y)/2$
give $A^2 + B^2 = x^2$, $AB = 3w'^2 \cdot 2$ with $w = 2w'$ forced
mod 8; the primitive parametrization gives $mn(m{-}n)(m{+}n) =
3w'^2$ with pairwise-coprime factors: the $3$ sits in one factor,
the others are squares, and the four branches die by mod 3
($x^2{+}y^2 = 3d^2$), by **L5**, by mod-3 descent (**L4**), or
recurse into the same system at strictly smaller $x$ — a
well-founded descent. $\blacksquare$

**Lemma L4.** $a^2 + b^2 = 6w^2$ has no nonzero solutions: mod 3
forces $3 \mid a, b$, then $3 \mid w$ — descent. $\blacksquare$

**Lemma L5.** $x^4 - y^4 = 3T^2$ has no solutions with $xyT \ne 0$:
$\gcd$-splitting gives $x^2 + y^2 = \square$ (dead mod 3 in the
$3b^2$ branch) with $x^2 - y^2 = 3a^2$; the primitive
parametrization of the triple turns $x^2 - y^2$ into $\pm(m^4 -
6m^2n^2 + n^4) \equiv m^4 + n^4 \pmod 3$, forcing $3 \mid m, n$ —
contradiction. $\blacksquare$

**Reading.** The two-split-prime case needed genuinely more than
$\omega = 1$: the free rank-2 group brings incoherent patterns that
no factorization kills, and they land — remarkably — on the
classical quartic descents of Fermat: $x^4 - y^4 = \square$, the
non-congruence of 2 and 3. The additive layer at $\omega = 2$,
$a = b = 1$ is thus governed by the oldest theorems in the subject.
The next rungs: $a + b \ge 3$ (larger boxes: more incoherent
patterns) and $\omega = 3$ (rank 3: valuation pruning weakens). The
desert data says the answer will stay "never"; the machinery here —
prune, factor, descend — is built to scale (`classify_all_11`
generalizes to any box).

## 2.7 The $(2,1)$ box (split part $p^2q$): Theorem A3.8, partial

*(2026-08-29; general-box machinery in
`compute/two_prime_additive.py`; census artifact
`data_box21_census.json`, open equations `data_box21_open.json`;
check `a3.box21`.)*

**Status.** For $m = 2^s r\, p^2 q$ the machine census gives **189
canonical patterns**: 136 valuation-dead, 13 factored (extended
candidate list $\mathrm{Im/Re}[(1+it_1)^\alpha(1\pm it_2)^\beta]$),
12 congruence-dead, 28 residual. Of the residuals, 7 involve only
the $(1,1)$ sub-box and are closed by Theorem A3.7. **Eleven more
are closed below. Ten remain open** — the box is closed except for
ten explicit Diophantine equations (empty on all real prime data
searched).

**The level-2 frame.** Write $\ell = \lambda^2 = c_1 + is_1$, $w =
\mu^2 = c_2 + is_2$, $C = c_1^2 - s_1^2$, $S = 2c_1s_1$ (so $\ell^2
= C + iS$, $C^2 + S^2 = p^4$: the level-2 Pythagorean pair), $u =
c_2^2 - s_2^2$, $v = 2c_2s_2$. Multiplying a relation by
$p^4q^2$ gives an integer identity in $\mathrm{Im}(\ell^{2j}w^{\pm2})$-
terms with explicit $p, q$-powers; the collapse identities $\ell^2
\pm p^2 = 2c_1\ell$ resp. $2is_1\ell$ merge terms. All eleven kill
identities are machine-verified against the census polynomials.

**The eleven closures.**
- *$\alpha$ pair* ($\sin A = \mp 2\cos 2A \sin B$): the identity
  $Sp^2q^2 = \mp 2v(C^2 - S^2)$ with $\gcd(S, C^2 - S^2) = 1$ and
  $p \nmid C^2 - S^2$ forces $(C^2-S^2) \mid q^2$; the cases give
  $S = 0$ (dead), $q \mid 2v$ (dead), or $2C^2 = p^4 \pm q^2$,
  $2S^2 = p^4 \mp q^2$, whence $(p^2)^4 - q^4 = (2CS)^2$ —
  **Fermat (L1)**.
- *F-C pair* ($\tan 2A = \mp 2\sin B$): $CSq^2 = \mp(C^2-S^2)v$
  forces $(C^2 - S^2) \mid q^2$: $S = 0$ / $q \mid v$ /
  $p^8 - q^4 = (2CS)^2$ — **Fermat** again.
- *F-D* ($\tan B = 2\sin 2A$): $vp^4 = 4CSu$ forces $u \mid p^4$;
  $u = \pm 1$ gives $s_2 = 0$; $u = \pm p^e$ ($1 \le e \le 3$)
  forces $p \mid 4CS$, impossible; $u = \pm p^4$ gives $q^4 -
  (p^2)^4 = (4CS)^2$ — **Fermat**.
- *$\beta_1$ pair*: the total collapse
  $\mathrm{Im}(\ell^3w^{\pm2}) = 2q^2s_1C$ (machine-found, exact).
  The left side is a $q$-unit: $v_\mu(\ell^3w^2) = 2 \ne 0 =
  v_\mu(\bar\ell^3\bar w^2)$, so $v_q(\mathrm{Im}) = 0$, while the
  right side has $v_q \ge 2$ and $s_1C \ne 0$. **Dead by $q$-adic
  valuation.**
- *F-F quadruple* (doubled $2d_{(2,\pm1)} = d_{(2,\mp1)}$): the
  equations are $(C^2{-}S^2)v = -3\cdot 2CSu$ and $3(C^2{-}S^2)v =
  -2CSu$ — **exactly Theorem A3.7's Family III with $(c_1, s_1)
  \mapsto (C, S)$** (the level-2 pair is coprime with $C$ odd, $S$
  even, and the III-proof used nothing else): $t = 1$ dies mod 16
  ($q^4 - p^8 \equiv 8$), $t = 3$ descends through $p^8 - q^4 =
  32(\cdot)^2$ resp. $q^4 - p^8$-mirror to $mn(m^2-n^2) = 2b^2$ —
  **Lemma L2**.

**The grind (same day, second session): $\beta_2$ and E3 closed —
17 of 21 down.** (`a3.box21_grind` verifies every identity below
symbolically.)

- *$\beta_2$ quadruple.* The exact collapse (machine-verified):
  relation $= 2[\,CSq^2 + R_3(c_1v - s_1u)\,]$, $R_3 =
  c_1(c_1^2-3s_1^2) = c_1T_3$. Cancelling $c_1$ and using
  $\gcd(T_3, 2s_1C) = 1$: $T_3 \mid q^2$. The cases:
  $T_3 = \pm1$ forces $p^2 \mp 1 = (2s_1)^2$ — consecutive squares
  or $p^2 \equiv 3 \bmod 4$: dead. $T_3 = \pm q$ gives $c_1v
  \equiv s_1u \bmod q$ while $u^2 \equiv -v^2$: squaring forces
  $q \mid c_1^2 + s_1^2 = p^2$: dead. $T_3 = -q^2$ dies mod 16
  ($c_1^2 - 3s_1^2 \in \{1,5,9,13\}$, $-q^2 \in \{7,15\}$).
  $T_3 = +q^2$ forces $4 \mid s_1$ and splits $(c_1-q)(c_1+q) =
  3s_1^2$ into coprime halves; all four partitions land on
  $$p^2 = 16a^4 + 40a^2b^2 + 9b^4 = (4a^2+9b^2)(4a^2+b^2)$$
  (or the $144/40/1$ mirror $(36a^2+b^2)(4a^2+b^2)$) with
  **coprime factors** — one factor must be $1$, forcing $a = 0$:
  dead.
- *E3 pair.* The tree $p^2 \mid u$, $C \mid u'$ gives $u + iv =
  t'(p^2C + iS(4C - p^2))$, and the bracket **collapses in
  $\mathbb{Z}[i]$** (machine-verified): $p^2C + iS(4C-p^2) =
  \ell^4 + 2is_1\bar\ell^3$. Then: $t' = \pm1$ ($\bar\mu$-valuation
  kills $q$-content), the unit and sign are fixed mod 8 (Gaussian
  odd fourth powers are $\equiv 1 \bmod 8$; the case $s_1 \equiv 2
  \bmod 4$ dies here), leaving exactly
  $$\mu^4 - \ell^4 = 2is_1\bar\ell^3 .$$
  The four factors $\prod_k(\mu - i^k\ell)$ have pairwise
  differences $= \mathrm{unit}\cdot\ell$ (a $\bar\lambda$-unit), so
  $\bar\lambda^6$ concentrates in ONE factor: that factor has norm
  $\ge p^6$. But the norm identity $q^4 = p^8 + 4s_1^2p^6 +
  4s_1\,\mathrm{Im}(\ell^7)$ gives $q \le \sqrt3\,p^2$, so every
  factor has norm $\le (\sqrt q + p)^2 < 5.4\,p^2$ — impossible
  for $p \ge 2$. **Dead with no descent at all: pure valuation and
  size in $\mathbb{Z}[i]$.**

**The four E1/E2 equations — second wave: reduced to the $g = 3$
sliver** (`a3.box21_sliver`). Their tree ($p^2 \mid v$, then $Su =
-v'(Cp^2 \pm 2C_4)$) bottoms in $N_\pm = g\cdot\mathrm{unit}\cdot
\mu^4$, where $N_+ = 2c_1\ell^3 + \bar\ell^4 = K_+ + iSp^2$ and
$N_- = \bar\ell^4 + 2is_1\ell^3 = -(K_- + iSp^2)$, with $K_\pm =
Cp^2 \pm 2C_4$, $g = \gcd(S, K_\pm)$, and $4 \mid s_1$ forced
mod 8.

**Content lemma (PROVEN).** $g \in \{1, 3\}$: for an odd prime $r
\mid s_1$: $K_+ \equiv 3c_1^4$, $K_- \equiv -c_1^4 \pmod r$; for
$r \mid c_1$: $K_+ \equiv s_1^4$, $K_- \equiv -3s_1^4$; so $r \mid
g$ forces $r = 3$, with $3 \mid s_1$ in the $+$ case and $3 \mid
c_1$ in the $-$ case; and mod 9 the 3-valuation of $K_\pm$ is
exactly 1. (Component identities symbolic; the lemma verified on
every split prime to the profile bound.)

**$g = 1$ is dead in both cases.** The $-$ case is the E3 clone:
the unit is forced to 1 mod 8, giving $\mu^4 - \bar\ell^4 =
2is_1\ell^3$, and the four factors $\prod_k(\mu - i^k\bar\ell)$
have unit-times-$\bar\ell$ differences, so $\lambda^6$ concentrates
in one factor of norm $\ge p^6$ — against the $q \le \sqrt3\,p^2$
norm ceiling. The $+$ case forces unit $= -1$ mod 8, i.e. $\mu^4 +
\bar\ell^4 = -2c_1\ell^3$, which **factors over $\mathbb{Z}[i]$**:
$(\mu^2 + i\bar\ell^2)(\mu^2 - i\bar\ell^2) = -2c_1\ell^3$. The two
factors differ by the $\lambda$-unit $2i\bar\ell^2$, so $\lambda^6$
concentrates in one factor of norm $\ge p^6$, against the ceiling
$(\sqrt q + p^2)^2 \le 7.5\,p^4$ — dead for every $p$.

**The sliver falls — Theorem A3.8 is COMPLETE** (`a3.box21_complete`;
third wave, same day). First, the symmetric form: with $2c_1 =
\ell + \bar\ell$ and $2is_1 = \ell - \bar\ell$,
$$N_\pm \;=\; \ell^4 \pm p^2\ell^2 + \bar\ell^4,$$
whence the norm identity $|N_\pm|^2 = K_\pm^2 + S^2p^4$ (machine-
verified; equivalently $F(x) = (4x^2+x-2)^2 + (1-x^2)$ at $x =
\pm C/p^2$). The sliver equation $3\,\mathrm{unit}\cdot\mu^4 =
N_\pm$ gives $|N_\pm| = 3q^2$ and, after dividing the content
($K_1 = K_\pm/3$, $S_1 = S/3$, both integral in the sliver, $K_1$
odd):
$$q^4 = K_1^2 + S_1^2 p^4 .$$
**The final descent.** Factor: $(q^2 - K_1)(q^2 + K_1) = S_1^2p^4$.
Both factors are positive (their product is positive since $S_1
\ne 0$, their sum is $2q^2$), both even, and their halves are
coprime: a common divisor would divide $q^2$ and $K_1$, but $q
\nmid K_1$ — otherwise $q$ divides both factors, so $q \mid S_1$,
making $q \mid N_\pm/3 = K_1 + iS_1p^2$, impossible since
$v_{\bar\mu}(\mu^4) = 0$. The prime $p$ cannot divide both halves
($p \ne q$), so the coprime split forces
$$\Bigl\{\tfrac{q^2-K_1}{2}, \tfrac{q^2+K_1}{2}\Bigr\} = \{U^2,\
p^4V^2\}, \qquad UV = S_1/2 \ne 0,$$
and adding: $q^2 = U^2 + p^4V^2$ with $U, V \ge 1$, hence $q^2 >
p^4$. But the triangle inequality gives $3q^2 = |N_\pm| \le
|\ell^4| + |p^2\ell^2| + |\bar\ell^4| = 3p^4$, with equality only
when $\ell^2$ is real ($s_1 = 0$ or $c_1 = 0$, degenerate) — so
$q^2 < p^4$ strictly. **Contradiction: the sliver is empty, in
both cases, for every unit.** $\blacksquare$

*Remark (why no shortcut existed).* The norm identity puts the
sliver on the elliptic curve $y^2 = 16x^4+8x^3-16x^2-4x+5$
(Jacobian $y^2 = x^3 - 2214x + 40041$, discriminant $2^4 3^{12}
229$), which has **rank $\ge 1$**: $(24, 27)$ is a non-torsion
point with $2\cdot(24,27) = (33,54)$. A rank-0 argument was never
available; the kill is the classical leg decomposition $q^2 = U^2
+ (p^2V)^2$ against the size window $q < p^2$ — the curve's
rational points all live outside the physical region.

**Theorem A3.8 — CORRECTED STATUS (same day, the all-plus audit;
`a3.allplus_audit`).** The pattern enumeration behind the censuses
excluded all-equal coefficient signs as "positivity-trivial." That
was WRONG: the census coefficient is (relation sign) $	imes$
(orientation), and orientations are solution-determined, so
all-plus sine patterns are legitimate. The corrected sweep:
**A3.7 stands** (its one all-plus machine-open, $	an B =
-2\sin A$, is covered by the Family-II tree, which never used the
sign in its divisor cases). Of the six $(2,1)$ all-plus opens,
four are covered by the existing sign-agnostic trees ($eta_1$
collapse, F-D, sub-box), but the **all-plus E3$^-$ pair**
($\sin(A{+}B) = -2\sin 2A\cos B$, classes $\{(1,\pm1), (2,1),
(2,-1)\}$) is genuinely new: its tree gives $u = p^2Ct'$, $v =
-t'S(4C{+}p^2)$, $t' = \pm1$, so $\mu^4 = \pm(p^2C -
iS(4C{+}p^2))$ with $q \in [p^2/2,\ 2.24\,p^2]$ and $p^2$
dividing the odd leg of $q^4$ — overdetermined but NOT closed
tonight.

**Theorem A3.8 therefore reads: for $m = 2^s r p^2 q$, $D(m)$
admits no signed additive relation, except possibly relations
realizing the all-plus E3$^-$ pair** — *and that pair is now
closed* (`a3.e3minus_closed`, same night):

**The E3$^-$ descent.** The relation reduces to $p^2(Cv + Su) =
-4uCS$ (symbolic), the tree forces $\pm\mu^4 = p^2C - iS(4C+p^2)$
with the norm identity $q^4 = p^8 + 8CS^2(p^2 + 2C)$, so $q \le
\sqrt5\,p^2$. The odd leg of $\mu^4$ is $x^2 - y^2$ with $(x,y)$
the unique legs of $q^2$: $p^2 \mid (x-y)(x+y)$ with coprime odd
factors, and $x + y \le \sqrt2\,q < 3.17\,p^2$ forces $x + y =
ep^2$, $e \in \{1, 3\}$. **$e = 1$: $x - y = C$ and parity force
$x = c_1^2$, $y = s_1^2$, so $q^2 = c_1^4 + s_1^4$ — Fermat's
$x^4 + y^4 = z^2$, impossible.** $e = 3$: $9p^4 + C_1^2 = 2q^2$
dies mod 3. The branch $x - y = ep^2$ dies by size. $lacksquare$

**THEOREM A3.8 (RESTORED, COMPLETE — all-plus patterns included).**
For $m = 2^s r\,p^2q$, $D(m)$ admits no signed additive relation.
**Corollary (A3.6 + A3.7 + A3.8): the split part of any MSS3 center
is $p^3q$, $p^2q^2$, or has at least three distinct split primes.**
Fittingly, the last pattern standing fell to the *other* classical
Fermat quartic: the ladder has now used both $x^4 - y^4 = z^2$ and
$x^4 + y^4 = z^2$.

## 2.8 The $(3,1)$ and $(2,2)$ campaigns: opened, machine-swept, survivor families pinned

*(2026-08-29 late; check `a3.box3122_campaign`; artifacts
`data_box31_census.json`, `data_box22_census.json`, and the two
`_survivors` files.)*

**Censuses.** Split part $p^3q$ (the $(3,1)$ box): **540** canonical
patterns — 429 valuation-dead, 16 factored, 32 congruence-dead, 63
residual. Split part $p^2q^2$ (the $(2,2)$ box): **924** patterns —
746 / 28 / 48 / 102. The machine layers kill $\approx 88\%$ on
their own, exactly as in the smaller boxes.

**Residual accounting.** Of $63 + 102 = 165$: **74** involve only
closed sub-boxes (Theorems A3.7/A3.8) — done. **32** of the
$(2,2)$ residuals have all $k$-exponents even: they are
$k$-replications of $(2,1)$ patterns over the level-2 pair
$(u, v)$; their lower-box analogues are all closed, and the
machine-layer kills (valuation/factored/congruence) transfer
generically, but 32 of them replicate onto patterns that were
closed by *hand trees* whose divisor enumerations lengthen under
replication ($T \mid q^2$ becomes $T \mid q^4$) — the level-shifted
re-derivations are **queued, not claimed**. The q-unit and
cyclotomic templates closed 2 more. **57 survivors** (33 + 24)
are pinned with their exact polynomials.

**The cyclotomic collapse lemma (PROVEN; the master tool).** For
every $d$:
$$p^{2d} \pm \ell^{2d} = \ell^d\,(\bar\ell^d \pm \ell^d) =
\ell^d \cdot \bigl(2\,\mathrm{Re}(\ell^d)\ \text{resp.}\
-2i\,\mathrm{Im}(\ell^d)\bigr),$$
so any two relation terms sharing the same $k$-sign collapse into
a single $w$-monomial times an *integer* factor $2\mathrm{Re}
(\ell^d)$ or $2\mathrm{Im}(\ell^d)$. Demonstrated instant kill
($\sin(A{+}B)$ vs $\sin(3A)$, $\sin(3A{+}B)$ shapes): the relation
reduces to $q^2(3C^2 - S^2) = 2\,\mathrm{Re}(\ell^4w^2)$ after
dividing the common $S$ — dead, since the right side is twice a
$q$-unit and $\mathrm{Re} = 0$ is impossible by the
$\lambda$-valuation mismatch. When the extracted factor does not
divide the pure part, the same collapse yields the reduced branch
$q^2 \mid 2\mathrm{Re/Im}(\ell^d)$ with $|\cdot| \le 2p^d$ — the
$\beta_2$-analogue trees one level up.

**Survivor families.** $(3,1)$: shapes $\{(1{,}1), (3{,}\pm1)\}$-
and $\{(2{,}1), (3{,}\pm1)\}$-mixtures, the doubled $(3,\pm1)$
pairs, and $\{(j,0), (3,1), (3,-1)\}$ mixed-sign trios. $(2,2)$:
$\{(1{,}2),(2{,}1),(2{,}2)\}$ (the large family, 18 patterns) and
$\{(1{,}1),(2{,}2),(2{,}2)\}$. All are the $\beta_2$/E-analogues
one level up; every tool they need — divisibility trees, the
$q$-window, leg decomposition, the classical descents — now
exists and has closed 400+ patterns below them. Mechanical, long,
queued.

## 2.9 Theorem A3.9: the $(3,1)$ box is closed (split part $p^3q$)

*(2026-08-30; the grind of entries 61--66; theorem ledger
`a3.p3q_theorem`.)*

**Theorem A3.9 (PROVEN).** For $m = 2^s r\, p^3 q$, $D(m)$ admits
no signed additive relation. **The corollary sharpens: the split
part of any MSS3 center is $p^2q^2$, $p^4q$-or-higher, or has at
least three distinct split primes.**

*Proof architecture.* The complete canonical pattern space (both
sign classes, by the completeness audit) is closed by: the machine
layers ($pprox 88\%$); sub-box recurrences (A3.7/A3.8); and the
named trees: the G1/G2 cyclotomic collapses ($q$-unit and
$C \mid q^2$-Fermat kills), the mixed-same-$j$ block (parity,
$T \mid q^2$ trees, leg window), M1 (both branches Fermat), M2
(mod 16; the $P_5' = \pm q^2$ double coprime split onto
$(2m)^2 = P_5/P_5'(a,b)$, disjoint mod 16), the G3 double pincer,
Lemma G4 (the uniform doubled kill), and H1/H2 (bracket identities
forcing rigid $(u,v)$-forms; parity odd $=$ even$^2$; the
leg-overflow $lphaeta = c_1s_1p^4 \Rightarrow q^2 \ge p^8$
against $q^4 \le 50p^{12}$; the leg-window with residues
$p \in \{5, 13\}$ checked exactly). Every step is machine-pinned
in the suite (checks `a3.g1_lemma` through `a3.h1h2_closed`).
$lacksquare$

The $(2,2)$ box stands at one remaining family
($\{(1,1),(2,2),(2,-2)\}$, 8 patterns) plus the 44 level-shifted
replication re-derivations — Theorem A3.10 ($p^2q^2$) is one
session away.

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
