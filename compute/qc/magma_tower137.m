// Entry 137/138: the last sixteen (1,1,1) classes sit over four genus-3 hyperelliptic curves E3 (Magma's models from block B of
// magma_tower136.m, made integral by scaling y).  PARI: all four have the same Frobenius polynomials at every prime tested, which
// factor as (quadratic)(quartic): the Jacobian is isogenous to 666d1 (rank 1) times a simple abelian surface P.  RankBounds gave
// [0, 2], so rank(J) is 1 or 2, below the genus 3: Chabauty-Coleman applies once the rank is known.  Wanted here: are the four
// curves isomorphic; the points; a torsion bound; extra automorphisms; an odd-degree model (for Coleman integration in Sage).
P<x> := PolynomialRing(Rationals());
H1 := HyperellipticCurve(1162261467*x^8 - 10847773692*x^7 + 42874534116*x^6 - 92980917360*x^5 + 119689016256*x^4 - 92547261504*x^3 + 41937072192*x^2 - 10657163520*x + 1375605504);   // classes 1632, 1639, 1783, 1784
H2 := HyperellipticCurve(110592*x^8 - 552960*x^7 + 1133568*x^6 - 1244160*x^5 + 804096*x^4 - 308736*x^3 + 62208*x^2 - 4608*x + 576);   // classes 1634, 1637, 1782, 1785
H3 := HyperellipticCurve(177990455916*x^8 + 612860910480*x^7 + 1071854613648*x^6 + 1051281032256*x^5 + 604264437504*x^4 + 208633501440*x^3 + 42756989184*x^2 + 4808014848*x + 228953088);   // classes 2803, 2805, 2904, 2905
H4 := HyperellipticCurve(244157004*x^8 - 2522061360*x^7 + 13232773008*x^6 - 38936334528*x^5 + 67140493056*x^4 - 69544500480*x^3 + 42756989184*x^2 - 14424044544*x + 2060577792);   // classes 2807, 2809, 2902, 2903

print "isomorphic pairs:";
for i in [1..4] do for j in [i+1..4] do b := IsIsomorphic(H[i], H[j]) where H := [H1, H2, H3, H4]; print i, j, b; end for; end for;

print "===== H1";
H := H1; J := Jacobian(H);
print "points of height <= 10^4:", Points(H : Bound := 10000);
print "torsion bound:", TorsionBound(J, 30);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
try A := AutomorphismGroup(H); print "automorphism group order:", #A; catch e print "AutomorphismGroup failed:", e`Object; end try;
b, Hodd := HasOddDegreeModel(H); print "odd degree model:", b; if b then print Hodd; end if;

print "===== H2";
H := H2; J := Jacobian(H);
print "points of height <= 10^4:", Points(H : Bound := 10000);
print "torsion bound:", TorsionBound(J, 30);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
try A := AutomorphismGroup(H); print "automorphism group order:", #A; catch e print "AutomorphismGroup failed:", e`Object; end try;
b, Hodd := HasOddDegreeModel(H); print "odd degree model:", b; if b then print Hodd; end if;

print "===== H3";
H := H3; J := Jacobian(H);
print "points of height <= 10^4:", Points(H : Bound := 10000);
print "torsion bound:", TorsionBound(J, 30);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
try A := AutomorphismGroup(H); print "automorphism group order:", #A; catch e print "AutomorphismGroup failed:", e`Object; end try;
b, Hodd := HasOddDegreeModel(H); print "odd degree model:", b; if b then print Hodd; end if;

print "===== H4";
H := H4; J := Jacobian(H);
print "points of height <= 10^4:", Points(H : Bound := 10000);
print "torsion bound:", TorsionBound(J, 30);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
try A := AutomorphismGroup(H); print "automorphism group order:", #A; catch e print "AutomorphismGroup failed:", e`Object; end try;
b, Hodd := HasOddDegreeModel(H); print "odd degree model:", b; if b then print Hodd; end if;

