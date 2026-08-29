# The state of the program

*A standing honest assessment: what has genuinely been achieved, what it
means, and what it does not mean. Updated at milestones (last:
2026-08-28, after the M12 wave: the literature sweep and Hill
refutation, the $H^{2,0}$ atlas, the fourth-sieve ladder
A9.6–A9.12, the desert at $3\times10^4$ and the first golden centers,
and the additive desert at $10^7$). Every claim below carries the
repository's provenance tags and is enforced by the verification suite
(`python3 -m verify`, currently 124 checks); the
[README ledger](../README.md#claims-ledger) is the row-by-row record,
and [ROADMAP.md](ROADMAP.md) is the standing battle plan.*

## The one-sentence truth

**The existence question is untouched — by us and by everyone — but this
program has built, on two independent fronts, a detailed structural map
of *why* the problem is hard; several pieces of that map are new
mathematics, and the sphere front's obstruction is now a proven
elementary law rather than a mystery.**

The repository's standing banner applies to every line of this memo: the
open problem remains open, and nothing here claims otherwise.

## Front 1: the surface (A5/A7/A8)

The moduli space of the problem is a surface $X \subset \mathbb{P}^8$
(a complete intersection of 6 quadrics, degree 64, with 256 nodes),
which Bruin–Thomas–Várilly-Alvarado (2022) proved *algebraically
quasi-hyperbolic*: it carries only finitely many curves of genus
$\le 1$. Their proof is abstract; they wrote that computing the
symmetric differentials that drive it is "out of range of current
computational techniques", and no one had enumerated the low-genus
curves or made the finiteness explicit for $X$. That gap is where this
program worked, via descent along the $(\mathbb{Z}/2)^8$ cover of the
Lucas plane (Theorem A8.1). The results — all first-party,
machine-verified, and unconditional unless flagged:

1. **The spectrum is computed.** $h^0$ of symmetric differentials on
   the open surface, all 256 characters, degrees through 8; on the
   *resolution*, degree 4 has exactly **one** section $\eta_\star$
   (PROVEN), and **Theorem A8.18** closes the invariant ladder with no
   gaps: $4 \to 1,\ 5 \to 0,\ 6 \to 0,\ 7 \to 0,\ 8 \to 1$ — every
   invariant section through degree 8 is a power of $\eta_\star$
   (PROVEN by sandwich; the $m = 8$ lower bound $\eta_\star^2$ is
   re-certified exactly on every suite run), with full-character
   vanishing now also at degrees 5 and 6 (the 10.3-hour survey).
   The abstract finiteness theorem has one explicit object carrying
   it — and the cuboid-style *two-section* shortcut is provably
   unavailable at these degrees.

2. **The structure theory of rational curves.** Every complete genus-0
   curve on $X$ passes through nodes over $\ge 3$ distinct triple
   points of the branch arrangement, and 3 is sharp (Theorems
   A8.8/A8.14/A8.15, PROVEN, exact certificates); any such curve whose
   node pattern spans a $\ge 2$-dimensional extension space *is* one of
   the 128 classical degenerate AP components (Theorem A8.16, PROVEN);
   everything else must be an integral curve of the single web
   $\eta_\star$, of degree $\ge 3$, and the web's line and conic levels
   are closed with nothing new (Theorem A8.17 + the A7.6/M10-B budget).
   **Any hypothetical new 1-parameter family of near-solutions is
   cornered into one explicit, finitely-checkable system.**

3. **The motive fragments (M12-A, the $H^{2,0}$ atlas).** The
   canonical bundle decomposes over the 256 characters with no
   singular corrections (every sub-arrangement point is ADE —
   verified); $h^{2,0}$ census: **84 K3 characters + 9 Horikawa
   characters** ($K^2 = 2$, $\chi = 4$, on the Noether line), total
   $111 = \chi(\mathcal{O}) - 1$, cross-confirming Noether; only 19
   orbit types govern the entire transcendental structure, with
   proven K3 Picard bounds $\rho \ge 16 + t_3$. The W2
   Picard/Brauer/$L$-function program is now a finite list of
   classical objects.

4. **No local obstruction** (F5, long established here): the system is
   solvable modulo every prime power — whatever excludes magic squares
   of squares, it is not a congruence.

*The frontier on this front:* the web's cubic level (M11-J-2 = ROADMAP
M12-C), the exact K3 lattices of the 16 orbit types (M13-A), then the
arithmetic endgame (Picard/Galois, Brauer–Manin — Conjecture E and the
twist-descent formulation of ROADMAP W3). The $m = 7$
nontrivial-character survey runs orbit-checkpointed in the background.

## Front 2: the discrete spheres (A9)

