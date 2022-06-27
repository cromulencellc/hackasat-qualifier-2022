# Quals Challenge: Doppler #

**Category:** RF
**Relative Difficulty:** 4/5
**Author:** [Cromulence](https://cromulence.com/)

Wideband capture of a satellite downlink with doppler and other path effects, decode and get the flag.

## Running ##
Build and run the challenge
```sh
make generator
```
Build and run the solver
```sh
place sat_downlink_120ksps.iq file in data/
make solver

with gnuradio installed, you can use the solver.grc flowgraph to see the waterfall, fft, and constellation plots during the solve.
```