/* Example program demonstrating the use of pipes */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    int fd[2];
    int status;
    int nread;
    char buffer[100];

    /* Create the pipe */
    if (pipe(fd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    printf("Pipe OK!\n");

    /* Create a child process */
    switch (fork()) {
        case -1:
            perror("fork");
            exit(EXIT_FAILURE);
        case 0:
            // This is the child process
            // Close the write descriptor of the pipe in the child process
            if (close(fd[1]) == -1) {
                perror("close");
            }

            // Read the information contained in the pipe
            nread = read(fd[0], buffer, sizeof(buffer));
            switch (nread) {
                case -1:
                    perror("read");
                    break;
                case 0:
                    perror("EOF");
                    break;
                default:
                    buffer[nread] = '\0'; // Add null terminator for printf
                    printf("Child: read %d bytes ('%s')\n", nread, buffer);
                    exit(EXIT_SUCCESS);
            }
            break;
        default:
            // This is the parent process
            // Close the read descriptor in the parent process
            if (close(fd[0]) == -1) {
                perror("close");
            }

            // The parent process writes to the pipe
            if (write(fd[1], "hola hijo", 9) == -1) {
                perror("write");
            }

            // The parent process waits for the child process to finish
            wait(&status);
            exit(EXIT_SUCCESS);
    }
}
