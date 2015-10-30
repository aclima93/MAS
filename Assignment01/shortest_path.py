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


def minimum_distance(dist, q):
    vertex = -1
    min_dist = float("inf")
    for v in q:
        if dist[v] < min_dist:
            min_dist = dist[v]
            vertex = v
    return vertex

def dijkstra(graph, edges, vertices, source, target):

    dist = dict()
    previous = dict()

    for vertex in vertices:
        dist[vertex] = float("inf")
        previous[vertex] = None

    dist[source] = 0
    q = set(vertices)

    while len(q) > 0:
        u = minimum_distance(dist, q)

        # terminate if we reach the target
        if u == target:
            return previous

        q.remove(u)

        if dist[u] == float('inf'):
            break

        neighbours = graph[u]
        for vertex in neighbours:
            alt = dist[u] + 1  # dist_between(graph, u, vertex) is always 1
            if alt < dist[vertex]:
                dist[vertex] = alt
                previous[vertex] = u

    return previous


# number of nodes it contains, including the source and terminal nodes
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

def find_dijkstra_solution(graph, edges, vertices, source, target, output_file):

    path = dijkstra(graph, edges, vertices, source, target)
    path = list_path_from_dict_path(path, source, target)

    output_file.write("\n\nDijkstra Shortest Path: " + str(path) + '\n')
    output_file.write("Dijkstra Shortest Path Weight: " + str(calculate_path_weight(path)) + '\n')


def visit_neighbours(graph, paths, path, node, target):

    if graph[node] is not None:
        for neighbour in graph[node]:
            path.append(neighbour)
            paths = visit_neighbours(graph, paths, path.copy(), neighbour, target)
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

    for i in range(len(path)-1):
        edge = [path[i], path[i+1]]
        if edge in edges:
            counter = counter + 1

    return counter


# calculates edge-pair coverage
def edge_pair_coverage(edges, path):
    counter = 0

    for i in range(len(path)-2):
        left_edge = [path[i], path[i+1]]
        right_edge = [path[i+1], path[i+2]]
        if (left_edge in edges) and (right_edge in edges):
            counter = counter + 1

    return counter

def find_all_solutions(graph, edges, vertices, source, target, output_file):

    paths = visit_neighbours(graph, [], [source], source, target)

    output_file.write("\n\nAll Paths: \n")
    for path in paths:
        output_file.write("Path: " + str(path) + '\n')
        output_file.write("NC: " + str(node_coverage(path)) + '\n')
        output_file.write("EC: " + str(edge_coverage(edges, path)) + '\n')
        output_file.write("EPC: " + str(edge_pair_coverage(edges, path)) + '\n')
        output_file.write('\n')




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

        # shortest path (dijkstra)
        find_dijkstra_solution(graph, edges, vertices, source, target, output_file)

        find_all_solutions(graph, edges, vertices, source, target, output_file)

        # largest path (ford-fulkerson)

        output_file.close()

    else:
        print("shortest_path expects arguments: <input file>")
