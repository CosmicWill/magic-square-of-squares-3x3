# A5 — The surface: explicit model, verified geometry, precise open problems

**Status:** STUB with **PROVEN/VERIFIED nuggets** — the explicit model,
smoothness criterion, branch-arrangement combinatorics, and
$\mathbb{F}_p$ point counts are established here; the heavy geometry
(Picard, Brauer, curve enumeration) is posed as precise open problems
with the modern literature CITED. Verification:
`python3 -m verify --only a5`.

## 1. The explicit model (PROVEN/VERIFIED)

Let $X \subset \mathbb{P}^8$, coordinates $(x_1 : \dots : x_9)$ (the
*roots*, row-major), be defined by "the nine squares $x_i^2$ form a magic
square". The magic conditions are linear in the entries, hence quadrics
in the roots: the seven differences of line sums span a space of rank
**exactly 6** (`a5.model` — matching the modern literature's "$X$ is cut
by 6 quadrics in $\mathbb{P}^8$", CITED: Bruin–Thomas–Várilly-Alvarado
2022, Rome–Yamagishi 2024). A convenient independent set: with
$R_j, C_j, D, A$ the row/column/diagonal sums,
$$R_1{-}R_2,\; R_2{-}R_3,\; R_1{-}C_1,\; C_1{-}C_2,\; C_2{-}C_3,\;
R_1{-}D \quad (\text{and } R_1{-}A \text{ is dependent on these}).$$
$\dim X = 8 - 6 = 2$: a surface.

**Proposition A5.1 (smoothness off the coordinate hyperplanes —
PROVEN).** Every point of $X$ with all nine coordinates nonzero is a
smooth point. *Proof.* The Jacobian of the six quadrics
$Q_k = \sum_i m_{ki} x_i^2$ is $(2 m_{ki} x_i)_{k,i} = 2 M
\operatorname{diag}(x)$; when all $x_i \neq 0$,
$\operatorname{rank} = \operatorname{rank} M = 6$ (the rank computed
above), which is maximal. ∎ So all singularities live where some root
vanishes — the degeneracy locus — matching the literature's description
of $X$ as a singular (nodal) surface with special locus among degenerate
squares.

**Symmetries.** $(\pm 1)^9$ sign flips (trivial on entries) and the
$D_4$ of F1 act on $X$; modulo the global scalar this is a group of
order $2^8 \cdot 8$ — any curve/point enumeration should be organized by
this action (`a5.fp_counts` finds all point counts divisible by 64).

## 2. $X$ as an iterated double cover of $\mathbb{P}^2$, and the branch arrangement (VERIFIED)

Forgetting signs, $X \to \mathbb{P}^2_{(c:u:v)}$ (the Lucas plane) is a
$2^8$-to-1 (mod scalars) iterated double cover, branched over the
arrangement $\mathcal{A}$ of **nine lines** — the entry lines
$$c,\quad c \pm u,\quad c \pm v,\quad c \pm (u{+}v),\quad c \pm (u{-}v).$$
`a5.arrangement` computes the combinatorics: $\mathcal{A}$ has exactly
**8 triple points and 12 double points** (and no higher multiplicities):
the triples are
$$(0{:}0{:}1),\ (0{:}1{:}0),\ (0{:}1{:}{\pm}1) \quad\text{(on the line } c = 0\text{)},
\qquad (1{:}{\pm}1{:}0),\ (1{:}0{:}{\pm}1).$$
This is the standard setup (Hirzebruch-style abelian covers branched
along line arrangements) in which $\chi$, $K^2$, and lattice data of
such surfaces are classically computed — the concrete route to Problem
P1 below.

## 3. Point counts over $\mathbb{F}_p$ (VERIFIED), and Lang in miniature

Counting via the cover ($\#X$-cone $= \sum_{(c,u,v)} \prod_i
(1 + \chi(\ell_i))$), `a5.fp_counts` verifies:

| $p$ | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|
| $\#X(\mathbb{F}_p)$ | 320 | 384 | 1280 | 1344 | 1536 | 2304 | 2944 |

