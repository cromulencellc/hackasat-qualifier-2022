# Quals Challenge: Its A Wrap #

**Category:** 
**Relative Difficulty:** 0/5
**Author:** [Cromulence](https://cromulence.com/)

Challenge based on the fact that FORTRAN and C order matrices differently.  FORTRAN is wrapped in C and is the wrapped in
Python.  When the C code calls the FORTRAN code it puts the matrices into "FORTRAN" order but then does not put the 
resulting matrix back into "C" order before returning it to Python.

The code encrypts a phrase by multiplying it by a set encryption matrix.  The players must determine what the encrypted
values will be.  This is based on the website: http://aix1.uottawa.ca/~jkhoury/cryptography.htm

## Files needed to serve with challenge
1. libfoo.so
2. encrypt.pyc


# Build process
## Build challenge DLL
Builds the DLL used by the challenge, copies .so file to the challenge folder
```sh
cd ./Source
make clean
make all
```

## Build and Test Challenge ##
Builds the challenge and deploys it on localhost to test
```sh
make challenge
```

socat is required for the container to deploy locally to test (otherwise the Make target will just build the container)
```
sudo apt install socat
```

## Build and Test Solver ##
Builds the solver and deploys it on localhost along with the challenge container to test
```sh
make solver
```

## Pushing Images to Infrastructure ##
This should occur automatically with the gitlab-ci file and get pushed to registry.mlb.cromulence.com/has3/quals/infrastructure/hello_aws:challenge and registry.mlb.cromulence.com/has3/quals/infrastructure/hello_aws:solver

