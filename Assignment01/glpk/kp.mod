/* KP, Knapsack Problem */

/* Written in GNU MathProg inspired on https://en.wikibooks.org/wiki/GLPK/Knapsack_Problem */

/* Max. Coverage */
param maxC, integer, >= 0;

/* Min Coverage Percent. */
param minCP, integer, >= 0;

param n, integer, >= 0;
/* number of paths */

set I := {i in 1..n};
set J := {j in 1..maxC};

/* Path Coverage Frequency Matrix */
param f{i in I, j in J}, binary, >= 0;

/* Path Weight Matrix */
param w{i in I}, integer, >= 0;

/* Path Selection Matrix */
var x{I}, binary, >= 0;


minimize obj : sum{i in I} x[i] * w[i];

/*
minimize obj : sum{i in I} x[i];
*/

/* At least one path must be chosen */
/*
s.t. pathSelected: sum{i in I} x[i] >= 1;
*/

/* Selected Paths Coverage */
/*s.t. pathCoverage{j in J}: sum{i in I} ((f[i,j] * x[i]) * 100) / maxC >= minCP;*/

/* Selected Paths Coverage */
s.t. pathCoverage{j in J}: sum{i in I} f[i,j] * x[i] >= 1;

/* Cover at least Min. Coverage Percent. */
/*s.t. minPathCoverage : ((f[i,j] * x[i]) * 100) / maxC >= minCP;*/

solve;

printf('=== START ===\n');
printf {i in I: x[i] == 1} "%d\n", i;
printf('=== END ===\n\n');

end;
