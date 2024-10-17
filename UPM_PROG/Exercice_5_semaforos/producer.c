#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "common.h"

#define KEY 1234
#define BUFFER_SIZE 5

int main() {
    int semid;
    struct sembuf operation;

    // Create a set of three semaphores
    semid = semget(KEY, 3, IPC_CREAT | 0600);
    if (semid == -1) {
        perror("semget");
        exit(EXIT_FAILURE);
    }

    // Initialize semaphores: 
    // semaphore 0 (spaces) = BUFFER_SIZE (available spaces)
    // semaphore 1 (items) = 0 (no items at the start)
    // semaphore 2 (mutex) = 1 (for mutual exclusion)
    semctl(semid, 0, SETVAL, BUFFER_SIZE);
    semctl(semid, 1, SETVAL, 0);
    semctl(semid, 2, SETVAL, 1);

    int i = 0;
    while (1) {
        // Produce item
        printf("Producer producing item %d\n", i);

        // Wait if there are no spaces
        operation.sem_num = 0; // spaces semaphore
        operation.sem_op = -1; // attempt to decrement the semaphore, can't do it if it's not positive
        operation.sem_flg = 0;
        semop(semid, &operation, 1);

        // Mutual exclusion (wait for the mutex)
        operation.sem_num = 2; // mutex semaphore
        operation.sem_op = -1;
        semop(semid, &operation, 1);

        // Place item in buffer (simulated with a print)
        printf("Producer places item %d in buffer\n", i);
        pausa();
        i++;

        // Release mutual exclusion
        operation.sem_num = 2; // mutex semaphore
        operation.sem_op = 1;
        semop(semid, &operation, 1);

        // Signal that there is an available item
        operation.sem_num = 1; // items semaphore
        operation.sem_op = 1;
        semop(semid, &operation, 1);

        pausa();

    }

    return 0;
}
