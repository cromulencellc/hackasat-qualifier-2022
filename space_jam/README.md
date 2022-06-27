# Quals Challenge: Space Jam #

**Category:** RF
**Relative Difficulty:** 5/5
**Author:** [Cromulence](https://cromulence.com/)

It's a noisy world out there and you just want to transmit from your satellite. Use the transmitter controls to transmit the flag to yourself. Make sure you receive the flag before the transmission window ends.

Configure your signal with a JSON command using the following format:
```
{
    "frequency":100000,
    "constellation":"PSK",
    "samples_per_symbol":1000,
    "diff_encoding":"OFF",
    "amplitude":100.0
}
```


# Build and run the challenge

To build the challenge run the following from the root directory
```
make challenge
```

The challenge will tell you how to connect
# Build and run the challenge and solver
```
make solver
```

# A few notes:

## Solvers

This challenge is configured to have a many possible solutions depending on how good you are at DSP.

The most straight forward solutions can be solved by using the GNU radio PSK tutorial as a primer.

## Does this challenge send too much data

The challenge is limited to the length of the SpaceJam song sent out at 10 samples per symbol. The total number of bytes transmitted by the challenge is:
```
Btx = 3334 Bytes/song * 8 bits/byte * (1/2) symbol/bit * 8 Btx/symbol  
```

Expanding out the math the numbre of bytes transmitted is 
```
3334 * 8 * 0.5 * 8 = 106688 bytes 
```
Assuming worst case scenario lets assume 2000 teams that all try the challenge 100 times (unlikely)

```
106688 bytes * 2000 players * 100 attempts = 19.8 GB
```

At the cost of 0.09 dollars per  GB that comes out to $1.78 dollars.

