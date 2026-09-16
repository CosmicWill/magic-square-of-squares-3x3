// NOTE (entry 142): this script was NOT run.  The Prym test it prepares was carried out locally in SageMath instead
// (compute/qc/prym_test.sage; results in compute/data_prym_test_142.json): the function-field place counts give the same
// L-polynomials at a fraction of the calculator's cost, and the identification of the twelve blocks of magma_tower142.m with
// four curves is a consequence of the group structure.  Kept as the Magma equivalent for anyone wishing to cross-check.
// Entry 142 (prepared), follow-up of magma_tower142b.m.  A2 and B2 have simple Jacobians (irreducible L-polynomials at good
// primes).  Three things remain, one block at a time: (1) the full quotients of families C and D (blocks C2L, D2L: the
// L-polynomials only); (2) the identification of the other eight curves of magma_tower142.m with A2/B2/C2/D2 (block ID:
// the L-polynomials at p = 13, 17 -- the full quotient by the group {1, joint, diag(1,1), diag(-1,-1)} is one curve however
// it is computed, and the sign classes of a family share it); (3) the PRYM TEST: J(component) x J(full)^2 ~ product of the
// Jacobians of the three index-2 quotients (Kani-Rosen), so an elliptic or genus-2 factor of the component's Jacobian that
// the full quotient does not see must appear as a factor of degree <= 4 of the L-polynomial of one of them.  Blocks P*.

