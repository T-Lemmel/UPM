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
    char respuesta[15];  // Response from process 2: "bigger", "smaller", "guessed"
} datos;

int main(void) {
    int shmid; // Shared memory id
    datos *zona_comun; // Variable holding the shared memory content
    int max = 100, min = 0, guess;

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

    // Loop for guessing the number
    while (1) {
        // Busy waiting: wait for the turn
        while (zona_comun->turno != 1) { /* busy waiting */ }

        // Make a guess using dichotomy
        guess = (min + max) / 2;
        printf("Process 1 (Guesser): Guessing %d\n", guess);
        zona_comun->intento = guess;

        // Give the turn to process 2
        zona_comun->turno = 2;

        // Busy waiting: wait for the answer
        while (zona_comun->turno != 1) { /* busy waiting */ }

        // Check the response
        printf("Process 1 (Guesser): Response is %s\n", zona_comun->respuesta);
        if (strcmp(zona_comun->respuesta, "bigger") == 0) {
            min = guess + 1;
        } else if (strcmp(zona_comun->respuesta, "smaller") == 0) {
            max = guess - 1;
        } else if (strcmp(zona_comun->respuesta, "guessed") == 0) {
            printf("Process 1: Guessed the correct number: %d\n", guess);
            break;
        }
    }

    // Detach the shared memory
    if (shmdt(zona_comun) == -1) {
        perror("shmdt");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}
