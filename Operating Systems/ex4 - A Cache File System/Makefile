CC = g++ -std=c++11

RANLIB = ranlib

LIBSRC = CacheFS.cpp
LIBOBJ = $(LIBSRC:.cpp=.o)

INCS = -I
CFLAGS = -Wall -g $(INCS)
LOADLIBES = -L./

CACHELIB = CacheFS.a
TARGETS = $(CACHELIB)

TAR = tar
TARFLAGS = -cvf
TARNAME = ex4.tar
TARSRCS = $(LIBSRC) README Makefile Answers.pdf

all: $(TARGETS)

CacheFS.a:  CacheFS.o
	ar rcs CacheFS.a CacheFS.o
		$(RANLIB) $@

CacheFS.o: CacheFS.cpp
	$(CC) -Wall -c CacheFS.cpp -o CacheFS.o

clean:
	$(RM) $(CACHELIB) $(LIBOBJ) $(TARNAME) *~ *core

depend:
	makedepend -- $(CFLAGS) -- $(SRC) $(LIBSRC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)