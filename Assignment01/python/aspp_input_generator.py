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

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 4:

        input_filename = sys.argv[1]
        previous_solutions_filename = sys.argv[2]
        output_filename = sys.argv[3]

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

        output_file.write("data;\n\n")

        output_file.write(str("param n := ") + str(num_vertices) + str(";\n"))
        output_file.write(str("param s := ") + str(source) + str(";\n"))
        output_file.write(str("param t := ") + str(target) + str(";\n"))

        # write previous found solutions as forbidden edges for the this iteration
        previous_solutions_file = open(previous_solutions_filename, 'r')
        lines = previous_solutions_file.readlines()

        output_file.write(str("param fn := ") + str(len(lines)) + str(";\n"))

        output_file.write("\nset FE :=\n")
        for line in lines:
            output_file.write(line)
        output_file.write(";\n")

        previous_solutions_file.close()

        output_file.write("\nparam : E :   c :=")
        for node1, node2 in edges:
            # unweighed == same weight for all
            output_file.write(str("\n") + str(node1) + str("\t") + str(node2) + str("\t") + str("1"))

        output_file.write(";\n\nend;\n")

        output_file.close()

    else:
        print("aspp_input_generator expects arguments: <input file> <previous solutions file> <output file> ")
