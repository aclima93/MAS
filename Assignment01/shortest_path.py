__author__ = 'aclima'

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


def minimum_distance(dist, Q):
    vertex = -1
    min_dist = float("inf")
    for v in Q:
        if dist[v] < min_dist:
            min_dist = dist[v]
            vertex = v
    return vertex;

def dijkstra(graph, edges, vertices, source, target):

    paths = []

    # TODO: este range tem de ser algum tipo número de vértices usados?
    for iteration in range(1):

        dist = dict()
        previous = dict()

        for vertex in vertices:
            dist[vertex] = float("inf")
            previous[vertex] = None

        dist[source] = 0
        Q = set(vertices)

        while len(Q) > 0:
            u = minimum_distance(dist, Q)

            # terminate if we reach the target
            if u == target:
                paths.append(previous)
                break

            Q.remove(u)

            if dist[u] == float('inf'):
                break

            neighbours = graph[u]
            for vertex in neighbours:
                alt = dist[u] + 1  # dist_between(graph, u, vertex) is always 1
                if alt < dist[vertex]:
                    dist[vertex] = alt
                    previous[vertex] = u

        paths.append(previous)

    return paths

# number of nodes it contains, including the source and terminal nodes
def calculate_path_weight(path):
    return len(set(path))  # set removes duplicates


def list_path_from_dict_path(dict_path, source):

    reversed_dict = {}
    for key, vals in dict_path.items():
        if vals is not None:
            if vals
            for val in vals:
                reversed_dict[val] = key

    print(reversed_dict)

    node = source
    list_path = []
    while node is not None:
        print(node)
        list_path.append(node)
        node = reversed_dict[node]
    return list_path


if __name__ == '__main__':

    argc = len(sys.argv)  # program name also counts

    # input file
    if argc == 2:
        input_file = sys.argv[1]
        output_file = str(input_file) + str(".txt")

        input_file = open(input_file, 'r')
        output_file = open(output_file, 'w')

        graph, edges, vertices = create_graph(input_file)

        # start and end nodes of our graph are defined by the corresponding minimum and maximum node numbers
        vertices.sort()
        source = vertices[0]
        target = vertices[-1]

        # find solutions
        paths = dijkstra(graph, edges, vertices, source, target)
        solutions = []
        min_weight = len(vertices) + 1  # no shortest path can traverse more than the number of vertices

        print(paths)

        for path in paths:

            print(path)
            path = list_path_from_dict_path(path, source)
            print(path)

            # number of vertices traverssed
            weight = calculate_path_weight(path)

            if weight < min_weight:
                min_weight = weight
                solutions = [path]

            elif weight == min_weight:
                solutions.append(path)

        input_file.close()
        output_file.close()

    else:
        print("shortest_path expects arguments: <input file>")