The owner's geometric picture — the square as lattice points on spheres
— made exact, pushed through class-group territory, and now resolved
into an elementary law:

1. **The dictionary (PROVEN).** A magic square of squares with center
   $m^2$ is 8 points of the single sphere $\mathcal{S}(3m^2)$ glued by
   shared coordinates; the through-center slice *is* A3's congrua set;
   the whole family lives in one field, $\mathbb{Q}(\sqrt{-3})$, with
   $r_3^*(3m^2) = 24\,h(-3m^2)$.

2. **The three-sieve pair desert, and its true depth.** Positivity,
   genus-character coherence (Theorem A9.3), and single-class
   representation kill **every** ordered congrua pair for **every**
   center $m \le 30{,}000$ — 146,914 pairs at 6,101 centers
   (VERIFIED($3\times10^4$), zero survivors) — and the additive desert
   itself stands VERIFIED to $m \le 10^7$ (99.3M pairs, zero
   triples). **But the sieves' totality is probabilistic, not a law:**
   the calibrated actuarial model predicted first sieve-transparent
   centers in the $10^{4.5}$–$10^5$ decade, and the extension found
   them exactly there — the first **golden centers** at
   $m = 34{,}225 = 185^2$ (pair $(108786216, 718725000)$, both
   orders; `a9.golden`). Golden means the class-group layer goes
   transparent; it is *not* a square candidate ($U \pm V \notin D(m)$;
   the additive desert covers it). The desert's depth is
   additive-structural, not sieve-eternal — measured, predicted, and
   now observed. **And the golden regime has a law — the scaling
   law (Lemma A9.13, PROVEN):** sieve verdicts only soften along
   $(m,U,V) \to (qm, q^2U, q^2V)$; the golden pair is the
   37-scaling of a coherence-dead 925 base, the C2-exception is the
   29-scaling of *the* 725 passer, and the square-root-center motif
   is just the self-scaling slice ($q\cdot 5^2q = (5q)^2$). The
   ladder sweep of the window $(53400, 150000]$ found **20 golden +
   68 near-golden pairs from four fertile seeds** — minimal new
   golden centers $96425, 105125, 126875, 147175$, all *nonsquare*
   (so "sieves total off the square family" is refuted too).
   Transparency is the ladder's asymptotic behavior: **the sieves
   provably cannot carry nonexistence alone.** The frontier moves to
   (a) the fertile-seed arithmetic (why $5^2\cdot\{29,37,41\}$ and
   not $5^2\cdot17$; why the 925/1025 seeds resurrect only along
   their own prime) and (b) the representable-vs-attained gap —
   golden corners are still never actual squares
   (`a9.scaling_law`, `a9.ladder_sweep`, `a9.family_primitivity`).

