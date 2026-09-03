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

The $(2,2)$ box stood at one remaining family
($\{(1,1),(2,2),(2,-2)\}$, 8 patterns) plus the 44 level-shifted
replication re-derivations; the family fell next (§2.10).

## 2.10 H3 and the double lever: the $(2,2)$ box has no open native pattern

*(2026-08-30; check `a3.h3_closed`.)*

The last family standing in either campaign box was
$\{(1,\epsilon),(2,2),(2,-2)\}$ ($\epsilon = \pm1$; all sign
vectors, $\epsilon_0$ normalized: 8 patterns). Clearing $p^4q^4$
and pairing the two level-2 terms by conjugation (identities exact
in the suite):

$$\epsilon_0\, p^2q^2\,\operatorname{Im}(\ell^2 w^{2\epsilon})
  \;=\; -2\epsilon_1 \cdot \begin{cases}
    U \cdot 2CS & (\epsilon_2 = \epsilon_1)\\[2pt]
    V \cdot C_4 & (\epsilon_2 = -\epsilon_1)
  \end{cases}$$

with $C + iS = \ell^2$, $C_4 + i\,2CS = \ell^4$, $u + iv = w^2$,
$U + iV = w^4$. This is the first family where **both primes hold a
lever on one equation** — a $q^2$-divisibility on the $p$-frame and
a $p^2$-divisibility on the $q$-frame bite simultaneously, and each
lever's window makes the other's conclusion *exact*.

**Same-sign case** ($\epsilon_2 = \epsilon_1$). $q \nmid 4U$ (since
$U \equiv -2v^2 \bmod q$ and $q \nmid v$), so $q^2 \mid CS$, and
$\gcd(C,S) = 1$ forces $q^2 \mid C$ xor $q^2 \mid S$. On the other
side $p \nmid 4CS$, so $p^2 \mid U = (u-v)(u+v)$ — coprime, odd,
nonzero factors — whence $p^4 \le (u \mp v)^2 < 2q^4$. The window
pins exactly: $0 < |C|, S < p^2 < \sqrt2\,q^2$ gives $C = \pm q^2$
or $S = q^2$, i.e.
$$p^4 - q^4 = S^2 \ \text{ or } \ C^2,$$
a nontrivial solution of Fermat's $x^4 - y^4 = z^2$ ($C$ odd,
$S \ge 2$). Dead.

**Opposite-sign case** ($\epsilon_2 = -\epsilon_1$). $q \nmid 4uv$,
so $q^2 \mid C_4 = (C-S)(C+S)$ — coprime, odd, nonzero — whence
$q^4 \le (C \mp S)^2 < 2p^4$. And $p \nmid C_4$ (it is $-2S^2$ mod
$p$), so $p^2 \mid uv$ with $\gcd(u,v) = 1$:

* $p^2 \mid v$: $v$ even and $p^2$ odd force $v \ge 2p^2$, so
  $q^2 > v \ge 2p^2$ — contradicting $q^4 < 2p^4$. Dead.
* $p^2 \mid u$: $|u| < q^2 < \sqrt2\,p^2$ pins $u = \pm p^2$, so
  $$v^2 = q^4 - p^4, \qquad v = 2c_2s_2 \ge 4,$$
  Fermat's quartic again, instantly. Dead.

*(Remark — the kill is overdetermined: the $q$-lever alone gives
$(C \mp S)^2 = q^4$, i.e. $2CS = \pm(q^4 - p^4) = \mp v^2$, so
$v^2 = 2|C|S = 4\,|C|\,c_1 s_1$ with $|C|, c_1, s_1$ pairwise
coprime — three coprime positive factors of a square, forcing
$c_1 = \gamma^2$, $s_1 = \delta^2$, $|\gamma^4 - \delta^4| =
\alpha^2$: the same Fermat endpoint reached through the $p$-frame
instead of the $q$-frame.)*

All 8 die sign-uniformly — the sign vector enters only through
squares. Machine pinning (`a3.h3_closed`): the pair-collapse and
per-pattern collapse identities exact in $\mathbb{Z}[c_1,s_1,c_2,s_2]$;
a cross-engine pin (the tan-half `relation_poly` homogenizes to the
Gaussian `cleared_relation`, all 8); every frame fact of the proof
(parity, coprimality, $p$-/$q$-indivisibility, size windows) on all
split primes in range; real-data emptiness of all 8 cleared
relations; the Fermat search corroboration.

**Status: the additive queue is EMPTY.** Every native canonical
pattern of the $(1,1)$, $(2,1)$, $(3,1)$, $(2,2)$ boxes is closed.
Theorem A3.10 ($p^2q^2$) now gates on the 44 level-shifted
replications of closed $(2,1)$ parents — analysed next.

## 2.11 The $p^2q^2$ replications and the rigidity lemma (P1's core)

*(2026-08-30; checks `a3.p2q2_accounting`, `a3.p2q2_reduction`.
**A3.10 is REDUCED, not proven** — stated honestly.)*

The $(2,2)$ box enumerates to $1144$ canonical patterns which
partition, with **zero gaps** (machine-audited), as: $1008$ machine
kills ($912$ valuation, $36$ factored, $60$ congruence); $34$ in the
$(2,1)$ sub-box and $26$ in the $(1,2)$ sub-box (both closed by
Theorem A3.8, the second via the $p\leftrightarrow q$ symmetry of
the additive-relation condition); $32$ already in the closed ledger
(the $24$ $G3$ double-pincer patterns closed during the $(3,1)$
campaign — they are $(2,2)$-box patterns — plus the $8$ $H3$); and
$44$ **replications** ($26$ with all $k$ even, $18$ with all $j$
even).  The replications are the whole of what remains, and the $18$
$j$-children are the $p\leftrightarrow q$ transposes of $18$ of the
$26$ $k$-children (identity pinned), so **the task is exactly the
$26$ $k$-children.**

A $k$-child is a halving: its cleared relation equals its
$(2,1)$-parent's under the **$q$-level shift**
$(c_2,s_2)\mapsto(c_2^2{-}s_2^2,\,2c_2s_2)$ (pinned exact for all
$26$).  The transfer is *not* automatic, because the parent theorem
A3.8 covers the second prime being a genuine prime $q'$, whereas the
child needs the second slot to be $q^2$ with the level-2 frame
structure.  Twelve children survive this for free — the
**collapsed-valuation kill** (the odd term carries $q^4$ while the
collapsed $(2,\pm2)$ pair is a $q$-unit, so the cleared relation
cannot vanish), the $F1$ family landing on $x^4+y^4=2z^2$ (hence
Fermat $x^4-y^4=z^2$), and the $F9$ squeeze / $F10$ pinch.

The other **fourteen reduce to a single rigidity endpoint.**  Block A
$\{(1,\pm2),(2,2),(2,-2)\}$ (8 patterns) collapses to one $p$-lever
$p^2\mid U$ (resp. $V$) forcing, after the coprime-factor descent,
$\mathrm{Re}(w^4)=\pm p^2C$; the minus sign dies mod $8$
($\mathrm{Re}(w^4)\equiv1$, $-p^2C\equiv3,7$), and the plus sign is

$$\boxed{\;c_2^4 - 6c_2^2s_2^2 + s_2^4 \;=\; c_1^4 - s_1^4\;}
\qquad(\mathrm{Re}(w^4)=c_1^4-s_1^4),$$

with $c_1^4-s_1^4 = (c_1^2{-}s_1^2)(c_1^2{+}s_1^2) = p^2C$.  Block B
(6 patterns, the fusion families with a pure $(2,0)$ term) reduces
analogously via a $q^4$ lever.

**This endpoint is the core lemma of the uniform program (P1).**  It
is the level-2 instance of a rigidity phenomenon that recurs in every
higher box, so proving it is worth more than the single theorem.

**CORRECTION (same day, entry 72): the "pure" quartic is FALSE.**  An
earlier draft of this section, on the strength of a height-400
search, called the equation a clean Diophantine statement with no
coprime solution at all.  A height-4000 search found
$$(c_2,s_2,c_1,s_1)=(1369,\,3320,\,1017,\,320),\qquad
c_2^4-6c_2^2s_2^2+s_2^4 = c_1^4-s_1^4 = 1059267975521,$$
with the right parities and coprimality — a genuine point on the
quartic surface (a K3, which had simply hidden its points above
height 1500, exactly the failure mode a quartic surface invites).
It is **not** a frame solution: $c_1^2+s_1^2 = 137\cdot 8297$ and
$c_2^2+s_2^2 = 29\cdot 401\cdot 1109$ are not squares.  So the
Pythagorean/primality hypotheses are **load-bearing**, and a descent
on the bare surface would have been an attempt to prove a false
theorem.  The correct target is the **prime-frame version**: no
solution with $c_1+is_1=\pi^2$, $c_2+is_2=\rho^2$ for Gaussian
primes $\pi,\rho$ — machine-checked empty to $p,q<2000$, and no
congruence in the frame variables obstructs it.  In that form the
equation reads
$$\mathrm{Re}(\rho^8) \;=\; N(\pi)^2\,\mathrm{Re}(\pi^4),$$
a relation between the *arguments* of two Gaussian primes, and the
primality supplies a lever the surface lacks: $p^2\mid\mathrm{Re}(\rho^8)$
forces $(\rho/\bar\rho)^8\equiv-1 \pmod{\pi^2}$, an element of order
$16$ in the cyclic group $(\mathbb{Z}[i]/\pi^2)^\times$ of order
$p(p-1)$, hence **$p\equiv 1 \pmod{16}$** — a constraint on the prime
itself, invisible to any frame-level sieve, and confirmed on data
(below $3000$ the only prime ever admitting $p^2\mid\mathrm{Re}(\rho^8)$
is $17$).  The attack is therefore Gaussian-prime arithmetic, not K3
geometry.

**The descent, as far as it goes (entry 73; check
`a3.rigidity_frame_lemma`).**  Write $R_4 + iI_4 = \rho^4$ (so
$R_4^2+I_4^2 = q^4$, coprime, $R_4$ odd, $I_4 \equiv 0 \bmod 8$).
The endpoint is $(R_4-I_4)(R_4+I_4) = p^2 A_4$ with coprime-odd
factors on the left and $p\nmid A_4$, so $p^2$ lands wholly in one
factor: WLOG $R_4+I_4 = p^2D$, $R_4-I_4 = A_4/D$ for a divisor $D$
of $A_4$, and adding squares,
$$2q^4 \;=\; p^4D^2 + (A_4/D)^2. \tag{$*$}$$
This turns the lemma into a **finite check per prime $p$** over the
divisors of $A_4$, valid for all $q$ at once — and $(*)$ has no
solution for any prime $p<10^6$ (entry 73).  Two divisor cases are
theorems:

* $D=\pm1$: $2q^4 = (c_1^2+s_1^2)^2 + (c_1^2-s_1^2)^2 = 2(c_1^4+s_1^4)$,
  so $q^4 = c_1^4 + s_1^4$ — **Fermat's $x^4+y^4=z^4$.**
* $D=\pm A_4$ (i.e. $R_4 - I_4 = \pm1$): $(p^2A_4)^2 + 1 = 2q^4$ —
  **Ljunggren's $x^2+1=2y^4$**, whose only solutions are $y\in\{1,13\}$;
  at $q=13$ it needs $p^2 \mid 239$, a prime.

Since $A_4 = (c_1-s_1)(c_1+s_1)$ is composite by construction, the
natural splits $D = \pm(c_1\pm s_1)$ are the heart of the general
case.  Case N ($D = c_1+s_1$) is *equivalent* to
$$\rho^4 \;=\; \pi^2 + K(1+i),\qquad K = \tfrac{(p^2-1)(c_1+s_1)}{2},$$
i.e. $R_4 - c_1 = I_4 - s_1 = K$ (pinned exact): the $q$-prime's
fourth power and the $p$-prime's square differ by a "diagonal"
multiple of $1+i$.  It forces $c_1\equiv1$, $s_1\equiv0 \pmod 8$ and
$q\equiv1\pmod 8$ on top of $p\equiv1\pmod{16}$, is consistent modulo
$\pi$ and $\bar\pi$ (so no cheap kill), and in $\mathbb{Z}[\sqrt2]$
reads $N(q^2+I_4\sqrt2) = N(p^2+ps_1\sqrt2)$ — two elements of equal
norm $p^2A_4$ related by recombining the split primes.  **The general
intermediate-$D$ case is the open proof obligation.**  Status: proven
for the extreme divisors, verified for every $p<10^6$ and all $q$,
reduced to a clean two-ring ($\mathbb{Z}[i]$, $\mathbb{Z}[\sqrt2]$)
recombination problem in the middle.

**The intermediate case: what it is, and the quartic sieve (entry 74;
`compute/quartic_sieve.py`, check `a3.rigidity_quartic_sieve`).**
Three structural facts first.  *(i) The obstruction is quadratic:*
$T=(p^4D^2+E^2)/2$ is never even a perfect *square* for intermediate
$D$ (57,392 cases, $p<2\cdot10^5$), so the equation already fails at
$(p^2D)^2+E^2=2X^2$ before any fourth-power condition.  *(ii) But it
is not local:* no modulus has $T$'s residues missing the squares, every
Jacobi symbol the equation forces to $+1$ is $+1$, and the primes
witnessing non-squareness are random large primes.  *(iii) It is a
congruent-number question:* "$T$ square" means $(X^2\pm A)/2$ are both
squares with $A=c_1^4-s_1^4$, i.e. a Pythagorean $(I,R,X)$ with
$R^2-I^2=A$, i.e. $m^4-6m^2n^2+n^4=A$ — a point on
$y^2=A(x^4-6x^2+1)$, whose Jacobian is $Y^2=X(X{+}4)(X{+}8)\cong
y^2=x^3-x$ (isogeny confirmed by point counts), so the twisted curve is
**the congruent-number curve $y^2=x^3-A_4^2x$ for $n=A_4=c_1^2-s_1^2$.**
And $A_4=\mathrm{Re}(\pi^4)=a^4-6a^2b^2+b^4$ is itself a value of the
quartic form, so the frame point $x=a/b$ is a non-torsion rational
point: **rank $\ge1$ for every $p$** (Tunnell agrees on all 26 primes
tested).  Hence no rank-0/Selmer argument exists; the lemma is an
*integral-point* statement on a positive-rank curve — which is why
no sieve on $T$ can see it.

The lever is the **fourth power**.  $(1+i)\rho^4=E+ip^2D$ with
$\rho^4=R_4+iI_4$, $R_4=(p^2D+E)/2$, $I_4=(p^2D-E)/2$; reducing
modulo every Gaussian prime $\lambda$ of $D$, $E$, $R_4$, $I_4$ (and
of $K$ in the natural split, where $\rho^4=\pi^2+K(1+i)$) turns the
equation into quartic-residue conditions on data computable from
$(p,D)$ alone, with one shared unknown unit $\varepsilon=i^j$:
$[D]$ $\chi_\lambda(E)+\chi_\lambda(1{+}i)=\chi_\lambda(2)+j\chi_\lambda(i)$;
$[E]$ $\chi_\lambda(p^2D)=j\chi_\lambda(i)+\chi_\lambda(1{+}i)$;
$[R]$ $\chi_\lambda(i)+\chi_\lambda(I_4)=0$; $[I]$ $\chi_\lambda(R_4)=0$;
$[K]$ $2\chi_\lambda(\pi)=0$.  A case with no admissible $j$ is
provably dead.  Two closed-form consequences: **an inert prime
$\ell\equiv7\pmod{16}$ dividing $A_4$ kills every $D$** (there
$\chi_\ell(1{+}i)=-1$ while $\chi_\ell$ is trivial on rational
integers), and in the natural split **$3\mid K$ always, forcing $p$ to
be a quadratic residue mod 3, i.e. $p\equiv1\pmod3$** (this is what
kills the first survivor of the plain $[D][E]$ sieve, $p=113$).  The
With *signed* $(D,E)$ the equation is exact — there is no unit at all
($\varepsilon=1$), so every condition is a fixed equality — and two
further natural families apply: $[2]$ $\rho^4 \bmod 32$ and $\bmod 64$
lies in a fixed small set; $[C]$ combination primes
$\lambda\mid uR_4+vI_4$ give $\rho^4\equiv I_4(ui-v)/u$.  The sieve is
sound — synthetic true solutions $(1+i)\rho^4$ pass the *full* sieve
end to end — and on data it is complete: the $[D][E][R][I][K]$ system
alone left exactly two survivors below $15000$, both at $p=5569$ where
$A_4=-31\cdot239\cdot2671$ has every prime $\equiv15\pmod{16}$ (the
*transparent* class in which the quartic characters carry no
information); $[2]$ kills one and $[C]$ the other, and **the upgraded
sieve has no residual at all for $p<15000$** ($3128$ cases: $2416$
die $2$-adically, $477$ at $[D]$, $183$ at $[E]$, $44$ at $[R]$, $7$
at $[I]$, $1$ at $[C]$).  **Status of the intermediate case: a
quartic-residue sieve, complete on data, verified empty to $10^6$ by
the finite check — not a proof.**  Any finite list of local conditions
leaves a residual class in principle; a proof needs a reciprocity
argument that the conditions are globally inconsistent — the
classical Fermat/Euler route — and the sieve's kill statistics say
exactly which conditions carry the weight: the $2$-adic one first,
then the characters at the primes of $A_4$ itself.

**The reciprocity verdict (entry 75; check `a3.rigidity_reciprocity`).**
Attacking that argument produced two theorems and closed the route.

*Class Lemma (proven).*  For **any** primitive $\rho\in\mathbb{Z}[i]$,
every odd prime dividing $\mathrm{Re}((1+i)\rho^4)$ or
$\mathrm{Im}((1+i)\rho^4)$ is $\equiv1$ or $15\pmod{16}$.  Proof: a
split $\lambda\mid\mathrm{Im}$ makes $(1+i)\rho^4$ congruent to a
rational integer mod $\lambda$; conjugating the same statement at
$\bar\lambda$ makes $(1-i)\bar\rho^4$ congruent to the same integer
mod $\lambda$, so $(\rho/\bar\rho)^4\equiv-i\pmod\lambda$: $-i$ is a
quartic residue, forcing $\ell\equiv1\pmod{16}$ (a split
$\lambda\mid\mathrm{Re}$ gives $+i$, same conclusion); an inert $\ell$
needs $\chi_\ell(1+i)=1$, which holds iff $\ell\equiv15\pmod{16}$.
Verified on synthetic fourth powers with zero exceptions.  Applied to
$E+ip^2D=(1+i)\rho^4$: **every prime of $A_4=DE$ is $\equiv\pm1\pmod{16}$**
— a condition on $p$ alone that $\sim84\%$ of primes $p\equiv1\pmod{16}$
fail.  With the order-16 lemma, **the rigidity lemma is a theorem for
$\sim96\%$ of all split primes $p$**; the survivors form the thin
*transparent* class.

*2-adic Lemma (proven by exhaustion).*  $(1+i)\rho^4\equiv1+i\pmod{16}$
for every primitive $\rho$ (all 8192 residues mod 128), i.e.
$\rho^4\equiv1\pmod{(1+i)^7}$.  Hence $E\equiv p^2D\equiv1\pmod{16}$,
and with $p^2\equiv1\pmod{32}$: **$D\equiv E\equiv1\pmod{16}$**.  This
is the sieve's dominant killer, now in closed form; on data it is
exactly equivalent to the mod-$32$/$64$ set test.

*The Reciprocity Law — a consistency, not an obstruction.*  Over
every transparent intermediate case (404 cases, $p<20000$, with or
without the 2-adic restriction) the sum of all $[D]$ and $[E]$
condition values over the Gaussian primes of $D$ and $E$ is
$\equiv0\pmod 4$ without exception.  That is the signature of a
reciprocity identity: quartic reciprocity makes the $[D][E]$ system
**globally consistent**.  So the classical Fermat/Euler contradiction
does *not* exist at the $(D,E)$ level — every $[D][E]$ kill is an
individual term failing, never a global parity — and the 68 cases
(to $p<20000$) that pass $\{2\text{-adic},\text{class},[D],[E]\}$ are
killed only by $[R][I][C]$, the conditions at the primes of
$R_4=(p^2D+E)/2$ and $I_4=(p^2D-E)/2$: the hypothetical $\rho^4$'s own
components, transversal to the $p$-side data, and not
reciprocity-closable in terms of it (their contributions to the
global sum are mixed: 46 zero, 22 nonzero).

**Where this leaves the lemma.**  Proven for $\sim96\%$ of split
primes (order-16 + Class Lemma); in the transparent class, proven to
force $D\equiv E\equiv1\pmod{16}$ and the $[D][E]$ residue system;
that system is reciprocity-consistent, so the remaining obstruction
is genuinely global — "$(E+ip^2D)/(1+i)$ is not a fourth power" is
detected only at its own primes.  Verified empty to $10^6$ by the
finite check.  A proof of the transparent class needs a new idea — a
height or integral-point argument on the congruent-number curve of
$A_4$, not local residuosity.

