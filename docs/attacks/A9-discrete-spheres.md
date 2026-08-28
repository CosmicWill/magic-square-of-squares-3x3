# A9 — The discrete-sphere model

**Status:** §1 dictionary **PROVEN** (exact identities, machine-checked
by `a9.dictionary`); §2 tension **quantified** (`a9.tension`); §3 the
class-group program (A9-T1) has four layers landed — the
Eisenstein anchor / Gauss map / slice confinement; the gluing law
with its **coherence obstruction** (Theorem A9.3: necessity proven,
bite measured); the **three-sieve pair desert**
(positivity + coherence + representation kill every ordered congrua
pair for every center $m \le 1200$); and the **anatomy of the
kills** — Gauss composition implemented, the principal genus
theorem machine-verified, a validated local criterion certifying
21 of the 57 killed lines as local and **36 as strictly beyond
every character (inside cosets of $\mathrm{Cl}^2$)**.
Verification: `python3 -m verify --only a9`.

## 0. Origin

The owner's geometric picture: the problem is a configuration of
spheres in 9-dimensional space, with solutions the integer points
where they meet, and the all-equal square the point where every
sphere "crosses each number line at the same spot". This document
makes that picture exact and connects it to the classical theory of
**lattice points on spheres** — the "non-solid sphere"
$$\mathcal{S}(n) \;=\; \{(x,y,z) \in \mathbb{Z}^3 :
x^2 + y^2 + z^2 = n\},$$
a finite set with deep arithmetic structure (Gauss: sizes are
class-number-like; Gauss/Venkov: the points are organized by the
class group of $\mathbb{Q}(\sqrt{-n})$ via quaternions; Duke,
after Linnik: the normalized points equidistribute as
$n \to \infty$). *(Classical background, PROVEN-CLASSICAL; used
descriptively — every computed claim below is first-party.)*

## 1. The dictionary (PROVEN, `a9.dictionary`)

Write a magic square of squares in root coordinates, center entry
$m^2$. Every line of a $3\times3$ magic square sums to $3\,\times$
center, so **each of the 8 lines is a point of the single discrete
sphere $\mathcal{S}(3m^2)$**, and the square is 8 such points glued
by shared coordinates (the center root lies on 4 of them, corner
roots on 3, edge roots on 2). Exact facts, verified for every
$m \le 200$ (`compute/discrete_spheres.py`):

- **The trivial point.** $(m, m, m) \in \mathcal{S}(3m^2)$ always —
  the all-equal square: precisely the owner's "same spot on every
  number line" observation.
- **The $m$-slice is A3.** The through-center lines are the sphere
  points with a coordinate equal to $m$, and they biject with the
  congrua set $D(m)$ of
  [A3](A3-simultaneous-congrua.md) via
  $$e^2 + f^2 = m^2,\ d = 2ef \;\longleftrightarrow\;
  (|e-f|,\; m,\; e+f), \qquad
  (e{-}f)^2 + m^2 + (e{+}f)^2 = 3m^2 .$$
  The A3 attack *is* the discrete-circle slice of this sphere: an
  MSS3 with center $m^2$ needs an additive quadruple
  $u, v, u{+}v, u{-}v \in D(m)$, i.e. four slice points in
  arithmetic relation.
- **Parity shadow.** For odd $m$, $3m^2 \equiv 3 \pmod 8$, and every
  three-square representation of a number $\equiv 3 \pmod 8$ has all
  coordinates odd (exhaustive residue check) — the sphere-side
  source of the F4 parity facts.
- **Nodes, and the magic/oblique split.** A subtlety the machine
  check enforces: the square's 8 **magic lines** are the *zero-sum*
  triples of Lucas labels, while the 8 **triple points** of the
  arrangement (where the 256 nodes of $X$ live) are the
  *grid-collinear* triples — and exactly **four** of those are magic
  lines (the $\{a{=}0\}$, $\{b{=}0\}$ and two diagonal pencils,
  i.e. the points $A_0, B_0, D_\pm$: vanishing there collapses a
  whole sphere condition), while the outer four ($A_\pm, B_\pm$) are
  *oblique* triples whose three entries belong to three different
  magic lines. The A8 theorems read: *any 1-parameter family of
  solutions passes through $\ge 3$ of these eight degeneration
  points* — and, pleasingly, the four sphere-collapse points
  $\{A_0, B_0, D_\pm\}$ are exactly the four triple points on the
  central entry line, the set that organizes the special subspaces
  of the A8 §8 classification.

