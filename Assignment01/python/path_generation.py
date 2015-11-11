__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys
import re

DEBUG = False

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
    file.write("param maxC := " + str(max_coverage) + ";\n")
    file.write("\n")
    file.write("/* Max. Coverage Percent. */\n")
    file.write("param maxCP := " + str(100) + ";\n")
    file.write("param minCP := " + str(0) + ";\n")
    file.write("\n")
    file.write("/* Items: index, weight, coverage */\n")
    file.write("set I :=\n")

def print_footer(file):
    file.write(";\n\n end;\n")

def print_path_info(file, path_index, path, weight, coverage):

    # comments for better understanding of the .dat file
    file.write("/*\n")
    file.write("Path Index: " + str(path_index) + '\n')
    file.write("Path: " + str(path) + '\n')
    file.write("Weight: " + str(weight) + '\n')
    file.write("Coverage: " + str(coverage) + '\n')
    file.write("*/\n")
    file.write(str(path_index) + " " + str(weight) + " " + str(coverage) + '\n')
    file.write('\n')


# parse edges from file
def parse_file(file, cycles_flag):

    paths = {}
    all_paths_edges = []
    edges_solution = []
    lines = file.readlines()

    if DEBUG:
        print("filename: ")
        print(file.name)

    for line in lines:

        if DEBUG:
            print("line: ")
            print(line)

        # empty line
        if re.match("\n", line):

            # remove the last edge, we already know it cycles back to the source
            # and this way we can check what is the source of the cycle further on
            if cycles_flag:
                edges_solution = edges_solution[:-1]

            if edges_solution not in all_paths_edges:
                all_paths_edges.append(edges_solution)
            edges_solution = []

        # edge line
        elif re.match("(\d)+ (\d)+", line):
            node1, node2 = line.split()
            edges_solution.append( [int(node1), int(node2)] )

    if DEBUG:
        print("all_paths_edges: ")
        print(all_paths_edges)
        print("\n")

    # remove empty paths and order the rest
    for path_edges in all_paths_edges:

        if len(path_edges) == 0:
            all_paths_edges.remove(path_edges)
        else:
            path = {}
            for edge in path_edges:
                path[edge[0]] = edge[1]

            # the source node is the one key which does not appear in the values
            source_node = list(set(path.keys()) - set(path.values()))

            if len(source_node) == 1:
                source_node = source_node[0]

                if source_node in paths:
                    if path not in paths[source_node]:
                        paths[source_node].append(path)
                else:
                    paths[source_node] = [path]

    if DEBUG:
        print("paths: ")
        print(paths)
        print("\n")
        print("all_paths_edges: ")
        print(all_paths_edges)
        print("\n")

    return paths, all_paths_edges


def get_dict_of_lists(dict_of_dicts):

    dict_of_lists = {}
    for dict_source, dicts in dict_of_dicts.items():

        dict_of_lists[dict_source] = []
        for cur_dict in dicts:
            cur_node = dict_source  # source node
            path = []
            while cur_node in cur_dict:
                path.append(cur_node)
                cur_node = cur_dict[cur_node]

            path.append(cur_node)  # add target node
            dict_of_lists[dict_source].append(path)

    if DEBUG:
        print("dict_of_lists: ")
        print(dict_of_lists)
        print("\n")

    return dict_of_lists


def combine_paths_with_cycles(paths, cycles):

    if DEBUG:
        print("paths: ")
        print(paths)
        print("\n")
        print("cycles: ")
        print(cycles)
        print("\n")

    # #
    # Paths
    if DEBUG:
        print("paths_lists: ")
    paths_lists = get_dict_of_lists(paths)

    # #
    # Cycles
    if DEBUG:
        print("cycles_lists: ")
    cycles_lists = get_dict_of_lists(cycles)

    # #
    # Paths With Cycles
    paths_with_cycles = []
    for paths_lists_v in paths_lists.values():
        for cycles_source in cycles_lists.keys():

            # example: path = {0: [0,1,4]} cycle = {1: [1,2,3]} result = 0,1,2,3,1,4
            for path in paths_lists_v:

                if path not in paths_with_cycles:
                    paths_with_cycles.append(path)

                if cycles_source in path:

                    index = path.index(cycles_source)

                    for cycle in cycles_lists[cycles_source]:

                        if index + 1 < len(path):
                            resulting_path = path[:index] + cycle + [cycles_source] + path[index + 1:]
                        else:
                            resulting_path = path[:index] + cycle + [cycles_source]

                        # avoid duplicates
                        if resulting_path not in paths_with_cycles:
                            paths_with_cycles.append(resulting_path)

    if DEBUG:
        print("paths_with_cycles: ")
        print(paths_with_cycles)
        print("\n")

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
        basics_paths, basics_paths_edges = parse_file(basic_paths_file, False)
        paths, paths_edges = parse_file(paths_file, False)
        cycles, cycles_edges = parse_file(cycles_file, True)

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
