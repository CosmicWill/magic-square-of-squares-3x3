// Entry 142 (prepared), follow-up of magma_tower142.m: all twelve full-quotient curves are non-hyperelliptic (genus 3: plane quartics;
// genus 4: canonical curves).  Two questions the calculator can still answer, one block at a time (120 s limit): does the Jacobian
// split (an elliptic factor shows as a degree-2 factor of the L-polynomial at every good prime), and does the curve have automorphisms
// beyond the monomial ones (an involution gives a lower-genus quotient)?  Either would give a map to a curve the tower can decide.
// ===== block A2: the same curve as block A of magma_tower142.m (diag(-1,-1)_then_joint of the (7,3) components; member classes [[69319, 2], [69321, 2], [70010, 2], [70011, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-576)*X^0*Y^3 + (6912)*X^1*Y^1 + (9024)*X^1*Y^2 + (2640)*X^1*Y^3 + (-3840)*X^2*Y^0 + (-11200)*X^2*Y^1 + (-7312)*X^2*Y^2 + (-1132)*X^2*Y^3 + (2240)*X^3*Y^0 + (3344)*X^3*Y^1 + (1308)*X^3*Y^2 + (119)*X^3*Y^3 + (-208)*X^4*Y^0 + (-148)*X^4*Y^1 + (-35)*X^4*Y^2 + (4)*X^5*Y^0);
print "block A2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block B2: the same curve as block B of magma_tower142.m (diag(-1,-1)_then_joint of the (8,4) components; member classes [[69318, 2], [69320, 2], [70012, 2], [70013, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (64)*X^0*Y^4 + (-768)*X^1*Y^2 + (-1920)*X^1*Y^3 + (-208)*X^1*Y^4 + (8704)*X^2*Y^1 + (16640)*X^2*Y^2 + (3424)*X^2*Y^3 + (140)*X^2*Y^4 + (-24320)*X^3*Y^0 + (-47744)*X^3*Y^1 + (-15136)*X^3*Y^2 + (-1000)*X^3*Y^3 + (-15)*X^3*Y^4 + (20672)*X^4*Y^0 + (11360)*X^4*Y^1 + (784)*X^4*Y^2 + (18)*X^4*Y^3 + (-2512)*X^5*Y^0 + (-184)*X^5*Y^1 + (-3)*X^5*Y^2 + (4)*X^6*Y^0);
print "block B2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block C2: the same curve as block C of magma_tower142.m (diag(-1,-1)_then_joint of the (8,4) components; member classes [[75216, 1], [75218, 1], [75547, 2], [75548, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (64)*X^0*Y^4 + (256)*X^1*Y^2 + (640)*X^1*Y^3 + (-208)*X^1*Y^4 + (2560)*X^2*Y^1 + (-4352)*X^2*Y^2 + (-1824)*X^2*Y^3 + (140)*X^2*Y^4 + (-30464)*X^3*Y^0 + (-23680)*X^3*Y^1 + (-1056)*X^3*Y^2 + (504)*X^3*Y^3 + (-15)*X^3*Y^4 + (18112)*X^4*Y^0 + (6112)*X^4*Y^1 + (-464)*X^4*Y^2 + (-6)*X^4*Y^3 + (-2640)*X^5*Y^0 + (-24)*X^5*Y^1 + (9)*X^5*Y^2 + (36)*X^6*Y^0);
print "block C2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block D2: the same curve as block D of magma_tower142.m (diag(-1,-1)_then_joint of the (8,4) components; member classes [[75217, 1], [75219, 1], [75549, 2], [75550, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (576)*X^0*Y^4 + (2304)*X^1*Y^2 + (-384)*X^1*Y^3 + (-2640)*X^1*Y^4 + (-1536)*X^2*Y^1 + (-7424)*X^2*Y^2 + (6112)*X^2*Y^3 + (1132)*X^2*Y^4 + (-3840)*X^3*Y^0 + (8064)*X^3*Y^1 + (-1056)*X^3*Y^2 + (-1480)*X^3*Y^3 + (-119)*X^3*Y^4 + (2240)*X^4*Y^0 + (-1824)*X^4*Y^1 + (-272)*X^4*Y^2 + (10)*X^4*Y^3 + (-208)*X^5*Y^0 + (40)*X^5*Y^1 + (1)*X^5*Y^2 + (4)*X^6*Y^0);
print "block D2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block E2: the same curve as block E of magma_tower142.m (diag(1,1)_then_joint of the (7,3) components; member classes [[69319, 2], [70010, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^3 + (131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (17408)*X^1*Y^3 + (-65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (-2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (10240)*X^3*Y^1 + (608)*X^3*Y^2 + (119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (-512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block E2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block F2: the same curve as block F of magma_tower142.m (diag(1,1)_then_joint of the (7,3) components; member classes [[69321, 2], [70011, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (36864)*X^0*Y^3 + (-131072)*X^1*Y^1 + (4096)*X^1*Y^2 + (-17408)*X^1*Y^3 + (65536)*X^2*Y^1 + (-3328)*X^2*Y^2 + (2560)*X^2*Y^3 + (8192)*X^3*Y^0 + (-10240)*X^3*Y^1 + (608)*X^3*Y^2 + (-119)*X^3*Y^3 + (-2048)*X^4*Y^0 + (512)*X^4*Y^1 + (-35)*X^4*Y^2 + (144)*X^5*Y^0);
print "block F2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block G2: the same curve as block G of magma_tower142.m (joint_then_diag(1,1) of the (7,3) components; member classes [[69319, 2], [70010, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (37760)*U2^0*V2^0 + (4944)*U2^0*V2^1 + (-29568)*U2^0*V2^2 + (-11336)*U2^0*V2^3 + (-7952)*U2^1*V2^0 + (14672)*U2^1*V2^1 + (26024)*U2^1*V2^2 + (8596)*U2^1*V2^3 + (-7760)*U2^2*V2^0 + (-14592)*U2^2*V2^1 + (-8260)*U2^2*V2^2 + (-1846)*U2^2*V2^3 + (4992)*U2^3*V2^0 + (3500)*U2^3*V2^1 + (958)*U2^3*V2^2 + (119)*U2^3*V2^3 + (-868)*U2^4*V2^0 + (-245)*U2^4*V2^1 + (-35)*U2^4*V2^2 + (49)*U2^5*V2^0);
print "block G2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block H2: the same curve as block H of magma_tower142.m (joint_then_diag(1,1) of the (7,3) components; member classes [[69321, 2], [70011, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<U2,V2> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-6816)*U2^0*V2^0 + (11952)*U2^0*V2^1 + (28752)*U2^0*V2^2 + (11336)*U2^0*V2^3 + (8672)*U2^1*V2^0 + (-21328)*U2^1*V2^1 + (-29064)*U2^1*V2^2 + (-8596)*U2^1*V2^3 + (6848)*U2^2*V2^0 + (11008)*U2^2*V2^1 + (7740)*U2^2*V2^2 + (1846)*U2^2*V2^3 + (-3064)*U2^3*V2^0 + (-1836)*U2^3*V2^1 + (-630)*U2^3*V2^2 + (-119)*U2^3*V2^3 + (314)*U2^4*V2^0 + (85)*U2^4*V2^1);
print "block H2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block I2: the same curve as block I of magma_tower142.m (diag(1,1)_then_joint of the (8,4) components; member classes [[69318, 2], [70012, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (-4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (-6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (-12)*X^4*Y^3 + (2048)*X^5*Y^0 + (144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block I2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block J2: the same curve as block J of magma_tower142.m (diag(1,1)_then_joint of the (8,4) components; member classes [[69320, 2], [70013, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (131072)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (-57344)*X^3*Y^1 + (-6912)*X^3*Y^2 + (-608)*X^3*Y^3 + (15)*X^3*Y^4 + (-8192)*X^4*Y^0 + (6656)*X^4*Y^1 + (-64)*X^4*Y^2 + (12)*X^4*Y^3 + (2048)*X^5*Y^0 + (-144)*X^5*Y^1 + (-3)*X^5*Y^2 + (16)*X^6*Y^0);
print "block J2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block K2: the same curve as block K of magma_tower142.m (diag(1,1)_then_joint of the (8,4) components; member classes [[75216, 1], [75547, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-4096)*X^0*Y^4 + (-131072)*X^1*Y^2 + (-8192)*X^1*Y^3 + (2048)*X^1*Y^4 + (-65536)*X^2*Y^1 + (61440)*X^2*Y^2 + (4352)*X^2*Y^3 + (-320)*X^2*Y^4 + (28672)*X^3*Y^1 + (-7424)*X^3*Y^2 + (-672)*X^3*Y^3 + (15)*X^3*Y^4 + (-4096)*X^4*Y^0 + (-3840)*X^4*Y^1 + (32)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (192)*X^5*Y^1 + (9)*X^5*Y^2);
print "block K2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;

