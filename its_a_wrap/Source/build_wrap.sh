gfortran -c multmat.for
gcc -c -fPIC compute.c
gcc -shared -o libfoo.so compute.o multmat.o -lgfortran
