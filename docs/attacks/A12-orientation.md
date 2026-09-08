# Orientation: what the open classes share

2026-09-07, entry 129 (R.13 path 1). Code `compute/orientation.py`; data `compute/data_orientation.json`; check `a3.orientation`. Sequel to [A11](A11-height-system.md). The magic-square problem remains open; nothing here is a solution, and the one new theorem (T1) is a consequence of A3.HS stated in a form that is uniform in the number of primes.

## 1. Orientations

Fix a class of an all-ones box (every exponent $1$, $N$ split primes). Write $w_X=\varepsilon_Xe_X\in\{-1,0,1\}^N$ for the four signed exponent vectors; the relations depend only on $Z_X=\prod_j\rho_j^{2w_{X,j}}$, and the class is the $4\times N$ matrix $W$ up to column permutations, column sign flips, the global sign and the $A\leftrightarrow B$ swap (this is the column canonical form of entry 128).

Arithmetically, $w_{X,j}=0$ means $p_j^2$ divides the offset $d_X$; $w_{X,j}=\pm1$ records which of $\pi_j,\bar\pi_j$ the offset's Gaussian factor carries — its **orientation** at $p_j$. For two offsets both prime to $p_j^2$, the product $w_{X,j}w_{Y,j}$ is their *relative* orientation at $p_j$, invariant under every symmetry of the class. Say the pair **flips** between $p_j$ and $p_k$ if the relative orientations differ.

## 2. The height system is a statement about flips (Theorem A3.OR)

For a class of an all-ones box the rows of the height system (A11, version 3) are exactly the following, with $t\in\{2,3\}$ the 2-adic factor of (B1), $K\le4$, and $\lambda$ as in A11:

- **Binomial** at column $j$ for two labels $X,Y$ nonzero at $j$ (the column has a deficit elsewhere): the exponent of $p_k$ on the right is $2$ if the pair flips between $j$ and $k$, $1$ if exactly one of $X,Y$ vanishes at $k$, $0$ if they agree or both vanish. For $|\lambda|=1$:
$$2^t\,p_j^2\ \le\ \prod_{k:\ \text{flip}}p_k^2\ \prod_{k:\ \text{one zero}}p_k .$$
- **Trinomial** at column $j$ for three labels of a circuit, all nonzero at $j$: $p_k$ goes to the *left* (exponent $2$) if the three keep their mutual orientations at $k$ with none vanishing, to the right (exponent $2$) if two of them flip relative to each other at $k$, and drops out otherwise:
$$p_j^2\prod_{k:\ \text{agree}}p_k^2\ \le\ K\prod_{k:\ \text{flip}}p_k^2 .$$

*Proof.* With $s_X=\operatorname{sgn}e_{X,j}$ the A11 quantity $f_{X,k}=-s_Xe_{X,k}$ equals $-w_{X,j}w_{X,k}$, so $d_k=f_{Y,k}-f_{X,k}=w_{X,j}(w_{X,k}-w_{X,j}w_{Y,j}w_{Y,k})$ has $|d_k|\in\{0,1,2\}$ as stated, and for a triple $2\min(f_{\max,k},-f_{\min,k})$ is $-2$ when the three $f$'s coincide and are nonzero, $+2$ when both signs occur, $0$ otherwise. $\square$  The prediction was checked against the height system's own rows on every lemma survivor of the three boxes ($750+7{,}087+44{,}882$ classes): identical coefficients and $|\lambda|$ in every row.

## 3. Theorem T1: three never-disagreeing offsets

**Theorem.** *If three labels forming a circuit ($\{A,B,C\}$, $\{A,B,D\}$, $\{A,C,D\}$ or $\{B,C,D\}$) are all nonzero at some column $j$, and at no other column do two of them flip relative to each other, the class is impossible for every choice of primes.*

*Proof.* The trinomial row at $j$ has no term on the right: $p_j^2\prod_{\text{agree}}p_k^2\le K\le4$, while $p_j\ge5$. $\square$

For general exponent shapes the same argument works with the signs of the $f$'s in place of orientations (a flip at $k$ = both signs among $f_{X,k},f_{Y,k},f_{Z,k}$), since $p_j^{2M}\ge25>K$.

**Corollary.** *If no pair of labels flips at all, the class is impossible.* (At any column three labels are nonzero by the prime-column lemma; they form a circuit with no flip column.)

**Coverage.** T1 explains $212$ of the $576$ local kills at three frames ($37\%$), $1{,}340$ of $3{,}935$ at four ($34\%$), $5{,}022$ of $15{,}972$ at five ($31\%$), and $1{,}000$ of the $3{,}304$ height-system kills of the $(2,1,1)$ campaign; it fires on none of the $174+3{,}152+28{,}910$ open all-ones classes nor on any of the $1{,}388+2{,}206$ open classes of the $(2,1,1)$ and $(3,1,1)$ campaigns. The remaining kills are cycles of two or more rows across columns, and about a ninth of all kills need the constants ($2^t$, $K$) rather than the exponents.

## 4. What the open classes share

Contrapositively, every open class satisfies:

1. **Every circuit flips relative to every prime.** For each $j$ and each three labels nonzero at $j$, some other prime sees two of them in opposite relative orientation (T1).
2. **Every pair of labels flips somewhere,** except that a pair may fail to flip if it is compensated by one-zero columns; classes in which every pair flips are open $99\%$ of the time ($4/4$, $404/415$, $6{,}598/6{,}656$), the exceptions dying through the constants.
3. **A feasible prime hierarchy.** The flip pattern admits a consistent size ordering of the primes. About a third of the open classes ($56/174$, $1{,}137/3{,}152$, $9{,}799/28{,}910$) allow all primes to be comparable; the rest force a spread: at five frames $2{,}499$ open classes force one prime to be at least $125$ times another, and some force ratios above $10^9$ (`data_orientation.json` records the forced minimal ratio $\max_jp_j/\min_jp_j$ of every open class).

Nothing else is visible at first order: the height system depends on the class only through the flip pattern and the zero pattern, and for an open class those admit a feasible hierarchy by definition. So **the open classes are the orientation-generic ones** — the four offsets' orientations at the center's primes are mixed enough that every size inequality can be satisfied — and the residual local information is exactly the *values* of the congruences (which primes' frames the flipped products must be divisible by), which is prime-specific and does not scale uniformly.

## 5. Consequences for the plan

- Path 1 is answered in the form the data allows: the uniform structure of the survivors is orientation genericity plus a feasible hierarchy, and T1 is the sharpest single-row uniform exclusion; further uniform exclusions of the same kind are cycle conditions, i.e. the LP itself.
- The decay of the kill rate with $\omega$ (entry 128) is explained: each extra prime adds a column at which a pair may flip, so flips become generic.
- A proof cannot come from orientations and sizes alone. The levers left are global: the class curves for fixed shapes (path 2), the exact congruences as a rigidity (the pair search), and a descent in the number of primes (path 3) — for which the hierarchical classes are the natural first targets, since they force a huge prime that the others must generate through the divisibilities.
