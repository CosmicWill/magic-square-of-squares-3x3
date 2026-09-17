# References, with provenance flags

Because this working environment cannot fetch most primary sources (general
web fetching is proxy-blocked; PyPI/apt only), we flag every reference
honestly:

- **READ** — primary source read in full here (uploaded by the
  repository owner into [papers/](../papers/) when the proxy blocks
  direct fetching).
- **SUMMARY-ONLY** — content known through search-result summaries and
  secondary descriptions; theorem statements from these are never
  load-bearing for this repository's PROVEN claims (we reprove what we need).
- **EXISTENCE-VERIFIED** — we confirmed the work exists (title/author/venue),
  nothing more.
- **VERIFIED-OBJECT** — a specific mathematical object from the source
  (e.g. a numerical square) that we have re-verified computationally here,
  independent of the source's text.
- **ACQUIRED** — primary-source PDF is in [papers/](../papers/) but not
  yet digested here; theorem statements from it are not yet load-bearing.
  (Most ACQUIRED tags date to the 2026-08-28 full-access sweep,
  RESEARCH_LOG entry 30.)

## Problem origin and surveys

| Ref | Provenance |
|---|---|
| M. LaBar, problem proposal, *College Mathematics Journal* (1984). | EXISTENCE-VERIFIED |
| R. K. Guy, *Unsolved Problems in Number Theory*, 2nd ed., problem D15 (1994). | SUMMARY-ONLY |
| M. Gardner, prize announcement, *Quantum* (1996); $100 prize, unclaimed. | SUMMARY-ONLY |
| C. Boyer, "Some notes on the magic squares of squares problem," *Math. Intelligencer* 27(2) (2005) 52–64; prizes at multimagie.com. | SUMMARY-ONLY |
| Numberphile, "The Parker Square" (2016) and "Magic Squares of Squares (are PROBABLY impossible)" with T. Várilly-Alvarado (2023). | SUMMARY-ONLY |

## Structural / congruence results

| Ref | Provenance |
|---|---|
| É. Lucas (1876): classical parametrization of 3×3 magic squares. | SUMMARY-ONLY (reproved from scratch in [F1](foundations/F1-parametrization.md)) |
| L. W. Rabern, "Properties of magic squares of squares," *Rose-Hulman Undergrad. Math. J.* 4(1) (2003), art. 3. | SUMMARY-ONLY |
| T. Pierrat, C. Thiriet, P. Zimmermann, "Magic squares of squares" (2015): primitive ⇒ entries ≡ 1 (mod 24), magic sum ≡ 3 (mod 72). | SUMMARY-ONLY (reproved from scratch in [F4](foundations/F4-congruences-mod-72.md)) |
| D. Weisenberg, "Some thoughts on the 3×3 magic square of squares problem," *Rose-Hulman Undergrad. Math. J.* 24(1) (2023), art. 7. | SUMMARY-ONLY |
| C. Woll, "A partial residue categorization of the magic square of squares," arXiv:1809.03067 (2018). | **ACQUIRED** 2026-08-28 (PDF in papers/) |

## Near-misses and elliptic-curve analyses

| Ref | Provenance |
|---|---|
| A. Bremner, "On squares of squares," *Acta Arith.* 88 (1999) 289–297; "…II," *Acta Arith.* 99 (2001) 289–308. | **ACQUIRED** 2026-08-28 (both PDFs in papers/); digest pending — unblocks A4 cross-check |
| Bremner–Sallows 7-square example **AB1** (magic sum 541875). | **VERIFIED-OBJECT** — re-verified in `verify/checks/f6_known_squares.py` |
| L. Euler, 4×4 magic square of squares (letter to Lagrange, 1770), magic sum 8515. | **VERIFIED-OBJECT** — re-verified in `verify/checks/f6_known_squares.py` |
| R. Rathbun: enumeration of >1.16×10⁸ magic squares with ≥6 square entries; no new ≥7. | SUMMARY-ONLY (source pages archived in papers/multimagie/, 2026-08-28) |
| L. Morgenstern (2007): any MSS3 has all entries ≥ 10¹⁴ (multimagie.com search page). | **ACQUIRED** 2026-08-28 — pages saved to papers/multimagie/; digest pending (turns the CITED bounds into READ) |
| O. M. Cain, "Gaussian integers, rings, finite fields, and the magic square of squares," arXiv:1908.03236 (2019). | **ACQUIRED** 2026-08-28 (PDF in papers/) |
| C. Wolird, "A new transformation of the magic square of squares," arXiv:2310.12164 (2023). | **ACQUIRED** 2026-08-28 (PDF in papers/) |

