__author__ = 'aclima'
"""
Create an appropriate .dat file for GLPK spp.mod from the input .dat file

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
param s := 1;
param t := 13;

param : E :   c :=
1	2	1
1	3	1
2	3	1
2	4	1
3	13	1
4	5	1
4	6	1
5	6	1
5	9	1
6	3	1
6	7	1
6	8	1
7	9	1
8	9	1
9	10	1
10	11	1
10	12	1
11	12	1
12	13	1;

end;
"""

import sys

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]

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
        if vertices[0] == 0:
            vertices = [x + 1 for x in vertices]
            edges = [[x + 1, y + 1] for x, y in edges]

        source = vertices[0]
        target = vertices[-1]
        num_vertices = len(vertices)

        # write to output file
        output_file = open(output_filename, 'w')

        output_file.write("data;\n\n")
        output_file.write(str("param n := ") + str(num_vertices) + str(";\n"))
        output_file.write(str("param s := ") + str(source) + str(";\n"))
        output_file.write(str("param t := ") + str(target) + str(";\n"))

        output_file.write("\nparam : E :   c :=")
        for node1, node2 in edges:
            # unweighed == same weight for all
            output_file.write(str("\n") + str(node1) + str("\t") + str(node2) + str("\t") + str("1"))
        output_file.write(";\n\n")

        output_file.write("end;")

        output_file.close()

    else:
        print("dat_file_generator expects arguments: <input file> <output file>")
