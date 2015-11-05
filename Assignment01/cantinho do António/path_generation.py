__authors__ = 'aclima, ilpetronilho, pjaneiro'

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


# create graph from input file node pairs
def create_graph(input_file):
    graph = {}
    edges = []

    for line in input_file.readlines():
        node1, node2 = line.rstrip().lstrip().split()  # remove right and left whitespace then split

        node1 = int(node1)
        node2 = int(node2)

        if graph.get(node1):
            graph[node1].append(node2)
        else:
            graph[node1] = [node2]

        edges.append([node1, node2])

    return graph, edges


def combine_paths_with_cycles(paths, cycles):
    pass


if __name__ == '__main__':

    paths_file = open("paths.txt", 'r')
    cycles_file = open("cycles.txt", 'r')
    paths_with_cycles_file = open("paths_with_cycles.txt", 'w')

    paths, paths_edges = create_graph(paths_file)
    cycles, cycles_edges = create_graph(cycles_file)
    paths_file.close()
    cycles_file.close()

    paths_with_cycles = combine_paths_with_cycles(paths, cycles)

    for path, edges in paths_with_cycles:
        print_path(paths_with_cycles_file, path, edges)

    paths_with_cycles_file.close()
