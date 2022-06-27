#!/usr/bin/env python3

import json
import os
import sys

from bitstring import BitArray
from math import log2

# Local Imports
from libs.timeout import timeout, TimeoutError, MINUTE
from libs.levels import Easy, Medium, Hard

# Generic Challenge enviroment variables
FLAG = os.getenv("FLAG", "flag{flip_this}")
TO = int(os.getenv("TIMEOUT", 5 * MINUTE))

# Challenge Variables
BIT_SIZE = 16
MAX_NUM = 2**BIT_SIZE-1


# Print properly in docker/socket env
def p(s, end="\n", flush=True):
    sys.stdout.write(f"{s}{end}")
    if flush: sys.stdout.flush()

def challenge(lvl):
    guesses = 0
    num_guesses = lvl.num_guesses

    p(f"Round {lvl.level}. {num_guesses} guesses. FIGHT.")

    while guesses < num_guesses:
        p("Guess: ", end="")

        line = sys.stdin.readline()
        line = line.replace("\n","")

        try:
            guess = int(line)
            if guess < 0:
                raise ValueError("Negative val")
            elif guess > MAX_NUM:
                raise ValueError("Too large")
            
            guess = BitArray(uint=guess, length=BIT_SIZE)
        except ValueError as e:
            p(f"Invalid number: {e}")
            guesses+=1
            continue
        
        if lvl.rotate_and_xor(guess):
            return True
        
        guesses += 1
    
    return False

@timeout(TO)
def main():
    # TODO: Add file checks for lookup.json
    with open("lookup.json", "r") as f:
        lookup = json.load(f)
    
    easy   = Easy(BIT_SIZE, lookup)
    medium = Medium(BIT_SIZE, lookup)
    hard   = Hard(BIT_SIZE, lookup)

    if challenge(easy) and challenge(medium) and challenge(hard):
        p(f"Got em: Flag: {FLAG}")
    else:
        p(f"Maybe next time?")
        exit(1)

if __name__ == "__main__":
    sys.stdin.flush()

    try:
        main()
    except TimeoutError:
        p("\nTimeout, Bye")
        sys.exit(1)