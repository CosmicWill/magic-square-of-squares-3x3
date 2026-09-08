// Entry 139 (prepared during entry 138): the genus-2 endpoints of the (2,1,1) and (3,1,1) classes that stay open on every frame
// of the all-frames sweep, ranked by the number of classes that meet them.  Each block is self-contained: paste ONE block at a
// time into the Magma calculator (120 s limit).  A block decides its curve's rational points when the rank is 0 (torsion only) or
// 1 (Chabauty on the generator of the proved group); a decided curve becomes a KNOWN_GENUS2 entry of compute/symmetry_tower.py
// and kills every class whose fibers over its points are degenerate (the way K killed the last sixteen (1,1,1) classes).
// For |disc| <= 10^6 the LMFDB curves with the same |disc| are listed as candidates (isomorphism not checked).
// ===== block A: y^2 = (1)*x^6 + (-90)*x^5 + (4367)*x^4 + (-940)*x^3 + (-1009)*x^2 + (294)*x^1 + (1)
// (16 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant 10078984 = [2, 3; 1259873, 1]; PARI points to 10^4: [[-1, 64], [-1, -64], [0, 1], [0, -1], [1/3, 64/27], [1/3, -64/27]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-90)*x^5 + (4367)*x^4 + (-940)*x^3 + (-1009)*x^2 + (294)*x^1 + (1));
J := Jacobian(C);
print "block A: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block B: y^2 = (-16384)*x^6 + (2560)*x^4 + (-100)*x^2 + (1)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant 303038464 = [2, 20; 17, 2]; PARI points to 10^4: [[0, 1], [0, -1], [-1/8, 0], [1/8, 0]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((-16384)*x^6 + (2560)*x^4 + (-100)*x^2 + (1));
J := Jacobian(C);
print "block B: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block C: y^2 = (-1024)*x^6 + (512)*x^4 + (-48)*x^2 + (1)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant 22429696 = [2, 14; 37, 2]; PARI points to 10^4: [[0, 1], [0, -1]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((-1024)*x^6 + (512)*x^4 + (-48)*x^2 + (1));
J := Jacobian(C);
print "block C: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block D: y^2 = (1)*x^6 + (-184)*x^5 + (17904)*x^4 + (-8448)*x^3 + (-57600)*x^2 + (51200)*x^1 + (4096)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant 21218784 = [2, 5; 3, 1; 83, 1; 2663, 1]; PARI points to 10^4: [[-4, 2048], [-4, -2048], [0, 64], [0, -64], [8, 7744], [8, -7744], [4/3, 2048/27], [4/3, -2048/27], [12/5, 63488/125], [12/5, -63488/125], [-268/27, 274548736/19683], [-268/27, -274548736/19683], [20/51, 16369664/132651], [20/51, -16369664/132651]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-184)*x^5 + (17904)*x^4 + (-8448)*x^3 + (-57600)*x^2 + (51200)*x^1 + (4096));
J := Jacobian(C);
print "block D: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block E: y^2 = (1)*x^6 + (-76)*x^5 + (1200)*x^4 + (-4224)*x^3 + (19200)*x^2 + (-19456)*x^1 + (4096)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant -221952 = [2, 8; 3, 1; 17, 2]; PARI points to 10^4: [[-4, 1024], [-4, -1024], [0, 64], [0, -64], [12, 2048], [12, -2048], [4/3, 2048/27], [4/3, -2048/27]])
// LMFDB curves with the same |disc| (same-discriminant candidates only, isomorphism not checked): 13872.b.221952.1 (analytic rank 1, torsion 2, 2 points); 27744.b.221952.1 (analytic rank 2, torsion 2, 10 points)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-76)*x^5 + (1200)*x^4 + (-4224)*x^3 + (19200)*x^2 + (-19456)*x^1 + (4096));
J := Jacobian(C);
print "block E: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block F: y^2 = (1)*x^6 + (-42)*x^5 + (335)*x^4 + (-268)*x^3 + (335)*x^2 + (-42)*x^1 + (1)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant -109520 = [2, 4; 5, 1; 37, 2]; PARI points to 10^4: [[-1, 32], [-1, -32], [0, 1], [0, -1], [39, 22112], [39, -22112], [1/39, 22112/59319], [1/39, -22112/59319]])
// LMFDB curves with the same |disc| (same-discriminant candidates only, isomorphism not checked): 13690.a.109520.1 (analytic rank 1, torsion 2, 6 points); 54760.a.109520.1 (analytic rank 2, torsion 3, 6 points); 54760.b.109520.1 (analytic rank 2, torsion 1, 10 points); 109520.a.109520.1 (analytic rank 2, torsion 1, 6 points); 109520.b.109520.1 (analytic rank 0, torsion 3, 0 points)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-42)*x^5 + (335)*x^4 + (-268)*x^3 + (335)*x^2 + (-42)*x^1 + (1));
J := Jacobian(C);
print "block F: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block G: y^2 = (1)*x^6 + (-52)*x^4 + (128)*x^2 + (3072)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant -59579786330112 = [2, 36; 3, 1; 17, 2]; PARI points to 10^4: [])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-52)*x^4 + (128)*x^2 + (3072));
J := Jacobian(C);
print "block G: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block H: y^2 = (1)*x^6 + (-36)*x^4 + (176)*x^2 + (320)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant -7349762785280 = [2, 30; 5, 1; 37, 2]; PARI points to 10^4: [])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-36)*x^4 + (176)*x^2 + (320));
J := Jacobian(C);
print "block H: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block I: y^2 = (1)*x^6 + (200)*x^5 + (-3600)*x^4 + (-8448)*x^3 + (286464)*x^2 + (-47104)*x^1 + (4096)
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant 21218784 = [2, 5; 3, 1; 83, 1; 2663, 1]; PARI points to 10^4: [[-4, 2048], [-4, -2048], [0, 64], [0, -64], [2, 968], [2, -968], [12, 2048], [12, -2048], [20/3, 63488/27], [20/3, -63488/27], [204/5, 16369664/125], [204/5, -16369664/125], [-108/67, 274548736/300763], [-108/67, -274548736/300763]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (200)*x^5 + (-3600)*x^4 + (-8448)*x^3 + (286464)*x^2 + (-47104)*x^1 + (4096));
J := Jacobian(C);
print "block I: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block J: y^2 = (1)*x^5 + (688)*x^4 + (3808)*x^3 + (-10496)*x^2 + (6400)*x^1
// (8 open classes of the (2,1,1)/(3,1,1) campaigns meet this curve on some frame; minimal discriminant -1355284480000 = [2, 22; 5, 4; 11, 1; 47, 1]; PARI points to 10^4: [[0, 0]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^5 + (688)*x^4 + (3808)*x^3 + (-10496)*x^2 + (6400)*x^1);
J := Jacobian(C);
print "block J: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;
