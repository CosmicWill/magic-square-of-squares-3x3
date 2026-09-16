// Entry 143 (prepared 2026-09-15): what the Magma online calculator can still contribute after entry 142.  Everything that is a
// point count, a genus or a quotient now runs locally in Sage (compute/qc/prym_test.sage); the calculator is reserved for the
// three undecided genus-2 curves that still block classes: A139 = A140 (rank 3; 16 classes), D139 = B140 (rank 3; 8 classes),
// I139 = C140 (rank 2 or 3; 8 classes).  E140 and F140 touch no open class any more (their classes died with D140 in entry 141).
// One block at a time (120 s limit).  Paste the whole output back, including error messages.
//
// Blocks L1-L3: the ANALYTIC RANK of each curve (conductor, L-series, functional-equation check, order of vanishing at s = 1) --
// heuristic guidance, not a proof (BSD is not known for these Jacobians): rank 3 > genus leaves no Chabauty method at all, rank 2 =
// genus leaves quadratic Chabauty (research code, a licensed Magma).  Block L3 also compares the Euler factors of D139 and I139.
// Blocks R*: 2-DESCENT RANK BOUNDS for the higher-genus hyperelliptic endpoints (the census of 2026-09-15: 40 (2,1,1) classes have
// a frame whose every component reaches a genus-3 endpoint, 24 (3,1,1) classes a genus-4 one).  A rank bound below the genus makes
// Chabauty-Coleman possible (Magma has it built in only for genus 2; higher genus needs the Balakrishnan-Tuitman package and a
// licensed copy); a rank bound of 0 decides the curve outright (its points are torsion, found by reduction).  RankBound on a
// genus-3/4 Jacobian needs class groups of degree-8/10 fields and may exceed the calculator's limit: report whatever it prints.

// ===== block L1: A139 = A140, rank 3 (proved); analytic rank for the record.  Conductor 1259873 (prime, PARI genus2red).
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 90*x^5 + 4367*x^4 - 940*x^3 - 1009*x^2 + 294*x + 1);
try
    N := Conductor(C); print "block L1 (A139): conductor", N, "=", Factorization(N);
    L := LSeries(C);
    print "functional equation check (should be tiny):", CFENew(L);
    print "analytic rank:", AnalyticRank(L);
catch e
    print "block L1: error", e`Object;
end try;

// ===== block L2: D139 = B140, rank 3 (proved).  Conductor 663087 = 3 * 83 * 2663.
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 184*x^5 + 17904*x^4 - 8448*x^3 - 57600*x^2 + 51200*x + 4096);
try
    N := Conductor(C); print "block L2 (D139/B140): conductor", N, "=", Factorization(N);
    L := LSeries(C);
    print "functional equation check (should be tiny):", CFENew(L);
    print "analytic rank:", AnalyticRank(L);
catch e
    print "block L2: error", e`Object;
end try;

// ===== block L3: I139 = C140, rank 2 or 3.  Conductor 663087 = 3 * 83 * 2663 (the same as D139: are the Jacobians isogenous?).
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 + 200*x^5 - 3600*x^4 - 8448*x^3 + 286464*x^2 - 47104*x + 4096);
try
    N := Conductor(C); print "block L3 (I139/C140): conductor", N, "=", Factorization(N);
    L := LSeries(C);
    print "functional equation check (should be tiny):", CFENew(L);
    print "analytic rank:", AnalyticRank(L);
