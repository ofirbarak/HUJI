#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "mpi.h"

#define ROW 0
#define COL 1
#define HEIGHT 2
#define K 5
#define MAT_SIZE K*K

void writeMatToFile(char *filename, double Mat[K][K]){
    FILE *f = fopen(filename, "w");
    fprintf(f, "\n");
    for (int i = 0; i < K; ++i) {
        for (int j = 0; j < K; ++j) {
            fprintf(f, "%d, ", (int)Mat[i][j]);
        }
        fprintf(f, "\n");
    }

    fclose(f);
}


void createInput(double Mat1[K][K], int rank, int first){
    srand(first*time(NULL)*(rank+1)); //todo: change with time
    for (int i = 0; i < K; ++i) {
        for (int j = 0; j < K; ++j) {
            Mat1[i][j] = rand()%10000;
        }
    }
}


void multMatrices(double A[K][K], double B[K][K], double C[K][K]){
    int sum = 0;
    for (int i = 0; i < K; ++i) {
        for (int j = 0; j < K; ++j) {
            sum = 0;
            for (int k = 0; k < K; ++k) {
                sum += A[i][k]*B[k][j];
            }
            C[i][j] = sum;
        }
    }
}


void createComm(int argc, char **argv, int *mySize, int *myRank, int myCoords[2],
                int *pcubeP, MPI_Comm *myRow_comm, MPI_Comm *myCol_comm,
                MPI_Comm *myHei_comm, MPI_Comm *cart) {
    // initialize MPI
    int size;
    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, myRank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int cubeP = (int)cbrt(size);
    *pcubeP = cubeP;
    *mySize = size;

    if (pow(cubeP, 3) != size) {
        if (myRank == 0) {
            perror("Cube root of p is not an integer");
            fflush(stdout);
        }
        MPI_Abort(MPI_COMM_WORLD, -1);
    }

    // create a cartesian grid communicator
    MPI_Comm cart_comm;
    int dim[3], periodic[3];
    dim[0] = cubeP;
    dim[1] = cubeP;
    dim[2] = cubeP;
    periodic[0] = true;
    periodic[1] = true;
    periodic[2] = true;
    MPI_Cart_create(MPI_COMM_WORLD, 3, dim, periodic, false, &cart_comm);
    *cart = cart_comm;

    // get current processor's coordinates
    MPI_Cart_coords(cart_comm, *myRank, 3, myCoords);

    MPI_Comm rowsComm, colsComm, heisComm;

    MPI_Comm_split(MPI_COMM_WORLD, myCoords[HEIGHT], myCoords[ROW], &rowsComm);
    MPI_Comm_split(rowsComm, myCoords[COL], myCoords[ROW], myRow_comm);

    MPI_Comm_split(MPI_COMM_WORLD, myCoords[HEIGHT], myCoords[COL], &colsComm);
    MPI_Comm_split(colsComm, myCoords[ROW], myCoords[COL], myCol_comm);

    MPI_Comm_split(MPI_COMM_WORLD, myCoords[ROW], myCoords[COL], &heisComm);
    MPI_Comm_split(heisComm, myCoords[COL], myCoords[HEIGHT], myHei_comm);

}


int main(int argc, char **argv){
    int size, myRank, myCoords[3], cubeP;
    MPI_Comm myRow_comm, myCol_comm, myHei_comm, cart_comm;
    createComm(argc, argv, &size, &myRank, myCoords, &cubeP,
               &myRow_comm, &myCol_comm, &myHei_comm, &cart_comm);

    double myA[K][K], myB[K][K], myC[K][K], **myResult=NULL;
    char inputFileName1[50], inputFileName2[50], outputFileName[50];

    if (myCoords[ROW] == 0) {
        createInput(myA, myRank, 1);
        sprintf(inputFileName1, "./IO3/input_A_%d_%d",
                myCoords[COL], myCoords[HEIGHT]); // todo:remove IO directory
        writeMatToFile(inputFileName1, myA);
    }
    if (myCoords[COL] == 0) {
        createInput(myB, myRank, 2);
        sprintf(inputFileName2, "./IO3/input_B_%d_%d", myCoords[HEIGHT], myCoords[ROW]);
        writeMatToFile(inputFileName2, myB);
    }

    double startTime,endTime;
    startTime = MPI_Wtime();

    // send/receive data
    int root = 0;
    MPI_Bcast(&myA[0][0], MAT_SIZE, MPI_DOUBLE, root, myRow_comm);
    MPI_Bcast(&myB[0][0], MAT_SIZE, MPI_DOUBLE, root, myCol_comm);

    multMatrices(myA, myB, myC);


    if (myCoords[HEIGHT] == 0){
        myResult = (double **)malloc(MAT_SIZE*sizeof(double));
    }

    MPI_Reduce(&myC[0][0], myResult,
                       MAT_SIZE, MPI_DOUBLE, MPI_SUM, root, myHei_comm);

    endTime = MPI_Wtime();

    if (myCoords[HEIGHT] == 0) // just the upper processors print the output
    {
        sprintf(outputFileName, "./IO3/output_%d_%d", myCoords[COL], myCoords[ROW]);
        writeMatToFile(outputFileName, myResult);
        free(myResult);
    }

    printf("took: %f seconds\n", endTime-startTime);

    MPI_Finalize();
    return 0;
}




