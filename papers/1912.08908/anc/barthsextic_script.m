// preamble
SetColumns(0);
SetLogFile("barthsextic.out");
SetEchoInput(true);

//computation of module M^{vv} in reduction 
p:=10000000000000000000000000000000000000883;
k:=GF(p^2);
r:=Sqrt(k!5);
phi:=(1+r)/2;
P3<x,y,z,w>:=ProjectiveSpace(k,3);
F:=4*(phi^2*x^2-y^2)*(phi^2*y^2-z^2)*(phi^2*z^2-x^2)-(1+2*phi)*(x^2+y^2+z^2-w^2)^2*w^2;

R:=Parent(y);
OX:=quo<RModule(R,[0])|[F]>;
v:=[P3.i: i in [1..4]];
K:=FoF(Parent(y));
DP3<Dx,Dy,Dz,Dw>:=PolynomialRing(K,4);
preDX:=quo<RModule(R,[1,1,1,1])|
   [[i eq j select f else 0: i in [1..4]]:j in [1..4],f in [F]] cat
   [[Derivative(f,x): x in v]: f in [F]]>;
I:=[ <1, 2>, <1, 3>, <1, 4>, <2,3>,<2,4>,<3,4>];
MR:=Matrix([v[i[1]]*preDX.i[2]-v[i[2]]*preDX.i[1]: i in I]);
R6:=RModule(R,[2: i in [1..#I]]);
krn:=Kernel(Homomorphism(R6,preDX,MR));
DX,R6toDX:=quo<R6|krn>;
DXbasis:=[P3.i[1]*DP3.i[2]-P3.i[2]*DP3.i[1]:i in I];
T2DX,toT2DX:=TensorProduct(DX,DX);
J:=[<i,j>: i in[j..Rank(DX)], j in [1..Rank(DX)]];
S2DX,T2DXtoS2DX:=quo<T2DX|[toT2DX(DX.j[1],DX.j[2])-toT2DX(DX.j[2],DX.j[1]): j in J]>;
M:=S2DX;
time Md,mp1:=Hom(M,OX);
time Mdd,mp2:=Hom(Md,OX);

//lifting to characteristic 0
K<r5>:=QuadraticField(5);
_<xK>:=PolynomialRing(K);
Ktok:=func< u | a[1]+r*a[2] where a:=Eltseq(u)>;
function lift_coef(kelt)
    _,nm:=RationalReconstruction(Norm(kelt));
    _,tr:=RationalReconstruction(Trace(kelt));
    rts:=Roots(xK^2-tr*xK+nm);
    L:=[r[1]: r in rts | Ktok(r[1]) eq kelt];
    assert #L eq 1;
    return L[1];
end function;
_<X,Y,Z,W>:=PolynomialRing(K,4,"grevlex");
function lift_pol(g)
    G:=Parent(X)!0;
    for t in Terms(g) do
        e:=Exponents(t);
        G+:=lift_coef(Coefficients(t)[1])*PowerProduct([X,Y,Z,W],e);
    end for;
    return G;
end function;

//lifting. We write our results into a separate file, so that we do not have
//to execute this part again.
//we lift the module M to characteristic 0. No problems here: we know the coefficients
//are small enough to recover reliably.
relM:=[[lift_pol(g): g in Eltseq(r)]: r in Relations(M)];
Write("sextic_results.m","K<r5>:=QuadraticField(5);");
Write("sextic_results.m","R<X,Y,Z,W>:=PolynomialRing(K,4);");
Write("sextic_results.m","M_grading:=");
Write("sextic_results.m",Grading(M));
Write("sextic_results.m",";");
Write("sextic_results.m","M_relations:=");
Write("sextic_results.m",relM);
Write("sextic_results.m",";");

//lifting of Md, and store matrix "A" as Md_matrix
relMd:=[[lift_pol(g): g in Eltseq(r)]: r in Relations(Md)];
Write("sextic_results.m","Md_grading:=");
Write("sextic_results.m",Grading(Md));
Write("sextic_results.m",";");
Write("sextic_results.m","Md_relations:=");
Write("sextic_results.m",relMd);
Write("sextic_results.m",";");
Write("sextic_results.m","Md_matrix:=");
Write("sextic_results.m",[[lift_pol(g): g in Eltseq(Matrix(mp1(a)))]: a in Basis(Domain(mp1))]);
Write("sextic_results.m",";");

//lifting of Mdd, and store matrix "B" as Mdd_matrix
relMdd:=[[lift_pol(g): g in Eltseq(r)]: r in Relations(Mdd)];
Write("sextic_results.m","Mdd_grading:=");
Write("sextic_results.m",Grading(Mdd));
Write("sextic_results.m",";");
Write("sextic_results.m","Mdd_relations:=");
Write("sextic_results.m",relMdd);
Write("sextic_results.m",";");
Write("sextic_results.m","Mdd_matrix:=");
Write("sextic_results.m",[[lift_pol(g): g in Eltseq(Matrix(mp2(a)))]: a in Basis(Domain(mp2))]);
Write("sextic_results.m",";");

//the results of the code above are loaded by the command below.
load "sextic_results.m";

//reconstruct modules (in characteristic 0!) from listed data
S2DX:=quo<RModule(R,M_grading)|M_relations>; //this one is guaranteed to be correct
Md:=quo<RModule(R,Md_grading)|Md_relations>;
hatS2DX:=quo<RModule(R,Mdd_grading)|Mdd_relations>;
A:=Md_matrix;
Amat:=Matrix(A);
B:=Mdd_matrix;
Bmat:=Matrix(B);
phi:=(1+r5)/2;
F:=4*(phi^2*X^2-Y^2)*(phi^2*Y^2-Z^2)*(phi^2*Z^2-X^2)-(1+2*phi)*(X^2+Y^2+Z^2-W^2)^2*W^2;
P3:=Proj(R);
B6:=Scheme(P3,F);
SB6:=SingularSubscheme(B6);
sing:=Support(SB6);

//Check that the matrices A and B describe well-defined pairings.
assert forall{ v : v in Relations(Md) | S2DX!Eltseq(Vector(v)*Amat) eq 0 };
assert forall{ v : v in Relations(S2DX) | Md!Eltseq(Vector(v)*Transpose(Amat)) eq 0};
assert forall{v: v in Relations(hatS2DX) | Md!Eltseq(Vector(v)*Bmat) eq 0 };
assert forall{v: v in Relations(Md) | hatS2DX!Eltseq(Vector(v)*Transpose(Bmat)) eq 0};

//check that Mdd is isomorphic to its double dual
OX:=quo<RModule(R,[0])|[F]>;
Mddd:=Hom(hatS2DX,OX);
Mdddd:=Hom(Mddd,OX);
assert HilbertSeries(hatS2DX) eq HilbertSeries(Mdddd);

I:=[ <1, 2>, <1, 3>, <1, 4>, <2,3>,<2,4>,<3,4>];
J:=[<i,j>: i in [j..6], j in [1..6]];

assert Grading(hatS2DX) eq [0,0,0,-1,-1,-1];

L:=[];
//We consider 4 affine patches, with particular representatives of our sheaves chosen.
patches:=[<<3,2,4>,[1,3,6]>,
<<3,2,4>,[3,4,5]>,
<<2,1,3>,[4,5,6]>,
<<2,1,4>,[2,4,6]>];
//we collect the determinants of the matrices we need to invert:
//outside the vanishing of that determinant, the differentials we compute
//are appropriately described (since we multiply by the adjoint rather than by the inverse
//of the matrix, there are no denominators to deal with)
//We also need to consider the plane "at infinity" for each of the chosen
//patches, but in each case, the determinant ends up vanishing there too.
//The vanishing of each of these determinants forms a dimension one subscheme of the surface
//On the complement of the union of these, all four descriptions are valid
Adets:=[];
//we also collect the matrices that describe the differentials. We can take
//pairwise resultants of these to bound the locus in which genus 0 curves can occur.
//Each C is a 6x3 matrix. Each row contains the coefficients for
//(du)^2, du*dv, (dv)^2, where u,v are local parameters
//the rows 4,5,6 correspond to the weight -1 generators of the module. Those are the ones
//we can use to make regular symmetric differentials that vanish on an arbitrary hyperplane section.
Cs:=[];
for p in patches do
    //p0 is the index of the variable determining the affine patch, so Y=1 corresponds to p0=2
    //p1,p2 are the indices of the variables that are taken to be local parameters.
    p0,p1,p2:=Explode(p[1]);
    //we need to select three rows from the matrix A in order to get a square matrix.
    //this selection is relatively arbitrary.
    rowsel:=p[2];
    i1:=(p0 lt p1) select Index(I,<p0,p1>) else Index(I,<p1,p0>);
    i2:=(p0 lt p2) select Index(I,<p0,p2>) else Index(I,<p2,p0>);
    if i2 gt i1 then
        i1,i2:=Explode(<i2,i1>);
    end if;
    j1:=Index(J,<i1,i1>);
    j2:=Index(J,<i1,i2>);
    j3:=Index(J,<i2,i2>);
    Jsel:=[j1,j2,j3];
    Aprime:=Matrix([a[Jsel]: a in A[rowsel]]);
    Bprime:=Matrix([b[rowsel]: b in B]);
    C:=Bprime*Adjoint(Transpose(Aprime));
    Append(~Adets,Determinant(Aprime));
    Append(~Cs,C);
end for;

function sylvester(v,w)
    return Determinant(Matrix([Eltseq(v) cat [0], [0] cat Eltseq(v), Eltseq(w) cat [0], [0] cat Eltseq(w)]));
end function;

//this is the locus where all the resultants that we consider vanish. It turns out to be a 0-dimensional
//locus, meaning that any of the genus 0 or 1 curves that we know are bounded by the kind of differentials
//we consider, must lie in the locus of vanishing of one of the determinants we collected.
locs:=[Scheme(B6,[sylvester(C[4],C[5]),sylvester(C[4],C[6]),sylvester(C[5],C[6])]) : C in Cs];
locus:=&meet locs;

//For some computations working directly in characteristic 0 is infeasible.
//instead, we work modulo a (large) prime and use rational reconstruction to lift our results back.
//We generally need some verification to check that our computation is correct.
//some other results can be derived directly from the reduction. In those cases we would end up with
//results faster by using a smaller prime (and one where 5 is a square).
p:=10000000000000000000000000000000000000883;
Fq:=GF(p^2);
red:=hom<K->Fq| Bang(Rationals(),Fq),Sqrt(Fq!(5))>;
P3Fq:=ProjectiveSpace(Fq,3);
redR:=hom<CoordinateRing(P3)->CoordinateRing(P3Fq) | red, [P3Fq.i: i in [1..4]]>;

_<xK>:=PolynomialRing(K);
function lift_coef(kelt)
    _,nm:=RationalReconstruction(Norm(kelt));
    _,tr:=RationalReconstruction(Trace(kelt));
    rts:=Roots(xK^2-tr*xK+nm);
    L:=[r[1]: r in rts | red(r[1]) eq kelt];
    assert #L eq 1;
    return L[1];
end function;

function lift_pol(g)
    G:=Parent(X)!0;
    for t in Terms(g) do
        e:=Exponents(t);
        G+:=lift_coef(Coefficients(t)[1])*PowerProduct([X,Y,Z,W],e);
    end for;
    return G;
end function;

//Back to the locus defined by the vanishing of the Sylvester determinants.
//We confirm the dimension is 0 in reduction, and therefore also over K. That means any genus 0 curves
//that lie in a plane and any genus 1 curves that avoid the singular locus, must occur in the vanishing
//locus of the determinants of one of the A'.
Dimension(Scheme(P3Fq,[redR(g): g in DefiningPolynomials(locus)]));

//taking radical ideals is one of the things that is not feasible in
//characteristic 0. So, we define a function that does it in reduction, decomposes into
//primary components, and then uses rational reconstruction to lift the components.
//computing colon ideals is much cheaper and can be done in characteristic 0,
//so we certify our lifted result by showing that removing each of the lifted components
//leaves us with the empty scheme. That shows that the lifted components indeed contain the support
//of the original scheme. Note that this routine expects an equidimensional support
//and that no component splits further in reduction (that could disrupt lifting!)
//it turns out these things all hold for our applications.
function decompose(D)
    Dr:=Scheme(P3Fq,[redR(f): f in DefiningPolynomials(D)]);
    print "computing reduced subscheme ...";
    rDr:=ReducedSubscheme(Dr);
    print "decomposing ...";
    rpc:=PrimaryComponents(rDr);
    print "lifting ...:";
    pc:=[ Scheme(P3,[lift_pol(g): g in DefiningPolynomials(c)]): c in rpc];
    print "colon ideals!";
    T:=D;
    for p in pc do
        e:=Degree(T);
        repeat
            d:=e;
            T:=Difference(T,p);
            e:=Degree(T);
        until e eq d;
    end for;
    if Dimension(T) ne -1 then
        error "Lifted components do not support scheme fully";
    end if;
    return pc;
end function;

//After checking that "locus" is of dimension 0 and hence does not contain any curves,
//we see that any "special" curves
//(genus 1 curves not passing through any nodes or genus 0 curves passing through nodes in a hyperplane)
//would have to lie in the locus where det(A') vamishes, for one of the four A' we consider.
//We use the "decomposition" routine above to find the curves that make up that locus.
Aloci:=[Scheme(B6,d): d in Adets];
Acurves:=[decompose(a): a in Aloci];

//we find various components in each locus, but there's overlap.
//in total, we're left with 29 curves.
[#a : a in Acurves];
Aset:={a: a in b, b in Acurves};
#Aset;
Aset:={Curve(a):a in Aset};

//next we determine curves that are "accounted for": curves that lie in planes spanned by nodes.
plns:={Krn.1: s in  Subsets(sing,3) | Dimension(Krn) eq 1 where Krn:=Kernel(Transpose(Matrix([Eltseq(v): v in s])))};

//automorphism group of the Barth sextic:
m1:=Matrix(K,4,4,[0,1,0,0, 0,0,1,0, 1,0,0,0, 0,0,0,1]) where w:=((r5+1)/2);
m2:=1/2*Matrix(K,4,4,[w,w-1,1,0, w-1,1,-w,0, -1,w,w-1,0, 0,0,0,2]) where w:=((r5+1)/2);
Gamma:=sub<GL(4,K)|m1,m2>;
function normalize(v)
    for i in [1..4] do
        if v[i] ne 0 then
            return v/v[i];
        end if;
    end for;
end function;

AUT:={map<P3->P3 | Eltseq(Vector([P3.1,P3.2,P3.3,P3.4])*ChangeRing((m),Parent(X)))>: m in Gamma};
assert forall{a: a in AUT | B6@@a eq B6 };

//in order to save some work, we take orbit representatives of the planes under AUT.
V:=plns;
representatives:=[];
repeat
    v:=Rep(V);
    Append(~representatives,v);
    orb:={normalize(w): w in Orbit(Gamma,v)};
    assert orb subset V;
    V diff:=orb;
until #V eq 0;
#representatives;

//Take the plane sections
PlaneSections:=[ReducedSubscheme(Scheme(B6,&+[v[i]*P3.i: i in [1..4]])): v in representatives];

//Take the irreducible components. These are the relevant curves on the Barth sextic
//We split them by genus 0 and 1 and take full orbits under the automorphisms
PlaneCurves:={Curve(C): C in PrimaryComponents(a), a in PlaneSections};
genus0:={C@@a: a in AUT, C in PlaneCurves | Genus(C) eq 0};
genus1:={C@@a: a in AUT, C in PlaneCurves | Genus(C) eq 1};

//some stats on the degree of the curves and the number of nodes they go through.
{*<Degree(C),Degree(C meet SB6)>: C in genus0*};
{*<Degree(C),Degree(C meet SB6)>: C in genus1*};

//demonstration that the degree 6 curve of "genus 1" splits when sqrt(-1) is adjoined
//into a union of two plane cubics (passing through 9 nodes).
C6:=[C: C in genus1 | Degree(C) eq 6][1];
PrimaryComponents(BaseChange(C6,CompositeFields(K,QuadraticField(-1))[1]));

//We remove from our 29 curves the curves accounted for above. This leaves us with 6 curves.
Arem:=Setseq(Aset diff genus0 diff genus1);
#Arem;
//We compute genera in reduction. A non-hyperbolic curve cannot reduce to a hyperbolic one,
//so this allows us to discard several of the curves.
genus_A:=[Genus(Curve(P3Fq,[redR(g): g in DefiningPolynomials(a)])): a in Arem];
genus_A;
//there are two curves. Each is an intersection of 2 quadrics passing through 16 nodes
remaining:=[Arem[i]: i in [1..#Arem]| genus_A[i] le 1];
[<Degree(C),Degree(C meet SB6)>: C in remaining];
//these are genus 1 curves passing through nodes spanning P3, so we are not making statements about them,
//but it is interesting that we find these curves anyway. The two curves found here are part of an
//orbit of length 15 under the automorphism group.
#{C@@a: C in remaining, a in AUT};

quit;
