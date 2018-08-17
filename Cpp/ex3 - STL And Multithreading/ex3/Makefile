CC= g++ -std=c++11
FLAGS= -Wvla -Wall -Wextra -pthread

# All Target
all: GenericMatrixDriver
	./GenericMatrixDriver

#Excutables
GenericMatrixDriver: GenericMatrixDriver.cpp Complex.o Matrix
	$(CC) $(FLAGS) GenericMatrixDriver.cpp Complex.o -o GenericMatrixDriver

Matrix: Matrix.hpp MatrixExceptions.h Matrix.h
	$(CC) $(FLAGS) Matrix.hpp MatrixExceptions.h -o Matrix.hpp.gch


# Object Files
Complex.o: Complex.cpp Complex.h
	g++ -std=c++11 -c Complex.cpp

# Other Targets
clean:
	-rm -f *.o GenericMatrixDriver Matrix.hpp.gch

