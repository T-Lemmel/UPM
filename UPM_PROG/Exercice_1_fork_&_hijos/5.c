#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h> 
#include <stdio.h>
#include <pwd.h> 

/* Variables globales */

/* Función principal */
int main(void) {
    int ppid; /* padre id */
    int pid1; /* hijo1 id */
    int pid2; /* hijo2 id */
    int Z = 0; /* variable que cambia entre los procesos */
    uid_t uid; /* user id */
    struct passwd *mipass; /* passwd es una estructura que presenta distintos campos con información del usuario */

    /* initial Z */

    printf("Hola, yo soy el padre, y tengo PID %d, para yo Z = %d\n", getpid(), Z);
    mipass = getpwuid(getuid());
    printf("Soy : %s \n", mipass->pw_gecos);
    printf("Mi login es: %s\n", mipass->pw_name);
    printf("Mi id es: %d \n", (int) (mipass->pw_uid));
    printf("Mi directorio de trabajo es: %s\n", mipass->pw_dir);
    printf("Mi shell es: %s\n\n", mipass->pw_shell);
    
    /* Creación de dos procesos hijos */
    switch (pid1 = fork()) {
        case (pid_t) -1:
            perror("fork");
            printf("Error en el fork del hijo 1\n");
            exit(-1);

        case (pid_t) 0:
            mipass = getpwuid(getuid());
            printf("Soy : %s \n", mipass->pw_gecos);
            printf("Mi login es: %s\n", mipass->pw_name);
            printf("Mi id es: %d \n", (int) (mipass->pw_uid));
            printf("Mi directorio de trabajo es: %s\n", mipass->pw_dir);
            printf("Mi shell es: %s\n", mipass->pw_shell);
            Z += 1;
            printf("Hola, yo soy el hijo 1, y tengo PID %d. Mi padre es el PID %d, my valor de Z = %d\n\n", getpid(), getppid(), Z);
            
            exit(0);

        default:
            switch (pid2 = fork()) {
                case (pid_t) -1:
                    perror("fork");
                    printf("Error en el fork del hijo 2\n");
                    exit(-1);

                case (pid_t) 0:
                    mipass = getpwuid(getuid());
                    printf("Soy : %s \n", mipass->pw_gecos);
                    printf("Mi login es: %s\n", mipass->pw_name);
                    printf("Mi id es: %d \n", (int) (mipass->pw_uid));
                    printf("Mi directorio de trabajo es: %s\n", mipass->pw_dir);
                    printf("Mi shell es: %s\n", mipass->pw_shell);
                    Z += 2;
                    printf("Hola, yo soy el hijo 2, y tengo PID %d. Mi padre es el PID %d, my valor de Z = %d\n\n", getpid(), getppid(), Z);
                    exit(0);
            }
            break;
    }
    exit(0);
}
