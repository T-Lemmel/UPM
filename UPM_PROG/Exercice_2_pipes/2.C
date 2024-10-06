/* Parent guess the child's random number */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdbool.h>

int main(void) {
    int fd_parent_child[2]; // File descriptor for the pipe parent --> child
    int fd_child_parent[2]; // File descriptor for the pipe child --> parent
    int status;
    int nread;
    char buffer_parent_child[100];
    char buffer_child_parent[100];
    bool have_not_guessed = true;

    /* Create the pipe parent --> child */
    if (pipe(fd_parent_child) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    printf("Pipe parent --> child OK!\n");

    /* Create the pipe child --> parent */
    if (pipe(fd_child_parent) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    printf("Pipe child --> parent OK!\n");

    /* Create a child process */
    switch (fork()) {
        case -1:
            perror("fork");
            exit(EXIT_FAILURE);
        case 0:
            // This is the child process
            printf("Child process created\n");
            int x; // Random number to guess by the parent

            // Close the write descriptor of the pipe parent --> child in the child process
            close(fd_parent_child[1]);
            // Close the read descriptor of the pipe child --> parent in the child process
            close(fd_child_parent[0]);

            // Generate random number that the parent will guess
            srandom(getpid());   // inicializa la semilla para los numeros  
            x=(int)(256.0*random()/RAND_MAX);   // x será un numero entre 0 y 256
            printf("Number to guess: %d\n", x);

            while (have_not_guessed)
            {
                // Read the information contained in the pipe
                nread = read(fd_parent_child[0], buffer_parent_child, sizeof(buffer_parent_child));
                switch (nread) {
                    case -1:
                        perror("read");
                        break;
                    case 0:
                        perror("EOF");
                        break;
                    default:
                        buffer_parent_child[nread] = '\0'; // Add null terminator for printf
                        char result;
                        if (x > atoi(buffer_parent_child)) {
                            printf("Child: The parent guessed too small\n");
                            result = '0'; // Too small
                        } else if (x == atoi(buffer_parent_child)) {
                            printf("Child: The parent guessed the number\n");
                            result = '1'; // Equal
                        } else if (x < atoi(buffer_parent_child)) {
                            printf("Child: The parent guessed too large\n");
                            result = '2'; // Too large
                        }
                        // Send the result to the parent
                        if (write(fd_child_parent[1], &result, 1) == -1) {
                            perror("write");
                        }
                        if (result == '1') {
                            have_not_guessed = false;
                        }
                }
            }

        default:
            // This is the parent process
            // Close the read descriptor of the pipe parent --> child in the parent process
            close(fd_parent_child[0]);
            // Close the write descriptor of the pipe child --> parent in the parent process
            close(fd_child_parent[1]);

            // The parent tries to guess the number
            int low = 0;
            int high = 255;
            char result;
            char guess_str[4]; // Previous guess for dichotomy
            int guess;

            while (have_not_guessed) {
                guess = (low + high) / 2;
                snprintf(guess_str, sizeof(guess_str), "%d", guess);

                // Write the guess to the pipe
                if (write(fd_parent_child[1], guess_str,sizeof(guess_str)) == -1) {
                    perror("write");
                } else {
                    printf("Parent: Guessing %d\n", guess);
                }

                // Read the result from the child
                if (read(fd_child_parent[0], &result, 1) == -1) {
                    perror("read");
                } else {
                    //printf("Parent: Result %c\n", result);

                    if (result == '0') {
                        printf("Parent: I guessed too small\n");
                        low = guess + 1;
                    } else if (result == '1') {
                        printf("Parent: I guessed the number\n");
                        have_not_guessed = false;
                    } else {
                        printf("Parent: I guessed too large\n");
                        high = guess - 1;
                    }
                }
            }
            // The parent process waits for the child process to finish
            wait(&status);
            exit(EXIT_SUCCESS);
    }
}
