# Independent proof research: workspace and strategy

Status: global cover-compatibility direction approved by the owner, 2026-09-09.
First investigation: finite Brauer-obstruction limitations and boundary covers.

Checkpoint: [global-obstructions.md](docs/research/global-obstructions.md).
It records the finite-Brauer barrier on the original open surface, failed
entry-symbol and homogeneous-direction approaches, and a root-sum cover
with twist (34,178,3026) that is locally soluble everywhere. GB.8 now
excludes its u=0 genus-three boundary using Tunnell's theorem and an exact
finite certificate. Together with GB.7 and the projective-image audit,
this gives a smooth proper model with no rational boundary points.
No MSS3 or campaign classes were newly excluded.

Current priority, explicitly approved by the owner: the universal
reduction, not additional isolated twists. The new
[universal-twist note](docs/research/universal-twist-reduction.md) proves
that every hypothetical solution reaches a signed odd squarefree triple
with sum 3 mod 8 and unit lift coordinates at 2. It couples the labels'
prime factors to the center and primitive direction. A full 401-adic
control shows signs and D4 symmetry do not locally force the earlier
product-square subfamily.

The [coupled-cycle continuation](docs/research/coupled-cycle-descent.md)
now combines the frames into four independent even-cycle parameters.
Their support depends only on the primitive direction, independently of
the center and common offset factor. All four are 1 mod 8 under canonical
signs. An infinite permitted subfamily still has smooth rational boundary,
so an unrestricted finite-Brauer exclusion cannot handle the entire family.

The [finite-descent audit](docs/research/finite-descent-barrier.md) now
extends the barrier to the canonical domain at 2. Demeio's rational-boundary
lifting theorem, combined with Harari's formal lemma, leaves a surviving
twist after any fixed finite torsor/finite-Brauer step. Adding another
finite cover alone cannot complete that universal proof template.

The [arithmetic continuation](docs/research/arithmetic-descent-audit.md)
now gives an exact divisor model for the corner-label-1 branch:
n^2=(ai+cg)/2, with r,s dividing n^2, and five retained square tests for
the center and four sides. It also proves that a homogeneous linear
formula centered at n has constant projective shape. Quadratic
numerators over a common linear denominator reduce projectively to a
linear formula; the apparent n scale cancels on primitive normalization.
These are restrictions on constructions, not exclusions of solutions.

The [nonlinear continuation](docs/research/nonlinear-descent-fibers.md)
identifies n -> rs/n as a reflected rescaling: it preserves all five
tests but leaves the primitive center unchanged. At every admissible
rational ratio k=r/s, the full five-square fiber is a degree-32 cover
with 20 simple branch points, hence genus 129 by Riemann--Hurwitz.
Elliptic multiplication cannot lift to a rational self-map of that full
fiber. These genus and map-degree statements are CITED deductions from
classical curve theory, supported by exact branch certificates. Each
fiber retains 128 rational AP boundary points; its rational interior
is unclassified.

Resume with a point-dependent change of divisor ratio or a multivalued
arithmetic correspondence with a justified rational branch. It must
preserve the five square tests, retain an iteratable domain and strictly
decrease the primitive integer invariant. A uniform arithmetic exclusion
of the divisor system is another option. No such construction or exclusion
is known. The nontrivial corner labels remain unbounded and need a universal
argument as well. Any alternative integral or height restriction must be
justified for every candidate in its scope.
The [root-reciprocity note](docs/research/root-functions-and-reciprocity.md)
(2026-09-17) closes the last untracked item of the previous session: the
exact Hilbert-symbol evaluator on the root ratios, with local controls
showing the symbol is not locally forced; a failed attempt as an exclusion.
See the [handoff](docs/research/GLOBAL-OBSTRUCTION-HANDOFF.md).

## Workspace

- Branch: `research/proof-alternatives`.
- Worktree: `.worktrees/proof-alternatives` under the primary checkout.
- Fork: `a719b635e7ca969ef62a805d85c0a9d6b5fbc17e` (main, entry 140).
- Created: 2026-09-09.
- Main's uncommitted files were not copied into this worktree.
- `.worktrees/` is already excluded by the repository's local Git rules.

Run research commands with this worktree as their working directory. Worktree
files are separate, but Git refs and metadata are shared. Do not switch,
reset, clean, or update another worktree or its branch. Avoid concurrent
heavy calculations until machine resource use is coordinated.

## Existing tracks, as observed during setup

| Location | Documented work |
|---|---|
| Primary checkout, main | Symmetry towers, admissibility twists, endpoint point arithmetic, and exclusions for prime-exponent shapes; committed through entry 140, with further Magma-related files uncommitted. |
| `.worktrees/independent-cofactors` | Uniform prime-column grouping, exact cancellation cofactors, compatibility between circuits, and possible descent. Its charter and first results are uncommitted at this checkpoint. |

The owner accepted this division of work. These descriptions record the
files observed at setup; they do not track other agents' subsequent work.

## Agreed track: global compatibility of square covers

Investigate arithmetic obstructions on the magic-square surface or a
specified auxiliary cover, using the retained square conditions. This
follows the independent cover-compatibility proposal in
`docs/REVIEW-AND-PLAN-2026-09-08.md`, section 4.D, and the longer-term
W2/W3 program in `docs/ROADMAP.md`.

The question is whether a concrete descent or Brauer class can constrain
nondegenerate rational points beyond the conditions already retained by
the current campaigns. This is a proposed investigation, not a claim that
such a class exists or can exclude all admissible points.

### First checkpoint

1. Audit the exact surface, maps, removed divisors, and relevant prior
   attempts. Use the explicit nine-entry-line model in A5 and the later
   character atlas in A8; reconcile historical roadmap descriptions with
   those models before using them.
2. Select one explicit cover or quotient and state how every point in the
   claimed scope reaches it, including exceptional fibers and square-lift
   conditions. State whether the scope is universal or a restricted family.
3. Construct a candidate class or descent condition. Establish its domain,
   ramification behavior, and nontriviality on the actual target. In
   particular, check that a proposed class does not become trivial when
   the original square roots are adjoined.
4. Compute exact evaluations or compatibility conditions where justified.
   Check known rational degeneracies and every applicable falsification
   control; explain precisely what new restriction, if any, survives.
5. Deliver either a rigorously verified restriction with explicit scope,
   or a precise account of why the chosen construction fails and what that
   failure rules out. A class on a quotient alone is not an exclusion on
   the original surface; a finite sample is not a uniform obstruction.

Any prospective route to full impossibility must account for isolated
admissible rational points. Classifying rational curves alone is insufficient.
Known degenerate rational points must be accommodated explicitly. Do not
assume that degenerate and nondegenerate points occupy disjoint twist classes.

## Alternatives for alignment

- The parked two-split-prime, arbitrary-exponent frontier: a narrower
  uniform theorem target, distinct from the current higher-support campaigns.
- The explicit differential web and its integral curves: a geometric
  explanation of families, with an additional arithmetic step still needed
  for an impossibility proof about individual points.

These alternatives are reserves; the global compatibility track is active.

## Evidence and integration

Follow `docs/protocol/status-taxonomy.md` and
`docs/protocol/sanity-checks.md`. Keep exploratory documents, code, and
artifacts in branch-specific files. Avoid editing the shared research log,
roadmap, campaign ledgers, or global theorem numbering during exploration.

At a mathematical checkpoint, record hypotheses, exact certificates and
checks, source versions, remaining gaps, and an integration note. Review
upstream changes before deliberately integrating them; do not merge
automatically or silently reinterpret data generated at another checkpoint.