**The height argument (entry 76; `compute/selmer_descent.py`, check
`a3.rigidity_height`).**  *Theorem (proven).*  A solution of the
endpoint gives $(I,R,X)$ Pythagorean with $R^2-I^2=A=p^2A_4$, hence
the **integral** point $P_{\mathrm{sol}}=(X^2,\,2IRX)$ on
$E:\ y^2=x^3-A^2x$ (indeed $x-A=2I^2$, $x+A=2R^2$), whose 2-descent
image is $(X^2,2I^2,2R^2)\equiv(1,2,2)$.  The frame point
$P_0=(p^2,\,2c_1s_1p)$ has image $(p^2,2s_1^2,2c_1^2)\equiv(1,2,2)$
as well, and $\ker\delta=2E(\mathbb{Q})$, so
$$P_{\mathrm{sol}}\in P_0+2E(\mathbb{Q}).$$
Everything therefore turns on the rank of $E_{A_4}$.  A complete
2-descent (local images at the odd primes of $A_4$, at $2$ — including
points of negative 2-adic valuation, which supply the class $(1,5,5)$
— and at $\infty$; exact on rank-0 and rank-1 controls) gives the
2-Selmer rank bound, and on the transparent primes below $6000$ it is
**1 for four of them and 2 or 3 for ten.**  Where it is $1$ the rank is
exactly $1$ ($P_0$ has infinite order), $E(\mathbb{Q})=\langle G\rangle\oplus E[2]$,
$P_{\mathrm{sol}}=kG+T_0$ with $k$ odd, $\pm P_0$ are excluded by
$w=1\ne p$, and every odd multiple of $P_0$ up to $k=11$ is
non-integral ($p\mid\mathrm{denom}\,x(2P_0)$; the denominators of
$3P_0$ already run to 30–57 digits) — so for those primes the quadratic
lemma reduces to an effective integrality statement for odd multiples
of an integral point, standard (elliptic divisibility sequences /
Baker) but not carried out here.  Where the Selmer bound is $2$ or $3$
the rank itself is undetermined without a 4-descent or $L$-values.
One heuristic corrected along the way: $P_{\mathrm{sol}}$'s height is
*not* pinned near $2\hat h(P_0)$, because $Q(m,n)=p^2A_4$ is a Thue
equation whose solutions can be large; the rigorous version is
Siegel/Baker on the cyclic subgroup, not a height comparison.
**Status: the height argument is rigorous in structure, splits the
transparent class into a rank-1 part (provable in principle) and a
higher-Selmer part (rank unknown), and is a proof for no prime yet.**

**The Rank-1 Theorem (entry 77; check `a3.rigidity_rank1_theorem`) —
PROVEN, with no heights and no divisibility sequences.**  Let $p$ be
transparent with $\operatorname{rank}E(\mathbb{Q})=1$ for
$E:\ y^2=x^3-A_4^2x$, so $E(\mathbb{Q})=\mathbb{Z}G\oplus E[2]$ (the
torsion of every congruent-number curve is $E[2]$).  Then
$P_0=mG+T_0$ with **$m$ odd** — its descent image $(1,2,2)$ is not a
torsion image, so $P_0\notin2E(\mathbb{Q})+E[2]$ — and any solution
point, lying in $P_0+2E(\mathbb{Q})=P_0+2\mathbb{Z}G$, is
$P_{\mathrm{sol}}=kG+T_0$ with the **same** $T_0$ and $k$ odd.
Reduce modulo $p$, a prime of good reduction ($p\nmid2A_4$):
$P_0=(p^2,2c_1s_1p)$ reduces to $T_1=(0,0)$, while on this
$p$-minimal model $P_{\mathrm{sol}}=(X^2/p^2,\,2IRX/p^3)$ with
$p\nmid X$ (else $p\mid R,I$ against $\gcd(R,I)=1$) reduces to $O$.
Hence, in the **cyclic** group $\langle\tilde G\rangle\subset\tilde E(\mathbb{F}_p)$,
$$m\tilde G=\tilde T_1+\tilde T_0,\qquad k\tilde G=\tilde T_0.$$
Every case dies.  $T_0=O$: $m\tilde G=\tilde T_1$ has order $2$, so
$N=\operatorname{ord}\tilde G$ is even, yet $N\mid k$ with $k$ odd.
$T_0=T_1$: $N\mid m$ forces $N$ odd, but $k\tilde G=\tilde T_1$ has
order $2$.  $T_0=T_\pm$: $\tilde T_\pm$ and $\tilde T_\mp$ are two
*distinct* points of order $2$ inside a cyclic group.  So **no
solution exists.**  The obstruction is not the trivial one — $A_4\equiv-2s_1^2$
is a quadratic residue mod $p$, so $\tilde T_1\in2\tilde E(\mathbb{F}_p)$ —
it is the cyclicity of the reduction of a rank-one group.  The
2-descent certifies rank $1$ exactly when its Selmer bound is $1$
($P_0$ has infinite order), and the group-theoretic core is verified
by brute force inside every $\tilde E(\mathbb{F}_p)$ concerned (zero
offending configurations).

**Consequence.**  With the order-16 lemma, the Class Lemma and this
theorem, **the frame rigidity lemma is a theorem for every prime $p$
except the transparent primes whose curve $E_{A_4}$ has 2-Selmer rank
$\ge2$** — below $30000$: $21$ of the $67$ transparent primes are
proven (113, 3761, 4993, 5569, 7121, …), $46$ remain.  For those the
rank itself is the unknown; if it is in fact $1$ (nontrivial
$Ш[2]$) the same argument applies but cannot be certified by a
2-descent, and if it is $\ge2$ the reduction of the free part need
not be cyclic.

**Certifying the ranks (entry 78; check `a3.rigidity_rank_certificates`).**
*Parity is free.*  The root number of $E_n:\ y^2=x^3-n^2x$ is $+1$ for
$n\equiv1,2,3\pmod8$ and $-1$ for $n\equiv5,6,7\pmod8$; every
transparent $A_4$ has all its primes $\equiv\pm1\pmod{16}$, so
$|n|\equiv1$ or $7\pmod8$.  The 2-Selmer bound has the root-number
parity on **every** transparent prime (Dokchitser–Dokchitser parity;
an independent validation of the descent).  Hence the $46$ split:

* **$|n|\equiv1\pmod8$ ($27$ primes; Selmer bounds $2$ and $4$):** the
  rank is *even* and $\ge1$, so $\ge2$ — the Rank-1 Theorem can never
  apply.  With Selmer bound $2$ the rank is exactly $2$ (unless
  $Ш[2^\infty]$ is infinite, in which case the rank is $1$ and the
  theorem applies after all).  These need a **rank-2 argument**, not a
  certificate.
* **$|n|\equiv7\pmod8$ with Selmer bound $3$ ($19$ primes):** rank
  $1$ or $3$.  **$L'(E,1)\neq0$ certifies rank exactly $1$
  unconditionally** (Gross–Zagier–Kolyvagin), and the Rank-1 Theorem
  finishes the prime.

*The $L$-value certificate* (`compute/lseries_cm.py`).  $E_n$ is the
quadratic twist by $n$ of the CM curve $y^2=x^3-x$, so
$a_p=2\operatorname{Re}\pi$ for the primary Gaussian prime $\pi$ over
$p\equiv1\pmod4$, $a_p=0$ for $p\equiv3\pmod4$, twisted by $(n/p)$;
conductor $32n^2$; and for root number $-1$
$$L'(E,1)=2\sum_{m\ge1}\frac{a_m}{m}E_1\!\Big(\frac{2\pi m}{\sqrt N}\Big),$$
with an explicit tail bound from $|a_m|\le d(m)\sqrt m$.  Controls:
$a_p$ against point counts; $L'(37a,1)=0.30599977383405$; Tunnell's
finite formula $L(E_n,1)=\beta(A_n-2B_n)^2/(16\sqrt n)$ on rank-0
twists to ten digits; $L(E_1,1)=0.6555143885$.  **Certified — rank
$1$, rigidity lemma proven:**

| $p$ | $n$ | $L'(E,1)$ | tail $\le$ |
|---|---|---|---|
| 337 | 52319 | 2.1047928093 | $4.6\cdot10^{-8}$ |
| 1201 | 1437599 | 0.4961895104 | $1.3\cdot10^{-6}$ |
| 6353 | 3294559 | 1.5904808187 | $2.9\cdot10^{-6}$ |
| 15073 | 8162879 | 0.2776859806 | $7.1\cdot10^{-6}$ |

So below $30000$ the rigidity lemma is now a theorem for **$25$ of the
$67$ transparent primes** ($21$ by Selmer bound $1$, $4$ by
$L'$-certificate); $42$ remain: $27$ of even rank (rank-2 argument
needed) and $15$ of odd rank whose conductors ($n\ge1.5\cdot10^7$, so
$\ge3\cdot10^8$ series terms) exceed this machine.  Those, and the
scalable algebraic route (a Cassels–Tate pairing on $\mathrm{Sel}^2$),
are PARI territory (`ellrank`), which this machine does not have.

**PARI certificates and the Rank-$r$ criterion (entry 79; check
`a3.rigidity_pari_certificates`, data `compute/data_pari_ranks.json`).**
PARI/GP 2.17.4 was obtained as a portable extraction of the official
installer (verified SHA256; the installer itself demands UAC).  Its
`ellrank` performs the 2-descent and the 2-part of the Cassels pairing
and returns $[r_1,r_2,s,L]$ with $r_2=C-T-s$ an **unconditional** upper
bound ($C$ = 2-Selmer rank, $T=2$, $s$ = rank of $Ш[2]/2Ш[4]$ detected
by the pairing); $r_1$ may use parity, so we call a rank *certified*
only when the number of independent points found (independence
re-verified through descent images) equals $r_2$.  Sweep over all $67$
transparent curves, effort escalated to $8$ (to $20$ for two) and the
points 2-saturated by `ellsaturation`:

