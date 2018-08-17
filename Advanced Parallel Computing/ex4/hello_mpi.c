#include <stdio.h>
#include "mpi.h"


// run in terminal "mpirun -quiet -n 2 hello_mpi.exe"

int main(int argc, char **argv){
    int rank, size;
    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0){
        MPI_Barrier(MPI_COMM_WORLD);
        printf("Hello world!\n");
    }
    else {
        printf("My rank is: %d, and the total number of ranks in the system is: %d\n", rank, size);
        MPI_Barrier(MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}
