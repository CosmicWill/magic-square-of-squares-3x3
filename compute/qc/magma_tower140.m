// Entry 140: the genus-2 endpoint curves -- twisted and untwisted -- shared by the (2,1,1) and (3,1,1) classes that stay open on
// every frame of the twisted all-frames sweep, ranked by the number of classes that meet them.  Paste ONE block at a time into
// the Magma calculator (120 s limit).  A decided curve (rank 0, or rank 1 with the group proved or its index certified, Chabauty)
// joins KNOWN_GENUS2 of compute/symmetry_tower.py and kills through the fibers; a twisted curve's points bound the admissible
// (or all rational) points of every class that meets it.
// ===== block A: y^2 = (1)*x^6 + (-90)*x^5 + (4367)*x^4 + (-940)*x^3 + (-1009)*x^2 + (294)*x^1 + (1)
// (16 open classes meet this curve on some frame, 0 of the occurrences through a twisted model; min disc 10078984 = [2, 3; 1259873, 1]; PARI points to 10^4: [[-1, 64], [-1, -64], [0, 1], [0, -1], [1/3, 64/27], [1/3, -64/27]])
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

// ===== block B: y^2 = (1)*x^6 + (-184)*x^5 + (17904)*x^4 + (-8448)*x^3 + (-57600)*x^2 + (51200)*x^1 + (4096)
// (8 open classes meet this curve on some frame, 0 of the occurrences through a twisted model; min disc 21218784 = [2, 5; 3, 1; 83, 1; 2663, 1]; PARI points to 10^4: [[-4, 2048], [-4, -2048], [0, 64], [0, -64], [8, 7744], [8, -7744], [4/3, 2048/27], [4/3, -2048/27], [12/5, 63488/125], [12/5, -63488/125], [-268/27, 274548736/19683], [-268/27, -274548736/19683], [20/51, 16369664/132651], [20/51, -16369664/132651]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (-184)*x^5 + (17904)*x^4 + (-8448)*x^3 + (-57600)*x^2 + (51200)*x^1 + (4096));
J := Jacobian(C);
print "block B: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block C: y^2 = (1)*x^6 + (200)*x^5 + (-3600)*x^4 + (-8448)*x^3 + (286464)*x^2 + (-47104)*x^1 + (4096)
// (8 open classes meet this curve on some frame, 0 of the occurrences through a twisted model; min disc 21218784 = [2, 5; 3, 1; 83, 1; 2663, 1]; PARI points to 10^4: [[-4, 2048], [-4, -2048], [0, 64], [0, -64], [2, 968], [2, -968], [12, 2048], [12, -2048], [20/3, 63488/27], [20/3, -63488/27], [204/5, 16369664/125], [204/5, -16369664/125], [-108/67, 274548736/300763], [-108/67, -274548736/300763]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^6 + (200)*x^5 + (-3600)*x^4 + (-8448)*x^3 + (286464)*x^2 + (-47104)*x^1 + (4096));
J := Jacobian(C);
print "block C: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block D: y^2 = (25)*x^5 + (-656)*x^4 + (3808)*x^3 + (11008)*x^2 + (256)*x^1
// (8 open classes meet this curve on some frame, 16 of the occurrences through a twisted model; min disc -1355284480000 = [2, 22; 5, 4; 11, 1; 47, 1]; PARI points to 10^4: [[0, 0]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((25)*x^5 + (-656)*x^4 + (3808)*x^3 + (11008)*x^2 + (256)*x^1);
J := Jacobian(C);
print "block D: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block E: y^2 = (25)*x^5 + (-556)*x^4 + (1184)*x^3 + (26240)*x^2 + (44288)*x^1 + (1024)
// (8 open classes meet this curve on some frame, 16 of the occurrences through a twisted model; min disc -84705280000 = [2, 18; 5, 4; 11, 1; 47, 1]; PARI points to 10^4: [[-4, 0], [0, 32], [0, -32], [12, 1024], [12, -1024]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((25)*x^5 + (-556)*x^4 + (1184)*x^3 + (26240)*x^2 + (44288)*x^1 + (1024));
J := Jacobian(C);
print "block E: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block F: y^2 = (25)*x^6 + (-556)*x^5 + (1184)*x^4 + (26240)*x^3 + (44288)*x^2 + (1024)*x^1
// (8 open classes meet this curve on some frame, 16 of the occurrences through a twisted model; min disc -135528448 = [2, 18; 11, 1; 47, 1]; PARI points to 10^4: [[0, 0], [-4, 0], [4/3, 10240/27], [4/3, -10240/27]])
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((25)*x^6 + (-556)*x^5 + (1184)*x^4 + (26240)*x^3 + (44288)*x^2 + (1024)*x^1);
J := Jacobian(C);
print "block F: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;