// ===== block C2L: the full quotient of family C (block C2 of magma_tower142.m), L-polynomials only
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (64)*X^0*Y^4 + (256)*X^1*Y^2 + (640)*X^1*Y^3 + (-208)*X^1*Y^4 + (2560)*X^2*Y^1 + (-4352)*X^2*Y^2 + (-1824)*X^2*Y^3 + (140)*X^2*Y^4 + (-30464)*X^3*Y^0 + (-23680)*X^3*Y^1 + (-1056)*X^3*Y^2 + (504)*X^3*Y^3 + (-15)*X^3*Y^4 + (18112)*X^4*Y^0 + (6112)*X^4*Y^1 + (-464)*X^4*Y^2 + (-6)*X^4*Y^3 + (-2640)*X^5*Y^0 + (-24)*X^5*Y^1 + (9)*X^5*Y^2 + (36)*X^6*Y^0);
print "block C2L: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block D2L: the full quotient of family D (block D2 of magma_tower142.m), L-polynomials only
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (576)*X^0*Y^4 + (2304)*X^1*Y^2 + (-384)*X^1*Y^3 + (-2640)*X^1*Y^4 + (-1536)*X^2*Y^1 + (-7424)*X^2*Y^2 + (6112)*X^2*Y^3 + (1132)*X^2*Y^4 + (-3840)*X^3*Y^0 + (8064)*X^3*Y^1 + (-1056)*X^3*Y^2 + (-1480)*X^3*Y^3 + (-119)*X^3*Y^4 + (2240)*X^4*Y^0 + (-1824)*X^4*Y^1 + (-272)*X^4*Y^2 + (10)*X^4*Y^3 + (-208)*X^5*Y^0 + (40)*X^5*Y^1 + (1)*X^5*Y^2 + (4)*X^6*Y^0);
print "block D2L: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block ID: the eight other curves of magma_tower142.m at p = 13 and 17 (expected: E2 = F2 = G2 = H2 = A2 and I2 = J2 = B2, K2 = C2, L2 = D2)
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^3 + (131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (17408)*X^1*Y^3 + (-65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (-2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (10240)*X^3*Y^1 + (608)*X^3*Y^2 + (119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (-512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block ID E2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (36864)*X^0*Y^3 + (-131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (-17408)*X^1*Y^3 + (65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (-10240)*X^3*Y^1 + (608)*X^3*Y^2 + (-119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block ID F2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (37760)*U2^0*V2^0 + (4944)*U2^0*V2^1 + (-29568)*U2^0*V2^2 + (-11336)*U2^0*V2^3 + (-7952)*U2^1*V2^0 + (14672)*U2^1*V2^1 + (26024)*U2^1*V2^2 + (8596)*U2^1*V2^3 + (-7760)*U2^2*V2^0 + (-14592)*U2^2*V2^1 + (-8260)*U2^2*V2^2 + (-1846)*U2^2*V2^3 + (4992)*U2^3*V2^0 + (3500)*U2^3*V2^1 + (958)*U2^3*V2^2 + (119)*U2^3*V2^3 + (-868)*U2^4*V2^0 + (-245)*U2^4*V2^1 + (-35)*U2^4*V2^2 + (49)*U2^5*V2^0);
print "block ID G2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-6816)*U2^0*V2^0 + (11952)*U2^0*V2^1 + (28752)*U2^0*V2^2 + (11336)*U2^0*V2^3 + (8672)*U2^1*V2^0 + (-21328)*U2^1*V2^1 + (-29064)*U2^1*V2^2 + (-8596)*U2^1*V2^3 + (6848)*U2^2*V2^0 + (11008)*U2^2*V2^1 + (7740)*U2^2*V2^2 + (1846)*U2^2*V2^3 + (-3064)*U2^3*V2^0 + (-1836)*U2^3*V2^1 + (-630)*U2^3*V2^2 + (-119)*U2^3*V2^3 + (314)*U2^4*V2^0 + (85)*U2^4*V2^1);
print "block ID H2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (-4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (-6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (-12)*X^4*Y^3 + (2048)*X^5*Y^0 + (144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block ID I2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (-57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (-608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (12)*X^4*Y^3 + (2048)*X^5*Y^0 + (-144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block ID J2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-65536)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (28672)*X^3*Y^1 + (-7424)*X^3*Y^2 + (-672)*X^3*Y^3 + (15)*X^3*Y^4 + (-4096)*X^4*Y^0 + (-3840)*X^4*Y^1 + (32)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (192)*X^5*Y^1 + (9)*X^5*Y^2);
print "block ID K2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^4 + (131072)*X^1*Y^2 + (-16384)*X^1*Y^3 + (17408)*X^1*Y^4 + (65536)*X^2*Y^1 + (-61440)*X^2*Y^2 + (7424)*X^2*Y^3 + (-2560)*X^2*Y^4 + (-28672)*X^3*Y^1 + (9984)*X^3*Y^2 + (-928)*X^3*Y^3 + (119)*X^3*Y^4 + (-4096)*X^4*Y^0 + (3328)*X^4*Y^1 + (-672)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (-64)*X^5*Y^1 + (1)*X^5*Y^2);
print "block ID L2: genus", Genus(C);
for p in [13, 17] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PA-joint: the joint quotient (index 2) of the (7, 3) component of class 69319 frame 2 (family A: members [[69319, 2], [69321, 2], [70010, 2], [70011, 2]])
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-7)*X^5*Y^0 + (5)*X^4*Y^2 + (35)*X^4*Y^1 + (67)*X^4*Y^0 + (-17)*X^3*Y^3 + (-89)*X^3*Y^2 + (-191)*X^3*Y^1 + (-101)*X^3*Y^0 + (101)*X^2*Y^3 + (191)*X^2*Y^2 + (89)*X^2*Y^1 + (17)*X^2*Y^0 + (-67)*X^1*Y^3 + (-35)*X^1*Y^2 + (-5)*X^1*Y^1 + (7)*X^0*Y^3);
print "block PA-joint: genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PA-diag(1,1): the diag(1,1) quotient (index 2) of the (7, 3) component of class 69319 frame 2 (family A: members [[69319, 2], [69321, 2], [70010, 2], [70011, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (35)*U^7*V^2 + (-144)*U^7*V^0 + (-119)*U^6*V^3 + (512)*U^6*V^1 + (-608)*U^5*V^2 + (2048)*U^5*V^0 + (2560)*U^4*V^3 + (-10240)*U^4*V^1 + (3328)*U^3*V^2 + (-8192)*U^3*V^0 + (-17408)*U^2*V^3 + (65536)*U^2*V^1 + (-4096)*U^1*V^2 + (36864)*U^0*V^3 + (-131072)*U^0*V^1);
print "block PA-diag(1,1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PA-diag(-1,-1): the diag(-1,-1) quotient (index 2) of the (7, 3) component of class 69319 frame 2 (family A: members [[69319, 2], [69321, 2], [70010, 2], [70011, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (35)*U^7*V^2 + (-4)*U^7*V^0 + (-119)*U^6*V^3 + (148)*U^6*V^1 + (-1308)*U^5*V^2 + (208)*U^5*V^0 + (1132)*U^4*V^3 + (-3344)*U^4*V^1 + (7312)*U^3*V^2 + (-2240)*U^3*V^0 + (-2640)*U^2*V^3 + (11200)*U^2*V^1 + (-9024)*U^1*V^2 + (3840)*U^1*V^0 + (576)*U^0*V^3 + (-6912)*U^0*V^1);
print "block PA-diag(-1,-1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PB-joint: the joint quotient (index 2) of the (8, 4) component of class 69318 frame 2 (family B: members [[69318, 2], [69320, 2], [70012, 2], [70013, 2]])
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-1)*X^5*Y^1 + (-5)*X^5*Y^0 + (3)*X^4*Y^3 + (56)*X^4*Y^2 + (90)*X^4*Y^1 + (25)*X^4*Y^0 + (-3)*X^3*Y^4 + (-150)*X^3*Y^3 + (-392)*X^3*Y^2 + (-268)*X^3*Y^1 + (-31)*X^3*Y^0 + (31)*X^2*Y^4 + (268)*X^2*Y^3 + (392)*X^2*Y^2 + (150)*X^2*Y^1 + (3)*X^2*Y^0 + (-25)*X^1*Y^4 + (-90)*X^1*Y^3 + (-56)*X^1*Y^2 + (-3)*X^1*Y^1 + (5)*X^0*Y^4 + (1)*X^0*Y^3);
print "block PB-joint: genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PB-diag(1,1): the diag(1,1) quotient (index 2) of the (8, 4) component of class 69318 frame 2 (family B: members [[69318, 2], [69320, 2], [70012, 2], [70013, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (3)*U^8*V^2 + (-16)*U^8*V^0 + (12)*U^7*V^3 + (-144)*U^7*V^1 + (-15)*U^6*V^4 + (64)*U^6*V^2 + (-2048)*U^6*V^0 + (-608)*U^5*V^3 + (6656)*U^5*V^1 + (320)*U^4*V^4 + (6912)*U^4*V^2 + (8192)*U^4*V^0 + (4352)*U^3*V^3 + (-57344)*U^3*V^1 + (-2048)*U^2*V^4 + (-61440)*U^2*V^2 + (-8192)*U^1*V^3 + (131072)*U^1*V^1 + (4096)*U^0*V^4 + (131072)*U^0*V^2);
print "block PB-diag(1,1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PB-diag(-1,-1): the diag(-1,-1) quotient (index 2) of the (8, 4) component of class 69318 frame 2 (family B: members [[69318, 2], [69320, 2], [70012, 2], [70013, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (3)*U^8*V^2 + (-4)*U^8*V^0 + (-18)*U^7*V^3 + (184)*U^7*V^1 + (15)*U^6*V^4 + (-784)*U^6*V^2 + (2512)*U^6*V^0 + (1000)*U^5*V^3 + (-11360)*U^5*V^1 + (-140)*U^4*V^4 + (15136)*U^4*V^2 + (-20672)*U^4*V^0 + (-3424)*U^3*V^3 + (47744)*U^3*V^1 + (208)*U^2*V^4 + (-16640)*U^2*V^2 + (24320)*U^2*V^0 + (1920)*U^1*V^3 + (-8704)*U^1*V^1 + (-64)*U^0*V^4 + (768)*U^0*V^2);
print "block PB-diag(-1,-1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PC-joint: the joint quotient (index 2) of the (8, 4) component of class 75216 frame 1 (family C: members [[75216, 1], [75218, 1], [75547, 2], [75548, 2]])
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (3)*X^5*Y^1 + (5)*X^5*Y^0 + (3)*X^4*Y^3 + (40)*X^4*Y^2 + (38)*X^4*Y^1 + (-25)*X^4*Y^0 + (3)*X^3*Y^4 + (-90)*X^3*Y^3 + (-280)*X^3*Y^2 + (-128)*X^3*Y^1 + (31)*X^3*Y^0 + (-31)*X^2*Y^4 + (128)*X^2*Y^3 + (280)*X^2*Y^2 + (90)*X^2*Y^1 + (-3)*X^2*Y^0 + (25)*X^1*Y^4 + (-38)*X^1*Y^3 + (-40)*X^1*Y^2 + (-3)*X^1*Y^1 + (-5)*X^0*Y^4 + (-3)*X^0*Y^3);
print "block PC-joint: genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PC-diag(1,1): the diag(1,1) quotient (index 2) of the (8, 4) component of class 75216 frame 1 (family C: members [[75216, 1], [75218, 1], [75547, 2], [75548, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (9)*U^8*V^2 + (24)*U^7*V^3 + (192)*U^7*V^1 + (15)*U^6*V^4 + (32)*U^6*V^2 + (1024)*U^6*V^0 + (-672)*U^5*V^3 + (-3840)*U^5*V^1 + (-320)*U^4*V^4 + (-7424)*U^4*V^2 + (-4096)*U^4*V^0 + (4352)*U^3*V^3 + (28672)*U^3*V^1 + (2048)*U^2*V^4 + (61440)*U^2*V^2 + (-8192)*U^1*V^3 + (-65536)*U^1*V^1 + (-4096)*U^0*V^4 + (-131072)*U^0*V^2);
print "block PC-diag(1,1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PC-diag(-1,-1): the diag(-1,-1) quotient (index 2) of the (8, 4) component of class 75216 frame 1 (family C: members [[75216, 1], [75218, 1], [75547, 2], [75548, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (9)*U^8*V^2 + (36)*U^8*V^0 + (-6)*U^7*V^3 + (-24)*U^7*V^1 + (-15)*U^6*V^4 + (-464)*U^6*V^2 + (-2640)*U^6*V^0 + (504)*U^5*V^3 + (6112)*U^5*V^1 + (140)*U^4*V^4 + (-1056)*U^4*V^2 + (18112)*U^4*V^0 + (-1824)*U^3*V^3 + (-23680)*U^3*V^1 + (-208)*U^2*V^4 + (-4352)*U^2*V^2 + (-30464)*U^2*V^0 + (640)*U^1*V^3 + (2560)*U^1*V^1 + (64)*U^0*V^4 + (256)*U^0*V^2);
print "block PC-diag(-1,-1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PD-joint: the joint quotient (index 2) of the (8, 4) component of class 75217 frame 1 (family D: members [[75217, 1], [75219, 1], [75549, 2], [75550, 2]])
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (1)*X^5*Y^1 + (7)*X^5*Y^0 + (1)*X^4*Y^3 + (-8)*X^4*Y^2 + (-62)*X^4*Y^1 + (-67)*X^4*Y^0 + (17)*X^3*Y^4 + (66)*X^3*Y^3 + (56)*X^3*Y^2 + (128)*X^3*Y^1 + (101)*X^3*Y^0 + (-101)*X^2*Y^4 + (-128)*X^2*Y^3 + (-56)*X^2*Y^2 + (-66)*X^2*Y^1 + (-17)*X^2*Y^0 + (67)*X^1*Y^4 + (62)*X^1*Y^3 + (8)*X^1*Y^2 + (-1)*X^1*Y^1 + (-7)*X^0*Y^4 + (-1)*X^0*Y^3);
print "block PD-joint: genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PD-diag(1,1): the diag(1,1) quotient (index 2) of the (8, 4) component of class 75217 frame 1 (family D: members [[75217, 1], [75219, 1], [75549, 2], [75550, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (1)*U^8*V^2 + (24)*U^7*V^3 + (-64)*U^7*V^1 + (119)*U^6*V^4 + (-672)*U^6*V^2 + (1024)*U^6*V^0 + (-928)*U^5*V^3 + (3328)*U^5*V^1 + (-2560)*U^4*V^4 + (9984)*U^4*V^2 + (-4096)*U^4*V^0 + (7424)*U^3*V^3 + (-28672)*U^3*V^1 + (17408)*U^2*V^4 + (-61440)*U^2*V^2 + (-16384)*U^1*V^3 + (65536)*U^1*V^1 + (-36864)*U^0*V^4 + (131072)*U^0*V^2);
print "block PD-diag(1,1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;


// ===== block PD-diag(-1,-1): the diag(-1,-1) quotient (index 2) of the (8, 4) component of class 75217 frame 1 (family D: members [[75217, 1], [75219, 1], [75549, 2], [75550, 2]])
A2<U,V> := AffineSpace(Rationals(), 2);
C := Curve(A2, (1)*U^8*V^2 + (4)*U^8*V^0 + (10)*U^7*V^3 + (40)*U^7*V^1 + (-119)*U^6*V^4 + (-272)*U^6*V^2 + (-208)*U^6*V^0 + (-1480)*U^5*V^3 + (-1824)*U^5*V^1 + (1132)*U^4*V^4 + (-1056)*U^4*V^2 + (2240)*U^4*V^0 + (6112)*U^3*V^3 + (8064)*U^3*V^1 + (-2640)*U^2*V^4 + (-7424)*U^2*V^2 + (-3840)*U^2*V^0 + (-384)*U^1*V^3 + (-1536)*U^1*V^1 + (576)*U^0*V^4 + (2304)*U^0*V^2);
print "block PD-diag(-1,-1): genus", Genus(C);
for p in [3, 5, 7, 11, 13] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": factor degrees", [<Degree(t[1]), t[2]> : t in Factorization(L)], "L =", L;
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;

