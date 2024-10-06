/* Programa de ejemplo del uso de colas de mensajes -- consumidor */
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

/* Definición de la clave de la cola */
#define CLAVE_COLA 1

/* Estructura del mensaje */
struct msgbuf {
    long mtype;
    char mtext[15];
};

/* Función auxiliar que crea la cola, retornando el identificador */
int crearcola(int key) {
    int msgqid = msgget(key, IPC_CREAT | 0666);
    if (msgqid == -1) {
        perror("msgget");
        return -1;
    }
    return msgqid;
}

/* Función principal */
int main(void) {
    int id_cola, i, ret;
    struct msgbuf mensaje;

    /* Llamada a la función de creación de colas */
    id_cola = crearcola(CLAVE_COLA);
    if (id_cola == -1) {
        printf("No se ha podido crear la cola!\n");
        exit(EXIT_FAILURE);
    }

    /* Inicialización de los campos de la estructura */
    mensaje.mtype = 1;

    for (i = 0; i < 10; i++) {
        /* Lectura de datos de la cola */
        ret = msgrcv(id_cola, &mensaje, sizeof(mensaje.mtext), 1, 0);
        if (ret == -1) {
            perror("msgrcv");
            exit(EXIT_FAILURE);
        }
        printf("He recibido el mensaje: %s\n", mensaje.mtext);
    }

    /* Elimina la cola del sistema */
    ret = msgctl(id_cola, IPC_RMID, NULL);
    if (ret == -1) {
        perror("msgctl");
    } else {
        printf("La cola se ha cerrado correctamente\n");
    }

    return 0;
}
