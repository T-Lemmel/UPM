#ifndef COMMON_H
#define COMMON_H

#include <sys/types.h>

/* Clave de acceso a la zona de memoria compartida */
#define CLAVE_SHM ((key_t) 1001)

/* Estructura de datos que se comparte en la zona de memoria común */
typedef struct {
    int unEntero;       // Un entero
    float unFloat;      // Un flotante
    char unArray[10];   // Un array de caracteres de tamaño 10
} datos;

#endif // COMMON_H