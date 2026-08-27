# A8 — Symmetric differentials by descent to the Lucas plane

**Status:** §1 paper digests (six Tier-1 sources acquired 2026-08-26;
García-Fritz–Urzúa READ in full); §2 structure of the arrangement
**PROVEN** (machine-checked); §3 the decomposition theorem **PROVEN**;
§4 the local calculus **PROVEN** (with the executable engine as its
implementation); §5 first results **VERIFIED** — notably
$q(\widetilde X) = 0$, $h^0(X^\circ, S^2\Omega^1) = 0$ and the six
explicit invariant sections at $m_{\min} = 4$; §6 the Vojta/GFU
deficit analysis (honest negative); §7 the special-curve locus:
**Lemma A8.6 PROVEN**, Certificate A8.7 (mod-$p$ scan) upgraded the
same day by **Theorem A8.7′ PROVEN** (exact resultants, exact gcd),
so **Theorem A8.8 — every complete genus-0 curve on $X$ passes
through a node — is PROVEN, unconditional**; §8 the node-extension
layer: **$h^0(\widetilde X, S^4\Omega^1) = 1$** (the resolution's
unique symmetric quartic differential $\eta_\star = \eta_4$, PROVEN),
universal $\eta_\star$-integrality of rational curves,
$\widetilde C \cdot E \ge 4$, the node-pattern dichotomy, and the
pattern-counting theorems **A8.14–A8.15 PROVEN: every genus-0 curve
meets nodes over $\ge 3$ distinct triple points — sharp** (the
classical families attain 3); §9 roadmap. Verification:
`python3 -m verify --only a8`.

## 0. Goal

BTVA prove quasi-hyperbolicity of $X$ abstractly but state that
computing $\hat S^m\Omega^1_X$ explicitly — the input to their
special-curve-locus machinery (Corollary `C:explicit_resultant_locus`)
— "*is out of range of current computational techniques*". Their route
is Gröbner-basis module algebra over the coordinate ring of
$X \subset \mathbb{P}^8$ (degree 64), which does not see the cover
structure. This document replaces it with **descent along the
$(\mathbb{Z}/2)^8$ cover** $\pi : X \to \mathbb{P}^2$: the space of
symmetric differentials on the open surface splits into 256 character
eigenspaces, each an exact finite linear-algebra problem *on the Lucas
plane*.

## 1. The acquired sources (papers/, 2026-08-26)

- **García-Fritz–Urzúa** (arXiv:1804.07671, Math. Z.; READ in full):
  the Vojta-style method — an $\omega \in H^0(X_0, L \otimes
  S^r\Omega^1)$ with known *$\omega$-integral curves* (curves where
  $\omega$ pulls back to zero), towers of cyclic covers branched on
  integral curves, the toric local calculus on cyclic quotient
  singularities (§4.1), and the key mechanism: genus $\le 1$ curves
  are forced into integral loci when the twist
  $\sum \frac{1}{m_i} D_i - L$ is ample (their Theorems 4.1/5.1); for
  double covers ($m = 2$, $A_1$ singularities) the strict form fails
  (their Remarks 2.7/4.2) and the workaround (§3) is extra vanishing
  of $\omega$ at the nodes, yielding for the cuboid surface: every
  genus $\le 1$ curve through $\ge 2$ nodes; rational non-conic curves
  have $C \cdot E \ge 8$.
- **Stoll–Testa** (arXiv:1009.0388v2, updated 2025): the cuboid
  surface's full Picard lattice ($\rho = h^{1,1} = 64$, maximal;
  discriminant $-2^{28}$), automorphisms (order 1536), Brauer group,
  and the classification of all integral curves with $C \cdot K \le 6$;
  their Lemma 21 gives $C \cdot E \ge 8$ (rational non-conic) and
  $\ge 4$ (genus 1) by lattice methods. Three independent methods
  (BTVA / GFU / lattice) now all certify node-passage bounds *on the
  cuboid*; nothing analogous exists for $X$ — that is A8's target.
- **Lu–Miyaoka** (MRL 2 (1995)) and **Miyaoka** (Publ. RIMS 44
  (2008)): effective canonical-degree bounds for low-genus curves —
  requiring $K^2 > c_2$. For $X$: $K^2 = 576 < 768 = c_2$, and even
  the $A_1$-orbifold correction only lowers $c_2$ to
  $768 - 256/2 = 640 > 576$. **The effective-bound route (old A7
  roadmap item "orbifold-Miyaoka") is closed for the full surface** —
  deficit 64 — leaving intermediate quotients as the only opening
  (scan scheduled; the M9 double-plane scan already found no
  $s_2 > 0$ quotient at the double-plane level).
- **Bruin–Ilten–Xu** (EPIGA 9 (2025)): Wahl local Euler
  characteristics for all $A_n$ (the $n = 1$ case is BTVA's, already
  reproduced in `a7btva.*`), plus their §5 machinery for explicit
  regular differentials.
- **Horie–Yamauchi** (arXiv:2512.22520): the cuboid surface's full
  $L$-function and $\operatorname{Pic}(\bar S)$ as a Galois module —
  the template's arithmetic endpoint.

## 2. Structure of the arrangement (PROVEN, `a8.structure`)

Index the nine entry lines by the $3{\times}3$ grid:
$\ell_{(a,b)} = c + au + bv$, $(a,b) \in \{-1,0,1\}^2$. Dualizing,
concurrency of lines is collinearity of grid points, so:

- **The 8 triple points are exactly the 8 lines-of-three of the
  grid** (3 rows, 3 columns, 2 diagonals). The four triples on the
  entry line $c$ are the four lines-of-three through $(0,0)$.
- **Pencil structure**: the three "column" pencils $\{a = t\}$ have
  base points $A_0 = (0{:}1{:}0)$, $A_\pm = (1{:}\mp1{:}0)$ — all on
  the difference line $v = 0$; the three "row" pencils $\{b = t\}$
  have base points $B_0, B_\pm$ on $u = 0$. The degenerate genus-0
  families of Theorem A7.3 live exactly over these two lines.
- **Conic split**: the six lines $\{(\pm1,0), (0,\pm1), (1,1),
  (-1,-1)\}$ are tangent to a single smooth conic (dual conic
  $X^2 - Y^2 - Z^2 + YZ = 0$ through their grid points), and the
  complementary three lines form the $\{a = -b\}$ pencil; mirror
  statement for $X^2 - Y^2 - Z^2 - YZ$ and the $\{a = b\}$ pencil.
  So the arrangement is "6 tangents of a conic + a pencil", two ways.