## 2. The tension, quantified (`a9.tension`)

The discrete-sphere view and the surface view pull against each
other, and the table makes it numeric. As $m$ grows the sphere gets
RICH — $|\mathcal{S}(3m^2)|$ reaches 64 already by $m \le 200$, and
grows on average like a class number (Duke: the points spread
uniformly) — so naive counting heuristics predict compatible
configurations should appear. Yet the compatibility ladder on the
slice stays EMPTY: for all $m \le 200$ (and A3's far larger desert
bounds), the additive-triple and additive-quadruple counts are
$$L_3 = L_4 = 0$$
— abundance without compatibility. The surface side explains the
scarcity structurally ($X$ is of general type, quasi-hyperbolic,
with every curve forced through the sphere-degeneration points); the
Bombieri–Lang philosophy predicts at most finitely many
nondegenerate points, against the heuristic's optimism. Any
resolution of the problem must reconcile exactly these two forces.

## 3. The class-group layer (A9-T1, first results)

(`compute/sphere_classes.py`; checks `a9.class_numbers`,
`a9.gauss_map`.)

**The Eisenstein anchor (PROVEN for the range).** Since
$n = 3m^2$, the binary quadratic theory of every sphere in the
vertical family lives in the *single field* $\mathbb{Q}(\sqrt{-3})$:
the relevant order is $\mathbb{Z}[m\sqrt{-3}]$, of discriminant
$-3m^2$ and conductor $m$, with ring class number
$$h(-3m^2) \;=\; \frac{m}{3}\prod_{p \mid m}
\Bigl(1 - \frac{\chi_{-3}(p)}{p}\Bigr) \quad (m > 1), \qquad
h(-3) = 1,$$
verified against an independent primitive-reduced-form enumeration
for every valid $m < 60$.

**The counting identity (VERIFIED on the sample; classical).** The
primitive sphere sizes are exactly Eisenstein class numbers:
$$r_3^*(3m^2) \;=\; 24\,h(-3m^2) \qquad (m > 1;\ 8 = 24/3\ \text{at}
\ m = 1),$$
checked for $m \in \{1, 5, 9, 13, 17, 25, 29, 33, 37, 41, 65, 85,
105\}$ — the sphere's size *is* a class number, as Gauss's theory
demands.

**The Gauss map, implemented.** Each primitive point $v$ maps to the
class of the binary form on the orthogonal lattice $v^\perp \cap
\mathbb{Z}^3$ (determinant $n$ certified by saturation; even Gram
convention, discriminant $-4n$) — the Aka–Einsiedler–Shapira object.
Measured structure: fibers are **uniform** (48 generically, the
signed-permutation orbit; torsor behavior), and the hit-class count
tracks $h$ up to the expected 2-to-1 conflations.

**Slice concentration (measured — the first class-group constraint
on configurations).** The primitive through-center points (the A3
congrua slice) are nonempty iff every odd prime factor of $m$ is
$\equiv 1 \pmod 4$ (the hypotenuse condition), and then they number
$$48 \cdot 2^{\omega_1 - 1} \ \text{points in at most}\ 2^{\omega_1}
\ \text{classes} \qquad (\omega_1 = \#\{p \mid m : p \equiv 1 \bmod
4\}),$$
while the ambient class number grows linearly in $m$: **the
through-center lines of any magic square are exponentially
class-confined**, the outer lines are not. A magic configuration
needs its four through-center points inside this thin class window
*and* its four outer points glued to them — which the next layer
turns into an obstruction.

### The gluing law and the coherence obstruction (second layer)

(`compute/sphere_gluing.py`; checks `a9.gluing_law`,
`a9.coherence`.)