## Local solubility (why congruence proofs cannot win)

| Ref | Provenance |
|---|---|
| L. Morgenstern, "Magic squares of squares modulo 2^N" (multimagie.com, 2012): explicit solutions mod 2^N up to 2⁹⁰. | SUMMARY-ONLY (reproduced independently in miniature in [F5](foundations/F5-local-solubility.md)) |
| G. Labruna, *Magic squares of squares of order three over finite fields*, M.S. thesis, Montclair State (2018); journal version. | SUMMARY-ONLY (𝔽_p solutions found independently here, [F5](foundations/F5-local-solubility.md)) |

## Geometry and the modern viewpoint

| Ref | Provenance |
|---|---|
| N. Bruin, J. Thomas, A. Várilly-Alvarado, "Explicit computation of symmetric differentials and its application to quasi-hyperbolicity," *Algebra & Number Theory* 16 (2022) 1377–1405; arXiv:1912.08908. Magic-square-of-squares surface is algebraically quasi-hyperbolic (finitely many curves of genus ≤ 1). | **READ** (v3 source in [papers/1912.08908/](../papers/1912.08908/); magic-square numbers independently reproduced, `verify/checks/a7_btva.py`; digest in [A7 §7](attacks/A7-curve-enumeration.md)) |
| A. Várilly-Alvarado, "The geometric disposition of Diophantine equations," *Notices AMS* 68 (2021) 1291–1300. | **ACQUIRED** 2026-08-28 (PDF in papers/); the citable source for "6 quadrics in ℙ⁸" / 256 nodes |
| N. Rome, S. Yamagishi, "On the existence of magic squares of powers," arXiv:2406.09364; *Res. Number Theory* **11:91 (2025)**. n×n magic squares of squares exist for all n ≥ 4; **n = 3 is the only open order**. | **ACQUIRED** 2026-08-28 (arXiv v2 + published PDF in papers/); digest pending |
| D. Flores, "Existence of K-multimagic squares…," arXiv:2411.01091; *Bull. Aust. Math. Soc.* | **ACQUIRED** 2026-08-28 (PDF in papers/) |
| S. D. Kominers, "Center-zero magic squares of squares over number fields" (scottkom.com). Solutions over ℚ(i,√n); degree 4 minimal. | **ACQUIRED** 2026-08-28 (PDF in papers/); digest pending — A3.K cross-check |

## Curve enumeration & effective hyperbolicity (Front 1 / A7; added 2026-08-26)

