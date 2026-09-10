# Independent proof research: setup and proposed strategy

Status: global cover-compatibility direction approved by the owner, 2026-09-09.
First investigation: finite Brauer-obstruction limitations and boundary covers.

Checkpoint: [global-obstructions.md](docs/research/global-obstructions.md).
It records the finite-Brauer barrier on the original open surface, failed
entry-symbol and homogeneous-direction approaches, and a root-sum cover
with twist (34,178,3026) that is locally soluble everywhere. Its all-equal
rational fibers and v=0 AP boundary are excluded; the u=0 genus-three
boundary remains open. No MSS3 or campaign classes were newly excluded.

Resume with the AP-u curve in GB.7, including projective fibers. A rational
boundary point would bring back GB.3; a bounded search with no points is
not a boundary exclusion. The full twist family, rather than this one
test case, would have to be controlled for a universal impossibility proof.

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
