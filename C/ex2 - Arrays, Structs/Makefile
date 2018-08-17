CC= gcc
CFLAGS= -c -std=c99 -Wvla -Wall -Wextra -DNDEBUG
FLAGS= -std=c99 -Wvla -Wall -Wextra -DNDEBUG

# All Target
all: ListExample


# Exceutables
CheckDependency: CheckDependency.c
	$(CC) $(FLAGS) CheckDependency.c -o CheckDependency

ListExample: MyLinkedList.c ListExample.c
	$(CC) $(FLAGS) MyLinkedList.c ListExample.c -o ListExample

ReadDirectory: ReadDirectory.c
	$(CC) $(FLAGS) ReadDirectory.c -o ReadDirectory

# Object Files
CheckDependency.o: CheckDependency.c
	$(CC) $(CFLAGS) CheckDependency.c -o CheckDependency.o
	 
MyLinkedList.o: MyLinkedList.c MyLinkedList.h
	$(CC) $(CFLAGS) MyLinkedList.c -o MyLinkedList.o


# Other Targets
clean:
	-rm -f *.o CheckDependency ListExample ReadDirectory