| Ref | Provenance |
|---|---|
| M. Stoll, D. Testa, "The surface parametrizing cuboids," arXiv:1009.0388**v2** (updated 2025). Picard lattice ($\rho = 64$ maximal, disc $-2^{28}$), Aut (order 1536), Brauer group, all curves with $C\cdot K \le 6$; Lemma 21: rational non-conic $C\cdot E \ge 8$, genus-1 $\ge 4$. | **READ** (PDF in [papers/](../papers/); intro + main theorems digested; lattice details on demand) |
| K. Horie, T. Yamauchi, "The L-function of the surface parametrizing cuboids," arXiv:2512.22520v3 (2026). Full $L$-function and $\operatorname{Pic}(\bar S)$ as Galois module. | **READ** (PDF in papers/; main theorem digested) |
| S. Lu, Y. Miyaoka, "Bounding curves in algebraic surfaces by genus and Chern numbers," Math. Res. Lett. 2 (1995) 663–676. Effective $CK$ bounds — requires $K^2 > c_2$. | **READ** (PDF in papers/; main theorems digested — hypotheses FAIL for $X$: $576 < 768$, see A8 §1) |
| Y. Miyaoka, "The orbibundle Miyaoka–Yau–Sakai inequality and an effective Bogomolov–McQuillan theorem," Publ. RIMS 44 (2008) 403–417. Orbibundle MYS inequality; $CK \le a(g-1)+b$ when $K^2 > c_2$. | **READ** (PDF in papers/; main theorems digested — orbifold-corrected $c_2 = 640 > 576 = K^2$ still fails for $X$, A8 §1) |
| F. Hirzebruch, "Arrangements of lines and algebraic surfaces," Progr. Math. 36 (1983) 113–140; Barthel–Hirzebruch–Höfer, Vieweg (1987). Cover invariants from arrangement combinatorics. | **ACQUIRED** 2026-08-28 (MPIM eprint scan in papers/); context only — stratification numbers independently certified |
| P. Pokora, "Hirzebruch-type inequalities viewed as tools in combinatorics," Electron. J. Combin. 28 (2021), arXiv:1808.09167; "On algebraic surfaces associated to line arrangements," arXiv:1612.06730; G. Urzúa, J. Alg. Geom. 19 (2010) 335–365. Practical formula sources. | **ACQUIRED** 2026-08-28 (both arXiv PDFs in papers/); Urzúa JAG still EXISTENCE-VERIFIED |
| N. Bruin, N. Ilten, Z. Xu, "Local Euler characteristics of $A_n$-singularities and their application to hyperbolicity," EPIGA 9 (2025), arXiv:2312.01722. Wahl local Euler characteristics for all $A_n$; explicit-regular-differential machinery. | **READ** (PDF in papers/; framework digested; $n=1$ case already reproduced in `a7btva.*`) |
| BTVA ancillary Magma code, `arxiv.org/src/1912.08908/anc` (per N. Bruin's SFU publications page). | **READ** (acquired with the source, [papers/1912.08908/anc/](../papers/1912.08908/anc/): Barth sextic + perfect cuboid **only** — no magic-square script) |
| J. Wahl, "Second Chern class and Riemann–Roch for vector bundles on resolutions of surface singularities," Math. Ann. 295 (1993) 81–110. Local $\chi^0/\chi^1$ framework used by BTVA. | SUMMARY-ONLY (used through BTVA's statements, which we re-verified numerically) |
| N. García-Fritz, G. Urzúa, "Families of explicit quasi-hyperbolic and hyperbolic surfaces," arXiv:1804.07671; Math. Z. Vojta-method towers of cyclic covers branched on $\omega$-integral curves; toric local calculus; cuboid: genus ≤ 1 ⟹ ≥ 2 nodes, rational non-conic $C\cdot E \ge 8$. | **READ in full** (PDF in [papers/](../papers/); the method source for [A8](attacks/A8-descent-differentials.md)) |

## Discrete spheres, class groups, composition (Front 2 / A9; added 2026-08-28)

| Ref | Provenance |
|---|---|
| W. Duke, "Hyperbolic distribution problems and half-integral weight Maass forms," *Invent. Math.* 92 (1988) 73–90. Equidistribution of lattice points on spheres (Linnik's problem). | **ACQUIRED** (author's PDF in papers/); descriptive use |
| W. Duke, "An introduction to the Linnik problems" (expository survey). | **ACQUIRED** (author's PDF in papers/) |
| M. Aka, M. Einsiedler, U. Shapira, "Integer points on spheres and their orthogonal lattices," arXiv:1502.04209; *Invent. Math.* 206 (2016) 379–396. | **ACQUIRED** (PDF in papers/); descriptive use |
| J. Ellenberg, P. Michel, A. Venkatesh, "Linnik's ergodic method and the distribution of integer points on spheres," arXiv:1001.0897. The modern exposition of the Venkov/class-group parametrization of $S(n)$ — the A9-T1 input. | **ACQUIRED** (PDF in papers/); digest pending — the P8 anchor |
| R. Schulze-Pillot, "Representation by integral quadratic forms — a survey" (2004). Genus/spinor-genus representation theory. | **ACQUIRED** (PDF in papers/); digest pending — the A9 composition-frontier reference |
| Spinor-genus structure papers: A. G. Earnest, A. Haensch et al., completeness of spinor-regular ternary list, arXiv:1711.05811; exceptional sets, arXiv:2203.02620; spinor genera of lattice cosets, arXiv:2104.08798. | **ACQUIRED** (PDFs in papers/); the precise-question toolkit for "which classes inside a genus represent" |
| "Average representation numbers for spinor genera," arXiv:math/0509484. | EXISTENCE-VERIFIED (fetch failed 2026-08-28; still wanted) |

## New in the field, 2025–2026 (found in the 2026-08-28 sweep)

| Ref | Provenance |
|---|---|
| N. Bruin, B. Creutz, "Explicit Brauer–Manin obstructions on plane quartics," arXiv:2601.16975 (2026). Worked modern template for explicit Brauer–Manin computations — relevant to the A8 arithmetic endgame. | **ACQUIRED** (PDF in papers/); digest pending |
| D. Thanos, M. Bonsangue, A. Laarman, "Quantum algorithms for magic square Diophantine equations," arXiv:2605.04106 (2026). Periodicity/QFT viewpoint on magic-square constraint systems; does not address the n = 3 squares existence question. | **ACQUIRED** (PDF in papers/); tangential |
| "Quartic reductions and elliptic obstructions for perfect Euler bricks," arXiv:2604.09328 (2026). Cuboid-adjacent. | **ACQUIRED** (PDF in papers/); context |
| "There are infinitely many Hilbert cubes of dimension 3 in the set of squares," arXiv:2604.05459 (2026). Additive structure of the squares — adjacent to F2/F3 territory. | **ACQUIRED** (PDF in papers/); context |
| Field-status checks 2026-08-28: Várilly-Alvarado CV (Aug 2026) and N. Bruin's publication page list **nothing new** on the magic-square or cuboid surfaces beyond BTVA 2022 and Bruin–Ilten–Xu 2025; the problem remains open on all status pages; prizes unclaimed. | checked directly |

## Claimed proofs (unaccepted; audited here)

| Ref | Provenance |
|---|---|
| J. C. Ferreira, arXiv:1506.06621 (2015, math.GM). Claimed nonexistence proof; not accepted. | EXISTENCE-VERIFIED |
| O. Hill, arXiv:2510.08286 (math.GM; v1 Oct 2025, v2 Oct 2025, **v3 Apr 2026**), "On arithmetic progressions and a proof of the nonexistence of magic squares of squares." Claimed nonexistence proof; as of 2026-08-28 still math.GM, no public refutation, no endorsement, no journal acceptance. **Formally refuted here, [A1 §7](attacks/A1-hill-audit.md)** (2026-08-28): its eq. (29) is an identity-multiple of its own Lemma-3.2 constraint; the final coefficient-comparison inference fails on an explicit six-square witness. First refutation we are aware of anywhere. | **READ** (v3 PDF in papers/, read in full; refutation machine-verified, `a1.eq29_*`) |

## Classical ingredients (reproved where used)

| Ref | Provenance |
|---|---|
| Fermat/Euler: no four distinct squares in arithmetic progression. | PROVEN from scratch in [F3](foundations/F3-no-four-term-ap.md) |
| Fermat: no congruum is a perfect square (right-triangle theorem). | Stated where used; classical |
| H. Darmon, L. Merel, "Winding quotients and some variants of Fermat's Last Theorem" (1997): $x^n + y^n = 2z^n$ has no nontrivial solutions for $n \ge 3$. Kills the 4th-power analogue instantly; silent for squares. | SUMMARY-ONLY |
| Mason–Stothers theorem (polynomial abc). | PROVEN from scratch in [attacks/A2-function-field.md](attacks/A2-function-field.md) |
| A. Auel, B. Singer, "The algebraic geometry of 3×3 magic squares of squares," [arXiv:2609.09351v1](https://arxiv.org/html/2609.09351v1) (8 Sep 2026). Surface invariants, automorphisms, coordinate projections and a proposed Picard-rank bound. **Entry 148:** an exact Hodge-index witness shows that the archived matrix does not establish the claimed lower bound 518; see [A3 §2.70](attacks/A3-simultaneous-congrua.md#270-picard-module-bookkeeping-and-an-exact-intersection-matrix-obstruction-entry-148). | READ (introduction, Theorem 3, §§4.2 and 5); `papers/2609.09351-auel-singer.pdf` |
| D. Morrison, "On K3 surfaces with large Picard number," Invent. Math. 75 (1984). A complex K3 surface of Picard rank $\ge 19$ admits a Shioda–Inose structure (its transcendental lattice is that of an abelian surface, $E\times E'$ for rank 19/20). Used in entry 147 for the reading of the Frobenius polynomials of the K3 pieces. | SUMMARY-ONLY |
| R. Livné, "Motivic orthogonal two-dimensional representations of $\mathrm{Gal}(\bar{\mathbb Q}/\mathbb Q)$," Israel J. Math. 92 (1995). A singular K3 surface over $\mathbb Q$ has a modular transcendental lattice: a weight-3 newform with CM. Entry 147: the pieces B–F. | SUMMARY-ONLY |
| M. Schütt, "K3 surfaces with Picard rank 20 over $\mathbb Q$," Algebra & Number Theory 4 (2010). The singular K3 surfaces over $\mathbb Q$ are those whose transcendental lattice has discriminant $d$ with 2-elementary class group $\mathrm{Cl}(-d)$; in particular CM by $\mathbb Q(\sqrt{-6})$ (class number 2) occurs. Entry 147: the piece F, attached to the weight-3 form of level 24 rather than to any elliptic curve. | SUMMARY-ONLY |
| N. Elkies, M. Schütt, "Modular forms and K3 surfaces," Adv. Math. 240 (2013). K3 surfaces over $\mathbb Q$ of Picard rank 19: the transcendental representation is $\operatorname{Sym}^2$ of the representation of a weight-2 newform up to twist, an elliptic curve over $\mathbb Q$ only when the Shioda–Inose structure descends; otherwise a $\mathbb Q$-curve. Entry 147: the five classes of rank 19 not attached to a curve over $\mathbb Q$. | SUMMARY-ONLY |
| B. Singer, [companion repository to Auel–Singer](https://github.com/BenSinger2005/A-Geometric-Approach-to-3-x-3-Magic-Squares-of-Squares). `IntersectionMatrix.m`, archived with its full SHA-256 in `papers/auel-singer-2026/`. Entry 148: a principal minor has two positive directions, contradicting its interpretation as a divisor Gram matrix. | READ; source bytes and exact witness replayed by `a3.picard_module_148`; full rational congruence available via `compute.picard_matrix_audit --full` |
## Independent global-obstruction track (2026-09-10)

These sources support explicitly CITED deductions in
[GB.3--GB.8](research/global-obstructions.md), not a headline impossibility proof.

| Ref | Provenance |
|---|---|
| J. B. Tunnell, "A Classical Diophantine Problem and Modular Forms of Weight 3/2," Invent. Math. 72 (1983), 323--334. [Original scan](https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf). | **READ**, printed pp.323--325 visually inspected. The unconditional necessary condition and its ternary counts are used in GB.8; modular-form proof CITED. |
| Stacks Project, [Theorem 54.14.5](https://stacks.math.columbia.edu/tag/0BGP), [surface-resolution introduction](https://stacks.math.columbia.edu/tag/0ADX). | **READ**, statements and context; resolution existence in GB.8 is CITED. No explicit blowup sequence computed. |
| PARI/GP, [elliptic-curve manual](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Elliptic_curves.html), ellfromeqn, ellrank, elltors. | **READ**, relevant entries; version 2.17.4 run. Independent diagnostic in GB.8, not a dependency of the exclusion. |
| J.-L. Colliot-Thelene, A. N. Skorobogatov, [The Brauer--Grothendieck Group, author manuscript](https://www.imo.universite-paris-saclay.fr/~jean-louis.colliot-thelene/BGgroup_book.pdf). | **READ**, relevant portions of sections 9.5.1, 12.6 and 1.5; formal lemma and local constancy CITED in GB.3. |
| D. Harari, "Methode des fibrations et obstruction de Manin," Duke Math. J. 75 (1994), 221--260. [Author PDF](https://www.imo.universite-paris-saclay.fr/~david.harari/articles/duke.pdf). | **READ**, formal lemma 2.6.1 and local-density discussion. Original source behind GB.3. |

## Nonlinear divisor-fiber audit (2026-09-14)

These inputs support the explicitly CITED geometric deductions in
[ND.3--ND.4](research/nonlinear-descent-fibers.md). The polynomial branch
certificates and reciprocity identities are checked separately in-repo.

| Ref | Provenance |
|---|---|
| Stacks Project, [Section 53.12, Riemann--Hurwitz, Lemma 53.12.2](https://stacks.math.columbia.edu/tag/0C1B). | **READ** 2026-09-14, formula, hypotheses and proof discussion; used for genus and map degree. |
| Stacks Project, [Section 53.2, Lemma 53.2.2](https://stacks.math.columbia.edu/tag/0BXX). | **READ** 2026-09-14; rational maps from normal curves to proper varieties extend to morphisms. |
| A. Sutherland, [MIT 18.783 Lecture 5 slides, 14 February 2022](https://math.mit.edu/classes/18.783/2022/LectureSlides5.pdf#page=24). | **READ** 2026-09-14, final-slide degree and separability statement for multiplication-by-n; degree n^2 remains CITED. |
