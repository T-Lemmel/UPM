#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

// Mutex and condition variables for synchronization
pthread_mutex_t mut;
pthread_cond_t cond1, cond2;
int wakeup1 = 0; // Flag to wake up thread 1
int wakeup2 = 0; // Flag to wake up thread 2

// Function executed by thread 1
void* function1(void *arg)
{
    int i = 0;
    pthread_t my_id = pthread_self();
    printf("\n Hello, soy el thread 1 (%lu) y me voy a dormir...\n", (unsigned long) my_id);

    // Lock the mutex before checking the condition and modify the wakeup flag
    pthread_mutex_lock(&mut);

    // Wait for the signal from thread 2
    while (!wakeup1)
        pthread_cond_wait(&cond1, &mut); // Wait for the signal from thread 2 also release the mutex so wakeup1 can be modified be thread 2, relock the mutex when the signal is received

    // Reset the wakeup flag
    wakeup1--;
    // Unlock the mutex
    pthread_mutex_unlock(&mut);

    // Do Thread 1 task
    for (i = 0; i < 3; i++) {
        printf("\n Hello, soy el thread 1 (%lu)\n", (unsigned long) my_id);
        sleep(1);
    }
    printf("\n T1 says: bye bye !\n");

    // Lock the mutex and signal thread 2
    pthread_mutex_lock(&mut);
    pthread_cond_signal(&cond2);

    // Set the wakeup flag for thread 2
    wakeup2++;

    // Unlock the mutex
    pthread_mutex_unlock(&mut);

    return NULL;
}

// Function executed by thread 2
void* function2(void *arg)
{
    pthread_t my_id = pthread_self();
    int i;

    // Perform thread 2 task
    for (i = 0; i < 10; i++) {
        printf("\n Hello, soy el thread 2 (%lu)\n", (unsigned long) my_id);
        sleep(1);
        if (i == 3) {
            // Lock the mutex before signaling thread 1 and set the wakeup flag for thread 1
            pthread_mutex_lock(&mut);
            wakeup1++;

            // Signal thread 1 to wake up
            pthread_cond_signal(&cond1);
            // Unlock the mutex
            pthread_mutex_unlock(&mut);

            // Lock the mutex before waiting for the signal from thread 1
            pthread_mutex_lock(&mut);
            // Wait for the signal from thread 1
            while (!wakeup2)
                pthread_cond_wait(&cond2, &mut); // Wait for the signal from thread 1
            // Reset the wakeup flag
            wakeup2--;
            // Unlock the mutex
            pthread_mutex_unlock(&mut);
        }
    }
    printf("\n T2 says: Hasta luego lucas !\n");
    return NULL;
}

int main(void)
{
    pthread_t t1_id, t2_id;
    int err;

    // Initialize condition variables and mutex
    pthread_cond_init(&cond1, NULL);
    pthread_cond_init(&cond2, NULL);
    pthread_mutex_init(&mut, NULL);

    // Create thread 1
    err = pthread_create(&t1_id, NULL, &function1, NULL);
    if (err != 0)
        printf("\ncan't create thread :[%s]", strerror(err));
    else
        printf("\n Thread created successfully\n");

    // Create thread 2
    err = pthread_create(&t2_id, NULL, &function2, NULL);
    if (err != 0)
        printf("\ncan't create thread :[%s]", strerror(err));
    else
        printf("\n Thread created successfully\n");

    // Wait for both threads to finish
    pthread_join(t1_id, NULL);
    pthread_join(t2_id, NULL);

    // Destroy condition variables and mutex
    pthread_cond_destroy(&cond1);
    pthread_cond_destroy(&cond2);
    pthread_mutex_destroy(&mut);

    return 0;
}