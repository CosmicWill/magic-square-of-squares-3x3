# The height system: unit congruences turned into prime inequalities

2026-09-07, entry 123. Sequel to [A10](A10-cancellation-descent.md) (CP.3, CP.4) and to the prime-column lemma [A3.PC](A3-simultaneous-congrua.md#249-the-prime-column-lemma-theorem-a3pc-a-uniform-exclusion-from-the-valuations-alone-entry-120). Code: `compute/height_system.py` (the system and its linear programme with exact certificates), `compute/height_search.py` (the finite search behind a cap), `compute/height_identities.py` (numeric verification of the algebra with genuine Gaussian primes); data `compute/data_height_system.json.gz`; check `a3.height_system`. The magic-square problem remains open; every kill below is a kill of a class of labels and signs for all choices of split primes.

## 1. Setting

Labels $A,B,C,D$ with entries $e_{X,j}$, signs $\varepsilon_X$, split primes $p_j=\pi_j\bar\pi_j$, $\rho_j=\pi_j/\bar\pi_j$, $Z_X=\prod_j\rho_j^{2\varepsilon_Xe_{X,j}}$, $s(Z)=Z-Z^{-1}$. The two additive relations are $F=s(Z_A)+s(Z_B)-s(Z_C)=0$ and $G=s(Z_A)-s(Z_B)-s(Z_D)=0$; with $m_s^2=\prod p_j^{2a_j}$ one has $m_s^2\,s(Z_X)/2i=\varepsilon_X\,e(X)$ exactly, $e(X)$ the ledger's `elem_box`, so $F$ and $G$ are the relations $R_1,R_2$ of the class (verified on genuine frames by `identity_tests`).

Fix a column $j$, write $\pi=\pi_j$, $M=\max_X|e_{X,j}|$. A deficient label $E$ has $|e_{E,j}|=M-g$ with $g\ge1$; by A3.PC there is at most one. For a maximal label put $s_X=\operatorname{sgn}e_{X,j}$, $\sigma_X=\varepsilon_Xs_X$, and
$$U_X=\prod_{k\ne j}\rho_k^{2f_{X,k}},\qquad f_{X,k}=-s_Xe_{X,k}.$$
CP.3 gives, for both signs of $\varepsilon_Xe_{X,j}$,
$$\pi^{2M}s(Z_X)=-\sigma_X\bar\pi^{2M}U_X+O(\pi^{4M})\ (X\text{ maximal}),\qquad \pi^{2M}s(Z_E)\in(\pi^{2g})\ (E\text{ deficient}).$$
Hence each of the four circuits $F$, $G$, $F+G$, $F-G$ (coefficient vectors $(1,1,-1,0)$, $(1,-1,0,-1)$, $(2,0,-1,-1)$, $(0,2,-1,1)$) yields, after division by $-\bar\pi^{2M}$,
$$\sum_X c_X\sigma_XU_X\equiv0\quad\text{mod }\pi^{4M}\ \text{(three maximal labels: a trinomial)}\ \text{ or mod }\pi^{2g}\ \text{(the deficient label dropped: a binomial)}.$$
In a deficient column three circuits are binomials and one (the circuit avoiding $E$) is a trinomial; in a four-maxima column all four are trinomials. This is where A10 stopped: it used only the binomials, with the modulus-$|A|$ bound.

## 2. The sharpening

**Binomials.** For the pair $(X,Y)$ with coefficients $a_X,a_Y\in\{\pm1,\pm2\}$, $|a_X|\ge|a_Y|$, the congruence reads $U_Y/U_X\equiv\lambda:=-a_X/a_Y$ mod $\pi^{2g}$. With $d=f_Y-f_X$,
$$U_Y/U_X=A/\bar A,\qquad A=\prod_{d_k>0}\pi_k^{2d_k}\prod_{d_k<0}\bar\pi_k^{2|d_k|}\in\mathbb Z[i],\qquad |A|=P:=\prod_{k\ne j}p_k^{|d_k|},$$
and $A$ is neither real nor imaginary: otherwise $U_Y=\pm U_X$, every $d_k=0$ by unique factorisation in $\mathbb Z[i]$, and $X=\pm Y$ as labels.

- $\lambda=1$: $A-\bar A=2i\operatorname{Im}A\in(\pi^{2g})$ with $\operatorname{Im}A$ a rational integer, so $p^{2g}\mid\operatorname{Im}A$. Every $\pi_k^2$ is $\pm1$ mod $4$, so $A\equiv\pm1$ mod $4$ and $4\mid\operatorname{Im}A$ ($8$ when every $d_k$ is even). Hence $2^tp_j^{2g}\le|\operatorname{Im}A|\le P$, $t\in\{2,3\}$. **(B1)**
- $\lambda=-1$: $A+\bar A=2\operatorname{Re}A$, so $p^{2g}\mid\operatorname{Re}A\ne0$ and $p_j^{2g}\le P$. **(B1′)**
- $\lambda=\pm2$: $p^{2g}\mid N(A-\lambda\bar A)=5P^2-2\lambda\operatorname{Re}(A^2)$, nonzero and $\le9P^2$, so $p_j^g\le3P$. **(B2)**

A10's bound was $p_j^g\le(1+|\lambda|)P$ in every case; (B1) and (B1′) double the exponent, and every deficient column has at least one row with $|\lambda|=1$ (for an A or B deficit all three).

**Trinomials.** For the circuit $(X,Y,Z)$ with coefficients $a$, $K=\sum|a_X|\in\{3,4\}$: multiply by the common denominator and remove the common Gaussian factor,
$$T_X=\prod_{k\ne j}\pi_k^{2(f_{X,k}-\min f)}\bar\pi_k^{2(\max f-f_{X,k})},\qquad |T_X|=Q:=\prod_{k\ne j}p_k^{r_k},\quad r_k=\max_Yf_{Y,k}-\min_Yf_{Y,k},$$
so that $S=\sum a_XT_X\in\mathbb Z[i]$ and $S\equiv0$ mod $\pi^{4M}$. **$S\ne0$:** with coefficients $\pm1,\pm1,\pm1$, a vanishing sum of three numbers of equal modulus is an equilateral triangle, i.e. a ratio $e^{\pm i\pi/3}\notin\mathbb Q(i)$; with $2,\pm1,\pm1$ it forces $|T_Y\pm T_Z|=2Q$, hence $T_Y=\pm T_Z$, hence $f_Y=f_Z$ and $Y=\pm Z$ as labels. Therefore
$$p_j^{2M}\le|S|\le KQ. \textbf{ (T)}$$

**Coupling.** Two binomials from *different* columns $j,j'$ with $|\lambda|=1$, the same kind (Im or Re) and the same $d$ up to global sign constrain the same integer, so $p_j^{2g_j}p_{j'}^{2g_{j'}}$ divides it. **(C)**

**Lower bounds** (CP.2): a split prime is $\ge5$; a C- or D-deficit prime is $1$ mod $8$, hence $\ge17$; a four-maxima prime admits $t$ with $t,1+t,1-t$ nonzero squares, which $5,13,17$ do not and $29$ does, hence $\ge29$.

Every condition is $\prod_jp_j^{a_j}\le K$ with integers $a_j$ and a rational $K$: a linear inequality in $x_j=\log p_j$. The system is invariant under the frame group (the inequalities depend only on $|d|$, $r$, $K$), so the canonical representative decides its whole orbit.

**The reality sharpening (T′), entry 124.**  For a circuit among maximal labels the congruence is the shadow of an exact identity: summing the CP.3 expansions gives $\sum_Xc_X\pi^{2M}s(Z_X)=-\bar\pi^{2M}W+\pi^{4M}\bar\pi^{-2M}\bar W$ with $W=\sum_Xc_X\sigma_XU_X$ (exact, since the error terms are $\sigma_X\pi^{4M}\bar\pi^{-2M}U_X^{-1}$ and $U_X^{-1}=\bar U_X$; `circuit_identity_tests`), so a solution has $\bar\pi^{4M}W=\pi^{4M}\bar W$.  With $S=GW$, $G=\prod_{k\ne j}\pi_k^{-2f_{\min,k}}\bar\pi_k^{2f_{\max,k}}$, and $S=\pi^{4M}S_1$ this says $S_1\bar G=\bar S_1G$: **$S_1\bar G$ is real.**  Writing $G=G_+/G_-$ with integral $G_\pm$, the rational integer $R=S_1\bar G_+G_-$ is divisible by $\bar G_+G_-$ and by its conjugate, hence by $\prod_kp_k^{\max(u_k,v_k)}$ where $u_k,v_k$ are the exponents of $\pi_k,\bar\pi_k$ in $\bar G_+G_-$; as $u_k-v_k=2(f_{\max,k}+f_{\min,k})$,
$$|S_1|\ \ge\ \prod_{k\ne j}p_k^{|f_{\max,k}+f_{\min,k}|},\qquad\text{hence}\qquad p_j^{2M}\le K\prod_{k\ne j}p_k^{\,2\min(f_{\max,k},-f_{\min,k})}. \textbf{ (T′)}$$
The exponent $2\min(f_{\max},-f_{\min})$ is at most the spread $r_k$ of (T), often $0$, and negative when the three exponents share a sign.  In the worked case of §4 the $G$-trinomial of column $2$ improves to $p_2^2\le3p_1^2$.  Re-deciding the $214+1{,}960$ classes left unbounded by (T) with (T′) in place of (T): **$44+572$ more infeasible**, none capped, $170+1{,}388$ unbounded (§4).  The version of the system is recorded with every certificate; the entry-123 certificates remain valid for version 1.

## 3. The decision and its certificates

For each class the linear programme in $x$ is solved (HiGHS through scipy) and every verdict is certified in exact rational arithmetic:

- **infeasible** — Farkas multipliers $y\ge0$ with $\sum_iy_ia_i=0$ and $\prod_iK_i^{Dy_i}<1$ ($D$ the common denominator): no primes at all satisfy the necessary conditions. *The class is impossible.*
- **capped** — for each prime, multipliers with $\sum_iy_ia_i=e_j$: $p_j^D\le\prod K_i^{Dy_i}$ exactly. When all three primes are capped, `height_search` enumerates every split-prime triple inside the caps and tests, in order: every inequality exactly; the residue conditions; every exact divisibility ($p_j^{2g}\mid\operatorname{Im}A$, $\operatorname{Re}A$ or $N(A-\lambda\bar A)$; $\pi_j^{4M}\mid S$) under each of the eight choices of conjugate frames; and finally the relations $R_1=R_2=0$ themselves. No survivor means *the class is impossible*.
- **unbounded** — an exact positive recession direction $x$ with $\sum_ja_{ij}x_j\le0$ for every homogeneous part: these inequalities alone give no cap.

## 4. Results

| Box | Open before | Infeasible | Capped, searched, dead | Unbounded (still open) |
|---|---:|---:|---:|---:|
| (1,1,1) | 488 | 274 | 0 | 214 |
| additional (2,1,1) | 4,744 | 2,732 | 52 | 1,960 |

**Version 2 (entry 124, the reality sharpening):** of the $214+1{,}960$ unbounded classes, $44+572$ become infeasible; open $170$ and $1{,}388$; tallies $(1,1,1)$ dead $2774$ / finite $170$, $(2,1,1)$ dead $77{,}980$ / finite $1{,}388$.

Caps of the 52: all three primes at most $6561$, median $108$; the searches examined at most $887{,}124$ admissible triples per class, at most $1{,}001$ passed the inequalities, none passed the divisibilities. Tallies after the fold: (1,1,1) dead $2730$ / finite $214$; (2,1,1) dead $77{,}408$ / finite $1{,}960$. Every certificate was re-verified exactly from the class alone (`verify_certificate`).

**A worked case** (class $[[0,0,1],[1,-1,-1],[1,-1,1],[1,1,-1]]$, signs $(1,-1,1,-1)$, roles AA$*$). Column $0$ is A-deficient with $g=1$: the $F$-binomial gives $p_0^2\mid\operatorname{Re}(\pi_2^4)$; column $1$ likewise gives $p_1^2\mid\operatorname{Re}(\pi_2^4)$; the coupling (C) gives $p_0^2p_1^2\le|\operatorname{Re}\pi_2^4|\le p_2^2$. Column $2$ has four maxima; its $G$-trinomial gives $p_2^2\le3p_0p_1^2$. Together $p_0\le3$: impossible.

**What is left.** The 214 + 1,960 unbounded classes are the ones whose inequalities admit a positive recession direction — typically classes with a four-maxima column whose trinomial bounds have large spreads $r_k$, or A/B deficits whose $|d_k|=2$. For them the *exact* divisibilities remain, now as congruences between the primes ($p_j^{2g}$ dividing an explicit integer built from the other two), which the search can test to any bound, and the values of the binomials modulo the next power of $\pi$ (the deficient label's leading unit) are not yet used.

**Version 3 (entry 125).**  For a circuit with coefficients $2,\pm1,\pm1$ the Gaussian integer $S\equiv\pm2\pm1\pm1\pmod 4$ is even (every $\pi_k^2\equiv\pm1$ mod $4$), so $S_1$ is even and $K=4$ improves to $2$.  This changes no verdict: unboundedness is a property of the homogeneous rows, and every one of the $170+1{,}388$ open classes stays unbounded.  The local method is exhausted at first order for them: their inequalities admit a positive recession direction whatever the constants, and the binomial rows have no reality sharpening (the exact identity of a binomial circuit involves the deficient term and yields a residue condition only).

## 5. Proof boundary

The kills rest on: A3.PC (2.49); CP.2 and CP.3 of A10 (re-derived in entry 122 and verified exactly on genuine frames by `identity_tests`); the nonvanishing arguments of §2; unique factorisation in $\mathbb Z[i]$; and the exactly verified certificates. Only the *reported* cap values are floating-point evaluations of exact rational expressions; the search used the exact integer caps. Nothing here bounds the number of split primes: the system is per class, and the classes are per exponent shape.

## 6. The pair search (entry 125)

For an open class the divisibilities are congruences between the primes: at a deficient column $j$, $p_j^{2g}\mid I(\pi_k,\pi_l)$ with $I=\operatorname{Im}A$, $\operatorname{Re}A$ or $N(A-\lambda\bar A)$ an explicit integer in the other two frames; at a four-maxima column $\pi_j^{4M}\mid S(\pi_k,\pi_l)$.  So a pair $(p_k,p_l)$ determines finitely many candidates for $p_j$, the prime-power divisors of $I$ or of $N(S)$, whatever the size of $p_j$.  `compute/height_pairs.py` enumerates, for every column $j$, every ordered pair of admissible split primes $\le B$ in the other two columns and both conjugate frames of each, determines the candidates from the column's cheapest relation, and tests every candidate triple against every inequality, every residue condition, every divisibility under all conjugate-frame choices, and finally the relations $R_1=R_2=0$.  A solution of the class whose two smallest primes are $\le B$ is caught by the run in the column of its largest prime.

**Result at $B=500$ over all $170+1{,}388$ open classes:** no candidate passes every divisibility, so none reaches the relations; there is no near miss.  *No open class has a solution whose two smallest primes are at most 500.*  This is data, not a proof — the classes stay finite — but it is also a consistency test of the whole pipeline, and the absence of near misses says the divisibilities are already very restrictive at these sizes.  Check `a3.height_pairs`.
