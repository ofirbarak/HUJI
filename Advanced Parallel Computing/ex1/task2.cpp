#include <iostream>
#include <ctime>

int main() {
    register long i = 6000000000L;
    clock_t start, finish;
    double  duration;

    // Measure the duration of an event.
    printf( "Time to do %ld empty loops is ", i );
    start = clock();
    while( i-- )
        ;
    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    printf( "%2.1f seconds\n", duration );
}