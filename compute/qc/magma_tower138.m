// Entry 138: the last sixteen (1,1,1) classes.  Frame 0 gives one genus-3 curve H (block C of magma_tower137.m: the four
// models are isomorphic; rank bounds [0, 2]; automorphism group of order 4; no odd-degree model).  Frames 1 and 2 give, for
// every one of the sixteen classes, the quotient by h -> -1/h, an even octic in g whose odd companion is ONE genus-2 curve
//     K: w^2 = z^5 + 80 z^4 + 126 z^3 - 16 z^2 + z        (z = g^2; the reciprocal z^5 - 16 z^4 + 126 z^3 + 80 z^2 + z is the same curve),
// whose Jacobian has the same Frobenius quartics as the Prym of H (PARI): J(K) is that Prym.  PARI finds only the point (0, 0)
// below height 5000.  If rank J(K) = 0, K(Q) is the torsion set and every point lifts only to g in {0, oo} (degenerate) unless
// a point with z a nonzero square appears; if rank 1, Chabauty decides K(Q).  Either way the sixteen classes are decided.
P<x> := PolynomialRing(Rationals());
K := HyperellipticCurve(x^5 + 80*x^4 + 126*x^3 - 16*x^2 + x);
J := Jacobian(K);
print "points of height <= 10^5:", Points(K : Bound := 100000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "2-Selmer:", TwoSelmerGroup(J);
print "torsion:", TorsionSubgroup(J);
if ru eq 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: K(Q) =", pts; print "index primes:", N; end if;
end if;
