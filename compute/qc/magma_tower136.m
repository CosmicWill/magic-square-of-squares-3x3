// Entry 136: the intermediate genus-3 curves of the symmetry tower of the 24 (1,1,1) survivors that end on a rank-1 elliptic curve.
// (a) the eight (4,4) classes 2914-2917, 2940-2943: C/<g -> -1/g> is hyperelliptic of genus 3, y^2 = D(h) (an octic in h);
//     its Jacobian is isogenous to 99a2 (rank 1) times a 2-dimensional Prym.  Wanted: RankBounds, torsion, small points.
// (b) the sixteen (8,8) classes: E3(u, v) = C/<g -> -1/g, h -> -1/h>, a (4,4) curve of genus 3 whose quotient by (u,v) -> (-u,-v)
//     is 666d1 (rank 1).  Wanted: IsHyperelliptic (and the model), RankBounds if hyperelliptic, small points.
// Paste one block at a time (120 s).  Four distinct octics and six distinct E3 occur; the others are sign variants.
P<x> := PolynomialRing(Rationals());

// ---- block A: the octics y^2 = D(x) of the (4,4) classes
print "===== class 2914 (genus 3, hyperelliptic)";
H := HyperellipticCurve(16*x^8 - 208*x^6 + 576*x^4 - 208*x^2 + 16);
print "genus", Genus(H); J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru;
print "torsion", TorsionSubgroup(J); print "points of height <= 1000", Points(H : Bound := 1000);

// class 2915: the same octic as class 2914
// class 2916: the same octic as class 2914
// class 2917: the same octic as class 2914
// class 2940: the same octic as class 2914
// class 2941: the same octic as class 2914
// class 2942: the same octic as class 2914
// class 2943: the same octic as class 2914
// ---- block B: the genus-3 curves E3(u, v) of the (8,8) classes
Q<u,v> := PolynomialRing(Rationals(), 2); A := AffineSpace(Q);
print "===== class 1632 (E3, genus 3)";
C := Curve(A, -3*u^4*v^2 - 2*u^3*v^3 + u^2*v^4 + 4*u^4 + 8*u^3*v + 36*u^2*v^2 - 16*u*v^3 - 128*u*v + 64*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

print "===== class 1634 (E3, genus 3)";
C := Curve(A, u^4*v^2 - 2*u^3*v^3 - 4*u^3*v + 9*u^2*v^2 + 2*u*v^3 + v^4 + 4*u^2 - 8*u*v - 12*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

// class 1637: the same E3 as class 1634
// class 1639: the same E3 as class 1632
// class 1782: the same E3 as class 1634
// class 1783: the same E3 as class 1632
// class 1784: the same E3 as class 1632
// class 1785: the same E3 as class 1634
print "===== class 2803 (E3, genus 3)";
C := Curve(A, -27*u^4*v^2 - 18*u^3*v^3 + 9*u^2*v^4 + 4*u^4 + 152*u^3*v - 24*u^2*v^2 - 40*u*v^3 + 4*v^4 - 240*u^2 + 224*u*v - 48*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

// class 2805: the same E3 as class 2803
print "===== class 2807 (E3, genus 3)";
C := Curve(A, 3*u^4*v^2 - 14*u^3*v^3 + 15*u^2*v^4 - 4*u^4 + 40*u^3*v + 24*u^2*v^2 - 152*u*v^3 - 4*v^4 - 144*u^2 + 288*u*v + 432*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

// class 2809: the same E3 as class 2807
print "===== class 2902 (E3, genus 3)";
C := Curve(A, 3*u^4*v^2 + 14*u^3*v^3 + 15*u^2*v^4 - 4*u^4 - 40*u^3*v + 24*u^2*v^2 + 152*u*v^3 - 4*v^4 - 144*u^2 - 288*u*v + 432*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

// class 2903: the same E3 as class 2902
print "===== class 2904 (E3, genus 3)";
C := Curve(A, -27*u^4*v^2 + 18*u^3*v^3 + 9*u^2*v^4 + 4*u^4 - 152*u^3*v - 24*u^2*v^2 + 40*u*v^3 + 4*v^4 - 240*u^2 - 224*u*v - 48*v^2);
print "genus", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic", b; if b then print H; J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds", rl, ru; print "torsion", TorsionSubgroup(J); end if; catch e print "failed:", e`Object; end try;
print "points of height <= 300", Points(C : Bound := 300);

// class 2905: the same E3 as class 2904
