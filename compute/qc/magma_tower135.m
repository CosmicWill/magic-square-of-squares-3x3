// Entry 135: the symmetry tower of the 28 surviving (1,1,1) classes.  Paste ONE BLOCK at a time into the Magma calculator
// (http://magma.maths.usyd.edu.au/calc/, 120 s limit).  Block 1 is the valuable one: the four genus-2 endpoints (classes
// 2918-2921): hyperelliptic model, rank bounds, torsion, points, and Chabauty when the rank is 1.  Blocks 2 and 3: the
// twenty-four genus-4 curves -- hyperellipticity and automorphism group, a few curves per paste if it times out.
// Lifts (u^2 - 4, v^2 - 4 rational squares; x a rational square; g, h admissible) are checked in Python from the point lists.

// ================= block 1: the four genus-2 second quotients (coordinates u, v) =================
P<uu,vv> := PolynomialRing(Rationals(), 2);
A := AffineSpace(P);
print "===== class 2918";
C := Curve(A, -10*uu^2*vv^3 + 4*uu*vv^4 + 10*uu^3*vv - 17*uu^2*vv^2 + 32*uu*vv^3 - 8*vv^4 + 29*uu^3 + 28*uu^2*vv + 28*uu*vv^2 - 24*vv^3 - 34*uu^2 - 168*uu*vv - 4*vv^2 - 36*uu + 144*vv + 40);
b, H := IsHyperelliptic(C); print "hyperelliptic:", b; print H;
if b then
  J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds:", rl, ru; print "torsion:", TorsionSubgroup(J);
  print "points of height <= 10^4:", Points(H : Bound := 10000);
  if ru eq 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0]; pts := Chabauty(m(free[1])); print "Chabauty: H(Q) =", pts;
  end if;
end if;

print "===== class 2919";
C := Curve(A, 2*uu^2*vv^3 + 4*uu*vv^4 - 2*uu^3*vv - 25*uu^2*vv^2 - 8*vv^4 + 5*uu^3 + 4*uu^2*vv + 28*uu*vv^2 - 8*vv^3 + 46*uu^2 + 8*uu*vv + 28*vv^2 + 60*uu - 16*vv - 280);
b, H := IsHyperelliptic(C); print "hyperelliptic:", b; print H;
if b then
  J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds:", rl, ru; print "torsion:", TorsionSubgroup(J);
  print "points of height <= 10^4:", Points(H : Bound := 10000);
  if ru eq 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0]; pts := Chabauty(m(free[1])); print "Chabauty: H(Q) =", pts;
  end if;
end if;

print "===== class 2920";
C := Curve(A, -2*uu^2*vv^3 + 4*uu*vv^4 + 2*uu^3*vv - 25*uu^2*vv^2 - 8*vv^4 + 5*uu^3 - 4*uu^2*vv + 28*uu*vv^2 + 8*vv^3 + 46*uu^2 - 8*uu*vv + 28*vv^2 + 60*uu + 16*vv - 280);
b, H := IsHyperelliptic(C); print "hyperelliptic:", b; print H;
if b then
  J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds:", rl, ru; print "torsion:", TorsionSubgroup(J);
  print "points of height <= 10^4:", Points(H : Bound := 10000);
  if ru eq 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0]; pts := Chabauty(m(free[1])); print "Chabauty: H(Q) =", pts;
  end if;
end if;

print "===== class 2921";
C := Curve(A, 10*uu^2*vv^3 + 4*uu*vv^4 - 10*uu^3*vv - 17*uu^2*vv^2 - 32*uu*vv^3 - 8*vv^4 + 29*uu^3 - 28*uu^2*vv + 28*uu*vv^2 + 24*vv^3 - 34*uu^2 + 168*uu*vv - 4*vv^2 - 36*uu - 144*vv + 40);
b, H := IsHyperelliptic(C); print "hyperelliptic:", b; print H;
if b then
  J := Jacobian(H); rl, ru := RankBounds(J); print "rank bounds:", rl, ru; print "torsion:", TorsionSubgroup(J);
  print "points of height <= 10^4:", Points(H : Bound := 10000);
  if ru eq 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0]; pts := Chabauty(m(free[1])); print "Chabauty: H(Q) =", pts;
  end if;
end if;

