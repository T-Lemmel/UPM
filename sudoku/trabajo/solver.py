import rub_cube as rb
import networkx as nx
from collections import deque
import random
import matplotlib.pyplot as plt
import heapq

class RubiksCube:
    def __init__(self):
        # Define the solved cube: each face is a 3x3 matrix with a uniform color
        self.faces = {
            '0': [
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]],  # Face 0

            '1': [
            [1, 1, 1], 
            [1, 1, 1], 
            [1, 1, 1]],  # Face 1

            '2': [
            [2, 2, 2], 
            [2, 2, 2], 
            [2, 2, 2]],  # Face 2
            
            '3': [
            [3, 3, 3], 
            [3, 3, 3], 
            [3, 3, 3]],  # Face 3
            
            '4': [
            [4, 4, 4], 
            [4, 4, 4], 
            [4, 4, 4]],  # Face 4
            
            '5': [
            [5, 5, 5], 
            [5, 5, 5], 
            [5, 5, 5]]   # Face 5
        }

    def __lt__(self, other):
        """Define comparison based on the f_cost (g_cost + heuristic)."""
        if not isinstance(other, RubiksCube):
            return NotImplemented
        # Compare by the f_cost, using the serialized state as a unique representation.
        return self.f_cost < other.f_cost

    def rotate_x(self, n, is_positive):
        
        # Extract face 4 row 2-n, face 0 col n, face 5 row n, and face 2 col 2-n
        face_4_row_2_n = self.faces['4'][2 - n][:]
        face_0_col_n = [self.faces['0'][i][n] for i in range(3)]
        face_5_row_n = self.faces['5'][n][:]
        face_2_col_2_n = [self.faces['2'][i][2-n] for i in range(3)]

        if is_positive :
            # Rotate the rows and columns
            for i in range(3):
                self.faces['4'][2 - n][i] = face_2_col_2_n[i]
                self.faces['0'][i][2-n] = face_4_row_2_n[i]
                self.faces['5'][n][i] = face_0_col_n[i]
                self.faces['2'][i][n] = face_5_row_n[i]
        else:
            # Rotate the rows and columns
            for i in range(3):
                self.faces['4'][2 - n][i] = face_0_col_n[i]
                self.faces['0'][i][2-n] = face_5_row_n[i]
                self.faces['5'][n][i] = face_2_col_2_n[i]
                self.faces['2'][i][n] = face_4_row_2_n[i]
        

    def rotate_y(self, n, is_positive):

        # Extract face 4 col 2-n, face 1 row 2-n, face 5 col 2-n, and face 3 col n
        face_4_col_2_n = [self.faces['4'][i][2 - n] for i in range(3)]
        face_1_col_2_n = [self.faces['1'][i][2 - n] for i in range(3)]
        face_5_col_2_n = [self.faces['5'][i][2 - n] for i in range(3)]
        face_3_col_n = [self.faces['3'][i][n] for i in range(3)]

        if is_positive:
            # Rotate the rows and columns
            for i in range(3):
                self.faces['4'][i][2 - n] = face_3_col_n[i]
                self.faces['1'][i][2 - n] = face_4_col_2_n[i]
                self.faces['5'][i][2 - n] = face_1_col_2_n[i]
                self.faces['3'][i][n] = face_5_col_2_n[i]
        else:
            # Rotate the rows and columns
            for i in range(3):
                self.faces['4'][i][2 - n] = face_1_col_2_n[i]
                self.faces['1'][i][2 - n] = face_5_col_2_n[i]
                self.faces['5'][i][2 - n] = face_3_col_n[i]
                self.faces['3'][i][n] = face_4_col_2_n[i]
        

    def rotate_z(self, n, is_positive):
        # Extract face 3 row n, face 0 row n, face 1 row n, and face 2 row n
        face_3_row_n = self.faces['3'][n][:]
        face_0_row_n = self.faces['0'][n][:]
        face_1_row_n = self.faces['1'][n][:]
        face_2_row_n = self.faces['2'][n][:]
        
        if is_positive:
            # Rotate the rows
            self.faces['3'][n] = face_2_row_n
            self.faces['0'][n] = face_3_row_n
            self.faces['1'][n] = face_0_row_n
            self.faces['2'][n] = face_1_row_n
        else:
            # Rotate the rows
            self.faces['3'][n] = face_0_row_n
            self.faces['0'][n] = face_1_row_n
            self.faces['1'][n] = face_2_row_n
            self.faces['2'][n] = face_3_row_n
        

def serialize_cube(cube):
    return "".join(
        "".join("".join(map(str, row)) for row in cube.faces[face])
        for face in sorted(cube.faces.keys())
    )


def heuristic(current_state, goal_state):
    # number of misplaced tiles
    return sum(1 for c, g in zip(current_state, goal_state) if c != g)

