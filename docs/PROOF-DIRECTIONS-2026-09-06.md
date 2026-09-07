# Proof directions after the twist audit

**Historical review, with follow-through now recorded.** Entries 118–120 repaired the remaining twist sites, closed the sixteen C2 cases, and folded the prime-column lemma into the ledgers. The open counts are now 488 and 4,744. The engine filter and [reproducible inventory](RESEARCH-INVENTORY.md) are implemented. [A10](attacks/A10-cancellation-descent.md) settles the first valuation-support experiment and derives the leading-unit congruences. The [current roadmap](ROADMAP.md#r12-current-research-portfolio-2026-09-06) keeps cancellation descent as the lead within a diverse, revisable portfolio. The review and counts below describe the earlier commit and are preserved as history.

Written against `d5dbf48`, 2026-09-06. The main purpose is to propose proof mechanisms that can extend across exponent shapes and numbers of primes. Section 2 contains a complete elementary lemma; its novelty relative to the literature is not asserted. The subsequent research programs are proposals, not claimed solutions of the magic-square problem.

## 1. Light review of the repairs

The repaired `_disc_model`, square-only content reduction, denominator clearing in the towers, and decision-policy cache key address the defects at those locations. `python -m verify --fast --only omega3_twist` passes, including the original rational-point control and one live recheck of a withdrawn tower exclusion. PARI discovery is now configurable. Complete certification, gauntlet coverage and the fast-profile budget are explicitly deferred.

There are still copies of the constant-dropping operation in `compute/omega3_unknowns.py:47` and `compute/omega3_quotients.py:365,470`. The first has a live counterexample even after the repair:

```python
import sympy as sp
from compute.omega3_unknowns import _rank0_model_points
t = sp.Symbol('t')
D = 337*(t**4 + 1)
assert D.subs(t, sp.Rational(4, 3)) == sp.Rational(337, 9)**2
print(_rank0_model_points(D, t))
# Current output claims a complete rank-zero model t^4+1 with t-values [0].
```

The returned list misses the displayed rational point. This does not identify a newly incorrect committed campaign verdict, but the remaining paths must retain their constants too. `gp_model` should also explicitly require integral coefficients or clear rational denominators by a square: its current `int(c)` conversion silently truncates general rational inputs. The current R.11 opening paragraph still uses the old 1492/1452 tally despite the corrected audit record.

No existing proof code or campaign verdict was changed in this follow-up. A read-only census script accompanies the mathematical argument below.

## 2. A universal prime-column lemma

**Status: PROVEN by the argument below.** This uses only the two additive equations and the existing Gaussian-prime frame dictionary. It applies to every number of distinct split primes and every exponent shape.

Write the four signed offsets as

\[
d_A=U,\quad d_B=V,\quad d_C=U+V,\quad d_D=U-V.
\]

For a candidate with center root split part \(\prod_j p_j^{a_j}\), let \(e_{X,j}\) be the exponent label of offset X at prime \(p_j\). Signs in front of an offset do not affect valuations. Then:

> For every prime column j with some nonzero label, the maximum of
> \(|e_{A,j}|,|e_{B,j}|,|e_{C,j}|,|e_{D,j}|\)
> must occur at least three times.

### Proof: the additive half

For any odd prime p, the minimum of

\[
v_p(U),\ v_p(V),\ v_p(U+V),\ v_p(U-V)
\]

occurs at least three times, assuming the four numbers are nonzero.

If \(v_p(U)<v_p(V)\), both U+V and U−V have valuation \(v_p(U)\), giving three minima. The reversed inequality is identical. If the valuations are equal to k, divide U,V by p^k. The resulting u,v are units. Both u+v and u−v cannot vanish modulo p, since their sum is 2u, a unit. Thus at least one of U+V,U−V has valuation k, again giving three minima.

Equivalently, use all four three-term relations:

\[
d_A+d_B=d_C,\quad d_A-d_B=d_D,\quad
2d_A=d_C+d_D,\quad 2d_B=d_C-d_D.
\]

All coefficients are p-adic units for odd p. Requiring a repeated minimum in every three-element subset forces at least three minima among the four values. The last two relations can exclude patterns that pass each original equation separately.

### Proof: the Gaussian-frame half

Fix \(p_j=\pi_j\bar\pi_j\), with distinct nonassociate Gaussian primes, and use the project's frame \(\ell_j=\pi_j^2\). Ignoring the non-split scalar, which is a unit at \(p_j\), a labeled offset is

\[
d_X=\left(\prod_j p_j^{2(a_j-|e_{X,j}|)}\right)
\operatorname{Im}\left(\prod_j \ell_j^{2e_{X,j}}\right),
\]

where a negative exponent inside this formula means a positive power of the conjugate, as in `elem_box`, not an inverse.

When \(e_{X,j}\ne0\), precisely one of the Gaussian product and its conjugate is divisible by \(\pi_j\). All factors belonging to the other distinct primes are units there. Their difference is therefore a unit at \(\pi_j\). Since 2i is a unit too, the imaginary part is a unit. The offset is a rational integer, so its Gaussian valuation at \(\pi_j\) equals its ordinary p_j-adic valuation. Consequently

\[
v_{p_j}(d_X)=2(a_j-|e_{X,j}|)\qquad(e_{X,j}\ne0).
\]

When \(e_{X,j}=0\), the corresponding valuation is at least \(2a_j\). It need not equal \(2a_j\), which is why the zero-label case must be stated separately.

Let \(M_j=\max_X|e_{X,j}|>0\). The minimum offset valuation is exactly \(2(a_j-M_j)\), attained precisely by labels with absolute exponent M_j. The additive half requires at least three such labels. This proves the lemma. ∎

### Stronger form for primitive squares

For a primitive square, \(M_j=a_j\). Otherwise all four offsets and the center m² are divisible by \(p_j^2\), so all nine roots are divisible by p_j, contradicting primitivity. Thus at every split prime dividing the center root, **at least three labels are at the full exponent**, and at most one has an exponent deficit.

This gives a useful arithmetic organization of arbitrary prime support: each center prime has either no deficit or a deficit assigned to exactly one of A,B,C,D. It does not bound how many primes may occur, and it does not itself exclude all patterns.

### Immediate consequence: every free-frame class is impossible

A frame appearing in exactly one label has a unique positive column maximum, violating the lemma. This excludes every free-frame class for every exponent shape, without invoking any two-prime ladder theorem, weighted-relation theorem, elliptic rank or point computation. In particular, proving a separate content-2 theorem is unnecessary for closing the remaining free-frame cases of entry 116.

### Exact census on the current records

**Status: VERIFIED on the two committed data files at d5dbf48.** Run:

```sh
python -m compute.valuation_signature_probe
```

| Recorded finite classes | Fail an original equation's valuation condition | Additional failures using the combined equations | Survive the column lemma |
|---|---:|---:|---:|
| (1,1,1): 1,460 | 878 | 78 | 504 |
| Additional (2,1,1): 63,336 | 55,700 | 2,892 | 4,744 |

Thus the lemma excludes 956 and 58,592 currently finite classes respectively. If combined with the recorded exclusions, the resulting partitions would be 2,440 dead / 504 finite for (1,1,1), and 74,624 dead / 4,744 finite for the 79,368 additional (2,1,1) classes. These are derived counts; the script does not rewrite the official ledgers.

All 4,230 remaining finite free-frame classes fail. The sixteen C2 classes from the previous review all survive, so the bielliptic descent remains relevant. Most newly excluded classes already fail a valuation condition of an original equation: the current three-frame geometric engine did not carry the elementary prime-specific filter through its computations on arbitrary Pythagorean frame ratios.

Independent consistency checks use Gaussian integer multiplication without importing the curve engine: 522 frame valuations and 24,750 examples of the additive minimum rule. The finite checks support the implementation; the proof above supplies the universal quantifier.

## 3. Main ambitious program: cancellation patterns and global descent

The prime-column lemma is the first step of a larger approach: classify how a prime can participate in the full system before introducing its numerical value or bounding its exponent.

Normalize the four Gaussian squares to circle points z_A,...,z_D of norm 1. With \(s(z)=z-z^{-1}\), the equations are

\[
s(z_A)+s(z_B)-s(z_C)=0,\qquad
s(z_A)-s(z_B)-s(z_D)=0.
\]

These define one fixed Laurent-polynomial ideal in four variables. Prime columns are valuation directions of its points, with additional even-valuation and square-lifting conditions from the Gaussian squares. Computing the initial ideals for the whole ideal can expose cancellation constraints missed by its two displayed generators. The distinction between a tropical prevariety from generators and the tropical variety of the full ideal is standard; finite tropical bases provide a systematic framework ([Bogart–Jensen–Speyer–Sturmfels–Thomas](https://arxiv.org/abs/math/0507563)).

**First experiment.** Determine whether the three-maxima condition exhausts the valuation obstruction, or whether further initial-ideal conditions remove additional sign patterns. Work symbolically with arbitrary exponent sizes. Keep special coefficient primes separate. A finite fan is an organization of necessary conditions, not a nonexistence theorem.

**The research target that could reach arbitrary prime support.** On each surviving cone, retain the leading-unit equations as well as valuations. The cancellation at one Gaussian prime gives divisibility conditions on expressions involving the others. Search for a finite collection of such relations whose absolute-value estimates force either a proper torsion-coset relation or a descending cycle of heights.

A schematic cycle has p forcing a lower bound on q, q on r, and r on p. A positive net gain, with every constant controlled, could give a contradiction or an effective global height bound. The missing theorem is precisely that every admissible primitive configuration must have such a cycle. Neither a cycle nor its positive gain follows merely from the column lemma.

**Why this is distinct from extending the box census.** The objects to classify are the few possible cancellation roles of a prime, including their leading units. The hoped-for proof depends on those roles, rather than on how many primes or exponent labels have been enumerated. It would generalize the successful concentration/window arguments into a mechanism for the coupled system.

**Success criterion.** One symbolic reduction valid for an infinite family of surviving prime signatures, with a strict height decrease, a uniform bound, or a torsion-coset contradiction. Pure congruence pruning cannot be the final step: the system has local solutions.

**Stop criterion.** If the initial ideals add nothing beyond the column lemma, stop expanding the tropical computation and investigate the residue-unit/height step. If proposed cycles also occur in admissible local models but give no global inequality, do not call their prevalence evidence of a descent theorem.

## 4. Second program: preserve lifts and manufacture useful elliptic quotients

The C2 example suggests a general proof-design principle: a low-genus quotient with a difficult Jacobian can discard the very lifting conditions that make the original arithmetic tractable.

For models of the form

\[
y^2=A(t^2)B(t^2),
\]

analyze the gcd of the homogenized forms before attempting all rational points of the quotient. A resultant controls the possible common prime divisors, with leading coefficients and denominator valuations handled explicitly. A finite set of common squareclasses delta gives covering constraints such as

\[
z^2=\delta B(t^2).
\]

When B is cubic, this is a bielliptic genus-2 curve, with elliptic quotients given by B(s) and sB(s), including the twist delta. The previous review's two curves have both elliptic factors of rank 1, fitting [Bianchi–Padurariu's method](https://arxiv.org/abs/2212.11635) and its [Sage implementation](https://github.com/bianchifrancesca/QC_bielliptic).

**First experiment.** Apply this construction to the 504 surviving finite (1,1,1) classes, beginning with the sixteen C2 classes. Record which square-lifting constraints were lost at each quotient, and which factor-wise descents restore elliptic quotients of useful rank. Include every exceptional fiber.

**Ambitious target.** Prove a family theorem: a specified label structure always produces a bounded collection of twist models with controlled elliptic factors. This could replace thousands of unrelated high-genus point problems with a small reusable arithmetic argument.

**Risk.** Resultants and their prime supports can grow with exponents; simple high-dimensional Jacobian factors may remain. Neither the finite twist list nor the favorable rank pattern is presently uniform. The sixteen-class calculation is the appropriate first test of the mechanism.

## 5. Third program: treat the quartic differential as a dynamical system

The surface program has an explicit differential but mostly studies its integral curves by increasing degree. There is another concrete object to investigate: the foliation obtained by adjoining the tangent slope.

On the chart u=1, put p=dc/dv. Factoring the stored quartic differential and removing its common degree-9 numerator factor gives the slope equation

\[
F(c,v,p)=c(c^2-1)-3c(c^2+v^2-1)p^2
 +2v(3c^2+v^2-1)p^3-3cv^2p^4=0.
\]

**Status: VERIFIED exact identity** against `compute.web_lines.eta_star()`. Removal is valid only away from that common divisor; its components and chart-boundary curves must be handled separately.

On the slope surface F=0, the vector field

\[
\mathcal D=F_p(\partial_v+p\partial_c)
 -(F_v+pF_c)\partial_p
\]

is tangent: \(\mathcal D(F)=0\) identically. Away from the singular/vertical locus, integral curves of the web lift to trajectories of this field.

**First experiment.** Search for a nonconstant rational first integral H, satisfying D(H)=0 modulo F, or invariant algebraic curves through Darboux-polynomial/extactic constructions. This provides a systematic alternative search object to arbitrary plane curves. [Pereira's work](https://arxiv.org/abs/math/0011205) gives computational criteria for rational first integrals of a specified degree and the relevant invariant-variety framework. Applicability to the singular slope surface requires checking its hypotheses after normalization/resolution.

**Ambitious target.** If a first integral exists, compute the generic fibers and their pullbacks to the magic-square surface, then classify exceptional fibers that could carry rational curves. Alternatively, derive a justified degree bound from the resolved foliation's singularity structure. Either outcome could replace unbounded degree-by-degree scanning by a complete geometric classification.

**Risk and scope.** A rational first integral may not exist. Failure to find one at bounded degree proves little; plane-foliation degree bounds cannot automatically be applied to this slope surface. Even a complete rational-curve classification proves a statement about families and the function-field problem, not nonexistence of isolated rational magic squares.

## 6. Recommended sequence

1. Review and incorporate the prime-column lemma, with a certificate for each newly excluded class. Finish the remaining twist-normalization fixes separately.
2. Rebase all research inventories on the actual 504 and 4,744 survivors. Do not spend more curve-computation time on the free-frame remainder: the lemma excludes it uniformly.
3. Make cancellation-pattern/global-descent research the principal attempt at a proof for arbitrary prime support. Use the remaining classes as difficult examples for proposed lemmas.
4. Execute the C2 bielliptic descent as the concrete arithmetic test, and the slope-surface first-integral calculation as the geometric test. Broaden either program only when it yields a mechanism that extends beyond its initial example.

The intended measure of progress is a statement that covers infinitely many cases, or that converts an ineffective conclusion into a complete finite proof. Raw box size and the number of computed genera are supporting data.
