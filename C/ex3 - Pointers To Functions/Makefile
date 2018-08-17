CC= gcc
FLAGS= -std=c99 -Wvla -Wall -Wextra -DNDEBUG -D MAX_ROW_ELEMENTS=2

all: HashIntSearch
	./HashIntSearch 1 0

libgenericHashTable.a: GenericHashTable.o
	ar rcs libgenericHashTable.a GenericHashTable.o

GenericHashTable: GenericHashTable.o
	ar rcs libgenericHashTable.a GenericHashTable.o

GenericHashTable.o: GenericHashTable.c GenericHashTable.h TableErrorHandle.h
	$(CC) $(FLAGS)  -c GenericHashTable.c

TableErrorHandle.o: TableErrorHandle.h TableErrorHandle.c
	$(CC) $(FLAGS) -c TableErrorHandle.c

MyIntFunctions.o: MyIntFunctions.c MyIntFunctions.h
	$(CC) $(FLAGS) -c MyIntFunctions.c

MyStringFunctions.o: MyStringFunctions.c MyStringFunctions.h
	$(CC) $(FLAGS) -c MyStringFunctions.c

HashIntSearch.o: MyIntFunctions.c GenericHashTable.h TableErrorHandle.h MyIntFunctions.h
	$(CC) $(FLAGS) -c HashIntSearch.c

HashStrSearch.o: HashStrSearch.c GenericHashTable.h TableErrorHandle.h MyStringFunctions.c
	$(CC) $(FLAGS) -c HashStrSearch.c

HashIntSearch: HashIntSearch.o MyIntFunctions.o TableErrorHandle.o libgenericHashTable.a
	$(CC) HashIntSearch.o MyIntFunctions.o TableErrorHandle.o -L. -lgenericHashTable -o HashIntSearch

HashStrSearch: HashStrSearch.o libgenericHashTable.a MyStringFunctions.o TableErrorHandle.o
	$(CC) HashStrSearch.o MyStringFunctions.o TableErrorHandle.o -L. -lgenericHashTable -o HashStringSearch

# Other Targets
clean:
	-rm -f *.o HashIntSearch HashStrSearch libgenericHashTable.a
