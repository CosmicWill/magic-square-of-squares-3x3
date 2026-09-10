# Global-obstruction checkpoint, 2026-09-10

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
  then a complete 3-adic obstruction).
- GB.8: **CITED deduction from Tunnell's unconditional theorem:** the u=0
  genus-three boundary has no rational points, including projective and
  exceptional fibers. It maps to y^2=89(1-t^4). A nonexceptional point
  gives a rational right triangle of area 89, but the complete ternary
  counts are N8=48 and N32=20, contradicting N8=2*N32. No BSD assumption.
- GB.8: the selected cover has a smooth proper compactification with
  **no rational boundary points**. The proof uses the morphism to the
  projective base to cover infinity, zero entries, all degeneracy lines,
  normalization and exceptional divisors. Surface resolution and the
  four-square AP theorem remain CITED inputs. An explicit blowup sequence
  and a Brauer-group computation have not been carried out.
- An explicit row quartic and the five additional square conditions needed
  to recover the full cover are recorded at the end of GB.8. PARI/GP 2.17.4
  independently gives rank zero and torsion order two for the decisive
  elliptic quotient; the exclusion proof does not depend on that computation.

Full proofs, status distinctions, sources, and maps are in
[global-obstructions.md](global-obstructions.md). All labels are local
to this research note, not replacements for the repository's A-series.

## Next concrete task

Start with the row quartic in GB.8 and derive an explicit fibration or
candidate Brauer class. Retain all five additional square conditions;
test whether a class survives their pullback before evaluating it.
Then certify ramification on a specified smooth model and local evaluations.
The selected cover's rational-point set is still unknown. Removing the
rational-boundary explanation for GB.3 does not prove a Brauer obstruction.

Before any larger campaign, establish a necessary restriction on the full
twist family. This one twist does not cover every hypothetical MSS3;
neither q3=q1*q2 nor these three constants have been shown necessary.

## Reproduce

```text
python -m compute.global_obstruction_probe --ap-bound 100
python -m compute.global_obstruction_probe --boundary-certificate
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --fast --only f1.
python -m verify --fast --only f4.
python -m verify --only gauntlet
```

The 11 branch checks passed at FULL bounds (three added since 2c91f31).
The complete count certificate and the separate GP quotient diagnostic
also ran successfully. The suite has 233 registered checks in this worktree.
Five existing f4 checks at FAST bounds and both gauntlet checks at FULL
were rerun and passed: 18 checks passed in this continuation.
At the preceding checkpoint, 18 related existing checks passed (a5, f5,
f1, f4 at FAST bounds; the two gauntlet checks at FULL). This is not a
replay of the full suite or other branches' computations.

Optional PARI diagnostic, using the actual executable rather than the
PowerShell `gp` alias:

```powershell
& 'C:\Users\Will\pari-2.17.4\gp.exe' -q -f compute/global_boundary_quotients.gp
```

The new checks cover explicit algebra and finite calculations. They do
not reprove Harari, Lang--Weil, Hasse--Minkowski, Riemann--Hurwitz, Tunnell,
or surface resolution. No
candidate nonexistence proof or new MSS3 exclusion is asserted.
