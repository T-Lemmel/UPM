import rub_cube as rb
import networkx as nx
import random
import heapq

class RubiksCube:
    def __init__(self):
        """Initialize the Rubik's cube with the solved state, it is a list of 54 integers."""
        self.state = [
            *[0] * 9,  # Face 0
            *[1] * 9,  # Face 1
            *[2] * 9,  # Face 2
            *[3] * 9,  # Face 3
            *[4] * 9,  # Face 4
            *[5] * 9   # Face 5
        ]

    def __lt__(self, other):
        """Define comparison based on the f_cost (g_cost + heuristic), needed to use heapq."""
        return self.f_cost < other.f_cost

    def rotate_x(self, n, is_positive):
        """Rotate the cube around the X axis by 90 degrees in the positive or negative direction."""
        # Indices of relevant pieces for an X rotation (found analyzing the geometry of the cube)
        rows = [
            [45 + 3 * n, 46 + 3 * n, 47 + 3 * n],  # Face 4 row 2-n
            [n, 3 + n, 6 + n],                    # Face 0 col n
            [51 - 3 * n, 52 - 3 * n, 53 - 3 * n], # Face 5 row n
            [29 - n, 26 - n, 23 - n]              # Face 2 col 2-n
        ]

        if is_positive:
            self._rotate_pieces(rows, [1, 2, 3, 0])
        else:
            self._rotate_pieces(rows, [3, 0, 1, 2])

    def rotate_y(self, n, is_positive):
        """Rotate the cube around the Y axis by 90 degrees in the positive or negative direction."""
        # Indices of relevant pieces for a Y rotation (found analyzing the geometry of the cube)
        cols = [
            [36 + n, 39 + n, 42 + n],  # Face 4 col 2-n
            [9 + n, 12 + n, 15 + n],   # Face 1 col 2-n
            [36 + 6 - n, 39 + 6 - n, 42 + 6 - n], # Face 5 col 2-n
            [27 + n, 30 + n, 33 + n]   # Face 3 col n
        ]

        if is_positive:
            self._rotate_pieces(cols, [3, 0, 1, 2])
        else:
            self._rotate_pieces(cols, [1, 2, 3, 0])

    def rotate_z(self, n, is_positive):
        """Rotate the cube around the Z axis by 90 degrees in the positive or negative direction."""
        # Indices of relevant pieces for a Z rotation (found analyzing the geometry of the cube)
        rows = [
            [27 + 3 * n, 28 + 3 * n, 29 + 3 * n],  # Face 3 row n
            [n, 1 + n, 2 + n],                    # Face 0 row n
            [9 + n, 10 + n, 11 + n],              # Face 1 row n
            [18 + n, 19 + n, 20 + n]              # Face 2 row n
        ]

        if is_positive:
            self._rotate_pieces(rows, [3, 0, 1, 2])
        else:
            self._rotate_pieces(rows, [1, 2, 3, 0])

    def _rotate_pieces(self, groups, order):
        """Rotate pieces in the specified order for the given groups, e.g. [1, 2, 3, 0] becomes [2, 3, 0, 1] or [0, 1, 2, 3]."""
        temp = [self.state[idx] for idx in groups[order[0]]]
        for i in range(3):
            for j in range(3):
                self.state[groups[order[i]][j]] = self.state[groups[order[i + 1]][j]]
        for j in range(3):
            self.state[groups[order[-1]][j]] = temp[j]


