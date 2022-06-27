# Quals Challenge: Ominous Etude

**Category:** Reverse Engineering?
**Relative Difficulty:** 1/5
**Author:** [Cromulence](https://cromulence.com/)

A single microblaze crackme, designed to be solvable with symbolic execution.

## Dev Work

This challenge ships with a `Dockerfile-dev` used to enable quickly cycling on
C++ dev, including `gdb`.

**DO NOT USE THIS IMAGE TO RUN THE CHALLENGE IN A PUBLICLY VISIBLE WAY.**
The `docker run` command it calls
removes seccomp protections and
adds the `SYS_PTRACE` capability and
that's probably not what you want other people connecting to and hacking lol.

```sh
make dev
```

## Generating `quick_maths.cpp`

This challenge is kind of a foundation for `blazin_etudes`,
so it's a very formulaic crackme, with the real algorithmic
stuff happening in `challenge/src/quick_maths.cpp`

The program `generate.rb` outputs that file, and also `challenge/hint.txt`

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
This should occur automatically with the `.gitlab-ci.yml` file,
and get pushed to 
`registry.mlb.cromulence.com/has3/quals/infrastructure/ominous_etude:challenge`
and 
`registry.mlb.cromulence.com/has3/quals/infrastructure/ominous_etude:solver`

## compiing on μblaze

```sh
# host
docker build -t ominous_etude-build
docker run --rm -it -v $(pwd):/mnt ominous_etude-build

# guest
cd /mnt/challenge
make
```

## running on μblaze

```sh
# host
docker run --rm -it -v $(pwd):/mnt alpine:latest

# guest
apk add qemu-microblaze
qemu-microblaze /mnt/challenge/build/ominous_etude
```