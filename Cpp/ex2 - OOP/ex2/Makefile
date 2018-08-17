CC= g++ -std=gnu++11
FLAGS= -Wvla -Wall -Wextra -pthread
CODEFILES= ex2.tar README Makefile Line.cpp Line.h Point.cpp Point.h PrintOuts.cpp PrintOuts.h Shape.cpp\
Shape.h Shapes.cpp Trapezoid.cpp Trapezoid.h Triangle.cpp Triangle.h Defs.h

# All Target
all: Shapes


#Excutables
Shapes: Shapes.o Triangle.o Trapezoid.o PrintOuts.o Shape.o Line.o Point.o
	$(CC) $(FLAGS) Shapes.o Triangle.o Trapezoid.o Shape.o Line.o Point.o PrintOuts.o -o Shapes

# Object Files
Shapes.o: Shapes.cpp Triangle.h Trapezoid.h PrintOuts.h
	g++ -std=c++11 -c Shapes.cpp

Shape.o: Shape.cpp Shape.h Line.h Point.h
	g++ -std=c++11 -c Shape.cpp

Line.o: Line.cpp Line.h Point.h
	g++ -std=c++11 -c Line.cpp

Point.o: Point.cpp Point.h Defs.h
	g++ -std=c++11 -c Point.cpp

Triangle.o: Triangle.cpp Triangle.h Shape.h
	g++ -std=c++11 -c Triangle.cpp

Trapezoid.o: Trapezoid.cpp Trapezoid.h Shape.h
	g++ -std=c++11 -c Trapezoid.cpp

PrintOuts.o: PrintOuts.cpp PrintOuts.h Defs.h
	g++ -std=c++11 -c PrintOuts.cpp

tar:
	tar -cf $(CODEFILES)

# Other Targets
clean:
	-rm -f ex2.tar *.o Shapes

