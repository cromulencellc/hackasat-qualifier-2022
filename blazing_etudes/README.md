# Quals Challenge: Blazing Etudes

**Category:** Reverse Engineering
**Relative Difficulty:** 4/5
**Author:** [Cromulence](https://cromulence.com/)

A whole pile of microblaze crackmes,
designed to functionally require symbolic execution to
solve them.

## Dev Work and Generating Binaries

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