**Lemma A9.1 (the gluing-representation law; PROVEN — one-line
proof, machine-verified on 960 points).** For $v = (x,y,z)$ with
$|v|^2 = n$, the cross-vectors $(0,-z,y),\ (z,0,-x),\ (-y,x,0)$ lie
in $v^\perp \cap \mathbb{Z}^3$ with norms $n - x^2$, $n - y^2$,
$n - z^2$. Hence **the Gauss class of every magic line represents
the co-norm $3m^2 - e$ of each of its three entries** — the entries
of a line are visible inside its class. (This is how gluing reaches
composition: shared entries force shared represented values.)

**Lemma A9.4 (even lattices; PROVEN).** All points of
$\mathcal{S}(3m^2)$ have all-odd coordinates ($m$ odd), and
$w \cdot v = 0$ with $v \equiv (1,1,1) \bmod 2$ forces $|w|^2 \equiv
(\sum_i w_i)^2 \equiv 0 \bmod 2$: every orthogonal lattice is
*even*.

**Genus-character invariance (classical; machine-validated).** For
each odd $p \mid 3m^2$ the Legendre character $\chi_p$ is constant
on the values of a class coprime to the discriminant — validated by
brute enumeration per sphere; the 2-adic candidate characters
correctly *fail* here ($n \equiv 3 \bmod 4$) and are excluded.

**Theorem A9.3 (the coherence obstruction; necessity PROVEN via
A9.1 + invariance).** In a magic square of squares with center
$m^2$ and Lucas differences $U, V$ (so $U, V, U{+}V, U{-}V \in
D(m)$), every one of the 8 lines forces its **co-norm triple** to be
$\chi_p$-coherent (all members coprime to $p$ share one character
value) for every odd $p \mid 3m^2$: the four center lines give
$(2m^2,\ 2m^2 \pm X)$ for $X \in \{U, V, U{+}V, U{-}V\}$, and the
four outer lines give
$(2m^2{+}U,\ 2m^2{-}U{-}V,\ 2m^2{+}V)$,
$(2m^2{-}V,\ 2m^2{+}U{+}V,\ 2m^2{-}U)$,
$(2m^2{+}U,\ 2m^2{-}U{+}V,\ 2m^2{-}V)$,
$(2m^2{+}V,\ 2m^2{+}U{-}V,\ 2m^2{-}U)$.

**The measured bite (pinned in `a9.coherence`).** Applied to
*ordered congrua pairs* $(U,V) \in D(m)^2$ — a necessary condition
for a pair to extend to a magic square, requiring **no** assumption
that $U \pm V$ are congrua — the obstruction kills **10 of 12**
pairs at $m = 65, 85, 130$ (survivors: exactly the two imprimitive
branches paired with each other, e.g. $(3000, 4056)$ at $m=65$, the
$5\cdot(5,12,13)$ and $13\cdot(3,4,5)$ branches), **6 of 12** at
$m = 145$ (survivors: exactly the six pairs involving the 5-branch
congruum $21000$), and **nothing** at the prime powers $25, 125$.
This is the first necessary condition on extending congrua pairs
beyond the classical $24 \mid d$ layer (A3/F4) — cross-branch
gluing at multi-prime hypotenuses is mostly *arithmetically
incoherent*.

**Window refinement (measured).** The slice classes sit **strictly**
inside the classes representing $2m^2$ (at $m = 13$: 2 classes
against 5): the confinement window of §3 is genuinely finer than
the representation condition that A9.1 alone imposes.

### The three-sieve pair desert (third layer)

(Check `a9.pair_desert`.) An honest postscript first: the
coherence "survivors" of the kill table above are all *trivially*
impossible — for every one of them $U + V > m^2$, so the smallest
edge entry $m^2 - U - V$ would be negative. The character sieve
was measured there in isolation; the two sieves turn out to be
**complementary** (positivity kills the large-sum pairs characters
miss, characters kill the small-sum pairs positivity misses). So
stack the proven-necessary conditions:

1. **Positivity:** $U + V \le m^2$.
2. **Coherence:** Theorem A9.3.
3. **Representation (the class level proper):** each of the 8
   co-norm triples must be *represented by a single class* — some
   even class of discriminant $-4 \cdot 3m^2/g^2$, where $g$ runs
   over the hypothetical point's possible contents (odd,
   $g^2 \mid 3m^2$, $g^2$ dividing the whole triple), representing
   all three scaled co-norms. Necessity is Lemma A9.1 + Lemma A9.4
   applied to the reduced point (the cross-vectors lie in the
   *saturated* orthogonal lattice); it is **strictly stronger than
   the character test** — same genus does not mean same class.

