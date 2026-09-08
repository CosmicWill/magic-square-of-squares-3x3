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
A3.C would be a genuinely new impossibility theorem — note the direction
of the implication: no additive triple implies no additive quadruple,
hence no magic square, so A3.C is *stronger* than the full problem, not
weaker (corrected in entry 117; the two-frame theorems A3.7–A3.10 are
cases of A3.C, and through the free-frame reduction of 2.46 they already
feed the three-frame boxes). (It does
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

## 2.21 Build B v2a: the polynomial gcd, the split index-3 cofactor, bounded primes

*(2026-09-02; entry 90.)*

Three mechanical pieces, each answering an exact failure mode.  **The
polynomial gcd.**  For the $(J,1)$-type families the coefficients
$A,B$ of the linear form share the factor $C_1^2-3S_1^2$ (the cofactor
of $C_3$); a common polynomial factor that never vanishes on a frame
is a factor of the relation, not content, so the rigid form is built
from $A/F$, $B/F$ — after checking that no irreducible factor of $F$
vanishes on a frame (a zero needs $C_1/S_1=m/n$ rational with $m$ odd,
$n$ even and $m^2+n^2$ a prime square; the rational roots are
enumerated).  For $J=4$ the Gaussian form drops from degree $8$ to $6$
and the size kill applies.  **The split index-3 cofactor.**
$4X_1^2-P^2=(2X_1-P)(2X_1+P)$, coprime odd factors of modulus $<3P$,
replaces the coarse target bounded by $3P^2$.  **Bounded primes.**
When the levers' inequalities leave $p^{e}<K$ with $K>5^{e}$, $p$ (or
$q$) ranges over the explicit split primes below $K^{1/e}$; each has an
explicit frame, the other lever divides an explicit integer value of
it, and the relation is evaluated exactly on the finitely many frame
pairs (this is how the G3 index-$3$ rows now die, at $p<10$).

**Result.**  $20$ of the $32$ singles and $22$ more doubles:

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 310/322 | 138/140 | 210/220 | 542/576 | 668/732 |

$2036/2136$ ($95.3\%$); $100$ open: $88$ doubles and $12$ singles.
The $12$ are precisely: the $k=3$ replications of H2 in $(3,3)$ ($8$),
where $w^6=\pm Z/g$ gives $q\le1.2p$ and the only surviving target is
the index-$3$ Re-cofactor $4U_1^2-3q^2$, whose window pins
$4U_1^2-3q^2=\pm tp^2$, $t\in\{\pm1,\pm3\}$ — a finite tree of conics
$(2U_1)^2-3q^2=tp^2$ (most branches dead by parity, size, or the norm
form of $\mathbb Q(\sqrt3)$; one lands on the genus-$1$ quartic
$V_1^2=b^4-3a^2b^2+9a^4$ with $q=b^2+3a^2$, $p=b^2-3a^2$, which needs a
rank computation); and the $J=5$ family $\{(4,\pm1),(5,1),(5,-1)\}$
($4$), where after the gcd the form has degree $8$, $q\le1.73p^4$
against $q\ge p^4/2$, and the window $|t|<1.3\sqrt p$ is no longer a
constant — no pin, so the residual needs the rigid form's exact
structure.  Build B v2b: conic splitting after pins, elliptic
endpoints by rank, and the doubles' pair residuals.

## 2.22 The pin stage — the k = 3 family closed; the (J,1) content-3 residual is the frontier

*(2026-09-02; entry 91.)*

The conic tree of §2.21 collapses to two lines once the content-$3$
size bound is used sharply.  For the $k=3$ replications, $w^6=\pm Z/3$
with $|Z|<3p^6$ gives $q<p$; every deep target of $\mathrm{Im}(\rho^{12})$
then dies by size except the index-$3$ Re-cofactor $4U_1^2-3q^2$,
whose window $|t|<3q^2/p^2<3$ leaves $t=\pm1$: $t=+1$ needs
$p^2=4U_1^2-3q^2<q^2<p^2$, and $t=-1$ makes $4U_1^2\equiv-1\equiv2
\pmod3$.  Mechanized as a **pin stage** inside the size kill: a target
that survives the size window is pinned to $T=tp^{e}$, the admissible
$t$ are enumerated from the window with $q<q_{\max}=(M/d)^{1/k}$, and
each $t$ is tested by the target's shape (range against $q_{\max}$,
the mod-$3$ obstruction of the Re-cofactor).  The size kill works per
content: each $d\mid N$ dies by size/pin or by the concentration and
sliver branches.  All $8$ die.

| box | (2,1) | (2,2) | (3,2) | (4,1) | (5,1) | (4,2) | (3,3) |
|---|---|---|---|---|---|---|---|
| dead / total | 26/26 | 120/120 | 310/322 | 138/140 | 210/220 | 542/576 | 676/732 |

$2044/2136$ ($95.7\%$); $92$ open: $88$ doubles and $4$ singles.

**The frontier residual.**  The four singles are the $J=5$ family
$\{(4,\pm1),(5,1),(5,-1)\}$: rigid form $w^2=\pm(B-iA)/g$ with
$A=p^2S_8$, $Z=-(\ell^{10}+\ell^9\bar\ell+\bar\ell^{10})$, no
polynomial gcd, content bound $3$.  Content $1$ dies by concentration.
Content $3$ is the degree-$10$ cousin of the content-$3$ lemma,
$$3\rho^4=\bar\ell^{10}+2C_1\ell^9,\qquad 9\mid S_1,\ p\equiv1\pmod{12},$$
and here the deep descent's $q\ge p^4/2$ meets only $q<p^5$: a gap of a
factor $p$, so no pin and no size kill — the same for every
$(J,1)$-type family with $J\ge5$.  The residual is empty for all $181$
frames with $9\mid S_1$ below $20000$.  Whatever kills it must use more
than size: the congruence $3\rho^4\equiv\bar\ell^{2J}\pmod{\pi^{4J-2}}$
pins $\rho^4$ to one residue class whose lift is the equation itself,
and over $\mathbb Z[\zeta_{12}]$ the factors $\sqrt3\rho^2\mp\bar\ell^J$
each absorb one prime above $\pi$ (blind descent).  This single
residual and the $88$ doubles are the frontier of the uniform
$\omega\le2$ program.

## 2.23 The frontier residual: reconnaissance, and Conjecture R_J

*(2026-09-02; entry 92; check `a3.frontier_residual`.)*

For the $(J,1)$-type family with $J\ge5$ the content-$3$ branch is
$$3\rho^4=\bar\ell^{2J}+2C_1\ell^{2J-1},\qquad 9\mid S_1,\ p\equiv1\pmod{12},$$
with the real equations $3U_2=C_{2J}+2C_1C_{2J-1}$, $3V_2=p^2S_{2J-2}$
and the norm identity $9q^4-p^{4J}=8C_1C_{2J-1}C_{2J}$.  Everything in
the toolkit was tried on it.  *Size:* the deep descent's $q\ge p^4/2$
against $q<p^J$ leaves a gap $p^{J-4}$; no constant window.  *Local
methods cannot work:* the bare equation has the solution $\pi=\rho=1$
for every $J$ ($Z(1)=3$), so only the frame conditions exclude
solutions and no congruence can.  *$\mathbb Z[\zeta_{12}]$:* the case
with both primes above $\pi$ in one factor dies by norms; the split
case gives constraints only — $3$ a quartic residue mod $p$, and every
prime $r\equiv5\pmod{12}$ of $C_1$ to an even power (the ideal
$\mathfrak b$ with $\mathfrak b\,\sigma(\mathfrak b)=(2C_1)$ is
$\sigma$-stable at primes inert in $K/\mathbb Q(i)$) — keeping $15\%$
of the frames.  *Small representatives:* $\rho^2$ is the unique element
of modulus $<p^{2J-1}/2$ in the class of $-\bar\ell^J s^{-1}$ modulo
$\pi^{4J-2}$ ($s^2\equiv3$), and the equation asks that lift to satisfy
the identity exactly — tautologically consistent.  *Geometry:* with
$y=\ell/\bar\ell$, $X=\rho/\bar\pi^J$ it is a $\mathbb Q(i)$-point of
$3X^4=y^{2J}+y^{2J-1}+1$, genus $13$ at $J=5$: finitely many by
Faltings, non-effective, and not uniform in $J$.

**Evidence.**  Empty for all $6503$ frames with $9\mid S_1$ below
$10^6$ ($J=5$), for all $1480$ frames below $200000$ at $J=7$ and
$J=9$, and, with no primality at all, for every primitive $\pi$ of norm
$\le20000$ ($J=5$).

**Conjecture R_J.**  For every $J\ge5$, $3\rho^4=\bar\ell^{2J}+
2C_1\ell^{2J-1}$ has no solution with $\pi,\rho$ Gaussian primes of odd
norm.  It is the only single-lever residual left in the ladder and its
shape is the same for every $J$; the box theorems for $(J,1)$, $J\ge5$,
are conditional on it (verified to $p<10^6$).  A proof needs a global
method that the present toolkit does not have.

## 2.24 Two attacks on the frontier: the quadruple pivot, and the cyclotomic splitting of R_J

*(2026-09-02; entry 93; checks `a3.quadruple_pivot`, `a3.cyclotomic_split`.)*

**The quadruple pivot.**  MSS3 requires not a triple but an additive
*quadruple* in some $D(m)$: $x,y,x+y,x-y$, which is two additive
triples sharing two elements with opposite relative sign, both holding
for the same center — so **two relations, two levers per prime**.
Among the $92$ open triples there are $56$ candidate quadruples ($0$ in
$(3,2)$, $8$ in $(5,1)$, $16$ in $(4,2)$, $32$ in $(3,3)$), and **every
one dies by the pooled two-lever pincer**: a $p$-lever from one triple
and a $q$-lever from the other bound the same prime both ways (in
$(5,1)$, $p^2\mid\mathrm{Im}(w)$ gives $q>p^4/2$ while $q^2\mid
\mathrm{Re}(\ell^9)$ gives $q^4<2p$, so $p^{15}<$ const).  This is
exactly what the pivot was reserved for: the second relation is the
missing lever.  A direct search finds no quadruple in any $D(m)$ with
$|D(m)|\ge3$, $m<4000$.  Status: reconnaissance — the mechanism closes
every enumerated candidate; a rigorous quadruple theorem needs the
joint-valuation engine and the completeness of the label enumeration.

**The cyclotomic splitting.**  $Z_J$ has the factor $F=\ell^2+\ell
\bar\ell+\bar\ell^2=3C_1^2-S_1^2$ exactly when $3\mid J-1$.  With
$G=Z_J/F$ polynomial-coprime and $\mathrm{Res}_\ell(F,G)=R_J\bar\ell^{
4(J-1)}$ ($R_J=19,61,127$ for $J=4,7,10$), a solution $3\rho^4=Z_J$
factors as $(3)(\rho)^4=(F)(G)$ with $(\rho)$ landing entirely in one
factor.  *Main branch (unconditional):* $(\rho)^4\mid(G)$ forces
$F\mid3$, impossible since $|3C_1^2-S_1^2|\equiv3\pmod8$ is never $\pm1$
or $\pm3$ (those conics have no prime-hypotenuse frame), so $|F|\ge5$.
*Second branch (thin):* $(\rho)^4\mid(F)$ forces $|G|\le3$, a
Diophantine-approximation residual (degree $\ge6$), empty on frames in
range.  So **Conjecture R_J is open only for $J\not\equiv1\pmod3$** —
the splitting removes a third of the cases and subsumes entry 90's
$J=4$ gcd.

> **Erratum (entry 96, §2.27).**  The equation $3\rho^4=Z_J$ analysed
> above is *not* the machine's residual for $J\equiv1\pmod3$: the
> polynomial-gcd stage (entry 90) cancels $F$, and the residual finisher
> then reports content bound $1$ with every branch open, so the frontier
> there is $\rho^4=\pm G_J$ ($G_J$ irreducible over $\mathbb Q(i)$).  The
> literal equation is unsolvable outright by a norm argument — which is
> exactly why $F$ is cancelled.  **The reduction of R_J is withdrawn.**

**Where R_J sits.**  It follows from ABC over $\mathbb Q(i)$ with
quality $4J/(J+4)$ ($2.22$ at $J=5$, above the record $1.63$); local
methods cannot prove it ($\pi=\rho=1$ solves the bare equation); it is
a $\mathbb Q(i)$-point of the superelliptic $3X^4=y^{2J}+y^{2J-1}+1$
(genus $J-1$); and $A3.C$ in full is a case of the $n$-conjecture
($n=6$) over $\mathbb Q(i)$.  A proof is a global statement.

## 2.25 The rigorous quadruple engine: MSS3 attacked directly

*(2026-09-03; entry 94; `compute/quadruple.py`, check `a3.quadruple_engine`.)*

