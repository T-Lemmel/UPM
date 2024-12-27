#include <igraph.h>
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;

igraph_t create_graph() {
    igraph_t graph;
    igraph_empty(&graph, 0, IGRAPH_UNDIRECTED);

    // Step 1: Add all nodes
    vector<tuple<int, int, int, int, int, int, int, int, int>> nodes;
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 4; ++k) {
                for (int l = 0; l < 4; ++l) {
                    for (int m = 0; m < 4; ++m) {
                        for (int n = 0; n < 4; ++n) {
                            for (int o = 0; o < 4; ++o) {
                                for (int p = 0; p < 4; ++p) {
                                    for (int q = 0; q < 4; ++q) {
                                        tuple<int, int, int, int, int, int, int, int, int> node = make_tuple(i, j, k, l, m, n, o, p, q);
                                        nodes.push_back(node);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    for (size_t i = 0; i < nodes.size(); ++i) {
        igraph_add_vertices(&graph, 1, 0);
    }

    // Step 2: Add all edges
    for (size_t i = 0; i < nodes.size(); ++i) {
        for (int r = 0; r < 9; ++r) {
            auto node = nodes[i];
            auto new_angles = node;
            get<r>(new_angles) = (get<r>(new_angles) + 1) % 4;
            auto it = find(nodes.begin(), nodes.end(), new_angles);
            if (it != nodes.end()) {
                int neighbor_index = distance(nodes.begin(), it);
                if (!igraph_are_connected(&graph, i, neighbor_index)) {
                    igraph_add_edge(&graph, i, neighbor_index);
                }
            }
        }
    }

    return graph;
}

void visualize_sudoku(igraph_t &graph, vector<int> node) {
    igraph_vector_t neighbors;
    igraph_vector_init(&neighbors, 0);

    int node_index = -1;
    for (int i = 0; i < igraph_vcount(&graph); ++i) {
        if (node == nodes[i]) {
            node_index = i;
            break;
        }
    }

    if (node_index != -1) {
        igraph_neighbors(&graph, &neighbors, node_index, IGRAPH_ALL);
        for (int i = 0; i < igraph_vector_size(&neighbors); ++i) {
            int neighbor_index = VECTOR(neighbors)[i];
            auto neighbor = nodes[neighbor_index];
            cout << "Neighbor " << i << ": ";
            for (int j = 0; j < 9; ++j) {
                cout << get<j>(neighbor) << " ";
            }
            cout << endl;
        }
    }

    igraph_vector_destroy(&neighbors);
}

int main() {
    igraph_t graph = create_graph();
    vector<int> node = {0, 1, 3, 2, 1, 3, 2, 1, 2};
    visualize_sudoku(graph, node);
    igraph_destroy(&graph);
    return 0;
}