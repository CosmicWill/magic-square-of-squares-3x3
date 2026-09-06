// Entry 115 (O2 with Sage): the sixteen finite classes of the (1,1,1) box whose component has a
// genus-0 quotient by t -> -1/t and no further involution all reduce, over Q, to the rational
// points of ONE genus-2 curve
//     C2 : y^2 = (25 s^3 - 61 s^2 + 43 s + 1) (25 s^3 - 29 s^2 + 11 s + 1)
// (discriminant 2^62 5^4 23 83; at least 14 rational points: s in {-3, 0, 1, 1/3, -1/5, 3/5} and
// two at infinity; Frobenius polynomials irreducible at most good primes, so the Jacobian is
// presumably simple with End = Z).  Each class's own model is y^2 = Dt(s) with Dt(s) =
// mu * C2(lambda s) or mu * s^6 C2(lambda / s), mu a square, lambda in {1, 56644, 42025/1849}.
// Every rational point of every one of the sixteen components lifts from a rational point of C2
// (the lift is exact: s = t^2, tg = (N(t) +- y)/(2 M(t)), th = v(t)).  What is needed:
//   (1) RankBound(J): if rank <= 1, Chabauty + Mordell-Weil sieve determines C2(Q) and the
//       sixteen classes are decided by lifting (compute/omega3 records the lifts);
//   (2) if rank = 2 = genus, quadratic Chabauty is out of reach for End(J) = Z; report the rank.
// Runs within the online calculator's limits for RankBound; Chabauty needs a generator P.
P<s> := PolynomialRing(Rationals());
f := (25*s^3 - 61*s^2 + 43*s + 1) * (25*s^3 - 29*s^2 + 11*s + 1);
C := HyperellipticCurve(f);
J := Jacobian(C);
print "genus", Genus(C);
print "discriminant", Factorization(Integers() ! Discriminant(C));
pts := Points(C : Bound := 10000);
print "rational points to height 10000:", #pts, pts;
print "torsion subgroup of J:", TorsionSubgroup(J);
rb := RankBound(J);
print "RankBound(J) =", rb;
if rb le 1 then
    // find a point of infinite order among the differences of the known points
    Ps := [ J ! [pts[i], pts[1]] : i in [2..#pts] ];
    Ps := [ Q : Q in Ps | Order(Q) eq 0 ];
    if #Ps gt 0 then
        print "Chabauty:", Chabauty(Ps[1]);
    else
        print "no point of infinite order found among small points";
    end if;
end if;
