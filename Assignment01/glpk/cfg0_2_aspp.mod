/* ASPP, All Shortest Path Problem */

/* Written in GNU MathProg by Andrew Makhorin <mao@gnu.org> */

/* Given a directed graph G = (V,E), its edge lengths c(i,j) for all
   (i,j) in E, and two nodes s, t in V, the All Shortest Path Problem (ASPP)
   is to find a directed path from s to t whose length is minimal,
   without using the forbidden edges of FE */

param n, integer, >= 0;
/* number of nodes */

set E, within {i in 0..n, j in 0..n};
/* set of edges */

param c{(i,j) in E};
/* c[i,j] is length of edge (i,j); note that edge lengths are allowed
   to be of any sign (positive, negative, or zero) */

param s, in {0..n};
/* source node */

param t, in {0..n};
/* target node */

var x{(i,j) in E}, binary, >= 0;
/* x[i,j] = 1 means that edge (i,j) belong to shortest path;
   x[i,j] = 0 means that edge (i,j) does not belong to shortest path;
   note that variables x[i,j] are binary, however, there is no need to
   declare them so due to the totally unimodular constraint matrix */

minimize Z: sum{(i,j) in E} c[i,j] * x[i,j];
/* objective function is the path length to be minimized */

s.t. constraint0_1{i in 0..n}: sum{(j,i) in E} x[j,i] + (if i = s then 1) =
                   sum{(i,j) in E} x[i,j] + (if i = t then 1);
/* conservation conditions for unity flow from s to t; every feasible
   solution is a path from s to t */
s.t. constraint0_2{i in 0..n}: sum{(j,i) in E} x[j,i] + (if i = s then 1) <= 1;
s.t. constraint0_3{i in 0..n}: sum{(i,j) in E} x[i,j] + (if i = t then 1) <= 1;
/* each node can only have at most one edge coming in & one edge coming out
 	Note1: this allows for cycles that do not overlap with the solution path
 	to be included in the solution, howerver this is not problematic because 
 	we will start athe the Source node and always reach the Target node without
 	as if the cycles weren't there in the first place. The only problem is that 
 	we will have "redundant" solutions which is inelegant but, 
 	at the moment, unavoidable. 

 	Note2: this in turn is another great way to find both all paths 
 	from source to target and all cycles unrelated to each of those paths */

s.t. constraint1: (sum{(i,j) in E} x[i,j]) - ( x[0,9] ) >= 1;
s.t. constraint2: (sum{(i,j) in E} x[i,j]) - ( x[0,5] + x[5,9] ) >= 1;
s.t. constraint3: (sum{(i,j) in E} x[i,j]) - ( x[0,1] + x[1,9] ) >= 1;
s.t. constraint4: (sum{(i,j) in E} x[i,j]) - ( x[0,5] + x[5,7] + x[7,9] ) >= 1;
s.t. constraint5: (sum{(i,j) in E} x[i,j]) - ( x[0,5] + x[5,6] + x[6,9] ) >= 1;
s.t. constraint6: (sum{(i,j) in E} x[i,j]) - ( x[0,1] + x[1,4] + x[4,9] ) >= 1;
s.t. constraint7: (sum{(i,j) in E} x[i,j]) - ( x[0,1] + x[1,2] + x[2,9] ) >= 1;
s.t. constraint8: (sum{(i,j) in E} x[i,j]) - ( x[0,1] + x[1,2] + x[2,3] + x[3,9] ) >= 1;
s.t. constraint9: (sum{(i,j) in E} x[i,j]) - ( x[0,5] + x[5,7] + x[7,8] + x[8,9] ) >= 1;

solve;

printf('=== START ===\n');
/* x[i,j] = 1 means that edge (i,j) belong to shortest path;
   x[i,j] = 0 means that edge (i,j) does not belong to shortest path; */
printf{(i,j) in E}:'%d\t%d\t%d\n', i, j, x[i,j]; 
printf('=== END ===\n\n');
data;

param n := 10;
param s := 0;
param t := 9;

param : E :   c :=
0	1	1
0	5	1
0	9	1
1	2	1
1	4	1
1	9	1
2	3	1
2	9	1
3	9	1
4	9	1
5	6	1
5	7	1
5	9	1
6	9	1
7	8	1
7	9	1
8	9	1;

end;
