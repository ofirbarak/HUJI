CC=g++
RANLIB=ranlib

LIBSRC=MapReduceFramework.cpp Search.cpp
LIBOBJ=$(LIBSRC:.c=.o)
LIBH = MapReduceFramework.h


INCS=-I.
CFLAGS = -std=gnu++11 -Wall -g $(INCS)
LOADLIBES = -L.

MAP_REDUCE_LIB = MapReduceFramework.a
TARGETS = $(MAP_REDUCE_LIB) Search

TAR=tar
TARFLAGS=-cvf
TARNAME=ex3.tar
TARSRCS=$(LIBSRC) Makefile README
LOG_FILENAME = .MapReduceFramework.log

all: Search 

libMapReduceFramework.a : MapReduceFramework.o
	ar rcs MapReduceFramework.a MapReduceFramework.o

clean:
	$(RM) -f *.o *.a $(LOG_FILENAME) Search *~ *core

depend:
	makedepend -- $(CFLAGS) -- $(SRC) $(LIBSRC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

MapReduceFramework.o : MapReduceFramework.cpp MapReduceFramework.h\
	MapReduceClient.h
	g++ $(CFLAGS) -c MapReduceFramework.cpp

Search.o : Search.cpp
	g++ $(CFLAGS) -c Search.cpp

Search : Search.o libMapReduceFramework.a
	g++ $(CFLAGS) -pthread Search.cpp -L. -l:MapReduceFramework.a -o Search

