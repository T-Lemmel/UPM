#include <stdio.h>

void swap(int *a, int *b) { // swap the values of two integers
    int temp = *a;
    *a = *b;
    *b = temp;
}

int findMax(int arr[], int size) {
    if (size <= 0) return -1; // Handle empty arrays

    int max = arr[0];
    int max_index = 0;
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
            max_index = i;
        }
    }
    return max_index;
}

void recursiveSort(int arr[], int n) {

    if (n == 1) { // if the array has only one element the recursion stops
        return;
    }

    int max_index = findMax(arr, n); // find the index of the max element
    swap (&arr[max_index], &arr[n - 1]); // place the max element at the end by swapping with the one before
    recursiveSort(arr, n - 1); // sort the array from 0 to end - 1
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {5,4,8,9,7,2,1,3,6,3};
    int n = sizeof(arr) / sizeof(arr[0]); // length of the vector
    recursiveSort(arr, n);
    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}