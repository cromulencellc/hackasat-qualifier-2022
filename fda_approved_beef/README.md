# Quals Challenge: fprime-exploitation #

**Category:** Rapid Unplanned Disassembly (RUD)
**Relative Difficulty:** TBD
**Author:** [Cromulence](https://cromulence.com/)

## Running ##

Build

make build

Run the challenge with

docker run -it -p 5000:5000 -p 50050:5001 -e FLAG=flag{test123test123987654321} registry.mlb.cromulence.com/has2/quals/challenges/fprime-exploitation/fprime-exploitation:challenge

And run the solver with

docker run -it --rm --net="host" registry.mlb.cromulence.com/has2/quals/challenges/fprime-exploitation/fprime-exploitation:solver

Or better yet:

make test


## Description
There is a flag hidden on a the spacecraft in flight software. Figure out interact with the the ground and space software to unlock the flag.

## Notes ##


This challenge is requires participants to learn about the NASA JPL F-Prime (F') spacecraft flight software framework. [F-Prime Github](https://github.com/nasa/fprime). The participant needs to evaluate the ground system webpage hosted by the challenge container [GDS-WEB](http://localhost:5000) to figure out how to exploit the system and get the passcode required to retrieve the flag. 