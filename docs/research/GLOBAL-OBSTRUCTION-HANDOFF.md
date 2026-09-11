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

## Universal reduction continuation

The owner asked to make the universal reduction the lead question.
[universal-twist-reduction.md](universal-twist-reduction.md) records:

- UT.1, **PROVEN:** the exact eight-element root-sign orbit of the product
  class T. The four noncentral frames account for D4 symmetry.
- UT.2, **PROVEN:** every hypothetical MSS3 reaches a cover with signed
  odd squarefree q_i, sum(q_i)=3 mod 8, and z_i 2-adic units. There are
  16 residue triples, but infinitely many numerical labels. Every triple
  in this family has full admissible local lifts at 2; the normalization
  does not create a new local obstruction.
- UT.3, **PROVEN:** the triple gcd of the labels divides the squarefree
  center; pairwise shared primes come from the center or gcd(U,V); center
  primes 5 mod 8 occur in all labels or none according to center parity.
  More precisely q1*q2*q3=m*H times a rational square, with H supported
  only on primitive-direction differences. Once that direction is fixed,
  H has finitely many possibilities independently of m and gcd(U,V).
- UT.4, **PROVEN:** a full admissible Q_401 configuration has nonsquare
  product class in all four frames and all eight sign choices. Thus the
  earlier product-one restriction is not forced locally or algebraically
  by the square equations and symmetries. This does not refute a possible
  additional global theorem solely about rational admissible points.

## Next concrete task

The [coupled-cycle continuation](coupled-cycle-descent.md) proves:

- CC.1: four even-cycle parameters are signed odd squarefree and 1 mod 8;
  their support depends only on the primitive direction, independently of
  m and G. The first two labels have gcd dividing 5.
- CC.2: the corner-cycle class is (ai+cg)/(2m^2); four independent divisor
  valuations certify that the combined cover has geometric degree 16.
  A full Q_97 point has nonsquare corner class under every sign and D4 choice.
- CC.3: every single corner double cover has a smooth rational boundary
  point on an explicit blowup chart, regardless of its coefficient.
- CC.4: an infinite subfamily of the simultaneous permitted covers has
  smooth rational boundary too. The first explicit tuple is
  (-119,-15,1,-7), with direction (1,8). By GB.3, unrestricted finite
  ordinary Brauer tests cannot exclude these twists. This does not settle
  the canonical 2-adic subdomain or another justified integral restriction.

Seek a global compatibility condition retaining canonical roots and unit
lift coordinates at 2, or a further descent preserving the full grid.
Keep the primitive direction unbounded. If computing a Brauer class,
audit its ramification on a proper model and survival after all original
and cycle square roots are restored. Merely testing a quotient is insufficient.

The UT.2 family still includes twists with smooth rational boundary
points, so the GB.3 barrier remains relevant. The selected fixed cover's
rational-point set is also still unknown. No uniform global contradiction
or finite reduction of the numerical twist labels has been proved.

## Reproduce

```text
python -m compute.global_obstruction_probe --ap-bound 100
python -m compute.global_obstruction_probe --boundary-certificate
python -m compute.universal_twist_probe --precision 8
python -m compute.coupled_cycle_probe
python -m verify --only cce.
python -m verify --only ut.
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --fast --only f1.
python -m verify --fast --only f4.
python -m verify --only gauntlet
```

At checkpoint bfd894a, the 11 gb branch checks passed at FULL bounds
(three added since 2c91f31).
The complete count certificate and the separate GP quotient diagnostic
also ran successfully. That checkpoint had 233 registered checks.
Five existing f4 checks at FAST bounds and both gauntlet checks at FULL
were rerun and passed: 18 checks passed in this continuation.
At the preceding checkpoint, 18 related existing checks passed (a5, f5,
f1, f4 at FAST bounds; the two gauntlet checks at FULL). This is not a
replay of the full suite or other branches' computations.

The universal continuation adds five ut checks (238 registered total).
Their FULL run passed: 277 canonical AP controls x 4 frames, 199 support
controls x 4 frames, 19 full square-grid lifts to 2^24, and the complete
32-product residue certificate with all nine roots lifted to 401^8.
The all-precision local statements follow from the written lifting proofs.
The support check also uses 12 admissible local grids x 4 frames x 8
sign choices, independently checking cancellation of a common offset prime.
The 11 gb checks and both gauntlet checks also passed at FULL bounds in
this continuation, along with the five f4 checks at FAST bounds: 23
relevant checks passed in total. The strengthened product support identity
was followed by another successful run of all five ut checks.

The coupled-cycle continuation adds five cce checks (243 registered total).
All five cce, five ut, eleven gb and two gauntlet checks passed at FULL
bounds: 23 targeted checks. The new certificates include four independent
valuation rows, all 16 canonical offset residues modulo 32, 400 signed
corner identities, a complete 97-adic sign certificate, the explicit
resolved boundary point, and nine admissible local lifts on the rescaled
degree-16 cover. An initial broad substring filter also ran and passed
the seven existing a7cc checks; the new prefix is now cce to avoid that
unrelated match. This was not a replay of the full verification suite.

Optional PARI diagnostic, using the actual executable rather than the
PowerShell `gp` alias:

```powershell
& 'C:\Users\Will\pari-2.17.4\gp.exe' -q -f compute/global_boundary_quotients.gp
```

The new checks cover explicit algebra and finite calculations. They do
not reprove Harari, Lang--Weil, Hasse--Minkowski, Riemann--Hurwitz, Tunnell,
or surface resolution. No
candidate nonexistence proof or new MSS3 exclusion is asserted.