// ================= block 2: the sixteen genus-4 second quotients of the (8,8) classes (coordinates u, v) =================
P<uu,vv> := PolynomialRing(Rationals(), 2);
A := AffineSpace(P);
print "===== class 1632";
C := Curve(A, -3*uu^4*vv^6 - 2*uu^3*vv^7 + uu^2*vv^8 + 10*uu^5*vv^4 + 8*uu^4*vv^5 + 46*uu^3*vv^6 - 4*uu^2*vv^7 - 4*uu*vv^8 - 3*uu^6*vv^2 + 6*uu^5*vv^3 - 71*uu^4*vv^4 - 72*uu^3*vv^5 - 148*uu^2*vv^6 + 40*uu*vv^7 + 4*vv^8 - 4*uu^6*vv - 48*uu^5*vv^2 - 44*uu^4*vv^3 - 408*uu^3*vv^4 + 752*uu^2*vv^5 + 8*uu*vv^6 - 48*vv^7);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1634";
C := Curve(A, 2*uu^4*vv^5 - 3*uu^3*vv^6 - 2*uu^2*vv^7 - 4*uu^5*vv^3 + 3*uu^4*vv^4 + 2*uu^3*vv^5 + 37*uu^2*vv^6 + 10*uu*vv^7 + vv^8 + 2*uu^6*vv - 5*uu^5*vv^2 - 6*uu^4*vv^3 - 34*uu^3*vv^4 - 104*uu^2*vv^5 - 114*uu*vv^6 - 12*vv^7 + 5*uu^6 + 14*uu^5*vv + 33*uu^4*vv^2 + 142*uu^3*vv^3 + uu^2*vv^4 + 304*uu*vv^5 + 64*vv^6);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1637";
C := Curve(A, 2*uu^4*vv^5 - 3*uu^3*vv^6 - 2*uu^2*vv^7 - 4*uu^5*vv^3 + 3*uu^4*vv^4 + 2*uu^3*vv^5 + 37*uu^2*vv^6 + 10*uu*vv^7 + vv^8 + 2*uu^6*vv - 5*uu^5*vv^2 - 6*uu^4*vv^3 - 34*uu^3*vv^4 - 104*uu^2*vv^5 - 114*uu*vv^6 - 12*vv^7 + 5*uu^6 + 14*uu^5*vv + 33*uu^4*vv^2 + 142*uu^3*vv^3 + uu^2*vv^4 + 304*uu*vv^5 + 64*vv^6);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1639";
C := Curve(A, -3*uu^4*vv^6 - 2*uu^3*vv^7 + uu^2*vv^8 + 10*uu^5*vv^4 + 8*uu^4*vv^5 + 46*uu^3*vv^6 - 4*uu^2*vv^7 - 4*uu*vv^8 - 3*uu^6*vv^2 + 6*uu^5*vv^3 - 71*uu^4*vv^4 - 72*uu^3*vv^5 - 148*uu^2*vv^6 + 40*uu*vv^7 + 4*vv^8 - 4*uu^6*vv - 48*uu^5*vv^2 - 44*uu^4*vv^3 - 408*uu^3*vv^4 + 752*uu^2*vv^5 + 8*uu*vv^6 - 48*vv^7);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1782";
C := Curve(A, 2*uu^4*vv^5 - 3*uu^3*vv^6 - 2*uu^2*vv^7 - 4*uu^5*vv^3 + 3*uu^4*vv^4 + 2*uu^3*vv^5 + 37*uu^2*vv^6 + 10*uu*vv^7 + vv^8 + 2*uu^6*vv - 5*uu^5*vv^2 - 6*uu^4*vv^3 - 34*uu^3*vv^4 - 104*uu^2*vv^5 - 114*uu*vv^6 - 12*vv^7 + 5*uu^6 + 14*uu^5*vv + 33*uu^4*vv^2 + 142*uu^3*vv^3 + uu^2*vv^4 + 304*uu*vv^5 + 64*vv^6);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1783";
C := Curve(A, -3*uu^4*vv^6 - 2*uu^3*vv^7 + uu^2*vv^8 + 10*uu^5*vv^4 + 8*uu^4*vv^5 + 46*uu^3*vv^6 - 4*uu^2*vv^7 - 4*uu*vv^8 - 3*uu^6*vv^2 + 6*uu^5*vv^3 - 71*uu^4*vv^4 - 72*uu^3*vv^5 - 148*uu^2*vv^6 + 40*uu*vv^7 + 4*vv^8 - 4*uu^6*vv - 48*uu^5*vv^2 - 44*uu^4*vv^3 - 408*uu^3*vv^4 + 752*uu^2*vv^5 + 8*uu*vv^6 - 48*vv^7);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1784";
C := Curve(A, -3*uu^4*vv^6 - 2*uu^3*vv^7 + uu^2*vv^8 + 10*uu^5*vv^4 + 8*uu^4*vv^5 + 46*uu^3*vv^6 - 4*uu^2*vv^7 - 4*uu*vv^8 - 3*uu^6*vv^2 + 6*uu^5*vv^3 - 71*uu^4*vv^4 - 72*uu^3*vv^5 - 148*uu^2*vv^6 + 40*uu*vv^7 + 4*vv^8 - 4*uu^6*vv - 48*uu^5*vv^2 - 44*uu^4*vv^3 - 408*uu^3*vv^4 + 752*uu^2*vv^5 + 8*uu*vv^6 - 48*vv^7);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 1785";
C := Curve(A, 2*uu^4*vv^5 - 3*uu^3*vv^6 - 2*uu^2*vv^7 - 4*uu^5*vv^3 + 3*uu^4*vv^4 + 2*uu^3*vv^5 + 37*uu^2*vv^6 + 10*uu*vv^7 + vv^8 + 2*uu^6*vv - 5*uu^5*vv^2 - 6*uu^4*vv^3 - 34*uu^3*vv^4 - 104*uu^2*vv^5 - 114*uu*vv^6 - 12*vv^7 + 5*uu^6 + 14*uu^5*vv + 33*uu^4*vv^2 + 142*uu^3*vv^3 + uu^2*vv^4 + 304*uu*vv^5 + 64*vv^6);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2803";
C := Curve(A, -243*uu^4*vv^6 - 162*uu^3*vv^7 + 81*uu^2*vv^8 + 522*uu^5*vv^4 + 1368*uu^4*vv^5 + 486*uu^3*vv^6 + 540*uu^2*vv^7 - 252*uu*vv^8 - 243*uu^6*vv^2 - 810*uu^5*vv^3 + 1753*uu^4*vv^4 - 2488*uu^3*vv^5 - 1284*uu^2*vv^6 - 376*uu*vv^7 + 196*vv^8 - 324*uu^6*vv - 6552*uu^5*vv^2 - 14524*uu^4*vv^3 - 3536*uu^3*vv^4 -);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2805";
C := Curve(A, -243*uu^4*vv^6 - 162*uu^3*vv^7 + 81*uu^2*vv^8 + 522*uu^5*vv^4 + 1368*uu^4*vv^5 + 486*uu^3*vv^6 + 540*uu^2*vv^7 - 252*uu*vv^8 - 243*uu^6*vv^2 - 810*uu^5*vv^3 + 1753*uu^4*vv^4 - 2488*uu^3*vv^5 - 1284*uu^2*vv^6 - 376*uu*vv^7 + 196*vv^8 - 324*uu^6*vv - 6552*uu^5*vv^2 - 14524*uu^4*vv^3 - 3536*uu^3*vv^4 -);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2807";
C := Curve(A, 45*uu^4*vv^6 - 210*uu^3*vv^7 + 225*uu^2*vv^8 - 150*uu^5*vv^4 + 1272*uu^4*vv^5 - 1018*uu^3*vv^6 - 964*uu^2*vv^7 - 1020*uu*vv^8 + 45*uu^6*vv^2 - 1370*uu^5*vv^3 + 297*uu^4*vv^4 + 5768*uu^3*vv^5 + 4732*uu^2*vv^6 + 6984*uu*vv^7 + 1156*vv^8 + 252*uu^6*vv - 1400*uu^5*vv^2 - 12764*uu^4*vv^3 + 13360*uu^3*vv^);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2809";
C := Curve(A, 45*uu^4*vv^6 - 210*uu^3*vv^7 + 225*uu^2*vv^8 - 150*uu^5*vv^4 + 1272*uu^4*vv^5 - 1018*uu^3*vv^6 - 964*uu^2*vv^7 - 1020*uu*vv^8 + 45*uu^6*vv^2 - 1370*uu^5*vv^3 + 297*uu^4*vv^4 + 5768*uu^3*vv^5 + 4732*uu^2*vv^6 + 6984*uu*vv^7 + 1156*vv^8 + 252*uu^6*vv - 1400*uu^5*vv^2 - 12764*uu^4*vv^3 + 13360*uu^3*vv^);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2902";
C := Curve(A, 45*uu^4*vv^6 + 210*uu^3*vv^7 + 225*uu^2*vv^8 - 150*uu^5*vv^4 - 1272*uu^4*vv^5 - 1018*uu^3*vv^6 + 964*uu^2*vv^7 - 1020*uu*vv^8 + 45*uu^6*vv^2 + 1370*uu^5*vv^3 + 297*uu^4*vv^4 - 5768*uu^3*vv^5 + 4732*uu^2*vv^6 - 6984*uu*vv^7 + 1156*vv^8 - 252*uu^6*vv - 1400*uu^5*vv^2 + 12764*uu^4*vv^3 + 13360*uu^3*vv^);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2903";
C := Curve(A, 45*uu^4*vv^6 + 210*uu^3*vv^7 + 225*uu^2*vv^8 - 150*uu^5*vv^4 - 1272*uu^4*vv^5 - 1018*uu^3*vv^6 + 964*uu^2*vv^7 - 1020*uu*vv^8 + 45*uu^6*vv^2 + 1370*uu^5*vv^3 + 297*uu^4*vv^4 - 5768*uu^3*vv^5 + 4732*uu^2*vv^6 - 6984*uu*vv^7 + 1156*vv^8 - 252*uu^6*vv - 1400*uu^5*vv^2 + 12764*uu^4*vv^3 + 13360*uu^3*vv^);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2904";
C := Curve(A, -243*uu^4*vv^6 + 162*uu^3*vv^7 + 81*uu^2*vv^8 + 522*uu^5*vv^4 - 1368*uu^4*vv^5 + 486*uu^3*vv^6 - 540*uu^2*vv^7 - 252*uu*vv^8 - 243*uu^6*vv^2 + 810*uu^5*vv^3 + 1753*uu^4*vv^4 + 2488*uu^3*vv^5 - 1284*uu^2*vv^6 + 376*uu*vv^7 + 196*vv^8 + 324*uu^6*vv - 6552*uu^5*vv^2 + 14524*uu^4*vv^3 - 3536*uu^3*vv^4 +);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2905";
C := Curve(A, -243*uu^4*vv^6 + 162*uu^3*vv^7 + 81*uu^2*vv^8 + 522*uu^5*vv^4 - 1368*uu^4*vv^5 + 486*uu^3*vv^6 - 540*uu^2*vv^7 - 252*uu*vv^8 - 243*uu^6*vv^2 + 810*uu^5*vv^3 + 1753*uu^4*vv^4 + 2488*uu^3*vv^5 - 1284*uu^2*vv^6 + 376*uu*vv^7 + 196*vv^8 + 324*uu^6*vv - 6552*uu^5*vv^2 + 14524*uu^4*vv^3 - 3536*uu^3*vv^4 +);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