## 3. The decomposition theorem (PROVEN)

**Theorem A8.1.** Let $X^\circ = X \smallsetminus \{256\ \text{nodes}\}$
and let $G = \{\pm1\}^9/\{\pm1\} \cong (\mathbb{Z}/2)^8$ act by sign
flips of the root coordinates. Then for every $m$:
$$H^0(X^\circ, S^m\Omega^1) \;=\; \bigoplus_{\substack{S \subseteq
\{\text{lines}\} \\ |S| \text{ even}}} V_S, \qquad
V_S \cong \Bigl\{\eta \in S^m\Omega^1_{k(\mathbb{P}^2)} :
\pi^*(\eta)\big/\textstyle\prod_{j\in S} x_j \text{ regular on }
X^\circ\Bigr\},$$
and membership in $V_S$ is a **divisorial** condition: writing
$\eta = \sum_k a_k \, d\ell_j^{\,k}\, dv^{m-k}$ in coordinates adapted
to the line $\ell_j$,
$$\eta \in V_S \iff \operatorname{ord}_{\ell_j}(a_k) \ge
\Bigl\lceil \tfrac{\varepsilon_j - k}{2} \Bigr\rceil \ \ \forall j, k
\qquad (\varepsilon_j = [\,j \in S\,]),$$
together with regularity of $\eta$ along every other divisor of
$\mathbb{P}^2$ (in particular along $u = 0$, $v = 0$ and at infinity).

*Proof.* $G$ acts on $X^\circ$ (the nodes are a $G$-stable set), so
the section space splits into eigenspaces indexed by
$\widehat G = \{$even subsets$\}$ (odd subsets are characters of
$\{\pm1\}^9$ that do not descend past the global scalar). For $\omega$
in the $\chi_S$-eigenspace, $\omega \cdot \prod_{S} x_j$ is invariant
with poles only over the branch locus, and $\pi$ is generically
étale, so it is $\pi^*(\eta)$ for a rational $\eta$ downstairs; this
inverts. Regularity of a rational section of a *vector bundle* on the
smooth surface $X^\circ$ is a codimension-1 condition (its polar locus
is a divisor), and the divisors of $X^\circ$ lying over the plane are:
the $R_j$ (over the generic points of the branch lines, local model
$x_j^2 = \ell_j$, i.e. $f = w^2$, $d f = 2w\,dw$, which yields the
displayed order condition for each monomial $df^k dv^{m-k}$ divided by
$w^{\varepsilon_j}$), and divisors over non-branch lines where $\pi$
is étale (condition: $\eta$ itself regular). Points over double points
and triple points of the arrangement, and the nodes themselves, have
codimension 2 and impose nothing. ∎

Consequences worth stating separately: for $j \in S$ the restriction
coefficient $a_0$ *vanishes* along $\ell_j$ (an integrality
condition), while for $j \notin S$ the differential may carry a pole
of depth $\lfloor m/2 \rfloor$ in the $d\ell_j^{\,m}$-direction —
the cover's ramification absorbs it.

## 4. The engine (`compute/descent_differentials.py`)

Chart 1 ($u = 1$, coordinates $(c,v)$) sees all nine lines
$c + a + bv$; chart 2 ($c = 1$) sees the one divisor chart 1 misses
($u = 0$); the missing point $(0{:}0{:}1)$ is codimension 2. Each
$V_S$ becomes: unknown numerator polynomials $N_0, \dots, N_m$ over
the denominator $\prod_{j \notin S}\ell_j^{\lfloor m/2 \rfloor}
\prod_{j \in S}\ell_j^{\lfloor (m-1)/2 \rfloor}$, subject to (i) the
per-line divisibility rows of Theorem A8.1 (implemented by exact
$c \mapsto -a - bv$ substitution of iterated $c$-derivatives), and
(ii) chart-2 regularity along $y = 0$ (exact coefficient conditions
after the substitution $(c,v) = (1/y, z/y)$, under which
$dc^i dv^{m-i}$ contributes $y^{-2m+t}$ to the $dy^{m-t}dz^t$-part).
Exact sparse Gaussian elimination over $\mathbb{Q}$; every reported
dimension is recomputed at numerator-degree bound $+2$ and required
to agree (saturation); the 8 grid symmetries organize the 256
characters into 51 orbits.

