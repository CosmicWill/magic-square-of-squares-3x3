// Entry 131 (R.13 path 2): the two genus-2 curves behind the eight open octic tower classes 0-7 of the (1,1,1) box.
// Each is the odd quotient w^2 = u Qt(u) of the level-0 model y^2 = Qt(t^2); neither is bielliptic (the general test of
// entry 131), so the E1 x E2 quadratic Chabauty route is closed; the known points (1, 4) and (-1/5, .) have infinite order
// in the Jacobian (entry 131), so the rank is >= 1.  Needed: the rank (2-descent) and, if it is 1, Chabauty + the
// Mordell-Weil sieve.  Paste into the Magma calculator (http://magma.maths.usyd.edu.au/calc/, 120 s limit); if it times
// out, run one curve at a time.  A class dies if EVERY rational point of the curve has u in {0, 1, -1, oo} or u a
// non-square (t = sqrt(u) must be a rational frame ratio, and 0, +-1, oo are degenerate).
// First run (2026-09-07, C_a): rank bounds 1 1, 2-Selmer (Z/2)^3, torsion Z/2 + Z/4, MW group Z/2 + Z/4 + Z, seven points of
// height <= 10^4: oo, (-1,0), (0,0), (1,+-4), (-1/5, +-32/25).  The Chabauty call below is the corrected one.
P<x> := PolynomialRing(Rationals());
for f in [25*x^5 - 36*x^4 - 18*x^3 + 44*x^2 + x, 25*x^5 - 4*x^4 - 18*x^3 + 12*x^2 + x] do
    C := HyperellipticCurve(f);
    J := Jacobian(C);
    print "curve", f;
    print "  points of height <= 10^4:", Points(C : Bound := 10000);
    rl, ru := RankBounds(J);
    print "  rank bounds (lower from points, upper from 2-descent):", rl, ru;
    print "  torsion:", TorsionSubgroup(J);
    if ru eq 1 then
        // the full Mordell-Weil group: abstract group G, map m to J, and the two proof flags
        G, m, rankproved, groupproved := MordellWeilGroupGenus2(J);
        print "  MW group:", G;
        print "  rank proved:", rankproved, " group proved (generators generate all of J(Q)):", groupproved;
        free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
        Pt := m(free[1]);
        print "  generator of the free part:", Pt;
        pts, N := Chabauty(Pt);
        print "  Chabauty + Mordell-Weil sieve: C(Q) =", pts;
        print "  index condition: complete if the index of <Pt> + torsion in J(Q) is coprime to", N, "(it is 1 when the group is proved)";
    end if;
end for;
