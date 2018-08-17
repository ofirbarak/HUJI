#include <ctime>
#include <iostream>
#include <math.h>
#include <cmath>
#include <fcntl.h>
#include <fstream>

const int MATRIX_SIZE = 256;

int firstMatrix[MATRIX_SIZE][MATRIX_SIZE];
int secondMatrix[MATRIX_SIZE][MATRIX_SIZE];
int resultMatrix[MATRIX_SIZE][MATRIX_SIZE];
clock_t t1,t2;

void reset_matrix()
{
    for(int i = 0; i < MATRIX_SIZE; i++)
    {
        for(int j = 0; j < MATRIX_SIZE; j ++)
        {
            firstMatrix[i][j] = rand() * 100;
            secondMatrix[i][j] = rand() * 100;
            resultMatrix[i][j] = 0;
        }
    }
}
float three_nested_loops()
{
    t1 = clock();
    for(int i = 0; i < MATRIX_SIZE; i++)
    {
        for(int j = 0; j < MATRIX_SIZE; j ++)
        {
            for(int k = 0; k < MATRIX_SIZE; k++)
            {
                resultMatrix[i][j] += firstMatrix[i][k] * secondMatrix[k][j];
            }
        }
    }
    t2 = clock();
    return (float(t2) - float(t1))/CLOCKS_PER_SEC;
//    std::cout << diff/CLOCKS_PER_SEC << "\n";
}

template <std::size_t size>
float matrix_mul_recursive(int N, int i, int j, int firstMatrix[size][size], int secondMatrix[size][size], int resultMatrix[size][size]) {
    if (N == 1) {
        return *(const_cast<int*>(&(firstMatrix[0][0])) + i) * (*(const_cast<int*>(&(secondMatrix[0][0])) + j));
    }
    else {
        const int H = N / 2;
        const int T = (size * H);

        int r = i / size;
        int c = 0;
        if (j < size) {
            c = j;
        }
        else {
            c = j % size;
        }

        resultMatrix[r][c] += matrix_mul_recursive<size>(H, i, j, firstMatrix, secondMatrix, resultMatrix) +
                              matrix_mul_recursive<size>(H, i + H, T + j, firstMatrix, secondMatrix, resultMatrix);
        resultMatrix[r][c + H] += matrix_mul_recursive<size>(H, i, j + H, firstMatrix, secondMatrix, resultMatrix) +
                                  matrix_mul_recursive<size>(H, i + H, T + j + H, firstMatrix, secondMatrix, resultMatrix);
        resultMatrix[r + H][c] += matrix_mul_recursive<size>(H, T + i, j, firstMatrix, secondMatrix, resultMatrix) +
                                  matrix_mul_recursive<size>(H, T + i + H, T + j, firstMatrix, secondMatrix, resultMatrix);
        resultMatrix[r + H][c + H] += matrix_mul_recursive<size>(H, T + i, j + H, firstMatrix, secondMatrix, resultMatrix) +
                                      matrix_mul_recursive<size>(H, T + i + H, T + j + H, firstMatrix, secondMatrix, resultMatrix);
    }
    return 0;
}

float six_nested_loops(int n) {
    t1 = clock();
    int sum = 0;
    for (int i = 0; i < MATRIX_SIZE; i += n) {
        for (int j = 0; j < MATRIX_SIZE; j += n) {
            for (int k = 0; k < MATRIX_SIZE; k += n) {
                for (int i1 = i; i1 < std::min(i + n, MATRIX_SIZE); i1++) {
                    for (int j1 = j; j1 < std::min(j + n, MATRIX_SIZE); j1++) {
                        sum = 0;
                        for (int k1 = k;
                             k1 < std::min(k + n, MATRIX_SIZE); k1++) {
                            sum += firstMatrix[i1][k1] * secondMatrix[k1][j1];
                        }
                        resultMatrix[i1][j1] += sum;
                    }
                }
            }
        }
    }
    t2 = clock();
    return ((float) t2 - (float) t1) / CLOCKS_PER_SEC;
//    std::cout << diff << "\n";
}

void plot6NestedLoop()
{
    std::ofstream file("/home/ofir/Desktop/6NestedLoopResults.txt");
    reset_matrix();
    for (int n = 2; n < 100; n++) {
        file << n << "," << six_nested_loops(n) << "\n";
    }
}


void plot3NestedLoop(){
    std::ofstream file("/home/ofir/Desktop/3NestedLoopResults.txt");
    reset_matrix();
    float x = three_nested_loops();
    for (int n = 2; n < 100; n++) {
        file << n << "," << x << "\n";
    }
}

void plotRecursiveLoop(){
    std::ofstream file("/home/ofir/Desktop/RecursiveResults.txt");
    reset_matrix();
    float time;
    clock_t t1,t2;
    t1 = clock();
    time = matrix_mul_recursive(MATRIX_SIZE, 0, 0, firstMatrix,
                                secondMatrix, resultMatrix);
    t2 = clock();
    float diff = ((float) t2 - (float) t1) / CLOCKS_PER_SEC;
    for (int n = 2; n < 100; n++) {
        file << n << "," << diff << "\n";
    }
}

int main()
{
    plot6NestedLoop();
    plot3NestedLoop();
    plotRecursiveLoop();
}