**Result (measured, pinned): for every center $m \le 1200$, every
ordered congrua pair dies.** Of 1782 ordered pairs across the 153
centers with $|D(m)| \ge 2$: **1608** die by positivity, **152**
by coherence, and the **22** that pass both (11 unordered, the
first at $m = 425$: $(54600, 97104)$; also $m = 481, 725, 845,
850, 901, 925, 962, 1025$) are all killed by representation —
in every one of the 22 cases the $U{+}V$ diagonal center line's
triple $(2m^2,\, 2m^2 \pm (U{+}V))$ is representable by **no**
class at any admissible discriminant, and usually most outer lines
too. Zero pairs remain.

Two soundness controls are built into the check: the *actual* $U$-
and $V$-center lines (which exist as sphere points whenever
$U, V \in D(m)$) always have nonempty candidate sets — the
machinery never kills a line that exists — and the actual points'
(content, reduced class) pairs are verified to lie in their own
lines' candidate sets.

This is not a new desert *bound* (A3's quadruple search reaches
much further); it is the first structural *explanation* at the
pair level: three arithmetic obstructions, each proven necessary
and none requiring any square-testing search, jointly annihilate
every candidate pair in range.

### The anatomy of the kills: local certificates and the composition frontier (fourth layer)

(`compute/sphere_composition.py`; checks `a9.composition`,
`a9.local_criterion`, `a9.kill_anatomy`.)

**A soundness correction first (honesty protocol).** The original
content enumeration behind the representation sieve looped over
*odd* point contents, justified by the all-odd lemma — which
requires $m$ odd. For **even** centers every point of
$\mathcal{S}(3m^2)$ has each coordinate of 2-adic valuation
*exactly* $v_2(m)$ (three squares summing to $0 \bmod 4$ are all
even, so the sphere reduces to the odd sphere), and the true
content is $2^{v_2(m)} \cdot \text{odd}$ — never matched by the
odd-only loop. Fixed; **all 22 kills stand with identical
signatures**, the even centers now exactly reproducing their odd
cores ($850 = 2\cdot425$, $962 = 2\cdot481$, with pairs
$4\times$ the odd-core pairs — a strong consistency check), and
the never-kill-a-real-line controls now also run at the even
centers.

**Gauss composition, implemented and verified
(`a9.composition`).** Composition of primitive classes via united
representatives (with determinant $+1$ enforced — an improper
change of variables silently inverts the class, a bug the group
axioms caught). Verified as a group with pinned structure:
$\mathrm{Cl}(-507) \cong \mathbb{Z}/4$,
$\mathrm{Cl}(-3\cdot65^2) \cong \mathbb{Z}/12 \times \mathbb{Z}/2$
(full order multisets). **Gauss's principal genus theorem — the
squares are exactly the trivial-character genus — is
machine-verified**, so "invisible to every genus character"
rigorously means "inside a coset of $\mathrm{Cl}^2$". The
occurring character vectors form an index-2 subgroup of
$\{\pm1\}^\mu$ whose derived annihilator is supported at 3 alone:
**every value of every class has 3-free part $\equiv 1 \bmod 3$**
(the norm-residue law of the Eisenstein family).

**The local criterion (`a9.local_criterion`).** Classical local
lattice theory gives an exact criterion for an odd $w > 0$ to be
represented by *some* primitive class of disc $-3k^2$: inert
primes divide $w$ to even order; at $p \mid k$ with $e = v_p(k)$,
valuations below $2e$ are even with pinned character, and the
anisotropic case $p \equiv 2 \bmod 3$ forces even valuation above
too; the pinned signs must extend to an occurring vector (the
$\chi_3$ norm-residue law). **Validated exhaustively: criterion
$=$ brute-force class search for every odd $w \le 6000$ at three
sample discriminants (9000 values, zero mismatches).**

**The anatomy theorem (`a9.kill_anatomy`, measured and
certified).** Every one of the **57 killed lines** behind the 22
representation kills is classified:

- **21 are L0 — provably local**: a single co-norm value violates
  the validated local criterion at every stratum (all 24 such
  values certified);
- **0 are genus-mismatch**;
- **36 are GLOBAL — provably beyond-local**: every value passes
  the local criterion, *a single genus admits all three values*
  (with same-genus witnesses, e.g. at $m = 425$ a 45-class genus
  with per-value representing sets of sizes $45/8/2$ and empty
  triple intersection), yet **no single class represents the
  triple**. By the verified principal genus theorem these kills
  live inside cosets of $\mathrm{Cl}^2$ — no congruence or
  character condition can ever see them.

**The sharpest instance: $m = 725$.** *Both* pairs at $m = 725$
die exclusively through GLOBAL kills — that part of the pair
desert exists *only* because of composition structure. **The
fourth sieve is the class group proper.**

**Still open in A9-T1:** the *law* governing which classes
represent which co-norm triples inside a genus — the composition
word problem on the prime ideal classes (quaternionic/Venkov,
Aka–Einsiedler–Shapira joint-equidistribution territory), now
with a precise question: *what invariant of
$(2m^2, 2m^2 \pm X)$ separates the three representing sets
inside one genus?* Plus the full 9-entry gluing (corner entries
tie pairs of outer-line classes). **A9-T2 (acquisitions,
backlog):** Duke (Invent. Math. 92, 1988),
Aka–Einsiedler–Shapira, Venkov — see
[papers/WANTED.md](../../papers/WANTED.md) P8.

### The mechanism of the beyond-genus kills (fifth layer, M12-B) — and the desert to $10^4$

*(2026-08-28, ROADMAP W4/W6 first actions; `compute/redei_probe.py`,
`compute/desert_extension.py`; checks `a9.kill_mechanism`,
`a9.desert_ext`.)*

**The desert extends 25× with zero survivors (VERIFIED($3\times10^4$)).**
The three sieves annihilate **every** ordered congrua pair for every
center $m \le 30{,}000$: 6,101 centers, 146,914 ordered pairs —
122,630 positivity + 18,992 coherence + **5,292 representation**
kills, **no golden center** (frozen artifacts `data_desert_10k.json`
[1667 / 32,850 = 28,028 + 3,816 + 1,006] and `data_desert_30k.json`;
sampled representation kills re-verified live on every suite run;
the extension toward $10^5$ runs checkpointed). The
representation-kill corpus grew from 22 pairs to 5,292 — the anatomy
sample for the fourth-sieve law is now 240 times larger.

**Lemma A9.5 (inverse-closure; PROVEN).** *Representing sets are
inverse-closed ($f$ and $\bar f$ represent the same integers), so a
character constant on one takes value $\pm 1$ there. Hence:
(i) odd-order characters never separate two representing sets;
(ii) if the 2-Sylow subgroup of $\mathrm{Cl}$ is elementary abelian
(4-rank 0), every character's $\pm1$-part is a genus character,
and NO character of any order can separate representing sets inside
a genus.* Character certificates for beyond-genus kills can exist
only at discriminants with 4-rank $> 0$, and only through characters
of even order $\ge 4$.

**The verdicts (measured, pinned).** For all 36 GLOBAL kill-lines
behind the $m \le 1200$ desert, on their admitting strata:

- **6 kills are CHARACTER** — a quartic character (order exactly 4,
  every separator, no order-8, none odd — Lemma A9.5 confirmed on
  data) is constant on two of the three representing sets with
  opposite values. All six live at $m = 481$ and its even double
  $m = 962$ (lines 4, 6, 7; disc with $h = 144$, genus size 36,
  4-rank $> 0$). **This is the Rédei/4-rank layer, real but
  minority.**
- **30 kills are ARC** — *no character of any order separates*
  (at $m = 425, 725, 845, 850, 901, 925, 1025$; most of these discs
  have odd genus size, i.e. 4-rank 0, where Lemma A9.5 makes
  character certificates impossible outright — and at $m = 845$,
  where 4-rank $> 0$ offers quartic characters, they still fail).
  The kill is the **product-set geometry of prime ideal classes**:
  typical shapes $|S| = [2, 2, 24]$ or $[300, 4, 2]$ with one empty
  pairwise intersection — the kill reduces to explicit class
  equations $[\mathfrak{p}_1$-word$] \ne [\mathfrak{p}_2$-word$]$
  between tiny inverse-symmetric sets.