| $r_2$ | points found | curves | status |
|---|---|---|---|
| 1 | 1 | 32 | rank 1 certified → **Rank-1 Theorem, proven** (includes the 4 $L'$ primes — an independent confirmation) |
| 2 | 2 | 5 | rank 2 certified, generators known → criterion below |
| 2 | 1 (only $P_0$) | 22 | rank 2 (upper bound unconditional; lower bound by parity), second generator beyond effort-20 search |
| 3 | 3 | 2 | rank 3 certified, generators known → criterion below |
| 3 | 1 | 6 | rank 1 or 3; $s=0$ means either rank 3 or $Ш$ with 4-torsion |

*The Rank-$r$ criterion (proven).*  Let $\Lambda=\langle G_1,\dots,G_r\rangle+E[2]$
have **odd** index $d$ in $E(\mathbb{Q})$ (2-saturation).  A solution
gives $P_{\mathrm{sol}}=P_0+2Q$; reducing, $2\tilde Q=\tilde T_1$; and
$dQ=\sum a_iG_i+T$ gives
$\tilde T_1=d\tilde T_1=2d\tilde Q=2\sum a_i\tilde G_i\in 2H$, $H=\langle\tilde G_1,\dots,\tilde G_r\rangle$.
So **$\tilde T_1\notin 2H$ implies no solution** — a finite computation
in $\tilde E(\mathbb{F}_p)$ once generators are known (for $r=1$ it is
automatic: the Rank-1 Theorem).  On the seven complete generator sets it
**proves $p=3137,\,8369,\,9473,\,13633$** (rank 2) and fails for
$2657$ (rank 2), $9137,\,29201$ (rank 3): there $H$ genuinely contains
a half of $\tilde T_1$, i.e. a rational point in the right coset
reduces to $O$, and the mod-$p$ method cannot work for those primes at
all — they need the integrality/height side.

*The 2-descent is blind at $p$.*  $2$ is a quartic residue modulo
every transparent $p<30000$ (equivalently $1+i$ is a square mod $p$), so
the halves $(\pm in,\cdot)$ of $\tilde T_1$ have trivial descent class —
$\tilde T_1\in4\tilde E(\mathbb{F}_p)$ — and every 2-Selmer class
localizes trivially at $p$.  Hence no criterion using only Selmer
classes can ever apply in the transparent class; only full generators
carry information.

*$L'$ for the undetermined.*  A segmented coefficient sieve (memory
$O(\text{block})$) reaches $n\sim2\cdot10^7$ and certifies rank $1$ for
three of the six:

| $p$ | $n$ | $L'(E,1)$ | tail $\le$ | terms |
|---|---|---|---|---|
| 4001 | 14724799 | 2.8979305410 | $1.3\cdot10^{-5}$ | $3.3\cdot10^8$ |
| 4657 | 16471199 | 25.0428222709 | $1.4\cdot10^{-5}$ | $3.7\cdot10^8$ |
| 4817 | 18969439 | 10.4236084369 | $1.7\cdot10^{-5}$ | $4.3\cdot10^8$ |

Rank $1$, proven — and since the Cassels pairing saw nothing on these
curves, $Ш\supseteq(\mathbb{Z}/4)^2$ there: the case a 2-descent can
never settle.

### 2.12 Front A: the endpoint extractor and the type census (entry 81)

*The first step of the adopted plan (ROADMAP §R.6-A): make the hand-trees
of A3.8–A3.10 mechanical, so the whole $(a,b)$ ladder can be seen at
once.*  Module `compute/lucas_endpoints.py`, check `a3.lucas_extractor`.

**The three facts that make it mechanical.**  In the cleared relation
$\sum_i c_i\,p^{2(J-|j_i|)}q^{2(K-|k_i|)}\operatorname{Im}(\ell^{2j_i}w^{2k_i})=0$:

1. *Collapse.*  The cleared weights are exactly the relative weights in
   the sum-to-product identity, so any two terms collapse to
   $\pm2p^{2a}q^{2b}\operatorname{Trig}_1(D)\operatorname{Trig}_2(M)$ with
   $D,M$ the half-difference and half-sum monomials.  No sign
   convention is trusted: each collapse is found as an exact
   polynomial identity in $\mathbb{Z}[c_1,s_1,c_2,s_2]$.
2. *Units.*  A trig-monomial involving $\ell$ is a $p$-unit and one
   involving $w$ a $q$-unit ($\pi$ divides one of the two conjugate
   products, never both).  Only a **pure**-$w$ monomial can absorb a
   power of $p$; only a pure-$\ell$ one a power of $q$.
3. *Lever.*  Collapse the pair of minimal weight at a lever prime; the
   third term's surplus $P^e$ must divide the product, hence land on a
   pure factor of the other prime — or the pattern is dead.  What
   remains is the **endpoint**: $P^e\mid\operatorname{Trig}(\text{pure})$
   plus the residual product equation.

**The census.**  Surveying boxes with the engine's general layers
(complete enumeration, `canon_full` dedup):

| box | canonical patterns | OPEN | distinct OPEN | endpoint families | new families |
|---|---|---|---|---|---|
| (2,1) | 224 | 34 | 26 | 17 | 17 |
| (2,2) | 1144 | 136 | 120 | 72 | 55 |
| (3,2) | 3264 | 322 | 298 | 177 | 105 |
| (4,1) | 1456 | 140 | 124 | 86 | 41 |
| (3,3) | 9200 | 732 | 696 | 396 | 219 |
| (4,2) | 7084 | 576 | 544 | 328 | 110 |
| (5,1) | 2720 | 220 | 200 | 140 | 54 |

Every one of the $2008$ distinct OPEN patterns is an ENDPOINT (no
failed collapse, none dead by the pure-factor rule); every OPEN
distinct pattern carries a lever (the only unit-balanced residuals are
the two-term doubled patterns).  The families are exponent-parametrized
and **grow with the box**, as an infinite ladder must — but they fall
into **about eighteen shape types** (which of $D,M,C$ is pure-$w$,
pure-$\ell$ or mixed, and where the levers land).  The dominant types
carry a mixed factor and a mixed third term; the fully separated types
(pure × pure against a pure third term) are exactly the
Lucas-coincidence equations, the rigidity lemma among them.

**Consequence.**  A uniform $\omega\le2$ theorem is a *finite* list of
type-lemmas, each to be proved for all exponents; the hand-closed boxes
already contain proofs of many instances, to be generalized.

**The chase (same entry).**  The endpoint is rewritten in *Lucas
values* $U_y=\operatorname{Re}w^y,\ V_y=\operatorname{Im}w^y,\ C_x=\operatorname{Re}\ell^x,\ S_x=\operatorname{Im}\ell^x$
(a mixed third term expands by $\operatorname{Im}(\ell^xw^y)=S_xU_y+C_xV_y$,
doubled exponents reduce by the double-angle formulas), and every such
equation is verified to reproduce the cleared relation exactly — 146
of 146 on the closed boxes, in three to seven symbols.  The chase then
does what the hand-proofs did: split the equation into a product form
$\prod A_i=\pm\prod B_j$, derive per-atom divisibilities from the
structural coprimality facts ($\gcd(U_y,V_y)=\gcd(C_x,S_x)=1$; $U,C$
odd, $V,S$ even; $\ell$-side values are $p$-units, $w$-side values
$q$-units — a $p$-power dividing a $w$-side value is *content*, the
lever, never structure; a polynomial factor is coprime to its own
symbol when its other term is), and close them by the lemma
$X\mid P^eY,\ Y\mid X,\ P^e\mid X,\ \gcd(P,Y)=1\Rightarrow X=\pm P^eY$.
**It re-derives the rigidity lemma**: from both Block-A patterns it
returns $U_4=\pm p^2C_2$ with residual $S_2(4C_2+p^2)\mp V_4=0$ —
the hand derivation, sign cases included (pinned in
`a3.lucas_extractor`).  On the closed boxes the coincidences it finds
are of a handful of types only:
$S_x=\pm V_y$, $U_y=\pm p^2C_x$, $V_y=\pm p^2S_x$, $C_x=\pm q^2U_y$,
$S_x=\pm q^2V_y$ and mirrors — **the Lucas-coincidence family, now
produced by machine.**  The full chase uses all three pair-collapses of a pattern (all three
identities hold), the Pythagorean rewrites $U_y^2\to q^{2y}-V_y^2$
etc. before splitting, every split of up to six terms, a depth-1
substitution of each derived equality into the other collapse
equations, and drops tautologies; each equality is classified as
*parity-dead* (odd = even), *unit collapse* ($X=\pm P^e$), weighted or
unweighted *coincidence* ($X=\pm P^eY$, $X=\pm Y$) or *rearrangement*.

*Coverage and the coincidence types.*  Box (2,1): 14 of the 26
endpoints reach a coincidence and 12 do not (rearrangements only, or
no equality — their equations mix exponents such as 1, 3, 4 on one
side, and after the general multiple-angle reduction to the gcd
exponent they need the Gaussian-prime valuation arguments of the
hand-proofs, the next layer) — and the coincidences are of exactly
six types: $S_2=\pm V_2$, $S_4=\pm V_2$,
$V_2=\pm S_2$, $V_2=\pm S_4$, $U_2=\pm p^2C_2$, $V_2=\pm p^2S_2$
(pinned).  The weighted ones are the $(k,j)$-family of the rigidity
lemma ($U_4=\pm p^2C_2$ is $(4,2)$; $U_2=\pm p^2C_2$ is $(2,2)$).
Box (2,2): 40 of the 120 endpoints reach a coincidence, of exactly
sixteen types — the eight unweighted $S_x=\pm V_y$, $V_y=\pm S_x$
with $x,y\in\{2,4\}$, and the eight weighted $U_y=\pm p^2C_2$,
$V_y=\pm p^2S_2$, $C_x=\pm q^2U_2$, $S_x=\pm q^2V_2$ for
$x,y\in\{2,4\}$ — i.e. the weighted family is
$\operatorname{Trig}(w^y)=\pm p^2\operatorname{Trig}(\ell^2)$ and its
mirror, the Lucas-coincidence family with the prime-square weight
fixed by the box.

