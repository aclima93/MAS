__authors__ = 'aclima, ilpetronilho, pjaneiro'
"""
Strip the excess information from the GLPK output and draw the selected paths

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
3
5
13
=== END ===

Model has been successfully processed
"""

import sys
import re
import networkx as nx
import matplotlib.pyplot as plt


def get_solutions_edges(lines):

    solutions = []
    edges = []
    for line in lines:  # skip the source node

        # empty line
        if re.match("\n", line):
            if edges not in solutions:
                solutions.append(edges)
            edges = []

        # edge line
        elif re.match("(\d)+ (\d)+", line):
            node1, node2 = line.rstrip().lstrip().split()  # remove right and left whitespace then split
            edges.append([int(node1), int(node2)])

    return solutions


def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    nx_graph = nx.DiGraph()

    # add nodes
    for node in nodes:
        nx_graph.add_node(node)

    # add edges
    for edge in graph:
        nx_graph.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(nx_graph)
    nx.draw(nx_graph, pos)

    # show graph
    plt.show()


if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 6:

        graph_filename = sys.argv[1]
        node_coverage_filename = sys.argv[2]
        edge_coverage_filename = sys.argv[3]
        edge_pair_coverage_filename = sys.argv[4]
        paths_with_cycles_filename = sys.argv[5]

        # read input file and filter useful information
        graph_file = open(graph_filename, 'r')
        graph_edges = get_solutions_edges(graph_file.readlines())
        graph_file.close()

        paths_with_cycles_file = open(paths_with_cycles_filename, 'r')
        paths_with_cycles_edges = get_solutions_edges(paths_with_cycles_file.readlines())
        paths_with_cycles_file.close()

        # read solution indexes returned by kp.mod
        filenames = [node_coverage_filename, edge_coverage_filename, edge_pair_coverage_filename]
        solutions_indexes = []
        for filename in filenames:

            file = open(filename, 'w')
            data_lines = file.readlines()
            indexes = []

            if ("=== START ===\n" in data_lines) and ("=== END ===\n" in data_lines):

                start = data_lines.index("=== START ===\n")
                end = data_lines.index("=== END ===\n")
                data_lines = data_lines[start + 1:end]  # skip start line

                for line in data_lines:
                    indexes.append(int(line.rstrip().lstrip()))  # remove right and left whitespace then split

            solutions_indexes.append(indexes)
            file.close()

        draw_graph(graph_edges)
        for indexes in solutions_indexes:
            for index in indexes:
                draw_graph(paths_with_cycles_edges[index - 1])

    else:
        print("output_graphs expects arguments: <graph file> <coverage output file> <edge coverage output file> <edge-pair coverage output file> <paths with cycles file>")
