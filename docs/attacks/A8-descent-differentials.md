# A8 — Symmetric differentials by descent to the Lucas plane

**Status:** §1 paper digests (six Tier-1 sources acquired 2026-08-26;
García-Fritz–Urzúa READ in full); §2 structure of the arrangement
**PROVEN** (machine-checked); §3 the decomposition theorem **PROVEN**;
§4 the local calculus **PROVEN** (with the executable engine as its
implementation); §5 first results **VERIFIED** — notably
$q(\widetilde X) = 0$, $h^0(X^\circ, S^2\Omega^1) = 0$ and the six
explicit invariant sections at $m_{\min} = 4$; §6 the Vojta/GFU
deficit analysis (honest negative); §7 the special-curve locus:
**Lemma A8.6 PROVEN**, **Certificate A8.7 VERIFIED (2 primes)**,
**Theorem A8.8 — every complete genus-0 curve on $X$ passes through a
node — PROVEN modulo the certificate's exact upgrade** (task A8-T3);
§8 roadmap. Verification: `python3 -m verify --only a8`.

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
A curve component of $Z_{\overline{\mathbb{Q}}}$ beyond the nine lines
would have to thread all three test lines through residues of
crossings at both primes simultaneously — no such component is
visible, but the *exact* statement ($Z$'s curve part over
$\overline{\mathbb{Q}}$ = the nine lines) awaits the exact bivariate
gcd / primary decomposition, recorded as **task A8-T3**. Everything
upstream (Lemma A8.6, the catalogue) is exact.

**Theorem A8.8 (node passage for rational curves). PROVEN modulo
Certificate A8.7** (which is VERIFIED at two primes; exact upgrade =
A8-T3). **Every complete curve of geometric genus 0 on $X$ — every
rational curve on $X^\circ$'s closure — passes through at least one
of the 256 nodes.** Equivalently: on the resolution $\widetilde X$,
every rational curve meets the exceptional $(-2)$-locus.

*Proof.* Suppose $C$ avoids the nodes. Lemma A8.6 puts $\pi(C)$ inside
the curve part of $Z$ but off the entry lines; Certificate A8.7 says
the curve part of $Z$ consists of the entry lines alone. $\blacksquare$

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

## 8. Roadmap

1. ~~$m = 3, 4$ surveys~~ **done** (§5): $m_{\min} = 4$, six invariant
   generators stored. Remaining: **$m = 5, 6, 7$ mod-$p$ surveys**
   (growth of the section ring; $\hat\chi(7) = +384$ guarantees
   $h^0 \ge 384$ by $m = 7$ — is the ring generated at $m = 4$?).
2. ~~Cuboid positive control~~ **done** (§4): $h^0 = 13$ reproduced
   exactly, fingerprint and element-level.
3. **Node-extension layer** — now the route from Theorem A8.8's
   "$\ge 1$ node" to the cuboid-grade "$\ge 2$ nodes": which elements
   of the 6-space extend over which exceptional curves (the
   $\chi^0$-conditions, computed on the cone model $w_3^2 = \alpha
   w_1^2 + \beta w_2^2$), then GFU §3 / BTVA cuboid-Theorem-1.2-style
   counting against $C \cdot E$.
4. **A8-T3 (exact upgrade of Certificate A8.7):** identify the curve
   part of $Z$ over $\overline{\mathbb{Q}}$ exactly — the bivariate
   resultants $\operatorname{Res}(F_a, F_b) \in \mathbb{Q}[c, v]$
   (degree $\le 112$ each) via modular interpolation + rational
   reconstruction, then their exact gcd/primary decomposition. Until
   then Theorem A8.8 carries the mod-$p$ tag honestly.
5. **Sub-cover Segre scan**: $s_2$ (orbifold-corrected) of all
   intermediate quotients, hunting for a Lu–Miyaoka-eligible quotient
   ($K^2 > c_2$); the M9 double-plane scan says none exists at the
   bottom level.
6. The two-conic + two-pencil structure of §2 as a source of special
   curves/fibrations on $X$ (each conic's tangent-line family is a
   1-parameter family of 6-tangency lines — compare the M10-B budget).

## 9. What the verify script proves mechanically

`verify/checks/a8_descent.py` (16 checks): the §2 structural facts
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
three: $Z$ proper (exact), the special-line catalogue (exact,
including the chart-2 $u = 0$ slice and the transpose-symmetry
agreement), and the $Z$-scan certificate (3 lines $\times$ 2 primes,
structure pinned to $72 = 9 \times 8 + 0$).
