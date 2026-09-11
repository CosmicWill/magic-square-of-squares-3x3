# Universal root-sum twist reduction

2026-09-10. Independent branch `research/proof-alternatives`, following
the owner's instruction to prioritize a universal route to impossibility.
Base mathematical context is still main a719b635 (entry 140).

The result here is a **necessary reduction for every hypothetical MSS3**,
not an exclusion. It also rejects a proposed local/algebraic shortcut to
the previously selected twist family. No finite list of numerical twists
has been shown sufficient, and no new MSS3 class is declared impossible.

The computational checks are `python -m verify --only ut.`. They include
known rational degenerate grids as positive controls; those are not
admissible solutions. The proofs below state which parts are universal
and which calculations are bounded evidence.

## Notation and exact scope

Use primitive integer roots, center m>0, and integer offsets U,V:

\[
 \begin{pmatrix}
 m^2+U&m^2-U-V&m^2+V\\
 m^2-U+V&m^2&m^2+U-V\\
 m^2-V&m^2+U+V&m^2-U
 \end{pmatrix}.
\]

Every displayed entry is a root squared. F4's elementary mod-4 and
mod-3 arguments imply that all primitive roots are odd and coprime to
3, and 24 divides U and V. Those arguments do not require distinctness.
For an admissible grid, G=gcd(U,V)>0 and all eight distinctness factors
in GB.7 are nonzero. Set k=U/G and l=V/G.

Choose one noncentral row or column, with integer roots (a,b,c) in order,
so a^2+b^2+c^2=3m^2. Write (A,B,C)=(a,b,c)/m. This note uses cyclic
edge order (A,B),(B,C),(C,A). Permuting the row permutes the three twist
labels; GB.7 uses a different ordering of the same top row.

Put

\[
 s_1=(A+B)/2,\quad s_2=(B+C)/2,\quad s_3=(C+A)/2,\qquad
 s_i=q_i z_i^2.
\]

Here q_i is the signed squarefree integer representing the nonzero
rational square class of s_i. Thus d_i=2q_i in GB.7's cover convention.
The admissible domain makes all pair sums and pair differences nonzero.
The full cover includes the other five entry-root equations, not just
the equation for the three roots in the selected row.

## UT.1. The exact sign orbit

**PROVEN.** Define

\[
 L_1=A^2-B^2,\quad L_2=B^2-C^2,\quad L_3=C^2-A^2,\quad T=s_1s_2s_3.
\]

For signs epsilon_i in {+1,-1}, the changed slot on edge (i,j) has class

