# F5 — No local obstruction: why congruence arguments cannot settle the problem

**Status:** F5.1, F5.2 **PROVEN** (complete proofs); F5.3 **VERIFIED**
(exhaustive, exact exceptional set below 1000) with the general statement
CITED (Labruna) and a Weil-bound route noted; F5.4 **VERIFIED** (explicit
stored witness, deterministic generator).
Verification: `python3 -m verify --only f5`.

This document is the program's negative meta-theorem. It delimits, with
proofs, the class of arguments that **cannot** prove Conjecture 0.3 — so
that the attack documents spend effort only where a proof could live.

## F5.1 The bare congruence system is solvable modulo every $n$ (PROVEN)

Formally: a *bare congruence refutation* would be an integer $n \ge 2$ such
that no $(c, u, v) \in (\mathbb{Z}/n)^3$ has all nine Lucas entries in the
set of squares mod $n$. (Any integer MSS3 reduces mod $n$ to such a
triple; distinctness of integers imposes **no** condition mod $n$, since
distinct integers may share a residue.)

**Theorem.** No such $n$ exists: $(c,u,v) = (1,0,0)$ has all nine entries
$\equiv 1 = 1^2 \pmod n$ for every $n$.  ∎

That one line kills the naive program. The serious content is that even
*non-degenerate* local solutions exist everywhere:

## F5.2 Solutions with nine distinct entries over $\mathbb{Z}_p$ for every prime $p$, and over $\mathbb{R}$ (PROVEN)

**Hensel lemma (odd $p$), as used.** If $a \in \mathbb{Z}_p^\times$ and
$a \equiv x_0^2 \pmod p$ with $x_0 \not\equiv 0$, then $a$ is a square in
$\mathbb{Z}_p$. *Proof.* Iterate: given $x_k$ with $x_k^2 \equiv a \pmod
{p^k}$, set $x_{k+1} = x_k + tp^k$ where $t \equiv (a - x_k^2)p^{-k}
(2x_k)^{-1} \pmod p$ (valid: $2x_k$ is a unit); then $x_{k+1}^2 \equiv a
\pmod{p^{k+1}}$. The limit exists in $\mathbb{Z}_p$. ∎

**2-adic criterion.** $a \in \mathbb{Z}_2^\times$ is a square in
$\mathbb{Z}_2$ iff $a \equiv 1 \pmod 8$. *Proof.* Necessity: odd squares
are $\equiv 1 \pmod 8$. Sufficiency: given $x_k$ ($k \ge 3$) with $x_k^2
\equiv a \pmod{2^k}$, one of $x_k$, $x_k + 2^{k-1}$ works mod $2^{k+1}$
(their squares differ by $2^k x_k + 2^{2k-2} \equiv 2^k \pmod {2^{k+1}}$
since $x_k$ is odd and $2k-2 \ge k+1$); start from $x_3 = 1$. ∎

**Theorem.** For every prime $p$ there is a magic square of nine
**distinct** squares over $\mathbb{Z}_p$ (and over $\mathbb{R}$, and by
CRT over $\mathbb{Z}/n$ for every $n$, with entries distinct in
$\mathbb{Z}$-lifts).

*Proof.* Take $c = 1$. For odd $p$: choose $u = p\,u_0$, $v = p\,v_0$ with
$u_0, v_0$ any integers making the F1.3 distinctness product nonzero (e.g.
$u_0 = 1, v_0 = 3$... any pair avoiding the eight linear relations). All
nine entries are $\equiv 1 \pmod p$, hence unit squares in $\mathbb{Z}_p$
by Hensel; the entries are distinct elements of $\mathbb{Z}_p$ by F1.3.
For $p = 2$: take $u = 8u_0$, $v = 8v_0$ similarly; entries are $\equiv 1
\pmod 8$, hence squares in $\mathbb{Z}_2$. Over $\mathbb{R}$: any Lucas
triple with $c$ large relative to the offsets has nine distinct positive
entries, all real squares. ∎

**Consequence.** Any impossibility proof must use inputs invisible to all
completions of $\mathbb{Q}$ separately — genuinely global structure:
descent chains (as in F3), height/size interplay, or the geometry of the
parametrizing surface. "Cannot exist because of residues" is off the
table, permanently.

## F5.3 The finer question: nine *distinct* entries over $\mathbb{F}_p$ (VERIFIED + CITED)

Over $\mathbb{F}_p$ (residues, not $p$-adics), distinctness *is* a real
constraint. Pigeonhole: nine distinct entries that are squares require
$(p+1)/2 \ge 9$, i.e. $p \ge 17$. The truth is more interesting.
**Exhaustive computation** (`f5.fp_scan`; WLOG $c = 1$ by scaling): among
all primes $p < 1000$, a magic square of nine distinct **nonzero** squares
over $\mathbb{F}_p$ exists **iff**
$$p \in \{59, 73, 83, 97\} \quad\text{or}\quad p \ge 107.$$
Equivalently, the exceptional primes are exactly
$$\{5,7,11,13,17,19,23,29,31,37,41,43,47,53\} \cup \{61,67,71,79,89,101,103\}.$$
So the naive "each entry is a square with probability $\tfrac12$"
heuristic fails badly below 59 — the nine quadratic conditions on the two
parameters $(u,v)$ are strongly correlated — and then wins permanently
(within the verified range) from 107 on.

- CITED (Labruna 2018): solutions with nine distinct entries exist over
  $\mathbb{F}_p$ for infinitely many $p$. Our computation refines this to
  an exact list in $[2, 1000)$.
- **Provable route for all large $p$** (stated as a task, not claimed):
  the number of $(u,v)$ with all eight off-center entries nonzero squares
  is $\frac{p^2}{2^8} + O(p^{3/2})$ by Weil's bounds applied to the
  character sums $\sum_{u,v} \prod_i (1 + \chi(e_i(u,v)))$ — the error
  terms are sums of $\chi$ over products of distinct linear forms, i.e.
  point counts on superelliptic curves. With an explicit constant this
  proves existence for all $p > p_0$; combining with computation up to
  $p_0$ would upgrade F5.3 to a clean theorem "for every prime
  $p \ge 107$". **Open Task F5-T1** (tracked in A5/A6 spirit: provable
  with standard tools, bounded work).

## F5.4 An explicit witness modulo $2^{32}$ (VERIFIED)

`compute/mod2n_lift.py` (deterministic) generates, and
`verify/targets.py` stores, a Lucas triple mod $2^{32}$ with **nine
distinct entries, each given with an explicit square root** — a
miniature, first-party reproduction of Morgenstern's mod-$2^N$
constructions (CITED, examples to $2^{90}$), witnessing F5.2's 2-adic
branch concretely. `f5.mod2n` re-verifies every root and re-runs the
generator.

## What remains available to an impossibility proof

| Input | Status |
|---|---|
| Congruences / residues mod $n$ | **Dead** (F5.1) |
| $p$-adic arguments, any single $p$ | **Dead** (F5.2) |
| Real-place positivity alone | **Dead** (F5.2) |
| Order-$n$-insensitive arguments | **Dead** (Euler/Rome–Yamagishi, F6) |
| Base-field-insensitive arguments | **Dead** (Kominers, CITED — over $\mathbb{Q}(i,\sqrt n)$ solutions exist) |
| Descent / infinite descent (F3-style) | Open |
| Height gaps, size vs. divisibility interplay | Open |
| Geometry of the parametrizing surface (BTVA) + rational-point finiteness inputs | Open (conditional today) |

This table is the program's map: attacks A1–A6 live entirely in the last
three rows.