All counts vastly exceed $\sim p^2$: the points are concentrated on the
**degeneracy locus** (the sub-curves with repeated/zero entries, lifted
through up to $2^8$ sign choices — note $64 \mid$ every count). Indeed
by [F5.3](../foundations/F5-local-solubility.md) the *nondegenerate*
locus (nine distinct nonzero entries) is **empty** for every $p < 59$:
over small fields, literally all points of $X$ are degenerate. This is
the Bombieri–Lang philosophy for $X$ visible in miniature — rational
points concentrate on the finitely many special curves — and it is
exactly what the open problem asks to establish over $\mathbb{Q}$.

## 4. The precise open problems

- **P1 (invariants).** Compute $\chi(\mathcal{O})$, $K^2$, and the
  Picard lattice of (a resolution of) $X$, e.g. via the §2 cover
  structure over the $(t_2, t_3) = (12, 8)$ arrangement. No published
  computation is known to us (survey caveat: SUMMARY-ONLY provenance
  throughout).
- **P2 (Brauer–Manin).** [F5](../foundations/F5-local-solubility.md)
  kills all local obstructions, so the natural computable global
  candidate is Brauer–Manin on (a resolution of) $X$; we found no
  published computation. Caveat: for surfaces of general type BM need
  not capture everything — but even a negative computation would be
  informative.
- **P3 (curve enumeration — the keystone).** BTVA (**READ**, source in
  [papers/1912.08908/](../../papers/1912.08908/)) prove $X$ is
  algebraically quasi-hyperbolic: finitely many curves of genus
  $\le 1$. **Enumerate them and check each lies in the degeneracy
  locus.** *Now underway in [A7](A7-curve-enumeration.md): the line
  layer (Theorem A7.3) **and the conic layer (Theorem A7.6)** are
  completely classified — no genus ≤ 1 curve on $X$ has line image
  beyond the three degenerate families, and none has conic image at
  all, so every genus ≤ 1 curve has plane image of degree ≥ 3 (char 0);
  the resolution's
  invariants are computed ($K^2 = 576$, $c_2 = 768$, $\chi(\mathcal{O})
  = 112$, $s_2 = -192 < 0$ — the hyperbolicity is carried by the 256
  nodes) and confirmed against BTVA's complete-intersection Chern
  formulas (A7 §7), and their magic-square bounds ($m \ge 47$,
  $h^0 \ge 8448$) are exactly reproduced from our invariants. The paper itself contains no
  enumeration for $X$ and calls the explicit-differentials route out of
  computational range there — P3 remains open and non-duplicative.* This single computation would: (i) settle Conjecture A2.C
  over $\bar{\mathbb{Q}}$ (no nondegenerate rational curves = no
  function-field solutions), and (ii) reduce the rational-point question
  to genus-$\ge 2$ curves + finitely many sporadic points, i.e. prove
  "all but finitely many magic squares of squares are degenerate"
  unconditionally... conditional today only on completing the
  enumeration. In our judgment, jointly with A2-T1 (the same task seen
  from function fields), this is the most valuable open computation in
  the problem's orbit.
- **P4 (Cain's reformulation — CITED pointer).** O. Cain
  (arXiv:1908.03236) recasts the problem as quartics with factorization
  constraints over abelian extensions of $\mathbb{Q}$ and derives
  search methods; we could not obtain the primary source
  (SUMMARY-ONLY), so we record it as a direction to be reconciled with
  the F2/A3 congrua framework once readable.

## 5. What the verify script proves mechanically

`verify/checks/a5_surface.py`: the rank-6 computation (exact, over
$\mathbb{Q}$); the smoothness criterion's rank identity at sample
nonvanishing points mod $p$; the arrangement combinatorics
($t_2, t_3) = (12, 8)$ with the triple points as listed; the
$\mathbb{F}_p$ point-count table; divisibility by 64; and the emptiness
of the nondegenerate locus for $p < 59$ (cross-reference to `f5.fp_scan`).
