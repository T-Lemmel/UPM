/* Creación de una zona de memoria compartida */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "common.h"  // Fichero que contiene la información común (clave y estructura de datos)

int main(void) {
    int shmid;
    datos *zona_comun;

    // Crear una zona de memoria compartida
    shmid = shmget(CLAVE_SHM, sizeof(datos), IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget");
        exit(EXIT_FAILURE);
    }

    // Adjuntar la zona de memoria compartida al espacio de direcciones del proceso
    zona_comun = (datos*) shmat(shmid, 0, 0);
    if (zona_comun == (void*) -1) {
        perror("shmat");
        exit(EXIT_FAILURE);
    }

    // Inicializar los datos en la zona de memoria compartida
    zona_comun->unEntero = 123;
    zona_comun->unFloat = 1.23;
    strcpy(zona_comun->unArray, "hola mundo");

    // Desvincular la zona de memoria compartida
    if (shmdt(zona_comun) == -1) {
        perror("shmdt");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}