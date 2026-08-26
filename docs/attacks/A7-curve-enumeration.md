# A7 — Low-genus curves on X: machinery, the line theorem, sweeps, and invariants

**Status:** §1 state-of-field **verified-as-searched** (keyword-negative;
see caveats), with the BTVA questions **resolved by acquisition** (§7);
§2 machinery and §3 **Theorem A7.3 PROVEN** (complete
classification of genus ≤ 1 curves over plane lines, with the
no-rational-points corollary via our own F3.2); §4 conic layer now
**CLOSED**: sharp budget lemma A7.5 **PROVEN** and **Theorem A7.6
PROVEN** (no genus ≤ 1 curve on $X$ has conic image; every genus ≤ 1
curve has Lucas-image degree ≥ 3 in characteristic 0) by exhaustive
exact sweeps of all six residual classes; §5 invariants
**VERIFIED** with a structural discovery ($s_2 < 0$: the hyperbolicity
lives in the nodes); §6 roadmap; §7 the BTVA digest — the paper READ,
its magic-square numbers **VERIFIED** (exact reproduction from our own
invariants), three display-level errata recorded. Verification:
`python3 -m verify --only a7`.

## 0. Goal

BTVA (**READ**; arXiv:1912.08908v3 = *Algebra & Number Theory* 16 (2022)
1377–1405; source archived in
[papers/1912.08908/](../../papers/1912.08908/)) prove the surface
$X \subset \mathbb{P}^8$
of magic squares of squares is algebraically quasi-hyperbolic: it carries
only finitely many curves of geometric genus ≤ 1. **Enumerating** those
curves and checking each is harmless would (a) settle Conjecture A2.C
over char-0 constant fields, and (b) reduce the rational-point problem to
genus ≥ 2 curves plus finitely many sporadic points. This document begins
that enumeration from first principles.

## 1. State of the field (2026-08-26 sweep; ~35 searches + agent)

No paper, preprint, thesis, or talk we could reach enumerates the
low-genus curves on $X$, computes its Picard/NS lattice or Brauer group,
or proves its genus ≤ 1 curves all degenerate. Key intelligence, with
provenance flags (all SUMMARY-ONLY unless noted):

- BTVA's finiteness proof runs through symmetric differentials and
  **Jouanolou's theorem — structurally non-effective**; the abstract
  grants "curves pass through ≥ k singularities" refinements to Barth's
  sextic and the cuboid surface but *not* to $X$. *(Resolved 2026-08-26
  from the acquired source, §7: the snippet's "Theorem 1.5" is the
  cuboid theorem `thm:CuboidIntro`; the paper contains **no**
  node-passage refinement and no curve list for $X$, and says the
  explicit method is out of computational range there.)*
