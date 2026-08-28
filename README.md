# The 3×3 Magic Square of Squares: an impossibility attack program

> **Standing banner — read this first.** The existence of a 3×3 magic square
> whose nine entries are distinct perfect squares is an **open problem**
> (LaBar 1984; Gardner 1996; Boyer 2005; the "Parker Square" problem).
> **This repository does not claim a solution.** It is a rigorous, verifiable
> research program that attacks the impossibility direction: it proves the
> reduction structure from first principles, proves why entire classes of
> attack *cannot* work, pushes several genuine attack directions to honest
> verdicts, and documents failures as carefully as successes.

## The problem

Does there exist a 3×3 magic square — all three rows, all three columns, and
both diagonals having the same sum — whose nine entries are **distinct perfect
squares**? Equivalently: integers $x_1,\dots,x_9 \ge 0$, with $x_1^2,\dots,x_9^2$
pairwise distinct, such that

$$\begin{pmatrix} x_1^2 & x_2^2 & x_3^2 \\ x_4^2 & x_5^2 & x_6^2 \\ x_7^2 & x_8^2 & x_9^2 \end{pmatrix}$$

has all eight lines summing to the same $S$. Nobody knows. The best published
search bound says any example has every entry $\ge 10^{14}$; the modern
geometric heuristic (Bruin–Thomas–Várilly-Alvarado 2022 + the Bombieri–Lang
conjecture) predicts at most finitely many examples exist — but neither
direction is settled. Since Rome–Yamagishi (2024) constructed $n \times n$
magic squares of squares for every $n \ge 4$, **$n = 3$ is the only open
order.**

See [docs/00-problem-statement.md](docs/00-problem-statement.md) for precise
definitions and [docs/references.md](docs/references.md) for the literature
with provenance flags. **For the standing honest assessment of what this
program has genuinely achieved — and what it has not — read
[docs/PROGRESS.md](docs/PROGRESS.md). For the strategic battle plan toward
an actual proof — the workstreams, milestones, and creative bets — read
[docs/ROADMAP.md](docs/ROADMAP.md).**

## Quickstart

```sh
python3 -m verify          # run the full verification suite (FULL bounds)
python3 -m verify --fast   # pre-commit gate, < 60 s
python3 -m verify --only f4  # substring filter
```

Pure Python 3.11 stdlib suffices for every proof-critical check. Optional
extras (`pip install sympy gmpy2`, `apt install pari-gp`) enable additional
exploratory checks, which SKIP cleanly when the tools are absent.

## How rigor works here (no proof assistant, no hand-waving)

1. Every mathematical document carries claims tagged with exactly one status:
   **PROVEN** · **PROVEN-CLASSICAL** · **CITED** · **VERIFIED(bound)** ·
   **CONJECTURED** · **FAILED-ATTEMPT**. Definitions in
   [docs/protocol/status-taxonomy.md](docs/protocol/status-taxonomy.md).
2. Everything computationally checkable is checked by a named script under
   `verify/checks/`, run by the single command above and by CI on every push.
3. Every candidate impossibility argument must pass the **falsification
   gauntlet** ([docs/protocol/sanity-checks.md](docs/protocol/sanity-checks.md)):
   it must *not* rule out the known near-solutions — the Bremner–Sallows
   7-square square, Euler's 4×4 magic square of squares, solutions over
   $\mathbb{F}_p$, solutions mod $2^N$ — because those exist.
4. Failed attempts are written up in [RESEARCH_LOG.md](RESEARCH_LOG.md) with
   an autopsy, not deleted.

## Repository map

| Path | Content |
|---|---|
| `docs/00-problem-statement.md` | Definitions, symmetry group, primitivity, status |
| `docs/foundations/F1…F6` | The structural theory, proven from first principles |
| `docs/attacks/A1…A8` | The attack lines (each with an honest verdict) |
| `papers/` | Acquired primary sources (uploaded; provenance-tracked) |
| `docs/protocol/` | Status taxonomy and the falsification gauntlet |
| `docs/references.md` | Literature, with provenance flags |
| `verify/` | The mechanical verification suite (`python3 -m verify`) |
| `compute/` | Exploratory searches and data generation (not proof-critical) |
| `RESEARCH_LOG.md` | Dated log of everything, including negative results |

## Headline results of this repository

Beyond reproving the foundations from scratch, the program produced:

1. **Two unconditional function-field theorems** (new in this setting as
   far as our survey reaches): over $k[t]$, $\operatorname{char} k
   \notin \{2,3\}$, every 4-term AP of squares, and every 3-AP of squares
   with square common difference, is a square multiple of a constant one
   — by an elementary degree-halving descent (Lemma A2.L) whose
   nondegeneracy self-propagates. Over $\mathbb{Q}[t]$ the congruum
   statement holds outright. ([A2](docs/attacks/A2-function-field.md))
2. **The additive desert** (first-party exhaustive): for every
   $m \le 10^7$, no two congrua of $m$ sum to a congruum of $m$ —
   the additive pattern an MSS3 needs never reaches even three of its
   four constraints; and this is a *square-center* phenomenon: at
   non-square centers the pattern genuinely occurs ($c = 157441$).
   ([A3](docs/attacks/A3-simultaneous-congrua.md),
   [A4](docs/attacks/A4-eight-squares.md))
3. **Eight-square taxonomy and bounds**: the open 8-square problem
   splits into classes C/E/K; class E is dead to center
   $9\times10^{10}$; no 8-square square of any class has center
   $\le 10^6$; AB1 (and its scalings) confirmed as the unique
   $\ge 7$-square configuration in range, and its fiber curve computed —
   certified **rank 3**. ([A4](docs/attacks/A4-eight-squares.md))
4. **A center-zero magic square of nine distinct squares over
   $\mathbb{Q}(i,\sqrt5)$**, fully explicit
   ($L(0, 41^2, 720)$, entries $\{0, \pm41^2, \pm720, \pm49^2,
   \pm31^2\}$), with the degree-4 minimality proven — now a live
   falsification target. ([A3](docs/attacks/A3-simultaneous-congrua.md))
5. **A boundary meta-theorem for claimed proofs** — no descent-free
   congruence/order argument can settle the problem (executable
   pseudo-solutions for every modulus) — **and the formal refutation of
   arXiv:2510.08286** (v3): its eq. (29) is proven to be an identity-
   multiple of its own spacing constraint, and its final inference fails
   on an explicit magic square with six perfect-square entries.
   ([A1 §7](docs/attacks/A1-hill-audit.md); standalone write-up:
   [docs/refutations/2510.08286-hill.md](docs/refutations/2510.08286-hill.md))
6. **A four-square-theorem reduction chain** ending in one classical
   quartic, each step machine-verified
   ([F3](docs/foundations/F3-no-four-term-ap.md)); the exact
   $\mathbb{F}_p$ solvability classification below 1000
   ([F5](docs/foundations/F5-local-solubility.md)); and the surface's
   explicit model, smoothness locus, branch arrangement and
   $\mathbb{F}_p$ counts ([A5](docs/attacks/A5-surface-geometry.md)).

## Claims ledger

*The per-document status tags are authoritative; this table is the map.*

| Claim | Status | Where |
|---|---|---|
| Lucas parametrization, both directions; distinctness criterion | PROVEN | F1 |
| AP ↔ Pythagorean dictionary; $\mathbb{Z}[i]$ counting; center needs $\prod(2a_i{+}1) \ge 9$ | PROVEN | F2 |
| FRT $x^4 - y^4 \ne z^2$; no square triangle area; no square congruum | PROVEN(-CLASSICAL) | F3 |
| Four-squares-in-AP theorem | PROVEN-CLASSICAL; in-repo chain complete except quartic (Q) = Open F3-T1; VERIFIED to roots 3000 | F3 |
| Entries $\equiv 1 \pmod{24}$, sum $\equiv 3 \pmod{72}$ (primitive) | PROVEN (+ exhaustive mod-72 core) | F4 |
| $\ell \equiv 3,5 \pmod 8$ divides an off-center entry $\Rightarrow \ell \mid m$; $\ell \equiv 5$: never a middle-side entry | PROVEN | F4 |
| No local obstruction: mod every $n$; over every $\mathbb{Z}_p$, $\mathbb{R}$ with distinct entries | PROVEN | F5 |
| $\mathbb{F}_p$ (distinct entries) solvable iff $p \in \{59,73,83,97\}$ or $p \ge 107$, for $p < 1000$ | VERIFIED | F5 |
| AB1 & Euler 4×4 anchors; $D(425)$ admits no MSS3 | VERIFIED | F6 |
| Pseudo-solutions defeat congruence+order endgames (any modulus) | PROVEN | A1 |
| Hill arXiv:2510.08286 (v3 READ) | **Proof REFUTED (PROVEN)**: its eq. (29) = positive cofactor × its own Lemma-3.2 constraint (identity; no Diophantine content); the "(29) ⟹ β₁ = 1" coefficient step fails on an explicit witness (magic square $(4,3360,2112)$-grid, six square entries, β₁ = 6/5, both sides of (29) ≠ 0). Encoding proven faithful & complete (= Lucas grid). Problem statement untouched | A1 §7; [refutations/2510.08286-hill](docs/refutations/2510.08286-hill.md); `a1.eq29_identity`, `a1.eq29_witness`, `a1.hill_grid` |
| $k[t]$: primitive 4-APs of squares constant; square-congruum APs constant; $\mathbb{Q}[t]$ outright | PROVEN | A2 |
| No MSS3 over $\mathbb{F}_q[t]$, nonconstant center, tabulated $(q, \deg)$ ranges | VERIFIED | A2 |
| Full $k[t]$ conjecture = no nondegenerate rational curves on $X$ | CONJECTURED (A2.C); Open A2-T1 | A2 |
| Congruent-number/AP/elliptic dictionary | PROVEN | A3 |
| Additive desert: no triple in any $D(m)$, $m \le 10^7$ (99.3M pairs, 3.1M centers; 33× extension 2026-08-28) | VERIFIED; A3.C CONJECTURED | A3; `a3.additive_ext` |
| No quadratic field has center-zero solutions; $\mathbb{Q}(i,\sqrt n)$ does ($n$ congruent); explicit $\mathbb{Q}(i,\sqrt5)$ witness | PROVEN | A3 |
| 8-square taxonomy C/E/K; class-E ⇒ additive triple | PROVEN | A4 |
| No 8-square square with center $\le 10^6$; class E dead to $9\times10^{10}$ | VERIFIED | A4 |
| AB1 fiber Jacobian has certified rank 3, torsion $(\mathbb{Z}/2)^2$ | VERIFIED (PARI) | A4 |
| $X$: 6 quadrics, rank exact; smooth off coordinate hyperplanes; arrangement $(t_2,t_3) = (12,8)$; $\mathbb{F}_p$ counts | PROVEN/VERIFIED | A5 |
| Bound ladder (three cross-validated implementations) | VERIFIED | A6 |
| Genus ≤ 1 curves on $X$ over plane **lines**: complete classification (only $u{=}0$, $v{=}0$: genus 0 degenerate; $c{=}0$: genus 1, no nondegenerate $\mathbb{Q}$-points via F3.2) | PROVEN | A7 |
| Every nonconstant $k(t)$-MSS3 has Lucas-image degree ≥ 2 (char ∉ {2,3}); degree ≥ 3 in char 0 | PROVEN | A7 |
| Resolution invariants: $K^2 = 576$, $c_2 = 768$, $\chi(\mathcal{O}) = 112$, $s_2 = -192 < 0$ (hyperbolicity is nodal); 256 $A_1$ nodes located | VERIFIED | A7 |
| **Conic layer closed**: sharp budget lemma (six residual classes) + exhaustive exact sweeps ($\mathbb{Q}(\sqrt D)$ pencil roots, elimination certificates): no genus ≤ 1 curve on $X$ has conic image; genus ≤ 1 ⟹ Lucas-image degree ≥ 3 (char 0); nonconstant $k(t)$-MSS3 needs degree ≥ 3 | PROVEN (Thm A7.6) | A7 §4 |
| BTVA (arXiv:1912.08908) READ from acquired source; its $X$ results reproduced exactly from our invariants ($\ell_{\min}(8)=217$; sections from $m = 47$, $h^0 \ge 8448$); no enumeration/node refinement for $X$ exists there; 3 display errata found | VERIFIED | A7 §7, papers/1912.08908 |
| Descent decomposition: $H^0(X^\circ, S^m\Omega^1) = \bigoplus_{256}$ plane-level linear problems (executes BTVA's "out of range" step by another route) | PROVEN | A8 |
| $q(\widetilde X) = 0$, hence $b_2 = 766$, $h^{1,1} = 544$ (all 256 characters at $m=1$; matches classical pencil-character theory) | VERIFIED | A8 |
| $h^0(X^\circ, S^2\Omega^1) = 0$ — the $m=2$ explicit-differential program (13-dimensional on the cuboid) is **empty** on $X$ | VERIFIED (methodology positively controlled) | A8 |
| **Cuboid control passed**: the same engine reproduces BTVA's $h^0(X_{\mathrm{pc}}, \hat S^2\Omega^1) = 13$ exactly — full 16-character fingerprint + element-level generator membership | VERIFIED | A8 §4 |
| First-section bracket: $\chi(X,\hat S^m\Omega^1) < 0$ for $m \le 6$, $= +384$ at $m = 7$ ⟹ first nonzero symmetric degree on $X^\circ$ is in $\{3..7\}$ (vs BTVA's $m \ge 47$ on $Y$) | PROVEN (h²-vanishing PROVEN-CLASSICAL) | A8 |
| $h^0(X^\circ, S^3\Omega^1) = 0$ (saturated mod-$p$ proof, all 256 characters) | VERIFIED | A8 |
| **First explicit symmetric differentials on $X$**: $\dim V_\varnothing(m{=}4) = 6$, certified (6 exact verified generators + mod-$p$ upper bound); $m_{\min} = 4$ — BTVA's "out of range" computation executed; their explicit special-curve machinery now applicable to $X$ | VERIFIED (generators stored & re-verified in-repo) | A8, `compute/data_m4_generators.py` |
| Lu–Miyaoka / orbibundle-MYS effective bounds inapplicable to $X$: $K^2 = 576 < 640 = c_2^{\mathrm{orb}} < 768 = c_2$ | READ + computed | A8 §1 |
| Unconditional reduction (Lemma A8.6): a node-avoiding complete genus-0 curve on $X$ has Lucas image of degree ≥ 3, off all triple points, inside the proper common-root locus $Z$ of the six $m{=}4$ quartics; the nine entry lines lie in $Z$; $u{=}0$, $v{=}0$ and the six distinctness lines are not integral | PROVEN (exact certificates) | A8 §7 |
| **Node passage (Theorem A8.8): every complete genus-0 curve on $X$ passes through ≥ 1 of the 256 nodes** — first node-passage statement for the magic-square surface (BTVA prove these only for Barth/cuboid) | **PROVEN, unconditional** (Theorem A8.7′: exact resultants by provably complete CRT, $\gcd(R_{12}, R_{34}) = \prod \ell^8$, coprime cofactors; the 2-prime $Z$-scan stands as independent consistency) | A8 §7 |
| **$h^0(\widetilde X, S^4\Omega^1) = 1$: the resolution carries a unique symmetric quartic differential** $\eta_\star = \eta_4$ (BTVA's resolution guarantee began at $m \ge 47$); every rational curve on $X$ is an $\eta_\star$-integral curve, and the classical AP families comply ($u{=}0$, $v{=}0$ are $\eta_\star$-integral) | PROVEN (exact local $\tau$-calculus on the uniform AP-cone $z_3^2 = (z_1^2{+}z_2^2)/2$; direct certification through the transpose symmetry) | A8 §8 |
| Exceptional-degree bound: every complete genus-0 curve has $\widetilde C \cdot E \ge 4$ on the resolution (cuboid benchmark: $C \cdot E \ge 8$); node-pattern dichotomy: image integral for the 4-dim extension subspace of each visited triple point (lattice: pairwise 2–3, triples 2, global 1) | PROVEN | A8 §8 |
| **Theorem A8.14: every complete genus-0 curve on $X$ meets nodes over ≥ 2 distinct triple points (≥ 2 distinct nodes)** — the magic-square analogue of BTVA's cuboid ≥ 2-nodes theorem, via 8 exact subsystem-resultant certificates (entry lines peel to ≥ 8, cofactors coprime over $\mathbb{Q}$) | PROVEN | A8 §8 |
| **Theorem A8.15 (SHARP): … over ≥ 3 distinct triple points (≥ 3 distinct nodes)** — all 28 two-point patterns excluded (coprime cofactors / exact point prefilters / carrier-line mechanism = the AP-family logic / a ℚ-irreducible degree-18 cofactor through all 8 rational triple points, certified by mod-$p$ factor-degree subset-sums); the classical AP families attain exactly 3, so **the pattern-counting layer is complete** | PROVEN | A8 §8 |
| **Theorem A8.16: a genus-0 curve whose pattern $S$ has $\dim V_S \ge 2$ is one of the 128 classical AP components** — the census over all $\|S\| \ge 3$ finds exactly 8 subspaces (7 of dim 2, tied to the central and outer entry lines and the family clusters), each locus classified exactly with Galois-integrality refutations of the ℚ-irreducible leftovers; 17 dim-2 patterns impossible. **Every other rational curve on $X$ lives on the single web $\eta_\star$** — the problem is reduced to one differential | PROVEN | A8 §8 |
| **Theorem A8.18: the $\eta_\star$-web is spectrally rigid through degree 8** — $h^0(S^5) = 0$ AND $h^0(\widetilde Y, S^6\Omega^1) = 0$ for every character (two full 51-orbit surveys + the $\tau$-test); trivial-character resolution ladder complete, $4 \to 1,\ 5 \to 0,\ 6 \to 0,\ 7 \to 0,\ 8 \to 1$: $h^0(\widetilde Y, S^8\Omega^1)^{\mathrm{inv}} = \langle\eta_\star^2\rangle$ **exactly** (mod-$p$ $\tau$-test upper bound + $\eta_\star^2$ certified exactly, live on every suite run). **No second invariant section** — the two-section finiteness shortcut is closed; the web analysis is unavoidable | PROVEN (sandwich) | A8 §8, `a8.section_spectrum` |
| **Theorem A8.17: the $\eta_\star$-web has exactly 15 integral lines** — the 9 entry lines, $u{=}0$, $v{=}0$, and four new $\mathbb{Q}(\sqrt3)$-lines $\sqrt3 c = \pm u \pm v$ (one $D$-point each, genus $\ge 2$ upstairs by A7.3: no new rational curves). Completeness by nonzero-resultant gcd peeling $b^{24}(b^2{-}1)^{24}(3b^2{-}1)^6$ to a constant | PROVEN | A8 §8, `compute/web_lines.py` |
| The discrete-sphere model (owner's picture, exact): a magic square of squares = 8 glued lattice points on the single sphere $\mathcal{S}(3m^2)$; the $m$-slice = A3's congrua set $D(m)$ (exact bijection $\forall m \le 200$); the magic/oblique split of the 8 triple points (the 4 sphere-collapse points = the central-line points of A8 §8); abundance (spheres to 64 points) vs compatibility ($L_3 = L_4 = 0$) quantified | PROVEN (dictionary) + measured | A9 |
| The class-group layer of the sphere model: the Eisenstein anchor ($r_3^*(3m^2) = 24\,h(-3m^2)$ — one field $\mathbb{Q}(\sqrt{-3})$ carries the whole family), the Gauss orthogonal-lattice map (uniform fibers, even lattices), exponential slice confinement; the gluing law (each line's class represents its three co-norms) and **Theorem A9.3, the coherence obstruction**: kills 10/12 ordered congrua pairs at $m = 65, 85, 130$ and 6/12 at $145$ — the first extension obstruction beyond the classical $24 \mid d$ layer | PROVEN (necessity) + measured (bite) | A9 §3 |
| **The three-sieve pair desert**: positivity ($U{+}V \le m^2$) + coherence (A9.3) + **class representation** (each line's co-norm triple must be represented by one even class at an admissible discriminant — strictly beyond genus) kill **every** ordered congrua pair for **every** center $m \le 3\times10^4$ (2026-08-28 extension: 146,914 pairs at 6,101 centers — 122,630/18,992/**5,292**, zero golden centers; previously 1782 pairs to $m \le 1200$; the $U{+}V$ diagonal unrepresentability and never-kill-a-real-line controls stand) — the A3 desert's first structural explanation at the pair level, now with a 5,292-pair anatomy corpus. **First golden (sieve-transparent) centers found 2026-08-28 at $m = 34{,}225 = 185^2$** — exactly the decade the actuarial model predicted: sieve totality was probabilistic, and the A9.12 law confirms every line live | PROVEN (necessity of each sieve) + VERIFIED($m \le 3\times10^4$ perfect; golden onset at 34,225) | A9 §3; `a9.desert_ext`, `a9.golden` |
| **Theorem A9.6 (the center cap)**: for every congrua pair, the $U$- and $V$-center lines carry the actual sphere points $(e{-}f, m, e{+}f)$ and can never be representation-killed; at most two center lines (the phantom $U{\pm}V$ lines) can die — the sampled cap $k_c \le 2$ is a theorem for **all** $m$, and the fourth sieve is revealed as the class-group shadow of the A3 additive condition | PROVEN (constructive certificates over the 5,292-pair corpus) | A9 §3; `a9.center_cap` |
| **The fourth-sieve mechanism (M12-B)**: Lemma A9.5 (inverse-closure: odd-order characters never separate; 4-rank 0 ⟹ no character certificate can exist) PROVEN; verdicts on all 36 beyond-genus kills: **6 CHARACTER** (all at $m = 481, 962$; every separator of order exactly 4 — the Rédei/4-rank layer) + **30 ARC** (no character of any order; prime-class product-set geometry; all of $m = 725$); the ideal-product law EXACT on 62/62 conductor-coprime values. H-Rédei refuted as universal, confirmed as the 4-rank layer; refined to H-align | PROVEN (lemma, law) + measured (verdicts, pinned) | A9 §3 fifth layer; `a9.kill_mechanism` |
| **The $H^{2,0}$ character atlas (M12-A)**: $h^{2,0}(\chi_S) = \binom{\|S\|/2-1}{2}$ (all sub-arrangement singularities ADE — max concurrency 3, verified); the transcendental motive fragments into **84 K3** characters ($t_3$-census 2/20/46/16, $\rho \ge 16 + t_3$) + **9 Horikawa** characters ($K^2{=}2$, $\chi{=}4$); total 111 $=$ $\chi(\mathcal{O}) - 1$ cross-confirmed; 19 orbit types govern everything | PROVEN-CLASSICAL (formula) + machine census | A8 §10; `a8.h20_atlas` |
| **The anatomy of the kills — the fourth sieve is composition**: Gauss composition implemented and verified as a group ($\mathrm{Cl}(-507) \cong \mathbb{Z}/4$, $\mathrm{Cl}(-3\cdot65^2) \cong \mathbb{Z}/12{\times}\mathbb{Z}/2$); **principal genus theorem machine-verified** (squares = trivial genus); a local representability criterion validated exhaustively (9000 values, 0 mismatches; the $\chi_3$ norm-residue law); the 57 killed lines decompose as **21 provably-local + 0 genus + 36 strictly beyond every character** (inside cosets of $\mathrm{Cl}^2$, same-genus witnesses certified); at $m=725$ both pairs die by the class group alone; even-center content law fixed and controlled ($850/962$ exactly double $425/481$) | PROVEN-CLASSICAL (verified) + measured anatomy | A9 §3 |
| **The open problem itself** | **OPEN — no claim** | everywhere |

**Open tasks:** F3-T1 (close the quartic (Q) descent), F5-T1 (Weil-bound
proof of $\mathbb{F}_p$ solvability for all $p \ge 107$), A2-T1 = A5-P3
(enumerate the finitely many low-genus curves on $X$ — the keystone),
A3-Q (a Selmer-type invariant explaining the desert), A4-T1 (genus of
the eighth-square cover over the rank-3 fiber), A6-T1 (compiled sieve).
(A8-T3 — the exact identification of the special-curve locus — was
closed the day it was opened: Theorem A8.7′.)
