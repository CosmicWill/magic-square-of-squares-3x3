# References, with provenance flags

Because this working environment cannot fetch most primary sources (general
web fetching is proxy-blocked; PyPI/apt only), we flag every reference
honestly:

- **READ** — primary source read in full here. *(None yet; flag exists so the
  ledger can improve.)*
- **SUMMARY-ONLY** — content known through search-result summaries and
  secondary descriptions; theorem statements from these are never
  load-bearing for this repository's PROVEN claims (we reprove what we need).
- **EXISTENCE-VERIFIED** — we confirmed the work exists (title/author/venue),
  nothing more.
- **VERIFIED-OBJECT** — a specific mathematical object from the source
  (e.g. a numerical square) that we have re-verified computationally here,
  independent of the source's text.

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
| C. Woll, "A partial residue categorization of the magic square of squares," arXiv:1809.03067 (2018). | EXISTENCE-VERIFIED |

## Near-misses and elliptic-curve analyses

| Ref | Provenance |
|---|---|
| A. Bremner, "On squares of squares," *Acta Arith.* 88 (1999) 289–297; "…II," *Acta Arith.* 99 (2001) 289–308. | SUMMARY-ONLY |
| Bremner–Sallows 7-square example **AB1** (magic sum 541875). | **VERIFIED-OBJECT** — re-verified in `verify/checks/f6_known_squares.py` |
| L. Euler, 4×4 magic square of squares (letter to Lagrange, 1770), magic sum 8515. | **VERIFIED-OBJECT** — re-verified in `verify/checks/f6_known_squares.py` |
| R. Rathbun: enumeration of >1.16×10⁸ magic squares with ≥6 square entries; no new ≥7. | SUMMARY-ONLY |
| L. Morgenstern (2007): any MSS3 has all entries ≥ 10¹⁴ (multimagie.com search page). | SUMMARY-ONLY |
| O. M. Cain, "Gaussian integers, rings, finite fields, and the magic square of squares," arXiv:1908.03236 (2019). | SUMMARY-ONLY |
| C. Wolird, "A new transformation of the magic square of squares," arXiv:2310.12164 (2023). | EXISTENCE-VERIFIED |

## Local solubility (why congruence proofs cannot win)

| Ref | Provenance |
|---|---|
| L. Morgenstern, "Magic squares of squares modulo 2^N" (multimagie.com, 2012): explicit solutions mod 2^N up to 2⁹⁰. | SUMMARY-ONLY (reproduced independently in miniature in [F5](foundations/F5-local-solubility.md)) |
| G. Labruna, *Magic squares of squares of order three over finite fields*, M.S. thesis, Montclair State (2018); journal version. | SUMMARY-ONLY (𝔽_p solutions found independently here, [F5](foundations/F5-local-solubility.md)) |

## Geometry and the modern viewpoint

| Ref | Provenance |
|---|---|
| N. Bruin, J. Thomas, A. Várilly-Alvarado, "Explicit computation of symmetric differentials and its application to quasi-hyperbolicity," *Algebra & Number Theory* 16 (2022) 1377–1405; arXiv:1912.08908. Magic-square-of-squares surface is algebraically quasi-hyperbolic (finitely many curves of genus ≤ 1). | SUMMARY-ONLY |
| A. Várilly-Alvarado, "The geometric disposition of Diophantine equations," *Notices AMS* (2021). | SUMMARY-ONLY |
| N. Rome, S. Yamagishi, "On the existence of magic squares of powers," arXiv:2406.09364; *Research in Number Theory* (2025). n×n magic squares of squares exist for all n ≥ 4; **n = 3 is the only open order**. | SUMMARY-ONLY |
| D. Flores, "Existence of K-multimagic squares…," arXiv:2411.01091. | EXISTENCE-VERIFIED |
| S. D. Kominers, "Center-zero magic squares of squares over number fields" (recent; venue unconfirmed). Solutions over ℚ(i,√n); degree 4 minimal. | SUMMARY-ONLY |

## Curve enumeration & effective hyperbolicity (Front 1 / A7; added 2026-08-26)

| Ref | Provenance |
|---|---|
| M. Stoll, D. Testa, "The surface parametrizing cuboids," arXiv:1009.0388 (2010). Picard lattice + curve enumeration on the sister (cuboid) surface — the worked template. | SUMMARY-ONLY |
| K. Horie, T. Yamauchi, "The L-function of the surface parametrizing cuboids," arXiv:2512.22520 (2025). Full Picard Galois module of that surface. | EXISTENCE-VERIFIED |
| S. Lu, Y. Miyaoka, "Bounding curves in algebraic surfaces by genus and Chern numbers," Math. Res. Lett. 2 (1995) 663–676. | SUMMARY-ONLY |
| Y. Miyaoka, "The orbibundle Miyaoka–Yau–Sakai inequality and an effective Bogomolov–McQuillan theorem," Publ. RIMS 44 (2008) 403–417. Effective canonical-degree bounds with orbifold ($A_1$) contributions. | SUMMARY-ONLY |
| F. Hirzebruch, "Arrangements of lines and algebraic surfaces," Progr. Math. 36 (1983) 113–140; Barthel–Hirzebruch–Höfer, Vieweg (1987). Cover invariants from arrangement combinatorics. | SUMMARY-ONLY |
| P. Pokora, "Hirzebruch-type inequalities viewed as tools in combinatorics," Electron. J. Combin. 28 (2021); G. Urzúa, J. Alg. Geom. 19 (2010) 335–365. Practical formula sources. | EXISTENCE-VERIFIED |
| N. Bruin, N. Ilten, Z. Xu, "Local Euler characteristics of $A_n$-singularities and their application to hyperbolicity," EPIGA 9 (2025), arXiv:2312.01722. The $A_1$-node toolkit. | SUMMARY-ONLY |
| BTVA ancillary Magma code, `arxiv.org/src/1912.08908/anc` (per N. Bruin's SFU publications page). | EXISTENCE-VERIFIED (unfetched) |

## Claimed proofs (unaccepted; audited here)

| Ref | Provenance |
|---|---|
| J. C. Ferreira, arXiv:1506.06621 (2015, math.GM). Claimed nonexistence proof; not accepted. | EXISTENCE-VERIFIED |
| O. Hill, arXiv:2510.08286 (Oct 2025, math.GM), "On arithmetic progressions and a proof of the nonexistence of magic squares of squares." Claimed nonexistence proof; no public refutation or endorsement found. **Audited in [attacks/A1-hill-audit.md](attacks/A1-hill-audit.md).** | SUMMARY-ONLY |

## Classical ingredients (reproved where used)

| Ref | Provenance |
|---|---|
| Fermat/Euler: no four distinct squares in arithmetic progression. | PROVEN from scratch in [F3](foundations/F3-no-four-term-ap.md) |
| Fermat: no congruum is a perfect square (right-triangle theorem). | Stated where used; classical |
| H. Darmon, L. Merel, "Winding quotients and some variants of Fermat's Last Theorem" (1997): $x^n + y^n = 2z^n$ has no nontrivial solutions for $n \ge 3$. Kills the 4th-power analogue instantly; silent for squares. | SUMMARY-ONLY |
| Mason–Stothers theorem (polynomial abc). | PROVEN from scratch in [attacks/A2-function-field.md](attacks/A2-function-field.md) |