// ================= block 3: the eight genus-4 joint quotients without the inversion symmetry (coordinates x, y) =================
Q<x,y> := PolynomialRing(Rationals(), 2);
B := AffineSpace(Q);
print "===== class 2914";
C := Curve(B, -9*x^3*y - 4*x^3 + 3*x^2*y^3 + 8*x^2*y^2 + 14*x^2*y + 4*x^2 - 4*x*y^4 + 6*x*y^3 - 8*x*y^2 - 9*x*y + 4*y^4 + 3*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2915";
C := Curve(B, -3*x^3*y + 4*x^3 + x^2*y^3 - 8*x^2*y^2 - 6*x^2*y - 4*x^2 + 4*x*y^4 + 34*x*y^3 + 8*x*y^2 - 3*x*y - 4*y^4 + y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2916";
C := Curve(B, -5*x^3*y - 4*x^3 + 7*x^2*y^3 + 16*x^2*y^2 + 6*x^2*y + 4*x^2 + 4*x*y^4 - 2*x*y^3 - 16*x*y^2 - 5*x*y - 4*y^4 + 7*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2917";
C := Curve(B, -7*x^3*y + 4*x^3 + 5*x^2*y^3 + 16*x^2*y^2 + 2*x^2*y - 4*x^2 - 4*x*y^4 - 6*x*y^3 - 16*x*y^2 - 7*x*y + 4*y^4 + 5*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2940";
C := Curve(B, -5*x^3*y - 4*x^3 + 7*x^2*y^3 + 16*x^2*y^2 + 6*x^2*y + 4*x^2 + 4*x*y^4 - 2*x*y^3 - 16*x*y^2 - 5*x*y - 4*y^4 + 7*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2941";
C := Curve(B, -7*x^3*y + 4*x^3 + 5*x^2*y^3 + 16*x^2*y^2 + 2*x^2*y - 4*x^2 - 4*x*y^4 - 6*x*y^3 - 16*x*y^2 - 7*x*y + 4*y^4 + 5*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2942";
C := Curve(B, -9*x^3*y - 4*x^3 + 3*x^2*y^3 + 8*x^2*y^2 + 14*x^2*y + 4*x^2 - 4*x*y^4 + 6*x*y^3 - 8*x*y^2 - 9*x*y + 4*y^4 + 3*y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

print "===== class 2943";
C := Curve(B, -3*x^3*y + 4*x^3 + x^2*y^3 - 8*x^2*y^2 - 6*x^2*y - 4*x^2 + 4*x*y^4 + 34*x*y^3 + 8*x*y^2 - 3*x*y - 4*y^4 + y^3);
print "genus:", Genus(C);
try b, H := IsHyperelliptic(C); print "hyperelliptic:", b; if b then print H; end if; catch e print "IsHyperelliptic failed:", e`Object; end try;
try G := AutomorphismGroup(C); print "automorphism group order:", #G; catch e print "AutomorphismGroup failed:", e`Object; end try;

