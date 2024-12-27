import networkx as nx
from itertools import product
import magiccube as mc

def create_graph():
    G = nx.Graph()

    # Step 1: Add all nodes
    nodes = list(product(range(4), repeat=9))  # Generate all combinations for 9 variables
    G.add_nodes_from(nodes)

    # Step 2: Add all edges
    for node in nodes:
        print(node)
        for r in range(9):  # Iterate over each position in the node
            new_angles = list(node)
            new_angles[r] = (new_angles[r] + 1) % 4
            neighbor = tuple(new_angles)
            G.add_edge(node, neighbor, weight=1)

    return G


def solve_rubixcube(start_rubixcube, end_rubixcube):
    start = tuple(start_rubixcube)
    end = tuple(end_rubixcube)
    path = nx.shortest_path(graph, source=start, target=end)
    return path


def visualize_rubixcube(graph, node):
    node = tuple(node)
    neighbors = list(graph.neighbors(node))

    for i, neighbor in enumerate(neighbors):
        print(f"Neighbor {i}: {neighbor}")

def show_solution(path_to_start):
    moves = {1: "1F", 2: "2F", 3: "3F", 4: "1L", 5: "2L", 6: "3L", 7: "1D", 8: "2D", 9: "3D"}
    cube = mc.Cube(3,"YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")

    moves_in_order = []

    # First take the path in reverse order to by able to print the start state for visualization purposes
    for i in range(len(path_to_start) - 1):
        for j in range(9):
            if path_to_start[i][j] != path_to_start[i + 1][j]:
                difference = path_to_start[i + 1][j] - path_to_start[i][j]
                if difference == 3:
                    difference = -1
                move = moves[j+1]
                if difference ==-1:
                    move += "'"
                cube.rotate(move)
                moves_in_order.append(move)

    print("Start state")
    print(cube)    
    
    # Take the path reversed as the solution
    reverse_moves = moves_in_order[::-1]
    for i,move in enumerate(reverse_moves):
        if "'" in move:
            move = move.replace("'", "")
        else:
            move += "'"
        print("Move:", move)
        cube.rotate(move)
        print(cube)

if __name__ == '__main__':
    graph = create_graph()
    start_rubixcube = [0, 0, 2, 0, 0, 1, 0, 2, 3]
    end_rubixcube = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    path_to_start = solve_rubixcube(end_rubixcube, start_rubixcube)
    show_solution(path_to_start)