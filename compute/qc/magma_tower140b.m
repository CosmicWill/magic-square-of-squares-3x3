// Entry 141 (pending), follow-up of magma_tower140.m.  Paste ONE block at a time (120 s limit).
// With Q(x) = 25x^4 - 656x^3 + 3808x^2 + 11008x + 256 the three new curves are D: y^2 = x Q(x), E: y^2 = (x + 4) Q(x),
// F: y^2 = x (x + 4) Q(x).

// ===== block D2: certify block D's point set.  Chabauty gave {(0,0), oo} with "group proved: false" and index primes {3}; the
// torsion is Z/2 (T = [(0,0) - oo]), so the set is unconditional once neither the generator Q nor Q + T is divisible by 3 in J(Q)
// (if 3 divided the index of <Q> + <T>, some R would have 3R = kQ + eT with 3 not dividing k, and then Q + e'T = 3(k'R - mQ)).
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(25*x^5 - 656*x^4 + 3808*x^3 + 11008*x^2 + 256*x);
J := Jacobian(C);
G, m, rp, gp := MordellWeilGroupGenus2(J);
print "MW group:", G; print "rank proved:", rp, "group proved:", gp;
free := [G.i : i in [1..Ngens(G)] | Order(G.i) eq 0];
tors := [G.i : i in [1..Ngens(G)] | Order(G.i) ne 0];
Q := m(free[1]);
print "generator Q:", Q;
print "Q divisible by 3?", IsDivisibleBy(Q, 3);
for t in tors do
    T := m(t);
    print "torsion point T:", T;
    print "Q + T divisible by 3?", IsDivisibleBy(Q + T, 3);
end for;

// ===== block E2: a sharper rank bound for E through isogenous surfaces (the rank is an isogeny invariant).  If a Richelot-isogenous
// surface is a product of elliptic curves, their ranks give the rank of J(E) exactly; if it is a Jacobian, its own 2-descent
// bound may be sharper.  Errors (no rational quadratic splitting) are caught and printed.
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(25*x^5 - 556*x^4 + 1184*x^3 + 26240*x^2 + 44288*x + 1024);
J := Jacobian(C);
rl, ru := RankBounds(J); print "E: rank bounds:", rl, ru;
print "E: 2-Selmer:", TwoSelmerGroup(J);
try
    S := RichelotIsogenousSurfaces(J);
    print "E: Richelot-isogenous surfaces:", #S;
    for A in S do
        print Type(A), A;
        if Type(A) eq JacHyp then
            al, au := RankBounds(A); print "   rank bounds of the isogenous Jacobian:", al, au;
        elif Type(A) eq List or Type(A) eq SeqEnum then
            for Ec in A do print "   factor:", Ec, " rank bounds:", RankBounds(Ec); end for;
        end if;
    end for;
catch e
    print "E: Richelot failed:", e`Object;
end try;

// ===== block F2: the same for F.
P<x> := PolynomialRing(Rationals());
C := HyperellipticCurve(25*x^6 - 556*x^5 + 1184*x^4 + 26240*x^3 + 44288*x^2 + 1024*x);
J := Jacobian(C);
rl, ru := RankBounds(J); print "F: rank bounds:", rl, ru;
print "F: 2-Selmer:", TwoSelmerGroup(J);
try
    S := RichelotIsogenousSurfaces(J);
    print "F: Richelot-isogenous surfaces:", #S;
    for A in S do
        print Type(A), A;
        if Type(A) eq JacHyp then
            al, au := RankBounds(A); print "   rank bounds of the isogenous Jacobian:", al, au;
        elif Type(A) eq List or Type(A) eq SeqEnum then
            for Ec in A do print "   factor:", Ec, " rank bounds:", RankBounds(Ec); end for;
        end if;
    end for;
catch e
    print "F: Richelot failed:", e`Object;
end try;
