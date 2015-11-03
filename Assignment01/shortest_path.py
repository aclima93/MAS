__authors__ = 'aclima, ilpetronilho, pjaneiro'

import sys


# create graph from input file node pairs
def create_graph(input_file):
    graph = {}
    edges = []
    vertices = []

    for line in input_file.readlines():
        node1, node2 = line.rstrip().lstrip().split()  # remove right and left whitespace then split

        node1 = int(node1)
        node2 = int(node2)

        if graph.get(node1):
            graph[node1].append(node2)
        else:
            graph[node1] = [node2]

        edges.append([node1, node2])

        if node1 not in vertices:
            vertices.append(node1)
        if node2 not in vertices:
            vertices.append(node2)

    return graph, edges, vertices

'''
number of nodes it contains, including the source and terminal nodes
'''
def calculate_path_weight(path):
    num_nodes_traversed = len(path)  # number of nodes traversed
    num_unique_nodes = len(set(path))  # number of unique nodes traversed
    weight = num_unique_nodes - (num_nodes_traversed - num_unique_nodes)  # penalize paths that repeat nodes
    return weight


def list_path_from_dict_path(dict_path, source, target):
    node = target
    list_path = []
    while node is not None and node is not source:
        list_path.append(node)
        node = dict_path[node]

    list_path.append(source)
    list_path.reverse()  # actual order
    return list_path


def visit_neighbours_acyclic(graph, available_edges, paths, path, node, target):

    if graph[node] is not None:
        for neighbour in graph[node]:
            edge = [node, neighbour]
            if edge in available_edges:
                # do
                available_edges.remove(edge)
                path.append(neighbour)
                paths = visit_neighbours_acyclic(graph, available_edges, paths, path.copy(), neighbour, target)
                # undo
                path = path[:-1]
                available_edges.append(edge)

            else:
                # do
                path.append(neighbour)
                paths = visit_neighbours_acyclic(graph, available_edges, paths, path.copy(), neighbour, target)
                # undo
                path = path[:-1]

    else:
        paths.append(path)

    return paths

def visit_neighbours(graph, paths, path, node, target):

    if graph[node] is not None:
        for neighbour in graph[node]:

            # do
            path.append(neighbour)
            paths = visit_neighbours(graph, paths, path.copy(), neighbour, target)

            # undo
            path = path[:-1]
    else:
        paths.append(path)

    return paths


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


def print_path(path, edges):

    output_file.write("Path: " + str(path) + '\n')
    output_file.write("Length: " + str(len(path)) + '\n')
    output_file.write("NC: " + str(node_coverage(path)) + '\n')
    output_file.write("EC: " + str(edge_coverage(edges, path)) + '\n')
    output_file.write("EPC: " + str(edge_pair_coverage(edges, path)) + '\n')
    output_file.write('\n')


def find_all_solutions(graph, edges, vertices, source, target, output_file):

    # find basis edges
    non_basic_edges = []
    min_paths_from_node_to_target = []
    for node in vertices[:-1]:  # exclude the terminal node to itself
        min_paths_from_node_to_target.append( shortest_path_in_paths( visit_neighbours(graph, [], [node], node, target)))

        first_edge = min_paths_from_node_to_target[node][0:2]
        if first_edge not in non_basic_edges:
            non_basic_edges.append(first_edge)

    basis_edges = get_basis_edges(edges, non_basic_edges)

    # generate all acyclic paths
    paths = visit_neighbours_acyclic(graph, basis_edges, [], [source], source, target)

    output_file.write("Vertices: " + str(vertices) + "\n")
    output_file.write("Edges: " + str(edges) + "\n")
    output_file.write("Non-Basic Edges: " + str(non_basic_edges) + "\n")
    output_file.write("Basis Edges: " + str(basis_edges) + "\n")

    output_file.write("\n\nAll Paths: \n")
    for path in paths:
        print_path(path, edges)

    output_file.write("\n\nShortest Path: \n")
    print_path( shortest_path_in_paths( paths), edges)


def shortest_path_in_paths(paths):

    shortest_path = paths[0]
    for path in paths[1:]:
        if len(path) < len(shortest_path):
            shortest_path = path

    return shortest_path

def get_basis_edges(edges, non_basic_edges):
    basis_edges = []
    for edge in edges:
        if edge not in non_basic_edges:
            basis_edges.append(edge)
    return basis_edges


if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 2:
        input_file = sys.argv[1]
        output_file = str(input_file) + str(".txt")

        input_file = open(input_file, 'r')
        graph, edges, vertices = create_graph(input_file)
        input_file.close()

        # start and end nodes of our graph are defined by the corresponding minimum and maximum node numbers
        vertices.sort()
        source = vertices[0]
        target = vertices[-1]
        graph[target] = None

        # find solutions and write solutions
        output_file = open(output_file, 'w')

        # all paths without contraints
        find_all_solutions(graph, edges, vertices, source, target, output_file)

        output_file.close()

    else:
        print("shortest_path expects arguments: <input file>")
