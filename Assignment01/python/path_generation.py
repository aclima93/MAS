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

def print_path_info(file, path, edges):

    file.write("Path: " + str(path) + '\n')
    file.write("Length: " + str(len(path)) + '\n')
    file.write("NC: " + str(node_coverage(path)) + '\n')
    file.write("EC: " + str(edge_coverage(edges, path)) + '\n')
    file.write("EPC: " + str(edge_pair_coverage(edges, path)) + '\n')
    file.write('\n')


# parse edges from file
def parse_file(file):

    paths = {}
    edges = {}
    source = None
    new_solution = True
    for line in file.readlines():

        # strip troublesome whitespace
        line = line.rstrip().lstrip()

        # empty line
        if re.match("\n", line):
            new_solution = True

        # edge line
        elif re.match("(\d)+ (\d)+", line):

            node1, node2 = re.match("(\d)+ (\d)+", line).group(0).split()

            if new_solution:
                source = int(node1)
                new_solution = False

            edge = [int(node1), int(node2)]

            if edges.get(source):
                edges[source].append(edge)
            else:
                edges[source] = [edge]

    # remove empty paths and order the rest
    for source_node, path_edges in edges.items():

        if len(path_edges) == 0:
            edges.pop(source_node)
        else:
            paths[source_node] = {}
            for edge in path_edges:
                paths[source_node][edge[0]] = edge[1]

    return paths, edges


def get_paths_lists_from_dict(paths):

    paths_lists = {}

    for paths_k, paths_v in paths.items():

        cur_node = paths_k
        path = []

        while paths_v.get(cur_node):

            # counter-measure for cycles dicts
            if cur_node in path:
                break
            else:
                path.append(cur_node)
                cur_node = paths_v[cur_node]

        paths_lists[paths_k] = path

    return paths_lists


def combine_paths_with_cycles(paths, cycles):

    '''
    print(paths)
    print(paths_edges)
    print(cycles)
    print(cycles_edges)
    '''

    # #
    # Paths
    paths_lists = {}
    for paths_k, paths_v in paths.items():

        cur_node = paths_k
        path = []

        while paths_v.get(cur_node):

            # counter-measure for cycles dicts
            if cur_node in path:
                break
            else:
                path.append(cur_node)
                cur_node = paths_v[cur_node]

        path.append(cur_node)  # add the target node
        paths_lists[paths_k] = path

    # #
    # Cycles
    cycles_lists = {}
    for cycles_k, cycles_v in cycles.items():

        cur_node = cycles_k
        path = []

        while cycles_v.get(cur_node):

            # counter-measure for cycles dicts
            if cur_node in path:
                break
            else:
                path.append(cur_node)
                cur_node = cycles_v[cur_node]

        path.append(cycles_k)  # add the starting node of the cycle for easier fitting afterwards
        cycles_lists[cycles_k] = path

    '''
    print(paths_lists)
    print(cycles_lists)
    '''

    # #
    # Paths With Cycles
    paths_with_cycles = []
    for paths_lists_v in paths_lists.values():
        for cycles_lists_k in cycles_lists.keys():

            # example: path = 0,1,4 cycle = 1,2,3,1 result = 0,1,2,3,1,4
            if cycles_lists_k in paths_lists_v:
                index = paths_lists_v.index(cycles_lists_k)
                if index + 1 < len(paths_lists_v):
                    path = paths_lists_v[:index] + cycles_lists[cycles_lists_k] + paths_lists_v[index + 1:]
                else:
                    path = paths_lists_v[:index] + cycles_lists[cycles_lists_k]

                # avoid duplicates
                if path not in paths_with_cycles:
                    paths_with_cycles.append(path)

    # print(paths_with_cycles)

    return paths_with_cycles


def get_path_edges(path):
    edges = []
    for i in range(len(path) - 1):
        edge = path[i:i + 2]
        if edge not in edges:
            edges.append(edge)

    # print(edges)

    return edges


if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 5:

        basic_paths_filename = sys.argv[1]
        cycles_filename = sys.argv[2]
        paths_filename = sys.argv[3]
        output_filename = sys.argv[4]

        basic_paths_file = open(basic_paths_filename, 'r')
        paths_file = open(paths_filename, 'r')
        cycles_file = open(cycles_filename, 'r')

        basics_paths, basics_paths_edges = parse_file(basic_paths_file)
        paths, paths_edges = parse_file(paths_file)
        cycles, cycles_edges = parse_file(cycles_file)

        basic_paths_file.close()
        paths_file.close()
        cycles_file.close()

        output_file = open(output_filename, 'w')

        paths_with_cycles = combine_paths_with_cycles(paths, cycles)
        for path in paths_with_cycles:
            print_path_info(output_file, path, get_path_edges(path))

        output_file.close()

    else:
        print("path_generation expects arguments: <basic paths file> <cycles file> <paths file> <output file>")
