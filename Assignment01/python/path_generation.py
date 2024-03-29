import itertools

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


def get_basis_edges(solutions_paths, solutions_edges, all_graph_edges):
    basis_edges = []
    non_basic_edges = []

    # get non-basic edges
    for solution_path_source_node, solution_path_dict in solutions_paths.items():
        for path_dict in solution_path_dict:
            first_edge = [solution_path_source_node, path_dict[solution_path_source_node]]
            if first_edge not in non_basic_edges:
                non_basic_edges.append(first_edge)

    # get basis_edges edges
    for edge in all_graph_edges:
        if edge not in non_basic_edges:  # basis edges are edges that are not non-basic
            if edge not in basis_edges:  # avoid duplicates
                basis_edges.append(edge)

    return basis_edges


def print_header(file, num_paths, max_coverage, min_coverage):
    file.write("data;\n")
    file.write("\n")
    file.write("/* Max. Coverage i.e. Coverage of the full graph */\n")
    file.write("param maxC := " + str(max_coverage) + ";\n")
    file.write("\n")
    file.write("/* Min. Coverage Percent. */\n")
    file.write("param minCP := " + min_coverage + ";\n")  # only this one has to be tweeked for testing purposes
    file.write("\n")
    file.write("/* Number of Paths */\n")
    file.write("param n := " + str(num_paths) + ";\n")
    file.write("\n")

def print_weight_set(file):
    file.write("\nparam w :=\n")

def print_weight_set_end(file):
    file.write(";\n")

def print_coverage_set(file, len_coverage):
    range_str = ""
    for i in range(1, len_coverage + 1):
        range_str += str(i) + " "
    file.write("\nparam f : " + range_str + " :=\n")

def print_coverage_set_end(file):
    file.write(";\n")

def print_footer(file):
    file.write("\nend;\n")

def print_path_coverage(file, path_index, path, path_edges, all_edges):

    # comments for better understanding of the .dat file
    file.write("/* Path: " + str(path) + '\n')
    file.write("Path Index: " + str(path_index) + " */\n")

    coverage = ""
    for edge in all_edges:
        if edge in path_edges:
            coverage += "1 "
        else:
            coverage += "0 "

    file.write(str(path_index) + " " + coverage + '\n')
    file.write('\n')

def print_path_weight(file, path_index, path, weight):

    # comments for better understanding of the .dat file
    file.write("/* Path: " + str(path) + '\n')
    file.write("Path Index: " + str(path_index) + " */\n")
    file.write(str(path_index) + " " + str(weight) + '\n')
    file.write('\n')


# parse edges from file
def parse_file(file, cycles_flag):

    paths = {}
    all_paths_edges = []
    edges_solution = []
    lines = file.readlines()

    for line in lines:

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
            if path not in dict_of_lists[dict_source]:
                dict_of_lists[dict_source].append(path)

    return dict_of_lists


def combine_paths_with_cycles(paths, cycles):

    # Paths
    paths_lists = get_dict_of_lists(paths)

    # Cycles
    cycles_lists = get_dict_of_lists(cycles)

    # Paths With Cycles
    paths_with_cycles = []
    for paths_lists_v in paths_lists.values():
        # example: path = {0: [0,1,4]} cycle = {1: [1,2,3]} result = 0,1,2,3,1,4
        for path in paths_lists_v:

            # path before adding cycles must also be included
            if path not in paths_with_cycles:
                paths_with_cycles.append(path)

            # check if this path shares a node with the cycles
            for cycles_lists_v in cycles_lists.values():

                relevant_cycles = []
                relevant_cycles_sources = []

                for cycle in cycles_lists_v:
                    for node in cycle:
                        if node in path:
                            relevant_cycles.append(cycle)
                            relevant_cycles_sources.append(node)
                            break

                # all combinations of cycles (through their indexes in the list)
                iterable = range(len(relevant_cycles))
                for s in range(len(iterable) + 1):
                    for comb in itertools.combinations(iterable, s):

                        resulting_path = path[:]

                        for cycle_index in comb:

                            cycles_source = relevant_cycles_sources[cycle_index]
                            common_node_index = resulting_path.index(cycles_source)  # index of shared node between cycle and path
                            cycle = relevant_cycles[cycle_index]

                            if common_node_index + 1 < len(resulting_path):
                                resulting_path = resulting_path[:common_node_index] + cycle + [cycles_source] + resulting_path[common_node_index + 1:]
                            else:
                                resulting_path = resulting_path[:common_node_index] + cycle + [cycles_source]

                            # avoid duplicates
                            if resulting_path not in paths_with_cycles:
                                paths_with_cycles.append(resulting_path)

    return paths_with_cycles


def get_path_edges(path):
    edges = []
    for i in range(len(path) - 1):
        edge = path[i:i + 2]
        if edge not in edges:
            edges.append(edge)

    return edges

def get_nodes_from_edges(edges):
    nodes = []
    for edge in edges:
        for node in edge:
            if node not in nodes:
                nodes.append(node)

    nodes.sort()
    return nodes

def get_edge_pairs_from_edges(edges):
    edge_pairs = []

    for edge1 in edges:
        for edge2 in edges:
            if not(edge1 == edge2):
                node11, node12 = edge1
                node21, node22 = edge2

                if (node12 == node21) and ([edge1, edge2] not in edge_pairs):
                    edge_pairs.append([edge1, edge2])
                if (node11 == node22) and ([edge2, edge1] not in edge_pairs):
                    edge_pairs.append([edge2, edge1])

    return edge_pairs


