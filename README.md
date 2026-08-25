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

## Claims ledger

*Synced at each milestone; the per-document status tags are authoritative.*

| Claim | Status | Where |
|---|---|---|
| (populated as milestones land) | | |
