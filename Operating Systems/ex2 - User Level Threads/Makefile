CC=g++

OSMLIB = libuthreads.a
TARGETS = $(OSMLIB)

TAR=tar
TARFLAGS=-cvf
TARNAME=ex2.tar
TARSRCS=$(LIBSRC) Makefile README

all: $(TARGETS) 

$(TARGETS): uthreads.o
	ar -rv libuthreads.a uthreads.o

uthreads.o:	uthreads.cpp uthreads.h Thread.h
	g++ -Wall -c -std=c++11 uthreads.cpp 




depend:
	makedepend -- $(CFLAGS) -- $(SRC) $(LIBSRC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)
