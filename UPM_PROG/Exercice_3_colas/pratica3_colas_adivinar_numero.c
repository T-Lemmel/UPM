// The father will try to guess the son's number using a queue

#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// Definition of the queue key
#define QUEUE_KEY 1

// Message structure
struct msgbuf {
    long mtype; // 1 for the father's guess, 2 for the son's answer
    char mtext[15]; // the actual message (guess or answer)
};

// Function that creates the queue and returns id
int create_queue(int key) {
    int msgqid = msgget(key, IPC_CREAT | 0666);
    if (msgqid == -1) {
        perror("msgget");
        return -1;
    }
    return msgqid;
}

// Main function
int main(void) {
    int queue_id, ret;
    bool guessed = false;

    // Creation of the queue
    queue_id = create_queue(QUEUE_KEY);
    if (queue_id == -1) {
        printf("Could not create the queue!\n");
        exit(EXIT_FAILURE);
    }
    printf("Created the queue\n");

    switch (fork()) {
    case -1:
        perror("fork");
        exit(EXIT_FAILURE);

    case 0: {
        // Son
        printf("Son created\n");
        struct msgbuf received_guess_msg;
        struct msgbuf son_answer;
        son_answer.mtype = 2;

        // Generate a random number between 0 and 100
        srandom(getpid()); 
        int x = (int)(100.0 * (random() / (float)RAND_MAX)); // x will be between 0 and 100

        while (!guessed) {
            // Reading the guess
            ret = msgrcv(queue_id, &received_guess_msg, sizeof(received_guess_msg.mtext), 1, 0);
            if (ret == -1) {
                perror("msgrcv");
                exit(EXIT_FAILURE);
            }
            printf("Son received the guess: %s\n", received_guess_msg.mtext);

            // Chose the answer according to the guess
            int number = atoi(received_guess_msg.mtext);
            if (number > x) {
                strcpy(son_answer.mtext, "smaller");
            } else if (number < x) {
                strcpy(son_answer.mtext, "bigger");
            } else {
                strcpy(son_answer.mtext, "guessed");
                guessed = true;
            }

            // Sending the answer
            ret = msgsnd(queue_id, &son_answer, sizeof(son_answer.mtext), 0);
            if (ret == -1) {
                perror("msgsnd");
                exit(EXIT_FAILURE);
            }
        }
        exit(EXIT_SUCCESS);
    }

    default: {
        // Father

        int max = 100 ;
        int min = 0;
        char guess_char[15];
        struct msgbuf guess_msg;
        guess_msg.mtype = 1;
        struct msgbuf received_answer;

        while (!guessed) {
            int guess = (max + min) / 2;
            sprintf(guess_char, "%d", guess);
            strcpy(guess_msg.mtext, guess_char); // Use strcpy to copy the string

            // Sending the guess
            ret = msgsnd(queue_id, &guess_msg, sizeof(guess_msg.mtext), 0);
            if (ret == -1) {
                perror("msgsnd");
                exit(EXIT_FAILURE);
            }
            printf("Father sent the guess: %s\n", guess_msg.mtext);

            // Reading the son's answer
            ret = msgrcv(queue_id, &received_answer, sizeof(received_answer.mtext), 2, 0); // Correct sizeof parameter
            if (ret == -1) {
                perror("msgrcv");
                exit(EXIT_FAILURE);
            }
            printf("Father received the answer: %s\n", received_answer.mtext);

            // Check how was the previous guess and adapt the range or close the queue
            if (strcmp(received_answer.mtext, "smaller") == 0) {
                max = guess - 1;
            } else if (strcmp(received_answer.mtext, "bigger") == 0) {
                min = guess + 1;
            } else if (strcmp(received_answer.mtext, "guessed") == 0) {
                guessed = true;
                printf("Father guessed the number: %s\n", guess_msg.mtext);
                if (msgctl(queue_id, IPC_RMID, NULL) == -1) {
                    perror("msgctl");
                    exit(EXIT_FAILURE);
                }
                printf("Queue closed\n");
            }
        }
        exit(EXIT_SUCCESS);
    }
    }
    return 0;
}
