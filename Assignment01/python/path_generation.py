__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys
import re

# calculates node coverage
def path_node_coverage(path):
    return len(set(path))


# calculates edge coverage
def path_edge_coverage(edges, path):
    counter = 0

    for i in range(len(path) - 1):
        edge = [path[i], path[i + 1]]
        if edge in edges:
            counter += 1

    return counter


# calculates edge-pair coverage
def path_edge_pair_coverage(edges, path):
    counter = 0

    for i in range(len(path) - 2):
        left_edge = [path[i], path[i + 1]]
        right_edge = [path[i + 1], path[i + 2]]
        if (left_edge in edges) and (right_edge in edges):
            counter += 1

    return counter

def print_header(file, max_coverage):
    file.write("data;\n")
    file.write("\n")
    file.write("/* Max. Coverage i.e. Coverage of the full graph */\n")
    file.write("param mc := " + str(max_coverage) + ";\n")
    file.write("\n")
    file.write("/* Max. Coverage Percent. */\n")
    file.write("param mcp := 100;\n")
    file.write("\n")
    file.write("/* Items: index, weight, coverage */\n")
    file.write("set I :=\n")

def print_footer(file):
    file.write(";\n\n end;")

def print_path_info(file, path_index, path, weight, coverage):

    # comments for better understanding of the .dat file
    file.write("/*\n")
    file.write("Path Index: " + str(path_index) + '\n')
    file.write("Path: " + str(path) + '\n')
    file.write("Weight: " + str(weight) + '\n')
    file.write("Coverage: " + str(coverage) + '\n')
    file.write("/*\n")
    file.write(str(path_index) + " " + str(weight) + " " + str(coverage))
    file.write('\n\n')


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


def combine_paths_with_cycles(paths, cycles):

    print(paths)
    print(cycles)

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

    print(paths_lists)
    print(cycles_lists)

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


def get_nodes_from_edges(edges):
    nodes = []
    for edge in edges:
        node1, node2 = edge.lstrip().rstrip().split()
        nodes.append(node1)
        nodes.append(node2)

    nodes = list(set(nodes))
    nodes.sort()
    return nodes


def get_edge_pairs_from_edges(edges):
    edge_pairs = []

    for edge1 in edges:
        for edge2 in edges:
            if not(edge1 == edge2):
                node11, node12 = edge1.lstrip().rstrip().split()
                node21, node22 = edge2.lstrip().rstrip().split()

                if (node12 == node21) and ([edge1, edge2] not in edge_pairs):
                    edge_pairs.append([edge1, edge2])
                if (node11 == node22) and ([edge2, edge1] not in edge_pairs):
                    edge_pairs.append([edge2, edge1])

    return edge_pairs

if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 8:

        graph_filename = sys.argv[1]
        basic_paths_filename = sys.argv[2]
        cycles_filename = sys.argv[3]
        paths_filename = sys.argv[4]
        node_coverage_filename = sys.argv[5]
        edge_coverage_filename = sys.argv[6]
        edge_pair_coverage_filename = sys.argv[7]

        graph_file = open(graph_filename, 'r')
        basic_paths_file = open(basic_paths_filename, 'r')
        paths_file = open(paths_filename, 'r')
        cycles_file = open(cycles_filename, 'r')

        # load the computed data from the output files
        graph_edges = graph_file.readlines()
        basics_paths, basics_paths_edges = parse_file(basic_paths_file)
        paths, paths_edges = parse_file(paths_file)
        cycles, cycles_edges = parse_file(cycles_file)

        graph_file.close()
        basic_paths_file.close()
        paths_file.close()
        cycles_file.close()

        node_coverage_file = open(node_coverage_filename, 'w')
        edge_coverage_file = open(edge_coverage_filename, 'w')
        edge_pair_coverage_file = open(edge_pair_coverage_filename, 'w')

        # write beginning of each .dat file
        print_header(node_coverage_file, len(get_nodes_from_edges(graph_edges)))
        print_header(edge_coverage_file, len(graph_edges))
        print_header(edge_pair_coverage_file, len(get_edge_pairs_from_edges(graph_edges)))

        # combine paths and graphs
        paths_with_cycles = combine_paths_with_cycles(paths, cycles)

        # write the data of each .dat file
        path_index = 0
        for path in paths_with_cycles:
            edges = get_path_edges(path)
            weight = len(path)
            print_path_info(node_coverage_file, path_index, path, weight, path_node_coverage(path))
            print_path_info(edge_coverage_file, path_index, path, weight, path_edge_coverage(edges, path))
            print_path_info(edge_pair_coverage_file, path_index, path, weight, path_edge_pair_coverage(edges, path))
            path_index += 1

        # write ending of each .dat file
        print_footer(node_coverage_file)
        print_footer(edge_coverage_file)
        print_footer(edge_pair_coverage_file)

        node_coverage_file.close()
        edge_coverage_file.close()
        edge_pair_coverage_file.close()

    else:
        print("path_generation expects arguments: <graph edges> <basic paths file> <cycles file> <paths file> <node coverage output file> <edge coverage output file> <edge-pair coverage output file>")
