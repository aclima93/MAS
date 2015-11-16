/* Partial Coverage Problem */

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

/* Checks if column (node, edge, edge-pair) is covered */
var t{J}, binary, >=0;

/* Minimize with respect to the weight of each path */
minimize obj : sum{i in I} x[i] * w[i];

/* Selected Paths Coverage & with leat one is chosen */
/*s.t. pathCoverage{j in J}: sum{i in I} f[i,j] * x[i] >= 1;*/
s.t. columnCover{j in J}: t[j] = sum{i in I} f[i,j] * x[i];

/* Cover at least Min. Coverage Percent. */
s.t. minPathCoverage: sum{j in J} t[j] * 100 >= minCP * maxC;

solve;

/*printf {j in J, i in I} "%d\t%d\t%d\n", i, j, f[i,j];*/
printf('=== START ===\n');
printf {i in I: x[i] == 1} "%d\n", i;
printf('=== END ===\n\n');

end;
