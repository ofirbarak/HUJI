#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "mpi.h"

#define ROW 0
#define COL 1
#define BLOCK_SIZE 5

void writeMatToFile(char *filename, double Mat[BLOCK_SIZE][BLOCK_SIZE]){
    FILE *f = fopen(filename, "w");
    for (int i = 0; i < BLOCK_SIZE; ++i) {
        for (int j = 0; j < BLOCK_SIZE; ++j) {
            fprintf(f, "%f, ", Mat[i][j]);
        }
        fprintf(f, "\n");
    }

    fclose(f);
}


void transposeMat(double Mat[BLOCK_SIZE][BLOCK_SIZE]) {
    double temp;
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < i; j++) {
            temp = Mat[i][j];
            Mat[i][j] = Mat[j][i];
            Mat[j][i] = temp;
        }
    }
}


void createInput(double Mat[BLOCK_SIZE][BLOCK_SIZE], int rank){
    srand(time(NULL)*(rank+1));
    for (int i = 0; i < BLOCK_SIZE; ++i) {
        for (int j = 0; j < BLOCK_SIZE; ++j) {
            Mat[i][j] = rand();
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
    int coords[2];
    MPI_Cart_coords(cart_comm, rank, 2, coords);

    char inputFileName[50], outputFileName[50];
    sprintf(inputFileName, "./IO/input_%d_%d", coords[ROW], coords[COL]);
    sprintf(outputFileName, "./IO/output_%d_%d", coords[ROW], coords[COL]);

    // create and write input A's slice
    double Aslice[BLOCK_SIZE][BLOCK_SIZE];
    createInput(Aslice, rank);
    writeMatToFile(inputFileName, Aslice);

    transposeMat(Aslice);

    // send (and receive) transposed A's slice matrix to the correct place on the grid

    // get destination rank
    int destRank;
    int destCoords[2];
    destCoords[ROW] = coords[COL];
    destCoords[COL] = coords[ROW];
    MPI_Cart_rank(cart_comm, destCoords, &destRank);

    double Bslice[BLOCK_SIZE][BLOCK_SIZE];
    MPI_Request send_request, recv_request;

    MPI_Isend(&Aslice[0][0], BLOCK_SIZE*BLOCK_SIZE, MPI_DOUBLE, destRank, 1, cart_comm, &send_request);
    MPI_Irecv(&Bslice[0][0], BLOCK_SIZE*BLOCK_SIZE, MPI_DOUBLE, destRank, 1, cart_comm, &recv_request);

    MPI_Wait(&send_request, NULL);
    MPI_Wait(&recv_request, NULL);

    // write output
    writeMatToFile(outputFileName, Bslice);

    MPI_Finalize();
    return 0;
}


