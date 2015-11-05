__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys
import re

# calculates node coverage
def node_coverage(path):
    return len(set(path))


# calculates edge coverage
def edge_coverage(edges, path):
    counter = 0

    for i in range(len(path) - 1):
        edge = [path[i], path[i + 1]]
        if edge in edges:
            counter += 1

    return counter


# calculates edge-pair coverage
def edge_pair_coverage(edges, path):
    counter = 0

    for i in range(len(path) - 2):
        left_edge = [path[i], path[i + 1]]
        right_edge = [path[i + 1], path[i + 2]]
        if (left_edge in edges) and (right_edge in edges):
            counter += 1

    return counter

def print_path(output_file, path, edges):

    output_file.write("Path: " + str(path) + '\n')
    output_file.write("Length: " + str(len(path)) + '\n')
    output_file.write("NC: " + str(node_coverage(path)) + '\n')
    output_file.write("EC: " + str(edge_coverage(edges, path)) + '\n')
    output_file.write("EPC: " + str(edge_pair_coverage(edges, path)) + '\n')
    output_file.write('\n')


# parse edges from file
def parse_file(file):

    paths = {}
    edges = {}
    aux = None
    for line in file.readlines():

        # strip troublesome whitespace
        line = line.rstrip().lstrip()

        # vertex line
        if re.fullmatch("(\d)+", line):
            aux = int(re.fullmatch("(\d)+", line).group(0))

        # edge line
        elif re.fullmatch("(\d)+ (\d)+", line):

            node1, node2 = re.fullmatch("(\d)+ (\d)+", line).group(0).split()
            edge = [int(node1), int(node2)]

            if edges.get(aux):
                edges[aux].append(edge)
            else:
                edges[aux] = [edge]

    # remove empty paths and order the rest
    for source_node, path_edges in edges.items():

        if len(path_edges) == 0:
            edges.pop(source_node)
        else:
            paths[source_node] = {}
            for edge in path_edges:
                paths[source_node][edge[0]] = edge[1]

    return paths, edges


def combine_paths_with_cycles(paths, cycles):
    pass


if __name__ == '__main__':

    paths_file = open("paths.txt", 'r')
    cycles_file = open("cycles.txt", 'r')
    paths_with_cycles_file = open("paths_with_cycles.txt", 'w')

    paths, paths_edges = parse_file(paths_file)
    cycles, cycles_edges = parse_file(cycles_file)

    paths_file.close()
    cycles_file.close()

    '''
    print(paths)
    print(paths_edges)
    print(cycles)
    print(cycles_edges)
    '''

    paths_with_cycles = combine_paths_with_cycles(paths, cycles)

    '''
    for path, edges in paths_with_cycles:
        print_path(paths_with_cycles_file, path, edges)
    '''

    paths_with_cycles_file.close()
