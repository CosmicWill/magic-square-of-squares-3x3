# WANTED — sources to acquire, in priority order

Compiled 2026-08-26 after the Front-1 state-of-the-field sweep (~35
searches; see RESEARCH_LOG entry 8). Everything here is currently known
to us only through search snippets, except where marked ACQUIRED.

## P1 — the load-bearing paper (and its code) — ✅ ACQUIRED 2026-08-26

**Bruin, Thomas, Várilly-Alvarado — "Explicit computation of symmetric
differentials and its application to quasi-hyperbolicity"**
- ✅ arXiv **source** tarball v3 *including the ancillary Magma files*,
  uploaded by the repository owner; archived in
  [`papers/1912.08908/`](1912.08908/) and digested (provenance now
  **READ** in `docs/references.md`; reproductions in
  `verify/checks/a7_btva.py`).
- Answers to the four questions we posed: (a) the snippet's
  "Theorem 1.5" is the **perfect-cuboid** theorem (`thm:CuboidIntro`),
  *not* about the magic-square surface — for $X_{\mathrm{ms}}$ the paper
  proves bare quasi-hyperbolicity (`thm:magicsquares`) plus the bound
  $h^0(S^{47}\Omega^1) \ge 8448$, nothing about node passage; (b) their
  model is our model (7 line-sum equations in ℙ⁸) and they state 256
  ordinary double points, matching our derivation; (c) **no** effective
  curve-degree bound anywhere in the body — Jouanolou finiteness, as
  expected, and they say $X_{\mathrm{ms}}$ is "out of range of current
  computational techniques" for the explicit method; (d) the ancillary
  Magma covers **only** Barth's sextic and the cuboid — no magic-square
  script exists.
- Published version (nice-to-have, for page-numbered citations only):
  Algebra & Number Theory 16 (2022) 1377–1405,
  doi:10.2140/ant.2022.16.1377.

## P1.5 — NEW top priority after the BTVA digest (2026-08-26)

**García-Fritz & Urzúa — "Families of explicit quasi-hyperbolic and
hyperbolic surfaces"**, Math. Z. (cited by BTVA as "to appear"; search
by exact title — an arXiv version should exist, and Urzúa's UC Chile
page lists his papers).

*Why (this is now the load-bearing item):* BTVA's cuboid theorem is
powered by a symmetric differential **descended to the base plane**
(their $\omega_7 = \phi^*(\eta)/(y_1y_2y_3z^2)$), and they credit this
cyclic-cover viewpoint to García-Fritz–Urzúa, who proved "every genus
≤ 1 curve on the cuboid surface passes through ≥ 2 nodes" that way.
Our M11 plan (A7 roadmap item 2) is exactly the magic-square analogue
on the Lucas plane — their paper is the worked method.

## P2 — free expository anchor

**Várilly-Alvarado — "The geometric disposition of Diophantine
equations"**, Notices AMS 68 (2021) 1291–1300. Free:
- https://www.ams.org/journals/notices/202108/rnoti-p1291.pdf
- mirror: https://par.nsf.gov/servlets/purl/10339137

*Why:* the citable source for "6 quadrics in ℙ⁸" and the "256 ordinary
double points" claim we have independently derived and want to confirm.

## P3 — the worked template on the sister surface

- **Stoll & Testa — "The surface parametrizing cuboids"**:
  https://arxiv.org/abs/1009.0388 (also
  http://ftp.mathe2.uni-bayreuth.de/stoll/papers/Cuboidi-2010-09-02.pdf)
- **Horie & Yamauchi — "The L-function of the surface parametrizing
  cuboids"**: https://arxiv.org/abs/2512.22520

*Why:* Stoll–Testa did for the perfect-cuboid surface exactly what we
want for X: resolve the nodes, compute Pic with Galois action, enumerate
low-degree classes, identify the 32 known conics. Our M10 would follow
their playbook step by step.

## P4 — the effective-bound machinery

- **Lu & Miyaoka — "Bounding curves in algebraic surfaces by genus and
  Chern numbers"**, Math. Res. Lett. 2 (1995) 663–676:
  https://intlpress.com/site/pub/files/_fulltext/journals/mrl/1995/0002/0006/MRL-1995-0002-0006-a001.pdf
- **Miyaoka — "The orbibundle Miyaoka–Yau–Sakai inequality and an
  effective Bogomolov–McQuillan theorem"**, Publ. RIMS 44 (2008)
  403–417: https://www.kurims.kyoto-u.ac.jp/~prims/pdf/44-2/44-2-15.pdf

*Why:* our planning-stage computation (to be code-verified this
milestone) gives the **resolution** of X the invariants K² = 576,
χ_top = 768 — i.e. c₁² − c₂ = −192 < 0, so the *naive* Bogomolov route
fails and the hyperbolicity genuinely lives in the 256 nodes. Miyaoka's
orbifold version (nodes contribute) is then the natural effective tool;
we need its exact hypotheses and constants.

## P5 — cover-invariant formulas *(priority LOWERED 2026-08-26: our
stratification numbers are now independently certified by BTVA's
complete-intersection Chern formulas, so these are context, not
load-bearing)*

- **Hirzebruch — "Arrangements of lines and algebraic surfaces"**,
  Progr. Math. 36 (1983) 113–140; free scan:
  https://hirzebruch.mpim-bonn.mpg.de/id/eprint/244/
- Practical modern sources: **Pokora** https://arxiv.org/abs/1808.09167 ;
  **"On algebraic surfaces associated to line arrangements"**
  https://arxiv.org/abs/1612.06730 ; **Urzúa**, J. Alg. Geom. 19 (2010).
- (Book, if easy: Barthel–Hirzebruch–Höfer, *Geradenkonfigurationen und
  algebraische Flächen*, Vieweg 1987.)

## P6 — current-generation node toolkit

**Bruin, Ilten, Xu — "Local Euler characteristics of A_n-singularities
and their application to hyperbolicity"**, EPIGA 9 (2025), open access:
https://epiga.episciences.org/15201 (arXiv:2312.01722).

*Why:* applies verbatim (n = 1) to our 256 A₁ points; the modern way to
quantify how much hyperbolicity the nodes buy.

## P7 — backlog from earlier milestones (unblocks other fronts)

- **Bremner — "On squares of squares"** I: Acta Arith. 88 (1999)
  289–297 (https://eudml.org/doc/207247); II: Acta Arith. 99 (2001)
  289–308. *(Unblocks: the 8-square front A4's configuration
  cross-check.)*
- **Kominers — center-zero paper**:
  https://www.scottkom.com/assets/articles/Kominers_Center-Zero_Magic_Squares.pdf
  *(Confirms/refines our independently derived A3.K.)*
- **Hill — arXiv:2510.08286** (https://arxiv.org/pdf/2510.08286).
  *(Unblocks the pending A1 re-audit of the claimed proof.)*
- **Rome & Yamagishi — arXiv:2406.09364** (https://arxiv.org/pdf/2406.09364).
- Morgenstern / Boyer pages (save-as-PDF of
  http://www.multimagie.com/English/SquaresOfSquaresSearch.htm and
  .../Morgenstern17.htm). *(Turns the CITED search bounds into READ.)*
