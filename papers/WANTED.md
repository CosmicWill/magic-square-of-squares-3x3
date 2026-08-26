# WANTED — sources to acquire, in priority order

Compiled 2026-08-26 after the Front-1 state-of-the-field sweep (~35
searches; see RESEARCH_LOG entry 8). **P1 is the single most important
item.** Everything here is currently known to us only through search
snippets.

## P1 — the load-bearing paper (and its code)

**Bruin, Thomas, Várilly-Alvarado — "Explicit computation of symmetric
differentials and its application to quasi-hyperbolicity"**
- arXiv PDF (v3, Oct 2021): https://arxiv.org/pdf/1912.08908
- **Ancillary files (Magma code!)**: https://arxiv.org/src/1912.08908/anc
  — downloads as a tarball; per Nils Bruin's SFU publications page the
  Magma code for the paper lives here, *not* on GitHub. Please grab the
  whole thing.
- Published version (nice-to-have): Algebra & Number Theory 16 (2022)
  1377–1405, doi:10.2140/ant.2022.16.1377.

*Why:* we need (a) the actual statement of what the paper proves about
the magic-squares surface (a snippet hints at a "Theorem 1.5" with a
"hyperplane section / ≥ 6 singularities" clause — unconfirmed), (b) their
model of X and node analysis (256 nodes?), (c) whether any effective
bound hides in the body (their method is Jouanolou-finiteness, so we
expect NOT), (d) whether the ancillary Magma covers the magic-square
case or only Barth/cuboid.

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

## P5 — cover-invariant formulas (to certify our stratification numbers)

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