\[
 [s'_{ij}]=[\epsilon_i s_{ij} L_{ij}^{\delta_{ij}}],\qquad
 \delta_{ij}=\begin{cases}0&\epsilon_i=\epsilon_j,\\1&\epsilon_i\ne\epsilon_j.\end{cases}
\]

Indeed, when the signs differ,
(A-B)/2=L_1/(4s_1). The ratio to s_1 L_1 is the square 1/(4s_1^2).
When signs agree the only change is their common sign. The same identity
applies on every edge.

Consequently the complete set of product square classes is

\[
              [\,\pm T\,],\quad[\,\pm T L_1L_2\,],\quad
              [\,\pm T L_2L_3\,],\quad[\,\pm T L_3L_1\,].
\]

A triangle cut has either zero or two edges; global sign reversal
changes the sign of the product. This accounts for all eight root-sign
choices. The four noncentral rows/columns account for the entire D4
orbit of the selected row, and reordering a row does not change T.

This is an exact test for whether signs and grid symmetries can achieve
[q_1 q_2 q_3]=1. It does not assert that the test always succeeds.

## UT.2. An explicit family covering every hypothetical solution

**PROVEN.** Every hypothetical MSS3 has a signed-root lift to a cover with

\[
 q_i\text{ signed, odd and squarefree},\qquad
 q_1+q_2+q_3\equiv3\pmod8,\qquad z_i\in\mathbb Z_2^\times.
\]

The same choice of all nine root signs works for all four noncentral
rows/columns. There are 16 possible ordered residue triples modulo 8.
The sizes, signs and odd prime factors of q_i are not bounded here.

*Proof.* Independently choose each integer root r so r=m mod 4. Then
each normalized root r/m is 1 mod 4 in Z_2. In any selected row,
s_i=(a+b)/(2m) is a 2-adic unit. Its class is represented by the odd
integer m(a+b)/2, since multiplying s_i by m^2 does not change its
square class. Removing its square factors gives odd q_i and a rational
unit z_i.

Write A=1+4x, B=1+4y, C=1+4z in Z_2. From A^2+B^2+C^2=3 we get
x+y+z+2(x^2+y^2+z^2)=0, hence x+y+z is even. Thus
s_1+s_2+s_3=A+B+C=3 mod 8. Since z_i is an odd 2-adic unit, z_i^2=1
mod 8, so s_i=q_i mod 8. This proves the asserted congruence. For any
two odd residue classes, exactly one of the four odd residues can be
the third; there are therefore 16 possibilities.

The unit restriction on z_i is part of the normalization. An arbitrary
point on a cover with odd q_i can have even z_i; its coefficients need
not obey this particular residue condition. Positive real q_i are also
not justified by the sign normalization, so signed coefficients are kept.

### This family has no further obstruction at 2

**PROVEN.** Every triple of odd integers q_i whose sum is 3 mod 8 has a
full 2-adic square-grid lift with z_i units and normalized row roots 1
mod 4. Admissible local lifts exist as well. Squarefreeness is unnecessary
for this local assertion.

Let s_i=q_i z_i^2 and use the row quartic from GB.8:

\[
 F=3(s_1^2+s_2^2+s_3^2)-2(s_1s_2+s_2s_3+s_3s_1)-3=0.
\]

For odd z_i, F=9-(q_1+q_2+q_3)^2 mod 16. In particular F=0 mod 16
at the seed (z_1,z_2,z_3)=(1,5,9). Its derivative in z_1 is

\[
 4q_1z_1(3q_1z_1^2-q_2z_2^2-q_3z_3^2),
\]

which is 4 times an odd unit. For n>=4, changing z_1 by 2^(n-2)
changes F by 2^n modulo 2^(n+1); the quadratic and higher Taylor terms
are divisible by 2^(n+1). This gives a compatible lift to every precision
and therefore a 2-adic solution. The same construction works while the
two other odd coordinates vary sufficiently close to their seeds.

The recovered row roots are s_1-s_2+s_3, s_1+s_2-s_3, -s_1+s_2+s_3.
Because sum(q_i)=3 mod 8 they are all 1 mod 4. Every other required
entry radicand has the form 2-R^2 or 1+R^2-S^2 for odd row roots,
and is therefore 1 mod 8. It has a square root in Q_2: starting from
the root 1 mod 4, changing a root by 2^(n-1) toggles the n-th bit of
its square for n>=3. This restores all five missing square conditions.

All roots and all z_i are nonzero, so this is a smooth point of the
finite cover. The two free local parameters can avoid the finitely many
distinctness divisors: the geometrically integral cover dominates the
original surface (GB.7), so none of those divisors contains a local open
neighborhood. The printed finite controls check lifts on the full square
surface; the generic perturbation argument supplies admissibility.

For comparison, without selecting the row signs, a unit-z lift requires
sum(q_i)=3 or 5 mod 8 by the same mod-16 calculation. Sum 5 corresponds
to row roots -1 mod 4. No congruence conclusion here is an obstruction
to the universal family just constructed.

## UT.3. Prime factors of the universal twist labels

**PROVEN.** Let m,U,V,G come from a hypothetical primitive MSS3. For any
of its canonically signed noncentral frames:

1. gcd(m,G)=1, all prime divisors of m are 1 mod 4, and gcd(a,b,c)=1.
2. gcd(|q_1|,|q_2|,|q_3|) divides the squarefree part of m.
3. Any prime common to two q_i divides mG. Thus the labels are pairwise
   coprime away from the center and the common offset factor.
4. If p=5 mod 8 divides m, then p occurs in all three squarefree labels
   exactly when v_p(m) is odd, and occurs in none when it is even.
5. Set ell_i=(r_i^2-r_j^2)/G for the three cyclic edges of the integer
   row. There is a signed odd squarefree H supported only on
   ell_1 ell_2 ell_3 such that

   \[
                       q_1q_2q_3=mH w^2,\qquad w\in\mathbb Q^*.
   \]

   These ell_i are nonzero primitive-direction expressions. In top-row
   order they are 2k+l, -k-2l, l-k. Thus, for any fixed primitive
   direction, H has finitely many possibilities independently of m and G.
   The primitive direction itself is not bounded.

*Proof of 1.* A prime dividing m and G makes every entry divisible by p,
hence every root divisible by p, contrary to primitivity. If p=3 mod 4
divides m, each opposite-root equation x^2+y^2=2m^2 forces p to divide
both roots, with the same contradiction. The elementary nonsquareness of
-1 at such primes is also used and proved in F4's quadratic-residue core.
Finally if p divides a,b,c, their row sum forces p|m unless p=3. For
p!=3 the row equations then force U=V=0 mod p in the corresponding
frame, and all nine roots are divisible by p. The case p=3 was already
excluded by the primitive mod-3 argument.

For the remaining claims use the exact parity identity at odd p:

\[
 v_p(q_{ij})\equiv v_p(m)+v_p(a_i+a_j)\pmod2.
\]

If p|m, two vanishing pair sums would give a=c=-b modulo p and
3b^2=0. Since p!=3 and the row is primitive modulo p, this is impossible.
Thus at most one pair sum is divisible by a center prime. At least two
labels have parity v_p(m). A prime in all three labels must consequently
occur oddly in m. A noncenter prime in all three labels would divide all
three pair sums, and therefore all three row roots. This proves 2.

If p does not divide m and occurs in two labels, the corresponding two
pair sums vanish modulo p. The row relation gives a^2=b^2=c^2=m^2
modulo p when p!=3, so p divides both offsets and hence G. The prime 3
already divides G, since 24 divides the offsets. This proves 3.

For p=5 mod 8 dividing m, a vanishing pair sum a+b would imply
c^2=-2a^2 mod p. Here -2 is nonsquare, so a=b=c=0 mod p, impossible.
Thus no pair sum vanishes and all three parities equal v_p(m), proving 4.
The distinction p=1 mod 8 is essential: modulo 17 the row (1,-1,7)
has squared sum zero and one vanishing pair sum.

For 5, write b_ij=(a_i+a_j)/2, an odd integer. By the definition of the
labels, [q_1q_2q_3]=[m^3 b_12 b_23 b_31]=[m b_12 b_23 b_31]. Set
H=sqclass(b_12 b_23 b_31); this gives the displayed rational square w^2.
The prime 2 cannot divide H. Consider an odd prime p not dividing
ell_1 ell_2 ell_3. If p does not divide G either, none of the entry
differences is zero modulo p, so no pair sum is divisible by p, whether
or not p divides m. If p|G, coprimality gives p not dividing m and
every row root is congruent to +m or -m modulo p. There are either zero
or two edges with opposite signs. On each such edge the complementary
root difference is a unit, so

\[
 v_p(a_i+a_j)=v_p(a_i^2-a_j^2)=v_p(G),
\]

because p does not divide ell_i. The sum of the three valuations is
therefore zero or 2v_p(G), always even. Hence p cannot divide H.

This last cancellation is the useful coupling: arbitrary new primes in
G do not independently enter the product twist. After factoring out the
center class, only primitive-direction primes remain. The center and
primitive direction remain unbounded; this is not finite numerical twist
control for the whole problem.

## UT.4. A shortcut to the old family fails locally

**PROVEN.** There is a point of the admissible full square surface over
Q_401 for which no root-sign choice and no D4 symmetry makes the three
root-sum twist labels have square product.

Take center 1 and offsets u=79, v=82. Modulo 401 the entry and root grids
are respectively

\[
 \begin{pmatrix}80&241&83\\4&1&399\\320&162&323\end{pmatrix},\qquad
 \begin{pmatrix}90&38&22\\2&1&143\\180&76&137\end{pmatrix}.
\]

All nine entries are distinct nonzero squares modulo this prime.
The displayed roots lift uniquely from these residues to square roots
of the exact integer entries over Q_401. At each step the derivative
2r is a unit, giving the explicit correction in the source code. Since
the entries are already distinct and nonzero modulo 401, the lift is
admissible. It is a local point, not a rational magic square: some of the
exact integer entries are negative.

For each noncentral row/column, all three entry differences are
nonsquares modulo 401, while -1 is a square. UT.1 therefore says that
every sign change preserves the quadratic character of T. The four
products T at the displayed root signs are 52,84,101,336, respectively;
all are nonsquares modulo 401. Equivalently, direct enumeration gives:

| Frame | Products for all eight root-sign choices, modulo 401 |
|---|---|
| Top row | 349,236,19,54,347,382,165,52 |
| Bottom row | 317,127,46,371,30,355,274,84 |
| Left column | 300,230,259,270,131,142,171,101 |
| Right column | 65,96,107,211,190,294,305,336 |

Every entry in this table has 200th power -1 modulo 401. These remain
nonsquare units in Q_401 and throughout a local neighborhood. The four
frames, all sign choices, and root permutations exhaust the choices
relevant to the original three-sum construction.

**FAILED-ATTEMPT (local/algebraic forcing of product-one twists).** One
cannot deduce q_1q_2q_3 square from the full square equations plus root
signs and grid symmetry in every completion, or by an algebraic identity
valid in characteristic zero. In particular, the restriction q_3=q_1q_2
used to choose (17,89,1513) is not justified by those mechanisms.

This is deliberately narrower than a refutation of a theorem about
rational admissible points. A genuinely global argument might still
force rational points into a smaller family despite the local example.
The example establishes that such an argument would be additional work,
not an automatic consequence of choosing signs or changing frames.

## What is now required for an impossibility proof

Every hypothetical solution reaches the explicit UT.2 family, and UT.3
couples its labels to the same center and primitive direction. A global
exclusion must handle this infinite family, or prove a further necessary
reduction. Independently ruling out a succession of numerical triples
does not accomplish that.

The next precise questions are:

1. Can the product square class [q_1q_2q_3]=[mH] from UT.3
   be related to a norm or reciprocity obstruction that survives all five
   additional square roots? Keep m and (k,l) as parameters.
2. Can the four frames' restrictions be combined, using the common m,G
   and the UT.1 sign orbit, to force a contradiction or a decrease in a
   positive integer invariant? A proposed decrease must preserve all nine
   square equations and distinctness.
3. If a Brauer calculation is attempted on the row quartic, derive its
   dependence on general signed q_i. The fixed triple (17,89,1513) remains
   a method test, not the universal target.

The existing GB.3 limitation still applies to any twist with a suitable
smooth rational boundary point. The universal family includes such twists;
UT.2 does not eliminate that difficulty.

## Reproduction and provenance

```text
python -m compute.universal_twist_probe --precision 8
python -m verify --only ut.
python -m verify --only gb.
python -m verify --only gauntlet
```

UT.1--UT.4 are proved here from the explicit equations and the elementary
primitive congruences in [F4](../foundations/F4-congruences-mod-72.md).
The quartic, geometric integrality and original cover are those of
[GB.7--GB.8](global-obstructions.md). No novelty claim relative to the
literature is made. No new external arithmetic theorem is needed for the
results in this note.

The searches through rational AP controls are bounded regression checks,
not evidence for the universal assertions beyond their stated bounds.
The 401 residue certificate is complete for that one local configuration;
its lift to all precisions follows from the written unit-derivative
argument. No campaign ledger or headline impossibility predicate changes.
