CC = mpicc

TARGET = hello_mpi transpose grid 3d-mult

all: $(TARGET)

hello_mpi : hello_mpi.c
	$(CC) hello_mpi.c -o hello_mpi

transpose : transpose.c
	$(CC) transpose.c -o transpose -lm

grid : grid.c
	$(CC) grid.c -o grid -lm

3d-mult : 3d-mult.c
	$(CC) 3d-mult.c -o 3d-mult -lm

clean:
	rm *.o $(TARGET)
