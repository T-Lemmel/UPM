#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node, *ptree;

ptree createNode(int data) {
    ptree newNode = (ptree)malloc(sizeof(Node));
    if (!newNode) {
        printf("Memory error\n");
        return NULL;
    }
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

ptree insertNode(ptree root, int data) {
    if (root == NULL) {
        root = createNode(data);
    } else if (data < root->data) {
        root->left = insertNode(root->left, data);
    } else {
        root->right = insertNode(root->right, data);
    }
    return root;
}

ptree vec2tree(ptree root, int *v, int num_elem) {
    for (int i = 0; i < num_elem; i++) {
        root = insertNode(root, v[i]);
    }
    return root;
}

void tree2vec(ptree root, int *v, int *pos) {
    if (root != NULL) {
        tree2vec(root->left, v, pos);
        v[(*pos)++] = root->data;
        tree2vec(root->right, v, pos);
    }
}

void destruir(ptree *root) {
    if (*root != NULL) {
        destruir(&(*root)->left);
        destruir(&(*root)->right);
        free(*root);
        *root = NULL;
    }
}

void sort(int *v, int n) {
    ptree t = NULL;
    int pos = 0;
    t = vec2tree(t, v, n);
    tree2vec(t, v, &pos);
    destruir(&t);
}

int main() {
    int v[] = {5, 3, 8, 4, 2, 7, 1, 6,9,8,7,50,1,5,2,8,2,8,2,2,821,9,1,5,9,7,6,8,4,2,3,0,1};
    int n = sizeof(v) / sizeof(v[0]);

    sort(v, n);

    for (int i = 0; i < n; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");

    return 0;
}