/* KP, Knapsack Problem */

/* Written in GNU MathProg inspired on https://en.wikibooks.org/wiki/GLPK/Knapsack_Problem */

/* Max. Coverage */
param mc;

/* Max. Coverage Percent. */
param mcp;

/* Items: index, weight, coverage */
set I, dimen 3;

/* Indices */
set J := setof{(i, w, c) in I} i;

/* Assignment */
var a{J}, binary;

maximize obj : sum{(i, w, c) in I} w * a[i];

/* Covegare between 0 and Max. Coverage Percent. */
s.t. minCoverage : sum{(i, w, c) in I} c * a[i] >= 0;
s.t. maxCoverage : sum{(i, w, c) in I} ((c * a[i]) * 100) / mc <= mcp;

solve;

printf "Selected Paths: \n";
printf {(i, w, c) in I: a[i] == 1} "%i\n", i;
printf "\n";

end;