CC = g++ -std=c++11

RANLIB = ranlib

LIBSRC = whatsappServer.cpp whatsappClient.cpp
LIBOBJ = $(LIBSRC:.cpp=.o)

INCS = -I
CFLAGS = -Wall -g $(INCS)
LOADLIBES = -L./

PROGRAMES = whatsappClient whatsappServer
TARGETS = $(PROGRAMES)

TAR = tar
TARFLAGS = -cvf
TARNAME = ex5.tar
TARSRCS = $(LIBSRC) README Makefile

all: $(TARGETS)

whatsappClient:  whatsappClient.o

whatsappServer: whatsappServer.o

whatsappClient.o: whatsappClient.cpp
	$(CC) -Wall -c whatsappClient.cpp -o whatsappClient.o

whatsappServer.o: whatsappClient.cpp
	$(CC) -Wall -c whatsappServer.cpp -o whatsappServer.o

clean:
	$(RM) $(PROGRAMES) $(LIBOBJ) $(TARNAME) *~ *core

depend:
	makedepend -- $(CFLAGS) -- $(SRC) $(LIBSRC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)
