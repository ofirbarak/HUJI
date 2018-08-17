#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include "mpi.h"

#define ROW 0
#define COL 1
#define VECTOR_SIZE 5

#define UP 0
#define DOWN 1
#define LEFT 2
#define RIGHT 3

#define DIRECTIONS 4

void writeMatToFile(char *filename, int Vec[VECTOR_SIZE]){
    FILE *f = fopen(filename, "w");
    for (int i = 0; i < VECTOR_SIZE; ++i) {
        fprintf(f, "%d, ", Vec[i]);
    }
    fprintf(f, "\n");

    fclose(f);
}


void createInput(int Vec[VECTOR_SIZE], int rank){
    srand(rank+1);
    for (int i = 0; i < VECTOR_SIZE; ++i) {
        Vec[i] = rand()%100000;
    }
}


/*
 * return array result = [up, down, left, right]
 */
void getDestinationRanks(MPI_Comm cart_comm, const int myCoords[DIRECTIONS], int *result){
    int coords[2];
    coords[0] = myCoords[0] - 1;
    coords[1] = myCoords[1];

    MPI_Cart_rank(cart_comm, coords, &result[UP]);

    coords[0] = myCoords[0] + 1;
    MPI_Cart_rank(cart_comm, coords, &result[DOWN]);

    coords[0] = myCoords[0];
    coords[1] = myCoords[1] - 1;
    MPI_Cart_rank(cart_comm, coords, &result[LEFT]);

    coords[1] = myCoords[1] + 1;
    MPI_Cart_rank(cart_comm, coords, &result[RIGHT]);
}


void calcConvolution(int Vectors[DIRECTIONS][VECTOR_SIZE], int myVector[VECTOR_SIZE],
                     int result[VECTOR_SIZE]){
    for (int k = 0; k < VECTOR_SIZE; ++k) {
        result[k] = myVector[k];
    }
    for (int i = 0; i < DIRECTIONS; ++i) {
        for (int j = 0; j < VECTOR_SIZE; ++j) {
            result[j] += (i+1)*Vectors[i][j];
        }
    }
}


int main(int argc, char **argv){
    // initialize MPI
    int rank, size;
    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int sqrtP = (int)sqrt(size);

    if (pow(sqrtP, 2) != size){
        if (rank == 0)
            perror("Square root of p is not an integer");
        MPI_Abort(MPI_COMM_WORLD, -1);
    }

    // create a cartesian grid communicator
    MPI_Comm cart_comm;
    int dim[2], periodic[2];
    dim[ROW] = sqrtP;
    dim[COL] = sqrtP;
    periodic[ROW] = true;
    periodic[COL] = true;
    MPI_Cart_create(MPI_COMM_WORLD, 2, dim, periodic, false, &cart_comm);

    // get current processor's coordinates
    int myCoords[2];
    MPI_Cart_coords(cart_comm, rank, 2, myCoords);

    char inputFileName[50], outputFileName[50];
    sprintf(inputFileName, "./IO2/input_%d_%d", myCoords[ROW], myCoords[COL]); // todo:remove IO directory
    sprintf(outputFileName, "./IO2/output_%d_%d", myCoords[ROW], myCoords[COL]);// todo:remove IO directory

    // create and write input A's slice
    int myVector[VECTOR_SIZE];
    createInput(myVector, rank);
    writeMatToFile(inputFileName, myVector);


    // send and receive data
    int destRanks[DIRECTIONS];
    getDestinationRanks(cart_comm, myCoords, destRanks);

    int vectors[DIRECTIONS][VECTOR_SIZE], resultVector[VECTOR_SIZE];
    MPI_Request send_request[DIRECTIONS],recv_request[DIRECTIONS];

    for (int i = 0; i < DIRECTIONS; ++i) {
        MPI_Isend(&myVector, VECTOR_SIZE, MPI_INT, destRanks[i], 1, cart_comm, &send_request[i]);
        MPI_Irecv(&vectors[i], VECTOR_SIZE, MPI_INT, destRanks[i], 1, cart_comm, &recv_request[i]);
    }

    for (int i = 0; i < DIRECTIONS; ++i) {
        MPI_Wait(&send_request[i], NULL);
        MPI_Wait(&recv_request[i], NULL);
    }

    // write output
    calcConvolution(vectors, myVector, resultVector);
    writeMatToFile(outputFileName, resultVector);

    MPI_Finalize();
    return 0;
}



