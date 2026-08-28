# papers/ — acquired primary sources

*(Historical note: the original cloud working environment could not fetch
most of the web — the egress proxy allowed only PyPI, apt, and GitHub git
traffic — so literature knowledge was SUMMARY-ONLY unless a primary source
landed in this directory. On 2026-08-28 the program ran on the owner's
local machine with full web access and cleared the entire WANTED backlog;
see RESEARCH_LOG entry 29.)

**Workflow:**

1. [WANTED.md](WANTED.md) lists the sources we need, in priority order,
   with exact IDs and links.
2. Drop the PDFs (and any ancillary tarballs/code) into this directory,
   named like `1912.08908v3.pdf`, `1912.08908-anc.tar.gz`,
   `stoll-testa-1009.0388.pdf` — any reasonable name works; keep the
   arXiv ID or author-year visible.
3. Commit/push (or just tell Claude they're here). Each source is then
   read and digested: its provenance flag in `docs/references.md` is
   upgraded from SUMMARY-ONLY to **READ**, claims that were quarantined
   as unverified get resolved, and follow-on work that was blocked on it
   gets scheduled.

Copyright note: only upload what you may lawfully store in this
repository (arXiv PDFs and open-access journal PDFs are fine; if the
repo is public, prefer arXiv versions over paywalled publisher PDFs).

**Acquired so far:**

| Source | Directory | Status |
|---|---|---|
| BTVA, arXiv:1912.08908v3 (source + ancillary Magma) | [1912.08908/](1912.08908/) | READ & digested 2026-08-26 (A7 §7; `verify --only a7btva`) |
| García-Fritz–Urzúa, arXiv:1804.07671 | `1804.07671-garcia-fritz-urzua.pdf` | READ in full 2026-08-26 (A8 method source) |
| Stoll–Testa, arXiv:1009.0388v2 (2025 update) | `1009.0388-stoll-testa.pdf` | READ (main theorems) 2026-08-26 |
| Horie–Yamauchi, arXiv:2512.22520v3 | `2512.22520-horie-yamauchi.pdf` | READ (main theorem) 2026-08-26 |
| Lu–Miyaoka, MRL 2 (1995) | `lu-miyaoka-1995-mrl2.pdf` | READ (main theorems; hypotheses fail for X) 2026-08-26 |
| Miyaoka, Publ. RIMS 44 (2008) | `miyaoka-2008-orbibundle-rims44.pdf` | READ (main theorems; hypotheses fail for X) 2026-08-26 |
| Bruin–Ilten–Xu, arXiv:2312.01722 | `2312.01722-bruin-ilten-xu.pdf` | READ (framework) 2026-08-26 |

**Acquired in the 2026-08-28 full-access sweep** (RESEARCH_LOG entry 29;
digestion status tracked in `docs/references.md`):

| Source | File | Status |
|---|---|---|
| Hill, arXiv:2510.08286**v3** (Apr 2026) — the claimed proof under A1 audit | `2510.08286v3-hill.pdf` | READ in full 2026-08-28; A1 re-audit pending (see A1 §6) |
| Bremner, "On squares of squares" I, Acta Arith. 88 (1999) | `bremner-1999-squares-of-squares-I-aa88.pdf` | acquired; digest pending (unblocks A4 cross-check) |
| Bremner, "On squares of squares II", Acta Arith. 99 (2001) | `bremner-2001-squares-of-squares-II-aa99.pdf` | acquired; digest pending |
| Rome–Yamagishi, arXiv:2406.09364v2 | `2406.09364-rome-yamagishi.pdf` | acquired; digest pending |
| Rome–Yamagishi, published: Res. Number Theory **11:91 (2025)** | `rome-yamagishi-rnt-2025-91-published.pdf` | acquired (citable version) |
| Kominers, "Center-zero magic squares of squares over number fields" | `kominers-center-zero-magic-squares.pdf` | acquired; digest pending (A3.K cross-check) |
| Flores, arXiv:2411.01091 (publ. Bull. Aust. Math. Soc.) | `2411.01091-flores.pdf` | acquired; context |
| Várilly-Alvarado, "The geometric disposition of Diophantine equations", Notices AMS 68 (2021) | `varilly-alvarado-2021-notices-rnoti-p1291.pdf` | acquired (P2 expository anchor) |
| Woll, arXiv:1809.03067 | `1809.03067-woll.pdf` | acquired |
| Cain, arXiv:1908.03236 | `1908.03236-cain.pdf` | acquired |
| Wolird, arXiv:2310.12164 | `2310.12164-wolird.pdf` | acquired |
| Boyer/Morgenstern search + bounds pages (multimagie.com, saved 2026-08-28) | [`multimagie/`](multimagie/) | acquired — turns the CITED search bounds into READ-able artifacts |
| Duke, "Hyperbolic distribution problems…", Invent. Math. 92 (1988) | `duke-1988-hyperbolic-distribution-inventiones92.pdf` | acquired (P8) |
| Duke, "An introduction to the Linnik problems" (expository) | `duke-linnik-problems-introduction.pdf` | acquired (P8 bonus) |
| Aka–Einsiedler–Shapira, arXiv:1502.04209, Invent. Math. 206 (2016) | `1502.04209-aka-einsiedler-shapira.pdf` | acquired (P8) |
| Ellenberg–Michel–Venkatesh, "Linnik's ergodic method and the distribution of integer points on spheres", arXiv:1001.0897 | `1001.0897-ellenberg-michel-venkatesh-linnik.pdf` | acquired (P8 — the modern Venkov/class-group exposition, the A9-T1 input) |
| Schulze-Pillot, "Representation by integral quadratic forms — a survey" (2004) | `schulze-pillot-representation-survey-talca.pdf` | acquired (A9 composition frontier) |
| Earnest–Haensch et al.: spinor-regular ternary completeness, arXiv:1711.05811; exceptional sets, arXiv:2203.02620; spinor genera of lattice cosets, arXiv:2104.08798 | `1711.05811-…`, `2203.02620-…`, `2104.08798-…` | acquired (A9 composition frontier) |
| Hirzebruch, "Arrangements of lines and algebraic surfaces" (1983), MPIM eprint scan | `hirzebruch-1983-arrangements-of-lines.pdf` | acquired (P5 context) |
| Pokora, arXiv:1808.09167; line-arrangement surfaces, arXiv:1612.06730 | `1808.09167-pokora.pdf`, `1612.06730-line-arrangement-surfaces.pdf` | acquired (P5 context) |
| **New 2026 finds:** Bruin–Creutz, "Explicit Brauer–Manin obstructions on plane quartics", arXiv:2601.16975 | `2601.16975-bruin-creutz-brauer-manin-quartics.pdf` | acquired — worked modern template for the arithmetic endgame |
| Thanos–Bonsangue–Laarman, "Quantum algorithms for magic square Diophantine equations", arXiv:2605.04106 | `2605.04106-quantum-magic-square-diophantine.pdf` | acquired; tangential (periodicity/QFT viewpoint) |
| "Quartic reductions and elliptic obstructions for perfect Euler bricks", arXiv:2604.09328 | `2604.09328-euler-bricks-elliptic-obstructions.pdf` | acquired; cuboid-adjacent context |
| "There are infinitely many Hilbert cubes of dimension 3 in the set of squares", arXiv:2604.05459 | `2604.05459-hilbert-cubes-of-squares.pdf` | acquired; additive-structure-of-squares context |
