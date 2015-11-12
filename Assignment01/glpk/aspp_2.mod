

solve;

printf('=== START ===\n');
/* x[i,j] = 1 means that edge (i,j) belong to shortest path;
   x[i,j] = 0 means that edge (i,j) does not belong to shortest path; */
printf{(i,j) in E}:'%d\t%d\t%d\n', i, j, x[i,j]; 
printf('=== END ===\n\n');