def expand_cube_states_A_star(start_cube, goal_cube, max_depth):
    graph = nx.DiGraph()
    visited = set()

    # Priority queue (using heapq for a min-heap)
    queue = []

    start_state = serialize_cube(start_cube)
    goal_state = serialize_cube(goal_cube)

    # Initially, add the start state to the queue (f_cost, g_cost, state, cube)
    heapq.heappush(queue, (heuristic(start_state, goal_state) + 0, 0, start_state, start_cube))  # (f_cost, g_cost, state, cube)

    iteration_count = 0

    # Mapping move functions and their descriptions
    moves = [
        (lambda c: c.rotate_x(0, True), "rotate_90('x',0,1)"),
        (lambda c: c.rotate_x(0, False), "rotate_90('x',0,-1)"),
        (lambda c: c.rotate_x(1, True), "rotate_90('x',1,1)"),
        (lambda c: c.rotate_x(1, False), "rotate_90('x',1,-1)"),
        (lambda c: c.rotate_x(2, True), "rotate_90('x',2,1)"),
        (lambda c: c.rotate_x(2, False), "rotate_90('x',2,-1)"),
        (lambda c: c.rotate_y(0, True), "rotate_90('y',0,1)"),
        (lambda c: c.rotate_y(0, False), "rotate_90('y',0,-1)"),
        (lambda c: c.rotate_y(1, True), "rotate_90('y',1,1)"),
        (lambda c: c.rotate_y(1, False), "rotate_90('y',1,-1)"),
        (lambda c: c.rotate_y(2, True), "rotate_90('y',2,1)"),
        (lambda c: c.rotate_y(2, False), "rotate_90('y',2,-1)"),
        (lambda c: c.rotate_z(0, True), "rotate_90('z',0,1)"),
        (lambda c: c.rotate_z(0, False), "rotate_90('z',0,-1)"),
        (lambda c: c.rotate_z(1, True), "rotate_90('z',1,1)"),
        (lambda c: c.rotate_z(1, False), "rotate_90('z',1,-1)"),
        (lambda c: c.rotate_z(2, True), "rotate_90('z',2,1)"),
        (lambda c: c.rotate_z(2, False), "rotate_90('z',2,-1)"),
    ]
    
    while queue:
        iteration_count += 1
        # Pop the item with the lowest f_cost (g_cost + h_cost)
        f_cost, g_cost, current_state, current_cube = heapq.heappop(queue)

        if current_state in visited:
            continue
        visited.add(current_state)

        graph.add_node(current_state)

        # Check if we've reached the goal state
        if current_state == goal_state:
            print(f"Goal state reached at depth {g_cost}")
            print("iteration count: ", iteration_count)
            graph.add_node(goal_state)  # Add the goal state to the graph
            break  # Stop after adding the goal state to the graph

        if g_cost >= max_depth:
            continue

        # Generate the next states
        next_states = []
        for move, move_description in moves:
            new_cube = RubiksCube()
            new_cube.faces = {face: [row[:] for row in current_cube.faces[face]] for face in current_cube.faces}
            move(new_cube)  # Apply the move to the new cube

            new_state = serialize_cube(new_cube)
            new_g_cost = g_cost + 1  # Increment the path length
            new_cube.f_cost = new_g_cost + heuristic(new_state, goal_state)  # f_cost = g_cost + h_cost
            next_states.append((new_g_cost + heuristic(new_state, goal_state), new_g_cost, new_state, new_cube))  # f_cost = g_cost + h_cost

            # Add the edges to the graph
            graph.add_edge(current_state, new_state, move=move_description)

        # Add all next states to the priority queue
        for next_state in next_states:
            heapq.heappush(queue, next_state)

    return graph

# Initialize the cube
solved_cube = RubiksCube()

# Define the start state with random moves
start_cube = RubiksCube()

# Apply random moves to the start state
for _ in range(6):
    random_move = random.choice([
        start_cube.rotate_x,
        start_cube.rotate_y,
        start_cube.rotate_z
    ])
    random_move(random.randint(0, 2), random.choice([True, False]))


# # Display the start state
print(f"Start state: {serialize_cube(start_cube)}")
# # Generate the graph of states

print("expanding from the solved state to the start state using A* with number of misplaces tiles heuristic")
state_graph = expand_cube_states_A_star(solved_cube, start_cube, max_depth=6)

# # Display basic graph information
print(f"Number of nodes (states): {state_graph.number_of_nodes()}")
print(f"Number of edges (moves): {state_graph.number_of_edges()}")

# Find the shortest path between the random state and the solved state
solved_state = serialize_cube(solved_cube)

# Check if the path exists
try:
    path = nx.shortest_path(state_graph, solved_state,serialize_cube(start_cube))
    print(f"Shortest path from start to solved state: {path}")

# Run the path in solved - Unsolved path first to have a starting point for displaying the moves
    b=rb.RubCube(3)
    moves_list = []
    for i in range(len(path)-1):
        move = state_graph.edges[path[i], path[i+1]]["move"]
        print(f"Move {i+1}: {move}")
        eval(f"b.{move}")
        moves_list.append(move)
    b.plot()

    # Run the path in Unsolved - Solved path
    moves_list_reversed = moves_list[::-1]
    for i in range(len(moves_list_reversed)):
        move = moves_list_reversed[i]
        if move[-2:] == "1)":
            move = move[:-2] + "-1)"
        else:
            move = move[:-3] + "1)"
        print(move)
        eval(f"b.{move}")
        b.plot()

except nx.NetworkXNoPath:
    print(f"No path found from {start_cube} to the solved state.")