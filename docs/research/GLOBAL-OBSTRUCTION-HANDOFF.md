# Global-obstruction checkpoint, 2026-09-09

Source: main `a719b635e7ca969ef62a805d85c0a9d6b5fbc17e`, through entry 140.
Branch: `research/proof-alternatives`. Calculations ran locally; primary
literature was consulted online. Other agents' files and campaign ledgers
were not changed, and no messages were sent to other people or agents.

## Results to review

- GB.1--2: entry-monomial quaternion classes pull back to constants, and
  the original square cover has trivial twist label at every full rational
  square configuration. These do not furnish the proposed separation.
- GB.3: **CITED consequence of Harari's formal lemma**, with all hypotheses
  verified for the normalized surface: any finite B in Br(U) has nonempty
  U(A_Q)^B, even allowing ramification along deleted degeneracies. The
  proof handles almost-all integrality, not just a product of local sets.
- GB.4: a concrete root-dependent quaternion is nontrivial but regular at
  the all-equal rational point; stronger fourth-power local controls exist.
- GB.5--6: the homogeneous direction covers have a rational-boundary trap.
  One/two-line twists always have a smooth rational boundary point; the
  three-line locally soluble case reduces to Hasse--Minkowski. Four-line
  direction boundaries give 70 subsets and 11 geometric genus-one types,
  but any rationally realizable direction again supplies a boundary point.
- GB.7: the degree-eight root-sum cover
  34 z1^2=A+B, 178 z2^2=B+C, 3026 z3^2=C+A is geometrically integral,
  locally soluble at every place, and has no rational signed all-equal
  fiber. Its v=0 AP boundary has no rational lift (real sign selection,
  then a complete 3-adic obstruction). The u=0 boundary is a genus-three
  curve, still open. The 12,178-case parameter search is only bounded evidence.

Full proofs, status distinctions, sources, and maps are in
[global-obstructions.md](global-obstructions.md). All labels are local
to this research note, not replacements for the repository's A-series.

## Next concrete task

Decide the AP-u curve in GB.7, starting with its quotient curves or a
descent and preserving every branch and infinite fiber. If it has a
rational point, it restores the finite-Brauer limitation for this twist.
If it has none, finish the smooth-model boundary audit before computing a
Brauer class. This one twist does not cover every hypothetical MSS3;
uniform control of twist classes remains a separate unresolved requirement.

## Reproduce

```text
python -m compute.global_obstruction_probe --ap-bound 100
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --fast --only f1.
python -m verify --fast --only f4.
python -m verify --only gauntlet
```

At this checkpoint the eight new checks passed at FULL bounds; 18 related
existing checks passed (a5, f5, f1, f4 at FAST bounds; the two gauntlet checks
at FULL). The suite has 230 registered checks in this worktree. This was
not a replay of the full suite or other branches' computations.

The new checks cover explicit algebra and finite calculations. They do
not reprove Harari, Lang--Weil, Hasse--Minkowski, or Riemann--Hurwitz. No
candidate nonexistence proof or new MSS3 exclusion is asserted.