- At $m = 725$ every kill is ARC: the sharpest instance is entirely
  beyond reciprocity-by-characters.

**The ideal-product law (PROVEN-CLASSICAL, machine-verified on kill
data).** For values coprime to the conductor, the representing set is
exactly $c_3^{v_3(w)} \cdot \prod_{p \text{ split}, p^e \| w}
\{P_p^{k} : |k| \le e,\ k \equiv e \bmod 2\}$ — verified EXACT on
**62 of 62** conductor-coprime kill values, zero mismatches (the
remaining 46 values share primes with the conductor: the
non-invertible-ideal regime, the model's next extension).

**Verdict on H-Rédei (ROADMAP W4).** As a universal law: **refuted**
— 30 of 36 kills cannot be certified by any character, and Lemma A9.5
shows why (4-rank 0 makes it structurally impossible). As a layer:
**confirmed exactly** — where 4-rank bites, the separators are
precisely quartic. The refined working hypothesis (**H-align**): the
fourth sieve is the statement that *the classes of the prime ideals
dividing the coupled co-norms never align into the required product
relations*; quartic characters are its abelianized shadow. The law
now lives in the joint behavior of prime classes at algebraically
coupled arguments — exactly Venkov/quaternionic territory (W9's
probe is next), with the 1,006-pair corpus as its test bed.

### The center cap is a theorem (A9.6) — real lines never die

*(2026-08-28, proving the regularity the actuarial sample surfaced;
check `a9.center_cap` — constructive certificates over the entire
5,292-pair corpus.)*

**Theorem A9.6 (the center cap; PROVEN, all $m$).** Let $m \ge 1$ and
let $(U, V)$ be an ordered congrua pair of center $m^2$ (distinct
$U, V \in D(m)$). Then the center lines with offsets $U$ and $V$
(`pair_lines` indices 0, 1) always admit representing classes.
Consequently **at most two of the four center lines can be
unrepresentable — and they are exactly the two phantom lines with
offsets $U + V$ and $U - V$ (indices 2, 3).**

*Proof.* $U \in D(m)$ means $U = 2ef$ with integers $e > f > 0$,
$e^2 + f^2 = m^2$ (and $e \neq f$, since $2e^2 = m^2$ is impossible).
Set $v_U = (e{-}f,\ m,\ e{+}f) \in \mathbb{Z}^3$. Then
$$|v_U|^2 = (e{-}f)^2 + m^2 + (e{+}f)^2 = 2(e^2 + f^2) + m^2 = 3m^2,$$
so $v_U$ is an **actual point** of $\mathcal{S}(3m^2)$, its coordinate
squares are the $U$-line's entries $\{m^2 - U,\ m^2,\ m^2 + U\}$, and
its co-norm triple is $(2m^2 + U,\ 2m^2,\ 2m^2 - U)$ — precisely line
0's triple. Let $g$ be the content of $v_U$; the reduced point
$v_U/g$ lies on $\mathcal{S}(3m^2/g^2)$, its cross-vectors (the
gluing law, Lemma A9.1) lie in the saturated orthogonal lattice and
realize the three norms $\mathrm{tri}/g^2$, and the Gram form of that
lattice is an even form of discriminant $-12m^2/g^2$ (Lemma A9.4).
So $(g, \text{orthogonal form})$ is a sound candidate in
`line_classes`: line 0 is not killed. The same construction with $V$
handles line 1. Lines 2 and 3 carry offsets $U \pm V$, which admit
such an automatic point **iff $U \pm V \in D(m)$** — exactly the
additive-quadruple condition the desert forbids — so among center
lines only they can die. $\blacksquare$

**Corollary A9.6.1.** $k_c \le 2$ for every pair and every $m$ — the
sampled center cap is a theorem, unconditionally (not
range-verified); killed center lines are always $\subseteq
\{L_{U+V}, L_{U-V}\}$.

**Corollary A9.6.2 (the sieve's true shape).** The representation
sieve never acts through real lines: its entire action on center
lines is a test of the two phantom sums $U \pm V$. The fourth sieve
is thereby revealed as *the class-group shadow of the A3 additive
condition*: line 2 (resp.\ 3) is representable-by-a-real-point iff
$U + V \in D(m)$ (resp.\ $U - V$), and killing it is the class-group
way of saying "the sum fails to be a congruum *for structural
reasons*". The measured companion — every corpus kill includes line
2 or 3 ($k_c \ge 1$ on all 160 samples) — remains empirical, but now
reads: *the pair desert dies, always, at the additive coupling*,
never merely at the outer entries.

### The Gram sieve (A9.7) — the fourth sieve is (almost) a principal-form law

*(2026-08-28, the $k_c \ge 1$ companion hunt; `compute/gram_sieve.py`,
check `a9.gram_sieve`.)*

**Theorem A9.7 (pairwise Gram necessity; PROVEN).** Let $L$ be a
positive-definite rank-2 lattice with $\det L = N$, and let $w_1, w_2$
be norms of vectors $x_1, x_2 \in L$. If $x_1, x_2$ are independent,
then $t := \langle x_1, x_2\rangle$ and the index
$k := [L : \mathbb{Z}x_1 + \mathbb{Z}x_2] \ge 1$ satisfy
$$w_1 w_2 \;=\; t^2 + N k^2$$
(det of the Gram matrix of the sublattice is $k^2 \det L$); if
proportional, $w_1w_2 = t^2$ is a perfect square. **Hence a line whose
co-norm triple is represented by a single class of determinant $N$
has every pairwise product $w_iw_j$ of the form $t^2 + Nk^2$,
$k \ge 1$ (or a perfect square)** — at the top stratum
$N = 3m^2$: representable by the *principal* form $x^2 + 3m^2y^2$
with $y \ge 1$. The line-level test (`gram_line_ok`: some admissible
content stratum passes all three pairs) is a machine-checkable
necessary condition for representability. $\blacksquare$

**Proposition A9.7.1 (coherence is the local Gram layer).** For an
odd prime $p \mid 3m^2$, reducing $w_1w_2 = t^2 + 3m^2k^2$ modulo $p$
forces $w_1w_2 \equiv t^2$, i.e. $\chi_p(w_1) = \chi_p(w_2)$ whenever
both are nonzero mod $p$ — exactly the pairwise
$\chi_p$-coherence of Theorem A9.3. *The coherence sieve is the local
shadow of the Gram sieve; the Gram sieve's global content
(representability by the principal class, not merely everywhere
locally) is beyond all genus characters* — precisely where the
M12-B anatomy located the 36 GLOBAL kills.

**The census (measured, pinned).** On the eleven $\le 1200$ passers
(the M12-B anatomy set) and a 30-pair corpus sample ($m \le 4000$):

- **soundness: zero violations** — no representable line fails the
  Gram test, on every line of every pair examined (the theorem,
  confirmed on data);
- **the Gram sieve explains 56 of the 57 anatomy kills** — including
  the beyond-genus GLOBAL kills: the ARC mechanism of M12-B *is*, in
  all but one case, the principal-form Gram condition. The single
  exception — $m = 725$, pair $(171600, 282576)$, line 5 — is killed
  but pairwise-Gram-alive: the one known kill requiring the
  third-vector (syzygy) layer beyond pairwise Gram;
- **the companion, mechanized:** in all 30 sampled corpus pairs a
  phantom line (2 or 3) is killed, and in all 30 the phantom kill is
  a *Gram failure*. Every observed kill pattern contains line 2 or 3.

**Refined working hypotheses.** (**H-Gram**, replacing H-align's
vague form): *the representation sieve equals the Gram sieve plus
rare syzygy corrections* — the fourth sieve is the principal-norm
law $w_iw_j \in \{t^2 + 3m^2k^2\}$. (**A9.C2**, the companion at
Gram level): *any Gram failure among the eight lines forces a Gram
failure on line 2 or 3* — now a pure statement about the arithmetic
of the ten products; first analysis: both Brahmagupta pairings of
$u_+v_+ = (3m^2 - d_1^2)(3m^2 - d_2^2)$ land on the real side
($t^2 - 3m^2k^2$), so no outer product passes for free — the
companion's content is genuinely two-sided. Proving A9.C2 proves
$k_c \ge 1$ modulo the (single known) syzygy exception.

### The actuarial model, v1 (ROADMAP W6) — is the desert's record surprising?

*(2026-08-28; `compute/actuarial_model.py`; sample artifacts
`data_actuarial_smallm.json` (40 pairs, $m \le 6000$, pinned by
`a9.actuarial_sample`) and `data_actuarial_sample.json` (120 pairs,
full range). Status: heuristic — CONJECTURED-class reasoning on
measured inputs; nothing here is load-bearing for any PROVEN claim.)*

**Measured inputs.** On stratified samples of the stage-3 (rep-killed)
corpus, the full 8-line kill scan gives: per-line kill probability
$p \approx 0.70$–$0.73$, **flat in $m$** (bands to $3\times10^4$ —
notable in itself: representing sets grow with $h \sim m$, yet the
coupled co-norms hold the kill rate constant); outer lines die at
$\approx 95\%$, center lines at $\approx 49\%$.

**Two law-shaped regularities** (VERIFIED on 160 sampled pairs):
1. **The center cap:** the number of killed center lines is always
   1 or 2 — never 0, never 3 or 4. *The $\le 2$ half is now
   **Theorem A9.6** (previous subsection): the $U$- and $V$-lines are
   real sphere points and can never die; only the phantom
   $U \pm V$-lines can.* The $\ge 1$ half ("every kill includes a
   center kill") remains measured, tying the death of a pair to the
   additive coupling rather than the outer entries — even though
   outer lines individually die more often.
2. Consequently the killed-line count caps at **6 of 8** (98/120 at
   exactly 6), and a truncated-binomial (independent-lines) fit is
   demonstrably wrong in shape.

**The model and its reading.** Under the (imperfect) independence
baseline, $\mathbb{E}[\text{golden} \le 3\times10^4] \approx 0.2$–$0.4$
— **the desert's perfect record to $3\times10^4$ is expected, not yet
evidence for an all-$m$ law.** The expectation crosses 1 near
$m \sim 10^5$ and reaches $\sim 10^2$ by $10^6$ (stage-3 density
fitted as $\sim M^{1.7}$ from $22 \to 5292$; survival held at the
pooled $(1-p)^8 \approx 4$–$7 \times 10^{-5}$; the measured line
dependence widens the honest uncertainty to at least an order of
magnitude each way). **Decision rule adopted:** the running $10^5$
leg is the model's first real test; a zero-golden outcome at $10^6$
would strain every variant of the random model and constitute genuine
evidence that the fourth sieve is a law (W4) — while a golden center
found is W6's telescope working as designed. Either outcome pays.

## 4. What the verify script proves mechanically

`verify/checks/a9_spheres.py`: the all-lines-on-one-sphere identity
(symbolic, via the Lucas parametrization), the trivial point, the
exact slice $\leftrightarrow$ $D(m)$ bijection for every $m$ up to
the profile bound, the all-odd residue fact, the pinned tension
table (max sphere size vs $L_3 = L_4 = 0$); and the class layer:
the two independent $h(-3m^2)$ computations agreeing with pinned
values, and the Gauss-map profile ($r_3^* = 24h$ asserted per
sphere, uniform fibers, the slice-concentration law) on the pinned
sample; the cross-vector gluing law, on-sphere coherence, and even
lattices on every point of 4 spheres (960 points), the pinned
coherence kill table with its survivor structure and the strict
window inclusion at $m = 13$; the three-sieve pair desert —
positivity/coherence/representation totals pinned to $m \le 1200$
with zero survivors, the $U{+}V$-diagonal unrepresentability in
all 22 passing pairs, and the never-kill-a-real-line controls
(odd and even centers); and the fourth layer — composition group
laws with pinned class-group structures, the principal genus
theorem, the exhaustively validated local criterion (9000 values),
and the pinned kill anatomy ($21$ L0 $+$ $0$ GENUS $+$ $36$
GLOBAL with all certifications).
