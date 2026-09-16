// Entry 145 (prepared 2026-09-16): the second-level quotient census found one genus-2 curve the tower never reached: T5, the even
// quotient of the rationality twist of R5's reciprocal model, T5: y^2 = (z + 4) G2(z) = z^6 - 108 z^5 + 1952 z^4 + 2688 z^3
// - 31488 z^2 + 1024 z + 65536 (G2 = z^5 - 112 z^4 + 2400 z^3 - 6912 z^2 - 3840 z + 16384, the even quotient of R5).  Conductor
// 14389 (prime), minimal discriminant 2^6 * 14389 = 920896 (inside the LMFDB's range).  Small points: (-4, 0), (0, +-256), (12, +-4096),
// (4/3, +-4096/27) and the two points at infinity.  One block, the standard genus-2 pattern.

// ===== block T5: y^2 = z^6 - 108 z^5 + 1952 z^4 + 2688 z^3 - 31488 z^2 + 1024 z + 65536  (genus 2; the twisted route of R5's eight (3,1,1) classes)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 108*x^5 + 1952*x^4 + 2688*x^3 - 31488*x^2 + 1024*x + 65536);
J := Jacobian(C);
print "block T5: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// The completed census (2026-09-16) found a second family of eight (3,1,1) classes reaching two genus-2 curves at level 3 of the
// classical quotients: U1 through 'inversion h (s=-1) -> even -> reciprocal' and U2 through 'inversion h (s=-1) -> reciprocal ->
// even'.  The standard genus-2 blocks.

// ===== block U1: y^2 = x^6 - 157 x^5 + 5890 x^4 - 70088 x^3 + 351008 x^2 - 764944 x + 600352  (genus 2; eight (3,1,1) classes, level 3)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 157*x^5 + 5890*x^4 - 70088*x^3 + 351008*x^2 - 764944*x + 600352);
J := Jacobian(C);
print "block U1: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block U2: y^2 = x^6 - 145 x^5 + 4380 x^4 - 29088 x^3 + 59520 x^2 - 25856 x + 3072  (genus 2; the same eight classes, level 3)
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(x^6 - 145*x^5 + 4380*x^4 - 29088*x^3 + 59520*x^2 - 25856*x + 3072);
J := Jacobian(C);
print "block U2: points of height <= 10^4:", Points(C : Bound := 10000);
rl, ru := RankBounds(J); print "rank bounds:", rl, ru;
print "torsion:", TorsionSubgroup(J);
if ru le 1 then
    G, m, rp, gp := MordellWeilGroupGenus2(J); print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
    free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
    if #free gt 0 then pts, N := Chabauty(m(free[1])); print "Chabauty: C(Q) =", pts; print "index primes:", N; end if;
end if;

// ===== block U1b: sharpening U1's rank bound (2-Selmer bound 4, points give >= 1 on U2).  Richelot-isogenous Jacobians can have a
// smaller 2-descent bound (the rank is an isogeny invariant); the isomorphism U1 = U2 is tested; the 2-Selmer group's size shown.
P<x> := PolynomialRing(Rationals());
C1 := HyperellipticCurve(x^6 - 157*x^5 + 5890*x^4 - 70088*x^3 + 351008*x^2 - 764944*x + 600352);
C2 := HyperellipticCurve(x^6 - 145*x^5 + 4380*x^4 - 29088*x^3 + 59520*x^2 - 25856*x + 3072);
try
    iso, mp := IsIsomorphic(C1, C2); print "block U1b: U1 isomorphic to U2 over Q:", iso;
catch e
    print "block U1b: IsIsomorphic error", e`Object;
end try;
J := Jacobian(C1);
try
    S, mS := TwoSelmerGroup(J); print "2-Selmer group of J(U1):", S;
catch e
    print "TwoSelmerGroup: error", e`Object;
end try;
try
    R := RichelotIsogenousSurfaces(J); print "Richelot-isogenous surfaces:", #R;
    for A in R do
        print "  surface:", A;
        try
            rl, ru := RankBounds(A); print "  rank bounds of the isogenous Jacobian:", rl, ru;
        catch e2
            print "  RankBounds: error", e2`Object;
        end try;
    end for;
catch e
    print "RichelotIsogenousSurfaces: error", e`Object;
end try;
