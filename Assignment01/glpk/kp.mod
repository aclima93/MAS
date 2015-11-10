/* KP, Knapsack Problem */

/* Written in GNU MathProg inspired on https://en.wikibooks.org/wiki/GLPK/Knapsack_Problem */

/* Max. Coverage */
param maxC;

/* Max., Min Coverage Percent. */
param maxCP;
param minCP;

/* Items: index, weight, coverage */
set I, dimen 3;

/* Indices */
set J := setof{(i, w, c) in I} i;

/* Assignment */
var a{J}, binary;


maximize obj : sum{(i, w, c) in I} a[i] * w;

/* At least one path must be chosen */
s.t. pathSelected: sum{(i, w, c) in I} a[i] >= 1;

/* Covegare between Min. and Max. Coverage Percent. */
s.t. minCoverage : sum{(i, w, c) in I} ((c * a[i]) * 100) / maxC >= minCP;
s.t. maxCoverage : sum{(i, w, c) in I} ((c * a[i]) * 100) / maxC <= maxCP;

solve;

printf "Selected Paths: \n";
printf {(i, w, c) in I: a[i] == 1} "%d %d %d\n", i, w, c;
printf "\n";

end;