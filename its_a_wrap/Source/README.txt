C calls Fortran function:
gfortran -c hello_world.f90
gcc -c cwrap.c
gcc cwrap.o hello_world.o -lgfortran

No-Worky:
gcc -shared -Wl,-soname,cwrap -o cwrap.so -fPIC cwrap.c

C calls other C file and Fortran:
gfortran -c hello_world.f90
gcc -c cwrap.c morec.c
gcc cwrap.o morec.o hello_world.o -lgfortran

Now need to call from Python:
gfortran -c hello_world.f90
gcc -c cwrap.c morec.c
gcc -shared -o libfoo.so cwrap.o morec.o hello_world.o -lgfortran
python_wrap.py

Now add java:
