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
with provenance flags.

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
| `docs/attacks/A1…A6` | The attack lines (each with an honest verdict) |
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
   $m \le 300{,}000$, no two congrua of $m$ sum to a congruum of $m$ —
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
5. **A boundary meta-theorem for claimed proofs**: no descent-free
   congruence/order argument can settle the problem (executable
   pseudo-solutions for every modulus), applied to the unrefuted
   arXiv:2510.08286. ([A1](docs/attacks/A1-hill-audit.md))
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
| Hill arXiv:2510.08286 | UNRESOLVED (text unobtainable); its described method space provably insufficient | A1 |
| $k[t]$: primitive 4-APs of squares constant; square-congruum APs constant; $\mathbb{Q}[t]$ outright | PROVEN | A2 |
| No MSS3 over $\mathbb{F}_q[t]$, nonconstant center, tabulated $(q, \deg)$ ranges | VERIFIED | A2 |
| Full $k[t]$ conjecture = no nondegenerate rational curves on $X$ | CONJECTURED (A2.C); Open A2-T1 | A2 |
| Congruent-number/AP/elliptic dictionary | PROVEN | A3 |
| Additive desert: no triple in any $D(m)$, $m \le 3\times10^5$ | VERIFIED; A3.C CONJECTURED | A3 |
| No quadratic field has center-zero solutions; $\mathbb{Q}(i,\sqrt n)$ does ($n$ congruent); explicit $\mathbb{Q}(i,\sqrt5)$ witness | PROVEN | A3 |
| 8-square taxonomy C/E/K; class-E ⇒ additive triple | PROVEN | A4 |
| No 8-square square with center $\le 10^6$; class E dead to $9\times10^{10}$ | VERIFIED | A4 |
| AB1 fiber Jacobian has certified rank 3, torsion $(\mathbb{Z}/2)^2$ | VERIFIED (PARI) | A4 |
| $X$: 6 quadrics, rank exact; smooth off coordinate hyperplanes; arrangement $(t_2,t_3) = (12,8)$; $\mathbb{F}_p$ counts | PROVEN/VERIFIED | A5 |
| Bound ladder (three cross-validated implementations) | VERIFIED | A6 |
| **The open problem itself** | **OPEN — no claim** | everywhere |

**Open tasks:** F3-T1 (close the quartic (Q) descent), F5-T1 (Weil-bound
proof of $\mathbb{F}_p$ solvability for all $p \ge 107$), A2-T1 = A5-P3
(enumerate the finitely many low-genus curves on $X$ — the keystone),
A3-Q (a Selmer-type invariant explaining the desert), A4-T1 (genus of
the eighth-square cover over the rank-3 fiber), A6-T1 (compiled sieve).
