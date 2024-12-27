import networkx as nx


def create_graph():
    G = nx.Graph()
    
    # Step 1: Add all nodes
    nodes = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    for m in range(4):
                        for n in range(4):
                            for o in range(4):
                                for p in range(4):
                                    for q in range(4):
                                        print(i, j, k, l, m, n, o, p, q)
                                        node = (i, j, k, l, m, n, o, p, q)
                                        nodes.append(node)
    G.add_nodes_from(nodes)
    
    # Step 2: Add all edges
    for node in nodes:
        for r in range(9):
            print(node)
            new_angles = list(node)
            new_angles[r] = (new_angles[r] + 1) % 4
            neighbor = tuple(new_angles)
            if neighbor in nodes and not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor, weight=1)
    
    return G


def solve_sudoku(start_sudoku):
    start = tuple(start_sudoku)
    end = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1])
    path = nx.shortest_path(graph, source=start, target=end)
    return path

def visualize_sudoku(graph,node):

    node = tuple(node)
    neighbors = list(graph.neighbors(node))
    
    for i, neighbor in enumerate(neighbors):
        print(f"Neighbor {i}: {neighbor}")

if __name__ == '__main__':
    graph = create_graph()
    visualize_sudoku(graph, [0, 1, 3, 2, 1, 3, 2, 1, 2])
    # start_sudoku = [0, 0, 0, 0, 0, 3, 0, 0, 0]
    # path = solve_sudoku(start_sudoku)
    # print(path)