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
