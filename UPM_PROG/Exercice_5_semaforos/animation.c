#include <stdio.h>

#define BUFFER_SIZE 5
char buffer[BUFFER_SIZE];

// Function to print the current buffer state
void print_buffer() {
    printf("Buffer: ");
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if (buffer[i] == 'X') {
            printf("[X]");
        } else {
            printf("[ ]");
        }
    }
    printf("\n");
}

// Function to place an item in the buffer (used by producer)
void place_item(int index) {
    buffer[index] = 'X';
    print_buffer();
}

// Function to remove an item from the buffer (used by consumer)
void remove_item(int index) {
    buffer[index] = ' ';
    print_buffer();
}