**Controls — all passing.** (i) The two-line sub-cover is
$\mathbb{P}^1 \times \mathbb{P}^1$: the engine returns $0$ for all its
characters at
$m = 1, 2, 3$, as it must (no global symmetric differentials — note
the instructive near-trap: $\eta = d\ell_1 d\ell_2$ pulls back to the
affinely-regular $4\,dx_1 dx_2$, and the engine correctly rejects it
for its order-4 pole over $u = 0$). (ii) $m = 1$ on the full cover
computes the irregularity, and the result ($q = 0$, §5) matches the
classical Zariski/Esnault–Viehweg picture: irregularity of abelian
line-arrangement covers comes from pencil sub-arrangements attached to
characters, and our even characters contain no pencils. (iii)
Orbit-equivariance and saturation are asserted mechanically.
(iv) **The gold-standard positive control PASSES**
(`compute/descent_cuboid.py`, `a8.cuboid_control`): the perfect-cuboid
surface is a $(\mathbb{Z}/2)^4$ cover of $\mathbb{P}^2$ branched on
four $\mathbb{Q}$-irreducible conics (three line-pairs and the
circle; its 48 nodes sit over the 3 line-pair vertices and the 6
tangency points with the circle — all codimension 2, so the same
divisorial theorem applies, with a pole allowance of $|T|$ along the
étale line $x_1 = 0$ from the projective balancing
$\omega \cdot \prod_T \mathrm{root}_i / x_1^{|T|}$). Running the same
methodology there reproduces BTVA's Magma-computed
$h^0(X_{\mathrm{pc}}, \hat S^2\Omega^1) = 13$ **exactly**, including
the full 16-character fingerprint read off their Table 1
($3, 3, 3, 1, 1, 1, 1$ on $\varnothing, \{z\}, \{y_1y_2y_3\},$ the
three $y$-pairs, $\{y_1y_2y_3z\}$; zero on the other nine), with
element-level membership of their descended generators ($\omega_4
\mapsto dc^2/Q_3 - dv^2/Q_2$, $\omega_7 \mapsto (Q_2\,dc^2 - 2cv\,
dc\,dv + Q_3\,dv^2)/Q_4$, and $x_2\omega_7, x_3\omega_7$) — and
$q(X_{\mathrm{pc}}') = 0$ at $m = 1$. The §5 zeros no longer carry a
pending-control caveat.

## 5. First results (VERIFIED, `a8.q_zero` / `a8.m2_survey`)

**Theorem A8.2 (irregularity).** $q(\widetilde X) =
h^0(X^\circ, \Omega^1) = 0$: all 256 characters vanish at $m = 1$.
Consequently (with M9's $b_2 = 766 + 4q$): $b_1(\widetilde X) = 0$,
$b_2(\widetilde X) = 766$, $h^{1,1}(\widetilde X) = 766 - 2p_g =
766 - 222 = 544$. *(The Picard number satisfies $\rho \le 544$; the
Stoll–Testa question "is $\rho$ maximal?" is now well-posed for $X$.)*

**Theorem A8.3 (no quadratic symmetric differentials).**
$$h^0(X^\circ, S^2\Omega^1) \;=\; h^0(X, \hat S^2\Omega^1_X) \;=\; 0:$$
all 256 character eigenspaces vanish at $m = 2$ (51 orbit
representatives, saturation-checked; methodology positively controlled
by the cuboid reproduction of §4). Contrast: the perfect-cuboid
surface has $h^0(\hat S^2\Omega^1) = 13$ (BTVA — now independently
**re-derived by this engine**), which powers their entire explicit
program there. **For the magic-square surface the
$m = 2$ explicit program is not merely out of computational range — its
input space is empty.** Any future explicit-resultant attack must work
at $m \ge 3$ (the corresponding surveys run on this engine; $m = 3$ in
progress at the time of writing).

**Theorem A8.4 (the first-section bracket).** With our verified
$(K^2, c_2, \ell) = (576, 768, 256)$ and the exact $A_1$ local Euler
characteristic, Blache's local-global formula gives
$$\chi(X, \hat S^m\Omega^1_X) = \chi(Y, S^m\Omega^1_Y) +
256\,\chi_{\mathrm{loc}}(m) =
-624,\ -1344,\ -1360,\ -1632,\ -560,\ \mathbf{+384}$$
for $m = 2, \dots, 7$ (`a8.chi_hat_bracket`; note the near-miss at
$m = 6$). Since $h^2(X, \hat S^m\Omega^1_X) = 0$ for $m \ge 3$
(Bogomolov–De Oliveira / Deschamps, as invoked in BTVA's Leray lemma —
PROVEN-CLASSICAL/CITED), $h^0(X^\circ, S^7\Omega^1) \ge 384$:
**the first nonzero symmetric degree on $X^\circ$ lies in
$\{3, \dots, 7\}$** — far below BTVA's resolution-level guarantee
$m \ge 47$, and within reach of this engine (a mod-$p$ fast path
proves zeros cheaply; only nonzero candidates need exact runs).

**Theorem A8.5 (first sections at $m = 4$ — the "out of range"
computation, executed).** $h^0(X^\circ, S^3\Omega^1) = 0$ (all 256
characters, proved by saturated mod-$p$ elimination — a zero nullity
mod $p$ proves the exact zero, since rank only drops under reduction),
while at $m = 4$ the **trivial character** carries
$$\dim V_\varnothing(4) = 6,$$
certified sandwich-style: six exact rational vectors *verified against
the exact condition system* (dimension $\ge 6$) meeting the mod-$p$
nullity ($\le 6$). **These are the first explicit symmetric
differentials ever computed on the magic-square surface** — six
invariant sections of $S^4\Omega^1$ on $X^\circ$, i.e. six elements of
$H^0(X, \hat S^4\Omega^1_X)$, with exact coefficients stored in
`compute/data_m4_generators.py` (numerators over the denominator
$\prod_{(a,b)} \ell_{(a,b)}^2$, re-verified from scratch by
`a8.m4_generators`). So the first nonzero symmetric degree is exactly
$$m_{\min} = 4 \qquad (\text{vs BTVA's resolution-level guarantee }
m \ge 47),$$
and with $\ge 2$ independent sections in hand, BTVA's explicit
special-curve machinery (their §`s:resultants`) is applicable to $X$
for the first time: every complete genus-0 curve on $X$ avoiding the
nodes lies in the resultant locus $\operatorname{res}(\omega_i,
\omega_j)$ — computed in §7 below.

**The full $m = 4$ spectrum** (all 51 orbits, saturated mod-$p$; run
record in `compute/data_m4_spectrum.json`): **every non-trivial
character vanishes**, so
$$h^0(X^\circ, S^4\Omega^1) \;=\; h^0(X, \hat S^4\Omega^1_X) \;=\; 6,
\qquad \text{all of it Galois-invariant.}$$
The first symmetric differentials on $X$ descend from *orbifold*
symmetric differentials of the pair $(\mathbb{P}^2, \tfrac12
\sum_{(a,b)} \ell_{(a,b)})$ — the Lucas plane itself carries them.
(Compare the cuboid, where the $m = 2$ space spreads over seven
characters.)

## 6. The Vojta/GFU route: a structural deficit (honest analysis)

For GFU's Theorem 4.1/5.1-style conclusions one needs $\omega$ on
$\mathbb{P}^2$ with all nine lines $\omega$-integral and
$\sum \tfrac12 \ell_j - L$ ample, i.e. $L = \mathcal{O}(d)$ with
$d < 9/2$. The natural constructions all miss:

- **Pencil products.** $\theta_P = g\,df - f\,dg \in
  H^0(\Omega^1(2))$ kills exactly the lines through $P$; the two
  triple-products $\omega_{\mathrm{col}} = \theta_{A_0}\theta_{A_+}
  \theta_{A_-}$ and $\omega_{\mathrm{row}}$ (§2) have **all nine lines
  integral with completely classified integral curves** (the three
  pencils) — but cost $d = 6$. Each pencil-$\theta$ covers 3 lines
  (credit $3/2$) at cost $2$: deficit $1/2$ per factor, always.
- **Conic duals.** The GFU §4 differential of a conic's tangent
  family costs $S^2\Omega^1(4)$ and covers the 6 tangent lines:
  ratio $6/8$ — the same $3/4$ as pencils. Nine lines tangent to one
  conic would break even; our maximum is 6 (§2).
- **Cheaper sections do not exist**: $S^r\Omega^1(d)$ has no sections
  at all for $d \le r + 1$ (Bott), a triple point forces $r \ge 3$
  distinct null directions (or vanishing of $\omega$ there), and the
  machine-checkable candidate spaces at $d \le 4$ are zero.

This is as it must be: $X$ *has* genus $\le 1$ curves, so no
exception-free Vojta statement can hold. The productive versions —
zero-deficit relative statements over sub-covers, and the GFU §3-style
node-passage bounds using the $E$-vanishing that the engine's local
calculus provides (at a node over a triple point, $\pi^*$ of an
$r$-symmetric $\eta$ vanishes along the exceptional curve to order
$\ge r + 2\nu$, $\nu$ = vanishing order of $\eta$ at the triple
point) — are the continuation, joined with §5's spaces once a
nonzero $m$ is located.

## 7. The special-curve locus and node passage (M11-D)

The continuation §6 called for, executed with §5's spaces
(`compute/special_locus.py`; checks `a8.z_properness`,
`a8.z_catalogue`, `a8.z_scan`).

Write the six invariant generators of $H^0(X^\circ, S^4\Omega^1)$ as
$\omega_a = \pi^*\eta_a$ with
$\eta_a = D^{-1}\sum_{k=0}^4 N^{(a)}_k(c, v)\, dc^k\, dv^{4-k}$,
$D = \prod \ell_{(a,b)}^2$ (Theorem A8.5). At a plane point $P$ the
**direction quartic** of $\eta_a$ is the binary form $F_a(P; dc, dv) =
\sum_k N^{(a)}_k(P)\, dc^k dv^{4-k}$ (the common denominator cancels
from root conditions), and the **special-curve locus** is
$$Z \;=\; \bigl\{P \in \mathbb{P}^2 : F_1(P), \dots, F_6(P) \text{
have a common projective root}\bigr\},$$
a closed subset (the image of the incidence variety in
$\mathbb{P}^2 \times \mathbb{P}^1$ under the proper first projection).
Every numerator coefficient $N_k$ has total degree $\le 14 = d_N - 9$
(asserted at load; for $N_0$ this is exactly regularity of $\eta$
along $u = 0$, see below).

**Lemma A8.6 (unconditional reduction). PROVEN.** Let $C \subset X$ be
a complete curve of geometric genus $0$ containing none of the 256
nodes. Then:

1. its Lucas image $\pi(C)$ avoids all 8 triple points of the
   arrangement — in particular $\pi(C)$ is **not** an entry line
   (each carries 2, 3 or 4 triple points, A7 §3) and **not** a pencil
   carrier $u = 0$, $v = 0$ (3 each, §2);
2. $\pi(C)$ is a common integral curve of the whole six-dimensional
   system: at a general point $P$ of $\pi(C)$ the tangent direction is
   a common root of $F_1(P), \dots, F_6(P)$ — so $\pi(C) \subseteq Z$;
3. $Z$ is a **proper** closed subset of the plane (exact certificate:
   the six quartics are coprime at rational points, `a8.z_properness`),
   so $\pi(C)$ is one of its finitely many curve components; and
   $\deg \pi(C) \ge 3$ by Theorems A7.3 + A7.6.

*Proof.* (1) The fibre of $\pi$ over a triple point consists of nodes
only: three branch lines meet there, the local $(\mathbb{Z}/2)^3$
subcover is $z_i^2 = \ell_i$ — eliminating, the $A_1$ cone
$z_3^2 = \alpha z_1^2 + \beta z_2^2$ — and the remaining
$(\mathbb{Z}/2)^5$ acts freely, giving the $8 \times 32 = 256$ count
(A7 §5). $C \to \pi(C)$ is surjective (complete curve, finite $\pi$),
so a triple point on $\pi(C)$ would put a point of $C$ in a nodal
fibre. (2) On the normalization $\nu: \mathbb{P}^1 \to C \subset
X^\circ$ ($X^\circ$ is smooth), $S^4$ of the cotangent restriction
$\nu^*\Omega^1_{X^\circ} \twoheadrightarrow \Omega^1_{\mathbb{P}^1}$
sends each $\omega_a$ to a global section of
$\mathcal{O}_{\mathbb{P}^1}(-8) = 0$. By (1), $\pi(C)$ is not a branch
line, so $\pi \circ \nu$ maps $\mathbb{P}^1$ dominantly (and
separably, char 0) to $\pi(C)$, and $0 = \nu^*\omega_a =
(\pi\nu)^*\eta_a$ forces $\eta_a$ to restrict to zero on $\pi(C)$:
at a general $P \in \pi(C)$ off the arrangement the tangent direction
annuls every $F_a(P)$. (3) Properness: a point with coprime quartics
lies off $Z$; closed $\ne \mathbb{P}^2$ means $\dim Z \le 1$. The
degree bound is A7.6 with A7.3 (no genus-0 curve over any line except
the entry-degenerate families over $u{=}0/v{=}0$, excluded in (1); no
genus $\le 1$ curve over any conic). $\blacksquare$

**Exact catalogue facts** (`a8.z_catalogue`, all six generators,
exact rational arithmetic):

- **all nine entry lines lie in $Z$**: along $\ell_{(a,b)}$, the
  line's own direction is a common root of all six direction quartics.
  (This is *root containment at the poles*, not integrality — and it
  is the consistency floor for the scan below: $Z$'s curve part
  contains at least these nine lines.)
- **$v = 0$ is not integral**, and neither are the six distinctness
  lines $u = \pm v$, $u = \pm 2v$, $2u = \pm v$ (horizontal lines
  $v = k$ in the chart).
- **$u = 0$ is not integral.** The $(c,v)$-chart cannot see $u = 0$;
  in the chart $c = 1$ with $(y, z) = (u/c, v/c)$ one computes
  $$\eta = y^{-13} \textstyle\sum_k (-1)^k \widetilde N_k\, dy^k
  (y\,dz - z\,dy)^{4-k} \big/ \widetilde D, \qquad
  \widetilde N_k = y^{23} N_k(1/y, z/y),$$
  whose $dz^4$-component is $y^{-9}\widetilde N_0/\widetilde D$.
  Since $\pi$ is étale over $u = 0$ away from the three
  $B$-triple-points, $\eta$ is regular there, forcing $y^9 \mid
  \widetilde N_0$, i.e. $\deg N_0 \le 14$ (holds); the pullback to
  $\{y = 0\}$ is then $([y^9]\widetilde N_0)(z)\, dz^4 /
  (1 - z^2)^6$, so $u = 0$ is integral iff the total-degree-14 part
  of $N_0$ vanishes — it does **not** (generators 2 and 6 carry
  degree-14 terms). Cross-check: the transpose symmetry
  $(c{:}u{:}v) \mapsto (c{:}v{:}u)$ preserves the invariant 6-space
  and swaps $u = 0 \leftrightarrow v = 0$, so the two verdicts must
  agree — they do.

**Certificate A8.7 (the curve part of $Z$). VERIFIED (mod $p$: 2
primes $\times$ 3 exact lines $\times$ all 15 pairs;
`a8.z_scan`).** For each of three exact rational test lines $L$ —
certified generic on the fly: the nine entry-line crossing parameters
are pairwise distinct rationals, so $L$ avoids every multiple point of
the arrangement — and each of $p \in \{999999937,\ 1000003919\}$,
interpolate the fifteen restricted resultants
$R_{ab}(t) = \operatorname{Res}_{(dc:dv)}\bigl(F_a|_{L(t)},
F_b|_{L(t)}\bigr) \bmod p$ (degrees 92–96, against the a-priori bound
$8 \times 14 = 112$) and form $g_L = \gcd_{a<b} R_{ab}$. **In all six
scans:**
$$\deg g_L = 72 = 9 \times 8: \text{ the nine entry-line crossings,
each of multiplicity exactly } 8, \text{ and nothing else.}$$
Since $Z \cap L \subseteq V(g_L)$ (a common root of all six quartics
is in particular a common root of every pair), and the nine entry
lines already lie in $Z$ (catalogue) and account for the *entire*
gcd, **the curve part of $Z$ mod $p$ is exactly the nine entry
lines**: any further curve component would meet every test line, and
(the lines avoiding the multiple points) generically in a
non-crossing point — a root of $g_L$ with no room to exist.

*What is and is not certified.* The computation is exact linear
algebra mod two independent 30-bit primes; by Gauss's lemma the
primitive $\mathbb{Q}$-gcd reduces to a divisor of $g_L$ mod each
prime, so over $\mathbb{Q}$: $\deg \gcd \le 72$ and every root of the
$\mathbb{Q}$-gcd reduces into the crossing set modulo **both** primes.
The scan alone left the *exact* statement open (the former task
A8-T3) — **closed the same day by Theorem A8.7′ below**; the scan
stands as an independent consistency check of the exact factorization
(its per-crossing multiplicity 8 is exactly the gcd exponent below).

**Theorem A8.7′ (exact identification of $Z$; A8-T3 closed).
PROVEN** (`a8.z_exact`, `compute/z_exact.py`, ~5 s; exact resultants
stored in `compute/data_z_resultants.json`). *The curve part of $Z$
over $\overline{\mathbb{Q}}$ is contained in the nine entry lines.*

*Proof, machine-executed.* $Z \subseteq V(R_{12}) \cap V(R_{34})$ for
the pairwise resultants $R_{ab} = \operatorname{Res}_{(dc:dv)}(F_a,
F_b) \in \mathbb{Z}[c, v]$ (a point of $Z$ makes *every* pair share a
root; the universal binary-form resultant also vanishes when a form
degenerates, so the containment needs no genericity). The two
resultants are computed **exactly**:

- *Provably exact CRT.* Interpolate the $8 \times 8$ Sylvester
  determinant on a $113 \times 113$ grid modulo 30-bit primes. Every
  coefficient of the determinant is bounded by $\prod_{\text{rows}}
  (\ell^1\text{-norm of the row})$ — the permutation expansion — and
  the prime product exceeds twice that bound ($B \approx 10^{24}$,
  three primes suffice: the six generators have 2–3-digit integer
  coefficients after clearing content). Independently spot-verified
  at six integer points against exact integer Sylvester determinants.
  Result: $R_{12}$ of total degree 96 (864 terms, $\le 15$-digit
  coefficients), $R_{34}$ of degree 92.
- *Exact peeling.* Synthetic division over $\mathbb{Z}$ by the
  monic-in-$c$ linear forms $\ell_{(a,b)}$ gives the exact
  multiplicities: every entry line divides **both** resultants to
  order $\ge 8$, with
  $$R_{12} = \Bigl(\prod \ell^{8}\Bigr) \ell_{(0,0)}^{4}\, C_{12},
  \qquad R_{34} = \Bigl(\prod \ell^{8}\Bigr)
  \ell_{(-1,0)}^{2}\ell_{(1,0)}^{2}\ell_{(0,-1)}^{4}\ell_{(0,1)}^{4}
  \, C_{34},$$
  with cofactors $C_{12}$ (degree 20), $C_{34}$ (degree 8) divisible
  by no entry line.
- *Coprime cofactors, sound direction.* A common irreducible factor
  $H$ (WLOG primitive in $\mathbb{Z}[c,v]$, by Gauss) with $\deg_v H
  \ge 1$ has $\operatorname{lc}_v(H) \mid \operatorname{lc}_v(C_{ab})$
  in $\mathbb{Z}[c]$; the prime $p = 999999937$ keeps both
  $\operatorname{lc}_v$'s alive, so $H \bmod p$ would be a common
  positive-$v$-degree factor of the reductions — impossible:
  $\operatorname{Res}_v(C_{12}, C_{34})$ evaluated at $c_0 = 2$
  (where neither $\operatorname{lc}_v$ vanishes) is nonzero mod $p$.
  Common factors with $\deg_v = 0$ are excluded by the exact
  $v$-content gcd over $\mathbb{Q}$ ($= 1$).

Hence in the UFD $\mathbb{Q}[c, v]$ (and coprimality persists over
$\overline{\mathbb{Q}}$: Euclid in $\mathbb{Q}(c)[v]$ plus the
univariate content gcd are field-stable),
$$\gcd(R_{12}, R_{34}) \;=\; \prod_{(a,b)} \ell_{(a,b)}^{\,8}
\quad (\text{up to a nonzero constant}),$$
and an irreducible curve $V(H) \subseteq Z$ forces $H \mid R_{12}$,
$H \mid R_{34}$, so $H$ is an entry line. $\blacksquare$

**Theorem A8.8 (node passage for rational curves). PROVEN —
unconditional.** **Every complete curve of geometric genus 0 on $X$ —
every rational curve on $X^\circ$'s closure — passes through at least
one of the 256 nodes.** Equivalently: on the resolution
$\widetilde X$, every rational curve meets the exceptional
$(-2)$-locus.

*Proof.* Suppose $C$ avoids the nodes. Lemma A8.6 puts $\pi(C)$ inside
the curve part of $Z$ but off the entry lines; Theorem A8.7′ says the
curve part of $Z$ consists of entry lines alone. $\blacksquare$

**Non-vacuity.** $X$ *does* carry complete rational curves — the
$64 + 64$ entry-degenerate AP-family components over $u = 0$ and
$v = 0$ (Theorem A7.3). The theorem is sharp on them and they verify
it independently: their images carry the $B$- resp. $A$-triple points,
whose fibres are nodal (Lemma A8.6(1)) — the classical families all
pass through nodes, as the theorem demands.

**Placement.** BTVA prove node-passage refinements for the Barth
sextic (their Theorem `thm:barth`) and the cuboid surface
(`thm:CuboidIntro`), and state that $X$ is out of range of their
explicit machinery; GFU §3 and Stoll–Testa's lattice method give the
cuboid statements independently. Theorem A8.8 is the **first
node-passage statement for the magic-square surface itself**, at the
minimal symmetric degree $m_{\min} = 4$ — and it is exactly the
geometric mechanism behind the classical phenomenology: every known
rational family on $X$ is nodal, i.e. degenerate through the
triple-point structure. Strengthening "$\ge 1$ node" to "$\ge 2$
nodes" (the cuboid-grade statement) needs the node-extension layer —
which elements of the 6-space extend over which exceptional
$(-2)$-curves — scheduled as the next milestone (§8 item 3).

## 8. The node-extension layer (M11-F)

Which of the six differentials survive onto the **resolution**
$\widetilde X \to X$?  (`compute/node_extension.py`; checks
`a8.node_tau`, `a8.node_extension`.)

**Lemma A8.9 (local extension calculus). PROVEN.** Every one of the
8 triple points is the base of a 3-term *arithmetic progression* of
entry lines ($\ell_A + \ell_C = 2\ell_B$: rows, columns and diagonals
of the grid are APs), so the local $(\mathbb{Z}/2)^3$ subcover is
always the same cone $z_3^2 = (z_1^2 + z_2^2)/2$, $z_1^2 = \ell_A$,
$z_2^2 = \ell_C$ — rationally parametrized by its smooth double
cover $\mathbb{C}^2_{(s,t)}$ via
$$q_1 = s^2 + 2st - t^2, \quad q_2 = -s^2 + 2st + t^2, \quad
q_3 = s^2 + t^2, \qquad q_1^2 + q_2^2 = 2q_3^2 .$$
For $\omega = \pi^*\eta$ near a node, write the invariant germ on
$\mathbb{C}^2_{(s,t)}$ as $\sum f_k\, ds^k dt^{4-k}$ and let
$\tau(\eta, P)$ be the minimal coefficient order ($=$ minimal
$(s,t)$-order of the pulled-back numerator differential minus
$\operatorname{ord} = 24$ of $(\ell_A\ell_B\ell_C)^2$).  Then $\tau$
is even (invariance) and $\ge 0$ (regularity on $X^\circ$ +
Hartogs), and in the resolution chart $(\xi, w) = (s^2, t/s)$ the
$d\xi^j dw^{4-j}$-component of $\widetilde\omega$ has
$$\operatorname{ord}_\xi \ge \Bigl\lceil \tfrac{\tau + 4 - 2j}{2}
\Bigr\rceil, \qquad j = 0, \dots, 4$$
(each $dt = w\,ds + s\,dw$ spends an $s$ on every $dw$; both charts
by $s \leftrightarrow t$ symmetry).  So $\widetilde\omega$ **extends
across the exceptional curve iff $\tau \ge 4$**, and otherwise has
pole order $2 - \tau/2 \le 2$ along it.  All 32 nodes over one
triple point see the same $\tau$ (the residual $(\mathbb{Z}/2)^5$
acts freely and the space is invariant). $\blacksquare$

**Theorem A8.10 (the $\tau$-table and the resolution section).
PROVEN (exact; `a8.node_tau`, `a8.node_extension`).** At every one
of the 8 triple points the filtration of the 6-space is
$$\dim V_{\tau \ge 0} = 6, \quad V_{\tau \ge 2} = V_{\tau \ge 4} =
4, \quad V_{\tau \ge 6} = 0$$
— a 4-dimensional subspace extends over each point's 32 exceptional
curves, the rest have pole order exactly 2 ($\tau$ jumps $0 \to 4$).
The visible half of the $\tau$-table (columns $A_0, A_\pm$ = column
pencils, $D_\pm$ = diagonals; the $B$-columns follow by the
transpose):

| | $A_0$ | $A_+$ | $A_-$ | $D_+$ | $D_-$ |
|---|---|---|---|---|---|
| $\eta_1$ | 0 | 0 | 0 | 0 | 0 |
| $\eta_2$ | 4 | 0 | 0 | 0 | 0 |
| $\eta_3$ | 4 | 0 | 0 | 0 | 0 |
| $\eta_4$ | **4** | **4** | **4** | **4** | **4** |
| $\eta_5$ | 0 | 0 | 0 | 4 | 4 |
| $\eta_6$ | 4 | 4 | 4 | 0 | 0 |

The grid symmetries act on the 6-space as an explicit
$D_4$-representation (the transpose $\sigma$ swaps $\eta_1
\leftrightarrow \eta_2$ up to a factor 4 and $\eta_3 \leftrightarrow
\eta_6$, fixing $\eta_4, \eta_5$; the flips act diagonally;
$\sigma r$ has order 4 — all pinned by `a8.node_extension`), and the
intersection lattice of the eight extension subspaces is: pairwise
dimension 2 (22 pairs) or 3 (exactly the five middle-pencil pairs
$A_0B_0, A_0B_\pm, A_\pm B_0$ and $D_+D_-$), $A$- and $B$-triples of
dimension 2, and
$$W \;=\; \bigcap_{P \,\text{triple}} V_{\tau \ge 4}(P) \;=\;
\langle \eta_4 \rangle, \qquad \dim W = 1,$$
certified **directly**: $\tau(\eta_4) = 4$ at the five visible
points and $\tau(\sigma^*\eta_4) = 4$ again (covering the three
$B$-points).  Since restriction to $X \smallsetminus \{\text{nodes}\}
= \widetilde X \smallsetminus E$ is injective on
$H^0(\widetilde X, S^4\Omega^1)$,
$$h^0(\widetilde X, S^4\Omega^1_{\widetilde X}) \;=\; 1
\qquad (\text{and} \;=0 \text{ for } S^m,\ m \le 3),$$
**the resolution itself carries a unique symmetric quartic
differential** $\widetilde\omega_\star$ ($\eta_\star := \eta_4$,
spanning the trivial $D_4$-line) — at $m = 4$, against BTVA's
resolution-level guarantee $m \ge 47$.

**Theorem A8.11 (universal integrality). PROVEN.** *Every* complete
curve of geometric genus 0 on $X$ — through nodes or not — has Lucas
image an integral curve of the single differential $\eta_\star$.
(Strict transform meets $\widetilde\omega_\star$ regular; the
restriction to the normalization is a section of
$\mathcal{O}_{\mathbb{P}^1}(-8) = 0$; the image is not an entry line
by A7.3, so vanishing descends.)  Exact consistency: $u = 0$ and
$v = 0$ — the carriers of the classical AP families — **are**
$\eta_\star$-integral, while no single non-branch special line
beyond them is ($v = \pm1, \pm2, \pm\tfrac12$ all fail), matching
A7.3 exactly: the only genus-0 line images are $u = 0$ and $v = 0$.

**Theorem A8.12 (exceptional-degree bound). PROVEN.** On the
resolution, every complete genus-0 curve $C$ (strict transform
$\widetilde C \not\subseteq E$) satisfies
$$\widetilde C \cdot E \;\ge\; 4 .$$
*Proof.* Some $\omega$ in the 6-space restricts nonzero to
$\widetilde C$ (else the image is a common integral curve of all
six, forcing it into an entry line by Theorem A8.7′ — impossible by
A7.3).  That $\omega$ has pole orders $\in \{0, 2\}$ along the
$E$'s (Theorem A8.10), so its restriction is a nonzero section of a
line bundle of degree $\le -8 + 2\,\widetilde C \cdot E$.
$\blacksquare$  (Compare Stoll–Testa/GFU on the cuboid:
$C \cdot E \ge 8$ for rational non-conic curves — this is the first
bound of that type for $X$.)

**Theorem A8.13 (pattern dichotomy). PROVEN.** Let $C$ be a complete
genus-0 curve on $X$ with node pattern $S \subseteq \{8\ \text{triple
points}\}$ (the triple points whose nodes $C$ meets; $S \ne
\varnothing$ by Theorem A8.8).  Then the Lucas image of $C$ is a
common integral curve of the subspace $V_S = \bigcap_{P \in S}
V_{\tau \ge 4}(P)$, of dimension per the lattice above ($\ge 2$
whenever $|S| \le 2$, $\supseteq \langle\eta_4\rangle$ always).
Exact consistency with the classical families: the components over
$u = 0$ have $S \subseteq \{B_0, B_\pm\}$, and $u = 0$ is indeed
integral for the full 2-dimensional $B$-triple space $\langle \eta_3,
\eta_4 \rangle$ (mutatis mutandis $v = 0$ and $\langle \eta_4, \eta_6
\rangle$) — verified exactly.  **Consequence:** any genus-0 curve
whose nodes sit over at most 2 triple points has image inside the
resultant locus of a $\ge 2$-dimensional subsystem — a finite,
explicitly computable curve list.

**Theorem A8.14 (two triple points). PROVEN**
(`compute/pattern_loci.py`, `a8.pattern_singletons`; ~45 s for all
eight points).  *Every complete curve of geometric genus 0 on $X$
meets nodes over at least **two distinct triple points** of the
arrangement — in particular it passes through at least two distinct
nodes.*

*Proof, machine-executed.*  Suppose the node pattern is $S = \{P\}$.
By Theorem A8.13 the Lucas image is a common integral curve of the
4-dimensional $V_P$, so it lies in the curve part of $Z(V_P)$; and
for **each** of the eight triple points that curve part is contained
in the nine entry lines, by the Theorem-A8.7′ machinery applied to
the subsystem: two basis-pair resultants, computed provably exactly
(CRT past the $\ell^1$ bound, independently spot-verified), have
every entry line peeling off to order $\ge 8$ and **coprime peeled
cofactors** (witnessed over $\mathbb{Q}$; the first basis-pair
choice $(b_0b_1, b_0b_2)$ succeeds at all eight points, with
cofactor degrees 8–24).  A genus-0 curve has no entry-line image
(Theorem A7.3), contradiction.  $\blacksquare$

This is the magic-square analogue of BTVA's cuboid Theorem 1.2
("genus $\le 1$ curves pass through $\ge 2$ of the 48 nodes") — for
genus 0, by a different mechanism (extension subspaces instead of
$E$-vanishing counting).  And it is not the end:

**Theorem A8.15 (three triple points — SHARP). PROVEN**
(`a8.pattern_pairs`; all 28 two-point patterns, ~90 s).  *Every
complete curve of geometric genus 0 on $X$ meets nodes over at least
**three** distinct triple points — in particular through at least
three distinct nodes.  The bound is sharp: the classical AP
components over $u = 0$ and $v = 0$ have node pattern exactly
$\{B_0, B_\pm\}$ resp. $\{A_0, A_\pm\}$.*

*Proof, machine-executed.*  A pattern-$\{P, Q\}$ image contains $P$
and $Q$ (their nodes map there), avoids the other six triple points,
is integral for $V_S = V_P \cap V_Q$, and is not an entry line
(A7.3).  For a 2-dimensional pencil $V_S$, $Z(V_S) = V(\operatorname
{Res})$ *exactly*, so the image is a component of the peeled
cofactor.  The 28 patterns die three ways:

- **6 pairs** (the dim-3 lattice pairs): two of the three basis-pair
  resultants have coprime peeled cofactors — $Z(V_S)$'s curve part
  is the entry lines, as in Theorem A8.14.
- **10 pairs**: the peeled cofactor does not vanish at $P$ or at $Q$
  (exact projective evaluation), so no component passes through
  both.  (Where the line $PQ$ divides first — the pencil carriers
  $v = 0$, $u = 0$ for the $A$- and $B$-family pairs — the line is
  excluded by the third family point it carries, exactly the
  AP-family mechanism, and divided out until the quotient misses
  $P$ or $Q$.)
- **12 pairs** (outer points of different families): the cofactor is
  a degree-18 curve through **all eight** triple points, PROVEN
  irreducible over $\mathbb{Q}$ — restrictions to degree-preserving
  rational lines, squarefree over $\mathbb{Q}$, with mod-$p$
  factor-degree subset-sums *empty* across lines and primes (one
  line/prime pair even gives an irreducible restriction mod $p$).
  A $\mathbb{Q}$-rational point on a $\mathbb{Q}$-irreducible curve
  lies on **every** Galois-conjugate $\overline{\mathbb{Q}}$-
  component; the six outside triple points are rational and on the
  curve, so every component hits them: excluded.  $\blacksquare$

Since patterns of size 0, 1, 2 are now all impossible (A8.8, A8.14,
A8.15) and size 3 is attained, the pattern-counting layer is
**complete**.  What remains is classification at $|S| = 3$: which
integral curves beyond the classical families do the triple-pattern
subsystems admit?  (For the $A$-/$B$-triples, the 2-dimensional
spaces $\langle\eta_4, \eta_6\rangle$/$\langle\eta_3, \eta_4\rangle$;
for mixed triples, down to $\langle\eta_4\rangle$ — the
$\eta_\star$-web itself.)  That, and the GFU-§2-style analysis of the
$\eta_\star$-web, is the road to a Stoll–Testa-grade classification
of all rational curves on $X$.

## 9. Roadmap

1. ~~$m = 3, 4$ surveys~~ **done** (§5): $m_{\min} = 4$, six invariant
   generators stored. Remaining: **$m = 5, 6, 7$ mod-$p$ surveys**
   (growth of the section ring; $\hat\chi(7) = +384$ guarantees
   $h^0 \ge 384$ by $m = 7$ — is the ring generated at $m = 4$?).
2. ~~Cuboid positive control~~ **done** (§4): $h^0 = 13$ reproduced
   exactly, fingerprint and element-level.
3. ~~Node-extension layer~~ **done** (§8, M11-F): the $\tau$-calculus
   on the uniform AP-cone, the full extension lattice,
   $h^0(\widetilde X, S^4\Omega^1) = 1 = \langle\eta_4\rangle$,
   universal $\eta_\star$-integrality, $\widetilde C \cdot E \ge 4$,
   and the pattern dichotomy; singleton patterns excluded (M11-G,
   Theorem A8.14); **two-point patterns excluded (M11-H, Theorem
   A8.15): every genus-0 curve visits $\ge 3$ triple points — SHARP.
   The pattern-counting layer is complete.**  Remaining (M11-I): the
   $|S| = 3$ *classification* — integral curves of the triple-pattern
   subsystems beyond the classical families (down to the
   $\eta_\star$-web for mixed triples), GFU-§2-style; the road to the
   full rational-curve classification.
4. ~~A8-T3 (exact upgrade of Certificate A8.7)~~ **done the same
   day** (Theorem A8.7′, §7): exact $R_{12}, R_{34}$ by provably
   complete CRT, exact line-peeling, coprime cofactors — Theorem
   A8.8 is unconditional. (The full 15-pair exact gcd and the exact
   *scheme* structure of $Z$ — its finitely many isolated points —
   remain available extensions if ever needed.)
5. **Sub-cover Segre scan**: $s_2$ (orbifold-corrected) of all
   intermediate quotients, hunting for a Lu–Miyaoka-eligible quotient
   ($K^2 > c_2$); the M9 double-plane scan says none exists at the
   bottom level.
6. The two-conic + two-pencil structure of §2 as a source of special
   curves/fibrations on $X$ (each conic's tangent-line family is a
   1-parameter family of 6-tangency lines — compare the M10-B budget).

## 10. What the verify script proves mechanically

`verify/checks/a8_descent.py` (21 checks): the §2 structural facts
(grid-line triples, pencil base points on $u{=}0/v{=}0$, both conic
splits with smoothness); the quadric control at $m = 1, 2$; the
$d\ell_1 d\ell_2$ near-trap rejected for exactly the chart-2 reason;
$q = 0$ (all orbits, $m = 1$); the $m = 2$ survey (FULL: all 51
orbits with saturation; FAST: pinned sample) with total $0$;
orbit-equivariance of the solver on a full orbit; character-count
bookkeeping (51 orbits covering 256); the cuboid control (§4:
$h^0 = 13$, 16-character fingerprint, element memberships); mod-$p$
soundness (rank drops under reduction — a zero nullity mod $p$ is a
proof); the $m = 3$ survey (zero); the six $m = 4$ generators
re-verified from scratch against the exact condition system plus the
mod-$p$ ceiling ($h^0 = 6$ certified); the stored $m = 4$ spectrum
record (only the trivial character); the $\hat\chi$ bracket; and §7's
four: $Z$ proper (exact), the special-line catalogue (exact,
including the chart-2 $u = 0$ slice and the transpose-symmetry
agreement), the $Z$-scan certificate (3 lines $\times$ 2 primes,
structure pinned to $72 = 9 \times 8 + 0$), and the **exact**
certificate (recomputes $R_{12}, R_{34}$ with the provably complete
CRT, re-peels, re-witnesses coprimality, and compares against the
stored data file — Theorem A8.7′/A8.8 re-proved from scratch on
every FULL and FAST run); and §8's two: the $\tau$-table +
filtration $6/4/4/0$ at the visible triple points (with parity and
regularity asserted inside the $\tau$-computation), and the
node-extension bundle — $D_4$-representation matrices pinned,
extension lattice pinned ($22 \times 2 + 6 \times 3$, triples,
$W = \langle\eta_4\rangle$ with direct $\tau$-certification through
the transpose), the AP-family dichotomy consistency ($u = 0$
integral for the $B$-triple space, $v = 0$ for the $A$-triple
space), the eight singleton-pattern certificates (Theorem A8.14:
subsystem resultants exactly, entry lines peel to $\ge 8$, cofactors
coprime), and the 28 two-point-pattern certificates (Theorem A8.15:
coprime cofactors / point-evaluation prefilters / carrier-line
peeling / the degree-18 irreducibility certificates).
