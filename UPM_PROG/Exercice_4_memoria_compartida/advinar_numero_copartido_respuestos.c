#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>

#define CLAVE_SHM 1234 // Shared memory key

typedef struct {
    int turno;           // 1 for process 1 (guesser), 2 for process 2 (answerer)
    int intento;         // The guess number
    char respuesta[15];  // Response: "bigger", "smaller", "guessed"
} datos;

int main(void) {
    int shmid; // Shared memory id
    datos *zona_comun; // Variable holding the shared memory content
    int target_number; 

    // Create the shared memory
    shmid = shmget(CLAVE_SHM, sizeof(datos), IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget");
        exit(EXIT_FAILURE);
    }

    // Attach the shared memory
    zona_comun = (datos*) shmat(shmid, 0, 0);
    if (zona_comun == (void*) -1) {
        perror("shmat");
        exit(EXIT_FAILURE);
    }

    // Generate a random number between 0 and 100
    srand(getpid()); // Seed the random number generator
    target_number = rand() % 101; // Random number between 0 and 100
    printf("Process 2 (Answerer): Chose the number %d\n", target_number);

    // Set the initial turn to process 1
    zona_comun->turno = 1;

    // Loop to respond to guesses
    while (1) {
        // Busy waiting: wait for the guess
        while (zona_comun->turno != 2) { /* busy waiting */ }

        // Read the guess
        printf("Process 2 (Answerer): Received guess %d\n", zona_comun->intento);
        if (zona_comun->intento > target_number) {
            strcpy(zona_comun->respuesta, "smaller");
        } else if (zona_comun->intento < target_number) {
            strcpy(zona_comun->respuesta, "bigger");
        } else {
            strcpy(zona_comun->respuesta, "guessed");
            printf("Process 2: Process 1 guessed the correct number!\n");
            break;
        }

        // Give the turn back to process 1
        zona_comun->turno = 1;
    }
    
    // Detach the shared memory and remove it
    if (shmdt(zona_comun) == -1) {
        perror("shmdt");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}