MSS3 $\iff$ a quadruple $u,v,u+v,u-v$ in one $D(m)$, which is two
additive triples $T_1=\{u,v,u+v\}$, $T_2=\{u,v,u-v\}$ on the shared
pair $\{u,v\}$ (with $u$'s sign opposite), both holding for the same
frame.  The quadruple carries **every lever of $T_1$ and of $T_2$**;
the sound kill demands a pincer for *every* selection of one target per
lever (the true frame realizes one per lever, unknown to us).
survey_box's complete open-triple enumeration makes it complete: every
live quadruple (both triples open) is an enumerated pair.

**Correcting the reconnaissance (2.24).**  The best-target count "all
$56$ die" was optimistic.  Under the sound rule, over the $92$ open
triples: **$16$ pairs die, $40$ survive.**

* **Die ($16$, the balanced shapes).**  Each triple gives both a
  $p$-lever and a $q$-lever, so the bounds oppose: a $(4,2)$-shape pair
  has $T_1:p^2<c\,q^2$ and $T_2:q^2<c\,p^4$, min pincer exponent $2$
  ($p^2<$ const, dead for $p\ge5$).  Those quadruples are impossible.
* **Survive ($40$: $8$ of $(5,1)$-shape, $32$ of $(3,3)$-shape).**  Here
  $T_1$ gives only $p$-levers, so both levers read the same direction
  $q\sim p^J$ — a compatible size *window*, not a pincer.  The $(5,1)$
  survivors are exactly the frontier residual $R_5$ (the shallow
  cofactor $q^2<9p^8$ of $\mathrm{Re}(\ell^9)$ against $q>p^4/2$); the
  $(3,3)$ survivors are a diagonal window $p\sim q$.

**Reading.**  The second relation is a real second lever, but it
pincers only when the two triples bound *opposite* prime-ratio
directions — which balanced boxes provide and $(J,1)$-type boxes
($b=1$, only $p$-levers) do not.  So the pivot rigorously kills MSS3 in
the balanced shapes and reduces the rest to the residuals already
isolated ($R_J$ and the diagonal window); it narrows MSS3, it does not
solve it.  The next build is the **joint residual solver**: where the
pincer leaves a window, $T_1$ and $T_2$ give two equations in the same
$\rho$, an overdetermined system size alone cannot see.

## 2.26 The joint residual solver: no MSS3 for a family of split-part shapes

*(2026-09-03; entry 95; `compute/quadruple.py` `joint_residual_kill`,
check `a3.quadruple_joint`, data `compute/data_quadruple_pairs.json`.)*

Where the two-lever pincer (2.25) left a compatible window, the two
triples of a quadruple give two cleared relations $R_1=R_2=0$ on one
frame ($c_1,s_1=\mathrm{Re},\mathrm{Im}\,\ell$; $c_2,s_2=\mathrm{Re},
\mathrm{Im}\,w$).  Eliminating the $w$-frame, $\mathrm{Res}_{s_2}(R_1,
R_2)=0$ is necessary for a common $s_2$.  It factors; every non-monomial
factor is **pure in $(c_1,s_1)$** (the $w$-frame decouples — no
$c_2$-mixing factor arises) and homogeneous, so it vanishes on a frame
only if $c_1/s_1$ is a rational root that is a **frame ratio**
($|r|=m/n$ with $m^2+n^2$ a perfect square — either sign, entry 96).  None of the joint forms has
such a root, so $\mathrm{Res}$ has no frame zero, no common $s_2$, no
quadruple.

**The complete result.**  The $92$ open triples give $14$ distinct
quadruple orbits (entry 95 listed each four times as $56$; corrected in
entry 96, §2.27); **all $14$ die** — $4$ by the pincer, $10$ by the joint
solver (degree-$26$ form for $(5,1)$; degrees $6,56,64$ for $(3,3)$),
zero survivors.  The boxes $(1,1),(2,1),(2,2),(3,1),(4,1)$ have no open
triple.

**Theorem (quadruple / MSS3).**  No 3×3 magic square of distinct
squares has center norm $m$ whose split part is $p^aq^b$ for
$(a,b)\in\{(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(5,1),(3,3)\}$
($p,q$ distinct primes $\equiv1\bmod4$, and transposes).  *Proof.*
MSS3 $\iff$ a quadruple in $D(m)$; a quadruple is two additive triples
sharing a pair, both patterns in box $(a,b)$; each is machine-dead or
one of the $92$ open triples; all $14$ open orbits die; the other boxes
have no open triple. $\blacksquare$

**Significance.**  This is the first family of shapes where MSS3 is
killed *directly*, and it includes $(3,2),(4,2),(5,1),(3,3)$ where the
no-triple conjecture A3.C is still open ($R_J$).  MSS3 is strictly
easier than A3.C: the quadruple's two relations overdetermine the
frame, and eliminating the shared prime leaves a single binary form
whose only candidate roots are finitely many rationals, none a frame
ratio.  The corollary's minimal $\omega=2$ shapes $p^2q^2$ and $p^4q$
are eliminated.  *Scope:* a finite family, not all $\omega=2$ and not a
general MSS3 theorem; the next step is $(5,2),(6,1),(4,3),(4,4),\dots$

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

## 2.27 The audit of entries 93–95: the theorem stands; the cyclotomic reduction is withdrawn

*(2026-09-03; entry 96; check `a3.audit_entry96`; data `compute/data_quadruple_pairs.json`.)*

Entries 93–95 were re-verified by recomputation outside their own code
paths: the $92$ open triples rebuilt from the entry-90 survivors ($100$
patterns through `kill_pattern`: $92$ open, $8$ dead — $12$ in $(3,2)$,
$8$ in $(5,1)$, $28$ in $(4,2)$, $44$ in $(3,3)$); the pairs re-enumerated
independently and compared orbit by orbit; every pair re-killed; the
cyclotomic algebra re-derived; the $(J,1)$ rigid form re-derived by
machine for each $J$.

**Frame ratios have either sign.**  The frame $\ell=\pi^2$ may be any of
$\pm\pi^2,\pm\bar\pi^2$, so $c_1/s_1=\pm(a^2-b^2)/(2ab)$; $3-4i=
\overline{(2+i)^2}$ is a frame with ratio $-3/4$.  The entry-95 test
rejected negative ratios — a gap in the code, closed.  Re-killing every
joint form with $|r|$ tested: each linear factor has root $\pm1$ only
($1+1=2$ is not a square); the other factors are irreducible of degree
$\ge2$ (no rational root at all); every pure factor is homogeneous, $R_1,
R_2$ are bihomogeneous, and no $c_2$-mixing factor arises.  Every kill
stands.

**Orbits, not listings.**  Labels live in the survey normal form ($j\ge0$;
$k>0$ when $j=0$); a label and its negative are the same element with
$\operatorname{Im}$ negated, so flipping a label flips its coefficient.
The entry-95 enumeration compared raw labels after the conjugation
images: under $\ell\to\bar\ell$ no $j>0$ label can match, and under
$w\to\bar w$ a shared $(0,k)$ becomes $(0,-k)$ — blind to a shared $j=0$
element (a synthetic example is pinned) and listing each orbit four
times.  The $92$ open triples carry no $j=0$ label, so the kill list was
complete; in normal form they give **14 distinct quadruple orbits** —
$2$ in $(5,1)$, $4$ in $(4,2)$, $8$ in $(3,3)$ — all dead: $4$ pincer
$+$ $10$ joint.  `quadruple_pairs` now normalizes, takes $T_2$ over each
triple and its partial conjugate (the only two images — the
$\ell$-conjugate image equals the $w$-conjugate image after
normalization), and returns one representative per orbit.

**Theorem (unchanged in substance).**  No 3×3 magic square of distinct
squares has center split part $p^aq^b$ with $(a,b)\in\{(1,1),(2,1),(2,2),
(3,1),(3,2),(4,1),(4,2),(5,1),(3,3)\}$ or a transpose.

**The cyclotomic splitting (§2.24) analysed the wrong equation.**  For
$J\equiv1\pmod3$ the machine's rigid form of the $(J,1)$ single is
$Z_J/(-F)$: the polynomial-gcd stage cancels $F=3C_1^2-S_1^2$, which
never vanishes on a frame, and the residual finisher then reports
content bound $1$ with all four branches open ($G_J$ irreducible over
$\mathbb Q(i)$; degree $12$ at $J=7$, $18$ at $J=10$).  The frontier at
$J\equiv1\pmod3$ is therefore $\rho^4=\pm G_J$, untouched by §2.24.  The
literal equation $3\rho^4=Z_J$ is unsolvable outright: $F\in\mathbb Z$
with $|F|\ge5$; if $\rho\nmid F$ then $F\mid3$; if $\rho^a\,\|\,F$ with
$a\ge1$ then $q^a\mid F$ (as $F$ is real) and $N(G)\ge q^{4-a}$, so
$3q^2=|F||G|\ge q^{(a+4)/2}$ forces $q\le9$, i.e. $q=5$ and $5\mid\gcd(F,
G)\mid R_J$ — and $5\nmid R_J$ ($G(\omega)\equiv0\pmod5$ would need
$\omega\in\mathbb F_5$).  That is precisely why the machine divides $F$
out.  **The reduction of R_J to $J\not\equiv1\pmod3$ is withdrawn.**
Conjecture R_J is to be read as: the machine's $(J,1)$ residual has no
frame solution — $3\rho^4=\pm Z_J$ for $J\not\equiv1$, $\rho^4=\pm G_J$
for $J\equiv1\pmod3$.  The shape "$3\rho^4=Z_J$ for all $J\ge5$" was
generalized by hand from $J=5$ in §2.23 (entry 92); the audit flags it
there as well.

**Lessons.**  Re-derive a hand-generalized shape by machine for every
parameter value — the gcd stage may have cancelled the factor being
exploited; audit every test on a frame ratio against all four
orientations; count orbits, not listings.

## 2.28 The ω = 3 front: the (1,1,1) box's quadruples are curves

*(2026-09-03; entry 97; check `a3.omega3_engine`; code `compute/omega3.py`,
`compute/pari_genus1.py`; data `compute/data_omega3_box111.json`.)*

**The setting.**  Split part $pqr$, frames $\ell=\pi^2$, $w=\rho^2$,
$v=\sigma^2$.  An element of $D(m)$ has a label $(j,k,l)\in\{-1,0,1\}^3
\setminus 0$ (mod sign) and equals the $(2,2,2)$-form
$(c_1^2+s_1^2)^{1-|j|}(c_2^2+s_2^2)^{1-|k|}(c_3^2+s_3^2)^{1-|l|}
\operatorname{Im}(\ell^{2j}w^{2k}v^{2l})$ (negative exponents are
conjugates).  A quadruple $d_A+d_B=d_C$, $d_A-d_B=d_D$ gives two
relations $R_1=R_2=0$ on one frame.  Eliminating a frame $f$,
$\operatorname{Res}_{s_f}(R_1,R_2)=c_f^{\,k}\,\Phi_f$ with
$\Phi_f(t_g,t_h)=0$ a **plane curve in the two other frame ratios**
$t=s/c$, depending only on the pattern, not on the primes.  At $\omega=2$
the same elimination gave a binary form (§2.26); at $\omega=3$ the whole
box becomes rational points on finitely many fixed curves — the shape of
the long-term goal (ROADMAP R.7).  Modulo the frame group $S_3\times
(\mathbb Z/2)^3$, the global sign and the $A\leftrightarrow B$ swap there
are $2944$ candidate classes; every two-frame class dies at once.

**Sound kills (uniform in $p,q,r$).**  $\operatorname{Res}=0$ is
necessary, so an irreducible factor vanishes at the frame.  Monomials
never; a univariate factor only at a rational root that is a frame ratio
($|t|=n/m$, $m^2+n^2$ a square); $t_g=\pm t_h$ and $t_gt_h=\pm1$ force the
same prime.  A component quadratic in one variable needs a rational
point on $y^2=\operatorname{disc}(t)$ (squarefree model, or a root of the
square part); when that curve has genus $1$ with **PARI rank $0$** and a
complete enumeration (a quartic with rank-$0$ Jacobian is empty or a
torsor under $E_{\mathrm{tors}}$, so it has exactly $|E_{\mathrm{tors}}|$
points), every rational $t$ is known, and if none is a non-degenerate
frame ratio ($t\notin\{0,\pm1,\infty\}$) the component is dead.  Genus
$\ge2$ is Faltings-finite.  The **Pythagorean pullback**
$t=2\tau/(1-\tau^2)$, $\tau=b/a$, gives the curve of Pythagorean frame
pairs $\Psi(\tau_g,\tau_h)=0$, decided the same way; a genus-$0$ factor
is an infinite Pythagorean family.

**Result.**  Of the $2944$ classes: **$821$ dead** uniformly in the primes
($349$ by trivial factors, $472$ by rank-$0$ curves); $540$ *finite*
(hyperelliptic models of genus $2,3,5$); $316$ *infinite* (a genus-$0$
factor of the pullback); $1267$ *unknown* (bidegree $>6$, not pulled back).
The $472$ curve kills use only **thirteen** genus-$1$ models, all even
quartics $y^2=at^4+bt^2+c$ of conductor $32,48,56,80$ — $t^4+18t^2+1$,
$t^4+34t^2+1$, $9t^4-14t^2+9$, $t^4-3t^2+1$, $t^4+t^2+1$, … — with rank
$0$ and rational points exactly $t\in\{0,\pm1,\infty\}$: the Fermat–Euler
family ($x^4-y^4=z^2$ and its twists).  Example: the class $\{$$v$-pure,
$w$-pure, $\ell$-pure, $\operatorname{Im}(\ell^2\bar w^2)\}$ forces
$\tan\alpha\tan\beta=-3$ between two frame angles; with both Pythagorean
this is $y^2=9u^4-14u^2+9$, rank $0$, torsion $8$, points
$u\in\{0,\pm1,\infty\}$ — no frames.  Every model is even ($t\to-t$ is
the conjugate frame); the finite models are also reciprocal ($t\to1/t$,
the associate frame), so they carry quotient towers down to elliptic
curves — the classical route, not yet executed.

**What this is and is not.**  Not a theorem for the box.  It is the
first uniform-in-the-primes statement at $\omega=3$ ($821$ shapes cannot
occur for any three split primes), obtained by exactly the long-term
goal's mechanism, and an explicit map of the rest: $540$ shapes on
Faltings-finite curves (towers, then Chabauty where towers stop); $316$
shapes with a rational family of Pythagorean pairs on the projection,
where descent on the projected curve cannot finish and the third
frame's Pythagorean condition plus the primality of the norms must
enter; $1267$ high-bidegree shapes not yet analysed.  Next: the
third-frame lift of the $316$ families, the pullback of the high-degree
components, the quotient towers of the $540$, then the $(2,1,1)$ box.

## 2.29 The third-frame lift: the monomial lemma kills every rational family

*(2026-09-03; entry 98; check `a3.omega3_engine`; code `compute/omega3.py`.)*

**The families.**  Each of the $316$ "infinite" classes of §2.28 had, in
its best frame, a genus-$0$ factor of the Pythagorean pullback: a
rational curve of Pythagorean frame pairs $(\tau_g,\tau_h)$ on the
projected relation.  Parametrizing every such factor (linear in one
variable; quadratic with a discriminant that is a square times a
constant; or a conic through a small rational point, with the points a
parametrization can miss — square-part roots, roots of the leading
coefficient, a base point with $y_0=0$ — kept as candidates) and writing
$w=(1+i\tau)/(1-i\tau)=\pi/\bar\pi$ for each prime's own circle point,
**every family satisfies a monomial relation identically**:
$w_g^{\,a}=\varepsilon\,w_h^{\,b}$ with $\varepsilon$ a unit, the
relations found being $(a,b)=(1,2),(1,-2),(2,1),(2,-1),(1,3),(2,3)$ in
best frames (also $(3,2),(3,1)$ elsewhere).  They are angle-multiple
coincidences: the $(1,2)$ family is $\tau_g=t_h$, the half-angle of one
prime equal to the full angle of the other (the first example
$t_gt_h^2-t_g+2t_h=0$ is the double-angle formula itself); $(1,3)$ is
tripling; negative $b$ are conjugate versions.

**The monomial lemma.**  For frames of distinct split primes $p\ne q$, a
relation $w_g^{\,a}=\varepsilon w_h^{\,b}$ ($a\ge1$, $b\ne0$,
$\varepsilon$ a unit) is impossible: clearing denominators,
$\pi_g^{\,a}\bar\pi_h^{\,b}=\varepsilon\bar\pi_g^{\,a}\pi_h^{\,b}$ (for
$b>0$), so the Gaussian prime $\pi_g$ divides $\bar\pi_g^{\,a}\pi_h^{\,b}$,
hence $\pi_g\sim\bar\pi_g$ ($p=2$) or $\pi_g\sim\pi_h$ ($p=q$); for $b<0$
exchange $\pi_h,\bar\pi_h$.  This generalizes the same-prime lemma
($a=b=1$).  A family on which such a relation holds identically
contains no frame pair of distinct primes at all, for any primes: the
kill is uniform.  The remaining genus-$0$ shapes (the $(2,2)$ factors and
the pullbacks of bilinear components) have discriminant $=$ (non-square
constant)$\times$(square), so no rational points off the square part,
whose roots are degenerate.  **The lift to the third frame was never
needed.**

**Result.**  Over the $2944$ classes: **dead $1077$** (349 trivial; the
thirteen rank-$0$ curves; $248$ by the monomial lemma; $72$ by non-square
discriminants, counted in best frames), finite $600$, unknown $1267$
(bidegree $>6$, not pulled back), **no class infinite or candidate**.  Of
the $316$, $256$ died and $60$ became finite.  Within the box, the
obstruction to a uniform theorem is now purely the finite one: $600$
classes on even reciprocal hyperelliptic curves of genus $2,3,5$ (quotient
towers, then Chabauty where towers stop) and the high-bidegree components
(a cheaper factorization route is needed; one bidegree-$(4,4)$ pullback
did not factor in ten minutes).  What the engine can see is either dead
for all primes or on a curve with finitely many rational points.  Not a
theorem for the box.

**The five curves (entry 99).**  Identified with PARI, the thirteen killing
quartics are five curves up to isomorphism: Cremona **32a2** ($j=1728$, CM
by $\mathbb Z[i]$ — the Fermat/congruent-number curve of $x^4-y^4=z^2$ and
of four squares in arithmetic progression), **48a1**, **48a3**, **56a2**,
**80a1**; all full $2$-torsion, rank $0$, conductor $2^k\cdot\{1,3,5,7\}$.
The reading: a Pythagorean frame is a square in the rational circle group,
so each frame condition is a double cover of the circle branched at the
degenerate frame values; two such conditions on a rational component give
a $(2,2)$-cover of the line branched over four points — genus $1$ — whose
$j$-invariant is fixed by the cross-ratio of the branch points, and only a
few cross-ratios can arise from degenerate values.  If this persists across
boxes, the genus-$1$ pieces of every quadruple curve are twists of curves
from a fixed finite list and a uniform theorem needs only their ranks: the
Fermat–Euler descent as the universal mechanism, with the monomial lemma
disposing of the positive-dimensional families.  The plan built on this is
ROADMAP R.8.

## 2.30 Quotient towers: 296 more classes dead; what blocks the last 304

*(2026-09-04; entry 100; check `a3.omega3_towers`; code `compute/omega3_towers.py`.)*

**The towers.**  A finite class has a component whose rational points lie
on a hyperelliptic model $y^2=D(t)$ of genus $2,3,5$ ($D$ the squarefree
part of the discriminant in the component's quadratic variable, $t$ the
other frame ratio), or the same in $\tau$ at the pullback level.  Every
$\Phi$-level model is even (the conjugate frame $t\to-t$), its leading
coefficient is a square (the points at infinity are $t=\infty$), and some
carry a twisted reciprocity $t^dD(\kappa/t)=cD(t)$.  Each involution gives
a quotient curve over $\mathbb Q$ receiving the rational points: $u=t^2$
($D=G(t^2)$), $w=t+\kappa/t$ ($D=t^{d/2}P(w)$), and the odd companion
$Y^2=xQ_0(x)$ of an even quotient polynomial $Q(x)=Q_0(x^2)$; iterated to
depth three.  A genus-$1$ quotient of PARI rank $0$ with a complete point
enumeration lifts to finitely many $t$; if none is a non-degenerate frame
ratio the class is dead.  The genus-$2$ sextic quotients of the genus-$5$
models are even and split into two elliptic curves, which is how those
die.

**Result.**  $296$ of the $600$ finite classes are dead, through eight
rank-$0$ quotient curves: 30a2 ($u=t^2$, torsion $12$; $96$ classes), 80a1
($w=t-1/t$; $48$), 11a3 (odd companion of $w=t+1/t$, torsion $5$; $40$),
48a3 ($36$), 528j2 ($32$), 24a1 ($20$), 128c2 and 400d1 ($12$ each).  The
$304$ that remain: $224$ have only rank-$1$ elliptic quotients, $24$ rank
$2$ (389a1, 664a1, 13280a1 appear), $56$ none (genus-$2$ quotients only, or
a $(3,3)$ component with no hyperelliptic model).  Height searches to
$2000$ on $276$ of them found no non-degenerate point.  Box tally: **dead
$1373$, finite $304$, unknown $1267$.**

**The five-curve pattern, corrected.**  The branched-cover argument of
§2.29 is right for the $(2,2)$ components and wrong as a claim about
towers: the quotient curves of the genus-$3$ and $-5$ models range over two
dozen isomorphism classes, killers of conductor $11$ to $528$ and
positive-rank quotients up to conductor $13280$.  The mechanism is uniform;
the curve list is not finite in the naive sense.  The remaining $304$ are
the classical elliptic-Chabauty / two-cover situation (points of a rank-$1$
curve with a square coordinate), effective in principle with tools not
available here (Magma, Sage); the searches make them very likely empty.

## 2.31 The (2,1,1) box: the same engine, the same shapes, less coverage

*(2026-09-04; entry 101; check `a3.omega3_box211`; data
`compute/data_omega3_box211_sample.json`; `compute.omega3.set_box`.)*

**The box.**  Split part $p^2qr$.  The engine now takes any exponents
$(a,b,c)$: labels $|j|\le a$ etc. mod sign, elements
$(c_1^2+s_1^2)^{a-|j|}(c_2^2+s_2^2)^{b-|k|}(c_3^2+s_3^2)^{c-|l|}
\operatorname{Im}(\ell^{2j}w^{2k}v^{2l})$ — $(2a,2b,2c)$-forms — and the
symmetry group of conjugations and permutations of frames with equal
exponents.  For $(2,1,1)$: $22$ labels, $(4,2,2)$-forms (the exponent-$2$
frame enters through $\operatorname{Im}\ell^4=4c_1s_1(c_1^2-s_1^2)$, the
Chebyshev formula), agreeing with the two-frame relations on a $(2,1)$
pattern; $89{,}732$ classes, $79{,}368$ of them new.

**The sample.**  $400$ new classes, seeded, through decision and towers:
dead $88$ ($55$ at the decision level, $33$ by towers), finite $55$,
unknown $257$.  Median $9$ s per class; a full sweep is about $60$
CPU-hours and was not run.

**The same shapes recur.**  The rank-$0$ quartics that kill are the
$(1,1,1)$ list plus a few new twists ($t^4-14t^2+1$, $4t^4+7t^2+4$,
$3t^4-10t^2+3$, $t^4-6t^2+1$); the monomial lemma kills every rational
family again, now with angle multiples up to $4$ ($(2,1),(3,2),(4,1),
(3,1),(1,4),\dots$); the tower killers are the same eight curves plus
34a2, 592c1, 48a1, 56a2, 14a4, 80a2.  The mechanism transfers unchanged
to the exponent-$2$ frame; the curve list grows modestly.

**What changes is coverage.**  The resultants reach bidegree $(16,16)$ and
components above bidegree $6$ are not pulled back, so $64\%$ of the sampled
classes are unknown ($43\%$ in $(1,1,1)$).  Everything the engine sees is
dead or Faltings-finite; the fraction it sees shrinks with the exponent.
The high-bidegree components (R.8 phase 2) are therefore the bottleneck for
every box beyond $(1,1,1)$.

## 2.32 Phase 2: a genus lower bound certifies the high-bidegree classes finite

*(2026-09-04; entry 102; check `a3.omega3_genus`; code `compute/omega3_genus.py`,
`compute/omega3_sieve.py`.)*

**The obstruction.**  $1267$ classes had, in every frame, a component of
bidegree $\ge(3,3)$ with no hyperelliptic model, singular exactly at the
degenerate frame values ($t=0,\infty,\pm i$, and $-1\pm\sqrt2$ for the
$(8,8)$ ones), absolutely irreducible, with real points, and with an
irreducible pullback.  Two attempts failed and are recorded: a local
sieve (frames have $c$ odd, $s\equiv0\bmod4$, $(c,s)\ne(0,0)$ mod every
prime) is vacuous because every element is an imaginary part and the
all-real residue class always solves an Im-type relation; and factoring
the pullback (PARI does it instantly) leaves an irreducible curve of
doubled bidegree.

**The bound.**  For an absolutely irreducible $\Phi(t,x)=0$ of bidegree
$(d_g,d_h)$, Riemann–Hurwitz for the projection to the $t$-line gives
$2g-2=-2d_h+\sum_P(e_P-1)$, and over a branch value $b$ the ramification is
at least $d_h-\sum_{Q\mid b}m_Q$, since a point of multiplicity $m_Q$
carries at most $m_Q$ branches; with $I_Q$ the root multiplicity of $x_Q$
in the fiber ($x=\infty$ included), $g\ge1-d_h+\tfrac12\sum_b\sum_{Q\mid
b}(I_Q-m_Q)$.  Computed exactly: branch values grouped by the irreducible
factors $q$ of the discriminant, the fiber factored over $\mathbb Q[a]/(q)$
in PARI, $m_Q$ the least order of a partial derivative not divisible by the
point's factor; factors of degree above $40$ skipped (their contribution is
$\ge0$, so the bound stays valid); both projections taken.  Absolute
irreducibility is certified by irreducibility mod $p$ with a smooth
$\mathbb F_p$-point.  The genus-$1$ control gives $g\ge1$ exactly.

**Result as committed (entry 102).**  $1224$ of the $1267$ classes were
certified Faltings-finite; $43$ remained.  **Corrected in entry 103 (§2.33):**
those bounds were computed with PARI's `factor` over a *non-monic* modulus,
which silently rescales the generator of the branch-value field; $204$ of
the component bounds were wrong in value ($182$ too low, $22$ too high),
none crossed the threshold downward, so the $1224$ certifications stand;
the recomputation (nffactor against nfinit of the monic integral polynomial
of the scaled root) certifies $1264$ of the $1267$, and the $3$ others are
the degenerate classes, which have no high-bidegree component at all.  The
exact genera of §2.33 supersede the bounds.

## 2.33 The box closed: exact genera by resolution, and the three degenerate classes

*(2026-09-04; entry 103; check `a3.omega3_resolve`; code `compute/omega3_resolve.py`,
`compute.omega3.reduced_relations`.)*

**The exact genus.**  For an absolutely irreducible $\Phi(t,x)=0$ of
bidegree $(d_g,d_h)$, $g=p_a-\sum_Q\delta_Q$ with $p_a=(d_g-1)(d_h-1)$ and
$\delta_Q=\sum_P m_P(m_P-1)/2$ over the infinitely near points of the
blow-up tree at the singular point $Q$; the tree also counts the branches
$r_Q$.  Directions that are conjugate over the current field are handled in
the extension (PARI `rnfequation`, every field monic integral and factored
by `nffactor` against its own `nfinit`) and counted with multiplicity.
*Cross-check:* with $r_Q$ known, Riemann–Hurwitz for the $t$-projection is
exact, $R=R_{\rm lb}+\sum_Q(m_Q-r_Q)$, and $2g=2-2d_h+R$ must agree with
$p_a-\sum\delta_Q$ — required for every component (discriminant factors
to degree $400$).  Validated on the textbook singularities (node, cusp,
tacnode, triple point, $E_6$, $E_8$, the conjugate node $x^2+t^2$,
$x^4+t^4$), the genus-$1$ control, and $40$ recorded hyperelliptic genera.

**Result.**  All $1264$ high-bidegree classes are certified finite, each in
its recorded frame by one component of exact genus between $3$ and $23$
($(4,4)$: $3$–$9$; $(6,6)$: $5$–$13$; $(6,8)$, $(8,6)$: $5$–$19$; $(8,8)$:
$11$–$23$), consistent and absolutely irreducible.  The exact genus equals
the corrected bound for $1144$ components.  Among the $8086$ Galois orbits
of singular points there is no cusp: $6260$ nodes, $888$ tacnodes, ordinary
triple, $4$-fold and $6$-fold points, and $128$ orbits with fewer branches
than the multiplicity — exactly where the bound of §2.32 lost.

**The three degenerate classes.**  Their two relations share a common
factor $G$ depending on every frame ($4s_2s_3(c_1^2+s_1^2)$,
$4s_3(c_2s_1-c_1s_2)$, $4s_3(c_1c_2+s_1s_2)$), so every resultant vanished.
But $R_1=R_2=0$ iff $G=0$ or $R_1/G=R_2/G=0$: the factors of $G$ are
degenerate frames, norms, or the same-prime relations $t_1=t_2$,
$t_1t_2=-1$ (the $(2,\pm2)$ monomial relation $w_1^2=\pm w_2^2$, impossible
for distinct primes), and the reduced pairs force a degenerate frame or
the same relations.  The engine now divides out the common factor first;
$48$ classes have one (norms, monomials, same-prime factors only), $45$
already dead, the $3$ now dead.

**The box.**  $\boxed{\text{dead }1376,\ \text{finite }1568,\ \text{unknown }0}$
of $2944$: every class is impossible for every triple of distinct primes,
uniformly, or has in some frame only components with finitely many
rational points — hence can be carried by at most finitely many prime
pairs.  This is finiteness, not effectivity: the $304$ hyperelliptic models
blocked by positive-rank quotients and the $1264$ curves of genus $3$–$23$
need Chabauty-type methods (Magma/Sage) to make their finite sets explicit,
and the uniform statement of goal G is exactly that those sets contain no
non-degenerate frame pair.

## 2.34 The sweep made fast, and the finiteness statement for shape (1,1,1)

*(2026-09-05; entry 104; checks `a3.omega3_finiteness`, `a3.omega3_sweep_engine`,
`a3.omega3_box211_resample`; code `compute/omega3_finiteness.py`, `compute/omega3.py`.)*

**The finiteness statement.**  With every class of the $(1,1,1)$ box dead
or finite (§2.33), one gap separated the engine from a statement about
squares: a *base point* of the elimination — a frame pair $(t_g,t_h)$ at
which every coefficient of both relations, as polynomials in the
eliminated frame, vanishes — makes the relations hold for every third
frame, i.e. a square for every third prime.  The base locus is a
zero-dimensional system per class, solved exactly: $1024$ of the $1568$
finite classes have an empty base locus and $544$ have only the degenerate
points $t\in\{0,\pm1\}$; no admissible base point.  Since a frame ratio
$t=m/n$ in lowest terms determines its prime $p=\sqrt{m^2+n^2}$, every
square of that shape is one of finitely many frame pairs on a component
with finitely many rational points, times finitely many third ratios:

> **Up to scaling by the inert cofactor, only finitely many $3\times3$
> magic squares of squares have a center whose split part is a product of
> three distinct first-power primes.**

Ineffective (Faltings gives no bound), and resting on the engine's
verdicts — PARI's factorization over number fields, its unconditional rank
bounds, and the genus computations, each pinned by live recomputation in
the suite.  Not a theorem that no such square exists.

**The sweep made fast.**  The $(2,1,1)$ sweep's true baseline was $\sim470$
CPU-hours (the sample's mean, $21$ s per class, not its median).  Profiles
found two culprits: the monomial test (sympy's `simplify` on rational
functions with Gaussian coefficients, $95\%$ of the slowest class) and the
six-variable factorization of the resultant.  The monomial test is now an
exact polynomial identity over $\mathbb Q(i)$ (with $\tau=P/Q$ and
$w=(Q+iP)/(Q-iP)$, $w_g^a=\varepsilon w_h^b$ is $A_g^aB_h^b=\varepsilon
B_g^aA_h^b$), and the resultant is dehomogenized first: the relations are
bihomogeneous in every frame, so with $c=1$, $s=t$ they are polynomials in
$s_f$ over $\mathbb Q[t_g,t_h]$ whose bivariate resultant carries exactly
the non-monomial factors of the six-variable one.  The genus routes of
§§2.32–2.33 now run inside the engine (the bound first, with a field-degree
cap and an alarm that only skip fields; the resolution second, certified
only with its cross-check, else *provisional*), and the class decision is
two-pass.  On the entry-101 sample no verdict regressed, $254$ of $257$
unknown classes became finite ($129$ rigorously, $125$ provisionally), and
the cost fell from $21$ s to $1.2$ s per class.  The full sweep was launched.

## 2.35 The quadruple curves as pullbacks of the circle: the minor formula, the singular locus, the lift (attempt C, first step)

*(2026-09-05; entry 105; check `a3.omega3_minors`.)*

**The trigonometric form.**  Write a frame as $\ell=c+is=p\,e^{i\theta}$, so
$t=s/c=\tan\theta$ and $e^{i\theta}=\pi/\bar\pi$ is the circle-group generator
of the prime.  Every element of the $(1,1,1)$ box is, up to the common factor
$c_1^2c_2^2c_3^2\sec^2\theta_1\sec^2\theta_2\sec^2\theta_3$,
$$e(j,k,l)=\sin\bigl(2(j\theta_1+k\theta_2+l\theta_3)\bigr),\qquad j,k,l\in\{-1,0,1\}$$
(checked on all 13 labels), and the two quadruple relations are two
three-term sine relations among linear forms in the angles.  *The primes
enter only through "$\tan\theta_i$ is the ratio of a prime's frame".*

**The minor formula (theorem).**  Fix the frame $f$ to eliminate.  In
$(X,Y,N)=(2c_fs_f,\;c_f^2-s_f^2,\;c_f^2+s_f^2)$, with $X^2+Y^2=N^2$, every
element is linear: an element with $l=\pm1$ is $\operatorname{Im}((Y\pm iX)Z)=
Y\operatorname{Im}Z\pm X\operatorname{Re}Z$ and one with $l=0$ is $N\operatorname{Im}Z'$, where
$Z,Z'$ are monomials $\ell_g^{2j}\ell_h^{2k}$ in the other two frames.  So
$$R_1=a_1X+b_1Y+c_1N,\qquad R_2=a_2X+b_2Y+c_2N,$$
with $a_i,b_i,c_i$ bihomogeneous forms of bidegree $\le(2,2)$ in the frames
$g,h$ (real and imaginary parts of the monomials).  Writing $R_i=A_ic_f^2+B_ic_fs_f+C_is_f^2$,
one has $(a_i,b_i,c_i)=(B_i/2,(A_i-C_i)/2,(A_i+C_i)/2)$, and the classical
resultant of two binary quadratics,
$\operatorname{Res}=(A_1C_2-A_2C_1)^2-(A_1B_2-A_2B_1)(B_1C_2-B_2C_1)$, is exactly
$$\operatorname{Res}_{s_f}(R_1,R_2)=4\,(D_X^2+D_Y^2-D_N^2),\qquad
(D_X,D_Y,D_N)=(a_1,b_1,c_1)\times(a_2,b_2,c_2).$$
Hence **every quadruple curve $\Phi_f$ is a component of the pullback of the
circle $X^2+Y^2=N^2$ under the rational map $m=(D_X:D_Y:D_N)\colon
\mathbb P^1\times\mathbb P^1\dashrightarrow\mathbb P^2$ given by the three
$2\times2$ minors, of bidegree $\le(4,4)$** — which is why the components
never exceed bidegree $(8,8)$.  Verified on 30 sampled certified classes
(every component divides $D_X^2+D_Y^2-D_N^2$; 30/30).

**The singular locus.**  For $F=m^*(X^2+Y^2-N^2)$ one has $dF=2(D_XdD_X+D_YdD_Y-D_NdD_N)$,
so the singular points of $\Phi_f$ are of two kinds: the **base points** of
$m$, where $D_X=D_Y=D_N=0$ — the two relations become proportional, the third
frame is unconstrained on a whole line, which meets the circle in two points:
the two branches of a node (nodes are 6260 of the 8086 singular orbits of the
box) — and points where $m$ is tangent to the circle.  On the sample the
second kind occurs only over the degenerate frame values $t=\pm i$ and $t=0$
(21 of 30 classes have every affine singular point on the base locus; the 9
exceptions are all at $t^2+1$ or $t$).  The base locus is where the two rows
$(a_i,b_i,c_i)$ — vectors of cosines and sines of $2(j\theta_g+k\theta_h)$ — are
proportional: three trigonometric equations of small frequency in two angles,
whose common zeros are the torsion points $e^{2i\theta}$ of order dividing $24$
($t=\pm1$, $t^2=3$, $3t^2=1$, $t^2\pm2t=1$, $t^2\pm4t=-1$) and the
"half-Pythagorean" points with $\cos2\theta\in\{\tfrac13,\tfrac34,\tfrac14,\tfrac23,\tfrac18,\tfrac56,\tfrac54\}$
(where $e^{2i\theta}=\alpha/\bar\alpha$ for a small-norm $\alpha$ in
$\mathbb Q(\sqrt{-2}),\mathbb Q(\sqrt{-7}),\mathbb Q(\sqrt{-15}),\mathbb Q(\sqrt{-5}),\mathbb Q(\sqrt{-11})$, or $w=2$),
plus six quartic values — the 50 $t$-factors of the census, 8086 orbits.  The
base points of the *elimination* (both rows zero, entry 104's finiteness check)
are the rank-0 part of this locus.

**The third frame in closed form.**  At a point of $\Phi_f$ the eliminated
frame is $(X:Y:N)=(D_X:D_Y:D_N)$, so $t_f=D_X/(D_N+D_Y)$ and the Pythagorean
condition for $f$ reads
$$2\,D_N\,(D_N+D_Y)=\square\quad\text{on }\Phi_f$$
(since $(D_N+D_Y)^2+D_X^2=2D_N(D_N+D_Y)$ on the curve).  So the full
frame-triple curve is the $(2,2,2)$-cover of $\Phi_f$ cut by $1+t_g^2=\square$,
$1+t_h^2=\square$ and this condition — three double covers with explicit
branch loci: $t_g=\pm i$, $t_h=\pm i$, and $D_N(D_N+D_Y)=0$ on $\Phi_f$.  The
structural lemma of R.9.C is the statement that these branch loci stay on the
torsion/half-Pythagorean set for every box; the minor formula makes it a
question about the zeros of two explicit forms on the curve.

**What generalizes.**  For a box with exponent $a_f$ on the eliminated frame,
the elements are polynomials of degree $a_f$ in $(X,Y,N)$ (Chebyshev in the
double angle), so $\Phi_f$ is the pullback of a curve of degree $a_f$ in the
plane of $(X:Y:N)$ intersected with the circle — the resultant of two degree-$a_f$
forms restricted to the conic — and the same three double covers describe the
frame conditions.  Uniformity in the exponents is the question of how the
base loci of these maps grow.

## 2.36 Quotient kills: 72 finite classes die through rank-0 quotients by their involutions

*(2026-09-05; entry 105; check `a3.omega3_quotients`; code `compute/omega3_quotients.py`.)*

Every certified component of the $(1,1,1)$ box is invariant under the
joint sign change $(t_g,t_h)\mapsto(-t_g,-t_h)$, and $944$ of the $1264$
carry a further involution on one coordinate ($t\mapsto-t$, $1/t$, $-1/t$)
or the swap.  The quotient by an involution has lower genus; a genus-$1$
quotient that is quadratic in a variable has the hyperelliptic model
$y^2=\mathrm{disc}(u)$, PARI's unconditional rank bound with a complete
enumeration lists every rational point, each lifts to finitely many
rational preimages, and if none is a pair of admissible frame ratios the
class is dead — the mechanism of the quotient towers (§2.30) on the
non-hyperelliptic curves.  Result: **72 classes die** (routes: negrec_h 32, neg_g 16, rec_g 16, rec_h 8).
**Box tally after entry 105: dead $1448$, finite $1496$, unknown $0$.**

**The two-step route (entry 106).**  The joint quotient $E=\Phi/\sigma$ has
genus $1$ for $96$ curves but no model quadratic in a variable (bidegree up to
$(4,4)$ in both the $(t_g^2,t_gt_h)$ and the $(t_g^2,t_h^2)$ models).  A second
involution $\tau$ of the curve descends to $E$, and $W=E/\bar\tau$ has lower
degree: for $W$ of genus $1$ the rank-$0$ route lists its points and each has
finitely many preimages on $E$ and on the curve (both coordinates rational
squares); for $W$ of genus $0$ the parametrization makes $E$ the double cover
$y^2=\Delta(\lambda)$, its own quartic model.  Result: **36 more classes die**
(32 through $t\mapsto-1/t$ or $1/t$ with $W$ of genus $1$, $4$ through the swap
with $W$ of genus $0$); $16$ are blocked by a non-quadratic $W$ and $28$ have no
second involution.  A bug fixed on the way: a cubic model $y^2=f$ was never
"complete" because its point at infinity was not counted.  **Box tally: dead
$1484$, finite $1460$, unknown $0$.**  The $24$ genus-$0$ quotients
(hyperelliptic curves of bidegree $(6,8)$, $(8,6)$, $(6,6)$) need a rational
parametrization of a rational curve of bidegree $(4,6)$ or $(3,6)$ — a
Riemann–Roch computation that Sage or Magma provides and our tools do not.
The genus $\ge2$ quotients and the positive-rank genus-$1$ quotients are the
honest Chabauty list for attempt B.


## 2.37 The (2,1,1) sweep: the whole box decided; the killers are ten curves

*(2026-09-05; entry 107; check `a3.omega3_box211_sweep`; data
`compute/data_omega3_box211.json.gz`.)*

All $79{,}368$ new three-frame classes of the $(2,1,1)$ box through the fast
engine at the decision level (44.9 CPU-hours, median 1.1 s per class), the
residue re-decided with the entry-105 fixes.  **Tally: dead $11962$
(15.1%), finite $41784$ (52.6%), finite with a provisional genus
$25428$ (32.0%), unknown $188$.**  The dead fraction falls from
$50\%$ in $(1,1,1)$ to $15\%$ because the components are mostly of high
bidegree, where only the genus decides.  The rank-$0$ killers are $29$
quartic models but **ten curves up to isomorphism**: the five of the
$(1,1,1)$ box and $24a1$, $15a3$, $528j2$, $240d2$, $240d4$ (eight
$j$-invariants; conductors from $\{2,3,5,7,11\}$) — the finite-list
reading of the elliptic killers survives the growth of an exponent.  The
monomial relations reach angle multiple $4$ (and $5$ in the residue).  A
sample of the certified curves shows the same singular locus as in
$(1,1,1)$: torsion points of small order, $\pm i$, infinity, a thin
algebraic tail.  Open in the box: the unknown components of genus $0$ or
$1$ at high bidegree (the elliptic and parametrization routes are not yet
available there), the provisional third (a cross-check that avoids field
initialization, or Sage), and then the finiteness statement for the shape.

## 2.38 The unknowns of the (2,1,1) box: the conjugate-components kill; no unknown class remains

*(2026-09-05; entry 108; check `a3.omega3_unknowns`; code `compute/omega3_unknowns.py`.)*

The $188$ unknown classes had components of exact genus $0$ or $1$ at high
bidegree.  Three routes decide them all.  The two-step trick one level up:
a genus-$1$ component's quotient by an involution of genus $0$, parametrized,
makes the component its own double cover $y^2=\Delta(\lambda)$, a quartic
model with a rank; of genus $1$ and rank $0$, the finitely many preimages.
The pullback at cap $12$ for genus-$0$ components quadratic in a variable.
And the decisive one, the **conjugate-components kill**: $320$ quotients came
out with "genus $-1$", impossible for an absolutely irreducible curve, and
indeed those components are irreducible over $\mathbb Q$ but split over
$\mathbb Q(\sqrt3)$ into two conjugate pieces; every rational point lies on
both, i.e. on $A=P_1+\bar P_1$ and $B=(P_1-\bar P_1)/\sqrt3$, two polynomials
over $\mathbb Q$ with a finite common zero set, and no common rational zero
is an admissible frame pair.  Result: of the $188$, $164$ dead ($156$ by
conjugate components, $8$ by the pullback) and $24$ finite; the six
"degenerate" classes die by their one-frame common factor $t_1=\pm1$; a
failed absolute-irreducibility certificate no longer blocks finiteness (the
dichotomy: genus $\ge2$ if absolutely irreducible, a finite intersection of
conjugates if not).  **Box $(2,1,1)$: dead $12132$, finite $41808$, finite with a
provisional genus $25428$, unknown $0$.**  The finiteness statement for the shape
waits for the rigorous pass on the provisional third and the base-locus check.

## 2.39 The singular-locus dichotomy is a theorem (attempt C, second step)

*(2026-09-06; entry 109; check `a3.omega3_dichotomy`.)*

**Setting.**  Put $w=e^{2i\theta}=(1+it)/(1-it)$ for each frame; the three frames
are coordinates on the torus $(\mathbb C^*)^3$, and each relation of a class
is a Laurent polynomial
$$R_i=\sum_e \varepsilon_e\operatorname{Im}\bigl(w_g^{j_e}w_h^{k_e}w_f^{l_e}\bigr),$$
six monomials each.  When the eliminated frame $f$ has exponent $1$
($l_e\in\{-1,0,1\}$), $w_fR_i$ is a quadratic $q_i(w_f)$ whose coefficients are
the rows $(a_i,b_i,c_i)$ of the minor formula (§2.35).  The space curve
$\Gamma=\{R_1=R_2=0\}$ projects onto the elimination curve; a component
$\Phi_f$ is the image of the branches of $\Gamma$ over it.

**Theorem (the dichotomy).**  Let $a_f=1$.  A singular point $p$ of a component
$\Phi_f$ is one of:
1. a **base point of the minor map** — the quadratics $q_1,q_2$ are proportional
   at $p$ (all three minors vanish; the third frame is free on a line meeting
   the circle twice: a node);
2. the projection of a **singular point of $\Gamma$**;
3. a point on the **toric boundary** — $t_g$ or $t_h$ equals $\pm i$ (a frame
   at $w\in\{0,\infty\}$), or a common root of the $q_i$ at $w_f\in\{0,\infty\}$
   ($t_f=\pm i$), where the Laurent description degenerates.

*Proof.*  Take $\gamma=(p,w_f)\in\Gamma$ off the boundary with $\Gamma$ smooth at
$\gamma$.  The projection $\pi\colon\Gamma\to(w_g,w_h)$ maps a neighbourhood of
$\gamma$ isomorphically onto a smooth branch unless its differential kills the
tangent line of $\Gamma$, i.e. the tangent is vertical: $\partial R_1/\partial w_f
=\partial R_2/\partial w_f=0$ at $\gamma$.  Since $R_i=q_i(w_f)/w_f$ and
$q_i(w_f)=0$, this says $q_i'(w_f)=0$: $w_f$ is a double root of both quadratics,
so $q_1$ and $q_2$ are both multiples of $(w-w_f)^2$ — proportional — and $p$
is a base point (case 1).  If the image branch is smooth but $\Phi_f$ is singular
at $p$, another branch of $\Gamma$ passes over $p$: a second common root
$w_f'\neq w_f$ of $q_1,q_2$, and two quadratics with two common roots are
proportional (case 1 again).  What remains is a singular point of $\Gamma$
(case 2) or a point where the argument's hypotheses fail (case 3). $\square$

**What the census now says.**  Of the $8086$ singular orbits of the $1264$
certified curves, $3908$ affine $t$-factors were tested against the base locus
(§2.35): $878$ curves entirely on it, and $408$ exceptions.  Every exception is
of type 3 or 2: of the 492 exceptional singular points re-examined exactly, 464 are base points after all (the rows at the point have rank 0 or 1 — the entry-105 test had used a non-squarefree gcd), and the remaining 28 lie over $t=\pm i$ with the eliminated frame at $\pm i$ too; with the corrected test, 1248 of the 1264 curves have every affine singular point on the base locus and the exceptions are {'t^2 + 1': 16}.  So on the whole box the singular points of
the quadruple curves are the base points of the minor map, the toric boundary,
and singular points of $\Gamma$ at the torsion values $t\in\{0,\infty,\pm1,\tan(\pm22.5^\circ)\}$.

**Why it matters.**  The theorem reduces the singular locus — hence the genus,
by resolution — to two explicit zero-dimensional systems on the torus: the
proportionality of two coefficient rows (the base locus), and the rank drop of
a $2\times3$ Jacobian of two six-term Laurent polynomials (the singular points of
$\Gamma$).  Both are questions about *vanishing sums of few monomials on a torus*,
where the torsion part is bounded uniformly (Conway–Jones), which is the shape
of the base-locus theorem that R.10.O3 asks for.  The same proof applies to every
box in which the eliminated frame has exponent $1$ — in particular to $(2,1,1)$
eliminating a first-power frame, and to every $(a,1,1)$.

## 2.40 The base locus of the minor map (attempt C, third step) and the field-free cross-check

*(2026-09-06; entry 110; check `a3.omega3_baselocus`.)*

**The equations.**  In the torus coordinate $w_f$ each relation is, after the
unit factors $(w+1)^k$, a quadratic $q_i=\alpha_iw_f^2+\beta_iw_f+\gamma_i$ whose
coefficients are Laurent polynomials in $(w_g,w_h)$: $\alpha_i$ has one term per
element of the relation with $l_e\ne0$ ($W_e$ or $\bar W_e$ by the sign of $l_e$),
$\beta_i$ one per element with $l_e=0$ ($W_e-\bar W_e$), and $\gamma_i$ is $\bar\alpha_i$
up to a monomial.  The base locus of the minor map — $q_1\propto q_2$ — is the
common zero set of
$$\alpha_1\gamma_2-\alpha_2\gamma_1=0,\qquad \alpha_1\beta_2-\alpha_2\beta_1=0,$$
two Laurent polynomials with at most nine monomials.  When both $\alpha_i$ are
single monomials (262 of the $1264$ certified pairs) the first equation is
the torsion coset $W_1/W_2=\pm1$ and the second a one-variable Laurent equation
of degree $\le4$ along it, which is why the coordinates of base points have
degree $\le4$ over $\mathbb Q$; in general the torsion part of such a system is
bounded uniformly (Conway–Jones).

**The census (all $1264$ certified classes, exact).**  The affine base locus is
the union of three kinds of pieces.  *Curves:* the common factor of the three
minors — a same-prime coset $t_g=\pm t_h$ or $t_gt_h=\pm1$ ($w_g=\pm w_h^{\pm1}$: a
point of it carries the frame of one prime twice), or, for the $18$ classes
whose relations both involve the eliminated frame in all three elements (so
$\beta_1=\beta_2=0$ and $\mathrm{Res}=(\alpha_1\gamma_2-\alpha_2\gamma_1)^2$), the
quadruple curve itself, a bidegree-$(4,4)$ curve of genus $7$ or $9$ ($4$ and $14$ classes) along which the
minors give no third frame ($w_f^2=-\gamma_1/\alpha_1$, two values over every
point): equal frames (same prime) in 36 classes; perpendicular frames (same prime) in 36 classes; the quadruple curve itself in 18 classes; conjugate frames (same prime) in 6 classes; conjugate-perpendicular frames (same prime) in 6 classes.  *Lines:* full lines $t=c$ of the
residual locus, on the box only degenerate or boundary lines: $t_h=\pm i$ in 68 classes; $t_h=0$ in 36 classes.
*Isolated points* (after saturation by the line equations), whose coordinates,
by irreducible factor, are degenerate values $0$, $\pm1$; $\pm i$; torsion
points $\tan(k\pi/n)$ with $n\in\{3,6,8,12\}$; half-Pythagorean values ($t^2$
rational, $\cos2\theta\in\{1/3, 1/4, 1/6, 1/8, 2/3, 3/4, 5/4, 5/6, 7/8, 7/9, -1/3, -1/4, -1/6, -1/8, -2/3, -3/4, -5/4, -5/6, -7/8, -7/9\}$, the value $\pm\tfrac54$ hyperbolic, $w=\pm2,\pm\tfrac12$);
values with $\tan2\theta\in\{\pm\tfrac23,\pm\tfrac32\}$ (the non-even quadratics);
and quartic values.  Counts: {'degenerate rational 0': 2384, '+-i': 2336, 'degenerate rational 1': 1184, 'degenerate rational -1': 1184, 'half-Pythagorean': 708, 'torsion n=6': 567, 'torsion n=3': 555, 'algebraic deg 4': 396, 'torsion n=8': 288, 'torsion n=12': 148, 'algebraic deg 2': 56}; status of the loci: {'points': 1058, 'lines + points': 104, 'curves + points': 84, 'curves': 18}.
**No coordinate of an isolated point or a line is a frame ratio, and a point
of a same-prime coset carries the frame of one prime twice: outside the $18$
self-base classes no base point of the minor map is an admissible frame pair;
on those $18$ the statement is the class's own (Faltings) finiteness
certificate.**

**The field-free cross-check (O1(a)).**  The exact ramification of the
$t$-projection is $\sum_b\bigl[\deg P_b-\deg\mathrm{sqf}(P_b)+(I_\infty-1)^+\bigr]+\sum_{Q\ \mathrm{sing}}(1-r_Q)$:
the first sum needs only a gcd over $\mathbb Q(b)$ (no field initialization,
no factorization over the field), the second is the resolution's own branch
count.  It reproduces the field-based check (2g = 42 on a certified $(8,8)$ in
0.1 s instead of 14 s) and certifies the $(16,16)$ and $(12,8)$ components of the
$(2,1,1)$ box; the rigorous pass over the $25{,}428$ provisional classes runs on
it (entry 111 reports).

## 2.41 The elimination base-locus theorem (attempt C, the finiteness statements made structural)

*(2026-09-06; entry 111; check `a3.omega3_elimination`.)*

**What the finiteness statements need.**  A finiteness statement for an exponent
shape (2.36 for $pqr$) rests on two facts about every class: every component of the
quadruple curve $\Phi_f$ of the deciding frame is Faltings-finite, and the
*elimination base locus* — the pairs $(t_g,t_h)$ at which every coefficient of both
relations, as polynomials in the eliminated frame, vanishes, so that the relations
hold for every third frame — contains no admissible pair.  The second fact was a
census (entry 104: 122 rational base points, all degenerate).  It is a theorem.

**The coefficients.**  In the torus coordinates $w_j=e^{2i\theta_j}$ an element is
proportional to $W_e-W_e^{-1}$, $W_e=\prod_j w_j^{e_j}$.  Write $W_e=M_e\,w_f^{l_e}$
with $M_e$ a monomial in the two other frames.  A relation
$\sum_{e\in S}\varepsilon_e(W_e-W_e^{-1})=0$ ($|S|=3$) is a Laurent polynomial in $w_f$
whose coefficient of $w_f^{\,j}$ is
$$c_j=\sum_{l_e=j}\varepsilon_eM_e-\sum_{l_e=-j}\varepsilon_eM_e^{-1},$$
with $\#\{l_e=j\}+\#\{l_e=-j\}$ terms for $j\ne0$ and $2\,\#\{l_e=0\}$ terms for $j=0$.
Each term is a monomial in $(w_g,w_h)$ with a sign.

**Lemma A (monomials and binomials).**  A monomial never vanishes on the torus
$|w_g|=|w_h|=1$.  A binomial $\varepsilon M+\varepsilon'M'$ vanishes exactly on the
torsion coset $M/M'=\mp1$, i.e. $w_g^aw_h^b=\pm1$ with $(a,b)$ the exponent
difference; if $(a,b)=(0,0)$ it is identically zero or nowhere zero.

**Lemma B (no admissible pair on a proper torsion coset).**  The frame of a split
prime $p$ is $\ell=u\pi_p^2$ ($u$ a unit, $\pi_p$ a Gaussian prime over $p$), so
$w_p=\ell/\bar\ell=\pm(\pi_p/\bar\pi_p)^2$.  If $w_g^aw_h^b$ is a root of unity with
$(a,b)\ne(0,0)$ and $p_g\ne p_h$, then $\pi_g^{2a}\pi_h^{2b}=\zeta\,\bar\pi_g^{2a}\bar\pi_h^{2b}$
in $\mathbb Z[i]$ with $\zeta$ a unit; the four primes $\pi_g,\bar\pi_g,\pi_h,\bar\pi_h$ are
pairwise non-associate, so unique factorization forces $a=b=0$.  In the same way no
frame ratio is a torsion point ($\pi_p^2$ is not associate to $\bar\pi_p^2$); the
rational torsion points are exactly the degenerate values $t\in\{0,\pm1,\infty\}$.

**Theorem (elimination base locus).**  Let $f$ be the eliminated frame.  For each
relation call it *empty-type* if some $j\ne0$ has exactly one element with
$|l_e|=j$ (then $c_j$ is a monomial), *torsion-type* if every nonzero coefficient is
a binomial (at most two elements at each $|l_e|=j>0$ and at most one with $l_e=0$),
and *trinomial-type* otherwise (all three elements at the same $|l_e|=j>0$).  Then the
elimination base locus is

* empty on the torus, if either relation is empty-type;
* a union of torsion cosets and torsion points, if both are torsion-type — and then
  it contains no admissible pair (Lemma B);
* contained in the torsion cosets of the torsion-type relation, if one relation is
  torsion-type and the other trinomial-type — again no admissible pair;
* the intersection of the two trinomial curves $\{c_{j_1}^{(1)}=0\}\cap\{c_{j_2}^{(2)}=0\}$
  (with their conjugates) if both are trinomial-type, i.e. exactly when **the
  eliminated frame appears with the same absolute exponent in all four labels**.

*Proof.*  The locus is the common zero set of all coefficients of both relations;
Lemma A describes each coefficient's zero set; Lemma B excludes admissible pairs on
proper torsion cosets, and the cosets are proper because a monomial ratio of two
distinct labels' monomials has $(a,b)\ne(0,0)$ unless the labels agree outside $f$,
in which case the binomial is a constant multiple of a monomial (empty) or zero
(then the coefficient is absent).  $\square$

**Corollary.**  For every exponent shape the base-locus condition of the finiteness
statement is automatic except for the classes in which the eliminated frame has the
same absolute exponent in all four labels; for those it is the finite intersection
of two trinomial curves (or, if the trinomials share a factor, a curve to be
examined), and it is a finite exact computation.  On the $(1,1,1)$ box: 834 empty-type, 516 torsion-type and 218 trinomial-type classes among the 1568 finite at entry 104;
the exact loci agree with the prediction in every class (empty -> empty: 502; torsion -> empty: 372; empty -> points: 332; trinomial -> empty: 150; torsion -> points: 144; trinomial -> points: 68), and the
trinomial-type classes' base points are on the toric boundary ($t=\pm i$, 124 coordinates) or degenerate ($t=0$, 12); the torsion-type loci carry degenerate values, boundary points and torsion of order 3 and 6 only.

**The minor-map base locus, extended.**  The census of 2.40 covered the $1264$ classes
with a resolution block; the $304$ finite classes with a single low-bidegree
component are now included: status {'curves + lines': 154, 'points': 88, 'curves': 46, 'lines + points': 16}; curves {'curve': 212, 'perpendicular frames (same prime)': 16, 'equal frames (same prime)': 16} (the 200 self-base classes are exactly the trinomial-type ones there, $18+200=218$); lines {'tg = +-i': 104, 'th = +-i': 48, 'th = degenerate rational 0': 20, 'tg = degenerate rational 0': 6, 'th = degenerate rational 1': 6, 'th = degenerate rational -1': 6}; coordinate kinds {'degenerate rational 0': 208, '+-i': 180, 'degenerate rational 1': 104, 'degenerate rational -1': 104, 'algebraic deg 6': 64, 'algebraic deg 4': 44}; no coordinate is a frame ratio.

## 2.42 The killers are fifteen curves, eleven of them Legendre (attempt C; R.10 objective O3, "why ten killers")

*(2026-09-06; entry 112; check `a3.omega3_killers`.)*

**A correction.**  Entries 100 and 107 listed ten killing curves up to
isomorphism.  Identifying every rank-0 model on record gives more.  *(A) The
coordinate and joint quotients* — the models of 2.37 (entry 105) and of the
$(2,1,1)$ sweep, $31$ quartics $y^2=q(x)$ — are **eleven** curves: the ten and
`120b2` ($y^2=x^4+x^2+4$, $y^2=4x^4+x^2+1$), which entry 105 used for $16$
kills.  *(B) The two-step route* of entry 106 ($W=E/\tau$, cubic and quartic
models) killed through **four more**: `30a1`, `240b1`, `30a2`, `240b2`.  Fifteen
curves across all routes.

**Legendre form of the quotient-route killers.**  All eleven have full rational
$2$-torsion (torsion subgroup of order $4$ or $8$), so each is a *quadratic
twist* $dy^2=x(x-1)(x-\lambda)$ of a Legendre curve — $\lambda$ fixes the curve
only over $\bar{\mathbb Q}$, and the table below contains twist pairs sharing
$\lambda$ (`48a1`/`24a1`, `15a3`/`240d2`); writing the $S_3$-orbit of $\lambda$ by
its largest element, one value per curve (corrected in entry 117):

| curve | $\lambda$ | kills (both boxes) | models $y^2=q(x)$, coefficients of $q$ |
|---|---|---|---|
| `120b2` | $8/3$ | 16 | (1, 0, 1, 0, 4); (4, 0, 1, 0, 1) |
| `15a3` | $16$ | 96 | (15, 0, -34, 0, 15) |
| `240d2` | $16$ | 88 | (1, 0, -62, 0, 1); (25, 0, 34, 0, 9); (4, 0, 7, 0, 4); (9, 0, 34, 0, 25) |
| `240d4` | $25/9$ | 32 | (25, 0, -14, 0, 25); (9, 0, 82, 0, 9) |
| `24a1` | $4$ | 168 | (3, 0, -10, 0, 3) |
| `32a2` | $2$ | 166 | (1, 0, -6, 0, 1); (1, 0, 6, 0, 1) |
| `48a1` | $4$ | 5596 | (1, 0, -14, 0, 1); (1, 0, 1, 0, 1); (1, 0, 10, 0, 9); (3, 0, 10, 0, 3); (5, -8, 10, -8, 5); (5, 8, 10, 8, 5); (9, 0, 10, 0, 1) |
| `48a3` | $9$ | 2232 | (1, 0, 34, 0, 1); (5, -16, 10, 16, 5); (5, 16, 10, -16, 5); (9, 0, -14, 0, 9) |
| `528j2` | $33$ | 60 | (1, 0, 130, 0, 1) |
| `56a2` | $8$ | 332 | (1, 0, -3, 0, 4); (1, 0, 30, 0, 1); (4, 0, -3, 0, 1) |
| `80a1` | $5$ | 1346 | (1, 0, -3, 0, 1); (1, 0, -6, 0, 25); (1, 0, 18, 0, 1); (25, 0, -6, 0, 1) |

so $\lambda\in\{2, 8/3, 25/9, 4, 5, 8, 9, 16, 33\}$.  For every even model $y^2=ax^4+bx^2+c$ the
product $ac$ is a square and
$$\lambda=\frac{b-2\sqrt{ac}}{b+2\sqrt{ac}}$$
(in the orbit; the four non-even models, twists of `48a1`/`48a3`, are the
$(x,z)$-route models).  The two-step curves:

| curve | form | kills |
|---|---|---|
| `240b1` | no full rational 2-torsion | 16 |
| `240b2` | Legendre, lambda = 32/5 | 1 |
| `30a1` | no full rational 2-torsion | 16 |
| `30a2` | Legendre, lambda = 32/5 | 3 |

**What is and is not explained.**  The *shape* of a quotient-route killer is
explained: a coordinate quotient of a quadruple curve is $y^2=ax^4+bx^2+c$ with
$ac$ a square, hence a Legendre curve with the $\lambda$ above; every integer value is a power of two or one more than a power of two ($\lambda\in\{2, 4, 5, 8, 9, 16, 33\}$), while $8/3$ and $25/9$ do not fit, and the branch
points of the models in the torus coordinate are torsion for some (`48a1`:
order $12$; `32a2`: order $8$; `24a1`: orders $3,6$), hyperbolic (real $w$) for
others, on the circle but not torsion, or generic — no uniform pattern.  *Rank
zero* is verified (2-descent in the kills, analytic rank here), not explained;
why these $\lambda$ recur across both boxes stays open.

## 2.43 The finiteness statement for shape $(2,1,1)$ (attempt C; R.10 objective O1)

*(2026-09-06; entry 113; check `a3.omega3_box211_finiteness`.)*

**Statement.**  Up to the scaling of the square, there are finitely many
$3\times3$ magic squares of distinct squares whose split part is $p^2qr$
($p,q,r$ distinct primes $\equiv1\pmod4$; Faltings-ineffective).

**Proof, by the two halves of 2.36.**  *(a) Every class is dead or Faltings-finite
with a rigorous genus.*  The sweep (2.38, entry 108) left $25{,}428$ classes
"finite*", their certifying components resolved without the field-based
cross-check.  The rigorous pass re-resolved every such component of the deciding
frame with the field-free Riemann–Hurwitz check of 2.40: $25378$ classes upgraded,
$50$ left; the tally of the $79{,}368$ new classes is now {'dead': 12132, 'finite': 67186, 'finite*': 50}; the
re-resolved components have genera 7 (72), 9 (784), 10 (1176), 11 (1324), 12 (208), 13 (3160), 14 (1008), 15 (1180), 16 (1456), 17 (1230), 18 (488), 19 (1976), 20 (560), 21 (944), 22 (24), 23 (1006), 24 (312), 25 (944), 26 (848), 27 (304), 28 (848), 29 (624), 30 (192), 31 (1148), 32 (504), 33 (286), 34 (640), 35 (232), 37 (720), 38 (48), 39 (272), 40 (48), 41 (84), 42 (96), 43 (8), 44 (160), 45 (180), 46 (64), 47 (48), 49 (28), 50 (48), 51 (56), 52 (32), 53 (8) (all cross-checks consistent:
{'True': 25378}); $16.7$ CPU-hours.  *(b) No admissible pair in an elimination base locus.*
For every finite class the base locus of the elimination in the deciding frame
(2.36; lines reported since entry 111) was solved exactly: status {'empty (Groebner basis 1)': 18088, 'zero-dimensional': 49148}; $1982$
rational base points, all degenerate ({"('0', '0')": 1408, "('0', '1')": 119, "('0', '-1')": 119, "('-1', '1')": 72, "('1', '-1')": 72, "('1', '1')": 68, "('-1', '-1')": 68, "('1', '0')": 28, "('-1', '0')": 28}); lines none; **no admissible
point or line**.  The elimination base-locus theorem (2.41) predicts from the
labels {'empty': 26390, 'trinomial': 22474, 'torsion': 18372} (by deciding frame, $0$ the exponent-$2$ frame: {"(0, 'empty')": 7116, "(0, 'torsion')": 2406, "(0, 'trinomial')": 1108, "(1, 'empty')": 9908, "(1, 'torsion')": 10942, "(1, 'trinomial')": 13210, "(2, 'empty')": 9366, "(2, 'torsion')": 5024, "(2, 'trinomial')": 8156}), and the
pass agrees — predicted empty: no rational base point; predicted torsion: only
degenerate points (('empty', 'empty (Groebner basis 1)', True): 7458; ('trinomial', 'zero-dimensional', True): 17484; ('torsion', 'zero-dimensional', True): 12732; ('empty', 'zero-dimensional', True): 18932; ('trinomial', 'empty (Groebner basis 1)', True): 4990; ('torsion', 'empty (Groebner basis 1)', True): 5640; no violation).  With (a) and (b), the argument of 2.36
applies verbatim.  $\square$

**What the theorem bought.**  Two thirds of the base-locus half were automatic
by 2.41; the trinomial-type third — the deciding frame at one absolute exponent
in all four labels — was a finite exact computation, and on this box too its
base points are all degenerate.

**Addendum (entry 114).**  The $50$ classes left "finite*" above were
provisional only through a component of a *non-deciding* frame; their deciding
frames rest on rigorous genus bounds.  Their deciding components ($(8,8)$ and
$(8,4)$) were re-resolved exactly with the field-free cross-check — genera
11 (16), 13 (16), 15 (16), 23 (2), all consistent — so **no provisional class remains**: the
tally of the $79{,}368$ new classes is {'dead': 12132, 'finite': 67236}.

## 2.44 Conjecture R_J: no concentration route, and a withdrawn pointer (entry 114)

*(2026-09-06; entry 114; check `a3.rj_trinomial`.)*

**The frontier, restated.**  The uniform $\omega\le2$ program (attempt E of
R.9) is blocked at Conjecture R_J (2.23, 2.27): for the $(J,1)$ boxes with
$J\ge5$, the equation $3\rho^4=\bar\ell^{2J}+2C_1\ell^{2J-1}$ in Gaussian primes
($\rho^4=\pm G_J$ for $J\equiv1\pmod3$).  Two equivalent forms worth keeping:
$$3\rho^4=2C_{2J}+p^2\ell^{2J-2},\qquad 3X^4=y^{2J}+y^{2J-1}+1\ (y=\ell/\bar\ell,\ X=\rho/\bar\pi^J),$$
the second a $\mathbb Q(i)$-point of the superelliptic curve $3X^4=y^{2J}+y^{2J-1}+1$,
of genus $3J-2$ for odd $J$ and $3J-3$ for even $J$ (a cyclic $4$-cover of the
$y$-line totally ramified at the $2J$ roots; $13$ at $J=5$, as 2.23 says); its
quadratic quotient $w^2=3(y^{2J}+y^{2J-1}+1)$, $w=3X^2$, has genus $J-1$ — the
lift from the quotient needs $3w$ to be a square, a condition that must be
retained (corrected in entry 117).  The
first gives two "sliver" identities, $\pi^{4J-2}\mid3\rho^4-\bar\ell^{2J}$ with
cofactor $2C_1$ and $\bar\pi^2\mid3\rho^4-\ell^{2J}$ with cofactor $2C_{2J-1}$;
every consequence extracted from them (norms, the discriminant of the
quadratic in $\rho^4$, primitive divisors of $U_{2J-2}$ and $V_{2J}$) is a
tautology of the norm identity $9q^4-p^{4J}=8C_1C_{2J-1}C_{2J}$.

**No concentration route.**  Every box closed by the ladder (entries 83–91)
factored its residual into coprime pieces and concentrated the prime power in
one.  For $J\not\equiv1\pmod3$ the trinomial $y^{2J}+y^{2J-1}+1$ is irreducible
over $\mathbb Q$, $\mathbb Q(i)$, $\mathbb Q(\sqrt3)$, $\mathbb Q(\sqrt{-3})$,
$\mathbb Q(\zeta_8)$, $\mathbb Q(\zeta_{12})$ and $\mathbb Q(\zeta_{24})$ (PARI,
$J=5,\dots,12$); for $J\equiv1\pmod3$ only $y^2+y+1$ splits off, and 2.27 showed
the machine cancels it.  So there is no factorization to concentrate on: R_J
needs a global method.  The effective one is Chabauty / the Mordell–Weil sieve
on the quadratic quotient $w^2=3(y^{2J}+y^{2J-1}+1)$ over $\mathbb Q(i)$, genus
$J-1\ge4$, keeping the squareclass condition $3w\in\mathbb Q(i)^{*2}$ for the
lift — Magma territory (Sage handles genus $\le2$), and per $J$; uniformity in
$J$ is the open research question.

**A withdrawn pointer.**  A memory index line had kept "attack the P1
rigidity lemma" alive as the ω ≤ 2 program's core.  That one-equation lemma
was superseded by the concentration theorem (entry 83) and Theorem A3.10
(entry 84); the pointer is corrected, and R.10's O5 now names R_J.

## 2.45 O2 with Sage: the genus-0 quotients — eight classes dead through 11a3, sixteen on one genus-2 curve (entry 115)

*(2026-09-06; entry 115; check `a3.omega3_genus0`; Magma script `compute/magma/genus0_quotients_C2.m`.)*

**The route.**  Twenty-four finite classes of the $(1,1,1)$ box have a component
(bidegree $(6,8)$, $(8,6)$ or $(6,6)$, genus $5$) with a genus-$0$ quotient $W$ by
$t\mapsto-1/t$ on one coordinate (2.36).  Sage parametrizes every $W$ over
$\mathbb Q$, $(u,v)=(u(t),v(t))$; writing $u=N/M$, the component's rational points
over the rational points of $W$ are the rational points of the hyperelliptic
curve
$$H:\ y^2=D(t)=N(t)^2+4M(t)^2,\qquad t_g=\frac{N\pm y}{2M},\ t_h=v(t),$$
of genus $5$; the exceptional set ($t=\infty$, $M=0$, the rational singular
points of $W$) is degenerate.  In $22$ classes $D$ is even, so $s=t^2$ gives a
genus-$2$ quotient $y^2=D_t(s)=C_1(s)C_2(s)$, a product of two cubics; the other
two carry a Klein four-group of Möbius involutions and become even after
$\tau=t/(t-p)$.

**Two curves.**  Up to $\mathbb Q$-isomorphism (Igusa invariants, then explicit
rescalings) the genus-$2$ quotients are exactly two curves.
*$\mathcal C_1$:* $y^2=(s^3-5s^2+11s+1)(s^3+11s^2-5s+1)$, with the involution
$s\mapsto1/s$ ($8$ classes, after $s\mapsto s/4$, $s\mapsto s/78400$ and the
$\tau$-change).  Writing $D_t=s^3Q(w)$, $w=s+1/s$, $Q=w^3+6w^2-52w+136$, its two
elliptic quotients are $Y^2=Q(w)(w\pm2)$, and $E_+$ is **11a3, rank $0$, five
torsion points**, all listed (three affine, two at infinity).  So the rational
points of $\mathcal C_1$ lie over $w\in\{2,-2,\infty\}$, i.e. $s\in\{1,-1,0,\infty\}$,
and the lifts through $t^2=s$, the parametrization and the two values of $t_g$
are all degenerate: **eight classes dead** (the first kills at genus $5$).
*$\mathcal C_2$:* $y^2=(25s^3-61s^2+43s+1)(25s^3-29s^2+11s+1)$, discriminant
$2^{62}5^423\cdot83$, at least $14$ rational points ($s\in\{-3,0,1,\tfrac13,-\tfrac15,\tfrac35\}$
and two at infinity), no Möbius involution of its six roots, Frobenius
polynomials irreducible over $\mathbb Q$ at $13,17,19,29,31,41,43,47,53$: a
presumably simple Jacobian with $\mathrm{End}=\mathbb Z$.  Sixteen classes reduce
to it ($D_t=\mu\,\mathcal C_2(\lambda s)$ or $\mu s^6\mathcal C_2(\lambda/s)$, $\mu$ a square,
$\lambda\in\{1,56644,\tfrac{42025}{1849}\}$).  The known points lift to no rational
point of any of the sixteen components, but $\mathcal C_2(\mathbb Q)$ is not known to
be complete.  With $14$ points the rank is presumably $\ge2$: Chabauty–Coleman
would need rank $\le1$, and quadratic Chabauty needs more endomorphisms than
$\mathbb Z$.  `RankBound` in Magma is the missing datum; the script is ready.

**What this shows for O2.**  The exclusion of a finite class goes through its
quotient tower: an involution with a genus-$0$ quotient turns the component
into a hyperelliptic curve, further involutions cut it to genus $2$, and a
last one to genus $1$, where rank $0$ finishes.  Where the tower stops at genus
$2$ without extra involutions, the problem is a genuine genus-$2$ rational-point
problem and the tools end.  Tally of the box: dead $1492$, finite $1452$.

## 2.46 The free-frame reduction: ω = 3 reduced to the ω = 2 theorems for a quarter of the box (goal G, first instance; entry 116)

*(2026-09-06; entry 116; `compute/omega3_freeframe.py`; check `a3.omega3_freeframe`.)*

**The observation.**  Call a class *free-frame* if some frame $f$ appears in
exactly one of its four labels, $L$.  Then $e(L)$ is the only element through
which $f$ enters the two relations
$$R_1=\varepsilon_Ae(A)+\varepsilon_Be(B)-\varepsilon_Ce(C),\qquad R_2=\varepsilon_Ae(A)-\varepsilon_Be(B)-\varepsilon_De(D).$$
*If $L=C$ or $D$*, the other relation does not contain $e(L)$ at all: it is a
signed three-term additive relation among elements of the two-frame box of
the remaining frames, exactly the relations the ladder theorems exclude —
A3.7 for shape $(1,1)$, A3.8 for $(2,1)$, A3.9 for $(3,1)$, A3.10 for $(2,2)$ (all
signed patterns, repetitions allowed, in frames of two distinct split primes).
**So every such class is dead by theorem, in every box whose two-frame shapes
are proven, before any sweep.**  *If $L=A$ or $B$*, eliminating $e(L)$ leaves the
weighted relation $2\varepsilon_Be(B)-\varepsilon_Ce(C)+\varepsilon_De(D)=0$ (a doubled
element: four terms, outside the ladder's literal scope); with the third
frame reduced to its norm it is a polynomial relation $G(t_g,t_h)=0$, and its
factors die by three mechanisms: a torsion coset $w_g^aw_h^b=\zeta$ (Lemma B of
2.41), a degenerate-only factor, or — when $G$ is linear in one ratio,
$t_g=P(t_h)/Q(t_h)$ — the **frame-condition curve** $y^2=P^2+Q^2$, which must
have a rational point for $t_g$ to be a frame ratio.  Those curves are the
killers of 2.42 (here `48a1`, `48a3`: $9T^4-14T^2+9$ for the class with
$t_2=3(T^2-1)/(2T)$, $T=\tan2\theta_3$); at rank $0$ their torsion points are
listed, each gives a pair $(t_g,t_h)$, and an admissible pair must still lift
to the free frame ($e(L)$ is then determined; its ratio must be a rational
frame-ratio root), which none does.

**On the two boxes.**  $(1,1,1)$: $444$ free-frame classes (and $28$ with a frame
in no label), all already dead by the engine; the reduction re-derives
354 of them uniformly (E: 108, T: 228, Z: 18; A3.7 for the C/D cases).
$(2,1,1)$: $11{,}912$ free-frame classes, 8130 of them Faltings-finite after entry 113;
**3900 of those are now dead** — 3576 by Theorem A3.8 alone (free label $C$ or $D$,
two-frame shape $(2,1)$), the rest by the weighted mechanisms (BE: 120, E: 204, T: 3576; curves {'48a3': 324}); 4230 weighted cases remain (frame
conditions of genus $\ge2$, or relations not linear in either ratio).  Tally of
the $79{,}368$ new classes: {'dead': 16032, 'finite': 63336}.

**Why this matters.**  It is the first reduction of ω = 3 to ω = 2 in the
program (goal G of R.9): a positive fraction of every three-frame box dies by
the two-frame theorems, uniformly and before computation, and the weighted
remainder is a *four-term* relation with a doubled element — the natural next
target for the ladder machinery (a "content-2" extension of A3.7/A3.8 would
kill the rest of the free-frame classes in every box at once).

## 2.47 The bielliptic descent completed: the sixteen classes of 2.45 are dead (entry 118)

*(2026-09-06; entry 118; `compute/qc/` (scripts, logs, sieve reports); check `a3.omega3_bielliptic`.)*

**The descent (from the review, verified).**  A rational point of
$\mathcal C_2:\ y^2=A(s)B(s)$ with a square coordinate $s=t^2$, $t=a/b$ in lowest
terms, gives $F=b^6A(a^2/b^2)$ and $G=b^6B(a^2/b^2)$, both positive since
$A(s)=s(5s-7)^2+(3s-1)^2$ and $B(s)=s(5s-3)^2+(s+1)^2$, with
$F-G=-32a^2b^2(a^2-b^2)$; so $\gcd(F,G)$ has $v_2\in\{0,3\}$ (both odd: $F\equiv G\equiv8
\pmod{16}$) and $v_5\in\{0,2\}$ ($5\mid b$: $F/25\equiv a^4(a^2-k^2)$, $G/25\equiv a^4(a^2+k^2)$
mod $5$ cannot both vanish), i.e. $\gcd\in\{1,8,25,200\}$, and $FG=\square$ forces $F$
and $G$ into one squareclass $\delta\in\{1,2\}$: $(t,z)$ with $z^2=\delta B(t^2)$ is a
rational point of the bielliptic genus-$2$ curve
$$G_\delta:\ z^2=\delta\,(25t^6-29t^4+11t^2+1).$$
Its elliptic quotients $E_1$, $E_2$ (the code's models) have rank $1$ and trivial
torsion ($\delta=1$: `1840d1`, `184b1`; $\delta=2$: `7360r1`, `1472a1`), and $J(\mathbb Q)$ is
torsion-free.

**Quadratic Chabauty.**  Bianchi–Padurariu's `QC_bielliptic` (commit `209117b`,
SageMath 10.7 in WSL) at the good ordinary primes $p=11,13$, precision $25$,
recovers exactly the known points and leaves extra $p$-adic points in most of
the $\Omega$-classes ($30$ for $G_1$, $28$ for $G_2$); their coefficients modulo $p^4$
with respect to $B_1=\pi_1^*G_1$, $B_2=\pi_2^*G_2$ are all integral, so the
integrality filter alone prunes nothing.

**The sieve on $E_1\times E_2$.**  Pushing the coefficient relation forward gives,
for a rational point $P$, $\pi_1(P)=\pi_1(P_0)+2A\,G_1$ and $\pi_2(P)=\pi_2(P_0)+2B\,G_2$
exactly, so the integers $(m_1,m_2)=(2A,2B)$ are known modulo $11^4\cdot13^4$ per
$\Omega$-class (the classes are compatible across primes; the recovered points
sit in the same class at both).  At an auxiliary prime $\ell$ of good reduction
whose reduced generators have orders divisible by $11$ or $13$, $(m_1,m_2)$ must
reduce into the image of $H(\mathbb F_\ell)$ (with $\pi_1(\infty_\pm)=O$,
$\pi_2(\infty_\pm)=(0,\pm a_0\sqrt{a_6})$) — elliptic-curve arithmetic only, no
genus-$2$ Jacobian arithmetic.  Every candidate pair dies on both curves ($19$
auxiliary primes for $G_1$, more for $G_2$) while every known point survives every
prime.  **Hence $G_1(\mathbb Q)=\{(0,\pm1),\infty_\pm\}$ and $G_2(\mathbb Q)=\{(\pm1,\pm4)\}$**,
so $t\in\{0,\pm1,\infty\}$, $s\in\{0,1,\infty\}$ on $\mathcal C_2$, and the lifts of these to
the sixteen components are degenerate (2.45): **sixteen classes dead**.  Tally of
the $(1,1,1)$ box: dead $1500$, finite $1444$.  Conditional on the correctness of
the published QC code and of `compute/qc/qc_sieve.sage`.

## 2.48 The twist audit, continued: three more sites (entry 119)

*(2026-09-06; entry 119; the reviewer's follow-up `docs/PROOF-DIRECTIONS-2026-09-06.md` §1; check `a3.omega3_twist`.)*

The entry-117 repair covered the three routines named by the review, not the
three further copies of the same step: the W-route sites of
`omega3_quotients.two_step_joint` and `omega3_quotients._w_route`, and
`omega3_unknowns._rank0_model_points`, all build the squarefree model from
`factor_list(D)[1]` alone and discard `factor_list(D)[0]`.  The reviewer's live
control: `_rank0_model_points(337(t⁴+1))` returned a complete rank-$0$ model
$t^4+1$ with $t$-values $\{0\}$, missing $t=4/3$ ($y=337/9$).  `gp_model` also
converted coefficients with `int()`, which silently truncates a rational
coefficient.  Repaired as in 2.46 (the squarefree part of the constant kept,
sign included; denominators cleared by the *square* of their lcm).

**Re-decision.**  The entry-117 re-run of the $72+36$ quotient kills could not
detect a dropped constant at these sites (it was gone before `gp_model` saw
the model).  With the repaired sites, all $108$ kills were re-decided and every
constant the sites now keep was recorded: **all $108$ still die**; $106$ never
depended on a non-square constant (the constants were $1$), and two two-step
kills had dropped the sign $-1$ in one branch and still die with the sign
kept.  No verdict changes.  The $(2,1,1)$ box has no kill through these sites
(the unknowns attack of entry 108 killed by the conjugate route and the
pullback only).  Tally unchanged: dead $1500$, finite $1444$.

**Rule (added to the audit's lessons).**  Instrument or repair the step that
discards the constant, not a routine downstream of it; a source guard in the
check now asserts that no site builds a squarefree model without
`squarefree_part(dfl[0])`.

## 2.49 The prime-column lemma (Theorem A3.PC): a uniform exclusion from the valuations alone (entry 120)

*(2026-09-06; entry 120; proposed by the independent review, `docs/PROOF-DIRECTIONS-2026-09-06.md` §2, and re-derived here; `compute/prime_column.py`; check `a3.prime_column`.)*

**Setting.**  A class of the box $p_1^{a_1}p_2^{a_2}p_3^{a_3}$ is four labels
$A,B,C,D$, each a vector $(e_1,e_2,e_3)$ with $|e_j|\le a_j$, and four signs; the
offsets of the additive quadruple are $d_X=\varepsilon_X\,e(X)$ with
$d_C=d_A+d_B$, $d_D=d_A-d_B$ (the relations $R_1,R_2$), where
$$e(X)=\prod_j p_j^{\,2(a_j-|e_{X,j}|)}\cdot\operatorname{Im}\Big(\prod_j \ell_j^{\,2e_{X,j}}\Big),\qquad \ell_j=\pi_j^2,$$
a negative exponent meaning the conjugate power (`elem_box`).  The non-split
part of the center is a common factor of all four offsets and a unit at every
$p_j$.

**Theorem A3.PC.**  *In every prime column $j$ in which some label is nonzero,
the maximum of $|e_{A,j}|,|e_{B,j}|,|e_{C,j}|,|e_{D,j}|$ is attained by at least
three of the four labels.*

*Proof.*  (Additive half.)  For an odd prime $p$ and nonzero $U,V,U+V,U-V$, the
minimum of their $p$-adic valuations is attained at least three times: if
$v(U)<v(V)$ then $v(U\pm V)=v(U)$, symmetrically if $v(U)>v(V)$; if
$v(U)=v(V)=k$ write $U=p^ku$, $V=p^kv$ with units $u,v$ — $u+v$ and $u-v$ cannot both
be divisible by $p$ (their sum $2u$ is a unit), so one of $U\pm V$ has valuation
$k$.  (Gaussian half.)  Put $z=\prod_k\ell_k^{2e_{X,k}}$.  If $e_{X,j}\neq0$, exactly one
of $z,\bar z$ is divisible by $\pi_j$ (the other frames are units at $\pi_j$, and
$\pi_j\nmid\bar\pi_j$), so $z-\bar z$ is a unit at $\pi_j$; $2i$ is a unit as well, hence
$\operatorname{Im}z=(z-\bar z)/2i$ is a unit at $\pi_j$ and, being a rational integer,
prime to $p_j$.  Therefore
$$v_{p_j}(d_X)=2(a_j-|e_{X,j}|)\ \text{ exactly when } e_{X,j}\neq0,\qquad v_{p_j}(d_X)\ge2a_j\ \text{ when } e_{X,j}=0 .$$
With $M_j=\max_X|e_{X,j}|>0$ the minimal valuation among the four offsets is
$2(a_j-M_j)$, attained exactly by the labels with $|e_{X,j}|=M_j$; the additive
half says there are at least three of them. $\square$

**Corollaries.**  (i) A frame appearing in exactly one label is impossible
outright: the free-frame reduction (2.46, entry 116) and its pending content-$2$
extension are subsumed — every free-frame class of both boxes fails the lemma.
(ii) For a primitive square $M_j=a_j$ at every split prime of the center (else
every entry is divisible by $p_j^2$), so at least three labels carry the full
exponent and at most one has a deficit.  (iii) The lemma is necessary, not
sufficient: it says nothing about the leading units, and the sixteen classes of
2.45 pass it (the bielliptic descent of 2.47 was needed).

**The census (both ledgers, from the labels alone).**  $(1,1,1)$: of the $1444$
finite classes $956$ fail and are dead; $1210$ of the $1500$ dead classes fail
as well; survivors $290$ dead $+\ 488$ finite.  $(2,1,1)$: of the $63{,}336$ finite
classes $58{,}592$ fail; $15{,}338$ of the $16{,}032$ dead classes fail; survivors
$694+4{,}744$.  The $28$ classes leaving one prime out of every label (scaled
$\omega=2$ configurations) were dead already.  Tallies: $(1,1,1)$ dead $2456$ /
finite $488$; $(2,1,1)$ dead $74{,}624$ / finite $4{,}744$.  The engine had never
carried this elementary filter: it works with the frame ratios as rational
parameters, where the residue at a particular prime is invisible.  For every
future box the lemma is applied first (`compute/prime_column.excluded`),
before any curve is built.

**Follow-through (entry 121).** Both class-decision entry points now apply the
lemma before geometry. The [survivor inventory](../RESEARCH-INVENTORY.md) is
generated from the authoritative class records. [A10](A10-cancellation-descent.md)
classifies the valuation support of the relaxed Laurent system, derives exact
unit congruences and binomial norm bounds, and records a positive unbounded
height direction for every open class. The individual norm bounds therefore
cannot finish the descent; compatibility across primes remains the target.

## 2.50 The height system (Theorem A3.HS): the unit congruences as prime inequalities (entry 123)

*(2026-09-07; entry 123; full statement, proofs and results in [A11](A11-height-system.md); `compute/height_system.py`, `compute/height_search.py`; check `a3.height_system`.)*

**Theorem A3.HS.**  *Let a class (labels $A,B,C,D$, signs) admit a solution with split primes $p_j=\pi_j\bar\pi_j$.  At every column $j$ (maximum $M$, deficit $g$ if a label is deficient), every circuit $F,G,F\pm G$ of the two additive relations gives, among the maximal labels, either a binomial $U_Y/U_X\equiv\lambda$ mod $\pi_j^{2g}$ ($\lambda\in\{\pm1,\pm2\}$) or a trinomial $\sum a_XU_X\equiv0$ mod $\pi_j^{4M}$, and these imply the exact divisibilities and inequalities*
$$p_j^{2g}\mid\operatorname{Im}A\ (\lambda=1),\quad p_j^{2g}\mid\operatorname{Re}A\ (\lambda=-1),\quad p_j^{2g}\mid N(A-\lambda\bar A)\ (|\lambda|=2),\quad \pi_j^{4M}\mid S,$$
$$2^tp_j^{2g}\le\prod_{k\ne j}p_k^{|d_k|},\qquad p_j^{g}\le3\prod_{k\ne j}p_k^{|d_k|},\qquad p_j^{2M}\le K\prod_{k\ne j}p_k^{r_k}\ (K\in\{3,4\}),$$
*with $A$ the Gaussian monomial of the exponent difference $d=f_Y-f_X$ (neither real nor imaginary), $S$ the nonzero Gaussian integer of the trinomial, binomials of different columns on the same integer multiplying, and $p_j\ge5$, $\ge17$ (C/D deficit), $\ge29$ (four maxima).*  The proofs are in A11 §2: the binomial half is $A/\bar A\equiv\lambda$ read on the rational integer $A\mp\bar A$; the trinomial half is the equilateral-triangle / collinearity argument; the lower bounds are CP.2.

**Decision.**  The inequalities are linear in $\log p_j$.  A class whose system is infeasible (an exact Farkas certificate) is impossible for every choice of primes; a class whose system caps all three primes is decided by the finite search inside the caps (A11 §3).  **Results:** $(1,1,1)$: $274$ of the $488$ open classes infeasible, $214$ unbounded; $(2,1,1)$: $2{,}732$ infeasible, $52$ capped and searched to death (caps $\le6561$), $1{,}960$ unbounded.  Tallies: $(1,1,1)$ dead $2730$ / finite $214$; $(2,1,1)$ dead $77{,}408$ / finite $1{,}960$.  These are the first kills in the record that are unconditional for all primes and independent of any curve computation beyond the prime-column lemma.  *Entry 124 (A11 §2, (T′)):* the trinomial congruence is the shadow of an exact identity $\bar\pi^{4M}W=\pi^{4M}\bar W$, so $S_1=S/\pi_j^{4M}$ has $S_1\bar G$ real and $|S_1|\ge\prod p_k^{|f_{\max}+f_{\min}|}$: the trinomial exponents drop to $2\min(f_{\max},-f_{\min})$; $44+572$ further classes infeasible; tallies $(1,1,1)$ dead $2774$ / finite $170$, $(2,1,1)$ dead $77{,}980$ / finite $1{,}388$.

## 2.51 The (3,1,1) box with the lemma and the height system first (entry 126)

*(2026-09-07; entry 126; `compute/data_omega3_box311.json.gz`; check `a3.omega3_box311`.)*

The box $p^3qr$ has $388{,}216$ classes, $290{,}064$ of them new three-frame classes (some label with $|e_1|=3$, all three frames used), the same convention as the $(2,1,1)$ campaign.  Instead of the curve engine, the two uniform exclusions ran first: **Theorem A3.PC kills $281{,}362$ ($97.0\%$)** — with a column exponent $3$ the lemma demands three labels at $|e_1|=3$, which few classes have — and **Theorem A3.HS (version 3) kills $6{,}464$ more as infeasible and $16$ by a cap (primes $\le46,140,420$) and the finite search**; only $2{,}222$ classes ($0.77\%$) reached the engine, in $44$ seconds of stage A.  The engine (entry 104's fast decision level, the $(2,1,1)$ settings) then gave: dead $16$, finite $1025$, finite$^*$ $1181$, undecided $0$, in $7.53$ CPU-hours.  Box tally: **dead $287,858$ / finite $1,025$ / finite$^*$ $1181$ / undecided $0$.**

The open classes' role words: `CBD` 112, `DBC` 112, `D*C` 96, `CBC` 88, `DBD` 88, `A**` 72, `C**` 66, `D**` 66, `ADC` 64, `ACD` 64, `C*D` 64, `C*C` 64.  The same families survive as in the two smaller boxes (C/D deficits and four-maxima columns; no class with two A/B deficits in different columns), and the exponent-$3$ column changes nothing structurally: the survivors are the classes whose labels have no zero entries where they would give strong binomials.  The $(2,1,1)$ campaign cost $44.9$ CPU-hours for $79{,}368$ classes; this one cost $7.5$ CPU-hours for $290{,}064$, all of it in the engine's $2{,}222$ classes — the uniform exclusions did the work in $44$ seconds.

## 2.52 The (1,1,1,1) box: the local method weakens with the number of primes (entry 127)

*(2026-09-07; entry 127; `compute/omega_boxes.py`, `compute/data_omega4_box1111.json.gz`; check `a3.omega4_box1111`.)*

Four split primes, every exponent $1$.  Labels are the $40$ nonzero vectors of $\{-1,0,1\}^4$ up to sign; classes are taken up to $S_4\times$ conjugations ($384$ elements), the global sign and the $A\leftrightarrow B$ swap, the same canonical form as `omega3.canon_cand` (the module reproduces the $(1,1,1)$ ledger exactly).  Only classes using all four frames.  There are $48,854$ such classes; the prime-column lemma leaves $7{,}087$, and the height system (version 3) kills $3{,}935$ of them ($55.5\%$), caps none, and leaves $3{,}152$ open.

The comparison with three frames decides path 5 of R.13.  The $(1,1,1)$ box's $2{,}916$ three-frame classes leave $750$ lemma survivors, of which the height system kills $576$ ($76.8\%$).  At four frames the kill rate drops to $55.5\%$, and the three-frame regularity "no two A/B deficits in different columns" fails: $801$ open classes have two A/B deficits, $94$ three, $1$ four.  The reason is structural: a binomial bound $p_j^{2g}\le\prod_{k\ne j}p_k^{|d_k|}$ has one more factor on the right for each extra prime, so a recession direction is easier to find.  **The local method weakens with $\omega$.**  Consequences: a uniform proof cannot come from the height system alone for large $\omega$; the role-word theorem (path 1) must be sought in a different form (what the survivors *share* as $\omega$ grows, rather than an exclusion by counting deficits); and $\omega\ge4$ is where the analytic dimension of the solution set grows ($\omega-2$), so it is also where a solution could hide from every curve method.

## 2.53 The (1,1,1,1,1) box and the trend: the local method decays with the number of primes (entry 128)

*(2026-09-07; entry 128; `compute/omega_boxes.py` (the column canonical form), `compute/data_omega5_box11111.json.gz`; check `a3.omega5_box11111`.)*

A class of the all-ones box with $N$ frames is the $4\times N$ matrix of signed exponent vectors $w_X=\varepsilon_Xe_X$ (the relations depend only on $Z_X=\prod_j\rho_j^{2w_{X,j}}$); the frame group permutes and sign-flips its columns, so the canonical form is the sorted tuple of sign-normalised columns, minimised over the global sign and the $A\leftrightarrow B$ swap — linear in $N$, and it reproduces the $(1,1,1)$ and $(1,1,1,1)$ ledgers as identical key sets.  Five frames: $497,166$ five-frame classes; the lemma leaves $44{,}882$ (it is very selective at five columns: $1$ raw quadruple in $13$); the height system (version 3) kills $15{,}972$ of them, caps none, leaves $28{,}910$ open.

| frames | classes | lemma survivors | killed by the height system | open | kill rate |
|---:|---:|---:|---:|---:|---:|
| 3 | 2,916 | 750 | 576 | 174 | 76.8% |
| 4 | 48,854 | 7,087 | 3,935 | 3,152 | 55.5% |
| 5 | 497,166 | 44,882 | 15,972 | 28,910 | 35.6% |

Open classes at five frames carry up to five A/B deficits ($668$ with four, $10$ with five) and up to five four-maxima columns ($168$ with all five).  **The local method decays with $\omega$**, as the structure predicts: each binomial bound $p_j^{2g}\le\prod_{k\ne j}p_k^{|d_k|}$ gains a factor per extra prime.  For the plan (R.13) this settles path 5: no uniform proof can come from the height system as $\omega$ grows, so the theory must find what the open classes have in common that the local method does not see — or a descent that reduces $\omega$.

## 2.54 Orientation: what the open classes share (entry 129; Theorem A3.OR and Theorem T1)

*(2026-09-07; entry 129; [A12](A12-orientation.md); `compute/orientation.py`, `compute/data_orientation.json`; check `a3.orientation`.)*

For an all-ones box the height system's rows depend on the class only through the **flip pattern** of the signed exponent vectors $w_X=\varepsilon_Xe_X$: for two labels nonzero at $p_j$, the exponent of $p_k$ in the binomial row is $2$ where the pair's relative orientation at $p_k$ differs from that at $p_j$, $1$ where exactly one of them vanishes at $p_k$, $0$ where they agree; for three labels of a circuit the trinomial row puts $p_k^2$ on the *left* where the three keep their mutual orientations, on the right where two flip (Theorem A3.OR, verified against every row on all $52{,}719$ lemma survivors of the three all-ones boxes).  **Theorem T1:** three labels of a circuit, nonzero at $p_j$ and never flipping relative to one another at any other prime, kill the class ($p_j^2\prod p_k^2\le K\le4$) — uniform in the number of primes and in the shape.  T1 explains $212/576$, $1340/3935$, $5022/15972$ of the local kills at $3/4/5$ frames and $1000/3304$ in the $(2,1,1)$ campaign, and fires on no open class of any campaign; its corollary (no pair of labels ever flips $\Rightarrow$ dead) is the reason the no-flip classes were always dead.

**What the open classes share:** orientation genericity — every circuit flips relative to every prime, every pair flips or is compensated by one-zero columns (classes in which every pair flips are open $99\%$ of the time), and the flip pattern admits a feasible hierarchy of prime sizes: about a third of the open classes allow all primes comparable, the rest force a spread, $2499$ five-frame classes forcing a ratio $\ge125$ and some above $10^9$.  Nothing else is visible at first order; the residual local information is the exact value of the congruences, which is prime-specific.  R.13 path 1 is answered in this form.

## 2.55 The towers' bielliptic models: twelve more classes dead (entry 130; R.13 path 2)

*(2026-09-07; entry 130; `compute/qc/qc_general.sage`, `compute/qc/general_F1.{json,log}`; check `a3.towers_bielliptic`.)*

Of the $170$ open $(1,1,1)$ classes, $32$ carry tower records: a frame whose component is quadratic in one ratio has the level-0 hyperelliptic model $y^2=D(t)$ in the other ratio.  Recomputing $D$ exactly: **eight** classes have $D=G_1=25t^6-29t^4+11t^2+1$ (or $t^6G_1(1/t)$), the curve of 2.47, whose rational points are $(0,\pm1)$ and $\infty_\pm$; **four** have $D=F_1=t^6+11t^4-5t^2+1$ (or its reciprocal), a bielliptic genus-$2$ curve with elliptic quotients `352b1`, `352c1`, both of rank $1$ and trivial torsion.  For $F_1$ the method of 2.47 was rerun (Bianchi–Padurariu's `QC_bielliptic` at the two smallest good ordinary primes, then the Mordell–Weil sieve on $E_1\times E_2$): every candidate eliminated, the known points surviving as controls, so $F_1(\mathbb Q)=\{(0 : -1 : 1), (0 : 1 : 0), (0 : 1 : 1)\}$.  Every rational point of either curve has ratio $t\in\{0,\infty\}$, degenerate; the component has no admissible point, the frame is dead, and a dead frame kills the class.  Tally: dead $2786$ / finite $158$.

The tower route of entry 100 had stopped at these curves because their elliptic quotients have positive rank; the bielliptic descent of 2.47 is what decides them.  The remaining $20$ tower classes have genus-$3$ models ($y^2=$ an even octic) whose genus-$2$ quotient is not bielliptic by the tower's test, and $8$ have a $(6,6)$ component with no hyperelliptic model: these need a rank bound on a genus-$2$ Jacobian (Magma) or a new idea.

## 2.56 The general bielliptic test; the genus-2 curves of the octic towers; four classes dead through the LMFDB (entry 131; R.13 path 2)

*(2026-09-07; entry 131; `compute/qc/bielliptic_test.sage`, `compute/bielliptic.py`, `compute/qc/g2_cc_points.sage`, `compute/qc/g2_iso.sage`, `compute/qc/magma_towers131.m`; check `a3.towers_genus2`.)*

**The test.**  A genus-$2$ curve $y^2=f(x)$ is bielliptic iff a Möbius involution $\sigma$ of $\mathbb P^1$ permutes its six branch points.  Such a $\sigma$ fixes no branch point: a non-hyperelliptic involution $\tilde\sigma$ of the curve fixing a Weierstrass point would, together with the hyperelliptic involution, give a Klein four-group in the stabilizer of that point, which acts faithfully on the tangent line and is therefore cyclic.  So the six points split into three swapped pairs, a perfect matching, and the Möbius map interchanging two given pairs is determined by them (three linear conditions on its four entries) and is an involution.  The test builds the map exactly over $\bar{\mathbb Q}$ for each of the $15$ matchings and checks the third pair; a rational $\sigma=(ax+b)/(cx-a)$ with rational fixed points ($a^2+bc$ a square) is moved to $x\mapsto -x$, giving the even form $y^2=g(x^2)$ of 2.47 with its quotients $E_1,E_2$.  Five controls behave as expected ($F_1$, $G_1$, $y^2=x^5+x$ with six involutions, $y^2=x^6+x^3+8$ with $x\mapsto 2/x$, $y^2=x^5-x$).

**The octic towers.**  The twelve open classes with genus-$3$ models $y^2=Q(t^2)$ have the odd quotients $w^2=uQ(u)$: three curves up to $u\mapsto 1/u$, $C_a\colon w^2=25u^5-36u^4-18u^3+44u^2+u$, $C_b\colon w^2=25u^5-4u^4-18u^3+12u^2+u$ (classes $0$–$7$, one in each frame) and $C_c\colon w^2=u^5-4u^4+6u^3+12u^2+u$ (both frames of classes $9,10,13,14$).  **None is bielliptic** — no matching admits an involution — so the $E_1\times E_2$ quadratic Chabauty route is closed here; their Frobenius polynomials at small primes are irreducible, so the Jacobians are simple over $\mathbb Q$ (not necessarily absolutely simple: a failed bielliptic test does not exclude elliptic maps of higher degree — the review's correction, entry 135).

**$C_c$ through the LMFDB.**  $C_c$ has minimal discriminant $-2^{14}\cdot 11$ and is $\mathbb Q$-isomorphic to the LMFDB curve `1408.b.180224.2`, $y^2=2x^5-4x^3-x^2+2x+1$, by $(x,y)\mapsto\big((x-1)/(-x-1),\,2y/(-x-1)^3\big)$ (verified exactly).  Its Jacobian has rank $0$ by $2$-descent (two-Selmer rank $2$, equal to the $2$-torsion rank; `mw_rank_proved`), torsion $\mathbb Z/2\times\mathbb Z/8$.  Independently, $\gcd_p\#J(\mathbb F_p)=16$ and the known points generate $16$ classes, so $J(\mathbb Q)$ is exactly those; the classes of the form $[P-\infty]$ are the ones whose reduced Mumford representative has degree $\le 1$, and enumerating the $16$ gives $C_c(\mathbb Q)=\{\infty,(0,0),(-1,0),(1,\pm4)\}$.  Every $u$ lies in $\{0,-1,1,\infty\}$, so $t=\sqrt u$ is degenerate, the frame is dead, and the four classes die.  Conditional on the LMFDB's $2$-descent (Magma) and Sage's Jacobian arithmetic.  Tally $(1,1,1)$: dead $2790$, finite $154$.

**$C_a$, $C_b$.**  The classes of $(1,4)$ and $(-1/5,\cdot)$ have infinite order (their orders in $J(\mathbb F_p)$ vary with $p$), so both Jacobians have rank $\ge1$; neither curve is in the LMFDB.  A $2$-descent rank bound and, for rank $1$, Chabauty with the Mordell–Weil sieve are Magma computations: `compute/qc/magma_towers131.m` is the paste-ready script.  The eight remaining tower classes have $(6,6)$ pullbacks of genus $25$, beyond every curve method here.

## 2.57 The octic towers closed by Magma: $C_a$, $C_b$ have rank $1$ and seven rational points (entry 132; R.13 path 2)

*(2026-09-07; entry 132; `compute/qc/magma_towers131.m`, `compute/qc/magma_towers131.out.txt`, `compute/genus2_counts.py`; check `a3.towers_magma`.)*

The user ran the script of 2.56 in the Magma online calculator.  For both curves, $C_a\colon w^2=25u^5-36u^4-18u^3+44u^2+u$ and $C_b\colon w^2=25u^5-4u^4-18u^3+12u^2+u$: rank bounds $1,1$ (points below, $2$-descent above), torsion $\mathbb Z/2\times\mathbb Z/4$ (matching $\gcd_p\#J(\mathbb F_p)=8$, recomputed here from point counts over $\mathbb F_p$ and $\mathbb F_{p^2}$), Mordell–Weil group $\mathbb Z/2\times\mathbb Z/4\times\mathbb Z$ **proved**, free generator $[(1,-4)-\infty]$, and Chabauty with the Mordell–Weil sieve returns exactly the seven known points $\infty,(0,0),(-1,0),(1,\pm4),(-1/5,\pm32/25)$ resp. $(-1/5,\pm16/25)$; the completeness condition (the index of $\langle P\rangle+\text{torsion}$ in $J(\mathbb Q)$ coprime to $\{3,23\}$ resp. $\{7,17\}$) holds with index $1$ because the group is proved.

A rational point $(t,y)$ of the frame's genus-$3$ curve $y^2=Q(t^2)$ maps to $(u,w)=(t^2,ty)$ on the odd quotient, so $t$ is a square root of one of the seven $u$-values: $u\in\{0,\pm1,\infty\}$ gives a degenerate ratio and $u=-1/5$ is not a square.  Both frames of each of the eight open octic classes carry one of the two curves, so both frames are dead and the classes die: tally $(1,1,1)$ dead $2798$, finite $146$.  Conditional on Magma, as 2.47/2.55 are on the QC code; everything else is re-verified exactly.  The towers are now closed except for the eight genus-$25$ $(6,6)$ classes; the other $138$ open classes have no component quadratic in a ratio.

## 2.58 The binomial square root (Theorem A3.SQ): the height system's binomial rows double their exponent (entry 134; R.13 path 3)

*(2026-09-08; entry 134; `compute/height_system.py` version 4, `compute/hierarchy.py`, `compute/data_hierarchy.json.gz`; check `a3.square_root`.)*

**Theorem A3.SQ.**  *At a deficient column $j$ (deficit $g$) let a binomial circuit with $|\lambda|=1$ give $p_j^{2g}\mid\operatorname{Im}A$ ($\lambda=1$) or $p_j^{2g}\mid\operatorname{Re}A$ ($\lambda=-1$), $A=\prod_{k\ne j}\pi_k^{2d_k}$ (conjugates for $d_k<0$), $P=|A|=\prod p_k^{|d_k|}$.  Then $p_j^{4g}<P$ ($\lambda=1$), $p_j^{4g}\le 2P$ ($\lambda=-1$), and $p_j^{8g}\le 4P$ when $\lambda=1$ and every $d_k$ is even.*

*Proof.*  $A=B^2$ with $B=\prod\pi_k^{d_k}$.  $B$ is primitive: a rational prime dividing $B$ would be $2$ (but $B$ has odd norm), a prime $\equiv3\pmod4$ (a Gaussian prime not among the $\pi_k$), or $p_k=\pi_k\bar\pi_k$ (but only one of $\pi_k,\bar\pi_k$ divides $B$).  Hence $\gcd(\operatorname{Re}B,\operatorname{Im}B)=1$; both are nonzero, since $B$ real or imaginary forces $B/\bar B=\pm1$, i.e. every $d_k=0$ by unique factorisation; and $\operatorname{Re}B\ne\pm\operatorname{Im}B$, since $(1+i)\nmid B$.  Now $\operatorname{Im}A=2\operatorname{Re}B\operatorname{Im}B$ and $\operatorname{Re}A=(\operatorname{Re}B-\operatorname{Im}B)(\operatorname{Re}B+\operatorname{Im}B)$, the second pair with gcd dividing $2$; the odd prime power $p_j^{2g}$ divides exactly one factor, and $|\operatorname{Re}B|,|\operatorname{Im}B|<|B|=\sqrt P$, $|\operatorname{Re}B\pm\operatorname{Im}B|\le\sqrt2|B|$.  If every $d_k$ is even, $B=C^2$ with $C$ primitive, $\operatorname{Im}A=4(\operatorname{Re}C-\operatorname{Im}C)(\operatorname{Re}C+\operatorname{Im}C)\operatorname{Re}C\operatorname{Im}C$, four factors pairwise coprime up to $2$, each $\le\sqrt2|C|=\sqrt2P^{1/4}$. $\square$

A11's (B1) was $2^tp_j^{2g}\le P$: the exponent of the deficient prime doubles.  The coupling rows (C), the trinomial rows (T′) and the $|\lambda|=2$ rows are unchanged.  **Version 4** of the height system carries the new rows (squared to keep the constants rational); the certificates of versions 1–3 remain valid, and `verify_certificate` honours the recorded version.

**How it was found.**  Path 3 began with the hierarchical open classes.  `compute/hierarchy.py` computes the forced ratio and its binding rows, the *rigid* rows — those whose slack is bounded on the feasible region, so that the divisibility behind the row becomes an exact equation with finitely many constants — and the *frame divisibilities* (binomials whose $d$ is supported on one column $k$: $p_j^{2g}$ divides a component $c_k$, $s_k$, $c_k\pm s_k$ of the frame of $p_k$).  Rigid rows are common: $94/146$, $649/3152$, $2312/28910$ open classes have at least one at three, four, five frames (the first three-frame class examined had none, its recession cone being full-dimensional).  In the five-frame class with forced ratio $4.3\cdot10^9$ the rigid row $p_4^2\mid c_0^2-s_0^2$ with $p_0\le2p_4^2$ forces $c_0^2-s_0^2=\pm p_4^2$, so $(c_0-s_0,c_0+s_0)=(1,p_4^2)$ and $p_0=(p_4^4+1)/2>2p_4^2$: impossible.  The general statement is the theorem; rigidity was only the lens.

**The harvest** (every open class of every campaign re-decided with version 4; exact certificates, each shown new by the feasibility of version 3):

| Box | Open before | Infeasible (dead) | Open after |
|---|---:|---:|---:|
| $(1,1,1)$ | 146 | 118 | 28 |
| $(2,1,1)$ | 1,388 | 1,092 | 296 |
| $(3,1,1)$ | 1,025 | 761 | 264 |
| $(1,1,1,1)$ | 3,152 | 2,021 | 1,131 |
| $(1,1,1,1,1)$ | 28,910 | 10,472 | 18,438 |

Tallies: $(1,1,1)$ dead $2916$ / finite $28$; $(2,1,1)$ dead $79{,}072$ / finite $296$; four frames dead $5,956$ / open $1,131$; five frames dead $26,444$ / open $18,438$.  In the $(1,1,1)$ box every survivor has two four-maxima columns (only trinomial rows there), and most survivors elsewhere do ($212/296$, $244/264$, $949/1131$ at $(2,1,1)$, $(3,1,1)$, four frames), so the next uniform lever is a trinomial sharpening.  The eight genus-$25$ tower classes are dead; the $28$ open $(1,1,1)$ classes have undecided components of bidegree $(8,8)$ (16) and $(4,4)$ (12).

**The descent formulation (recorded).**  Peeling $p=p_j$ from $Y_c=\sum_Xc_Xz_X^2$: with $y_X=z_X^2/\pi^{4w_{X,j}}$ and $P_\pm,P_0$ the circuit sums over the labels of orientation $\pm1,0$ at $p_j$, $Y=\pi^4P_++\bar\pi^4P_-+p^2P_0$ and $Y-\bar Y=\pi^4W-\bar\pi^4\bar W+p^2(P_0-\bar P_0)$, $W=P_+-\bar P_-$ (identities, machine-checked on random frames).  For a solution at a four-maxima column $W=r\bar\pi^4$ with $r\in\mathbb Z\setminus\{0\}$: the configuration on the other $N-1$ primes, its negatively oriented labels conjugated and negated, has circuit sums $r_F\bar\pi^4$, $r_G\bar\pi^4$ — a *twisted* configuration, and eliminating $\pi$ gives $\operatorname{Im}(W_F\bar W_G)=0$ on the smaller frames.  At a deficient column, $\bar\pi^2\mid W$ and $\operatorname{Im}(\pi^2W_1)=-c_E\operatorname{Im}(y_E)$ exactly ($W_1=W/\bar\pi^2$), the second-order equation A11 §4 left unused.  Peeling a second prime re-inserts the first (the twist $\bar\pi^4=(\bar\pi^2)^2$ distributes over the labels by the second prime's orientations), so the naive descent in the number of primes stops after one step; what remains is the elimination — the class curve of the smaller frames, path 2.

## 2.59 The symmetry tower of the 28 survivors (entry 135; the review's technique carried forward)

*(2026-09-08; entry 135; `compute/data_joint_quotients.json`, `compute/qc/magma_tower135.m`; check `a3.joint_quotients`.)*

Every surviving $(1,1,1)$ class has one undecided component $\Phi(g,h)$ of bidegree $(8,8)$ (sixteen classes) or $(4,4)$ (twelve), and every $\Phi$ is invariant under the joint sign change $(g,h)\mapsto(-g,-h)$: as a polynomial for the $(8,8)$ components (every monomial of even total degree), up to sign for the $(4,4)$ ones.  The quotient by that involution is the curve $Q(x,y)=0$ with $x=g^2$, $y=gh$ ($Q(g^2,gh)=g^{2s}\Phi$, or $g^{2s+1}\Phi$ in the odd case): bidegree $(6,8)$ and genus $10$ for the $(8,8)$ components, bidegree $(3,4)$ and genus $4$ for the $(4,4)$ ones (Sage).  Twenty of the $Q$ are invariant under the double inversion $(x,y)\mapsto(1/x,1/y)$, from $(g,h)\mapsto(1/g,1/h)$; the second quotient is the image of $(u,v)=(x+1/x,\,y+1/y)$, a map of degree $2$ on the curve, and its equation is the repeated factor of the resultant eliminating $x,y$ from $Q$, $x^2-ux+1$, $y^2-vy+1$: genus $4$ for the sixteen $(8,8)$ classes, **genus $2$ for classes $2918$–$2921$**.  The eight remaining $(4,4)$ classes ($2914$–$2917$, $2940$–$2943$) have no inversion symmetry.

| Survivors | Component | Joint-sign quotient | Double-inversion quotient |
|---|---|---|---|
| 16 classes | $(8,8)$ | genus 10 | genus 4 |
| 4 classes ($2918$–$2921$) | $(4,4)$ | genus 4 | genus 2 |
| 8 classes | $(4,4)$ | genus 4 | none |

A rational point of a quotient bears on the class only through its lifts: $u^2-4$ and $v^2-4$ must be rational squares (then $x$, $y$ are rational), $x$ must be a rational square (then $g$, $h=y/g$ are rational), and $g,h$ must be admissible frame ratios (not $0,\pm1,\infty$).  Sage's function fields over $\mathbb Q$ give no canonical divisor for a plane curve, so the hyperelliptic models of the four genus-$2$ curves, their rank bounds and Chabauty, and the automorphism groups and hyperellipticity of the twenty-four genus-$4$ curves are left to the Magma calculator (`compute/qc/magma_tower135.m`, one block at a time); the lift analysis from the returned points is done in Python.  No verdict changes here.  The same tower should be run on the $296$ and $264$ survivors of the $(2,1,1)$ and $(3,1,1)$ campaigns: if the endpoints are the same few curves, the atlas question of R.15 has a positive first answer.

## 2.60 The symmetry-tower kills: twelve more classes dead through 80a1 and 528j2 (entry 136)

*(2026-09-08; entry 136; `compute/data_symmetry_tower.json`, `compute/qc/magma_tower136.m`; check `a3.symmetry_tower`.)*

Every surviving component is invariant under a group of sign-and-inversion maps $(g,h)\mapsto(\pm g^{\pm1},\pm h^{\pm1})$: of order $8$, generated by $s=(-g,-h)$, $r_g=(-1/g,h)$, $r_h=(g,-1/h)$, for the sixteen $(8,8)$ components and for classes $2918$–$2921$; of order $4$, $\langle s,r_g\rangle$, for the other eight $(4,4)$ classes.  Quotients by subgroups reach elliptic curves, and two of them have rank $0$:

- **Classes $2918$–$2921$.**  $C/\langle r_g,r_h\rangle$ in $u=g-1/g$, $v=h-1/h$ (the repeated factor of the resultant with $g^2-ug-1$, $h^2-vh-1$) is a $(2,2)$ curve of genus $1$ with Jacobian **80a1** (rank $0$, torsion $\mathbb Z/4$).  Its four rational points are $(0,0)$, $(\infty,0)$, $(0,\infty)$, $(\infty,\infty)$ (the curve has a rational point, so it has exactly $\#E(\mathbb Q)$ of them), and $u\in\{0,\infty\}$ forces $g\in\{\pm1,0,\infty\}$: degenerate.  The frame's only component has no admissible point: dead.
- **Classes $2914$–$2917$, $2940$–$2943$.**  $C/\langle r_g\rangle$ is quadratic in $u$ with discriminant $16(h^8-13h^6+36h^4-13h^2+1)$, one hyperelliptic curve of genus $3$ shared by all eight; its quotient by $h\mapsto1/h$ ($w=h+1/h$) is $Y^2=w^4-17w^2+64$, the curve **528j2** (rank $0$, torsion $\mathbb Z/4$), whose four rational points are $(0,\pm8)$ and the two at infinity.  $w=0$ has no rational $h$, and $w=\infty$ forces $h\in\{0,\infty\}$: every rational point of $C/\langle r_g\rangle$ has $h$ degenerate.  Dead.

Twelve classes dead; the $(1,1,1)$ tally is dead $2928$ / finite $16$.  The sixteen $(8,8)$ classes reach **666d1** (rank $1$) through a genus-$3$ curve $E_3$ of bidegree $(4,4)$; their other order-$4$ quotients have genus $4$.  $E_3$'s Jacobian (hyperellipticity, rank) is the question left to the Magma calculator (`magma_tower136.m`, block B).  The ranks are PARI $2$-descents; the identities are re-derived exactly by the check.  80a1 is one of the fifteen killers of entry 112.

## 2.61 The symmetry tower on the shape survivors (entry 137; `compute/symmetry_tower.py`)

*(2026-09-08; entry 137; `compute/data_symmetry_tower_shapes.json`; check `a3.symmetry_tower_shapes`.)*

The module makes 2.59–2.60 systematic.  For a class's elimination component $\Phi(g,h)$: the symmetry group among the sixteen maps $(g,h)\mapsto(\pm g^{\pm1},\pm h^{\pm1})$; the quotient steps — the joint sign change ($x=g^2$, $y=gh$), single and double inversions ($u=a+s/a$, the repeated factor of the resultant with $a^2-ua+s$, of multiplicity equal to the fibre), monomial coordinate changes to a model quadratic in one variable ($y^2=D(o)$, the square part of $D$ absorbed into $y$, never a twist), and the even and reciprocal quotients of that model; elliptic endpoints decided by PARI (rank bounds, torsion, the points, completeness); genus-2 endpoints matched to $G_1,F_1,C_a,C_b,C_c$ up to $o\mapsto\lambda x^{\pm1}$ and a square scaling; every endpoint point lifted back to $(g,h)$ exactly.  A class dies when the frame's other components are dead, no univariate factor is live, and an endpoint is complete with no admissible lift.

| Campaign | Open before | Dead | Open after | Endpoints of the kills |
|---|---:|---:|---:|---|
| $(2,1,1)$ | 296 | 54 | 242 | inversion g (s=-1) -> reciprocal: rank-0 elliptic, torsion 4 (28); inversion g (s=-1): G1 (8); inversion g (s=-1) -> joint: C_a (4); inversion g (s=-1): F1 (4); joint: C_a (4); joint: C_b (4); inversion g (s=-1) -> joint: C_c (2) |
| $(3,1,1)$ | 264 | 44 | 220 | inversion g (s=-1) -> reciprocal: rank-0 elliptic, torsion 4 (28); double inversion (-1,-1) -> even: rank-0 elliptic, torsion 6 (8); joint: C_a (4); joint: C_b (4) |

The endpoints are the curves of the $(1,1,1)$ box again — $G_1$, $F_1$, $C_a$, $C_b$, $C_c$, the 528j2-type reciprocal quotients — and the rank-$1$ curves 88a1, 92b1, 664a1, 352b1/c1, 184b1, 1840d1, 2656d1, 13280a1: the atlas recurs across shapes.  The open classes sit over positive-rank elliptic curves or over unidentified genus-$2$ and genus-$3$ curves (palindromic sextics with a reciprocal involution, for the general bielliptic test and the LMFDB), or have components too large for the quotient search.

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