*A coincidence alone never kills.*  $S_2=\pm V_2$ says two primitive
frames with prime hypotenuses have equal leg products $c_1s_1=c_2s_2$,
i.e. equal congrua — and that happens: $(a,b)=(5,2)$ and $(6,1)$ both
give the congruum $840$ with hypotenuses $29$ and $37$; six such pairs
below generator $60$ ($(109,197)$, $(193,401)$, …).  So every
type-lemma is a statement about the **system** coincidence + residual
(for the rigidity family: $U_4=\pm p^2C_2$ *and*
$S_2(4C_2+p^2)\mp V_4=0$), and the chase reports both.  **The valuation layer (same entry).**  Every collapse identity is an
equality of *products*, $\pm2p^{2a}q^{2b}\operatorname{Trig}_1(D)\operatorname{Trig}_2(M)=-c\,p^{2a'}q^{2b'}\operatorname{Im}(C)$,
so the $p$- and $q$-adic valuations balance term by term — and the
$q$-adic valuations of *all* the $\ell$-side Lucas values are governed
by one unknown, the rank of apparition $r=\operatorname{ord}(\ell/\bar\ell \bmod \rho)$,
through the lifting-the-exponent lemma:
$v_q(S_n)=v_0+v_q(n/r)$ if $r\mid n$ (else $0$),
$v_q(C_n)=v_0+v_q(2n/r)$ if $r\mid 2n,\ r\nmid n$ (else $0$), with
$v_0=v_q(S_r)\ge1$; likewise the $w$-side at $p$.  Three collapses ×
two primes give six linear balance equations in $(v_0,v_0')$ over the
finitely many $(r,r')$ cases (and the finitely many small primes that
could divide an exponent ratio): no solution is a rigorous kill; the
survivors are exact divisibility configurations.  It kills the
endpoint above at once ($\operatorname{Im}\ell^4=4C_1S_1C_2$ carries
$C_1$, so the $q^2$ cannot balance), kills 4 of 26 in (2,1) and 16 of
120 in (2,2), and **on the rigidity family it returns
$r'=8$, $v_p(\operatorname{Re}w^4)=2$ in every configuration — the
order-16 lemma, by machine.**  So an endpoint is now a *system*:
valuation configuration + coincidence + residual, each part
mechanical.

**Residual analysis (same entry).**  Lucas values of primitive
Gaussian powers never vanish, $U,C,p,q$ are odd and $V,S$ even, so a
residual factor that is odd as a polynomial cannot be zero; a
coincidence whose residual carries such a factor in *both* sign
branches kills the pattern.  On the (2,1) box this is exactly what
the hand-proofs did: ten of the fourteen coincidence endpoints have
residuals $2U_2\pm p^2$, $2U_2\pm p^4$ or $2C_2\pm q^2$ — odd — and
die; the surviving four are one system,
$$U_2=\pm p^2C_2,\qquad V_2=\pm S_2(4C_2+p^2),$$
the $(2,2)$-member of the rigidity family (the rigidity lemma is
$(4,2)$: $U_4=\pm p^2C_2$, $V_4=\pm S_2(4C_2+p^2)$).  Combined with
the valuation layer, the machine closes $14$ of the $26$ (2,1)
endpoints outright, isolates $4$ as one coincidence system, and
leaves $8$ for the Gaussian-prime concentration arguments of A3.8.
Next: the type-lemmas — the $(k,2)$ family $U_k=\pm p^2C_2$,
$V_k=\pm S_2(4C_2+p^2)$ first (reduction rigidity with explicit
exceptional sets, as for $k=4$), unit collapses via primitive
divisors, and the concentration layer for the rest.

### 2.13 The rigidity system is a fixed curve (entry 82)

*What the machine's residual changes.*  The entry 73–79 campaign
attacked the rigidity lemma as the single equation
$\operatorname{Re}\rho^8=p^2\operatorname{Re}\pi^4$, i.e. $U_4=\pm p^2C_2$,
with the prime $p$ as a parameter — hence a congruent-number curve
*per prime* and a rank question per prime.  The chase attaches to that
coincidence a **second equation**, the residual
$V_4=\pm S_2(4C_2+p^2)$, and the two together determine $w^4$
completely:
$$w^4\in\{\pm Z,\ \pm\bar Z\},\qquad Z:=p^2C_2+i\,S_2(4C_2+p^2).$$
Writing $\ell=\pi^2$ and using $p^2=\ell\bar\ell$, $C_2=\operatorname{Re}\ell^2$,
$S_2=\operatorname{Im}\ell^2$:
$$Z=\ell^4+\ell^3\bar\ell-\bar\ell^4=\bar\pi^{8}\,(s^8+s^6-1),\qquad s:=\pi/\bar\pi$$
(verified exactly on every prime frame; check `a3.rigidity_fixed_curve`).
The same system with $U_2,V_2$ is the $(2,1)$-box survivor, and in
general the **$(k,2)$-family** $U_k=\pm p^2C_2$, $V_k=\pm S_2(4C_2+p^2)$
says $\rho^{2k}=\varepsilon Z$ (or its conjugate), i.e.
$$s^8+s^6-1=\varepsilon\,\rho^{2k}\bar\pi^{-8}\in\varepsilon\,(\mathbb{Q}(i)^*)^{\gcd(2k,8)}.$$

**Theorem.**  A solution of any $(k,2)$-system is a $\mathbb{Q}(i)$-point
$(s,y)$ with $s=\pi/\bar\pi$ on the **fixed** curve
$H_\varepsilon:\ y^2=\varepsilon(s^8+s^6-1)$ (genus 3), and for even
$k$ on $C_\varepsilon:\ y^4=\varepsilon(s^8+s^6-1)$ (genus 9), $\varepsilon$
a unit; $s$ determines $p$ (it has denominator $p$) and $y$ determines
$\rho$.  Hence, by Faltings, **the $(k,2)$-family — the rigidity lemma
included — has only finitely many solutions $(p,q,k)$ altogether**,
unconditionally though ineffectively: the lemma can fail for at most
finitely many primes $p$.  Machine sweep: $N(Z)=F(c_1,s_1)=p^4C_2^2+S_2^2(4C_2+p^2)^2$
is never a perfect power of exponent $\ge4$ on any prime frame below
$20000$ — the whole family, every $k\ge2$ and every $q$, in one line.

*The effective question.*  The elliptic quotient $x=s^2$,
$E_\varepsilon:\ Y^2=\varepsilon(x^4+x^3-1)$, has over $\mathbb{Q}(i)$
two twist classes ($\varepsilon\equiv1,2$), and PARI gives the
$\mathbb{Q}$-ranks of $y^2=d(x^4+x^3-1)$ as $2,1,1,1$ for
$d=1,-1,2,-2$ (conductors $4528,1132,18112,18112$), so
$\operatorname{rank}E_1(\mathbb{Q}(i))=3$, $\operatorname{rank}E_2(\mathbb{Q}(i))=2$:
the elliptic quotient alone does not finish, and elliptic Chabauty
needs rank $<[K:\mathbb{Q}]=2$.  The route is the other quotient of
$H$: since $s^8+s^6-1=G(s^2)$, $\operatorname{Jac}(H)\sim E\times\operatorname{Jac}(H')$
with $H':\ Y^2=x(x^4+x^3-1)$ of genus 2, and $H(\mathbb{Q}(i))$ lifts
from $H'(\mathbb{Q}(i))$ two-to-one via $(s,y)\mapsto(s^2,sy)$.  Facts
about $H'$ (odd part of the conductor $283$; PARI cannot settle the
2-part, so its analytic-rank output is *not* to be trusted): torsion
of $\operatorname{Jac}(H')$ divides $2$ over $\mathbb{Q}$ and $4$ over
$\mathbb{Q}(i)$ (reductions at all good primes below $200$); $H'(\mathbb{Q})$
contains $\infty,(0,0),(\pm1,\pm1)$ — six points against torsion $\le2$,
so $\operatorname{rank}\operatorname{Jac}(H')(\mathbb{Q})\ge1$
rigorously; an exact search to height $60$ finds the $\mathbb{Q}(i)$-points
with $x\in\{0,\pm1,\pm i,\pm2i\}$ (fourteen points with $\infty$) and
no others.  So $H'(\mathbb{Q}(i))$ is finite (Faltings) but not
torsion-enumerable: its determination is a genus-2 Chabauty /
Mordell–Weil-sieve problem over $\mathbb{Q}(i)$ (2-descent on the
Jacobian and its $-1$-twist, Coleman integration: Magma territory).
The unit-circle points that matter — $s=\alpha/\bar\alpha$ — are
absent for every primitive $\alpha$ with $N(\alpha)\le1.96\cdot10^6$
(623,895 of them; only $\alpha=1$).  What was a rank problem per
prime is now one curve.

*The ladder census (same entry).*  Valuation layer first, then chase +
residual, on the distinct OPEN patterns:

| box | dead (valuation) | dead (residual) | coincidence systems | rearrangement only | no equality |
|---|---|---|---|---|---|
| (2,1) | 4 | 10 | 4 | 2 | 6 |
| (2,2) | 16 | 24 | 16 | 4 | 60 |
| (3,2) | 28 | 38 | 24 | 28 | 180 |
| (4,1) | 16 | 24 | 10 | 18 | 56 |
| (3,3) | 48 | 60 | 36 | 78 | 474 |
| (4,2) | 48 | 56 | 36 | 36 | 368 |
| (5,1) | 20 | 30 | 12 | 22 | 116 |

The surviving coincidence systems are of **four weighted shapes
only**, $\operatorname{Trig}(w^k)=\pm p^{2e}\operatorname{Trig}(\ell^{2j})$
and their mirrors: $(2j,2e)=(2,2)$ — $U_k=\pm p^2C_2$ for $k=2,4,6$
and $C_k=\pm q^2U_2$ for $k\le8$, the fixed-curve family above;
$(4,4)$ — $U_k=\pm p^4C_4$; $(2,4)$ — $V_k=\pm p^4S_2$; $(2,8)$ —
$V_2=\pm p^8S_2$.  The no-equality fraction grows with the box (68%
at (3,3)): the Gaussian-prime concentration layer of the hand-proofs
is the machine's main missing piece.

### 2.14 The concentration theorem: every weighted coincidence family of the ladder is empty (entry 83)

The finiteness of §2.13 becomes *emptiness*, by the argument A3.8
used for E3, applied to the pinned Gaussian integer.  Take the
rigidity system: $\rho^{2k}=Z_+=\ell^4+\ell^3\bar\ell-\bar\ell^4$
(the other sign/conjugate cases are mirrors).  Then
$$\rho^{2k}+\bar\ell^4=\ell^3(\ell+\bar\ell)=2c_1\pi^6,\qquad
\rho^{2k}+\bar\ell^4=(\rho^k+i\bar\ell^2)(\rho^k-i\bar\ell^2).$$
The two factors differ by $2i\bar\ell^2=2i\bar\pi^4$, so their gcd
divides $2$; hence $\pi^6$ lies wholly in one factor, and the other,
$B$, divides $2c_1$: $|B|\le2|c_1|<2p$.  But $B\pm2i\bar\pi^4\equiv0
\pmod{\pi^6}$, so either $B=\mp2i\bar\pi^4$ (modulus $2p^2>2p$) or
$|B\pm2i\bar\pi^4|\ge p^3$ — while $|B\pm2i\bar\pi^4|<2p+2p^2<p^3$
for $p\ge3$.  **Contradiction, for every $k\ge1$ and all $p\ne q$**;
$q$ never enters.  The same three lines dispose of
$Z_-=\ell^4+2is_1\bar\ell^3$ (E3's identity: $\rho^{2k}-\ell^4=2is_1\bar\pi^6$),
of the Block-A opposite-sign integer $W=-(\ell^4+\ell\bar\ell^3+\bar\ell^4)$
($W+\ell^4=-2c_1\bar\pi^6$), and — mechanically — of every weighted
family the census found.

**Theorem (concentration kill, mechanical).**  Let $w^k=P(\ell,\bar\ell)$
be pinned.  If $P-T=\mathrm{cof}\cdot\lambda^{2a}$ for a target
$T=\pm\bar\ell^{2j}$ ($\lambda=\pi$) or $\pm\ell^{2j}$ ($\lambda=\bar\pi$),
$a\ge2$, with $2p^j>|\mathrm{cof}|_{\max}$ and
$|\mathrm{cof}|_{\max}+2p^j<p^a$ for all $p\ge5$ (polynomial
inequalities in $p$, certified by an exact real-root count), then the
system has no solution.  Certificates (`a3.concentration_theorem`,
24 in all — every sign and conjugate variant):

| family | pinned $P$ | target | $\lambda^{2a}$ | cofactor |
|---|---|---|---|---|
| (2,2) $Z_+$ | $\ell^4+\ell^3\bar\ell-\bar\ell^4$ | $-\bar\ell^4$ | $\pi^6$ | $\ell+\bar\ell$ |
| (2,2) $Z_-$ | $\ell^4+2is_1\bar\ell^3$ | $+\ell^4$ | $\bar\pi^6$ | $\ell-\bar\ell$ |
| Block A opp. $W$ | $-(\ell^4+\ell\bar\ell^3+\bar\ell^4)$ | $-\ell^4$ | $\bar\pi^6$ | $-(\ell+\bar\ell)$ |
| (4,4) | $Z_+(\ell^2)$ | $-\bar\ell^8$ | $\pi^{12}$ | $\ell^2+\bar\ell^2$ |
| (2,4) | $V_2=\pm p^4S_2$, $U_2=\mp(C_2^3-7C_2S_2^2)$ | $\mp\bar\ell^6$ | $\pi^8$ | $\pm(\ell^2-\bar\ell^2)$ |
| (2,8) | $V_2=\pm p^8S_2$, $U_2=\mp(C_2^5-22C_2^3S_2^2+9C_2S_2^4)$ | $\mp\bar\ell^{10}$ | $\pi^{12}$ | $\pm(\ell^4-\bar\ell^4)$ |

The higher-$k$ members found in the $(3,3)$ box carry the *same*
residual shapes — $U_6=\pm p^2C_2$ with $V_6=\pm S_2(4C_2+p^2)$ is
$Z_\pm$ at $k=6$; $V_4,V_6=\pm p^4S_2$ with $U_k=\mp(C_2^3-7C_2S_2^2)$
is the $(2,4)$ family; and the mirrors $C_6=\pm q^2U_2$ with
$S_6=\pm V_2(4U_2+q^2)$, $S_6=\pm q^4V_2$ with $C_6=\mp(U_2^3-7U_2V_2^2)$
are the same families with $p\leftrightarrow q$ — so the certificates
above cover them (the theorem is uniform in $k$).  So **every weighted
coincidence system the ladder has produced is empty, uniformly in
$k$, $p$, $q$** — including the rigidity family of A3.10 in both its
sign variants.  The one-equation "rigidity
lemma" of entries 72–79 was never the right statement; the system is.

**A3.10, honestly.**  Of its fourteen rigidity children the machine
now closes six end to end (two by valuation, four by concentration
with certificates); the remaining eight — Block A's opposite-sign
variants and Block B — are not pinned by the chase yet (a first hand
pinning of the opposite-sign case rested on a false gcd step and was
withdrawn), so they wait for the tree layer.  **A3.10 is not claimed.**

### 2.15 Theorem A3.10: the $(2,2)$ box is closed — split part $p^2q^2$ (entry 84)

**Theorem A3.10 (PROVEN).**  For $m=2^sr\,p^2q^2$ ($p\ne q$ split
primes, $r$ inert), $D(m)$ admits no signed additive relation.
**Corollary: the split part of any MSS3 center is $p^4q$ or higher, or
has at least three distinct split primes.**

*Proof architecture* (every step machine-pinned).  The $1144$ canonical
patterns of the box partition with zero gaps (`a3.p2q2_accounting`)
into $1008$ machine kills, $34+26$ patterns of the $(2,1)$ and $(1,2)$
sub-boxes (Theorem A3.8 and its $p\leftrightarrow q$ transpose — the
cleared relation depends only on the two frames, not on the exponent
of $q$ in $m$), $32$ ledger patterns ($24$ G3 double-pincers,
$8$ H3; `a3.h3_closed`), and $44$ replications: $18$ $j$-children that
are transposes of $k$-children, and $26$ distinct $k$-children.  **The
26 $k$-children are killed by the machine, end to end**
(`a3.p2q2_theorem`, every certificate recomputed on each run):

| layer | children | mechanism |
|---|---|---|
| valuation | 4 | rank-of-apparition balance |
| residual parity | 10 | odd residual factors $2U_2\pm p^k$ |
| concentration | 8 | $Z_\pm$ pinned systems, and the content lemma ($d\mid3$) with the sliver certificate |
| unit collapse | 4 | Block B: $T=\pm q^4$, coprime split, 2-adic kill |

**The tree layer (same entry).**  Three pieces mechanize what the
hand-trees did:
*(i) The content lemma.*  A prime $r\mid S_x=\operatorname{Im}\ell^x$
makes $u=\ell/\bar\ell$ a root of unity of order $d\mid x$ modulo $r$,
so a polynomial factor $G=\bar\ell^mB(u)$ is divisible by $r$ only if
$r\mid B(\zeta_d)$: $\gcd(S_x,G)\mid\prod_{d\mid x}|\operatorname{Res}_u(B,\Phi_d)|$
(for $C_x$: orders $2d$, $x/d$ odd).  It returns $3$ for $2C_2-p^2$
against $S_2$ — the hand "content lemma $g\in\{1,3\}$" — and $1$, $3$,
$15$ for the other factors in play.  The closure then concludes
$X=\pm P^eY/d$ with $d\mid N$.
*(ii) The sliver certificate.*  For $d>1$: $w^k=P/d$ with
$U$ odd, $V$ even and $p^{2e}\mid V$, $\gcd(U,V)=1$, so
$(q^k-U)(q^k+U)=V^2$ splits into coprime halves $\{a^2,p^{4e}b^2\}$
and $q^k\ge p^{4e}+1$, while $dq^k=|P|\le|P|_{\max}$ — a contradiction
whenever $d(p^{4e}+1)>|P|_{\max}$ for all $p\ge5$.  (The hand proof of
the A3.8 sliver, now a certificate.)
*(iii) Block B — the unit collapse* (`block_b_lemma`).  The $q^4$-lever
equation factors as $2X\,T\,M=\mp4C_1S_1q^4(C_1-S_1)(C_1+S_1)$ with
$X\in\{C_1,S_1\}$ cancelling, $M=\operatorname{Im}(\ell w^4)$-type a
$q$-unit (the structural test: send $w\to0$), and $T\in\{C_1^2-3S_1^2,
3C_1^2-S_1^2\}$ odd and coprime to the cofactors (content $1$); hence
$T=\pm q^4$.  But $T=p^2-4s_1^2$ or $4c_1^2-p^2$, so $(p\mp2s_1)$ or
$(2c_1\mp p)$ are coprime factors of $\pm q^4$, forcing
$\{1,q^4\}$ and $16c_1^2$ (or $16s_1^2$) $=(3q^4\pm1)(q^4\pm3)$; the
coprime odd parts are squares, and $q^4+3=4v^2$ gives
$(2v-q^2)(2v+q^2)=3$ while $q^4-3=2v^2$ needs $v^2\equiv7\pmod8$.
Dead in every sign.

The general structural unit test (a polynomial in both frames' Lucas
symbols is a $p$-unit iff a single monomial survives $\ell\to0$) and
the cross-exponent Lucas rules ($C_{2^tn}$ coprime to $C_n,S_n$) were
what the oracle had lacked.

### 2.16 The general unit collapse; Theorem A3.8 by machine (entry 85)

Block B's kill generalizes to a module (`unit_collapse_kill`).  A lever
equation with prime $P$ factors, after cancelling common atoms, as
$\mathrm{const}\cdot(\text{one-sided atoms})\cdot T\cdot M=\mathrm{const}'\cdot(\text{one-sided atoms})\cdot P^{e}$,
with $M$ a $P$-unit (the structural test) and $T$ the single one-sided
polynomial atom that is not.  The cofactors' coprimality to $T$ is
decided by the **angle-polynomial resultant**: two same-side polynomials
$T=\bar\ell^mB_T(u)$, $G=\bar\ell^{m'}B_G(u)$ share a prime $r$ only if
$u\equiv\ell/\bar\ell$ is a common root mod $r$, so $\gcd(T,G)\mid\operatorname{Res}_u(B_T,B_G)$
(for $G=C_1\pm S_1$ this is $2$: those primes force $u\equiv\mp i$).
With every cofactor coprime and $T$ odd, $T=\pm c'P^{e}$.  Then $T$,
a quadratic form in $(C_x,S_x)$ with $p^{2x}=C_x^2+S_x^2$, must be a
difference of squares $a^2p^{2x}-b^2S_x^2$ (or with $C_x$); the coprime
split gives finitely many linear cases $ap^x\mp bS_x\in\{\pm t_1,\pm t_2P^e\}$,
each leaving $C_x^2=R(P)$ with $R$ a polynomial in $P^{e}$; and a
residual dies when, after factoring $\mathrm{den}\cdot R$ into factors
pairwise coprime up to powers of $2$, some factor $f$ is certified never
$2^k\cdot\square$ for every $k$ — by an exact modular test (units mod
$m$) or, when $f=X^2+c$, by the size argument $(2^{k/2}v-X)(2^{k/2}v+X)=c$.

It re-derives Block B exactly ($T=\pm q^4$, factors $q^4\pm3$), and it
kills the four patterns of the $(2,1)$ box that the machine had left —
the same shape with $T=\pm q^2$ and factors $q^2\pm3$ ($k$ even: size;
$k$ odd: mod $8$).  **Hence every one of the 26 distinct OPEN patterns
of the $(2,1)$ box dies in the complete machine** — 10 by residual
parity, 4 by valuation, 8 by concentration, 4 by unit collapse — with
no hand tree at all (`a3.box21_machine`; the 8 doubled patterns are
Lemma G4's).  Theorem A3.8, which took a multi-session grind of named
trees ($\beta_1$, $\beta_2$, E3, the sliver…), is now a machine
theorem.  The machine's layers, in order: valuation (rank of
apparition + LTE) → chase (collapse, closure, content) → residual parity
→ concentration / sliver → unit collapse.

*The $(2,2)$ box under the complete machine.*  Of its 120 distinct OPEN
patterns, **88 die**: 24 residual parity, 16 valuation, 32
concentration, 16 unit collapse — every sub-box pattern and every one
of the 44 replications ($k$- and $j$-children alike).  The 32 survivors
are *exactly the 32 ledger patterns* (H3's 8 and G3's 24; exponent
shape $\{1,2,2\}$ on both primes), which the hand campaign closed by
the double lever and the double pincer: two levers on one equation and
the **size windows** ($|C|,S<p^2<\sqrt2\,q^2$) pinning $C=\pm q^2$ or
$u=\pm p^2$ exactly, landing on Fermat's $x^4-y^4=z^2$.  That window
argument was the one finisher the machine still lacked; §2.17 builds it.

## 2.17 The window finisher: the $(2,2)$ box closed end to end by machine — and a ledger gap found and closed

*(2026-09-02; entry 86; `compute/window_kill.py`; checks
`a3.window_finisher`, `a3.p2q2_theorem` (strengthened).)*

**The module.**  For every pair collapse $2s\,p^{2a}q^{2b}\,T_1(D)T_2(M)
= -c\,p^{2w_p}q^{2w_q}\,\mathrm{Trig}(\text{third})$ the surplus
$p^{2e_p}$, $q^{2e_q}$ of the third term must be absorbed by the pure
factor of the right side (mixed factors are units at both primes;
$\ell$-values are $p$-units, $w$-values $q$-units) — a **lever** with
an explicit prime power on an explicit Lucas value; a negative surplus
is absorbed by the third term's own value, which must then be pure.  A
pattern's levers may sit on different collapses (G3 has one on each of
two groupings).  Each lever's value is split into **coprime-factor
targets** — a disjunction — with a size bound and a parity:
even index $2h$: $C_{2h}=(C_h-S_h)(C_h+S_h)$, coprime odd factors
$\le\sqrt2P^h$; $S_{2h}=2C_hS_h$, the coprime legs $<P^h$ ($C_h$ odd,
$S_h$ even); index $3$: $\mathrm{Re}(X^3)=X_1(4X_1^2-3P^2)$,
$\mathrm{Im}(X^3)=Y_1(4X_1^2-P^2)$, $\gcd\mid3$, the cofactor odd and
strictly inside $(-aP^2,(4-a)P^2)$.  Levers are conjunctive, targets
disjunctive: the pattern dies iff every tuple of targets dies by

* a **pincer** — $p^{\alpha}\le\kappa q^{\beta}$ and $q^{\gamma}\le
  \kappa'p^{\delta}$ give $p^{\alpha\gamma-\beta\delta}\le\kappa^\gamma
  \kappa'^\beta$, false at $p\ge5$;
* a **window** — $R^e\mid X$, $|X|<B$ and the other lever's inequality
  bound $B/R^e\le2$, so $X=\pm R^e$ exactly (parity kill when $X$ is
  even), or $B/R^e\le1$ (no $X$ at all);
* a **Fermat pin** — a leg of a frame of *even* index $h$ pinned to
  $\pm R^{e}$ with $e$ even gives $(\text{other leg})^2=(P^{h/2})^4-
  (R^{e/2})^4$, Fermat's quartic; odd $h$ or odd $e$ is refused
  ($25^2+312^2=313^2$ has $c=q^2$);
* the **index-3 cofactor pair** — both levers on cofactors,
  $4U_1^2=aq^2+tp^2$ and $4C_1^2=a'p^2+t'q^2$ with $t,t'$ odd,
  $|tt'|<9$, $a+t,\ a'+t'\in\{0,4\}\bmod8$, and the leg windows
  $0<U_1^2<q^2$, $0<C_1^2<p^2$ making each pair $(t,t')$ an empty
  interval for $r=p^2/q^2$ (the $p$-lever bounds $r$ above, the
  $q$-lever below).

**Result.**  All $32$ survivors of §2.16 die: H3's $8$ exactly as in
§2.10 (the $q^2$-window pins $C_2=\pm q^2$, Fermat; the $S_2$ branch is
a parity kill), $20$ of G3's $24$ by pincers.  **The last $4$ exposed a
gap in the hand ledger.**  Entry 63 closed "all 24 sign variants" of
$\{(1,2),(2,1),(2,2)\}$ by the pincer $q^2\mid2c_1$ or $2s_1$, $p^2\mid
c_2$ or $s_2$ — but its identities are those of the sign class with
$(2,2)$; for the class $\{(1,2),(2,1),(2,-2)\}$ (two patterns up to
$w$-conjugation, four ledger entries) *both* groupings collapse onto
index-$3$ values, $q^2\mid\mathrm{Im}/\mathrm{Re}(\ell^3)$ and $p^2\mid
\mathrm{Re}/\mathrm{Im}(w^3)$, and the stated pincer does not apply.
(For $16$ of the other $20$ one grouping is index $3$ too, but the
weaker bound $q^2<p^3$ or $p^2<q^3$ still pincers.)  Those four die
by the index-3 cofactor lemma above: three target tuples by pincers,
the cofactor–cofactor tuple by the empty-interval solver — a real
proof where the ledger had a wrong citation.  So **Theorem A3.10 now
rests entirely on machine certificates**: sub-boxes (A3.8 by machine),
$44$ replications (§2.15), and all $32$ ledger patterns through
`kill_pattern`'s window stage; $120/120$ distinct OPEN patterns of the
$(2,2)$ box die in the complete machine — $24$ residual parity, $16$
valuation, $16$ unit collapse, $32$ concentration, $32$ window (the
$16$ doubled patterns are Lemma G4's).

*Lesson recorded.*  A ledger tag is a claim, not a proof; the
identities of a hand lemma must be re-derived per sign class, which is
exactly what the machine does and the hand did not.

**The ladder under the complete stack** (distinct OPEN patterns dead /
total, doubled patterns counted dead by Lemma G4):

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 278/322 | 110/140 | 160/220 | 478/576 | 560/732 |

$1732$ of $2136$ ($81\%$); $404$ open, of exactly two shapes.  **168
single levers**, $p^{2e}\mid\mathrm{Re}/\mathrm{Im}(w^2)$, $w^4$, $w^6$
(and the $q$-mirrors in $(3,3)$), with nothing to pincer against — the
H1/H2 "bracket identity" territory of the $(3,1)$ campaign: the third
term's relation is linear in the $w$-legs once $U_2=p^{2e}t$ is
substituted.  **236 double levers in which a value has index $\ge5$**
(indices $[1,5]\times72$, $[3,5]\times40$, $[4,6]\times32$,
$[6,6]\times24$, $[1,7]\times20$, $[4,5]\times16$, …), above the
module's current targets; no double-lever pattern with both indices
$\le4$ survives anywhere.  The Chebyshev cofactor
$\mathrm{Re}(X^n)=X_1P_n(X_1^2,P^2)$ with its exact sup bound and
$\gcd\mid n$ (even $n$ by recursion through the half-index legs) is the
uniform extension and the larger next win; the residual-system
finisher for single levers is the deeper one.

## 2.18 Build A: targets at every index — and the audit of A3.7 and A3.9 by machine

*(2026-09-02; entry 87; `compute/window_kill.py`; `a3.window_finisher`
(v)–(vi).)*

**The audit first.**  Per the lesson of §2.17, the $(1,1)$ and $(3,1)$
boxes were run through the complete machine.  $(1,1)$: all $8$
distinct OPEN patterns die ($4$ residual parity, $4$ doubled) — Theorem
A3.7 is a machine theorem.  $(3,1)$: $66$ of $78$ die; the $12$
survivors are *exactly* the two hand-tree families of the A3.9 ledger,
H2 $\{(2,\pm1),(3,1),(3,-1)\}$ ($8$) and M2-opp
$\{(2,\pm1),(3,0),(3,\mp1)\}$ ($4$), both single $p$-levers
$p^2\mid\mathrm{Re}/\mathrm{Im}(w^2)$.  Their checks pin the polynomial
identities and the finite residue kills; the assignment of identities
to sign classes is hand work of the kind that hid the G3 gap.  So
**A3.9 stands on $12$ hand-closed patterns the machine cannot yet
reproduce** — the first targets of build B; nothing new is claimed
about them.

**Targets at every index.**  The frames are Gaussian squares,
$\ell=\pi^2$, $w=\rho^2$, so $X^n=(\pi^n)^2$ with $\pi^n=a+bi$,
$a^2+b^2=P^n$ odd: $\mathrm{Re}(X^n)=a^2-b^2$ is odd and
$\mathrm{Im}(X^n)=2ab\equiv0\pmod4$ at every index.  For odd $n$,
with $x=X_1/P$ and $u=x^2$,
$$\mathrm{Re}(X^n)=X_1P^{\,n-1}\,\frac{T_n(x)}{x},\qquad
  \mathrm{Im}(X^n)=Y_1P^{\,n-1}\,U_{n-1}(x),$$
Chebyshev cofactors that are polynomials in $u$; $|\cos n\theta|\le
n|\cos\theta|$ and $|\sin n\theta|\le n|\sin\theta|$ give
$|\text{cofactor}|<nP^{n-1}$; $\gcd(\text{leg},\text{cofactor})\mid n$;
termwise $X_1^2\equiv P^2\equiv1\pmod 8$ gives cofactor$_R\equiv1$ and
cofactor$_I\equiv n\pmod8$.  Even $n=2h$ recurses through the
half-index legs.  When the lever prime may divide $n$ the split cases
carry the reduced exponent, and the lever prime is then explicit ($5$,
frame $(3,4)$): the partner lever's value is an explicit integer and
the relation is evaluated exactly on the finitely many explicit frame
pairs.  Three finishers use the targets: the pincer and the window as
before (with the exact parity and residue of every target); the
**homogeneous cofactor-pair solver** (exact ranges of the cofactor
polynomials on the open interval, strict at non-attained ends, $p\ne q$
— a closed-interval version let $p/q=1$ through and was caught by the
four G3 patterns); and **pin-and-substitute**: an index-$1$ leg pin
$U_1=\pm p^e$ gives $q^2=p^{2e}+V_1^2$, and the cofactor pin with its
residue reads $p^{n-1}(Q(u)-t')=t'V_1^2$ — a sign contradiction, or,
with $(u-1)\mid Q-t'$, a perfect square $W=-p^{n-3}H(u)/t'$; when
$W=k^2(p^2-a^2C_1^2)$ with $a\ge2$, $p^2=(aC_1)^2+m^2$ contradicts the
unique two-squares representation of $p^2$.  With the recursive
targets H3 dies by pincers alone ($q^2\mid C_1\mp S_1<\sqrt2p$ or
$C_1,S_1<p$, against $p^2<\sqrt2q^2$), a simpler proof than §2.10's.

**Result.**  $108$ of the $404$ ladder survivors die — all $72$ of the
$[1,5]$ shape and $36$ across $[3,5]$, $[4,5]$, $[4,6]$, $[6,6]$:

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 294/322 | 114/140 | 164/220 | 494/576 | 628/732 |

$1840/2136$ ($86\%$).  The $296$ left are the $168$ single levers
(untouched) and $128$ double levers whose open tuples are
non-homogeneous cofactor pairs (different degrees in $p$ and $q$,
$|tt'|$ unbounded) or pins whose window is not a constant ($[1,7]$:
$q^2<7p^6$ leaves $q$ up to $p^3$).  Size bookkeeping is exhausted
there; what remains needs the residual equation itself — build B.

## 2.19 Build B: the residual finisher — rigid forms, and the content-3 gap in H2

*(2026-09-02; entry 88; `compute/residual_kill.py`; check
`a3.residual_finisher`.)*

**Mechanism** (the H2 tree of §2.9, made mechanical).  When a collapse
equation of an OPEN pattern involves one frame only through the legs
of a single index, $A\,X_k+B\,Y_k=0$ with $A,B$ in the other frame's
Lucas values, coprimality of the legs forces the **rigid form**
$(X_k,Y_k)=\pm(B,-A)/g$, $g=\gcd(A,B)$, i.e. the coincidence
$$\text{frame}^k=\pm\frac{B-iA}{g},$$
a pinned system of the §2.14 type with a multi-term Gaussian
polynomial.  It is killed by parity (the Im-leg is $\equiv0\bmod4$, so
an odd $A$ is dead at once), by the content lemma bounding $g$, and by
the concentration and sliver certifiers over every sign, conjugation
and content branch.  No lever is needed: the linear relation carries
it.  The mirror (linear in the $\ell$-legs, coefficients in the
$w$-frame) is the same code with the roles swapped.

**Result.**  $96$ of the $168$ single-lever ladder survivors die
($8$, $12$, $28$, $24$, $24$ in the boxes $(3,2)$, $(4,1)$, $(5,1)$,
$(4,2)$, $(3,3)$), and in the $(3,1)$ audit $8$ of the $12$
hand-closed patterns become machine theorems: the four H2 same-sign
combos (four $d=1$ branches each, content bound $3$) and all four
M2-opp rows.  The ladder stands at

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 302/322 | 126/140 | 192/220 | 518/576 | 652/732 |

$1936/2136$ ($90.6\%$).  **Every remaining single lever ($72$) is one
residual**: the H2 opposite-sign form $A=p^2S_4=2p^2C_2S_2$, $B=X$ a
fixed sextic in $(C_1,S_1)$, at level $k=2$ or its replications.  The
machine kills all four content-$1$ branches (the certificate:
$\rho^4+\bar\ell^{6}=-2C_1\ell^5$, so $\ell^5$ sits in one factor of
$(\rho^2+i\bar\ell^3)(\rho^2-i\bar\ell^3)$ and the other has modulus
$<2p$ but $\ge p^5-2p^3$) and none of the content-$3$ branches.

**The content-3 gap.**  $3\mid A$ always ($3\mid C_1S_1$ or
$C_1^2\equiv S_1^2$), and $3\mid X\iff3\mid S_1$; so **half of all
frames have content $3$**, and then $(U_2,V_2)=\pm(X,-A)/3$.  Entry 66
wrote $q^4=X^2+(2SCp^2)^2$ — content $1$ — and never treated this
case; its "$p\le16$" step could not be reconstructed either, but the
machine's concentration kill replaces it for content $1$.  For content
$3$: $3\rho^4+\bar\ell^6=-2C_1\ell^5$ does not factor over
$\mathbb Z[i]$; over $\mathbb Z[\zeta_{12}]$ it does, and the norm
argument kills it whenever $\pi$ is inert there ($p\not\equiv1\bmod
12$) — but $3\mid S_1$ forces $p\equiv1\pmod{12}$, exactly the split
case where the two conjugate factors can each absorb one prime above
$\pi$.  Reduction mod $3$ forces $9\mid S_1$; mod $9$, $27$ and the
$2$-adic residues are all consistent.  **So Theorem A3.9 rests on one
open lemma:** for $p\equiv1\pmod{12}$ with $9\mid S_1$, the four H2
X6-route patterns have no solution with $\gcd(A,X)=3$.  The residual
system is empty for every split $p<20000$ in both contents (a fact,
not a proof).  The same lemma, at level $k$, is what the $72$ ladder
singles need.

## 2.20 The deep descent: the content-3 lemma is a theorem — Theorem A3.9 by machine

*(2026-09-02; entry 89; `compute/window_kill.py` (deep targets),
`compute/residual_kill.py` (the rigid-form size kill); checks
`a3.box31_machine`, `a3.residual_finisher` (iii), `a3.window_finisher`.)*

**The lemma.**  Fix the surviving branch $3\rho^4=\ell^6+\bar\ell^6+
\ell^5\bar\ell$ (mod $4$ kills the other sign).  The rigid form says
$V_2=\mathrm{Im}(w^2)=\mp A/3$ with $A=p^2S_4$, so $p^2\mid
\mathrm{Im}(\rho^4)$.  Now descend one level further than the frame:
$\rho=u+iv$ is the Gaussian prime itself, $u^2+v^2=q$, $\gcd(u,v)=1$,
opposite parity, and
$$\mathrm{Im}(\rho^4)=4uv(u-v)(u+v),$$
four **pairwise coprime** factors each of modulus $<\sqrt{2q}$.  So
$p^2$ divides one of them and $q\ge p^4/2$.  On the other side
$3q^2=|\ell^6+\bar\ell^6+\ell^5\bar\ell|\le3p^6$ gives $q\le p^3$.
Hence $p^4/2\le p^3$, $p\le2$: **no solution for any $p$, either
content** ($g=1$ gives $q\le\sqrt3\,p^3$, $p\le2\sqrt3$).  This is
exactly the descent of entry 66 — "$p^4$ in a leg of $q^2$, then
$p^2\mid(g\mp h)$ or $p^2\mid gh$" *is* $p^2\mid u\pm v$ or $p^2\mid
uv$ — which was content-independent all along; its crude bound
$64p^6$ left "$p\le16$" and a finite residue check, and only that
check was content-$1$-specific.  With the sharp bound nothing finite
remains.  Numerically the content-$3$ frames are half of all frames
and none solves the system to $p<20000$; the lemma now explains why.

**Made uniform.**  Two mechanical pieces.  *(i) Deep targets:* the
index-$1$ legs of a frame $X=\pi^2$ recurse to the legs of $\pi=a+bi$
itself — $C_1=(a-b)(a+b)$ with coprime odd factors $<\sqrt{2P}$,
$S_1=2ab$ with coprime factors $<\sqrt P$ — so every lever inequality
of the window finisher gains a square root: $p^{2e}\mid\mathrm{Trig}(w^n)$
now bounds $q$ below by $p^{4e}/2$ at the deepest level instead of
$p^{2e}$.  *(ii) The rigid-form size kill:* from $\text{frame}^k=\pm
(B-iA)/g$, $q^k=|B-iA|/g\le M(p)/g$ with $M$ the coefficient bound,
while the Im-leg carries the $(\ell\bar\ell)$-content $p^{2m}$ of $A$
and hence divides one deep coprime factor of $\mathrm{Im}(\rho^{2k})$;
each target's inequality $p^{2m}<c\,q^{h}$ combined with the size
bound is a polynomial inequality in $p$, false on $[5,\infty)$ by an
exact Sturm count.  Every remaining single lever of the ladder is this
residual at level $k=2$ or $4$.

**Theorem A3.9 by machine.**  The $(3,1)$ box under the complete stack:
$78/78$ distinct OPEN patterns dead — $16$ residual parity, $8$
valuation, $16$ concentration, $6$ unit collapse, $12$ window, $4$
rigid form + concentration (H2 same-sign), $4$ rigid form + size (H2
X6-route, the lemma), $12$ doubled (Lemma G4).  The twelve rows that
rested on hand trees (H2 $\times8$, M2-opp $\times4$) are certified by
`a3.box31_machine` on every run.  With §2.16–2.17, **Theorems A3.7,
A3.8, A3.9 and A3.10 all rest on machine certificates alone.**

**On the ladder.**  The size kill takes $40$ more singles and the deep
targets $18$ of the $128$ doubles ($[1,7]\times10$, $[2,8]\times6$,
$[2,10]\times2$):

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 310/322 | 134/140 | 202/220 | 534/576 | 668/732 |

$1994/2136$ ($93.4\%$); $142$ open: $110$ doubles and $32$ singles.
The $32$ singles are two families the size kill misses by structure,
not by strength: the $k=3$ replications of H2 in the $(3,3)$ box
($8$), where the lever can land on the index-$3$ Im-cofactor
$4U_1^2-q^2$, which the targets bound by $3q^2$ but which factors as
$(2U_1-q)(2U_1+q)$ with coprime odd factors $<3q$ — the missing deep
target — and then needs the pin $2U_1\pm q=\pm tp^2$, $t\in\{\pm1,\pm3\}$,
substituted; and the $(J,1)$-type families $\{(J{-}1,\pm k),(J,k),(J,-k)\}$
with $J\ge4$ ($24$), where the rigid-form bound $q\le\kappa p^{J}$ and
the deep lever $q\ge p^4/2$ meet at $J=4$ with a constant to spare, so
the window pins a leg of $\rho$ to $\pm p^2$ exactly and the residual
must be chased after that pin.  Both are the next build (v2), together
with the doubles' non-homogeneous cofactor pairs.

**Ledger after entry 79: the rigidity lemma is a theorem for $39$ of the
$67$ transparent primes below $30000$** ($32$ of certified rank $1$, $4$
rank-2 primes by the criterion, $3$ by $L'$ where the 2-descent was
blind).  Remaining $28$: $22$ rank-2 curves whose second generator lies
beyond effort-20 search (the targeted `ell2cover` + `hyperellratpoints`
route, or a 4-descent, is the way in); $3$ where the criterion provably
fails ($2657,9137,29201$); $3$ of undetermined rank with
$n\ge1.3\cdot10^8$ (conductor $\ge5\cdot10^{17}$).

Once this lemma falls, A3.10 closes (Block A directly; Block B by its
analogue) and the corollary sharpens to: *the split part of any MSS3
center is $p^3q^2$-or-higher, $p^4q$-or-higher, or has $\ge3$ distinct
split primes* — leaving $\omega=2$ with only the $a,b\ge2$,
$\max(a,b)\ge3$ boxes, which the uniform lemma is built to sweep.

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
