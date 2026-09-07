# Cancellation patterns and global descent

2026-09-06. A lead investigation within the [research portfolio](../ROADMAP.md#r12-current-research-portfolio-2026-09-06), with independent geometric, arithmetic, and experimental attacks kept active. The magic-square problem remains open. Novelty relative to the literature is not asserted for the elementary results below.

The prime-column lemma [A3.PC](A3-simultaneous-congrua.md#249-the-prime-column-lemma-theorem-a3pc-a-uniform-exclusion-from-the-valuations-alone-entry-120) is proved. The [survivor inventory](../RESEARCH-INVENTORY.md) contains the 488 open finite classes of (1,1,1) and the 4,744 open classes of the additional (2,1,1) campaign. This note takes the first step beyond their valuations.

## 1. The fixed equations and what has been relaxed

Write the signed offsets as A=U, B=V, C=U+V, D=U−V. For distinct split primes let

\[
 \rho_j=\pi_j/\bar\pi_j,\qquad
 Z_X=\prod_j\rho_j^{2\epsilon_X e_{X,j}},\qquad s(Z)=Z-Z^{-1}.
\]

The Gaussian frame dictionary gives \(d_X=m^2s(Z_X)/(2i)\), with the common nonsplit scalar included in m. Thus

\[
 F=s(Z_A)+s(Z_B)-s(Z_C)=0,\qquad
 G=s(Z_A)-s(Z_B)-s(Z_D)=0.
\]

In the original problem the Z are squares in Q(i), have norm one, and share the prescribed prime support. If we allow four independent variables in an algebraically closed valued field, those arithmetic restrictions disappear. Keeping that distinction explicit is essential.

## 2. CP.1: the column rule exhausts rational valuation directions of the relaxed system

**Proposition (proved here).** Over the algebraic closure of Q((t)), a rational vector w occurs as \((v(Z_A),\ldots,v(Z_D))\) of a solution of F=G=0 if and only if w=0 or the largest \(|w_X|\) occurs at least three times. There is no further restriction on the signs of w from this Laurent ideal.

**Necessity.** Set y_X=s(Z_X). When w_X is nonzero, v(y_X)=−|w_X|; when w_X=0, v(y_X)≥0, allowing y_X=0. For nonzero w, the negative minimum of the four y-valuations is attained exactly at the maximal |w_X|. The four additive circuits, with coefficients 1 and 2, require at least three such minima by the additive half of A3.PC. The argument still works when a nonminimal y_X vanishes.

**Sufficiency.** Rescale rational weights to integer weights, using a root of t if necessary. Put M=max |w_X|. If there is one exceptional coordinate E of magnitude m<M, set its y-value to b=t^(−m), and use a=t^(−M) in the following table:

| Exceptional coordinate | y_A | y_B | y_C | y_D |
|---|---|---|---|---|
| A | b | a | b+a | b−a |
| B | a | b | a+b | a−b |
| C | a | b−a | b | 2a−b |
| D | a | a−b | 2a−b | b |

Every row satisfies both additive equations and has the desired y-valuations. If all four magnitudes equal M, take (a,2a,3a,−a); this also handles M=0. For each coordinate solve

\[
 Z_X^2-y_X Z_X-1=0.
\]

If v(y_X)=−m<0, the two roots have valuations −m and m: their product is −1, and their sum has negative valuation. Choose either root to obtain the requested sign of w_X. If v(y_X)≥0, both roots are units, because their sum is integral and their product is a unit. The four independent choices give a solution with valuation vector w. This proves sufficiency. ∎

The proposition concerns the full ideal, not only the initial forms of two chosen generators: a constructed solution cannot be excluded by any polynomial consequence of F and G. It settles the proposed valuation-support experiment without a large Gröbner fan calculation. Finite tropical bases provide the general framework for this distinction ([Bogart et al., Computing Tropical Varieties](https://arxiv.org/abs/math/0507563)); this particular proof is direct.

**Implication for the program.** Stop seeking further sign or magnitude exclusions from valuation support over an algebraically closed field alone. This result does not supply the Gaussian rational points, conjugation compatibility, common prime support, or square roots required by an integer magic square. Those are the next sources of information. It also does not classify scheme multiplicities of all initial ideals.

## 3. CP.2: the five leading-residue roles

Let p be a split prime in a nonzero column. Put M=max |e_X| and k=2(a−M). Divide the center and every entry by the square p^k. The resulting entries are still integer squares; the center is divisible by p^(2M), hence is zero modulo p. Every offset at the column maximum is a nonzero square modulo p, since center plus that offset is one of the nine entries. Nonmaximal offsets vanish modulo p.

The additive equations give these leading vectors, up to multiplication by a nonzero square:

| Role | (A,B,C,D) modulo p | Necessary square condition |
|---|---|---|
| A deficient | (0,1,1,−1) | always possible for p=1 mod 4 |
| B deficient | (1,0,1,1) | always possible for p=1 mod 4 |
| C deficient | (1,−1,0,2) | 2 is a square modulo p |
| D deficient | (1,1,2,0) | 2 is a square modulo p |
| *: four maxima | (1,t,1+t,1−t) | t, 1+t, 1−t are nonzero squares |

**Corollary (proved).** A prime assigned a C or D deficit is 1 modulo 8, since p=1 modulo 4 and (2/p)=1. The four-maximum condition can be tested exactly at a supplied p; for example p=5,13,17 admit no such leading vector, while p=29 does (t=5).

These are necessary residue conditions, not uniform exclusions of the variable-prime classes in the inventory. They are not claims about full p-adic lifting. The square conditions use the original entries, so they restore information deliberately absent from CP.1.

## 4. CP.3: exact Gaussian unit congruences, with a modulus from the gap

Fix a column j and write \(\pi=\pi_j\), \(b_X=\epsilon_Xe_{X,j}\). The unit

\[
 h_X=\pi^{-2b_X}Z_X
     =\bar\pi^{-2b_X}\prod_{k\ne j}\rho_k^{2\epsilon_Xe_{X,k}}
\]

is a square in the local field at pi. For a maximal label, define

\[
 q_X=-\operatorname{sgn}(b_X)h_X^{-\operatorname{sgn}(b_X)}.
\]

This is a signed monomial in the unit frames, with no discarded constant. The identity

\[
 \pi^{2M}s(Z_X)=q_X+O(\pi^{4M})
\]

holds in the local ring. Here O means membership in the indicated ideal, not an analytic estimate. If E is deficient and g=M−|e_E|>0, then \(\pi^{2M}s(Z_E)\) belongs to \((\pi^{2g})\); when e_E=0 its valuation may be higher, which causes no problem.

**Proposition (proved by substitution).** Every original solution satisfies the following congruences modulo \(\pi^{2g}\):

| Deficit | Unit congruences |
|---|---|
| A | q_C=q_B, q_D=−q_B |
| B | q_C=q_A, q_D=q_A |
| C | q_B=−q_A, q_D=2q_A |
| D | q_B=q_A, q_C=2q_A |

For four maxima, the original two equations hold on the q_X modulo \(\pi^{4M}\). To prove the table, multiply F and G by pi^(2M), substitute the displayed identity, and eliminate the deficient coordinate. All resulting errors lie in the stated ideal. The constant 2 remains a unit and must be retained. ∎

This is a concrete interface to a global descent: after clearing denominators that are units at pi, each row gives divisibility of an explicit Gaussian binomial by pi^(2g). Its nonvanishing and denominator sizes can in fact be settled directly, as follows.

## 5. CP.4: nonzero binomials and the first height bound

For two maximal labels X,Y at column j, write \(\sigma_X=\operatorname{sgn}(e_{X,j})\). The common factor \(\bar\pi_j^{2M}\) in q_X and q_Y cancels. A row of the preceding table becomes

\[
 W=\prod_{k\ne j}\rho_k^{2d_k}\equiv\lambda\pmod{\pi_j^{2g}},
 \quad d_k=\sigma_Y e_{Y,k}-\sigma_X e_{X,k},
 \quad \lambda\in\{1,-1,2,-2\},
\]

where the precise sign of lambda includes the original offset signs. The implementation retains it.

**Proposition (proved).** If the four labels are distinct modulo global sign, W−lambda is nonzero for every such binomial. Moreover every solution satisfies

\[
 p_j^g\ \le\ (1+|\lambda|)\prod_{k\ne j}p_k^{|d_k|}. \tag{H}
\]

**Proof.** If |lambda|=2, equality W=lambda is impossible because |W|=1 in the complex embedding. If lambda=±1, Gaussian-prime factorization forces every d_k=0. The labels then agree after orienting their j-th coordinates positively, including that coordinate since both are maximal. This contradicts their distinctness modulo sign.

Write W=A/B in Gaussian integers by moving the negative exponents into B. Neither A nor B is divisible by pi_j, and

\[
 |A|=|B|=\prod_{k\ne j}p_k^{|d_k|}.
\]

The nonzero Gaussian integer A−lambda B is divisible by pi_j^(2g), so its absolute value is at least p_j^g. The triangle inequality bounds it above by (1+|lambda|)|B|, proving (H). ∎

This closes the zero-binomial branch for the three-maximum roles. Exact **trinomial** relations in four-maximum columns remain a separate problem.

**First experiment (exact finite result).** Apply all inequalities (H) to every open record. With H_j=log p_j, search for a positive integer vector x satisfying

\[
 g x_j\le\sum_{k\ne j}|d_k|x_k
\]

for every recorded binomial. Such an x is a certificate that H=T x satisfies all the upper inequalities for arbitrarily large T, since their constant terms are positive. The generated inventory records one for **every one of the 5,232 open classes**:

| Positive direction x | Open classes |
|---|---:|
| (1,1,1) | 4,672 |
| (1,1,2) | 448 |
| (1,2,1) | 56 |
| (1,2,2) | 56 |

Thus these necessary norm inequalities, taken together, give no height cap on any open record. This conclusion is about a relaxation in real log-primes. It does not construct primes, meet the unit congruences, or solve the magic-square equations. Sixteen records have four maxima in every column and contribute no binomial inequalities; their witnesses are vacuous for this test.

**What this teaches us.** Repeating the same norm bounds cannot establish descent. The next argument must retain extra information: compatibility of the binomial residues, cancellation in their arguments, common factors between different binomials, the four-maximal trinomial equations, or a geometric/global invariant. This is a reason to sharpen the target and keep independent attacks active.

## 6. The ambitious question, now made precise

**Open target CD.** Use the coupled unit congruences for every prime of a primitive configuration to prove an actual reduction of the configuration, an effective height bound, or an unavoidable exact monomial relation inconsistent with distinct primes and nondegeneracy.

The desired mechanism must work with arbitrary prime support and exponents. A directed cycle of inequalities is useful only after its constants and denominators are controlled and its total gain is proved positive. No such theorem is established here.

The next experiments are independent enough to pursue in different orders:

1. **Smallest coupled unit systems.** Start with `***` and `*CD` representatives in both inventories. Their binomials and individual norm bounds are now recorded. Investigate gcds and compatibility between different binomials, or the omitted trinomial equations, to recover information lost in CP.4. Deliver either a proved strict inequality on a stated infinite subfamily, or an explicit reason the stronger proposed height cannot decrease.
2. **Exact-relation branch.** The three-maximum zero binomials are impossible by CP.4. Classify the four-maximal trinomial relations and their proper subsums, using distinct Gaussian-prime factorization where it applies. The classes with no deficits are essential controls.
3. **Lift-preserving arithmetic.** Compare identical cancellation roles with different quotient/tower behavior. A role that does not determine a curve is useful negative information: it identifies the additional squareclass or branch data a uniform theorem needs.
4. **Cross-check with geometry and global obstructions.** Map unit relations to divisors or covers of the magic-square surface. A divisor relation might suggest a height, a Brauer class, or a fibration; each requires its own proof and can become the lead if it explains more than the current descent attempt.

A failed inequality, a counterexample to a proposed family rule, or a proof that two approaches are equivalent is a worthwhile deliverable. The point is to learn which information is fundamental. Preserve local controls and exceptional fibers, and distinguish finite experiments from universal statements.

## 7. Reproduction and proof boundary

`compute/cancellation_patterns.py` records all five role templates, exact Laurent additive witnesses, signed exponent ratios, congruence depths, finite-field square controls, exact binomial exponents, and the height-direction experiment. `a3.cancellation_patterns` checks the identities and finite instances independently of the curve engine. `a3.prime_column_engine` verifies that excluded classes bypass curve computation and survivors reach it. `a3.research_inventory` checks completeness, provenance, binomial exponents, every positive height direction, and freshness of the generated inventory.

The proofs above supply the universal claims; the finite checks validate their implementation. No new magic-square nonexistence slice beyond A3.PC is claimed by these computations.
