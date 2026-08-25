# 00 — Problem statement, notation, symmetries

## Definitions

**Definition 0.1 (magic square).** A *3×3 magic square* over a commutative
ring $R$ is a matrix

$$M = \begin{pmatrix} a_1 & a_2 & a_3 \\ a_4 & a_5 & a_6 \\ a_7 & a_8 & a_9 \end{pmatrix},\qquad a_i \in R,$$

whose **eight lines** — three rows, three columns, two main diagonals — have
equal sums. The common value $S$ is the *magic sum*. (We always require all
eight lines; a square magic only in rows and columns is called *semi-magic*
and is explicitly labeled as such when it appears.)

**Definition 0.2 (magic square of squares, MSS).** A 3×3 magic square over
$\mathbb{Z}$ is a *magic square of squares* if its nine entries are perfect
squares. It is **admissible** if the nine entries are moreover *pairwise
distinct*. Throughout, "MSS3" means an admissible 3×3 magic square of squares
over $\mathbb{Z}$.

Distinctness is essential: without it, trivial examples exist (e.g. all nine
entries equal to the same square; or the classical construction from any
three-term AP placed suitably). The open problem is about admissible squares.

**Convention.** Entries are written $a_i = x_i^2$ with $x_i \ge 0$, and we
freely pass between "the entry" $x_i^2$ and "the root" $x_i$.

## The open problem

> **Problem (LaBar 1984).** Does an admissible 3×3 magic square of squares
> exist?

> **Conjecture 0.3 (No-MSS3 — the conjecture this repository attacks).**
> No admissible 3×3 magic square of squares exists over $\mathbb{Z}$
> (equivalently, by clearing denominators, over $\mathbb{Q}$).

Status: **open in both directions** as of 2026. See
[references.md](references.md) for the literature and
[foundations/F6-known-squares.md](foundations/F6-known-squares.md) for the
closest known near-misses (seven of nine entries square is achievable — one
essentially unique example is known; eight is open; nine is the problem).

## Symmetries and normalizations

**Proposition 0.4 (symmetry group).** The dihedral group $D_4$ of order 8
(rotations and reflections of the grid) acts on the set of 3×3 magic squares,
preserving the magic sum, admissibility, and squareness of entries.
*Proof.* Rotations and reflections of the grid permute the eight lines among
themselves (rows ↔ columns under transpose-like reflections; the two
diagonals are preserved or swapped), so equal line sums are preserved; the
multiset of entries is unchanged. $\blacksquare$ **[PROVEN]**

**Proposition 0.5 (scaling).** If $(x_i^2)$ is an MSS3 with magic sum $S$ and
$k \in \mathbb{Z}_{>0}$, then $(k^2 x_i^2)$ is an MSS3 with magic sum $k^2 S$.
Conversely, dividing by the gcd: if $g = \gcd(x_1,\dots,x_9)$ then
$((x_i/g)^2)$ is an MSS3. *Proof.* Linearity of line sums; distinctness is
preserved under multiplication/division by $k^2 \ne 0$. For the converse,
$\gcd(x_1^2,\dots,x_9^2) = g^2$ because $\gcd$ of squares is the square of
the $\gcd$ (immediate from unique factorization, prime by prime:
$\min_i(2v_p(x_i)) = 2\min_i v_p(x_i)$). $\blacksquare$ **[PROVEN]**

**Definition 0.6 (primitive, essentially different).** An MSS3 is *primitive*
if $\gcd(x_1,\dots,x_9)=1$. Two squares are *essentially the same* if one is
obtained from the other by a $D_4$ symmetry followed by a scaling. By 0.4/0.5
it suffices to attack the conjecture for primitive squares, up to $D_4$.

## What "attacking impossibility" means here

By [F5](foundations/F5-local-solubility.md), the system defining MSS3 has
solutions modulo every prime power tested and over every completion of
$\mathbb{Q}$ where this has been examined — **there is no local obstruction**,
so no argument that only uses congruences can prove Conjecture 0.3. Any
successful impossibility proof must exploit *global* arithmetic (descent,
elliptic curves, geometry of the parametrizing surface). Every candidate
argument developed in `docs/attacks/` must pass the falsification gauntlet in
[protocol/sanity-checks.md](protocol/sanity-checks.md).

**Verification:** `python3 -m verify --only f1` exercises the parametrization
identities underlying 0.4/0.5 (they are special cases of the F1 linear
structure); the propositions above are otherwise elementary enough to check
by eye.