catch e
    print "block L3: error", e`Object;
end try;
// the Euler factors of D139 and I139 at the first good primes: equal factors at every good prime would mean isogenous Jacobians
// (then rank(I139) = rank(D139) = 3 and I139 is settled as hopeless)
D := HyperellipticCurve(x^6 - 184*x^5 + 17904*x^4 - 8448*x^3 - 57600*x^2 + 51200*x + 4096);
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37] do
    try
        print "p =", p, ": L_p(D139) =", EulerFactor(D, p), " L_p(I139) =", EulerFactor(C, p), " equal:", EulerFactor(D, p) eq EulerFactor(C, p);
    catch e
        print "p =", p, ": error";
    end try;
end for;

// ===== block R1: y^2 = (1)*x^8 + (124)*x^7 + (-1428)*x^6 + (3220)*x^5 + (7614)*x^4 + (-9500)*x^3 + (3516)*x^2 + (-500)*x^1 + (25)  (genus 3; 16 classes of the (2,1,1) box: 39554, 39555, 39560, 39561, 39851, 39853, 39854, 39856 ...; routes e.g. inversion h (s=-1) -> even)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^8 + (124)*x^7 + (-1428)*x^6 + (3220)*x^5 + (7614)*x^4 + (-9500)*x^3 + (3516)*x^2 + (-500)*x^1 + (25));
print "block R1: genus", Genus(C);
print "points of naive height <= 10^4:", Points(C : Bound := 10000);
J := Jacobian(C);
try
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
catch e
    print "RankBounds: error", e`Object;
    try
        ru := RankBound(J); print "rank bound:", ru;
    catch e2
        print "RankBound: error", e2`Object;
    end try;
end try;
try
    print "torsion bound (primes 3..31):", TorsionBound(J, 10);
catch e
    print "TorsionBound: error", e`Object;
end try;

// ===== block R2: y^2 = (1)*x^8 + (-296)*x^7 + (5564)*x^6 + (-20952)*x^5 + (24582)*x^4 + (-11800)*x^3 + (2236)*x^2 + (-104)*x^1 + (1)  (genus 3; 16 classes of the (2,1,1) box: 75056, 75057, 75058, 75059, 75072, 75073, 75074, 75075 ...; routes e.g. inversion h (s=-1) -> even)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^8 + (-296)*x^7 + (5564)*x^6 + (-20952)*x^5 + (24582)*x^4 + (-11800)*x^3 + (2236)*x^2 + (-104)*x^1 + (1));
print "block R2: genus", Genus(C);
print "points of naive height <= 10^4:", Points(C : Bound := 10000);
J := Jacobian(C);
try
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
catch e
    print "RankBounds: error", e`Object;
    try
        ru := RankBound(J); print "rank bound:", ru;
    catch e2
        print "RankBound: error", e2`Object;
    end try;
end try;
try
    print "torsion bound (primes 3..31):", TorsionBound(J, 10);
catch e
    print "TorsionBound: error", e`Object;
end try;

// ===== block R3: y^2 = (1)*x^8 + (-57)*x^6 + (596)*x^4 + (-688)*x^2 + (192)  (genus 3; 8 classes of the (2,1,1) box: 75302, 75303, 75304, 75305, 75559, 75560, 75561, 75562; routes e.g. inversion h (s=-1) -> reciprocal)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^8 + (-57)*x^6 + (596)*x^4 + (-688)*x^2 + (192));
print "block R3: genus", Genus(C);
print "points of naive height <= 10^4:", Points(C : Bound := 10000);
J := Jacobian(C);
try
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
catch e
    print "RankBounds: error", e`Object;
    try
        ru := RankBound(J); print "rank bound:", ru;
    catch e2
        print "RankBound: error", e2`Object;
    end try;
end try;
try
    print "torsion bound (primes 3..31):", TorsionBound(J, 10);
catch e
    print "TorsionBound: error", e`Object;
end try;

