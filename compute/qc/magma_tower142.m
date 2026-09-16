// Entry 142 (prepared): the full quotient curves of the route-less classes' components -- the quotient by the whole sign-and-inversion
// group, reached by the joint sign change and the diagonal double inversion in either order.  They have genus 3 or 4 (Sage) and are
// quadratic in no coordinate, so the tower cannot model them; this script asks Magma whether they are hyperelliptic in other
// coordinates, and if so for the model, the rank bounds and the points.  Paste ONE block at a time (120 s limit).  The member
// classes of each curve are listed (ledger index, frame) so a decided curve can be folded on exactly those classes.
// ===== block A: the full quotient (diag(-1,-1)_then_joint) of the (7,3) components of 4 route-less (2,1,1) classes: [[69319, 2], [69321, 2], [70010, 2], [70011, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-576)*X^0*Y^3 + (6912)*X^1*Y^1 + (9024)*X^1*Y^2 + (2640)*X^1*Y^3 + (-3840)*X^2*Y^0 + (-11200)*X^2*Y^1 + (-7312)*X^2*Y^2 + (-1132)*X^2*Y^3 + (2240)*X^3*Y^0 + (3344)*X^3*Y^1 + (1308)*X^3*Y^2 + (119)*X^3*Y^3 + (-208)*X^4*Y^0 + (-148)*X^4*Y^1 + (-35)*X^4*Y^2 + (4)*X^5*Y^0);
print "block A: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block B: the full quotient (diag(-1,-1)_then_joint) of the (8,4) components of 4 route-less (2,1,1) classes: [[69318, 2], [69320, 2], [70012, 2], [70013, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (64)*X^0*Y^4 + (-768)*X^1*Y^2 + (-1920)*X^1*Y^3 + (-208)*X^1*Y^4 + (8704)*X^2*Y^1 + (16640)*X^2*Y^2 + (3424)*X^2*Y^3 + (140)*X^2*Y^4 + (-24320)*X^3*Y^0 + (-47744)*X^3*Y^1 + (-15136)*X^3*Y^2 + (-1000)*X^3*Y^3 + (-15)*X^3*Y^4 + (20672)*X^4*Y^0 + (11360)*X^4*Y^1 + (784)*X^4*Y^2 + (18)*X^4*Y^3 + (-2512)*X^5*Y^0 + (-184)*X^5*Y^1 + (-3)*X^5*Y^2 + (4)*X^6*Y^0);
print "block B: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block C: the full quotient (diag(-1,-1)_then_joint) of the (8,4) components of 4 route-less (2,1,1) classes: [[75216, 1], [75218, 1], [75547, 2], [75548, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (64)*X^0*Y^4 + (256)*X^1*Y^2 + (640)*X^1*Y^3 + (-208)*X^1*Y^4 + (2560)*X^2*Y^1 + (-4352)*X^2*Y^2 + (-1824)*X^2*Y^3 + (140)*X^2*Y^4 + (-30464)*X^3*Y^0 + (-23680)*X^3*Y^1 + (-1056)*X^3*Y^2 + (504)*X^3*Y^3 + (-15)*X^3*Y^4 + (18112)*X^4*Y^0 + (6112)*X^4*Y^1 + (-464)*X^4*Y^2 + (-6)*X^4*Y^3 + (-2640)*X^5*Y^0 + (-24)*X^5*Y^1 + (9)*X^5*Y^2 + (36)*X^6*Y^0);
print "block C: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block D: the full quotient (diag(-1,-1)_then_joint) of the (8,4) components of 4 route-less (2,1,1) classes: [[75217, 1], [75219, 1], [75549, 2], [75550, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (576)*X^0*Y^4 + (2304)*X^1*Y^2 + (-384)*X^1*Y^3 + (-2640)*X^1*Y^4 + (-1536)*X^2*Y^1 + (-7424)*X^2*Y^2 + (6112)*X^2*Y^3 + (1132)*X^2*Y^4 + (-3840)*X^3*Y^0 + (8064)*X^3*Y^1 + (-1056)*X^3*Y^2 + (-1480)*X^3*Y^3 + (-119)*X^3*Y^4 + (2240)*X^4*Y^0 + (-1824)*X^4*Y^1 + (-272)*X^4*Y^2 + (10)*X^4*Y^3 + (-208)*X^5*Y^0 + (40)*X^5*Y^1 + (1)*X^5*Y^2 + (4)*X^6*Y^0);
print "block D: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block E: the full quotient (diag(1,1)_then_joint) of the (7,3) components of 2 route-less (2,1,1) classes: [[69319, 2], [70010, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^3 + (131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (17408)*X^1*Y^3 + (-65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (-2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (10240)*X^3*Y^1 + (608)*X^3*Y^2 + (119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (-512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block E: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block F: the full quotient (diag(1,1)_then_joint) of the (7,3) components of 2 route-less (2,1,1) classes: [[69321, 2], [70011, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (36864)*X^0*Y^3 + (-131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (-17408)*X^1*Y^3 + (65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (-10240)*X^3*Y^1 + (608)*X^3*Y^2 + (-119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block F: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block G: the full quotient (joint_then_diag(1,1)) of the (7,3) components of 2 route-less (2,1,1) classes: [[69319, 2], [70010, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (37760)*U2^0*V2^0 + (4944)*U2^0*V2^1 + (-29568)*U2^0*V2^2 + (-11336)*U2^0*V2^3 + (-7952)*U2^1*V2^0 + (14672)*U2^1*V2^1 + (26024)*U2^1*V2^2 + (8596)*U2^1*V2^3 + (-7760)*U2^2*V2^0 + (-14592)*U2^2*V2^1 + (-8260)*U2^2*V2^2 + (-1846)*U2^2*V2^3 + (4992)*U2^3*V2^0 + (3500)*U2^3*V2^1 + (958)*U2^3*V2^2 + (119)*U2^3*V2^3 + (-868)*U2^4*V2^0 + (-245)*U2^4*V2^1 + (-35)*U2^4*V2^2 + (49)*U2^5*V2^0);
print "block G: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block H: the full quotient (joint_then_diag(1,1)) of the (7,3) components of 2 route-less (2,1,1) classes: [[69321, 2], [70011, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-6816)*U2^0*V2^0 + (11952)*U2^0*V2^1 + (28752)*U2^0*V2^2 + (11336)*U2^0*V2^3 + (8672)*U2^1*V2^0 + (-21328)*U2^1*V2^1 + (-29064)*U2^1*V2^2 + (-8596)*U2^1*V2^3 + (6848)*U2^2*V2^0 + (11008)*U2^2*V2^1 + (7740)*U2^2*V2^2 + (1846)*U2^2*V2^3 + (-3064)*U2^3*V2^0 + (-1836)*U2^3*V2^1 + (-630)*U2^3*V2^2 + (-119)*U2^3*V2^3 + (314)*U2^4*V2^0 + (85)*U2^4*V2^1);
print "block H: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block I: the full quotient (diag(1,1)_then_joint) of the (8,4) components of 2 route-less (2,1,1) classes: [[69318, 2], [70012, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (-4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (-6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (-12)*X^4*Y^3 + (2048)*X^5*Y^0 + (144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block I: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block J: the full quotient (diag(1,1)_then_joint) of the (8,4) components of 2 route-less (2,1,1) classes: [[69320, 2], [70013, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (-57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (-608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (12)*X^4*Y^3 + (2048)*X^5*Y^0 + (-144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block J: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block K: the full quotient (diag(1,1)_then_joint) of the (8,4) components of 2 route-less (2,1,1) classes: [[75216, 1], [75547, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-65536)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (28672)*X^3*Y^1 + (-7424)*X^3*Y^2 + (-672)*X^3*Y^3 + (15)*X^3*Y^4 + (-4096)*X^4*Y^0 + (-3840)*X^4*Y^1 + (32)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (192)*X^5*Y^1 + (9)*X^5*Y^2);
print "block K: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;

// ===== block L: the full quotient (diag(1,1)_then_joint) of the (8,4) components of 2 route-less (2,1,1) classes: [[75217, 1], [75549, 2]]
// A plane model of genus 3 or 4 (Sage): is it hyperelliptic?  If so, the hyperelliptic model, the rank bounds of its Jacobian and its small points.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^4 + (131072)*X^1*Y^2 + (-16384)*X^1*Y^3 + (17408)*X^1*Y^4 + (65536)*X^2*Y^1 + (-61440)*X^2*Y^2 + (7424)*X^2*Y^3 + (-2560)*X^2*Y^4 + (-28672)*X^3*Y^1 + (9984)*X^3*Y^2 + (-928)*X^3*Y^3 + (119)*X^3*Y^4 + (-4096)*X^4*Y^0 + (3328)*X^4*Y^1 + (-672)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (-64)*X^5*Y^1 + (1)*X^5*Y^2);
print "block L: genus", Genus(C);
b, H, m := IsHyperelliptic(C);
print "hyperelliptic?", b;
if b then
    print "model:", H;
    J := Jacobian(H);
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
    print "points of height <= 10^4:", Points(H : Bound := 10000);
else
    print "canonical model:", CanonicalImage(C);
end if;