// ===== block L2: the same curve as block L of magma_tower142.m (diag(1,1)_then_joint of the (8,4) components; member classes [[75217, 1], [75549, 2]])
// (i) the L-polynomials at small good primes, factored: a repeated linear-times-quadratic pattern (a degree-2 factor at every prime)
//     means an elliptic factor of the Jacobian; (ii) the automorphism group and the genera of the quotients by its involutions.
A2<X,Y> := AffineSpace(Rationals(), 2);
C := Curve(A2, (-36864)*X^0*Y^4 + (131072)*X^1*Y^2 + (-16384)*X^1*Y^3 + (17408)*X^1*Y^4 + (65536)*X^2*Y^1 + (-61440)*X^2*Y^2 + (7424)*X^2*Y^3 + (-2560)*X^2*Y^4 + (-28672)*X^3*Y^1 + (9984)*X^3*Y^2 + (-928)*X^3*Y^3 + (119)*X^3*Y^4 + (-4096)*X^4*Y^0 + (3328)*X^4*Y^1 + (-672)*X^4*Y^2 + (24)*X^4*Y^3 + (1024)*X^5*Y^0 + (-64)*X^5*Y^1 + (1)*X^5*Y^2);
print "block L2: genus", Genus(C);
for p in [3, 5, 7, 11, 13, 17, 19, 23] do
    try
        Cp := ChangeRing(C, GF(p));
        L := LPolynomial(Cp);
        print "p =", p, ": L-polynomial factors", [<Degree(t[1]), t[2]> : t in Factorization(L)];
    catch e
        print "p =", p, ": bad reduction or error";
    end try;
end for;
try
    G, m := AutomorphismGroup(C);
    print "automorphism group order:", #G;
    for gG in G do
        if Order(gG) eq 2 then
            Q, q := CurveQuotient(sub<G | gG>);
            print "   involution: quotient genus", Genus(Q);
        end if;
    end for;
catch e
    print "automorphism group: error", e`Object;
end try;