// ===== block R4: y^2 = (1)*x^10 + (370)*x^9 + (-11515)*x^8 + (101912)*x^7 + (-125518)*x^6 + (-356820)*x^5 + (684194)*x^4 + (-218728)*x^3 + (26765)*x^2 + (-1358)*x^1 + (25)  (genus 4; 16 classes of the (3,1,1) box: 206786, 206787, 206792, 206793, 207227, 207229, 207230, 207232 ...; routes e.g. inversion h (s=-1) -> even)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^10 + (370)*x^9 + (-11515)*x^8 + (101912)*x^7 + (-125518)*x^6 + (-356820)*x^5 + (684194)*x^4 + (-218728)*x^3 + (26765)*x^2 + (-1358)*x^1 + (25));
print "block R4: genus", Genus(C);
print "points of naive height <= 10^4:", Points(C : Bound := 10000);
J := Jacobian(C);
try
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
catch e
    print "RankBounds: error", e`Object;
    try
        ru := RankBound(J); print "rank bound:", ru;
    catch e2
        print "RankBound: error", e2`Object;
    end try;
end try;
try
    print "torsion bound (primes 3..31):", TorsionBound(J, 10);
catch e
    print "TorsionBound: error", e`Object;
end try;

// ===== block R5: y^2 = (1)*x^10 + (-112)*x^8 + (2400)*x^6 + (-6912)*x^4 + (-3840)*x^2 + (16384)  (genus 4; 8 classes of the (3,1,1) box: 220302, 220303, 220304, 220305, 220306, 220307, 220308, 220309; routes e.g. inversion h (s=-1) -> reciprocal)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve((1)*x^10 + (-112)*x^8 + (2400)*x^6 + (-6912)*x^4 + (-3840)*x^2 + (16384));
print "block R5: genus", Genus(C);
print "points of naive height <= 10^4:", Points(C : Bound := 10000);
J := Jacobian(C);
try
    rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
catch e
    print "RankBounds: error", e`Object;
    try
        ru := RankBound(J); print "rank bound:", ru;
    catch e2
        print "RankBound: error", e2`Object;
    end try;
end try;
try
    print "torsion bound (primes 3..31):", TorsionBound(J, 10);
catch e
    print "TorsionBound: error", e`Object;
end try;

// Blocks G1-G3: R3 and R5 are EVEN polynomials in x, so each splits one level further under x -> -x (the tower applies the classical
// quotients once; this is the second level, to be mechanised if it pays): R3 = x^8 - 57x^6 + 596x^4 - 688x^2 + 192 has the even
// quotient y^2 = f(t), t = x^2, an ELLIPTIC curve of RANK 3 (PARI ellrank: conductor 33424, no torsion -- useless) and the odd
// companion w^2 = t f(t) of genus 2 (block G1); R5 = x^10 - 112x^8 + 2400x^6 - 6912x^4 - 3840x^2 + 16384 has the even quotient
// y^2 = g(t) of genus 2 (block G2, rational points at least at t = 0, 1, 4, 12 and infinity) and the odd companion w^2 = t g(t)
// of genus 2 (block G3).  Every rational point of R3 (resp. R5) maps to a rational point of each piece, so a piece with finitely
// many known points determines the x-coordinates of R3 (resp. R5) up to sign.  The standard genus-2 block: points, rank bounds,
// torsion, and (rank <= 1) the Mordell-Weil group and Chabauty.

// ===== block G1: the odd companion of R3, w^2 = t^5 - 57 t^4 + 596 t^3 - 688 t^2 + 192 t  (genus 2; decides R3, 8 (2,1,1) classes)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^5 - 57*x^4 + 596*x^3 - 688*x^2 + 192*x);
J := Jacobian(C);
print "block G1: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block G2: the even quotient of R5, y^2 = t^5 - 112 t^4 + 2400 t^3 - 6912 t^2 - 3840 t + 16384  (genus 2; with G3 decides R5, 8 (3,1,1) classes)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^5 - 112*x^4 + 2400*x^3 - 6912*x^2 - 3840*x + 16384);
J := Jacobian(C);
print "block G2: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block G3: the odd companion of R5, w^2 = t^6 - 112 t^5 + 2400 t^4 - 6912 t^3 - 3840 t^2 + 16384 t  (genus 2)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 112*x^5 + 2400*x^4 - 6912*x^3 - 3840*x^2 + 16384*x);
J := Jacobian(C);
print "block G3: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;