- Their Magma code ships as **arXiv ancillary files**
  (`arxiv.org/src/1912.08908/anc`), not on GitHub. *(Acquired: it
  covers only Barth's sextic and the cuboid — no magic-square script.)*
- The worked template for the enumeration exists on the sister surface:
  **Stoll–Testa** (perfect cuboids, 48 nodes → Picard lattice → the 32
  known conics), recently extended by **Horie–Yamauchi** (full Picard
  Galois module). Nothing analogous exists for $X$.
- The arrangement underlying $X$ (nine lines, $(t_2, t_3) = (12, 8)$ —
  our data, `a5.arrangement`) appears in no arrangements literature we
  could find; the Hirzebruch-cover invariant route is unexploited.
- *Caveat:* this is a keyword-search negative, not a citation-graph
  negative (MathSciNet/zbMATH unreachable from this environment).

## 2. The cover machinery (PROVEN)

$\pi : X \to \mathbb{P}^2_{(c:u:v)}$ is the degree-$2^8$ abelian cover
with function field $k(\mathbb{P}^2)\big(\sqrt{\ell_i/\ell_9}\big)$,
branched over the nine entry lines $\ell_1, \dots, \ell_9$; its Galois
character group is $\{S \subseteq \{1..9\} : |S| \text{ even}\}$, the
character $\chi_S$ cutting the double cover branched on
$\sum_{i \in S} L_i$. (Independence: no nonempty product of distinct
lines is a square.)

Let $C \subset \mathbb{P}^2$ be an irreducible curve with normalization
$\tilde C$ of genus $g_C$, not an entry line (that case below). For each
entry line, restrict: $\ell_i|_C$ is a form on $\tilde C$; let
$p_1, \dots$ be the $\bar k$-points of $\tilde C$ supporting these
restrictions and $v_i \in \mathbb{F}_2^{\{p_j\}}$ the mod-2 multiplicity
vector of $\ell_i|_C$.

**Lemma A7.1 (splitting and genus).** The reduced preimage
$\pi^{-1}(C)$ splits into $2^8/2^k$ isomorphic irreducible components,
where $k = \operatorname{rank}_{\mathbb{F}_2}
\{\sum_{i \in S} v_i : |S| \text{ even}\}$; each component is an
elementary-abelian $(\mathbb{Z}/2)^k$-cover of $\tilde C$ branched
exactly at the points $p_j$ where the image lattice has odd support
("effective branch points", $r_{\mathrm{eff}}$ of them), all with
ramification index 2. Hence, for $C$ rational ($g_C = 0$):
$$\chi = 2^{k+1} - r_{\mathrm{eff}} \cdot 2^{k-1}, \qquad
g = 1 + 2^{k-2}\,(r_{\mathrm{eff}} - 4) \quad (k \ge 2),$$
with $g = (r_{\mathrm{eff}}-2)/2$ for $k = 1$ and $g = 0$ for $k = 0$.

*Proof.* Components correspond to the quotient of the character group by
$H = \{S : \ell_S|_C \text{ a square in } k(\tilde C)\}$
($\ell_S = \prod_{i \in S}\ell_i$), and $\ell_S|_C$ is a square iff all
multiplicities are even, i.e. $\sum_{i\in S} v_i = 0$: so the component
character group is the image lattice, of rank $k$. A point $p_j$
ramifies in the component cover iff some surviving character has odd
multiplicity there — iff the image has odd support at $p_j$. Each
surviving character is a double cover, so inertia is $\mathbb{Z}/2$ and
Riemann–Hurwitz for the $(\mathbb{Z}/2)^k$-cover of $\tilde C$ gives the
displayed $\chi$. ∎

**Lemma A7.2 (every collision point counts; lines are rigid).** If some
$\ell_i$ has odd multiplicity at $p_j$ and some entry line misses $p_j$,
then $p_j$ is an effective branch point (take $S = \{i, i'\}$ with
$\ell_{i'}$ supported away from $p_j$). For a **line** $C$ (not an entry
line), all nine restrictions are linear, multiplicities are the collision
multiplicities of $C$ with the arrangement, every collision point is
effective, and
$$k = r - 1, \qquad r = \#\,C \cap (L_1 \cup \dots \cup L_9),$$
so that $g = 1 + 2^{r-3}(r-4)$.
*Proof of $k = r-1$:* the achievable image vectors are exactly the
parity patterns $(a_1..a_r)$ obtained by choosing $s_j$ lines at $p_j$
($0 \le s_j \le m_j$, $s_j \equiv a_j$), subject to $\sum s_j = |S|$
even; since $\sum s_j \equiv \sum a_j \pmod 2$, the image is precisely
the even-weight subspace, of rank $r - 1$. ∎

For $C = L_j$ an entry line, the same analysis applies to the eight
remaining restrictions (the preimage lies in $\{x_j = 0\}$); parts of the
collision pattern have size (multiplicity $-\,1$).

## 3. The line theorem

**Theorem A7.3 (complete classification over lines). PROVEN.** A curve
on $X$ of geometric genus ≤ 1 whose image in the Lucas plane is a line
lies over exactly one of:

| image line | $r$ | $k$ | genus | components | nature |
|---|---|---|---|---|---|
| $u = 0$ | 3 | 2 | **0** | 64 | degenerate: entries repeat in triples — the classical 3-AP-of-squares family |
| $v = 0$ | 3 | 2 | **0** | 64 | same, transposed |
| $c = 0$ | 4 | 3 | **1** | 16 | center-zero: nine *distinct* entries, center $= 0$ |

and there are no others.

*Proof.* By Lemma A7.2, genus ≤ 1 forces $r \le 4$. For a non-entry
line, nine collisions in ≤ 4 points with per-point multiplicity ≤ 3
($t_4 = 0$) force the pattern $(3,3,3)$, $(3,3,2,1)$ or $(3,2,2,2)$ — in
every case the line passes through **at least two multiple points** of
the arrangement. The candidate set — the 9 entry lines plus every line
through two of the 20 multiple points, 69 lines in all — is therefore
exhaustive, and the mechanical sweep (`compute/curve_pullbacks.py`,
re-run by `a7.lines`) finds exactly the three rows above. For entry
lines, parts have size ≤ 2 (a size-2 part is a triple point of the
arrangement on the line), so $r \le 4$ with eight collisions forces the
pattern $(2,2,2,2)$: four triple points on one entry line — which only
the central line $c$ has (the $u$-type entry lines carry 2 triples,
$r = 6$, genus 17; the $(u{\pm}v)$-type carry 3, $r = 5$, genus 5). ∎

**Explicitly:**

- Over $u = 0$: entries are $c \times 3$, $(c{+}v)\times 3$,
  $(c{-}v)\times 3$; a component is parametrized by the classical family
  $c = (t^2+1)^2$, $v = 4t(t^2-1)$ — root vector
  $(t^2{+}1,\ t^2{-}2t{-}1,\ t^2{+}2t{-}1, \dots)$ — and the six
  defining quadrics vanish identically (machine-checked). These are
  rational curves on $X$, **entry-degenerate**.
- Over $c = 0$: a component is the space curve
  $$E:\quad \gamma^2 = \alpha^2 + \beta^2, \qquad
  \delta^2 = \alpha^2 - \beta^2 \quad \subset \mathbb{P}^3,$$
  via $u = \alpha^2$, $v = \beta^2$, $u+v = \gamma^2$, $u-v = \delta^2$
  (smooth intersection of two quadrics: genus 1). **Its rational points
  are all degenerate by our own Theorem F3.2** (multiplying the
  equations gives $\alpha^4 - \beta^4 = (\gamma\delta)^2$, Fermat's
  right-triangle equation), while over $\mathbb{Q}(i,\sqrt 5)$ it has
  the nondegenerate point $(\alpha,\beta,\gamma,\delta) =
  (41,\ 12\sqrt5,\ 49,\ 31)$ — precisely the
  [A3.K](A3-simultaneous-congrua.md) witness. The catalog and the
  descent-gap analysis meet exactly where they should.

**Corollary A7.4 (new, unconditional).** Every nonconstant magic square
of squares over $k(t)$ ($\operatorname{char} k \notin \{2,3\}$) has
Lucas-plane image of **degree ≥ 2**: the only genus-0 curves on $X$ over
lines are the entry-degenerate families above. *(For
$\operatorname{char} k = 0$ this is strengthened to degree ≥ 3 by
Theorem A7.6 below.)* Moreover every genus ≤ 1
curve on $X$ with line image either is entry-degenerate or (the $c = 0$
elliptic components) carries no nondegenerate rational point — the
latter by F3.2, i.e. by Fermat's own descent, proven in this repository.

## 4. The conic layer: budget lemma and sweeps

An irreducible conic lies in no entry line and no difference line, so
along it the nine entries are pairwise distinct nonzero functions: **any
genus-0 component over a conic would be a nondegenerate rational curve
on $X$** — a function-field magic square of squares, disproving A2.C.
The stakes are correspondingly high.

**Lemma A7.5 (sharp conic budget). PROVEN.** Let $C$ be a smooth conic
and $p \in C$ a point of the arrangement, lying on $\mu(p) \in
\{1,2,3\}$ entry lines. Every line through a point of a smooth conic
meets it there with multiplicity 1 (transversal) or 2 (the unique
tangent line), so the transversal/tangent counts at $p$ are forced:
$$(s_p, t_p) \in \{(\mu(p), 0),\ (\mu(p)-1, 1)\},$$
$p$ is branch-effective iff $s_p \ge 1$ (free iff $(s,t) = (0,1)$: a
tangency at a *simple* point), and $\sum_p (s_p + 2t_p) = 18$. Since
multiple points of the arrangement are rational and $s_p \le 3$,
writing $T$ for the number of tangent entry lines
($\sum_p s_p = 18 - 2T$):

- **genus 0** on a component forces $r_{\mathrm{eff}} \le 3$, hence
  $18 - 2T \le 9$, i.e. $T \ge 5$;
- **genus 1** forces $r_{\mathrm{eff}} = 4$ exactly (with $\le 4$
  points, $\sum s_p \le 12$ needs $T \ge 3$; $r_{\mathrm{eff}} \le 3$
  is the genus-0 case), and if $T \le 4$ the multiset of effective
  point types is **exactly one of six classes**:
  $$\begin{array}{ll}
  \text{C1: } 4 \times (3,0)\text{-triple} + 3 \text{ free} &
  \text{C2: } 3 \times (3,0)\text{-triple} + (1,0)\text{-simple} + 4
  \text{ free}\\
  \text{C3: } 3 \times (3,0)\text{-triple} + (1,1)\text{-double} + 3
  \text{ free} &
  \text{C4: } 2 \times (3,0)\text{-triple} + 2 \times
  (2,0)\text{-double} + 4 \text{ free}\\
  \text{C5: } 2\times(3,0)\text{-tr.} + (2,0)\text{-db.} +
  (2,1)\text{-tr.} + 3 \text{ free} &
  \text{C6: } 2 \times (3,0)\text{-triple} + 2 \times
  (2,1)\text{-triple} + 2 \text{ free.}
  \end{array}$$
  ($(s,t)$-triple/double = passage through a triple/double point with
  $t = 1$ meaning the conic's tangent line there is an entry line.)

*Proof.* The alphabet is forced as stated; the genus formula of Lemma
A7.1 gives $g \le 1 \Rightarrow r_{\mathrm{eff}} \le 4$ in every
$k$-branch; the class list is the exhaustive enumeration of type
multisets under the multiplicity identity — machine-checked as such by
`a7cc.budget_lemma`, which regenerates exactly these six signatures. ∎

**Theorem A7.6 (no low-genus curves over conics). PROVEN (exhaustive
exact computation, characteristic 0).** No curve of geometric genus
$\le 1$ on $X$ has conic image in the Lucas plane. Consequently (with
Theorem A7.3) **every genus $\le 1$ curve on $X_{\bar{\mathbb{Q}}}$ has
Lucas-image degree $\ge 3$**, and every nonconstant magic square of
squares over $k(t)$, $\operatorname{char} k = 0$, has Lucas-image
degree $\ge 3$ (over $\operatorname{char} p > 3$ the degree-$\ge 2$
statement of Corollary A7.4 stands).

*Proof structure* (each leg mechanical, `python3 -m verify --only
a7cc`; engines in `compute/conic_complete.py`):

1. **$T \ge 5$.** A smooth conic tangent to five entry lines has a
   *smooth* dual conic through their five rational dual points; so no
   three of the five lines are concurrent (no 3 collinear points on a
   smooth conic), and the dual is the *unique* conic through those five
   points — in particular rational. Of the 126 5-subsets, 98 contain a
   concurrent triple (no smooth tangent conic exists; the through-duals
   system yields a line pair) and 28 give the unique rational
   candidate, all swept in M9: **zero genus $\le 1$**
   (`a7cc.t5_completeness` + `a7.conics`).
2. **C1, C4** (4-point pencils: 70 quadruples of triples, 1848
   triple-pairs × double-pairs). Members tangent to $\ge 3$ (resp.
   $\ge 4$) lines are common roots of the nine restriction-discriminant
   binary quadratics — rational or *quadratic-irrational*, handled
   exactly in $\mathbb{Q}(\sqrt D)$ by a field-generic analyzer
   (validated against the M9 analyzer on all 216 rational candidates).
   Point sets with three collinear members (47 resp. 822; the 10
   collinear triple-triples live on $c$, the four $(u{\pm}v)$ lines,
   and $u{=}0$, $v{=}0$) admit only reducible conics. Result: one
   irreducible member in C1 — **the circle** $u^2{+}v^2 = c^2$, genus
   9 — and eight in C4, all genus 33. **Zero genus $\le 1$.**
3. **C3, C5, C6** (tangent-at-a-multiple-point classes: 1104, 6048,
   3780 linear systems of $\ge 5$ conditions; "tangent to $\ell$ at
   $p$" is the linear condition $Mp \parallel \ell$). Unique solutions
   analyzed exactly; degenerate systems are skipped only with *proof*
   of reducibility — a determinant cubic vanishing on a grid
   $\{0..3\}^d$ vanishes identically (degree 3 < 4 per variable) — and
   pencil fallbacks re-enter the engine of leg 2. 1252 irreducible
   solutions analyzed: **zero genus $\le 1$.**
4. **C2** (46 non-collinear triple-nets; tangency to 4 of the 9 lines
   on a net of conics). For each net and 4-subset, common zeros of the
   four discriminant quadrics are confined by pairwise $z$-resultants
   (Sylvester-exact, after a basis change making every leading
   coefficient a nonzero constant — otherwise the formal resultant
   vanishes spuriously); the gcd of the six resultants being constant
   **certifies emptiness over $\bar{\mathbb{Q}}$** (plus direct checks
   at the two loci the chart misses). 5792 of 5796 net-subsets are so
   certified; the 4 surviving candidate solutions are all **the circle
   again** (tangent to $c{\pm}u$, $c{\pm}v$ through the other four
   triples — genus 9). Candidate roots resolve in degree $\le 2$;
   any deeper algebraic root would be flagged (none is). **Zero genus
   $\le 1$.** ∎

The circle $u^2{+}v^2 = c^2$ — tangent to four lines at four triple
points, genus 9, rediscovered independently by the C1 and C2 engines —
is the unique "near miss" of the whole conic layer, a measure of how
rigid the budget is. The M9 caveats (irrational coefficients, mixed
configurations) are hereby **closed**: every genus $\le 1$ conic-image
curve would satisfy one of the rational class systems, whose solutions
the sweeps resolve completely (pencil classes in degree $\le 2$; net
classes by elimination certificates).

## 5. Invariants of the resolution (VERIFIED) — and where the hyperbolicity lives

`cover_invariants()` recomputes, from the incidence data alone
(re-checked by `a7.invariants`):

$$\chi_{\mathrm{top}}(X) = 512, \quad
\chi_{\mathrm{top}}(\widetilde X) = 768, \quad
K^2_{\widetilde X} = 576 \ \ (\text{two independent routes}), \quad
\chi(\mathcal{O}) = \frac{576 + 768}{12} = 112 \in \mathbb{Z},$$

with the 256 nodes of $X$ sitting 32 over each triple point (local model
$z_3^2 = a z_1^2 + b z_2^2$: $A_1$), resolved crepantly. Consequences:

- **$s_2 = c_1^2 - c_2 = -192 < 0$**: the resolution is *not* in the
  naive Bogomolov range, and the scan of all intermediate double planes
  ($|S| \in \{6, 8\}$) finds **none** with $s_2 > 0$ either. The
  quasi-hyperbolicity of $X$ is therefore genuinely carried by the
  **nodes** (Bogomolov–De Oliveira/BTVA mechanism: nodal surfaces admit
  more symmetric differentials than their resolutions' Chern numbers
  suggest) — the effective enumeration route must be the *orbifold*
  Miyaoka–Yau–Sakai inequality with $A_1$ contributions
  ([papers/WANTED.md](../../papers/WANTED.md) P4, P6), not plain
  Chern-number Bogomolov.
- $b_2(\widetilde X) = 766 + 4q$: the Néron–Severi lattice is *much*
  larger than the cuboid surface's — a Stoll–Testa-style full lattice
  computation is heavier here; intermediate quotients may be the
  practical vehicle (roadmap).
- Consistency: Noether integrality holds ($112$), the two $K^2$ routes
  agree (branched-cover formula and adjunction $K = 3H$, $\deg X = 64$
  from $H = \frac12\pi^* H_{\mathbb{P}^2}$), and the big
  $\mathbb{F}_p$ counts of `a5.fp_counts` are consistent with a large
  $b_2$.

## 6. Roadmap (updated after the BTVA digest; paper-gated items marked ◆)

1. ~~Digest BTVA (P1)~~ **done** — see §7. Outcome: no shortcut exists
   in the paper (no explicit differentials for $X$, no effective bound);
   but it hands us the exact $A_1$ local-Euler toolkit and a proof
   template that *descends to the base plane* (item 2).
2. **Base-descended symmetric differentials on the Lucas plane (the new
   lead).** BTVA's cuboid theorem is powered not by surface-level module
   computations but by one differential of the form
   $\omega = \phi^*(\eta)/(y_1y_2y_3z^2)$ with $\eta$ a degree-2
   symmetric differential **on $\mathbb{P}^2$** whose integral curves
   they classify completely (a conic and its tangent lines). The
   $X$-analogue: find $\eta$ on the Lucas plane, with denominator a
   monomial in the nine entry lines, such that $\pi^*(\eta)/(\prod
   \ell_i^{a_i})$ is regular on $X - S$ (a *local* double-cover
   computation along each branch line — tractable by exactly our §4
   absorption calculus), then classify $\eta$'s integral curves. Success
   would constrain genus ≤ 1 curves of **all** image degrees at once —
   bypassing the "out of range" module computation entirely. Precedent:
   García-Fritz–Urzúa did this for the cuboid surface via
   $\mathbb{P}^1 \times \mathbb{P}^1$ and got "every genus ≤ 1 curve
   passes through ≥ 2 nodes" (cited by BTVA, `GarciaFritzUrzua`); no
   analogue exists for $X$.
3. ◆ Orbifold-Miyaoka with 256 $A_1$ points (P4/P6): extract an
   effective canonical-degree bound $K \cdot C \le B$ for genus ≤ 1
   curves; each plane-image degree $d$ satisfies
   $K \cdot C = 3 H \cdot C$ with $H \cdot C$ expressible through $d$
   and the component splitting — a bound $B$ makes §3's analysis a
   *finite* sweep over $d$.
4. ~~Finish the conic layer~~ **done** (M10-B): Lemma A7.5 sharpened
   the class list to C1–C6, all swept exactly (quadratic fields and
   elimination certificates included) — Theorem A7.6: **no genus ≤ 1
   curve over conics**; image degree ≥ 3 in characteristic 0.
5. Cubic images: the same machinery applies (nodal cubics are rational);
   the budget tightens (27 total multiplicity; the smooth-point
   alphabet gains $(s,t)$ options at nodes/cusps of the cubic) —
   enumerate the analogous special-position classes.
6. Stoll–Testa lattice route on a *quotient*: pick an intermediate cover
   with manageable $b_2$, compute its NS lattice with Galois action, and
   enumerate low classes there; curves on $X$ map to curves on every
   quotient, so quotient bounds constrain $X$.
7. If ever a candidate section of $\hat S^m\Omega^1_X(-\lfloor m/2
   \rfloor H)$ becomes computable (by item 2 or new tooling), BTVA's
   Corollary `C:explicit_resultant_locus` applies verbatim at $n = 8$:
   every genus-0 curve on $X$ is in the resultant locus, in finitely
   many node-spanned hyperplanes, or passes through **≥ 9 nodes spanning
   $\mathbb{P}^8$**; every genus-1 curve not in the locus lies in a
   linear space at most one dimension above the span of the nodes it
   meets (in particular meets ≥ 2 nodes, and has degree ≤ 64 when its
   nodes span at most $\mathbb{P}^6$).

## 7. The BTVA digest (2026-08-26): exactly what the paper gives $X$, verified

Source acquired (owner upload) and READ end to end; archived with the
authors' ancillary Magma files in
[papers/1912.08908/](../../papers/1912.08908/). Everything below is now
first-party-verified where marked; reproduction checks:
`python3 -m verify --only a7btva` (implementation
`compute/btva_bounds.py`, exact rationals throughout).

**What the paper proves about $X$ — all of it.** (i) `thm:magicsquares`:
$X$ is algebraically quasi-hyperbolic, because a complete intersection
of $n-2$ quadrics in $\mathbb{P}^n$ with $\ell$ isolated $A_1$ points
has big cotangent bundle (on the resolution) once $\ell \ge
\ell_{\min}(n)$, and $X$ has $(n, \ell) = (8, 256)$ with
$\ell_{\min}(8) = 217$. (ii) The remark after it: the lower bound
$h^0(Y, S^m\Omega^1_Y) \ge \chi(Y, S^m\Omega^1_Y) + \ell\,
\chi^1(s, S^m\Omega^1_Y)$ (their Theorem `thm:main`) turns positive at
$m = 47$, with $h^0(Y, S^{47}\Omega^1_Y) \ge 8448$. (iii) Their model of
$X$ is our model (the seven line-sum equations in $\mathbb{P}^8$),
"smooth except for 256 isolated ordinary double points". **That is the
complete list.** There is no node-passage refinement for $X$ (the
sweep-phase "Theorem 1.5" snippet was `thm:CuboidIntro`, about the
perfect-cuboid surface), no curve enumeration, and no magic-square
ancillary code; the paper states $X$ "*is out of range of current
computational techniques to explicitly determine*
$\hat S^m\Omega^1_{X_{\mathrm{ms}}}$, *so we cannot apply the methods
from Corollary* `C:explicit_resultant_locus`". Our enumeration program
(§§2–5) is confirmed non-duplicative — now by the primary source, not
by keyword absence.

**Independent confirmation of §5, both directions.** Their CI Chern
formulas $K^2 = (n-5)^2 2^{n-2}$, $c_2 = (n^2 - 7n + 16)2^{n-3}$
(via Atiyah's simultaneous-resolution theorem: the resolution of a
nodal CI has the smooth CI's Chern numbers) give $(576, 768)$ at
$n = 8$ — equal to our branched-cover stratification values, computed
by a completely different route (`a7btva.ci_invariants` asserts both
routes agree). Their 256-node statement matches our 32-per-triple-point
count. Conversely our verified invariants feed their bound machinery
below.

**Their machinery, now in this repository (exact statements
implemented).** Wahl's local Euler characteristics at an $A_1$ point —
$\chi^0$ (codimension of the extension conditions; piecewise cubic mod
6, leading term $\tfrac{11}{108}m^3$) and $\chi^1$ (piecewise cubic mod
3, leading term $\tfrac{4}{27}m^3$) — with $\chi^0 + \chi^1 = \chi(s)$
verified as an identity of the three printed piecewise families to
$m = 2000$; the global $\chi(Y, S^m\Omega^1_Y)$ Riemann–Roch cubic; the
two lower bounds of `thm:main`; and the pole-refinement
(`C:regdif_lowerbound_quasiproj`): allowing poles along $r$ chosen
exceptional curves adds $r\chi^0$, and when the result still grows like
$Cm^3$ ($C > 0$) one gets *finitely many genus ≤ 1 curves through at
most $\ell - r$ nodes* — their partial-information lever.

**Reproductions (all exact, `a7btva.*`):** the $\chi^0$ first-values
table ($m \le 12$); the $\ell_{\min}$ table $73/145/217/145/0$
($n = 6..\ge 10$); **$X$: positivity exactly from $m = 47$ on** (proved
for all $m \ge 47$ via per-residue-class Cauchy root bounds, not a
finite scan) **with value $8448$ at $m = 47$** and growth
$\tfrac{160}{27}m^3$; the cuboid calibration ($\ell = 48 < 73$, poles
at $r = 35$ nodes give leading coefficient $\tfrac1{108}$, positivity
exactly from $m = 862$, $r = 35$ minimal); Barth's decic ($m \ge 160$,
$h^0 \ge 15755$) and Sarti's surface ($m \ge 28$, $h^0 \ge 7646$).

**Three display-level errata found** (conclusions unaffected — each
verified correct): (1) the §7 quadric-CI display's constant term reads
"$3n^2 - 27 + 66$" for $3n^2 - 27n + 66$; (2) at the $m \ge 47$ remark
in §`s:QuadricCIs` the bound is printed as
"$H^0(Y_{\mathrm{ms}}, \Omega^1_{Y_{\mathrm{ms}}}) \ge 8448$", missing
the $S^{47}$ (the introduction states it correctly); (3) the displayed
piecewise bound for Barth's decic corresponds, in all four coefficients
of all three residue classes, to $\ell = 339$ rather than
$(d, \ell) = (10, 345)$ — a substitution typo; with $\ell = 339$ its
threshold would be $808$, while the stated $m \ge 160$ and $15755$
match $\ell = 345$ exactly.

**Two facts worth recording for strategy.** (a) For $X$ the
partial-information lever is *subsumed*: the $r = 0$ bound already
grows cubically, i.e. full quasi-hyperbolicity — no node-passage
statement for $X$ can be extracted from their inequalities beyond
finiteness itself (we checked: the leading coefficient is positive for
every $r$). What their framework does **not** give — and what remains
the value of this program — is *which* curves the finite set contains.
(b) The older Bogomolov–De Oliveira/Serre-duality route
($h^0 \ge \chi + \ell\chi^0$, their Remark `rem:BORR`) fails for $X$:
its leading coefficient is $-\tfrac{160}{27} < 0$, and it would have
needed $\ell \ge 315 > 256$ nodes. The $\chi^1$-based bound is the one
that works — by a margin of $256 - 217 = 39$ nodes.

## 8. What the verify script proves mechanically

`verify/checks/a7_curves.py`: the 69-candidate line sweep reproduces
exactly the three-row table (and the entry-line $r$-profile $4/6/6/5/5$…);
the $k = r{-}1$ achievability lemma checked on all realized patterns;
the $u = 0$ parametrization satisfies all six quadrics identically
(complete-grid degree argument); the $c = 0$ component model is smooth
genus 1, carries the $\mathbb{Q}(i,\sqrt5)$ witness (exact quartic
algebra), and its $\alpha^4 - \beta^4 = (\gamma\delta)^2$ consequence
ties to F3.2's exhaustive check; `cover_invariants()` values asserted
(incl. Noether integrality and the two-route $K^2$); the circle conic's
exact analysis $(k, r_{\mathrm{eff}}, g) = (4, 6, 9)$; the conic sweeps
re-run (bounded in FAST) with zero hits; cross-module consistency of the
`ENTRY_LINES` data.

`verify/checks/a7_conics.py` (§4, M10-B): the $\mathbb{Q}(\sqrt D)$
arithmetic layer (square testing, inversion, quartic $\mathbb{Z}$-
splitting, exact gcd) unit-tested; the field-generic analyzer equal to
the M9 analyzer on all 216 rational candidates; **the budget lemma's
case analysis regenerated mechanically** (all admissible type multisets
under the multiplicity identity: genus 0 forces $T \ge 5$, genus 1
residual = exactly C1–C6); the tangent-to-5 dual-conic completeness
argument (28 candidate vs 98 concurrent-killed 5-subsets); the five
pure classes swept with pinned bookkeeping (systems/skips/analyzed
counts) and zero hits or unresolved flags; the C2 elimination
certificates (5792/5796 empty, 4 candidates = the genus-9 circle); the
10 collinear triple-triples identified line by line.

`verify/checks/a7_btva.py` (§7): the $A_1$ local-Euler identities and
first-values table; CI-formula ↔ cover-stratification agreement at
$(576, 768)$ with 256 nodes; the corrected §`s:QuadricCIs` display; the
$\ell_{\min}$ table with boundary minimality; the $X$ threshold
$m = 47$ / value $8448$ / growth $\tfrac{160}{27}m^3$ (Cauchy-bound
rigor) and the failure of the Serre-duality route ($\ell \ge 315$
needed); the cuboid partial-information calibration ($\tfrac1{108}$,
$862$, $r = 35$ minimal); the Barth-decic and Sarti reproductions plus
the $\ell = 339$ display-typo identification.
