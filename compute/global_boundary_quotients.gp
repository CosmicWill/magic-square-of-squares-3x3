\\ Independent global-obstruction branch: GB.8 diagnostics only.
\\ The exclusion proof uses Tunnell's finite certificate, not these ranks.
\\ Run with the PARI/GP executable, not PowerShell's alias gp=Get-ItemProperty.
default(parisize, "64M");
setrand(1);
print("PARI_VERSION ", version());
for(i=1,3, q=[17,89,1513][i]; E=if(i==2,ellinit(ellfromeqn(y^2-q*(1-x^4))),ellinit([0,-2*q,0,2*q^2,0])); r=ellrank(E); T=elltors(E); print("QUOTIENT ",i," q=",q," coefficients=",E[1..5]," rank=",r," torsion=",T); if(r[2]!=[1,0,1][i] || T[1]!=2,error("unexpected diagnostic bounds")); for(j=1,#r[4],if(!ellisoncurve(E,r[4][j]),error("point off curve"))));
quit;
