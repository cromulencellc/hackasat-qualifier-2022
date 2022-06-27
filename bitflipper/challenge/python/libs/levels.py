#!/usr/bin/env python3

import random
import secrets
import sys

from bitstring import BitArray

# Print properly in docker/socket env
def p(s, end="\n", flush=True):
    sys.stdout.write(f"{s}{end}")
    if flush: sys.stdout.flush()

class Easy():
    def __init__(self, bit_size, lookup):
        if bit_size < 4:
            p("Bit size not valid... Bailing out")
            exit(-1)
        
        self.level = 1
        self.num_guesses = 1000

        self.lookup = lookup
        self.bit_size = bit_size
        self.num = self.get_random_num(bit_size)

        self.rotate_amount = random.randrange(1,self.bit_size)

    def get_random_num(self, bit_size):
        d = [idx for idx,num in enumerate(self.lookup) if num == self.bit_size]
        
        print(len(d), len(self.lookup))

        return BitArray(uint=random.choice(d), length=self.bit_size)

    def rotate_num(self, guess):
        guess.rol(self.rotate_amount)

    def xor(self, guess):
        self.num = self.num ^ guess

    def rotate_and_xor(self, guess):
        self.rotate_num(guess)
        self.xor(guess)

        return self.num.int == 0

class Medium():
    def __init__(self, bit_size, lookup):
        if bit_size < 4:
            p("Bit size not valid... Bailing out")
            exit(-1)

        self.level = 2
        self.num_guesses = 1000

        self.lookup = lookup
        self.bit_size = bit_size
        self.num = self.get_random_num(bit_size)

        self.rotate_amount = 0

    def get_random_num(self, bit_size):
        d = [idx for idx,num in enumerate(self.lookup) if num == self.bit_size]

        return BitArray(uint=random.choice(d), length=self.bit_size)
    
    def rotate_num(self, guess):
        self.rotate_amount = random.randrange(0,self.bit_size)
        guess.rol(self.rotate_amount)

    def xor(self, guess):
        self.num = self.num ^ guess

    def rotate_and_xor(self, guess):
        self.rotate_num(guess)
        self.xor(guess)

        return self.num.int == 0

class Hard():
    MAX_NUM = 0
    def __init__(self, bit_size, lookup):
        if bit_size < 4:
            p("Bit size not valid... Bailing out")
            exit(-1)

        self.level = 3
        self.num_guesses = 1000

        self.lookup = lookup
        self.bit_size = bit_size
        self.num = self.get_random_num(bit_size)

        self.rotate_amount = 0

        Hard.MAX_NUM = 2**bit_size-1

    def get_random_num(self, bit_size):
        d = [idx for idx,num in enumerate(self.lookup) if num == self.bit_size]

        return BitArray(uint=random.choice(d), length=self.bit_size)

    def rotate_and_xor(self, guess):
        num = self.num
        rotations = []

        largest_rotation = 0

        for _ in range(self.bit_size):
            guess.rol(1)

            poss = guess ^ num
            tmp = self.lookup[poss.int]

            if largest_rotation < tmp:
                largest_rotation = tmp
                rotations = [poss]
            elif largest_rotation == tmp:
                rotations.append(poss)
        
        self.num = random.choice(rotations)
        
        return self.num.int == 0
