/* SCPP, Shortest Cycle Path Problem */

/* Written in GNU MathProg by Andrew Makhorin <mao@gnu.org> */

/* Given a directed graph G = (V,E), its edge lengths c(i,j) for all
   (i,j) in E, and two nodes s, t in V, the Shortest Cycle Path Problem (SCPP)
   is to find a directed path from s to t whose length is minimal. */

param n, integer, >= 0;
/* number of nodes */

set E, within {i in 0..n, j in 0..n};
/* set of edges */

param c{(i,j) in E};
/* c[i,j] is length of edge (i,j); note that edge lengths are allowed
   to be of any sign (positive, negative, or zero) */

set FE, within {i in 0..n, j in 0..n};
/* set of forbidden edges */

var x{(i,j) in E}, binary;
/* x[i,j] = 1 means that edge (i,j) belong to shortest cycle path;
   x[i,j] = 0 means that edge (i,j) does not belong to shortest cycle path;
   note that variables x[i,j] are binary, however, there is no need to
   declare them so due to the totally unimodular constraint matrix */

s.t. r1{i in 0..n}: sum{(j,i) in E} x[j,i] =
                   sum{(i,j) in E} x[i,j];

s.t. r2: sum{(i,j) in E} x[i,j] >= 1;
/* at least one edge must be chosen */

s.t. r3: sum{(i,j) in FE} x[i,j] <= 0;
/* no forbidden edge can be chosen */

minimize Z: sum{(i,j) in E} c[i,j] * x[i,j];
/* objective function is the path length to be maximized */

solve;

printf('=== START ===\n');
/* x[i,j] = 1 means that edge (i,j) belong to shortest cycle path;
   x[i,j] = 0 means that edge (i,j) does not belong to shortest cycle path; */
printf{(i,j) in E}:'%d\t%d\t%d\n', i, j, x[i,j]; 
printf('=== END ===\n\n');

end;
