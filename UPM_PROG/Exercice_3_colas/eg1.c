/* Programa de ejemplo del uso de colas de mensajes -- productor */
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
int crear_cola(int key) {
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
    id_cola = crear_cola(CLAVE_COLA);
    if (id_cola == -1) {
        printf("No se ha podido crear la cola!\n");
        exit(EXIT_FAILURE);
    }

    /* Inicialización de los campos de la estructura */
    mensaje.mtype = 1;

    for (i = 0; i < 10; i++) {
        sleep(1);
        sprintf(mensaje.mtext, "Mensaje %d", i);

        /* Envío del mensaje (introducción en la cola) */
        ret = msgsnd(id_cola, &mensaje, sizeof(mensaje.mtext), 0);
        if (ret == -1) {
            perror("msgsnd");
            exit(EXIT_FAILURE);
        }
        printf("He enviado el mensaje: %s\n", mensaje.mtext);
    }

    return 0;
}
