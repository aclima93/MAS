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


def minimum_distance(dist, q):
    vertex = -1
    min_dist = float("inf")
    for v in q:
        if dist[v] < min_dist:
            min_dist = dist[v]
            vertex = v
    return vertex

def dijkstra(graph, edges, vertices, source, target):

    paths = []

    # TODO: este range tem de ser algum tipo número de vértices usados?
    for iteration in range(0, 1):

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
                paths.append(previous)
                break

            q.remove(u)

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


def list_path_from_dict_path(dict_path, source, target):

    node = target
    list_path = []
    while node is not None and node is not source:
        print(node)
        list_path.append(node)
        node = dict_path[node]

    list_path.append(source)
    list_path.reverse()  # actual order
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
            path = list_path_from_dict_path(path, source, target)
            print(path)

            # number of vertices traverssed
            weight = calculate_path_weight(path)

            if weight < min_weight:
                min_weight = weight
                solutions = [path]

            elif weight == min_weight:
                solutions.append(path)

        output_file.write(str(solutions))

        input_file.close()
        output_file.close()

    else:
        print("shortest_path expects arguments: <input file>")
