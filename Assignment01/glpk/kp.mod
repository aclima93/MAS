/* KP, Knapsack Problem */

/* Written in GNU MathProg inspired on https://en.wikibooks.org/wiki/GLPK/Knapsack_Problem */

/* Max. Coverage */
param maxC, integer, >= 0;

/* Min Coverage Percent. */
param minCP, integer, >= 0;

param n, integer, >= 0;
/* number of paths */

/* Coverages matrix for each path */
param C{i in 0..n, j in 0..maxC}, integer, >= 0;

/* Items: index, weight */
set W, dimen 2;

/* Indices */
set J := setof{(i, w) in W} i;

/* Assignment */
var a{J}, binary, >= 0;


minimize obj : sum{(i, w) in W} a[i] * w;

/* At least one path must be chosen */
s.t. pathSelected: sum{(i, w) in W} a[i] >= 1;

/* Cover at least Min. Coverage Percent. of everything */
/*s.t. minCoverage : sum{(i, w) in W} ((c * a[i]) * 100) / maxC >= minCP;*/

solve;

printf "Selected Paths: \n";
printf {(i, w) in W: a[i] == 1} "%d %d\n", i, w;
printf "\n";

end;