def heuristic(current_state, goal_state):
    """Optimistic heuristic for the Rubik's cube-like problem.
    The heuristic calculates the minimum number of moves to place each piece in its target face using the sum of all the manhattan distance for the misplaced tiles.

    If the piece is in the correct face but wrong position, 1 move.
    If the piece is in the opposite face, 2 moves.
    """
    manhattan_distance = 0
    face_opposites = {0: 2, 1: 3, 2: 0, 3: 1, 4: 5, 5: 4}  # Mapping of opposite faces

    # Step 1: Identify the target faces for each piece in the goal state
    goal_face_positions = {i: [] for i in range(6)}  # List of positions for each face in the goal state
    for i in range(6):  # For each face (0-5)
        for j in range(9):  # For each position on the face (9 positions)
            value = goal_state[j + i * 9]
            goal_face_positions[value].append(i * 9 + j)  # Store target positions by face
    # Step 2: Calculate the Manhattan distance
    for i in range(6):  # Loop through each face
        for j in range(9):  # Loop through each position on the face
            # Get the current piece's value in the current state
            current_value = current_state[j + i * 9]
            
            if current_value != goal_state[j + i * 9]:  # The piece is misplaced
                target_faces = goal_face_positions[current_value]  # Get the target faces for this value
                
                # Find the closest target face for the current piece
                closest_target_face = min(target_faces, key=lambda x: abs(x // 9 - i))  # Min distance on the faces

                # Check if the piece is on the opposite face or adjacent face
                if closest_target_face // 9 == face_opposites[i]:
                    manhattan_distance += 2  # Piece is on the opposite face
                else:
                    manhattan_distance += 1  # Piece is on an adjacent face

    return manhattan_distance

            
def expand_cube_states_A_star(start_cube, goal_cube, max_depth):
    graph = nx.DiGraph()
    visited = set()
    queue = []
    start_state = start_cube.state
    goal_state = goal_cube.state

    heapq.heappush(queue, (heuristic(start_state, goal_state), 0, start_state)) # f_cost, g_cost, state

    moves = [
        (lambda c: c.rotate_x(0, True), "rotate_90('x',0,1)"),
        (lambda c: c.rotate_x(0, False), "rotate_90('x',0,-1)"),
        (lambda c: c.rotate_y(0, True), "rotate_90('y',0,1)"),
        (lambda c: c.rotate_y(0, False), "rotate_90('y',0,-1)"),
        (lambda c: c.rotate_z(0, True), "rotate_90('z',0,1)"),
        (lambda c: c.rotate_z(0, False), "rotate_90('z',0,-1)"),
        (lambda c: c.rotate_x(1, True), "rotate_90('x',1,1)"),
        (lambda c: c.rotate_x(1, False), "rotate_90('x',1,-1)"),
        (lambda c: c.rotate_y(1, True), "rotate_90('y',1,1)"),
        (lambda c: c.rotate_y(1, False), "rotate_90('y',1,-1)"),
        (lambda c: c.rotate_z(1, True), "rotate_90('z',1,1)"),
        (lambda c: c.rotate_z(1, False), "rotate_90('z',1,-1)"),
        (lambda c: c.rotate_x(2, True), "rotate_90('x',2,1)"),
        (lambda c: c.rotate_x(2, False), "rotate_90('x',2,-1)"),
        (lambda c: c.rotate_y(2, True), "rotate_90('y',2,1)"),
        (lambda c: c.rotate_y(2, False), "rotate_90('y',2,-1)"),
        (lambda c: c.rotate_z(2, True), "rotate_90('z',2,1)"),
        (lambda c: c.rotate_z(2, False), "rotate_90('z',2,-1)")
    ]

    while queue:
        f_cost, g_cost, current_state = heapq.heappop(queue) 
        if tuple(current_state) in visited: # Skip if already visited
            continue
        visited.add(tuple(current_state))
        graph.add_node(tuple(current_state))

        if current_state == goal_state: # Goal state found
            print("Goal state found at depth", g_cost)
            break

        if g_cost >= max_depth: # Skip if max depth reached
            continue

        for move, move_desc in moves:
            new_cube = RubiksCube()
            new_cube.state = current_state.copy()
            move(new_cube)
            new_state = new_cube.state
        
            if tuple(new_state) not in visited:
                new_g_cost = g_cost + 1
                new_f_cost = new_g_cost + heuristic(new_state, goal_state)
                heapq.heappush(queue, (new_f_cost, new_g_cost, new_state)) # f_cost, g_cost, state
                graph.add_edge(tuple(current_state), tuple(new_state), move=move_desc)

    return graph

def main(number_of_random_moves, max_depth):
    # Initialize the cubes
    solved_cube = RubiksCube()
    start_cube = RubiksCube()    

    # Randomize the start state
    for _ in range(number_of_random_moves):
        move = random.choice([start_cube.rotate_x, 
                    start_cube.rotate_y, 
                    start_cube.rotate_z])
        move(random.randint(0, 2), random.choice([True, False]))

    # Solve the cube
    print("starting to explore the state space pls wait, restart with fewer random moves if it takes too long")
    state_graph = expand_cube_states_A_star(solved_cube, start_cube, max_depth)
    print(f"Number of nodes: {state_graph.number_of_nodes()}")
    print(f"Number of edges: {state_graph.number_of_edges()}")

    # Check if the path exists
    try:
        path = nx.shortest_path(state_graph, tuple(solved_cube.state), tuple(start_cube.state))
        print(f"Shortest path from solved to start: {path}")

        # Run the path in solved-to-unsolved direction first (to have the start state stored in b and then run the moves in reverse to display the path)
        b = rb.RubCube()
        moves_list = []
        for i in range(len(path) - 1):
            move = state_graph.edges[path[i], path[i + 1]]['move'] # 'move' describes the movement along the edge
            print(f"Move {i + 1}: {move}")
            eval(f"b.{move}") # Execute the move
            moves_list.append(move)
        b.plot()

        # Run the path in unsolved-to-solved direction
        moves_list_reversed = moves_list[::-1]
        for move in moves_list_reversed:
            if move.endswith("1)"):
                inverse_move = move.replace("1)", "-1)") # Invert the direction of the move eg rotate_90('x',0,1) -> rotate_90('x',0,-1)

            print(f"Inverse move: {inverse_move}")
            eval(f"b.{inverse_move}")
            b.plot()

    except nx.NetworkXNoPath:
        print("No path found from start to solved state.")

if __name__ == "__main__":
    """Run the main function with the number of random moves and max depth desired."""
    number_of_random_moves = 3
    max_depth = 5
    main(number_of_random_moves, max_depth)
