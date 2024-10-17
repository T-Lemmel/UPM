#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "common.h"

#define KEY 1234

int main() {
    int semid;
    struct sembuf operation;

    // Get the semaphore set created by the producer
    semid = semget(KEY, 3, 0600);
    if (semid == -1) {
        perror("semget");
        exit(EXIT_FAILURE);
    }

    int consumed_items = 0;
    while (consumed_items < 10) {

        // Wait if there are no items
        operation.sem_num = 1; // item semaphore
        operation.sem_op = -1;
        operation.sem_flg = 0;
        semop(semid, &operation, 1);

        // Mutual exclusion (wait for the mutex)
        operation.sem_num = 2; // mutex semaphore
        operation.sem_op = -1;
        semop(semid, &operation, 1);

        // Consume item from the buffer
        printf("Consumer consumes item %d\n", consumed_items);
        printf("After consuming item %d, there are %d items in the buffer\n", consumed_items, semctl(semid, 1, GETVAL, 0));
        pausa();
        consumed_items++;

        // Release mutual exclusion
        operation.sem_num = 2; // mutex semaphore
        operation.sem_op = 1;
        semop(semid, &operation, 1);

        // Signal that there is an available slot
        operation.sem_num = 0; // slot semaphore
        operation.sem_op = 1;
        semop(semid, &operation, 1);
        
        pausa();


    }
    // Remove the semaphore set
    semctl(semid, 0, IPC_RMID, 0);

    return 0;
}
