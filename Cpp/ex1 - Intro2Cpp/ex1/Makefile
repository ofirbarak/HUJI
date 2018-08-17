CC= g++ -std=c++11
FLAGS= -Wvla -Wall -Wextra -pthread
CODEFILES= ex1.tar README Point.cpp Point.h PointSet.cpp PointSet.h ConvexHull.cpp PointSetBinaryOperations.cpp Makefile

# All Target
all: ConvexHull PointSetBinaryOperations
	./PointSetBinaryOperations

#Excutables
PointSetBinaryOperations: PointSetBinaryOperations.o PointSet.o Point.o
	$(CC) $(FLAGS) PointSetBinaryOperations.o PointSet.o Point.o -o PointSetBinaryOperations

ConvexHull: ConvexHull.o PointSet.o Point.o
	$(CC) $(FLAGS) ConvexHull.o PointSet.o Point.o -o ConvexHull

# Object Files
ConvexHull.o: ConvexHull.cpp PointSet.h Point.h
	g++ -std=c++11 -c ConvexHull.cpp

PointSetBinaryOperations.o: PointSetBinaryOperations.cpp PointSet.h Point.h
	g++ -std=c++11 -c PointSetBinaryOperations.cpp

PointSet.o: PointSet.cpp PointSet.h
	g++ -std=c++11 -c PointSet.cpp

Point.o: Point.cpp Point.h
	g++ -std=c++11 -c Point.cpp



tar:
	tar -cf $(CODEFILES)

# Other Targets
clean:
	-rm -f ex1.tar *.o PointSetBinaryOperations ConvexHull

