import networkx as nx
import matplotlib.pyplot as plt

# Create a more complex graph with nodes and weighted edges
G = nx.Graph()

# Add weighted edges to the graph using the format (node1, node2, weight)
edges = [
    (1, 2, 10), (1, 3, 15), (1, 4, 20), (2, 3, 35), (2, 5, 25),
    (3, 6, 30), (4, 6, 20), (4, 5, 15), (5, 6, 10), (5, 7, 5),
    (6, 7, 5), (7, 1, 50)
]
# Adds all edges and their weights to the graph
G.add_weighted_edges_from(edges)

# 1. TSP (Traveling Salesman Problem) using approximation
tsp_path = nx.approximation.traveling_salesman_problem(G, weight='weight')

# 2. CPP (Chinese Postman Problem) for non-Eulerian graphs
# Convert the graph into an Eulerian graph by adding extra edges where necessary
eulerian_graph = nx.eulerize(G)

# Generate the Eulerian circuit
cpp_circuit = list(nx.eulerian_circuit(eulerian_graph, source=1))

# 3. Shortest Path using A* algorithm
shortest_path = nx.astar_path(G, source=1, target=6, heuristic=lambda a, b: abs(a - b), weight='weight')


# Function to visually display the graph and highlight the TSP path, CPP circuit, and shortest path
def visualize_graph(G, tsp_path, cpp_circuit, shortest_path):
    pos = nx.spring_layout(G)  # Spring layout positions the nodes dynamically
    
    plt.figure(figsize=(12, 8))

    # Draw the base graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold')

    # Draw edge weights as labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight the TSP path in red with arrows showing the direction
    tsp_edges = [(tsp_path[i], tsp_path[i + 1]) for i in range(len(tsp_path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=tsp_edges, edge_color='red', width=2, arrows=True, arrowstyle='-|>', arrowsize=20, label="TSP Path")

    # Highlight the CPP circuit in blue with arrows showing the direction
    cpp_edges = [(u, v) for u, v in cpp_circuit]
    nx.draw_networkx_edges(G, pos, edgelist=cpp_edges, edge_color='blue', style='dashed', width=2, arrows=True, arrowstyle='-|>', arrowsize=20, label="CPP Circuit")

    # Highlight the Shortest Path in green with arrows showing the direction
    sp_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=sp_edges, edge_color='green', width=2, arrows=True, arrowstyle='-|>', arrowsize=20, label="Shortest Path (A*)")

    # Add a legend to distinguish between paths
    plt.legend(["TSP Path", "CPP Circuit", "Shortest Path (A*)"])
    plt.title("Graph Visualization with Direction of Travel for TSP, CPP, and Shortest Path")
    
    plt.show()


# Display results with explanations
def display_results(tsp_path, cpp_circuit, shortest_path):
    # Traveling Salesman Problem (TSP) result
    print("1. Traveling Salesman Problem (TSP) Approximate Path:")
    print(f"   Path: {tsp_path}")
    print(f"   Total Cost: {sum(G[tsp_path[i]][tsp_path[i+1]]['weight'] for i in range(len(tsp_path)-1))}")

    # Chinese Postman Problem (CPP) result
    print("\n2. Chinese Postman Problem (Eulerian Circuit):")
    print("   Circuit: ", [edge for edge in cpp_circuit])

    # Shortest Path (A*) result
    print("\n3. Shortest Path from Node 1 to Node 6 (using A*):")
    print(f"   Path: {shortest_path}")
    print(f"   Total Cost: {sum(G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))}")


# Call functions to display results and visualize the graph
display_results(tsp_path, cpp_circuit, shortest_path)
visualize_graph(G, tsp_path, cpp_circuit, shortest_path)
