# A7 — Low-genus curves on X: machinery, the line theorem, sweeps, and invariants

**Status:** §1 state-of-field **verified-as-searched** (keyword-negative;
see caveats); §2 machinery and §3 **Theorem A7.3 PROVEN** (complete
classification of genus ≤ 1 curves over plane lines, with the
no-rational-points corollary via our own F3.2); §4 conic layer: budget
lemma **PROVEN**, three systematic sweeps **VERIFIED** (0 hits),
completeness for conics honestly **OPEN** (scoped); §5 invariants
**VERIFIED** with a structural discovery ($s_2 < 0$: the hyperbolicity
lives in the nodes); §6 roadmap. Verification:
`python3 -m verify --only a7`.

## 0. Goal

BTVA (CITED, arXiv:1912.08908) prove the surface $X \subset \mathbb{P}^8$
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
  sextic and the cuboid surface but *not* to $X$. (A low-confidence
  snippet hints at a magic-square "Theorem 1.5"; resolve on acquisition
  — [papers/WANTED.md](../../papers/WANTED.md) P1.)
- Their Magma code ships as **arXiv ancillary files**
  (`arxiv.org/src/1912.08908/anc`), not on GitHub; unfetchable here.
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
lines are the entry-degenerate families above. Moreover every genus ≤ 1
curve on $X$ with line image either is entry-degenerate or (the $c = 0$
elliptic components) carries no nondegenerate rational point — the
latter by F3.2, i.e. by Fermat's own descent, proven in this repository.

## 4. The conic layer: budget lemma and sweeps

An irreducible conic lies in no entry line and no difference line, so
along it the nine entries are pairwise distinct nonzero functions: **any
genus-0 component over a conic would be a nondegenerate rational curve
on $X$** — a function-field magic square of squares, disproving A2.C.
The stakes are correspondingly high.

**Lemma A7.5 (conic budget). PROVEN.** For a smooth conic, total
collision multiplicity is 18; a collision point is effective unless every
restricted form has even multiplicity there (for a smooth conic: exactly
the *free tangency* points, one line tangent and no other line through
the point). Per-point multiplicities are bounded by 4 (tangent line at a
triple point), 3 (transversal triple or tangent-at-double), 2, 1.
Consequently $r_{\mathrm{eff}} \le 4$ forces
$$\#\{\text{tangencies}\} \;\ge\; 9 - 2\,r_{\mathrm{eff}} + 
(\text{tangencies at multiple points}) \;\ge\; 1,$$
and in the $r_{\mathrm{eff}} = 3$ (potentially rational) regime the
conic must carry **at least five tangencies or pass through at least
four triple points** (case bookkeeping in the doc's checked sweep
classes below).

**Sweeps run (all exact arithmetic; `compute/conic_pullbacks.py`,
re-run by `a7.conics`): 216 irreducible candidate conics, zero genus
≤ 1 components.**

1. *Tangent-to-5*: for each 5-subset of the nine lines, the unique conic
   tangent to all five (via the dual conic), when irreducible. This
   class is **complete** for any low-genus conic with ≥ 5 tangencies —
   which includes every $r_{\mathrm{eff}} \le 3$ configuration with
   $\le 3$ triple-point passages.
2. *Through-5-triples*: all conics through five of the eight triple
   points.
3. *4-triple pencils*: for each of the 70 pencils of conics through four
   triple points, every member tangent to at least one entry line at a
   rational pencil parameter. Complete for low-genus conics through ≥ 4
   triples (any such must be tangent somewhere, by the budget), up to
   the rational-parameter caveat below.
4. Symmetric families (e.g. $u^2 + v^2 = \alpha c^2$); the showcase
   $u^2{+}v^2 = c^2$, tangent to four lines *at four triple points*, is
   verified to give $k = 4$, $r_{\mathrm{eff}} = 6$, genus **9** — a
   measure of how hard the budget is to satisfy.

**Honestly open for conics (scoped for M10):** mixed configurations with
exactly 3–4 tangencies and ≤ 3 triple-point passages (finitely many
polynomial systems, enumerated in §6), and conics with *irrational*
coefficients (Galois pairs; the analyzer is currently
$\mathbb{Q}$-exact). No claim of completeness is made beyond the swept
classes.

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

## 6. Roadmap (M10, paper-gated items marked ◆)

1. ◆ Digest BTVA (P1): the exact magic-square theorem, their
   differential spaces, and whether the ancillary Magma treats $X$; if
   their symmetric differentials on $X$ are computable, their base locus
   contains all genus ≤ 1 curves — the direct enumeration route.
2. ◆ Orbifold-Miyaoka with 256 $A_1$ points (P4/P6): extract an
   effective canonical-degree bound $K \cdot C \le B$ for genus ≤ 1
   curves; each plane-image degree $d$ satisfies
   $K \cdot C = 3 H \cdot C$ with $H \cdot C$ expressible through $d$
   and the component splitting — a bound $B$ makes §3's analysis a
   *finite* sweep over $d$.
3. Finish the conic layer: the two remaining finite configuration
   families (3 triples + 2 tangencies: 56×36 resultant systems; 1–2
   triples + 3–4 tangencies), plus extension-field coefficients.
4. Cubic images: the same machinery applies (nodal cubics are rational);
   the budget tightens (27 total multiplicity) — enumerate the
   analogous special-position classes.
5. Stoll–Testa lattice route on a *quotient*: pick an intermediate cover
   with manageable $b_2$, compute its NS lattice with Galois action, and
   enumerate low classes there; curves on $X$ map to curves on every
   quotient, so quotient bounds constrain $X$.

## 7. What the verify script proves mechanically

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
