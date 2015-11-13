__authors__ = 'aclima, ilpetronilho, pjaneiro'
"""
Create an appropriate .dat file for GLPK aspp.mod from the input .dat file

----------INPUT-----------
 0  1
 0  2
 1  2
 1  3
 2 12
 3  4
 3  5
 4  5
 4  8
 5  2
 5  6
 5  7
 6  8
 7  8
 8  9
 9 10
 9 11
10 11
11 12

-----------OUTPUT------------
data;

param n := 13;
param s := 0;
param t := 12;

param : E :   c :=
0	1	1
0	2	1
1	2	1
1	3	1
2	12	1
3	4	1
3	5	1
4	5	1
4	8	1
5	2	1
5	6	1
5	7	1
6	8	1
7	8	1
8	9	1
9	10	1
9	11	1
10	11	1
11	12	1;

end;
"""

import sys
import re

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 6:

        input_filename = sys.argv[1]
        previous_solutions_filename = sys.argv[2]
        aspp_1_filename = sys.argv[3]
        aspp_2_filename = sys.argv[4]
        output_filename = sys.argv[5]

        input_file = open(input_filename, 'r')

        edges = []
        vertices = []
        for line in input_file.readlines():
            node1, node2 = line.rstrip().lstrip().split()  # remove right and left whitespace then split

            node1 = int(node1)
            node2 = int(node2)

            edges.append([node1, node2])

            if node1 not in vertices:
                vertices.append(node1)
            if node2 not in vertices:
                vertices.append(node2)

        input_file.close()

        # start and end nodes of our graph are defined by the corresponding minimum and maximum node numbers
        vertices.sort()
        source = vertices[0]
        target = vertices[-1]
        num_vertices = len(vertices)

        # write to output file
        output_file = open(output_filename, 'w')

        # write 1st half of aspp.mod model
        aspp_1_file = open(aspp_1_filename, 'r')
        for line in aspp_1_file.readlines():
            output_file.write(line)
        aspp_1_file.close()

        # write previous found solutions as forbidden edges for the this iteration
        previous_solutions_file = open(previous_solutions_filename, 'r')
        lines = previous_solutions_file.readlines()
        previous_solutions_file.close()

        all_paths_edges = []
        edges_solution = []
        for line in lines:

            # empty line
            if re.match("\n", line):

                if edges_solution not in all_paths_edges:
                    all_paths_edges.append(edges_solution)
                edges_solution = []

            # edge line
            elif re.match("(\d)+ (\d)+", line):
                node1, node2 = line.split()
                edges_solution.append( [int(node1), int(node2)] )

        constraint_counter = 0
        for edges_solution in all_paths_edges:
            constraint_counter += 1
            constraint = "\ns.t. constraint" + str(constraint_counter) + ": (sum{(i,j) in E} x[i,j]) - ( "
            sums = ""
            for edge in edges_solution[:-1]:
                sums += "x[" + str(edge[0]) + "," + str(edge[1]) + "] + "
            sums += "x[" + str(edges_solution[-1][0]) + "," + str(edges_solution[-1][1]) + "]"
            # s.t. constraint_n: (sum{(j,i) in E} x[j,i]) - ( <edge_1> + ... + <edge_m> ) >= 1;
            constraint += sums + " ) >= " + str(1) + ";"
            output_file.write( constraint)

        # write 2nd half of aspp.mod model
        aspp_2_file = open(aspp_2_filename, 'r')
        for line in aspp_2_file.readlines():
            output_file.write(line)
        aspp_2_file.close()

        # write problem data for aspp.mod
        output_file.write("data;\n\n")
        output_file.write(str("param n := ") + str(num_vertices) + str(";\n"))
        output_file.write(str("param s := ") + str(source) + str(";\n"))
        output_file.write(str("param t := ") + str(target) + str(";\n"))

        output_file.write("\nparam : E :   c :=")
        for node1, node2 in edges:
            # unweighed == same weight for all
            output_file.write(str("\n") + str(node1) + str("\t") + str(node2) + str("\t") + str("1"))

        output_file.write(";\n\nend;\n")

        output_file.close()

    else:
        print("aspp_input_generator expects arguments: <input file> <previous solutions file> <aspp_1 file> <aspp_2 file> <output file> ")
