__author__ = 'aclima'

import sys
import numpy as np


# create graph from input file node pairs
def create_graph(input_file):
    graph = {}

    for line in input_file.readlines():
        node1, node2 = line.rstrip().lstrip().split()

        if graph.get(node1):
            graph[node1].append(node2)
        else:
            graph[node1] = [node2]

    return graph

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 2:
        input_file = sys.argv[1]
        output_file = str(input_file) + str(".txt")

        input_file = open(input_file, 'r')
        output_file = open(output_file, 'w')

        graph = create_graph(input_file)

        # start and end nodes of our graph are defined by the corresponding minimum and maximum node numbers
        start_node = min(graph.keys())
        end_node = max(graph.keys())

        input_file.close()
        output_file.close()

    else:
        print("shortest_path expects arguments: <input file>")