3. **The fourth-sieve ladder (A9.6–A9.12) — the front's deepest
   result, all PROVEN.** The kills that lie provably beyond every
   congruence and character condition (M12-B: 36 of 57, inside cosets
   of $\mathrm{Cl}^2$; six quartic-Rédei kills at $m = 481/962$; the
   ideal-product law EXACT on all conductor-coprime values) are
   nevertheless governed by an **elementary Diophantine law**:
   - **A9.6**: real lines never die — the $U$- and $V$-center lines
     carry actual sphere points; only the phantom $U\pm V$ lines can
     be killed (the center cap, a theorem for all $m$);
   - **A9.7/A9.7.1**: pairwise Gram necessity
     ($w_iw_j = t^2 + Nk^2$); $\chi_p$-coherence is exactly its local
     shadow;
   - **A9.8/A9.8.1**: the sandwich ($k{=}1$ solvability $\Rightarrow$
     representability $\Rightarrow$ Gram), and the free identities
     (the column law $d^2 + s^2 = 2m^2$ *is* the real lines' witness);
   - **A9.9**: the rank-2 syzygy ($\det_3 = 0$) — with pairwise Gram
     it explains 57/57 anatomy kills;
   - **A9.10/A9.11**: sufficiency — $q = 1$ witnesses certify
     constructively, and the full overlattice lemma (per-prime chain;
     the 2-adic case closed by the family's $8 \mid U$,
     co-norms $\equiv 2 \bmod 8$ congruences forcing an anisotropic
     norm space with unique even-maximal lattice) covers every $q$;
   - **Theorem A9.12 (= C4)**: *a line is representable iff its
     elementary system — three pair equations plus the syzygy — has a
     nondegenerate integer witness.* Verified as an exact equivalence
     on all 88 anatomy lines, corpus samples, and the golden center's
     8 lines. **The class group was the language, never the
     mechanism.**

*The frontier on this front:* the desert in its Diophantine form (why
do the phantom/outer systems fail so persistently — the A9.C2
companion at the witness level, now elementary), the conductor-
entangled extension of the ideal-product law, and the golden-center
regime opening above $3\times10^4$ (W6's telescope, now catching).

## The convergence — the program's central structural finding

The two fronts were built independently and still say the same thing,
now more precisely: **the obstruction to a 3×3 magic square of squares
is genuinely global arithmetic — and where we have fully resolved it
(the sphere front), it is an explicit, elementary, machine-checkable
law, not a transcendental mystery.** No congruence excludes the square
(F5; the beyond-genus kills); what excludes candidate configurations
in every reachable range is the rigidity of one global differential
(surface side) and the Diophantine witness systems of A9.12 (sphere
side) — with the additive coupling, not the class layer, as the
desert's deep cause. This remains the signature of the hardest class
of Diophantine problems; the program's contribution is to have
*located and named* the mechanisms.

## Honest calibration — what none of this does

- **Rational curves are not rational points.** The surface theorems
  constrain *families*; a single magic square of squares would be one
  rational point, and no result here excludes one. Even a complete
  M11-J would yield "no new families" plus — *conditionally on
  Bombieri–Lang* — "at most finitely many squares". Finitely many is
  not zero.
- **A proven sieve law is not a proven desert.** Theorem A9.12 says
  exactly *when* a line survives the representation sieve; it does not
  say the sieves kill every pair forever — indeed they provably do
  not (the golden centers). The desert facts remain range-verified:
  pair desert perfect to $3\times10^4$, additive desert to $10^7$,
  slice confinement and anatomy exact in their stated ranges,
  conjectural beyond. Spectral rigidity is through degree 8, trivial
  character plus full-character vanishing at degrees 5–6 (nontrivial
  characters at $m \in \{7,8\}$: survey in progress, scope-noted).
- **The actuarial reading cuts both ways.** The random model
  (measured inputs, stated dependence caveats) correctly predicted
  the golden onset — evidence that sieve-survival is statistical.
  The same model expects the *additive* coincidences an actual square
  needs to be far rarer still; nothing here converts that heuristic
  into a theorem.
- **Novelty is claimed relative to a full-access literature sweep**
  (2026-08-28, RESEARCH_LOG entry 30: the WANTED backlog cleared; the
  field's own pages confirm nothing new on either surface since BTVA
  2022 / Bruin–Ilten–Xu 2025). Everything is machine-verified;
  **nothing is peer-reviewed** — the A8 and A9 ladders are paper-ready
  claims awaiting external eyes (ROADMAP W8).
- **The one claimed proof in the field is refuted, not the problem
  solved**: the A1 re-audit proves the arXiv:2510.08286v3 argument
  invalid — its eq. (29) is an identity-multiple of its own
  constraint, and its final inference fails on an explicit six-square
  witness. A statement about a paper, not about the problem.
- The multi-hour computations are recorded artifacts with pinned
  system shapes; the suite re-verifies exactly what is cheap enough
  to re-verify (the $\eta_\star^2$ certification, the sampled desert
  kills, the golden center's lines, live, in exact arithmetic).

## What an actual resolution would still require

Three known-shaped paths, all hard, none with a visible finish line:
**(i)** the arithmetic endgame on $X$ — Picard/Galois module through
the 19-orbit atlas, then a Brauer–Manin/twist-descent global
obstruction (Conjecture E; the cuboid literature provides the
template); **(ii)** the desert as a theorem in its now-elementary
Diophantine form — why the phantom and outer witness systems fail,
uniformly enough to matter, with the golden regime showing exactly
where uniformity ends; **(iii)** something genuinely new (the
abc/Vojta bridge of A2 §6 is formulated; the naive route is a
recorded FAILED-ATTEMPT). In the other direction, existence would
need a construction or a search far beyond current bounds — the
structure found here is evidence *against* accessible solutions and
proof of nothing asymptotic.

## Reproducing the state

```sh
python3 -m verify              # 124 checks, FULL bounds
python3 -m verify --only a8    # the surface front (incl. the atlas)
python3 -m verify --only a9    # the sphere front (incl. the ladder)
python3 -m verify --only c4    # Theorem A9.12 end-to-end
```

Attack documents: [A8](attacks/A8-descent-differentials.md) (surface),
[A9](attacks/A9-discrete-spheres.md) (spheres), with A1–A7 and the
foundations F1–F6 linked from the [README](../README.md); the battle
plan is [ROADMAP.md](ROADMAP.md).
[RESEARCH_LOG.md](../RESEARCH_LOG.md) is the dated narrative,
entries 1–44.
