__authors__ = 'aclima, ilpetronilho, pjaneiro'
"""
Count how many nodes there are in the graph

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
13
"""

import sys

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 2:

        input_filename = sys.argv[1]

        input_file = open(input_filename, 'r')

        vertices = []
        for line in input_file.readlines():
            node1, node2 = line.rstrip().lstrip().split()  # remove right and left whitespace then split

            node1 = int(node1)
            node2 = int(node2)

            if node1 not in vertices:
                vertices.append(node1)
            if node2 not in vertices:
                vertices.append(node2)

        input_file.close()

        # start and end nodes of our graph are defined by the corresponding minimum and maximum node numbers
        vertices.sort()

        for vertex in vertices:
            print(vertex)

    else:
        print("vertices_counter expects arguments: <input file>")
