__author__ = 'aclima'
"""
Strip the excess information from the GLPK spp.mod output and add it to the colective output file

----------INPUT-----------
GLPSOL: GLPK LP/MIP Solver, v4.52
Parameter(s) specified in the command line:
 -m spp.mod -d cfg1_glpk.dat
Reading model section from spp.mod...
spp.mod:54: warning: final NL missing before end of file
54 lines were read
Reading data section from cfg1_glpk.dat...
cfg1_glpk.dat:28: warning: final NL missing before end of file
28 lines were read
Generating r...
Generating Z...
Model has been successfully generated
GLPK Simplex Optimizer, v4.52
14 rows, 19 columns, 57 non-zeros
Preprocessing...
13 rows, 19 columns, 38 non-zeros
Scaling...
 A: min|aij| =  1.000e+00  max|aij| =  1.000e+00  ratio =  1.000e+00
Problem data seem to be well scaled
Constructing initial basis...
Size of triangular part is 12
*     0: obj =   2.000000000e+00  infeas =  0.000e+00 (1)
*     2: obj =   2.000000000e+00  infeas =  0.000e+00 (1)
OPTIMAL LP SOLUTION FOUND
Time used:   0.0 secs
Memory used: 0.1 Mb (131220 bytes)

=== START ===
1
1	2	0
1	3	1
2	3	0
2	4	0
3	13	1
4	5	0
4	6	0
5	6	0
5	9	0
6	3	0
6	7	0
6	8	0
7	9	0
8	9	0
9	10	0
10	11	0
10	12	0
11	12	0
12	13	0
=== END ===

Model has been successfully processed


-----------OUTPUT------------
1
1	3	1
3	13	1
"""

import sys

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 3:

        input_filename = sys.argv[1]
        output_filename = sys.argv[2]

        # read input file and filter useful information
        input_file = open(input_filename, 'r')

        data_lines = input_file.readlines()
        start = data_lines.index("=== START ===\n")
        end = data_lines.index("=== END ===\n")
        data_lines = data_lines[start + 1:end]

        for line in data_lines[1:]:  # skip the source node
            node1, node2, isUsed = line.rstrip().lstrip().split()  # remove right and left whitespace then split
            if isUsed == "0":  # remove this line if the edge is not used in the shortest path
                data_lines.remove(line)

        input_file.close()

        # write to output file
        output_file = open(output_filename, 'a')

        for line in data_lines:
            output_file.write(line)

        output_file.close()

    else:
        print("output_file_appender expects arguments: <input file> <output file>")
