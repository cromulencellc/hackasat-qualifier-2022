CC = gcc
FOR = gfortran

CFLAGS = -c -fPIC
FFLAGS = -c

all: libfoo

clean:
	rm *.*o

libfoo: compute.o multmat.o
	$(CC) -shared -o libfoo.so compute.o multmat.o -lgfortran
	@echo "Copying dll..."
	cp libfoo.so ../challenge/libfoo.so
	cp libfoo.so ../solver/libfoo.so

compute.o: compute.c
	$(CC) $(CFLAGS) compute.c

multmat.o: multmat.f90
	$(FOR) $(FFLAGS) multmat.f90


