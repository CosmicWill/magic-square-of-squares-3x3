// Entry 131 (R.13 path 2): the two genus-2 curves behind the eight open octic tower classes 0-7 of the (1,1,1) box.
// Each is the odd quotient w^2 = u Qt(u) of the level-0 model y^2 = Qt(t^2); neither is bielliptic (the general test of
// entry 131), so the E1 x E2 quadratic Chabauty route is closed; the known points (1, 4) and (-1/5, .) have infinite order
// in the Jacobian (entry 131), so the rank is >= 1.  Needed: the rank (2-descent) and, if it is 1, Chabauty + the
// Mordell-Weil sieve.  Paste into the Magma calculator (http://magma.maths.usyd.edu.au/calc/, 120 s limit) one curve at a time.
// A class dies if EVERY rational point of the curve has u in {0, 1, -1, oo} (a degenerate frame ratio t = sqrt(u)).
P<x> := PolynomialRing(Rationals());
for f in [25*x^5 - 36*x^4 - 18*x^3 + 44*x^2 + x, 25*x^5 - 4*x^4 - 18*x^3 + 12*x^2 + x] do
    C := HyperellipticCurve(f);
    J := Jacobian(C);
    print "curve", f;
    print "  points of height <= 10^4:", Points(C : Bound := 10000);
    rl, ru := RankBounds(J);
    print "  rank bounds (lower from points, upper from 2-descent):", rl, ru;
    print "  2-Selmer rank:", TwoSelmerGroup(J);
    print "  torsion:", TorsionSubgroup(J);
    if ru eq 1 then
        // Chabauty needs a generator of a finite-index subgroup of J(Q): take the known point
        pts := Points(C : Bound := 100);
        D := pts[#pts] - pts[1];
        ok, gens := MordellWeilGroupGenus2(J);   // may take long; alternative below
        print "  MW group:", ok, gens;
        print "  Chabauty:", Chabauty(gens[1]);
    end if;
end for;