def parse_graph_file(lines):

    graph_edges = []
    for line in lines:
        node1, node2 = line.lstrip().rstrip().split()
        graph_edges.append([int(node1), int(node2)])

    graph_nodes = get_nodes_from_edges(graph_edges)
    graph_edge_pairs = get_edge_pairs_from_edges(graph_edges)

    return graph_nodes, graph_edges, graph_edge_pairs



if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 10:

        graph_filename = sys.argv[1]
        shortest_paths_filename = sys.argv[2]
        cycles_filename = sys.argv[3]
        paths_filename = sys.argv[4]
        node_coverage_filename = sys.argv[5]
        edge_coverage_filename = sys.argv[6]
        edge_pair_coverage_filename = sys.argv[7]
        paths_with_cycles_filename = sys.argv[8]
        partial_coverage_percentage = sys.argv[9]

        graph_file = open(graph_filename, 'r')
        shortest_paths_file = open(shortest_paths_filename, 'r')
        paths_file = open(paths_filename, 'r')
        cycles_file = open(cycles_filename, 'r')

        # load the computed data from the output files
        graph_nodes, graph_edges, graph_edge_pairs = parse_graph_file(graph_file.readlines())
        shortest_paths, shortest_paths_edges = parse_file(shortest_paths_file, False)
        paths, paths_edges = parse_file(paths_file, False)
        cycles, cycles_edges = parse_file(cycles_file, True)

        graph_file.close()
        shortest_paths_file.close()
        paths_file.close()
        cycles_file.close()

        # get the basis edges from
        basis_edges = get_basis_edges(shortest_paths, shortest_paths_edges, graph_edges)

        node_coverage_file = open(node_coverage_filename, 'w')
        edge_coverage_file = open(edge_coverage_filename, 'w')
        edge_pair_coverage_file = open(edge_pair_coverage_filename, 'w')

        # combine paths and graphs
        paths_with_cycles = combine_paths_with_cycles(paths, cycles)

        # only paths that have at most one occorrence of each basis edge are relevant
        for path in paths_with_cycles:
            edges = get_path_edges(path)

            for basis_edge in basis_edges:
                if edges.count(basis_edge) > 1:
                    paths_with_cycles.remove(path)
                    break

        # save relevant paths for easier access later on
        paths_with_cycles_file = open(paths_with_cycles_filename, 'w')
        for path in paths_with_cycles:
            edges = get_path_edges(path)

            # write the path's edges to the file
            for edge in edges:
                for node in edge:
                    paths_with_cycles_file.write(str(node) + " ")
                paths_with_cycles_file.write("\n")  # separate edges
            paths_with_cycles_file.write("\n")  # separate solutions
        paths_with_cycles_file.close()

        # write beginning of each .dat file
        num_paths = len(paths_with_cycles)
        print_header(node_coverage_file, num_paths, len(graph_nodes), partial_coverage_percentage)
        print_header(edge_coverage_file, num_paths, len(graph_edges), partial_coverage_percentage)
        print_header(edge_pair_coverage_file, num_paths, len(graph_edge_pairs), partial_coverage_percentage)

        # #
        # Coverage Data

        print_coverage_set(node_coverage_file, len(graph_nodes))
        print_coverage_set(edge_coverage_file, len(graph_edges))
        print_coverage_set(edge_pair_coverage_file, len(graph_edge_pairs))

        # write the coverage data to each .dat file
        path_index = 1
        for path in paths_with_cycles:
            edges = get_path_edges(path)
            nodes = get_nodes_from_edges(edges)
            edge_pairs = get_edge_pairs_from_edges(edges)

            # node coverage
            print_path_coverage(node_coverage_file, path_index, path, nodes, graph_nodes)

            # edge coverage
            print_path_coverage(edge_coverage_file, path_index, path, edges, graph_edges)

            # edge-pairs coverage
            print_path_coverage(edge_pair_coverage_file, path_index, path, edge_pairs, graph_edge_pairs)

            path_index += 1

        print_coverage_set_end(node_coverage_file)
        print_coverage_set_end(edge_coverage_file)
        print_coverage_set_end(edge_pair_coverage_file)

        # #
        # Weight Data

        print_weight_set(node_coverage_file)
        print_weight_set(edge_coverage_file)
        print_weight_set(edge_pair_coverage_file)

        # write the weight data to each .dat file
        path_index = 1
        for path in paths_with_cycles:
            weight = len(path)

            # node coverage
            print_path_weight(node_coverage_file, path_index, path, weight)

            # edge coverage
            print_path_weight(edge_coverage_file, path_index, path, weight)

            # edge-pairs coverage
            print_path_weight(edge_pair_coverage_file, path_index, path, weight)

            path_index += 1

        print_weight_set_end(node_coverage_file)
        print_weight_set_end(edge_coverage_file)
        print_weight_set_end(edge_pair_coverage_file)

        # write ending of each .dat file
        print_footer(node_coverage_file)
        print_footer(edge_coverage_file)
        print_footer(edge_pair_coverage_file)

        node_coverage_file.close()
        edge_coverage_file.close()
        edge_pair_coverage_file.close()

    else:
        print("path_generation expects arguments: <graph edges> <shortest paths file> <cycles file> <paths file> <node coverage output file> <edge coverage output file> <edge-pair coverage output file> <paths with cycles file> <partial coverage percentage>")
